---
title: "Percona Bug Report: November 2023"
date: "2023-12-19T00:00:00+00:00"
tags: ['Percona', 'opensource', 'PMM', 'Kubernetes', 'MySQL']
authors:
  - aaditya_dubey
images:
  - blog/2023/12/BugReportNovember2023.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://perconadev.atlassian.net/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs,

## Percona Server/MySQL Bugs

[PS-8086](https://perconadev.atlassian.net/browse/PS-8086) : Increased memory usage in LRU manager with ROW_FORMAT=COMPRESSED, so it seems that after evicting uncompressed frames for a compressed table, Percona Server LRU manager uses more memory to track them than upstream MySQL.

*Reported Affected Version/s: 5.7.x, 8.0.26, 8.0.32*

[PS-8737](https://perconadev.atlassian.net/browse/PS-8737) / [[Bug #110706](https://bugs.mysql.com/bug.php?id=110706)] : Data will be lost when you perform table rebuild immediately after INSERT or DELETE commands. This means that all ALTER TABLE operations that require table rebuild, including a “null” alteration; that is, an ALTER TABLE statement that “changes” the table to use the storage engine that it already has Eg: "ALTER TABLE t1 ENGINE = InnoDB;", So after INSERT and DELETE, please do not execute table rebuild statement immediately.You can find the full list of ALTER operations that require table rebuild at https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html Check for column “Rebuilds Table”. All operations for which this column contains “Yes” or “No*” are affected.

*Reported Affected Version/s: 8.0.[28/29/30/31/32]*

[PS-8428](https://perconadev.atlassian.net/browse/PS-8428) : ALTER TABLE t ADD FULLTEXT crashes the server when --innodb_encrypt_online_alter_logs=ON. The problem has nothing to do with either innodb_encrypt_online_alter_logs, or Parallel Threads for Online DDL Operations. The issues turned out that in binaries built with OpenSSL 3.0.x my_aes_crypt() function has a flaw and can no longer decrypt data encrypted with the same function previously.

*Reported Affected Version/s: 8.0.30-22*

*Fixed version: 8.0.30-22*

Please don't get confused with the affected & fix version is the same for this bug since this bug was reported internally during testing of the release build & that’s the reason it gets the same affected & fix version.

[PS-8987](https://perconadev.atlassian.net/browse/PS-8987) / [[Bug #112935](https://bugs.mysql.com/bug.php?id=112935)] : This bug results in inconsistency seen between MYISAM and MEMORY for simple CREATE and SELECT operation.

Please check the below scenario where result inconsistency is seen:

1. Added sample data to MyISAM/InnoDB Tables.

2. Executed SELECT statement which is a bit complex so can’t be added here but it can be seen in the bug report.

3. Empty set return when SELECT executed against MyISAM/InnoDB Tables & 4 rows return when same query executed against Memory Engine. 

*Reported Affected Version/s: 8.0.34-26, 8.0.35-27*

[PS-8990](https://perconadev.atlassian.net/browse/PS-8990) / [[Bug #112979](https://bugs.mysql.com/bug.php?id=112979)] : MySQL server does not respect system [variable binlog_transaction_compression_level_zstd](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_transaction_compression_level_zstd) so it sets the compression level for binary log transaction compression on this server, which is enabled by the [binlog_transaction_compression](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_transaction_compression) system variable. The value is an integer that determines the compression effort, from 1 (the lowest effort) to 22 (the highest effort). If you do not specify this system variable, the compression level is set to 3. As the compression level increases, the data compression ratio increases, which reduces the storage space and network bandwidth required for the transaction payload.

*Reported Affected Version/s: 8.0.34-26, 8.0.35-27*

[PS-9015](https://perconadev.atlassian.net/browse/PS-9015) / [[Bug #113256](https://bugs.mysql.com/bug.php?id=113256)] : "DATA_FREE" shows a different value when comparing information_schema.TABLES vs information_schema.PARTITIONS. It is hard to say which result set is correct since we don’t have a source of truth.

*Reported Affected Version/s: 5.7.43-47, 8.0.34-26*

[PS-9011](https://perconadev.atlassian.net/browse/PS-9011) / [[Bug #112946](https://bugs.mysql.com/bug.php?id=112946)] : Prior to 8.0.29 INSTANT column exists on a non-system table with NULL columns in the MySQL SCHEMA which eventually leads to a corruption post 8.0.30+ upgrades. Although it's probably not a best practice to create tables in  mysql SCHEMA, it should not lead to corruption, especially when INSTANT is the default algorithm.

## Percona Xtradb Cluster

[PXC-4343](https://perconadev.atlassian.net/browse/PXC-4343) : Occasionally, during SST, InnoDB tablespace gets silently corrupted, resulting in the later Xtrabackup failure with the following error [MY-012224] [InnoDB] Header page contains inconsistent data in datafile. The triggering condition appears to be PXC 5.7 => 8.0 upgrade, where the corruption manifests in a 2nd node that joins later from the upgraded node. The corruption gets discovered once the 3rd node tries to join from the 2nd node as the donor or when a regular backup is taken from the 2nd node. To workaround this issue, always specify the first upgraded node as a donor.

*Reported Affected Version/s: 8.0.34-26*

[PXC-4237](https://perconadev.atlassian.net/browse/PXC-4237) : When adding a new node, with PXC tarball installation error is being reported saying `[WSREP] Failed to read 'ready <addr>' from: wsrep_sst_xtrabackup-v2`. However, this issue is expected to be fixed by the upcoming release of PXC 8.0.35, and fortunately, below workaround can fix the issue quickly:

```
Create /var/run/mysqld/ folder owned by mysql OS user.

Backup wsrep_sst_common file before editing:

shell> cp -nvp /usr/local/mysql/bin/wsrep_sst_common /usr/local/mysql/bin/wsrep_sst_common.orig.for-bug-PXC-4237

Implement the change:

shell> sed -i '297s/.*/set +e; & ; set -e/' /usr/local/mysql/bin/wsrep_sst_common

Verify the changes:

shell> sed -n '297p' /usr/local/mysql/bin/wsrep_sst_common.orig.for-bug-PXC-4237 
            MYSQLD_PATH=$(readlink -f /proc/${WSREP_SST_OPT_PARENT}/exe)
shell> sed -n '297p' /usr/local/mysql/bin/wsrep_sst_common
set +e;             MYSQLD_PATH=$(readlink -f /proc/${WSREP_SST_OPT_PARENT}/exe) ; set -e
```

*Reported Affected Version/s: 8.0.32-24, 8.0.34-26*

[PXC-4318](https://perconadev.atlassian.net/browse/PXC-4318) : PXC cluster stalls and eventually crashes due to a long semaphore wait, which is happening because ha_commit_low does not commit a transaction that does not perform any changes such as an empty transaction and it can’t be controlled since it is an internal process. Fortunately, the upcoming release of PXC 8.0.35 will fix the issue. 

*Reported Affected Version/s: 8.0.33-25*

[PXC-4336](https://perconadev.atlassian.net/browse/PXC-4336) : PXC node eviction when a new CHECK CONSTRAINT is created which violates the condition, Eg. table is created with one entry say id 100 and after creation we added CHECK CONSTRAINT using ALTER TABLE t ADD CONSTRAINT CHK_id CHECK (id <=75); Here 100 is not less than 75 which violate the conditions and eventually node become inconsistent and get disconnected/evicted from the cluster. To avoid this scenario make sure to avoid violation of CHECK CONSTRAINT conditions.

*Reported Affected Version/s: 8.0.34-26*

[PXC-4034](https://perconadev.atlassian.net/browse/PXC-4034) : When PXC cluster uses as a source and an async replication as a replica where "set @@session.sql_log_bin = off;" is used, this introduces a GTID gap in the "gtid_executed" set on the PXC source. As a workaround to the issue avoid using statement with "set @@session.sql_log_bin = off;" in the source/PXC

*Reported Affected Version/s: 5.7.38-31.59, 8.0.28-19, 8.0.34-26*


## Percona Toolkit

[PT-1724](https://perconadev.atlassian.net/browse/PT-1724) : Percona toolkit unable to work if user using 'caching_sha2_password' Authentication plugin

*Reported Affected Version/s: 3.0.13, 3.5.5*

[PT-2030](https://perconadev.atlassian.net/browse/PT-2030) : pt-heartbeat is not compatible with PostgreSQL throwing Cannot get MySQL var character_set_server: DBD::Pg::db selectrow_array failed: ERROR:  syntax error at or near "LIKE" LINE 1: SHOW VARIABLES LIKE 'character_set_server'

*Reported Affected Version/s: 3.3.1, 3.5.5*

[PT-2083](https://perconadev.atlassian.net/browse/PT-2083) : when running pt-archiver with --charset option in MySQL 8.0 does not work.

*Reported Affected Version/s: 3.3.1, 3.5.5*

*Fixed version: 3.5.6 [Pending Release]*

[PT-2106](https://perconadev.atlassian.net/browse/PT-2106) : In pt-online-schema-change adding column to table (parent table) with having foreign key reference which triggers rebuilding constraints and can cause inconsistencies.

*Reported Affected Version/s: 3.3.1, 3.5.5*

[PT-2207](https://perconadev.atlassian.net/browse/PT-2207) : pt-archiver doesn't work when ANSI_QUOTES is set in sql_mode

*Reported Affected Version/s: 3.5.2, 3.5.5*

*Fixed version: 3.5.6 [Pending Release]*


## Percona Monitoring and Management (PMM)

[PMM-4712](https://perconadev.atlassian.net/browse/PMM-4712) : PMM frequently crashes due to out of memory kills with postgres_exporter consuming 20-30GB of RAM and to debug it pprof endpoints to postgres_exporter was missing

*Fixed version: 2.41.0 [Pending Release]*

[PMM-12013](https://perconadev.atlassian.net/browse/PMM-12013) : rds_exporter unreliable for large deployments which generate gaps in the gathered metrics and some improvement fix done here at PMM-11727

*Reported Affected Version/s: 2.35.0*

[PMM-12349](https://perconadev.atlassian.net/browse/PMM-12349) : ReplicaSet Summary shows wrong data when a node is gone

*Reported Affected Version/s: 2.40.1*

[PMM-12631](https://perconadev.atlassian.net/browse/PMM-12631) : Route of /logs.zip crashes with `reflect: call of reflect.Value.NumField on string`

*Reported Affected Version/s: 2.40.1*
*Fixed version: 2.41.0 [Pending Release]*

[PMM-12738](https://perconadev.atlassian.net/browse/PMM-12738) : File certificate.conf is required, but not mentioned anywhere in helm charts but in fact, it should not be required.

*Reported Affected Version/s: 2.40.1*

## Percona XtraBackup

[PXB-2860](https://perconadev.atlassian.net/browse/PXB-2860) : Xtrabackup keeps locking table even using --tables-exclude and –lock-ddl-per-table.

*Reported Affected Version/s: 8.0.33-28*
*Fixed version: 8.0.34-29*

[PXB-3168](https://perconadev.atlassian.net/browse/PXB-3168) : Under high write load, backup fails with "log block numbers mismatch" error

*Reported Affected Version/s: 8.0.33-28, 8.0.34-29*
*Fixed version: 8.0.35-30, 8.2*

[PXB-3079](https://perconadev.atlassian.net/browse/PXB-3079) : Prepare skips rollback on encrypted tables and completes successfully if the keyring plugin is not loaded.

*Reported Affected Version/s: 8.0.33-27*
*Fixed version: 8.0.34-29*

[PXB-3147](https://perconadev.atlassian.net/browse/PXB-3147) : Xtrabackup failed to execute query 'DO innodb_redo_log_consumer_register("PXB"); if sql_mode=’ANSI_QUOTES’ is used.' This results in the Xtrabackup execution failure. 

*Reported Affected Version/s: 8.0.33-28*
*Fixed version: 8.0.35-30, 8.2*

[PXB-2954](https://perconadev.atlassian.net/browse/PXB-2954) : Xtrabackup failing with "[ERROR] [MY-011825] [Xtrabackup] innodb_init(): Error occurred" to prepare in case of orphan ibd

*Reported Affected Version/s: 8.0.28-21*
*Fixed version: 8.0.32-26*

## Percona Kubernetes Operator

[K8SPG-404](https://perconadev.atlassian.net/browse/K8SPG-404) : Upgrade from percona PostgreSQL Operator 1.3 to 1.4 is ending up with a cluster without any replicas.

*Reported Affected Version/s: 1.4.0*
*Fixed version: 1.5.0 [Pending Release]*

[K8SPG-420](https://perconadev.atlassian.net/browse/K8SPG-420) : Ending up in multiple shared repo after cluster pause and unpause.

*Reported Affected Version/s: 1.4.0*
*Fixed version: 1.5.0 [Pending Release]*

[K8SPG-435](https://perconadev.atlassian.net/browse/K8SPG-435) : Pod is recreated when /tmp is filled

*Reported Affected Version/s: 2.2.0*
*Fixed version: 2.3.0 [Pending Release]*

[K8SPG-443](https://perconadev.atlassian.net/browse/K8SPG-443) : Only english locale is installed, missing other languages support in Postgres

*Reported Affected Version/s: 2.2.0*
*Fixed version: 2.3.0 [Pending Release]*

[K8SPG-453](https://perconadev.atlassian.net/browse/K8SPG-453) : pg_stat_monitor hangs primary instance and it's impossible to disable it

*Reported Affected Version/s: 2.2.0*
*Fixed version: 2.3.0 [Pending Release]*

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).
 
Quick References:

* [Percona JIRA](https://perconadev.atlassian.net)

* [MySQL Bug Report](https://bugs.mysql.com/)

* [Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)

* [Percona Forums](https://forums.percona.com/)
