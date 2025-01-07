.. _waf_coraza:

.. include:: ../_include/head.rst

==============
Coraza (OWASP)
==============

.. include:: ../_include/wip.rst

Intro
#####

The `Coraza Open-Source Web-Application-Firewall <https://coraza.io/>`_ is managed by the `OWASP organization <https://owasp.org/www-project-coraza-web-application-firewall/>`_.

The `Core-Ruleset <https://coraza.io/docs/tutorials/coreruleset/>`_ can be used as protection against various practical attacks. See also: `github.com/corazawaf/coraza-coreruleset <https://github.com/corazawaf/coraza-coreruleset>`_ & `Core-Ruleset Docs <https://coreruleset.org/docs/concepts/anomaly_scoring/>`_

This set of rules can be implemented quite quickly/easily and customized for specific applications.

This WAF can be integrated into existing load balancers: `Caddy <https://github.com/corazawaf/coraza-caddy>`_, `Nginx <https://github.com/corazawaf/coraza-nginx>`_, `HAProxy <https://github.com/corazawaf/coraza-spoa>`_

----

HAProxy Integration
###################

**Info**: The HAProxy integration is not yet considered production-ready!

The `HAProxy SPOE interface <https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine>`_ is used to integrate it.

To integrate this WAF into HAProxy (Community), the following must be implemented on the target system:

Alternatively, the Ansible role can be used: `HAProxy Coraza-WAF <https://github.com/ansibleguy/haproxy_waf_coraza>`_

----

HAProxy Installation
********************

Install HAProxy in version >= 3.1 (*SPOE Refactor*)

Debian: `haproxy.debian.net <https://haproxy.debian.net/>`_

----

Coraza-SPOE Installation
************************

Currently you have to compile it from source-code (by using `Golang <https://go.dev/doc/install>`_).

Alternatively you could use `the pre-compiled binary <https://github.com/O-X-L/coraza-spoa/releases>`_ from our repository.


.. code-block:: bash

    cd /tmp

    # golang
    wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    # echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

    # coraza-spoe
    wget https://github.com/corazawaf/coraza-spoa/archive/refs/heads/main.zip
    unzip main.zip
    cd coraza-spoa-main/
    go build -o /usr/bin/coraza-spoa
    /usr/bin/coraza-spoa -help

----

Service-User
************

Add a service user:

.. code-block:: bash

    useradd coraza-spoa --shell /usr/sbin/nologin

----

Service
*******

Add the service:

.. code-block:: bash

    wget https://raw.githubusercontent.com/corazawaf/coraza-spoa/refs/heads/main/contrib/coraza-spoa.service -O /etc/systemd/system/coraza-spoa.service


Optional - Service-Einstellungen per Override anpassen:

.. code-block:: bash

    mkdir /etc/systemd/system/coraza-spoa.service.d
    nano /etc/systemd/system/coraza-spoa.service.d/override.conf

Override content (e.g.):

.. code-block:: text

    [Unit]
    Documentation=https://github.com/corazawaf/coraza-spoa
    Documentation=https://github.com/corazawaf/coraza
    Documentation=https://coraza.io/docs/seclang/directives/

    [Service]
    User=coraza-spoa
    Group=coraza-spoa

    StandardOutput=journal
    StandardError=journal
    SyslogIdentifier=coraza-spoa
    Restart=on-failure
    RestartSec=5s

Activate it:

.. code-block:: bash

    systemctl daemon-reload
    systemctl enable coraza-spoa.service

----

Main Configuration
******************

.. code-block:: bash

    mkdir /etc/coraza-spoa
    chmod 750 /etc/coraza-spoa
    chown root:coraza-spoa /etc/coraza-spoa
    nano /etc/coraza-spoa/config.yaml

Example:

.. code-block:: yaml

    ---

    bind: '127.0.0.1:9000'

    log_level: 'info'
    log_file: '/dev/stdout'
    log_format: 'json'

    applications:
      - name: 'app1'
        directives: |
          Include /etc/coraza-spoa/apps/app1/@coraza.conf
          Include /etc/coraza-spoa/apps/app1/@crs-setup.conf
          Include /etc/coraza-spoa/apps/app1/@owasp_crs/*.conf

        response_check: false
        transaction_ttl_ms: 60000

        log_level: 'info'
        log_file: '/var/log/coraza-spoa/app1.log'
        log_format: 'json'

      - name: 'app1-api'
        directives: |
          Include /etc/coraza-spoa/apps/app1-api/@coraza.conf
          Include /etc/coraza-spoa/apps/app1-api/@crs-setup.conf
          Include /etc/coraza-spoa/apps/app1-api/@owasp_crs/*.conf

        response_check: false
        transaction_ttl_ms: 60000

        log_level: 'info'
        log_file: '/var/log/coraza-spoa/app1-api.log'
        log_format: 'json'

      - name: 'fallback'
        # you may want to use a detect-only config as fallback
        directives: ''
        response_check: false
        transaction_ttl_ms: 60000

        log_level: 'info'
        log_file: '/var/log/coraza-spoa/default.log'
        log_format: 'json'

Note: Instead of using multiple app-specific ruleset-directories you can also only use a single one and add config-overrides to the 'directives' afterwards:

.. code-block::

      - name: 'app'
        directives: |
          Include /etc/coraza-spoa/crs/coraza-coreruleset-4.7.0/rules/@coraza.conf
          Include /etc/coraza-spoa/crs/coraza-coreruleset-4.7.0/rules/@crs-setup.conf
          Include /etc/coraza-spoa/crs/coraza-coreruleset-4.7.0/rules/@owasp_crs/*.conf
          SecRuleEngine On
          <add-other-overrides-here>

----

Core-Ruleset
************

.. code-block:: bash

    cd /tmp/
    wget https://github.com/corazawaf/coraza-coreruleset/archive/refs/tags/v4.7.0.tar.gz
    mkdir /etc/coraza-spoa/crs
    tar -xzvf v4.7.0.tar.gz -C /etc/coraza-spoa/crs

    # add the default ruleset for your app(s)
    cd /etc/coraza-spoa
    mkdir -p apps/app1
    cp -r crs/coraza-coreruleset-4.7.0/rules/@owasp_crs/ apps/app1/
    cp -r crs/coraza-coreruleset-4.7.0/rules/@coraza.conf-recommended apps/app1/@coraza.conf
    cp -r crs/coraza-coreruleset-4.7.0/rules/@crs-setup.conf.example apps/app1/@crs-setup.conf

    # start service
    systemctl start coraza-spoa.service

    # check it
    systemctl status coraza-spoa.service

----

HAProxy SPOE
************

Download the standard SPOE configuration:

.. code-block:: bash

    wget https://raw.githubusercontent.com/corazawaf/coraza-spoa/refs/heads/main/example/haproxy/coraza.cfg -O /etc/haproxy/coraza-spoe.cfg

We will change some options in this setup:

.. code-block:: text

    [coraza]
    spoe-agent coraza-agent
        # Process HTTP requests only (the responses are not evaluated)
        messages    coraza-req
        groups      coraza-req
        # Comment the previous line and add coraza-res, to process responses also.
        #messages   coraza-req     coraza-res
        option      var-prefix      coraza
        option      set-on-error    error
        timeout     hello           2s
        timeout     idle            2m
        timeout     processing      500ms
        use-backend coraza-spoa
        log         global

    spoe-message coraza-req
        # Arguments are required to be in this order
        args app=var(txn.waf_app) src-ip=src src-port=src_port dst-ip=dst dst-port=dst_port method=method path=path query=query version=req.ver headers=req.hdrs body=req.body
        # event on-frontend-http-request

    spoe-group coraza-req
        messages coraza-req

    spoe-message coraza-res
        # Arguments are required to be in this order
        args app=var(txn.waf_app) id=var(txn.coraza.id) version=res.ver status=status headers=res.hdrs body=res.body
        event on-http-response

----

HAProxy Configuration
*********************

Add the backend:

.. code-block:: text

    backend coraza-spoa
        mode tcp
        server coraza-waf 127.0.0.1:9000 check


We can use the :code:`txn.waf_app` variable to switch between multiple WAF-applications:

.. code-block:: text

    http-request set-var(txn.waf_app) str(app1) if domain_app1 !location_api
    http-request set-var(txn.waf_app) str(app1-api) if domain_app1 location_api
    http-request set-var(txn.waf_app) str(fallback) if !{ var(txn.waf_app) -m found }
    filter spoe engine coraza config /etc/haproxy/coraza-spoe.cfg
    http-request send-spoe-group coraza coraza-req

We can log the coraza information as follows:

.. code-block:: text

    http-request capture var(txn.waf_app) len 50
    http-request capture var(txn.coraza.id) len 16
    http-request capture var(txn.coraza.error) len 1
    http-request capture var(txn.coraza.action) len 8

We can perform the following actions:

.. code-block:: text

    http-request deny status 403 if { var(txn.coraza.action) -m str deny }
    http-response deny status 403 if { var(txn.coraza.action) -m str deny }

    http-request silent-drop if { var(txn.coraza.action) -m str drop }
    http-response silent-drop if { var(txn.coraza.action) -m str drop }

    # optional:
    # http-request redirect code 302 location %[var(txn.coraza.data)] if { var(txn.coraza.action) -m str redirect }
    # http-response redirect code 302 location %[var(txn.coraza.data)] if { var(txn.coraza.action) -m str redirect }

----

Coraza Configuration
********************

Inside the :code:`/etc/coraza-spoa/apps/<APP>/@coraza.conf` config you can `configure the Coraza-WAF functionalities <https://coraza.io/docs/seclang/directives/>`_.

To enable blocking of bad traffic - you have to at least set :code:`SecRuleEngine On`!

----

Ruleset Configuration
*********************

See: `Core-Ruleset Docs <https://coreruleset.org/docs/concepts/anomaly_scoring/>`_

Of course, additional rules can also be configured that are specifically tailored to the applications.
