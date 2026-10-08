---
id: SPEAK-2834
jira: SPEAK-2834
title: Zero-Downtime Migration with Percona ClusterSync for MongoDB
layout: single
speakers:
- adnan_supic
talk_url: https://feit.stu.cn.ua/foss/
presentation_date: '2026-10-02'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2026'
event: FEIT STU - Free/Open Source Software in Education, Science & Business
event_jira: SPEAK-2636
event_status: Accepted
event_date_start: '2026-10-01'
event_date_end: '2026-10-02'
event_url: https://feit.stu.cn.ua/foss/
event_location: ''
talk_tags:
- MongoDB
- Open-Source
- Tech
- software-development
slides: ''
video: ''
images:
- talks/2026/2026-10-02-zero-downtime-migration-with-percona-clustersync-for-mongodb.png
---
Migrating a production MongoDB deployment without disrupting applications is challenging, especially when the source must continue accepting writes throughout the process.

This session explores how Percona ClusterSync for MongoDB (PCSM) enables near-zero-downtime migrations by cloning existing data and continuously replicating changes between MongoDB environments. We’ll walk through the migration pipeline, explain how PCSM works under the hood, and demonstrate a real-world migration from MongoDB Atlas to a Percona Server for MongoDB replica set.

Attendees will learn how to prepare and execute the migration, monitor the key metrics that determine when it is safe to cut over, and minimize the remaining downtime associated with restoring indexes on the target.

We’ll also examine current limitations, operational considerations, and lessons learned from building PCSM, giving DBAs and engineers a practical understanding of how to approach their own MongoDB migrations safely.