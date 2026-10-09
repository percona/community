---
title: "Retry-safe webhook ingestion with PostgreSQL: duplicates, concurrent requests and old snapshots"
date: "2026-10-08T00:00:00Z"
draft: false
authors:
  - aslan_akhmetov
tags:
  - PostgreSQL
  - Python
  - Testing
  - Concurrency
images: []
---

*This is a synthetic laboratory example, not a customer production incident. AI assisted with drafting and checking the material.*

A webhook sender cannot always tell whether a delivery worked. The receiver may commit a database transaction and lose the connection before returning a response. A retry then arrives for work that is already complete.

Event IDs address that ambiguity, but they do not solve ordering. Two different events can describe the same object, and the older event can arrive last. A receiver that blindly replaces the stored state can move an order from a newer revision back to an older one.

This lab uses two PostgreSQL tables and one transaction per delivery. It keeps an immutable record of accepted events and a current object snapshot. The tests use separate database connections, including cases where one transaction actually waits for another. There is no queue or HTTP framework in the example, so the database behavior is visible.

## Define what an event means

The example uses synthetic order snapshots with five fields:

```json
{
  "source": "shop",
  "event_id": "event-3",
  "object_id": "order-1",
  "revision": 3,
  "snapshot": {"status": "paid", "total_cents": 4200}
}
```

This design depends on a specific contract:

- The same event ID always identifies the same content within a source.
- Each object revision belongs to exactly one event ID.
- Revisions increase within an object, and each event contains a complete snapshot.
- The source namespace includes the provider account or tenant. It comes from authenticated context, not an untrusted request field.

Revision 3 can replace revision 1 without receiving revision 2. That is valid for complete snapshots. It would be wrong for events such as “add $10” or “remove line item 4,” which may depend on earlier changes. If the provider supplies neither ordered versions nor a way to fetch authoritative state, this receiver cannot manufacture an ordering guarantee.

The inbox remains append-only in this lab. Deleting old entries would change the period over which identity collisions can be detected.

## Put both identities in the schema

`schema.sql` creates the event inbox and the current projection:

```sql
CREATE TABLE webhook_inbox (
    source text NOT NULL CHECK (source <> ''),
    event_id text NOT NULL CHECK (event_id <> ''),
    object_id text NOT NULL CHECK (object_id <> ''),
    revision bigint NOT NULL CHECK (revision > 0),
    snapshot jsonb NOT NULL CHECK (jsonb_typeof(snapshot) = 'object'),
    received_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    PRIMARY KEY (source, event_id),
    UNIQUE (source, object_id, revision)
);

CREATE TABLE object_state (
    source text NOT NULL,
    object_id text NOT NULL,
    revision bigint NOT NULL CHECK (revision > 0),
    snapshot jsonb NOT NULL CHECK (jsonb_typeof(snapshot) = 'object'),
    PRIMARY KEY (source, object_id)
);
```

The inbox has two different identities to protect. Its primary key identifies a delivery across retries. Its second unique constraint prevents two event IDs from claiming the same object revision. Even if those two events carry identical JSON, the lab treats them as a violation of the stated source contract.

The projection has one row per object and source. An older snapshot can be retained in the inbox without becoming the current projection. `received_at` is diagnostic information; it never decides which state wins.

## Claim the event before changing state

The first statement attempts to add the event to the inbox:

```sql
INSERT INTO webhook_inbox
    (source, event_id, object_id, revision, snapshot)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
RETURNING event_id;
```

An inserted row means this transaction can proceed with the projection. No returned row requires another check; it does not automatically mean a harmless retry.

The Python code issues a separate query for the event ID and compares the stored object, revision and JSON value with the request. An exact match returns `duplicate`. A mismatch raises `ReusedEventId`. If the event ID is absent, the other unique constraint rejected the insert, so the code raises `ReusedRevision`.

Why a separate statement? At READ COMMITTED, an insert can wait for a conflicting transaction whose row was not visible in its initial snapshot. The next statement gets a new snapshot. Combining the insert and lookup into one statement changes that visibility question. [PostgreSQL transaction isolation](https://www.postgresql.org/docs/16/transaction-iso.html)

The conflict clause intentionally has no target. Targeting only `(source, event_id)` would leave a conflict on the separate object-revision unique constraint unhandled. PostgreSQL documents that an omitted target for `DO NOTHING` handles all usable unique constraints and indexes. The follow-up lookup then distinguishes the expected duplicate from a protocol conflict. [INSERT and ON CONFLICT](https://www.postgresql.org/docs/16/sql-insert.html#SQL-ON-CONFLICT)

The comparison also stays in PostgreSQL. Python considers `True == 1` to be true. That is not the identity rule wanted for JSON snapshots. A regression test retries the same event ID with `{"value": true}` changed to `{"value": 1}` and expects rejection.

## Advance the projection only to a newer revision

For a newly accepted event, the second write is:

```sql
INSERT INTO object_state AS current
    (source, object_id, revision, snapshot)
VALUES (%s, %s, %s, %s)
ON CONFLICT (source, object_id) DO UPDATE
    SET revision = EXCLUDED.revision,
        snapshot = EXCLUDED.snapshot
    WHERE current.revision < EXCLUDED.revision
RETURNING revision;
```

The version comparison belongs in the update itself. Reading a revision in Python and later issuing an unconditional update would leave a gap for another writer.

An event that advances the projection returns `applied`. An event that loses the version comparison returns `stale`; its inbox entry still commits. PostgreSQL does not return a row when the conflict row was locked but the update condition was false. [INSERT RETURNING behavior](https://www.postgresql.org/docs/16/sql-insert.html)

The lock-order test exercises both outcomes. First, revision 2 holds the object row while revision 1 waits. After revision 2 commits, revision 1 leaves it unchanged. In the other order, revision 3 holds the row while revision 4 waits; revision 4 advances it after the lock is released. The test checks the database's blocking relationship before releasing the first transaction, rather than relying on a guessed delay.

All writers of this projection must follow the same rule. Another application that writes an arbitrary revision directly can invalidate the guarantee.

## Keep the inbox and projection in one transaction

The public wrapper in `ingest.py` is deliberately small:

```python
def ingest(conn, event):
    with conn:
        result = apply_in_transaction(conn, event)
    return result
```

The connection uses READ COMMITTED with autocommit disabled. The return happens after the transaction context commits. An HTTP adapter must wait for this function to finish before acknowledging a delivery.

Two tests cover the response boundary. One closes a connection while its writes remain uncommitted; a new connection can then accept the same event. The other commits, closes the connection and retries as if the sender received no acknowledgement; the retry returns `duplicate`.

These are transaction-boundary simulations. They do not inject a broken network or kill the database server. The tests use disposable memory-backed storage, so they also do not demonstrate survival of a host power failure. Production durability depends on storage, WAL settings and replication policy. [PostgreSQL WAL configuration](https://www.postgresql.org/docs/16/runtime-config-wal.html)

## Run the tests

[Download the runnable lab](/labs/postgresql-webhook-lab-2026-10-08.zip), including the schema, Python implementation, tests and recorded verification logs. It needs Docker and Python 3.10 or later:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
LAB_PYTHON=.venv/bin/python bash run_lab.sh
```

The runner starts a separate container on a random loopback port and removes its own container when finished. It does not connect to an existing database. The image digest pins the PostgreSQL 16.14 build used for verification; the driver is psycopg2 2.9.10. The pin makes the lab reproducible and is not a production patch recommendation.

The suite checks these cases:

| Case | Expected result |
| --- | --- |
| Sequential retry | One inbox row; retry is `duplicate` |
| Concurrent duplicate, first transaction commits | Second waits, then returns `duplicate` |
| Concurrent duplicate, first transaction rolls back | Second waits, then applies the event |
| Revision 3 followed by 1 and 2 | Projection stays at 3; all three inbox entries remain |
| Different revisions contend for the same object | The greater revision wins in both tested lock orders |
| Connection closes before commit | Neither write survives; a retry can apply |
| Commit succeeds but acknowledgement is treated as lost | Retry is `duplicate` |
| Event ID or object revision is reused | Reject the conflict without changing the projection |
| Identical IDs from separate sources | Independent inbox and projection rows |
| 24 concurrent deliveries of eight events | Eight inbox rows, 16 duplicates, final revision 8 |
| Invalid snapshot or changed JSON type | Reject without accepting the conflicting data |

The verified full run passes 13 tests. The concurrency regression is also run 30 times; its log is included with the lab. The wall-clock time is a test result, not a throughput benchmark.

## The boundary of the guarantee

This receiver converges on the greatest accepted snapshot revision while recognising repeated deliveries. A successful duplicate or stale delivery can receive a success response. A changed event identity needs investigation. A transient database failure needs a retry of the entire transaction or a retryable response, not a success response hiding the exception.

External effects need a separate design. Sending email or charging a card inside this function would not make those operations atomic with PostgreSQL. For that extension, a transactional outbox can record work to dispatch, and the external receiver still needs an appropriate idempotency contract.

For the snapshot problem here, the useful division is explicit: the inbox answers whether an event was accepted, and the projection answers which version is current. The transaction ensures those answers cannot be committed halfway through a delivery.
