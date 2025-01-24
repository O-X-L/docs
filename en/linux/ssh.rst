.. _linux_ssh:

.. include:: ../_include/head.rst

===
SSH
===

.. include:: ../_include/wip.rst

Intro
#####

SSH is a commonly used remote-access protocol that can be used to manage many different kinds of devices and servers.

This article will focus on its use on Linux servers and clients.

----

Server
######

Documentation: `sshd_config <https://manpages.debian.org/unstable/manpages-de/sshd_config.5.de.html>`_

Authentication
**************

Root
====

For security-reasons - direct root access should be disabled:

.. code-block::

    PermitRootLogin no

Method
======

You may also always want enable Public-Key authentication.

Public-/Private-Keypairs for clients can be generated like this: :code:`ssh-keygen -t ed25519`

This is how you can enable Public-Key auth:

.. code-block::

    PasswordAuthentication no
    PermitEmptyPasswords no
    PubkeyAuthentication yes
    AuthenticationMethods publickey

If you want to require both, Public-Key and password to connect:

.. code-block::

    PasswordAuthentication yes
    PermitEmptyPasswords no
    PubkeyAuthentication yes
    AuthenticationMethods publickey,password

----

Match
*****

You can override specific settings for **User, Group, Host and Address**.

Match User
==========

This statement can be used to set user-specific settings.

**Examples**:

* Allow unprivileged user to authenticate by only using public-key - if others require a password too:

    .. code-block::

        PubkeyAuthentication yes
        PasswordAuthentication yes
        AuthenticationMethods publickey,password

        Match User <USER>
            AuthenticationMethods publickey

* Limit source-IPs from which a user is able to connect:

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

As the cluster-communication will use SSH for some node-to-node communications, you will have to ensure some config is set:

.. code-block::

    # you can add multiple Port-statements if you use another port for management-access
    Port 22

    AcceptEnv LC_PVE_TICKET

If you use a second ssh-port for management-access: You may want to filter network-access to port 22 so only pve-hosts can connect to it.

----

Client
######

Documentation: `ssh <https://manpages.debian.org/testing/manpages-de/ssh.1.de.html>`_

tbd

SSH Tunnel
**********

tbd

.. include:: ../_include/user_rath.rst
