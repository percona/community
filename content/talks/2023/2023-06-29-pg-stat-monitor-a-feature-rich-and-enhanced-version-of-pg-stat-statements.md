---
id: "3eb06b96-e8ac-4358-912e-439ae3415832"
title: "pg_stat_monitor: A feature-rich and enhanced version of pg_stat_statements"
layout: single
speakers:
  - kai_wagner
talk_url: "https://www.pgday.ch/2023/#schedule"
presentation_date: "2023-06-29"
presentation_date_end: ""
presentation_time: ""
talk_year: "2023"
event: "Swiss PGDay 2023"
event_status: "Done"
event_date_start: ""
event_date_end: ""
event_url: ""
event_location: ""
talk_tags: ['PostgreSQL']
slides: "https://www.pgday.ch/common/slides/2023_pg_stat_monitor.pdf"
video: ""
---
## Abstract

The pg_stat_monitor is the statistics collection tool based on PostgreSQL's contrib module pg_stat_statements. PostgreSQL's pg_stat_statements provides only detailed statistics from the last time it was reset, which is often not enough. This makes it harder to observe query performance patterns during specific times. Those patterns are what's needed when debugging degraded query and server performance. pg_stat_monitor collects and aggregates data on time window basis. Additionally, it differentiates between queries originating from different applications, clients and users. And I haven't even mentioned the queries execution timing histogram. These features make it especially useful in analyze query behavior generally and during specific time of a day. With plenty of configuration options, turning off actual query parameters, pg_stat_monitor covers observability from all different aspects without compromising on security. pg_stat_monitor is added to Percona Monitoring and Management to collect query metrics. It gives users the ability to see examples instead of fingerprints. Pg_stat_monitor provides more accurate data because of the bucket-based logic. The talk will cover the usage of pg_stat_monitor, its features, and how it can help to enhance your database inspection and monitoring.