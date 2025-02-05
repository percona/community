---
title: "Release Roundup April 2, 2024"
date: "2024-04-02T00:00:00+00:00"
tags: ['Percona', 'opensource', 'XtraBackup', 'MongoDB', 'MySQL', 'PMM', 'releases']
categories: ['MongoDB', 'MySQL', 'PMM']
description: "Percona software releases and updates March 18 - April 2, 2024."
authors:
  - david_quilty
images:
  - blog/2024/04/Roundup-April-2.jpg
---

*Percona software releases and updates March 18 - April 2, 2024.*

Percona is a leading provider of unbiased, performance-first, open source database solutions that allow organizations to easily, securely, and affordably maintain business agility, minimize risks, and stay competitive, free from vendor lock-in. Percona software is designed for peak performance, uncompromised security, limitless scalability, and disaster-proofed availability.

Our Release Roundups showcase the latest Percona software updates, tools, and features to help you manage and deploy our software. It offers highlights, critical information, links to the full release notes, and direct links to the software or service itself to download.

Today's post includes those releases and updates that have come out since March 18, 2024. Take a look.

## Percona Monitoring and Management 2.41.2

[Percona Monitoring and Management 2.41.2](https://docs.percona.com/percona-monitoring-and-management/release-notes/2.41.2.html) was released on March 22, 2024. It is an open source database monitoring, management, and observability solution for MySQL, PostgreSQL, and MongoDB. Starting with PMM 2.41.2, we now offer pmm-client packages for the latest version of Debian. You can install these packages by following the instructions in our documentation. We have also added several experimental dashboards, which are subject to change and recommended for testing purposes only.

[Download Percona Monitoring and Management 2.41.2](https://www.percona.com/software/database-tools/percona-monitoring-and-management)

## Percona Operator for MySQL based on Percona Server for MySQL 0.7.0

[Percona Operator for MySQL based on Percona Server for MySQL 0.7.0](https://docs.percona.com/percona-operator-for-mysql/ps/ReleaseNotes/Kubernetes-Operator-for-PS-RN0.7.0.html) was released on March 25, 2024. Percona Operator for MySQL allows users to deploy MySQL clusters with both asynchronous and group replication topology. This release includes various stability improvements and bug fixes, getting the Operator closer to the General Availability stage. Version 0.7.0 of the Percona Operator for MySQL is still a tech preview release and it is not recommended for production environments.

[Download Percona Operator for MySQL based on Percona Server for MySQL 0.7.0](https://www.percona.com/mysql/software/percona-operator-for-mysql)

## Percona XtraBackup 8.3.0-1

[Percona XtraBackup 8.3.0-1](https://docs.percona.com/percona-xtrabackup/innovation-release/release-notes/8.3.0-1.html) was released on March 26, 2024. Percona XtraBackup 8.3.0-1 is based on MySQL 8.3 and fully supports the Percona Server for MySQL 8.3 Innovation series and the MySQL 8.3 Innovation series. This release allows taking backups of Percona Server 8.3.0-1 and MySQL 8.3. This Innovation release is only supported for a short time and is designed to be used in an environment with fast upgrade cycles. Developers and DBAs are exposed to the latest features and improvements. Patches and security fixes are included in the next Innovation release instead of a patch release or fix release within an Innovation release. To keep your environment current with the latest patches or security fixes, upgrade to the latest release.

[Download Percona XtraBackup 8.3.0-1](https://www.percona.com/mysql/software/percona-xtrabackup)

## Percona Distribution for MongoDB 6.0.14

[Percona Distribution for MongoDB 6.0.14](https://docs.percona.com/percona-distribution-for-mongodb/6.0/release-notes-v6.0.14.html) was released on March 26, 2024. It is a freely available MongoDB database alternative, giving you a single solution that combines enterprise components from the open source community, designed and tested to work together. Release highlights include:

-   Fixed the issue with missing peer certificate validation if neither CAFile nor clusterCAFile is provided.
-   Fixed the issue with multi-document transactions missing documents when the movePrimary operation runs concurrently by detecting placement conflicts in multi-document transactions.
-   Allow a clustered index scan in a clustered collection if a notablescan option is enabled.
-   Fixed tracking memory usage in SharedBufferFragment to prevent out of memory issues in the WiredTiger storage engine.
-   Added an index on the process field for the `config.locks` collection to ensure update operations on it are completed even in heavy loaded deployments.
-   Fixed the incorrect hardware checksum calculation on zSeries for buffers on stack.

[Download Percona Distribution for MongoDB 6.0.14](https://www.percona.com/mongodb)

## Percona Server for MongoDB 6.0.14-11

[Percona Server for MongoDB 6.0.14-11](https://docs.percona.com/percona-server-for-mongodb/6.0/release_notes/6.0.14-11.html) was released on March 26, 2024. It is an enhanced, source-available, and highly-scalable database that is a fully-compatible, drop-in replacement for MongoDB Community Edition 6.0.14. It is based on MongoDB 6.0.14 Community Edition and includes improvements and bug fixes provided by MongoDB.

[Download Percona Server for MongoDB 6.0.14-11](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

## Percona Backup for MongoDB 2.4.1

On March 25, 2024, [Percona Backup for MongoDB 2.4.1](https://docs.percona.com/percona-backup-mongodb/release-notes/2.4.1.html) was released. It is a distributed, low-impact solution for consistent backups of MongoDB sharded clusters and replica sets. This is a tool for creating consistent backups across a MongoDB sharded cluster (or a non-sharded replica set), and for restoring those backups to a specific point in time.

This release fixes the issue of failing incremental backups. It was caused by the backup metadata document reaching the maximum size limit of 16MB. The issue is fixed by introducing the new approach to handling the metadatada document: it no longer contains the list of backup files which is now stored separately on the storage and is read by PBM on demand. The new metadata handling approach applies to physical, incremental, and snapshot-based backups.

[Download Percona Backup for MongoDB 2.4.1](https://www.percona.com/mongodb/software/percona-backup-for-mongodb)

That's it for this roundup, and be sure to [follow us on Twitter](https://twitter.com/Percona) to stay up-to-date on the most recent releases! Percona is a leader in providing best-of-breed enterprise-class support, consulting, managed services, training, and software for MySQL, MongoDB, PostgreSQL, MariaDB, and other open source databases in on-premises and cloud environments and is trusted by global brands to unify, monitor, manage, secure, and optimize their database environments.