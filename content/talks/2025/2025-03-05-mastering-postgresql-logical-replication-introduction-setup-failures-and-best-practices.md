---
id: SPEAK-1337
jira: SPEAK-1337
title: 'Mastering PostgreSQL Logical Replication: Introduction, Setup, Failures, and
  Best Practices'
layout: single
speakers:
- bhargav_kamineni
- sagar_jadhav
talk_url: https://pgconf.in/conferences/pgconfin2025
presentation_date: '2025-03-05'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2025'
event: PGConf India 2025
event_jira: SPEAK-1336
event_status: Done
event_date_start: '2025-03-05'
event_date_end: '2025-03-07'
event_url: https://pgconf.in/conferences/pgconfin2025
event_location: Bangalore
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2025/2025-03-05-mastering-postgresql-logical-replication-introduction-setup-failures-and-best-practices.png
---
Logical replication in PostgreSQL is how you copy a subset of changes to another cluster: reporting, upgrades, or moving data between versions, without copying the whole instance the way physical replication does.

This talk covers setup (publication and subscription), typical failure modes (lag, slots, schema changes, conflicts), how to read the logs and debug, and what to tune so it stays reliable.
