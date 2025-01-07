.. _waf_coraza:

.. include:: ../_include/head.rst

==============
Coraza (OWASP)
==============

.. include:: ../_include/wip.rst

Intro
#####

Die `Coraza Open-Source Web-Application-Firewall <https://coraza.io/>`_ wird von der `OWASP Organisation <https://owasp.org/www-project-coraza-web-application-firewall/>`_ geführt.

Als Schutz gegen diverse praktisch eingesetzte Attacken, kann das `Kern-Regelwerk <https://coraza.io/docs/tutorials/coreruleset/>`_ eingesetzt werden. Siehe auch: `github.com/corazawaf/coraza-coreruleset <https://github.com/corazawaf/coraza-coreruleset>`_ & `Core-Ruleset Docs <https://coreruleset.org/docs/concepts/anomaly_scoring/>`_

Dieses Regelwerk kann recht schnell/leicht implementiert und Applikations-Spezifisch angepasst werden.

Diese WAF kann in existierende Load-Balancer eingebunden werden: `Caddy <https://github.com/corazawaf/coraza-caddy>`_, `Nginx <https://github.com/corazawaf/coraza-nginx>`_, `HAProxy <https://github.com/corazawaf/coraza-spoa>`_

----

HAProxy Integration
###################

**Info**: Die HAProxy Integration wird noch nicht als Production-Ready angesehen!

Für die Integration wird die `HAProxy SPOE Schnittstelle <https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine>`_ genutzt.

Um diese WAF in HAProxy (Community) zu integrieren, muss folgendes am Zielsystem umgesetzt werden:

Alternativ kann die Ansible Role genutzt werden: `HAProxy Coraza-WAF <https://github.com/ansibleguy/haproxy_waf_coraza>`_

**Video:** `YouTube @OXL-IT <https://youtu.be/80Ckor6vQW0>`_

----

HAProxy installieren
********************

Installation von HAProxy >= 3.1 (*SPOE Refactor*)

Debian: `haproxy.debian.net <https://haproxy.debian.net/>`_

----

Coraza-SPOE installieren
************************

Zur Zeit muss man es (via `Golang <https://go.dev/doc/install>`_) von Source-Code kompilieren.

Alternativ kann der `von uns vor-kompilierte <https://github.com/O-X-L/coraza-spoa/releases>`_ genutzt werden.


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

Einen Service-Benutzer hinzufügen:

.. code-block:: bash

    useradd coraza-spoa --shell /usr/sbin/nologin

----

Service
*******

Den Service hinzufügen:

.. code-block:: bash

    wget https://raw.githubusercontent.com/corazawaf/coraza-spoa/refs/heads/main/contrib/coraza-spoa.service -O /etc/systemd/system/coraza-spoa.service


Optional - Service-settings via override anpassen:

.. code-block:: bash

    mkdir /etc/systemd/system/coraza-spoa.service.d
    nano /etc/systemd/system/coraza-spoa.service.d/override.conf

Override Inhalt (z.B.):

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

Service aktivieren:

.. code-block:: bash

    systemctl daemon-reload
    systemctl enable coraza-spoa.service

----

Haupt-Konfiguration
*******************

.. code-block:: bash

    mkdir /etc/coraza-spoa
    chmod 750 /etc/coraza-spoa
    chown root:coraza-spoa /etc/coraza-spoa
    nano /etc/coraza-spoa/config.yaml

Beispiel:

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

Notiz: Statt mehrere App-Spezifische Ruleset-Directories, kann man auch ein generisches nutzen und danach Config-Overrides zu den 'directives' hinzufügen:

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

Die standard SPOE-Konfiguration herunterladen:

.. code-block:: bash

    wget https://raw.githubusercontent.com/corazawaf/coraza-spoa/refs/heads/main/example/haproxy/coraza.cfg -O /etc/haproxy/coraza-spoe.cfg

In diesem Setup werden wir einige Optionen ändern:

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

HAProxy Konfiguration
*********************

Das Backend hinzufügen:

.. code-block:: text

    backend coraza-spoa
        mode tcp
        server coraza-waf 127.0.0.1:9000 check


Wir können die :code:`txn.waf_app` Variable setzen, um zwischen den WAF-Applikationen zu wechseln.

.. code-block:: text

    http-request set-var(txn.waf_app) str(app1) if domain_app1 !location_api
    http-request set-var(txn.waf_app) str(app1-api) if domain_app1 location_api
    http-request set-var(txn.waf_app) str(fallback) if !{ var(txn.waf_app) -m found }
    filter spoe engine coraza config /etc/haproxy/coraza-spoe.cfg
    http-request send-spoe-group coraza coraza-req

Folgenderweise können wir die Coraza-Infos loggen:

.. code-block:: text

    http-request capture var(txn.waf_app) len 50
    http-request capture var(txn.coraza.id) len 16
    http-request capture var(txn.coraza.error) len 1
    http-request capture var(txn.coraza.action) len 8

Folgenderweise können wir Aktionen durchführen:

.. code-block:: text

    http-request deny status 403 if { var(txn.coraza.action) -m str deny }
    http-response deny status 403 if { var(txn.coraza.action) -m str deny }

    http-request silent-drop if { var(txn.coraza.action) -m str drop }
    http-response silent-drop if { var(txn.coraza.action) -m str drop }

    # optional:
    # http-request redirect code 302 location %[var(txn.coraza.data)] if { var(txn.coraza.action) -m str redirect }
    # http-response redirect code 302 location %[var(txn.coraza.data)] if { var(txn.coraza.action) -m str redirect }

----

Coraza Konfiguration
********************

In der :code:`/etc/coraza-spoa/apps/<APP>/@coraza.conf` kann/muss man `die Funktionen der Coraza-WAF konfigurieren <https://coraza.io/docs/seclang/directives/>`_.

Um WAF scharf zu schalten, muss zumindest das Setting :code:`SecRuleEngine On` gesetzt werden!

----

Ruleset Konfiguration
*********************

Siehe: `Core-Ruleset Docs <https://coreruleset.org/docs/concepts/anomaly_scoring/>`_

Es können natürlich auch zusätzliche Regeln konfiguriert werden, die speziell auf die Applikationen zugeschnitten sind.
