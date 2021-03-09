---
title: 'Minimize MySQL Deadlocks with 3 Steps'
date: Mon, 24 Sep 2018 10:49:35 +0000
draft: false
tags: ['author_aftabkhan', 'application development', 'deadlock', 'Entry Level', 'MySQL']
---

![application deadlock in MySQL transactions](https://www.percona.com/community-blog/wp-content/uploads/2018/09/application-deadlock-in-MySQL-transactions-200x150.jpg)MySQL has locking capabilities, for example table and row level locking, and such locks are needed to control data integrity in multi-user concurrency. Deadlocks—where two or more transactions are waiting for one another to give up locks before the transactions can proceed successfully—are an unwanted situation. It is a classic problem for all databases including MySQL/PostgreSQL/Oracle etc. By default, MySQL detects the deadlock condition and to break the deadlock it rolls back one of the transactions. For a deadlock example, see [InnoDB deadlocks](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlock-example.html)

Some misconceptions
-------------------

There are some misconceptions about deadlocks: a) **Transaction isolation levels are responsible for deadlocks**. The possibility of deadlocks is not affected by isolation level. Isolation level changes the behavior of read operations, but deadlock occurs due to write operations. However, isolation level sets fewer locks, hence it can help you to avoid certain lock types (e.g. gap locking). b) **Small transactions are not affected by deadlocks.** Small transactions are less prone to deadlocks but it can still happen if transactions do not use the same order of operations. c) **Deadlocks are dangerous.** I still hear from some customers who are using MyISAM tables that their reason for not switching to InnoDB is the deadlock problem. Deadlocks aren't dangerous if you retry the transaction that failed due to deadlock and follow the steps given below in this article. I hope that this article will help clear such misconceptions. Back to the topic of this article. There are many possibilities that can cause deadlocks to occur and, for simplicity, I have grouped my recommendations into 3 steps.

1) Use a lock-avoiding design strategy
--------------------------------------

*   Break big transactions into smaller transactions: keeping transactions short make them less prone to collision.
*   If you use INSERT INTO ... SELECT to copy some or all rows from one table to another, consider using a lesser locking transaction isolation level (e.g. READ\_COMMITTED) and set the binary log format to row/mixed for that transaction. Alternatively, design your application to put a single INSERT statement in a loop and copy row(s) into the table.
*   If your application performs locking reads, for example SELECT ... FOR UPDATE or SELECT .. FOR SHARE consider using the NOWAIT and SKIPPED LOCK options available in MySQL 8.0, see [Locking Read Concurrency with NOWAIT and SKIP LOCKED](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking-reads.html#innodb-locking-reads-nowait-skip-locked). Alternatively, you may consider using a lesser locking transaction isolation level (described earlier)
*   Multiple transactions updating data set in one or more tables, should use the same order of operation for their transactions. Avoid locking table A, B, C in one transaction and C,A,B in another.
*   If you have the application retry when a transaction fails due to deadlock, you should ideally have the application take a brief pause before resubmitting its query/transaction. This gives the other transaction involved in the deadlock a chance to complete and release the locks that formed part of the deadlock cycle.

2) Optimize queries
-------------------

*   Well optimized queries examine fewer rows and as result set fewer locks.

3) Disable deadlock detection (for systems running MySQL 8+)
------------------------------------------------------------

*   If you're running a high concurrency system, it maybe more efficient to disable deadlock detection and rely on the [innodb\_lock\_wait\_timeout](https://dev.mysql.com/doc/refman/5.5/en/innodb-parameters.html#sysvar_innodb_lock_wait_timeout) setting. However, keep this setting low. The default timeout setting is 50 seconds which is too long if you're running without deadlock detection. Be careful when disabling deadlock detection as it may do more harm than good.

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors' own. When using the advice from this or any other online resource **test** ideas before applying them to your production systems, and **always **secure a working back up._