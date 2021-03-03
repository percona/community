---
title: "How to Speed Up Re Sync of Dropped Percona Xtradb Cluster Node"
date: "2021-02-24T00:00:00+00:00"
authors:
  - wayne
images:
  - blog.jpg
---

## The Problem

HELP, HELP! My Percona XtraDB Cluster version: 5.7.31-31. Single Node is stuck in a joined state.

I recently had the privilege to help a client with a fascinating issue.

NODE-B dropped out of the 3 node PXC cluster. It looked to be DISK IO that caused NODE-B to fall far behind and eventually be removed from the cluster. A restart of NODE-B allowed it
to rejoin the cluster. NODE-B looked to have been down for about 4 hours. Once NODE-B was back as part of the cluster, it required a full SST.

When NODE-B stayed in a joint state for more than 12 hours, the client gave me a call. They were concerned that there was another issue with this cluster.

Before going forward, let’s make sure we know the CPU, RAM and Database Size.

- 8 CPU
- 32 GB RAM
- Database Size approx. 2.75TB

Let’s gather some base information.

I pulled the below data once I understood what was going on.

```
SHOW STATUS LIKE ‘wsrep_last%';
+----------------------+----------+
| Variable_name        | Value    |
+----------------------+----------+
| wsrep_last_applied   |  9802457 |
+----------------------+----------+
| wsrep_last_committed | 10103670 |
+----------------------+----------+
SHOW GLOBAL STATUS LIKE 'wsrep_local_state_comment';
```

```
+---------------------------+--------+
| Variable_name             | Value  |
+---------------------------+--------+
| wsrep_local_state_comment | Joined |
+---------------------------+--------+
```

```
SHOW STATUS LIKE 'wsrep_cert_deps_distance';
+--------------------------+---------+
| Variable_name            | Value   |
+--------------------------+---------+
| wsrep_cert_deps_distance | 148.96  |
+--------------------------+---------+
```

Pulled the below stats about one hour later.

```
NODE-B
+----------------------+----------+
| Variable_name        | Value    |
+----------------------+----------+
| wsrep_last_applied   | 11901100 |
+----------------------+----------+
| wsrep_last_committed | 12801100 |
+----------------------+----------+
```

```
NODE-A
+----------------------+----------+
| Variable_name        | Value    |
+----------------------+----------+
| wsrep_last_applied   | 32900981 |
+----------------------+----------+
| wsrep_last_committed | 32901100 |
+----------------------+----------+
```

As we can see above, NODE-B is processing write sets, but very slowly. The gcache files were being consumed very quickly, but being only 128MB in size would be slow going to get in sync. At this time, NODE-A and NODE-B seqno’s were separated by 20,100,000.

Now we know NODE-B is working as it should. At this rate, it could be a day or more to catch up.

## Gathering Data and Coming up with a solution

I did a quick review of the PXC settings and found:

1. The wsrep_slave_threads = 2
2. Many tables had no primary key. The mysql.log file was approx 500Mb in size. The gal-leria cache size was set at the default 128MB (Now I saw why NODE-B needed a fullSST)
3. The client had set the wsrep_doner_node to use NODE-C. NODE-C had a higher laten-cy to NODE-B than NODE-B had to NODE-A. I would prefer to have PXC choose the donor. Not have it set up to use NODE-C.

A scheduled 500 million row data extract started right about the time NODE-B re-joined the cluster. Now we have a large data load taking place plus a full SST to NODE-B.

Let’s now talk about how we helped to speed up NODE-B going from Joined to Synced.

## Recommendations

We upped the slave threads from 2 to 8. This is equal to the number of CPU’s on the system. Exceeding 8 threads could cause performance impact.

```mysql
set global wsrep_slave_threads=8;
```

Changed pxc_stright_mode from permissive too disabled. This was done to stop all PXC warnings being written to mysqld.log.

```mysql
set global pxc_strick_mode = disabled;
```

Relaxed ACID compliance. I made these changes to help NODE-B get back into a sync status quicker. I don’t recommend relaxing ACID compliance. This change should only be made if the client fully understands the risk.

```mysql
set global innodb_flush_log_at_trx_commit = 2;
set global sync_binlog = 0;
```

We let these changes bake in for about 2 hours. The client did not want to stop the data extract just yet. They were very open to the idea and did not want to lose the work that had already been completed. This did not bother me because I know the NODE-B was working as it should be. We let these changes bake in for about two hours.

## Improvement