.. _atm_ydotool:

.. include:: ../_include/head.rst

=======
yDoTool
=======

.. include:: ../_include/wip.rst

Intro
#####

`yDoTool <https://github.com/ReimuNotMoe/ydotool>`_ ist ein Linux-Tool, mit dem Sie Maus- und Tastaturaktionen automatisieren können. Es unterstützt die Desktop-Umgebungen X11 und Wayland.

Das `xDoTool <https://github.com/jordansissel/xdotool>`_ funktioniert nur auf X11.

----

Setup
#####

Siehe auch: `Github issue <https://github.com/ReimuNotMoe/ydotool/issues/207>`_

Er hat eine System- und eine Benutzerkomponente.

Der Systemdienst muss mit Root-Rechten laufen.

Dieser Dienst erstellt einen benutzerspezifischen Socket, der von der Benutzerkomponente verwendet wird.

----

Applikation
***********

Wenn Sie mit Ubuntu oder Debian arbeiten, können Sie versuchen, die vorkompilierten ausführbaren Dateien von den `Github releases <https://github.com/ReimuNotMoe/ydotool/releases>`_ zu verwenden. Achtung: Diese Version kann zur Zeit einige Bugs haben.

Sonst muss man diese `manuell Kompilieren <https://gabrielstaples.com/ydotool-tutorial/#1-build-and-install-ydotool>`_.

Installieren Sie es NICHT über den APT-Paketmanager - denn die Version ist SEHR alt!

Kompilieren via Docker
======================

Dockerfile:

.. code-block::

    FROM debian:latest
    # FROM ubuntu:latest

    WORKDIR /tmp

    RUN apt update && \
        apt -y install cmake scdoc pkg-config git

    RUN git clone https://github.com/ReimuNotMoe/ydotool.git

    RUN cd /tmp/ydotool && \
        mkdir -p build && \
        cd build && \
        cmake /tmp/ydotool && \
        make -j "$(nproc)"

Ausführen:

.. code-block:: bash

    docker build -f Dockerfile_ydotool -t build_ydotool .

Applikation exportieren:

.. code-block:: bash

    docker run --rm -it -v /tmp:/tmp2 build_ydotool sh
    cp /tmp/ydotool/build/ydotool* /tmp2/

Säubern:

.. code-block:: bash

    docker image rm build_ydotool

----

System Komponente
*****************

Die ausführbare Datei verschieben:

.. code-block:: bash

    sudo mv ~/Downloads/ydotoold-release-ubuntu-latest /usr/local/sbin/ydotoold
    sudo chown root:root /usr/local/sbin/ydotoold
    sudo chmod 750 /usr/local/sbin/ydotoold

Den Dienst installieren:

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

Diesen aktivieren und starten:

.. code-block:: bash

    sudo systemctl daemon-reload

    sudo systemctl enable ydotool@${UID}.service
    sudo systemctl start ydotool@${UID}.service

    systemctl status ydotool@${UID}.service

----

Benutzer Komponente
*******************

Die ausführbare Datei verschieben:

.. code-block:: bash

    sudo mv ~/Downloads/ydotool-release-ubuntu-latest /usr/local/bin/ydotool
    sudo chown root:root /usr/local/bin/ydotool
    sudo chmod 755 /usr/local/bin/ydotool

Die Ausführung testen:

.. code-block:: bash

    ydotool --help

    ydotool mousemove -x -100 -y 110

Wenn es noch nicht funktioniert, müssen Sie möglicherweise den Pfad zum Socket konfigurieren:

.. code-block:: bash

    # dieser Socket sollte vorhanden sein! sonst gibt es ein Problem mit dem Dienst
    ls -l /run/user/${UID}/.ydotool_socket

    echo 'export YDOTOOL_SOCKET="/run/user/${UID}/.ydotool_socket"' >> "$HOME/.profile"

    # danach ein neues Terminal öffnen und es erneut testen

----

Nutzung
#######

Kommands
********

Zu Anfang - die Hilfe lesen:

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
