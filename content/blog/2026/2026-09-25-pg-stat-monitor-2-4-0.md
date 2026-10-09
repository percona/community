---
title: "Make pg_stat_monitor stable again!"
date: "2026-09-25T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_stat_monitor', 'monitoring', 'pg_artem']
categories: ['PostgreSQL']
authors:
  - artem_gavrilov
images:
  # TODO: add cover image, e.g. blog/2026/09/pgsm-2-4-0-cover.png (relative to assets/)
---

pg_stat_monitor started as a fork of pg_stat_statements, built to be a more advanced replacement for it. It provides more detailed information about query execution and groups it in configurable time buckets, so you can look at what happened in a particular time window. It also powers the Query Analytics feature in Percona Monitoring and Management. However, over time other work took priority at Percona, and the extension stopped getting the attention it needed. The original developers moved on to other things, and the reasoning behind several design decisions went with them. For a couple of years it stayed in maintenance mode, we were fixing reported bugs, and never stepped back to look at deep architectural issues. All that led to a degraded user experience and stability issues.

2.4.0 is our attempt to turn that around. It is the biggest release in years: about 250 commits since 2.3.2. We restructured the code and fixed bugs across the whole extension, and the C code got about 20% smaller. Among the fixes are several buffer overflows, a use-after-free, a lock ordering problem and a few statistics that were simply wrong. We also backported the pg_stat_statements regression tests. The most important fixes, though, are about memory management, and that is what this post is about. For everything else, see the [release notes](https://docs.percona.com/pg-stat-monitor/release-notes/2.4.0.html).

## The symptoms

Well, memory leaked under certain workloads. The end was always the same: the process eventually got killed by the OOM killer.

Not every workload was affected, it depended on how it was run. Queries sent over the simple protocol were fine. Named prepared statements leaked memory on every execution. Statements running through SPI inside a background worker leaked the same way. In both cases nothing reclaimed the memory, so growth stopped only when the session or the worker did.

Another problematic case is when statements produce warnings. On PostgreSQL 18 and earlier, each warning caused a small memory leak, which could accumulate over time if many warnings were generated.

## How PostgreSQL manages memory

Server code does not call `malloc()` and `free()` directly. Instead it uses memory contexts, also known as memory arenas outside PostgreSQL. Every allocation happens within a context, and freeing the context releases all allocated memory at once. Contexts form a tree structure, so freeing a parent context frees every child context as well. This is what lets PostgreSQL manage memory efficiently and survive an error thrown in the middle of a query.

So when you write an extension, you should keep in mind which context your allocations belong to and when that context will be freed.

Four contexts matter for our topic:

* `TopMemoryContext` is the root context for the backend. It lives as long as the backend does and is only destroyed when the backend exits.
* `TopTransactionContext` is reset at every commit and every abort, which deletes all of its child contexts.
* `MessageContext` is reset after each client protocol message.
* `ErrorContext` is reserved for error reporting. On PostgreSQL 18 and earlier, it is only reset during error recovery.

An extension can create its own context or use one of the existing ones. Choosing a context with the wrong lifetime causes problems: your data either vanishes too early or stays around longer than needed. The latter looks exactly like a leak, even though every byte is still accounted for.

## How pg_stat_monitor managed its memory

### The original design

pg_stat_monitor collects per-statement statistics in backend-local memory first, and dumps them into the shared time buckets when the statement finishes and we have the full set of data. That local memory lived in a context called `PgsmMemoryContext`, and it was created as a child of `TopMemoryContext`. `TopMemoryContext` lives as long as the backend does. So instead of relying on context lifetime, pg_stat_monitor used a persistent context, and for cleanup it used a reset callback assigned to another context: `MessageContext`. `MessageContext` is reset after every client protocol message, and a reset invokes the callback, which cleaned out `PgsmMemoryContext` without destroying it.

One detail matters for everything below. A reset callback in PostgreSQL is one-shot: it is popped off the context's callback list before it is called, so it fires once and is gone. To keep the cleanup working, pg_stat_monitor had to register a fresh callback for every message. It did this from the post parse analyze hook, one of the first steps in the statement lifecycle. So callback setup depends not on the statement finishing, but on the next message going through parse analysis. The design has two weak points, and we hit both of them.

### The callback is not registered on every execution path

Background workers have no `MessageContext`. So a statement running through SPI inside a background worker never arms the reset callback at all. Nothing resets `PgsmMemoryContext`, and because its parent is `TopMemoryContext`, nothing else is going to. It grows for the life of the worker.

Named prepared statements in the extended query protocol go through parse analysis once, and executions afterward do not trigger the post parse analyze hook. The `Parse` message arms the callback, the callback fires when `MessageContext` is reset after that message, and the hook never runs again to arm another one. With every `Bind` and `Execute` afterward, the context grows for the life of the session. This is the pattern database drivers use for prepared statements. The SQL-level `PREPARE` and `EXECUTE` commands are not affected, because each `EXECUTE` statement goes through parse analysis itself and re-arms the callback.

### The error path allocated into a context nobody resets

pg_stat_monitor records the warnings and errors a statement produces, so it hooks into the code PostgreSQL uses to emit log messages. That hook runs in the middle of error reporting, and error reporting has a memory context of its own, `ErrorContext`. PostgreSQL keeps that one reserved so it always has somewhere to build a message, even when the backend is short on memory. It is cleaned out when the server unwinds from a real error. A `WARNING` does not unwind anything, the statement simply carries on. PostgreSQL 19 added `ErrorContext` resets after reporting a warning, so this leak only affects PostgreSQL 18 and earlier.

Our hook copied the query text wherever it happened to be running, so that copy landed in `ErrorContext` instead of in pg_stat_monitor's own context. Nothing was ever going to reclaim it. The entry for the statement itself went to `PgsmMemoryContext`, so it stayed there until the next reset, if one ever came.

Both problems come from the same place. We inherited the design from pg_stat_statements, which we forked years ago, and we never revisited it as pg_stat_monitor grew code paths that upstream does not have. The test suite did not help either. We had nothing that ran a background worker in a loop, nothing that held a session open across thousands of `Bind` and `Execute` cycles, and nothing that measured backend memory at all. None of this is exotic.

## What we changed

Both problems have the same shape. The memory sat in a context that never dies, and the cleanup depended on an event that does not always happen. Rather than trying to make the cleanup callback fire on every path, we changed where the memory lives.

Every path that can execute a statement runs inside a transaction. Background worker SPI, named prepared statements, ordinary queries. A background worker may not have a `MessageContext`, but it always has a transaction.

The change is:

* `PgsmMemoryContext` is no longer a child of `TopMemoryContext`. It is created as a child of `TopTransactionContext`, so it is automatically deleted at every commit and every abort. There is no callback to register and nothing to re-arm, so there is no execution path left that can skip the cleanup.
* There is a special handling of subtransactions, but in any case the memory is tied to the top-level transaction and will be cleaned up when that transaction ends.
* The error and utility statement paths no longer allocate an entry at all. They use a local variable that goes away by itself when the function returns, which removes the `ErrorContext` allocations completely.

This covers all three cases from the beginning of the post. A background worker always runs its statements inside a transaction, so its memory is now freed when that transaction ends, the same as in a regular backend. Named prepared statements no longer depend on parse analysis to clean up after them, every `Execute` is followed by a commit that frees the memory. Warnings no longer allocate anything that outlives the hook.

## What's next

2.4.0 was about stabilizing the code base we already have. We reworked memory management, removed code we no longer need, and built the test coverage that should have been there from the start. We did not change how the extension is structured. That is the plan for the next major release: we want to revisit the architecture of pg_stat_monitor, starting with how it uses shared memory and how it behaves when that memory fills up.
