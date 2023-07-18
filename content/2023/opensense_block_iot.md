Title: Block IOT Network Outbound on OpnSense
Date: 2023-07-05 12:00
Category: OPNsense
Tags: opnsense
Authors: Andrew Kail

I have recently set up an IOT VLAN on my OPNsense router to move some devices to. How to block
the outbound took a little work to figure out but finally found the rule settings to get it working.

In my example below I'll be blocking all outbound network traffic on the IOT Vlan except to a single
host I expect the devices to talk to.  

The difficult part for me to wrap my brain around was blocking "inbound" traffic to the interface.  Once I understood
I would be blocking IOT "network" traffic to the interface it was relatively easy to finish setting up.

Relevant rule settings:

| Setting | Value |
| --- | --- |
| Action | Reject |
| Quick | True | 
| Interface | IOT | 
| Direction | in | 
| TCP/IP Version| IPv4 | 
| Protocol | any | 
|  Source | IOT net | 
|  Destination Invert | True | 
| Destination | Single host or Network | 
| Destination IP | 192.168.1.100  | 


![Example Rule]({static}/images/2023/opnsense-iot-fw/opnsense-iot-fw-1.png)

Once the rule is created be sure to apply the changes.

Now all devices on the IOT network will only be able to access the ip address defined above.  This was just the first step
in getting my IOT network up and will need to open up to other things I'm sure but its a start.

## Notes

* TCP/IP Version will be limited to IPv4 if you Destination IP is IPv4.

## Versions

| Software | Version |
| --- | --- |
| OPNsense | 23.1.9 |
