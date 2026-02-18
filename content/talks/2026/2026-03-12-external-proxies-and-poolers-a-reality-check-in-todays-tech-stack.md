---
id: "2c0674d0-91f3-80a5-bb9d-c5c1b3054981"
title: "External Proxies and Poolers - A reality check in todays tech stack"
layout: single
speakers:
  - jobin_augustine
talk_url: "https://pgconf.in/conferences/pgconfin2026/program/proposals/1076"
presentation_date: "2026-03-12"
presentation_date_end: "2026-03-13"
presentation_time: ""
talk_year: "2026"
event: "PGConf India 2026"
event_status: "Accepted"
event_date_start: "2026-03-11"
event_date_end: "2026-03-13"
event_url: "https://pgconf.in/conferences/pgconfin2026"
event_location: "Bengaluru, India"
talk_tags: ['PostgreSQL', 'Dev', 'performance']
slides: ""
video: ""
---
## Abstract

For decades, the standard PostgreSQL playbook has included an external connection pooler like PgBouncer or PgPool-II and proxies like HAProxy for service discovery, which we won’t see generally with other database installations like Oracle or SQLServer. This architectural pattern, mainly born from the high cost of process forking in older operating systems, is often treated as gospel. But what if this long-held wisdom is now outdated? It's time to do a reality check to see whether those old observations, remarks and premises are still relevant or not, considering the underlying technology stack had drastically changed over decades 
This talk discusses 
• Is process creation in modern Linux still the performance monster it once was?
• Changes in kernel schedulers and memory management that have dramatically altered this landscape.
• What is the bottleneck in the todays infrastructure for connection establishment and maintenance. (Benchmark results)
• Modern client libraries, drivers / connectors - (Java, Rust and Python examples)
• Assess the maturity and performance of modern, application-native connection poolers (e.g., HikariCP for Java, and equivalents in Rust, Python, etc.) and how they compare to the traditional external approach.
• Service discovery - Modern options and how it works.
• The Security Blind Spot: We will uncover the often-overlooked security risks and operational complexities of "man-in-the-middle" proxies, from TLS termination to query observability challenges.
• Fault-tolerance, Resilience - The modern approaches.
We will re-evaluate long-held assumptions through a data-driven lens, combining 20+ years of experience with modern benchmarks and contemporary case studies. Objective is to enlighten and bridge the gap between DBAs and AppDev, Which could result in huge savings, stable, performant systems and less carbon footprint.
This session is designed for Database Administrators, DevOps Engineers, Site Reliability Engineers (SREs), and Application Developers who are building or maintaining scalable systems with PostgreSQL. A basic understanding of database and application architecture is beneficial.