---
title: "Community Contribution Spotlight: Fixing the Netstat TCP Panel in PMM"
date: "2026-11-27T10:00:00+00:00"
draft: true
tags: ['PMM', 'Prometheus', 'PromQL', 'Grafana', 'Community', 'Contributions']
categories: ['PMM']
authors:
  - daniil_bazhenov
  - catalina_adam
images:
  - blog/2026/11/netstat-tcp-counters-rate-cover.png
slug: netstat-tcp-counters-rate
---

When your application reports dropped or slow connections to the database, one of the first places to look in Percona Monitoring and Management (PMM) is the **Netstat: TCP** panel on the **OS > Network Details** dashboard. It shows how many connections the node opens, accepts, and loses, and how much traffic it has to resend.

Up to PMM 3.10.0, that panel couldn't answer the question. Its lines sat in the hundreds of thousands and only ever climbed, so you couldn't tell when a connection storm started or whether it was over.

Bastian Triller, an engineer at Placetel in Cologne, spotted why: the panel plotted running totals instead of rates. He sent a fix as a [pull request](https://github.com/percona/pmm/pull/5913), and the PMM team reviewed and refined it. Starting with PMM 3.11.0, the panel shows what's happening on your node right now.

Read on to see what the panel shows now, how to use it to track down connection problems, and how Bastian and the PMM team got the fix into PMM. If you build your own dashboards, you'll also learn how to check them for the same mistake.

## What the panel showed before 3.11.0

On one of our test nodes, the `activeOpens` line read about 340,000. That wasn't how many connections the node was opening. It was how many it had opened since it last booted. Every line on the panel was a running total like this, so you couldn't tell a quiet hour from a busy one, or when a problem started.

The `established` line, the number of connections open right now, had a different problem. It was about 100 on the same node. On a shared scale that went up to hundreds of thousands, it looked like a flat line at zero.

Here's the panel in PMM 3.10.0 during a two-minute burst of short connections on a test node. The burst shows up as a climb, but after it ends, the lines stay up, so the panel can't tell you whether the problem is still happening:

![The Netstat: TCP panel in PMM 3.10.0. The lines show running totals, climb during a connection burst at 10:53, and stay high after it ends.](blog/2026/11/netstat-tcp-before.png)

## What you see now

After you upgrade PMM Server to 3.11.0, the panel shows two kinds of information on two scales:

- **Left scale, events per second:** how often connections are opened, reset, or fail, and how many TCP segments are resent. On the test node where `activeOpens` read about 340,000, these lines now read between 0 and 12 per second.
- **Right scale, Connections:** how many connections are open right now.

Here's the same burst on the updated panel. New connections jump to almost 2,000 per second and drop back to zero when the burst ends. Open connections on the right scale rise from about 70 to almost 400, then fall back:

![The Netstat: TCP panel in PMM 3.11.0. During the same burst, activeOpens and passiveOpens spike to almost 2,000 per second and drop back to zero, and established connections rise and fall on the right scale.](blog/2026/11/netstat-tcp-after.png)

## Use the panel to troubleshoot connection problems

When users report connection errors or slowness:

1. Open **OS > Network Details**, select the node that runs your database, and set the time range to cover the incident.
2. In **Netstat: TCP**, look for lines that jump at the time of the problem. Each line points you in a different direction:

    | Line | What a spike usually means |
    |---|---|
    | `passiveOpens` | Clients opened many new connections at once, for example after an application restart or without connection pooling. |
    | `activeOpens` | The node itself opened many outgoing connections, for example to other databases or services. |
    | `attemptfails` | Connection attempts failed, for example because the target port wasn't listening or a firewall blocked it. |
    | `estabResets` | Open connections were dropped abruptly, for example by a crashed process, a timeout, or a load balancer. |
    | `retransSegs` | The node had to resend data, which usually means packet loss or a congested network. |

3. Check `established` on the right scale. A sudden drop matches dropped connections. A line that keeps rising without coming back down can mean that connections aren't being closed.
4. Compare the time of the spike with the connection panels on your database dashboard to see whether the database or the network is the cause.

## Why the old panel showed totals

If you build your own dashboards, this part is for you.

Five of the six lines on the panel come from TCP counters that the node exporter reads from `/proc/net/snmp`. A counter only goes up, and it resets to zero when the host restarts. The sixth, `established`, is a gauge: a snapshot that goes up and down.

Before the fix, each counter used this query:

```promql
max_over_time(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[$interval])
  or
max_over_time(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[5m])
```

`max_over_time()` returns the highest value in each time step. For a counter, the highest value is always the latest one, so the query returned the total since boot.

The counters now use this query:

```promql
rate(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[$interval])
  or
irate(node_netstat_Tcp_ActiveOpens{node_name=~"$node_name"}[5m])
```

- `rate()` returns the average increase per second in each time step, and handles counter resets after a reboot.
- `irate()` is the fallback when the time step is too short for `rate()` to return a value. The **TCP Segments** and **Netstat: UDP** panels on the same dashboard use the same pattern.

`established` keeps its `max_over_time()` query, which suits a gauge because it keeps short peaks inside each time step. It's now on its own right axis, labeled **Connections**.

This mistake is easy to make with any dashboard. By convention, Prometheus counter names end in `_total`, but these come straight from the kernel, and the node exporter reports them as `untyped`. Nothing in the metric tells you it's a counter. To check your own panels:

- **Look at the shape.** A line that only climbs, with dips only at restarts, is almost always a raw counter.
- **Look at the size.** If a panel that should show activity shows six or seven digits on a quiet host, check the query.
- **Match the function to the type.** For counters, use `rate()`, `irate()`, or `increase()`. For gauges, use the raw value, `max_over_time()`, or `avg_over_time()`.

## How the fix reached PMM

Bastian first sent this fix in January 2025, to the old `percona/grafana-dashboards` repository, where it wasn't merged. When the PMM dashboards moved into the main `percona/pmm` repository, he sent it again as [percona/pmm#5913](https://github.com/percona/pmm/pull/5913) and filed [PMM-15559](https://perconadev.atlassian.net/browse/PMM-15559): use rates for the TCP counters, and give open connections their own axis.

Mattia Simonato from the PMM team reproduced the problem on a test node and confirmed the numbers. On top of Bastian's commit, he switched the counters from `irate()` to `rate()` to match the other panels on the dashboard, kept the original query for `established`, and added a release note. The PR merged on 11 November 2026.

Thank you, Bastian, and thanks for sticking with it.

## Get the fix

The fix is in [PMM 3.11.0](https://docs.percona.com/percona-monitoring-and-management/3/release-notes/3.11.0.html), released on 26 November 2026. Upgrade PMM Server, and the [**Netstat: TCP**](https://docs.percona.com/percona-monitoring-and-management/3/reference/dashboards/dashboard-network-details.html) panel shows rates for all your nodes. You don't need to change anything on PMM Client.

## Found a panel that looks wrong?

If a PMM panel shows numbers that don't make sense, you can:

- File a ticket in the [PMM Jira project](https://perconadev.atlassian.net/jira/software/c/projects/PMM/issues) with the dashboard and panel name, and a screenshot. That alone is a useful contribution.
- Fix it yourself, as Bastian did. Most PMM dashboards are JSON files in the [`dashboards/` directory of percona/pmm](https://github.com/percona/pmm/tree/main/dashboards). Send a PR with the Jira key in the title, and the team will help with the rest.
- Ask on the [Percona Community Forum](https://forums.percona.com/) if you're not sure whether it's a bug.

Which PMM panel have you stopped trusting? Tell us, or better, open a ticket.
