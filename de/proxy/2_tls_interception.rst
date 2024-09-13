.. _proxy_tls_interception:

.. include:: ../_include/head.rst

.. |intercept| image:: ../_static/img/proxy_tls_interception.svg
   :class: wiki-img
   :alt: OXL Docs - TLS Interception

====================
2 - TLS Interception
====================

Intro
#####

Beim Senden von Klartextverkehr über ein Netz kann jeder böswillige Akteur diesen abfangen/lesen/verändern. Der Kunde wird von diesem Eindringen nichts erfahren.

Wenn der Datenverkehr verschlüsselt ist (derzeit mit TLS), ist dies nicht möglich, da der Datenverkehr für Dritte nicht lesbar ist. Nur der Client und der Server, die den verschlüsselten 'Tunnel' aufbauen, wissen, welcher Verkehr gesendet und empfangen wird.

Um ein Abfangen des verschlüsselten Datenverkehrs zu ermöglichen, muss ein `Man-in-the-Middle-Angriff <https://en.wikipedia .org/wiki/Man-in-the-middle_attack>`_ durchgeführt werden. In diesem Fall baut der Client eine verschlüsselte Verbindung zum Mittelsmann auf, der sich seinerseits mit dem eigentlichen Zielserver verbindet.

Zum Schutz vor solchen Angriffen ist der TLS-Handshake nur dann erfolgreich, wenn das `Serverzertifikat <https://www.cloudflare.com/learning/ssl/how-does-ssl-work/>`_ von einer **vertrauenswürdigen Zertifizierungsstelle** signiert ist und einen gültigen **Subject Alternative Name** aufweist, der den tatsächlichen Server-/Dienstenamen enthält. Dieser Schutz ist als :ref:`SSL/TLS-Verifizierung <security_certs_verify>` bekannt.

Um diesen Schutz zu umgehen, muss der abfangende Proxy Zugang zu einer Zertifikatsautorität haben, der der Client vertraut. Unternehmen würden :ref:`eine interne PKI <security_certs_pki>` verwenden, um eine solche Zertifikatsvertrauenskette zu erstellen.

|intercept|

Einige Länder fangen den gesamten Verkehr ihrer öffentlichen Netze ab, da sie über Gesetze verfügen, die ihnen das Recht dazu einräumen. Auf diese Weise sind sie in der Lage, den Netzverkehr bzw. die Anfragen abzuhören und zu verändern/zensieren.


----

SNI Sniffing
############

Alternativ zum vollständigen Aufbrechen von TLS kann man den Ziel-Hostnamen aus der `TLS SNI-Erweiterung <https://www.cloudflare.com/learning/ssl/what-is-sni/>`_ auslesen, da er im Klartext übertragen wird, während der TLS-Handshake durchgeführt wird. Clients und Server sind sich dieser Art des Sniffings nicht bewusst.

Der Standard für `encrypted SNI <https://www.cloudflare.com/learning/ssl/what-is-encrypted-sni/>`_ soll dieses Informationsleck beheben. Einige Staaten wie China und Russland haben Berichten zufolge damit begonnen, alle ESNI-TLS-Handshakes zu blockieren.

.. include:: ../_include/user_rath.rst
