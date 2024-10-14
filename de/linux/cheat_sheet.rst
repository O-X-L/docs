.. _linux_cheat_sheet:

.. include:: ../_include/head.rst

===================
Command Cheat Sheet
===================

Allgemeine Shell-Nutzung
########################

Verweis auf das letzte Wort des letzten Befehls: 

.. code-block:: bash

   !$

Verweis auf den Exit-Code des letzten Befehls: 

.. code-block:: bash

   $?

Pfad zur ausführbaren Datei abrufen: 

.. code-block:: bash

   which EXE

String in Dateien rekursiv suchen: 

.. code-block:: bash

   grep -r 'SearchString'

Befehl als anderer Benutzer ausführen:

.. code-block:: bash

   su --shell /bin/bash -c '$COMMAND' $USER

Interaktive Shell im Kontext eines anderen Benutzers starten:

.. code-block:: bash

   su --login --shell /bin/bash $USER

Unterschiede zwischen den Verzeichnisinhalten anzeigen:

.. code-block:: bash

   diff --recursive --unified=3 --color before/vars/ vars/

Unterschiede mit Farben loggen:

.. code-block:: bash

   unbuffer diff --recursive --unified=3 --color before/vars/ vars/ | tee log.txt

Datetime-String in Zeitstempel umwandeln:

.. code-block:: bash

   date -d "$(get datetime string here)" +"%s"

Suchen und Ersetzen von Strings in Dateien:

.. code-block:: bash

   sed -i 's|FIND_REGEX|REPLACE|g' FILE

Suchen und Ersetzen von Zeichenfolgen in Dateien unter Verwendung von Variablen:

.. code-block::

    FIND_REGEX='my regex'
    REPLACE='replace'

    sed -i "s|$FIND_REGEX|$REPLACE|g" FILE

APT Update eines einzelnen Paketes: 

.. code-block:: bash

   sudo apt-get --only-upgrade install PKG

SSH-Schlüssel erstellen:

.. code-block:: bash

   ssh-keygen -t ed25519 -C 'comment'

Die letzten 100 logs eines Systemd-Dienstes abrufen:

.. code-block:: bash

   journalctl -u SERVICE.service --no-pager -n 100

Postfix-Log-Übersicht generieren: 

.. code-block:: bash

   pflogsumm -u 50 -h 50 -i --verbose-msg-detail mail.log mail.log.? > mail_report.log

Letzte Anmeldungen abrufen:

.. code-block:: bash

    last

    lastlog

Aktuelle offene Benutzersitzungen abrufen: 

.. code-block:: bash

    w

Schneller Überblick über Source-Code: 

.. code-block:: bash

    # sudo apt install cloc
    cd <REPO_BASE> && cloc

----

Ressourcenmanagement
####################

Größe des Verzeichnisses abfragen: 

.. code-block:: bash

    du -sh DIR

Größe der Unterverzeichnisse eines Verzeichnisses ermitteln:

.. code-block:: bash

    du -h --max-depth=1 DIR | sort -hr

Aktuelle Datenmenge des Verzeichnisses abrufen:

.. code-block:: bash

    du -sh --apparent-size DIR

Freien RAM in MB abfragen und alle 5s aktualisieren:

.. code-block:: bash

    free -m -s 5

Offene Dateien auflisten:

.. code-block:: bash

    lsof

Suche nach offenen Dateien eines bestimmten Dienstes:

.. code-block:: bash

    lsof -i -P | grep SERVICE

Offene Dateien im Pfad abrufen:

.. code-block:: bash

    lsof /var/data

Cpu-Nutzung bestimmter Prozesse abfragen:

.. code-block:: bash

    ps -eo size,pcpu,pid,user,command --sort -pcpu | grep fpm

Abfrage der Ram-Nutzung bestimmter Prozesse in B:

.. code-block:: bash

    ps -eo rss,pid,user,command --sort -rss | grep php-fpm

Ermittelt die Speichernutzung bestimmter Prozesse in MB:

.. code-block:: bash

    ps -eo rss,pid,user,command --sort -rss | awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' | grep php-fpm

Disk I/O über iotop (Prozessebene) loggen:

.. code-block:: bash

    iotop -P -o -t -a -d 10 -n 10 -b > iotop_output.txt

Disk I/O loggen:

.. code-block:: bash

    iostat -d -k -t -N -x 10 10 > iostat_output.txt

Weniger Swap nutzen:

.. code-block::

    sysctl vm.swappiness=1
    # add 'vm.swappiness=1' to /etc/sysctl.conf
    swapoff -a
    swapon

Mit Disk-Partitionen interagieren:

.. code-block::

    fdisk /dev/sdX

----

Logical Volume Manager (LVM)
****************************

Show volume groups:

.. code-block::

    vgs

    vgdisplay

Show volumes:

.. code-block::

    lvs

    lvdisplay

Scan for physical disks available to LVM:

.. code-block::

    pvs

    pvscan

Add physical disk to be available to LVM:

.. code-block::

    pvcreate /dev/sdX

Create volume:

.. code-block::

    lvcreate -n <lv-name> -L 50G <vg-name>

Create partition on volume:

.. code-block::

    # check
    ls -l /dev/mapper/

    mkfs.xfs /dev/mapper/<vg-name>-<lv-name>

Extend physical disk and volume group:

.. code-block::

    pvresize /dev/sdX
    vgextend <vg-name> /dev/sdX

Extend volume and partition:

.. code-block::

    lvextend /dev/<vg-name>/<lv-name> -L +20GB
    # or in %
    lvextend /dev/<vg-name>/<lv-name> -l +100%FREE

    resize2fs /dev/mapper/<vg-name>-<lv-name>

Remove:

.. code-block::

    umount <mountpoint>

    lvremove <lv-name>

    vgremove <vg-name>

----

Software RAID (MD)
******************

Erstellen:

.. code-block::

    # RAID1
    mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1

Status:

.. code-block::

    mdadm --detail /dev/md1

Entfernen:

.. code-block::

    mdadm --stop /dev/md1
    mdadm --fail /dev/md1 --remove /dev/md1

    # clean disk superblock
    dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=10

System Disk RAID1: (Siehe `Hetzner installimage scripts <https://github.com/hetzneronline/installimage>`_)

.. code-block::

    lsblk
    > nvme1n1        259:0    0 953.9G  0 disk
    > ├─nvme1n1p1    259:2    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > └─nvme1n1p2    259:3    0    30G  0 part
    >   └─md1          9:1    0    30G  0 raid1
    >     ├─vg0-root 252:0    0    10G  0 lvm   /
    >     ├─vg0-swap 252:1    0     4G  0 lvm
    >     └─vg0-var  252:2    0    10G  0 lvm   /var
    >
    > nvme0n1        259:1    0 953.9G  0 disk
    > ├─nvme0n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > └─nvme0n1p2    259:6    0    30G  0 part
    >   └─md1          9:1    0    30G  0 raid1
    >     ├─vg0-root 252:0    0    10G  0 lvm   /
    >     ├─vg0-swap 252:1    0     4G  0 lvm
    >     └─vg0-var  252:2    0    10G  0 lvm   /var

    # hetzner install-image config:
    #   SWRAID 1
    #   SWRAIDLEVEL 1
    #   PART /boot ext3 1024M
    #   PART lvm vg0 30G
    #   LV vg0 root /     ext4 10G
    #   LV vg0 swap swap  swap  4G
    #   LV vg0  var /var  ext4 10G

----

ZFS
***

Pool erstellen:

.. code-block::

    # RAID1-like
    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1 /dev/nvme1n1

    # RAID10-like
    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1 /dev/nvme1n1 mirror /dev/nvme2n1 /dev/nvme3n1

Status:

.. code-block::

    zpool list
    zpool status
    zfs list

Pool entfernen:

.. code-block::

    zpool destroy <pool-name>

ZFS on system disks: (*Proxmox VE usage*)

.. code-block::

    lsblk
    > nvme0n1        259:1    0 953.9G  0 disk
    > ├─nvme0n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > ├─nvme0n1p2    259:6    0    30G  0 part
    > │ └─md1          9:1    0    30G  0 raid1
    > │   ├─vg0-root 252:0    0    10G  0 lvm   /
    > │   ├─vg0-swap 252:1    0     4G  0 lvm
    > │   └─vg0-var  252:2    0    10G  0 lvm   /var
    > └─nvme0n1p3    259:7    0 922.9G  0 part  # ==> ZFS
    >
    > nvme1n1        259:1    0 953.9G  0 disk
    > ├─nvme1n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > ├─nvme1n1p2    259:6    0    30G  0 part
    > │ └─md1          9:1    0    30G  0 raid1
    > │   ├─vg0-root 252:0    0    10G  0 lvm   /
    > │   ├─vg0-swap 252:1    0     4G  0 lvm
    > │   └─vg0-var  252:2    0    10G  0 lvm   /var
    > └─nvme1n1p3    259:7    0 922.9G  0 part  # ==> ZFS

    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1p3 /dev/nvme1n1p3

    zpool status
    > NAME                  STATE     READ WRITE CKSUM
    > pve                   ONLINE       0     0     0
    >   mirror-0            ONLINE       0     0     0
    >     nvme-eui.1-part3  ONLINE       0     0     0
    >     nvme-eui.2-part3  ONLINE       0     0     0


----

Netzwerk
########

Netzstatistiken: 

.. code-block:: bash

    netstat -s

Alle vorhandenen Routen anzeigen:

.. code-block:: bash

    ip route show table all

IP-Nachbarn anzeigen:

.. code-block:: bash

    ip neighbor

Lokale Listenports anzeigen:

.. code-block:: bash

    netstat -tulpn

Prüfen, ob der Anschluss offen ist:

.. code-block:: bash

    nc -z -v -w5 $IP $PORT -s $SRC_IP

DNS-Abfrage:

.. code-block:: bash

    host DNS

    nslookup DNS

    dig DNS

Alle Werte eines DNS-Eintragstyps abrufen:

.. code-block:: bash

    dig +noall +answer +multiline _dmarc.oxl.at TXT

Versuchen, alle Subdomains abzufragen: (*wird in der Regel blockiert*)

.. code-block:: bash

    dig @NAMESERVER DOMAIN.TLD AXFR

Live-Datenverkehr sehen:

.. code-block:: bash

    # sudo apt install tcpdump
    tcpdump -i <INTERFACE> host <IP> port <PORT>

    # record to file (for wireshark)
    tcpdump -i <INTERFACE> host <IP> port <PORT> -w <FILE>.pcap

----

Zertifikate
***********

Server-Zertifikat via OpenSSL prüfen: 

.. code-block:: bash

    openssl s_client -showcerts -servername FQDN -connect IP/DNS:443 </dev/null

    # show status
    openssl s_client -connect IP/DNS:443 -status </dev/null 2>/dev/null

Prüfen, ob OCSP noch gültig ist (status-age = Mindestlaufzeit in Sekunden): 

.. code-block:: bash

    openssl ocsp -no_nonce -issuer chain.pem -verify_other chain.pem -cert cert.pem -respin ocsp.der -status_age 432000

Timestamp der OCSP-Aktualisierungszeit abrufen:

.. code-block:: bash

    date -d "$(openssl ocsp -respin "${tfile}.ocsp" -text -noverify | grep "This Update" | cut -d ':' -f2-)" +"%s"

Serverzertifikat (pem-Dateiinhalt) vom Dienst via OpenSSL abrufen:

.. code-block:: bash

    openssl s_client -connect IP/DNS:443 </dev/null 2>/dev/null | openssl x509

Informationen aus PEM Zertifikat auslesen:

.. code-block:: bash

    openssl x509 -in <PEM_FILE> -text

Script zum validieren von aktiven Zertifikaten: `ssl-validate.sh <https://gist.github.com/superstes/8e369be2c86bbbcbd1e64c57d34905f1>`_

Script zum validieren von OCSP: `ssl-ocsp-check.sh <https://gist.github.com/superstes/5ca4f4c346ea18703f716307a05d286b>`_

----

Daten Wiederherstellung
***********************

Disk Seriennummer finden:

.. code-block:: bash

    smartctl -x /dev/sdX

Disk Klonen:

.. code-block:: bash

    dd if=/dev/sdX of=/dev/sdX bs=1G status=progress

Siehe: `Testdisk <https://www.cgsecurity.org/wiki/TestDisk_Download>`_

Für SMART checks siehe: `dbi-services.com/blog <https://www.dbi-services.com/blog/linux-disks-diagnostic-using-smarctl/>`_

----

VPN & Tunnel
************

Libreswan IPSec
===============

IPSec-Tunnel für manuellen Start hinzufügen: 

.. code-block:: bash

    ipsec auto --add TUNNEL

IPSec-Tunnel manuell starten:

.. code-block:: bash

    ipsec auto --up TUNNEL

Tunnelstatus anzeigen:

.. code-block:: bash

    ipsec trafficstatus

Überprüfung der grundlegenden IPSec-Konfiguration/Funktionalität:

.. code-block:: bash

    ipsec verify

SSH
===

SSH-Tunnel (entfernte Ressource am lokalen Anschluss): 

.. code-block:: bash

    ssh -L localPort:targetIP:targetPort USER@HOST

WireGuard
=========

WireGuard VPN starten: 

.. code-block:: bash

    sudo wg-quick up CONFIG

WireGuard VPN stoppen:

.. code-block:: bash

    sudo wg-quick down CONFIG

----

Pentesting
**********

Scannen aller TCP-Ports mit der Option syn-option: 

.. code-block:: bash

    sudo nmap -vv -sS -p1-65535 -T5 --max-retries=1 -Pn <target>

    # -p1-65535 == -p-

Alle TCP-Ports scannen:

.. code-block:: bash

    sudo nmap -vv -p- -T5 --max-retries=1 -Pn <target>

Scannen aller TCP- und UDP-Ports:

.. code-block:: bash

    sudo nmap -vv -p- -T5 --max-retries=1 -Pn -sU -sT <target>

Schneller Gesamt-Scan:

.. code-block:: bash

    sudo nmap -T4 -A -p- --min-rate 1000 --open -oN scan.txt <target>

    # --open = only show open ports
    # -oN = save output to file
    # -A = OS detection

----

Dateien
#######

Dateien suchen
**************

Suche nach Datei nach Name: 

.. code-block:: bash

    find -type f -name NAME*

Suche nach Verzeichnis nach Name:

.. code-block:: bash

    find -type d -name NAME

----

Tar Archive
***********

Erstellen: 

.. code-block:: bash

    tar -czvf ARCHIVE DIR

Extrahieren:

.. code-block:: bash

    tar -xzvf ARCHIVE -C DIR

----

Datei Verschlüsselung
*********************

Age
===

Herunterladen: `FiloSottile/age <https://github.com/FiloSottile/age/releases>`_

Verschlüsseln: 

.. code-block:: bash

    age -R $AGE_PUB_KEY -o $OUTPUT

Entschlüsseln:

.. code-block:: bash

    age -d -i $AGE_PRIV_KEY $INPUT

----

Ansible
#######

Ansible-Vault string verschlüsseln: 

.. code-block:: bash

    ansible-vault encrypt_string 'VAR_VALUE'

Ansible-Vault Datei verschlüsseln:

.. code-block:: bash

    ansible-vault encrypt path/to/file.yml

Inhalt einer verschlüsselten Datei entschlüsselt anzeigen:

.. code-block:: bash

    ansible-vault view path/to/file.yml

----

Bildmanipulation
################

JPEG Bilder komprimieren
************************

Installation: 

.. code-block:: bash

    apt-get install imagemagick

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

Installation: 

.. code-block:: bash

    apt-get install webp

Alternativer Download:

.. code-block:: bash

    wget -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.1-linux-x86-32.tar.gz

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

Datenbank ändern: 

.. code-block:: bash

    use DATABASE;

Tabellen auflisten:

.. code-block:: bash

    show TABLES;

Tabellenschema anzeigen:

.. code-block:: bash

    desc TABLE;

Alle laufenden Prozesse anzeigen:

.. code-block:: bash

    SHOW FULL PROCESSLIST;

Alle Benutzer der MySQL-Instanz anzeigen:

.. code-block:: bash

    select host, user from mysql.user;

Binlog/Abfrage-Analyse:

.. code-block:: bash

    mysqlbinlog /var/lib/mysql/mysql-bin.NNNNN -v

Replikationsstatus abrufen:

.. code-block:: bash

    SHOW SLAVE STATUS\G

----

PostgreSQL
**********

Einstieg:

.. code-block:: bash

    sudo -u postgres psql

Datenbank ändern:

.. code-block:: bash

    \c DATABASE;

Tabellen auflisten:

.. code-block:: bash

    \dt

----

CockroachDB
***********

Siehe: `CockroachDB Releases <https://www.cockroachlabs.com/docs/releases/>`_

Client herunterladen:

.. code-block:: bash

    curl -s -L https://binaries.cockroachdb.com/cockroach-sql-v24.1.4.linux-amd64.tgz | tar -xz --strip-components=1 -C /tmp/ && sudo mv /tmp/cockroach /usr/local/bin/cockroach

Verbinden:

.. code-block:: bash

    cockroach-sql --url "postgres://root@servername:26257/mydb?sslmode=disable"

----

Container
#########

Docker
******

Interaktive shell in temporärem container starten:

.. code-block:: bash

    docker run --rm -it alpine sh


.. include:: ../_include/user_rath.rst
