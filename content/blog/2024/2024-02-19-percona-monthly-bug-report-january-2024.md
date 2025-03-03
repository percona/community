---
title: "Percona Bug Report: January 2024"
date: "2024-02-19T00:00:00+00:00"
tags: ['Percona', 'opensource', 'PMM', 'Kubernetes', 'MySQL']
categories: ['PMM', 'MySQL', 'Toolkit']
authors:
  - aaditya_dubey
images:
  - blog/2024/02/BugReportJanuary2024.jpg
---

At Percona, we believe that transparency is key to improving our products. We are dedicated to creating top-of-the-line open-source database solutions and providing support for any issues that may arise. We encourage feedback and bug reports to help us continually improve.

We stay updated on [bug reports](https://perconadev.atlassian.net/) through our own platform as well as [other sources](https://bugs.mysql.com/) to ensure we have the most up-to-date information. To make it easier for you, we have compiled a central list of the most critical bugs for your reference in this edition of our bug report.

In this episode of our bug report, we provide the following list of bugs.

## Percona Server/MySQL Bugs

[PS-8983](https://perconadev.atlassian.net/browse/PS-8983): System variable [group_replication_view_change_uuid](https://dev.mysql.com/doc/refman/8.0/en/group-replication-system-variables.html#sysvar_group_replication_view_change_uuid) introduced in MySQL 8.0.26 which corrected the issue [Bug#103641](https://bugs.mysql.com/bug.php?id=103641) in where data is inconsistent between nodes after killing primary node in group replication, However there is still an issue where these events are also generated on the standby/secondary cluster in a ClusterSet thus creating errant transactions, and if binlogs containing these events are purged, then it will not be possible to perform a failover between clusters.

*Reported Affected Version/s: 8.0.26*

*Fixed Version: 8.0.31-23*

[PS-9048](https://perconadev.atlassian.net/browse/PS-9048): When innodb_optimize_fulltext_only is enabled and running `OPTIMIZE TABLE <table_name>` which has fulltext index actually causing assertion in Percona server debug build, Please note issue is specifically happening when PARSER is [ngram](https://dev.mysql.com/doc/refman/8.0/en/fulltext-search-ngram.html).

*Reported Affected Version/s: 5.7.42, 8.0.34*
*Fixed Version: N/A [Fix in Progress]*

[PS-9018](https://perconadev.atlassian.net/browse/PS-9018): When replica has a non-replicated database then during intensive workload from the source where multi-threaded slave applier (MTS) is enabled and log_slave_updates=0 then DDL executed against this non-replicated database completely stalls the replica instance.

*Upstream Bug: [113727](https://bugs.mysql.com/bug.php?id=113727)*

*Reported Affected Version/s: 8.0.19+*
*Fixed Version: N/A [Fix in Review]*
*Workaround : Use log_slave_updates=1, Please note enabling this may produce huge binlog volume on the replica which may or may not be feasible with respect to storage.*

[PS-9083](https://perconadev.atlassian.net/browse/PS-9083): Percona server crashes when server is running with slow_query_log in conjunction with *long_query_time*, *log_slow_verbosity = profiling*,*query_info* variables.

*Reported Affected Version/s: 8.0.35*
*Fixed Version: 8.0.36 [Pending Release]*
*Workaround : Remove “query_info” from log_slow_verbosity*

[PS-9081](https://perconadev.atlassian.net/browse/PS-9081): Materializing happens when a query is being executed against performance_schema.data_locks can lead to excessive memory usage and OOM.

*Reported Affected Version/s: 8.0.34+*
*Fixed Version: It is expected to be fixed by PS 8.0.37*
*Workaround : Putting a LIMIT clause to read queries.*

## Percona Xtradb Cluster

[PXC-4341](https://perconadev.atlassian.net/browse/PXC-4341): Execution of prepared statement after FLUSH TABLES makes the node abort from the cluster.

*Reported Affected Version/s: 8.0.33+*
*Fixed Version: It is expected to be fixed by PXC 8.0.36*
*Workaround : There is no straight forward workaround but one can run the prepared statement and FLUSH TABLES statement separately.*

[PXC-4316](https://perconadev.atlassian.net/browse/PXC-4316): Network loss may lead to node's logs flooded with "changed identity" events which eventually let primary node go non-primary, and reconnect another node. It will keep non primary nodes so we ended with all nodes as non primary.

*Reported Affected Version/s: 8.0.33+*
*Fixed Version: It is expected to be fixed by PXC 8.0.36*

[PXC-4348](https://perconadev.atlassian.net/browse/PXC-4348): Cluster state interrupted with MDL BF-BF conflict when forcing deadlock. To hit the crash we are required to run queries on multiple sessions where one session should run "optimize table <tbl_name>;" multiple times so mysqlslap is the right candidate to repeat this behavior and other sessions will run delete/insert on the same table.

*Reported Affected Version/s: 8.0.33+*
*Fixed Version: It is expected to be fixed by PXC 8.0.36*

## Percona Toolkit

[PT-2217](https://perconadev.atlassian.net/browse/PT-2217): When running pt-mongodb-summary against psmdb6.0/psmdb7.0 it gives error  "BSON field 'getCmdLineOpts.recordStats' is an unknown field" Please note that PT tool does not work with MongoDB 6.0+.

*Reported Affected Version/s: 3.5.X*
*Fixed Version: It is expected to be fixed by PT 3.6.0*

[PT-2309](https://perconadev.atlassian.net/browse/PT-2309): When the primary key is a UUID binary 16 column pt-table-sync hits with error "Cannot nibble table `db_name`.`table_name` because MySQL chose no index instead of the `PRIMARY`"

*Reported Affected Version/s: 3.5.7*
*Fixed Version: It is expected to be fixed by PT 3.5.8*

[PT-2305](https://perconadev.atlassian.net/browse/PT-2305): pt-online-schema-change should error out if server is a slave/replica in row based replication. This can lead to source/replica becoming inconsistent if there are writes on source when the tool runs on replica. 

Please find the example below where data loss is seen:

1. Set-up classic source-replica
2. Make sure `binlog_format=row`
3. Create a table on master and add sufficient data so that pt-osc takes a little bit of time to run.
4. Then start pt-osc on slave, and execute updates/deletes on master.
5. Once pt-osc is done, check table checksum or table count to verify the data differences. Please check the below output with row differences:

```
master [localhost:22536] {msandbox} (test) > select count(*) from sbtest1;  
+----------+
| count(*) |
+----------+
|   999999 |
+----------+
1 row in set (0.58 sec)

slave1 [localhost:22537] {msandbox} (test) > select count(*) from sbtest1;
+----------+
| count(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.40 sec)
```

*Reported Affected Version/s: 3.5.7*
*Fixed Version: It is expected to be fixed by PT 3.6.0*

[PT-2284](https://perconadev.atlassian.net/browse/PT-2284): When running pt-kill with the --daemonize option, if the query has character like '柏木', pt-kill process exists with message "Wide character in printf at /usr/bin/pt-kill line 7508."

*Reported Affected Version/s: 3.5.7*
*Fixed Version: It is expected to be fixed by PT 3.6.0*
*Workaround : Running pt-kill without --daemonize option manually.*

[PT-2089](https://perconadev.atlassian.net/browse/PT-2089): When SHOW ENGINE INNODB STATUS reports garbled UTF characters then pt-deadlock-logger crashes with "server ts thread txn_id txn_time user hostname ip db tbl idx lock_type lock_mode wait_hold victim query" 

*Reported Affected Version/s: 3.3.1, 3.5.7*

## Percona Monitoring and Management (PMM)

[PMM-12806](https://perconadev.atlassian.net/browse/PMM-12806): We can't tune VictoriaMetrics running inside PMM since PMM does not honor the environment variables for VictoriaMetrics. So PMM pre-defines certain flags that allow users to set all other [VictoriaMetrics parameters](https://docs.victoriametrics.com/#list-of-command-line-flags) as environment variables.

```
Example:

To set downsampling, use the downsampling.period parameter as follows:

-e VM_downsampling_period=20d:10m,120d:2h
```

This instructs VictoriaMetrics to [deduplicate](https://docs.victoriametrics.com/#deduplication) samples older than 20 days with 10 minute intervals and samples older than 120 days with two hour intervals.

*Reported Affected Version/s: 2,40.1*
*Fixed Version: It is expected to be fixed by PMM 2.41.2*

[PMM-12805](https://perconadev.atlassian.net/browse/PMM-12805): When monitoring MongoDB servers, logs might get filled with the a CommandNotSupportOnView message, As a result, disk space fills up.

*Reported Affected Version/s: 2,40.0, 2.41.0*
*Fixed Version: It is expected to be fixed by PMM 2.41.2*

[PMM-12809](https://perconadev.atlassian.net/browse/PMM-12809): Common Vulnerabilities and Exposures (CVE) found in PMM gRPC(Remote Procedure Call (RPC)) which impacts PMM v2.40.1+

*Reported Affected Version/s: 2.41.0+*
*Fixed Version: It is expected to be fixed by PMM 2.41.2*


## Percona XtraBackup

[PXB-3024](https://perconadev.atlassian.net/browse/PXB-3024): Backups are not reliable when running on a secondary node of Group Replication(GR) since --lock-ddl does not have any effect on secondary node of GR.

*Reported Affected Version/s: 8.0.28-20, 8.0.31-24*
*Fixed Version: 8.0.32-26*

[PXB-2928](https://perconadev.atlassian.net/browse/PXB-2928): Xtrabackup crashes with signal 11 when taking a backup using [--page-tracking](https://docs.percona.com/percona-xtrabackup/8.0/page-tracking.html#install-the-component) option. So if you are using this option while taking backup then upgrading to PXB 8.0.31 is recommended since there is no workaround available to this issue at the moment.

*Reported Affected Version/s: 8.0.29-22*
*Fixed Version: 8.0.31-24*

[PXB-3037](https://perconadev.atlassian.net/browse/PXB-3037): In order to assure a consistent replication state, [--safe-slave-backup](https://docs.percona.com/percona-xtrabackup/8.0/make-backup-in-replication-env.html?h=safe+backup#the-safe-slave-backup-option) option stops the replication SQL thread and waits to start backing up until slave_open_temp_tables in SHOW STATUS is zero. If there are no open temporary tables, the backup will take place, otherwise the SQL thread will be started and stopped until there are no open temporary tables. The backup will fail if slave_open_temp_tables does not become zero after --safe-slave-backup-timeout seconds (defaults to 300 seconds). The replication SQL thread will be restarted when the backup finishes, But due to this bug if backup fails in between then SQL thread is not getting restarted. So restarting the SQL thread manually is required.

*Reported Affected Version/s: 8.0.31-24, 8.0.35-30*
*Fixed Version: No ETA*

[PXB-2733](https://perconadev.atlassian.net/browse/PXB-2733): backup-lock-timeout and backup-lock-retry-count do not work.

*Reported Affected Version/s: 2.4.24, 8.0.27-19, 8.0.35-30*
*Fixed Version: No ETA*

## Percona Kubernetes Operator

[K8SPG-492](https://perconadev.atlassian.net/browse/K8SPG-492): Restore job created by PerconaPGRestore doesn't inherit .spec.instances[].tolerations since restore Job pod get stuck in pending and causing down time.

*Reported Affected Version/s: 2.2.0*
*Fixed Version: It is expected to be fixed by PG operator 2.4.0*
*Workaround: Remove [taint](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/), wait until the restore container is scheduled and re-add it again. [K8SPSMDB-958](https://perconadev.atlassian.net/browse/K8SPSMDB-958): PMM fails to monitor mongos due to lack of permission.*

*Reported Affected Version/s: 1.14.0*
*Fixed Version: 1.15.0*

[K8SPG-291](https://perconadev.atlassian.net/browse/K8SPG-291): Modifying existing backup schedule does not work with PG operator v1.3.0

*Reported Affected Version/s: 1.3.0*
*Fixed Version: 1.4.0*

[K8SPG-286](https://perconadev.atlassian.net/browse/K8SPG-286): When requiring TLS for all connections, PMM client fails to connect with "no pg_hba.conf entry".

*Reported Affected Version/s: 1.2.0, 1.3.0, 2.0.0*
*Fixed Version: 1.4.0*


## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).
 
Quick References:

* [Percona JIRA](https://perconadev.atlassian.net)

* [MySQL Bug Report](https://bugs.mysql.com/)

* [Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)

* [Percona Forums](https://forums.percona.com/)
