Title: Some Systemd Root Mount Confusion
Date: 2023-09-14 00:00
Category: Linux
Tags: linux,systemd,bright
Authors: Andrew Kail

I recently ran into an interesting issue with systemd on a Bright Cluster. 

Bright Cluster Manager (BCM) has a tendency to restart the Slurm Daemons when
certain changes are made, such as adding a new partition.  Recently when we did this,
we found the daemon failed to restart on a large chunk of the nodes stating:

    Aug 29 14:11:15 node129 systemd[1]: Dependency failed for Slurm node daemon.
    Aug 29 14:11:15 node129 systemd[1]: Job slurmd.service/start failed with result 'dependency'.

A very confusing message as the system is up and running.  Fine.  Lets see which units have failed.

    [root@node ~]# systemctl list-units --state failed
      UNIT    LOAD   ACTIVE SUB    DESCRIPTION
    ● -.mount loaded failed failed /

Root failed to mount?

:suprised pikachu:

No amount of rebooting an

So, since this is a Brigth cluster, a `node-installer` is initially booted to and the system process are then turned over to the installed image.  Grossly over simplifying the process but that is the gist of it.  

    systemd-analays dot  | dot -Tsvg > plot.svg

While neat, was not helpful as all I could see what maybe `-.mount` depended on system.slic.  Which did start up just fine.


Interestingly enough, I did accidentally find "-.mount" entered a failed state after the node was up.

    :::bash
    [root@node ~]# systemctl list-units --state failed
      UNIT           LOAD   ACTIVE SUB    DESCRIPTION
    ● slurmd.service loaded failed failed Slurm node daemon

    LOAD   = Reflects whether the unit definition was properly loaded.
    ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
    SUB    = The low-level unit activation state, values depend on unit type.

    1 loaded units listed. Pass --all to see loaded but inactive units, too.
    To show all installed unit files use 'systemctl list-unit-files'.
    [root@node ~]# systemctl list-units --state failed
      UNIT           LOAD   ACTIVE SUB    DESCRIPTION
    ● -.mount        loaded failed failed /
    ● slurmd.service loaded failed failed Slurm node daemon

    LOAD   = Reflects whether the unit definition was properly loaded.
    ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
    SUB    = The low-level unit activation state, values depend on unit type.

    2 loaded units listed. Pass --all to see loaded but inactive units, too.
    To show all installed unit files use 'systemctl list-unit-files'.

Not sure if this meant anything, but its here.

    :::console
    [root@node129 ~]# systemctl | grep mount
      proc-sys-fs-binfmt_misc.automount       loaded active     waiting      Arbitrary Executable File Formats File System Automount Point
    ● -.mount                                 loaded failed     failed       /
      data.mount                              loaded active     mounted      /data
      data_lake.mount                         loaded active     mounted      /data_lake
      local.mount                             loaded active     mounted      /local
      tmp.mount                               loaded active     mounted      /tmp
      var-lib-nfs-rpc_pipefs.mount            loaded active     mounted      RPC Pipe File System
      var.mount                               loaded active     mounted      /var
      systemd-remount-fs.service              loaded active     exited       Remount Root and Kernel File Systems


The most frustrating thing is I can't get any information on this mount.  Any other mount service I can query, but I only get invalid option errors.

    :::bash
    [root@node129 ~]# systemctl status -.mount
    systemctl: invalid option -- '.'
    [root@node129 ~]# systemctl status "-.mount"
    systemctl: invalid option -- '.'
    [root@node129 ~]# systemctl status '-.mount'
    systemctl: invalid option -- '.'
    [root@node129 ~]# systemctl status '-\.mount'
    systemctl: invalid option -- '\'
    [root@node129 ~]# systemctl status "-\.mount"
    systemctl: invalid option -- '\'
    [root@node129 ~]# systemctl status "-\\.mount"
    systemctl: invalid option -- '\'
    [root@node129 ~]# systemctl status "-/\.mount"
    systemctl: invalid option -- '/'
    [root@node129 ~]# systemctl status "\-.mount"
    Unit \-.mount could not be found.
    [root@node129 ~]# systemctl status "-.mount"
    systemctl: invalid option -- '.'


While I can see the full dependency tree, it tells me nothing that is blocking "-.mount"

    ● │ │ ├─local-fs.target
    ● │ │ │ ├─-.mount
    ● │ │ │ ├─local.mount

Just looking at its parent, I only see one dependency

    [root@node129 ~]# systemctl list-dependencies local-fs.target
    local-fs.target
    ● ├─-.mount
    ● ├─local.mount
    ● ├─rhel-readonly.service
    ● ├─systemd-fsck-root.service
    ● ├─systemd-remount-fs.service
    ● ├─tmp.mount
    ● └─var.mount


So time to look elsewhere...

One of the more confusing items is mount and lsblk disagreeing.  The mount command shows `/` mounted, but lsblk does not.

    [root@node129 ~]# lsblk
    NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    nvme0n1     259:1    0  1.8T  0 disk
    ├─nvme0n1p1 259:4    0   40G  0 part
    ├─nvme0n1p2 259:5    0   20G  0 part /var
    ├─nvme0n1p3 259:6    0   20G  0 part /tmp
    ├─nvme0n1p4 259:7    0   12G  0 part [SWAP]
    └─nvme0n1p5 259:8    0  1.7T  0 part /local
    [root@node129 ~]# df -h
    Filesystem                                                      Size  Used Avail Use% Mounted on
    devtmpfs                                                        504G     0  504G   0% /dev
    tmpfs                                                           504G  3.2M  504G   1% /run
    /dev/nvme0n1p1                                                   40G   19G   22G  46% /
    tmpfs                                                           504G     0  504G   0% /dev/shm
    tmpfs                                                           504G     0  504G   0% /sys/fs/cgroup
    /dev/nvme0n1p3                                                   20G   33M   20G   1% /tmp
    /dev/nvme0n1p2                                                   20G  4.6G   16G  23% /var
    /dev/nvme0n1p5                                                  1.7T   33M  1.7T   1% /local


Next I tried doing an update, which did include some updates to the kernel and systemd but alas the issue persisted.

After pulling my hair out for a few days my only option was to take a known good image from another node class
and rebuild our image.  In the end, this worked but has still left puzzled as to what actually happened here.

If anyone has experienced this before on BCM or other cluster management software please reach out and let me
know what you found or possibly did to resolve it.
