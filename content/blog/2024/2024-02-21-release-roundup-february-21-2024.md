---
title: "Release Roundup February 21, 2024"
date: "2024-02-21T00:00:00+00:00"
tags: ['Percona', 'opensource', 'MySQL', 'MongoDB']
description: "Percona software releases and updates February 5 - February 21, 2024."
authors:
  - david_quilty
images:
  - blog/2024/02/Roundup-Feb-24.jpg
---

*Percona software releases and updates February 5 - February 21, 2024.*

Percona is a leading provider of unbiased, performance-first, open source database solutions that allow organizations to easily, securely, and affordably maintain business agility, minimize risks, and stay competitive, free from vendor lock-in. Percona software is designed for peak performance, uncompromised security, limitless scalability, and disaster-proofed availability.

Our Release Roundups showcase the latest Percona software updates, tools, and features to help you manage and deploy our software. It offers highlights, critical information, links to the full release notes, and direct links to the software or service itself to download.

Today's post includes those releases and updates that have come out since February 5, 2024. Take a look.

## Percona Distribution for MySQL (PS-based variation) 8.2.0

[Percona Distribution for MySQL (PS-based variation) 8.2.0](https://docs.percona.com/percona-distribution-for-mysql/innovation-release/release-notes-ps-8.2.html) was released on February 5, 2024. It is a bundling of open source MySQL software enhanced with carefully curated and designed enterprise-grade features. Percona Distribution for MySQL offers two download options; this one is based on Percona Server for MySQL.

This release merges the MySQL 8.2 code base, introducing several significant changes:

* Removes remains of Percona-specific encryption features (support for custom Percona 5.7 encrypted binlog format).

* Removes the deprecated `rocksdb_strict_collation_check` and `rocksdb_strict_collation_exceptions` RocksDB system variables.

[Download Percona Distribution for MySQL (PS-based variation) 8.2.0](https://www.percona.com/mysql/software)

## Percona Distribution for MongoDB 6.0.13

[Percona Distribution for MongoDB 6.0.13](https://docs.percona.com/percona-distribution-for-mongodb/6.0/release-notes-v6.0.13.html) was released on February 20, 2024. It includes the following components:

* Percona Server for MongoDB is a fully compatible source-available, drop-in replacement for MongoDB.

* Percona Backup for MongoDB is a distributed, low-impact solution for achieving consistent backups of MongoDB sharded clusters and replica sets.

This release of Percona Distribution for MongoDB is based on the production release of [Percona Server for MongoDB 6.0.13-10](https://docs.percona.com/percona-server-for-mongodb/6.0/release_notes/6.0.13-10.html) and [Percona Backup for MongoDB 2.3.1.](https://docs.percona.com/percona-backup-mongodb/release-notes/2.3.1.html)

[Download Percona Distribution for MongoDB 6.0.13](https://www.percona.com/mongodb/software)

## Percona Distribution for MongoDB 4.4.28

[Percona Distribution for MongoDB 4.4.28](https://docs.percona.com/percona-distribution-for-mongodb/4.4/release-notes-v4.4.28.html) was released on February 7, 2024. It's a freely available MongoDB database alternative, giving you a single solution that combines enterprise components from the open source community, designed and tested to work together.  In addition to bug fixes and improvements provided by MongoDB and included in Percona Server for MongoDB, Percona Backup for MongoDB 2.3.1 enhancements include the following:

* Support for Percona Server for MongoDB 7.0.x

* The ability to define custom endpoints when using Microsoft Azure Blob Storage for backups

* Improved PBM Docker image to allow making physical backups with the shared mongodb data volume

* Updated Golang libraries that include fixes for the security vulnerability CVE-2023-39325.

In addition, Percona Server for MongoDB 4.4.28-27 is no longer available on Ubuntu 18.04 (Bionic Beaver).

[Download Percona Distribution for MongoDB 4.4.28](https://www.percona.com/mongodb/software)

## Percona Distribution for MongoDB 4.2.25

On February 8, 2024, [Percona Distribution for MongoDB 4.2.25](https://docs.percona.com/percona-distribution-for-mongodb/4.2/release-notes-v4.2.25.html) was released. Release highlights include:

* Optimized the construction of the balancer’s collection distribution status histogram

* Fixed the query planner logic to distinguish parameterized queries in the presence of a partial index that contains logical expressions ($and, $or).

* Improved performance of updating the routing table and prevented blocking client requests during refresh for clusters with 1 million of chunks.

* Avoided traversing routing table in balancer split chunk policy

* Fixed the issue that caused the modification of the original ChunkMap vector during the chunk migration and that could lead to data loss. The issue affects MongoDB versions 4.4.25, 5.0.21, 6.0.10 through 6.0.11 and 7.0.1 through 7.0.2. Requires stopping all chunk merge activities and restarting all the binaries in the cluster (both mongod and mongos).

[Download Percona Distribution for MongoDB 4.2.25](https://www.percona.com/mongodb/software)

## Percona Server for MongoDB 6.0.13-10

[Percona Server for MongoDB 6.0.13-10](https://docs.percona.com/percona-server-for-mongodb/6.0/release_notes/6.0.13-10.html) was released on February 20, 2024. It is based on MongoDB 6.0.13 Community Edition and supports the upstream protocols and drivers.

Release highlights include:

Percona Server for MongoDB packages are available for ARM64 architectures, enabling users to install it on-premises. The ARM64 packages are available for the following operating systems:
* Ubuntu 20.04 (Focal Fossa)
* Ubuntu 22.04 (Jammy Jellyfish)
* Red Hat Enterprise Linux 8 and compatible derivatives
* Red Hat Enterprise Linux 9 and compatible derivatives

[Download Percona Server for MongoDB 6.0.13-10](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

## Percona Server for MongoDB 4.4.28-27

[Percona Server for MongoDB 4.4.28-27](https://docs.percona.com/percona-server-for-mongodb/4.4/release_notes/4.4.28-27.html) was released on February 7, 2024. It is a source available, highly-scalable database that is a fully-compatible, drop-in replacement for MongoDB 4.4.28 Community Edition enhanced with enterprise-grade features. Release highlights include these bug fixes, provided by MongoDB and included in Percona Server for MongoDB:

* Fixed the issue with the data and the ShardVersion mismatch for sharded multi-document transactions by adding the check that no chunk has moved for the collection being referenced since transaction started

* Improved cluster balancer performance by optimizing the construction of the balancer’s collection distribution status histogram

* Fixed the issue with blocking acquiring read/write tickets by TransactionCoordinator by validating that it can be recovered on step-up and can commit the transaction when there are no storage tickets available

* Investigated a solution to avoid a Full Time Diagnostic Data Capture (FTDC) mechanism to stall during checkpoint

Percona Server for MongoDB 4.4.28-27 is no longer available on Ubuntu 18.04 (Bionic Beaver).

[Download Percona Server for MongoDB 4.4.28-27](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

## Percona Server for MongoDB 4.2.25-25

[Percona Server for MongoDB 4.2.25-25](https://docs.percona.com/percona-server-for-mongodb/4.2/release_notes/4.2.25-25.html) was released on February 7, 2024. A release highlight is that Percona Server for MongoDB includes telemetry that fills in the gaps in our understanding of how you use Percona Server for MongoDB to improve our products. Participation in the anonymous program is optional. You can opt-out if you prefer not to share this information. Read more about Telemetry.

[Percona Server for MongoDB 4.2.25-25](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

That's it for this roundup, and be sure to [follow us on Twitter](https://twitter.com/Percona) to stay up-to-date on the most recent releases! Percona is a leader in providing best-of-breed enterprise-class support, consulting, managed services, training, and software for MySQL, MongoDB, PostgreSQL, MariaDB, and other open source databases in on-premises and cloud environments and is trusted by global brands to unify, monitor, manage, secure, and optimize their database environments.





