---
id: SPEAK-1357
jira: SPEAK-1357
title: Taming PostgreSQL Extensions in Kubernetes: Strategies for Dynamic Management
layout: single
speakers:
- peter_szczepaniak
talk_url: https://colocatedeventseu2025.sched.com/event/1u5hJ/taming-postgresql-extensions-in-kubernetes-strategies-for-dynamic-management-peter-szczepaniak-percona
presentation_date: '2025-04-01'
presentation_date_end: ''
presentation_time: '12:45'
talk_year: '2025'
event: Kubecon + CloudNativeCon Europe 2025
event_jira: SPEAK-1351
event_status: Done
event_date_start: '2025-04-01'
event_date_end: '2025-04-04'
event_url: https://kccnceu2025.sched.com/
event_location: London
talk_tags:
- Kubernetes
- Operators
- PostgreSQL
- Cloud-Native
- Open-Source
- Video
slides: ''
video: https://www.youtube.com/watch?v=_arr3sEckSw
youtube_id: _arr3sEckSw
images:
- talks/2025/2025-04-01-taming-postgresql-extensions-in-kubernetes-strategies-for-dynamic-management.png
---
Running PostgreSQL in Kubernetes is becoming increasingly popular, but managing database extensions in this environment presents a challenge. Containers are designed to be immutable, making it difficult to add extensions after the database is up and running. Rebuilding containers every time you need a new extension defeats the purpose of using pre-built images with security and best practices baked in. This talk explores different approaches to managing PostgreSQL extensions in Kubernetes, including their pros and cons, and discusses potential future standards for streamlined extension management.

Description:

Running PostgreSQL in Kubernetes is becoming increasingly popular, but managing database extensions in this environment presents a challenge. Containers are designed to be immutable, making it difficult to add extensions after the database is up and running. Rebuilding containers every time you need a new extension defeats the purpose of using pre-built images with security and best practices baked in. This talk explores different approaches to managing PostgreSQL extensions in Kubernetes, including their pros and cons, and discusses potential future standards for streamlined extension management.