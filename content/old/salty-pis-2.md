Title: Salty Pis Part 2
Date: 2018-06-22 00:00
Tags:  raspberry pi, salt


# Installing Salt

Installing Salt on a Raspberry Pi is pretty straightforward since there are up to date packages in the raspbian repositories.  For more details on installing Saltstack on any other platforms, please see the document [here](https://repo.saltstack.com/).

    :::bash
    sudo apt-get install salt-minion salt-master


Add the hostname 'salt' to the `hosts` file so that it points to the salt-master.

    :::bash
    echo "192.168.1.100 salt" >> /etc/hosts


Restart the minion so that it connects to itself as the master

    :::bash
    service salt-minion restart

# Master Key

list the keys

    :::bash
    salt-key -L

    salt-key -a pi-blue-01
    salt-key -A

# SLS files
Creating an sls files


Etc /etc/salt/master on the master

add /srv/salt as base directory

Create a basic top.sls
create vim.sls

    salt '*' state apply

# Basic Hardening
Now any new pi's I add to my home network will automatically become hardened once they are connected to the master.

Setting up the SLS files.

# what to do to add nother node
