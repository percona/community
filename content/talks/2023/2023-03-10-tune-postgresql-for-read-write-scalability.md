---
id: SPEAK-2542
jira: SPEAK-2542
title: Tune PostgreSQL for Read/Write Scalability
layout: single
speakers:
- ibrar_ahmed
talk_url: https://www.socallinuxexpo.org/scale/20x/presentations/tune-postgresql-readwrite-scalability
presentation_date: '2023-03-10'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2023'
event: SCaLE 20x
event_jira: ''
event_status: Done
event_date_start: '2023-03-10'
event_date_end: ''
event_url: https://www.socallinuxexpo.org/scale/20x/presentations/tune-postgresql-readwrite-scalability
event_location: ''
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2023/2023-03-10-tune-postgresql-for-read-write-scalability.png
---
PostgreSQL is one of the leading open-source databases. Out of the box, the default PostgreSQL configuration is not tuned for any particular workload. Nowadays, production systems have quite expensive machines, which require extra configuration for PostgreSQL. PostgreSQL provides extensive configuration parameters to configure it according to the available hardware. Sometimes it takes work to configure PostgreSQL to get the maximum performance output because it depends on the hardware, workload, and queries. Most of the time, people configure PostgreSQL according to hardware and don’t consider the workload and type of queries. Sometimes a database is write-intensive, sometimes read-intensive, and occasionally read and write-intensive. In all these three cases, there’s a different set of configurations. In this talk, users will see how to configure PostgreSQL for a Read/Write/Read-Write intensive load. This talk will explain every important configuration parameter with real-time examples.