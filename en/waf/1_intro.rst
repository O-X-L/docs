.. _waf_intro:

.. |waf_dev_flow| image:: ../_static/img/waf_intro.svg
   :class: wiki-img
   :alt: OXL Docs - WAF Development Flow

.. include:: ../_include/head.rst

=========
1 - Intro
=========

.. include:: ../_include/wip.rst

Intro
#####

Your application needs to be reachable for many users - many times even globally. Therefore it you will need to make sure it is secured.

WAFs supplement common (network) firewalls in protecting your systems.

The major two categories of WAFs are **cloud-hosted and self-hosted** ones.

See also: `Web application security <https://www.cloudflare.com/learning/security/what-is-web-application-security/>`_

Basic WAF workflow
******************

* **Defining the 'interfaces'**

  * Ways the users should be able to interact with this specific application
  * Defining the way users are allowed to interact with those 'interfaces'
  * Keeping track of APIs
  * Only allowing requests that match legitimate use-cases

* **Validating and scanning all requests**, the users are allow to perform, with attack-detection engines

* **Gathering information** about all requests and **analyzing it**

  * Detecting schemes in this information
  * Updating the WAF engine/ruleset as needed

  |waf_dev_flow|

----

Self Hosted
###########

As a WAF has access to all information that passes through it, including sensitive user data, it might not be acceptable for your company or project to have it hosted by a third party.

Some enterprise-grade solutions may get expensive, but you can always start-out with an Open-Source community product like :ref:`HAProxy <proxy_reverse_haproxy>` and upgrade later on.

I may be more work to get to a finished WAF setup, but you have

----

Cloud Hosted
############

Cloud hosted WAF providers like `Cloudflare <https://www.cloudflare.com/lp/ppc/waf-x/>`_ or `Barracuda <https://de.barracuda.com/products/application-protection/web-application-firewall>`_ have many functionalities and are able to provide you with state-of-the-art protection.

Providers like these have allocated many resources to continuously develop their systems. They can even provide you with engines to block Zero-Day exploits, that you cannot patch yet.

In that case it may make sense to also use other services from this provider, like a `CDN <https://www.cloudflare.com/de-de/lp/ppc/cdn-x>`_.

----

Self Developed Solutions
########################

If you are a developer, you might ask yourself 'Why not just extend my codebase to include Security checks?'. This is a justified question.

In practise it is recommended to decouple the WAF from your application. This has some legitimate reasons:

* **Expertise**

  In such cases I always remember the sentence: :code:`Never implement your own encryption algorithm. You might think its safe - but I can assure you - it's not!` (`from Cryptography Lectures <https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX>`_)

  WAF solutions have staff that is specialized in developing for this use-case.

  Your developers might know about `OWASP <https://www.cloudflare.com/learning/security/threats/owasp-top-10/>`_ and have good experience developing secure code, but a WAF has to have a broad toolset like (at least) :code:`DDOS protection`, :code:`Detect and Block common attacks via SQLi/XSS/CSRF/SSRF/...`, :code:`Blocking by IP and ASN/ISP` and :code:`Bot detection and handling`.

  You need to have a really good argument to invest a large amount of development time. And be aware that these systems need to be maintained.

  If you really need to do so - at least decouple this service from your application.

* **Complexity**

  Your app might get a lot more complex if you add these layers of protection.

* **Abstraction**

  WAFs, like common (network) firewalls, should be a dedicated service that is place in front of your applications service.

  This makes troubleshooting much easier and helps when you need to scale your infrastructure.

* **Performance**

  Most WAF systems run on C, Rust, Golang or some other fast/low-level programming language.

  If you implement all of this logic in Python, PHP, Javascript or some other high-level language, you might see much worse performance.

* **Support**

  If you use an existing solution, you can easily get support for it from third parties.

  Not so if it's your own codebase.

Not to say that you should not implement ANY security checks in your application! You should. But as mentioned above - a WAF is more than a few security checks. It really is a **firewall**!

.. include:: ../_include/user_rath.rst
