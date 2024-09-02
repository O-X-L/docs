.. _sw_odoo:

.. include:: ../_include/head.rst

===============
Odoo ERP System
===============

.. include:: ../_include/wip.rst

Intro
#####

See: `Odoo ERP <https://www.odoo.com>`_

----

On-Premise Installation
#######################

Community Edition
*****************

See: `Odoo Community Docs <https://www.odoo.com/documentation/17.0/administration/on_premise/packages.html>`_

Ansible Role: `ansibleguy.sw_odoo_community <https://github.com/ansibleguy/sw_odoo_community>`_


Enterprise Edition
******************

See: `Odoo Migration Docs <https://www.odoo.com/documentation/17.0/administration/on_premise/community_to_enterprise.html#on-linux-using-an-installer>`_

Note: Migrating from enterprise back to community edition is not easy as some features are not supported!

----

Administration
##############

Backup from WebUI
*****************

You can manage your databases from this URL: :code:`https://<YOUR-DOMAIN>/web/database/manager`

----

Backup from CLI
***************

You need to backup the database and files:

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

Full backup script example: `odoo_backup.sh <https://github.com/ansibleguy/sw_odoo_community/blob/latest/templates/usr/local/bin/odoo_backup.sh.j2>`_

----

Restore from WebUI
******************

You can manage your databases from this URL: :code:`https://<YOUR-DOMAIN>/web/database/manager`

Also note that the Odoo online setups might use newer versions than you can use on-premise. So you might need to contact the support on how to migrate the database.

----

Restore from CLI
****************

Make sure to create a backup before of your current state, before restoring another.

.. code-block:: bash

    # database
    xzcat odoo.sql.xz | su --login postgres psql -d odoo

    # files
    tar -xJvf /var/backups/odoo/odoo.file.xz -C /tmp/
    mv /tmp/var/lib/odoo/ /var/lib/odoo/
    chown -R odoo:odoo /var/lib/odoo/

----

Reset User Password
*******************

If you still have access to another admin-user - you can use the WebUI!

Else you need to use the shell:

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

If you want to limit outbound connections you might need to allow HTTP+S connections to these Domains:

* nightly.odoo.com
* apps.odoo.com
* partner-autocomplete.odoo.com
* www.odoo.com
* services.odoo.com
