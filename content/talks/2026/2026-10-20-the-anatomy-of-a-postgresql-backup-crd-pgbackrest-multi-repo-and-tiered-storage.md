---
id: SPEAK-1488
jira: SPEAK-1488
title: 'The Anatomy of a PostgreSQL Backup CRD: pgBackRest, Multi-Repo, and Tiered Storage'
layout: single
speakers:
- george_kechagias
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
- talks/2026/2026-10-20-the-anatomy-of-a-postgresql-backup-crd-pgbackrest-multi-repo-and-tiered-storage.png
---
Backing up a PostgreSQL cluster on Kubernetes looks simple from the outside: apply a CR, get a backup. Underneath, there are several layers working together, and each one shapes what you can recover and how fast.

This talk takes a closer look at those layers. We will see how pgBackRest works under the hood, how Kubernetes operators expose it, and how a multi-repo setup opens up tiered storage strategies that are hard to get any other way. Along the way we will touch on full, differential, and incremental backups, point-in-time recovery via WAL archiving, dedicated Backup and Restore CRs, multi-cloud storage backends, and clone-from-backup flows for spinning up a new cluster from an existing repository.