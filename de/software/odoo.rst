.. _sw_odoo:

.. include:: ../_include/head.rst

===============
Odoo ERP System
===============

.. include:: ../_include/wip.rst

Intro
#####

Siehe: `Odoo ERP <https://www.odoo.com>`_

----

On-Premise Installation
#######################

Community Edition
*****************

Siehe: `Odoo Community Docs <https://www.odoo.com/documentation/17.0/administration/on_premise/packages.html>`_

Ansible Role: `ansibleguy.sw_odoo_community <https://github.com/ansibleguy/sw_odoo_community>`_


Enterprise Edition
******************

Siehe: `Odoo Migration Docs <https://www.odoo.com/documentation/17.0/administration/on_premise/community_to_enterprise.html#on-linux-using-an-installer>`_

Hinweis: Die Migration von der Enterprise Edition zurück zur Community Edition ist nicht einfach, da einige Funktionen nicht unterstützt werden!

----

Modul-Entwicklung
#################

Wir können **maßgeschneiderte Odoo-Module und Funktionalitäten** für Ihre Bedürfnisse entwickeln! Siehe: `Odoo Modul-Entwicklung <https://www.oxl.at/odoo>`_

Anleitung
*********

Siehe: `Module-Development Guide <https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101.html>`_

Modul/Erweiterung installieren
******************************

1. Den :code:`addons_path` in der Konfiguration :code:`/etc/odoo/odoo.conf` setzen

    .. code-block::

        [options]
        ...
        addons_path = /var/lib/odoo/addons

2. Stellen Sie sicher, dass das Modul/Addon von der installierten Odoo-Version unterstützt wird. Andernfalls könnten Sie später auf einen :code:`Internal Server Error` stoßen!

    .. code-block:: bash

        # get installed version on ubuntu/debian
        apt policy odoo

3. Kopieren Sie das Modularchiv auf Ihren Odoo-Server.

    Zum Beispiel via :code:`scp` (*YOUR_ADDON ersetzen*)

    .. code-block:: bash

        scp ~/Download/${YOUR_ADDON}.zip ${YOUR_SERVER}:/tmp/

4. Das Modul hinzufügen. (*YOUR_ADDON ersetzen*)

    .. code-block:: bash

        cd /tmp
        unzip "${YOUR_ADDON}.zip"
        mv "$YOUR_ADDON" /var/lib/odoo/addons/
        chown -R root:odoo /var/lib/odoo/addons/

5. Odoo neustarten:

    .. code-block:: bash

        systemctl restart odoo.service

6. `Den Entwickler-Modus aktivieren <https://www.odoo.com/documentation/18.0/applications/general/developer_mode.html>`_

7. `Die App-Liste aktualisieren <https://www.odoo.com/documentation/18.0/applications/general/apps_modules.html#install-apps-and-modules>`_

8. Wenn Sie danach einen :code:`Internal Server Error` sehen:

    Ihr Code könnte einen Fehler haben!

    Vielleicht wird das Modul von der installierten Odoo-Version nicht unterstützt.

    Prüfen Sie Ihre Logs: :code:`tail -n 100 /var/log/odoo/odoo-server.log`

9. Wenn das Modul NICHT in der App-Liste angezeigt wird:

    * Stellen Sie sicher, dass die :code:`${YOUR_ADDON}/__manifest__.py` korrekt benannt ist und dessen `Inhalt akzeptable ist <https://www.odoo.com/documentation/18.0/developer/reference/backend/module.html>`_

    * Den :code:`App` Filter von der App-Ansicht entfernen (*von dieser manifest Einstellung* :code:`'application': true`)

----

Administration
##############

Sicherung via Weboberfläche
***************************

Sie können Ihre Datenbanken von dieser URL aus verwalten: :code:`https://<YOUR-DOMAIN>/web/database/manager`

----

Sicherung via CLI
*****************

Sie müssen die Datenbank und die Dateien sichern:

.. code-block:: bash

    set -euo pipefail
    apt install xz-utils

    BACKUP_DIR='/var/backups/odoo'

    # create backup directory
    mkdir -p "$BACKUP_DIR"
    chmod 750 "$BACKUP_DIR"

    # create database dump
    sudo -u postgres pg_dumpall | xz > "${BACKUP_DIR}/odoo.sql.xz"

    # backup files
    tar -cJvf "${BACKUP_DIR}/odoo.file.xz" /var/lib/odoo/ /etc/odoo/

    # limit access
    chmod 640 "${BACKUP_DIR}/odoo.sql.xz" "${BACKUP_DIR}/odoo.file.xz"

Beispiel eines Backup-Scripts: `odoo_backup.sh <https://github.com/ansibleguy/sw_odoo_community/blob/latest/templates/usr/local/bin/odoo_backup.sh.j2>`_

----

Wiederherstellung via Weboberfläche
***********************************

Sie können auf diese Art nur Sicherungen wiederherstellen, die auch über die WebUI erstellt wurden. NICHT die CLI-Backups!

Sie können Ihre Datenbanken von dieser URL aus verwalten: :code:`https://<YOUR-DOMAIN>/web/database/manager`

Beachten Sie auch, dass die Odoo-Online-Setups möglicherweise neuere Versionen verwenden als die, die Sie vor Ort nutzen können. Daher müssen Sie sich möglicherweise an den Support wenden, um zu erfahren, wie Sie die Datenbank migrieren können.

----

Wiederherstellung via CLI
*************************

Stellen Sie sicher, dass Sie zuvor eine Sicherungskopie Ihres aktuellen Zustands erstellen, bevor Sie einen anderen wiederherstellen.

.. code-block:: bash

    apt install xz-utils

    # database
    xzcat odoo.sql.xz | su --login postgres -c psql

    # files
    tar -xJvf /var/backups/odoo/odoo.file.xz -C /tmp/

    ## remove default files
    mv /var/lib/odoo/ /var/lib/odoo_new

    ## restore your files
    mv /tmp/var/lib/odoo/ /var/lib/odoo/
    mv /tmp/etc/odoo/ /etc/odoo/
    chown -R odoo:odoo /var/lib/odoo/
    chown -R root:odoo /var/lib/odoo/addons /etc/odoo

----

Kennwort Zurücksetzen
*********************

Wenn Sie noch Zugang zu einem anderen Admin-Benutzer haben, können Sie die WebUI verwenden!

Andernfalls müssen Sie die Shell verwenden:

.. code-block:: bash

    # generate password hash
     MYPWD='MY_PASSWORD' python3 -c "from os import environ; from passlib.context import CryptContext; print(CryptContext(['pbkdf2_sha512']).hash(environ['MYPWD']))"

    # update hash in DB
    su --login postgres
    psql
    \c odoo

    # check we have the correct account
    SELECT login, password FROM res_users WHERE id=2;

    # update it (change HASH to the value you got by running the 'python3' command above)
    UPDATE res_users SET password='HASH' WHERE id=2;

----

Firewalling
***********

Wenn Sie ausgehende Verbindungen einschränken möchten, müssen Sie möglicherweise HTTP+S-Verbindungen zu diesen Domänen zulassen:

* nightly.odoo.com
* apps.odoo.com
* partner-autocomplete.odoo.com
* www.odoo.com
* services.odoo.com
