---
id: SPEAK-2828
jira: SPEAK-2828
title: 'pgBackRest in HA setups: deployment patterns that work'
layout: single
speakers:
- stefan_fercot
talk_url: https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8238-pgbackrest-in-ha-setups-deployment-patterns-that-work/
presentation_date: '2026-10-20'
presentation_date_end: ''
presentation_time: '16:05'
room: ''
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
- talks/2026/2026-10-20-pgbackrest-in-ha-setups-deployment-patterns-that-work.png
---
The events of last April reminded us just how important pgBackRest has become. The strong reaction from users, vendors, and sponsors showed that this backup tool is relied upon in an extraordinary range of environments — from small deployments to some of the most critical PostgreSQL infrastructures in production today.

Yet many organizations use only a fraction of what pgBackRest can offer. Having a solid recovery plan is essential, because in a real outage, just having a backup is not enough.

pgBackRest provides a remarkably flexible foundation that can fit many different setups: using a dedicated backup host, taking backups from standby servers, or sending data straight to the cloud with S3, Azure, or Google Cloud. However, many of these deployment patterns remain largely unknown or underutilized.

In this talk, we'll go beyond the basics and look at several pgBackRest deployment patterns that can be combined for better resilience, performance, and cost efficiency. We'll discuss setups that mix backup hosts and cloud storage, make use of multiple standbys, and keep things running smoothly in High-Availability environments.

Based on real-world experience deploying this "undocumented magical solution" in highly critical systems, this session will show how to unlock pgBackRest's full potential and design resilient backup architectures that meet the requirements of modern HA environments.