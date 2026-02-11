---
id: "2ee674d0-91f3-8068-9bdd-c5b45f1a8056"
title: "MySQL Test Framework for Support and Bugs Work"
layout: single
speakers:
  - sveta_smirnova
talk_url: "https://archive.fosdem.org/2018/schedule/event/mysql_test_framework/"
presentation_date: "2018-02-04"
presentation_date_end: ""
presentation_time: ""
talk_year: "2018"
event: "FOSDEM 2018"
event_status: "Done"
event_date_start: "2018-02-03"
event_date_end: "2018-02-04"
event_url: "https://archive.fosdem.org/2018/schedule/"
event_location: "Brussels, Belgium"
talk_tags: ['MySQL', 'Video', 'Slides']
slides: "https://archive.fosdem.org/2018/schedule/event/mysql_test_framework/attachments/slides/2155/export/events/attachments/mysql_test_framework/slides/2155/MTR.pdf"
video: "https://archive.fosdem.org/2018/schedule/event/mysql_test_framework/"
---
## Abstract

MySQL Test Framework (MTR) provides unit test suite for MySQL. Tests in the framework are written by MySQL Server developers and contributors and run to ensure build is working correctly.
I found this is not the only thing which can be done with MTR. I regularly use it in my Support job to help customers and verify bug reports.
With MySQL Test Framework I can:
• Create complicated environment in single step and re-use it later
• Test same scenario on dozens of MySQL/Percona/MariaDB server versions with single command
• Test concurrent scenarios
• Test errors and return codes
• Work with results, external commands, stored routines
Everything with single script which can be reused on any machine any time with any MySQL/Percona/MariaDB Server version.
In this session I will show my way of working with MySQL Test Framework and I hope you will love it as I do!