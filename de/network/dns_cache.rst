.. _net_dns_cache:

.. include:: ../_include/head.rst


===========
DNS Caching
===========

----

Intro
#####

**Intro Video:** `YouTube @OXL-IT <https://youtu.be/Xaxx4tfx6Bg>`_

In einigen Situationen kann es Sinn machen innerhalb des internen Netzwerkes die DNS-Antworten von öffentlichen DNS-Servern zwischenzuspeichern.

Praktische Beispiele dazu:

* Geschwindigkeit von DNS-Abfragen verschnellern
* Applikationen, die viele DNS-Abfragen durchführen, lasten die öffentlichen Server nicht so sehr aus (*Rate Limits*)
* Die Endgeräte, Server und Netzwerkgeräte erhalten konsistentere DNS-zu-IP Auflösungen, da viele Cloud-Provider heutzutage SEHR niedrige DNS-TTL's setzen und somit ändern sich die IP's teilweise bei jeder Abfrage

Vor allem die konsistenten Auflösungen können für **Netzwerk Sicherheits-Filter** nötig sein. Zum Beispiel für:

* DNS-Variablen auf der Netzwerk-Firewall
* Proxy-Checks wie bei Squid - kann in folgendem Fehler resultieren: :code:`Host header forgery detected (local IP does not match any domain IP)`

----

Implementation
##############

Es gibt viele Möglichkeiten einen DNS-Cache zu implementieren.

Wir gehen hier jetzt nur auf den einfachen :code:`Systemd Resolved` ein - jedoch kann man natürlich auch vollwertige DNS-Server dafür nutzen.

----

Systemd Resolved
****************

Installation
============

(*auf Debian Linux*)

.. code-block:: bash

    apt install systemd-resolved
    systemctl enable systemd-resolved.service

Konfiguration
=============

.. code-block:: text

    # File: /etc/systemd/resolved.conf
    [Resolve]
    DNS=1.1.1.2 1.0.0.2
    FallbackDNS=
    Domains=.
    DNSSEC=allow-downgrade
    DNSOverTLS=opportunistic
    Cache=yes
    CacheFromLocalhost=yes
    DNSStubListener=yes
    DNSStubListenerExtra=127.0.0.1
    DNSStubListenerExtra=0.0.0.0
    ReadEtcHosts=no
    LLMNR=no
    #MulticastDNS=yes
    #ResolveUnicastSingleLabel=no

Danach noch: :code:`systemctl restart systemd-resolved.service`

Firewall Konfiguration
======================

(:ref:`Linux NFTables <fw_nftables>`)

Wichtig ist hier vor allem das **Destination-NAT**, mit welchem wir jegliche DNS-Anfragen zu unserem Cache-Dienst schicken.

Das Regelwerk wurde vereinfacht um verständlicher zu sein!

.. code-block:: text

    #!/usr/sbin/nft -f

    # add your public DNS-servers as configured in 'resolved.conf'
    define host_dns = { 1.1.1.2, 1.0.0.2 }
    # add all of your firewall-system's IPs:
    define host_self = { 127.0.0.1 }
    define user_dns_cache = systemd-resolve

    table inet default {
      chain output_dnat {
        type nat hook output priority -100; policy accept;

        ...

        meta l4proto { tcp, udp } th dport 53 ip saddr $host_self meta skuid != $user_dns_cache redirect

        ...
      }

      chain prerouting_dnat {
        type nat hook prerouting priority -100; policy accept;

        ...

        meta l4proto { tcp, udp } th dport 53 ip saddr $net_private redirect

        ...
      }

      chain input {
        type filter hook input priority 0; policy drop;

        ...

        # allow networks access to dns-cache
        meta l4proto { tcp, udp } th dport 53 ip saddr $net_private ip daddr $host_self accept
        meta l4proto { tcp, udp } th dport 53 ip saddr $host_self ip daddr $host_self accept

        ...
      }

      chain output {
        type filter hook output priority 0; policy drop;

        ...

        # allow firewall itself to query
        meta l4proto { tcp, udp } th dport 53 ip saddr $host_self ip daddr $host_self accept

        # allow dns-cache outbound queries
        tcp dport 853 ip daddr $host_dns meta skuid $user_dns_cache accept
        meta l4proto { tcp, udp } th dport 53 ip daddr $host_dns meta skuid $user_dns_cache accept

        ...
      }
    }


Analyse
=======

.. code-block:: bash

    resolvectl status
    resolvectl statistics
    resolvectl query oxl.at
    resolvectl flush-caches
    resolvectl monitor
