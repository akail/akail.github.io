Title: PXE Booting on Proxmox
Date: 2023-04-05 01:00
Category: Proxmox
Tags: proxmox,netboot
Authors: Andrew Kail

In last's week post I [installed netboot.xyz on an OPNSense firewall]({filename}/2023/opnsense_pxe.md). Now its
time to test the PXE boot process on a VM on my Proxmox Host.  Its very
straightforward, but there are a few caveats I found with netboot.

First, start the VM Creation process in Proxmox.  You will use the defaults on
most of the pages, but there are two important menu's you'll need to fill out.

![Create VM]({static}/images/2023/proxmox-pxe/proxmox-pxe-1.png)

The first is in the OS menu.  Instead of selecting an ISO which has been loaded
to the node, you'll want to select `Do no use any media`

![Select Install Media]({static}/images/2023/proxmox-pxe/proxmox-pxe-2.png)

The second caveat is when configuring the RAM.  During testing, I found there is
a minimum amount of RAM you need with PXE booting.  This is due to downloaded
media having to be stored in RAM before starting. Usually happens when running a
live OS like EndeavourOS.  You'll want to configure at least 4 Gigabytes of RAM.

![Select Ram]({static}/images/2023/proxmox-pxe/proxmox-pxe-3.png)

Finish creating the VM and go to the VM's console menu to start the VM.

![Start VM]({static}/images/2023/proxmox-pxe/proxmox-pxe-4.png)

Without any media configured and nothing installed to the virtual disk the VM
will automatically network boot and should pick up netboot.xyz right away.
You'll the be able to select from the menu what you want to boot.

![Netboot]({static}/images/2023/proxmox-pxe/proxmox-pxe-5.png)

I'm really impressed with how easy netboot.xyz was to install and use and I look
forward to using it.




