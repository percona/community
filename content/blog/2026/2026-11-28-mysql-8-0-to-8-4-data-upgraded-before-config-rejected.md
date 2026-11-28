---
title: "MySQL 8.0 to 8.4: the data was upgraded before the config file was rejected"
date: "2026-11-28T10:00:00+00:00"
draft: false
tags: ['MySQL', 'Upgrade', 'Replication']
categories: ['MySQL', 'Community']
authors:
  - fahri_cap
images:
  - blog/2026/11/mysql-8-0-to-8-4-upgrade-cover.png
slug: mysql-8-0-to-8-4-data-upgraded-before-config-rejected
---

MySQL 8.0 is out of community support, so a lot of 8.0 servers are about to become 8.4 servers. I wanted to know what an in-place upgrade does to a server that has been carried forward for years: first deployed on 5.7, upgraded in place to 8.0, with config lines added along the way and never cleaned. So I built one in a lab and upgraded it twice: once without preparing, once after fixing what the upgrade checker reported.

The result I did not expect: in this lab, MySQL 8.4 completed the data dictionary upgrade, then rejected an obsolete line in `my.cnf` and shut down. After that, 8.0 would not start on the same data directory. A config mistake did not fail safely.

The examples use synthetic data in disposable local containers. AI assistance was used to build the lab scripts and draft the text. The full output of the runs is published with the scripts, linked at the end.

## What the lab controls

Two servers, a primary and a replica, on the official Docker images, pinned:

```text
mysql:8.0.46   MySQL 8.0.46 Community Server
mysql:8.4.13   MySQL 8.4.13 Community Server, MySQL Shell 8.4.10
mysql:26.10.0  used only for MySQL Shell 26.10.0, in the follow-up checks
```

The 8.0 servers were set up the way long-lived servers look:

- a config file with `default_authentication_plugin`, `expire_logs_days`, `master_info_repository`, `relay_log_info_repository`, `binlog_transaction_dependency_tracking`, `transaction_write_set_extraction`, `skip_host_cache` and `ssl = ON`
- root, application and replication accounts on `mysql_native_password`
- replication configured with `CHANGE MASTER TO` and `START SLAVE`
- a foreign key that references a non-unique index
- a table with `AUTO_INCREMENT` on a `DOUBLE` column
- columns named `manual`, `parallel` and `qualify`

MySQL 8.0.46 runs all of this with deprecation warnings. The lab is one machine with a few rows per table. It shows what breaks and in what order. It says nothing about duration. The unprepared upgrade was done on the replica and the prepared one on the primary, so the two runs are not identical copies of one server.

## What the upgrade checker said

```text
mysqlsh --uri root@primary:3306 --js \
  -e 'util.checkForServerUpgrade(undefined, {targetVersion: "8.4"})'

Errors:   7
Warnings: 24
Notices:  2
```

The seven errors were five removed system variables, `default_authentication_plugin`, and the `AUTO_INCREMENT` column. The warnings were four accounts on `mysql_native_password`, the foreign key, and 19 changed defaults.

This was Shell 8.4.10, the version in the 8.4.13 image. It is older than the target server: asked for `targetVersion: "8.4.13"`, it says that upgrade is not supported and suggests `8.4`. Its `list` option showed 12 of its 42 checks included for 8.0 to 8.4, and `reservedKeywords` was not one of them. I come back to the current Shell below.

## First start: a clean failure

I swapped the replica's image to 8.4 and started it on the 8.0 data with the old config.

```text
[ERROR] [MY-015118] [Server] AUTO_INCREMENT is not supported with DOUBLE/FLOAT field.
        Please consider fixing (Schema:shop, Table:legacy_counter, Column:seq).
[ERROR] [MY-010020] [Server] Data Dictionary initialization failed.
```

The data dictionary upgrade did not complete. MySQL 8.0 reopened the same data directory and replication resumed.

## Second start: no in-place way back

I fixed the column on the primary, let it replicate, and tried 8.4 on the replica again.

```text
[System] [MY-013413] [Server] Data dictionary upgrade from version '80023' to '80300' completed.
[System] [MY-013381] [Server] Server upgrade from '80046' to '80413' completed.
[ERROR] [MY-000067] [Server] unknown variable 'default_authentication_plugin=mysql_native_password'.
[ERROR] [MY-010119] [Server] Aborting
```

The upgrade completed and then the server refused its own config file. Starting 8.0 again:

```text
[ERROR] [MY-014061] [InnoDB] Invalid MySQL server downgrade: Cannot downgrade from 80413 to 80046.
        Downgrade is only permitted between patch releases.
```

The manual already says there is no in-place downgrade from 8.4 to 8.0. Its supported ways back are a logical dump and load, or replication, and only for rollback, before any new 8.4 functionality has touched the data. What the lab adds is the order: the data was upgraded before the obsolete option was rejected. If you have no tested backup or separate 8.0 copy at this point, you are fixing the config file under pressure.

## Eight starts for eight lines

In this lab each failed start reported only the next rejected line. It took eight failed starts to get a config file 8.4 accepted:

| Start | Rejected | Reported by the checker |
|---|---|---|
| 1 | `default_authentication_plugin` | yes |
| 2 | `expire_logs_days` | yes |
| 3 | `master_info_repository` | yes |
| 4 | `relay_log_info_repository` | yes |
| 5 | `binlog_transaction_dependency_tracking` | yes |
| 6 | `transaction_write_set_extraction` | yes |
| 7 | `skip_host_cache` | no |
| 8 | `ssl = ON` | no |

The last two are startup options. Neither Shell 8.4.10 nor Shell 26.10.0 mentioned them, even when given the config file with the `configPath` option. Either one keeps the server down.

## The check that finds them without touching the data

`mysqld --validate-config`, run with the 8.4 binary against the old config file, reports the same lines. No data directory is involved, so a failure costs nothing:

```shell
docker run --rm --entrypoint mysqld \
  -v "$PWD/my.cnf:/tmp/my.cnf:ro" mysql:8.4.13 \
  --defaults-file=/tmp/my.cnf --validate-config
```

It exits 1 with the same message the real start gave. It also stops at the first problem, so it took eight runs to work through the file, in the same order as the table above. The ninth run exited 0. Each run took under a second. If your config uses `!include` or `!includedir`, mount those files too.

## Running, and locked out

On the ninth start the server came up.

```text
$ mysql -uroot -p
ERROR 1524 (HY000): Plugin 'mysql_native_password' is not loaded
```

Root could not log in. Neither could the application account. The one account created with `caching_sha2_password` worked. `mysqladmin ping` reported the server alive throughout: it checks that the server answers, not that anyone can log in. A readiness check needs a real login and a query.

Adding `mysql_native_password = ON` under `[mysqld]` and restarting restored both logins. That is a bridge: the plugin is removed in 9.0, so accounts still on it need to move before a 9.x upgrade or they stop authenticating.

## What else changed

- `SHOW SLAVE STATUS`, `START SLAVE`, `STOP SLAVE`, `CHANGE MASTER TO`, `SHOW MASTER STATUS`, `SHOW SLAVE HOSTS`, `PURGE MASTER LOGS` and `FLUSH HOSTS` all returned error 1064. Monitoring that parses `Slave_IO_Running` gets nothing back.
- The replacements `SHOW REPLICA STATUS`, `START REPLICA`, `CHANGE REPLICATION SOURCE TO` and `SHOW REPLICAS` already work on 8.0.46, so scripts can be changed first. `SHOW BINARY LOG STATUS` and `RESET BINARY LOGS AND GTIDS` do not exist on 8.0.46.
- Keywords: on 8.4.13, `INFORMATION_SCHEMA.KEYWORDS` marks `QUALIFY` and `TABLESAMPLE` as reserved, and `MANUAL` and `PARALLEL` as not reserved (they became nonreserved in 8.4.11). Matching that, an unquoted `qualify` column failed with a syntax error and `CREATE TABLE tablesample` failed, while `manual` and `parallel` worked. `CREATE TABLE shop.tablesample` worked too, because a reserved word after a period needs no quotes. Since the list changed between 8.4 patch releases, I would quote all four.
- The foreign key to a non-unique index survived with a warning and was still enforced. Creating a new one failed with error 6125, because `restrict_fk_on_non_standard_key` is on by default. A dump of the old schema will fail to restore on 8.4 with default settings. Setting that variable to `OFF` for the restore is a temporary workaround (the variable is deprecated). Pointing the key at a unique or primary key is the fix, after checking the column has no duplicates.

## Replication and the new plugin

The 8.4 replica replicated from the 8.0 primary without changes. It broke when I moved the replication account to `caching_sha2_password`:

```text
Last_IO_Error: Error connecting to source 'repl@mysqlup-primary:3306'. ...
Message: Authentication plugin 'caching_sha2_password' reported error:
Authentication requires secure connection.
```

In the lab I fixed it by letting the replica fetch the source's public key:

```sql
STOP REPLICA;
CHANGE REPLICATION SOURCE TO GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;
```

That protects the password exchange only. Replication traffic stays unencrypted, and the replica trusts whatever key it is sent. Outside a lab, use TLS with certificate verification on the channel instead, set up before the account changes plugin:

```sql
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
  SOURCE_SSL = 1,
  SOURCE_SSL_CA = '/etc/mysql/certs/ca.pem',
  SOURCE_SSL_VERIFY_SERVER_CERT = 1;
START REPLICA;
```

## The prepared run

For the primary I did the work on 8.0 first:

1. `ALTER USER ... IDENTIFIED WITH caching_sha2_password BY '...'` for each account still on `mysql_native_password`. The old hash cannot be converted, so this needs the password, and every client using that account needs to be ready for it.
2. Re-pointed the foreign key at a parent table with a primary key.
3. Rewrote the config file and restarted **8.0** on it:

| Removed in 8.4 | What the 8.4 config has instead |
|---|---|
| `default_authentication_plugin` | removed; `authentication_policy` if you need to set it |
| `expire_logs_days = 7` | `binlog_expire_logs_seconds = 604800` (still 7 days) |
| `master_info_repository`, `relay_log_info_repository` | removed; tables are the only option |
| `binlog_transaction_dependency_tracking`, `transaction_write_set_extraction` | removed |
| `skip_host_cache` | `host_cache_size = 0` |
| `ssl = ON` | removed; TLS stays on when certificates are present, `require_secure_transport` enforces it |
| `log_slave_updates`, `innodb_log_file_size` (deprecated) | `log_replica_updates`, `innodb_redo_log_capacity` |

4. Ran the checker again: 0 errors, 19 warnings, all changed defaults.

Then I swapped the image. MySQL 8.4 started at the first attempt, the application account logged in, and the replica reconnected on its next retry. Row counts on primary and replica matched.

Step 3 is the one I would not skip. Every line 8.4 rejected had a replacement that 8.0.46 accepted, so the config file can be made 8.4-clean while going back is still possible.

## The current checker

I ran the same checks again with MySQL Shell 26.10.0 against the same 8.0.46 server and config file. It now runs `reservedKeywords` for 8.0 to 8.4 and found the `qualify` column. It did not flag the table named `tablesample`. Its syntax check, done against the 8.4.0 grammar, flagged a stored procedure that uses the `manual` column as an error, although that procedure ran on 8.4.13. As above, it did not mention `skip_host_cache` or `ssl`.

## What I took from it

- Use the current MySQL Shell checker and also `mysqld --validate-config` with the target binary. They check different things, and neither listed everything on its own.
- Make the config file 8.4-clean and restart 8.0 on it before swapping binaries.
- Test a real login and a query after every start, not a ping.
- Put TLS on the replication channel before changing the replication account's plugin.
- Upgrade replicas first and the primary last. For rollback, keep a tested backup or a separate 8.0 copy from before the upgrade. Do not plan on an 8.0 replica continuing to replicate from an 8.4 primary: the manual says replication from a newer source to an older replica is generally not supported.
- Rehearse the whole upgrade on a copy first. The checker, the config validation and a rehearsal catch different failures.

## Scripts and output

The lab (`run.sh` for the upgrade runs, `preflight.sh` for the follow-up checks, the config files, the SQL and the full output) can be downloaded from the reference page below. It needs Docker, publishes no ports and takes about ten minutes.

For the end of support dates and what the managed services charge to stay on 8.0, see the longer reference this test was run for: [MySQL 8.0 end of life: dates and cost by provider, and what broke when we upgraded to 8.4](https://www.oreonit.com/mysql-8-0-end-of-life-upgrade-to-8-4-what-breaks/).
