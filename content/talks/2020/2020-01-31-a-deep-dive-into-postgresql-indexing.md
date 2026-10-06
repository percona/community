---
id: SPEAK-2526
jira: SPEAK-2526
title: A Deep Dive into PostgreSQL Indexing
layout: single
speakers:
- ibrar_ahmed
talk_url: https://fosdem.org/2020/schedule/event/postgresql_a_deep_dive_into_postgresql_indexing/
presentation_date: '2020-01-31'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2020'
event: FOSDEM 2020
event_jira: ''
event_status: Done
event_date_start: '2020-01-31'
event_date_end: ''
event_url: https://fosdem.org/2020/schedule/event/postgresql_a_deep_dive_into_postgresql_indexing/
event_location: ''
talk_tags: []
slides: ''
video: ''
images:
- talks/2020/2020-01-31-a-deep-dive-into-postgresql-indexing.png
---
Indexes are a basic feature of relational databases, and  PostgreSQL offers a rich collection of options to developers and designers. To take advantage of these fully, users need to understand the basic concept of indexes, to be able to compare the different index types and how they apply to different application scenarios. Only then can you make an informed decision about your database index strategy and design. One thing is for sure: not all indexes are appropriate for all circumstances, and using a ‘wrong’ index can have the opposite effect to that you intend and problems might only surface once in production. Armed with more advanced knowledge, you can avoid this worst-case scenario!

We’ll take a look at how to use pg_stat_statment to find opportunities for adding indexes to your database. We’ll take a look at when to add an index, and when adding an index is unlikely to result in a good solution. So should you add an index to every column? Come and discover why this strategy is rarely recommended as we take a deep dive into PostgreSQL indexing.