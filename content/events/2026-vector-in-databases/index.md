---
title: Vector in Databases
description: 'Radoslaw Szulgo, Sandra Romanchenko, and Yevhen Patlan spoke on vector search at Vector in Databases on October 23.'
layout: single
# Hand-written copy; keep jira for related-talks. sync: skip blocks events_publish overwrite.
sync: skip
jira: SPEAK-2671
speakers:
- evgeniy_patlan
- radoslaw_szulgo
- sandra_romanchenko
date: '2026-10-23'
event_date_end: '2026-10-23'
EventDate: October 23, 2026
EventLocation: Online
event_url: https://buildevcon.com/events/vector-in-databases
tags:
- Event
- opensource
- speaking
- ai
- databases
- vector-database
events_year:
- '2026'
events_category:
- Speaking
events_tag:
- Online
images:
- events/2026-vector-in-databases/card.png
---

**Vector in Databases** took place on **October 23, 2026**, online. The summit was for engineers building applications on vector search: embeddings, approximate nearest neighbor indexes, hybrid search, and production deployment.

- 📅 **October 23, 2026**
- 📍 **Online**
- 🔗 **Event page:** [buildevcon.com/events/vector-in-databases](https://buildevcon.com/events/vector-in-databases)

## Percona talks

### Vector Search on Your Terms: From Prototype to Production with Percona for MongoDB

**Speakers:** [Radoslaw Szulgo](/contributors/radoslaw_szulgo/) and [Sandra Romanchenko](/contributors/sandra_romanchenko/) · October 23, 14:01–14:30 UTC

Turning on vector search in MongoDB Community Edition is quick if your documents go out to a cloud API for the embeddings. Radoslaw and Sandra walked through what you give up with that, and how Percona Search for MongoDB on Percona Server for MongoDB (PSMDB) calls any OpenAI-compatible endpoint instead, including a model you run yourself. Sandra then added it to a three-node replica set and showed why a bad index returns an empty set, which is why the service sits on a Percona Monitoring and Management (PMM) dashboard.

[Talk page](/talks/2026/2026-10-23-vector-search-on-your-terms-from-prototype-to-production-with-percona-for-mongodb/) · [Recording](https://www.youtube.com/watch?v=Wjymxm6JQEs)

### Benchmarking Vector Indexes

**Speaker:** [Yevhen Patlan](/contributors/evgeniy_patlan/) · October 23, 14:30–15:01 UTC

Queries per second without recall do not tell you if the index returned the right rows. Yevhen showed Vector Bench, a Percona Lab harness that runs each engine from a pinned version on the same CPU cores and the same data, and reports the recall-versus-throughput curve. On one HNSW index, raising ef_search from 10 to 800 dropped throughput from 3,678 to 409 queries per second and lifted recall from 0.959 to 0.999.

[Talk page](/talks/2026/2026-10-23-benchmarking-vector-indexes/) · [Recording](https://www.youtube.com/watch?v=Nd1MBup7t80)
