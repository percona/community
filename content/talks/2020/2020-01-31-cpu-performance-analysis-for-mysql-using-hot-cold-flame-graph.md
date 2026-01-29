---
id: "f1ad372b-9772-4dcb-8ee0-70ecf5abaaa8"
title: "CPU performance analysis for MySQL using Hot/Cold Flame Graph"
layout: single
speakers:
  - vinicius_grippa
talk_url: "https://fosdem.org/2020/schedule/event/mysql_cpu_flames/"
presentation_date: "2020-01-31"
presentation_date_end: ""
presentation_time: "31/Jan/20 11:30 PM"
talk_year: "2020"
event: "FOSDEM 2020"
event_status: "Done"
event_date_start: "2020-02-01"
event_date_end: "2020-02-02"
event_url: "https://fosdem.org/2020/"
event_location: "Belgium"
talk_tags: ['MySQL', 'Open Source', 'Video']
slides: ""
video: "https://archive.fosdem.org/2020/schedule/event/mysql_cpu_flames/"
---
## Abstract

Come to see some real-life examples of how you can do CPU profiling with perf and eBPF/BCC, to create FlameGraphs and ColdGraphs visualizations of the on-CPU/off-CPU time spent by the database. Based on these visualizations and reading the database source code (this is why we love Open Source\!) you can quickly gain insight about what's burning CPU (FlameGraphs) and what's causing CPU to wait (ColdGraphs), and with this knowledge you will be several steps closer to answering "what's consuming all that CPU time".