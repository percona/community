---
title: "InnoDB Redo Log Sizing: Stop Guessing, Start Measuring"
date: "2026-05-02T00:00:00+00:00"
tags: ["OpenSource", "Percona", "MySQL", "InnoDB", "Performance", "Database Tuning"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2026/05/innodb-redo-log-sizing.png
---

## Introduction

Many MySQL configurations inherit redo log sizing from defaults, aging blog posts, or configuration folklore.

`innodb_redo_log_capacity` gets set once… and then quietly fades into the background.

But redo log capacity directly shapes how efficiently MySQL absorbs writes, manages checkpoint pressure, and handles burst-heavy workloads.

Set it too low, and aggressive flushing can throttle throughput.  
Set it too high, and crash recovery can become painfully long.

Redo logs are more than crash insurance.

They are part of your write-performance architecture.

> Redo logs are the shock absorbers of write-heavy MySQL. Too small, and performance jolts. Too large, and recovery drags.

## Why Redo Logs Matter

InnoDB redo logs are often described as crash recovery journals, but that description undersells their real operational value.

Redo logs function as a write buffer between committed transactions and eventual data file writes.

When a transaction commits:

- Changes are written to the redo log first
- Dirty pages remain in memory
- Data pages are flushed later

This write-ahead logging (WAL) design allows MySQL to:

- Absorb bursts of write activity
- Reduce immediate random disk writes
- Smooth checkpoint behavior
- Preserve durability

Redo logs act like pressure regulators in a write-heavy system.

They absorb pressure spikes so the entire system doesn’t thrash every time demand increases.

Without enough redo capacity, MySQL has less room to absorb write bursts before it must flush aggressively.

## Checkpoint Age and Flushing Pressure

Redo log sizing becomes most visible when checkpoint pressure builds.

Checkpoint age represents how far current write activity has advanced beyond the last durable checkpoint:

`Checkpoint Age = Current LSN - Last Checkpoint LSN`

As checkpoint age approaches total redo capacity:
- Adaptive flushing intensifies
- Page cleaners become more aggressive
- Dirty pages flush faster
- Disk I/O spikes
- Latency often becomes unstable

This is where undersized redo logs can trigger flush storms.

> MySQL isn’t writing more data. It’s being forced to write sooner and less efficiently.

### Useful metrics

- `Innodb_checkpoint_age`
- `Innodb_buffer_pool_pages_dirty`
- `Innodb_data_fsyncs`
- `Innodb_log_waits`

> When redo space shrinks, MySQL doesn’t stop writing. It starts panicking earlier.

## Symptoms of Undersized Redo

Small redo logs rarely announce themselves directly.

Instead, they often masquerade as generalized storage or write-performance issues.

### Common warning signs

- Periodic write stalls
- Spikes in fsync activity
- Sharp increases in page cleaner workload
- TPS drops during burst traffic
- Dirty page percentage volatility
- Stable CPU, unstable write latency

### A common misdiagnosis

Many systems blame disks when the real issue is insufficient redo headroom.

If writes are arriving faster than redo can comfortably buffer them, MySQL is forced into reactive flushing patterns.

The problem may not be disk speed.

It may be timing pressure.

## Measuring with Status Counters

Redo log sizing should be based on observed workload, not memory percentages or inherited defaults.

### Step 1: Measure redo generation rate

Use:

```sql
SHOW ENGINE INNODB STATUS;
```

Track:

- Log sequence number
- Log flushed up to
- Last checkpoint at

Measure LSN growth over time:

`Redo Generation Rate = (LSN delta) / elapsed time`

### Example

If LSN grows by 4 GB over one hour:

- 1 GB redo capacity = frequent pressure
- 4 GB redo capacity = ~1 hour buffer
- 8 GB redo capacity = larger burst tolerance

### Step 2: Watch for log stress

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_log_waits';
SHOW GLOBAL STATUS LIKE 'Innodb_os_log%';
```
### Key metric

`Innodb_log_waits`

If this value increases, transactions are waiting for log free space.

That is one of the clearest signs your redo logs may be too small.

`Innodb_log_waits` is less a tuning suggestion and more a smoke alarm.

## Practical Sizing Strategy

Forget percentage-of-RAM formulas.

Redo logs should be sized around workload intensity.

**A practical starting point:**

Size redo capacity to hold 30 to 60 minutes of peak redo generation

### Example

Peak redo generation = 6 GB/hour

**Minimum:**

30 minutes = 3 GB

**Safer:**

60 minutes = 6 GB

**Heavy burst environments:**

Larger sizing may reduce flush volatility further

## Trade-Offs

### Smaller Redo Logs

**Pros:**

- Faster crash recovery
- Lower storage footprint

**Cons:**

- Increased checkpoint pressure
- More aggressive flushing
- Greater write instability

### Larger Redo Logs

**Pros:**

- Better burst absorption
- Smoother sustained write performance
- Reduced flush storms

**Cons:**

- Longer crash recovery
- Delayed visibility into pressure buildup

## Common Mistakes

1. **Treating redo like buffer pool sizing**
    Redo capacity is about write throughput buffering, not memory caching.

2. **Ignoring Innodb_log_waits**
    This can leave obvious pressure invisible until performance suffers.

3. **Oversizing without testing recovery**
    Large redo logs may improve runtime but worsen restart scenarios.

4. **Sizing for average load instead of peak**
    Redo logs exist to absorb pressure spikes, not calm periods.

## Final Thoughts

The right redo log size isn’t about maximizing a configuration value.

It’s about matching capacity to workload behavior.

- Too small, and MySQL becomes reactive.
- Too large, and crash recovery becomes the hidden tax.

When redo logs are properly sized, they fade into the background.

They quietly absorb bursts, smooth checkpoint behavior, and preserve performance consistency under pressure.

> Redo logs work best when they disappear into the background, quietly absorbing pressure instead of creating it.

Stop guessing.

Measure your workload, observe your log pressure, and size with intent.