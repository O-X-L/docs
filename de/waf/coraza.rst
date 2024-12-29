.. _waf_coraza:

.. include:: ../_include/head.rst

==============
Coraza (OWASP)
==============

.. include:: ../_include/wip.rst

Intro
#####

Die `Coraza Open-Source Web-Application-Firewall <https://coraza.io/>`_ wird von der `OWASP Organisation <https://owasp.org/www-project-coraza-web-application-firewall/>`_ geführt.

Sie soll einen Nachfolger für die weitverbreitete `ModSecurity WAF <https://github.com/owasp-modsecurity/ModSecurity>`_ darstellen.

Als Schutz gegen diverse praktisch eingesetzte Attacken, kann das `Kern-Regelwerk <https://coraza.io/docs/tutorials/coreruleset/>`_ eingesetzt werden. Siehe auch: `github.com/corazawaf/coraza-coreruleset <https://github.com/corazawaf/coraza-coreruleset>`_

Dieses Regelwerk kann recht schnell/leicht implementiert und Applikations-Spezifisch angepasst werden.

Diese WAF kann in existierende Load-Balancer eingebunden werden: `Caddy <https://github.com/corazawaf/coraza-caddy>`_, `Nginx <https://github.com/corazawaf/coraza-nginx>`_, `HAProxy <https://github.com/corazawaf/coraza-spoa>`_

----

HAProxy Integration
###################

**Info**: Die HAProxy Integration wird noch nicht als Production-Ready angesehen!

Für die Integration wird die `HAProxy SPOE Schnittstelle <https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine>`_ genutzt.

Um diese WAF in HAProxy (Community) zu integrieren, muss folgendes am Zielsystem umgesetzt werden:

* Installation von HAProxy >= 3.1 (*SPOE Refactor*)
* Die Coraza-SPOE Binary..

    * ..via `Golang <https://go.dev/doc/install>`_ vom Source-Code kompilieren
    * ..oder die `von uns vor-kompilierte <https://github.com/O-X-L/coraza-spoa/releases>`_ nutzen

* tbc

Ansible Role: `HAProxy Coraza-WAF <https://github.com/ansibleguy/haproxy_waf_coraza>`_
