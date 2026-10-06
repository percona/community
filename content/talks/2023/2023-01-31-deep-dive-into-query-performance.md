---
id: SPEAK-2573
jira: SPEAK-2573
title: Deep Dive Into Query Performance
layout: single
speakers:
- peter_zaitsev
talk_url: https://p2d2.cz/rocnik-2023
presentation_date: '2023-01-31'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2023'
event: P2D2 2023
event_jira: ''
event_status: Done
event_date_start: '2023-01-31'
event_date_end: ''
event_url: https://p2d2.cz/rocnik-2023
event_location: ''
talk_tags: []
slides: ''
video: ''
images:
- talks/2023/2023-01-31-deep-dive-into-query-performance.png
---
If you look at data store as just another service, the things Application cares about is successfully establishing connection and getting results to the queries promptly and with correct results. In this presentation, we will explore this seemingly simple aspect of working with database in details. We will talk about why you want to go beyond the averages, and how to group queries together in the meaningful way so you’re not overwhelmed with amount of details but find the right queries to focus on. We will answer the question on when you should focus on tuning specific queries or when it is better to focus on tuning the database (or just getting a bigger box). We will also look at other ways to minimize user facing response time, such as parallel queries, asynchronous queries, queuing complex work, as well as often misunderstood response time killers such as overloaded network, stolen CPU, and even limits imposed by this pesky speed of light.
