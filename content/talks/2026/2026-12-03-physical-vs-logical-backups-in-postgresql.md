---
id: SPEAK-3392
jira: SPEAK-3392
title: Physical vs Logical Backups in PostgreSQL
layout: single
speakers:
- sonia_valeja
talk_url: https://buildevcon.com/events/powering-modern-apps
presentation_date: '2026-12-03'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2026'
event: 'Powering Modern Apps: Databases, Observability & Beyond'
event_jira: SPEAK-3389
event_status: Accepted
event_date_start: '2026-12-03'
event_date_end: '2026-12-03'
event_url: https://buildevcon.com/events/powering-modern-apps
event_location: Online
talk_tags: []
slides: ''
video: ''
images:
- talks/2026/2026-12-03-physical-vs-logical-backups-in-postgresql.png
---
Choosing between physical and logical backups in PostgreSQL involves more than selecting a backup tool. Each approach offers different recovery capabilities, operational benefits, and limitations. Understanding these differences helps teams choose a strategy that fits their database and business requirements.

This session provides a conceptual comparison of physical and logical backups, explaining what each method captures and how it affects restoration. We will discuss logical backups, its tools, highlight their flexibility for selective restores, migrations, and development or test environments. We will then examine physical backups, its tools, cover cluster recovery, WAL requirements, and support for point-in-time recovery.

The presentation compares both approaches across restore performance, database size, version compatibility, recovery scope, and disaster recovery needs. It also challenges common assumptions about backup portability, restore speed, and recovery guarantees.

Attendees will leave with a clearer understanding of when to use each approach, how they complement one another, and why recovery requirements should guide backup decisions.