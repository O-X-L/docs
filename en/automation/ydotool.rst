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
**************

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

----

Usage
#####

Commandos
*********

First of all - read the help texts:

.. code-block:: bash

    ydotool --help
    > Usage: ydotool <cmd> <args>
    > Available commands:
    >   click
    >   mousemove
    >   type
    >   key
    >   debug
    >   bakers
    > Use environment variable YDOTOOL_SOCKET to specify daemon socket.

    ydotool mousemove --help
    > Usage: mousemove [OPTION]... [-x <xpos> -y <ypos>] [-- <xpos> <ypos>]
    > Move mouse pointer or wheel.
    >
    > Options:
    >   -w, --wheel                Move mouse wheel relatively
    >   -a, --absolute             Use absolute position, not applicable to wheel
    >   -x, --xpos                 X position
    >   -y, --ypos                 Y position
    >   -h, --help                 Display this help and exit

    ydotool click --help
    > Usage: click [OPTION]... [BUTTONS]...
    > Click mouse buttons.
    >
    > Options:
    >   -r, --repeat=N             Repeat entire sequence N times
    >   -D, --next-delay=N         Delay N milliseconds between input events (up/down,                                a complete click means doubled time)
    >   -h, --help                 Display this help and exit
    >
    > How to specify buttons:
    >   Now all mouse buttons are represented using hexadecimal numeric values, with an optional
    > bit mask to specify if mouse up/down needs to be omitted.
    >   0x00 - LEFT
    >   0x01 - RIGHT
    >   0x02 - MIDDLE
    >   0x03 - SIDE
    >   0x04 - EXTR
    >   0x05 - FORWARD
    >   0x06 - BACK
    >   0x07 - TASK
    >   0x40 - Mouse down
    >   0x80 - Mouse up
    >   Examples:
    >     0x00: chooses left button, but does nothing (you can use this to implement extra sleeps)
    >     0xC0: left button click (down then up)
    >     0x41: right button down
    >     0x82: middle button up
    >   The '0x' prefix can be omitted if you want.

    ydotool type --help
    > Usage: type [OPTION]... [STRINGS]...
    > Type strings.
    >
    > Options:
    >   -d, --key-delay=N          Delay N milliseconds between keys (the delay between every key down/up pair) (default: 20)
    >   -H, --key-hold=N           Hold each key for N milliseconds (the delay between key down and up) (default: 20)
    >   -D, --next-delay=N         Delay N milliseconds between command line strings (default: 0)
    >   -f, --file=PATH            Specify a file, the contents of which will be be typed as if passed as an argument.
    >                                The filepath may also be '-' to read from stdin
    >   -e, --escape=BOOL          Escape enable (1) or disable (0)
    >   -h, --help                 Display this help and exit
    >
    > Escape is enabled by default when typing command line arguments, and disabled by default when typing from file and stdin.

    ydotool key --help
    > Usage: key [OPTION]... [KEYCODES]...
    > Emit key events.
    >
    > Options:
    >   -d, --key-delay=N          Delay N milliseconds between key events
    >   -h, --help                 Display this help and exit
    >
    > Since there's no way to know how many keyboard layouts are there in the world,
    > we're using raw keycodes now.
    >
    > Syntax: <keycode>:<pressed>
    > e.g. 28:1 28:0 means pressing on the Enter button on a standard US keyboard.
    >      (where :1 for pressed means the key is down and then :0 means the key is released)     42:1 38:1 38:0 24:1 24:0 38:1 38:0 42:0 - "LOL"
    >
    > Non-interpretable values, such as 0, aaa, l0l, will only cause a delay.
    >
    > See `/usr/include/linux/input-event-codes.h' for available key codes (KEY_*).
