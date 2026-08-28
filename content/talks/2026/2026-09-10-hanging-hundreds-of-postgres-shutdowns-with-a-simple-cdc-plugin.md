---
id: SPEAK-1381
jira: SPEAK-1381
title: Hanging hundreds of Postgres shutdowns with a simple CDC plugin
layout: single
speakers:
- yoann_la_cancellera
talk_url: ''
presentation_date: '2026-09-10'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: PGDay Lowlands
event_jira: SPEAK-1376
event_status: Accepted
event_date_start: '2025-09-12'
event_date_end: ''
event_url: ''
event_location: Rotterdam
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2026/2026-09-10-hanging-hundreds-of-postgres-shutdowns-with-a-simple-cdc-plugin.png
---
Whenever any simple switchover needed to be done, it took hours. The customer was killing the primary postmaster out of desperation because it was simply too long. It was reproducing perfectly every time, in every single production and most non-production environments. Was postgres hanging? Was it slow to finish something? Could some application hang a primary shutdown like this?

We will discuss debugging on Kubernetes, following the thread and debugging logical replication protocols, along with some simple pg_walreceiver patches