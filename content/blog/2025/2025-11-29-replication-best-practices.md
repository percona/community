---
title: "MySQL Replication Best Practices: How to Keep Your Replicas Sane (and Your Nights Quiet)"
date: "2025-11-29T00:00:00+00:00"
tags: ["Opensource", "Percona", "replication", "MySQL", "Community", "Percona Server", "toolkit"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2025/12/mysql-replication-best-practice.png
---
MySQL replication has been around forever, and yet… people still manage to set it up in ways that break at the worst possible moment. Even in 2025, you can get burned by tiny schema differences, missing primary keys, or one forgotten config flag. I’ve seen replicas drift so far out of sync they might as well live in a different universe.

This guide covers the practical best practices—the stuff real DBAs use every day to keep replication stable, predictable, and boring. (Boring is a compliment in database land.)

### Always Use GTIDs. Yes, Always.
GTID-based replication is one of those features that people resist turning on, and then once they do, they never want to go back.

Why GTIDs?

- Failover become sane
- Reparenting replicas stops being a headache
- Missing transactions are easy to detect

Your my.cnf should absolutely include:
```
gtid_mode=ON
enforce_gtid_consistency=ON
log_replica_updates=ON
```
Once GTIDs are enabled, do not mix in old-style replication. That path leads straight to confusion.

### Use Row-Based Replication (RBR)
Statement-based replication is a nostalgia trip that nobody asked for. It breaks on:

- NOW(), UUID(), and similar functions
- Floating point differences
- Collation mismatches
- Triggers behaving differently

Just skip the pain and use:
```
binlog_format=ROW
```
RBR is slightly more verbose, but 100× more predictable. When something breaks, it’s never because you chose ROW.

### Every Table Needs a Primary Key. No Exceptions.
If you take nothing else from this guide, take this:

**Replication without primary keys is a bad time.**

Row-based replication needs a way to find the row that changed. Without a PK (or at least a UNIQUE index), the server has to use every column as a lookup. That’s slow, error-prone, and sometimes impossible.

The usual symptoms:
- Replication lag slowly creeping up
- Replica doing full table scans on updates
- Rows failing to apply
- Errors like:
```
Error 1032: Can't find record in table
```
Save yourself hours of debugging and just make sure every table has a primary key.

### Keep the Schema Identical Everywhere

Replication assumes that everyone’s using the same schema. MySQL will happily keep going even if your schemas don’t match—and then quietly drift out of sync.

Here are the practical ways to keep schemas aligned:

#### Approach A — mysqldump (most common)
Export schemas only:
```
mysqldump --no-data mydb > schema.sql
```
From both servers, then:
```
diff source-schema.sql replica-schema.sql
```

#### Approach B — information_schema metadata
This approach is great for automaton:
```
SELECT table_name, column_name, column_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'mydb'
ORDER BY table_name, ordinal_position;
```
Execute this query on each server and diff the results. Update mydb to match the database whose schema metadata you want to examine.

#### Approach C — pt-table-checksum (data only)
This doesn’t compare schemas — it catches data drift.
You should consider running it on a schedule such as:
- high-change OLTP DBs run weekly or even daily
- huge multi-TB DBs run quarterly
- some sensitive systems avoid running it during peak hours

```
pt-table-checksum --replicate=percona.checksums
```
You can fix drift with:
```
pt-table-sync --execute --replicate=percona.checksums
```
Schema checks + data checks = safe replication.

### Harden Your Binary Log Settings
Your binlogs are the backbone of replication. Treat them carefully.
```
sync_binlog=1
binlog_row_image=FULL
binlog_expire_logs_seconds=604800  # 7 days
```
sync_binlog=1 is the big one—without it, a crash can corrupt binlogs or the GTID position, and that leads to a very bad day.

### Protect Your Replicas with super_read_only
Never allow accidental writes to replicas, in your my.cnf set:
```
read_only=ON
super_read_only=ON
```
**super_read_only** closes the loophole that even SUPER users could previously use to write to replicas.

### Use a Dedicated Replication User
Give the minimal permissions:
```
CREATE USER 'repl'@'%' IDENTIFIED BY 'strong_password';
GRANT REPLICATION REPLICA ON *.* TO 'repl'@'%';
```
This user should do exactly one thing: replicate.
Don’t reuse app users—you’re just begging for trouble.

### Replication Lag: Watch It Like a Hawk
Seconds_Behind_Source lies more often than you’d expect. It’s okay for a quick glance but don’t rely on it.

Better options:
- Performance Schema: replication_applier_status_by_worker
- Percona Monitoring and Management (PMM)
- Custom heartbeat tables
- pt-heartbeat

Lag is one of the biggest causes of outages—monitor it continuously. Lag is usually the first sign something is wrong—catch it early.

### Use Parallel Replication (But Don’t Overdo It)
If your primary has multiple writers or many concurrent transactions, in your my.cnf enable parallel workers:
```
replica_parallel_type=LOGICAL_CLOCK
replica_parallel_workers=4
```
4–8 workers is a sweet spot for most systems. More workers ≠ more speed; after a point it just increases memory footprint without real benefit.

But when it helps, it really helps—like cutting lag by 80–90%.

### Use SSL Anywhere Outside the LAN
Replication traffic isn’t something you want exposed.
```
source_ssl=1
source_ssl_ca=/path/ca.pem
```
Earlier versions used the master_ssl_* variables, but the idea is the same: encrypt the connection when it leaves your trusted network.

## Final Thoughts

MySQL replication can be rock-solid, but only if you follow a handful of rules that experienced DBAs know by heart:

- Use GTIDs
- Use RBR
- Always have primary keys
- Keep schemas aligned
- Check for data drift
- Harden binlog settings
- Protect replicas from accidental writes
- Monitor lag properly
- Use parallel workers when appropriate
- Encrypt connections over untrusted networks

Follow these, and your replicas will stay healthy, consistent, and (mostly) invisible—which is exactly how you want them.