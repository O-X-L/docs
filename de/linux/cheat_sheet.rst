.. _linux_cheat_sheet:

.. include:: ../_include/head.rst

===================
Command Cheat Sheet
===================


Allgemeine Shell-Nutzung
########################

Verweis auf das letzte Wort des letzten Befehls: :code:`!$`

Verweis auf den Exit-Code des letzten Befehls: :code:`$?`

Pfad zur ausführbaren Datei abrufen: :code:`which EXE`

String in Dateien rekursiv suchen: :code:`grep -r 'SearchString'`

Befehl als anderer Benutzer ausführen: :code:`su --shell /bin/bash -c '$COMMAND' $USER`

Interaktive Shell im Kontext eines anderen Benutzers starten: :code:`su --login --shell /bin/bash $USER`

Unterschiede zwischen den Verzeichnisinhalten anzeigen: :code:`diff --recursive --unified=3 --color before/vars/ vars/`

Unterschiede mit Farben loggen: :code:`unbuffer diff --recursive --unified=3 --color before/vars/ vars/ | tee log.txt`

Datetime-String in Zeitstempel umwandeln: :code:`date -d "$(get datetime string here)" +"%s"`

Suchen und Ersetzen von Strings in Dateien: :code:`sed -i 's|FIND_REGEX|REPLACE|g' FILE`

Suchen und Ersetzen von Zeichenfolgen in Dateien unter Verwendung von Variablen:

.. code-block::

    FIND_REGEX='my regex'
    REPLACE='replace'

    sed -i "s|$FIND_REGEX|$REPLACE|g" FILE

APT Update eines einzelnen Paketes: :code:`sudo apt-get --only-upgrade install PKG`

SSH-Schlüssel erstellen: :code:`ssh-keygen -t ed25519 -C 'comment'`

Die letzten 100 logs eines Systemd-Dienstes abrufen: :code:`journalctl -u SERVICE.service --no-pager -n 100`

Postfix-Log-Übersicht generieren: :code:`pflogsumm -u 50 -h 50 -i --verbose-msg-detail mail.log mail.log.? > mail_report.log`

Letzte Anmeldungen abrufen: :code:`last`, :code:`lastlog`

Aktuelle offene Benutzersitzungen abrufen: :code:`w`

Schneller Überblick über Source-Code: :code:`cd <REPO_BASE> && cloc`

----

Ressourcenmanagement
####################

Größe des Verzeichnisses abfragen: :code:`du -sh DIR`

Größe der Unterverzeichnisse eines Verzeichnisses ermitteln: :code:`du -h --max-depth=1 DIR | sort -hr`

Aktuelle Datenmenge des Verzeichnisses abrufen: :code:`du -sh --apparent-size DIR`

Freien RAM in MB abfragen und alle 5s aktualisieren: :code:`free -m -s 5`

Offene Dateien auflisten: :code:`lsof`

Suche nach offenen Dateien eines bestimmten Dienstes: :code:`lsof -i -P | grep SERVICE`

Offene Dateien im Pfad abrufen: :code:`lsof /var/data`

Cpu-Nutzung bestimmter Prozesse abfragen: :code:`ps -eo size,pcpu,pid,user,command --sort -pcpu | grep fpm`

Abfrage der Ram-Nutzung bestimmter Prozesse in B: :code:`ps -eo rss,pid,user,command --sort -rss | grep php-fpm`

Ermittelt die Speichernutzung bestimmter Prozesse in MB: :code:`ps -eo rss,pid,user,command --sort -rss | awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' | grep php-fpm`

Disk I/O über iotop (Prozessebene) loggen: :code:`iotop -P -o -t -a -d 10 -n 10 -b > iotop_output.txt`

Disk I/O loggen: :code:`iostat -d -k -t -N -x 10 10 > iostat_output.txt`

Weniger Swap nutzen:

.. code-block::

    sysctl vm.swappiness=1
    # add 'vm.swappiness=1' to /etc/sysctl.conf
    swapoff -a
    swapon

----

Netzwerk
########

Netzstatistiken: :code:`netstat -s`

Alle vorhandenen Routen anzeigen: :code:`ip route show table all`

IP-Nachbarn anzeigen: :code:`ip neighbor`

Lokale Listenports anzeigen: :code:`netstat -tulpn`

Prüfen, ob der Anschluss offen ist: :code:`nc -z -v -w5 $IP $PORT -s $SRC_IP`

DNS-Abfrage: :code:`host DNS`, :code:`nslookup DNS`, :code:`dig DNS`

Alle Werte eines DNS-Eintragstyps abrufen: :code:`dig +noall +answer +multiline _dmarc.oxl.at TXT`

Versuchen, alle Subdomains abzufragen: :code:`dig @NAMESERVER DOMAIN.TLD AXFR`

----

Zertifikate
***********

Server-Zertifikat via OpenSSL prüfen: :code:`openssl s_client -showcerts -servername FQDN -connect IP/DNS:443 </dev/null`

Prüfen, ob OCSP noch gültig ist (status-age = Mindestlaufzeit in Sekunden): :code:`openssl ocsp -no_nonce -issuer chain.pem -verify_other chain.pem -cert cert.pem -respin ocsp.der -status_age 432000`

Timestamp der OCSP-Aktualisierungszeit abrufen: :code:`date -d "$(openssl ocsp -respin "${tfile}.ocsp" -text -noverify | grep "This Update" | cut -d ':' -f2-)" +"%s"`

Serverzertifikat (pem-Dateiinhalt) vom Dienst via OpenSSL abrufen: :code:`openssl s_client -connect IP/DNS:443 </dev/null 2>/dev/null | openssl x509`

Informationen aus PEM Zertifikat auslesen: :code:`openssl x509 -in <PEM_FILE> -text`

----

VPN & Tunnel
************

Libreswan IPSec
===============

IPSec-Tunnel für manuellen Start hinzufügen: :code:`ipsec auto --add TUNNEL`

IPSec-Tunnel manuell starten: :code:`ipsec auto --up TUNNEL`

Tunnelstatus anzeigen: :code:`ipsec trafficstatus`

Überprüfung der grundlegenden IPSec-Konfiguration/Funktionalität: :code:`ipsec verify`

SSH
===

SSH-Tunnel (entfernte Ressource am lokalen Anschluss): :code:`ssh -L localPort:targetIP:targetPort USER@HOST`

WireGuard
=========

WireGuard VPN starten: :code:`sudo wg-quick up CONFIG`

WireGuard VPN stoppen: :code:`sudo wg-quick down CONFIG`

----

Pentesting
**********

Scannen aller TCP-Ports mit der Option syn-option: :code:`sudo nmap -vv -sS -p1-65535 -T5 --max-retries=1 -Pn <target>`

Alle TCP-Ports scannen: :code:`sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn <target>`

Scannen aller TCP- und UDP-Ports: :code:`sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn -sU -sT <target>`

----

Dateien
#######

Dateien suchen
**************

Suche nach Datei nach Name: :code:`find -type f -name NAME*`

Suche nach Verzeichnis nach Name: :code:`find -type d -name NAME`

----

Tar Archive
***********

Erstellen: :code:`tar -czvf ARCHIVE DIR`

Extrahieren: :code:`tar -xzvf ARCHIVE -C DIR`

----

Datei Verschlüsselung
*********************

Age
===

Herunterladen: `FiloSottile/age <https://github.com/FiloSottile/age/releases>`_

Verschlüsseln: :code:`age -R $AGE_PUB_KEY -o $OUTPUT`

Entschlüsseln: :code:`age -d -i $AGE_PRIV_KEY $INPUT`

----

Ansible
#######

Ansible-Vault string verschlüsseln: :code:` ansible-vault encrypt_string 'VAR_VALUE'`

Ansible-Vault Datei verschlüsseln: :code:`ansible-vault encrypt path/to/file.yml`

----

Bildmanipulation
################

JPEG Bilder komprimieren
************************

Installation: :code:`apt-get install imagemagick`

Einzelnes
=========

.. code-block::

    convert IMG.png -quality 70 IMG.jpg

Mehrere
=======

.. code-block::

    for img in IMG_*.jpg; do convert "$img" -quality 70 "$img"; done

    # oder von png
    for img in *.png; do convert "$img" -quality 70 "${img%.png}.jpg"; done


----

Webp Bilder komprimieren
************************

Installation: :code:`apt-get install webp`

Alternativer Download: :code:`wget -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.1-linux-x86-32.tar.gz`

Einzelnes
=========

.. code-block::

    cwebp -q 70 IMG.png -o IMG.webp

Mehrere
=======

.. code-block::

    for img in *.jpg; do cwebp -q 70 "$img" -o "${img%.jpg}.webp"; done

----

Datenbanken
###########

MySQL/MariaDB
*************

Datenbank ändern: :code:`use DATABASE;`

Tabellen auflisten: :code:`show TABLES;`

Tabellenschema anzeigen: :code:`desc TABLE;`

Alle laufenden Prozesse anzeigen: :code:`SHOW FULL PROCESSLIST;`

Alle Benutzer der MySQL-Instanz anzeigen: :code:`select host, user from mysql.user;`

Binlog/Abfrage-Analyse: :code:`mysqlbinlog /var/lib/mysql/mysql-bin.NNNNN -v`

Replikationsstatus abrufen: :code:`SHOW SLAVE STATUS\G`

----

PostgreSQL
**********

Einstieg: :code:`sudo -u postgres psql`

Datenbank ändern: :code:`\c DATABASE;`

Tabellen auflisten: :code:`\dt`

----

CockroachDB
***********

Siehe: `CockroachDB Releases <https://www.cockroachlabs.com/docs/releases/>`_

Client herunterladen: :code:`curl -s -L https://binaries.cockroachdb.com/cockroach-sql-v24.1.4.linux-amd64.tgz | tar -xz --strip-components=1 -C /tmp/ && sudo mv /tmp/cockroach /usr/local/bin/cockroach`

Verbinden: :code:`cockroach-sql --url "postgres://root@servername:26257/mydb?sslmode=disable"`

.. include:: ../_include/user_rath.rst
