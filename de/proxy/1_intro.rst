.. _proxy_intro:

.. include:: ../_include/head.rst

.. |proxy_reverse| image:: ../_static/img/proxy_reverse.svg
   :class: wiki-img-sm
   :alt: OXL Docs - Reverse Proxy

.. |proxy_forward| image:: ../_static/img/proxy_forward.svg
   :class: wiki-img-sm
   :alt: OXL Docs - Forward Proxy

=========
1 - Intro
=========

.. include:: ../_include/wip.rst

Typen
*****

Die beiden gängigsten Arten von Proxys sind:

Forward
=======

Forward Proxies werden zum Abfangen und Filtern des Datenverkehrs verwendet.

In den meisten Fällen werden sie transparent in Netzwerk-Firewall-Systemen als Sicherheitsmaßnahme eingesetzt.

Um TLS-Verkehr abzufangen, implementieren einige dieser Proxys :ref:`TLS interception <proxy_tls_interception>`.

Es kann illegal sein, den Netzverkehr abzufangen! Informieren Sie sich über die für Sie geltenden Gesetze und Vorschriften.

Es ist auch ein Eingriff in die Privatsphäre der betroffenen Nutzer (falls welche betroffen sind).

|proxy_forward|

Reverse
=======

Reverse Proxies werden vor die Dienste geschaltet.

In der Praxis werden sie zum Lastausgleich, zur Redundanz, zur Hochverfügbarkeit und zur Terminierung des (Client-zu-Server-) TLS-Tunnels eingesetzt.

|proxy_reverse|
