.. _proxy_reverse_haproxy:

.. include:: ../_include/head.rst


***********************
Reverse Proxy - HAProxy
***********************

----

Intro
#####

If you are configuring HAProxy - have the `configuration manual <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/>`_ ready/open! You will need it!

Ansible Role: `ansibleguy/infra_haproxy <https://github.com/ansibleguy/infra_haproxy>`_

----

Configuration
#############

Whenever you change the config - you might want to check it for errors:

.. code-block:: bash

    haproxy -c -f /etc/haproxy/haproxy.cfg

    # with multiple config files:
    haproxy -c -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d/


Afterwards you need to reload it:

.. code-block:: bash

    systemctl reload haproxy.service

Basics
******

ACLs
====

You can define ACLs to create some conditional matching:

.. code-block:: bash

    acl <NAME> <CONDITION>

    acl net_private src 192.168.0.0/16 172.16.0.0/12 10.0.0.0/8 127.0.0.0/8 ::1

These can also be used in-line as anonymous ACL - this makes sense if you only need to use it once:

.. code-block:: bash

    <ACTION> if { <CONDITION> }

Data can be matched in different ways:

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

You can combine ACLs with AND/OR/NOT conditions:

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

Variables
=========

Variables can be used for more dynamic use-cases.

Example:

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

Utilize the :code:`use_backend` action to choose the route the traffic should take:

.. code-block:: bash

    frontend fe_web:
        ...
        acl domains_adm req.hdr(host) -m str -i admin.example.oxl.at
        acl src_privileged src 192.168.0.48
        acl domains_test req.hdr(host) -m str -i test.oxl.at

        use_backend be_admin if domains_adm src_privileged
        use_backend be_test if domains_test

        use_backend be_fallback

    backend be_test
        mode http

        # plain http backends; but use sticky-session via cookie
        server test-1 192.168.10.11:80 check cookie test1
        server test-2 192.168.10.12:80 check cookie test2

    backend be_admin
        mode http

        # use ssl from haproxy to backends
        ## verify using default CA trust-store
        server srv-1 192.168.10.11:443 check ssl verify required

        ## verify using specific CA
        server srv-2 192.168.10.12:443 check ssl verify required ca-file /etc/ssl/certs/internal-ca.crt

        ## skip verification (not recommended)
        server srv-3 192.168.10.13:443 check ssl verify none

    backend be_fallback
        mode http
        http-request redirect code 302 location https://www.oxl.at

See: `HAProxy Backends <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/core-concepts/backends/>`_

----

Basic Auth
==========

You can either use plaintext or hashed (recommended) passwords.

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

See: `HAProxy Basic-Auth <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/authentication/basic-authentication/>`_

----

HTTP Methods
============

You might want to deny connections over unused HTTP methods:

.. code-block:: bash

    http-request deny status 405 default-errorfiles if { method TRACE CONNECT }

----

HTTP Headers
============

You may want to add and enforce security-related headers:

.. code-block:: bash

    # Note: use 'set' to add a new header or overwrite it if it already exists; 'add' might duplicate it
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload"
    http-response set-header X-Frame-Options "SAMEORIGIN"
    http-response set-header X-Content-Type-Options "nosniff"
    http-response set-header X-Permitted-Cross-Domain-Policies "none"
    http-response set-header X-XSS-Protection "1; mode=block"
    http-response set-header Referrer-Policy "strict-origin-when-cross-origin"

You can also only add them in case the proxied application has not already added them:

.. code-block:: bash

    http-after-response add-header X-Frame-Options "SAMEORIGIN" if !{ res.hdr(X-Frame-Options) -m found }
    http-after-response add-header X-Content-Type-Options "nosniff" if !{ res.hdr(X-Content-Type-Options) -m found }
    http-after-response add-header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload" if !{ res.hdr(Strict-Transport-Security) -m found }
    http-after-response add-header Referrer-Policy "strict-origin-when-cross-origin" if !{ res.hdr(Referrer-Policy) -m found }

Or overwrite/remove some from the responses:

.. code-block:: bash

    http-response set-header Server OXL-LB

    http-response del-header X-Powered-By

----

List Files
==========

You can load file-based lists and use them in ACLs.

This is specially useful if you need/want to use IP-Lists or match requests by some other data.

.. code-block:: bash

    # /etc/haproxy/lst/tor-exit-node.lst

    http-request deny status 418 if { src -f /etc/haproxy/lst/tor-exit-node.lst }

Example IP-Lists:

* `Tor Exit Nodes <https://check.torproject.org/torbulkexitlist>`_
* `Spamhaus DROP <https://www.spamhaus.org/drop/drop.txt>`_
* `Spamhaus EDROP <https://www.spamhaus.org/drop/edrop.txt>`_

----

Map Files
=========

You can use a file of key-value pairs to dynamically match/lookup data. Keys and values are separated by a whitespace.

This can be especially useful if you are able to abstract your HAProxy config to a point where you only need to update those files to add or remove services.

Example Map file:

.. code-block:: bash

    # JA4 TLS fingerprint matching: https://github.com/O-X-L/haproxy-ja4
    t13d1517h2_8daaf6152771_b0da82dd1658 Mozilla/5.0_(Windows_NT_10.0;_Win64;_x64)_AppleWebKit/537.36_(KHTML,_like_Gecko)_Chrome/125.0.0.0_Safari/537.36
    t13d1516h2_8daaf6152771_02713d6af862 Chromium_Browser
    ...

How to use it:

.. code-block:: bash

    http-request set-var(txn.fingerprint_app) var(txn.fingerprint_ja4),map(/etc/haproxy/map/fingerprint_ja4_app.map)

    # log it
    http-request capture var(txn.fingerprint_app) len 200

See: `HAProxy Maps <https://www.haproxy.com/blog/introduction-to-haproxy-maps>`_

----

Security Filters
****************

Flag Dumb-Bots
==============

You can easily flag some of the 'dumb' bots using rules like these:

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

This flag can be used to put stricter rules for those clients in-place:

.. code-block:: bash

    # see rate-limits section for more context
    http-request deny deny_status 429 if !{ var(txn.bot) -m int 0 } { sc_http_req_rate(1,be_limiter_http_short) gt 20 }
    http-request deny deny_status 429 if { var(txn.bot) -m int 0 } { sc_http_req_rate(1,be_limiter_http_short) gt 50 }

Example List-Files:

* `badbot-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_badbot-ua-sub.lst>`_
* `bot-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_bot-ua-sub.lst>`_
* `crawler-ua-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_crawler-ua-sub.lst>`_

----

Deny Script-Kiddies
===================

Filters like these will have to be modified for your environment and application(s).

You can basically observe your logs and add blocks as needed.

.. code-block:: bash

    # paths you want to exclude from all checks
    acl script_kiddy_excluded path -m sub -i -f /etc/haproxy/lst/waf-script-kiddy-excludes.lst

    # block if match in files
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m beg -i -f /etc/haproxy/lst/script-kiddy-path-beg.lst }
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m end -i -f /etc/haproxy/lst/script-kiddy-path-end.lst }
    http-request deny status 418 default-errorfiles if !script_kiddy_excluded { path -m sub -i -f /etc/haproxy/lst/script-kiddy-path-sub.lst }

Example List-Files:

* `script-kiddy-path-beg.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-beg.lst>`_
* `script-kiddy-path-sub.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-sub.lst>`_
* `script-kiddy-path-end.lst <https://docs.o-x-l.com/_static/raw/proxy_reverse_haproxy_script-kiddy-path-end.lst>`_

----

Rate Limits / Anti DDOS
=======================

See: :ref:`proxy_reverse_haproxy_rate`

----

GeoIP Filtering
===============

See: :ref:`proxy_reverse_haproxy_geoip`

----

TLS Client Fingerprinting
=========================

See: :ref:`proxy_reverse_haproxy_tls_fp`


----

Service
#######

You might want to log config-errors on reloads.

By default it executes reloads in :code:`quiet` mode and hides them.

.. code-block:: bash

    # /etc/systemd/system/haproxy.service.d/override.conf

    [Service]
    ExecReload=
    ExecReload=/usr/sbin/haproxy -Ws -f $CONFIG -c -q $EXTRAOPTS
    ExecReload=/bin/kill -USR2 $MAINPID

----

Stats
#####

You can enable a basic status-page for HAProxy like this:

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


Afterwards you can access the web-page: :code:`http://<HAPROXY-IP>:10000/stats` and login with the credentials specified.

You can also enable TLS like on every other frontend.

----

Logging
#######

You can either modify the default logging-formats for your frontends, or :code:`capture` data.

See: `HAProxy Logging <https://www.haproxy.com/blog/introduction-to-haproxy-logging>`_

Formats
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

See: `HAProxy Logging Formats <https://www.haproxy.com/blog/introduction-to-haproxy-logging#haproxy-log-format>`_

----

JSON
====

.. code-block:: bash

    global
        ...
        setenv HTTPLOG_JSON "%{+json}o %(client)ci %(client_port)cp %(request_date)tr %(frontend)ft %(backend)b %(backend_server)s %(time_request)TR %(time_wait)Tw %(time_connect)Tc %(time_response)Tr/%(time_active)Ta %(status)ST %(bytes_read)B %(termination_state)tsc %(actconn)ac %(feconn)fc %(beconn)bc %(srv_conn)sc %(retries)rc %(srv_queue)sq %(backend_queue)bq %(capture_request)hr %(capture_response)hs %(http_request){+Q}r"
        ...

    defaults
        log-format "${HTTPLOG_JSON} %(unique_id)[unique-id]"
        unique-id-format %{+X}o\ %Ts-%fi%fp%pid-%rt

Siehe: `HAProxy JSON & CBOR Log-Formats <https://www.haproxy.com/blog/encoding-haproxy-logs-in-machine-readable-json-or-cbor>`_

----

Capture
=======

With :code:`capture` you can dynamically catch data. This might be useful in some cases.

Example of logging GeoIP-country, GeoIP-ASN and User-Agent:

.. code-block:: bash

    140.82.115.0:33494 [04/May/2024:18:58:57.790] fe_web~ be_test2/srv2 0/0/26/26/52 200 1778 - - ---- 2/2/0/0/0 0/0 {US|36459|github-camo (4b76e509)} "GET /infra_haproxy.pylint.svg HTTP/1.1"

You can capture many kinds of data.

Captures can simply be added like this:

.. code-block:: bash

    http-request capture <WHAT-TO-LOG> len <MAX-LENGTH>

    # log a header
    http-request capture req.fhdr(User-Agent) len 200
    http-request capture req.hdr(Host) len 50
    http-request capture req.hdr(Referer) len 200

    # log a variable
    http-request capture var(txn.geoip_asn) len 10

For responses it is a little different:

.. code-block:: bash

    declare capture response len <MAX-LENGTH>
    http-response capture <WHAT-TO-LOG> id <POSITION>

    declare capture response len 20
    http-response capture res.hdr(Content-Type) id 1

See: `HAProxy Logging via Capture <https://www.haproxy.com/blog/introduction-to-haproxy-logging#other-fields>`_

----


Certificates
############

HAProxy will expect the public- and private-keys to be in the same file like this:

.. code-block:: bash

    cat "${FULLCHAINFILE}" "${KEYFILE}" > "${HAPROXY_CERT_DIR}/${CERTNAME}.pem"

You can provide HAProxy with a certificate directory if you have many certs - the correct one, that includes the target domain in its Subject-Alt-Name, will be automatically selected:

.. code-block:: bash

    bind [::]:443 v4v6 ssl crt /etc/ssl/haproxy_acme/certs alpn h2,http/1.1

HTTP requests may be redirected to HTTPS:

.. code-block:: bash

    http-request redirect scheme https code 301 if !{ ssl_fc } !{ path_beg -i /.well-known/acme-challenge/ }

ACME HTTP-challenges will need a separate web-server like :code:`nginx-light` to serve its challenge-tokens. Example backend config:

.. code-block:: bash

    frontend fe_web
        ...

        use_backend be_haproxy_acme if { path_beg -i /.well-known/acme-challenge/ }

        ...

    backend be_haproxy_acme
        server haproxy_acme 127.0.0.1:${ACME_CHALLENGE_PORT} check

Basic ACME nginx config:

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

Ansible Example: `ansibleguy/infra_haproxy - ACME <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleAcme.md>`_ | `dehydrated hooks <https://github.com/ansibleguy/infra_haproxy/blob/latest/templates/usr/local/bin/dehydrated_hook.sh.j2>`_

----

.. _proxy_reverse_haproxy_rate:

Rate Limits
###########

Configuring rate limits can be a little confusing.

Rate limits basically consist of two components: **tables** and **trackers**

----

Trackers
********

These track your client connections.

By default you have 3 of them available when using the community edition. In the enterprise edition you have 12.

You can increase them using the `tune.stick-counters <https://docs.haproxy.org/2.8/configuration.html#3.2-tune.stick-counters>`_ setting.


You can track clients like so:

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

You can use a single :code:`track-scN` to track a client in multiple tables.

----

Tables
******

Each table is able to track multiple stats.

Available ones are:

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

See the `HAProxy configuration manual <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#7-sc0_bytes_in_rate>`_ for more details.

----

Examples
********

For allowing you to analyze the current status of the configured rates - I would recommend to always use **named stick-tables**.

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

These are added as backends:

.. code-block:: bash

    global
        ...
        # enable the admin socket
        stats socket /run/haproxy/admin.sock mode 660 level admin

    backend be_limiter_xyz  # <= name
        stick-table type ipv6 size 10k expire 24h store http_req_cnt

You are able to read the current state using the admin socket

.. code-block:: bash

    apt install socat

    # show stats
    echo "show table be_limiter_xyz" | socat stdio /run/haproxy/admin.sock

    # clear stats
    echo "clear table be_limiter_xyz" | socat stdio /run/haproxy/admin.sock

See `HAProxy runtime API <https://www.haproxy.com/documentation/haproxy-runtime-api/installation/>`_ for more commands.

----

Basic
=====

We will:

* Set log-level to warning if denied

* Deny if 10min request limit is exceeded

* Keep request-count, request-error & -fail counter for diagnostics


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

Multiple
========

We will:

* Set log-level to warning if denied

* Keep request-count, request-error & -fail counter for diagnostics

* Track TCP connections

  * Drop if TCP connection-rate is too high

* Track HTTP connections in two tables

  * Deny if 10min request limit is exceeded

  * Deny if 1h requests limit is exceeded

  * Deny if API and daily requests exceed a limit

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

Counter per Client
==================

You can utilize general purpose counters for custom use-cases.

We will:

* Set log-level to warning if denied

* Count up if we find a script-kiddy request

* Deny if count is higher than 5

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

As seen in `this blog post <https://www.haproxy.com/blog/preserve-stick-table-data-when-reloading-haproxy>`_ we can configure a dummy-peer to make HAProxy keep the sticky-table entries when reloading the service.

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

The enterprise edition has a `built-in Maxmind-Module <https://www.haproxy.com/documentation/hapee/latest/load-balancing/geolocation/maxmind/>`_.

Community Edition
=================

You can use our `community-drive Lua module <https://github.com/O-X-L/haproxy-geoip>`_.

Ansible Example: `ansibleguy/infra_haproxy - GeoIP <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleGeoIP.md>`_ | `ansibleguy/infra_haproxy - GeoIP TCP Mode <https://github.com/ansibleguy/infra_haproxy/blob/latest/ExampleTCP.md>`_

Setup
-----

* Add the LUA script to your system
* Install and set up the `GeoIP lookup-backend <https://github.com/O-X-L/geoip-lookup-service>`_ of your choice

Config
------

* Load the LUA module by adding lua-load :code:`/etc/haproxy/lua/geoip_lookup.lua` in the global section
* Execute the LUA script on requests:

  * In HTTP mode

    .. code-block:: bash

        # country
        http-request lua.lookup_geoip_country
        # asn
        http-request lua.lookup_geoip_asn

  * In TCP mode

    .. code-block:: bash

        # country
        tcp-request content lua.lookup_geoip_country
        # asn
        tcp-request content lua.lookup_geoip_asn

* Log the data:

  * In HTTP mode

    .. code-block:: bash

        http-request capture var(txn.geoip_asn) len 10
        http-request capture var(txn.geoip_country) len 2

  * In TCP mode

    .. code-block:: bash

        tcp-request content capture var(txn.geoip_asn) len 10
        tcp-request content capture var(txn.geoip_country) len 2

----

.. _proxy_reverse_haproxy_tls_fp:

TLS Client Fingerprinting Support
#################################

JA3N
****

JA3 was possible natively using HAProxy built-in converters. But JA3 broke some time ago as browsers started to randomize the sorting of their extensions.

JA3N sorts the extensions before creating the same fingerprint.

You can create this kind of TLS-Client-Fingerprint by using our LUA plugin: `O-X-L/haproxy-ja3n <https://github.com/O-X-L/haproxy-ja3n>`_

**About JA3**:

* `Salesforce Repository <https://github.com/salesforce/ja3>`_
* `HAProxy Enterprise JA3 Fingerprint <https://customer-docs.haproxy.com/bot-management/client-fingerprinting/tls-fingerprint/>`_
* `Why JA3 broke => JA3N <https://github.com/salesforce/ja3/issues/88>`_

Setup
=====

* Add the LUA script `ja3n.lua` to your system

Config
======

* Enable SSL/TLS capture with the global setting `tune.ssl.capture-buffer-size 96 <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#tune.ssl.capture-buffer-size>`_
* Load the LUA module by adding `lua-load /etc/haproxy/lua/ja3n.lua` in the `global` section
* Execute the LUA script on HTTP requests: `http-request lua.fingerprint_ja3n`
* Log the fingerprint: `http-request capture var(txn.fingerprint_ja3n) len 32`

----

JA4
***

You can create a JA4 TLS-Client-Fingerprint by using our LUA plugin: `O-X-L/haproxy-ja4 <https://github.com/O-X-L/haproxy-ja4>`_

**About JA4**:

* `JA4 TLS details <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md>`_
* `Cloudflare Blog <https://blog.cloudflare.com/ja4-signals>`_
* `FoxIO Blog <https://blog.foxio.io/ja4%2B-network-fingerprinting>`_
* `FoxIO JA4 Database <https://ja4db.com/>`_
* `JA4 Suite <https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/README.md>`_

Setup
=====

* Add the LUA script `ja4.lua` to your system

Config
======

* Enable SSL/TLS capture with the global setting `tune.ssl.capture-buffer-size 128 <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#tune.ssl.capture-buffer-size>`_
* Load the LUA module by adding `lua-load /etc/haproxy/lua/ja4.lua` in the `global` section
* Execute the LUA script on HTTP requests: `http-request lua.fingerprint_ja4`
* Log the fingerprint: `http-request capture var(txn.fingerprint_ja4) len 36`

JA4 Database
============

You can use `the DB=>MAP script <https://github.com/O-X-L/haproxy-ja4/blob/latest/ja4db-to-map.py`_ to create a HAProxy Mapfile from the `FoxIO JA4-Database <https://ja4db.com/>`_:

.. code-block:: bash

    # download the DB in JSON format: https://ja4db.com/api/download/
    # place it in the same directory as the script

    # build the map-file
    python3 ja4db-to-map.py

    # examples:
    > t13d1517h2_8daaf6152771_b0da82dd1658 Mozilla/5.0_(Windows_NT_10.0;_Win64;_x64)_AppleWebKit/537.36_(KHTML,_like_Gecko)_Chrome/125.0.0.0_Safari/537.36
    > t13d1516h2_8daaf6152771_02713d6af862 Chromium_Browser

You can enable lookups like this: :code:`http-request set-var(txn.fingerprint_app) var(txn.fingerprint_ja4),map(/etc/haproxy/map/fingerprint_ja4_app.map)`

And log the results like this: :code:`http-request capture var(txn.fingerprint_app) len 200`

.. include:: ../_include/user_rath.rst
