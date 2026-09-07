---
id: SPEAK-1244
jira: SPEAK-1244
title: MySQL Performance - And what my query has to do with it?
layout: single
speakers:
- roberto_garcia_de_bem
talk_url: https://mysqlbrconf.com.br/
presentation_date: '2026-09-26'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: MySQL Brazil Conference 2026
event_jira: SPEAK-1220
event_status: Done
event_date_start: '2026-09-26'
event_date_end: ''
event_url: https://mysqlbrconf.com.br/
event_location: Brazil - São Paulo
talk_tags:
- Community
- MySQL
slides: ''
video: ''
images:
- talks/2026/2026-09-26-mysql-performance-and-what-my-query-has-to-do-with-it.png
---
Optimizing MySQL performance can seem complex and time-consuming. Where do you start? Tweaking variables? Upgrading hardware? When dealing with poorly written queries, these kinds of changes merely mask the problem temporarily rather than solving it.

The goal of this talk is to clarify the process of creating, analyzing, and optimizing your queries. We will explore how the MySQL optimizer reads your code, why simply creating an index won't always save a query, and the actual logic behind slow query performance.

This presentation is entirely inspired by concepts from Daniel Nichter's book  Efficient MySQL Performance  (such as "Thinking like MySQL" and "It was a good index until...").