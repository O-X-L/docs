.. _fw_nftables:

.. include:: ../_include/head.rst

.. |nft_flow| image:: ../_static/img/fw_nftables_flow.png
   :class: wiki-img-lg
   :alt: OXL Docs - NFTables Packet Flow

.. |nft_hooks| image:: ../_static/img/fw_nftables_hooks.png
   :class: wiki-img-lg
   :alt: OXL Docs - NFTables Chains & Hooks

.. |nft_tproxy| image:: ../_static/img/fw_nftables_tproxy.png
   :class: wiki-img-sm
   :alt: OXL Docs - NFTables TProxy

========
NFTables
========

.. include:: ../_include/wip.rst

----

Intro
#####

NFTables ist der `Nachfolger von IPTables <https://netfilter.org/projects/nftables/>`_ und eine weit verbreitete Linux-Firewall.

Sie kann als Host-Firewall oder sogar als Netzwerk-Firewall verwendet werden.

Es ist die `Standard-Firewall in Debian 10+ <https://wiki.debian.org/nftables>`_.

**Intro Video:** `YouTube @OXL-IT <https://www.youtube.com/watch?v=dnkuDjblI-k&t=41s>`_


Chain hooks/Table families
**************************

|nft_hooks|

Packet flow
***********

|nft_flow|

----

Links
*****

* `Quick reference <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes>`_
* `Change history <https://wiki.nftables.org/wiki-nftables/index.php/List_of_updates_since_Linux_kernel_3.13>`_
* `Differences with IPTables <https://wiki.nftables.org/wiki-nftables/index.php/Main_differences_with_iptables>`_
* Configuration

  * `tables <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Tables>`_, `table families <https://wiki.nftables.org/wiki-nftables/index.php/Nftables_families>`_
  * `chain know-how <https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains>`_, `chains <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Chains>`_, `chain hooks <https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks>`_
  * `rule know-how <https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management>`_, `rules <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules>`_
  * `sets <https://wiki.nftables.org/wiki-nftables/index.php/Sets>`_
  * `dynamic sets <https://wiki.nftables.org/wiki-nftables/index.php/Updating_sets_from_the_packet_path>`_, `elements <https://wiki.nftables.org/wiki-nftables/index.php/Element_timeouts>`_
  * `counters <https://wiki.nftables.org/wiki-nftables/index.php/Counters>`_
  * `limits <https://wiki.nftables.org/wiki-nftables/index.php/Rate_limiting_matchings>`_
  * `meters <https://wiki.nftables.org/wiki-nftables/index.php/Meters>`_
  * `maps <https://wiki.nftables.org/wiki-nftables/index.php/Maps>`_, `vmaps <https://wiki.nftables.org/wiki-nftables/index.php/Verdict_Maps_(vmaps)>`_
  * `set meta information <https://wiki.nftables.org/wiki-nftables/index.php/Setting_packet_metainformation>`_, `match meta information <https://wiki.nftables.org/wiki-nftables/index.php/Matching_packet_metainformation>`_

* NAT

  * `source/destination NAT <https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)>`_
  * `multi NAT <https://wiki.nftables.org/wiki-nftables/index.php/Multiple_NATs_using_nftables_maps>`_
  * `load balancing <https://wiki.nftables.org/wiki-nftables/index.php/Load_balancing>`_

* Examples

  * `Ruleset for server <https://wiki.nftables.org/wiki-nftables/index.php/Simple_ruleset_for_a_server>`_
  * `Ruleset for workstation <https://wiki.nftables.org/wiki-nftables/index.php/Simple_ruleset_for_a_workstation>`_

* `math operations <https://wiki.nftables.org/wiki-nftables/index.php/Math_operations>`_
* `mangle package headers <https://wiki.nftables.org/wiki-nftables/index.php/Mangling_packet_headers>`_
* `expressions <https://wiki.nftables.org/wiki-nftables/index.php/Building_rules_through_expressions>`_
* `routing information <https://wiki.nftables.org/wiki-nftables/index.php/Matching_routing_information>`_
* `bridge filtering <https://wiki.nftables.org/wiki-nftables/index.php/Bridge_filtering>`_
* `connection tracker helpers <https://wiki.nftables.org/wiki-nftables/index.php/Conntrack_helpers>`_
* `debugging <https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing>`_

----

Installation
############


Kernel Module
*************

Einige Funktionen von NFTables sind möglicherweise nicht standardmäßig aktiviert.

Um zu überprüfen, welche Funktionen für Ihren Kernel aktiv sind, prüfen Sie die Konfigurationsdatei:

.. code-block:: bash

    cat "/boot/config-$(uname -r)" | grep -E "CONFIG_NFT|CONFIG_NF_TABLES"

Um alle vorhandenen Module zu finden:

.. code-block:: bash

    find /lib/modules/$(uname -r) -type f -name '*.ko' | grep -E 'nf_|nft_'

Um ein Modul zu aktivieren:

.. code-block:: bash

    modprobe nft_nat
    modprobe nft_tproxy

----

Nutzung
#######

Config Files
************

NFTables kann vollständig über eine oder mehrere Konfigurationsdateien konfiguriert werden.

In den meisten Fällen werden sie mehrere verwenden wollen:

* Haupt-Konfiguration: :code:`/etc/nftables.conf`
* Ein Verzeichnis dessen Inhalt inkludiert wird: :code:`/etc/nft.conf.d/`

Der systemd-Dienst lädt standardmäßig die Hauptkonfigurationsdatei:

.. code-block:: nft

    # /lib/systemd/system/nftables.service
    [Unit]
    ...

    [Service]
    ...
    ExecStart=/usr/sbin/nft -f /etc/nftables.conf
    ExecReload=/usr/sbin/nft -f /etc/nftables.conf
    ExecStop=/usr/sbin/nft flush ruleset
    ...


Beispiel für die Hauptkonfigurationsdatei:

.. code-block:: nft

    #!/usr/sbin/nft -f
    flush ruleset
    include "/etc/nft.conf.d/*.conf"

Dann können Sie Ihre aktuelle Konfiguration in das Konfigurationsverzeichnis einfügen!

Um Ihre **Konfiguration zu testen**:

.. code-block:: bash

    nft -cf /etc/nftables.conf


CLI
***

* `CLI overview <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Nft_scripting>`_
* `Scripting <https://wiki.nftables.org/wiki-nftables/index.php/Scripting>`_

Programmatically
****************

Es gibt einige Libraries/Module, mit denen Sie NFTables direkt aus dem Code heraus verwalten können:

* Backend for the libraries: `libnftables <https://www.mankier.com/5/libnftables-json>`_
* GoLang: `github.com/google/nftables <https://pkg.go.dev/github.com/google/nftables>`_, `source code <https://github.com/google/nftables>`_
* Python3: `documentation <https://ral-arturo.org/2020/11/22/python-nftables-tutorial.html>`_, `source code <https://git.netfilter.org/nftables/tree/py>`_, `examples <https://github.com/aborrero/python-nftables-tutorial>`_


Ansible
*******

See: `NFTables Ansible-Role <https://github.com/ansibleguy/infra_nftables/blob/latest/docs/Example.md>`_, `NFTables Ansible-Modules <https://github.com/ansibleguy/collection_nftables>`_

----

Troubleshooting
###############

Trace
*****

Sie können Pakete markieren um ihren Weg durch die Chains zu verfolgen.

Siehe auch: `NFTables documentation - trace <https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing>`_

**Sie müssen dafür**:

* Markieren Sie die zu verfolgenden Pakete, indem Sie die Option :code:`meta nftrace set 1` zu einer Regel hinzufügen.

* Indem Sie :code:`nft monitor trace` in einem separaten Terminal ausführen, können sie die Logs dazu in Echtzeit sehen.

You may want to start the trace at the point where the traffic enters.

Sie sollten den trace an dem Punkt starten, an dem die Pakete in der Firewall ankommen.

Beispiel für **input Pakete**:

.. code-block:: nft

    chain input {
        type filter hook input priority 0; policy drop;

        # enable tracing for: tcp-traffic to port 1337 originating from a specific network
        tcp dport 1337 ip saddr 192.168.10.0/24 meta nftrace set 1

        ...

    }


Beispiel für **output Pakete**:

.. code-block:: nft

    chain output {
        type filter hook output priority 0; policy drop;

        # enable tracing for: http+s to a specific target
        tcp dport { 80, 443 } ip daddr 1.1.1.1 meta nftrace set 1

        ...

    }

Beispiel der **monitor Information**:

.. code-block:: bash

    nft monitor trace
    > trace id a95ea7ef ip filter trace_chain packet: iif "enp0s25" ether saddr 00:0d:b9:4a:49:3d ether daddr 3c:97:0e:39:aa:20 ip saddr 8.8.8.8 ip daddr 192.168.2.118 ip dscp cs0 ip ecn not-ect ip ttl 115 ip id 0 ip length 84 icmp type echo-reply icmp code net-unreachable icmp id 9253 icmp sequence 1 @th,64,96 24106705117628271805883024640
    > trace id a95ea7ef ip filter trace_chain rule meta nftrace set 1 (verdict continue)
    > trace id a95ea7ef ip filter trace_chain verdict continue
    > trace id a95ea7ef ip filter trace_chain policy accept
    > trace id a95ea7ef ip filter input packet: iif "enp0s25" ether saddr 00:0d:b9:4a:49:3d ether daddr 3c:97:0e:39:aa:20 ip saddr 8.8.8.8 ip daddr 192.168.2.118 ip dscp cs0 ip ecn not-ect ip ttl 115 ip id 0 ip length 84 icmp type echo-reply icmp code net-unreachable icmp id 9253 icmp sequence 1 @th,64,96 24106705117628271805883024640
    > trace id a95ea7ef ip filter input rule ct state established,related counter packets 168 bytes 53513 accept (verdict accept)


IPTables Regeln übersetzen
**************************

In den meisten Fällen ist das Verhalten von IPTables und NFTables nahezu identisch.

In einigen Distributionen, wie Debian, ist das Standard-IPTables-Backend bereits zu NFTables migriert.

**Warum von IPTables übersetzen?**

Es gibt 1000x mehr Ressourcen zu IPTables, die Ihnen helfen könnten, die Dinge zum Laufen zu bringen.

**Empfohlener Weg:**

* eine leere VM zum Testen des IPTables ruleset zu haben
* das minimale, funktionierend, ruleset speichern: :code:`iptables-save > /etc/iptables/rules.ipt`
* das ruleset zu NFTables übersetzen: :code:`iptables-restore-translate -f /etc/iptables/rules.ipt > /etc/iptables/rules.nft`
* Testen Sie den NFTables-Regelsatz und entfernen Sie die standard Chains, die Sie nicht benötigen (*IPTables ist etwas unordentlicher mit seinen Chains*)

Zur Info: man kann auch IPTables Regeln wiederherstellen: :code:`iptables-restore < /etc/iptables/rules.ipt`

----

Service
#######

Um zu verhindern, dass eine invalide Konfiguration Ihren :code:`nftables.service` tötet, können Sie eine Konfigurations-Validierung hinzufügen:

.. code-block:: text

    # /etc/systemd/system/nftables.service.d/override.conf

    [Service]
    # catch errors at start
    ExecStartPre=/usr/sbin/nft -cf /etc/nftables.conf

    # catch errors at reload
    ExecReload=
    ExecReload=/usr/sbin/nft -cf /etc/nftables.conf
    ExecReload=/usr/sbin/nft -f /etc/nftables.conf

    # catch errors at restart
    ExecStop=
    ExecStop=/usr/sbin/nft -cf /etc/nftables.conf
    ExecStop=/usr/sbin/nft flush ruleset

    Restart=on-failure
    RestartSec=5s

Dadurch werden Konfigurationsfehler abgefangen und protokolliert, bevor ein reload/restart durchgeführt wird.

Bei einem System-Neustart wird es immer noch fehlschlagen, wenn die Konfiguration fehlerhaft ist.

----

Addons
######

NFTables fehlt es an einigen Funktionen, die üblicherweise bei der Firewall verwendet werden.

Sie können ein geplantes Skript hinzufügen, das diese Funktionen zu NFTables hinzufügt!

Siehe: `Ansible-managed addons <https://github.com/ansibleguy/addons_nftables>`_

DNS
***

Es ist schön, Variablen zu haben, die die IPs von einigen DNS-Einträgen enthalten.

NFTables KANN DNS-Einträge auflösen - gibt aber einen Fehler aus, wenn der Eintrag zu mehr als einer IP-Adresse aufgelöst wird (Fehler: Hostname löst zu mehreren Adressen auf).

Siehe: `NFTables Addon DNS <https://github.com/O-X-L/nftables_addon_dns>`_

IPLists
*******

Dieses Addon wurde von der `gleichen Funktionalität inspiriert, die auf OPNSense <https://docs.opnsense.org/manual/how-tos/edrop.html#configure-spamhaus-e-drop>`_ angeboten wird.

Es lädt vorhandene IPListen herunter und fügt sie als NFTables-Variablen hinzu.

IPList Beispiele:

* `Spamhaus DROP <https://www.spamhaus.org/drop/drop.txt>`_
* `Spamhaus EDROP <https://www.spamhaus.org/drop/edrop.txt>`_
* `Tor exit nodes <https://check.torproject.org/torbulkexitlist>`_

Siehe: `NFTables Addon IPList <https://github.com/O-X-L/nftables_addon_iplist>`_

Failover
********

Siehe: `NFTables Addon Failover <https://github.com/O-X-L/nftables_addon_failover>`_


----

Konfiguration
#############

`NFTables Grundkonfiguration Beispiel <https://docs.o-x-l.com/en/latest/_static/raw/fw_nftables_base.txt>`_

.. _fw_nftables_tproxy:

TPROXY
******

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
-----

* `Kernel - TPROXY <https://docs.kernel.org/networking/tproxy.html>`_
* `PowerDNS - TPROXY <https://powerdns.org/tproxydoc/tproxy.md.html>`_
* `Squid - TPROXY <http://wiki.squid-cache.org/Features/Tproxy4>`_
* `Policy Routing - TPROXY <https://serverfault.com/questions/1052717/how-to-translate-ip-route-add-local-0-0-0-0-0-dev-lo-table-100-to-systemd-netw>`_
* `NFTables source - TPROXY <https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/net/netfilter/nft_tproxy.c>`_
* `Kernel source - TPROXY <http://git.netfilter.org/nftables/commit/?id=2be1d52644cf77bb2634fb504a265da480c5e901>`_

Nutzung
-------

Eine Sache müssen Sie wissen: Die Operation TPROXY kann nur in der Kette  **prerouting - filter (mangle)** verwendet werden!

Verkehr, der diese Chain/Hook standardmäßig durchläuft, kann leicht über einen Proxy geleitet werden.


**OUTPUT CHALLENGE:**

Aus diesem Grund kann der Verkehr, der am 'output' (*vom selben Host*) eingeht, nicht direkt umgeleitet werden.

Wir müssen ihn an 'loopback' weiterleiten, damit er 'prerouting' durchläuft.

HINWEIS: Dieses Bild zeigt das Problem, mit dem wir konfrontiert sind, in einer sehr abstrakten Weise. Es kann sein, dass es den Verkehrsfluss nicht korrekt darstellt!

|nft_tproxy|


**REMOTE PROXY CHALLENGE:**

Möglicherweise möchten Sie einen remote Proxyserver ansteuern. Dies ist jedoch meist nicht einfach über ein DNAT möglich.

Man müsste ein Proxy-Forwarder-Tool verwenden, das dies für Sie erledigen kann.

Wir haben ein bestehendes Tool für genau diesen Zweck gepatched: `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_

Mit einem solchen Tool können Sie den von TPROXY empfangenen reinen Datenverkehr verpacken und weiterleiten oder tunneln.

.. code-block:: text

    # NFTables =TCP=> TPROXY (forwarder @ 127.0.0.1) =HTTP[TCP]=> PROXY

    > curl https://www.o-x-l.com
    # proxy-forwarder
    2023-08-29 20:49:10 | INFO | handler | 192.168.11.104:36386 <=> www.o-x-l.com:443/tcp | connection established
    # proxy (squid)
    NONE_NONE/200 0 CONNECT www.o-x-l.com:443 - HIER_NONE/- -
    TCP_TUNNEL/200 6178 CONNECT www.o-x-l.com:443 - HIER_DIRECT/www.o-x-l.com -

    > curl http://www.o-x-l.com
    # proxy-forwarder
    2023-08-29 20:49:07 | INFO | handler | 192.168.11.104:50808 <=> www.o-x-l.com:80/tcp | connection established
    # proxy (squid)
    TCP_REFRESH_MODIFIED/301 477 GET http://www.o-x-l.com/ - HIER_DIRECT/www.o-x-l.com text/html



Examples
--------

* `NFTables TPROXY Beispiel <https://gist.github.com/superstes/6b7ed764482e4a8a75334f269493ac2e>`_, `local NFTables TPROXY Beispiel <https://docs.o-x-l.com/en/latest/_static/raw/fw_nftables_tproxy.txt>`_
* `IPTables TPROXY Beispiel <https://gist.github.com/superstes/c4fefbf403f61812abf89165d7bc4000>`_, `local IPTables TPROXY Beispiel <https://docs.o-x-l.com/en/latest/_static/raw/fw_iptables_tproxy.txt>`_

----

Examples
########

Ansible
*******

See: `Ansible-basiertes Beispiel <https://github.com/ansibleguy/infra_nftables/blob/latest/docs/UseCaseExamples.md>`_

IPv4 Baseline
*************


IPv6 Baseline
*************


Security Baseline
*****************


Docker host
***********


Proxmox host (PVE)
******************


Forwarder (Router, Network firewall, VPN Server)
************************************************


----

Integrations
############

Fail2Ban
********


Squid
*****

.. include:: ../_include/user_rath.rst
