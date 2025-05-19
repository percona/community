---
title: "Percona Bug Report: April 2025"
date: "2025-05-19T00:00:00+00:00"
tags: ['PMM', 'Kubernetes', 'MySQL', 'MongoDB', 'Percona', 'Opensource']
categories: ['PMM', 'Cloud', 'MySQL', 'MongoDB', 'Toolkit']
authors:
  - aaditya_dubey
images:
  - blog/2025/05/BugReportApril2025.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://jira.percona.com/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs.

## Percona Server/MySQL Bugs

[PS-8846](https://perconadev.atlassian.net/browse/PS-8846): The ALTER INSTANCE RELOAD TLS thread gets stuck. This happens in instances with a high new connections rate (>60/s) but not in all instances. Percona and Upstream did not fix it properly because the current implementation of ALTER INSTANCE RELOAD TLS requires all existing SSL connections to be closed. "A thread that executes ALTER INSTANCE RELOAD TLS tries to acquire an RCU Lock(Read-Copy-Update), waiting for the number of readers to become 0. In other words, when the server has a constant flow of new incoming SSL connections, the chances of acquiring this lock are pretty low." Therefore, Percona and Oracle only partially fixed this; this fix should improve this behaviour.

**Reported Affected Version/s**: 8.0.32-24, 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

[PS-9609](https://perconadev.atlassian.net/browse/PS-9609): The audit_log_filter can't be installed when the server is using component_keyring_kmip

**Reported Affected Version/s**: 8.0.39-30\
**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 8.0.42-33

<hr>

[PS-9628](https://perconadev.atlassian.net/browse/PS-9628): The binlog_encryption does not work with component_keyring_kmip

****Reported Affected Version/s****: 8.0.40-31

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 8.0.42-33

<hr>

[PS-9664](https://perconadev.atlassian.net/browse/PS-9664): With a very simple workload, MyRocks allocates a lot of memory and does not free it when the workload finishes. All instrumentation available either does not provide information about memory allocated or provides only part of it. As a result, users cannot predict how much RAM to install on the server that runs the MyRocks storage engine. With InnoDB same workload requires about 1.7G and frees about 0.5G once the job is finished.

****Reported Affected Version/s****: 8.0.39-30

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

[PS-9719](https://perconadev.atlassian.net/browse/PS-9719): When changing [binlog_transaction_dependency_tracking](https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-options-binary-log.html#sysvar_binlog_transaction_dependency_tracking) in high load workload, MySQL got a segmentation fault.

**Reported Affected Version/s**: 8.0.40, 8.0.41-32, 8.0.33

**Upstream Bug**:  [117922](https://bugs.mysql.com/bug.php?id=117922)

**Workaround/Fix**: "set global binlog_transaction_dependency_tracking = commit_order;"

**Fixed/Planned Version/s**: 8.0.42-33, 8.4.5-5

<hr>

[PS-9768](https://perconadev.atlassian.net/browse/PS-9768): An unexpected duplicate error occurs when running a select query with a group by JSON data.

**Reported Affected Version/s**: 8.0.41-32, 8.4.4-4

**Upstream Bug**:  [117927](https://bugs.mysql.com/bug.php?id=117927)

**Workaround/Fix**: Rebuilding the table with "alter table db_name.table_name = rocksdb;" can fix the issue.

**Fixed/Planned Version/s**: To Be Determined

<hr>

## Percona Xtradb Cluster

[PXC-4512](https://perconadev.atlassian.net/browse/PXC-4512): When DDLs run against tables with foreign key references when there is a write load simultaneously. The issue is typically triggered during pt-online-schema-change execution, and after a dozen or so iterations, random PXC nodes will terminate with MDL BF-BF conflict. Sometimes, the writer fails, and sometimes, the other nodes, but it can be reproducible with just the RENAME query.

**Reported Affected Version/s**: 8.0.33-25, 8.0.35-27, 8.0.36-28, 8.0.37-29, 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Only a full write stop would help.

**Fixed/Planned Version/s**: 8.0.42, 8.4.5

<hr>

[PXC-4648](https://perconadev.atlassian.net/browse/PXC-4648): After upgrading from 8.0.41 to 8.4.3, the node can't join the group with the following error.

```
[ERROR] [MY-000000] [Galera] /mnt/jenkins/workspace/pxc80-autobuild-RELEASE/test/rpmbuild/BUILD/Percona-XtraDB-Cluster-8.4.3/percona-xtradb-cluster-galera/gcs/src/gcs_group.cpp:group_check_proto_ver():343: Group requested gcs_proto_ver: 5, max supported by this node: 4.Upgrade the node before joining this group.Need to abort.
```

The problem is that 8.0.41 and 8.4.4 use Galera 26.4.21. It introduced the GCS protocol version 5, 8.0.40 and 8.4.3 using Galera 26.4.20. So, the node that doesn't understand protocol 5 tries to connect to a cluster that uses protocol 5.

It is fixed as a documented bug, which can be seen [here](https://docs.percona.com/percona-xtradb-cluster/8.4/upgrade-guide.html?h=upgrade+newest+8.0+version+ensure+is+newer+corresponding+8.4+plan).

**Reported Affected Version/s**: 8.4.3

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 8.4.4

<hr>

[PXC-4638](https://perconadev.atlassian.net/browse/PXC-4638): The binlog_utils_udf plugin fails to access binlog files correctly after an SST (State Snapshot Transfer) due to inconsistencies in the mysql-bin.index file.  After an SST, the first entry in the mysql-bin.index file can be incorrectly formatted with a relative path, while subsequent entries use absolute paths. This inconsistency can prevent the binlog_utils_udf plugin from locating the correct binlog files.

The resulting mysql-bin.index content after SST might appear as:
```
mysql-bin.000010  
/home/user/sandboxes/pxc_msb_8_0_40/node2/data/mysql-bin.000011  
/home/user/sandboxes/pxc_msb_8_0_40/node2/data/mysql-bin.000012 
```

**Reported Affected Version/s**: 8.0.40, 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Rewriting binlog.index and adding the "./" prefix to the first entry, and running flush binary logs resolved this issue.

**Fixed/Planned Version/s**: 8.0.42, 8.4.5

<hr>

[PXC-3576](https://perconadev.atlassian.net/browse/PXC-3576): Deploying a new installation using the setting lower_case_table_names=1 on the startup generates the following entry on the log:
```
[Warning] [MY-010324] [Server] 'db' entry 'percona_schema mysql.pxc.sst.role@localhost' had database in mixed case that has been forced to lowercase because lower_case_table_names is set. It will not be possible to remove this privilege using REVOKE.
```

Looking at the mysql.db, we can see the deployment was able to create the mysql.pxc.sst.role mapping an uppercase database name:

```
mysql> select * from mysql.db where user='mysql.pxc.sst.role';
+-----------+--------------------+--------------------+------+
| Host | Db | User | Select_priv | Insert_priv | Update_priv | Delete_priv | Create_priv | Drop_priv | Grant_priv | References_priv | Index_priv | Alter_priv | Create_tmp_table_priv | Lock_tables_priv | Create_view_priv | Show_view_priv | Create_routine_priv | Alter_routine_priv | Execute_priv | Event_priv | Trigger_priv |
+-----------+--------------------+--------------------+-------------+-------------+-------------+-------------+-------------+-----------+------------+-------------+
| localhost | PERCONA_SCHEMA | mysql.pxc.sst.role | N | N | N | N | Y | N | N | N | N | N | N | N | N | N | N | N | N | N | N |
| localhost | percona_schema | mysql.pxc.sst.role | N | N | N | N | Y | N | N | N | N | N | N | N | N | N | N | N | N | N | N |
```

This produces a duplicate entry for the percona_schema database and a warning message on the mysql.log.

**Reported Affected Version/s**: 8.0.21-12.1, 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 8.0.42, 8.4.5

<hr>

[PXC-4657](https://perconadev.atlassian.net/browse/PXC-4657): When executing DML and DDL on the same table, the DML will get a deadlock error. If the DML does not change the data but matches, it won't be replicated, for example.

```
mysql > UPDATE test.t SET d = d LIMIT 1;
Query OK, 0 rows affected (0.01 sec)
Rows matched: 1  Changed: 0  Warnings: 0

If the table contains a trigger, the DML does not get a deadlock error and will be replicated to other nodes.

CREATE TRIGGER `t_on_update` 
AFTER UPDATE ON `t`
FOR EACH ROW 
BEGIN
    INSERT INTO t_history (`d`)
    VALUES (NEW.`d`);
END
```

When other nodes apply the DML and DDL, the applier threads will get an MDL BF-BF conflict.

**Reported Affected Version/s**: 8.0.40, 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Using a single applier thread will skip the bug, but it may introduce a performance issue, such as flow control.

**Fixed/Planned Version/s**: 8.0.42, 8.4.5

<hr>

[PXC-4664](https://perconadev.atlassian.net/browse/PXC-4664): Converting thd->rli_slave to target type Slave_worker* causes a segmentation fault.

**Reported Affected Version/s**: 8.0.41

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

## Percona Toolkit

[PT-2392](https://perconadev.atlassian.net/browse/PT-2392): pt-online-schema-change resume functionality doesn't work with ADD INDEX

**Reported Affected Version/s**: 3.6.0, 3.7.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.7.1

[PT-2322](https://perconadev.atlassian.net/browse/PT-2322): The issue reports that pt-mysql-summary does not correctly detect and display the jemalloc memory management library, even when it is enabled. Despite jemalloc being loaded and visible in the process memory map (/proc/<mysqld_pid>/maps), the output from pt-mysql-summary is missing this information in some cases, unlike version 3.2.1, which correctly identifies and reports it.

**Reported Affected Version/s**: 3.5.6, 3.5.7\
**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.7.1

<hr>

[PT-2422](https://perconadev.atlassian.net/browse/PT-2422): When using the --history option with pt-online-schema-change (pt-osc), the query responsible for updating the history entry with the new_table_name is not appropriately constrained by a primary or unique key. As a result, this UPDATE operation can inadvertently modify all entries in the history table, rather than just the intended row.

This behavior can lead to significant issues when running multiple schema change operations in parallel, as the history entries for different migrations may interfere with each other, causing data consistency problems.

Additionally, if a migration is paused and later resumed, this lack of key constraint can result in only a subset of the data being correctly copied to the new table, potentially leading to partial data loss or corruption when the final table swap occurs.

**Reported Affected Version/s**: 3.5.6, 3.5.7\
**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.7.1

<hr>

[PT-2442](https://perconadev.atlassian.net/browse/PT-2442): Multiple security vulnerabilities have been identified in the latest version of Percona Toolkit, including:

<hr>

[CVE-2024-56171](https://nvd.nist.gov/vuln/detail/CVE-2024-56171): Use-After-Free Vulnerability in libxml2

<hr>

[CVE-2024-12797](https://nvd.nist.gov/vuln/detail/CVE-2024-12797): OpenSSL Raw Public Key Authentication Vulnerability

<hr>

[CVE-2022-37967](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-37967): Windows Kerberos Elevation of Privilege Vulnerability

<hr>

[CVE-2025-24928](https://nvd.nist.gov/vuln/detail/CVE-2025-24928): Stack-Based Buffer Overflow in libxml2

It is recommended that the associated advisories be reviewed and the necessary patches or upgrades be applied to mitigate the risk.

**Reported Affected Version/s**: 3.7.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.7.0-1

<hr>

## PMM (Percona Monitoring and Management)

[PMM-13694](https://perconadev.atlassian.net/browse/PMM-13694): When using a non-default pg_stat_statements.max value, the calculated QPS displayed in QAN may be wrong.

**Reported Affected Version/s**: 2.38.0, 2.44.0\
**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.2.0

<hr>

[PMM-13807](https://perconadev.atlassian.net/browse/PMM-13807): pmm-agent crashed at query.Fingerprint due to query including a column named "value"

**Reported Affected Version/s**: 2.44.0, 3.0.0

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.2.0

<hr>

[PMM-13847](https://perconadev.atlassian.net/browse/PMM-13847): PMM 3.0 doesn't support running on a different uid/gid in Kubernetes

**Reported Affected Version/s**: 3.0.0

[PMM-13984](https://perconadev.atlassian.net/browse/PMM-13984): Percona Monitoring and Management (PMM) version 3.1 with OVA image currently cannot be imported into VMware environments.

**Reported Affected Version/s**: 3.1.0

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

[PMM-12784](https://perconadev.atlassian.net/browse/PMM-12784): This error invalid GetActionRequest.ActionId: value length must be at least 1 runes. occurs in the QAN (Query Analytics) dashboard, indicating that the ActionId field in the GetActionRequest is empty or improperly formatted. This typically results from a missing or incorrectly populated Action ID parameter, which is required for retrieving query data.

**Reported Affected Version/s**: 2.33.0, 2.41.0, 2.44.0, 3.0.0

**Upstream Bug**: Not Available

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 3.2.0

<hr>

## Percona XtraBackup

[PXB-3421](https://perconadev.atlassian.net/browse/PXB-3421): XtraBackup fails when the --databases parameter contains a very long list of databases or has a large amount of whitespace before the actual database names. When the --databases parameter is provided with 1859 whitespace characters before a table name (e.g., db01.t1), XtraBackup crashes with a signal error. If the number of whitespace characters is reduced to 1858 or fewer, the backup proceeds successfully without error.

**Reported Affected Version/s**: 8.0.35-31

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

[PXB-3426](https://perconadev.atlassian.net/browse/PXB-3426): Using KMIP component causes double free of memory on error paths.

**Reported Affected Version/s**: 8.0.35-31

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 8.0.35-33, 8.4.0-3

<hr>

[PXB-3392](https://perconadev.atlassian.net/browse/PXB-3392): xtrabackup doesn't pick up --innodb-log-group-home-dir config parameter

**Reported Affected Version/s**: 8.0.35-30, 8.0.35-31, 8.0.35-32

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

## Percona Kubernetes Operator

[K8SPG-703](https://perconadev.atlassian.net/browse/K8SPG-703): When using ttlSecondsAfterFinished, there is a potential race condition where the backup jobs may be deleted before the Percona operator has had sufficient time to reconcile the perconapgbackups objects. This issue can occur even with relatively long timeouts like 1m, 5m, or 30m, not just extremely short intervals.

**Reported Affected Version/s**: 2.5.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 2.7.0

<hr>

[K8SPSMDB-1263](https://perconadev.atlassian.net/browse/K8SPSMDB-1263): While creating a 1.3TB logical backup, the replica's state changes to "errored" after approximately 16 hours with the message:

"failed to find CERTIFICATE"

despite the backup continuing to run and eventually completing. This raises concerns about the validity of the backup and the ability to restore from it without manually altering its status to "success."

**Reported Affected Version/s**: 1.13.0, 1.14.0, 1.15.0, 1.19.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 1.20.0

<hr>

[K8SPSMDB-1292](https://perconadev.atlassian.net/browse/K8SPSMDB-1292): When spec.tls.mode is set to requireTLS, physical backup restores fail with a "server selection timeout" error. This occurs because the operator cannot establish a secure connection to the MongoDB server, resulting in closed socket errors and the inability to disable Point-in-Time Recovery (PiTR).

**Reported Affected Version/s**: 1.19.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 1.21.0

<hr>

[K8SPSMDB-1294](https://perconadev.atlassian.net/browse/K8SPSMDB-1294): When using MCS on GKE 1.30, an API version mismatch occurs, resulting in the error:

"no matches for kind 'ServiceImport' in version 'net.gke.io/v1alpha1'"

This indicates that the expected ServiceImport kind is not available in the specified API version, preventing proper service discovery.

**Reported Affected Version/s**: 1.19.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 1.20.0

<hr>

[K8SPSMDB-1336](https://perconadev.atlassian.net/browse/K8SPSMDB-1336): Restoring a backup into a new Kubernetes cluster can lead to "Time monotonicity violation" errors on config servers and mongos, causing the pods to restart. This occurs when the restored chunk version timestamps are earlier than the expected timestamps in the new cluster, resulting in tripwire assertions and persistent crashes.

**Reported Affected Version/s**: 1.19.1

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: To Be Determined

<hr>

[K8SPXC-1548](https://perconadev.atlassian.net/browse/K8SPXC-1548): Failed to delete old backups on Google Cloud Storage

**Reported Affected Version/s**: 1.14.0, 1.15.1

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 1.18.0

## PBM (Percona Backup for MongoDB)

[PBM-1482](https://perconadev.atlassian.net/browse/PBM-1482): Selective Restore with replset-remapping hangs on oplog replay and doesn't finish

**Reported Affected Version/s**: 2.5.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 2.10.0

<hr>

[PBM-1487](https://perconadev.atlassian.net/browse/PBM-1487): Error Location6493100 on mongos after successful logical restore or PITR

**Reported Affected Version/s**: 2.8.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 2.10.0

<hr>

[PBM-1531](https://perconadev.atlassian.net/browse/PBM-1531): PBM Restore getting randomly stuck

**Reported Affected Version/s**: 2.6.0, 2.7.0, 2.8.0, 2.9.0

**Upstream Bug**: Not Applicable

**Workaround/Fix**: Not Available

**Fixed/Planned Version/s**: 2.10.0

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).

Quick References:

[Percona JIRA](https://jira.percona.com)

[MySQL Bug Report](https://bugs.mysql.com/)

[Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)
