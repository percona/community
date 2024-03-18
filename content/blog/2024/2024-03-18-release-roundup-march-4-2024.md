---
title: "Release Roundup March 18, 2024"
date: "2024-03-18T00:00:00+00:00"
tags: ['Percona', 'opensource', 'PostgreSQL', 'MongoDB', 'MySQL', 'releases']
description: "Percona software releases and updates March 5 - March 18, 2024."
authors:
  - david_quilty
images:
  - blog/2024/03/Roundup-March-18.jpg
---

*Percona software releases and updates March 5 - March 18, 2024.*

Percona is a leading provider of unbiased, performance-first, open source database solutions that allow organizations to easily, securely, and affordably maintain business agility, minimize risks, and stay competitive, free from vendor lock-in. Percona software is designed for peak performance, uncompromised security, limitless scalability, and disaster-proofed availability.

Our Release Roundups showcase the latest Percona software updates, tools, and features to help you manage and deploy our software. It offers highlights, critical information, links to the full release notes, and direct links to the software or service itself to download.

Today's post includes those releases and updates that have come out since March 4, 2024. Take a look.

## Percona Server for MySQL 5.7.44-49 (Post-EOL support version)

This release is [Percona Server for MySQL 5.7.44-49 (Post-EOL support version)](https://docs.percona.com/percona-server/5.7/release-notes/5.7.44-49.html), and the fixes are available to [MySQL 5.7 Post-EOL Support from Percona customers](https://www.percona.com/post-mysql-5-7-eol-support). Community members can [build this release from the source](https://docs.percona.com/percona-server/5.7/installation/git-source-tree.html).  Percona Server for MySQL 5.7.44-49 contains the fix for [CVE-2024-20963](https://nvd.nist.gov/vuln/detail/CVE-2024-20963) and a portability fix.

[Download Percona Server for MySQL 5.7.44-49 (Post-EOL support version)](https://www.percona.com/downloads#percona-server-mysql)

## Percona Distribution for MySQL 8.0.36 (PS-based variant)

On March 4, 2024, [Percona Distribution for MySQL 8.0.36 (PS-based variant)](https://docs.percona.com/percona-distribution-for-mysql/8.0/release-notes-ps-v8.0.36.html) was released. It is the most stable, scalable, and secure open source MySQL distribution, with two download options: one based on Percona Server for MySQL and one based on Percona XtraDB Cluster.  This release is focused on the Percona Server for MySQL-based deployment variation.  This release fixes the Orchestrator issues.

[Download Percona Distribution for MySQL 8.0.36 (PS-based variant)](https://www.percona.com/mysql/software)

## Percona Server for MySQL 8.0.36

[Percona Server for MySQL 8.0.36](https://docs.percona.com/percona-server/8.0/release-notes/8.0.36-28.html) was released on March 4, 2024. It includes all the features and bug fixes available in the MySQL 8.0.36 Community Edition, and enterprise-grade features developed by Percona. Improvements and bug fixes provided by Oracle for MySQL 8.0.36 and included in Percona Server for MySQL are the following:

-   The hashing algorithm employed yielded poor performance when using a HASH field to check for uniqueness. (Bug #109548, Bug #34959356)
-   All statement instrument elements that begin with `statement/sp/%`, except `statement/sp/stmt`, are disabled by default.

[Download Percona Server for MySQL 8.0.36](https://www.percona.com/mysql/software/percona-server-for-mysql)

## Percona Operator for MySQL based on Percona XtraDB Cluster 1.14.0

[Percona Operator for MySQL based on Percona XtraDB Cluster 1.14.0](https://docs.percona.com/percona-operator-for-mysql/pxc/ReleaseNotes/Kubernetes-Operator-for-PXC-RN1.14.0.html) was released on March 4, 2024. It contains everything you need to quickly and consistently deploy and scale Percona XtraDB Cluster instances in a Kubernetes-based environment on-premises or in the cloud. Among other new features, a custom prefix for Percona Monitoring and Management (PMM) allows using one PMM Server to monitor multiple databases, even if they have identical cluster names.

[Download Percona Operator for MySQL based on Percona XtraDB Cluster 1.14.0](https://www.percona.com/mysql/software/percona-operator-for-mysql)

## Percona Distribution for PostgreSQL 13.14

[Percona Distribution for PostgreSQL 13.14](https://docs.percona.com/postgresql/13/release-notes-v13.14.html) was released on March 6, 2024. It is a solution of a collection of tools from the PostgreSQL community that are tested to work together and assist you in deploying and managing PostgreSQL. A release highlight is that the Docker image for Percona Distribution for PostgreSQL is now available for ARM architectures. This improves the user experience with the Distribution for developers with ARM-based workstations.

[Download Percona Distribution for PostgreSQL 13.14](https://www.percona.com/postgresql/software/postgresql-distribution)

## Percona Distribution for PostgreSQL 12.18

On March 11, 2024, we released [Percona Distribution for PostgreSQL 12.18. ](https://docs.percona.com/postgresql/12/release-notes-v12.18.html)This release of Percona Distribution for PostgreSQL is based on PostgreSQL 12.18[.](https://docs.percona.com/postgresql/12/release-notes-v12.18.html)

[Download Percona Distribution for PostgreSQL 12.18](https://www.percona.com/postgresql/software/postgresql-distribution)

## Percona Backup for MongoDB 2.4.0

On March 5, 2024, [Percona Backup for MongoDB 2.4.0](https://docs.percona.com/percona-backup-mongodb/release-notes/2.4.0.html) was released. It is a distributed, low-impact solution for consistent backups of MongoDB sharded clusters and replica sets. This is a tool for creating consistent backups across a MongoDB sharded cluster (or a non-sharded replica set), and for restoring those backups to a specific point in time. A release highlight is that you can now [delete backup snapshots of a specific type](https://docs.percona.com/percona-backup-mongodb/usage/delete-backup.html#__tabbed_2_3). For example, delete only logical backups that you might have created and no longer need. You can also check what exactly will be deleted with the new `--dry-run flag`. This improvement helps you better meet the organization's backup policy and improves your experience with cleaning up outdated data.

[Download Percona Backup for MongoDB 2.4.0](https://www.percona.com/mongodb/software/percona-backup-for-mongodb)

<hr />

That's it for this roundup, and be sure to [follow us on Twitter](https://twitter.com/Percona) to stay up-to-date on the most recent releases! Percona is a leader in providing best-of-breed enterprise-class support, consulting, managed services, training, and software for MySQL, MongoDB, PostgreSQL, MariaDB, and other open source databases in on-premises and cloud environments and is trusted by global brands to unify, monitor, manage, secure, and optimize their database environments.