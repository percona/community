---
title: "Release Roundup April 30, 2024"
date: "2024-04-30T00:00:00+00:00"
tags: ['Percona', 'opensource', 'MongoDB', 'MySQL', 'releases']
categories: ['MongoDB', 'MySQL']
description: "Percona software releases and updates April 17 - April 30, 2024."
authors:
  - david_quilty
images:
  - blog/2024/04/Roundup-April-30.jpg
---

*Percona software releases and updates April 17 - April 30, 2024.*

Percona is a leading provider of unbiased, performance-first, open source database solutions that allow organizations to easily, securely, and affordably maintain business agility, minimize risks, and stay competitive, free from vendor lock-in. Percona software is designed for peak performance, uncompromised security, limitless scalability, and disaster-proofed availability.

Our Release Roundups showcase the latest Percona software updates, tools, and features to help you manage and deploy our software. It offers highlights, critical information, links to the full release notes, and direct links to the software or service itself to download.

Today's post includes releases and updates that have been released since April 15, 2024. Take a look.

## Percona Distribution for MySQL 8.3.0-1 (PS-based variant)

[Percona Distribution for MySQL 8.3.0-1 (PS-based variant)](https://docs.percona.com/percona-distribution-for-mysql/innovation-release/release-notes-ps-8.3.html) was released on April 16, 2024. This release is based on Percona Server for MySQL 8.3.0-1 and merges the MySQL 8.3 code base. It introduces the following changes:

-   Percona updates the Binary Log UDFs to make them compatible with new tagged GTIDs (Global Transaction Identifiers).

-   [PS-9044](https://perconadev.atlassian.net/browse/PS-9044): Adds the following variables to MyRocks:
    -   [`rocksdb_block_cache_numshardbits`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_block_cache_numshardbits)
    -   [`rocksdb_check_iterate_bounds`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_check_iterate_bounds)
    -   [`rocksdb_compact_lzero_now`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_compact_lzero_now)
    -   [`rocksdb_file_checksums`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_file_checksums)
    -   [`rocksdb_max_file_opening_threads`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_max_file_opening_threads)
    -   [`rocksdb_partial_index_ignore_killed`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_partial_index_ignore_killed)

    Changes the default values for the following variables:

    -   [`rocksdb_compaction_sequential_deletes`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_compaction_sequential_deletes) from 0 to 14999
    -   [`rocksdb_compaction_sequential_deletes_count_sd`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_compaction_sequential_deletes_count_sd) from `OFF` to `ON`
    -   [`rocksdb_compaction_sequential_deletes_window`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_compaction_sequential_deletes_window) from 0 to 15000
    -   [`rocksdb_force_flush_memtable_now`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_force_flush_memtable_now) from `ON` to `OFF`
    -   [`rocksdb_large_prefix`](https://docs.percona.com/percona-server/innovation-release/myrocks-server-variables.html#rocksdb_large_prefix) from `OFF` to `ON`

[Download Percona Distribution for MySQL 8.3.0-1 (PS-based variant)](https://www.percona.com/mysql/software)

## Percona Server for MySQL 8.3

On April 16, 2024, we released [Percona Server for MySQL 8.3](https://docs.percona.com/percona-server/innovation-release/release-notes/8.3.0-1.html). It includes all the features and bug fixes available in the MySQL 8.3 Community Edition in addition to enterprise-grade features developed by Percona. This release merges the MySQL 8.3 code base. Within this merge, Percona updates the Binary Log UDFs to make them compatible with new tagged GTIDs (Global Transaction Identifiers).

[Download Percona Server for MySQL 8.3](https://www.percona.com/mysql/software/percona-server-for-mysql)

## Percona Distribution for MongoDB 7.0.8

[Percona Distribution for MongoDB 7.0.8](https://docs.percona.com/percona-distribution-for-mongodb/7.0/release-notes-v7.0.8.html) was released on April 24, 2024. It is a freely available MongoDB database alternative that gives you a single solution that combines enterprise components from the open source community, designed and tested to work together. Bug fixes and improvements provided by MongoDB are included in Percona Distribution for MongoDB. Note: a number of issues with sharded multi-document transactions in sharded clusters of 2 or more shards have been identified that result in returning incorrect results and missing reads and writes. The issues occur when the transactions' metadata is being concurrently modified by using the following operations: `moveChunk`, `moveRange`, `movePrimary`, `renameCollection`, `drop`, and `reshardCollection`. Please check the release notes for further information.

[Download Percona Distribution for MongoDB 7.0.8](https://www.percona.com/mongodb)

## Percona Server for MongoDB 7.0.8-5

[Percona Server for MongoDB 7.0.8-5](https://docs.percona.com/percona-server-for-mongodb/7.0/release_notes/7.0.8-5.html) was released on April 24, 2024. It is an enhanced, source-available, and highly-scalable database that is a fully-compatible, drop-in replacement for MongoDB Community Edition 7.0.8. A number of issues with sharded multi-document transactions in sharded clusters of 2 or more shards have been identified that result in returning incorrect results and missing reads and writes. The issues occur when the transactions' metadata is being concurrently modified by using the following operations: `moveChunk`, `moveRange`, `movePrimary`, `renameCollection`, `drop`, and `reshardCollection`. Please check the release notes for further information.

[Download Percona Server for MongoDB 7.0.8-5](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

That's it for this roundup, and be sure to [follow us on Twitter](https://twitter.com/Percona) to stay up-to-date on the most recent releases! Percona is a leader in providing best-of-breed enterprise-class support, consulting, managed services, training, and software for MySQL, MongoDB, PostgreSQL, MariaDB, and other open source databases in on-premises and cloud environments and is trusted by global brands to unify, monitor, manage, secure, and optimize their database environments.