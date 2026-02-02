---
id: "166674d0-91f3-8082-93be-e7349ac8c26a"
title: "Modern SQL features in PostgreSQL that can transform the way we develop database applications"
layout: single
speakers:
  - jobin_augustine
talk_url: "https://pgconf.in/conferences/pgconfin2025/program/proposals/862"
presentation_date: "2025-03-06"
presentation_date_end: ""
presentation_time: "15:30"
talk_year: "2025"
event: "PGConf India 2025"
event_status: "Done"
event_date_start: "2025-03-05"
event_date_end: "2025-03-07"
event_url: "https://pgconf.in/conferences/pgconfin2025"
event_location: "Bangalore, India"
talk_tags: ['PostgreSQL', 'Video']
slides: "https://pgconf.in/files/presentations/2025/862.pdf"
video: "https://www.youtube.com/watch?v=s5pQXoSV6dk"
youtube_id: "s5pQXoSV6dk"
---
## Abstract

PostgreSQL is the most advanced open-source database in terms of SQL processing capabilities. However, many users are unaware of the sheer power hiding inside its SQL engine and still write SQL-92 statements. With advanced SQL capabilities, much higher concurrency and performance can be achieved. This talk discusses some of the modern SQL techniques for developing applications with examples.
• Implementation of data retention policy (archiving and purging) as a single statement.
• Partitioning large tables without causing heavy wait locks or downtime.
• Advanced uses of CTE - Complex transactions as a single statement.
• Modern features like Merge and its use, such as replacing pl/pgsql procedures with single statements.
• Cost of rollbacks and method to avoid