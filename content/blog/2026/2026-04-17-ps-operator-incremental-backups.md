---
title: "Incremental backups in Percona Kubernetes Operator for MySQL"
date: "2026-04-17T10:00:00+00:00"
tags: ['Kubernetes', 'Community', 'Open Source', 'MySQL']
categories: ['MySQL', 'Kubernetes']
authors:
  - mayank_shah
images:
  - blog/2026/04/Mayank.png
---

Starting with version 1.1.0, the Percona Kubernetes Operator for MySQL now supports **incremental backups**. This feature lets you backup only the changed data since the last backup, instead of copying your entire dataset each time. The result is dramatically smaller backup sizes, faster backup windows, and lower cloud storage costs.

In this post, we'll walk through how the feature works under the hood, how to configure it, and what to keep in mind when designing your backup strategy.

## How Incremental Backups Work in Percona XtraBackup

The foundation of this feature is [Percona XtraBackup (PXB)](https://docs.percona.com/percona-xtrabackup/latest/), an open source backup tool for MySQL. PXB has supported incremental backups for a while, and the operator now brings that capability into the backup workflow.

Every InnoDB data page carries a **Log Sequence Number (LSN)**, which is a monotonically increasing counter that records when the page was last modified. When PXB takes an incremental backup, it scans data pages and copies only those with an LSN newer than a reference point. The output is a set of compact `.delta` files instead of full tablespace copies.

Each backup produces an `xtrabackup_checkpoints` file:

```
backup_type = full-backuped
from_lsn = 0
to_lsn = 7345291
last_lsn = 7345291
```

Each incremental's `from_lsn` must equal the previous backup's `to_lsn`.

## Using Incremental Backups with the Operator

### On-Demand Incremental Backup

First, you need a full backup to serve as the base:

```yaml
apiVersion: ps.percona.com/v1
kind: PerconaServerMySQLBackup
metadata:
  name: weekly-full
spec:
  clusterName: my-cluster
  storageName: s3-us
  type: full
```

Once the full backup succeeds, create an incremental:

```yaml
apiVersion: ps.percona.com/v1
kind: PerconaServerMySQLBackup
metadata:
  name: daily-inc-1
spec:
  clusterName: my-cluster
  storageName: s3-us
  type: incremental
```

The operator automatically discovers the latest succeeded full backup for the same cluster and storage, fetches its LSN, and creates an incremental backup. If you want to pin a specific base, simply use the `incrementalBaseBackupName` field:

```yaml
spec:
  type: incremental
  incrementalBaseBackupName: weekly-full
```

### Scheduled Backups: Full + Incremental

The real power comes from combining full and incremental schedules. Here's an example: weekly full backups with daily incrementals:

```yaml
spec:
  backup:
    schedule:
      - name: weekly-full
        schedule: "0 0 * * 0"        # Sunday midnight
        keep: 4
        storageName: s3-us
        type: full
      - name: daily-incremental
        schedule: "0 0 * * 1-6"      # Monday through Saturday
        storageName: s3-us
        type: incremental
```

The `keep` rotation policy is chain-aware: it counts only full backups and automatically cascade-deletes all dependent incrementals when a full backup is rotated out.

### Restoring from an Incremental Backup

The `PerconaServerMySQLRestore` custom resource allows you to restore from any point in an incremental, similar to restoring a full backup:

```yaml
apiVersion: ps.percona.com/v1
kind: PerconaServerMySQLRestore
metadata:
  name: restore-to-wednesday
spec:
  clusterName: my-cluster
  backupName: daily-inc-3
```

The operator handles the complexity behind the scenes:

1. Discovers the full chain by listing the cloud storage directory
2. Downloads and prepares the base full backup
3. Applies each incremental in sequence
4. Applies the final incremental and rolls back uncommitted transactions
5. Moves the prepared data back to the MySQL data directory

You don't need to know which backup is the base or how many incrementals are in the chain, the operator figures it out.

## How It Works Under the Hood

### Storage Layout

The operator uses a specific directory convention to encode backup chains without any requiring any additional metadata:

```
s3://bucket/prefix/
  my-cluster-2026-04-06-full/                              # base full backup
  my-cluster-2026-04-06-full.incr/                         # incremental chain directory
    my-cluster-2026-04-07T000000-incr/                     # Monday's incremental
    my-cluster-2026-04-08T000000-incr/                     # Tuesday's incremental
    my-cluster-2026-04-09T000000-incr/                     # Wednesday's incremental
```

The `.incr/` suffix creates a self-describing structure. Any cluster with access to the storage bucket can reconstruct the chain, making cross-cluster restores straightforward.

### The Backup Flow

Here's what happens when you create an incremental backup:

1. **Resolve the base.** The controller finds the latest succeeded full backup (or the one you specified) and annotates the incremental CR with `percona.com/base-backup-name`.
2. **Fetch the LSN.** The controller calls the xtrabackup sidecar's `/backup/checkpoint-info` endpoint. The sidecar downloads `xtrabackup_checkpoints` from the previous backup via `xbcloud get`, parses it, and returns the `to_lsn`.
3. **Launch the backup job.** A Kubernetes Job is created with the `INCREMENTAL_LSN` environment variable set.
4. **Stream to storage.** The sidecar runs `xtrabackup --backup --stream=xbstream --incremental-lsn=<LSN>` and pipes the output through `xbcloud put` to the cloud destination.

### Chain Integrity Protection

The operator enforces chain integrity at multiple levels:

- **Deletion guards:** Only the latest incremental in a chain can be deleted. Attempting to delete a mid-chain backup is blocked using finalizers.
- **Cascade deletion:** Deleting a full backup automatically removes all dependent incrementals, from newest to oldest.
- **Concurrent backup prevention:** The controller uses a Lease-based mechanism to prevent multiple incremental backups from running at the same time.

## Designing Your Backup Strategy

### When to Use Incremental Backups

Incremental backups shine when:

- **Your database is large but change rate is low.** A 1 TB database with 2% daily change produces ~20 GB incremental backups instead of 1 TB full backups.
- **You need frequent backup points.** Run hourly incrementals with minimal overhead.
- **Cloud storage costs matter.** Example: with about **2%** of the data changing each day, **one full backup** plus **six daily incrementals** needs roughly **one-fifth** the space of keeping **six separate full backups** over the same week.

### What to Keep in Mind

- **All chain members must use the same storage backend.** You can't mix S3 and GCS within a chain.
- **Chain integrity is critical.** If a backup in the chain is corrupted, all subsequent incrementals in that chain become unrestorable. Regular full backups provide recovery checkpoints.
- **Restore time increases with chain length.** Each incremental adds a prepare step. For very long chains, consider more frequent full backups.

## Try It Out

Incremental backups are available in Percona Operator for MySQL version 1.1.0 and later. If you're already running the operator, upgrade your CRDs and add a `type: incremental` schedule to your backup configuration.

<!-- TODO -->
- [Operator documentation: Backups]()
- [Percona XtraBackup: Incremental backups](https://docs.percona.com/percona-xtrabackup/latest/create-incremental-backup.html)
- [GitHub: percona/percona-server-mysql-operator](https://github.com/percona/percona-server-mysql-operator)

Have questions or feedback? Join the conversation on the [Percona Community Forum](https://forums.percona.com/) or open an issue on GitHub. We'd love to hear how incremental backups are working for your MySQL-on-Kubernetes deployments.

