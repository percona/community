---
id: "cb28d895-aae4-4b78-86d3-4743eb27c19b"
title: "MySQL Test Framework for customer support and bug verification"
layout: single
speakers:
  - sveta_smirnova
talk_url: "https://tdconf.ru/2022/abstracts/8763"
presentation_date: "2022-06-26"
presentation_date_end: ""
presentation_time: "26/Jun/22 11:30 PM"
talk_year: "2022"
event: "Test Driven Conf 2022"
event_status: "Done"
event_date_start: "2022-04-28"
event_date_end: "2022-04-29"
event_url: "https://tdconf.ru/2022"
event_location: "Russia"
talk_tags: ['MySQL', 'Video']
slides: ""
video: "https://www.youtube.com/watch?v=cTzX6IMagnU"
youtube_id: "cTzX6IMagnU"
---
## Abstract

MySQL Test Framework (MTR) is a framework for MySQL regression tests. Tests for it are written by MySQL developers and run in preparation for new releases.

MTR can be used in other ways as well. I use it to test customer-reported issues and validate bug reports on multiple versions of MySQL at the same time.

With MTR you can:

* program complex deployments;
* test the problem on multiple versions of MySQL/Percona/MariaDB servers with a single command;
* test multiple simultaneous connections;
* check for errors and return values;
* work with query results, stored procedures and external commands.

The test can be run on any machine with a MySQL, Percona, or MariaDB server.

I will show how I work with MySQL Test Framework and I hope you will love this tool too.