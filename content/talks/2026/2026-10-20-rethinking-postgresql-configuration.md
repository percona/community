---
id: SPEAK-1501
jira: SPEAK-1501
title: Rethinking PostgreSQL Configuration
layout: single
speakers:
- zsolt_parragi
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
- talks/2026/2026-10-20-rethinking-postgresql-configuration.png
---
PostgreSQL relies on multiple configuration files. Among them, pg_hba, pg_ident, and pg_hosts use tabular formats with slightly different semantics.

The format of these files is unique to PostgreSQL and has been part of the project since its early days. Back then, tabular configuration formats were more common, but they are relatively rare nowadays.

The format has accumulated many features over the years, and the resulting complexity is especially visible in pg_hba.conf: support for includes, a complex options section at the end of each line, and yet another include syntax within those options. As PostgreSQL authentication methods and deployment environments continue to evolve, these limitations are becoming increasingly apparent. At this point, the format is difficult to read for both humans and machines, and it is becoming increasingly difficult to extend as authentication options continue to grow.

This talk presents an ongoing effort rather than a finished feature. We'd like to modernize these configuration files using a modern structured configuration format, making them more readable and easier to work with across a wide range of use cases.

We'll showcase our ideas, present our current proposal for an alternative format, and discuss some of the practical considerations around introducing it.

Most importantly, we'd like practical feedback from DBAs, PostgreSQL users, and contributors: what would you like to see, what's missing, and what's unnecessary? Feedback is welcome even before the talk, whether by email or on pgsql-hackers. If you send it early enough, we may even be able to incorporate it into the presentation!