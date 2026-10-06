---
id: SPEAK-1392
jira: SPEAK-1392
title: When Logical Replication Goes Wrong
layout: single
speakers:
- robert_bernier
talk_url: https://postgresql.us/events/pgconfus2025/sessions/session/2041-when-logical-replication-goes-wrong/
presentation_date: '2025-09-29'
presentation_date_end: ''
presentation_time: 2:30 pm
room: Forum B
talk_year: '2025'
event: PGConf NYC 2025
event_jira: SPEAK-1383
event_status: Done
event_date_start: '2025-09-29'
event_date_end: '2025-10-01'
event_url: https://2025.pgconf.nyc/
event_location: New York
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2025/2025-09-29-when-logical-replication-goes-wrong.png
---
Logical Replication has reached a milestone in PostgreSQL, it's more than just for upgrades. Whereas beforehand best practice was to implement High Availability architectures using a PRIMARY->STANDBY replication cluster, one can now implement active-active replication. But with this approach comes along new issues that can stall and even break your replication between multiple read-write hosts.

This session covers numerous kinds of replication stalls and their mitigation. And by following a step by step approach, conflict resolution can be achieved as you identify and resolve potential bottlenecks.