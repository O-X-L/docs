.. _security_encryption:

.. include:: ../_include/head.rst


==========
Encryption
==========

.. include:: ../_include/wip.rst

Intro
#####

Grundsätzlich wird zwischen **In-Transit** und **At-Rest** Verschlüsselung unterschieden.

Siehe auch: `RedHat - Encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-security_guide-encryption>`_

----

In Transit (asymmetric)
#######################

Die Verschlüsselung des Datenverkehrs über das Netz kann durch die Verwendung von TLS (*über TCP/UDP*) oder `QUIC <https://blog.cloudflare.com/the-road-to-quic/>`_ (*vorerst über UDP*) erreicht werden.

Diese Art der asymmetrischen Verschlüsselung erfordert :ref:`Zertifikate <security_certificates>` (*Public/Private KeyPairs*).

Wenn wir von SSL sprechen, meinen wir eigentlich `TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`_. SSL ist veraltet, da seine letzte Version 'SSLv3' sehr alt und anfällig für viele Angriffe ist.

Siehe auch: `Cloudflare - What is SSL <https://www.cloudflare.com/learning/ssl/what-is-ssl/>`_, `Cloudflare - TLS handshake <https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/>`_


----

At Rest (symmetric)
###################

Bei der symmetrischen Verschlüsselung wird ein privater Schlüssel zur Ver- und Entschlüsselung von Daten verwendet.

Dies wird häufig für die Verschlüsselung von Daten im Ruhezustand auf der Platte verwendet.

Diese Art der Verschlüsselung kann sehr nützlich sein, wenn Sie Geräte haben, die Sie nicht physisch vor dem Zugriff anderer schützen können. Beispiele hierfür sind: Server in einem verwalteten Rechenzentrum, mobile Geräte wie Laptops oder Smartphones, Sicherungen die außer Haus gebracht werden

Beispiele: `Linux LUKS disk encryption <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/security_hardening/encrypting-block-devices-using-luks_security-hardening>`_, `Android Encryption <https://source.android.com/docs/security/features/encryption>`_, `Microsoft Windows Bitlocker <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/>`_
