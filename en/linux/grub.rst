.. _linux_grub:

.. include:: ../_include/head.rst

===============
GRUB Bootloader
===============

Intro
#####

The `GRUB Bootloader <https://www.gnu.org/software/grub/>`_ is widely used on Linux systems.

----

Fix a failed GRUB
#################

If a Linux-System is not shown as option inside the BIOS-bootmenu - it can be necessary to repair the GRUB-bootloader.

1. Boot another Linux
=====================

You need a Linux-Live ISO or another Linux-System where you can attach the disk of the failed system.

Download a Linux-Live image like: `Debian Live (standard) <https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/>`_

You need to write the ISO-image on a bootable USB-stick.

We recommend the usage of the :ref:`Multi-Boot-Tool Ventoy <windows_ventoy_bootable_usb>` to create such bootable sticks.

English Keyboard
----------------

By default the Linux Live-System uses the english keyboard layout. (*QUERTY*)

Here are some often required key-mapping from the german layout: (*QUERTZ; Key => EN output*)

* **- => /**
* **ß => -**
* **? => _**
* **z => y**
* **y => z**

2. If required: Decrypt the disk
================================

.. code-block:: bash

    sudo -i

    # make sure we have a network connection
    ip a
    ping 1.1.1.1

    # install cryptmount
    apt update
    apt install cryptsetup

    # find your disk
    lsblk -o +model

    # decrypt the disk ('system' is just a generic name)
    # change '/dev/sdX3' to the block-device that contains your root-partition (or whatever partition is encrypted)
    cryptsetup luksOpen /dev/sdX3 system

    # you should be able to mount your decrypted partitions /dev/mapper/... in the next steps

3. Mount Root
=============

.. code-block:: bash

    mount -t efivarfs none /sys/firmware/efi/efivars

    # change '/dev/sdX' to your system-disk

    # mount root partition
    ## default example
    mount /dev/sdX3 /mnt

    ## example with multiple LVM partitions
    mount /dev/mapper/vg0-root /mnt
    mount /dev/mapper/vg0-var /mnt/var
    mount /dev/mapper/vg0-home /mnt/home

    # mount boot partition (if you have a dedicated one)
    mount /dev/sdX2 /mnt/boot

    # mount efi partition
    mount /dev/sdX1 /mnt/boot/efi

    # bind the runtime directories from the live-image
    mount --bind /dev /mnt/dev
    mount --bind /dev/pts /mnt/dev/pts
    mount --bind /proc /mnt/proc
    mount --bind /sys /mnt/sys
    mount --bind /sys/firmware/efi/efivars /mnt/sys/firmware/efi/efivars

    # switch into the new root-context
    chroot /mnt

See also: `wiki.debian.org <https://wiki.debian.org/GrubEFIReinstall>`_

4. Reinstall GRUB
=================

.. code-block:: bash

    # change '/dev/sdX' to your system-disk (not a partition but the actual disk)
    grub-install /dev/sdX

    CTRL+D
    reboot


.. include:: ../_include/user_rath.rst
