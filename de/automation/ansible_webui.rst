.. _atm_ansible_webui:

.. include:: ../_include/head.rst

===============
Ansible - WebUI
===============

.. include:: ../_include/wip.rst

**Intro Videos:** `YouTube @OXL-IT <https://www.youtube.com/playlist?list=PLsYMit2eI6VUgs7KZoS9GVJf67Qyarpc7>`_

Intro
#####

Alle :ref:`Ansible Web-Interfaces <atm_ansible_webui>` bauen auf dessen Kernfunktionalität auf. Wenn Sie verstehen wollen, wie es funktioniert und wie man Fehler behebt, empfehlen wir Ihnen, Ansible (*Anfangs*) über die Shell/CLI zu benutzen!

Wir werden (*noch*) nicht im Detail darauf eingehen, wie solche Web-Schnittstellen eingerichtet werden.

----

Security
########

Da diese Webanwendungen **Zugang zu Ihren Infrastruktur-Zugangsdaten** haben, um Jobs auszuführen, sollten Sie diesen Projekten wirklich vertrauen.

Außerdem haben diese **vom Design her eine Remote-Code-Ausführung** (*da es die Kern-Funktionalität der IT-Automatisierung ist*).

Wenn dieses Tool von einem Angreifer übernommen wird, haben Sie eine schlechte Zeit vor sich.

----

Offiziell
#########

Wenn Sie ein Unternehmen sind, das Ansible ausgiebig nutzen möchte - **empfehlen wir Ihnen, das von RedHat Ansible bereitgestellte Web-Interface zu nutzen und zu kaufen**: `Ansible Automation Platform <https://www.redhat.com/en/technologies/management/ansible>`_

Open-Source Version - AWX
*************************

Zu Testzwecken können Sie zunächst die Open-Source-Version des Programms verwenden: `Ansible AWX <https://www.ansible.com/community/awx-project>`_.

Diese wird jedoch nicht offiziell unterstützt.

Sie müssen Kubernetes einrichten und es darauf ausführen.

Aus praktischer Erfahrung **können wir es nicht für den Produktionseinsatz empfehlen**.

----

Community Projekte
##################

Es gibt einige andere Open-Source-Projekte, die Sie verwenden können. Sie alle haben Vor- und Nachteile.

Diese Tools können für Administratoren, Technikbegeisterte und kleine bis mittlere Unternehmen nützlich sein. Aber wenn Sie Ansible in größerem Umfang einsetzen oder Ihr Unternehmen davon abhängt - **investieren Sie das Geld und kaufen Sie das offizielle Ansible-Produkt**!

Leichtgewichtige lokale Ansible WebUI
*************************************

Wir haben eine sehr einfache und leichtgewichtige `Ansible WebUI <https://github.com/O-X-L/ansible-webui>`_ entwickelt!

.. code-block:: bash

    # install
    python3 -m pip install oxl-ansible-webui

    # enter your playbook directory; for example:
    cd ~/ansible

    # run
    python3 -m oxl-ansible-webui

    # copy the auto-created credentials

Danach können Sie auf die WebUI zugreifen: `http://localhost:8000 <http://localhost:8000>`_

Dokumentation: `ansible-webui.oxl.at <ansible-webui.oxl.at>`_

----

Ansible Forms
*************

Wenn Sie eine schöne WebUI wollen, die auf die Bereitstellung von Formularen für Ansible spezialisiert ist - `Ansible Forms <https://github.com/ansibleguy76/ansibleforms>`_ ist eine weitere Option.

Dokumentation: `ansibleforms.com <https://ansibleforms.com/introduction/>`_

----

Ansible Semaphore
*****************

`Semaphore <https://github.com/semaphoreui/semaphore>`_ ist auch eine Option.

Wir haben einige Probleme mit der Art und Weise erkannt, wie das Projekt gewartet wird (*viele offene Probleme, wichtige Fehler werden nach Monaten nicht behoben*) und die Richtung, in die es geht (*cloud-basiertes Produkt mit vielen Funktionen - kein Fokus auf Ansible*).

Daher **können wir es nicht empfehlen**.

Aber grundsätzlich hat es eine hübsche Benutzeroberfläche und könnte für Ihre Anwendungsfälle funktionieren.

Dokumentation: `docs.semaphoreui.com <https://docs.semaphoreui.com/>`_

.. include:: ../_include/user_rath.rst
