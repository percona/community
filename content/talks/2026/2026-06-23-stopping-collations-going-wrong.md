---
id: SPEAK-2320
jira: SPEAK-2320
title: Stopping Collations Going Wrong
layout: single
speakers:
- andreas_karlsson
talk_url: https://www.meetup.com/london-postgresql-meetup-group/events/315092418/
presentation_date: '2026-06-23'
presentation_date_end: ''
presentation_time: '19:00'
room: ''
talk_year: '2026'
event: London PostgreSQL Meetup
event_jira: ''
event_status: Done
event_date_start: '2026-06-23'
event_date_end: ''
event_url: https://www.meetup.com/london-postgresql-meetup-group/events/315092418/
event_location: London
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2026/2026-06-23-stopping-collations-going-wrong.png
---
Outside of causing trouble for you when upgrading libc what are collations good for? PostgreSQL's collations have gotten a lot of bad press from the upgrade issues but they are also a powerful and important tool, especially for working with text in other languages than English.

This talk will give an introduction to collations in PostgreSQL, including how to use them, what they are useful for, how they work plus some common pitfalls and misunderstandings. You will learn, among other things, about the three collation providers (libc, icu, builtin), BCP 47, case insensitive collations, CTYPEs, what new features have been introduced in recent PostgreSQL versions and get a brief look into the future of collations in PostgreSQL.
