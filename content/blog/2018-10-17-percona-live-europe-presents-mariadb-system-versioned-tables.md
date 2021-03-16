---
title: 'Percona Live Europe Presents: MariaDB System-Versioned Tables'
date: Wed, 17 Oct 2018 16:14:38 +0000
draft: false
tags: ['author_federico', 'Events', 'MariaDB', 'MySQL', 'Percona Live Europe 2018']
images:
  - blog/2018/10/PLE-Frankfurt-Logo.png
authors:
  - federico_razzoli
---

![PLE Frankfurt Logo](blog/2018/10/PLE-Frankfurt-Logo.png)

System-versioned tables, or temporal tables, are a typical feature of proprietary database management systems like DB2, Oracle and SQL Server. They also appeared at some point in PostgreSQL, but only as an extension; and also in CockroachDB, but in a somewhat limited fashion. 

The MariaDB® implementation is the first appearance of temporal tables in the MySQL ecosystem, and the most complete implementation in the open source world. 

[My presentation](https://www.percona.com/live/e18/sessions/mariadb-system-versioned-tables) will be useful for **analysts**, and some **managers**, who will definitely benefit from learning how to use temporal tables. Statistics about how data evolves over time is an important part of their job. This feature will allow them to query data as it was at a certain point in time. Or to query how data changed over a period, including rows that were added, deleted or modified. 

**Developers** will also find this feature useful, if they deal with data versioning or auditing. Recording the evolution of data into a database is not easy - several solutions are possible, but none is perfect. Streaming data changes to some event-based technology is also complex, and sometimes it’s simply a waste of resources. System-versioned tables are a good solution for many use cases. 

And of course, **DBA’s**. Those guys will need to know what this feature is about, suggest it when appropriate, and maintain it in production systems. 

More generally, many people are interested in understanding MariaDB's unique features, as well as its MySQL ones. Their approach allows them to choose “the right tool for the right purpose”.

#### What I'm looking forward to...

![federico razzoli](blog/2018/10/federico-razzoli.jpg)

I am excited about Percona Live agenda. A session that I definitely want to attend is **[MySQL Replication Crash Safety](https://www.percona.com/live/e18/sessions/demystifying-mysql-replication-crash-safety)**. I find extremely useful and interesting the talks about technology limitations and flaws. Jean-François has a long series of writings on MySQL replication and crash-safety, and I have questions for him. 

I also like the evolution that PMM and its components had over the years. I want to understand how to use them at best in my new job, so I am glad to see that there will be several sessions on the topic. I plan to attend some sessions about PMM and Prometheus. 

**[Performance Analyses Technologies for Databases](https://www.percona.com/live/e18/sessions/performance-analyses-technologies-for-databases)** makes me think to the cases when I saw a technology evaluated in an inappropriate way, and the talks I had with people impressed by some blog posts showing impressive benchmarks which didn't fully understand. I will definitely attend. 

And finally, I plan to learn something about **[ClickHouse](https://www.percona.com/live/e18/sessions/advanced-features-of-clickhouse)**, [**MyRocks**](https://www.percona.com/live/e18/sessions/myrocks-production-case-studies-at-facebook) and [**TiDB**](https://www.percona.com/live/e18/sessions/tidb-distributed-horizontally-scalable-mysql-compatible). 

See you there!