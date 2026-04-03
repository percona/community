---
title: "Percona Bug Report: March 2026"
date: "2026-04-03T00:00:00+00:00"
tags: ['Percona Server/MySQL', 'Percona XtraDB Cluster', 'Percona XtraBackup', 'Percona Toolkit', 'PMM', 'Kubernetes Operator', 'PBM', 'PSMDB', 'Percona Distribution for MySQL', 'Orchestrator', 'PCSM', 'PG_TDE']
categories: ['MySQL', 'MongoDB', 'PostgreSQL', 'Kubernetes', 'Backup', 'Monitoring', 'Toolkit']
authors:
  - aaditya_dubey
images:
  - blog/2026/04/BugReportMarch2026.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://perconadev.atlassian.net/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs.

---

## Percona Server/MySQL Bugs

[PS-10378](https://perconadev.atlassian.net/browse/PS-10378): In the MeCab plugin, BOOLEAN MODE full-text queries with a LIMIT clause do not behave as expected. Although the optimizer indicates that ranking should be skipped (Ft_hints: no_ranking), the query still performs full ranking and sorting before applying LIMIT, preventing the intended optimization and impacting performance.

**Reported Affected Version/s**: 8.4.x  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 8.0.46-37, 8.4.9-9, 9.7.0-0

---

[PS-10448](https://perconadev.atlassian.net/browse/PS-10448): Insert prepared statements fail on partitioned tables with timestamp-based partitions when the partition key uses a non-constant default (e.g., **CURRENT_TIMESTAMP**). After initial execution, the statement remains bound to the original partition and fails with a partition mismatch error when data should go into a different partition.

**Reported Affected Version/s**: 8.0.42-33, 8.0.43-34, 8.0.44-35, 8.4.7-7  
**Upstream Bug**: [Bug #119309](https://bugs.mysql.com/bug.php?id=119309)  
**Workaround/Fix**: Modify statements to explicitly use **NOW()** (requires updating procedures)  
**Fixed/Planned Version/s**: 8.0.46-37, 8.4.9-9, 9.7.0-0

---

[PS-10481](https://perconadev.atlassian.net/browse/PS-10481): The range optimizer incorrectly falls back to a full table scan instead of using an index range scan for WHERE ... IN() queries when values exceed column or prefix length on non-binary collations (e.g. utf8mb4_0900_ai_ci). A single truncated value in IN() can invalidate all valid ranges, forcing a full scan and degrading performance.

**Reported Affected Version/s**: 8.4.x  
**Upstream Bug**: [Bug #118009](https://bugs.mysql.com/bug.php?id=118009)  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: Not fixed yet

---

[PS-10593](https://perconadev.atlassian.net/browse/PS-10593): The audit_log plugin can crash (segfault) during memcpy operations when configured with audit_log_strategy=PERFORMANCE, audit_log_policy=ALL, and buffering enabled. The issue can be reproduced under specific memory allocator setups (e.g., jemalloc) and also occurs with standard libc malloc, indicating instability in the plugin’s memory handling.

**Reported Affected Version/s**: 8.0.34-26, 8.0.45-36, 8.4.7-7  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 8.0.46-37, 8.4.9-9

---

[PS-10990](https://perconadev.atlassian.net/browse/PS-10990): Server crashes (signal 11) in Item_cache::walk when executing queries that use JOIN with a subquery in an IN clause inside stored procedures. The issue occurs during query execution/privilege checking and is reproducible across MySQL and Percona Server 8.0.x versions.

**Reported Affected Version/s**: 8.0.45-36  
**Upstream Bug**: [Bug #115885](https://bugs.mysql.com/bug.php?id=115885)  
**Workaround/Fix**: Execute the query outside the stored procedure  
**Fixed/Planned Version/s**: Not specified

---

[PS-10578](https://perconadev.atlassian.net/browse/PS-10578): The legacy audit_log plugin does not populate the DB field in audit records unless the session is started with the --database option. Even when a database is selected later using USE or referenced explicitly in queries, the DB field may remain empty.

**Reported Affected Version/s**: 8.0.43-34, 8.0.45-36  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Use Audit Log Filter component (8.4) or audit log filter (8.0), where this issue is not reproducible  
**Fixed/Planned Version/s**: Not planned to be fixed

---

## Percona Xtradb Cluster

[PXC-4844](https://perconadev.atlassian.net/browse/PXC-4844): In PXC clusters under high load, inconsistency voting during DDL or DCL operations can trigger an internal deadlock, causing standby nodes to get stuck applying transactions and continuously request FC pause. Although voting completes successfully and no node is expelled, writes remain blocked in wsrep: replicating and certifying write set, effectively stalling the cluster until the affected node is restarted.

**Reported Affected Version/s**: 8.0.42  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Restart the blocked standby node to restore cluster activity  
**Fixed/Planned Version/s**: Not fixed yet  

---

[PXC-4799](https://perconadev.atlassian.net/browse/PXC-4799): In PXC clusters, when a backup lock (**LOCK INSTANCE FOR BACKUP**) is active and a replicated DDL is pending, executing **FLUSH TABLES WITH READ LOCK** on the same node can trigger a deadlock. This results in an inconsistency vote and causes the node to leave the cluster, disrupting backup operations.

**Reported Affected Version/s**: 8.0.42, 8.0.43, 8.4.6  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Avoid running DDL operations during backup or use a single backup instance instead of parallel runs  
**Fixed/Planned Version/s**: 8.0.46, 8.4.9, 9.7.0  

---

[PXC-4814](https://perconadev.atlassian.net/browse/PXC-4814): In PXC with **wsrep_OSU_method='RSU'**, a failed DDL due to table name case mismatch (e.g., **OPTIMIZE TABLE**) is incorrectly written to the binary log as a successful transaction (**error_code=0**). This results in a GTID being generated for a failed operation, causing GTID inconsistencies across cluster nodes and in replication setups.

**Reported Affected Version/s**: 8.0.33-25, 8.0.44, 8.4.6  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Validate table name case sensitivity before executing DDL in RSU mode  
**Fixed/Planned Version/s**: 8.0.45, 8.4.8, 9.6.0  

---

[PXC-4845](https://perconadev.atlassian.net/browse/PXC-4845): After an IST failure (e.g., due to network issues), a PXC node may remain running in an inconsistent state instead of restarting, causing the donor and other nodes to become unresponsive. The joiner node gets stuck during state transfer instead of failing cleanly, impacting overall cluster availability.

**Reported Affected Version/s**: 8.0.42  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 8.0.45, 8.4.8, 9.6.0  

---

[PXC-4849](https://perconadev.atlassian.net/browse/PXC-4849): A PXC node fails to start after successful SST when **read_only** or **super_read_only** is enabled and event scheduler objects exist on the donor. During initialization, the event scheduler fails to load, causing the node to abort, making it impossible to run read-only nodes with events defined in the cluster.

**Reported Affected Version/s**: 8.0.44, 8.4.7  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Start the node without read_only, then enable it manually later, or remove events  
**Fixed/Planned Version/s**: 8.0.46, 8.4.9, 9.7.0  

---

[PXC-4965](https://perconadev.atlassian.net/browse/PXC-4965): Passwords containing the `'` character are incorrectly handled, causing syntax errors during replication (e.g., **SET PASSWORD**) and triggering inconsistency voting that can force a node to leave the cluster.

**Reported Affected Version/s**: 8.0.45, 8.4.7  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Avoid using `'` character in passwords  
**Fixed/Planned Version/s**: 8.0.46, 8.4.8, 9.6.0  

---

[PXC-5198](https://perconadev.atlassian.net/browse/PXC-5198): Executing **SELECT ... FOR UPDATE SKIP LOCKED** can trigger InnoDB crashes with fatal errors (e.g., “Unknown error code 21: Skip locked records”) under concurrent transactional workloads. Instead of returning expected deadlock errors, the query causes mysqld to abort, impacting cluster stability.

**Reported Affected Version/s**: 8.0.33-25, 8.0.35-27, 8.0.36-28  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Avoid using **SKIP LOCKED** in **SELECT ... FOR UPDATE** queries  
**Fixed/Planned Version/s**: 8.0.46, 8.4.8, 9.6.0  

---

## Percona XtraBackup

[PXB-3543](https://perconadev.atlassian.net/browse/PXB-3543): Incremental backups in XtraBackup can become significantly slower than full backups on instances with a very large number of small tables, due to excessive CPU usage in memset during incremental processing. This leads to severe performance degradation, with incremental backups taking hours compared to minutes for full backups.

**Reported Affected Version/s**: 8.0.35-33, 8.0.35-34  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Use full backups instead of incremental backups  
**Fixed/Planned Version/s**: 8.0.35-35, 8.4.0-6, 9.6.0-1  

---

[PXB-3667](https://perconadev.atlassian.net/browse/PXB-3667): Installation of XtraBackup 8.4 fails on RHEL 9–based systems due to dependency conflicts between percona-xtrabackup-84, perl(DBD::mysql), and incompatible libmysqlclient versions. Percona Server 8.4 provides libmysqlclient.so.24, while required dependencies expect libmysqlclient.so.21, resulting in unresolved package installation errors.

**Reported Affected Version/s**: 8.4.0-5  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: Not specified  

---

## Percona Toolkit

[PT-2519](https://perconadev.atlassian.net/browse/PT-2519): pt-query-digest fails when processing large, slow query logs, repeatedly throwing “Argument "" isn't numeric” errors during the aggregate fingerprint stage. The tool retries multiple times but does not complete, resulting in stalled analysis and very slow progress.

**Reported Affected Version/s**: 3.7.0, 3.7.1  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 3.7.3  

---

[PT-2511](https://perconadev.atlassian.net/browse/PT-2511): pt-summary incorrectly reports that sshd is not running due to an invalid awk expression used to detect the process. The script checks the wrong field in ps output, causing false negatives even when sshd is active.

**Reported Affected Version/s**: 3.7.1  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 3.7.3  

---

[PT-2516](https://perconadev.atlassian.net/browse/PT-2516): pt-mongodb-index-check fails to detect duplicate indexes (e.g., `{a:1}` and `{a:1, b:1}`) and may produce no output, making it unclear whether the tool is functioning or connecting properly.

**Reported Affected Version/s**: 3.7.1  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: Not specified  

---

## PMM [Percona Monitoring and Management]

[PMM-14493](https://perconadev.atlassian.net/browse/PMM-14493): PMM fails to start when using Podman with the **--log-driver passthrough** option due to an error opening /dev/stderr during Nginx initialization. This causes the container to exit with configuration test failure, while other log drivers work as expected.

**Reported Affected Version/s**: 3.4.0, 3.4.1  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Use a different **--log-driver** option such as none or journald  
**Fixed/Planned Version/s**: 3.8.0  

---

[PMM-14576](https://perconadev.atlassian.net/browse/PMM-14576): PMM Client reports “failed to get backup status” errors during MongoDB backups, marking them as failed in the UI even though backups are successfully completed by PBM. This leads to incorrect backup status reporting and confusion for users.

**Reported Affected Version/s**: 3.5.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Avoid using PMM Backup Management (not ideal)  
**Fixed/Planned Version/s**: 3.9.0, 3.X  

---

[PMM-14594](https://perconadev.atlassian.net/browse/PMM-14594): PMM incorrectly reports compatible XtraBackup versions as incompatible with supported MySQL versions during backup validation. This causes backups to be blocked in PMM even when the installed XtraBackup version is the latest available and should be accepted.

**Reported Affected Version/s**: 3.5.0, 3.6.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Use the xtrabackup command-line tool to take backups  
**Fixed/Planned Version/s**: 3.9.0  

---

[PMM-14852](https://perconadev.atlassian.net/browse/PMM-14852): Some panels in the MongoDB InMemory dashboard show no data because they incorrectly use WiredTiger-specific metrics. As a result, dashboards for InMemory storage engine deployments can display empty or misleading panels instead of relevant metrics.

**Reported Affected Version/s**: 3.2.0, 3.6.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 3.8.0  

---

[PMM-14906](https://perconadev.atlassian.net/browse/PMM-14906): The postgres_exporter generates excessive **SELECT version()** queries (~4500/hour) after upgrading to PMM 3.6.0, flooding PostgreSQL logs and increasing unnecessary query load, causing log spam and disk growth.

**Reported Affected Version/s**: 3.6.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 3.8.0  

---

[PMM-14958](https://perconadev.atlassian.net/browse/PMM-14958): mysqld_exporter continues to generate duplicate metric collection errors with GTID and parallel replication enabled, even in PMM 3.6.0. These repeated errors (e.g., **mysql_perf_schema_replication_group_worker_transport_time_seconds**) lead to continuous log spam, causing rapid log growth (up to ~10GB/hour), disk space exhaustion, and increased noise that makes it difficult to identify real issues.

**Reported Affected Version/s**: 3.6.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 3.7.1  

---

## Percona Kubernetes Operator

[K8SPG-737](https://perconadev.atlassian.net/browse/K8SPG-737): In PostgreSQL Kubernetes deployments, the node_exporter in the PMM client sidecar cannot access the datadir mountpoint because it is not exposed via /proc, preventing collection of datadir-related metrics. This results in incomplete monitoring data for PostgreSQL pods.

**Reported Affected Version/s**: 2.9.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 2.10.0  

---

[K8SPXC-1737](https://perconadev.atlassian.net/browse/K8SPXC-1737): The PXC Operator crashes during reconciliation in CompareMySQLVersion when the cluster status lacks a MySQL version value. An empty version field causes a panic (“Malformed version”), preventing proper cluster reconciliation and replication setup.

**Reported Affected Version/s**: 1.18.0, 1.19.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Create the cluster before configuring replication or manually patch the CR status to include the missing version value, for example:
```
kubectl patch pxc <cluster-name> \
  --type=merge \
  --subresource=status \
  --patch '
status:
  pxc:
    version: "8.0.42-33.1"'
```
**Fixed/Planned Version/s:** 1.20.0

---

[K8SPXC-1843](https://perconadev.atlassian.net/browse/K8SPXC-1843): Backups can get stuck in a Running state if the Joiner/Garbd disconnects from the Donor (e.g., due to sst-idle-timeout). Even after the SST process fails and the donor leaves the cluster, the backup process (e.g., xbcloud put) continues indefinitely without timing out, preventing backup completion.

**Reported Affected Version/s**: 1.19.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 1.20.0  

---

[K8SPXC-1831](https://perconadev.atlassian.net/browse/K8SPXC-1831): When using mysqlAllocator=jemalloc on ARM images, the operator attempts to preload /usr/lib64/libjemalloc.so.1, but only libjemalloc.so.2 is available. This results in preload errors and prevents proper use of the jemalloc allocator.

**Reported Affected Version/s**: 1.19.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 1.20.0  

---

[K8SPXC-1830](https://perconadev.atlassian.net/browse/K8SPXC-1830): ProxySQL monitoring fails in PMM when using caching_sha2_password, causing proxysql_exporter to fail authentication with errors like:

```
Error opening connection to ProxySQL:
unexpected resp from server for caching_sha2_password, perform full authentication

```
This occurs because ProxySQL does not support the required RSA-based full authentication, breaking PMM monitoring integration.
**Reported Affected Version/s**: 1.19.0
**Upstream Bug**: Not applicable
**Workaround/Fix**: Use mysql_native_password
**Fixed/Planned Version/s**: 1.20.0

---

[K8SPSMDB-1617](https://perconadev.atlassian.net/browse/K8SPSMDB-1617): Scheduled backups can be triggered even when the MongoDB cluster is not ready (e.g., in initializing state) and without the required safety flags. This leads to failed backup attempts and inconsistent backup behaviour.

**Reported Affected Version/s**: 1.22.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: Not specified  

---

[K8SPSMDB-1524](https://perconadev.atlassian.net/browse/K8SPSMDB-1524): The PBM agent continuously triggers resync storage operations, causing backup processes to stall or remain in pending/unknown states. Logs show repeated resync commands being executed without completion, leading to unstable backup behaviour.

**Reported Affected Version/s**: 1.21.1  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 1.22.0  

---

[K8SPG-939](https://perconadev.atlassian.net/browse/K8SPG-939): Patroni does not propagate labels defined in the PostgreSQL Operator CR, causing failures in environments with strict label policies. As a result, Kubernetes rejects resource creation (e.g., Services) due to missing mandatory labels, preventing cluster reconciliation.

**Reported Affected Version/s**: 2.8.2  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 2.9.0  

---

## PBM [Percona Backup for MongoDB]

[PBM-1683](https://perconadev.atlassian.net/browse/PBM-1683): The size_uncompressed_h field in pbm describe-backup reports incorrect (inflated) sizes for non-base incremental backups, showing significantly larger values than the actual data size and leading to misleading backup size reporting.

**Reported Affected Version/s**: 2.10.0, 2.11.0, 2.12.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 2.14.0  

---

## PSMDB [Percona Server for MongoDB]

[PSMDB-1915](https://perconadev.atlassian.net/browse/PSMDB-1915): Newer PSMDB packages fail to install or upgrade on RHEL 9.4 due to a dependency on OpenSSL 3.4, which is not available in that OS version. This breaks upgrades (e.g., from 6.0.25 to 6.0.27) and affects multiple major versions.

**Reported Affected Version/s**: 6.0.27-21, 7.0.28-15, 8.0.17-6  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 6.0.27-21, 7.0.28-15, 8.0.17-6  

---

[PSMDB-1998](https://perconadev.atlassian.net/browse/PSMDB-1998): LDAP authentication can hang indefinitely when the LDAP server is unreachable due to missing timeout handling. This leads to continuously accumulating connections, eventually exhausting file descriptors and causing service disruption or crashes.

**Reported Affected Version/s**: 7.0.16-10, 7.0.30-16  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: No workaround available  
**Fixed/Planned Version/s**: 7.0.31-17, 8.0.20-8  

---

## Percona Distribution for MySQL [Orchestrator]

[DISTMYSQL-584](https://perconadev.atlassian.net/browse/DISTMYSQL-584): Orchestrator loses SSL-related settings such as SOURCE_SSL_CA and SOURCE_SSL_VERIFY_SERVER_CERT during failover when issuing CHANGE REPLICATION SOURCE, causing replication to run without required security configurations and potentially violating compliance requirements.

**Reported Affected Version/s**: 8.4.7  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: Not specified  

---

## PCSM [Percona ClusterSync for MongoDB]

[PCSM-294](https://perconadev.atlassian.net/browse/PCSM-294): PCSM replication can crash during change replication due to flawed conflict detection and unbatched pipeline generation. This results in oversized aggregation pipelines, memory exhaustion, or invalid $slice operations, causing replication to fail with errors such as stage limit exceeded, buffer limits, or invalid arguments.

**Reported Affected Version/s**: 0.7.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: 0.8.0  

---

## PG_TDE [Percona Transparent Data Encryption for PostgreSQL]

[PG-2125](https://perconadev.atlassian.net/browse/PG-2125): pg_tde fails to create/register symmetric keys when using HashiCorp KMIP, returning errors from the KMIP server during key registration. This prevents key setup and blocks encryption workflows for users relying on KMIP integration.

**Reported Affected Version/s**: pg_tde 2.1.0  
**Upstream Bug**: Not applicable  
**Workaround/Fix**: Not specified  
**Fixed/Planned Version/s**: pg_tde NEXT

---

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).

Quick References:

[Percona JIRA](https://jira.percona.com)

[MySQL Bug Report](https://bugs.mysql.com/)

[Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)
