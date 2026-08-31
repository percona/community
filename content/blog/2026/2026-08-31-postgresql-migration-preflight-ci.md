---
title: "A Fail-Fast PostgreSQL Migration Preflight for CI"
date: "2026-08-31T11:00:00+00:00"
tags: ['PostgreSQL', 'Migrations', 'CI', 'Testing', 'QA', 'DevOps']
categories: ['PostgreSQL']
authors:
  - yizangeren
images:
  - blog/2026/08/postgresql-migration-preflight-ci-cover.png
slug: postgresql-migration-preflight-ci
---

A database migration can be syntactically correct and still be a poor release candidate. A regular index build can block writes, an `ALTER TABLE` may wait behind a conflicting lock or hold a strong lock longer than expected, and a large data modification can turn a routine deployment into an incident.

Static analysis cannot determine whether a migration is safe in production. It does not know table size, traffic, open transactions, data distribution, or how the migration runner executes the file. But it can catch a smaller class of mistakes where the SQL itself provides strong evidence of operational risk.

I built [postgres-migration-preflight](https://github.com/yZangEren/postgres-migration-preflight) as an experiment in that narrower problem. It parses PostgreSQL SQL into an abstract syntax tree (AST), evaluates statements in source order, and exits non-zero when configured blocking rules fire. The examples and documentation references below use PostgreSQL 18.

The goal is not to certify a migration as production-safe. It is to make obvious hazards difficult to merge unnoticed.

## Focus on risks visible from SQL

The first version deliberately limits itself to rules that can be explained from the migration text:

- regular `CREATE INDEX` and `DROP INDEX` operations;
- selected lock-sensitive `ALTER TABLE` operations;
- destructive DDL such as `DROP TABLE` and `TRUNCATE`;
- `UPDATE` or `DELETE` statements without a `WHERE` clause;
- DDL without a preceding non-zero session-level `lock_timeout`;
- SQL that the parser cannot understand.

These rules are heuristics, not proofs. A normal `CREATE INDEX` allows reads but blocks inserts, updates, and deletes while the index is built. `CREATE INDEX CONCURRENTLY` avoids blocking those writes, but PostgreSQL performs two table scans, waits for relevant transactions, does more total work, and can leave an invalid index after certain failures. It also cannot run inside a transaction block. A migration framework may create such a transaction even when the SQL file contains no `BEGIN`, so the finding asks the reviewer to check both the index operation and the runner.

A normal `DROP INDEX` acquires an `ACCESS EXCLUSIVE` lock on the table. Its concurrent form reduces that interference but cannot run in a transaction block, cannot use `CASCADE`, and cannot remove an index that supports a `UNIQUE` or `PRIMARY KEY` constraint.

`ALTER TABLE` is a family of operations rather than one risk category. A column type change normally rewrites the table, but PostgreSQL can avoid the rewrite for some binary-compatible conversions. `SET NOT NULL` ordinarily scans existing rows, but can skip the scan when a valid `CHECK` constraint proves that no `NULL` can exist. A foreign key added as `NOT VALID` can enforce new writes before a separate `VALIDATE CONSTRAINT` checks existing rows with a less disruptive lock.

The current lab still blocks every column type change conservatively because it has no catalog context. That severity is a policy choice for review, not proof that a particular conversion will rewrite a table.

## Preserve order and fail closed

Some protections matter only when they appear before the statement they are meant to protect:

```sql
ALTER TABLE users
  ALTER COLUMN email TYPE varchar(320);

SET lock_timeout = '2s';
```

The timeout does not protect the preceding `ALTER TABLE`. The analyzer walks statements in source order and tracks the session-level `lock_timeout`. A non-zero value counts only for subsequent DDL, and setting it back to `0` disables the protection again.

This is a review signal, not a claim that a timeout makes DDL safe. `lock_timeout` limits only time spent waiting to acquire a lock. After the lock is acquired, an operation can continue much longer. An equal or shorter `statement_timeout` can also fire first.

The analyzer uses `pgsql-ast-parser` instead of regular expressions so supported rules operate on statement structure. It can distinguish an `UPDATE` with a predicate, a concurrent index declaration, and individual `ALTER TABLE` actions. An AST still does not provide catalog state or workload context. If the parser cannot understand valid PostgreSQL syntax, the tool emits `SQL_PARSE_ERROR` at blocker severity and exits non-zero. Parser failures are coverage gaps requiring review, not evidence that PostgreSQL would reject the migration.

## Compare passing and blocked migrations

A deliberately small passing example is:

```sql
SET lock_timeout = '2s';
SET statement_timeout = '15min';

CREATE INDEX CONCURRENTLY idx_users_last_seen_at
  ON users (last_seen_at);

UPDATE users
SET archived = true
WHERE id = 42;
```

The checker parses four statements and reports no findings. That result does not make the migration automatically safe: the caller still has to ensure the concurrent index statement is not executed inside a transaction block.

The blocked example contains stronger static signals:

```sql
CREATE INDEX idx_users_email
  ON users (email);

ALTER TABLE users
  ALTER COLUMN email TYPE varchar(320);

DELETE FROM audit_events;
```

The checker reports five findings: two critical, one high, and two medium. The critical findings cover the column type change and unbounded delete. The regular index build is high severity, while the medium findings identify DDL without a preceding non-zero `lock_timeout`. The process exits with code `1`, so CI can stop before deployment.

The examples test rule behavior, not the hardest PostgreSQL migration problems. A `WHERE` clause can still affect most rows of a large table, and a binary-compatible type change can be much cheaper than another statement with similar syntax. Production-scale changes still require workload-aware review.

## Give CI a simple contract

The CLI exits with `0` when no blocking finding exists, `1` when the migration is blocked, and `2` for invalid command usage. A minimal workflow is:

```yaml
- name: Install migration preflight
  run: npm ci

- name: Test the analyzer
  run: npm test

- name: Check the pending migration
  run: node src/check-migration.mjs path/to/migration.sql
```

JSON output can feed CI annotations or review tooling. The current test suite covers the passing case, the risky case, ordered timeout handling, and parser failure. I would introduce a gate gradually: start with rules supported by strong SQL evidence, measure false positives, and only then make broader organization-specific policies blocking.

The checker reports findings rather than rewriting migrations. Adding `CONCURRENTLY` can change transaction requirements and recovery steps, while splitting constraint creation and validation changes deployment sequencing. Those decisions still belong to the developer and reviewer.

## Keep the boundary explicit

SQL text cannot reveal relation size, data distribution, long-running transactions, current lock holders, replica lag, WAL capacity, application traffic, or a migration framework's transaction policy. PostgreSQL versions also differ in DDL behavior and available optimizations.

A passing preflight should therefore be followed by production-sized rehearsal and runtime verification for consequential migrations. That may include checking expected scans or rewrites, monitoring locks and replica lag, planning rollback procedures, and verifying constraints and indexes afterward. Following a failed concurrent index build, catalog state such as `pg_index.indisvalid` also needs inspection.

The value of a static gate is not that it understands production. Its value is that some mistakes do not require production knowledge to recognize. Catching those mistakes in CI leaves reviewers more time for the harder questions that static analysis cannot answer.

That is the boundary I want `postgres-migration-preflight` to maintain: a small, explainable first line of defense for PostgreSQL migrations, not a production-readiness oracle.

## References

- [PostgreSQL 18: Introduction to indexes](https://www.postgresql.org/docs/18/indexes-intro.html)
- [PostgreSQL 18: CREATE INDEX](https://www.postgresql.org/docs/18/sql-createindex.html)
- [PostgreSQL 18: DROP INDEX](https://www.postgresql.org/docs/18/sql-dropindex.html)
- [PostgreSQL 18: ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html)
- [PostgreSQL 18: Client connection defaults, including `lock_timeout`](https://www.postgresql.org/docs/18/runtime-config-client.html)
- [PostgreSQL 18: `pg_index` catalog](https://www.postgresql.org/docs/18/catalog-pg-index.html)
