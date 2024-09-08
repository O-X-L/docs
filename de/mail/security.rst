.. _mail_security:

.. include:: ../_include/head.rst

===================
Security & Spoofing
===================

.. include:: ../_include/wip.rst

Intro
#####

Technologisch gesehen ist jeder in der Lage, über jede E-Mail-Adresse E-Mails zu versenden. Es liegt in der **Verantwortung des Absenders und des Empfängers, die SPF-, DKIM- und DMARC-Protokolle korrekt zu konfigurieren**, um ihren E-Mail-Verkehr abzusichern.

Spoofing beschreibt den Akt, E-Mails für eine E-Mail-Adresse zu versenden, ohne dazu berechtigt zu sein.

In den meisten Fällen versucht der Angreifer, sich als jemand anderes auszugeben, um das Vertrauen des E-Mail-Empfängers zu gewinnen.

Zu den **Tricks der Angreifer** gehören unter anderem:

* Verwendung des :code:`Anzeigenamens` von E-Mails, um illegale Absender zu verbergen, da dieser Anzeigename der primäre Name ist, der den Empfängern angezeigt wird.

  Beispiel: :code:`Deine Vorgesetzte <xyz@gmail.com>`

* Verwendung `augenscheinlich gleicher Domains <https://en.wikipedia.org/wiki/IDN_homograph_attack>`_ zur Täuschung von Empfängern.

  Beispiel: :code:`yahoo.com (correct) VS yаhoo.com (fake)`

Siehe auch: `Cloudflare Blog - Email spoofing <https://www.cloudflare.com/learning/email-security/what-is-email-spoofing/>`_

----

SPF
###

**Sender Policy Framework**

* E-Mail **Absender** müssen es in ihren DNS-Einträgen konfigurieren
* E-Mail **Empfänger** müssen die SPF-Prüfung auf ihren E-Mail-Servern aktivieren


SPF ist im `RFC 7208 <https://tools.ietf.org/html/rfc7208>`_ definiert.

Der SPF-Datensatz beschreibt, welche Server autorisiert sind, als diese Domäne zu senden, indem Mechanismen zur Identifizierung autorisierter IP-Adressen und Hostnamen verwendet werden, oder sogar die SPF-Datensätze anderer Domänen einbezogen werden.

SPF kann E-Mail-Spoofing nicht verhindern. Es macht es für Angreifer nur etwas schwieriger.

Er prüft den Inhalt des :code:`envelope from`, nicht den :code:`message from`-Header, den der empfangende Mail-Client sieht. Die SMTP-Transaktionen sind für den Empfänger nicht sichtbar, selbst wenn er die :code:`message headers` der Nachricht ansieht. Wenn die E-Mail von einem Mailserver oder -proxy weitergeleitet wird, wird sie invalidiert.

SPF Examples
************

Dies sind die zulässigen Attribute: :code:`ip4:<IP>`, :code:`ip6:<IP>`, :code:`mx`, :code:`a:<DNS>`, :code:`include:<DNS>`, :code:`redirect:<DNS>`, :code:`exists`

* Nur E-Mails von Ihrem Mailserver zulassen, alle anderen ablehnen.

    .. code-block:: bash

        Record: o-x-l.com
        Type:   TXT
        Value:  v=spf1 mx -all

* E-Mails von Ihrem Mailserver und einem Cloud-Dienst zulassen, alle anderen ablehnen.

    .. code-block:: bash

      Record: o-x-l.com
      Type:   TXT
      Value:  v=spf1 mx include:amazonses.com -all


* Für DNS-Einträge, die nicht zum Versenden von E-Mails verwendet werden, sollten Sie immer alle verweigern! Andernfalls könnte jemand diese ausnutzen, um Spoofing-Mails zu versenden.

    .. code-block:: bash

        Record: *.o-x-l.com
        Type:   TXT
        Value:  v=spf1 -all

  Wir haben auch schon Spoofing-Versuche gesehen, bei denen DNS-Einträge verwendet wurden, die nicht für Mailing-Dienste genutzt werden. Sie sollten auch für diese ein SPF-deny konfigurieren.

    .. code-block:: bash

        Record: www.o-x-l.com
        Type:   A
        Value:  <IP OF WEB SERVICE>

        Record: www.o-x-l.com
        Type:   TXT
        Value:  v=spf1 -all


Limits
******

SPF-Datensätze sind ungültig, wenn es mehr als 10 :code:`include` (rekursiv) gibt! Dies kann besonders knifflig sein, wenn Sie einige Cloud-Anbieter nutzen, die intern bereits mehrere Includes verwenden.

----

DKIM
####

**DomainKeys Identified Mail**

* Der **Absender** muss ein Public/Private Key-Pair erstellen, das mit einem :code:`selector` identifiziert wird.
* Der **Absender** muss den Versanddienst so konfigurieren, dass die E-Mails mit seinem privaten Schlüssel signiert werden.
* Der **Absender** muss den öffentlichen Schlüssel in einem DNS-Eintrag veröffentlichen.
* Der **Empfänger** muss die DKIM-Prüfung auf seinem E-Mail-Server aktivieren.

DomainKeys Identified Mail ist ein Standard für die Authentifizierung von E-Mail-Nachrichten, der im `RFC 6376 <https://tools.ietf.org/html/rfc6376>`_ definiert ist.

DKIM authentifiziert die :code:`message headers` und nicht die :code:`SMTP headers`, so dass die DKIM-Authentifizierung auch dann gültig bleibt, wenn die Nachricht von einem Mail-Server oder -Proxy weitergeleitet wird.

Es gibt einige Angriffsvektoren auf dieses Protokoll - wie `DKIM forging <https://github.com/chenjj/espoofer>`_. Die Implementierung von DMARC kann Angriffe verhindern, die eine Überschreibung des Parameters :code:`d` ausnutzen.


DKIM Examples
*************

* Der Schlüsselpaar-Selektor lautet :code:`mail123`.

    .. code-block:: bash

        Record: mail123._domainkey.o-x-l.com
        Type:   TXT
        Value:  v=DKIM1;k=rsa;t=s;s=<SERVICE>;p=<PUBLIC-KEY-B64>

* Vollständiges Beispiel:

    .. code-block:: bash

        test._domainkey.oxl.at TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC0BtDBbXYRNcft4d6LeTGkybsxc1JVXxZ2hJHDteHhU7TUfQGq2MqcsegVU97l6THb8VZxv7hWKCFSXwLh1QHRAVB9bxVFbu08cI9OMPpfvjq2XyVdY6D1lRD36emn4Mk9F6kIb5apP6QQtFPvMsX/15NZLZ/pr+G2DHl3TfG7vQIDAQAB"


Generate Key-Pair
*****************

.. code-block:: bash

    openssl genrsa -out mail.key 2048
    chmod 600 mail.key
    openssl rsa -in mail.key -pubout > mail.crt
    cat mail.crt | tr -d '\n'

Kopiere den Public-Key (*ohne Prefix/Appendix*).

----

DMARC
#####

**Domain-based Message Authentication, Reporting and Conformance**

* Der **Absender** muss einen DMARC DNS-Eintrag veröffentlichen.
* Die **Empfänger** müssen die DMARC-Überprüfung auf ihren E-Mail-Servern aktivieren.

Der Standard ist im `RFC 7489 <https://www.rfc-editor.org/rfc/rfc7489>`_ definiert.

DMARC stellt sicher, dass die SPF- und DKIM-Authentifizierungsmechanismen tatsächlich gegen dieselbe Basisdomäne authentifiziert werden, die der Endbenutzer sieht.

Reporting
*********

Sie können :code:`rua` (aggregiert) und :code:`ruf` (forensisch) zu Ihrem DMARC-Eintrag hinzufügen, um von den empfangenden E-Mail-Systemen Berichte über Ihre Zustellungsstatistiken zu erhalten.

Dies ist sehr nützlich, um Einblicke in den Zustand Ihrer E-Mail-Flüsse zu erhalten. Es zeigt Ihnen auch, ob jemand Ihre E-Mail-Domäne fälscht.

**Beispiel**: :code:`rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc@o-x-l.com`

Sie können Tools wie `parsedmarc <https://github.com/O-X-L/dmarc-analyzer>`_ verwenden, um Statistiken über mögliche Mailing-Probleme zu erhalten, die Sie haben.

DMARC Examples
**************

Mögliche **Richtlinien**: :code:`none` (reporting/warning), :code:`quarantine`, :code:`reject`

* Fügen Sie zunächst einen DMARC-Eintrag im reinen Berichtsmodus hinzu.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=none; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1;

* Erzwingen Sie den DMARC-Abgleich und verschieben Sie alle anderen Nachrichten aus dieser Domäne in die Quarantäne des Empfängers.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1;

* Stellen Sie den SPF- und DKIM-Abgleich auf streng ein.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1; adkim=s; aspf=s;

* Hinzufügen einer Subdomain-Richtlinie.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1; adkim=s; aspf=s; sp=quarantine;

.. include:: ../_include/user_rath.rst
