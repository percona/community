---
title: "PMM - Percona Monitoring and Management"
description: "PMM - Percona Monitoring and Management for database observability"
---

Percona Monitoring and Management (PMM) has a [demo website](https://pmmdemo.percona.com/graph/) which allows you to quickly check out what it's all about. If you prefer text instead, here's quick list of what you can do with PMM:

* Query Analytics (intuitive interface enabling you to quickly analyze and optimize your queries)
* Metrics Monitor (historical view of metrics that are critical to your database server)
* Security Threat Tool (quickly find and fix common data security issues across all your open source databases)
* *...and much more*

If you've checked out the demo and are ready to give it a try, you can read more about how to set it up in our [installation documentation](https://www.percona.com/software/pmm/quickstart).

[![PMM stylistic screenshot illustration](grafana-dashboard.svg)](https://pmmdemo.percona.com/graph/)

## Which databases can PMM monitor?

PMM is fully open source. That means you can not only contribute to the software itself but also create tooling around it. We have created the following exporters to provide metrics to PMM:

* MongoDB Exporter
* MySQL Server Exporter
* Node Exporter
* ProxySQL Server Exporter
* Amazon RDS Exporter

For more details, please refer to our [Architecture](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html).

If you're interested in contributing, please check out our page on [contributing](/contribute) as well as the [main PMM repository](https://github.com/percona/pmm) that also lists all our exporter repositories.

