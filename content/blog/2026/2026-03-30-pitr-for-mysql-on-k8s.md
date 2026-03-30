---
title: "Point-in-time recovery for MySQL on Kubernetes"
date: "2026-03-30T12:00:00+00:00"
tags: ['cloud', 'kubernetes', 'operators', 'mysql']
categories: ['cloud', 'mysql']
authors:
  - ege_gunes
---

Since the v1.0.0 release of the new MySQL Operator (K8SPS), point-in-time recovery (PiTR) has been the most anticipated feature. Naturally, we decided to implement it in the upcoming v1.1.0 release.

PiTR relies on two processes:
1. Reliably collecting binary logs from MySQL servers and storing them somewhere safe
2. When the recovery is triggered, applying those binary logs up to a specific point

## Collecting binary logs

Our Galera replication-based MySQL Operator (K8SPXC) has a binary log collector that was developed by the Cloud Team. It has worked reliably for years but has a certain limitation that is inherent in its design: it depends on flushing the binary logs to collect them. This leads to huge numbers of binary logs on the MySQL server, which becomes a headache after running the collector for a few weeks. We mitigated this for the users by maintaining a cache for binary logs, but it didn't remove the pain—it just became ours.

At Percona, #FindABetterWay is one of our core values. In the spirit of finding a better way, when we first started to think about PiTR in K8SPS, we decided to improve the process of collecting binary logs. These discussions eventually led to the birth of a new product: [Percona Binlog Server (PBS)](https://github.com/Percona-Lab/percona-binlog-server).

PBS works by connecting to the MySQL server as a replica and streaming events. It either uploads these events to S3 or stores them on the filesystem. It supports replication source switchovers and is able to continue from where it left off. On top of these, it provides helper commands to search for a particular GTID or timestamp in the collected binary logs.

## Applying binary logs

The official [MySQL docs](https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery-binlog.html) suggest converting each binary log to text using `mysqlbinlog` and piping them into the `mysql` client for PiTR. This is already what we do in K8SPXC.

I decided to check if there's a better way. First, I checked old posts on the Percona Blog to see if our experts had written anything about a different PiTR approach. It's not surprising that they did. [Marcelo](https://www.percona.com/blog/mysql-point-in-time-recovery-right-way/) wrote about an approach leveraging replication appliers for recovery. It seemed much better than piping `mysqlbinlog` output into the client, since with replication we can have multithreading and parallel appliers for recovery. My only problem with this approach was that it required two `mysqld` instances. Of course it's possible, but I would love to not have to care about the state of two MySQL servers.

Luckily, [lefred](https://www.percona.com/blog/mysql-point-in-time-recovery-right-way/#comment-10968578) commented that there's an ["even better" approach](https://lefred.be/content/howto-make-mysql-point-in-time-recovery-faster/) that requires only one MySQL server!

At a high level, the process looks like this:

1. Restore the full backup into the MySQL datadir
2. Start a temporary `mysqld` instance
3. Download binary logs and put them as relay logs in the datadir
4. Start replication via `CHANGE REPLICATION SOURCE TO RELAY_LOG_FILE=..., SOURCE_HOST='dummy'`
5. Start applying binary logs via `START REPLICA SQL_THREAD UNTIL <GTID>`
6. Wait for the SQL thread to stop
7. `STOP REPLICA; RESET REPLICA ALL;`

I have already created an unpolished but working [PoC](https://github.com/percona/percona-server-mysql-operator/pull/1252). There is also an [RFC](https://github.com/percona/percona-server-mysql-operator/pull/1251) for explaining various decisions and tracking open questions that need answers. There's still work to do, but I'm confident that this approach is good and we'll release this as a _tech preview_ in the upcoming v1.1.0 release. If you have thoughts on the RFC or want to try the PoC, we'd love to hear your feedback.
