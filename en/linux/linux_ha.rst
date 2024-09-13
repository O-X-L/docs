.. _linux_ha:

.. include:: ../_include/head.rst

=======
LinuxHA
=======

.. include:: ../_include/wip.rst

Intro
#####

LinuxHA is the name for a software stack that allows you to design multi-server high-availability clusters.

This documentation focuses on the setup and maintenance on Debian linux.

See also: `RedHat HA Clusters <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html-single/configuring_and_managing_high_availability_clusters/index>`_

Ansible Collection: `ansibleguy.linuxha <https://github.com/ansibleguy/collection_linuxha>`_

----

Components
##########

Corosync
********

Documentation: `Manpage corosync <https://manpages.debian.org/unstable/corosync/corosync.conf.5.en.html>`_, `Corosync knet <http://people.redhat.com/ccaulfie/docs/KnetCorosync.pdf>`_

Service: :code:`corosync.service`

Votequorum
==========

Documentation: `Manpage votequorum <https://manpages.debian.org/unstable/corosync/votequorum.5.en.html>`_

It is important to understand how the cluster decides how to handle failure events and how it avoids split-brain scenarios.

It does this by having a number of votes assigned to each system in the cluster and ensuring that only when a majority of the votes are present, cluster operations are allowed to proceed.

----

Pacemaker
*********

Service: :code:`pacemaker.service`

Documentation: `Clusterlabs pacemaker <https://clusterlabs.org/pacemaker/>`_

It handles the resources and cluster actions.

----

QDevice
*******

Package: :code:`corosync-qdevice`

Service: :code:`corosync-qdevice.service`

Documentation: :code:`Manpage qdevice <https://manpages.ubuntu.com/manpages/focal/en/man8/corosync-qdevice.8.html>`_

It provides votes to the cluster quorum.

----

CRM Shell
*********

Package: :code:`crmsh`

Command-line interface to interact with the LinuxHA configuration.

----

QNet
****

Package: :code:`corosync-qnetd`

Service: :code:`corosync-qnetd.service`

Documentation: `Manpage qnetd <https://manpages.debian.org/testing/corosync-qnetd/corosync-qnetd.8.en.html>`_

It is designed to run outside of the cluster with the purpose of providing a vote to the corosync-qdevice model net.

It can serve multiple clusters and be almost configuration and state free.

Adding a qnetd can be used instead of :code:`auto_tie_breaker` to get quorate on an even number of nodes.

----

Install
#######

.. code-block:: bash

    apt install corosync pacemaker crmsh
    systemctl enable pacemaker.service corosync.service corosync-qdevice.service

    # configure corosync

    systemctl start pacemaker.service corosync.service
    systemctl restart pacemaker.service corosync.service

    systemctl start corosync-qdevice.service
    # if it fails => check 'corosync-cmapctl | grep quorum.device'

----

Configuration
#############

2-Node Cluster
**************

For 2-node clusters to function, you need to disable these features:

.. code-block:: bash

    crm configure

    property set stonith-enabled=false
    property no-quorum-policy=ignore

    commit

Alternatively, you can configure the :code:`quorum` to :code:`two_node: 1`.

----

Corosync
********

The configuration is placed at :code:`/etc/corosync/corosync.conf`.

It should have the same content on all nodes that are part of the cluster!

You can reload the config using: :code:`corosync-cfgtool -R`

Check the **current status** using:

* :code:`crm status bynode`

* :code:`corosync-quorumtool`

----

Totem
=====

The :code:`totem` basically describes how the nodes communicate with each other.

If you want to use encryption - you have to create a key-file using :code:`corosync-keygen` and place it at :code:`/etc/corosync/keyfile` on all cluster nodes.

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

        keyfile: '/etc/corosync/keyfile'  # default
        secauth: on  # sets cipher & hash as seen below
        # crypto_cipher: aes256
        # crypto_hash: sha256
    }

----

Quorum
======

The :code:`quorum` section configures the cluster voting system.

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

The :code:`nodelist` section configures the cluster nodes.

Names should match the actual node's hostnames.

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

The :code:`ring0` relates to the totem interfaces. If you have multiple networks for corosync to communicate over - you can add :code:`ring1_addr` and so on.

----

Full
====

This is a very basic full-example of the corosync config:

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

Resources
*********

You need to have a working corosync cluster to start configuring your resources.

The resources are the actual high-available services.

You can show your current config like this: :code:`crm configure show`

To configure them, enter the configuration context: :code:`crm configure`

To save your changes - :code:`commit` them.

----

Floating IP
===========

To configure a floating IP, you need to have NICs with the same names on all nodes. Maybe you can use NIC-aliases to workaround different hardware.

.. code-block::

    primitive resServiceIP IPaddr2 \
        params ip=192.168.0.50 nic=eth0 cidr_netmask=32 \
        op monitor interval=2s \
        meta target-role=Started

----

Systemd Service
===============

Services that are managed by LinuxHA should be disabled on startup to not interfere with the cluster-handling: :code:`systemctl disable <SERVICE>.service`

Make sure the service is running on all nodes:

.. code-block::

    primitive resHAProxy systemd:haproxy \
        op monitor interval=5
    clone cloneHAProxy resHAProxy

Or make sure the service only runs on one node, but should always be on the same node as the floating IP:

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

To make sure the current node is healthy, you can run ping-jobs that will impact the node-health if whenever they fail:

.. code-block::

    primitive resPingGw ocf:pacemaker:ping \
        params host_list="192.168.1" \
        op monitor interval=2s timeout=60 on-fail=restart

    clone clonePingGw resPingGw

----

Prefer node
===========

You can define that a specific resource should prefer a specific node if it is alive:

.. code-block::

    location locServiceIP resServiceIP role=Started inf: node1

----

DRBD Replication
================

Note: If you need a file-share & floating-IP to start with the :code:`resDRBDMount` - you can simple move it into a group and put the group inside the :code:`colocation` and :code:`order`

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
        op monitor interval=30s \
        meta target-role=Started maintenance=false

    ms msDRBD resDRBD \
        meta notify=true target-role=Started

    colocation colDRBD inf: resDRBDMount:Started msDRBD:Master
    order ordDRBD Mandatory: msDRBD:promote resDRBDMount:start

----

Maintenance
###########

Corosync Status
***************

You can easily see the node and resource stati.

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

If you see that the :code:`Total votes` are lower than the :code:`Expected votes` - something is wrong.

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

Move Resource
*************

.. code-block::

    crm resource move <RESOURCE> <TARGET-NODE>

----

Update Node
***********

Whenever you need to install updates/patch the system.

.. code-block::

    crm node standby <UPDATE-NODE>

    # wait a few seconds and check if all resources have been migrated successfully

    crm status bynode

    # if finished - update the system and reboot it
    # after the reboot, the node is still in standby - check if it's healthy and re-enable it

    crm node online <UPDATE-NODE>

----

Resource Maintenance
********************

If you need to do maintenance work on a single resource/service across the whole cluster.

LinuxHA will ignore its status in that period. Make sure the state is as before, when disabling the maintenance - else LinuxHA might be a little confused.

.. code-block::

    crm resource maintenance <RESOURCE> true

    # when finished

    crm resource maintenance <RESOURCE> false

----

Unknown Cluster Status
**********************

It might be you have a firewalling issue or your pacemaker services are not working correctly.

Check the status of all services.

----

Monitoring
##########

Here is an example script that can be used to monitor your LinuxHA cluster-status: `OXL/zabbix-linuxha <https://github.com/O-X-L/zabbix-linuxha>`_

Example usage:

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
