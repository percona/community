---
id: SPEAK-2188
jira: SPEAK-2188
title: Swap or Stop? How a Little Swap Can Keep PostgreSQL Running
layout: single
speakers:
- chetan_shivashankar
talk_url: https://2026.pgconf.eu
presentation_date: '2026-10-20'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: PGConf Europe 2026
event_jira: SPEAK-1476
event_status: Accepted
event_date_start: '2026-10-20'
event_date_end: '2026-10-23'
event_url: https://2026.pgconf.eu
event_location: Valencia
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2026/2026-10-20-swap-or-stop-how-a-little-swap-can-keep-postgresql-running.png
---
For years, the advice for Kubernetes was straightforward: disable swap. But with swap support becoming generally available in Kubernetes 1.34, it's worth asking whether that guidance still makes sense for PostgreSQL workloads.

In this talk, we'll follow the journey of swap from the Linux kernel all the way to the dashboards . We'll look at how swap space is configured, how memory and swap are accounted with cgroups, and how Kubernetes exposes those metrics through tools such as cAdvisor and Prometheus.

More importantly, we'll explore what actually happens when PostgreSQL encounters sudden memory pressure. Does the kernel immediately kill the pod? Can swap absorb short-lived memory spikes and give PostgreSQL enough breathing room to stay available? We'll examine real-world scenarios where swap can prevent OOM kills and keep critical database services online. Unfortunately, there are no magic wands in life, and swap is no exception. We'll discuss the trade-offs of using swap space so that you can evaluate if swap is suitable for your workloads.