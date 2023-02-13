Title: Pre-Patch Checklist for HPC Cluster Using Ansible
Date: 2101-01-01 12:00
Category: HPC
Tags: hpc,patching,ansible
Authors: Andrew Kail

Draft page

* Update repositories
* Verify we can get updates
* check for a kernel updates
* # yum updateinfo list security all
# yum updateinfo list sec
* Check for package updates
* 
* Apply all security updates
    * yum -y update --security

    
yum list installed | awk '{print $1";"$2";"$3}' > /home/list_installed.csv
yum list available | awk '{print $1";"$2";"$3}' > /home/list_available.csv
yum check-update | awk '{print $1";"$2";"$3}' > /home/check_update.csv

## References

* [https://access.redhat.com/solutions/10021](Redhat Yum Security)
