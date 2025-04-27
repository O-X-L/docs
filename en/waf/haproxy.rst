.. _waf_haproxy:

.. include:: ../_include/head.rst

=======
HAProxy
=======

.. include:: ../_include/wip.rst

Intro
#####

Before starting with advanced HAProxy feature - make sure to be familiar with the :ref:`basic HAProxy configration sets <proxy_reverse_haproxy>`!

----

HAProxy Enterprise
##################

The 'enterprise' version of HAProxy has a `dedicated WAF module <https://www.haproxy.com/solutions/web-application-firewall>`_ and built-in `support for ModSecurity <https://www.haproxy.com/blog/the-haproxy-enterprise-waf>`_.

----

HAProxy Community
#################

HAProxy built-in support for `external extensions using SPOE <https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine>`_.

Some external WAF frameworks can also be integrated:

* `Example <https://github.com/haproxy/spoa-modsecurity>`_ for `ModSecurity <https://modsecurity.org/>`_
* `Example <https://github.com/corazawaf/coraza-spoa>`_ for `Coraza WAF <https://github.com/corazawaf/coraza>`_

----

Basic Filters
#############

Rate Limits / Anti DDOS
=======================

See: :ref:`proxy_reverse_haproxy_rate`

----

GeoIP Filtering
===============

See: :ref:`proxy_reverse_haproxy_geoip`

----

TLS Client Fingerprinting
=========================

See: :ref:`proxy_reverse_haproxy_tls_fp`
