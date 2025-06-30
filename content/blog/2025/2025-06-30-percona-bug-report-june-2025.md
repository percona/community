---
title: "Percona Bug Report: June 2025"
date: "2025-06-30T00:00:00+00:00"
tags: ['PMM', 'Kubernetes', 'MySQL', 'MongoDB', 'Percona', 'Opensource']
categories: ['PMM', 'Cloud', 'MySQL', 'MongoDB', 'Toolkit']
authors:
  - aaditya_dubey
images:
  - blog/2025/06/BugReportJune2025.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://jira.percona.com/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs.

### Percona Server/MySQL Bugs

[PS-9823](https://perconadev.atlassian.net/browse/PS-9823)**:** [mysql\_migrate\_keyring](https://dev.mysql.com/doc/refman/8.4/en/mysql-migrate-keyring.html) fails with PS Components.

The failure is triggered by a missing symbol, but the underlying cause is the way keyring components are built in Percona Server. When attempting to migrate keyring data (e.g., from Vault to File), the tool fails to load the Percona Server component .so files, making the migration process unusable.  
	  
Percona Server builds a reference to the my\_free symbol, which is not properly resolved in the shared libraries. In contrast, upstream MySQL builds do not include this dependency.

This issue blocks both component-to-component and component-to-plugin keyring migrations, affecting users who rely on secure key management transitions.

**Reported Affected Version/s:** 8.0.x, 8.4.x  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** Under investigation. A fix or workaround is expected in a future release.

<hr>

[PS-9836](https://perconadev.atlassian.net/browse/PS-9836)**:** There is a regression issue with [audit\_log\_filter.so](https://docs.percona.com/percona-server/8.0/audit-log-filter-overview.html) compared to [audit\_log.so](https://docs.percona.com/percona-server/8.0/audit-log-plugin.html). The audit\_log\_filter, whether used as a plugin (8.0) or a component (8.0 and 8.4), shows a significant performance regression. When logging everything, QPS drops by over 70%. While configuring selective logging can reduce the impact, it still results in a 30–35% drop in QPS.

For this reason, moving to audit\_log\_filter in 8.0 is not recommended. Additionally, this should be taken into account when planning upgrades to 8.4, as audit logging can significantly impact performance. (audit\_log is not available as a component—only as a plugin.)

**Reported Affected Version/s:** 8.0.42-33, 8.4.5-5  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** Under investigation. A fix or workaround is expected in a future release.

<hr>

[PS-9837](https://perconadev.atlassian.net/browse/PS-9837)**:** A crash occurs on replica nodes during parallel replication when an INSERT is executed on a secondary index that recently had a DELETE on the same key. The issue is caused by a race condition in the secondary index reuse logic, leading to an assertion failure (row0ins.cc:268).

This issue is more likely to occur under **heavy write workloads**, particularly when the application frequently performs **DELETE followed by INSERT on the same keys**. It only affects **replica servers** where replica\_parallel\_workers \> 0 and slave\_preserve\_commit\_order=ON. 

**Reported Affected Version/s:** 8.0.36-28, 8.0.42-33  
**Upstream Bug:** [118334](https://bugs.mysql.com/bug.php?id=118334)  
**Workaround/Fix:** The user can modify their logic to use UPDATE instead of DELETE followed by INSERT, which avoids triggering the crash path.  
**Fixed/Planned Version/s:** Under investigation. A fix or workaround is expected in a future release.

<hr>

[PS-9861](https://perconadev.atlassian.net/browse/PS-9861)**:** The audit\_log\_filter plugin cannot be installed when component\_keyring\_kmip is enabled with Fortanix DSM. While testing with component\_keyring\_kmip, we enabled the **"Allow secrets with unknown operations"** option in Fortanix, which allowed the audit log installation to proceed one step further. At this point, a secret is successfully created for the audit log, but **MySQL crashes upon restart**.

This issue is related to **bug** [PS-9609](https://perconadev.atlassian.net/browse/PS-9609) and still persists when using **Fortanix DSM** as the KMIP server.

**Reported Affected Version/s:** 8.0.42-33  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** The issue has been fixed, and the fix is expected in the upcoming release of Percona Server (PS).

<hr>

[PS-9914](https://perconadev.atlassian.net/browse/PS-9914)**:** After running ALTER TABLE ... ENGINE=InnoDB to rebuild a large table (\~10 million rows) with ROW\_FORMAT=COMPRESSED, it was observed approximately a **50% drop in write-only workload throughput** (measured via sysbench), despite a reduction in .ibd file size and no changes to table structure or indexes. The table had previously undergone heavy deletions (\~50%), suggesting possible fragmentation prior to the rebuild.

**Reported Affected Version/s:** 8.0.37-29, 8.0.42-33  
**Upstream Bug:** [118411](https://bugs.mysql.com/bug.php?id=118411)  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** Under investigation. A fix or workaround is expected in a future release.

<hr>

[PS-9956](https://perconadev.atlassian.net/browse/PS-9956)**:** PS 8.4.4-4 with group replication crashes on Oracle Linux 9 during bootstrap or failover when the audit log filter component is enabled, but does not crash on Oracle Linux 8\.

**Reported Affected Version/s:** 8.4.4-4  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** Under investigation.

<hr>

### Percona Xtradb Cluster

[PXC-4652](https://perconadev.atlassian.net/browse/PXC-4652): PXC 8.4 crashes with a SIGSEGV in unordered\_map called from rpl\_gtid\_owned during high activity, while PXC 8.0 under the same workload and data remains stable; the crash occurs randomly during operations like COMMIT or INSERT.

**Reported Affected Version/s:** 8.4.3, 8.4.4  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 8.4.5 – Pending Release

<hr>

[PXC-4684](https://perconadev.atlassian.net/browse/PXC-4684): An UPDATE query that joins two tables but modifies only one—e.g., UPDATE test.t2 JOIN test.t1 USING (i) SET t2.d \= t2.d+1, t1.d \= t1.d;—causes an MDL BF-BF conflict on other PXC nodes, even without triggers, as both tables are included in the Table\_map\_log\_event.

**Reported Affected Version/s:** 8.0.41  
**Upstream Bug:** Not Available  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 8.0.42 – Released | 8.4.5 – Pending Release

<hr>

### Percona Toolkit

[PT-2418](https://perconadev.atlassian.net/browse/PT-2418): In **pt-online-schema-change 3.7.0**, data was lost when executing the following SQL — the value of column col\_2 was unexpectedly set to NULL:

Eg:
```
ALTER TABLE t RENAME COLUMN col_1 TO col_2;
MySQL version: 8.0+
pt-online-schema-change --no-version-check \
  h=127.0.0.1,u=root,p=xxx,P=xxx,D=sysbench,t=sbtest1 \
  --alter="RENAME COLUMN col_1 TO col_2" \
  --execute --statistics
```
**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PT-2419](https://perconadev.atlassian.net/browse/PT-2419)**:** pt-duplicate-key-checker Ignores DESC in Index Definitions. Users running pt-duplicate-key-checker regularly observed that a newly added composite index was being incorrectly flagged as a duplicate and removed.

```
Before:

KEY `idx_ts` (`ts`),
KEY `idx_ts_id` (`ts` DESC, `id`)

After:

KEY `idx_ts_id` (`ts`)
```

The tool appears to ignore the **DESC direction** in index definitions, leading to incorrect de-duplication. This behaviour may affect query plans and performance in setups relying on sort order.

**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PT-2425](https://perconadev.atlassian.net/browse/PT-2425)**:** Case-Sensitive MariaDB Detection Causes Sync Failure in pt-table-sync. In pt-table-sync 3.7.0, a case-sensitive check for the MariaDB flavor ($vp-\>flavor() \=\~ m/maria/) fails because flavor() returns "MariaDB Server", causing the condition to evaluate incorrectly. As a result, the tool looks for source\_host and source\_port in $source, while the actual keys are master\_host and master\_port, leading to failures or uninitialized value warnings.

The Error:

```
Use of uninitialized value in concatenation (.) or string at /usr/bin/pt-table-sync line 7086.
```

Manually updating the regex to m/maria/i resolves the issue. Similar case-sensitive checks appear elsewhere in the script and may require centralizing the MariaDB detection logic.

**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 3.7.1 \- Not Yet Released

<hr>

[PT-2197](https://perconadev.atlassian.net/browse/PT-2197)**:** In pt-online-schema-change (version 3.7.0), attempting to run an ALTER operation results in the following error:

```
Use of uninitialized value in string eq at /usr/bin/pt-online-schema-change line 4321
```

This occurs even when replica connectivity in both directions is fully functional and multiple replicas are connected. Notably, the issue does **not occur in version 3.5.1**, where the operation succeeds as expected (with the expected increase in connections). Schema change automation breaks unexpectedly on newer versions despite a valid replication setup.

**Reported Affected Version/s:** 3.5.2, 3.6.0, 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:**  A fix or workaround is expected in a future release.

<hr>

[PT-2432](https://perconadev.atlassian.net/browse/PT-2432)**:** While pt-replica-find includes internal logic for handling replication channels, it currently lacks a corresponding \--channel command-line option. Attempting to use it results in an error:

```
$ pt-replica-find --channel=foo
Unknown option: channel
```

This prevents users from specifying a replication channel directly, limiting the tool’s usability in multi-channel replication environments.

**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PT-2448](https://perconadev.atlassian.net/browse/PT-2448)**:** pt-k8s-debug-collector should not collect secret details of pgbouncer

**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PT-2446](https://perconadev.atlassian.net/browse/PT-2446)**:** When attempting to run **pt-table-checksum** with Group Replication enabled, and the tool returns the following error: 

```
Error checksumming table schema.table: DBD::mysql::st execute failed: The table does not comply with the requirements by an external plugin. [for Statement "DELETE FROM percona.checksums WHERE db = ? AND tbl = ?" with ParamValues: 0=' ', 1=' '] at /bin/pt-table-checksum line 11323.
```

It gets suspected that this is caused by the tool attempting to set @@binlog\_format := 'STATEMENT', which is **not supported under Group Replication**.

**Reported Affected Version/s:** 3.7.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

### PMM \[Percona Monitoring and Management\]

[PMM-13994](https://perconadev.atlassian.net/browse/PMM-13994)**:** pmm\_agent shows disconnected status despite active metrics collection, After a temporary connectivity issue, pmm\_agent continues to display a Disconnected status in pmm-admin list, even though connectivity has been restored and dashboards are populating correctly.

```
$ pmm-admin list
...
pmm_agent     Disconnected
...
```

**Reported Affected Version/s:** 2.43.2, 2.44.1, 3.1.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Restarting the pmm\_agent should fix the issue.  
**Fixed/Planned Version/s:** 3.4.0 \- Not Yet Released

<hr>

[PMM-13905](https://perconadev.atlassian.net/browse/PMM-13905)**:**  When adding both a MongoDB Cluster and a standalone MongoDB Replica Set (not part of the cluster) to the same PMM environment (e.g., "test"), the **MongoDB ReplSet Summary dashboard** does not allow viewing the standalone RS.

The **“cluster” filter cannot be unselected**, making it impossible to visualize replica sets that are not associated with a defined cluster. As a result, only RSs from the cluster are visible, while standalone RSs are excluded from the dashboard view.

**Reported Affected Version/s:** 3.1.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Whenever possible, use **separate environments** when adding the cluster and standalone RS nodes in PMM (e.g., use "env1" for the cluster and "env2" for the standalone RS).  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PMM-13910](https://perconadev.atlassian.net/browse/PMM-13910): In the **MongoDB Sharded Cluster Summary** and **Collections** dashboards, several graphs fail to populate correctly. Specifically:

* **Top Hottest Collections by Read**  
* **Top Hottest Collections by Write**

These graphs display only admin, config, and system collections, even when other collections are under heavy traffic. Additionally, the **Collections** dashboard shows no data across all graphs—**except for the first one** (Top 5 Databases By Size), which populates as expected.

**Reported Affected Version/s:** 3.1.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PMM-13950](https://perconadev.atlassian.net/browse/PMM-13950)**:** In both **PMM 2** and **PMM 3**, with **MySQL 5.7** and **MySQL 8.0**, the server\_uuid is not being collected from MySQL's global variables as expected. Despite being available via SHOW GLOBAL VARIABLES LIKE 'server\_uuid';, the PMM agent fails to parse or capture this value.

**Reported Affected Version/s:** 3.1.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[PMM-13792](https://perconadev.atlassian.net/browse/PMM-13792)**:** In PMM 2.44.0, the Advisor Insights incorrectly reports that *journaling is not enabled* for MongoDB 7.0.9-15, despite journaling being enabled by default in this version. 

Attempts to explicitly enable journaling in the MongoDB config result in a startup warning:

```
The storage.journal.enabled option and the corresponding --journal and --nojournal command-line options have no effect in this version... Journaling is always enabled. Please remove those options from the config.
```

False alert may confuse users and lead to misconfiguration attempts that prevent MongoDB from starting.

**Reported Affected Version/s:** 2.44, 3.1.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

### 

### Percona Kubernetes Operator

[K8SPG-772](https://perconadev.atlassian.net/browse/K8SPG-772)**:** In the Percona PostgreSQL Operator, a runtime panic occurs when CompletedAt is nil and not properly checked before dereferencing, leading to a segmentation fault:

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0]
```

**Stack trace:**

```
github.com/percona/percona-postgresql-operator/percona/watcher.getLatestBackup
  .../wal.go:123

github.com/percona/percona-postgresql-operator/percona/watcher.WatchCommitTimestamps
  .../wal.go:65
```

The CompletedAt field is not validated before being accessed in getLatestBackup(), which causes a crash during WAL watcher execution.

This panic can crash the operator's goroutine, interrupting WAL monitoring and potentially affecting backup or failover logic.

**Reported Affected Version/s:** 2.5.0, 2.6.0   
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.7.0 \- Pending Release

<hr>

[K8SPG-792](https://perconadev.atlassian.net/browse/K8SPG-792)**:** The upstream operator includes functionality that allows cluster or operator administrators to define default PostgreSQL images for each major version using environment variables. This enables users to create clusters without explicitly specifying spec.image, as the operator will automatically apply the predefined image.

However, a recently introduced Patroni version check does not align with this behavior. It introduces a hardcoded dependency on spec.image, effectively bypassing the default image mechanism and undermining the intended feature.

**Reported Affected Version/s:** 2.6.0   
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** A possible workaround exists by manually setting the Patroni version through annotations, but this is not ideal and diminishes the convenience and flexibility originally provided.  
**Fixed/Planned Version/s:** A fix or workaround is expected in a future release.

<hr>

[K8SPXC-1651](https://perconadev.atlassian.net/browse/K8SPXC-1651): While testing the Pod Scheduling Policy feature in [Everest](https://docs.percona.com/everest/index.html), we encountered a situation where a PXC database pod remained in the **Pending** state. This occurred because Kubernetes was unable to schedule the pod on any available node due to an affinity configuration mismatch.

However, even after updating the affinity rules in the PerconaXtraDBCluster object, the new configuration was not propagated to the pod, and it remained in the **Pending** state.

The fact that the Pod remains stuck in Pending **even after affinity is changed or removed** — and only a manual kubectl delete pod resolves it — indicates that **the operator fails to reconcile affinity changes properly**.

**Note:** This issue affects other operators as well, not just PXC.

**Reported Affected Version/s:** 1.17.0   
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 1.20.0 \- Yet to be released

<hr>

[K8SPXC-1648](https://perconadev.atlassian.net/browse/K8SPXC-1648)**:** The PVC size is rounded up to the nearest whole GiB value (e.g., 1.2Gi becomes 2Gi). When a storage resize operation is triggered, the operator deletes the existing StatefulSet (STS) and recreates it with the new requested PVC size.

However, if the new requested size rounds up to the same value as the original, the operator does not recreate the STS. Instead, it attempts to update the existing STS, which leads to the following error:

**Note:** This issue affects other operators as well, not just PXC.

```
Error: failed to deploy pxc: updatePod for pxc: failed to create or update sts:
update error: StatefulSet.apps "minimal-cluster-pxc" is invalid: spec: Forbidden:
updates to statefulset spec for fields other than 'replicas', 'ordinals',
'template', 'updateStrategy', 'persistentVolumeClaimRetentionPolicy' and
'minReadySeconds' are forbidden
```

**Reported Affected Version/s:** 1.17.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 1.20.0 \- Yet to be released

<hr>
 
### PBM \[Percona Backup for MongoDB\]

[PBM-1499](https://perconadev.atlassian.net/browse/PBM-1499)**:** Restore to Missing Backup Fails with Unclear Error in Restore Custom Resource Status.  
When attempting to restore from a backup that does not exist in the main storage, the operator logs correctly report the failure:

```
define base backup: get backup metadata from storage: get from store: no such file
```

However, the status.error field in the PerconaServerMongoDBRestore custom resource only shows a generic message:

```
error: 'define base backup: %v'
```

This results in a misleading or unclear error message being surfaced to the user through the custom resource, even though the logs contain the full and accurate description of the issue.

**Reported Affected Version/s:** 2.8.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

[PBM-1502](https://perconadev.atlassian.net/browse/PBM-1502)**:** In **PBM 2.9.0**, running pbm profile sync \<profile-name\> fails with the error:

```
Error: <profile-name> or --all must be provided
```

This occurs **even when a valid profile name is given**, such as:

```
pbm profile sync azure-blob
```

The issue affects all defined profiles (azure-blob, gcp-cs, minio) and prevents syncing individual profiles. This appears to be a bug where the CLI fails to recognize the passed argument.

**Reported Affected Version/s:** 2.9.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Use pbm profile sync \--all instead  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

[PBM-1538](https://perconadev.atlassian.net/browse/PBM-1538)**:** Backup is marked as successful, despite the oplog not being uploaded.

**Reported Affected Version/s:** 2.4.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

[PBM-1551](https://perconadev.atlassian.net/browse/PBM-1551)**:** In a single-node PSMDB replica set with one PBM agent, PBM occasionally **re-executes the last issued command**, causing errors like:

```
active lock is present
```

This typically occurs when the database is under load.

**Reported Affected Version/s:** 2.9.1  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

[PBM-1553](https://perconadev.atlassian.net/browse/PBM-1553)**:** When restoring a 33-shard physical backup from a mixed (MongoDB Enterprise \+ Percona) production cluster into a Percona-only test cluster, **PBM intermittently fails during the “clean-up and reset replicaset config” stage**. Some shards restore successfully, while others restore only partially or fail entirely.

* Both clusters run MongoDB 6, with FCV set to 5\.  
* Restore uses \--replset-remapping due to different replica set names  
* Issue affects restores regardless of matching node count per shard.

The problem appears tied to the restore logic handling replica set configuration cleanup.

**Reported Affected Version/s:** 2.9.1  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

[PBM-1564](https://perconadev.atlassian.net/browse/PBM-1564)**:**  A user environment experiences repeated failures during **incremental backups** with the error:

```
[ERROR: cannot use the configured storage: source backup is stored on a different storage]
```

Full, base incremental, and logical backups succeed without issues. There is no indication of recent storage or configuration changes, and pbm status shows backup attempts occur close together.

The issue temporarily resolves after running pbm config \--force-resync, suggesting a possible bug in storage metadata syncing or internal state handling.

**Reported Affected Version/s:** 2.8.0  
**Upstream Bug:** Not Applicable  
**Workaround/Fix:** Not Available  
**Fixed/Planned Version/s:** 2.10.0 \- Released

<hr>

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).

Quick References:

[Percona JIRA](https://jira.percona.com)

[MySQL Bug Report](https://bugs.mysql.com/)

[Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)
