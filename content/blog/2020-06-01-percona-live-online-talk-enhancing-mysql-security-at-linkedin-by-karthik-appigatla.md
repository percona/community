---
title: 'Percona Live ONLINE Talk: Enhancing MySQL security at LinkedIn by Karthik Appigatla'
date: Mon, 01 Jun 2020 08:01:24 +0000
draft: false
tags: ['Mayank Sharma', 'MySQL', 'mysql-and-variants', 'Open Source Databases', 'security', 'SRE', 'Tools']
images:
  - blog/2020/06/SC-3-Matt-Percona.jpg
authors:
  - mayank_sharma
slug: percona-live-online-talk-enhancing-mysql-security-at-linkedin-by-karthik-appigatla
---

MySQL, arguably the most popular relational database, is used pretty extensively at the popular professional social network LinkedIn. At Percona Live ONLINE 2020, the company’s flagship event held online for the first time due to the Covid-19 pandemic, Karthik Appigatla from LinkedIN’s database SRE team discussed the company’s approach to securing their database deployment without introducing operational hiccups or adversely affecting performance. 

Instead of just performing admin duties, Karthik’s team builds automated tools to scale their infrastructure, and he talked about some of these tailored tools in his presentation. The database SREs on his team also work with the developers at LinkedIn and help them streamline their applications to make best use of the database. 

Talking about LinkedIn’s reliance on MySQL, Karthik said that not only do all their infrastructural tools rely on MySQL, many of the internal applications use MySQL as their backend datastore, and so do a few of the website facing applications as well.

Database proliferation
----------------------

The magnitude of the MySQL deployment at LinkedIn is pretty impressive. Thanks to the sheer number of microservices, each of which gets its own database, Karthik’s team looks after more than 2300 databases. These are powered by different versions of the MySQL server, namely v5.6, v5.7 and v8.0, all of which are hosted atop RHEL 7 installations. 

As he ran through the layout of the MySQL deployments at LinkedIn, Karthik mentioned that they have a multi-tenant architecture where multiple databases are hosted on a single MySQL server instance. 

MySQL is consumed as-a-service at LinkedIn and all the administrative tasks like backups, bootstrapping clusters, monitoring, and such are handled by automated systems built by Karthik’s team. He said that the level of automation is so high in fact that application owners can actually provision a database for their applications with just a few mouse clicks.

Shared responsibility
---------------------

Given their scale of deployment, the developers at LinkedIn give special credence to the security of their databases. Karthik believes “security is a shared responsibility between the database SRE team and the application owners.” 

He illustrated how the databases are provisioned, from a security point of view and gave several security insights in his presentation based on his experience. For one, his team doesn't take the easy approach of isolating databases by running multiple mysqld processes. This approach doesn’t scale well since the overhead on the server increases linearly as the number of databases it hosts increases. 

His description of how the various applications access different databases on the different servers was also pretty insightful for anyone looking to deploy databases at scale. One of the peculiar issues he described is that various components inside individual applications usually need to access different databases simultaneously. His team handled this by employing multiple user accounts with varying privileges.

Access control
--------------

He dwelled on this some more and spent some time explaining the different access management controls they’ve built into the system to facilitate access. One of the interesting security measures he talked about is how they limit the number of hosts that can access a database by adopting an IP-based grants system, which is slightly cumbersome to implement but a lot more secure. 

Also interesting is their approach to granting SSH access to the database servers to the SREs. Instead of the default public-key authentication, his team uses a certificate-based authentication scheme, and Karthik presented a high-level overview of this arrangement. 

Auditing and monitoring are also important aspects of security. At LinkedIn, the logins are audited by the [Percona Audit Log plugin](https://www.percona.com/doc/percona-server/LATEST/management/audit_log_plugin.html%E2%80%9D), while the queries go through LinkedIN’s home-brewed Query Analyser agent. Karthik ran through the architecture of their Query Analyser agent, which LinkedIn plans to release under an open source license soon. 

Perhaps one of the biggest takeaways from the presentation was Karthik’s insight into the operational challenges that crop up due to their rather stringent security requirements, particularly their IP-based grants system. While the solutions he discussed were specific to LinkedIn, his presentation was peppered with tips and tricks that you can easily adapt for your deployments. 

[Click here to watch](https://www.percona.com/resources/videos/enhancing-mysql-security-linkedin-karthik-appigatla-percona-live-online-2020) Karthik’s presentation at Percona Live ONLINE 2020.