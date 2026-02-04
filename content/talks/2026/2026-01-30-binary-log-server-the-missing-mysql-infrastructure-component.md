---
id: "2ee674d0-91f3-8052-8d3d-e016fac9eef0"
title: "Binary Log Server - the missing MySQL infrastructure component"
layout: single
speakers:
  - yura_sorokin
talk_url: "https://www.mysqlandfriends.eu/post/prefosdem-mysql-belgian-days-2026-agenda/"
presentation_date: "2026-01-30"
presentation_date_end: ""
presentation_time: "9:35 am"
talk_year: "2026"
event: "MySQL Belgian Days (preFOSDEM) 2026"
event_status: "Accepted"
event_date_start: "2026-01-29"
event_date_end: ""
event_url: "https://www.mysql.com/news-and-events/events/mysql-belgian-aka-pre-fosdem-days/"
event_location: "Belgian, Brussels"
talk_tags: ['MySQL']
slides: ""
video: ""
---
## Abstract

In this session I will give you an introduction to a new open-source tool in the MySQL family – the Binary Log Server from Percona. This tool started as a simple continuous backup solution for Point-in-time Recovery (PITR). The Binary Log Server has a huge potential to become a first-class citizen in the MySQL infrastructure with multi-tenant support, REST API for management, and basic event data querying capabilities. The Binary Log Server can also serve as an intermediate link in complex replication topologies. It supports local file storage and AWS S3 for keeping binlog data and can be easily extended with other storage providers.
 https://github.com/Percona-Lab/percona-binlog-server