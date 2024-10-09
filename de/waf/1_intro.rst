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

**Web-Application-Firewalls** ergänzen herkömmliche (Netzwerk-)Firewalls beim Schutz Ihrer Systeme.

WAFs können grundlegend in **Cloud-Systeme** und **Eigenständige** kategorisiert werden.

Siehe auch: `Web application security <https://www.cloudflare.com/learning/security/what-is-web-application-security/>`_, `ModSecurity Intro <https://www.feistyduck.com/library/modsecurity-handbook-free/online/ch01-introduction.html>`_

----

Wie kann eine WAF Sie schützen?
*******************************

* Ihre Webseiten und Web-Applikationen sind eine der ersten Angriffsflächen, mit denen ein Angreifer interagiert.

  Wer dort schon auf Widerstand stoßt - sucht sich meist gleich ein besseres/einfacheres Ziel.

  Eine gut abgesicherte Web-Applikation spiegelt eine solide Haltung im Bezug auf IT-Security wieder und kann somit **für Hacker abschreckend** wirken.

* Angriffe durch Bots konsumieren oft einiges an Server-Ressourcen. Dies kann im schlimmsten Fall zu einem Ausfall führen (DOS/DDOS).

  Durch eine effektive Abwehr solcher Angriffen können Sie die **Performance** Ihrer Nutzer:innen **verbessern**.

  Außerdem kann man sich einiges an Ressourcen einsparen.

* Die Metadaten der WAF können auch an Ihre Web-Applikation weitergeleitet werden.

  Dies kann Ihnen erlauben, diese Informationen in einem **Risiko-Score** zu erfassen, welcher wiederum genutzt werden kann um Zugriffe für Bots oder 'böse User' einzuschränken.

  Praktisch kann dies zum Beispiel dazu genutzt werden, um Captcha's nur für auffällige User anzeigen zu lassen, kritische Aktionen (Newsletter Anmeldung, Account Registration, ...) zu unterbinden oder die Anzahl von Zugriffen innerhalb gewisser Zeit einzuschränken (Rate-Limits).

* Durch Scannen von Server-Responses kann eine WAF Ihre Applikation auch weitergehend **vor Datenabfluss schützen**.

* Eine WAF ist meist mit einem Load-Balancer (*wie HAProxy*) verknüpft.

  Dadurch können Sie mehrere Applikationsserver in einem **hochverfügbaren Verbund** vereinen.

* Durch die Integration von Reputations-Datenbanken können Sie das mögliche Risiko, das von einem Client/User ausgeht, besser einstufen.

  Neben reinen Datenbanken und IP-/ASN-Listen können auch dynamische Lösungen wie `CrowdSec <https://www.crowdsec.net/>`_ integriert werden.

Das Regelwerk einer WAF muss speziell auf die Anwendungen, die geschützt werden soll, abgestimmt sein. Dies kann initial etwas aufwendig sein - doch der Aufwand pendelt sich rasch ein.

----

Verwaltung eines WAF Regelwerks
*******************************

Dies ist keine einmalige Aufgabe! Sie **muss gewartet werden**! Vor allem bei Updates Ihrer Web-Anwendungen können Anpassungen nötig sein.

Meist nutzt man einen 'Audit-Modus' um das Verhalten der WAF zu testen, bevor diese wirklich aktiv geschalten wird.

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

----

Eigenständige WAF
#################

Eine WAF benötigt zwingend Zugriff auf alle Informationen, die zwischen Nutzer:in und Applikation ausgetauscht werden. Einschließlich sensibler Benutzerdaten. Dies kann das Outsourcing komplizieren.

Wir empfehlen die Nutzung von Open-Source Produkten wie :ref:`HAProxy <proxy_reverse_haproxy>`, `Coraza <https://github.com/corazawaf/coraza>`_ oder `ModSecurity <https://github.com/owasp-modsecurity/ModSecurity>`_.

Es gibt bereits `Sammlungen von Rulesets <https://coreruleset.org/>`_, die in solchen WAFs genutzt werden können.

Hosten kann man diese auf der eigenen Infrastruktur oder in einem Rechenzentrum. (z.B. `Hetzner Deutschland <https://www.hetzner.com/cloud/>`_)

**Vorteile**:

* Datenschutz & Digitale Privatsphäre

* Unabhängigkeit von einem Cloud-Provider

* Hochgradig Anpassbar

* Keine Lizenzkosten, wenn Open-Source genutzt wird


**Nachteile**:

* Keine AI-Basierte Erkennung (*zukünftig wird es auch möglich sein*)

* Sie müssen sicherstellen, dass Sie über genügend interne Ressourcen oder einen Dienstleister verfügen, um das Produkt zu warten

* Die initiale Einrichtung kann etwas aufwendiger sein

* System zur Visualisierung und Analyse von Logs nötig (z.B. `Graylog <https://graylog.org/products/source-available/>`_)

* Für Hoch-Verfügbarkeit muss gesorgt werden

----

Cloud Systeme
#############

WAF Cloud-Provider wie `Cloudflare <https://www.cloudflare.com/lp/ppc/waf-x/>`_ oder `Barracuda <https://de.barracuda.com/products/application-protection/web-application-firewall>`_ verfügen über zahlreiche Funktionen und sind in der Lage, Sie mit modernstem Schutz zu versorgen.

Diese Anbieter haben viele Ressourcen für die ständige Weiterentwicklung ihrer Systeme zur Verfügung. Sie können Ihnen sogar Engines zur Verfügung stellen, die Zero-Day-Exploits blockieren, die Sie noch nicht patchen können.

In diesem Fall kann es sinnvoll sein, auch andere Dienste dieses Anbieters zu nutzen, z. B. ein `CDN <https://www.cloudflare.com/de-de/lp/ppc/cdn-x>`_.

**Vorteile**:

* AI-Basierte Erkennung

* Regelwerk wird ständig angepasst und erweitert

* Weboberfläche zur Analyse von Logs

* Dynamische Skalierung


**Nachteile**:

* Höherer Kostenpunkt

* Cloud-Provider hat Zugriff auf Ihre Daten und die Daten Ihrer User

* Anpassbarkeit ist eingeschränkt

* Aufwand für Wartung des Regelwerks ist trotzdem nötig

* Eigenes Monitoring nur begrenzt möglich

* Logs können teilweise nicht zur Analyse/Archivierung weitergeleitet werden

----

Selbst Entwickelte Lösungen
###########################

Wenn Sie Entwickler sind, fragen Sie sich vielleicht: „Warum kann ich meine Codebasis nicht einfach um Sicherheitsprüfungen erweitern? Diese Frage ist berechtigt.

Wir raten grundsätzlich davon ab.

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
