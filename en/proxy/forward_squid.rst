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

  This application let's you intercept and modify network traffic.

  That can be illegal => you are warned.

----

Intro
#####

Whenever we are referring to a 'client' - it will be a server, workstation or network device in most cases.

Note: Squid can also be used as a reverse proxy, but this documentation will focus on its forward-proxy functionality.

**Intro Videos:** `YouTube @OXL-IT <https://www.youtube.com/playlist?list=PLsYMit2eI6VXwe0jaSggxvVw1diOfJ5bn>`_

----

Setup
*****

Manual
======



Docker
======

You can build a docker image as seen `in this repository <https://github.com/O-X-L/squid-openssl-docker>`_!


----

References
**********

* `Config examples <https://wiki.squid-cache.org/ConfigExamples/>`_ (*WARNING: some examples are deprecated and will not work on current versions*)


----

Installation
############

SSL
***

If you only want to read the Server-Name-Identifier from the TLS-Handshake - this should be enough:

.. code-block:: bash

    sudo apt install squid-openssl  # the package needs to have ssl-support enabled at compile-time

    mkdir /usr/share/squid/ssl
    chmod 750 /usr/share/squid/ssl

    openssl dhparam -outform PEM -out /usr/share/squid/ssl/bump.dh.pem 2048

    # openssl create self-signed cert
    openssl ecparam -out /usr/share/squid/ssl/snakeoil.key -name prime256v1 -genkey
    openssl req -new -x509 -nodes -key /usr/share/squid/ssl/snakeoil.key -out /usr/share/squid/ssl/snakeoil.crt -days 3650 -subj "/CN=Forward Proxy"

    chown -R root:proxy /usr/share/squid/ssl

If you want to intercept SSL connections (*Man-in-the-middle like*) - you will have to go through some more steps: `squid docs - ssl interception <https://wiki.squid-cache.org/ConfigExamples/Intercept/SslBumpExplicit>`_

As part of full TLS-interception you will need to create a Sub-CA and configure a cache/DB for the auto-generated spoofed certificates:

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

Modes
#####

----

HTTP_PORT
*********

The :code:`http_port` mode can be used as target proxy in applications like browsers.

Usual port 3128 is used for this mode.

The application creates a HTTP-CONNECT tunnel to the proxy and wraps its requests in it.

DNS resolution is done by the proxy.

HTTPS_PORT
**********

Like mode :code:`http_mode` but the HTTP-CONNECT tunnel is wrapped in TLS.

Usual port 3129 is used for this mode.

For the proxy to be able to handle the DNS resolution - **ssl-bump** must be configured. Else the proxy will not be able to read the Server-Name-Identifier used in the TLS handshake.

INTERCEPT
*********

In this mode the proxy will expect the plain traffic to arrive.

You will have to create a dedicated listener with **ssl-bump** enabled if you want to handle TLS traffic.

See also:

* `Squid documentation - interception <https://wiki.squid-cache.org/SquidFaq/InterceptionProxy>`_
* `Squid documentation - policy routing <https://wiki.squid-cache.org/ConfigExamples/Intercept/IptablesPolicyRoute>`_


SSL-BUMP
********

SSL-BUMP allows us to:

* read TLS handshake information
* intercept (*read/modify*) TLS traffic

PEAK
====

By *peaking* at TLS handshake information in ssl-bump step-1 we are able to gain some important information:

* target DNS/hostname from SNI

**Benefits:**

* less performance needed than full ssl-interception
* faster than full ssl-interception
* less problems with applications that check certificates on their end (*p.e. banking*)
* no need to create/manage an internal Sub-CA to dynamically create and sign certificates for ssl-intercepted targets

**Drawbacks:**

* less options to filter the traffic on
* connections to *trustable* targets could carry dangerous payloads
* will stop working if `encrypted SNI <https://www.cloudflare.com/learning/ssl/what-is-encrypted-sni/>`_ is enforced by the target server

In some cases a basic DNS 'allow-list' will be enough to ensure good security. Many automated attacks can be blocked using this approach.


INTERCEPT
=========

This one will be used in **zero-trust** environments.

See also: :ref:`TLS interception <proxy_tls_interception>`

**Note**:

...

    Even incorrectly used TLS usually makes it possible for at least one end of the communication channel to detect the proxies existence.
    Squid SSL-Bump is intentionally implemented in a way that allows that detection without breaking the TLS.
    Your clients **will be capable of identifying the proxy exists**.
    If you are looking for a way to do it in complete secrecy, dont use Squid.

**Benefits:**

* ssl-interception gives us much information that can be used to run IPS/IDS checks on
* possible dangerous payloads like downloads can be checked by anti-virus
* more restrictions make even interactive attacks harder to go through

**Drawbacks:**

* complex ruleset if you go with an *implicit-deny* approach
* much more performance needed
* increasing latency
* with a bad ruleset you will still have security-leaks but also have worse performance (*lose-lose*)

----

TPROXY
******

TProxy is a functionality built into current kernels.

It allows us to redirect traffic without modifying it. This solves the issue with overwritten destination-IPs by using Destination-NAT.

The major two integrations of TPROXY we will focus on are the ones in IPTables and NFTables.

NFTables
========

See: :ref:`NFTables TProxy <fw_nftables_tproxy>`


IPTables
========

See: `IPTables TPROXY <https://gist.github.com/superstes/c4fefbf403f61812abf89165d7bc4000>`_

----

Config
######

`Config options <https://docs.o-x-l.com/_static/raw/proxy_squid_config_options.txt>`_

Know-How
========

* Matching all subdomains of a Domain can be done by prepending a dot (*'wildcard' matching*)

  Example: '.example.com'

  You may not all 'example.com' and '.example.com' as it will result in a syntax error

* You may want to exclude Port-Probes from your logs and change the log-format:

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

You **need to define listeners**:

See also: `Squid documentation - http_port <http://www.squid-cache.org/Doc/config/http_port/>`_

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

You can define the **IPs Squid should use for outbound traffic**. This can be useful to define specific firewall rules for those addresses:

.. code-block:: text

    tcp_outgoing_address 192.168.10.2
    tcp_outgoing_address 2001:db8::1:2

These are some security-hardening settings:

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

Enable IPv6:

.. code-block:: text

    acl src_proto_ip6 src ipv6
    acl dst_proto_ip6 dst ipv6
    http_access deny src_proto_ip6 !all
    http_access deny dst_proto_ip6 !all


You may want to cover at least those basic filters:

* **only allow**

  * specific destination ports

    .. code-block:: text

        acl dest_ports port 80
        acl dest_ports port 443
        acl dest_ports port 587
        http_access deny !dest_ports

  * only allow proxy-access **from specific source** networks

    .. code-block:: text

        acl src_internal src 127.0.0.0/8
        acl src_internal src 192.168.0.0/16
        acl src_internal src 172.16.0.0/12
        acl src_internal src 10.0.0.0/8
        http_access deny !src_internal

  * only allow access **to specific destinations**

    * filter on an IP-basis

      .. code-block:: text

          acl dst_internal dst 192.168.0.0/16
          acl dst_internal dst 172.16.0.0/12
          acl dst_internal dst 10.0.0.0/8
          http_access allow dst_internal
          http_access deny all

    * filter on a DNS-basis (*SSL-Bump 'Peak' needed*)

      .. code-block:: text

          acl domains_allowed dstdomain example.com
          acl domains_allowed dstdomain www.o-x-l.com
          http_access allow domains_allowed
          http_access deny all

    * allow or deny access at specific times

      Day-Codes: :code:`M=Monday, T=Tuesday, W=Wednesday, H=Thursday, F=Friday, A=Saturday, S=Sunday`

      .. code-block:: text

          acl time_lunch MTWHF 11:30-13:30
          acl domains_lunch dstdomain .youtube.com
          http_access allow time_lunch domains_lunch

          acl time_evening 20:00-22:00
          http_access deny all time_evening

* **check server certificates** for issues (*expired, untrusted, weak ciphers*)

  .. code-block:: text

      tls_outgoing_options options=NO_SSLv3,NO_TLSv1 cipher=HIGH:MEDIUM:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS
      acl ssl_exclude_verify dstdomain .example.com
      sslproxy_cert_error allow ssl_exclude_verify
      sslproxy_cert_error deny all

* enable **ssl-bump 'peaking'**

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

To keep invalid configuration from stopping/failing your :code:`squid.service` - you can add a config-validation in it:

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

This will catch and log config-errors before doing a reload/restart.

When doing a system-reboot it will still fail if your config is bad.

----

Examples
########


----

Transparent Proxy
*****************

Sometimes setting the environment-variables 'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy' and 'https_proxy' for all applications and HTTP-clients may be problematic/too inconsistent.

An attacker might also be able to modify the environmental variables once a vulnerability has been exploited.

In :code:`inspection` and :code:`tproxy` mode you **NEED TO** implement a DNS-caching server: :ref:`DNS Cache Docs <net_dns_cache>`

Destination NAT
===============

In some older tutorials and write-ups you will see that people DNAT traffic from a 'client' system to a remote proxy server.

This **IS NOT SUPPORTED** by squid.

It will lead to an error like this: 'Forwarding loop detected'

Why is that?

Squid's transparent operation modes DO NOT handle DNS resolution! They instead use the actual destination IP from the IP-headers and send the outgoing traffic to it. That is because of `some vulnerability <http://www.squid-cache.org/Advisories/SQUID-2011_1.txt>`_

When using DNAT the destination IP is set to the proxy's IP. Therefore => loop.

Routed Traffic
==============

You can use this option if the proxy server shares a Layer 2 network with the system that sends or routes the traffic.

Practical examples of this:

* Network gateway (*router*) sends traffic to proxy for interception
* 'Client' devices use the proxy as gateway instead of the actual router

In this case we will need to set-up Squid listeners in **intercept** or **tproxy** mode to process the traffic.

Forwarded Traffic
=================

In some situations you will not be able to use the option to route the traffic to the proxy.

This might be because:

* you are not controlling the gateway/router
* the 'client' device is isolated (*only connected to WAN*)
* client and/or network restrictions don't allow for re-routing the traffic

Practical examples of this:

* A Cloud VPS or Root Server that is only connected to WAN
* Distributed Systems using a central proxy (*p.e. on-site at customers*)

In this case we might need other tools like `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_ to act as forwarder:


.. code-block:: text

    > curl https://www.o-x-l.com
    # proxy-forwarder
    2023-08-29 20:49:10 | INFO | handler | 192.168.11.104:36386 <=> www.o-x-l.com:443/tcp | connection established
    # squid
    NONE_NONE/200 0 CONNECT www.o-x-l.com:443 - HIER_NONE/- -
    TCP_TUNNEL/200 6178 CONNECT www.o-x-l.com:443 - HIER_DIRECT/www.o-x-l.com -

    > curl http://superstes.eu
    # proxy-forwarder
    2023-08-29 20:49:07 | INFO | handler | 192.168.11.104:50808 <=> www.o-x-l.com:80/tcp | connection established
    # squid
    TCP_REFRESH_MODIFIED/301 477 GET http://www.o-x-l.com/ - HIER_DIRECT/www.o-x-l.com text/html


|squid_remote|

----

Troubleshooting
###############

What does not work?
*******************

One might want to try some other ways of sending/redirecting traffic to a squid proxy.

Here are some examples that **DO NOT WORK**

* Destination NAT to remote Squid server in transparent mode

  .. code-block:: bash

      # journalctl -u squid.service -n 50
      ...
      WARNING: Forwarding loop detected for
      ...
      TCP_MISS/403 ORIGINAL_DST/<proxy-ip>
      ...


* DNAT 80/443 to squid in non-transparent mode

  .. code-block:: bash

      # journalctl -u squid.service -n 50
      ...
      Missing or incorrect access protocol
      ...
      NONE/400
      ...


* IPTables/NFTables TPROXY to `socat forwarder <https://manpages.debian.org/unstable/socat/socat.1.en.html>`_

  SOCat is actually correctly receiving and forwarding the traffic - BUT practically it acts like a DNAT operation

  .. code-block:: bash

      # 'client'
      socat tcp-listen:3129,reuseaddr,fork,bind=127.0.0.1,ip-transparent tcp:<proxy-ip>:3129

      # journalctl -u squid.service -n 50
      ...
      WARNING: Forwarding loop detected for
      ...
      TCP_MISS/403 ORIGINAL_DST/<proxy-ip>
      ...


* Intercept/TPROXY mode with Squid inside docker container

  Essentially docker seems to be NATing the traffic.

  .. code-block:: bash

      ERROR: NF getsockopt(ORIGINAL_DST) failed on conn18 local=192.168.0.2:3130 remote=192.168.0.1:48910 FD 12 flags=33: (2) No such file or directory
      ERROR: NAT/TPROXY lookup failed to locate original IPs on conn18 local=192.168.0.2:3130 remote=192.168.0.1:48910 FD 12 flags=33


Known problems
**************


* **Clients have many timeouts**

  It may be that your cache size is too small.

  This can happen when many requests hit the proxy in a short time period.

  **Possible Solution:**

    * Increase your main cache:

      :code:`cache_mem 1024 MB` (see `docs - cache_mem <http://www.squid-cache.org/Versions/v4/cfgman/cache_mem.html>`_)

    * Increase your session cache:

      :code:`sslproxy_session_cache_size 512 MB`

    * Increase your ssl cache (*only if you intercept ssl*)

      ssl_db => :code:`sslcrtd_program /usr/lib/squid/security_file_certgen -s /usr/share/squid/ssl_db -M 256M`

    * Increase your ssl session timeout

      :code:`sslproxy_session_ttl 600`


* **Bus error**

  It seems this happens when the value of :code:`sslproxy_session_cache_size` is larger than the one of :code:`ssl_db`


* **NONE_NONE/409 & SECURITY ALERT: Host header forgery detected**

  This error can occur whenever the squid proxy runs in :code:`intercept` or :code:`tproxy` mode  and resolves the target hostname to another IP than the client.

  That check can help against attacks that can trick the proxy into allowing bad traffic.

  As today's DNS servers use very low TTLs it might happen that some traffic triggers this check as false-positive.

  **You NEED to implement a DNS-caching server to solve this issue**: :ref:`DNS Cache Docs <net_dns_cache>`

  You can disable this check **for HTTP (plaintext) traffic** by setting :code:`host_verify_strict off` (*default*)

  **HTTPS traffic** will still be forced fail for some unclear reason.. :(

  See also: `Squid wiki - host_verify_strict <http://www.squid-cache.org/Doc/config/host_verify_strict/>`_ & `Squid wiki - host header forgery <https://wiki.squid-cache.org/KnowledgeBase/HostHeaderForgery>`_

  You could - of course use the `proxy-forwarder <https://github.com/O-X-L/proxy-forwarder>`_ to translate the intercepted TCP traffic into HTTP & HTTPS requests that you are able to send to the 'forward-proxy' port of squid. (*that one will ignore that check...*)

* **NONE_NONE/500:HIER_NONE** on Squid <=5.7 || **NONE_NONE/503:HIER_NONE** on Squid >=6.13

  Example logs:

  .. code-block:: bash

      # Squid v5.7
      [<CLIENT-IP>]:43586 NONE_NONE/200:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 200 0 36 "Debian APT-HTTP/1.3 (2.6.1)" "-"
      [<CLIENT-IP>]:43586 NONE_NONE/500:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 500 0 0 "-" "-"

      # Squid v6.13
      [<CLIENT-IP>]:51454 NONE_NONE/200:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 200 0 29 "Debian APT-HTTP/1.3 (2.6.1)" "-"
      [<CLIENT-IP>]:51454 TCP_TUNNEL/503:HIER_NONE "CONNECT deb.debian.org:443 HTTP/1.1" - 503 0 0 "-" "-"

  These errors can be a hint for proxy outbound-connections issues.

  In our case the :ref:`local DNS-resolver/-cache <net_dns_cache>` cause issues as we had activated DNSSEC. This lead to failure of establishing some connections.


.. include:: ../_include/user_rath.rst
