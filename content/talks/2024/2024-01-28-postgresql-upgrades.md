---
id: SPEAK-2427
jira: SPEAK-2427
title: PostgreSQL Upgrades
layout: single
speakers:
- bhargav_kamineni
- sagar_jadhav
talk_url: https://www.pgconf.in/conferences/pgconfin2024/program/proposals/681
presentation_date: '2024-01-28'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2024'
event: PGConf India 2024
event_jira: ''
event_status: Done
event_date_start: '2024-01-28'
event_date_end: ''
event_url: https://www.pgconf.in/conferences/pgconfin2024/program/proposals/681
event_location: ''
talk_tags: []
slides: ''
video: ''
images:
- talks/2024/2024-01-28-postgresql-upgrades.png
---
Postgres Minor version and Major version upgrade strategies

Why need to upgrade?

Upgrade types - Minor and major version upgrades

About Minor version upgrade

About Major version upgrade

Different ways of major version upgrades

Postgres upgrade using pg_dumpall

Postgres upgrade using pg_dump

Postgres upgrade using pg_upgrade

upgrade on RDS

Postgres upgrade using logical replication

Upgrade using PITR with LSN, pg_upgrade and logical replication to minimize downtime - https://www.percona.com/blog/the-magic-of-pitr-pg_upgrade-and-logical-replication-when-used-together-for-postgresql-version-upgrades/

On RDS- Quickly setup logical replication for upgrade using snapshot upgrade to avoid data copy - https://www.percona.com/blog/postgresql-logical-replication-using-an-rds-snapshot/

Performing a Major PostgreSQL Version Upgrade in a Cluster Managed by Patroni (if time permits )

Date: 2024 February 28 - 14:00Duration: 3 h 30 minRoom: ArabicaConference: PGConf India, 2024