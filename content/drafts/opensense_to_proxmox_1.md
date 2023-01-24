Title: Migrating OPNSense to Proxmox Part 1
Date: 2101-01-01 12:00
Category: Homelab
Tags: opnsense
Authors: Andrew Kail
Series: OPNSense to VM

Recently I moved back to Tennessee and have begun the process of getting the house wired up
with ethernet and new wifi Access Points.

Prior to the move, I was running a somewhat complicated setup with several points of failure, running
OPNSense as my firewall on a Qotom Mini PC, a Unifi POE switch, 3 Unifi APs, and a Proxmox hypervisor running Pi-Hole and the Unifi Controller.  

In the process of packing, I managed to move DNS, Ad-blocking, and the Unifi Controller to OPNsense which allowed me to shut down my server so I could pack it up.  I was
impressed that I found a plugin to handle the Unifi Controller available for OPNsense and didn't have any issues migrating the controller over.  During the weeks leading up
to the move everything ran without issue so I was pretty happy with the setup. I was looking forward to wiring the new house up a bit differently
and had some good ideas of what I wanted to do.

After arriving in Tennessee I was pleased that I was able to plug in a lot of my hardware and everything just WORKED.  Well,
everything worked until I updated OPNSense and tried to log into the Unifi Controller.  The controller was hosed.  After perusing the github [issues](https://github.com/mimugmail/opn-repo/issues/96)
for the plugin it appeared that the plugin build and OPNSense install could get a little out of sync sometimes and wreck MongoDB after an update.
Luckily the one AP I was running was still properly configured and functioning without the controller so I was able to continue on till I either
restored the controller or came up with a different solution. 

I had plans though to change out some hardware and have decided to move OPNSense to a VM on the same hardware and then run a container or VM with the controller. I wanted 
the heart of my networking stack to be on one device and easy to manage with backups and support containers.  This will also allow me to ditch a few of the unofficial plugins
and move pihole and Unifi to another VM on the same host.

I decided to go with Proxmox as that is what I have become familiar with in my homelab setup, running it on my main server and now my [Homeassistant](https://home-assistant.io)
device as well.  Its been easy to work with and started to become very popular in the self-hosting community.

## Planning The Install

I had to think out this install and do my research before

Planning this out was not easy as I will lose my network in the process.

A few things to keep in mind before starting:

* Device passthrough will not allow snapshots[ref][Snapshot blocked by pci-e device](https://forum.proxmox.com/threads/snapshot-blocked-by-pci-e-device.53790/)[/ref]

I decided to go ahead with enabling PCI passthrough even though I will lose snapshots as it
will make setting up the WAN and lan congifigurations


Plan

1. Run a backup of OPNSense
2. Upgrade the RAM
3. Download latest copy of Proxmox
4. Write Proxmox ISO to a thumb drive
5. Run installer on Qotom Mini PC with a head on
6. Direct connect to Port 0 on the qotom device
7. Import the congifiguration
8. Label Ports!


Big thanks to his [ServeTheHome](https://www.youtube.com/watch?v=IJhlqb4iGn4) Video which really helped me solidify how I should manage this


Port layout thanks to ServeTheHome

![ServeTheHome Ports]({static}/images/pve-qotom-ports.png)


But... We know how the best laid plans go...

## Reference
* https://www.servethehome.com/how-to-pass-through-pcie-nics-with-proxmox-ve-on-intel-and-amd/

![Alt Text]({static}/images/gifs/mike-tyson-smile.gif)


