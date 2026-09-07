---
id: SPEAK-1546
jira: SPEAK-1546
title: Zero-Downtime Migration with Percona ClusterSync for MongoDB
layout: single
speakers:
- inel_pandzic
talk_url: https://buildevcon.com/Home
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
- Databases
- MongoDB
- pcsm
- Cloud-Native
slides: ''
video: ''
images:
- talks/2026/2026-08-28-zero-downtime-migration-with-percona-clustersync-for-mongodb.png
---
Organizations running MongoDB on Atlas or Enterprise editions face a growing tension: rising costs, licensing changes, and vendor lock-in make it increasingly difficult to maintain control over their data infrastructure. Yet migrating between MongoDB clusters has traditionally required application downtime or complex manual orchestration -- leaving many teams stuck on platforms they've outgrown.

Percona ClusterSync for MongoDB (PCSM) is an open-source, cluster-to-cluster replication tool that frees users from vendor lock-in and enables zero-downtime data migration to open-source MongoDB options, including Percona Server for MongoDB and MongoDB Community Edition. It handles initial data cloning, continuous change stream-based replication, namespace filtering, and automatic index management -- all without interrupting production workloads.

PCSM supports both replica set and sharded cluster topologies, and because the source and target can differ in topology and shard count, it also enables infrastructure right-sizing -- for example, downscaling from a sharded cluster to a simpler replica set when your data no longer requires sharding, reducing both operational complexity and cost.

In this talk, we cover:

The business case for escaping MongoDB vendor lock-in and moving to open-source alternatives

How PCSM works: the two-phase replication model (clone + catch-up, then continuous real-time replication via change streams), its state machine, and the HTTP API for operational control

Deployment architecture options and how placement affects migration performance

Supported migration paths: Atlas, Enterprise, and Community as sources; Percona Server for MongoDB and Community Edition as targets; topology changes including sharded-to-replica-set downscaling

A live end-to-end demonstration: starting replication, monitoring progress, finalizing, and cutting over to the new cluster

Attendees will leave with a clear understanding of how to plan and execute a zero-downtime MongoDB migration, how to use PCSM for hybrid cloud synchronization, and how to right-size their infrastructure -- all using open-source tooling.