---
title: "Monitor your databases with Open Source tools like PMM"
date: "2023-03-06T00:00:00+00:00"
draft: false
tags: ["Monitor", "PMM", "Databases", "Open Source"]
categories: ["PMM"]
authors:
  - edith_puclla
images:
  - blog/2023/03/00-moni-cover.jpg
slug: monitor-your-databases-with-open-source-tools-like-pmm
---

In this post, we will cover the value of database monitoring and how we can use Open Source tools like **PMM** [Percona Monitoring and Management](https://www.percona.com/software/database-tools/percona-monitoring-and-management) to monitor and manage databases effectively.

## Why should I care about database monitoring?

Once you have passed the installation and configuration of your databases and it is well underway, you have to start monitoring it, and not only the database but the elements related to it.

Questions like these will begin to arise:

- Is my database performing well?

  - Are query response times consistently slow?

- Is my database available and accepting connections?

  - Connections to the database close to the maximum limit

- Is my system stable?

  - How about CPU, memory, and disk?

- Am I experiencing avoidable downtime?
  - Hardware failures, network outages.

* Am I experiencing data loss?
  - Disk crashes
  - Human errors
* Am I minimizing performance issues that can impact my business?
* Can I quickly identify and resolve issues before they become more significant problems?

To answer these questions, you will need to find tools that let you keep your database monitored, and you can opt for free tools for monitoring. **PMM** is one of them, which is entirely open source.

## Percona Monitoring and Management (PMM)

**PMM** is an open source database observability, monitoring, and management tool for:

- MySQL
- MariaDB
- PostgreSQL
- MongoDB
- And others

It can also help to improve the performance of your databases, simplify their management and strengthen their security.

**PMM** is built on top of open source software

- Grafana
- VictoriaMetrics/Prometheus
- ClickHouse
- PostgreSQL
- Docker

## PMM Interface

There are three levels of depth:

- Dashboards
- Graphs
- Metrics

![Interface](/blog/2023/03/01-interface.jpg)

## Metrics & Database Monitoring

Important database metrics you should monitor:

- It will depend on your specific database and use case
- Monitor the metrics that are relevant to your database and your business
- You should have alerts and monitoring processes to ensure you are aware of any problems as they occur or before

Some important metrics that could indicate potential database issues:

- Query performance
- High CPU utilization
- High Memory usage
- High Disk I/O
- User Connection
- Data growth
- Others

Let’s analyze each of them, and they will also answer your questions at the beginning.

### Long Query Response Times

**PMM** helps you monitor the performance of individual queries and identify slow-performing queries that need to be optimized.
We can use [Query Analytics in PMM](https://docs.percona.com/percona-monitoring-and-management/get-started/query-analytics.html) to visualize all the queries running in our database; we can inspect each of them and see which is the one sending more queries per second and much longer it takes to execute it. Also, **PMM** will show you suggestions to fix or improve queries.

![Long query Response](/blog/2023/03/02-long-query-response.jpg)

### High CPU Utilization

**PMM** helps you monitor the number of [CPU resources](https://docs.percona.com/percona-monitoring-and-management/details/dashboards/dashboard-cpu-utilization-details.html) the database uses and identify performance bottlenecks.

In the section on CPU utilization, you will see how much of your CPU is being used in a period of time. This is very useful when you need to increase your resources.

![High Cpu Utilization](/blog/2023/03/03-high-cpu-utilization.jpg)

### High Memory usage

**PMM** helps you [monitor the amount of memory](https://docs.percona.com/percona-monitoring-and-management/details/dashboards/dashboard-memory-details.html) being used by the database and determine if you need to add more memory or optimize your database configuration.

![High Memory Usage](/blog/2023/03/04-high-memory-usage.jpg)

### Disk I/O

PMM helps you monitor the number of [disk I/O operations](https://docs.percona.com/percona-monitoring-and-management/details/dashboards/dashboard-disk-details.html) performed by the database and identify any potential performance bottlenecks. See here the panel of Disk IO Latency!

![Disk Io](/blog/2023/03/05-disk-io.jpg)

### User connections

**PMM** helps you monitor the number of [active database connections](https://docs.percona.com/percona-monitoring-and-management/details/dashboards/dashboard-mysql-user-details.html) and determine if your user connection is sized appropriately. If you limit the number of users that should connect to your database, this panel will show you when you are reaching that limit so that you can increase the number.

![User Conexion](/blog/2023/03/06-user-conexion.jpg)

### Data growth

PMM helps you monitor [your database growth](https://docs.percona.com/percona-monitoring-and-management/details/dashboards/dashboard-mysql-table-details.html) over time and plan for capacity and performance needs. This dashboard helps to see the time period in which your database is growing and to be able to learn about performance issues or issues as they occur.

![Data Grown](/blog/2023/03/07-data-grown.jpg)

### Summary

We see the importance of monitoring databases and how to explore PMM for some essential metrics to detect issues and prevent them on time.

Want to try PMM? We have a [test environment to try PMM](https://pmmdemo.percona.com/graph/) without having to install it first. Feel free to play with it and see how PMM works. If you like it, you can [install PMM quickly and start using it in your own environment](https://www.percona.com/software/pmm/quickstart).
