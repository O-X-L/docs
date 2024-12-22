.. _atm_ansible_webui:

.. include:: ../_include/head.rst

===============
Ansible - WebUI
===============

.. include:: ../_include/wip.rst

**Intro Videos:** `YouTube @OXL-IT <https://www.youtube.com/playlist?list=PLsYMit2eI6VVjtK89CcwCEccT7KHah9Sh>`_

Intro
#####

All :ref:`Ansible Web-Interfaces <atm_ansible_webui>` build on-top of this core-tool. If you want to understand how it works and how to troubleshoot it - we recommend you starting to use Ansible via shell/CLI!

We will not (*yet*) go into the details on how to set-up such Web-Interfaces.

----

Security
########

As these web applications will have **access to your infrastructure credentials**, to run jobs, make sure you really trust those projects.

They also have **remote code execution by design** (*as this is what IT-Automation is all about*).

If this tool gets taken-down by an attacker - you have a bad time ahead of you.

----

Official
########

If you are a business that wants to use Ansible extensively - **we recommend to use & buy the Web-Interface provided by RedHat Ansible**: `Ansible Automation Platform <https://www.redhat.com/en/technologies/management/ansible>`_

Open-Source Version - AWX
*************************

For testing purposes you can first use the Open-Source version of it: `Ansible AWX <https://www.ansible.com/community/awx-project>`_.

But this one comes without any official support.

You have to set-up Kubernetes and run it on top of that.

From practical experience - **we cannot recommend it** for production use.

----

Community-Driven
################

There are some other Open-Source projects that you can use. They all have benefits and drawbacks.

These tool might be useful for admins, tech-enthusiasts and small to medium businesses. But if you are using Ansible on a larger scale or your business depends on it - invest the money and buy the official Ansible product!

Lightweight local Ansible WebUI
*******************************

We have developed a very simple and lightweight `Ansible WebUI <https://github.com/O-X-L/ansible-webui>`_!

.. code-block:: bash

    # install
    python3 -m pip install oxl-ansible-webui

    # enter your playbook directory; for example:
    cd ~/ansible

    # run
    python3 -m oxl-ansible-webui

    # copy the auto-created credentials

Afterwards you can access the WebUI: `http://localhost:8000 <http://localhost:8000>`_

Documentation: `ansible-webui.oxl.at <ansible-webui.oxl.at>`_

----

Ansible Forms
*************

If you want a nice WebUI that is specialized in providing forms for Ansible - `Ansible Forms <https://github.com/ansibleguy76/ansibleforms>`_ is another choice.

Documentation: `ansibleforms.com <https://ansibleforms.com/introduction/>`_

----

Ansible Semaphore
*****************

`Semaphore <https://github.com/semaphoreui/semaphore>`_ is another choice.

We have seen some issues with the way the project is maintained (*many open issues, important issues not being addressed in months*) and the direction in which it is going (*cloud-based product with many features - no focus on Ansible*).

Thus **we can not recommend it**.

But basically it has a pretty UI and could work for your use-cases.

Documentation: `docs.semaphoreui.com <https://docs.semaphoreui.com/>`_

.. include:: ../_include/user_rath.rst
