---
id: "2ee674d0-91f3-8031-a92f-c120a58cbaee"
title: "PostgreSQL and MySQL, Two Databases, Three Perspectives"
layout: single
speakers:
  - pep_pla
talk_url: "https://fosdem.org/2026/schedule/event/JWX9UM-postgres-mysql-two-databases-three-perspectives/"
presentation_date: "2026-01-31"
presentation_date_end: ""
presentation_time: "10:30"
talk_year: "2026"
event: "FOSDEM 2026"
event_status: "Accepted"
event_date_start: "2026-01-30"
event_date_end: "2026-02-02"
event_url: "https://pretalx.fosdem.org/fosdem-2026/cfp"
event_location: "Brussels, Belgium"
talk_tags: ['MySQL', 'PostgreSQL']
slides: ""
video: ""
---

## Abstract

In this session, four seasoned database administrators with sound knowledge of both PostgreSQL and MySQL present an unbiased comparison of the two technologies. Attendees will learn about the architectural and DX differences between the world's two most popular databases.

Pep Pla, with his peculiar sense of humour, will open the session with a deep dive into the MVCC architectures between the two. The audience will learn why we need MVCC. Postgres and MySQL take very different approaches to implementation: Postgres relies on row versioning and vacuuming dead tuples, while MySQL does in-place changes and tracks versions with the undo log.

A broad-strokes overview from Ben Dicken, who has worked closely with both, will emphasize where ecosystem cross-pollination would help. This includes differences in table storage, bloat management, replication, and process-per-connection vs thread-per-connection architecture.

Postgres and MySQL take fundamentally different approaches to logical replication. Rohit Nayak and Shlomi Noach will examine how these designs affect WAL/binlog retention, backpressure, and CDC workloads, explore their failover implications, and highlight key feature-parity gaps between the two systems.