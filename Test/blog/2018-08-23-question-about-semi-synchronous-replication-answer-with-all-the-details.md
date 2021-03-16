---
title: 'Question about Semi-Synchronous Replication: the Answer with All the Details'
date: Thu, 23 Aug 2018 12:49:59 +0000
draft: false
tags: ['author_jfgagne', 'Galera', 'Group Replication', 'InnoDB', 'InnoDB Crash Recovery', 'Lossless Semi-Synchronous Replication', 'MariaDB', 'MariaDB Server', 'MySQL', 'MySQL Crash Recovery', 'Percona Server', 'Percona XtraDB Cluster', 'Replication']
authors:
  - jeff_gagne
images: 
  - blog/2018/08/semi-sync-replication-MySQL.jpg
---

I was recently asked a question by mail about [MySQL Lossless Semi-Synchronous Replication](https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html). As I think the answer could benefit many people, I am answering it in a blog post. The answer brings us to the internals of transaction committing, of semi-synchronous replication, of MySQL (server) crash recovery, and of storage engine (InnoDB) crash recovery. I am also debunking some misconceptions that I have often seen and heard repeated by many. Let's start by stating one of those misconceptions. 

![semi-sync replication MySQL](blog/2018/08/semi-sync-replication-MySQL.jpg)

One of those misconceptions is the following (this is NOT true): semi-synchronous enabled slaves are always the most up-to-date slaves (again, this is **NOT** true). If you hear it yourself, then please call people out on it to avoid this spreading more. Even if some slaves have semi-synchronous replication disabled (I will use semi-sync for short in the rest of this post), these could still be the most up-to-date slaves after a master crash. I guess this false idea is coming from the name of the feature, not much can be done about this anymore (naming is hard). The details are in the rest of this post. 

Back to the question I received by mail, it can be summarized as follows:

*   In a deployment where a MySQL 5.7 master is crashed (kill -9 or echo c > /proc/sysrq-trigger ), a slave is promoted as the new master;
*   when the old master is brought back up, transactions that are not on the new master are observed on this old master;
*   is this normal in a lossless semi-sync environment?

The answer to that question is yes: it is normal to have transactions on the recovered old master that are not on the new master. This is not a violation of the semi-sync promise. To understand this, we need to go in detail about semi-sync (MySQL 5.5 and 5.6) and lossless semi-sync (MySQL 5.7).

Semi-Sync and Lossless Semi-Sync
--------------------------------

[Semi-sync replication](https://dev.mysql.com/doc/refman/5.5/en/replication-semisync.html) was introduced in MySQL 5.5. Its promise is that every transaction where the client has received a COMMIT acknowledgment would be replicated to a slave. It had a caveat though: while a client is waiting for this COMMIT acknowledgment, other clients could see the data of the committing transaction. If the master crashes at this moment (without a slave having received the transaction), it is a violation of transaction isolation. This is also known as phantom read: data observed by a client has disappeared. This is not very satisfactory. 

[Lossless semi-sync replication](https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html) was introduced in MySQL 5.7 to solve this problem. With lossless semi-sync, we keep the promise of semi-sync (every transaction where clients have received a COMMIT acknowledgment is replicated), with the additional promise that there is no phantom reads. To understand how this works, we need to dive into the way MySQL commits transactions.

The Way MySQL Commits Transactions
----------------------------------

When MySQL commits a transaction, it is going through the following steps:

1.  _Prepare_ the transaction in the storage engine (InnoDB),
2.  Write the transaction to the binary logs,
3.  _Complete_ the transaction in the storage engine,
4.  Return an acknowledgment to the client.

The implementation of semi-sync or lossless semi-sync inserts themselves into the above process. 

Semi-sync in MySQL 5.5 and 5.6 happens between step #3 and #4. After "completing" the transaction in the storage engine, a semi-sync master waits for one slave to confirm the replication of the transaction. As this happens after the storage engine has "completed" the transaction, other clients can see this transaction. **This is the cause of phantom reads.** Also — unrelated to phantom reads — if the master crashes at that moment and after bringing it back up, this transaction will be in the database as it has been fully "completed" in the storage engine. 

It is important to realize that for semi-sync (and lossless-semi-sync), transactions are written to the binary logs in the same way as in standard (non-semi-sync) replication. In other words, standard and semi-sync replication behave exactly the same way up to and including step #2. Also, once transactions are in the binary logs, they are visible to all slaves, not only to the semi-sync slaves. So a non-semi-sync slave could receive a transaction before the semi-sync slaves. This is why it is false to assume that the semi-sync slaves are the most up-to-date slaves after a master crash.

#### It is false to assume that the semi-sync slaves are the most up-to-date slaves after a master crash.

In lossless semi-sync, waiting for transaction replication happens between steps #2 and #3. At this point, the transaction is not "completed" in the storage engine, so other clients do not see its data yet. But even if this transaction is not "completed", a master crash at that moment and a subsequent restart would cause this transaction to be in the database. To understand why, we need to dive into MySQL and InnoDB crash recovery.

MySQL and InnoDB Crash Recovery
-------------------------------

During InnoDB crash recovery, transactions that are not "completed" (have not reached step #3 of transaction committing) are rolled back. So a transaction that is not yet committed (has not reached step #1) or a transaction that is not yet written to the binary logs (has not reached step #2) will not be in the database after InnoDB crash recovery. However, if InnoDB rolled back a transaction that has reached the binary logs (step #2) but that is not "completed" (step #3), this would mean a transaction that could have reached a slave would disappear from the master. This would create data inconsistency in replication and would be bad.

#### Once a transaction reaches the binary logs it should roll forward.

To avoid the data inconsistency described above, MySQL does its own crash recovery before storage engine crash recovery. This recovery consists of making sure that all the transactions in the binary logs are flagged as "completed". So if a transaction is between step #2 and #3 at the time of the crash, it is flagged as "completed" in the storage engine during MySQL crash recovery and it is rolled forward during storage engine crash recovery. In the case where this transaction has not reached at least a slave at the moment of the crash, it will appear in the master after crash recovery. It is important to note that this could happen even without semi-sync.

#### Having extra transactions on a recovered master can happen even without semi-sync.

The extra transactions that are visible on the recovered old master are because of the way MySQL and InnoDB carry out crash recovery. This is more likely to happen in a lossless semi-sync environment because of the delay introduced between steps #2 and #3 of the way MySQL commits transactions, but it could also happen without semi-sync if the timing is right.

The Facebook Trick to Avoid Extra Transactions
----------------------------------------------

There is an original trick to avoid having extra transactions on a recovered master. This trick was presented by Facebook during a talk at [Percona Live](https://www.percona.com/live/) a few years ago (sorry, I cannot find any link to this, please post a comment below if you know of public content about this). The idea is to force MySQL to roll-back (instead of rolling forward) the transactions that are not yet "completed" in the storage engine. It must be noted that this should only be done on an old master that has been replaced by a slave. If it is done on a recovering master without failing over to a slave, a transaction that could have reached a slave would disappear from the master. 

To trick MySQL into rolling back the non "completed" transactions, Facebook truncates the binary logs before restarting the old master. This way, MySQL thinks that the crash happened before writing to the binary logs (step #2). So MySQL crash recovery will not flag the transactions as "complete" in the storage engine and these will be rolled back during storage engine crash recovery. This avoids the recovered old master having extra transactions. Obviously, because these transactions were once in the binary logs, they could have been replicated to slaves. So the Facebook trick avoids the old master being ahead of the new master, possibly at the cost of bringing the old master behind the new master. 

I know that Facebook then re-slaves the recovered old master to the new master, but I am not sure that this is possible with standard MySQL. The Facebook variant of MySQL includes additional features, and I think one of those is to put GTIDs in the InnoDB Redo logs. With this, and after the recovery of the old master, the GTID state of the database can be determined even if the binary logs are gone. In standard MySQL, I think that truncating the binary logs will result in losing the GTID state of the database, which will prevent re-slaving the old master to the new master. However, as InnoDB crash recovery prints the binary log position or the last committed transaction, I think re-slaving the old master to a [Binlog Server](https://medium.com/booking-com-infrastructure/abstracting-binlog-servers-and-mysql-master-promotion-without-reconfiguring-all-slaves-44be1febc8a0) would be possible in a semi-sync environment. 

You can read more about semi-synchronous replication at Facebook below:

*   [Semi-Synchronous Replication at Facebook](http://yoshinorimatsunobu.blogspot.com/2014/04/semi-synchronous-replication-at-facebook.html)
*   [The highs and lows of semi-synchronous replication](https://www.percona.com/live/data-performance-conference-2016/sessions/highs-and-lows-semi-synchronous-replication)

Debunking Other Misconceptions
------------------------------

Before closing this post, I would like to debunk other misconceptions that I often hear. Some people say that semi-sync (or lossless semi-sync) increases the availability of MySQL. In my humble opinion, **this is false.** Semi-sync and lossless semi-sync actually lower availability, there is no increase here.

#### Lossless semi-sync is not a high availability solution.

The statement that semi-sync and lossless semi-sync have lower availability than standard replication is justified by the introduction of new situations where transactions could be prevented from committing. As an example, if no semi-sync slaves are present, transactions will not be able to commit. The promise of lossless semi-sync is not about increasing availability, it is about preventing the loss of committed transactions in case of a crash. The cost of this promise is the added COMMIT latency and the new cases where COMMIT would be prevented from succeeding (thus reducing availability).

#### Group Replication is not a high availability solution.

For the same reasons, Group Replication (or Galera or Percona XtraDB Cluster) reduces availability. Group replication also brings the promise of preventing the loss of committed transactions at the cost of adding COMMIT latency. There is also another cost of Group Replication: failing COMMIT in some situations (I do not know of any situation in standard MySQL where COMMIT can fail, if you know of one, please post a comment below). An example of COMMIT failing is mentioned in my previous post on [Group Replication certification](http://jfg-mysql.blogspot.com/2018/01/more-write-set-in-mysql-5-7-group-replication-certification.html). This additional cost introduces another interesting promise, but as this is not a post on Group Replication, so I am not covering this here.

#### Group Replication also introduces cases where COMMIT can fail.

This does not mean that lossless semi-sync and Group Replication cannot be used as a building block for a high availability solution, but by themselves and without other important components, they are not a high availability solution.

Thoughts about rpl_semi_sync_master_{timeout,wait_no_slave}
-----------------------------------------------------------------

Above, I write that there are situations where a transaction will be prevented from committing. One of those situations is when there are no semi-sync slaves or when those slaves are not acknowledging transactions (for any good or bad reasons). There are two parameters to bypass this: [rpl_semi_sync_master_wait_no_slave](https://dev.mysql.com/doc/refman/5.7/en/replication-options-master.html#sysvar_rpl_semi_sync_master_wait_no_slave) and [rpl_semi_sync_master_timeout](https://dev.mysql.com/doc/refman/5.7/en/replication-options-master.html#sysvar_rpl_semi_sync_master_timeout). Let's talk about these a little. 

The rpl_semi_sync_master_wait_no_slave parameter allows MySQL to bypass the semi-sync wait when there are not enough semi-sync slaves (semi-sync in MySQL 5.7 can wait for more than one slave and this behavior is controlled by the [rpl_semi_sync_master_wait_for_slave_count](https://dev.mysql.com/doc/refman/5.7/en/replication-options-master.html#sysvar_rpl_semi_sync_master_wait_for_slave_count) parameter). The default value for the "wait_no_slave" parameter is ON, which means it still waits even if there are not enough semi-sync slaves. This is a safe default as it enforces the promise of semi-sync (not acknowledging COMMIT before the transaction is replicated to slaves). Even if setting this parameter to OFF is voiding that promise, I like that it exists (details below). However, I would not run MySQL unattended with waiting disabled in a full semi-sync environment. 

The rpl_semi_sync_master_timeout parameter allows MySQL to short-circuit waiting for slaves after a timeout with acknowledging COMMIT to the client event is the transaction was not replicated. Its default is 10 seconds, which I think is wrong. After 10 seconds, there are probably thousands of transactions waiting for commit on the master and MySQL is already struggling. If we want to prevent MySQL from struggling, this parameter should be lower. However, if we want a zero-loss failover (and failover is taking more than 10 seconds), we should not commit transactions without replicating them to slaves, in which case this parameter should be higher. Higher or lower, which one should be used... 

Using a "low" value for rpl_semi_sync_master_timeout looks very strange to me in a full semi-sync environment. It looks like the DBA cannot choose between committing as often as possible (standard non-semi-sync replication) or only committing transactions that are replicated (semi-sync). There is no way to have the best of both worlds here:

*   either someone wants **high success rate on commit**, which means that the DBA does not deploy semi-sync (and the cost of this is to lose committed transactions on failover),
*   or someone wants **high persistence on committed transactions**, in which case the DBA deploys semi-sync at the cost of lowering the probability of a successful commit (and increasing commit latency).

I see one situation where these parameters are useful: transitioning from a non-semi-sync environment to a full semi-sync environment. During this transition, we want to learn about the new restrictions of semi-sync without causing too much disruption in production, and these parameters come in handy here. But once in a full semi-sync deployment, where we fully want to avoid loosing committed transactions when a master crash, I would not consider it a good idea to let transactions commit without being replicated to slaves. 

As a last comment on this, there are thoughts that a full semi-sync enabled master should probably crash itself when it is blocked for too long in waiting for slave acknowledgment. This is an interesting idea as it is the only way that MySQL has to unblock clients. I am not sure if this is implemented in some variant of MySQL though (maybe the Facebook variant). 

I hope this post clarified semi-sync and lossless semi-sync replication. If you still have questions about this or on related subjects, feel free to post them in the comments below.