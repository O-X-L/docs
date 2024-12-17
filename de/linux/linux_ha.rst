.. _linux_ha:

.. include:: ../_include/head.rst

=======
LinuxHA
=======

.. include:: ../_include/wip.rst

Intro
#####

LinuxHA ist der Name für einen Software-Stack, mit dem Sie Multi-Server Hochverfügbarkeitscluster erstellen können.

Diese Dokumentation konzentriert sich auf die Einrichtung und Wartung unter Debian-Linux.

Siehe auch: `RedHat HA Clusters <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html-single/configuring_and_managing_high_availability_clusters/index>`_

Ansible Collection: `ansibleguy.linuxha <https://github.com/ansibleguy/collection_linuxha>`_

----

Komponenten
###########

Corosync
********

Dokumentation: `Manpage corosync <https://manpages.debian.org/unstable/corosync/corosync.conf.5.en.html>`_, `Corosync knet <http://people.redhat.com/ccaulfie/docs/KnetCorosync.pdf>`_

Service: :code:`corosync.service`

Votequorum
==========

Dokumentation: `Manpage votequorum <https://manpages.debian.org/unstable/corosync/votequorum.5.en.html>`_

Es ist wichtig zu verstehen, wie der Cluster entscheidet, wie er mit Ausfallereignissen umgeht und wie er Split-Brain-Szenarien vermeidet.

Dies geschieht, indem jedem System im Cluster eine bestimmte Anzahl von Stimmen/Votes zugewiesen wird und sichergestellt wird, dass die Clusteroperationen nur dann fortgesetzt werden können, wenn eine Mehrheit der .

----

Pacemaker
*********

Service: :code:`pacemaker.service`

Dokumentation: `Clusterlabs pacemaker <https://clusterlabs.org/pacemaker/>`_

Es verwaltet die Ressourcen und Clusteraktionen.

----

QDevice
*******

Package: :code:`corosync-qdevice`

Service: :code:`corosync-qdevice.service`

Dokumentation: `Manpage qdevice <https://manpages.ubuntu.com/manpages/focal/en/man8/corosync-qdevice.8.html>`_

Es stellt Stimmen für das Cluster-Quorum zur Verfügung

----

CRM Shell
*********

Package: :code:`crmsh`

Befehlszeilenschnittstelle zur Interaktion mit der LinuxHA-Konfiguration.

----

QNet
****

Package: :code:`corosync-qnetd`

Service: :code:`corosync-qnetd.service`

Dokumentation: `Manpage qnetd <https://manpages.debian.org/testing/corosync-qnetd/corosync-qnetd.8.en.html>`_

Es ist so konzipiert, dass es außerhalb des Clusters läuft, um eine Abstimmung mit dem corosync-qdevice model net zu ermöglichen.

Er kann mehrere Cluster bedienen und ist nahezu konfigurations- und zustandsfrei.

Das Hinzufügen eines qnetd kann anstelle von :code:`auto_tie_breaker` verwendet werden, um Quorate auf einer geraden Anzahl von Nodes zu erhalten.

----

Installation
############

.. code-block:: bash

    apt install corosync pacemaker crmsh
    systemctl enable pacemaker.service corosync.service corosync-qdevice.service

    # configure corosync

    systemctl start pacemaker.service corosync.service
    systemctl restart pacemaker.service corosync.service

    systemctl start corosync-qdevice.service
    # if it fails => check 'corosync-cmapctl | grep quorum.device'

Prüfen Sie nach der Installation, ob die Cluster-Kommunikation nicht von Ihren Firewalls blockiert wird. Standardmäßig sollten Sie folgende Ports prüfen:

* :code:`UDP/5403` für qdevice/Qnetd
* :code:`UDP/5404` für Corosync/crm cluster init
* :code:`UDP/5405` für Corosync/Totem

----

Konfiguration
#############

2-Node Cluster
**************

Damit 2-Knoten-Cluster funktionieren, müssen Sie diese Funktionen deaktivieren:

.. code-block:: bash

    crm configure

    property stonith-enabled=false
    property no-quorum-policy=ignore

    commit

Alternativ kann man das :code:`quorum` auf :code:`two_node: 1` konfigurieren.

----

Corosync
********

Die Konfiguration befindet sich unter :code:`/etc/corosync/corosync.conf`.

Sie sollte auf allen Knoten, die Teil des Clusters sind, den gleichen Inhalt haben!

Sie können die Konfiguration folgendermaßen neu laden: :code:`corosync-cfgtool -R`

Prüfen Sie den **aktuellen Status** mit:

* :code:`crm status bynode`

* :code:`corosync-quorumtool`

----

Totem
=====

Das :code:`totem` beschreibt im Wesentlichen, wie die Nodes miteinander kommunizieren.

Wenn Sie eine Verschlüsselung verwenden möchten, müssen Sie eine Schlüsseldatei mit :code:`corosync-keygen` erstellen und sie unter :code:`/etc/corosync/authkey` auf allen Cluster-Nodes ablegen.

.. code-block::

    totem {
        version: 2
        cluster_name: <YOURCLUSTER>
        ip_version: ipv4-6  # prefer ipv4 over ipv6
        link_mode: passive
        # transport: knet  # default

        # you can have multiple links for network failover
        interface {
            linknumber: 0
        }

        keyfile: /etc/corosync/authkey  # default
        secauth: on  # sets cipher & hash as seen below
        # crypto_cipher: aes256
        # crypto_hash: sha256
    }

----

Quorum
======

Der Abschnitt :code:`quorum` konfiguriert das Abstimmungssystem des Clusters

.. code-block::

    quorum {
        provider: corosync_votequorum

        # example for qnetd
        device {
            votes: 1
            model: net
            net {
                tls: off
                host: <QNET-IP>
                algorithm: ffsplit
                tie-breaker: lowest
            }
        }

        # alternative to qnetd:
        # auto_tie_breaker:  1
        # auto_tie_breaker_node: lowest
    }

----

Nodelist
========

Der Abschnitt :code:`nodelist` konfiguriert die Cluster-Nodes.

Die Namen sollten mit den tatsächlichen Hostnamen der Nodes übereinstimmen.

.. code-block::

    nodelist {
        node {
            name: <NODE1-SHORTNAME>
            nodeid: 1
            quorum_votes: 1
            ring0_addr: <NODE1-IP>
        }
        node {
            name: <NODE2-SHORTNAME>
            nodeid: 2
            quorum_votes: 1
            ring0_addr: <NODE2-IP>
        }
    }

Der :code:`ring0` bezieht sich auf die Totem-Schnittstellen. Wenn Sie mehrere Netzwerke haben, über die corosync kommunizieren soll, können Sie :code:`ring1_addr` etc hinzufügen.

----

Full
====

Dies ist ein sehr einfaches Beispiel für die corosync-Konfiguration:

.. code-block::

    totem {
        version: 2
        cluster_name: cluster1

        transport: knet
        link_mode: passive
        secauth: on

        interface {
            linknumber: 0
        }
    }

    quorum {
        provider: corosync_votequorum
    }

    nodelist {
        node {
            name: node1
            nodeid: 1
            ring0_addr: 192.168.0.11
        }
        node {
            name: node2
            nodeid: 2
            ring0_addr: 192.168.0.12
        }
    }

    logging {
        to_syslog: yes
        debug: off
        logger_subsys {
            subsys: QUORUM
            debug: off
        }
    }


----

Ressourcen
**********

Sie benötigen einen funktionierenden corosync-Cluster, um mit der Konfiguration Ihrer Ressourcen zu beginnen.

Die Ressourcen sind die eigentlichen hochverfügbaren Dienste.

Sie können Ihre aktuelle Konfiguration wie folgt anzeigen: :code:`crm configure show`

Um sie zu konfigurieren, geben Sie den Konfigurationskontext ein: :code:`crm configure`

Um Ihre Änderungen zu speichern - :code:`commit` sie.

----

Floating IP
===========

Um eine floating-IP zu konfigurieren, müssen Sie NICs mit denselben Namen auf allen Nodes haben.

Wenn die NIC's unterschiedliche Namen haben, können Sie probieren den :code:`nic=` Parameter weg zu lassen. LinuxHA wird die IP automatisch zuweise - nicht vergessen dies zu testen! (*oder die NIC Namen via UDEV Regeln gleichstellen*)

.. code-block::

    primitive resServiceIP IPaddr2 \
        params ip=192.168.0.50 nic=eth0 cidr_netmask=32 \
        op monitor interval=2s \
        meta target-role=Started

----

Systemd Service
===============

Dienste, die von LinuxHA verwaltet werden, sollten beim Start deaktiviert werden, um die Handhabung des Clusters nicht zu beeinträchtigen: :code:`systemctl disable <SERVICE>.service`

Stellen Sie sicher, dass der Dienst auf allen Nodes läuft:

.. code-block::

    primitive resHAProxy systemd:haproxy \
        op monitor interval=5
    clone cloneHAProxy resHAProxy

Oder stellen Sie sicher, dass der Dienst nur auf einer Node läuft, der aber immer auf der selben Node wie die floating-IP sein soll:

.. code-block::

    primitive resServiceIP IPaddr2 \
        params ip=192.168.0.50 nic=eth0 cidr_netmask=32 \
        op monitor interval=2s \
        meta target-role=Started

    primitive resHAProxy systemd:haproxy \
        op monitor interval=5

    group groupFloating resServiceIP resHAProxy

----

Ping check
==========

Um sicherzustellen, dass die aktuelle Node ordnungsgemäß funktioniert, können Sie Ping-Jobs ausführen. Wenn diese fehlschlagen, wirken sie sich negativ auf den Node-Gesundheitsstatus aus.

.. code-block::

    primitive resPingGw ocf:pacemaker:ping \
        params host_list="192.168.1" \
        op monitor interval=2s timeout=60 on-fail=restart

    clone clonePingGw resPingGw

----

Prefer node
===========

Sie können festlegen, dass eine bestimmte Ressource eine bestimmte Node bevorzugen soll, wenn diese aktiv ist:

.. code-block::

    location locServiceIP resServiceIP role=Started inf: node1

----

DRBD Replication
================

Hinweis: Wenn Sie eine Dateifreigabe und eine floating-IP benötigen, welche mit dem :code:`resDRBDMount` starten soll, können Sie diese einfach in eine Gruppe verschieben und die Gruppe in die :code:`colocation` und :code:`order` einfügen.

.. code-block::

    primitive resDRBD ocf:linbit:drbd \
        params drbd_resource=r0 \
        op stop interval=0 timeout=100 \
        op start interval=0 timeout=240 \
        op promote interval=0 timeout=90 \
        op demote interval=0 timeout=90 \
        op notify interval=0 timeout=90 \
        op monitor interval=40 role=Slave timeout=20 \
        op monitor interval=20 role=Master timeout=90

    primitive resDRBDMount Filesystem \
        params device="/dev/drbd1" directory="/mnt/data" fstype=ext4 options=noatime \
        op monitor interval=10s \
        meta target-role=Started maintenance=false

    clone msDRBD resDRBD meta notify=true target-role=Started promotable=true
    colocation colDRBD inf: resDRBDMount:Started msDRBD:Master
    order ordDRBD Mandatory: msDRBD:promote resDRBDMount:start

Split-Brain Lösen
-----------------

Sollte es zu einer Split-Brain Situation kommen - kann diese wie folgt gelöst werden:

1. Wenn möglich zur Sicherheit eine Datensicherung beider Nodes erstellen
2. Am Split-Brain Opfer-Server (*dieser hat veraltete Daten*)

.. code-block::

    drbdadm disconnect <RES>
    drbdadm secondary <RES>
    drbdadm connect --discard-my-data <RES>

3. Am überlebenden Server, der bis zuletzt aktiv war und somit den neuesten Datenstand hat:

.. code-block::

    drbdadm primary <RES>
    drbdadm connect <RES>

----

Wartung
#######

Corosync Status
***************

Sie können den Status der Nodes und Ressourcen leicht erkennen.

.. code-block::

    root@node1: crm status bynode

    Cluster Summary:
      * Stack: corosync
      * Current DC: node1 (version 2.0.5-ba59be7122) - partition with quorum
      * Last updated: Fri Sep 13 18:39:02 2024
      * Last change:  Mon Sep  9 21:51:33 2024 by root via crm_attribute on node2
      * 2 nodes configured
      * 7 resource instances configured

    Node List:
      * Node node1: online:
        * Resources:
          * resDRBD (ocf::linbit:drbd):      Master
          * resDRBDMount    (ocf::heartbeat:Filesystem):     Started
          * resPingGw   (ocf::pacemaker:ping):   Started
      * Node node2: online:
        * Resources:
          * resServiceIP       (ocf::heartbeat:IPaddr2):        Started
          * resHAProxy       (systemd:haproxy.service):       Started
          * resDRBD (ocf::linbit:drbd):      Slave
          * resPingGw   (ocf::pacemaker:ping):   Started

----

Votequorum
**********

Wenn Sie sehen, dass die :code:`Total votes` niedriger sind als die :code:`Expected votes` - dann stimmt etwas nicht.

.. code-block::

    root@node1: corosync-quorumtool

    Quorum information
    ------------------
    Date:             Fri Sep 13 18:42:56 2024
    Quorum provider:  corosync_votequorum
    Nodes:            2
    Node ID:          1
    Ring ID:          1.1300c
    Quorate:          Yes

    Votequorum information
    ----------------------
    Expected votes:   3
    Highest expected: 3
    Total votes:      3
    Quorum:           2
    Flags:            Quorate Qdevice

    Membership information
    ----------------------
        Nodeid      Votes    Qdevice Name
             1          1    A,V,NMW node1 (local)
             2          1    A,V,NMW node2
             0          1            Qdevice

----

Ressource verschieben
*********************

.. code-block::

    crm resource move <RESOURCE> <TARGET-NODE>

----

Node updaten
************

Wann immer Sie Updates/Patches für das System installieren müssen.

.. code-block::

    crm node standby <UPDATE-NODE>

    # wait a few seconds and check if all resources have been migrated successfully

    crm status bynode

    # if finished - update the system and reboot it
    # after the reboot, the node is still in standby - check if it's healthy and re-enable it

    crm node online <UPDATE-NODE>

----

Ressource warten
****************

Wenn Sie Wartungsarbeiten an einer einzelnen Ressource/einem einzelnen Dienst im gesamten Cluster durchführen müssen.

LinuxHA wird den Status in diesem Zeitraum ignorieren. Vergewissern Sie sich, dass der Status wie zuvor ist, wenn Sie die Wartung deaktivieren - andernfalls könnte LinuxHA ein wenig verwirrt sein.

.. code-block::

    crm resource maintenance <RESOURCE> true

    # when finished

    crm resource maintenance <RESOURCE> false

----

Unbekannte Cluster Status
*************************

Möglicherweise haben Sie ein Firewall-Problem oder Ihre Pacemaker funktionieren nicht richtig.

Überprüfen Sie den Status aller Dienste.

----

Monitoring
##########

Hier ist ein Beispielskript, das zur Überwachung des Status Ihres LinuxHA-Clusters verwendet werden kann: `OXL/zabbix-linuxha <https://github.com/O-X-L/zabbix-linuxha>`_

Beispiel für die Nutzung:

.. code-block::

    python3 linuxha_monitoring.py members
    > 2

    python3 linuxha_monitoring.py members_active
    > 2

    python3 linuxha_monitoring.py votes
    > 1
    # true/false (we have all expected votes)

    python3 linuxha_monitoring.py quorum
    > 1
    # true/false (is quorate)

    python3 linuxha_monitoring.py resource resHAProxy
    > 1
    # true/false (is running on any node)

    python3 linuxha_monitoring.py resource_active resHAProxy
    > 1
    # true/false (is running on THIS node)


.. include:: ../_include/user_rath.rst
