---
id: "SPEAK-3317"
jira: "SPEAK-3317"
title: "When a Postgres Operator Decision Is Not Forever: Approaches and Experiences for Migrating Between Postgres Operators"
layout: single
speakers:
  - takis_panagiotis_stathopoulos
talk_url: "https://cloomba.com/e/6-postgresql-meetup-vienna"
presentation_date: "2026-11-11"
presentation_date_end: ""
presentation_time: "19:15"
room: ""
talk_year: "2026"
event: "6th PostgreSQL Meetup Vienna"
event_jira: "SPEAK-3316"
event_status: "Done"
event_date_start: "2026-11-11"
event_date_end: "2026-11-11"
event_url: "https://cloomba.com/e/6-postgresql-meetup-vienna"
event_location: "Vienna"
talk_tags: ['Kubernetes', 'PostgreSQL']
slides: ""
video: ""
images:
  - talks/2026/2026-11-11-when-a-postgres-operator-decision-is-not-forever-approaches-and-experiences-for-migrating-between-postgres-operators.png
---
The Postgres ecosystem on Kubernetes is thriving and this is particularly evident in the Postgres K8s Operators space.

As the Postgres Operator ecosystem matures, real world experience has shown that technical, licensing or operational constraints can make it necessary to migrate between PostgreSQL Kubernetes Operators over the lifecycle of a database platform.

In this talk we are going to:

* Provide an overview of the Postgres Operator landscape, reviewing widely adopted options such as CloudNativePG, Percona PostgreSQL Operator, Crunchy Data PGO, Zalando Operator, and Bitnami Helm charts.
* Examine why an operator migration can still become necessary, and the licensing, architectural and operational risks and opportunities to account for.
* Discuss implementation approaches for migrating between Operators, such as replication, backup and volume-based patterns.
* Deep dive on a particular Operator migration case study between two popular Postgres K8s operators.

By the end of this session, attendees will have a clearer understanding of the PostgreSQL Operator ecosystem, the risks and opportunities of an Operator technology switch, and concrete strategies for planning and executing the migration.