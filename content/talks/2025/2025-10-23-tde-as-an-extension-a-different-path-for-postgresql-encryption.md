---
id: 281674d0-91f3-8018-81b4-f3ff25a44861
title: 'TDE as an Extension: A Different Path for PostgreSQL Encryption'
layout: single
speakers:
- zsolt_parragi
talk_url: ''
presentation_date: '2025-10-23'
presentation_date_end: ''
presentation_time: 11:25–12:15
talk_year: '2025'
event: PGConf EU 2025 Riga
event_status: Done
event_date_start: '2025-10-21'
event_date_end: '2025-10-24'
event_url: https://2025.pgconf.eu
event_location: Riga, Latvia
talk_tags:
- PostgreSQL
- Security
- Open Source
- Slides
slides: https://www.postgresql.eu/events/pgconfeu2025/sessions/session/7191/slides/807/PGConf%20EU%202025%20Riga%20TDE%20slides.pdf
video: ''
images:
- talks/2025/2025-10-23-tde-as-an-extension-a-different-path-for-postgresql-encryption.png
---
## Abstract

Transparent Data Encryption (TDE) has been a long-standing challenge in the PostgreSQL community. While proprietary solutions exist and major patch sets have been proposed, the topic continues to spark debate on the hackers mailing list, with no clear path forward.
Our team decided to take a different approach: instead of building TDE directly into PostgreSQL, we explored how far we could go by implementing it as an extension, pushing core changes only where extensibility improvements were needed.
This has been, and still is, a demanding project. Along the way, we have built multiple prototypes, hit dead ends, and uncovered design trade-offs that were not obvious at the start.
In this talk, we will share the technical lessons from our journey: what failed, what succeeded, how our extension-based approach actually works, and which challenges remain unsolved.