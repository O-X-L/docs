.. _waf_fingerprinting:

.. include:: ../_include/head.rst

=========================
2 - Client Fingerprinting
=========================

.. include:: ../_include/wip.rst

Intro
#####

Für Web-Anwendungs-Firewalls ist es sehr nützlich, Fingerabdrücke ihrer Clients zu erstellen.

Je mehr Informationen wir über unsere Clients haben, desto einfacher ist es, Angriffsschemem zu erkennen und festzustellen, ob es sich bei den Anfragen um legitime Benutzer oder Bots handelt.

Natürlich hat die Erstellung von Fingerabdrücken auch den negativen Aspekt, dass die Privatsphäre ein wenig verloren geht, da die Clients leichter nachverfolgt werden können. Dies gilt insbesondere für Client-Side Fingerprinting. Beim Server-Side Fingerprinting stehen viel weniger Informationen über die Clients zur Verfügung.

----

Client-Side Fingerprinting
##########################

Viele Websites verwenden Javascript, um detaillierte Fingerabdrücke ihrer Kunden/Nutzer zu erstellen.

Javascript hat Zugang zu einer Vielzahl von Informationen über das Client-Gerät.

Hier ein einfaches Beispiel dafür, wie ein Javascript verwendet werden kann, um einen Fingerabdruck des Kunden zu erstellen: `Fingerprint MD5 hash <https://github.com/superstes/http-fingerprint/blob/latest/client_side/1/fp.js>`_

Ein solcher Fingerabdruck kann als Cookie oder HTTP-Header zu Anfragen hinzugefügt werden, damit der serverseitige Code ihn verarbeiten kann.

Siehe auch: `niespodd GitHub <https://github.com/niespodd/browser-fingerprinting>`_

----

Server-Side Fingerprinting
##########################

TLS Fingerprinting
******************

JA3
===

Siehe: `Salesforce JA3 Fingerprinting <https://github.com/salesforce/ja3>`_

JA3N
====

Die Browser haben begonnen, ihre TLS-Erweiterungen zu randomisieren, um einige Informationen zu entfernen.

Siehe: `Salesforce GitHub Issue <https://github.com/salesforce/ja3/issues/88>`_

Wir haben ein `JA3N HAProxy Lua Plugin <https://github.com/O-X-L/haproxy-ja3n>`_ erstellt. Es zeigt, wie der Fingerabdruck aufgebaut ist.

JA4
===

Siehe: `FoxIO JA4 TLS Fingerprint <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md>`_ | `FoxIO JA4 Database <https://ja4db.com/>`_

Wir haben ein `JA4 HAProxy Lua Plugin <https://github.com/O-X-L/haproxy-ja4>`_ erstellt. Es zeigt, wie der Fingerabdruck aufgebaut ist.

----

TCP Fingerprinting
******************

Da die TCP-Verbindung einige betriebssystemspezifische Attribute hat, können wir diese Informationen nutzen, um mehr den Client zu erfahren, mit dem wir kommunizieren.

Die Max-Segment-Size kann auch ein Hinweis darauf sein, ob die Verbindung des Clients zur Zeit über einen VPN oder Proxy läuft.

JA4T
====

Siehe: `FoxIO JA4T Fingerprint <https://medium.com/foxio/ja4t-tcp-fingerprinting-12fb7ce9cb5a>`_

----

JA4 Suite
*********

Siehe: `FoxIO JA4 Fingerprinting Suite <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/README.md>`_

.. include:: ../_include/user_rath.rst
