.. _security_certificates:

.. include:: ../_include/head.rst

.. |pki| image:: ../_static/img/security_certificates_pki.svg
   :class: wiki-img-lg
   :alt: OXL Docs - Public Key Infrastructure & x509 Certificates

==========
Encryption
==========

.. include:: ../_include/wip.rst

Intro
#####

The kind of certificates currently used are known as `X.509 <https://en.wikipedia.org/wiki/X.509>`_.

See also: `Cloudflare - What is an SSL certificate <https://www.cloudflare.com/learning/ssl/what-is-an-ssl-certificate/>`_

----

Certificates
############

x509 certificates have a public and a private key.

If you access a service - you and your device can see its public key. If the service is configured to do so, it will also show you the public keys of the parents inside the certificate hierarchy/trust chain.

Example: `Firefox <https://support.mozilla.org/en-US/kb/secure-website-certificate>`_

The **private keys need to be kept safe**! If not - attackers are able to impersonate your service and gain access to sensitive information!

----

Attributes
**********

Common Name
===========

The common name is the 'pretty name' users see first, when inspecting your certificate.

You might want to include your company name and a brief description of the service it is used for.

Example: :code:`OXL - Documentation`

Subject Alternative Names
=========================

Whenever a service is access over TLS, it will be access over either a DNS-name or an IP-address.

The SAN is a list of DNS/IP/EMAIL values that are valid for this specific certificate. The SAN is a security measure, that makes sure a leaked private-key cannot be abused for just any service.

Example: :code:`DNS:www.oxl.at,DNS:www.o-x-l.com,IP:1.1.1.1`

It is important to set this attribute correctly, as it will be validated!

----

Public Key Infrastructure & Trust Chains
****************************************

**Security is very important** when it comes to certificate trust-chains!

Whenever a trust chain is exploited, the attacker is able to :ref:`break all of your SSL/TLS connections <proxy_tls_interception>`!

A PKI builds a trust chain.

* Devices and Users trust the Root-CA
* The Root-CA signs a Sub-CA, marks it as trustworthy and enables it to sign certificates itself
* The Sub-CA is able to sign certificates for end-use (*users/clients/servers/services/software*)
* All of the users that trust the Root-CA will inherently trust the end-use certificates
* `Certificate revocation lists <https://en.wikipedia.org/wiki/Certificate_revocation_list>`_ are used to allow certificate to be revoked (*in case they were leaked/abused/...*)

|pki|

See also: `EasyRSA Docs <https://easy-rsa.readthedocs.io/en/latest/intro-to-PKI/>`_

----

Trust-Store
===========

Debian-based Linux
------------------

**Store**: :code:`/etc/ssl/certs/ca-certificates.crt`

**Install**: :code:`apt -y install ca-certificates`

**Adding CAs as Trusted**:

.. code-block:: bash

    # add ca public-key with .crt extension to /usr/share/ca-certificates/
    sudo update-ca-certificates

Windows
-------

See: `learn.microsoft.com <https://learn.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate>`_

----

Public vs Internal CAs
**********************

Public
======

Public CAs are technically the same. Only their are added to the default trust-store of many devices.

As end-users we have major limitations when using Public CAs. Most providers only allow you to create certificates for specific use-cases like :code:`server certificate`, :code:`user certificate` and :code:`digital signing certificate`. This is fine in most cases, but some edge-cases require advanced certificate types like :code:`subordinate certificate authority` (:ref:`TLS inspection <proxy_tls_interception>`).

Only a few certificate providers like `LetsEncrypt <https://letsencrypt.org/>`_ allow you to create certificates without **cost**. Most providers have a fee to pay.

Not all public certificate providers allow you to **create/update certificates non-interactively**. This is a common use-case if you use :ref:`IT Automation <atm_intro>`!

----

Private
=======

If you want to have full control - you may want to create a private CA!

**You will have to**:

* Make sure your PKI is designed well
* Take the Root CA (*private-key*) offline for security reasons
* Implement **Certificate Revocation Lists** to allow you to revoke existing certificates and sub-CAs
* Add the public-key of your root-CA to the trust-store of your devices, so they trust your PKI
* Secure the server, on which the PKI is places, to ensure the trust will not be abused
* Secure your certificate private keys

Examples for creation: `EasyRSA <https://github.com/OpenVPN/easy-rsa>`_, `Ansible Role <https://github.com/ansibleguy/infra_pki>`_, `Microsoft AD Certificate Services <https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/install-the-certification-authority>`_, `Hashicorp Vault <https://developer.hashicorp.com/vault/tutorials/secrets-management/pki-engine>`_

Best practices: `AWS <https://docs.aws.amazon.com/privateca/latest/userguide/ca-hierarchy.html>`_, `Microsoft AD Certificate Services <https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/pki-design-considerations>`_

----

.. _security_certificates_verify:

Verification
************

There are ways for attackers to :ref:`exploit trust chains and thus break encryption <proxy_tls_interception>`.

To stop the attacker from performing such a `Man-in-the-Middle attack <https://en.wikipedia.org/wiki/Man-in-the-middle_attack>`_ there are ways of enforcing TLS verification.

If an active check fails, so does the connection.

Trust
=====

This verification is on by default and should not be disabled.

It enables the basic trust-chain checks as described above.

Most software will use the system-wide trust-store for this validation.

If an attacker was able to insert his own CA in this store, this check will find no issue.

Subject Alternative Names
=========================

This verification is on by default and should not be disabled.

It checks that the DNS-name or IP-address we use to access the service, is listed inside the SAN of the certificate.

Specific Attributes
===================

Some software like OpenVPN allows you to validate the peer certificate by other certificate attributes.

Per example - we are able to check that the Common-Name attribute matches a specific string.

Only trust specific CA
======================

Privacy- or Security-sensitive software sometimes will implement a check that makes sure the peer certificate is signed by a specific certificate authority. This CA will be hardcoded inside the client-side application.

In that case, the software ignores the system trust-store.

We see this behavior in banking applications.

This is the only way of ensuring the connection between your client and server is not inspected by any 3th party.
