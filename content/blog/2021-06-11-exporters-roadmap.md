---
title: "Exporters Roadmap"
date: "2021-06-11T00:00:00+00:00"
authors:
  - andrii_skomorokhov
images:
  - blog/2021/06/pmm-exporters.jpg
slug: exporters-roadmap
---


## Exporters Roadmap

### Goals

Prometheus exports as a part of  PMM are a big and valuable component.

According to the goal to involve open source contributors to contribute to PMM and Percona to contribute to open source.  As the main focus, it was decided to start from the exporter.

For now PMM use the next exporters:

1. https://github.com/percona/node_exporter 
2. https://github.com/percona/mysqld_exporter 
3. https://github.com/percona/mongodb_exporter 
4. https://github.com/percona/postgres_exporter 
5. https://github.com/Percona-Lab/clickhouse_exporter 
6. https://github.com/percona/proxysql_exporter 
7. https://github.com/percona/rds_exporter 
8. https://github.com/percona/azure_metrics_exporter 


### Groups

We can split them into three groups.

**The first group** is exporters that are created by Percona or Percona contribution in its fork is so big  - that it cannot be pushed back upstream. 

1. https://github.com/percona/mongodb_exporter -  built by Percona from scratch.
2. https://github.com/percona/proxysql_exporter - built by Percona from scratch.
3. https://github.com/percona/rds_exporter - too far from upstream - Percona made a big contribution to fit it for PMM needs.

For those three exporters we are going to:
 - encourage contribution from the community;
 - create an easy setup dev environment to speed up development and testing;
 - consider user’s issues and request - and try to solve this with “community priority” level;
 - create regular releases with needed binaries for community consumption.


**The second group** is exporters that are not that far away from upstream and Percona would like to contribute back as much as possible.

1. https://github.com/percona/node_exporter
2. https://github.com/percona/mysqld_exporter
3. https://github.com/percona/postgres_exporter

For this group, we will try to push all fixes made by Percona to Upstream and are going to take part in development and bug fixing as open-source contributors - trying to bring value for the community as well as for PMM.

And **the third group** are exporters that currently fit PMM needs and Percona did not contribute a lot in its forks.

1. https://github.com/Percona-Lab/clickhouse_exporter
2. https://github.com/percona/azure_metrics_exporter

For those exporters, we are going to start using upstream and make changes if needed in other PMM components. Downstream repos would only be used as forks synced with upstream only for the PMM build support.

### Action plan

Here is some short term plan of tasks to implement a part of the plan above:

1. Remove fork of clickhouse_exporter and remove it as component from PMM - looks like the easiest task. The new version of the ClickHouse server exposes metrics in Prometheus format, so we can collect them without any exporters. (we can use build-in metrics exporter https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-prometheus starting from https://clickhouse.tech/docs/en/whats-new/changelog/2020/#clickhouse-release-v20-1-2-4-2020-01-22)

2. Discard our changes in azure_metrics_exporter and keep the fork in sync with upstream. We use common formulas in Grafana to visualize metrics from different exporters. Current azure_exporter has slightly different a few metric names - we can achieve the same by renaming using Prometheus recording rules https://prometheus.io/docs/prometheus/latest/configuration/recording_rules . This discard needs to keep the fork up to date with upstream.

3. Node exporter looks like the best candidate to contribute back to the community https://github.com/prometheus/node_exporter/compare/master...percona:main. This exporter’s source code did not go far away - so we can leverage what we can accept from upstream and create minimal PR to upstream with features we only required.

4. MySQL exporter can be the heaviest task to push back to upstream - we did a lot of change. So the tactic could be split difference into logical parts and try to push back it step by step https://github.com/percona/mysqld_exporter/pull/61/files.

5. PostgreSQL exporter is also quite far from upstream plus it requires a few fundamental improvements like a handle DB connection, etc. For this exporter, we also need split difference on logical parts and contribute it with small PR back to upstream https://github.com/percona/postgres_exporter/pull/28/files.

6. Maintain mongodb_exporter, add needed packaging, docker container and update helm chart.

7. Proxy exporter looks good for now, but we need to take into consideration that ProxySQL start exports metrics natively https://proxysql.com/documentation/prometheus-exporter.

8. And RDS exporter goes to be separated from upstream - now it contains a big part of code that serve mostly PMM needs.

For all the above we would try to use the GitHub Project board https://github.com/orgs/percona/projects/2 to track progress in different repositories for all mentioned tasks above.

We would sync with the community during Engineering Monthly Meeting https://percona.community/contribute/engineeringmeetings/  as well as by participating in Upstream meetings.

Come and join us on our journey in OpenSource! Contact us in [per.co.na/discord](per.co.na/discord).
