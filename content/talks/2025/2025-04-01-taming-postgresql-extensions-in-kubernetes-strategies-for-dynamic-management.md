---
id: "183674d0-91f3-80f8-9925-f59857164c66"
title: "Taming PostgreSQL Extensions in Kubernetes: Strategies for Dynamic Management"
layout: single
speakers:
  - peter_szczepaniak
talk_url: "https://colocatedeventseu2025.sched.com/event/1u5hJ/taming-postgresql-extensions-in-kubernetes-strategies-for-dynamic-management-peter-szczepaniak-percona"
presentation_date: "2025-04-01"
presentation_date_end: ""
presentation_time: "11:45"
talk_year: "2025"
event: "Kubecon + CloudNativeCon Europe 2025"
event_status: "Done"
event_date_start: "2025-04-01"
event_date_end: "2025-04-04"
event_url: "https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/"
event_location: "London, UK"
talk_tags: ['PostgreSQL', 'Operators', 'Kubernetes', 'Cloud Native', 'Open Source', 'Video']
slides: ""
video: "https://www.youtube.com/watch?v=_arr3sEckSw"
youtube_id: "_arr3sEckSw"
---
## Abstract

Running PostgreSQL in Kubernetes is becoming increasingly popular, but managing database extensions in this environment presents a challenge. Containers are designed to be immutable, making it difficult to add extensions after the database is up and running. Rebuilding containers every time you need a new extension defeats the purpose of using pre-built images with security and best practices baked in. This talk explores different approaches to managing PostgreSQL extensions in Kubernetes, including their pros and cons, and discusses potential future standards for streamlined extension management.