.. _proxy_intro:

.. include:: ../_include/head.rst

.. |proxy_reverse| image:: ../_static/img/proxy_reverse.svg
   :class: wiki-img

.. |proxy_forward| image:: ../_static/img/proxy_forward.svg
   :class: wiki-img

=========
1 - Intro
=========

.. include:: ../_include/wip.rst

Types
*****

The two most common types of proxies are:

Forward
=======

Forward proxies are used to intercept and filter traffic.

In most cases they are used transparently in network firewall systems as a security measure.

To intercept TLS traffic, some of these proxies implement :ref:`TLS interception <proxy_tls_interception>`.

It can be illegal to intercept network traffic! Make sure to review the laws and regulations that apply to you.

It's also an invasion on the privacy of the affected users (if any are affected).

|proxy_forward|

Reverse
=======

Reverse proxies are placed in front of services.

In practise they are used to achieve load balancing, redundancy, high availability and to terminate the (client-to-server) TLS tunnel.

|proxy_reverse|
