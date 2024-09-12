.. _waf_haproxy:

.. include:: ../_include/head.rst

=======
HAProxy
=======

.. include:: ../_include/wip.rst

Intro
#####

Bevor Sie mit den komplexeren Features von HAProxy starten, sollten Sie mit :ref:`der grundlegenden Konfiguration vertraut sein <proxy_reverse_haproxy>`!

----

HAProxy Enterprise
##################

Die 'Enterprise' Version von HAProxy hat ein `dediziertes WAF-Modul <https://www.haproxy.com/solutions/web-application-firewall>`_ und eingebaute `Unterstützung für ModSecurity <https://www.haproxy.com/blog/the-haproxy-enterprise-waf>`_.

----

HAProxy Community
#################

HAProxy hat eingebaute Unterstützung für `externe Erweiterungen über SPOE <https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine>`_.

Darüber können einige externe WAF-Frameworks eingebunden werden:

* `Beispiel <https://github.com/haproxy/spoa-modsecurity>`_ für `ModSecurity <https://modsecurity.org/>`_
* `Beispiel <https://github.com/corazawaf/coraza-spoa>`_ für `Coraza WAF <https://github.com/corazawaf/coraza>`_

----

Grundlegende Filter
###################

Rate Limits / Anti DDOS
=======================

Siehe: :ref:`proxy_reverse_haproxy_rate`

----

GeoIP Filtering
===============

Siehe: :ref:`proxy_reverse_haproxy_geoip`

----

TLS Client Fingerprinting
=========================

Siehe: :ref:`proxy_reverse_haproxy_tls_fp`
