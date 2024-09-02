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

Administration
##############

Backup aus der WebUI
********************

Sie können Ihre Datenbanken von dieser URL aus verwalten: :code:`https://<YOUR-DOMAIN>/web/database/manager`

----

Backup from CLI
***************

Sie müssen die Datenbank und die Dateien sichern:

.. code-block:: bash

    set -euo pipefail

    BACKUP_DIR='/var/backups/odoo'

    # create backup directory
    mkdir -p "$BACKUP_DIR"
    chmod 750 "$BACKUP_DIR"

    # create database dump
    sudo -u postgres pg_dumpall | xz > "${BACKUP_DIR}/odoo.sql.xz"

    # backup files
    tar -cJvf "${BACKUP_DIR}/odoo.file.xz" '/var/lib/odoo/'

    # limit access
    chmod 640 "${BACKUP_DIR}/odoo.sql.xz" "${BACKUP_DIR}/odoo.file.xz"

Beispiel eines Backup-Scripts: `odoo_backup.sh <https://github.com/ansibleguy/sw_odoo_community/blob/latest/templates/usr/local/bin/odoo_backup.sh.j2>`_

----

Restore from WebUI
******************

Sie können Ihre Datenbanken von dieser URL aus verwalten: :code:`https://<YOUR-DOMAIN>/web/database/manager`

Beachten Sie auch, dass die Odoo-Online-Setups möglicherweise neuere Versionen verwenden als die, die Sie vor Ort nutzen können. Daher müssen Sie sich möglicherweise an den Support wenden, um zu erfahren, wie Sie die Datenbank migrieren können.

----

Restore from CLI
****************

Stellen Sie sicher, dass Sie zuvor eine Sicherungskopie Ihres aktuellen Zustands erstellen, bevor Sie einen anderen wiederherstellen.

.. code-block:: bash

    # database
    xzcat odoo.sql.xz | su --login postgres psql -d odoo

    # files
    tar -xJvf /var/backups/odoo/odoo.file.xz -C /tmp/
    mv /tmp/var/lib/odoo/ /var/lib/odoo/
    chown -R odoo:odoo /var/lib/odoo/

----

Kennwort Zurücksetzen
*********************

Wenn Sie noch Zugang zu einem anderen Admin-Benutzer haben, können Sie die WebUI verwenden!

Andernfalls müssen Sie die Shell verwenden:

.. code-block:: bash

    # generate password hash
     export MYPWD='MY_PASSWORD'
    python3 -c "from os import environ; from passlib.context import CryptContext; print(CryptContext(['pbkdf2_sha512']).hash(environ['MYPWD']))"

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
