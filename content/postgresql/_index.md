---
title: "PostgreSQL"
description: "Run Percona: Embrace Open with Percona Distribution for PostgreSQL"
images:
- postgresql-graphic.png
---

{{% typography %}}

PostgreSQL is the reliable, open source relational database used by many enterprise-level database variants as their base. Percona Distribution for PostgreSQL combines several components into an enterprise-level distribution for PostgreSQL that you can download for free.

{{% downloadbutton "https://www.percona.com/downloads/postgresql-distribution-13/LATEST/" %}}
Download Percona Distribution for PostgreSQL
{{% /downloadbutton %}}

## What is included in Percona Distribution for PostgreSQL?

Percona Distribution for PostgreSQL is a single source installation providing enterprise-grade, open source PostgreSQL. It includes the following components:

* [PostgreSQL Core](https://www.postgresql.org/)
* [pg_repack](https://github.com/reorg/pg_repack) (allows for altering tables in order to reclaim free space, reduce IO, improve performance, and more)
* [pgaudit](https://www.pgaudit.org/) (for all your PostgreSQL auditing needs, including the monitoring of superuser actions)
* [pgBackRest](https://pgbackrest.org/) (backup and restore solution)
* [Patroni](https://github.com/zalando/patroni) (template for HA PostgreSQL solutions)
* [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Percona's query performance monitoring tool providing insightful information based on and extending pg_stat_statements)

![Percona Distribution for PostgreSQL features illustration](postgresql-graphic.png)

{{% /typography %}}