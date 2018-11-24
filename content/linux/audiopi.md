Title: Whole Home Audio With A Raspberry Pi
Date: 2018-05-13 00:00
Tags:  raspberry pi, raspbian, linux, automation

The hardware. 

Need an image of it


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

# Configuring wireless

Should be able to do this before I fire up the pi

edit /etc/wpa_supplicant/wpa_supplicant.conf and add a configuration for the network

Add the following to the file

    network={
        ssid="MyWirelessnetwork"
        psk="igotasecret"
    }

and add this to /etc/dhcpcd.conf if you want a static ip address set for the new interface

    interface wlan0
    static ip_address=192.168.2.201/24
    static routers=192.168.2.1
    static domain_name_servers=192.168.2.1


# Install snapcast

What is snapcast?  Well, glad you asked

install client and server using wget,dpkg and 

    sudo apt-get -f install

to fix any issues with dependencies

Configuration for server at /etc/defaults/snapserver
   
    SNAPSERVER_OPTS="-d -s pipe:///tmp/snapfifo?name=Radio&mode=read"

be sure to restart the server


to fix and issue with where the audio is going

    amixer cset numid=3 1

# Install Shairport

	apt-get install shairport-sync

configure

	general =
	{
		name = "Front Room";
		password = "secret";
		interpolation = "soxr";
	};

# Turn on and configure bluetooth

the a2dp needs to run with sudo privileges

maybe add pi user to bluetooth group?

	adduser pi bluetooth




# Testing

connect an iphone and it should work!
it did for me after all

# Reference

https://www.makeuseof.com/tag/setup-wi-fi-bluetooth-raspberry-pi-3/
https://gist.github.com/mill1000/74c7473ee3b4a5b13f6325e9994ff84c
shairport-sync github page
snapcast page
https://github.com/badaix/snapcast/blob/master/doc/player_setup.md#alsa
https://github.com/raspberrypi/linux/issues/1402
https://github.com/badaix/snapcast/issues/379
https://github.com/BaReinhard/Super-Simple-Raspberry-Pi-Audio-Receiver-Install
