---
id: "2f0674d0-91f3-8098-8085-cd6a523a20e8"
title: "Bringing Flamegraphs to MySQL Query Optimization"
layout: single
speakers:
  - vinicius_grippa
talk_url: "https://www.mysqlandfriends.eu/post/prefosdem-mysql-belgian-days-2026-agenda/"
presentation_date: "2026-01-30"
presentation_date_end: ""
presentation_time: "1:15 pm"
talk_year: "2026"
event: "MySQL Belgian Days (preFOSDEM) 2026"
event_status: "Done"
event_date_start: "2026-01-29"
event_date_end: ""
event_url: "https://www.mysql.com/news-and-events/events/mysql-belgian-aka-pre-fosdem-days/"
event_location: "Belgian, Brussels"
talk_tags: ['MySQL', 'Video']
slides: ""
video: "https://www.youtube.com/watch?v=tdx9leN2kBg"
youtube_id: "tdx9leN2kBg"
---
## Abstract

Brendan Gregg developed flame graphs, which provide a powerful way to visualize hierarchical data. Later on, Tanel Poder introduced the same concept for Oracle queries. This time, I’m bringing this idea for the first time as an open-source project to MySQL.
Using the new JSON format for MySQL, we can now perform detailed query analysis based on the actual execution plan, displaying the query’s internal operations in a way that can be programmatically consumed and visualized.
In this session, we will walk through how to transform raw execution-plan data into flame graphs and explore the benefits that visualization brings and how it helps us to interpret and diagnose query behavior.