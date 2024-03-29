Title: Exploding Sparse Files on Linux
Date: 2101-01-01 12:00
Category: Linux
Tags: linux
Authors: Andrew Kail

## Symtoms

    ╭─akail@bluefalcon /var/log
    ╰─➤  ls -alh lastlog                                                                                                                                                                                         130 ↵
    -rw-rw-r-- 1 root utmp 287K Jan  1 18:28 lastlog


    ╭─akail@bluefalcon /var/log
    ╰─➤  find /var/log -type f -printf "%S\t%p\n" | gawk '$1 < 1.0 {print}'
    0.0279709       /var/log/lastlog


    ╭─akail@bluefalcon /var/log
    ╰─➤  du -sh lastlog                                                                                                                                                                                            1 ↵
    8.0K    lastlog


    ╭─akail@bluefalcon /var/log
    ╰─➤  python -c "print(8/287)"


What is a sparse file?

df reports the amount of allocated and unallocated space of the file system.

Allocated space for a file isn't always the same as the files size.

## Lastlog

What is the last log file?  The lastlog file at `/var/log/lastlog` is generated by the pam_lastlog
module to record user logins.  It is a sparse database which can be queried using the `lastlog` command.

For Example:

    :::bash
    lastlog -u akail

    Username         Port     From                                       Latest
    akail            pts/14   192.168.1.24                              Tue Jan  3 09:33:38 -0500 2023

## Explosion

We recently

find /var -size +1G
find /var/log -type f -printf "%S\t%p\n" | gawk '$1 < 1.0 {print}'

So, why is this file so large on some systems and small on other systems?

cat /etc/login.defs | gerp LASTLOG_UID_MAX

Many times, it unset

## Remediation

Reboot the node is a possibility

run lsof on the file to determine what services are writing to it?

We don't want to remove it as it could possibly break authentication with pam

Increase the size of /var
Remove from AD, which is usually the culprint
Possibly set th


## References

* [Arch Linux Wiki](https://wiki.archlinux.org/title/sparse_file)
