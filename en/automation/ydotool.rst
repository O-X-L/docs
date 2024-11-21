.. _atm_ydotool:

.. include:: ../_include/head.rst

=======
yDoTool
=======

.. include:: ../_include/wip.rst

Intro
#####

`yDoTool <https://github.com/ReimuNotMoe/ydotool>`_ is a Linux tool that allows you to automate mouse and keyboard actions. It supports X11 and Wayland desktop environments.

The `xDoTool <https://github.com/jordansissel/xdotool>`_ only works on X11.

----

Setup
#####

See also: `Github issue <https://github.com/ReimuNotMoe/ydotool/issues/207>`_

It has a system- and a user-component.

The system service needs to run with root permissions.

This service creates a user-specific socket that is utilized by the user-component.

----

Executable
**********

If you are on Ubuntu or Debian - you can try to download the pre-compiled executables from the `Github releases <https://github.com/ReimuNotMoe/ydotool/releases>`_.

Else you might need to `manually compile <https://gabrielstaples.com/ydotool-tutorial/#1-build-and-install-ydotool>`_ them.

DO NOT install it via the APT package-manager - as the version is VERY old!

----

System Component
****************

Move the executable:

.. code-block:: bash

    sudo mv ~/Downloads/ydotoold-release-ubuntu-latest /usr/local/sbin/ydotoold
    sudo chown root:root /usr/local/sbin/ydotoold
    sudo chmod 750 /usr/local/sbin/ydotoold

Install the service:

.. code-block::

    # File: /etc/systemd/system/ydotool@.service

    [Unit]
    Description=Service to run yDoTool service

    [Service]
    Type=simple

    ExecStartPre=/bin/sleep 30
    ExecStart=/usr/local/sbin/ydotoold --socket-path="/run/user/%i/.ydotool_socket" --socket-own="%i:0"
    ExecReload=/usr/bin/kill -HUP $MAINPID

    KillMode=process
    Restart=always
    RestartSec=10
    TimeoutSec=180

    [Install]
    WantedBy=default.target

Enable & start it:

.. code-block:: bash

    sudo systemctl daemon-reload

    sudo systemctl enable ydotool@${UID}.service
    sudo systemctl start ydotool@${UID}.service

    systemctl status ydotool@${UID}.service

----

User Component
==============

Move the executable:

.. code-block:: bash

    sudo mv ~/Downloads/ydotool-release-ubuntu-latest /usr/local/bin/ydotool
    sudo chown root:root /usr/local/bin/ydotool
    sudo chmod 755 /usr/local/bin/ydotool

Test it:

.. code-block:: bash

    ydotool --help

    ydotool mousemove -x -100 -y 110

If it does not yet work - you might need to configure the path to the socket:

.. code-block:: bash

    # this socket should exist! else you have a problem with your service
    ls -l /run/user/${UID}/.ydotool_socket

    echo 'export YDOTOOL_SOCKET="/run/user/${UID}/.ydotool_socket"' >> "$HOME/.profile"

    # then open a new terminal and re-test it
