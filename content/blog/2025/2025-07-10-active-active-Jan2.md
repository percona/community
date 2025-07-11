---
title: "Active-active replication - the hidden costs and complexities"
date: "2025-07-10T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2025/07/jan-aa2-cover1.jpeg
---

In [Part 1](/blog/2025/06/18/postgresql-active-active-replication-do-you-really-need-it/) of this series, we discussed what active-active databases are and identified some "good" reasons for considering them, primarily centered around extreme high availability and critical write availability during regional outages. Now, let's turn our attention to the less compelling justifications and the substantial challenges that come with implementing such a setup.

## What are “bad” reasons?

### 1. Scaling write throughput

Trying to scale your write capacity by deploying active-active across regions may sound like a clean horizontal solution, but it is rarely that simple. Write coordination, conflict resolution, and replication overhead introduce latency that defeats the purpose. If you are thinking about low latency writes between regions like Australia and the US, keep in mind that you will still be paying the round-trip cost, typically 150-200ms+, to maintain consistency. Physics don’t do any favors. Even if you have multiple primaries, unless you accept weaker consistency or potential conflicts, your writes will not scale linearly. In many real-world cases, throughput actually suffers compared to a well tuned primary replica setup. If your real goal is better throughput, you are usually better served by:
   * Regional read replicas
   * Sharding
   * Task queuing and eventual delegation

### 2. Performance

Performance is often used as a vague justification. But active-active is not a panaceum for general slowness. If the issue is database bottlenecks, reasons may be as basic as not enough work spent on data structuring, indexing, query tuning or scaling reads before jumping into multi primary deployments. Way too often we find that performance problems come not from scale limits, but from poor design and neglected maintenance. We are in 2025 and lessons like [this classic one on fast inserts](https://www.depesz.com/2007/07/05/how-to-insert-data-to-database-as-fast-as-possible) are still painfully relevant. If what you are really facing is application level latency, that is a different challenge. And even then, active-active with strong guarantees often adds more latency, not less.

### 3. Load balancing

You don’t need multi-primary to load balance. If your goal is spreading traffic more evenly, and reads are your bottleneck, there are simpler and much safer ways to get there. That’s what read replicas are for. If what you are looking for is distributing writes, please re-read point 1: synchronizing state across regions adds cost, complexity, and consistency challenges. Multi-master does not eliminate contention, it just moves it. In these situations you will have conflicts, some due to lag, some for other reasons. Resolution logic becomes critical. Conflicts need to be logged and their resolution auditable.

### 4. Because other systems did it

The fact that multi master was possible in other systems is not, on its own, a good reason to adopt it. If you have worked with Oracle RAC or GoldenGate, you likely remember the long nights of debugging conflicts, performance issues, the layers of failover logic, the dedicated teams just to keep things running smoothly. These systems made big promises, but keeping them stable in production was rarely simple or cheap. Copying those patterns means copying those problems. And trying to reproduce them with PostgreSQL, or some other modern databases, often misses the point. This is our chance to rethink how we build, not repeat the same mistakes. If you are going to pay the cost of active active, make sure you are doing it for the right reasons, not just because it looks like something you are used to.

## The cost, the painful side of active-active

Let’s be very clear: active-active is not the shortcut it often appears to be. It's not simply "HA but better." It represents a fundamental system design change with significant, ongoing costs across engineering, operations, and product management. While it might be the only viable option in highly specific situations, by betting on extreme reliability, you are signing up for a hell of a lot of complexity.

Much of what makes active-active the *wrong* choice in typical scenarios comes down to these costs. So expect some repetition, that’s by design, because the price *is* the problem.

### 1. Conflict resolution is a problem of it’s own

Every multi-primary system has to answer one question: what happens when two nodes write to the same row at the same time?
PostgreSQL doesn’t have conflict resolution built-in. You can bolt it on with tools like pgactive or pglogical2, but none of them are perfect, far from it.

The most common approaches applied:

   * Last write wins (based on timestamps).
   * Source priority (some nodes win conflicts).
   * Application-defined merge logic.

They all come with trade-offs. None of them are free.

![PG Conflict](blog/2025/07/PG_conflict.png)

Consider how other systems handle this is very often not conflict handling but conflict avoidance:

   * CockroachDB avoids exposing raw conflict handling to users by using strict serializability and sacrificing performance
   * Oracle RAC handles it via centralized locking over a shared-disk architecture (and even that causes headaches)
   * CouchDB, which embraces multi-master natively, makes conflict resolution a first-class application responsibility and warns users upfront

Unless your app is very carefully designed to dodge conflicts, say, by writing to disjoint subsets of data, you're going to run into this. Probably when it's already too late and your data's out of sync.

### 2. Infrastructure & networking costs

Running active-active across regions increases your infra footprint and cost. Specifically:

   * More powerful machines or more of them – each node handles writes and replication
   * Higher network bandwidth usage – especially for busy systems or cross-region replication
   * Premium network setups – often needed for low-latency consistency
   * Increased complexity in monitoring – replication lag, node health, consistency checks

These costs aren’t just financial, they bleed into reliability and operational overhead too.

### 3. Operational and management overhead

Beyond setup, day-2 operations are where the real pain begins:

   * Deployments become dangerous – schema or app changes can break replication or trigger conflicts
   * Debugging is harder – tracing transactions across writeable nodes adds layers to incident response
   * Staffing costs rise – managing active-active needs deeper expertise in distributed systems
   * Auditing grows in importance – proving data consistency across nodes becomes a continuous task

Let’s be honest, what was hard before is now harder, and even the routine becomes risky.

## Don’t kill the messenger

I love food. Cooking, eating, talking about it. Anyone I’ve worked with can vouch that I’m a foodie at heart. I like spicy food, really spicy. In my kitchen, you’ll find everything from Sichuan pepper to naga jolokia “ghost pepper”, from kala namak to asafoetida. These aren’t ingredients you throw into every dish. The right spice, at the wrong time, ruins everything. The same spice, used precisely, can turn something ordinary into magic.

![PG Chili](blog/2025/07/PG_chili.png)

What’s exactly how active-active works. It’s not bad by nature, it’s just very specific. You need to understand the dish, the eater, and the context. If you add ghost pepper to scrambled eggs because someone said it’s “cool,” you’re very likely going to regret it. Same goes for multi-primary setups.

Know what you’re in for. Use the right tool for the right reason. And don’t reach for active-active just because it sounds hot.
(And if you *do* pull it off successfully, please send me your config. I owe you a beer.)
