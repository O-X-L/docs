.. _mail_security:

.. include:: ../_include/head.rst

===================
Security & Spoofing
===================

.. include:: ../_include/wip.rst

Intro
#####

Technologically - everybody is capable of sending mails for every email address. It is the **responsibility of the sender and receiver to have the SPF, DKIM and DMARC protocols configured correctly**, to secure their email flows.

Spoofing is describing the act of sending emails for an email-address without being authorized to do so.

Most of the time the attacker wants to impersonate someone to gain the trust of the email receiver.

**Tricks of attackers** also include:

* Using the :code:`display name` of emails to hide illegitimate email senders as this Display-Name is the primary one shown to receivers.

  Example: :code:`Your Boss <xyz@gmail.com>`

* Using `look-alike domains <https://en.wikipedia.org/wiki/IDN_homograph_attack>`_  to trick receivers.

  Example: :code:`yahoo.com (correct) VS yаhoo.com (fake)`

See also: `Cloudflare Blog - Email spoofing <https://www.cloudflare.com/learning/email-security/what-is-email-spoofing/>`_

----

SPF
###

**Sender Policy Framework**

* E-Mail **senders** have to configure it in their DNS records
* E-Mail **receivers** have to enable SPF checking on their E-Mail servers


SPF is defined in `RFC 7208 <https://tools.ietf.org/html/rfc7208>`_.

The SPF record describes which servers are authorized to send as that domain by using mechanisms to identify authorized IP addresses and hostnames, or even include the SPF records of other domains.

SPF cannot stop email spoofing. It only makes it a bit more difficult for an attacker.

It checks the content of the :code:`envelope from`, not the :code:`message from` header that the receiving mail client sees. The SMTP transaction are not visible to the end client, even when viewing the message headers. If the E-Mail is forwarded by a mail-server or -proxy, it invalidated.

SPF Examples
************

These are the allowed statements: :code:`ip4:<IP>`, :code:`ip6:<IP>`, :code:`mx`, :code:`a:<DNS>`, :code:`include:<DNS>`, :code:`redirect:<DNS>`, :code:`exists`

* Allowing only E-Mails from you mail server, deny all others.

    .. code-block:: bash

        Record: o-x-l.com
        Type:   TXT
        Value:  v=spf1 mx -all

* Allowing E-Mails from your mail server and a Cloud service, deny all others.

    .. code-block:: bash

      Record: o-x-l.com
      Type:   TXT
      Value:  v=spf1 mx include:amazonses.com -all


* For DNS records that are not used to send mails, you should always deny any! Else someone could exploit those to send spoofing mails.

    .. code-block:: bash

        Record: *.o-x-l.com
        Type:   TXT
        Value:  v=spf1 -all

  We've also seen spoofing attempts that use records that are used for non-mailing services. You may also want to deny mails from these.

    .. code-block:: bash

        Record: www.o-x-l.com
        Type:   A
        Value:  <IP OF WEB SERVICE>

        Record: www.o-x-l.com
        Type:   TXT
        Value:  v=spf1 -all


Limits
******

SPF records are invalid if there are more than 10 :code:`include` (recursively)! This can be especially tricky if you rely on some cloud providers that already use multiple includes internally.

----

DKIM
####

**DomainKeys Identified Mail**

* The **sender** needs to create a DKIM public-private key-pair that is identified using a :code:`selector`
* The **sender** needs to configure the sending service to sign the emails with its private key
* The **sender** needs to publish the public-key as a DNS record
* E-Mail **receivers** have to enable DKIM checking on their E-Mail servers

DomainKeys Identified Mail is a email message authentication standard, defined in `RFC 6376 <https://tools.ietf.org/html/rfc6376>`_.

DKIM authenticates the message headers, rather than the SMTP headers, thus DKIM authentication stays valid if the message is forwarded by a mail-server or -proxy.

There are some attack vectors on this protocol - like `DKIM forging <https://github.com/chenjj/espoofer>`_. Implementing DMARC may prevent attacks that exploit a :code:`d` parameter override.


DKIM Examples
*************

* The key-pair selector is :code:`mail123`

    .. code-block:: bash

        Record: mail123._domainkey.o-x-l.com
        Type:   TXT
        Value:  v=DKIM1;k=rsa;t=s;s=<SERVICE>;p=<PUBLIC-KEY-B64>

----

DMARC
#####

**Domain-based Message Authentication, Reporting and Conformance**

* The **sender** needs to publish a DMARC DNS record
* E-Mail **receivers** have to enable DMARC checking on their E-Mail servers

It is defined in `RFC 7489 <https://www.rfc-editor.org/rfc/rfc7489>`_.

DMARC ensures that the SPF and DKIM authentication mechanisms actually authenticate against the same base domain that the end user sees.

Reporting
*********

You can add :code:`rua` (aggregate) and :code:`ruf` (forensic) to your DMARC record to get sent reports from receiving mail systems, regarding your delivery stats.

This is very useful to gain insights into the health of your email flows. It also shows you if someońe is spoofing your email domain.

**Example**: :code:`rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc@o-x-l.com`

You can use tools like `parsedmarc <https://github.com/O-X-L/dmarc-analyzer>`_ to get statistics regarding possible mailing issues you have.

DMARC Examples
**************

Possible **policies**: :code:`none` (reporting/warning), :code:`quarantine`, :code:`reject`

* Initially add a DMARC record in reporting-only mode.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=none; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1;

* Enforce DMARC alignment and move all other messages from this domain into the receivers quarantine.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1;

* Set SPF & DKIM matching to be strict.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1; adkim=s; aspf=s;

* Add a subdomain-policy.

    .. code-block:: bash

        Record: _dmarc.o-x-l.com
        Type:   TXT
        Value:  v=DMARC1; p=quarantine; rua=mailto:dmarc@o-x-l.com; ruf=mailto:dmarc.o-x-l.com; fo=1; adkim=s; aspf=s; sp=quarantine;

.. include:: ../_include/user_rath.rst
