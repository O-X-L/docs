.. _waf_intro:

.. |waf_dev_flow| image:: ../_static/img/waf_intro.svg
   :class: wiki-img
   :alt: OXL Docs - WAF Development Flow

.. include:: ../_include/head.rst

=========
1 - Intro
=========

.. include:: ../_include/wip.rst

Intro
#####

Ihre Anwendung muss für viele Nutzer erreichbar sein - oft sogar weltweit. Deshalb müssen Sie dafür sorgen, dass sie gesichert ist.

WAFs ergänzen herkömmliche (Netzwerk-)Firewalls beim Schutz Ihrer Systeme.

Eine WAF muss speziell auf die Anwendungen, die sie schützten soll, abgestimmt sein. Dies ist keine einmalige Aufgabe! Sie muss **permanent gewartet** werden!

Durch Scannen von Request-Responses kann eine WAF Ihre Applikation auch weitergehend vor Datenabfluss schützen.

Die beiden Hauptkategorien von WAFs sind **Cloud-Hosted** und **Self-Hosted** WAFs.

Siehe auch: `Web application security <https://www.cloudflare.com/learning/security/what-is-web-application-security/>`_, `ModSecurity Intro <https://www.feistyduck.com/library/modsecurity-handbook-free/online/ch01-introduction.html>`_

Arbeiten mit einer WAF?
***********************

* **Definieren der 'Schnittstellen'**

  * Wege, auf denen die Benutzer mit dieser spezifischen Anwendung interagieren können sollen
  * Festlegung der Art und Weise, wie die Benutzer mit diesen 'Schnittstellen' interagieren dürfen
  * Übersicht über APIs behalten und diese Dokumentieren
  * Nur Anfragen zulassen, die legitimen Anwendungsfällen entsprechen

* Alle Requests, welche die Benutzer durchführen dürfen, durch WAF Regeln und Angriffs-Erkennungs-Engines **Überprüfen und Scannen**

* Alle Requests **Loggen und Analysieren**

  * Erkennen von Schemen in diesen Informationen
  * Aktualisieren der WAF-Engine/des Regelsatzes nach Bedarf

  |waf_dev_flow|

Meist nutzt man einen 'Audit-Modus' um das Verhalten der WAF zu testen, bevor diese wirklich aktiv geschalten wird.

----

Self Hosted
###########

Da eine WAF Zugriff auf alle Informationen hat, die zwischen Benutzer:in und Applikation ausgetauscht werden - einschließlich sensibler Benutzerdaten, ist es für Ihr Unternehmen oder Projekt möglicherweise nicht akzeptabel, eine WAF auf einer Infrastruktur zu hosten, die Sie nicht kontrollieren.

Einige Enterprise-Grade-Lösungen können teuer werden, aber Sie können immer mit einem Open-Source Produkt wie :ref:`HAProxy Community <proxy_reverse_haproxy>`, `SafeLine <https://github.com/chaitin/SafeLine>`_, `Coraza <https://github.com/corazawaf/coraza>`_ oder `ModSecurity <https://github.com/owasp-modsecurity/ModSecurity>`_ beginnen und später aufrüsten.

Sie müssen sicherstellen, dass Sie über genügend interne Ressourcen oder einen Berater verfügen, um das Produkt zu warten.

Es mag mehr Arbeit sein, eine fertige WAF einzurichten, aber auf diese Weise haben Sie ein unabhängiges System.

Es gibt bereits `Sammlungen von Rulesets <https://coreruleset.org/>`_, die in vielen WAFs genutzt werden können.

----

Cloud Hosted
############

In der WAF Cloud-Provider wie `Cloudflare <https://www.cloudflare.com/lp/ppc/waf-x/>`_ oder `Barracuda <https://de.barracuda.com/products/application-protection/web-application-firewall>`_ verfügen über zahlreiche Funktionen und sind in der Lage, Sie mit modernstem Schutz zu versorgen.

Diese Anbieter haben viele Ressourcen für die ständige Weiterentwicklung ihrer Systeme zur Verfügung. Sie können Ihnen sogar Engines zur Verfügung stellen, die Zero-Day-Exploits blockieren, die Sie noch nicht patchen können.

In diesem Fall kann es sinnvoll sein, auch andere Dienste dieses Anbieters zu nutzen, z. B. ein `CDN <https://www.cloudflare.com/de-de/lp/ppc/cdn-x>`_.

----

Self Developed Solutions
########################

Wenn Sie Entwickler sind, fragen Sie sich vielleicht: „Warum kann ich meine Codebasis nicht einfach um Sicherheitsprüfungen erweitern? Diese Frage ist berechtigt.

In der Praxis ist es empfehlenswert, die WAF von Ihrer Anwendung zu entkoppeln. Dies hat einige legitime Gründe:

* **Expertise**

  In solchen Fällen erinnere ich mich immer an den Satz: :code:`Implementieren Sie niemals Ihren eigenen Verschlüsselungsalgorithmus. Sie mögen denken, dass es sicher ist - aber ich kann Ihnen versichern, dass dies nicht zutrifft!` (`aus Kryptographie-Vorlesungen <https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX>`_)

  WAF-Provider haben Mitarbeiter:innen, die auf die Entwicklung für diesen Anwendungsfall spezialisiert sind.

  Ihre Entwickler kennen sich vielleicht mit `OWASP <https://www.cloudflare.com/learning/security/threats/owasp-top-10/>`_ aus und haben gute Erfahrungen mit der Entwicklung von sicherem Code, aber eine WAF muss über ein breites Toolset verfügen, wie (zumindest) :code:`DDOS-Schutz`, :code:`Erkennung und Blockierung gängiger Angriffe über SQLi/XSS/CSRF/SSRF/...`, :code:`Blockierung nach IP und ASN/ISP` und :code:`Bot-Erkennung und -Behandlung`.

  Sie müssen wirklich gute Argumente haben, um einen großen Teil der Entwicklungszeit zu investieren. Und seien Sie sich bewusst, dass diese Systeme gewartet werden müssen.

  Wenn es wirklich notwendig ist, sollten Sie diesen Dienst zumindest von Ihrer Anwendung entkoppeln.

* **Komplexität**

  Ihre Anwendung kann sehr viel komplexer werden, wenn Sie diese Schutzschichten hinzufügen.

* **Abstraktion**

  WAFs sollten, wie herkömmliche (Netzwerk-)Firewalls, ein dedizierter Dienst sein, der dem Anwendungsdienst vorangestellt wird.

  Dies erleichtert die Fehlersuche und hilft bei der Skalierung Ihrer Infrastruktur.

* **Performance**

  Die meisten WAF-Systeme laufen auf C, Rust, Golang oder einer anderen schnellen/einfachen Programmiersprache.

  Wenn Sie die gesamte Logik in Python, PHP, Javascript oder einer anderen Hochsprache implementieren, kann die Leistung deutlich schlechter ausfallen.

* **Unterstützung/Support**

  Wenn Sie eine bestehende Lösung verwenden, können Sie problemlos Unterstützung von Dritten erhalten.

  Nicht so, wenn es sich um Ihre eigene Codebasis handelt.

Das soll nicht heißen, dass Sie keine Sicherheitsüberprüfungen in Ihre Anwendung einbauen sollten! Das sollten Sie. Aber wie bereits erwähnt - eine WAF ist mehr als nur ein paar Sicherheitsprüfungen. Sie ist wirklich eine **Firewall**!

.. include:: ../_include/user_rath.rst
