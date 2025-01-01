.. _fw_nftables_tproxy:

.. include:: ../_include/head.rst

.. |nft_tproxy_full| image:: ../_static/img/fw_nftables_tproxy_full.svg
   :class: wiki-img-lg
   :alt: OXL Docs - NFTables TProxy Forward & Output

.. |nft_tproxy_fwd| image:: ../_static/img/fw_nftables_tproxy_fwd.svg
   :class: wiki-img-lg
   :alt: OXL Docs - NFTables TProxy Forward


===============
NFTables TProxy
===============

----

Intro
#####

**Intro Videos:** `YouTube @OXL-IT <https://www.youtube.com/playlist?list=PLsYMit2eI6VWm3atUEI-OwAcoxIXMtf3N>`_

Zitat von den `tproxy kernel docs <https://docs.kernel.org/networking/tproxy.html>`_:

.. note::

    Transparent proxying often involves "intercepting" traffic on a router.
    This is usually done with the iptables REDIRECT target; however, there are serious limitations of that method.
    One of the major issues is that it actually modifies the packets to change the destination address -- which might not be acceptable in certain situations. (Think of proxying UDP for example: you won't be able to find out the original destination address. Even in case of TCP getting the original destination address is racy.)
    The 'TPROXY' target provides similar functionality without relying on NAT.


Diese Funktionalität ermöglicht es uns, Datenverkehr an einen Userspace-Prozess zu senden und diesen zu lesen/zu verändern.

Dies kann **mächtige Lösungen** ermöglichen! Als Beispiel siehe: `blog.cloudflare.com - Abusing Linux's firewall <https://blog.cloudflare.com/how-we-built-spectrum/>`_

.. warning::

    TPROXY scheint nur lokale Ziele zu unterstützen.

    Wie man im Kernel-Sourcecode sehen kann, gibt es einem Check, ob der Ziel-Port in Nutzung ist:`nft_tproxy.c <https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/net/netfilter/nft_tproxy.c#n64>`_

Links
*****

* `Kernel - TPROXY <https://docs.kernel.org/networking/tproxy.html>`_
* `PowerDNS - TPROXY <https://powerdns.org/tproxydoc/tproxy.md.html>`_
* `Squid - TPROXY <http://wiki.squid-cache.org/Features/Tproxy4>`_
* `Policy Routing - TPROXY <https://serverfault.com/questions/1052717/how-to-translate-ip-route-add-local-0-0-0-0-0-dev-lo-table-100-to-systemd-netw>`_
* `NFTables source - TPROXY <https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/net/netfilter/nft_tproxy.c>`_
* `Kernel source - TPROXY <http://git.netfilter.org/nftables/commit/?id=2be1d52644cf77bb2634fb504a265da480c5e901>`_

----

Nutzung
#######

Wichtig: Die Operation TPROXY kann nur in der **Pre-Routing filter -150 (mangle)** Chain verwendet werden!

Datenfluss
**********

* **Endgeräte im Netzwerk**

  * **Pre-Routing -150 (mangle)**
  * Pre-Routing -100 (DNAT)
  * Routing (auf Loopback)
  * Input Filter (Proxy Service)

* **Ausgehender Datenverkehr** von dem System (Firewall) selbst
    
  * **Output -150 (mangle)**
  * Output -100 (DNAT)
  * Output Filter
  * Routing (auf Loopback)
  * Pre-Routing -100 (DNAT)
  * Routing
  * Input Filter (Proxy Service)

Wir müssen Datenverkehr auch an 'loopback' weiterleiten, damit dieser 'prerouting' durchläuft.

----

Einrichtung
***********

Dies konfiguriert das Routing des Datenverkehrs zum Loopback Interface:

.. code-block:: bash

    # enable traffic forwarding
    sysctl -w net.ipv4.ip_forward=1

    # disable the RP-filter for internal interfaces
    sysctl net.ipv4.conf.${IIF}.rp_filter=0
    sysctl net.ipv4.conf.lo.rp_filter=0

    # create a routing table
    echo "200 proxy_loopback" > /etc/iproute2/rt_tables.d/proxy.conf

    # route specifically marked traffic to loopback
    ip rule add fwmark 200 table proxy_loopback
    ip -6 rule add fwmark 200 table proxy_loopback
    ip route add local default dev lo table proxy_loopback
    ip -6 route add local default dev lo table proxy_loopback

:code:`200` ist in diesem fall das generische Firewall-Mark, welches wir auch in den NFTables Regeln referenzieren werden.

Damit die Routing-Konfiguration persistent ist, werden wir ein Script erstellen und dieses auch zum NFTables-Service hinzufügen:

.. code-block:: bash

    #!/bin/bash
    # File: /usr/local/sbin/proxy_loopback_routing.sh

    set -u

    TABLE='proxy_loopback'
    MARK=200

    if ! ip rule show | grep -q "$TABLE"
    then
      echo 'Adding TProxy IP4-rule'
      ip rule add fwmark "$MARK" table "$TABLE"
    fi

    if ! ip -6 rule show | grep -q "$TABLE"
    then
      echo 'Adding TProxy IP6-rule'
      ip -6 rule add fwmark "$MARK" table "$TABLE"
    fi

    if ! ip route show table all | grep -q "$TABLE"
    then
      echo 'Adding TProxy IP4-route'
      ip route add local default dev lo table "$TABLE"
    fi

    if ! ip -6 route show table all | grep -q "$TABLE"
    then
      echo 'Adding TProxy IP6-route'
      ip -6 route add local default dev lo table "$TABLE"
    fi


.. code-block:: text

    # File: /etc/systemd/system/nftables.service.d/override.conf
    [Service]
    ExecStartPost=/bin/bash /usr/local/sbin/proxy_loopback_routing.sh

.. code-block:: text

    # File: /etc/systemd/system/networking.service.d/override.conf
    [Service]
    ExecStartPost=/bin/bash /usr/local/sbin/proxy_loopback_routing.sh

Auch die Sysctl-Einstellungen müssen wir unter :code:`/etc/sysctl.conf` hinzufügen, damit diese persistent sind.

Die Routing-Setting könne über folgende Befehle geprüft werden:

.. code-block:: bash

    ip rule list
    ip -6 rule list
    ip route show table all | grep proxy
    ip -6 route show table all | grep proxy

----

Konfiguration
*************

In diesem Beispiel wird jeglicher HTTP+S Datenverkehr, der...

* von Endgeräten aus dem internen Netzwerk
* ein externes Ziel anzielt
* und über die Netzwerk-Firewall geschickt/geroutet wird

...zu einem lokalen (Squid) Proxy geschickt.

Das Regelwerk wurde vereinfacht um verständlicher zu sein!

Notiz: Im Fall vom :ref:`Squid-Proxy <proxy_forward_squid_cnf>` muss man für HTTP & HTTPS verschiedene Listeners und somit Ports nutzen.

|nft_tproxy_fwd|

.. code-block:: text

    define NET_PRIVATE = { 192.168.0.0/16, 172.16.0.0/12, 10.0.0.0/8 };
    # source: https://ipinfo.io/bogon
    define NET_BOGONS_V4 = { 0.0.0.0/8, 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 127.0.53.53, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 240.0.0.0/4, 255.255.255.255/32 };
    # add all of your firewall-system's IPs:
    define HOST_SELF = { 127.0.0.1 };

    define PROXY_PORT_HTTP = 3129;
    define PROXY_PORT_HTTPS = 3130;
    define PROXY_MARK = 200;
    define PROXY_PROTOS = { tcp };
    define PROXY_PORTS = { 80, 443 };

    table inet default {
      chain prerouting_mangle {
        type filter hook prerouting priority -150; policy accept;

        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip saddr $NET_PRIVATE ip daddr != $NET_BOGONS_V4 jump transparent_proxy
      }

      chain transparent_proxy {
        # route traffic to local target
        meta mark set $PROXY_MARK

        # redirect routed traffic to proxy
        tcp dport 80 tproxy ip to 127.0.0.1:$PROXY_PORT_HTTP
        tcp dport 443 tproxy ip to 127.0.0.1:$PROXY_PORT_HTTPS
        # tcp dport 80 tproxy ip6 to [::1]:$PROXY_PORT_HTTP
        # tcp dport 443 tproxy ip6 to [::1]:$PROXY_PORT_HTTPS
      }

      chain input {
        type filter hook input priority 0; policy drop;
        ...

        jump input_transparent_proxy

        ...
      }

      chain input_transparent_proxy {
        # do not handle 'real' input traffic
        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip daddr $HOST_SELF return

        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip saddr $NET_PRIVATE ip daddr != $NET_BOGONS_V4 accept
      }

      ...

----

Output & Forward Datenverkehr
=============================

Wenn man nun aber auch den ausgehenden Datenverkehr von dem System, auf dem NFTables direkt läuft, filtern möchte - wird es ein wenig komplexer.

|nft_tproxy_full|

.. code-block:: text

    define NET_PRIVATE = { 192.168.0.0/16, 172.16.0.0/12, 10.0.0.0/8 };
    # source: https://ipinfo.io/bogon
    define NET_BOGONS_V4 = { 0.0.0.0/8, 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 127.0.53.53, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 240.0.0.0/4, 255.255.255.255/32 };
    # add all of your firewall-system's IPs:
    define HOST_SELF = { 127.0.0.1 };

    define PROXY_PORT_HTTP = 3129;
    define PROXY_PORT_HTTPS = 3130;
    define PROXY_MARK_IN = 200;
    define PROXY_MARK_OUT = 201;
    define PROXY_USER = proxy;
    define PROXY_PROTOS = { tcp };
    define PROXY_PORTS = { 80, 443 };

    table inet default {
      chain output_mangle {
        type route hook output priority -150; policy accept;

        meta l4proto $proxy_protos th dport $PROXY_PORTS ip saddr $HOST_SELF ip daddr != $NET_BOGONS_V4 jump transparent_proxy_loop
      }

      chain transparent_proxy_loop {
        meta skuid != $PROXY_USER meta mark set $PROXY_MARK_IN
      }

      chain prerouting_mangle {
        type filter hook prerouting priority -150; policy accept;

        meta l4proto $proxy_protos th dport $PROXY_PORTS ip saddr $NET_PRIVATE ip daddr != $NET_BOGONS_V4 jump transparent_proxy
        meta l4proto $proxy_protos th dport $PROXY_PORTS ip saddr $HOST_SELF ip daddr != $NET_BOGONS_V4 jump transparent_proxy
      }

      chain transparent_proxy {
        # do not loop traffic that was already looped
        meta mark $PROXY_MARK_IN meta mark set $PROXY_MARK_OUT

        # route traffic to local target
        meta mark != $PROXY_MARK_OUT meta mark set $PROXY_MARK_IN

        # redirect routed traffic to proxy
        tcp dport 80 tproxy ip to 127.0.0.1:$PROXY_PORT_HTTP
        tcp dport 443 tproxy ip to 127.0.0.1:$PROXY_PORT_HTTPS
        # tcp dport 80 tproxy ip6 to [::1]:$PROXY_PORT_HTTP
        # tcp dport 443 tproxy ip6 to [::1]:$PROXY_PORT_HTTPS
      }

      chain input {
        type filter hook input priority 0; policy drop;
        ...

        jump input_transparent_proxy

        ...
      }

      chain input_transparent_proxy {
        # do not handle 'real' input traffic
        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip daddr $HOST_SELF return

        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip saddr $NET_PRIVATE ip daddr != $NET_BOGONS_V4 accept
        meta l4proto $proxy_protos th dport $PROXY_PORTS ip saddr $HOST_SELF ip daddr != $NET_BOGONS_V4 accept
      }

      chain output {
        type filter hook output priority 0; policy drop;

        jump output_transparent_proxy
        ...
      }

      chain output_transparent_proxy {
        # allow marked traffic to be proxied
        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip daddr != $NET_BOGONS_V4 meta skuid != $PROXY_USER meta mark $PROXY_MARK_IN accept

        # allow outbound traffic from proxy
        meta l4proto $PROXY_PROTOS th dport $PROXY_PORTS ip daddr != $NET_BOGONS_V4 meta skuid $PROXY_USER accept
      }

      ...

----

Test Proxy Script
*****************

Wie erwähnt in `diesem Cloudflare Blog-Artikel <https://blog.cloudflare.com/how-we-built-spectrum/>`_.

.. code-block:: python3

    #!/usr/bin/env python3
    import socket

    IP_TRANSPARENT = 19
    PORT = 3000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.IPPROTO_IP, IP_TRANSPARENT, 1)

        s.bind(('127.0.0.1', PORT))
        s.listen(32)
        print(f"[+] Bound to tcp://127.0.0.1:{PORT}")

        while True:
            c, (r_ip, r_port) = s.accept()
            l_ip, l_port = c.getsockname()
            print(f"[ ] Connection from tcp://{r_ip}:{r_port} to tcp://{l_ip}:{l_port}")
            c.send(b"HTTP/1.1 200 OK\nContent-Type: text/plain\n\nReceived by Proxy\n")
            c.close()

----

Remote-Proxy Problem
********************

Möglicherweise möchten Sie einen remote Proxyserver ansteuern. Dies ist jedoch meist nicht einfach über ein DNAT möglich.

Man müsste ein Proxy-Forwarder-Tool verwenden, das dies für Sie erledigen kann.

Wir haben ein bestehendes Tool für genau diesen Zweck gepatched: `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_

Mit einem solchen Tool können Sie den von TPROXY empfangenen reinen Datenverkehr verpacken und weiterleiten oder tunneln.

.. code-block:: text

    # NFTables =TCP=> TPROXY (forwarder @ 127.0.0.1) =HTTP[TCP]=> PROXY

    > curl https://www.oxl.at
    # proxy-forwarder
    2023-08-29 20:49:10 | INFO | handler | 192.168.11.104:36386 <=> www.oxl.at:443/tcp | connection established
    # proxy (squid)
    NONE_NONE/200 0 CONNECT www.oxl.at:443 - HIER_NONE/- -
    TCP_TUNNEL/200 6178 CONNECT www.oxl.at:443 - HIER_DIRECT/www.oxl.at -

    > curl http://www.oxl.at
    # proxy-forwarder
    2023-08-29 20:49:07 | INFO | handler | 192.168.11.104:50808 <=> www.oxl.at:80/tcp | connection established
    # proxy (squid)
    TCP_REFRESH_MODIFIED/301 477 GET http://www.oxl.at/ - HIER_DIRECT/www.oxl.at text/html
