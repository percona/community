---
id: SPEAK-2187
jira: SPEAK-2187
title: What Happens When MongoDB Runs Out of Disk on Kubernetes?
layout: single
speakers:
- eleonora_zinchenko
talk_url: https://buildevcon.com/events/document-databases
presentation_date: '2026-08-28'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: 'Build DevCon: Document Databases'
event_jira: SPEAK-1544
event_status: Accepted
event_date_start: '2026-08-28'
event_date_end: '2026-08-28'
event_url: https://buildevcon.com/events/document-databases
event_location: ''
talk_tags:
- CloudNative
- MongoDB
- Cloud-Native
slides: ''
video: ''
images:
- talks/2026/2026-08-28-what-happens-when-mongodb-runs-out-of-disk-on-kubernetes.png
---
In this talk, we’ll explore how MongoDB behaves as disk usage approaches its limits and how Kubernetes storage expansion can help. Using Percona Operator for MongoDB, we’ll look at automatic PVC resizing based on disk utilization, how it interacts with Kubernetes and the underlying storage provider, and what happens when expansion isn’t possible.

Through practical examples, we’ll cover the configuration, limitations, and failure scenarios.