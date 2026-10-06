---
id: SPEAK-2492
jira: SPEAK-2492
title: Using JSON in a Relational Database Best Practices
layout: single
speakers:
- dave_stokes
talk_url: https://www.socallinuxexpo.org/scale/20x/presentations/using-json-relational-database-best-practices
presentation_date: '2023-03-09'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2023'
event: SCaLE 20x
event_jira: ''
event_status: Done
event_date_start: '2023-03-09'
event_date_end: ''
event_url: https://www.socallinuxexpo.org/scale/20x/presentations/using-json-relational-database-best-practices
event_location: ''
talk_tags: []
slides: ''
video: ''
images:
- talks/2023/2023-03-09-using-json-in-a-relational-database-best-practices.png
---
Relational databases = strict data types and stored schema.  JSON = free form but no data rigor.  But what if you could reliably use JSON in your relational database to get performance, the processing power of Structured Query Language (SQL), and reatain the flexibility JSON is know for.  This talk will cover the best practices for using JSON in your realtional database, how to temporarily transform unstructured JSON data into structured data with JSON_TABLE() or permanently with generated columns.  And how do you ensure that the JSON data has the proper format or is required before entry to the database.