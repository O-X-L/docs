.. _atm_ansible_setup:

.. include:: ../_include/head.rst

===============
Ansible - Setup
===============

.. include:: ../_include/wip.rst

Intro
#####

This tutorial shows you how to set-up a simple Ansible controller.

At its base, Ansible is a command-line-tool. That's why the most lightweight and simple solution is to use it as such.

All :ref:`Ansible Web-Interfaces <atm_ansible_webui>` build on-top of this core-tool. If you want to understand how it works and how to troubleshoot it - we recommend you starting to use Ansible via shell/CLI!

----

Basic Ansible
#############

Prerequisites
*************

Ansible `can only run on a linux/unix system <https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html>`_!

Windows
=======

`Microsoft WSL is not supported <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements>`_. It might work, but it can be unstable.

If you are running on a Windows client-OS you will need to either:

* Install a Linux virtual machine locally (for example using `VirtualBox <https://www.virtualbox.org/>`_)

  If you are using an IDE/Editor to manage your Ansible projects - you might want to map/redirect your local project directories into your VM.

  You might not want/need a GUI installation of linux. Commandline-only will do. Per example: `Debian minimal <https://www.debian.org/CD/netinst/>`_ (*what we recommend*) or `Ubuntu server <https://ubuntu.com/download/server>`_

* Or `use a Docker container <https://hub.docker.com/r/ansible/ansible>`_

----

Editor / IDE
============

You can make your life a lot easier by installing a IDE/Editor that supports syntax checking for Ansible and its related file-types.

* `VSCode <https://code.visualstudio.com/download>`_

  `Official Ansible Plugin <https://marketplace.visualstudio.com/items?itemName=redhat.ansible>`_

* `PyCharm <https://www.jetbrains.com/pycharm/>`_

  `Ansible Plugin <https://plugins.jetbrains.com/plugin/14893-ansible>`_

----

Install
*******

You need Python3 and PIP to run Ansible:

.. code-block:: bash

    sudo apt install python3 python3-pip

The 'sshpass' package is needed for the SSH connection-type:

.. code-block:: bash

    sudo apt install sshpass

Create a `Python virtual-environment <https://realpython.com/python-virtual-environments-a-primer/>`_:

.. code-block:: bash

    python3 -m pip install virtualenv
    python3 -m virtualenv ~/venv_ansible

    # automatically activate the venv on login
    echo 'VIRTUAL_ENV_DISABLE_PROMPT=1 source ~/venv_ansible/bin/activate' >> ~/.bashrc

    # logout and -in

    # you can verify it is active by checking which python3 binary is currently used
    which python3
    > ~/venv_ansible/bin/python3

Install Ansible itself


.. code-block:: bash

    python3 -m pip install ansible

    # try to execute it
    ansible-playbook --help

----

Collections / Roles
###################

There are many Ansible Collections and Roles you can use.

Collections can provide a `wide range of features <https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html>`_.

**Important**: You need to have a security awareness:

* These Roles and Modules will get **access to the secrets you pass to Ansible** whenever you execute them!
* These Roles and Modules can **execute code on the target system** using your privileges!

So be sure they are from a trusted source and maintainer! Test them well.

See: `Ansible Collection Index <https://docs.ansible.com/ansible/latest/collections/index.html>`_, `Ansible Galaxy Collections <https://galaxy.ansible.com/ui/collections/>`_, `Ansible Galaxy Roles <https://galaxy.ansible.com/ui/standalone/roles/>`_

You can install them like so:

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

You can also save your requirements to a file:

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

See also: `Install Roles <https://galaxy.ansible.com/docs/using/installing.html#installing-multiple-roles-from-a-file>`_ and `install Collections <https://docs.ansible.com/ansible/devel/collections_guide/collections_installing.html#installing-collections-with-ansible-galaxy>`_

And install them:

.. code-block:: bash

    # roles
    ansible-galaxy install -r requirements.yml

    # collections
    ansible-galaxy collection install -r requirements.yml

----

Linting
#######

Using lint-checks helps you to ensure your code/scripts **comply with existing best-practices** and show you errors you have made.

These checks provide you with feedback and help you learn faster and more efficient.

Install
*******

.. code-block:: bash

    python3 -m pip install ansible-lint yamllint pylint

----

Configure
*********

You might have the need to disable or modify some tests.

Ansible-Lint
============

See: `Documentation <https://ansible-lint.readthedocs.io/configuring/>`_

YamlLint
========

See: `Documentation <https://yamllint.readthedocs.io/en/stable/configuration.html>`_

PyLint
======

Generate the default config for your current version of pylint:

.. code-block:: bash

    pylint --generate-rcfile > .pylintrc

See: `Documentation <https://yamllint.readthedocs.io/en/stable/configuration.html>`_

----

Run
***

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
