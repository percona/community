---
aliases:
- /talks/2023/2023-07-05-deep-dive-into-query-performance
event: Percona University Morocco 2023
event_date_end: ''
event_date_start: '2023-06-27'
event_jira: ''
event_location: Casablanca
event_status: Accepted
event_url: https://www.eventbrite.com/e/percona-university-morocco-2023-tickets-643139326037
id: SPEAK-2477
jira: SPEAK-2477
layout: single
presentation_date: '2023-06-27'
presentation_date_end: ''
presentation_time: ''
room: ''
slides: ''
speakers:
- peter_zaitsev
talk_tags: []
talk_url: https://www.eventbrite.com/e/percona-university-morocco-2023-tickets-643139326037
talk_year: '2023'
title: Deep Dive Into Query Performance
video: ''
images:
- talks/2023/2023-06-27-deep-dive-into-query-performance.png
---


If you look at data store as just another service, the things Application cares about is successfully establishing connection and getting results to the queries promptly and with correct results.

In this presentation, we will explore this seemingly simple aspect of working with PostgreSQL in details. We will talk about why you want to go beyond the averages, and how to group queries together in the meaningful way so you’re not overwhelmed with amount of details but find the right queries to focus on.

We will answer the question on when you should focus on tuning specific queries or when it is better to focus on tuning the database (or just getting a bigger box).

We will also look at other ways to minimize user facing response time, such as parallel queries, asynchronous queries, queueing complex work, as well as often misunderstood response time killers such as overloaded network, stolen CPU, and even limits imposed by this pesky speed of light.