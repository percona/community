---
title: 'Percona Live ONLINE Talk: Optimize and Troubleshoot MySQL using Percona Monitoring and Management by Peter Zaitsev'
date: Tue, 23 Jun 2020 15:09:57 +0000
draft: false
tags: ['Mayank Sharma', 'DevOps', 'MariaDB', 'Monitoring', 'MySQL', 'MySQL', 'mysql-and-variants', 'Open Source Databases', 'Percona Monitoring and Management', 'PMM', 'Tools']
images:
  - blog/2020/06/SC-3-Matt-Percona.jpg
authors:
  - mayank_sharma
---

Incorporating a database in an organization is a complicated task that involves a lot of people besides the DBAs. This is something that Peter Zaitsev, co-founder and CEO of Percona, understands very well. 

In the build-up to his hands-on presentation with the open source [Percona Monitoring and Management](https://www.percona.com/software/database-tools/percona-monitoring-and-management) (PMM) platform, Peter spoke about how inducting a database in an organization is a constant tussle between the developers, the management and the DBAs. While the developers want a solution that just works, the managers don't want the database to break the bank: “The DBAs just want to make sure they don’t spend too much time keeping them both happy,” he shared. 

This is why, Peter argues, DBAs want to make sure the databases in their realm are optimized for performance. Like security, performance optimization is an on-going process that begins during development and continues into the production environment as well.

Cover all bases
---------------

Based on his experience, Peter talked about the two factors that impact the performance of a database. On the one hand, you have applications that are responsible for the volume and type of queries they generate. If an application sends an unoptimized query it can put the database under unnecessary strain. On the other hand, you have hardware resources that when stretched to the limit can even delay the simplest of queries. 

Peter pointed out that PMM takes both these aspects into consideration, before launching into his hands-on demo of the latest version of the platform, PMM 2. He began with an overview of the new features in the release particularly its ability to look at groups of servers instead of a single server, something that Peter refers to as “treating the servers as a herd and not as pets”. 

He began the demo with the Query Analytics dashboard that shows all the database queries running across all deployed servers. He ran through the various metrics on which DBAs can sort the queries to get different kinds of results, such as the list of queries that run most frequently or the queries that take the longest to complete. 

As looking at averages doesn’t usually make a lot of sense for performance optimization, Peter demonstrated how you can use PMM 2 to drill down to particular problematic queries. He used the platform to pinpoint a particular inefficient query that was returning one row on average, but only after scanning about 100,000 rows leading to degradation in performance.

A 360-degree view
-----------------

He also demonstrated how DBAs can visualize the performance of the database using different parameters. For instance, you can sort it by users, which is particularly useful if you’ve followed the good practice of configuring different apps to run with different users. Viewing loads by users will help you identify the applications that are consuming the most resources. 

Next, he headed to the Node Summary dashboard, which is useful for observing the usage of the hardware resources on the servers. This dashboard tracks several additional parameters that help DBAs make more sense of the resource usage. For instance, instead of just CPU usage, you’re also able to see CPU saturation and max core utilization. The latter is particularly useful since single queries in MySQL can only execute on one CPU core. Peter showed how you can use this dashboard to make sure your multi-core CPU is being used efficiently. 

He ran through similar examples with memory utilization and Disk IO throughput, both of which display additional parameters to help you ensure the concerned resource is being used efficiently. He also demonstrated the MySQL Instance summary dashboard that displays various information about the MySQL servers as well as the InnoDB Details dashboard, which visualizes all kinds of InnoDB activity and is useful for identifying and diagnosing bottlenecks. One metric that Peter pointed out was InnoDB pending IOs, which can be very valuable for weeding out storage bottlenecks, especially when using cloud storage.

Advanced usage
--------------

One of the interesting features of PMM 2 is that you can ask it to [use ClickHouse](https://www.percona.com/blog/2020/03/30/advanced-query-analysis-in-percona-monitoring-and-management-with-direct-clickhouse-access/) to store query performance data. Peter demoed how you can access ClickHouse on PMM 2 and showed off a dashboard he built on top that isn’t yet part of the platform but promised to share it publicly soon. 

PMM 2 is [powered by Grafana](https://www.percona.com/blog/2019/11/22/designing-grafana-dashboards/) and Peter rounded up the presentation by sharing some interesting tips and tricks for using Grafana, such as ad-hoc filtering, which you can use to filter a dashboard by any of the defined clauses. For instance, Peter showed how you can use it to look at all the queries that send a maximum of ten rows. 

One of the new additions in PMM 2 is the Security Threat tool and Peter briefly ran through this during his demonstration. The tool runs daily checks for common database security issues and flags any non-compliance. 

Fielding questions, Peter clarified that while he focussed on MySQL, PMM 2 supports MariaDB as well. PMM monitoring doesn’t add much overhead and at the end of the day will surely help you save a lot more resources than it consumes. 

You can [watch Peter’s presentation](https://www.percona.com/resources/videos/optimize-and-troubleshoot-mysql-using-pmm-2-peter-zaitsev-percona-live-online-2020) and follow along on the publicly accessible [PMM 2 demo server](https://pmmdemo.percona.com/).