.. _security_encryption:

.. include:: ../_include/head.rst


==========
Encryption
==========

.. include:: ../_include/wip.rst

.. warning::

    This should only be a short intro to encryption. We will not go into the details.

Intro
#####

From a practical use-case standpoint we mainly differentiate between **in-transit** and **at-rest** encryption.

There are also different ways how the enc- and decryption is done.

If you want to broaden your knowledge about cryptography - we can recommend `theses Videos recorded at a german university !

If we talk about SSL - we actually mean `TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`_. SSL is deprecated as its last version 'SSLv3' is very old and vulnerable to many attacks.

See also: `dev.to - Data encryption <https://dev.to/documatic/data-encryption-securing-data-at-rest-and-in-transit-with-encryption-technologies-1lc2>`_, `RedHat - Encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-security_guide-encryption>`_

----

Use Cases
#########

In Transit
**********

Encryption of traffic over the network, in most cases, is achieved by utilizing TLS (*on top of TCP/UDP*) or `QUIC <https://blog.cloudflare.com/the-road-to-quic/>`_ (*on top of UDP for now*). TLS uses both, asymmetric (*session initiation*) and symmetric (*data transfer*) encryption.

Some applications, like VPNs, may use other protocols to encrypt their traffic. These sometimes only use symmetric encryption.

See also: `Cloudflare - What is SSL <https://www.cloudflare.com/learning/ssl/what-is-ssl/>`_, `Cloudflare - TLS handshake <https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/>`_

----

At Rest
*******

Symmetric encryption is often used for at-rest encryption of data on disk as there is no need to transfer the key over an unsecure connection.

This kind of encryption can be very useful if you have devices, which you cannot physically protect against the access of others. Examples are: Servers in a managed datacenter, Mobile devices like laptops or smartphones, off-site backups.

Examples: `Linux LUKS file encryption <https://opensource.com/article/21/4/linux-encryption>`_, `Linux LUKS disk encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/security_hardening/encrypting-block-devices-using-luks_security-hardening>`_, `Android Encryption <https://source.android.com/docs/security/features/encryption>`_, `Microsoft Windows Bitlocker <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/>`_

----

Kinds
#####

Symmetric
*********

It is faster than asymmetric encryption.

Symmetric encryption uses one private key to en- and decrypt data.

If symmetric encryption is used for in-transit encryption - protocols like `Diffie–Hellman <https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange>`_ need to be utilized to securely exchange the private key.

Asymmetric
**********

It uses a private & public key-pair to en- and decrypt data.

This removes the need for exchanging a private key if used for in-transit encryption.

The most common use-case of this kind of encryption is :ref:`TLS using certificates <security_certs>`.

.. include:: ../_include/user_rath.rst
