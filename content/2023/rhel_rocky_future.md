Title: The Impact of RHEL Changes on an HPC MSP
Date: 2023-06-27 12:00
Category: HPC
Tags: hpc,linux
Authors: Andrew Kail

Its been nearly a week now and after having stewed on it I think its time to speak my piece on this debacle.

The recent changes to how Red Hat Enterprise Linux (RHEL) distributes their
source code has caused quite a stir in the Linux and HPC community.  

While I can't fault RedHat/IBM for the business decision they have made, it does
leave us in a bit of a pickle with regard to the support we provide long term.

## What Happened

This feels like beating a dead horse really, so I'll just leave a few links on the situation:

* [The initial announcement](https://www.redhat.com/en/blog/furthering-evolution-centos-stream)
* [The RedHat response to Cricism](https://www.redhat.com/en/blog/red-hats-commitment-open-source-response-gitcentosorg-changes)
* Rocky Linux [1](https://rockylinux.org/news/2023-06-22-press-release/) [2](https://rockylinux.org/news/brave-new-world-path-forward/)
* [Alma Linux](https://almalinux.org/blog/impact-of-rhel-changes/)
* [Software Freedom Conservancy](https://sfconservancy.org/blog/2023/jun/23/rhel-gpl-analysis/)
* Jeff Geerling [1](https://www.jeffgeerling.com/blog/2023/dear-red-hat-are-you-dumb) [2](https://www.jeffgeerling.com/blog/2023/removing-official-support-red-hat-enterprise-linux) [3](https://www.jeffgeerling.com/blog/2023/im-done-red-hat-enterprise-linux)

**tldr** - RedHad sees no value in allowing rebuilds, so they're closing it off.


## How This Impacts Us

At the moment it doesn't thanks to the engineering teams at CIQ stepping up to provide continued updates which we are extremelly grateful for.  We are currently in the process of migrating customers from CentOS 7 clusters to Rocky 8 or 9 depending on the environment, with plans to migrate several more over the course of the year. This, of course, excludes the several we have that are running RHEL which will not be impacted at all by the change.

The big question is how long can CIQ keep these updates going? Or how long can Alma maintain cherry picking updates out of CentOS Stream? Once RedHat realizes they didn't kill off the derivative rebuilds will they pursue other legal or more drastic actions?  Going a step further, what about other open source projects from RedHat?  Looking at you Ansible, Podman, etc.

And what will IBM be doing for their products running on RHEL and OpenShift?  I'm worried about IBM Storage Scale (GPFS) only support clients on RHEL.

The bigger blow for our engineering or is Jeff Geerling dropping support for Enterprise Linux with his ansible roles,
which are used heavily for some of our deployments.  Who will follow in dropping support?  We've already seen some application developers, namely GROMACS, state they will only officially support container stacks.

Then, for so many of our clients, they can't absorb the licensing costs for the number of licenses they need.  Many are smaller clients on a budget and a huge increase in license costs will reduce the value they can provide to their users.  

## What next

We honestly don't know what the future holds for us in our space.  Most of our clients are on CentOS, Rocky, or RHEL spanning multiple versions.  Most of our storage stack are supported only on Enterprise Linux or heavily favor it.  If Rocky or Alma eventually go away we'll have to make some decisions on those clients.

In the meantime, we'll be prioritizing containerization of user applications via Singularity, Shifter, or CharlieCloud (Upcoming Article on this), as well as experiment with containerization of our supporting infrastructure.  While some pieces like the majority of the monitoring stack are easy to containerize, I am even looking at moving tools like Warewulf to a container which should be interesting.

Our other option is to migrate some of our customer base to OpenSuse Leap and offer paid support if they need it. Leap is the CentOS/Rocky equiavalent of Suse Enterprise Linux (SLES) and is maintained directly by Suse.  We've met with their team in the past and have dedicated resources and packages for HPC environments.  I think this is their opportunity to step into the HPC space for many institutions and I really hope they don't miss it.  I'll be exploring openSuseLeap and warewulf in the coming weeks with some blog posts I hope.

## Conclusion

This announcement hit me right before bed unfortunately what followed was not a good night's sleep as I wrestled with the implications.

We'll be fine for now and we have some work to do to support our customers in the long term. 

Also, what they have done doesn't appear to be illegal nor violate the GPL license. Time will tell, but I'm starting to see some bleedover of Big Blue into RedHat more and more and have deep concerns about how we can support our clients long term. I hope I'm wrong.
