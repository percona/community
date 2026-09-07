---
id: SPEAK-1492
jira: SPEAK-1492
title: 'Designing a new SQL language feature: Key joins'
layout: single
speakers:
- andreas_karlsson
- joel_jacobsson
talk_url: ''
presentation_date: '2026-10-20'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: PGConf Europe 2026
event_jira: SPEAK-1476
event_status: Accepted
event_date_start: '2026-10-20'
event_date_end: '2026-10-23'
event_url: https://2026.pgconf.eu
event_location: Valencia
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2026/2026-10-20-designing-a-new-sql-language-feature-key-joins.png
---
Back in 2021 Joel approached me with an idea: what if we could take inspiration from graph databases and allow people people to use foreign key relationships to express joins so people could do a bit less typing and at the same time avoid the risk of typos when writing the ON clause. Sounds pretty simple, right?

This talk tells the story all the way from the initial idea to the submission of a formal change proposal to the SQL standard and of a concrete patch to PostgreSQL. Along the way we had many false starts and bad ideas, Joel ended up joining the SQL committee and hosting an ISO meeting, more people joined forces to help us and the feature grew into something quite different, and in our opinion something much more useful.