.. _proxy_reverse_haproxy:

.. include:: ../_include/head.rst


***********************
Reverse Proxy - HAProxy
***********************


----

Configuration
#############

If you are configuring HAProxy - have the `configuration manual <https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/>`_ ready/open! You will need it!

Check if your configuration is valid:

.. code-block:: bash

    # default - only one config file:
    /usr/sbin/haproxy -c -f /etc/haproxy/haproxy.cfg

    # custom - multiple config files:
    /usr/sbin/haproxy -c -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d/

Rate Limits
***********

Configuring rate limits can be a little confusing.

Rate limits basically consist of two components: **tables** and **trackers**

Trackers
========

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

You can use a single :code:``track-scN` to track a client in multiple tables.

Tables
======

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


Examples
--------

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

.. include:: ../_include/user_rath.rst
