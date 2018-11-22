Title: Salty Pi Part 1
Date: 2018-05-13 00:00
Tags:  raspberry pi, saltstack, raspbian, linux


[Saltstack](https://saltstack.com) is a remote execution engine and configuration management system built on top of Python and is very similar to tools like Puppet, Chef and Ansible.  I was first exposed to Salt when attending the Supercomputing conference in 2014 in New Orleans.  Since then I have started to make use of Salt at work and have started to expand my usage to a small [homelab](https://reddit.com/r/homelab).  In the future I may take a look at some of these other configuration management tools, especially the ones that are built on Python like [Ansible](http://ansible.com).  My plan is to mess with Salt and some of its features at home in the hope I can translate some of this knowledge to work. It will help with setting up my home automation system and other projects I plan to do in the future.

In this first post we will install raspbian on a Raspberry Pi 3 and perform some basic configuration.  A future posts will cover setting up and configuring Salt on the Pi.

# Installing Raspbian

First thing to do is download and install the image from the Raspbian [Download Page](https://www.raspberrypi.org/downloads/raspbian/).  At the time of this writing Debian Stretch is the current version and for our purposes lets use the Lite version since this Pi's will be headless. Once downloaded we can verify the zip file by generating the sha256 check sum and then extract our image. Please take a moment to compare the hash generated here matches the has on the download page.  If it is wrong you should re-download the image.

    :::bash
    $ sha256sum 2017-11-29-raspbian-stretch-lite.img 
    e942b70072f2e83c446b9de6f202eb8f9692c06e7d92c343361340cc016e0c9f 2017-11-29-raspbian-stretch-lite.zip

    $ unzip 2017-11-29-raspbian-stretch-lite.zip
    Archive:  2017-11-29-raspbian-stretch-lite.zip
      inflating: 2017-11-29-raspbian-stretch-lite.img  


Now copy the image to the SD card.  I prefer to use the `dd` command as it doesn't require any dependencies and works pretty effeciently.  Just please make sure the `of` option is pointing to the correct mount point as you do not want to overwrite an existing file system.  Most of the time an SD card will show up under `/dev/mm*`, although in my case (running Manjaro) it showed up as `/dev/sdb`.

    :::bash
    $ sudo dd bs=4M if=2017-11-29-raspbian-stretch-lite.img of=/dev/sdb

Once the image has been written a few edits need to be made to the image since ssh is not enabled by default. To enable the ssh server, create an empty file in the boot partition of the SD card which will enable the ssh server on boot. Just remount the SD card (may require a reboot) and look for the boot partition, which should be seperate from the root install, and create an empty file `ssh`. For example:

    :::bash
    $ sudo cd <somedirectory>/boot
    $ sudo touch ssh

Now its time to get the Pi up and running and do a few more tweaks.  Pop the SD card into the Pi and power it up.

# Getting Raspbian Ready

With our Pi up and running, and connected to the network by ethernet, we will need to ssh into it. Before we can, we need to find out where it resides on the network. If you have the `nmap` tool installed you can use it to scan your subnet for any devices.  For example if my subnet is 192.168.1.0, we can use the following to scan for all local devices.

    :::bash
    $ sudo nmap -sP 192.168.1.0/24
        Host is up (0.099s latency).
        MAC Address: A1:A2:A2:A2:A2:A2 (RASPBERRY PI FOUNDATION)
        Nmap scan report for 192.168.1.10


Once we have found where the Pi is on the network lets go ahead and ssh into it. Remember the default username is `pi` and the default password is `raspberry`.

    :::bash
    $ ssh pi@192.168.1.10

Lets Change the password before we go any further.

    :::bash
    password 

And lets update the system, set the hostname, give it a static ip address and restart.

    :::bash
    $ sudo su - # go to root
    $ apt-get update && apt-get upgrade
    $ echo "pi-blue-01" > /etc/hostname

To set a static ip address we need to edit `/etc/dhcpcd.conf` for the interface.  

    interface eth0
    static ip_address=192.168.1.100/24
    static routers=192.168.1.1
    static domain_name_servers=192.168.1.1


Now restart to make these changes take effect

    :::bash
    # while root
    $ reboot

In the next article we will get Salt installed and configured.
