.. _net_dns_cache:

.. include:: ../_include/head.rst


===========
DNS Caching
===========

----

Intro
#####

**Intro Video:** `YouTube @OXL-IT <https://youtu.be/wQmiOde4cKU>`_

In some situations, it can make sense to cache the DNS responses from public DNS servers within the internal network.

Practical examples of this:

* Speed up DNS queries
* Applications that perform many DNS queries do not utilize the public servers as much (*rate limits*)
* The end devices, servers and network devices receive more consistent DNS-to-IP resolutions, as many cloud providers nowadays set VERY low DNS TTLs and therefore the IPs sometimes change with every query

The consistent resolutions in particular can be necessary for **network security filters**. For example for:

* DNS variables on the network firewall
* Proxy checks such as Squid - can result in the following error: :code:`Host header forgery detected (local IP does not match any domain IP)`

----

Implementation
##############

There are many ways to implement a DNS cache.

We will only cover the lightweight :code:`Systemd Resolved` - but you can also use a fully-fledged DNS-server for doing so.

----

Systemd Resolved
****************

Installation
============

(*on Debian Linux*)

.. code-block:: bash

    apt install systemd-resolved
    systemctl enable systemd-resolved.service

Configuration
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

Afterwards run: :code:`systemctl restart systemd-resolved.service`

Firewall Configuration
======================

(:ref:`Linux NFTables <fw_nftables>`)

The **Destination NAT**, which we use to send all DNS requests to our cache service, is particularly important here.

The rules have been simplified to make them easier to understand!

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

        jump dnat_dns_cache

        ...
      }

      chain prerouting_dnat {
        type nat hook prerouting priority -100; policy accept;

        jump dnat_dns_cache

        ...
      }

      chain dnat_dns_cache {
        meta l4proto { tcp, udp } th dport 53 ip saddr $host_self meta skuid != $user_dns_cache redirect
        ip saddr $host_self return
        meta l4proto { tcp, udp } th dport 53 ip saddr $net_private redirect
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


Analysis
========

.. code-block:: bash

    resolvectl status
    resolvectl statistics
    resolvectl query oxl.at
    resolvectl flush-caches
    resolvectl monitor
