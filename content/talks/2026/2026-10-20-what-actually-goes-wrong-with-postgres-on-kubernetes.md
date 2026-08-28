---
id: SPEAK-1493
jira: SPEAK-1493
title: What Actually Goes Wrong with Postgres on Kubernetes
layout: single
speakers:
- natalia_marukovich
talk_url: ''
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
- talks/2026/2026-10-20-what-actually-goes-wrong-with-postgres-on-kubernetes.png
---
Postgres on Kubernetes usually works well enough — until the operator itself becomes part of the incident. The harder problems tend to show up in two areas that operator documentation rarely covers: troubleshooting incidents that cross multiple systems, and sizing the operator pod and its reconciliation behaviour.

This session draws on real cases from working on the Percona Operator for PostgreSQL. The specific incidents are tied to design choices we made and bugs we shipped; different operators will hit different problems. What generalises is the shape of the problem.

Key discussion areas:

Why debugging operator-managed Postgres often means debugging three systems at once: Kubernetes, the operator, and Postgres

Correlating operator logs, Postgres logs, controller state, and Kubernetes events into a single debugging workflow

Sizing the operator pod: CPU, memory, and how much work it is allowed to reconcile in parallel

Attendees will leave with practical knowledge for debugging operator-managed Postgres, a starting point for sizing operator, and a set of questions to ask before trusting any Postgres operator in production.

This session is intended for SREs, DBAs, and platform engineers running or evaluating Postgres on Kubernetes.