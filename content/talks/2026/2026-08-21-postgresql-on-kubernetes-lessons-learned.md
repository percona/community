---
id: SPEAK-1453
jira: SPEAK-1453
title: 'PostgreSQL on Kubernetes: Lessons learned'
layout: single
speakers:
- jobin_augustine
talk_url: https://confbase.io/2026-hyd-pgdays/2026/schedule/1342
presentation_date: '2026-08-21'
presentation_date_end: ''
presentation_time: '10:00'
talk_year: '2026'
event: PGDay Hyderabad 2026
event_jira: SPEAK-1452
event_status: Done
event_date_start: '2026-05-20'
event_date_end: '2026-08-21'
event_url: https://2026.pghyd.in/
event_location: Hyderabad
talk_tags: []
slides: ''
video: ''
images:
- talks/2026/2026-08-21-postgresql-on-kubernetes-lessons-learned.png
---
This talk is a deep dive into the most frequent failures, performance bottlenecks, and architectural misunderstandings encountered when running PostgreSQL in a container-orchestrated world. Objective of the talk is to correct the expectation and more truthful picture, because carrying the wrong set of expectation can lead to outcomes ranging from Dissatisfaction to a complete investment failure.
This talk covers

The practical and real-world friction between the ""Cattle"" philosophy of Kubernetes and the ""Pet"" reality of relational databases. How it plays in many of the environments.

How Segregation of duties creates blind spots. Incidents caused by communication gaps.

Backbox of abstraction and how it affects the database.

Misunderstanding of DBAs duties. - Automation and its side effects how it affects database hosting.

Then the discussion switches to more technical side

Linux and PostgreSQL. A set of misunderstandings.

Dive in to Linux memory management and Pod in K8s

Containerization and resource management.

Causes of some of the major outages and how to deal with it.