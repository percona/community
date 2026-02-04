---
id: "145674d0-91f3-80c1-a21f-c59d0efc1e2c"
title: "Open-source support for JS stored programs in Percona Server"
layout: single
speakers:
  - dmitry_lenev
talk_url: "https://archive.fosdem.org/2025/schedule/event/fosdem-2025-4814-open-source-support-for-js-stored-programs-in-percona-server/"
presentation_date: "2025-02-02"
presentation_date_end: ""
presentation_time: ""
talk_year: "2025"
event: "FOSDEM 2025"
event_status: "Done"
event_date_start: "2025-02-01"
event_date_end: "2025-02-02"
event_url: "https://fosdem.org/2025/"
event_location: "Brussels, Belgium"
talk_tags: ['MySQL', 'Open Source', 'Video']
slides: "https://archive.fosdem.org/2025/events/attachments/fosdem-2025-4814-open-source-support-for-js-stored-programs-in-percona-server/slides/238825/Open-sour_Bi0nFa5.pdf"
video: "https://archive.fosdem.org/2025/schedule/event/fosdem-2025-4814-open-source-support-for-js-stored-programs-in-percona-server/"
---
## Abstract

Support for stored programs written in JavaScript (often abbreviated
as JS) was added by Oracle to MySQL version 9.0. Unfortunately, this
feature is only available in MySQL Enterprise Edition and not in
Community version of MySQL.
Percona is working on an alternative, free and open-source implementation
of JS stored programs for its Percona Server for MySQL, based on widely
used V8 engine (the latest version of code is available on Percona's GitHub
at  ** https://github.com/percona/percona-server/tree/js-lang** ).
This talk will provide an overview of this alternative implementation.
We will discuss what features are supported, what are the limitations
and how this implementation is different from the one from Upstream.
We will also talk about performance results for this implementation, some
interesting implementation details and challenges we encountered while
working on it.