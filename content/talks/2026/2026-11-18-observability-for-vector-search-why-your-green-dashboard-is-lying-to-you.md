---
id: SPEAK-1639
jira: SPEAK-1639
title: 'Observability for Vector Search: Why Your Green Dashboard Is Lying To You'
layout: single
speakers:
- radoslaw_szulgo
- sandra_romanchenko
talk_url: https://osmc.de
presentation_date: '2026-11-18'
presentation_date_end: ''
presentation_time: ''
talk_year: '2026'
event: Open Source Monitoring Conference 2026
event_jira: SPEAK-1638
event_status: Accepted
event_date_start: '2026-11-17'
event_date_end: '2026-11-19'
event_url: https://osmc.de
event_location: Germany
talk_tags:
- MongoDB
- PMM
- Vector-Search
- Open-Source
- Tech
- ai
- cloud
- monitoring
- observability
- open-source
slides: ''
video: ''
images:
- talks/2026/2026-11-18-observability-for-vector-search-why-your-green-dashboard-is-lying-to-you.png
---
Dashboards are green – steady QPS, zero 5xx errors, ultra-low latency – yet users report AI hallucinations. Welcome to the silent nightmare of ANN search: recall degradation without infrastructure failure. How do you detect invisible failures? This session maps the four tiers of vector observability: DB internals, index health, LLM performance, and output quality. We’ll explore a production OSS stack (Percona for MongoDB, PMM, mongot, vLLM) and expose where open source still falls short.