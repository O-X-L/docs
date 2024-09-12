.. _atm_ansible_setup:

.. include:: ../_include/head.rst

===============
Ansible - Setup
===============

.. include:: ../_include/wip.rst

Intro
#####

Dieses Tutorial zeigt Ihnen, wie Sie einen einfachen Ansible-Controller einrichten.

Ansible ist im Grunde genommen ein Kommandozeilen-Tool. Deshalb ist es die leichteste und einfachste Lösung, es als solches zu nutzen.

Alle :ref:`Ansible Web-Interfaces <atm_ansible_webui>` bauen auf dessen Kernfunktionalität auf. Wenn Sie verstehen wollen, wie es funktioniert und wie man Fehler behebt, empfehlen wir Ihnen, Ansible (*Anfangs*) über die Shell/CLI zu benutzen!

----

Grundinstallation
#################

Voraussetzungen
***************

Ansible `kann nur auf einem Linux/Unix-System ausgeführt werden <https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html>`_!

Windows
=======

`Microsoft WSL wird nicht unterstützt <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements>`_. Es kann funktionieren, aber es kann instabil sein.

Wenn Sie mit einem Windows-Client arbeiten, müssen Sie entweder:

* Eine lokal Linux VM installieren (z. B. mit `VirtualBox <https://www.virtualbox.org/>`_)

  Wenn Sie eine IDE/Editor zur Verwaltung Ihrer Ansible-Projekte verwenden, sollten Sie Ihre lokalen Projektverzeichnisse auf Ihre VM einbinden/umleiten.

  Sie wollen/brauchen vermutlich keine GUI-Installation von Linux. Eine reine Kommandozeilen-Installation ist ausreichend. Ein Beispiel: `Debian minimal <https://www.debian.org/CD/netinst/>`_ (*von uns empfohlen*) or `Ubuntu server <https://ubuntu.com/download/server>`_

* Oder nutzen Sie `einen Docker container <https://hub.docker.com/r/ansible/ansible>`_

----

Editor / IDE
============

Sie können sich das Leben sehr erleichtern, indem Sie eine IDE/einen Editor installieren, der die Syntaxprüfung für Ansible und die damit verbundenen Dateitypen unterstützt.

* `VSCode <https://code.visualstudio.com/download>`_

  `Official Ansible Plugin <https://marketplace.visualstudio.com/items?itemName=redhat.ansible>`_

* `PyCharm <https://www.jetbrains.com/pycharm/>`_

  `Ansible Plugin <https://plugins.jetbrains.com/plugin/14893-ansible>`_

----

Install
*******

Sie benötigen Python3 und PIP, um Ansible auszuführen:

.. code-block:: bash

    sudo apt install python3 python3-pip

Das Paket 'sshpass' wird für den SSH-Verbindungstyp benötigt:

.. code-block:: bash

    sudo apt install sshpass

Erstellen Sie ein `Python virtual-environment <https://realpython.com/python-virtual-environments-a-primer/>`_:

.. code-block:: bash

    python3 -m pip install virtualenv
    python3 -m virtualenv ~/venv_ansible

    # automatically activate the venv on login
    echo 'VIRTUAL_ENV_DISABLE_PROMPT=1 source ~/venv_ansible/bin/activate' >> ~/.bashrc

    # logout and -in

    # you can verify it is active by checking which python3 binary is currently used
    which python3
    > ~/venv_ansible/bin/python3

Installieren Sie Ansible:

.. code-block:: bash

    python3 -m pip install ansible

    # try to execute it
    ansible-playbook --help

----

Collections / Roles
###################

Es gibt viele Ansible-Collections und -Roles, die Sie verwenden können.

Collections können eine `breite Palette von Funktionen bieten <https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html>`_.

**Wichtig**: Sie müssen sich folgender Sicherheitsprobleme bewusst sein:

* Diese Rollen und Module erhalten **Zugang zu den Secrets, die Sie Ansible übergeben**, wenn Sie diese ausführen!
* Diese Rollen und Module können **Code auf dem Zielsystem** mit Ihren Berechtigungen ausführen!

Stellen Sie also sicher, dass sie von einer vertrauenswürdigen Quelle und einem vertrauenswürdigen Betreuer stammen! Testen Sie diese gut.

Siehe: `Ansible Collection Index <https://docs.ansible.com/ansible/latest/collections/index.html>`_, `Ansible Galaxy Collections <https://galaxy.ansible.com/ui/collections/>`_, `Ansible Galaxy Roles <https://galaxy.ansible.com/ui/standalone/roles/>`_

Sie können sie folgendermaßen installieren:

.. code-block:: bash

    # roles
    ansible-galaxy install ansibleguy.infra_wireguard

    ## from github
    ansible-galaxy install git+https://github.com/ansibleguy/infra_haproxy

    ## install to a specific path
    ansible-galaxy install --roles-path ./roles ansibleguy.infra_wireguard

    # collections
    ansible-galaxy collection install ansibleguy.opnsense

    ## from github
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense

    ## install to a specific path
    ansible-galaxy collection install ansibleguy.opnsense -p ./collections

Sie können Ihre Anforderungen auch in einer Datei speichern:

.. code-block:: yaml

    ---

    collections:
      - name: 'community.crypto'

      - name: 'https://github.com/ansibleguy/collection_opnsense.git'
        type: 'git'

    roles:
      - src: 'ansibleguy.infra_certs'

      - name: 'ansibleguy.infra_nftables'
        src: 'https://github.com/ansibleguy/infra_nftables'

Siehe auch: `Install Roles <https://galaxy.ansible.com/docs/using/installing.html#installing-multiple-roles-from-a-file>`_ and `install Collections <https://docs.ansible.com/ansible/devel/collections_guide/collections_installing.html#installing-collections-with-ansible-galaxy>`_

Und installieren Sie diese:

.. code-block:: bash

    # roles
    ansible-galaxy install -r requirements.yml

    # collections
    ansible-galaxy collection install -r requirements.yml

----

Linting
#######

Mithilfe von Lint-Checks können Sie sicherstellen, dass Ihr Code bzw. Ihre Skripte **mit den bestehenden Best Practices** übereinstimmen, und Ihnen Fehler aufzeigen, die Sie gemacht haben.

Diese Prüfungen geben Ihnen ein Feedback und helfen Ihnen, schneller und effizienter zu lernen.

Installation
************

.. code-block:: bash

    python3 -m pip install ansible-lint yamllint pylint

----

Konfiguration
*************

Möglicherweise müssen Sie einige Tests deaktivieren oder ändern..

Ansible-Lint
============

Siehe: `Documentation <https://ansible-lint.readthedocs.io/configuring/>`_

YamlLint
========

Siehe: `Documentation <https://yamllint.readthedocs.io/en/stable/configuration.html>`_

PyLint
======

Erzeugen Sie die Standardkonfiguration für Ihre aktuelle Version von pylint:

.. code-block:: bash

    pylint --generate-rcfile > .pylintrc

Siehe: `Documentation <https://yamllint.readthedocs.io/en/stable/configuration.html>`_

----

Ausführung
**********

You may want to create a script that runs those commands in the base-directory of your project:

.. code-block:: bash

    #!/usr/bin/env bash

    set -euo pipefail

    cd "$(dirname "$0")"

    echo ''
    echo '### LINTING ANSIBLE... ###'
    ansible-lint -c .ansible-lint.yml

    echo ''
    echo '### LINTING YAML... ###'
    yamllint .

    echo ''
    echo '### LINTING PYTHON... ###'
    pylint . --recursive=y

    echo ''
    echo '### DONE ###'

.. include:: ../_include/user_rath.rst
