.. _net_openwrt_hw:

.. include:: ../_include/head.rst

================
OpenWRT Hardware
================


.. include:: ../_include/wip.rst


Intro
#####

OpenWRT can be ran on many devices.

For this to be done, you need to flash the hardware-specific firmware-image on the target device.

----

Firmware
########

These images need are created by the community via `compiling <https://gist.github.com/chankruze/dee8c2ba31c338a60026e14e3383f981>`_ `OpenWRT source-code <https://www.github.com/openwrt/openwrt>`_ for specific hardware.

You can easily find existing images using the `OpenWRT Firmware Selector <https://firmware-selector.openwrt.org/>`_.

You are also able to build your customized images using the `Image Builder <https://openwrt.org/docs/guide-user/additional-software/imagebuilder>`_ with configuration, packages and services pre-installed & -configured.

----

Flash Process
#############

The flashing process is very vendor-specific.

You can search for installation methods in the `OpenWRT Documentation <https://openwrt.org/docs/guide-user/installation/installation_methods/start>`_.

The default IP is: :code:`192.168.1.1`

----

Mikrotik
********

* Download the :code:`squashfs-sysupgrade` and :code:`initramfs-kernel` for your Model - be aware that Pro/Lite/Mesh have different images!

  See: `OpenWRT Firmware Selector - Mikrotik wAP AC (older 1-port model) <https://firmware-selector.openwrt.org/?version=23.05.5&target=ath79%2Fmikrotik&id=mikrotik_routerboard-wap-g-5hact2hnd>`_, `OpenWRT Firmware Selector - Mikrotik wAP AC (newer 2-port model) <https://firmware-selector.openwrt.org/?version=23.05.5&target=ipq40xx%2Fmikrotik&id=mikrotik_wap-ac>`_

* Make sure you have a way of running Mikrotik Winbox or can connect via SSH to the AP.

  See: `Mikrotik Downloads <https://mikrotik.com/software>`_, `Mikrotik Winbox dockerized <https://github.com/obeone/winbox-docker>`_

  Dockerized:

  * Run: :code:`docker run -d --shm-size=512m -p 6901:6901 -e VNC_PW=password obeoneorg/winbox:latest`

  * Access: https://localhost:6901/

    User: :code:`kasm_user`

    Password: :code:`password`

* We recommend to use :code:`dnsmasq`

  Install: :code:`apt install dnsmasq`

  Script to execute (*in the same directory where you have downloaded the image into*)

  .. code-block:: bash

      IFNAME=enp0s31f6  # change to your interface name
      KERNEL_FILE=openwrt-23.05.3-ipq40xx-mikrotik-mikrotik_wap-ac-initramfs-kernel.bin  # change to your file

      /sbin/ip addr replace 192.168.1.10/24 dev $IFNAME
      /sbin/ip link set dev $IFNAME up
      /usr/sbin/dnsmasq --user=$USER \
      --no-daemon \
      --listen-address 192.168.1.10 \
      --bind-interfaces \
      -p0 \
      --dhcp-authoritative \
      --dhcp-range=192.168.1.100,192.168.1.200 \
      --bootp-dynamic \
      --dhcp-boot=$KERNEL_FILE \
      --log-dhcp \
      --enable-tftp \
      --tftp-root=$(pwd)

* Prepare the AP for the flashing

  * Unplug the AP
  * Press the reset button
  * Plug the AP in
  * Let the button go when the green led flashes
  * Connect to the AP default WLAN
  * Connect to the AP via Winbox or SSH

    Default IP is: :code:`192.168.88.1`

  * Configure these system settings:

    * System - RouterBOARD - Settings - Boot Device => :code:`try-ethernet-once-then-nand`

    * System - RouterBOARD - Settings - Boot Protocol => :code:`bootp` (*might differ if you do not use dnsmasq*)

    * System - RouterBOARD - Settings - Force Backup Booter => :code:`yes`

  * Save (OK/OK)
  * System - Shutdown

* Flash the AP

  * Start the dnsmasq script as root
  * Unplug the AP
  * Plug-in the AP
  * Wait for logs to appear on your screen - you need to see: :code:`dnsmasq-tftp: sent <FILE>`
  * Stop the dnsmasq script
  * Wait for the AP to boot to OpenWRT: :code:`ping 192.168.1.1`
  * Connect to AP: :code:`ssh -p22 root@192.168.1.1`
  * Transfer the image: :code:`scp -P22 -O <FILE>-squashfs-sysupgrade.bin root@192.168.1.1:/tmp/sysupgrade.bin`
  * Overwrite the firmware when connected via SSH: :code:`sysupgrade -n /tmp/sysupgrade.bin`

* Wait a few minutes for the upgrade to finish.

----

UniFi AP AC
***********

See: `OpenWRT Documentation Unifi AP AC <https://openwrt.org/toh/ubiquiti/unifiac>`_

* Download the :code:`squashfs-sysupgrade` for your Model - be aware that Pro/Lite/Mesh have different images!

  See: `OpenWRT Firmware Selector - Unifi AP AC Pro <https://firmware-selector.openwrt.org/?version=23.05.5&target=ath79%2Fgeneric&id=ubnt_unifiac-pro>`_

* Make sure you can access the AP via SSH. The default credentials are: :code:`ubnt/ubnt`

  :code:`ssh ubnt@192.168.1.20 -p22 -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostkeyAlgorithms=+ssh-rsa`

  The default unifi-AP IP is :code:`192.168.1.20`

  Restore the AP to defaults: :code:`syswrapper.sh restore-default`

* Transfer the image to the AP:

  :code:`scp -P22 -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostkeyAlgorithms=+ssh-rsa openwrt-23.05.3-ath79-generic-ubnt_unifiac-lite-squashfs-sysupgrade.bin ubnt@192.168.1.20:/tmp/`

* Check the filesystem blocks: :code:`cat /proc/mtd`

* Overwrite the default firmware with the new image:

  .. code-block:: bash

      dd if=/tmp/sysupgrade.bin of=/dev/mtdblock2
      dd if=/tmp/sysupgrade.bin of=/dev/mtdblock3
      dd if=/dev/zero bs=1 count=1 of=/dev/mtdblock4

* Reboot and wait for OpenWRT to boot up: :code:`ping 192.168.1.1`

Unbrick
=======

See: :ref:`net_openwrt_unifi_unbrick <Unifi AP Unbrick>`

----

UniFi AP
********

* Download the :code:`squashfs-sysupgrade` for your Model - be aware that Pro/Lite/Mesh have different images!

  See: `OpenWRT Firmware Selector - Unifi AP LR <https://firmware-selector.openwrt.org/?version=23.05.5&target=ath79%2Fgeneric&id=ubnt_unifi-ap-lr>`_

* Make sure you can access the AP via SSH. The default credentials are: :code:`ubnt/ubnt`

  :code:`ssh ubnt@192.168.1.20 -p22 -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostkeyAlgorithms=+ssh-rsa`

  The default unifi-AP IP is :code:`192.168.1.20`

  Restore the AP to defaults: :code:`syswrapper.sh restore-default`

* Install a TFTP client: :code:`apt install tftp`

* Boot the AP into TFTP recovery mode:

  * unplug AP
  * press reset
  * plug AP in
  * press reset for 20s - should flash in two colors
  * now its not pingable but has a tftp server started

* Change to the directory where you have downloaded the image into and start the tftp client:

  .. code-block:: bash

      tftp

      > connect 192.168.1.20
      > binary
      > rexmt 1
      > timeout 60
      > put openwrt-23.05.5-ath79-generic-ubnt_unifi-ap-lr-squashfs-sysupgrade.bin

.. _net_openwrt_unifi_unbrick:

Unbrick
=======

If you have failed on flashing your Unifi AP and it is not reachable at any IP address, you may only be able to fix it using a serial connector.

See: `Tutorial for serial connection <https://community.ui.com/questions/HOWTO-Unbrick-your-UniFi-AP/b6d2079f-38be-4a91-aea0-7ca5d14c470c>`_, `Unifi AP Serial Pins <https://openwrt.org/toh/ubiquiti/unifi_ap#serial>`_

Only connect Green/White to RX/TX (in some order)
If only female connectors are on the board - use male-to-male extension cables and just try to put them in on an angle.

For us - `minicom <https://linux.die.net/man/1/minicom>`_ at baud-rate 115200 worked well.


----

Known Issues
############

Mac-Address randomized on reboot
********************************

This is `a known issue <https://forum.openwrt.org/t/mac-address-changing-automatically-why/122037>`_ with some hardware.

It seems OpenWRT is not able to pull the hardware's mac-address.

In this case you will have to set the mac-addresses manually.

Example:

.. code-block:: bash

    PREFIX='C4:AD:34'  # vendor-specific prefix
    AP_NR=127
    AP_NR="$(printf "%06d" $AP_NR)"  # pad the number with leading zeros

    echo "${PREFIX}:${AP_NR:0:2}:${AP_NR:2:2}:${AP_NR:4:2}"
    # C4:AD:34:00:01:27

Then set it: :code:`uci set network.@device[0].macaddr=C4:AD:34:00:01:27`

Hardware: Mikrotik wAP (older 1-port models)
