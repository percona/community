---
title: "Percona Monthly Bug Report: February/March 2024"
date: "2024-04-29T00:00:00+00:00"
tags: ['Percona', 'opensource', 'PMM', 'Kubernetes', 'MySQL', 'PostgreSQL']
authors:
  - aaditya_dubey
images:
  - blog/2024/04/BugReportApril2024.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://jira.percona.com/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs,

## Percona Server/MySQL Bugs

[PS-9092](https://perconadev.atlassian.net/browse/PS-9092): A query over an InnoDB table that uses a backward scan over the index occasionally might return incorrect/incomplete results when changes to the table (for example, DELETEs in another or even the same connection followed by asynchronous purge) cause concurrent B-tree page merges.

**Reported Affected Version/s:** 5.7.44, 8.0.35, 8.0.36

**Upstream Bug:** [114248](https://bugs.mysql.com/bug.php?id=114248)

**Workaround/Fix:** Use descending indexes for the primary key. E.g.: 

```
CREATE TABLE bugTest.testTable (key int unsigned, version bigint unsigned, rowmarker char(3) not null default 'aaa', value MEDIUMBLOB, PRIMARY KEY (key DESC, version DESC)) Engine=InnoDB;
```

[PS-9107](https://perconadev.atlassian.net/browse/PS-9107): A delete/insert into the secondary index is being change-buffered. This causes an insert into the 'ibuf' tree. There is a limit on the maximum size of the ibuf. So, on every ibuf insert, there is a compaction of ibuf tree (ibuf_contract). As part of ibuf_contract, we randomly open an ibuf page and apply the ibuf entries to the actual secondary index pages. After applying these ibuf entries from ibuf index, the ibuf tree goes on merging pages (optimistic vs pessimistic btree operations). To do this ibuf pessimistic delete on the tree, we save the cursor position, commit mtr and do a restore. This restore does a search and position again on the ibuf entry we were processing earlier, causing [MY-013183] [InnoDB] Assertion failure: ibuf0ibuf.cc:3833:ib::fatal triggered thread.

**Reported Affected Version/s:** 8.0.34-26, 8.0.35-27, 8.0.36-28

**Fixed Version:** PS 8.0.37-29 [Yet to Release]

**Upstream Bug:** [114135](https://bugs.mysql.com/bug.php?id=114135)

**Workaround/Fix:**  Disable [innodb_change_buffering](https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_change_buffering)

[PS-9115](https://perconadev.atlassian.net/browse/PS-9115): MySQL crashes due to getting a native index from get_mutex_cond in group replication, and before the crash, the following set of warnings/Errors is generated:

```
[Warning] [MY-011630] [Repl] Plugin group_replication reported: 'Due to a plugin error, some transactions were unable to be certified and will now rollback.'

[ERROR] [MY-011631] [Repl] Plugin group_replication reported: 'Error when trying to unblock non certified or consistent transactions. Check for consistency errors when restarting the service'
```

**Reported Affected Version/s:** 8.0.35-27

**Fixed Version:** The fix is in progress and expected to be included in an upcoming release of Percona Servers.

**Workaround/Fix:** We can not guarantee that the bug will be avoided 100%, but shutting down/stopping group replication off-hours when the workload recedes should prevent the situation.

[PS-9121](https://perconadev.atlassian.net/browse/PS-9121): InnoDB updates the primary index but not the spatial index, which eventually corrupts the spatial index. The MySQL server crashes with "[ERROR] [MY-013183] [InnoDB] Assertion failure: row0ins.cc:268:!cursor->index->is_committed()." The update query changes the data from point(0.0000000000000099,0) to point(0.00000000000001,  0). When Innodb updates the record containing a spatial index, It updates the clustered index. This issue can be repeated using the following set of SQL statements.

```
CREATE TABLE a

  (

     id INT PRIMARY KEY,

     a  GEOMETRY NOT NULL,

     SPATIAL KEY (a)

  )

ENGINE=InnoDB;

INSERT INTO a VALUES (1,POINT(0.0000000000000099, 0));

UPDATE a SET a = Point(0.00000000000001, 0);

DELETE FROM a WHERE  id = 1;

INSERT INTO a VALUES  (1,POINT(0.0000000000000099, 0));
```

**Reported Affected Version/s:** 8.0.36-28, 8.X [Innovative Release]

**Fixed Version:** The fix is in progress and expected to be included in an upcoming release of Percona Servers.

**Upstream Bug:** [114252](https://bugs.mysql.com/bug.php?id=114252)

**Workaround/Fix:** Please consider resetting the shape to a different value from the new values.

[PS-9109](https://perconadev.atlassian.net/browse/PS-9109): The Percona server's slow query rate is not accurately logged, which is controlled via the [Log_slow_rate_type](https://docs.percona.com/percona-server/8.0/slow-extended.html?h=log_slow_rate_type#log_slow_rate_type) and [Log_slow_rate_limit](https://docs.percona.com/percona-server/8.0/slow-extended.html?h=log_slow_rate_type#log_slow_rate_limit) variables. Due to this issue, the slow query log records every query regardless of these variables' values.

**Reported Affected Version/s:** 8.0.35-27

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona Servers.

## Percona Xtradb Cluster

[PXC-4380](https://perconadev.atlassian.net/browse/PXC-4380): In a large cluster, for example, 15 nodes, in case one node has network issues and disconnects/re-connects/disconnects, the cluster might be sent to a non-primary state if the evs.install_timeout is reached.

**Reported Affected Version/s:** 5.7.42-31-65, 8.0.33-25, 8.0.35-27

**Fixed Version:** In such a big cluster, reaching consensus between nodes takes more time, so evs.install_timeout has to be adjusted. We can also configure the cluster to evict unresponsive nodes by setting evs.auto_evict=1. So, after investigation, we found that no fix is required, as everything works as expected/designed.

**Workaround/Fix:** Increasing the evs.install_timeout might fix the issue. The maximum value is 15S, which can still be reached depending on cluster size and how bad the flapping is.

```
The default value for evs.install_timeout is evs.inactive_timeout/2.

The minimum value is evs.join_retrans_period

The maximum time is evs.inactive_timeout + 1
```

So, If we keep defaults:

```
evs.join_retrans_period = 1s

evs.inactive_timeout = 15s

evs.install_timeout (default) = 7.5s

evs.install_timeout(min) = 1s

evs.install_timeout(max) = 16s
```

Please note that 15s is not a hard limit and is determined by evs.inactive_timeout

We have set wsrep_provider_options="evs.install_timeout=PT15S" for all nodes in the test environment and are now unable to reproduce the issue. So, we are on some timeout boundaries, and the above configuration parameters were introduced to fine-tune in such environments.

[PXC-4367](https://perconadev.atlassian.net/browse/PXC-4367): Innodb semaphore wait timeout failure seen after upgrade from 8.0.34 to 8.0.35. This issue is a possible side effect of this [patch](https://github.com/percona/percona-xtradb-cluster/pull/1854), Where PXC node acts as the async replica to some master and in parallel, the row is updated on PXC node and via replication, the PXC node hangs. To avoid the issue, upgrading to PXC 8.0.36 is recommended.

**Reported Affected Version/s:** 8.0.35-27

**Fixed Version:** 8.0.36-28

[PXC-4363](https://perconadev.atlassian.net/browse/PXC-4363): Concurrent CREATE and DROP USER queries on different nodes lead to permanent lock.

```
| 16 | system user  | db1 | Query | 411 | Waiting for table metadata lock | drop user IF EXISTS `msandbox_rw11`@`localhost` | 411380 | 0 |   
```

These queries cannot be cancelled or killed, and nodes refuse to be gracefully restarted. The shutdown is stuck with this forever. Only the forcible service kill helps restore the cluster.

```
2024-01-18T17:49:24.470428Z 0 [Note] [MY-000000] [Galera] Closing slave action queue.
```

**Reported Affected Version/s:** 8.0.35-27

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona Servers.

[PXC-4399](https://perconadev.atlassian.net/browse/PXC-4399): FLUSH TABLES during writes to the table with unique keys stall the cluster node; due to the stall, it's not possible to abort/kill any of the above connections. The node sends a permanent flow control pause. The only way to get out of this stall is to kill the node.

**Reported Affected Version/s:** 8.0.33-25, 8.0.35-27

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona Servers.

[PXC-4418](https://perconadev.atlassian.net/browse/PXC-4418): In MySQL, the optimizer creates a temp table definition with indexes, where 2 of them have the same name (<auto_key2>, <auto_key1>, <auto_key2>). When the query is executed, a temp table is created, then MySql tries to access <auto_key2>. In InnoDB, we search for index by name (dict_table_get_index_on_name()), which returns the wrong <auto_key2>. Then row_sel_convert_mysql_key_to_innobase() crashes as structures are not aligned. Please note this bug affects only very complicated queries with many JOINs and subqueries. To repeat this bug, the internal temporary table needs to be created at least for two parts of the query.

**Reported Affected Version/s:** 8.0.32-24, 8.0.34-26

**Fixed Version:** 8.0.36-28

## Percona Toolkit

[PT-2190](https://perconadev.atlassian.net/browse/PT-2190):The [pt-show-grants](https://docs.percona.com/percona-toolkit/pt-show-grants.html) use SHOW CREATE USER command to obtain grants from the MySQL server. By default, this query returns values as they are stored in the mysql.user table. When using caching_sha256_password, such hash of the password could contain a special character. Therefore, it would not be possible to use output printed by pt-show-grants to re-create users in the database. Since version 3.6.0, pt-show-grants checks if it runs against MySQL version 8.0.17 or higher and sets session option [print_identified_as_hex](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_print_identified_with_as_hex) to true before running SHOW CREATE USER command. This allows to print commands that could be used to re-create users.

**Reported Affected Version/s:** 3.5.1

**Fixed Version:** 3.6.0 [It is expected to be released soon]

[PT-2215](https://perconadev.atlassian.net/browse/PT-2215): pt-table-sync does not recognize the privileges in roles for MariaDB

**Reported Affected Version/s:** 3.5.2

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona ToolKit.

[PT-2316](https://perconadev.atlassian.net/browse/PT-2316): pt-config-diff with --pid option is broken with "Can't locate object method "make_PID_file" via package "Daemon" at /usr/bin/pt-config-diff line 5522" on Ubuntu 20.04

**Reported Affected Version/s:** 3.5.7

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona ToolKit.

[PT-2314](https://perconadev.atlassian.net/browse/PT-2314): pt-online-schema-change fails due to duplicate constraint names when it attempts to make a table copy for alteration.

**Reported Affected Version/s:** 3.5.7

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona ToolKit.

**Workaround/Fix:** Do not duplicate constraints name.

[PT-2322](https://perconadev.atlassian.net/browse/PT-2322): pt-mysql-summary does not detect jemalloc when installed as systemd.

**Reported Affected Version/s:** 3.5.6, 3.5.7

**Fixed Version:** The fix is expected to be included in an upcoming release of Percona ToolKit.

## PMM [Percona Monitoring and Management]

[PMM-11583](https://perconadev.atlassian.net/browse/PMM-11583): On MySQL 8.0, [innodb_redo_log_capacity](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_redo_log_capacity) supersedes [innodb_log_files_in_group](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_files_in_group) and [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size), which eventually breaks InnoDB Logging graphs. Due to this issue, the user can not determine whether the combined InnoDB redo log file size has to be increased or not.

**Reported Affected Version/s:** 2.41.1

**Fixed Version:** 2.41.3 [It is expected to be released soon]

[PMM-13017](https://perconadev.atlassian.net/browse/PMM-13017): For certain db.collection.find(query, projection, options) queries, the Explain tab for QAN returns an error message saying, "error decoding key command: invalid JSON input; expected value for 64-bit integer." Please note this issue specifically affects MongoDB monitoring.

**Reported Affected Version/s:** 2.35.0, 2.37.1, 2.41.1

**Fixed Version:** The fix is expected to be included in an upcoming release of PMM

[PMM-12522](https://perconadev.atlassian.net/browse/PMM-12522): When adding data relatively large chunks of data to MongoDB sharded cluster, pmm-agent log starts flooded with "level=error msg=\"cannot create metric for changelog... & level=error msg=\"Failed to get database names:..." which eventually shows MongoS as disconnected in PMM UI (PMM-Inventory/Services).

**Reported Affected Version/s:** 2.39.0, 2.40.0, 2.41.1

**Fixed Version:** 2.41.3 [It is expected to be released soon]

[PMM-12880](https://perconadev.atlassian.net/browse/PMM-12880): pmm-admin [--tls-skip-verify](https://docs.percona.com/percona-monitoring-and-management/details/commands/pmm-admin.html#mongodb) does not work when [x509 authentication](https://dev.mysql.com/doc/mysql-secure-deployment-guide/5.7/en/secure-deployment-user-accounts.html) is used.

**Reported Affected Version/s:** 2.41.0

**Fixed Version:** 2.41.3 [It is expected to be released soon]

[PMM-12989](https://perconadev.atlassian.net/browse/PMM-12989): PMM agent logs flooded with wrong log entries when monitoring auth-enabled arbiters. Please note this issue specifically affects MongoDB monitoring.

**Reported Affected Version/s:** 2.41.1

**Fixed Version:** 2.41.3 [It is expected to be released soon]

## Percona XtraBackup

[PXB-3251](https://perconadev.atlassian.net/browse/PXB-3251): When PXB fails to load the encryption key, the xtrabackup_logfile is still created in the target dir. This causes a second attempt at running PXB to fail with a new error. The [xtrabackup_logfile](https://docs.percona.com/percona-xtrabackup/8.0/xtrabackup-files.html?h=xtrabackup_logfile) file contains data needed to run the --prepare process. The bigger this file is, the longer the --prepare process will take to finish. So, PXB should not create any files on disk until the encryption key is loaded.

**Reported Affected Version/s:** 8.0.35-30

**Fixed Version:** The fix is expected to be included in future releases of PXB

## Percona Kubernetes Operator

[K8SPG-496](https://perconadev.atlassian.net/browse/K8SPG-496): When a PostgreSQL Database is set to a paused state via spec, the operator waits until all backups for the Database finish. After the backups finish, the PostgreSQL Database shall be paused, which is not happening.

**Reported Affected Version/s:** 2.3.0

**Fixed Version:** 2.3.1

[K8SPG-494](https://perconadev.atlassian.net/browse/K8SPG-494): High vulnerabilities found for pgbackrest, Postgres & pgbouncer package.

For pgbackrest and postgres: [CVE-2023-38408](https://nvd.nist.gov/vuln/detail/CVE-2023-38408)

For pgbouncer: [CVE-2023-32067](https://nvd.nist.gov/vuln/detail/CVE-2023-32067)

**Reported Affected Version/s:** 2.3.0

**Fixed Version:** 2.3.1

[K8SPG-521](https://perconadev.atlassian.net/browse/K8SPG-521): The upgrade path described in the [documentation](https://docs.percona.com/percona-operator-for-postgresql/2.0/update.html#update-database-and-operator-version-2x) leads to disabled built-in extensions(pg_stat_monitor, pg_audit).

**Reported Affected Version/s:** 2.3.1

**Fixed Version:** 2.4.0 [It is expected to be released soon]

[K8SPG-522](https://perconadev.atlassian.net/browse/K8SPG-522): Cluster is broken if PG_VERSION file is missing during the upgrade from 2.2.0 to 2.3.1.

**Reported Affected Version/s:** 2.3.1

**Fixed Version:** 2.4.0 [It is expected to be released soon]

**Workaround/Fix:** In order to fix the issue, please do the following:


1.  Create PG_VERSION with contents 14 in DB instance pod.

    `echo 14 > /pgdata/pg14/PG_VERSION`

2.  Apply crd and rbac

    `kubectl apply --force-conflicts --server-side -f crd.yaml`

    `kubectl -n operatornew apply --force-conflicts --server-side -f rbac.yaml`

3.  Restart the operator deployment.

    `kubectl -n operatornew rollout restart deployment percona-postgresql-operator`

4.  At this moment, patronictl show-config starts to enlist extensions.

    ```
    $ kubectl -n operatornew exec cluster1-instance1-gsvs-0 -it -- bash

    Defaulted container "database" out of: database, replication-cert-copy, postgres-startup (init), nss-wrapper-init (init)

    bash-4.4$ patronictl show-config

    loop_wait: 10

    postgresql:

      parameters:

        archive_command: pgbackrest --stanza=db archive-push "%p"

        archive_mode: 'on'

        archive_timeout: 60s

        huge_pages: 'off'

        jit: 'off'

        password_encryption: scram-sha-256

        pg_stat_monitor.pgsm_query_max_len: '2048'

        restore_command: pgbackrest --stanza=db archive-get %f "%p"

    shared_preload_libraries: pg_stat_monitor,pgaudit
    ```
5.  Now extensions appear in the \dx output without pod restarts, but all Postgresql servers will be restarted:


[K8SPG-547](https://perconadev.atlassian.net/browse/K8SPG-547): The pgbackrest container can't use pgbackrest 2.50. This is because pgbackrest 2.50 requires libssh2.so.1, which requires epel. Without that fix, microdnf installs pgbackrest 2.48, which creates inconsistency with the Postgresql container.

**Reported Affected Version/s:** 2.2.0

**Fixed Version:** 2.4.0 [It is expected to be released soon]

**Workaround/Fix:** This [patch](https://github.com/percona/percona-docker/pull/960) can be used until it is fixed.

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).

Quick References:

[Percona JIRA](https://jira.percona.com)

[MySQL Bug Report](https://bugs.mysql.com/)

[Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)

