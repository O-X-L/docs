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

Wenn Sie mit Ubuntu oder Debian arbeiten, können Sie versuchen, die vorkompilierten ausführbaren Dateien von den `Github releases <https://github.com/ReimuNotMoe/ydotool/releases>`_ zu verwenden.

Sonst muss man diese `manuell Kompilieren <https://gabrielstaples.com/ydotool-tutorial/#1-build-and-install-ydotool>`_.

Installieren Sie es NICHT über den APT-Paketmanager - denn die Version ist SEHR alt!

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
