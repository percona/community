---
title: 'Percona Live Europe Tutorial: Query Optimization and TLS at Large Scale'
date: Mon, 15 Oct 2018 14:05:06 +0000
draft: false
tags: ['Events', 'MariaDB', 'MySQL', 'Open Source Databases', 'Percona Live Europe 2018']
images:
  - blog/2018/10/MySQL-at-scale.jpg
authors:
  - jaime_crespo
slug: percona-live-europe-tutorial-query-optimization-workshop-tls-large-scale-session
---

[![MySQL has many ways to provide scalability, but can it provide it while at the same time guarantee perfect privacy? Learn it at my tutorial!](blog/2018/10/MySQL-at-scale.jpg)](https://www.percona.com/live/e18/sessions/tls-for-mysql-at-large-scale) For Percona Live Europe this year, [I got accepted](https://www.percona.com/live/e18/speaker/jaime-crespo) a workshop on query optimization and a 50-minute talk covering TLS for MySQL at Large Scale, talking about our experiences at the [Wikimedia Foundation](https://wikimediafoundation.org/).

### Workshop

The 3-hour workshop on Monday, titled [_**Query Optimization with MySQL 8.0 and MariaDB 10.3: The Basics**_](https://www.percona.com/live/e18/sessions/query-optimization-with-mysql-80-and-mariadb-103-the-basics) is a beginners' tutorial–though dense in content. It's for people who are more familiar with database storage systems other than InnoDB for MySQL, MariaDB or Percona Server. Or who, already familiar with them, are suffering performance and scaling issues with their SQL queries. If you get confused with the output of basic commands like EXPLAIN and SHOW STATUS and want to learn some SQL-level optimizations, such as creating the right indexes or altering the schema to get the most out of the performance of your database server, then you want to attend this tutorial before going into more advanced topics. Even veteran DBAs and developers may learn one or two new tricks, only available on the latest server versions! 

Something that people may enjoy is that, during the tutorial, every attendee will be able to throw queries to a real-time copy of the Wikipedia database servers—or setup their own offline Wikipedia copy in their laptop. They'll get practice by themselves what is being explained—so it will be fully hands-on. I like my sessions to be interactive, so all attendees should get ready to answer questions and think through the proposed problems by themselves!

### Fifty minutes talk

My 50 minute talk [_**TLS for MySQL at Large Scale**_](https://www.percona.com/live/e18/sessions/tls-for-mysql-at-large-scale) will be a bit more advanced, although maybe more attractive to users of other database technologies. On Tuesday, I will tell the tale of the mistakes and lessons learned while deploying encryption (TLS/SSL) for the replication, administration, and client connections of our databases. At the Wikimedia Foundation we take very seriously the privacy of our users—Wikipedia readers, project contributors, data reusers and every members of our community—and while none of our databases are publicly reachable, our aim is to encrypt every single connection between servers, even within our datacenters. 

However, when people talk about security topics, most of the time they are trying to show off the good parts of their set up, while hiding the ugly parts. Or maybe they are too theoretical to actually learn something. My focus will not be on the security principles everybody should follow, but on the pure operational problems, and the solutions we needed to deploy, as well what we would have done differently if we had known, while deploying TLS on our 200+ MariaDB server pool.

### Looking forward...

For me, as an attendee, I always look forward to the [ProxySQL sessions](https://www.percona.com/live/e18/speaker/ren-canna), as it is something we are currently deploying in our production. Also, I want to know more about the maturity and roadmap of the newest [MySQL](https://www.percona.com/live/e18/sessions/mysql-80-performance-scalability-benchmarks) and [MariaDB](https://www.percona.com/live/e18/sessions/whats-new-in-and-around-mariadb-server-103) releases, as they keep adding new interesting features we need, as well as cluster technologies such as Galera and [InnoDB Cluster](https://www.percona.com/live/e18/sessions/the-latest-mysql-replication-features). I like, too, to talk with people developing and using other technologies outside of my stack, and you never know when they will fill in a need we have ([analytics](https://www.percona.com/live/e18/sessions/clickhouse-at-messagebird-analysing-billions-of-events-in-real-time), [compression](https://www.percona.com/live/e18/sessions/myrocks-production-case-studies-at-facebook), [NoSQL](https://www.percona.com/live/e18/sessions/sharedrocks-a-scalable-master-slave-replication-with-rocksdb-and-shared-file-storage), etc.). 

But above all, the thing I enjoy the most is the networking—being able to talk with professionals that suffer the same problems that I do is something I normally cannot do, and that I enjoy doing a lot during Percona Live. [caption id="attachment_390" align="alignright" width="808"]

![Jaime Crespo](blog/2018/10/jaime_crespo_2018.jpeg) 

_Jaime Crespo in a Percona Live T-Shirt - why not come to this year's event and start YOUR collection._ \[/caption\]