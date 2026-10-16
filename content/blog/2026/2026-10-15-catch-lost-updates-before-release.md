---
title: "Catch Lost Updates Before Release: A Two-Client PostgreSQL Test on Windows"
date: "2026-10-15T00:00:00+00:00"
draft: true
tags: ['PostgreSQL', 'Concurrency', 'Testing', 'Docker', 'PowerShell', 'Windows']
categories: ['PostgreSQL', 'Community']
authors:
  - jack_vansickle
images: []
slug: catch-lost-updates-before-release
---

Two successful reservations of three units should reduce stock from ten to four. A read-calculate-write operation can instead leave seven: both clients overwrite the row with a value calculated from an earlier read. The useful release check is an invariant:

```text
final stock =
  starting stock -
  3 × committed reservations
```

Keep that assertion beside a controlled two-client test before releasing reservation code. This lab checks one inventory row at READ COMMITTED. Multi-SKU transactions, request idempotency, and Serializable retries need separate tests. It measures no throughput.

Count a reservation only after its UPDATE changes a row and COMMIT succeeds. The fixture stores one inventory row; application order records are outside this lab.

## The SQL failure and fix

The unsafe operation reads stock, subtracts three in application code, and writes its replacement:

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

A transaction around both statements does not preserve the invariant. A writes seven and holds its transaction open. B attempts the same update and waits. After A commits, B writes its stale seven and commits too.

At [READ COMMITTED](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED), PostgreSQL waits for a competing updater, then rechecks its condition against the updated row. The literal assignment still requests seven.

Move arithmetic and available-stock checking into the write:

```sql
UPDATE lu_lab.inventory
SET stock = stock - 3
WHERE sku = 1 AND stock >= 3
RETURNING stock;
```

B now subtracts from A's updated row. Starting at ten, A leaves seven and B leaves four. Starting at four, A leaves one and B's condition fails. [A zero-row UPDATE succeeds](https://www.postgresql.org/docs/18/sql-update.html); treat it as a rejected attempt. SKU 1 exists in this fixture. An application must also consider a missing SKU or other unmatched predicates.

RETURNING remains provisional until COMMIT succeeds. A returned row followed by ROLLBACK consumes no stock.

The positive integer three makes these examples directly runnable in psql. Before formatting fixture SQL, the Python helper requires exactly type int and a positive quantity. Application adaptations should use their database driver's parameter binding.

## Check the intended collision

Both workers begin at READ COMMITTED and read the seeded stock before A updates. A holds its transaction open while B issues the competing write. A's SQL session polls whether its PID appears in pg_blocking_pids(B). The test requires distinct worker PIDs and that blocking observation before releasing A's transaction. PostgreSQL documents these [session and blocker functions](https://www.postgresql.org/docs/18/functions-info.html).

A barrier establishes that both reads finished; the blocker check establishes database contention. Bounded waits and retrieved worker results make connection failures, missing lock waits, and worker exceptions fail the run.

Windows Python uses its standard library and Docker Desktop to coordinate persistent psql clients inside a disposable Linux Percona container. A separate controller session prepares and checks the fixture. The [lab appendix](/labs/postgresql-lost-update-pg18/README.txt) contains setup, commands, failure handling, and cleanup; the [complete Python source](/labs/postgresql-lost-update-pg18/lost_update_psql_lab.py) accompanies it.

## Assert outcomes, including rollback

Each attempt requests three units. These outcomes were observed on PostgreSQL 18:

Unsafe overwrite, two clients: starting stock 10; committed reservations 2; final stock 7. The defect is reproduced.

Conditional update, two clients: starting stock 10; committed reservations 2; final stock 4.

Conditional update, two clients: starting stock 4; committed reservations 1; final stock 1.

A rolls back while B waits: starting stock 4; committed reservations 1; final stock 1.

Insufficient stock, one client: starting stock 2; committed reservations 0; final stock 2.

Keep the unsafe case as a negative control: require seven and verify that it violates the invariant. Apply the invariant to every corrected case, checking committed count and final stock.

For rollback, A tentatively decrements four to one, B waits, and A rolls back. B then reserves three successfully. A contributes nothing to the committed count. The single-client insufficient case changes no row.

The column uses NOT NULL and CHECK (stock >= 0). Seven passes despite the lost update. [CHECK constraints](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS) reject invalid row values; they cannot reconstruct intent. Keep NOT NULL because a CHECK expression evaluating to NULL also passes.

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

Retain source, environment, output, and exit status together. Repetition checks this coordination, not every possible interleaving.

A conditional decrement does not make repeated requests idempotent. Multi-row work needs its own transaction rules and lock ordering. This harness does not exercise Serializable retries; applications using that isolation must [retry complete transactions after serialization failures](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html), including their reads and decisions.

Preserve the invariant, negative control, contention evidence, and failure assertions when adapting this release check.

*Automated Windows validation was AI-assisted using Codex on Jack VanSickle's SNOW-WOLF machine.*
