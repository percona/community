---
event: P99 CONF
event_date_end: ''
event_date_start: '2022-10-19'
event_jira: ''
event_location: ''
event_status: Done
event_url: https://www.p99conf.io/
id: SPEAK-2577
jira: SPEAK-2577
layout: single
presentation_date: '2022-10-19'
presentation_date_end: ''
presentation_time: ''
room: ''
slides: ''
speakers:
- peter_zaitsev
talk_tags:
- Video
talk_url: https://www.p99conf.io/
talk_year: '2022'
title: Deep Dive Into Query Performance
video: https://www.youtube.com/watch?v=rIfWASEoXC8
youtube_id: rIfWASEoXC8
images:
- talks/2022/2022-10-19-deep-dive-into-query-performance.png
---
If you look at data store as just another service, the things Application cares about is successfully establishing connection and getting results to the queries promptly and with correct results. In this presentation, we will explore this seemingly simple aspect of working with database in details. We will talk about why you want to go beyond the averages, and how to group queries together in the meaningful way so you’re not overwhelmed with amount of details but find the right queries to focus on. We will answer the question on when you should focus on tuning specific queries or when it is better to focus on tuning the database (or just getting a bigger box). We will also look at other ways to minimize user facing response time, such as parallel queries, asynchronous queries, queueing complex work, as well as often misunderstood response time killers such as overloaded network, stolen CPU, and even limits imposed by this pesky speed of light.
