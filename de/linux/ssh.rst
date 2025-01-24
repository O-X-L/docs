.. _linux_ssh:

.. include:: ../_include/head.rst

===
SSH
===

.. include:: ../_include/wip.rst

Intro
#####

SSH ist ein weit verbreitetes Fernzugriffsprotokoll, das für die Verwaltung vieler verschiedener Geräte und Server verwendet werden kann.

Dieser Artikel konzentriert sich auf die Verwendung auf Linux-Servern und -Clients.

----

Server
######

Dokumentation: `sshd_config <https://manpages.debian.org/unstable/manpages-de/sshd_config.5.de.html>`_

Listeners
*********

Folgenderweise kann man SSH auf alle IPs hören lassen:

.. code-block::

    # ipv4
    ListenAddress 0.0.0.0
    # ipv6
    ListenAddress \::

----

Authentifizierung
*****************

Root
====

Aus Sicherheitsgründen sollte der direkte Root-Zugriff deaktiviert werden:

.. code-block::

    PermitRootLogin no

Method
======

Es ist auch zu empfehlen die Public-Key-Authentifizierung aktivieren.

Public-/Private-Key-Paare für Clients können wie folgt erzeugt werden: :code:`ssh-keygen -t ed25519`

So können Sie die Public-Key-Authentifizierung aktivieren:

.. code-block::

    PasswordAuthentication no
    PermitEmptyPasswords no
    PubkeyAuthentication yes
    AuthenticationMethods publickey

Wenn Sie beides benötigen, Public-Key und Passwort, um eine Verbindung herzustellen:

.. code-block::

    PasswordAuthentication yes
    PermitEmptyPasswords no
    PubkeyAuthentication yes
    AuthenticationMethods publickey,password

----

Match
*****

Sie können Einstellungen für **User, Group, Host und Address** überschreiben.

Match User
==========

Diese Anweisung kann verwendet werden, um benutzerspezifische Einstellungen vorzunehmen.

**Examples**:

* Erlauben Sie unprivilegierten Benutzern, sich nur mit dem öffentlichen Schlüssel zu authentifizieren - wenn andere auch ein Passwort benötigen:

    .. code-block::

        PubkeyAuthentication yes
        PasswordAuthentication yes
        AuthenticationMethods publickey,password

        Match User <USER>
            AuthenticationMethods publickey

* Begrenzung der Quell-IPs, von denen aus ein Benutzer eine Verbindung herstellen kann:

    .. code-block::

        Match User <USER>
            AllowUsers <USER>@<IP>/32

        # example:
        Match User ansible
            AllowUsers ansible@192.168.0.10/32

----

Special Cases
*************

Proxmox VE
==========

Da die Clusterkommunikation SSH für die Kommunikation zwischen den Knoten verwendet, müssen Sie sicherstellen, dass einige Konfigurationseinstellungen vorgenommen werden:

.. code-block::

    # Sie können mehrere Port-Statements hinzufügen, wenn Sie einen anderen Port für den Management-Zugang verwenden
    Port 22

    AcceptEnv LC_PVE_TICKET

Wenn Sie einen zweiten SSH-Port für den Management-Zugang verwenden: Möglicherweise möchten Sie den Netzwerkzugriff auf Port 22 filtern, damit sich nur PVE-Hosts mit diesem Port verbinden können.

----

Client
######

Dokumentation: `ssh <https://manpages.debian.org/testing/manpages-de/ssh.1.de.html>`_

tbd

SSH Tunnel
**********

tbd


.. include:: ../_include/user_rath.rst
