.. _security_encryption:

.. include:: ../_include/head.rst


===============
Verschlüsselung
===============

.. include:: ../_include/wip.rst

.. warning::

    Dies soll nur eine kurze Einführung in die Verschlüsselung sein. Wir werden nicht auf die Details eingehen.


Intro
#####

Aus Sicht der praktischen Nutzung wird hauptsächlich zwischen **In-Transit** und **At-Rest** Verschlüsselung unterschieden.

Es gibt auch verschiedene Möglichkeiten, wie die Ver- und Entschlüsselung durchgeführt wird.

Wenn Sie Ihr Wissen über Kryptographie vertiefen wollen, können wir Ihnen `diese an einer deutschen Universität aufgenommenen Videos <https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX>`_ empfehlen

Wenn wir von SSL sprechen, meinen wir eigentlich `TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`_. SSL ist veraltet, da seine letzte Version 'SSLv3' sehr alt und anfällig für viele Angriffe ist.

Siehe auch:  `dev.to - Data encryption <https://dev.to/documatic/data-encryption-securing-data-at-rest-and-in-transit-with-encryption-technologies-1lc2>`_, `RedHat - Encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-security_guide-encryption>`_

----

Nutzung
#######

In Transit
**********

Die Verschlüsselung des Datenverkehrs über das Netz kann durch die Verwendung von TLS (*über TCP/UDP*) oder `QUIC <https://blog.cloudflare.com/the-road-to-quic/>`_ (*vorerst über UDP*) erreicht werden. TLS verwendet sowohl asymmetrische (*Sitzungsinitiierung*) als auch symmetrische (*Datenübertragung*) Verschlüsselung.

Einige Anwendungen, wie z. B. VPNs, können andere Protokolle zur Verschlüsselung ihres Datenverkehrs verwenden. Diese verwenden manchmal nur symmetrische Verschlüsselung.

Siehe auch: `Cloudflare - What is SSL <https://www.cloudflare.com/learning/ssl/what-is-ssl/>`_, `Cloudflare - TLS handshake <https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/>`_


----

At Rest
*******

Die symmetrische Verschlüsselung wird häufig für die Verschlüsselung von Daten im Ruhezustand auf der Festplatte verwendet, da der Schlüssel nicht über eine unsichere Verbindung übertragen werden muss.

Diese Art der Verschlüsselung kann sehr nützlich sein, wenn Sie Geräte haben, die Sie nicht physisch vor dem Zugriff anderer schützen können. Beispiele hierfür sind: Server in einem verwalteten Rechenzentrum, mobile Geräte wie Laptops oder Smartphones, Sicherungen die außer Haus gebracht werden.

Beispiele: `Linux LUKS file encryption <https://opensource.com/article/21/4/linux-encryption>`_, `Linux LUKS disk encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/security_hardening/encrypting-block-devices-using-luks_security-hardening>`_, `Android Encryption <https://source.android.com/docs/security/features/encryption>`_, `Microsoft Windows Bitlocker <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/>`_

----

Arten
#####

Symmetric
*********

Sie ist schneller als die asymmetrische Verschlüsselung.

Bei der symmetrischen Verschlüsselung wird ein privater Schlüssel zur Ver- und Entschlüsselung von Daten verwendet.

Wenn die symmetrische Verschlüsselung für die Verschlüsselung während der Übertragung verwendet wird, müssen Protokolle wie `Diffie-Hellman <https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange>`_ für den sicheren Austausch des privaten Schlüssels verwendet werden.

Asymmetric
**********

Es verwendet ein privates und öffentliches Schlüsselpaar zur Ver- und Entschlüsselung von Daten.

Dadurch entfällt die Notwendigkeit, einen privaten Schlüssel auszutauschen, wenn er für die Verschlüsselung während der Übertragung verwendet wird.

Der häufigste Anwendungsfall für diese Art der Verschlüsselung ist :ref:`TLS via Zertifikaten <security_certs>`.

.. include:: ../_include/user_rath.rst
