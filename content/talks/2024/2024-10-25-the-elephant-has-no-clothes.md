---
id: "aa9508bc-9ee6-4c4a-98df-1af62aca6018"
title: "The Elephant Has No Clothes"
layout: single
speakers:
  - jan_wieremjewicz
talk_url: "https://2024.pgconf.eu/"
presentation_date: "2024-10-25"
presentation_date_end: ""
presentation_time: ""
talk_year: "2024"
event: "PGConf EU 2024"
event_status: "Done"
event_date_start: "2024-10-22"
event_date_end: "2024-10-25"
event_url: "https://2024.pgconf.eu/"
event_location: "Athens, Greece"
talk_tags: ['PostgreSQL', 'Security', 'Video']
slides: ""
video: "https://www.youtube.com/watch?v=jzjmNmH7OJ0"
youtube_id: "jzjmNmH7OJ0"
---
## Abstract

PostgreSQL is the most popular open-source database among developers. It is one of the Top 5 databases in the world, and it is fully open source and community driven. But, PostgreSQL, the “Emperor” of databases, has no clothes! For all intents and purposes Slonik is “walking around naked” because there is no open source TDE solution to keep the elephant clothed.
Transparent Data Encryption (TDE) is the way that data at rest protection can be done on the database level, ensuring the data is encrypted on the disk as well as in your backups and no application changes are required. While TDE is not available in PostgreSQL we created an extension that addresses (clothes the elephant) this issue and strengthens the security of your database.
Join us as we tell the story of The Elephant Has No Clothes and how Percona is working to solve this issue by creating an open source TDE extension. We will go over data and findings that span the development of the extension, the added security benefits to your database, and point to what the future holds for TDE.