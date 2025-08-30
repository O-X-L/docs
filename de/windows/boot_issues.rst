.. _windows_boot_issues:

.. include:: ../_include/head.rst

============================
Windows: Fehler beim Starten
============================

Intro
#####

In der Praxis kann es schwer sein herauszufinden was die genaue Fehlerquelle ist, wenn Windows nicht mehr startet.

In dieser Dokumentation gehen wir auf einige solcher Fehlerquellen ein!


.. warning::

    Diese Dokumentation dient jeglich als Sammlung von Informationen.

    Wir empfehlen dass solche Wiederherstellungs-Aktionen nur von Techniker:innen mit der nötigen Ausbildung durchgeführt werden.

    Vor solchen Wiederherstellungs-Aktionen sollte immer eine Gesamtsicherung der Festplatten im betroffenen System durchgeführt werden!

    Sie sind selbst dafür verantwortlich diese Informationen richtig zu interpretieren und anzuwenden!



----

Windows UEFI Boot-Vorgang
#########################

Die zwei Boot-Typen UEFI und Legacy verhalten sich etwas unterschiedlich.

In der Regel nutzen aktuelle System UEFI!


1. Computer POST
================

Hier testet das BIOS des Computers die Hardware (CPU, Arbeitsspeicher, Grafikkarte) auf Fehler.

**Fehlerbild**:

* Bei einem POST-Fehler wird meist kein Bild angezeigt - mache Geräte biepsen auch.

* Das genaue Verhalten hängt vom Mainboard-Hersteller ab.

**Problembehebung**:

* Wenn es bereits hier einen Fehler gibt, müssen die physischen Komponenten des System geprüft werden. Meist durch testweisen Austausch oder Ausbau.

----

2. BIOS Boot / UEFI Firmware Initialization
===========================================

Es wird nach Bootoptionen gesucht und diese werden laut konfigurierter Priorität probiert.

Wenn der Windows-Boot richtig funktioniert wird von der Option :code:`Windows Boot Manager` gestartet.

Zu diesem Zeitpunkt haben Sie die Möglichkeit ins BIOS-Bootmenü oder -Setup Ihres Computers zu wechseln. Meist müssen dazu Funktions-Tasten in schneller Abfolge gedrückt werden (Bsp: Dell = F12, HP = F9)

**Fehlerbild**:

* Es wird angezeigt, dass keine Bootoptionen verfügbar sind

* Der Computer startet in eine andere Boot-Option, wie den Netzwerk-Boot

**Problembehebung**:

* Die System-Festplatte sollte auf Fehler geprüft werden - möglicherweise ist diese komplett defekt (*wie z.B. im August 2025 durch die Windows-Updates KB5063878 und/oder KB5062660 ausgelöst*; siehe: `Reddit <https://www.reddit.com/r/msp/comments/1n1sgxx/windows_11_update_kb5063878_causing_ssd_failures/>`_)

* Über das `Windows Recovery-Environment <windows_boot_issues_action_winre>`_ die System-Start-Problembehebung ausführen (*funktioniert leider meist nicht*)

* :ref:`Die EFI-Daten aktualisieren <windows_boot_issues_action_efi_bcd>`

* :ref:`Die EFI-Partition neu erstellen <windows_boot_issues_action_efi_partition>`

----

3. Windows Boot Manager
=======================

  Hier befindet sich der Boot-Prozess nun auf der 100MB großen Windows EFI-Partition.

  Es wird die Datei :code:`\\EFI\\Microsoft\\Boot\\bootmgfw.efi` geladen.

  **Fehlerbild**:

  * Windows startet direkt in das Recovery-Environment

  * Windows startet in die EFI-Shell

  **Problembehebung**:

  * Über das `Windows Recovery-Environment <windows_boot_issues_action_winre>`_ die System-Start-Problembehebung ausführen (*funktioniert leider meist nicht*)

  * :ref:`Die EFI-Daten aktualisieren <windows_boot_issues_action_efi_bcd>`

  * :ref:`Die EFI-Partition neu erstellen <windows_boot_issues_action_efi_partition>`

----

4. BCD - Boot Configuration Data
================================

  Es wird die Datei :code:`\\EFI\\Microsoft\\Boot\\BCD` geladen.

  Diese beinhaltet die Information, auf welcher Partition sich das Windows-System befindet, welches gestartet werden soll.

  **Fehlerbild**:

  * Windows startet direkt in das Recovery-Environment

  * Windows startet in die EFI-Shell

  **Problembehebung**:

  * Über das `Windows Recovery-Environment <windows_boot_issues_action_winre>`_ die System-Start-Problembehebung ausführen (*funktioniert leider meist nicht*)

  * :ref:`Die EFI-Daten aktualisieren <windows_boot_issues_action_efi_bcd>`

  * :ref:`Die EFI-Partition neu erstellen <windows_boot_issues_action_efi_partition>`

----

5. Windows OS Loader
====================

  Hier befindet sich der Boot-Prozess nun auf der Windows-System-Partition.

  Es wird die Datei :code:`C:\\Windows\\System32\\winload.efi` geladen.

  **Fehlerbild**:

  * Windows startet direkt in das Recovery-Environment

  **Problembehebung**:

  * Das :ref:`Windows-System über das Recovery-Environment auf Fehler prüfen <windows_boot_issues_action_sfc_chkdsk>`

----

6. Windows OS Loader
====================

  Es wird die Datei :code:`C:\\Windows\\System32\\ntoskrnl.exe` (das wirkliche Windows-Betriebssystem) geladen.

  **Fehlerbild**:

  * Windows startet direkt in das Recovery-Environment

  **Problembehebung**:

  * Das :ref:`Windows-System über das Recovery-Environment auf Fehler prüfen <windows_boot_issues_action_sfc_chkdsk>`

----

7. Laden der Treiber
====================

  Bis zu diesem Zeitpunkt nutzte der Boot-Prozess generische Treiber.

  Nun werden die spezifischen Treiber, die innerhalb des Windows-Betriebssystems installiert wurden, laut Windows-Registry und :code:`C:\\Windows\\system32\\drivers\\` geladen.

  **Fehlerbild**:
  * Falls die Storage-/Festplatten-Treiber für die System-Festplatte nicht korrekt geladen werden sieht man ein: `INACCESSIBLE_BOOT_DEVICE`
  * Es wird angezeigt, dass gewisse System-Treiber nicht gefunden wurden

  **Problembehebung**:
  * Im Fall von `INACCESSIBLE_BOOT_DEVICE` kann die BIOS-Einstellung zur Umschaltung zwischen **RAID und AHCI** Storage-Modus schuld sein!
    Das Windows-System kann nur in dem Storage-Modus gebootet werden, in dem es installiert wurde.
    Klassischerweise sieht man diese Meldung, wenn man eine Vollsicherung eines Computers auf einen anderen wiederherstellt.

  * Das :ref:`Windows-System über das Recovery-Environment auf Fehler prüfen <windows_boot_issues_action_sfc_chkdsk>`

  * Wenn andere Treiber nicht gefunden werden, kann es komplizierter werden.. :(

----

Wiederherstellungs-Aktionen
###########################

.. _windows_boot_issues_action_winre:

Windows Recovery-Environment (WINRE)
====================================

Siehe auch: `Microsoft Documentation <https://support.microsoft.com/en-us/windows/windows-recovery-environment-0eb14733-6301-41cb-8d26-06a12b42770b>`_

Normalerweise wird bei der Installation von Windows (10/11) automatisch am Ende der System-Festplatte eine Wiederherstellungs-Partition erstellt, welche dieses WINRE Bereitstellt.

Manchmal kann der Zugriff auf diese jedoch nicht möglich sein. In solchen Fällen wird hierzu ein Windows-Installationsmedium (ISO) und ein bootbarer USB-Stick nötig sein.

**Download** eines Windows Installations-Medium:
* `Windows 11 <https://www.microsoft.com/en-us/software-download/windows11>`_
* `Windows 10 <https://www.microsoft.com/software-download/windows10>`_
* `Windows Server <https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022>`_

Zur Erstellung eines **bootbaren USB-Sticks** empfehlen wir das :ref:`Multi-Boot-Tool Ventoy <windows_ventoy_bootable_usb>`

----

.. _windows_boot_issues_action_sfc_chkdsk:

Windows System-Partition überprüfen
===================================

1. Den Computer in eine :ref:`Windows-Recovery Umgebung starten <windows_boot_issues_action_winre>`

2. Unter den erweiterten Optionen die Kommandozeile (cmd) auswählen

3. Verifizieren dass die Windows System-Partition existiert

.. code-block:: cmd

    # auf die Festplatte mit dem Buchstaben C wechseln
    C:

    # die Ordner und Dateien darin anzeigen
    dir

    # es sollten einige Ordner wie 'Windows', 'Program Files', 'Users' gelistet werden
    # wenn dem nicht der Fall ist => andere Laufwerksbuchstaben durchprobieren!
    # Laufwerksbuchstaben merken!
    # falls die Windows System-Partition gar nicht gefunden werden kann, könnte es sich um einen Komplett-Ausfall der Festplatte handeln

4. Die System-Partition auf Fehler prüfen und diese gegebenenfalls reparieren:

.. code-block:: cmd

    # wenn nötig 'C:' mit Ihrem 'Windows System-Partition' Laufwerksbuchstaben austauschen!

    # System-Dateien überprüfen
    sfc /scannow /offbootdir=C:\ /offwindir=C:\Windows

    # System-Partition auf Fehler prüfen
    chkdsk /f /r C:

5. Mit :code:`exit` aussteigen und den Computer neu starten

----

.. _windows_boot_issues_action_efi_bcd:

EFI-Daten aktualisieren (BCD)
=============================

1. Den Computer in eine :ref:`Windows-Recovery Umgebung starten <windows_boot_issues_action_winre>`

2. Unter den erweiterten Optionen die Kommandozeile (cmd) auswählen

3. Verifizieren dass die Windows System-Partition existiert

.. code-block:: cmd

    # auf die Festplatte mit dem Buchstaben C wechseln
    C:

    # die Ordner und Dateien darin anzeigen
    dir

    # es sollten einige Ordner wie 'Windows', 'Program Files', 'Users' gelistet werden
    # wenn dem nicht der Fall ist => andere Laufwerksbuchstaben durchprobieren!
    # Laufwerksbuchstaben merken!
    # falls die Windows System-Partition gar nicht gefunden werden kann, könnte es sich um einen Komplett-Ausfall der Festplatte handeln

4. Nun muss die EFI-Partition gefunden und gemounted werden

.. code-block:: cmd

    # die Festplatten-Verwaltung starten
    diskpart

    # alle Festplatten anzeigen
    list disk

    # die Festplatte, auf der Windows installiert ist, via Nummer auswählen
    select disk N

    # alle Partitionen anzeigen
    list partition

    # die 100MB große EFI-Partition via Nummer auswählen
    select partition N

    # Laufwerks-Buchstaben 'V' zuweisen
    assign letter V

    # von der Festplatten-Verwaltung aussteigen
    exit

5. Nun aktualisieren wir die EFI-Daten:

.. code-block:: cmd

    # wenn nötig 'C:' mit Ihrem 'Windows System-Partition' Laufwerksbuchstaben austauschen!

    bcdboot C:\Windows /s V: /f ALL

6. Mit :code:`exit` aussteigen und den Computer neu starten

----

.. _windows_boot_issues_action_efi_partition:

EFI-Partition neu erstellen
===========================

1. Stellen Sie sicher, dass eine Sicherung der System-Festplatten existiert!

2. Zuvor bitte immer :ref:`versuchen die EFI-Daten zu aktualisieren (BCD) <windows_boot_issues_action_efi_bcd>`_!

3. Den Computer in eine :ref:`Windows-Recovery Umgebung starten <windows_boot_issues_action_winre>`

4. Unter den erweiterten Optionen die Kommandozeile (cmd) auswählen

5. Verifizieren dass die Windows System-Partition existiert

.. code-block:: cmd

    # auf die Festplatte mit dem Buchstaben C wechseln
    C:

    # die Ordner und Dateien darin anzeigen
    dir

    # es sollten einige Ordner wie 'Windows', 'Program Files', 'Users' gelistet werden
    # wenn dem nicht der Fall ist => andere Laufwerksbuchstaben durchprobieren!
    # Laufwerksbuchstaben merken!
    # falls die Windows System-Partition gar nicht gefunden werden kann, könnte es sich um einen Komplett-Ausfall der Festplatte handeln

6. Nun muss die EFI-Partition gefunden und gemounted werden

.. code-block:: cmd

    # die Festplatten-Verwaltung starten
    diskpart

    # alle Festplatten anzeigen
    list disk

    # die Festplatte, auf der Windows installiert ist, via Nummer auswählen
    select disk N

    # alle Partitionen anzeigen
    list partition

    # die 100MB große EFI-Partition via Nummer auswählen
    select partition N

    # !!! ACHTUNG: stellen Sie sicher, dass Sie WIRKLICH DIE RICHTIGE PARTITION ausgewählt haben !!!
    list partition

    # LÖSCHEN der ausgewählten Partition
    delete partition override

    # Partition neu erstellen und formatieren
    create partition EFI
    format fs=FAT32 quick

    # Laufwerks-Buchstaben 'V' zuweisen
    assign letter V

    # von der Festplatten-Verwaltung aussteigen
    exit

7. Nun aktualisieren wir die EFI-Daten:

.. code-block:: cmd

    # wenn nötig 'C:' mit Ihrem 'Windows System-Partition' Laufwerksbuchstaben austauschen!

    bcdboot C:\Windows /s V: /f ALL

8. Mit :code:`exit` aussteigen und den Computer neu starten

----

Sicherung einer Festplatte auf Block-Ebene
==========================================

.. warning::

    Diese Aktion ist etwas komplexer und Sie könnten ungewollt Daten vernichten, wenn Sie nicht über die nötige technische Expertise verfügen!

1. Externen Speicher vorbereiten - z.B. eine externe USB-Festplatte oder ein Netzlaufwerk (SMB)

2. Ein Linux Live-ISO herunterladen - Beispeil: `Debian Live (standard) <https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/>`_

3. Einen bootbaren USB-Stick erstellen - wir empfehlen das :ref:`Multi-Boot-Tool Ventoy <windows_ventoy_bootable_usb>`

4. Linux-ISO auf den USB-Stick kopieren

5. Vom Linux-ISO booten

6. Sudo werden (höhere Berechtigungen)

  .. code-block:: bash

      sudo -i

7. Ziel-Speicher einbinden

  * Wenn USB-Festplatte:

    .. code-block:: bash

        # alle Festplatten auflisten
        lsblk -o +model

        # die USB-Festplatte mounten
        mkdir /mnt/backup
        mount /dev/sdX1 /mnt/backup

  * Wenn Netzlaufwerk:

    .. code-block:: bash

        # sicherstellen, dass wir eine Netzwerkverbindung haben (Netzwerkkabel)
        ip a
        ping 1.1.1.1

        # SMB-client installieren
        apt update
        apt install smbclient cifs-utils

        # das Netzlaufwerk mounten
        mkdir /mnt/backup
        mount -t cifs //<SERVER-IP>/<SERVER-SHARE> /mnt/backup -o username=<USER>

8. Zu-sichernde Festplatte finden

.. code-block:: bash

    # alle Festplatten auflisten (sollte /dev/sdX oder /dev/nvmeXnX sein)
    lsblk -o +model

    # Erstellung eines Abbildes der Festplatte (/dev/sdX auf Ihre Festplatte ändern)
    dd if=/dev/sdX of="/mnt/backup/$(date +%Y-%m-%d_%H-%M)_backup.bin" bs=100M status=progress
