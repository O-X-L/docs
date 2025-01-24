.. _security_certs:

.. include:: ../_include/head.rst

.. |pki| image:: ../_static/img/security_certificates_pki.svg
   :class: wiki-img-lg
   :alt: OXL Docs - Public Key Infrastructure & x509 Certificates

===========
Zertifikate
===========

.. include:: ../_include/wip.rst

Intro
#####

Die derzeit verwendeten Arten von Zertifikaten sind als `X.509 <https://en.wikipedia.org/wiki/X.509>`_ bekannt.

x509-Zertifikate haben einen öffentlichen und einen privaten Schlüssel.

Wenn Sie auf einen Dienst zugreifen, können Sie und Ihr Gerät dessen öffentlichen Schlüssel sehen. Wenn der Dienst so konfiguriert ist, zeigt er Ihnen auch die öffentlichen Schlüssel der übergeordneten Stellen innerhalb der Zertifikatshierarchie/Trust-Chain an.

Beispiel: `Firefox <https://support.mozilla.org/en-US/kb/secure-website-certificate>`_

Die **privaten Schlüssel müssen sicher aufbewahrt werden**! Andernfalls können sich Angreifer als Ihr Dienst ausgeben und Zugang zu sensiblen Informationen erhalten!

Siehe auch: `Cloudflare - What is an SSL certificate <https://www.cloudflare.com/learning/ssl/what-is-an-ssl-certificate/>`_

----

Attribute
#########

Common Name
***********

Der CN ist der 'schöne Name' des Zertifikats, den die Benutzer als erstes sehen, wenn sie dieses prüfen.

Sie können den Namen Ihres Unternehmens und eine kurze Beschreibung des Dienstes, für den es verwendet wird, hinzufügen.

Beispiel: :code:`OXL - Documentation`

Subject Alternative Names
*************************

Wenn ein Dienst über TLS zugänglich ist, erfolgt der Zugriff entweder über einen DNS-Namen oder eine IP-Adresse.

Das SAN ist eine Liste von DNS/IP/EMAIL-Werten, die für dieses spezifische Zertifikat gültig sind. Das SAN ist eine Sicherheitsmaßnahme, die sicherstellt, dass ein geleakter privater Schlüssel nicht für irgendeinen Dienst missbraucht werden kann.

Beispiel: :code:`DNS:www.OXL.at,DNS:www.O-X-L.com,IP:1.1.1.1`

Es ist wichtig, dieses Attribut korrekt zu setzen, da es validiert wird!

----

.. _security_certs_pki:

Public Key Infrastructure & Trust Chains
########################################

**Sicherheit ist sehr wichtig**, wenn es um Zertifikats-Trust-Chains geht!

Wenn eine Trust-Chain ausgenutzt wird, ist der Angreifer in der Lage, :ref:`alle Ihre SSL/TLS-Verbindungen aufzubrechen <proxy_tls_interception>`!

Eine PKI baut eine Trust-Chain auf.

* Geräte und Benutzer vertrauen der Root-CA
* Die Root-CA signiert eine Sub-CA, kennzeichnet sie als vertrauenswürdig und ermöglicht ihr, selbst Zertifikate zu signieren
* Die Sub-CA ist in der Lage, Zertifikate für den Endverbraucher zu signieren (*Benutzer/Clients/Server/Dienste/Software*)
* Alle Benutzer, die der Root-CA vertrauen, vertrauen auch den Zertifikaten für den Endverbraucher.
* `Certificate revocation lists  <https://en.wikipedia.org/wiki/Certificate_revocation_list>`_ werden verwendet, um den Widerruf von Zertifikaten zu ermöglichen (*für den Fall, dass sie geleaked/missbraucht/... wurden*)

|pki|

Siehe auch: `EasyRSA Docs <https://easy-rsa.readthedocs.io/en/latest/intro-to-PKI/>`_

----

Trust-Store
***********

Debian-based Linux
==================

**Store**: :code:`/etc/ssl/certs/ca-certificates.crt`

**Installation**: :code:`apt -y install ca-certificates`

**CAs zum Trust-Store hinzufügen**:

.. code-block:: bash

    # add ca public-key with .crt extension to /usr/share/ca-certificates/
    sudo update-ca-certificates

Windows
=======

Siehe: `learn.microsoft.com <https://learn.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate>`_

----

Öffentliche vs Interne CAs
##########################

Öffentliche
***********

Öffentliche CAs sind technisch gesehen gleich wie Private. Nur werden sie in den Standard-Trust-Store vieler Geräte aufgenommen.

Als Endnutzer sind wir bei der Verwendung öffentlicher CAs stark eingeschränkt. Die meisten Anbieter erlauben nur die Erstellung von Zertifikaten für bestimmte Anwendungsfälle wie :code:`Serverzertifikat`, :code:`Benutzerzertifikat` und :code:`Digital Signing Certificate`. Dies ist in den meisten Fällen ausreichend, aber einige Edge-cases erfordern erweiterte Zertifikatstypen wie :code:`untergeordnete Zertifizierungsstelle` (:ref:`TLS-Überprüfung <proxy_tls_interception>`).

Nur wenige Zertifikatsanbieter wie `LetsEncrypt <https://letsencrypt.org/>`_ erlauben es Ihnen, Zertifikate kostenlos zu erstellen. Die meisten Anbieter haben eine **Gebühr** zu entrichten.

Nicht alle Anbieter öffentlicher Zertifikate erlauben die **nicht-interaktive** Erstellung/Aktualisierung von Zertifikaten. Dies ist ein häufiger Anwendungsfall, wenn Sie :ref:`IT Automation <atm_intro>` einsetzen!

----

Interne
*******

Wenn Sie die volle Kontrolle haben wollen, können Sie eine interne CA einrichten!

**Dafür müssen Sie**:

* Sicherstellen, dass Ihre PKI gut konzipiert ist
* Die Root-CA (*private-key*) aus Sicherheitsgründen offline nehmen
* **Certificate Revocation Lists** implementieren, damit Sie bestehende Zertifikate und Sub-CAs widerrufen können
* Fügen Sie den Public-Key Ihrer Root-CA in den Vertrauensspeicher Ihrer Geräte ein, damit diese Ihrer PKI vertrauen
* Sichern Sie den Server, auf dem die PKI liegt, stark ab um sicherzustellen, dass das Vertrauen nicht missbraucht wird.
* Sichern Sie die Private-Keys Ihrer Zertifikate ab.

Beispeile zur Erstellung: `EasyRSA <https://github.com/OpenVPN/easy-rsa>`_, `Ansible Role <https://github.com/ansibleguy/infra_pki>`_, `Microsoft AD Certificate Services <https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/install-the-certification-authority>`_, `Hashicorp Vault <https://developer.hashicorp.com/vault/tutorials/secrets-management/pki-engine>`_

Best practices: `AWS <https://docs.aws.amazon.com/privateca/latest/userguide/ca-hierarchy.html>`_, `Microsoft AD Certificate Services <https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/pki-design-considerations>`_

----

.. _security_certs_verify:

Verifizierung
#############

Es gibt Möglichkeiten für Angreifer, :ref:`Trust-Chains auszunutzen und so die Verschlüsselung zu brechen<proxy_tls_interception>`.

Um einen Angreifer von einer solchen `Man-in-the-Middle attack <https://en.wikipedia.org/wiki/Man-in-the-middle_attack>`_ abzuhalten, gibt es Möglichkeiten, eine TLS-Verifizierung zu erzwingen.

Wenn eine aktive Prüfung fehlschlägt, wird auch die Verbindung abgebrochen.

Trust-Store
***********

Diese Überprüfung ist standardmäßig eingeschaltet und sollte nicht deaktiviert werden.

Sie aktiviert die grundlegenden Überprüfungen der Vertrauenskette wie oben beschrieben.

Die meisten Programme verwenden den systemweiten Vertrauensspeicher für diese Überprüfung.

Wenn ein Angreifer in der Lage war, seine eigene CA in diesen Speicher einzufügen, wird diese Prüfung kein Problem finden.

Subject Alternative Names
*************************

Diese Überprüfung ist standardmäßig eingeschaltet und sollte nicht deaktiviert werden.

Sie überprüft, ob der DNS-Name oder die IP-Adresse, die wir für den Zugriff auf den Dienst verwenden, im SAN des Zertifikats aufgeführt ist.

Spezifische Attribute
*********************

Manche Software, wie OpenVPN, ermöglicht es Ihnen, das Peer-Zertifikat anhand anderer Zertifikatsattribute zu überprüfen.

Zum Beispiel können wir prüfen, ob das Attribut Common-Name mit einer bestimmten Zeichenfolge übereinstimmt.

Nur spezifischer CA vertrauen
*****************************

Datenschutz- oder sicherheitsrelevante Software implementiert manchmal eine Prüfung, die sicherstellt, dass das Peer-Zertifikat von einer bestimmten Zertifizierungsstelle signiert ist. Diese Zertifizierungsstelle wird in der clientseitigen Anwendung fest kodiert.

In diesem Fall ignoriert die Software den Trust-Store des Systems.

Wir sehen dieses Verhalten bei Bankanwendungen.

Dies ist die einzige Möglichkeit, um sicherzustellen, dass die Verbindung zwischen Client und Server nicht von einer dritten Partei inspiziert wird.

.. include:: ../_include/user_rath.rst
