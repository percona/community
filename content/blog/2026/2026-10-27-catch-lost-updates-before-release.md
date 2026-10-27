---
title: "Catch Lost Updates Before Release: A Two-Client PostgreSQL Test on Windows"
date: "2026-10-27T15:07:00+00:00"
draft: false
tags: ['PostgreSQL', 'Concurrency', 'Testing', 'Docker', 'PowerShell', 'Windows']
categories: ['PostgreSQL', 'Community']
authors:
  - jack_vansickle
images:
  - blog/2026/10/catch-lost-updates-before-release-cover.png
slug: catch-lost-updates-before-release
---

Two successful reservations of three units should reduce stock from ten to four. A read-calculate-write operation can instead leave seven: both clients overwrite the row with a value calculated from an earlier read. That mismatch is what this lab checks. The release check is an invariant:

```text
final stock =
  starting stock -
  3 × committed reservations
```

Keep that assertion beside a controlled two-client test before releasing reservation code. The lab uses one inventory row at READ COMMITTED, so the stock change is easy to compare with committed reservations. Multi-SKU transactions, request idempotency, and Serializable retries need separate tests. This lab measures no throughput.

For that comparison, count a reservation only after its UPDATE changes a row and COMMIT succeeds. The fixture stores one inventory row; application order records are outside this lab.

## The SQL failure and fix

Start with the unsafe operation: read stock, subtract three in application code, and write the replacement:

```sql
SELECT stock
FROM lu_lab.inventory
WHERE sku = 1;
-- Both clients read 10 and calculate 7.
UPDATE lu_lab.inventory
SET stock = 7
WHERE sku = 1
RETURNING stock;
```

Putting both statements in a transaction does not preserve the invariant. In the test, A writes seven and holds its transaction open while B attempts the same update and waits. After A commits, B writes its stale seven and commits too.

That wait is expected at [READ COMMITTED](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED). PostgreSQL waits for a competing updater, then rechecks its condition against the updated row. The problem is the assignment: it still asks PostgreSQL to write the literal seven.

To avoid that stale assignment, let the write do the arithmetic and check available stock:

```sql
UPDATE lu_lab.inventory
SET stock = stock - 3
WHERE sku = 1 AND stock >= 3
RETURNING stock;
```

With that change, B subtracts from A's updated row. Starting at ten, A leaves seven and B leaves four. Starting at four, A leaves one and B's condition fails. [A zero-row UPDATE succeeds](https://www.postgresql.org/docs/18/sql-update.html); treat it as a rejected attempt. SKU 1 exists in this fixture. An application must also consider a missing SKU or other unmatched predicates.

RETURNING remains provisional until COMMIT succeeds. A returned row followed by ROLLBACK consumes no stock.

The positive integer three makes these examples directly runnable in psql. Before formatting fixture SQL, the Python helper requires exactly type int and a positive quantity. Application adaptations should use their database driver's parameter binding.

## Check the intended collision

To check the fix, the test has to establish that B really waits for A. Both workers begin at READ COMMITTED and read the seeded stock before A updates. A holds its transaction open while B issues the competing write. A's SQL session polls whether its PID appears in pg_blocking_pids(B). The test requires distinct worker PIDs and that blocking observation before releasing A's transaction. PostgreSQL documents these [session and blocker functions](https://www.postgresql.org/docs/18/functions-info.html).

A barrier establishes that both reads finished, but it does not show that B waited for A's database lock. The blocker check supplies that evidence. Bounded waits and retrieved worker results make connection failures, missing lock waits, and worker exceptions fail the run.

Windows Python uses its standard library and Docker Desktop to coordinate persistent psql clients inside a disposable Linux Percona container. A separate controller session prepares and checks the fixture. The [lab appendix](/labs/postgresql-lost-update-pg18/README.txt) contains setup, commands, failure handling, and cleanup; the [complete Python source](/labs/postgresql-lost-update-pg18/lost_update_psql_lab.py) accompanies it.

## Assert outcomes, including rollback

With that overlap established, compare the committed count with the final stock. Each attempt requests three units. These outcomes were observed on PostgreSQL 18:

Unsafe overwrite, two clients: starting stock 10; committed reservations 2; final stock 7. The defect is reproduced.

Conditional update, two clients: starting stock 10; committed reservations 2; final stock 4.

Conditional update, two clients: starting stock 4; committed reservations 1; final stock 1.

A rolls back while B waits: starting stock 4; committed reservations 1; final stock 1.

Insufficient stock, one client: starting stock 2; committed reservations 0; final stock 2.

The unsafe case is useful precisely because it fails the invariant: keep it as a negative control, require seven, and verify the violation. For every corrected case, apply the same invariant and check both the committed count and the final stock.

For rollback, A tentatively decrements four to one, B waits, and A rolls back. B then reserves three successfully. A contributes nothing to the committed count. The single-client insufficient case changes no row.

These outcome checks matter even though the column uses NOT NULL and CHECK (stock >= 0). Seven passes despite the lost update. [CHECK constraints](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS) reject invalid row values; they cannot reconstruct intent. Keep NOT NULL because a CHECK expression evaluating to NULL also passes.

## Observed Windows validation

On October 15, 2026, twenty complete suites passed with eighty blocking observations: four paired cases per suite. A deliberately wrong-port probe exited 1 without a passing result.

| Environment | Recorded value |
| --- | --- |
| Run (UTC) | 2026-10-15T18:14:24.1203443Z to 2026-10-15T18:14:53.0113288Z |
| Server | PostgreSQL 18.6 — Percona Server 18.6.1, x86_64; server_version_num 180006 |
| Windows | Windows 11 Home 10.0.26300, build 26300 |
| Controller | PowerShell 7.6.5; Python 3.13.2 AMD64 |
| Docker | Desktop 4.95.0 (242831); client and Engine 29.8.2 |
| Image tag | percona/percona-distribution-postgresql:18.6 |

Image digest: `sha256:27a1dba816fcc4cec88f216d54e3ec86db4c1d4b16799f49800055c41606e11e`.

Harness SHA-256: `5d80c87e0ba114b5302efe2a97ac59bcdfaf3fb9f5952c853e512b7f2fada484`.

See the [recorded validation summary](/labs/postgresql-lost-update-pg18/recorded-evidence/psql-validation-summary.json).

Keep the source, environment, output, and exit status together when you repeat the lab, so you can tell exactly what was tested. Repetition checks this coordination, not every possible interleaving.

A conditional decrement does not make repeated requests idempotent. Multi-row work needs its own transaction rules and lock ordering. This harness does not exercise Serializable retries; applications using that isolation must [retry complete transactions after serialization failures](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html), including their reads and decisions.

When you adapt this release check, keep the invariant, negative control, contention evidence, and failure assertions together.

*Automated Windows validation was AI-assisted using Codex on Jack VanSickle's SNOW-WOLF machine.*

*This post is part of the [Percona Community Writers Program](/blog/write-for-percona-community/).*
