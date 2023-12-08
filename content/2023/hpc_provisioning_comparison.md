Title: Comparison of Provisioning/Cluster Managers in HPC
Date: 2023-12-08 00:00
Category: HPC
Tags: hpc,linux,provisioning
Authors: Andrew Kail

We are primarily a ~~Bright Cluster Manager~~ Base Command Manager (BCM) 
shop and recently some
uncertainty has arisen around the future of BCM after its purchase by Nvidia last year.
More specifically how 
pricing will be handled and whether BCM will only be available with Nvidia
superpods and DGX systems in the long term. 

As an HPC Managed Services Provider, we seek to leverage solutions that allow
us to quickly deploy and easily manage compute clusters. For our business operations, BCM 
has served us well in both the features it provides and the support from Nvidia.  Currently, all but
one HPC Cluster we manage runs BCM. 

Our lone outlier is a unique test case were we needed to manage both Linux
and Windows nodes in the same environment, so we instead went with another
provisioning software (Cobbler)[https://cobbler.github.io/] which had the ability
to support a Windows node.  We quickly however
realized there were many features missing we needed to fill via other means and the
Windows support proved more difficult that we like.

In this article, I'll take a look at what the options are in the HPC space and
review the features needed in an a standalone deployment.  My goal in writing this is to 
understand the gaps in the solutions so our team, clients, and you, know
which ones need to be filled.

## Provisioner vs Cluster Manager

First, I want to be clear about what is being compared here.  These tools will fall
into two categories, with one being a subset of the other.

All of the software compared here will provide some form of provisioning. Provisioners
typically use some form of network booting combined with PXE and a TFTP server to handle installing and configuring an operating system to either baremetal hardware or a VM.  This has become the standard method for provisioning in both HPC and enterprise environments.

The subcategory is cluster management software. A cluster managers are more specific to the HPC and parallel computing space. A cluster manager different from generic provisioning software in that it will typically run an agent on each node to manage and configure services for HPC.


## The software

I'll be comparing the following software stacks.  This is not an exhaustive list of available software and I have decided to focus on what is either well supported, well known, or niche to this industry.

### Provisioning Software

**[Cobbler](https://cobbler.github.io/)**

Cobbler is a provisioning software stack written in Python primarly geared towards
Linux network installations.  Its a very light install and leverages template and kickstart scripts for initial system configuration.

**[The Foreman](https://theforeman.org/)**

Foreman is a complete lifecycle management tool for physical and virtual servers.
More than just a provisioner, it can also handle security update management,
configuraiton management, and monitoring. Even with its rich feature set I am leaving it
out of the Cluster Managers list as it is not geared towards HPC Clusters.

### Cluster Managers

**[Base Command Manager](https://www.nvidia.com/en-us/ai-data-science/products/base-command-manager-essentials/)**

Our story's main character.  Base Command Manager is a proprietary turn-key
application for installaing, configuring and managing and HPC cluster with
all the batteries included.

**[Warewulf](https://warewulf.org/)**

Warewulf is fast becoming one of the big players in the HPC Cluster management space.  It's the primary manager for the [OpenHPC Project](https://openhpc.community/), is open source with the option for enterprise support.

**[Grendel](https://grendel.readthedocs.io)**

Grendel is a cluster manager out of the University at Buffalo Center for Computational Research where it is used to manage their hpc resources.

**[Scyld Clusterware](https://www.penguinsolutions.com/computing/products/software/scyld-clusterware/)**

Scyld is a proprietary cluster management product from Penguin Solutions.  Development is based on the
beo

**[xCAT](https://xcat-docs.readthedocs.io/en/stable/)**

I well known management stack, xCAT is unfortunately no longer in development by IBM, but there is an attempt by the Open Source
Community to revive it.  However, I wanted to leave it in this list
as it is very well known and feature rich, albeit difficult to install and manage.

Recently I did discover xCAT development has been continued by Lenovo under the name Confluent, albeit not
out in the open.  It can be found at [hpc.lenovo.com](https://hpc.lenovo.com).  

**[OpenHPC](https://openhpc.community/)**

OpenHPC is a community effort to provide common HPC components which can be mixed and matched to build an cluster.  OpenHPC itself builds on top of Warewulf's
provisioning and provides other tools and libraries such as Infiniband, Lustre, and other scientific applications.


## Features

* DHCP
* TFTP
* NTP
* IPMI configuration (During provisioning)
* Power control
* DNS
* Stateless provisioning
* Statefull provisioning
* Infiniband Driver
* Nvidia Drivers
* License
* Windows Provisioning
* User Management
* Firewall NAT Configuration
* Service Management (i.e. Systemd services)
* Image Management
* NFS Server
* Kernel Management
* Support Contract
* Slurm Management

For many of these features, we are looking at what is provided by the provisioning software itself, not from the OS or
other related tools like Puppet, Chef, etc.  For example, The Foreman can tightly integrate with Puppet, but requires
more setup on the admin side to handle some of the features above.

## Comparison

| Feature                    | Cobbler | The Foreman | BCM         | Warewulf | Grendel | Scyld       | xCAT | OpenHPC |
| -------                    | ------- | ----------- | ---         | -------- | ------- | -----       | ---- | ------- |
| DHCP                       | Yes     | Yes         | Yes         | Yes      | Yes     | Yes         | Yes  | Yes     |
| TFTP                       | Yes     | Yes         | Yes         | Yes      | Yes     | Yes         | Yes  | Yes     |
| NTP                        | No      | No          | Yes         | No       | Yes     | Yes         | Yes  | No      |
| IMPI Configuration         | No      | No          | Yes         | No       | No      | No          | No   | No      |
| Power Management           | Yes     | Yes         | Yes         | Yes      | Yes     | Yes         | Yes  | Yes     |
| DNS                        | No      | Yes         | Yes         | Yes      | Yes     | Yes         | Yes  | Yes     |
| Stateless provisioning     | No      | No          | Yes         | Yes      | Yes     | Yes         | Yes  | Yes     |
| Statefull provisioning     | Yes     | Yes         | Yes         | No       | Yes     | Yes         | Yes  | Yes     |
| Infiniband Drivers         | No      | No          | Yes         | No       | No      | Yes         | Yes  | Yes     |
| Nvidia Drivers             | No      | No          | Yes         | No       | No      | Yes         | Yes  | No      |
| License                    | FOSS    | FOSS        | Proprietary | FOSS     | FOSS    | Proprietary | FOSS | FOSS    |
| Windows Provisioning       | Maybe   | Yes         | No          | No       | No      | No          | Yes  | No      |
| User Management            | No      | No          | Yes         | No       | No      | No          | No   | No      |
| Firewall NAT Configuration | No      | No          | Yes         | No       | No      | Yes         | No   | No      |
| Service Management         | No      | No          | Yes         | Yes      | No      | No          | No   | Yes     |
| Image Management           | No      | No          | Yes         | Yes      | No      | Yes         | Yes  | Yes     |
| NFS Server                 | No      | No          | Yes         | Yes      | No      | No          | No   | Yes     |
| Kernel Management          | No      | No          | Yes         | Yes      | No      | Yes         | Yes  | Yes     |
| Support Contract           | No      | No          | Yes         | Yes      | No      | Yes         | No   | Yes     |
| Slurm Management           | No      | No          | Yes         | No       | No      | Yes         | No   | Yes     |


## Final Thoughts

Its likely I missed some things and I will continue to update the comparison as time goes on or as people possibly yell at me.

In the end, we have decided to plan migrations to OpenHPC as it covers the majority of what we need, has a robust community,
provided timely security updates, and will likely reduce costs for our customers. 

