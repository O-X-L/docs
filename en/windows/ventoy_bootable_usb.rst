.. _windows_ventoy_bootable_usb:

.. include:: ../_include/head.rst

=============================
Bootable USB-Stick via Ventoy
=============================


Intro
#####

For some technical activities, a computer/server must be started/booted from a specific ISO.

Bootable USB sticks are generally used for this purpose.

The tool `Ventoy <https://github.com/ventoy/Ventoy>`_ can be used to store multiple ISO files and, if necessary, additional data on an USB stick.

In addition to this useful functionality, its installation is very simple.

----

Usage
#####

* `Download Ventoy <https://sourceforge.net/projects/ventoy/files/>`_
* `Getting-Started Documentation <https://www.ventoy.net/en/doc_start.html>`_
* `GitHub - Project <https://github.com/ventoy/Ventoy>`_

Installation
============

* Download the installation
* Unpack it
* Connect an USB-stick **which data can be wiped**!
* Run the application :code:`Ventoy2Disk`
* Choose your USB-Stick and install Ventoy on it
* After it is finished: The USB-stick should again be available inside your file-explorer - if not - unplug & plug
* Copy bootable ISO-files on the USB-stick

When restarting your computer the USB-stick should be visible as boot-option inside the BIOS-bootmenu.

After booting from it Ventoy will show you a list of ISO-files that you can choose to boot from. Simply select some via your keyboard and choose 'normal' start.

.. include:: ../_include/user_rath.rst
