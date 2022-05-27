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
but we can help to reduce it. 

There are four vairables that we will look at in this post. 

 1. blinlog_transaction_dependency_tracking
 2. binlog_group_commit_sync_delay
 3. replica_parallel_type
 4. replica_parallel_workers
   
##Hardware:

Two Raspberry Pi 4 with 8GB of RAM.

##Software:

1. OS Raspbian Bullseye 64bit
2. Percona Server version 8.0.27
3. Sysbench 1.0.20
