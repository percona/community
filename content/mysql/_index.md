---
title: "MySQL"
description: "Run Percona: Embrace Open with Percona Distribution for MySQL"
---

{{% typography %}}

The Percona distributions for MySQL come in two flavors - one is based on MySQL and one is based on [XtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster). Percona XtraDB Cluster ensures maximum availability with stability and synchronous replication - while being and staying open source.

## When do I need the Percona Distribution for MySQL and when the Distribution with XtraDB Cluster?

For single node source/replica deployments or high availability through group replication in your typical MySQL environment, Percona Distribution for MySQL is the standard choice. If you're looking for high availability through Galera, the Percona Distribution based on [XtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster) will be your download of choice.

{{% grid size=2 %}}
{{% griditem %}}
{{% downloadbutton "https://www.percona.com/downloads/percona-distribution-mysql-ps/LATEST/" %}}
Download Percona Distribution for MySQL
{{% /downloadbutton %}}
{{% /griditem %}}
{{% griditem %}}
{{% downloadbutton "https://www.percona.com/downloads/percona-distribution-mysql-pxc/LATEST/#" %}}
Download Percona Distribution (XtraDB Cluster)
{{% /downloadbutton %}}
{{% /griditem %}}
{{% /grid %}}

## Which components are included in the Percona Distribution for MySQL?

The Percona Distribution for MySQL contains **either MySQL or XtraDB Cluster** (depending on your choice of download) as well as the following:

* [Percona XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) (your open source complete database backup solution for all versions of Percona Server for MySQL as well as MySQL)
* [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit) (a set of scripts to simplify and optimize database operations)
* Orchestrator (the replication topology manager for Percona Server for MySQL)
* HAProxy (the default high availability, load-balancing solution for Percona XtraDB Cluster)
* ProxySQL (a high performance, high availability protocol-aware proxy for Percona XtraDB Cluster)
* MySQL Shell (an advanced client and code editor for MySQL Server)
* MySQL Router (a lightweight middleware that provides transparent routing between your application and back-end MySQL Servers)

![Percona Distribution for MySQL features illustration](mysql-graphic.png)

{{% /typography %}}