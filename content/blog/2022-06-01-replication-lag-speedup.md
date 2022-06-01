---
title: 'Reduce Replication Lag'
date: "2022-06-01T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', 'Replication', 'LAG', 'performance']
authors:
  - wayne
images:
  - blog/2022/6/snail.jpg
slug: Speed-Up-Replication-Lag
---

Replication Lag is just a fact of life with async-replication. We can't stop lag,
but we can help to reduce it. Many times the Seconds_Behind_Source can be very deciving, I have
seen go from 1 hour behind to 0 lag in blink of the eye.

There are four vairables that we will look at in this post.

 1. blinlog_transaction_dependency_tracking = writeset
 2. binlog_group_commit_sync_delay = 3000
 3. replica_parallel_type = LOGICAL_CLOCK
 4. replica_parallel_workers = 4
  
## Hardware

1. Two Raspberry Pi 4 with 8GB of RAM.
2. Sandisk 128GB Extreme microSDXC card.

## Software

1. OS Raspbian Bullseye 64bit.
2. Percona Server version 8.0.27.
3. Sysbench 1.0.20.

## Testing data

Using Sysbench I set up 10 tables with 250,000 rows of data. If interested here is the command I used:

```text
sysbench /usr/share/sysbench/oltp_read_write.lua \
--mysql-db=YOUR-DB --threads=4 --mysql-host=YOUR-HOST \
--mysql-user=YOUR-USER --mysql-password=YOUR-PASSWORD --tables=10 \
--table-size=250000 prepare
```

## Test one with default settings

The initial testing was done with the following default settings. Make sure you make
these settings on both the primary and the replica. You will need to stop replication
on the replica before making the changes. Once changes are complete restart replication.

```text
 mysql >set global binlog_transaction_dependency_tracking = 'COMMIT_ORDER';
 mysql >set global binlog_group_commit_sync_delay = 0;
 mysql >set global replica_parallel_type = 'LOGICAL_CLOCK';
 mysql >set global replica_parallel_workers = 0;
 ```

 Using sysbench I ran the OLTP read/write test. I used the following setting for the test.

```text
 sysbench --db-driver=mysql --report-interval=2 \
 --threads=4 --time=300 --mysql-host=YOUR-HOST \
 --mysql-user=YOUR-USER --mysql-password=PASSWD \
 --mysql-db=YOUR-DB /usr/share/sysbench/oltp_read_write.lua run
```

At the end of this test, replicacation lag was 40 minutes behind the primary. The actual time
it took the replica to catch up to the primary was about 20 mins.

## Test two with adjusted settings

In the second test we will apply the new setting to help reduce replication lag time. Just like in test one
you will want to make these changes on both primary and replica. Make sure to stop replication on the replica
before applying the changes. Once changes are applied restart replication on the repliica.

```text
mysql >set global binlog_transaction_dependency_tracking = 'writeset';
 mysql >set global binlog_group_commit_sync_delay = 3000;
 mysql >set global replica_parallel_type = 'LOGICAL_CLOCK';
 mysql >set global replica_parallel_workers = 4;
 ```
