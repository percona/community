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


Replication Lag is just a fact of life with async-replication. We can't stop lag, but we can help to reduce it. Many times the Seconds_Behind_Source can be very deciving, I have seen it go from 1 hour behind to 0 lag in the blink of an eye. There are many factors that can add to replica lag. Some of these are:

- Network IO
- Disk IO
- Database Workload
- Database settings

In this blog we will look a few database settings to help reduce lag. The settings we will look at are listed below.

 1. blinlog_transaction_dependency_tracking
 2. binlog_group_commit_sync_delay
 3. replica_parallel_type
 4. replica_parallel_workers

### Hardware:

1. Two Raspberry Pi 4 with 8GB of RAM.
2. Sandisk 128GB Extreme microSDXC card.

### Software:

1. OS Raspbian Bullseye 64bit.
2. Percona Server version 8.0.26.
3. Sysbench 1.0.20.

## Testing Setup

Using Sysbench I set up 10 tables with 250,000 rows of data. If interested here is the command I used:

```text
sysbench /usr/share/sysbench/oltp_read_write.lua \
--mysql-db=YOUR-DB --threads=4 --mysql-host=YOUR-HOST \
--mysql-user=YOUR-USER --mysql-password=YOUR-PASSWORD --tables=10 \
--table-size=250000 prepare
```

## Test one with default settings

If you have not changed any of the default setting you can skip the blow changes. If your
not sure verify and change as needed.

The initial testing was done with the following default settings. Make sure you make
these settings on both the primary and the replica. You will need to stop replication
on the replica before making the changes. Once changes are complete restart replication.

```text
 mysql >set global binlog_transaction_dependency_tracking = 'COMMIT_ORDER';
 mysql >set global binlog_group_commit_sync_delay = 0;
 mysql >set global replica_parallel_type = 'DATABASE';
 mysql >set global replica_parallel_workers = 0;
 ```

 Using sysbench I ran the OLTP read/write test. I used the following setting for the test.

```text
 sysbench --db-driver=mysql --report-interval=2 \
 --threads=4 --time=300 --mysql-host=YOUR-HOST \
 --mysql-user=YOUR-USER --mysql-password=PASSWD \
 --mysql-db=YOUR-DB /usr/share/sysbench/oltp_read_write.lua run
```

At the end of this test, replicacation lag was **20 minutes** behind the primary.

## Test two with adjusted settings

In the second test we will apply the new setting to help reduce replication lag time. Just like in test one
you will want to make these changes on both primary and replica. Make sure to stop replication on the replica
before applying the changes. Once changes are applied restart replication on the repliica.

Make the following settings on your primary:

```text
 mysql >set global binlog_transaction_dependency_tracking = 'writeset';
 mysql >set global replica_parallel_type = 'LOGICAL_CLOCK';
 mysql >set global replica_parallel_workers = 4;
 ```

Make the following changes on your replica:

```text
 mysql >set global binlog_group_commit_sync_delay = 3000;
 mysql >set global replica_parallel_type = 'LOGICAL_CLOCK';
 mysql >set global replica_parallel_workers = 4;
```

I repeated the test from above. At the end of this test, replicacation lag was **6 minutes** behind the primary.

## blinlog_transaction_dependency_tracking = writeset

I repeated the test from above. At the end of this test, replication lag was **6 minutes** behind the primary.

## Setting Details:

## blinlog_transaction_dependency_tracking = writeset

This allows for transactions that are marked as indipendent to be applied in parallel on the replica. Note to take advantage of
this you need to set replica_parallel_workers to a non 0 value.

## binlog_group_commit_sync_delay = 3000

This controls how many microseconds the binary log commit waits before syncing the binlog to disk. Change this to a non 0 value
will enable more transactions to be synced at one time to disk. This will reduce the overall time to commit.

## replica_parallel_type = logical_clock

**As of version 8.0.27 the default value is logical_clock.**
Transaction will be applied in parrallel on the replica based on the source timestamp in the binlog.

## replica_parallel_workers = 4

**As of 8.0.27 this is a defaul value of 4.**
This allows for multithreading on the replica, and set the number of applier threads.

## Conclusion

As we look at the results of both tests we saw a very big difference in lag. The Sysbench workload might not reflect a real world
database uses, but it does provide us with baseline numbers to compare.

In the first test we saw a lag of 20 minutes at the end of the sysbench test. In our second test we say just 6 minutes of lag at
the end of the sysbench test.

Dropping lag from 20 minutes down to 6 minutes is a decrease of more than **50%**. That is a huge decrease.

As I high lighted above two of these variables will become default values with 8.0.27. I did my testing on 8.0.26 so I could demo these changes
on a version what did not have the new standards.
