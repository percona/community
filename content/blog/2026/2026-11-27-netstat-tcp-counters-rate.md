---
title: "Community Contribution Spotlight: Fixing the Netstat TCP Panel in PMM"
date: "2026-11-27T10:00:00+00:00"
draft: true
tags: ['PMM', 'Prometheus', 'PromQL', 'Grafana', 'Community', 'Contributions']
categories: ['PMM']
authors:
  - daniil_bazhenov
images:
  - blog/2026/11/netstat-tcp-counters-rate-cover.png
slug: netstat-tcp-counters-rate
---

Open **OS > Network Details** in Percona Monitoring and Management (PMM) 3.10.0 or earlier and look at the **Netstat: TCP** panel. On a busy node you'll see lines in the hundreds of thousands, climbing slowly and never coming down. On one of our test nodes, `ActiveOpens` sat at about 340,000.

That number isn't how many connections your node opens. It's how many it has opened since it last booted. The panel was graphing raw counters, so a connection storm at 3 a.m. barely moved the line.

Bastian Triller, an engineer at Placetel in Cologne, found the problem, fixed it, and sent the fix as a pull request. It shipped in PMM 3.11.0. This post walks through what was wrong, why the fix looks the way it does, and how you can spot the same mistake in your own dashboards.

## From a wrong graph to a merged fix

Bastian filed [PMM-15559](https://perconadev.atlassian.net/browse/PMM-15559) with a precise ask: use `rate()` or `irate()` for the five TCP counters on the panel, and put the established connections on their own axis. Then he didn't wait for someone else to do it. He changed the dashboard JSON himself and opened [percona/pmm#5913](https://github.com/percona/pmm/pull/5913).

Mattia Simonato from the PMM team reviewed it. He reproduced the problem on a test node, confirmed the numbers, refined the fallback query, and added a release note on top of Bastian's commit. The PR merged on 11 November 2026.

That's what a good community contribution looks like: a real problem, a clear ticket, and a patch that's small enough to review. Thank you, Bastian.

## Counters and gauges

Prometheus has two kinds of numeric metrics that matter here:

- A **counter** only goes up. It resets to zero when the process or the host restarts. Examples: bytes sent, queries executed, TCP connections opened.
- A **gauge** goes up and down. It's a snapshot of the current state. Examples: memory in use, replication lag, connections open right now.

The raw value of a counter is almost never what you want on a graph. You want how fast it grows.

The TCP metrics in this panel come from the node exporter, which reads them from `/proc/net/snmp`. Five of them are counters:

| Metric | What it counts |
|---|---|
| `node_netstat_Tcp_ActiveOpens` | Connections this host initiated |
| `node_netstat_Tcp_PassiveOpens` | Connections this host accepted |
| `node_netstat_Tcp_EstabResets` | Established connections that were reset |
| `node_netstat_Tcp_AttemptFails` | Connection attempts that failed |
| `node_netstat_Tcp_RetransSegs` | TCP segments retransmitted |

The sixth, `node_netstat_Tcp_CurrEstab`, is a gauge: the number of connections in the `ESTABLISHED` or `CLOSE-WAIT` state right now.

Here's the trap. By convention, Prometheus counters end in `_total`. These don't, because the names come straight from the kernel's SNMP MIB. Nothing in `node_netstat_Tcp_ActiveOpens` tells you it's a counter. You have to know.

## What `max_over_time` did to a counter

Before the fix, each counter in the panel used this query:

```promql
max_over_time(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[$interval])
  or
max_over_time(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[5m])
```

`max_over_time` returns the highest sample in the window. For a gauge, that's a sensible choice: it keeps short peaks that a plain sample at each step could skip.

For a counter, the highest sample in any window is simply the latest one. So `max_over_time(counter[$interval])` is just the counter, which is the total since boot. Every series on the panel became a slow upward ramp. A spike of a few thousand retransmits disappeared into a line that was already at hundreds of thousands.

It got worse because all six series shared one Y axis. `CurrEstab` was around 100 on that test node. Next to counters in the hundreds of thousands, it was a flat line at zero.

## `rate()` and `irate()`

After the fix, the same counter uses this query:

```promql
rate(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[$interval])
  or
irate(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[5m])
```

Here's what each part does.

**`rate(x[$interval])`** is the per-second average increase across the window. It also handles counter resets: if the value drops, for example after a reboot, `rate()` treats it as a reset to zero instead of a huge negative jump. That's the main reason not to calculate rates by hand with subtraction.

**`irate(x[5m])`** uses only the last two samples in the window. It reacts fast and shows sharp spikes, which is useful on short time ranges. On long ranges it's misleading: each point on the graph sees only two samples, so spikes appear and disappear as you zoom. That's why `irate()` isn't the primary query here.

**`or`** is the fallback. `rate()` needs at least two samples in the window to return anything. If `$interval` is shorter than the scrape interval, the left side is empty, and `or` falls back to `irate()` over a fixed five minutes. You'll see the same `rate ... or irate` pattern in the **TCP Segments** and **Netstat: UDP** panels on the same dashboard, so the panel now matches its neighbors.

After the change, the counters on the same test node read between zero and 12 per second. That's a number you can alert on, compare across nodes, and correlate with an incident.

## Keeping the gauge as it was

`CurrEstab` keeps its original query:

```promql
max_over_time(node_netstat_Tcp_CurrEstab{node_name=~"$node_name"}[$interval])
```

Running `rate()` on a gauge would give you the rate at which the number of open connections changes. That's rarely what you want. `max_over_time` is the right function for a gauge, because it keeps the peak inside each step.

The other half of Bastian's change moves `established` to its own Y axis on the right:

```json
"seriesOverrides": [
  {
    "alias": "established",
    "yaxis": 2
  }
]
```

The left axis now uses the `ops` unit (operations per second), and the right axis is labeled **Connections**. You can read the connection rate and the number of open connections on one panel without either scale flattening the other.

![The Netstat: TCP panel before and after the fix. Before, max_over_time() plots counter totals since boot. After, rate() shows events per second and a connection storm stands out.](blog/2026/11/netstat-tcp-before-after.svg)

The chart above is an illustration with synthetic data. The shapes match what Mattia measured on a real node: totals in the hundreds of thousands before, zero to 12 events per second after.

## Check your own dashboards for the same bug

This mistake isn't specific to PMM. Any dashboard can graph a raw counter, and it's easy to miss when the metric name doesn't end in `_total`. A few quick checks:

- **Look at the shape.** A line that only climbs, with small steps and no dips except at restarts, is almost always a raw counter.
- **Look at the magnitude.** If a "per something" panel shows six or seven digits on a quiet host, check the query.
- **Read the source.** For node exporter metrics, the kernel documentation for `/proc/net/snmp` and `/proc/net/netstat` tells you which fields are cumulative.
- **Match the function to the type.** For counters, use `rate()`, `irate()`, or `increase()`. For gauges, use `max_over_time()`, `avg_over_time()`, or the raw value. Never `max_over_time()` on a counter, and never `rate()` on a gauge.

## Shipped in PMM 3.11.0

The fix is in [PMM 3.11.0](https://docs.percona.com/percona-monitoring-and-management/3/release-notes/3.11.0.html), released on 26 November 2026. The same release adds alerts on slow queries from Query Analytics data, scheduled Advisors that email their results, a native PMM UI Inventory page, and the `pmm-admin update` command. After you upgrade PMM Server, the **Netstat: TCP** panel shows rates on all your nodes. You don't need to change anything on PMM Client.

## Found a panel that looks wrong?

Most PMM dashboards are JSON files in the [`dashboards/` directory of percona/pmm](https://github.com/percona/pmm/tree/main/dashboards). If a panel shows numbers that don't make sense, you can:

- File a ticket in the [PMM Jira project](https://perconadev.atlassian.net/jira/software/c/projects/PMM/issues) with the panel name, the query, and a screenshot. That alone is a useful contribution.
- Send a PR against `percona/pmm` with the fix, as Bastian did. Put the Jira key in the title, and the team will help with the rest.
- Ask on the [Percona Community Forum](https://forums.percona.com/) if you're not sure whether it's a bug.

Which PMM panel have you stopped trusting? Tell us, or better, open a ticket.
