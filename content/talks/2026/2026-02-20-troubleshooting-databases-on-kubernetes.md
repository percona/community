---
id: 306674d0-91f3-80e4-9b04-c860130be58b
title: Troubleshooting databases on Kubernetes
layout: single
speakers:
- ege_gunes
talk_url: https://buildevcon.com/cloud-native-databases/
presentation_date: '2026-02-20'
presentation_date_end: ''
presentation_time: ''
talk_year: '2026'
event: Cloud Native Databases
event_status: Accepted
event_date_start: '2026-02-20'
event_date_end: '2026-02-21'
event_url: https://buildevcon.com/cloud-native-databases/
event_location: 'Virtual '
talk_tags:
- Kubernetes
- Cloud Native
- database
- Open Source
slides: ''
video: ''
images:
- talks/2026/2026-02-20-troubleshooting-databases-on-kubernetes.png
---
## Abstract

Running stateful workloads on Kubernetes introduces a new layer of complexity when things go wrong. When a database node hangs or replication breaks, standard troubleshooting often falls short. In this session, we will dissect real-world failure scenarios--from storage I/O bottlenecks to networking partitions in distributed clusters.We will demonstrate a tiered troubleshooting approach using  Ephemeral Containers  for safe debugging,  kubectl plugins  for stateful insights, and (where necessary)  privileged access  for deep-kernel tracing. Attendees will leave with a checklist for building "troubleshoot-ready" operators and a toolkit for resolving database downtime faster.