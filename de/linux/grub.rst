.. _linux_grub:

.. include:: ../_include/head.rst

===============
GRUB Bootloader
===============


Intro
#####

Der `GRUB Bootloader <https://www.gnu.org/software/grub/>`_ ist weitverbreitet im Einsatz auf Linux Systemen.

----

Fehlerhaften GRUB reparieren
############################

Wenn ein Linux-System nicht mehr als Boot-Option im BIOS-Bootmenü angezeigt wird, kann es nötig sein den GRUB-Bootloader zu reparieren.

1. Anderes Linux booten
=======================

In jedem Fall benötigt man dazu ein Linux-Live ISO oder ein anderes Linux-System, an dem die Festplatte des betroffenen Systems angeschlossen wird.

Download eines Linux-Live Image wie: `Debian Live (standard) <https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/>`_

Dieses ISO-Image muss auf einem bootbaren USB-Stick aufgespielt werden.

Zur Erstellung eines **bootbaren USB-Sticks** empfehlen wir das :ref:`Multi-Boot-Tool Ventoy <windows_ventoy_bootable_usb>`.

Englisches Keyboard
-------------------

Standardmäßig nutzt ein Linux Live-System das englische Tastaturlayout. (*QUERTY*)

Hier einige oft benötigte Key-Mappings vom deutschen: (*QUERTZ; Taste => EN Output*)

* **- => /**
* **ß => -**
* **? => _**
* **z => y**
* **y => z**

2. Wenn nötig: Festplatte entschlüsseln
=======================================

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

3. Root Mounten
===============

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

Siehe auch: `wiki.debian.org <https://wiki.debian.org/GrubEFIReinstall>`_

4. GRUB aktualisieren
=====================

.. code-block:: bash

    # change '/dev/sdX' to your system-disk (not a partition but the actual disk)
    grub-install /dev/sdX

    CTRL+D
    reboot


.. include:: ../_include/user_rath.rst
