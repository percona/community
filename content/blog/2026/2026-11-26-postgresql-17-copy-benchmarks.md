---
title: "900,000+ Rows/Sec in PostgreSQL 17: Benchmarking COPY FROM STDIN vs. Batched INSERTs in Python & PHP 8.4"
date: "2026-11-26T00:00:00Z"
draft: false
authors:
  - santiago_zazo
categories:
  - PostgreSQL
tags:
  - PostgreSQL
  - Performance
  - Python
  - PHP
  - Benchmarks
description: "Reproducible PostgreSQL 17.12 bulk-ingestion benchmarks comparing row-by-row prepared INSERTs, 500-row batched INSERTs, and streaming COPY FROM STDIN—achieving 971,252 rows/sec (69.8x speedup) under 1.2 MB peak RAM."
---

High-volume CSV imports, IoT telemetry feeds, and audit log pipelines routinely bottleneck application backends when routed through ORM entity loops or batched `INSERT` statements. In this hands-on guide, we measure PostgreSQL 17.12's native `COPY FROM STDIN` protocol against traditional `INSERT` strategies using a reproducible CI benchmark suite, and cover the production safeguards needed for idempotent, memory-bounded ingestion.

## Why ORM Loops and Multi-Row INSERTs Hit a Wall

For a few hundred rows, prepared `INSERT` loops feel instantaneous. At 50,000 or 500,000 rows, three compounding costs pile up:

1. **Client-side object/array overhead:** Hydrating ORM entities or buffering 100,000 associative arrays in RAM quickly consumes hundreds of megabytes before a byte hits the wire.
2. **Per-statement round-trips and WAL overhead:** Sending 50,000 individual `INSERT` statements—even inside a single `BEGIN ... COMMIT` transaction—pays 50,000 client-server round-trips and executor tuple-routing invocations.
3. **SQL parsing and parameter limits on multi-row `INSERT`s:** Batching 500 rows into `INSERT INTO ... VALUES (...), (...)` reduces round-trips, but PostgreSQL still parses megabytes of SQL syntax and binds thousands of positional parameters (up to the 65,535 wire-protocol limit).

## Inside PostgreSQL `COPY FROM STDIN`

When you execute `COPY table_name (col1, col2, ...) FROM STDIN`, PostgreSQL switches the connection into `COPY_IN` streaming mode:

- **One parse and plan:** PostgreSQL parses and plans the `COPY` statement once, regardless of whether you stream 10,000 or 10 million rows.
- **Single continuous stream:** `libpq` transmits buffered chunks via `PQputCopyData` and closes with `PQputCopyEnd`.
- **Built-in observability:** Active `COPY` backends report real-time byte and tuple progress in `pg_stat_progress_copy`.

## Reproducible Benchmarks on PostgreSQL 17.12

Using our open-source benchmark suite ([`php-postgresql-copy-benchmarks`](https://github.com/Eelprofesor14/php-postgresql-copy-benchmarks)) running on **PostgreSQL 17.12** and **PHP 8.4.28 NTS** (4-vCPU AMD EPYC 9V74 Linux host, median of three 50,000-row runs after a 10,000-row warmup):

| Ingestion Strategy (50,000 rows) | Elapsed Time (ms) | Throughput (rows/s) | Peak Memory (MB) |
| :--- | ---: | ---: | ---: |
| Prepared `INSERT` (1 row/call, single txn) | `3,593.7 ms` | `13,913 rows/s` | `0.41 MB` |
| Batched `INSERT` (500 rows/stmt, single txn) | `199.0 ms` | `251,230 rows/s` | `1.18 MB` |
| Streaming `COPY FROM STDIN` (10k Generator chunks) | `51.5 ms` | `971,252 rows/s` | `1.17 MB` |

Streaming `COPY FROM STDIN` completed the 50,000-row load **69.8x faster** than single-row prepared statements (`3,593.7 ms` down to `51.5 ms`—nearly **1 million rows/second**) and **3.86x faster** than 500-row multi-value `INSERT` batches, while keeping peak allocator memory flat at **`1.17 MB`**.

*(In our companion Python/PostgreSQL telemetry pipeline of 50,000 rows, switching from batched `executemany()` to `COPY FROM STDIN` similarly reduced ingestion time from `4.82 s` to `0.34 s`—a 14.2x speedup—while cutting peak RAM by 73%.)*

## Production Safeguards: Staging Tables, Escaping & Dead-Letter Isolation

By default, `COPY` is all-or-nothing: one malformed row aborts the entire batch, and `COPY` does not natively support `ON CONFLICT DO UPDATE`. A resilient production pipeline combines three steps:

1. **Strict `COPY` text-format escaping:** Escape backslashes (`\\`) first, followed by `\t`, `\n`, `\r`, strip NUL bytes (`\0`), and represent `NULL` as `\N`.
2. **Pre-validation + JSONL Dead-Letter Queue (DLQ):** Validate types and UTF-8 encoding before streaming; route rejected rows with line numbers and error reasons to a DLQ file or table.
3. **Atomic `TEMP` staging upsert:** Stream clean rows into `CREATE TEMP TABLE telemetry_stage (LIKE telemetry INCLUDING DEFAULTS) ON COMMIT DROP`, then merge atomically with `INSERT INTO telemetry SELECT ... FROM telemetry_stage ON CONFLICT (ts_epoch, zone_id) DO UPDATE SET ...`.

All five runnable listings, strict escaping helpers, and GitHub Actions CI logs against PostgreSQL 17.12 are available at: <https://github.com/Eelprofesor14/php-postgresql-copy-benchmarks>.
