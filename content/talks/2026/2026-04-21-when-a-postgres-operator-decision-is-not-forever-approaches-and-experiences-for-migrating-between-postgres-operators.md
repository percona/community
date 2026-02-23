---
id: "2cc674d0-91f3-8016-ac50-cfe7f0b74306"
title: "When a Postgres Operator decision is not forever: approaches and experiences for migrating between Postgres Operators"
layout: single
speakers:
  - takis_panagiotis_stathopoulos
talk_url: "https://www.postgresql.eu/events/pgconfde2026/sessions/session/7562-when-a-postgres-operator-decision-is-not-forever-approaches-and-experiences-for-migrating-between-postgres-operators/"
presentation_date: "2026-04-21"
presentation_date_end: "2026-04-22"
presentation_time: ""
talk_year: "2026"
event: "PGConf Germany 2026"
event_status: "Accepted"
event_date_start: "2026-04-21"
event_date_end: "2026-04-22"
event_url: "https://2026.pgconf.de/"
event_location: "Essen, German"
talk_tags: ['PostgreSQL', 'Kubernetes']
slides: ""
video: ""
---
## Abstract

The Postgres ecosystem on Kubernetes is thriving and this is particularly evident in the Postgres K8s Operators space. 

As the Postgres Operator ecosystem matures, real world experience has shown that, technical, licensing or operational constraints can make it necessary to migrate between PostgreSQL Kubernetes Operators over the lifecycle of a database platform.
In this talk we are going to:

* Provide an overview of the Postgres Operator landscape, reviewing widely adopted options such as  CloudNativePG, Percona PostgreSQL Operator, Crunchy Data PGO, Zalando Operator , and Bitnami Helm charts. We will compare their key architectural, technological, and licensing choices to help attendees make more informed operator selection decisions.

* Examine the reasons why, even after a decision, you might be faced with an operator migration eventually, and the licensing, architectural and operational aspects, risks and opportunities, that you should take into account. 

* Discuss the different implementation approaches for migrating between Operators, such as replication, backup and volume-based patterns. 

* Finally, deep dive on a particular Operator migration case study between two popular Postgres K8s operators.  

By the end of this session, attendees will have a clearer understanding of the PostgreSQL Operator ecosystem, the risks and opportunities associated with an Operator technology switch, and finally concrete, actionable strategies for planning and executing Postgres Kubernetes Operator technology migrations.