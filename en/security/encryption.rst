.. _security_encryption:

.. include:: ../_include/head.rst


==========
Encryption
==========

.. include:: ../_include/wip.rst

Intro
#####

We basically differentiate between **in-transit** and **at-rest** encryption.

See also: `RedHat - Encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-security_guide-encryption>`_

----

In Transit (asymmetric)
#######################

Encryption of traffic over the network can be achieved by utilizing TLS (*on top of TCP/UDP*) or `QUIC <https://blog.cloudflare.com/the-road-to-quic/>`_ (*on top of UDP for now*).

This kind of asymmetric encryption requires :ref:`certificates <security_certificates>` (*public and private key-pairs*).

If we talk about SSL - we actually mean `TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`_. SSL is deprecated as its last version 'SSLv3' is very old and vulnerable to many attacks.

See also: `Cloudflare - What is SSL <https://www.cloudflare.com/learning/ssl/what-is-ssl/>`_, `Cloudflare - TLS handshake <https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/>`_


----

At Rest (symmetric)
###################

Symmetric encryption uses one private key to en- and decrypt data.

This is often used for at-rest encryption of data on disk.

This kind of encryption can be very useful if you have devices, which you cannot physically protect against the access of others. Examples are: Servers in a managed datacenter, Mobile devices like laptops or smartphones, off-site backups

Examples: `Linux LUKS disk encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/security_hardening/encrypting-block-devices-using-luks_security-hardening>`_, `Android Encryption <https://source.android.com/docs/security/features/encryption>`_, `Microsoft Windows Bitlocker <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/>`_
