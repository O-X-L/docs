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

Please note: If you have more users than licences, you have a few days to purchase the additional licence or delete the user account - but important functions such as ‘scheduled tasks’ will be deactivated during this period!

----

Module Development
##################

We can develop **custom Odoo-Modules and functionality** for your business needs! See: `Odoo Module Development <https://www.oxl.app/odoo>`_

Guide
*****

See: `Module-Development Guide <https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101.html>`_

Install Module/Addon
********************

1. Configure the :code:`addons_path` in your :code:`/etc/odoo/odoo.conf`

    .. code-block::

        [options]
        ...
        addons_path = /var/lib/odoo/addons

2. Make sure the module/addon is supported for the installed Odoo version. Else you might run into an :code:`Internal Server Error` later on!

    .. code-block:: bash

        # get installed version on ubuntu/debian
        apt policy odoo

3. Copy the module archive to your Odoo server.

    Per example - use :code:`scp` (*replace YOUR_ADDON*)

    .. code-block:: bash

        scp ~/Download/${YOUR_ADDON}.zip ${YOUR_SERVER}:/tmp/

4. Add your module. (*replace YOUR_ADDON*)

    .. code-block:: bash

        cd /tmp
        unzip "${YOUR_ADDON}.zip"
        mv "$YOUR_ADDON" /var/lib/odoo/addons/
        chown -R root:odoo /var/lib/odoo/addons/

5. Restart Odoo:

    .. code-block:: bash

        systemctl restart odoo.service

6. `Activate the developer mode <https://www.odoo.com/documentation/18.0/applications/general/developer_mode.html>`_

7. `Update the App-List <https://www.odoo.com/documentation/18.0/applications/general/apps_modules.html#install-apps-and-modules>`_

8. If you get an :code:`Internal Server Error` afterwards:

    Your code may have an error!

    Maybe the module is not supported for the installed odoo version.

    Check your logs: :code:`tail -n 100 /var/log/odoo/odoo-server.log`

9. If the module IS NOT showing in the App-List:

    * Make sure the :code:`${YOUR_ADDON}/__manifest__.py` is named correctly and its `content is acceptable <https://www.odoo.com/documentation/18.0/developer/reference/backend/module.html>`_

    * Remove the :code:`App` filter from the App-View (*related to the manifest setting* :code:`'application': true`)


----

Administration
##############

Database Queries
****************

It can be useful to perform manual queries to analyze the data of odoo.

This works even without an addition user-account. That is important in case you use the enterprise-version and do not want to allocate an additional license.

.. code-block:: bash

    QUERY="<QUERY-HERE>"
    su --login postgres -c "psql -d odoo -c '${QUERY}'" | cat

    # query examples:
    ## show tables
    QUERY="\dt"

    ## get last 20 entries of some table (creation time)
    QUERY="SELECT * FROM <TABLE> ORDER BY id DESC LIMIT 20;

    ## get last 20 entries of some table (modification time)
    QUERY="SELECT * FROM <TABLE> ORDER BY write_date DESC LIMIT 20;

----

Backup from WebUI
*****************

You can manage your databases from this URL: :code:`https://<YOUR-DOMAIN>/web/database/manager`

----

Backup from CLI
***************

You need to backup the database and files:

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

Full backup script example: `odoo_backup.sh <https://github.com/ansibleguy/sw_odoo_community/blob/latest/templates/usr/local/bin/odoo_backup.sh.j2>`_

----

Restore from WebUI
******************

You can only restore the backup take from a WebUI - NOT the CLI-Backup!

You can manage your databases from this URL: :code:`https://<YOUR-DOMAIN>/web/database/manager`

Also note that the Odoo online setups might use newer versions than you can use on-premise. So you might need to contact the support on how to migrate the database.

----

Restore from CLI
****************

Make sure to create a backup before of your current state, before restoring another.

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

Reset User Password
*******************

If you still have access to another admin-user - you can use the WebUI!

Else you need to use the shell:

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

If you want to limit outbound connections you might need to allow HTTP+S connections to these Domains:

* nightly.odoo.com
* apps.odoo.com
* partner-autocomplete.odoo.com
* www.odoo.com
* services.odoo.com

.. include:: ../_include/user_rath.rst
