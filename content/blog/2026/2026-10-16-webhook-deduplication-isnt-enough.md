---
title: "Why Webhook Deduplication Isn't Enough"
date: "2026-10-16T00:00:00+00:00"
tags: ['PostgreSQL', 'Webhooks', 'CRM', 'Concurrency']
categories: ['PostgreSQL']
authors:
  - yananai_chiwuta
slug: webhook-deduplication-isnt-enough
draft: true
---

Let's say you're processing events from an API into your CRM. An event comes in and tells you that a particular contact is a Director at a company. So you update the job title on their contact record in the CRM, along with some other fields like the company and whether they're qualified.

A few seconds later, you receive another webhook telling you the same contact is a Manager at that company.

What's happened here is that the second update was older than the first, but it took longer to arrive, and it has a different event ID.

This kind of thing is a big problem for GTM teams, because it affects how they segment, score and reach out to prospects.

The obvious thing to do to prevent things like this happening is to de-duplicate your webhooks – that is, make sure you're not processing the same event twice.

However, this doesn't help here.

Even though the handler was de-duplicating events, the second event still overwrote the information from the first.

To demonstrate the difference between the two methods, I've put together a small fixture in Python and Postgres. The two methods both de-duplicate events, and both process the database transactionally – the only difference is that the second one checks whether the contact revision in the incoming event is newer before it updates the CRM.

*Note: this isn't based on a real incident, or a real CRM – all records used here are synthetic.*

## Two different identities, two different guarantees

We're modelling a scenario where an external data provider periodically sends complete snapshots of a set of data fields for each contact (in this case, `company`, `job_title` and `lead_status`). Each event contains a tenant ID, the name of the provider, a unique event ID, and the ID of the contact to which the data applies. The data from the event also includes a revision from the source.

We're using Postgres and have two tables of interest:

- `inbound_events`, with `PRIMARY KEY (tenant_id, provider, event_id)`, to answer "have we seen this event before?"
- `crm_contacts`, with `PRIMARY KEY (tenant_id, provider, contact_id)`, to store the latest accepted snapshot for each contact.

The primary key on the first table lets us quickly determine whether we've seen an event before; the primary key on the second lets us find the contact the event concerns. But we also need a way to determine whether the snapshot in the event is more recent than what we have stored.

For this experiment, we're assuming that the revision field contains a monotonically increasing integer, which we can trust to accurately reflect recency of the data from the provider. The provider might skip revisions, but if it sends us revision 10 and then revision 12, we know 12 represents the more recent state of the data in the source.

| Arrival order | Event ID | Source revision | Job title | Lead status |
|---|---|---:|---|---|
| First | `e10` | 10 | Analyst | new |
| Second | `e12` | 12 | Director | customer |
| Third | `e11` | 11 | Manager | qualified |

Each event has a unique ID, so it represents a legitimate event to record. But when we receive `e11`, we already have revision 12 for the contact, so it would be incorrect to replace the existing data with the new (actually, older) data.

## First, make deduplication work correctly

The following SQL is run in both cases to claim an event:

```sql
INSERT INTO inbound_events
    (tenant_id, provider, event_id, contact_id, source_revision, snapshot)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (tenant_id, provider, event_id) DO NOTHING
RETURNING event_id;
```

That SQL relies on the table's primary key to prevent it from creating a new row. If the `RETURNING` clause yields no results, the existing event is read from the database and the contact ID, revision and snapshot are compared. The SQL includes `%s` placeholder strings, which are filled in by the psycopg driver.

That detail matters when two workers receive the same event concurrently. A unique-key conflict can force one worker to wait for the other's transaction. After that wait, the handler reads the existing event in a separate statement rather than relying on an earlier statement snapshot.

PostgreSQL's [transaction isolation documentation](https://www.postgresql.org/docs/17/transaction-iso.html) explains why statement snapshots matter in this situation.

The important point is that the control implementation already has working deduplication. The comparison doesn't depend on deliberately removing that protection.

## The control: every new event updates the CRM

The control handler receives each new versioned event and unconditionally UPSERTs the contact. This is the `ON CONFLICT` part of its contact `INSERT` statement:

```sql
ON CONFLICT (tenant_id, provider, contact_id) DO UPDATE SET
    source_revision = EXCLUDED.source_revision,
    company = EXCLUDED.company,
    job_title = EXCLUDED.job_title,
    lead_status = EXCLUDED.lead_status,
    last_applied_event = EXCLUDED.last_applied_event,
    application_count = crm_contacts.application_count + 1,
    updated_at = clock_timestamp()
RETURNING source_revision;
```

This works fine as long as the events are applied in source revision order, but what happens when they're not? Let's modify the test to insert events out of order, starting again with an empty database but this time inserting `e10`, `e12`, then `e11`. After `e12`, the contact is at revision 12 and has ExampleCo-12 / Director / customer from the enrichment store. When `e11` arrives, the control contact handler accepts the event (it has a new event ID) and applies the UPSERT. The result?

| Contact state after `e11` | Control handler |
|---|---|
| Source revision | **11** |
| Company | ExampleCo-11 |
| Job title | Manager |
| Lead status | qualified |
| Last applied event | `e11` |
| Application count | 3 |
| Event outcome | applied |

**Uh oh!** The source revision has gone backwards from 12 to 11.

Nothing failed at the database level. The event had a valid identity, the transaction committed and the handler did exactly what its SQL instructed.

Yet, somehow the data in the CRM system was older than it had been the last time delivery had occurred.

The issue here is that while the uniqueness of the event tells us whether we've seen it before, it doesn't tell a handler which order to apply updates to an entity in.

In order to fix this, it is necessary to ensure that an update only ever applies if the revision it represents is newer than the one currently held. The corrected code looks like this:

```sql
ON CONFLICT (tenant_id, provider, contact_id) DO UPDATE SET
    source_revision = EXCLUDED.source_revision,
    company = EXCLUDED.company,
    job_title = EXCLUDED.job_title,
    lead_status = EXCLUDED.lead_status,
    last_applied_event = EXCLUDED.last_applied_event,
    application_count = crm_contacts.application_count + 1,
    updated_at = clock_timestamp()
WHERE EXCLUDED.source_revision > crm_contacts.source_revision
RETURNING source_revision;
```

`EXCLUDED.source_revision` is the revision proposed by the incoming event. `crm_contacts.source_revision` is the revision already stored.

If the incoming revision is higher, PostgreSQL applies the update.

If it's equal or lower, the existing row isn't updated. The handler can then inspect the current contact and event history to classify what happened.

Running the same sequence against this implementation produced a different outcome:

| Contact state after `e11` | Unconditional control | Revision-aware handler |
|---|---|---|
| Source revision | **11** | **12** |
| Company | ExampleCo-11 | ExampleCo-12 |
| Job title | Manager | Director |
| Lead status | qualified | customer |
| Last applied event | `e11` | `e12` |
| Application count | 3 | 2 |
| `e11` outcome | applied | stale |

Even though the event handler code was fixed to avoid replacing revision 12 with the older inbound event `e11`, it still attempted to apply `e11` to the contact. However, since it didn't succeed in replacing the contact revision, the contact's application count, last applied event and `updated_at` timestamp were not affected.

The above state is the contact right after the first delayed event. It isn't where the test ends. The test then applies yet another event with a different ID and the same old snapshot, `e11-identical`. The control applies that too, so it finishes at revision 11 with an application count of 4. The revision-aware handler records it as stale, so it stays at revision 12 with a count of 2.

## What would happen if the workers were racing?

Although the above test scenario was useful for pinpointing the problem, in a real application, the webhooks would likely be processed by multiple workers concurrently.

It's possible to do the revision comparison in the application code (Python), but then one has to be careful about the stored revision changing between reading it and sending the update to PostgreSQL.

The test fixture avoids this problem by performing the revision comparison in the database in the contact UPSERT statement. It tests the concurrent execution of event handlers by connecting to the database with different connections.

The test starts with a contact at revision 10:

1. Worker A updates the contact to revision 12, then pauses **after** the contact UPSERT and **before** committing its transaction.
2. Worker B tries to apply another event with revision 11 to the same contact.
3. A third database connection observes what's happening.

Instead of assuming that the workers are contending with each other, the test inspects the Postgres activity and lock information to see what's going on:

```sql
SELECT pid, application_name, state, wait_event_type, wait_event,
       pg_blocking_pids(pid) AS blocking_pids
FROM pg_stat_activity
WHERE pid = ANY(%s)
ORDER BY pid;
```

The test also inspects `pg_locks` to see the corresponding transaction-ID locks.

Both times the test was run, it observed that one of the workers was indeed blocked by the other:

| Observation | Repetition 1 | Repetition 2 |
|---|---|---|
| Waiting worker's event | `Lock / transactionid` | `Lock / transactionid` |
| `pg_blocking_pids()` | Identified the revision 12 worker | Identified the revision 12 worker |
| Transaction-ID locks | Leader `ExclusiveLock` granted; follower `ShareLock` waiting | Leader `ExclusiveLock` granted; follower `ShareLock` waiting |
| Final contact revision | **12** | **12** |

In both runs, the revision 12 worker held a granted transaction-ID `ExclusiveLock`, while the other worker waited with an ungranted `ShareLock` on that transaction ID.

Once the revision 12 transaction committed, the waiting worker completed. Its revision 11 event was classified as stale.

The contact stayed at revision 12.

It was interesting to see that even though the stale UPSERT didn't actually do anything, it still had to wait. The [Postgres docs for `INSERT ... ON CONFLICT`](https://www.postgresql.org/docs/17/sql-insert.html) explain that the conflicting row is locked before the update's `WHERE` condition is evaluated, so there's still some lock contention even if the conditional update is rejected.

It may seem pedantic, but it's important to remember that the revision guard protects the state of the contact under the conditions tested. It doesn't make concurrent updates free of locking.

*Note: this was not intended as a benchmark, just something to work out if one worker would block the other and what state they were committed in.*

## Rollbacks, retries and contradictory revisions

Now, with the corrected handler:

What happened? Well, in the tests, after the UPSERT for the contact, but before the commit, an exception was injected. Due to the ACID properties of Postgres, that rolled back both the inbound event record and the mutation of the contact.

From an outside observer's perspective, the contact was still the original one that had been committed. But when the event was retried, it was only applied once.

There was another test that checked what happened when an exception was thrown after the commit. In this case, the caller didn't receive acknowledgement of the event.

In the database, the event had already been committed, and the contact had been created or updated. So, when the event was sent again, the contact wasn't changed.

There's a difference between throwing an exception before the commit and after the commit.

There is also a problem with two revisions from the same source being equal.

Two events with different event IDs that refer to the same revision of a contact may contain either (a) the same contact snapshot, in which case the second event is redundant (if it is for the current revision of the contact) or stale (if the contact has been revised further) unless it contradicts the retained revision history, or (b) different contact snapshots, in which case the two events present contradictory revision history from the provider.

The handler records a `revision_conflict` in the latter case and retains the previously accepted contact. It also checks for this when a contact is at a later revision but the events are retained in history. This way, it's possible to identify when a provider contradicts itself at an older revision, even if the contact has moved on.

It does not, however, determine which of the two conflicting payloads is the true one – it's a fixture to detect conflicts, not to resolve them.

There are tests for a few more things, including concurrent claims for the same event ID (and transaction rollback when that occurs), ensuring that events from different tenants or different providers don't affect each other, handling of explicit null values when supplied in a complete snapshot, and handling of events that don't provide a trustworthy revision.

The latter point is important: when an event is provided with no revision, the handler needs to record that it was seen but not alter the contact. It can't assume that the event is newer or older than the existing contact merely because it's arriving now.

## Reproducing the experiment

The complete fixture can be found in a [public repository](https://github.com/yananai-chiwuta/percona-crm-correctness): **PostgreSQL CRM correctness under duplicate and out-of-order events**.

The [exact tested release commit is `de003496`](https://github.com/yananai-chiwuta/percona-crm-correctness/tree/de00349697255cd4fd7e5b9d578c6a8eaf065478).

The repository contains a Python handler, PostgreSQL schema, tests, pinned dependencies and a GitHub Actions workflow. It doesn't include anything that would expose the handler as an HTTP endpoint for webhooks, or talk to a real CRM. It simulates the functions and database that are part of the fixture.

The fixture uses GitHub-hosted runners with temporary service containers for PostgreSQL, so there is no need to install it on a local machine.

It runs under the following environment:

| Component | Version |
|---|---|
| PostgreSQL server | 17.11 |
| Python | 3.12.15 |
| psycopg | 3.3.6 |
| pytest | 9.1.1 |
| Transaction isolation | READ COMMITTED |

A [verified run on GitHub Actions](https://github.com/yananai-chiwuta/percona-crm-correctness/actions/runs/38649001953) executes two independent repetitions against fresh instances of the temporary PostgreSQL service.

| Result | Repetition 1 | Repetition 2 |
|---|---:|---:|
| Tests passed | **85** | **85** |
| Failures, errors or skips | 0 | 0 |
| Observed blocking cases | 26 | 26 |

If you want to try to falsify this yourself and prove that it isn't correct, you can re-run the experiment by forking this repo, turning on GitHub Actions in your fork, and manually running the **CRM correctness experiment** workflow, ensuring all four jobs complete successfully on the same commit (two each for PostgreSQL 17.11 and Percona Distribution for PostgreSQL 18). The jobs create some evidence which you can download, but it won't be around for very long, so I've also attached the evidence from both runs to the [v1.1.0 release](https://github.com/yananai-chiwuta/percona-crm-correctness/releases/tag/v1.1.0) along with checksums. The important bits from the evidence are what you see here, and also in the repo's README.

*Note: there was one tricky bit that required a bit of work while developing this. One of the earlier runs failed because the observation query was trying to sort on the Postgres transaction ID directly. That doesn't work. But since the transaction ID was just used for sorting the results for display in the evidence, casting it to text was sufficient without changing anything about the processing or the assertions.*

The results you see above were run after making that change.

### Running it on Percona Distribution for PostgreSQL 18

I also ran the same tests against Percona Distribution for PostgreSQL 18.6.1, using the `percona/percona-distribution-postgresql:18.6.1-3` image (pinned by digest in the workflow). This was run twice as well, on fresh instances, against commit [`648beac`](https://github.com/yananai-chiwuta/percona-crm-correctness/tree/648beac9e5b3dae6e77b9a172c6604693dae5161) ([run 38931356745](https://github.com/yananai-chiwuta/percona-crm-correctness/actions/runs/38931356745)).

| Result | Repetition 1 | Repetition 2 |
|---|---:|---:|
| Tests passed | **85** | **85** |
| Failures, errors or skips | 0 | 0 |
| Observed blocking cases | 26 | 26 |

The outcome was the same as on 17.11. The control still went back to revision 11, the revision-aware handler stayed at revision 12, and the waiting worker was blocked by the revision 12 worker before it came back as stale.

## What this experiment does not prove

The revision guard depends on the contract on the events, namely:

- **The source provides revisions in a correct order.** The revision must come from something that can correctly and reliably order the updates to a given contact. Merely comparing two integers does not inherently establish which of two pieces of information is more recent.
- **The snapshots provided in the events contain all the fields enriched by the source.** If the source provides three fields, every accepted event must contain those three fields. If one of those fields should be cleared, the source must provide a value of null for that field. This doesn't handle the case where different sources are providing partial snapshots that need to be merged.
- **Revision conflicts are detected, not reconciled.** While the handler can detect when two snapshots with the same revision contain different information, and can ensure that a previously accepted snapshot is preserved, it has no way of determining which of the two payloads is correct.
- **An external CRM isn't part of the PostgreSQL transaction.** This experiment uses Postgres as the store for the contact information, which allows the handler to atomically commit the event and update the contact. If the update needed to be sent to an external API, the local PostgreSQL transaction alone couldn't ensure that both operations happened atomically.
- **This doesn't establish production correctness.** These tests only test a few specific sequences of event delivery. They don't prove that this approach is correct in all cases, that it will scale in a production environment, that it can handle all possible deadlocks, or that it will recover from all possible infrastructure problems.

## Conclusion

What went wrong? By applying an old event that was provided with a new ID to our duplicate-safe event handler, we created a situation where Postgres was happy to apply the transaction and still maintain a consistent event history according to our event handler rules. This allowed an old event to overwrite our CRM contact, reverting it from revision 12 back to revision 11.

By adding a condition to our UPSERT to only apply the contact update if the event's source revision is strictly higher than the one we already have, we can prevent this regression in all of the above scenarios. Interestingly, the concurrent scenarios still result in Postgres waiting on another transaction before returning.

This simple experiment illustrates two key questions we need to answer for an API-to-CRM workflow:

**Have we processed this event before?** – enforced by the event ID constraint.

**Are we sure that this event contains newer information than what we already have?** – enforced by trusting the ordering contract and only updating the CRM record if it is at a higher revision.

This experiment was built to illustrate the above point.

## References and tools

- [Companion code and tests](https://github.com/yananai-chiwuta/percona-crm-correctness)
- [Verified run on GitHub Actions](https://github.com/yananai-chiwuta/percona-crm-correctness/actions/runs/38649001953)
- [PostgreSQL 17: `INSERT` and `ON CONFLICT`](https://www.postgresql.org/docs/17/sql-insert.html)
- [PostgreSQL 17: Transaction Isolation](https://www.postgresql.org/docs/17/transaction-iso.html)
- [Verified run on GitHub Actions (Percona Distribution for PostgreSQL 18)](https://github.com/yananai-chiwuta/percona-crm-correctness/actions/runs/38931356745)
- [Evidence and checksums (v1.1.0 release)](https://github.com/yananai-chiwuta/percona-crm-correctness/releases/tag/v1.1.0)
- [Percona Distribution for PostgreSQL 18: Docker](https://docs.percona.com/postgresql/18/docker/docker.html)

*Methodology note: this is a synthetic experiment developed with the assistance of AI and verified through GitHub Actions runs.*
