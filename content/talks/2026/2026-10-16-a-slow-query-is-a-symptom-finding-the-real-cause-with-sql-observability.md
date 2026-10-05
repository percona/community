---
id: SPEAK-2890
jira: SPEAK-2890
title: 'A Slow Query Is a Symptom: Finding the Real Cause with SQL Observability'
layout: single
speakers:
- sonia_valeja
talk_url: https://osoday.com/
presentation_date: '2026-10-16'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2026'
event: Open Source Observability Day (VIRTUAL) 2026
event_jira: SPEAK-1471
event_status: Accepted
event_date_start: '2026-10-15'
event_date_end: '2026-10-16'
event_url: https://osoday.com
event_location: ''
talk_tags:
- Open-Source
slides: ''
video: ''
images:
- talks/2026/2026-10-16-a-slow-query-is-a-symptom-finding-the-real-cause-with-sql-observability.png
---
A slow query does not always mean that the SQL statement is poorly written. Database teams frequently treat a slow query as an isolated SQL problem: capture the statement, inspect its execution plan and add an index. In production environments, however, the query text may be only one part of the story.

A query can run slowly because it is blocked by another transaction, processing more data than usual, using an unexpected execution plan, spilling to temporary storage, competing for limited resources or waiting on slow infrastructure. A normally fast query can also become the largest performance problem when its execution frequency suddenly increases.

This session presents an observability-driven approach to investigating slow and long-running SQL queries. Using PostgreSQL examples, it demonstrates how query statistics, execution plans, wait events, locks, logs and operating-system metrics can be correlated to distinguish symptoms from root causes.

Attendees will learn how to determine whether the problem is the SQL statement, the execution plan, workload concurrency or infrastructure.