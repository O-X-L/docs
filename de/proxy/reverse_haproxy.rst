.. _proxy_reverse_haproxy:

.. include:: ../_include/head.rst


***********************
Reverse Proxy - HAProxy
***********************


----

Intro
#####

Wenn Sie HAProxy konfigurieren - halten Sie das `Konfigurationshandbuch <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/>`_ bereit/offen! Sie werden es brauchen!

Ansible Role: `ansibleguy/infra_haproxy <https://github.com/ansibleguy/infra_haproxy>`_

Konfiguration
#############

Wann immer Sie die Konfiguration ändern, sollten Sie sie auf Fehler überprüfen:

.. code-block:: bash

    haproxy -c -f /etc/haproxy/haproxy.cfg

    # with multiple config files:
    haproxy -c -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d/


Danach müssen Sie es neu laden:

.. code-block:: bash

    systemctl reload haproxy.service

Grundlagen
**********

ACLs
====

Sie können ACLs definieren, um spezifische Bedingungen festzulegen:

.. code-block:: bash

    acl <NAME> <CONDITION>

    acl net_private src 192.168.0.0/16 172.16.0.0/12 10.0.0.0/8 127.0.0.0/8 ::1

Diese können auch in-line als anonyme ACL verwendet werden - dies ist sinnvoll, wenn Sie sie nur einmal verwenden müssen:

.. code-block:: bash

    <ACTION> if { <CONDITION> }

Daten können auf unterschiedliche Weise verglichen werden:

.. code-block:: bash

    # match as string (hast to be full-match)
    acl domain1 req.hdr(host) -m str oxl.at

    # match case-insensitive
    acl domain1 req.hdr(host) -m str -i oxl.at

    # match an integer
    acl some_digit req.hdr(some-hdr) -m int 1000

    # check if the value exists
    acl has_some_header req.hdr(some-hdr) -m found

    # match if one of some values (has limits => see list-files)
    acl is_country_x res.hdr(X-Geoip-Country) -m str -i CN RU US

    # match beginning of string
    acl path_api path -m beg -i /api/

    # match part of string
    acl path_test path -m sub -i /test/

    # match end of string
    acl path_scripts path -m end -i .php .py

Sie können ACLs mit AND/OR/NOT-Bedingungen kombinieren:

.. code-block:: bash

    acl domains_adm req.hdr(host) -m str -i admin.example.oxl.at
    acl domains_test req.hdr(host) -m str -i test.oxl.at
    acl src_privileged src 192.168.0.48
    acl src_internal src 172.16.0.0/12

    # implicit AND condition
    use_backend be_test if domains_adm src_privileged

    # NOT condition
    http-request deny status 401 if domains_adm !src_privileged

    # OR condition
    http-request redirect code 302 location https://www.oxl.at domains_test || src_internal

    # with inline ACLs
    http-request deny status 400 if { path -m sub -i /.env/ /.git/ } ||

----

Variablen
=========

Variablen können für dynamischere Verwendungszwecke eingesetzt werden.

Beispiel:

.. code-block:: bash

    # set a variable
    http-request set-var(txn.bot) int(1) if !{ req.fhdr(User-Agent) -m found }

    # check if variable exists
    http-request set-var(txn.bot) int(0) if !{ var(txn.bot) -m found }

    # conditions
    http-request deny deny_status 400 if !{ var(txn.bot) -m int 0 }

    # log a variable with max-length of 1 characters
    http-request capture var(txn.bot) len 1

----

Backends
========

Verwenden Sie die Aktion :code:`use_backend`, um die Route zu wählen, die der Verkehr einschlagen soll:

.. code-block:: bash

    frontend fe_web:
        ...
        acl domains_adm req.hdr(host) -m str -i admin.example.oxl.at
        acl src_privileged src 192.168.0.48
        acl domains_test req.hdr(host) -m str -i test.oxl.at

        use_backend be_admin domains_adm src_privileged
        use_backend be_test domains_test

        use_backend be_fallback

    backend be_admin
        mode http
        # use ssl from haproxy to backends
        ## verify using default CA trust-store
        server srv-1 192.168.10.11:443 check ssl verify required

        ## verify using specific CA
        server srv-1 192.168.10.12:443 check ssl verify required ca-file /etc/ssl/certs/internal-ca.crt

        ## skip verification (not recommended)
        server srv-2 192.168.10.13:443 check ssl verify none

    backend be_fallback
        mode http
        http-request redirect code 302 location https://www.oxl.at

Siehe: `HAProxy Backends <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/core-concepts/backends/>`_

----

Basic Auth
==========

Sie können entweder Klartext oder gehashte (empfohlen) Passwörter verwenden.

.. code-block:: bash

    # plaintext
    userlist basic_auth_xyz_plain
        # user <USER> insecure-password <PASSWORD>
        user userTest insecure-password super!Secret

    # hashed; created via: 'mkpasswd -m sha-256 mypassword123'
    userlist basic_auth_xyz_hash
      user userTest password $5$s6Subz0X7FSX2zON$r94OtF6gOfWlGmySwvn3pDFIAHbIpe6mWneueqtBOm/

    backend be_xyz
        mode http
        http-request auth unless { http_auth(basic_auth_xyz_plain) }
        http-request del-header X-User
        http-request del-header X-Auth
        http-request del-header X-Auth-Type
        http-request del-header Authorization

Siehe: `HAProxy Basic-Auth <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/authentication/basic-authentication/>`_

----

HTTP Methods
============

Möglicherweise möchten Sie Verbindungen über nicht verwendete HTTP-Methoden verweigern:

.. code-block:: bash

    http-request deny status 405 default-errorfiles if { method TRACE CONNECT }

----

HTTP Headers
============

Möglicherweise möchten Sie sicherheitsrelevante Header hinzufügen und erzwingen:

.. code-block:: bash

    # Note: use 'set' to add a new header or overwrite it if it already exists; 'add' might duplicate it
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload"
    http-response set-header X-Frame-Options "SAMEORIGIN"
    http-response set-header X-Content-Type-Options "nosniff"
    http-response set-header X-Permitted-Cross-Domain-Policies "none"
    http-response set-header X-XSS-Protection "1; mode=block"
    http-response set-header Referrer-Policy "strict-origin-when-cross-origin"

Sie können sie auch nur dann hinzufügen, wenn die Anwendung sie nicht bereits hinzugefügt hat:

.. code-block:: bash

    http-after-response add-header X-Frame-Options "SAMEORIGIN" if !{ res.hdr(X-Frame-Options) -m found }
    http-after-response add-header X-Content-Type-Options "nosniff" if !{ res.hdr(X-Content-Type-Options) -m found }
    http-after-response add-header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload" if !{ res.hdr(Strict-Transport-Security) -m found }
    http-after-response add-header Referrer-Policy "strict-origin-when-cross-origin" if !{ res.hdr(Referrer-Policy) -m found }

Oder überschreiben/entfernen Sie einige:

.. code-block:: bash

    http-response set-header Server OXL-LB

    http-response del-header X-Powered-By

----

List Files
==========

Sie können dateibasierte Listen laden und sie in ACLs verwenden.

Dies ist besonders nützlich, wenn Sie IP-Listen verwenden oder Requests anhand anderer Daten zuordnen wollen.

.. code-block:: bash

    # /etc/haproxy/lst/tor-exit-node.lst

    http-request deny status 418 if { src -f /etc/haproxy/lst/tor-exit-node.lst }

Beispiel IP-Listen:

* `Tor Exit Nodes <https://check.torproject.org/torbulkexitlist>`_
* `Spamhaus DROP <https://www.spamhaus.org/drop/drop.txt>`_
* `Spamhaus EDROP <https://www.spamhaus.org/drop/edrop.txt>`_

----

Map Files
=========

Sie können eine Datei mit Schlüssel-Wert-Paaren verwenden, um Daten dynamisch abzugleichen. Schlüssel und Werte werden durch ein Leerzeichen getrennt.

Dies kann besonders nützlich sein, wenn Sie Ihre HAProxy-Konfiguration so weit abstrahieren können, dass Sie nur diese Dateien aktualisieren müssen, um Dienste hinzuzufügen oder zu entfernen.

Beispiel Map-Datei:

.. code-block:: bash

    # JA4 TLS fingerprint matching: https://github.com/O-X-L/haproxy-ja4
    t13d1517h2_8daaf6152771_b0da82dd1658 Mozilla/5.0_(Windows_NT_10.0;_Win64;_x64)_AppleWebKit/537.36_(KHTML,_like_Gecko)_Chrome/125.0.0.0_Safari/537.36
    t13d1516h2_8daaf6152771_02713d6af862 Chromium_Browser
    ...

Wie man diese benutzt:

.. code-block:: bash

    http-request set-var(txn.fingerprint_app) var(txn.fingerprint_ja4),map(/etc/haproxy/map/fingerprint_ja4_app.map)

    # log it
    http-request capture var(txn.fingerprint_app) len 200

Siehe: `HAProxy Maps <https://www.haproxy.com/blog/introduction-to-haproxy-maps>`_

----

Security Filter
***************

Dumme Bots flaggen
==================

Sie können einige der 'dummen' Bots mit Hilfe dieser Regeln leicht kennzeichnen:

.. code-block:: bash

    # flag bots by common user-agent substrings
    http-request set-var(txn.bot) int(1) if !{ var(txn.bot) -m found } !{ req.fhdr(User-Agent) -m found }
    http-request set-var(txn.bot) int(1) if !{ var(txn.bot) -m found } { req.fhdr(User-Agent) -m sub -i -f /etc/haproxy/lst/bot-ua-sub.lst }
    http-request set-var(txn.bot) int(1) if !{ var(txn.bot) -m found } { req.fhdr(User-Agent) -m sub -i -f /etc/haproxy/lst/crawler-ua-sub.lst }

    # flag well-known script-bots
    http-request set-var(txn.bot) int(1) if !{ var(txn.bot) -m found } { req.fhdr(User-Agent) -m sub -i -f /etc/haproxy/lst/badbot-ua-sub.lst }

    # fallback
    http-request set-var(txn.bot) int(0) if !{ var(txn.bot) -m found }

    # log it
    http-request capture var(txn.bot) len 1

Dieses Kennzeichen kann verwendet werden, um strengere Regeln für diese IPs einzuführen:

.. code-block:: bash

    # see rate-limits section for more context
    http-request deny deny_status 429 if !{ var(txn.bot) -m int 0 } { sc_http_req_rate(1,be_limiter_http_short) gt 20 }
    http-request deny deny_status 429 if { var(txn.bot) -m int 0 } { sc_http_req_rate(1,be_limiter_http_short) gt 50 }

Beispiel Listen:

* `badbot-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_badbot-ua-sub.lst>`_
* `bot-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_bot-ua-sub.lst>`_
* `crawler-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_crawler-ua-sub.lst>`_

----

Script-Kiddies blockieren
=========================

Filter wie diese müssen für Ihre Umgebung und Anwendung(en) angepasst werden.

Sie können Ihre Logs grundsätzlich beobachten und bei Bedarf die Listen erweitern.

.. code-block:: bash

    # paths you want to exclude from all checks
    acl script_kiddy_excluded path -m sub -i -f /etc/haproxy/lst/waf-script-kiddy-excludes.lst

    # block if match in files
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m beg -i -f /etc/haproxy/lst/script-kiddy-path-beg.lst }
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m end -i -f /etc/haproxy/lst/script-kiddy-path-end.lst }
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m sub -i -f /etc/haproxy/lst/script-kiddy-path-sub.lst }

Beispiel Listen:

* `script-kiddy-path-beg.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-beg.lst>`_
* `script-kiddy-path-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-sub.lst>`_
* `script-kiddy-path-end.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-end.lst>`_

----

Rate Limits / Anti DDOS
=======================

Siehe: :ref:`proxy_reverse_haproxy_rate`

----

GeoIP Filtering
===============

Siehe: :ref:`proxy_reverse_haproxy_geoip`

----

TLS Client Fingerprinting
=========================

Siehe: :ref:`proxy_reverse_haproxy_tls_fp`


----

Service
#######

Sie möchten vielleicht Konfigurationsfehler bei Reloads protokollieren.

Standardmäßig werden Reloads im Modus :code:`quiet` ausgeführt und versteckt.

.. code-block:: bash

    # /etc/systemd/system/haproxy.service.d/override.conf

    [Service]
    ExecReload=
    ExecReload=/usr/sbin/haproxy -Ws -f $CONFIG -c -q $EXTRAOPTS
    ExecReload=/bin/kill -USR2 $MAINPID

----

Stats
#####

Sie können eine einfache Statusseite für HAProxy wie folgt aktivieren:

.. code-block:: bash

    frontend stats
        mode http
        bind *:10000
        stats enable
        stats uri /stats
        stats refresh 10s
        stats realm Authorized\ Personal\ Only

        redirect code 301 location /stats if { path -i / }

        stats auth <STATS-USER>:<STATS-PWD>

        # this enables you to perform some actions
        stats admin if LOCALHOST

        # you may want to disable logging if your monitoring will check this endpoint; enable it if 'admin' is enabled..
        no log


Danach können Sie die Webseite aufrufen: :code:`http://<HAPROXY-IP>:10000/stats` und melden Sie sich mit den angegebenen Anmeldedaten an.

Sie können auch TLS wie bei jedem anderen Frontend aktivieren.

----

Logging
#######

Sie können entweder die Log-Formate für Ihre Frontends ändern oder Daten mit :code:`capture` erfassen.

Siehe: `HAProxy Logging <https://www.haproxy.com/blog/introduction-to-haproxy-logging>`_

Formate
=======

.. code-block:: bash

    # HTTP mode
    ## default
    [%ci]:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r

    ## with prefix for easier log-filtering
    HTTP: [%ci]:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r

    # TCP mode
    ## default
    [%ci]:%cp [%t] %ft %b/%s %Tw/%Tc/%Tt %B %ts %ac/%fc/%bc/%sc/%rc %sq/%bq

    ## with prefix for easier log-filtering
    TCP: [%ci]:%cp [%t] %ft %b/%s %Tw/%Tc/%Tt %B %ts %ac/%fc/%bc/%sc/%rc %sq/%bq

Siehe: `HAProxy Logging Formats <https://www.haproxy.com/blog/introduction-to-haproxy-logging#haproxy-log-format>`_

----

Capture
=======

Mit :code:`capture` können Sie dynamisch Daten abfangen. Dies kann in einigen Fällen nützlich sein.

Beispiel für die Aufzeichnung von GeoIP-Land und ASN:

.. code-block:: bash

    140.82.115.0:33494 [04/May/2024:18:58:57.790] fe_web~ be_test2/srv2 0/0/26/26/52 200 1778 - - ---- 2/2/0/0/0 0/0 {US|36459|github-camo (4b76e509)} "GET /infra_haproxy.pylint.svg HTTP/1.1"

Sie können viele Arten von Daten erfassen.

Erfassungen können einfach wie folgt hinzugefügt werden:

.. code-block:: bash

    http-request capture <WHAT-TO-LOG> len <MAX-LENGTH>

    # log a header
    http-request capture req.fhdr(User-Agent) len 200
    http-request capture req.hdr(Host) len 50
    http-request capture req.hdr(Referer) len 200

    # log a variable
    http-request capture var(txn.geoip_asn) len 10

Bei den Antworten ist es ein wenig anders:

.. code-block:: bash

    declare capture response len <MAX-LENGTH>
    http-response capture <WHAT-TO-LOG> id <POSITION>

    declare capture response len 20
    http-response capture res.hdr(Content-Type) id 1

Siehe: `HAProxy Logging via Capture <https://www.haproxy.com/blog/introduction-to-haproxy-logging#other-fields>`_

----


Zertifikate
###########

HAProxy erwartet, dass sich die öffentlichen und privaten Schlüssel in derselben Datei befinden:

.. code-block:: bash

    cat "${FULLCHAINFILE}" "${KEYFILE}" > "${HAPROXY_CERT_DIR}/${CERTNAME}.pem"

Wenn Sie viele Zertifikate haben, können Sie ein Zertifikatsverzeichnis zur Verfügung stellen - das richtige Zertifikat, welches die Zieldomäne in dessen Subject-Alt-Name enthält, wird automatisch ausgewählt:

.. code-block:: bash

    bind [::]:443 v4v6 ssl crt /etc/ssl/haproxy_acme/certs alpn h2,http/1.1

HTTP-Anfragen können auf HTTPS umgeleitet werden:

.. code-block:: bash

    http-request redirect scheme https code 301 if !{ ssl_fc } !{ path_beg -i /.well-known/acme-challenge/ }

ACME HTTP-Challenges benötigen einen separaten Webserver wie :code:`nginx-light`, um ihre Challenge-Tokens zu liefern. Beispiel Backend-Konfiguration:

.. code-block:: bash

    frontend fe_web
        ...

        use_backend be_haproxy_acme if { path_beg -i /.well-known/acme-challenge/ }

        ...

    backend be_haproxy_acme
        server haproxy_acme 127.0.0.1:${ACME_CHALLENGE_PORT} check

Grundlegende ACME nginx-Konfiguration:

.. code-block:: bash

    rm /etc/nginx/sites-enabled/default

    mkdir -p ${ACME_CHALLENGE_DIR}

    nano /etc/nginx/sites-enabled/haproxy_acme
    > server {
    >     listen 127.0.0.1:${ACME_CHALLENGE_PORT};
    >
    >     autoindex off;
    >     server_tokens off;
    >
    >     location ^~ /.well-known/acme-challenge {
    >         alias ${ACME_CHALLENGE_DIR};
    >     }
    >     location / {
    >         deny all;
    >     }
    > }

    systemctl enable nginx.service
    systemctl restart nginx.service


LetsEncrypt Script: `dehydrated <https://github.com/dehydrated-io/dehydrated>`_

Ansible Beispiel: `ansibleguy/infra_haproxy - ACME <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleAcme.md>`_ | `dehydrated hooks <https://github.com/ansibleguy/infra_haproxy/blob/latest/templates/usr/local/bin/dehydrated_hook.sh.j2>`_

----

.. _proxy_reverse_haproxy_rate:

Rate Limits
###########

Die Konfiguration von Rate-Limits kann ein wenig verwirrend sein.

Rate-Limits bestehen im Wesentlichen aus zwei Komponenten: **tables** und **trackers**

----

Trackers
********

Diese verfolgen Ihre Client-Verbindungen.

Bei der Community-Edition stehen Ihnen standardmäßig 3 davon zur Verfügung. In der Enterprise-Edition stehen Ihnen 12 zur Verfügung.

Sie können sie mit der Einstellung `tune.stick-counters <https://docs.haproxy.org/2.8/configuration.html#3.2-tune.stick-counters>`_ erhöhen.

Sie können Clients wie folgt verfolgen:

.. code-block:: bash

    # track each tcp connection by source-IP and add it into a table
    tcp-request connection track-sc0 src table be_limiter_tcp

    # track each http connection by source-IP and add it into a table
    http-request track-sc1 src table be_limiter_http

    # track each http connection by your custom fingerprint
    http-request set-var(txn.fingerprint) ...
    http-request track-sc1 var(txn.fingerprint) table be_limiter_http

    # track services separately (could be placed in backend section)
    http-request track-sc1 src table be_limiter_app1 if { req.hdr(host) -m str -i www.app1.com }
    http-request track-sc1 src table be_limiter_app2 if { req.hdr(host) -m str -i www.app2.com }

    # track by user-agent
    http-request track-sc1 req.fhdr(User-Agent) be_limiter_ua

Sie können einen einzigen :code:`track-scN` verwenden, um einen Client in mehreren Tabellen zu verfolgen.

----

Tables
******

In jeder Tabelle können mehrere Stats erfasst werden.

Die verfügbaren sind:

* :code:`gpc` (*general purpose counter*)
* :code:`gpc_rate`
* :code:`bytes_in_rate`
* :code:`bytes_out_rate`
* :code:`conn_cnt`
* :code:`conn_cur`
* :code:`conn_rate`
* :code:`http_err_cnt` (*http status codes 4xx*)
* :code:`http_err_rate`
* :code:`http_fail_cnt` (*http status codes 5xx*)
* :code:`http_fail_rate`
* :code:`http_req_cnt` (*total count of requests since first contact or table flush*)
* :code:`http_req_rate` (*count of requests in a given timeframe*)
* :code:`sess_cnt`
* :code:`sess_rate`

Für Details siehe: `HAProxy configuration manual <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#7-sc0_bytes_in_rate>`_

----

Beispiele
*********

Damit Sie den aktuellen Stand der konfigurierten Rates analysieren können, empfehlen wir Ihnen, immer **named stick-tables** zu verwenden.

.. code-block:: bash

    # stick-table type <data-type-to-track> size <max-entries> expire <entry-timeout-without-contact> store <what-to-track>
    # NOTE: the type 'ipv6' works in dual-stack for both ipv4 and ipv6

    # save requests in the last hour
    backend be_limiter_1h
        stick-table type ipv6 size 10k expire 2h store http_req_rate(3600s)

    # save errors
    backend be_limiter_err
        stick-table type ipv6 size 10k expire 2h store http_err_cnt,http_fail_cnt

    # save requests since last table-flush or entry-timeout
    backend be_limiter_req
        stick-table type ipv6 size 10k expire 2h store http_req_cnt

    # same as above, but track client by 32-char fingerprint; will use more memory
    backend be_limiter_req_fp
        stick-table type string len 32 size 10k expire 2h store http_req_cnt

----

Named stick-table
=================

Diese werden als Backends hinzugefügt:

.. code-block:: bash

    global
        ...
        # enable the admin socket
        stats socket /run/haproxy/admin.sock mode 660 level admin

    backend be_limiter_xyz  # <= name
        stick-table type ipv6 size 10k expire 24h store http_req_cnt

Sie können den aktuellen Status über den Admin-Socket auslesen:

.. code-block:: bash

    apt install socat

    # show stats
    echo "show table be_limiter_xyz" | socat stdio /run/haproxy/admin.sock

    # clear stats
    echo "clear table be_limiter_xyz" | socat stdio /run/haproxy/admin.sock

Für mehr Kommandos siehe: `HAProxy runtime API <https://www.haproxy.com/documentation/haproxy-runtime-api/installation/>`_

----

Basic
=====

Wir werden:

* Log-Level auf Warnung setzen, wenn verweigert

* Verweigern, wenn das 10-Minuten-Limit für Anfragen überschritten wird

* Behält Request-Count, Request-Error & -Fail-Zähler für Diagnosezwecke


.. code-block:: bash

    backend be_limiter_app1
        stick-table type ipv6 size 10k expire 1h store http_req_rate(600s),http_req_cnt,http_err_cnt,http_fail_cnt

    backend be_app1
        ...

        http-request track-sc0 src table be_limiter_app1
        acl over_limit_app1 sc0_http_req_rate(be_limiter_app1) gt 50
        http-request set-log-level warning if over_limit_app1
        http-request deny deny_status 429 if over_limit_app1

----

Mehrere
=======

Wir werden:

* Log-Level auf Warnung setzen, wenn verweigert

* Request-count, Request-error & -fail counter für Diagnosezwecke behalten

* TCP-Verbindungen verfolgen

  * Verwerfen, wenn die TCP-Verbindungsrate zu hoch ist

* HTTP-Verbindungen in zwei Tabellen verfolgen

  * Verweigern, wenn 10min Anfrage-Limit überschritten wird

  * Verweigern, wenn das Limit für 1h-Anfragen überschritten wird

  * Verweigern, wenn API und tägliche Anfragen ein Limit überschreiten

.. code-block:: bash

    backend be_limiter_tcp
        stick-table type ip size 10k expire 5m store conn_cur,conn_rate(10s)

    backend be_limiter_app2
        stick-table type ipv6 size 10k expire 30m store http_req_rate(600s),http_req_cnt,http_err_cnt,http_fail_cnt

    backend be_limiter_app2_1h
        stick-table type ipv6 size 10k expire 2h store http_req_rate(3600s),http_req_cnt,http_err_cnt,http_fail_cnt

    backend be_limiter_app2_api
        stick-table type ipv6 size 10k expire 24h store http_req_cnt,http_err_cnt,http_fail_cnt

    # flush table entries daily using cronjob for daily limits to work:
    #   'echo "clear table be_limiter_app2_api" | socat stdio /run/haproxy/admin.sock'

    backend be_app2
        ...

        # tcp limit - may make sense to move it to the frontend section
        tcp-request connection track-sc0 src table be_limiter_tcp
        acl dos1 src_conn_cur(be_limiter_tcp) ge 20
        acl dos2 src_conn_rate(be_limiter_tcp) ge 20
        http-request set-log-level warning if dos1 || dos2
        tcp-request connection reject if dos1 || dos2

        # 10 min limit
        http-request track-sc1 src table be_limiter_app2
        acl over_limit_app2_10m sc1_http_req_rate(be_limiter_app2) gt 50
        http-request set-log-level warning if over_limit_app2_10m
        http-request deny deny_status 429 if over_limit_app2_10m

        # 1h limit
        http-request track-sc1 src table be_limiter_app2_1h
        acl over_limit_app2_1h sc1_http_req_rate(be_limiter_app2_1h) gt 5000
        http-request set-log-level warning if over_limit_app2_1h
        http-request deny deny_status 429 if over_limit_app2_1h

        # daily limit for api
        acl is_api path_beg -i /api/
        http-request track-sc1 src table be_limiter_app2_api if is_api
        acl over_limit_app2_api_1d sc1_http_req_cnt(be_limiter_app2_api) gt 1000
        http-request set-log-level warning if is_api over_limit_app2_api_1d
        http-request deny deny_status 429 if is_api over_limit_app2_api_1d

----

Counter pro Client
==================

Sie können 'general purpose counters' für spezielle Verwendungszwecke einsetzen.

Wir werden:

* Log-Level auf Warnung setzen, wenn verweigert

* Hochzählen, wenn wir eine Script-Kiddy-Anfrage finden

* Verweigern, wenn die Anzahl höher als 5 ist

.. code-block:: bash

    backend be_limiter_app3
        stick-table type ip size 10k expire 5m store gpc0

    backend be_app3
        ...
        http-request track-sc1 src table be_limiter_app3
        http-request sc-inc-gpc0(0) if { path_beg -i /cgi-bin/ /manager/ /php /program/ /pwd/ /shaAdmin/ /typo3/ /admin/ /dbadmin/ /db/ /solr/ /weaver/ /joomla/ /App/ /webdav/ /. /xmlrpc /% /securityRealm/ /magmi/ /menu/ /etc/ /HNAP1 }
        http-request sc-inc-gpc0(0) if { path_end -i .php .asp .aspx .esp .lua .rsp .ashx .dll .bin .cgi .cs .application .exe .env .git/config .git/HEAD .git/index .DS_Store .aws/config .config .settings .zip .tar .tgz .gz .bz2 .rar .7z .sql .sqlite3 .bak }
        acl over_limit_kiddy src,table_gpc(0,be_limiter_app3) gt 5
        http-request set-log-level warning if over_limit_kiddy
        http-request deny deny_status 429 if over_limit_kiddy


----

Preserve on Reload
==================

Wie in `diesem Blogbeitrag <https://www.haproxy.com/blog/preserve-stick-table-data-when-reloading-haproxy>`_ beschrieben, können wir einen Dummy-Peer konfigurieren, damit HAProxy die Sticky-Table-Einträge beim erneuten Laden des Dienstes beibehält.

.. code-block:: bash

    peers preserve_on_reload
      peer <YOUR-SERVER-HOSTNAME> 127.0.0.1:10000

    backend be_limiter_xyz
        stick-table type ipv6 size 10k expire 24h store http_req_cnt peers preserve_on_reload

----

.. _proxy_reverse_haproxy_geoip:

GeoIP Support
#############

Enterprise Edition
==================

Die Enterprise-Ausgabe verfügt über ein `integriertes Maxmind-Modul <https://www.haproxy.com/documentation/hapee/latest/load-balancing/geolocation/maxmind/>`_.

Community Edition
=================

Sie können unser `LUA-Modul verwenden <https://github.com/O-X-L/haproxy-geoip>`_.

Ansible Beispiel: `ansibleguy/infra_haproxy - GeoIP <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleGeoIP.md>`_ | `ansibleguy/infra_haproxy - GeoIP TCP Mode <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleTCP.md>`_

Setup
-----

* Fügen Sie das LUA-Skript :code:`geoip_lookup.lua` zu Ihrem System hinzu
* Installieren und richten Sie das `GeoIP Lookup-Backend <https://github.com/O-X-L/geoip-lookup-service>`_ Ihrer Wahl ein.

Config
------

* Laden des LUA-Moduls durch Hinzufügen von lua-load :code:`/etc/haproxy/lua/geoip_lookup.lua` im globalen Abschnitt
* Lassen Sie das LUA-Skript bei Requests ausführen:

  * Im HTTP Modus

    .. code-block:: bash

        # country
        http-request lua.lookup_geoip_country
        # asn
        http-request lua.lookup_geoip_asn

  * Im TCP Modus

    .. code-block:: bash

        # country
        tcp-request content lua.lookup_geoip_country
        # asn
        tcp-request content lua.lookup_geoip_asn

* Die Daten loggen:

  * Im HTTP Modus

    .. code-block:: bash

        http-request capture var(txn.geoip_asn) len 10
        http-request capture var(txn.geoip_country) len 2

  * Im TCP Modus

    .. code-block:: bash

        tcp-request content capture var(txn.geoip_asn) len 10
        tcp-request content capture var(txn.geoip_country) len 2

----

.. _proxy_reverse_haproxy_tls_fp:

TLS Client Fingerprinting Support
#################################

JA3N
****

JA3 war nativ mit den in HAProxy eingebauten Konvertern möglich. Aber JA3 brach vor einiger Zeit zusammen, als die Browser begannen, die Sortierung ihrer Erweiterungen zu randomisieren.

JA3N sortiert die Erweiterungen, bevor es den gleichen Fingerabdruck erstellt.

Sie können diese Art von TLS-Client-Fingerprint mit Hilfe unseres LUA-Plugins erstellen: `O-X-L/haproxy-ja3n <https://github.com/O-X-L/haproxy-ja3n>`_

**Über JA3**:

* `Salesforce Repository <https://github.com/salesforce/ja3>`_
* `HAProxy Enterprise JA3 Fingerprint <https://customer-docs.haproxy.com/bot-management/client-fingerprinting/tls-fingerprint/>`_
* `Why JA3 broke => JA3N <https://github.com/salesforce/ja3/issues/88>`_

Setup
=====

* Fügen Sie das LUA-Skript :code:`ja3n.lua` zu Ihrem System hinzu

Config
======

* Aktivieren Sie die SSL/TLS-Erfassung mit der globalen Einstellung `tune.ssl.capture-buffer-size 96 <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#tune.ssl.capture-buffer-size>`_
* Laden Sie das LUA-Modul durch Hinzufügen von `lua-load /etc/haproxy/lua/ja3n.lua` in die globalen Einstellungen
* Ausführen des LUA-Skripts bei HTTP-Requests: `http-request lua.fingerprint_ja3n`
* Logge den Fingerprint: `http-request capture var(txn.fingerprint_ja3n) len 32`

----

JA4
***

Sie können einen JA4 TLS-Client-Fingerprint mit Hilfe unseres LUA-Plugins erstellen: `O-X-L/haproxy-ja4 <https://github.com/O-X-L/haproxy-ja4>`_

**Über JA4**:

* `JA4 TLS details <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md>`_
* `Cloudflare Blog <https://blog.cloudflare.com/ja4-signals>`_
* `FoxIO Blog <https://blog.foxio.io/ja4%2B-network-fingerprinting>`_
* `FoxIO JA4 Database <https://ja4db.com/>`_
* `JA4 Suite <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/README.md>`_

Setup
=====

* Fügen Sie das LUA-Skript :code:`ja4.lua` zu Ihrem System hinzu

Config
======

* Aktivieren Sie die SSL/TLS-Erfassung mit der globalen Einstellung `tune.ssl.capture-buffer-size 128 <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#tune.ssl.capture-buffer-size>`_
* Laden Sie das LUA-Modul durch Hinzufügen von `lua-load /etc/haproxy/lua/ja4.lua` in die globalen Einstellungen
* Ausführen des LUA-Skripts bei HTTP-Requests: `http-request lua.fingerprint_ja4`
* Logge den Fingerprint: `http-request capture var(txn.fingerprint_ja3n) len 36`

JA4 Datenbank
=============

You can use `the DB to MAP script <https://github.com/O-X-L/haproxy-ja4/blob/latest/ja4db-to-map.py`_ to create a HAProxy Mapfile from the `FoxIO JA4-Database <https://ja4db.com/>`_:

Sie können das `DB=>Map Skript <https://github.com/O-X-L/haproxy-ja4/blob/latest/ja4db-to-map.py`_ verwenden, um eine HAProxy-Mapdatei aus der `FoxIO JA4-Datenbank <https://ja4db.com/>`_ zu erstellen:

.. code-block:: bash

    # download the DB in JSON format: https://ja4db.com/api/download/
    # place it in the same directory as the script

    # build the map-file
    python3 ja4db-to-map.py

    # examples:
    > t13d1517h2_8daaf6152771_b0da82dd1658 Mozilla/5.0_(Windows_NT_10.0;_Win64;_x64)_AppleWebKit/537.36_(KHTML,_like_Gecko)_Chrome/125.0.0.0_Safari/537.36
    > t13d1516h2_8daaf6152771_02713d6af862 Chromium_Browser

So können Sie die Werte suchen: :code:`http-request set-var(txn.fingerprint_app) var(txn.fingerprint_ja4),map(/etc/haproxy/map/fingerprint_ja4_app.map)`

Und diese loggen: :code:`http-request capture var(txn.fingerprint_app) len 200`

.. include:: ../_include/user_rath.rst
