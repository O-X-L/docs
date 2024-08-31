.. _proxy_tls_interception:

.. include:: ../_include/head.rst

.. |intercept| image:: ../_static/img/proxy_tls_interception.svg
   :class: wiki-img

================
TLS Interception
================

Intro
#####

When sending plaintext traffic over a network, any bad actor can intercept/read/modify it. The client will not know
about this intrusion.

If the traffic is encrypted (currently using TLS) this is not possible, as the traffic is not readable for any third
parties. Only the client and server, that establish the encrypted 'tunnel' are aware of what traffic is being sent
and received.

To make interception of such encrypted traffic possible, a `Man-in-the-Middle attack <https://en.wikipedia
.org/wiki/Man-in-the-middle_attack>`_ needs to be performed. In that case the client will establish an encrypted
connection to the middle-man and it in turn will connect to the actual target server.

As a protection against such attacks, the TLS handshake will only be successful if the `server certificate
<https://www.cloudflare.com/learning/ssl/how-does-ssl-work/>`_ is **signed by a trusted certificate-authority** and
has a valid **subject alternative name** that includes its actual server/service name. This protection is known as
**SSL/TLS verification**.

To work around this protection, the intercepting proxy needs to have access to a certificate-authority that is
trusted by the client. Enterprises would use :ref:`an internal PKI <security_encryption>` to create such a certificate
trust chain.

|intercept|

Some countries are intercepting any traffic of their public networks as they have laws in-place that grant them the
rights to do so. This way they are able to sniff and modify/censor network traffic/requests.

----

SNI Sniffing
############

Alternatively to full TLS-Interception, Interceptors can read your target hostname from the TLS handshake as it is
transferred as plaintext as the handshake is performed. Clients and Servers are not aware of this kind of sniffing.

The `encrypted SNI <https://www.cloudflare.com/learning/ssl/what-is-encrypted-sni/>`_ standard is designed to fix
this information leak. Some states like China and Russia have reportedly started to block any ESNI TLS
handshakes.
