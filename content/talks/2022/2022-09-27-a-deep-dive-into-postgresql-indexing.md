---
event: PGCONF NYC 2022
event_date_end: ''
event_date_start: '2022-09-27'
event_jira: ''
event_location: ''
event_status: Done
event_url: https://postgresql.us/events/pgconfnyc2022/schedule/session/1039-a-deep-dive-into-postgresql-indexing/
id: SPEAK-2534
jira: SPEAK-2534
layout: single
presentation_date: '2022-09-27'
presentation_date_end: ''
presentation_time: ''
room: ''
slides: ''
speakers:
- ibrar_ahmed
talk_tags:
- PostgreSQL
- Video
talk_url: https://postgresql.us/events/pgconfnyc2022/schedule/session/1039-a-deep-dive-into-postgresql-indexing/
talk_year: '2022'
title: A Deep Dive into PostgreSQL Indexing
video: https://www.youtube.com/watch?v=3rQZpq_HXhY
youtube_id: 3rQZpq_HXhY
images:
- talks/2022/2022-09-27-a-deep-dive-into-postgresql-indexing.png
---
Indexes are a fundamental feature of relational databases, and PostgreSQL offers developers and designers a rich collection of options. To take advantage of these entirely, users need to understand the basic concept of indexes to compare the different index types and apply them to different application scenarios. Only then can you make an informed decision about your database index strategy and design. One thing is for sure: not all indexes are appropriate for all circumstances, and using a ‘wrong’ index can have the opposite effect to what you intend, and problems might only surface once in production. Armed with more advanced knowledge, you can avoid this worst-case scenario! We’ll take a look at how to use pg_stat_statment to find opportunities for adding indexes to your database. We’ll look at when to add an index, and when adding an index is unlikely to result in a good solution. So should you add an index to every column? Come and discover why this strategy is rarely recommended as we take a deep dive into PostgreSQL indexing.
