Title: Running Netboot.xyz From OPNSense
Date: 2023-03-29 01:00
Category: OPNSense
Tags: opnsense,netboot
Authors: Andrew Kail

After working with some PXE booting at work recently, I decided to pick up a
long standing todo of installing netboot.xyz on my network.  When I started to
take a deeper look into it I realized I could probably install it on my OPNSense
VM as it is the DHCP server and comes with a TFTP plugin.

## Install TFTP

The first thing we need to do is install the TFTP plugin.  One note about this
plugin is that it is no longer maintained so there is a possibility it may go
away in the future.  Hopefully that is not the case.

Navigate to `System > Firmware > Plugins` and search for `os-tftp`, then click
the `+` button to install the plugin.

![Install TFTP Plugin]({static}/images/2023/opnsense-pxe/opnsense-pxe-1.png)


Once we have the plugin installed we'll need to create the tftp directory and
install netboot before enabling the service.  Otherwise it will fail. This step
requires ssh access.

```
ssh root@opnsense

# Select '8' at the menu to enter the shell

mkdir /usr/local/tftp
cd /usr/local/tftp

# Download netboot files
fetch https://boot.netboot.xyz/ipxe/netboot.xyz.kpxe
fetch https://boot.netboot.xyz/ipxe/netboot.xyz.efi
fetch https://boot.netboot.xyz/ipxe/netboot.xyz-arm64.efi
```

I downloaded three files above to support the main types of network booting I
expect on my home network.  Namely Bios, EFI, and ARM EFI.  If you feel you need
to use a different bootloader you'll want to read the netboot documenation for
that.

Now we can enable the service, making sure to set the "Listen Address" to the ip
we expect to boot from. 

![Enalbe TFTP]({static}/images/2023/opnsense-pxe/opnsense-pxe-2.png)

Click save and make sure the TFTP service has properly started.  You should see
a green play button in the top right indicating the service is running.

## Configure DHCP

Now we need to enable the dhcp server to allow network booting.

Navigate to `Services > DHCPv4 > [Name of you boot network]`.  Making sure to
select the network you wish to boot from.  In my case, its my Internal network.

![Configure Network Booting]({static}/images/2023/opnsense-pxe/opnsense-pxe-3.png){: width="300" class="center-img" }

Scroll down till you see  `Network Booting` and click the `Advanced` button to
show all the full settings.

![Advanced Settings]({static}/images/2023/opnsense-pxe/opnsense-pxe-4.png)

Fill out the form with the IP Address we configured for the TFTP service.  For
the filenames, you can do the following:

| Setting               | Filename              |
| -------               | --------              |
| bios                  | netboot.xyz.kpxe      |
| x86 UEFI (32-bit)     | netboot.xyz.efi       |
| x86 UEFI (64-bit)     | netboot.xyz.efi       |
| ARM x86 UEFI (32-bit) | netboot.xyz-arm64.efi |
| ARM x86 UEFI (64-bit) | netboot.xyz-arm64.efi |


![Boot Filenames]({static}/images/2023/opnsense-pxe/opnsense-pxe-5.png)

Scrool down to click save and the DHCP service should restart.  Now when you do
network booting with a system on the network it will bring up a slick menu to
boot your favorite distribution.

## References

- [Netboot.xyz](https://netboot.xyz/docs/booting/tftp)
- [Reddit
Thread](https://www.reddit.com/r/OPNsenseFirewall/comments/zx86ve/how_to_configure_opnsense_for_netbootxyz/)
