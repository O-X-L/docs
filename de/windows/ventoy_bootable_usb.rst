.. _windows_ventoy_bootable_usb:

.. include:: ../_include/head.rst

==============================
Bootbarer USB-Stick via Ventoy
==============================


Intro
#####

Für einige technische Tätigkeiten muss ein Computer/Server von einem spezifischen ISO gestartet/-bootet werden.

In der Regel nutzt man bootbare USB-Sticks für einen solchen Zweck.

Das Tool `Ventoy <https://github.com/ventoy/Ventoy>`_ kann dazu genutzt werden um mehrere ISO-Dateien und gegebenenfalls zusätzliche Daten auf einem USB-Stick abzulegen.

Zusätzlich zu dieser nützlichen Funktionalität ist die Installation sehr einfach.

----

Nutzung
#######

Zur Erstellung eines bootbaren USB-Sticks empfehlen wir das Multi-Boot-Tool 'Ventoy':
* `Download Ventoy <https://sourceforge.net/projects/ventoy/files/>`_
* `Getting-Started Documentation <https://www.ventoy.net/en/doc_start.html>`_
* `GitHub - Project <https://github.com/ventoy/Ventoy>`_

Installation:
* Installations-Anwendung herunterladen
* Entpacken
* Einen USB-Stick anstecken, **dessen Inhalt gelöscht** werden kann!
* Die Applikation :code:`Ventoy2Disk` ausführen
* Den USB-Stick auswählen und Ventoy auf dem Stick installieren
* Der USB-Stick sollte danach wieder über den File-Explorer verfügbar sein - sonst einmal aus- & einstecken
* Bootbare ISO-Dateien auf den USB-Stick kopieren

Nun sollte es beim Neustart des Computers möglich sein über das BIOS-Bootmenü den USB-Stick auszuwählen.

Ventoy zeigt danach eine Liste der verfügbaren ISO-Dateien an. Einfach via Tastatur auswählen und 'normal' starten auswählen.

.. include:: ../_include/user_rath.rst
