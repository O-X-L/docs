.. _waf_fingerprinting:

.. include:: ../_include/head.rst

=========================
2 - Client Fingerprinting
=========================

.. include:: ../_include/wip.rst

Intro
#####

For Web-Application firewalls it is very useful to fingerprint their clients.

The more information we have about our clients, the easier it is to recognize attack schemes and validate if requests are legitimate users or bots.

Of course - fingerprinting has also the negative aspect of losing a bit of privacy as clients can be tracked easier. This is especially true for client-side fingerprinting. Server-side fingerprinting has a lot less information about its clients.

----

Client-Side Fingerprinting
##########################

Many websites are using Javascript to create detailed fingerprints of their clients/users.

Javascript has access to a lot of information about the device it is running on.

Here is a very basic example on how a Javascript can be utilized to create a client fingerprint: `Fingerprint MD5 hash <https://github.com/superstes/http-fingerprint/blob/latest/client_side/1/fp.js>`_

Such a fingerprint can be added to requests as cookie or HTTP-header, so the server-side code can process it.

See also: `niespodd GitHub <https://github.com/niespodd/browser-fingerprinting>`_

----

Server-Side Fingerprinting
##########################

TLS Fingerprinting
******************

JA3
===

See: `Salesforce JA3 Fingerprinting <https://github.com/salesforce/ja3>`_

JA3N
====

Browsers started to randomize their TLS extensions to remove some information.

See: `Salesforce GitHub Issue <https://github.com/salesforce/ja3/issues/88>`_

We've created a `JA3N HAProxy Lua Plugin <https://github.com/O-X-L/haproxy-ja3n>`_. It showcases how the fingerprint is constructed.

JA4
===

See: `FoxIO JA4 TLS Fingerprint <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md>`_ | `FoxIO JA4 Database <https://ja4db.com/>`_

We've created a `JA4 HAProxy Lua Plugin <https://github.com/O-X-L/haproxy-ja4>`_. It showcases how the fingerprint is constructed.

----

TCP Fingerprinting
******************

As the TCP connection has some Operating-System specific attributes, we can utilize this information to gather some knowledge about the client we are communicating with.

The Max-Segment-Size can also be a hint if the client is currently connecting over a VPN or Proxy.

JA4T
====

See: `FoxIO JA4T Fingerprint <https://medium.com/foxio/ja4t-tcp-fingerprinting-12fb7ce9cb5a>`_

----

JA4 Suite
*********

See: `FoxIO JA4 Fingerprinting Suite <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/README.md>`_

.. include:: ../_include/user_rath.rst
