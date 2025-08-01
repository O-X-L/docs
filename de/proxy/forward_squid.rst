.. _proxy_forward_squid:

.. include:: ../_include/head.rst

.. |squid_remote| image:: ../_static/img/proxy_forward_squid_remote.png
   :class: wiki-img
   :alt: OXL Docs - Proxy Remote Forwarding

*********************
Forward Proxy - Squid
*********************

.. include:: ../_include/wip.rst

.. warning::

  Mit dieser Anwendung können Sie den Netzwerkverkehr abfangen und verändern.

  Das kann illegal sein => Sie sind gewarnt.

----

Intro
#####

Wenn wir uns auf einen „Client“ beziehen, handelt es sich in den meisten Fällen um einen Server, eine Arbeitsstation oder ein Netzwerkgerät.

Hinweis: Squid kann auch als Reverse-Proxy verwendet werden, aber diese Dokumentation konzentriert sich auf seine Forward-Proxy-Funktionalität.

**Intro Videos:** `YouTube @OXL-IT <https://www.youtube.com/playlist?list=PLsYMit2eI6VUrHgpqH4CCOYzLzQu0L_ze>`_

----

Setup
*****

Manual
======



Docker
======

Sie können ein Docker-Image erstellen, wie in `diesem Repository zu sehen  <https://github.com/O-X-L/squid-openssl-docker>`_!


----

Links
*****

* `Beispiel-Config <https://wiki.squid-cache.org/ConfigExamples/>`_ (*WARNUNG: einige Beispiele sind veraltet und funktionieren nicht mit aktuellen Versionen*)


----

Installation
############

SSL
***

If you are only 'peaking' at SSL connections - this should be enough:

Wenn Sie nur den Server-Name-Identifier aus dem TLS-Handshake auslesen möchte, sollte dies ausreichend sein:

.. code-block:: bash

    sudo apt install squid-openssl  # the package needs to have ssl-support enabled at compile-time

    mkdir /usr/share/squid/ssl
    chmod 750 /usr/share/squid/ssl

    openssl dhparam -outform PEM -out /usr/share/squid/bump.dh.pem 2048

    # openssl create self-signed cert
    openssl ecparam -out /usr/share/squid/bump.key -name prime256v1 -genkey
    openssl req -new -x509 -nodes -key /usr/share/squid/bump.key -out /usr/share/squid/bump.crt -days 3650 -subj "/CN=Forward Proxy"

    chown -R root:proxy /usr/share/squid/ssl

Wenn Sie SSL-Verbindungen abfangen wollen (*Man-in-the-middle-like*), müssen Sie einige weitere Schritte durchführen: `squid docs - ssl interception <https://wiki.squid-cache.org/ConfigExamples/Intercept/SslBumpExplicit>`_

Unter anderem muss man für eine volle TLS-Interception eine Sub-CA und Zertifikats-Cache/-DB erstellen:

.. code-block:: bash

    # todo: replace self-signed certs with a Sub-CA your clients and network devices trust - as the proxy needs to spoof the destination certificates

    # create ssl cache DB
    /usr/lib/squid/security_file_certgen -c -s /usr/share/squid/ssl_db -M 20MB
    chown -R proxy:proxy /usr/share/squid/ssl_db
    chmod 700 /usr/share/squid/ssl_db

    # inside the squid config:
    # add the parameters 'generate-host-certificates=on dynamic_cert_mem_cache_size=20MB' to your listeners
    sslcrtd_program /usr/lib/squid/security_file_certgen -s /usr/share/squid/ssl_db -M 20MB
    sslcrtd_children 5 startup=5 idle=1

----

Modi
####

----

HTTP_PORT
*********

Der Modus :code:`http_port` kann als Zielproxy in Anwendungen sowie Browsern verwendet werden.

Der Port 3128 wird üblicherweise für diesen Modus verwendet.

Die Anwendung erstellt einen HTTP-CONNECT-Tunnel zum Proxy und verpackt ihre Requests darin.

Die DNS-Auflösung erfolgt durch den Proxy.

HTTPS_PORT
**********

Wie Modus :code:`http_mode`, aber der HTTP-CONNECT-Tunnel ist mit TLS ummantelt.

Der übliche Port 3129 wird für diesen Modus verwendet.

Damit der Proxy die DNS-Auflösung durchführen kann, muss **ssl-bump** konfiguriert sein. Andernfalls ist der Proxy nicht in der Lage, den im TLS-Handshake verwendeten Server-Name-Identifier zu lesen.

INTERCEPT
*********

In diesem Modus erwartet der Proxy, dass der reine Datenverkehr ankommt.

Sie müssen einen eigenen Listener mit aktiviertem **ssl-bump** erstellen, wenn Sie TLS-Verkehr verarbeiten wollen.

Siehe auch:

* `Squid Dokumentation - interception <https://wiki.squid-cache.org/SquidFaq/InterceptionProxy>`_
* `Squid Dokumentation - policy routing <https://wiki.squid-cache.org/ConfigExamples/Intercept/IptablesPolicyRoute>`_


SSL-BUMP
********

SSL-BUMP ermöglicht es uns:

* TLS-Handshake-Informationen lesen
* TLS-Verkehr abzufangen (*lesen/ändern*)

PEAK
====

By *peaking* at TLS handshake information in ssl-bump step-1 we are able to gain some important information:

Indem wir in die TLS-Handshake-Informationen in ssl-bump Schritt-1 *peaken* können wir einige wichtige Informationen gewinnen:

* Ziel-DNS/Hostname aus SNI

**Vorteile:**

* weniger Leistung als bei vollständiger SSL-interception erforderlich
* schneller als vollständige SSL-interception
* weniger Probleme mit Anwendungen, die Zertifikate auf ihrer Seite prüfen (*z.B. Banken*)
* keine Notwendigkeit, eine interne Sub-CA zu erstellen/verwalten, um dynamisch Zertifikate für SSL-intercepted Ziele zu erstellen und zu signieren

**Nachteile:**

* weniger Möglichkeiten, den Datenverkehr zu filtern
* Verbindungen zu *vertrauenswürdigen* Zielen können gefährliche Nutzdaten enthalten
* funktioniert nicht mehr, wenn der Zielserver `encrypted SNI <https://www.cloudflare.com/learning/ssl/what-is-encrypted-sni/>`_ erzwingt

In einigen Fällen reicht eine einfache DNS-Allowlist aus, um eine gute Sicherheit zu gewährleisten. Viele automatisierte Angriffe können mit diesem Ansatz blockiert werden.

INTERCEPT
=========

Diese wird in **Zero-Trust** Umgebungen verwendet.

Siehe auch: :ref:`TLS interception <proxy_tls_interception>`

**Notiz**:

...

    Selbst bei falschem Einsatz von TLS ist es für mindestens ein Ende des Kommunikationskanals möglich, die Existenz des Proxys zu erkennen.
    Squid SSL-Bump ist absichtlich so implementiert, dass diese Erkennung möglich ist, ohne das TLS zu brechen.
    Ihre Clients werden **in der Lage sein, die Existenz des Proxys zu erkennen**.
    Wenn Sie nach einer Möglichkeit suchen, dies in völliger Geheimhaltung zu tun, sollten Sie Squid nicht verwenden.

**Vorteile:**

* ssl-interception gibt uns viele Informationen, die für IPS/IDS-Prüfungen verwendet werden können
* mögliche gefährliche Nutzdaten wie Downloads können von Anti-Virus überprüft werden
* Mehr Einschränkungen erschweren selbst interaktive Angriffe.

**Nachteile:**

* komplexer Regelsatz, wenn Sie einen *impliziten Verweigerungsansatz* wählen
* viel mehr Leistung erforderlich
* zunehmende Latenzzeit
* mit einem schlechten Regelsatz werden Sie immer noch Sicherheitslücken haben, aber auch eine schlechtere Leistung (*lose-lose*)

----

TPROXY
******

TProxy ist eine Funktion, die in aktuelle Kernel eingebaut ist.

Sie ermöglicht es uns, den Verkehr umzuleiten, ohne ihn zu verändern. Dies löst das Problem der überschriebenen Ziel-IPs bei der Verwendung von Destination-NAT.

Die beiden wichtigsten Integrationen von TPROXY, auf die wir uns konzentrieren werden, sind die in IPTables und NFTables.

NFTables
========

Siehe: :ref:`NFTables TProxy <fw_nftables_tproxy>`


IPTables
========

Siehe: `IPTables TPROXY <https://gist.github.com/superstes/c4fefbf403f61812abf89165d7bc4000>`_

----

Config
######

`Config Optionen <https://docs.o-x-l.com/_static/raw/proxy_squid_config_options.txt>`_

Know-How
========

* Alle Subdomains einer Domain können mit einem vorangestellten Punkt abgeglichen werden (*'wildcard' matching*)

  Beispiel: '.example.com'

  Sie dürfen nicht alle 'example.com' und '.example.com' verwenden, da dies zu einem Syntaxfehler führt.

* Möglicherweise möchten Sie Port-Proben aus Ihren Logs ausschließen und das Log-Format anpassen:

    .. code-block:: text

        acl hasRequest has request

        # syslog usage:
        logformat custom_log [%>a]:%>p %Ss/%03>Hs:%Sh "%rm %ru HTTP/%rv" %mt %>Hs %<st %tr "%{User-Agent}>h" "%{Referer}>h"
        logfile_rotate 0
        access_log syslog:local2 custom_log hasRequest

        # log-file usage: (with timestamp)
        # logformat custom_log %{%Y-%m-%d %H:%M:%S}tl [%>a]:%>p %Ss/%03>Hs:%Sh "%rm %ru HTTP/%rv" %mt %>Hs %<st %tr "%{User-Agent}>h" "%{Referer}>h"
        access_log /var/log/squid/access.log custom_log hasRequest

.. _proxy_forward_squid_cnf:

Baseline
========

Sie müssen **Listeners definieren**:

Siehe auch: `Squid Dokumentation - http_port <http://www.squid-cache.org/Doc/config/http_port/>`_

.. code-block:: text

    # clients =HTTP[TCP]=> SQUID =TCP=> TARGET
    http_port 3128 ssl-bump tcpkeepalive=60,30,3 cert=/usr/share/squid/bump.crt key=/usr/share/squid/bump.key cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS tls-dh=prime256v1:/usr/share/squid/bump.dh.pem options=NO_SSLv3,NO_TLSv1

    # clients =HTTPS[TCP]=> SQUID =TCP=> TARGET
    https_port 3128 ssl-bump tcpkeepalive=60,30,3 cert=/usr/share/squid/bump.crt key=/usr/share/squid/bump.key cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS tls-dh=prime256v1:/usr/share/squid/bump.dh.pem options=NO_SSLv3,NO_TLSv1

    # clients =ROUTED TCP=> SQUID =TCP=> TARGET
    http_port 3129 intercept
    https_port 3130 intercept ssl-bump tcpkeepalive=60,30,3 cert=/usr/share/squid/bump.crt key=/usr/share/squid/bump.key cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS tls-dh=prime256v1:/usr/share/squid/bump.dh.pem options=NO_SSLv3,NO_TLSv1

    # clients =TPROXY TCP=> SQUID (@127.0.0.1) =TCP=> TARGET
    http_port 3129 tproxy
    https_port 3130 tproxy ssl-bump tcpkeepalive=60,30,3 cert=/usr/share/squid/bump.crt key=/usr/share/squid/bump.key cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS tls-dh=prime256v1:/usr/share/squid/bump.dh.pem options=NO_SSLv3,NO_TLSv1
    spoof_client_ip deny all

Sie können die **IPs definieren, die Squid für den ausgehenden Verkehr verwenden soll**. Dies kann nützlich sein, um spezifische Firewall-Regeln für diese Adressen zu definieren:

.. code-block:: text

    tcp_outgoing_address 192.168.10.2
    tcp_outgoing_address 2001:db8::1:2

Einige Settings sind zur Security empfohlen:

.. code-block:: text

    httpd_suppress_version_string on
    via off
    reply_header_access Server deny all
    reply_header_access X-Squid-Error deny all
    reply_header_access X-Cache deny all
    reply_header_access X-Cache-Lookup deny all
    follow_x_forwarded_for allow localhost
    follow_x_forwarded_for deny all
    request_header_access X-Forwarded-For deny all
    forwarded_for delete
    http_access deny manager
    tls_outgoing_options options=NO_SSLv3,NO_TLSv1 cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS
    http_access deny !localhost to_localhost

IPv6 aktivieren:

.. code-block:: text

    acl src_proto_ip6 src ipv6
    acl dst_proto_ip6 dst ipv6
    http_access deny src_proto_ip6 !all
    http_access deny dst_proto_ip6 !all

Zumindest diese grundlegenden Filter sollten Sie abdecken:

* **Erlaube nur..**

  * spezifische Ziel Ports

    .. code-block:: text

        acl dest_ports port 80
        acl dest_ports port 443
        acl dest_ports port 587
        http_access deny !dest_ports

  * Proxy Zugriff nur **von bestimmten Netzen aus** erlauben

    .. code-block:: text

        acl src_internal src 127.0.0.0/8
        acl src_internal src 192.168.0.0/16
        acl src_internal src 172.16.0.0/12
        acl src_internal src 10.0.0.0/8
        http_access deny !src_internal

  * nur Zugriff **auf spezifische Ziel Netze** zulassen

    * filter on an IP-basis

      .. code-block:: text

          acl dst_internal dst 192.168.0.0/16
          acl dst_internal dst 172.16.0.0/12
          acl dst_internal dst 10.0.0.0/8
          http_access allow dst_internal
          http_access deny all

    * auf DNS-basis filtern (*SSL-Bump 'Peak' benötigt*)

      .. code-block:: text

          acl domains_allowed dstdomain example.com
          acl domains_allowed dstdomain www.O-X-L.com
          http_access allow domains_allowed
          http_access deny all

    * zu spezifischen Zeiten Zugriffe freigeben oder blockieren

      Tages-Kürzel: :code:`M=Montag, T=Dienstag, W=Mittwoch, H=Donnerstag, F=Freitag, A=Samstag, S=Sonntag`

      .. code-block:: text

          acl time_lunch MTWHF 11:30-13:30
          acl domains_lunch dstdomain .youtube.com
          http_access allow time_lunch domains_lunch

          acl time_evening 20:00-22:00
          http_access deny all time_evening

* **Server Zertifikate** auf Fehler prüfen (*expired, untrusted, weak ciphers*)

  .. code-block:: text

      tls_outgoing_options options=NO_SSLv3,NO_TLSv1 cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS
      acl ssl_exclude_verify dstdomain .example.com
      sslproxy_cert_error allow ssl_exclude_verify
      sslproxy_cert_error deny all

* **ssl-bump 'peaking'** aktivieren

  .. code-block:: text

      # add the parameter 'generate-host-certificates=off' to your listeners

      acl CONNECT method CONNECT
      acl ssl_ports port 443
      acl step1 at_step SslBump1

      http_access deny CONNECT !ssl_ports
      http_access allow CONNECT step1  # without 'step1' here one would be able to 'tunnel' unwanted traffic through the proxy
      ssl_bump peek step1 ssl_ports
      ssl_bump splice all

----

Service
#######

Um zu verhindern, dass eine invalide Konfiguration Ihren :code:`squid.service` tötet, können Sie einen Config-Check hinzufügen:

.. code-block:: text

    # /etc/systemd/system/squid.service.d/override.conf

    [Service]
    ExecStartPre=
    ExecStartPre=/usr/sbin/squid -k parse
    ExecStartPre=/usr/sbin/squid --foreground -z

    ExecReload=
    ExecReload=/usr/sbin/squid -k parse
    ExecReload=/bin/kill -HUP $MAINPID

    Restart=on-failure
    RestartSec=5s

Dadurch werden Konfigurationsfehler abgefangen und protokolliert, bevor ein Neuladen/Neustart durchgeführt wird.

Bei einem System-Neustart wird es immer noch fehlschlagen, wenn die Konfiguration fehlerhaft ist.

----

Beispiele
#########

----

Transparent Proxy
*****************

Manchmal kann das Setzen der Umgebungsvariablen 'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy' und 'https_proxy' für alle Anwendungen und HTTP-Clients problematisch/zu inkonsistent sein.

Ein Angreifer könnte auch in der Lage sein, die Umgebungsvariablen zu ändern, sobald eine Sicherheitslücke ausgenutzt wurde.

Um den :code:`inspection` oder :code:`tproxy` Modus nutzen zu können **MUSS** ein DNS-caching Server implementiert werden: :ref:`DNS Cache Docs <net_dns_cache>`

Destination NAT
===============

In einigen älteren Anleitungen und Beiträgen sehen Sie, dass DNAT-Verkehr von einem 'Client-System' zu einem remote Proxy-Server leiten.

Dies wird von Squid **NICHT UNTERSTÜTZT**.

Es wird zu einer Fehlermeldung wie dieser führen: 'Forwarding loop detected'

Warum ist das so?

Die transparenten Betriebsmodi von Squid übernehmen KEINE DNS-Auflösung! Stattdessen verwenden sie die tatsächliche Ziel-IP aus dem IP-Header und senden den ausgehenden Verkehr dorthin. Dieses Verhalten hat `eine Sicherheits-Schwachstelle <http://www.squid-cache.org/Advisories/SQUID-2011_1.txt>`_ zu Grunde.

Bei Verwendung von DNAT wird die Ziel-IP auf die IP des Proxys gesetzt. Daher => loop.

----

Routed Traffic
==============

Sie können diese Option verwenden, wenn der Proxyserver ein Layer-2-Netzwerk mit dem System teilt, das den Datenverkehr sendet oder weiterleitet.

Praktische Beispiele hierfür:

* Netzwerk-Gateway (*Router*) sendet Verkehr zum Abfangen an den Proxy
* 'Client-Geräte' verwenden den Proxy als Gateway anstelle des eigentlichen Routers

In diesem Fall müssen wir Squid-Listener im **intercept** oder **tproxy** einrichten, um den Datenverkehr zu verarbeiten.

----

Forwarded Traffic
=================

In manchen Situationen können Sie die Option zur Weiterleitung des Datenverkehrs an den Proxy nicht nutzen.

Dies kann der Fall sein:

* Sie haben keine Kontrolle über das Gateway/den Router
* das 'Client-Gerät' isoliert ist (*nur mit dem WAN verbunden ist*)
* Client- und/oder Netzwerkeinschränkungen lassen eine Umleitung des Datenverkehrs nicht zu

Praktische Beispiele hierfür:

* Ein Cloud-VPS oder Root-Server, der nur mit dem WAN verbunden ist
* Verteilte Systeme, die einen zentralen Proxy verwenden (*z.B. beim Kunden vor Ort*)

In diesem Fall benötigen wir möglicherweise andere Tools wie `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_ um die Weiterleitung abzuhandeln:


.. code-block:: text

    > curl https://www.O-X-L.com
    # proxy-forwarder
    2023-08-29 20:49:10 | INFO | handler | 192.168.11.104:36386 <=> www.O-X-L.com:443/tcp | connection established
    # squid
    NONE_NONE/200 0 CONNECT www.O-X-L.com:443 - HIER_NONE/- -
    TCP_TUNNEL/200 6178 CONNECT www.O-X-L.com:443 - HIER_DIRECT/www.O-X-L.com -

    > curl http://superstes.eu
    # proxy-forwarder
    2023-08-29 20:49:07 | INFO | handler | 192.168.11.104:50808 <=> www.O-X-L.com:80/tcp | connection established
    # squid
    TCP_REFRESH_MODIFIED/301 477 GET http://www.O-X-L.com/ - HIER_DIRECT/www.O-X-L.com text/html


|squid_remote|

----

Troubleshooting
###############

Was funktioniert nicht?
***********************

Vielleicht möchten Sie einige andere Möglichkeiten ausprobieren, um Datenverkehr an einen Squid-Proxy zu senden/umzuleiten.

Hier sind einige Beispiele, die **NICHT FUNKTIONIEREN**

* DNAT zum remote Squid-Server im transparenten Modus

  .. code-block:: bash

      # journalctl -u squid.service -n 50
      ...
      WARNING: Forwarding loop detected for
      ...
      TCP_MISS/403 ORIGINAL_DST/<proxy-ip>
      ...


* DNAT 80/443 zu Squid im nicht-transparenten Modus

  .. code-block:: bash

      # journalctl -u squid.service -n 50
      ...
      Missing or incorrect access protocol
      ...
      NONE/400
      ...


* IPTables/NFTables TPROXY zu `socat forwarder <https://manpages.debian.org/unstable/socat/socat.1.en.html>`_

  SOCat empfängt den Datenverkehr korrekt und leitet ihn weiter, verhält sich aber praktisch wie eine DNAT-Operation

  .. code-block:: bash

      # 'client'
      socat tcp-listen:3129,reuseaddr,fork,bind=127.0.0.1,ip-transparent tcp:<proxy-ip>:3129

      # journalctl -u squid.service -n 50
      ...
      WARNING: Forwarding loop detected for
      ...
      TCP_MISS/403 ORIGINAL_DST/<proxy-ip>
      ...


* Abfang/TPROXY-Modus mit Squid im Docker-Container

  Es scheint als würde Docker den Datenverkehr NATen.

  .. code-block:: bash

      ERROR: NF getsockopt(ORIGINAL_DST) failed on conn18 local=192.168.0.2:3130 remote=192.168.0.1:48910 FD 12 flags=33: (2) No such file or directory
      ERROR: NAT/TPROXY lookup failed to locate original IPs on conn18 local=192.168.0.2:3130 remote=192.168.0.1:48910 FD 12 flags=33


Bekannte Probleme
*****************


* **Clients haben viele Zeitüberschreitungen**

  Es kann sein, dass Ihr Cache zu klein ist.

  Dies kann der Fall sein, wenn viele Anfragen in einem kurzen Zeitraum auf den Proxy zukommen.

  **Mögliche Lösungen:**

    * Den main cache erweitern:

      :code:`cache_mem 1024 MB` (siehe `docs - cache_mem <http://www.squid-cache.org/Versions/v4/cfgman/cache_mem.html>`_)

    * Den session cache erweitern:

      :code:`sslproxy_session_cache_size 512 MB`

    * Den ssl cache erweitern (*wenn du SSL aufbrichst*)

      ssl_db => :code:`sslcrtd_program /usr/lib/squid/security_file_certgen -s /usr/share/squid/ssl_db -M 256M`

    * Das SSL session timeout erhöhen

      :code:`sslproxy_session_ttl 600`


* **Bus error**

  Es scheint, dass dies passiert, wenn der Wert von :code:`sslproxy_session_cache_size` größer ist als der von :code:`ssl_db`.


* **NONE_NONE/409 & SECURITY ALERT: Host header forgery detected**

  Dieser Fehler kann auftreten, wenn der Squid-Proxy im Modus :code:`intercept` läuft und den Ziel-Hostnamen zu einer anderen IP als der des Clients auflöst.

  Diese Prüfung kann gegen Angriffe helfen, die den Proxy austricksen, damit er bösen Datenverkehr zulässt.

  Da die heutigen DNS-Server sehr niedrige TTLs verwenden, kann es vorkommen, dass ein Teil des Verkehrs diesen Check als falsch-positiv auslöst.

  **Um diese Problem zu lösen MUSS ein DNS-Caching Server implementiert werden**: :ref:`DNS Cache Docs <net_dns_cache>`

  Sie können diese Check **für HTTP (plaintext) Verkehr** deaktivieren, indem Sie :code:`host_verify_strict off` setzen (*Standard*)

  **HTTPS-Verkehr** wird aus einem unklaren Grund immer noch fehlschlagen :(

  Siehe auch: `Squid wiki - host_verify_strict <http://www.squid-cache.org/Doc/config/host_verify_strict/>`_ & `Squid wiki - host header forgery <https://wiki.squid-cache.org/KnowledgeBase/HostHeaderForgery>`_

  Sie können natürlich den `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_ nutzen um den abgefangenen TCP-Verkehr in HTTP- und HTTPS-Anfragen zu übersetzen, die Sie an den 'Forward-Proxy'-Port von Squid senden können. (*diese Prüfung wird ignoriert...*)

* **NONE_NONE/500:HIER_NONE** auf Squid <=5.7 || **NONE_NONE/503:HIER_NONE** auf Squid >=6.13

  Beispiel Logs:

  .. code-block:: bash

      # Squid v5.7
      [<CLIENT-IP>]:43586 NONE_NONE/200:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 200 0 36 "Debian APT-HTTP/1.3 (2.6.1)" "-"
      [<CLIENT-IP>]:43586 NONE_NONE/500:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 500 0 0 "-" "-"

      # Squid v6.13
      [<CLIENT-IP>]:51454 NONE_NONE/200:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 200 0 29 "Debian APT-HTTP/1.3 (2.6.1)" "-"
      [<CLIENT-IP>]:51454 TCP_TUNNEL/503:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 503 0 0 "-" "-"

  Diese Fehler weisen auf Verbindungsprobleme vom Proxy ausgehen hin.

  In unserem Fall machte der :ref:`lokale DNS-Resolver/-Cache <net_dns_cache>` Probleme, da wir dort DNSSEC aktiviert hatten. Dies führte teilweise zu Fehlern beim Verbindungsaufbau.

.. include:: ../_include/user_rath.rst
