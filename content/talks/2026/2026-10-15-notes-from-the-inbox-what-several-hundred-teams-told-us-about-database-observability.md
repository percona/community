---
id: SPEAK-2891
jira: SPEAK-2891
title: 'Notes from the inbox: what several hundred teams told us about database observability'
layout: single
speakers:
- valeria_bogatyreva
talk_url: https://osoday.com/
presentation_date: '2026-10-15'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2026'
event: Open Source Observability Day (VIRTUAL) 2026
event_jira: SPEAK-1471
event_status: Accepted
event_date_start: '2026-10-15'
event_date_end: '2026-10-16'
event_url: https://osoday.com
event_location: ''
talk_tags:
- Open-Source
slides: ''
video: ''
images:
- talks/2026/2026-10-15-notes-from-the-inbox-what-several-hundred-teams-told-us-about-database-observability.png
---
Most database observability advice comes from people who build the tools. This talk comes from the inbox.
Over the past 4.5 yearsI've been reading and listening to what database teams say when they describe what's broken - unprompted, in their own words, before anyone tries to sell them anything. Inbound inquiries across MySQL, PostgreSQL and MongoDB shops, win/loss interviews, and Percona's State of Open Source Database Management Report.
The patterns are not the ones you'd expect. Coverage is rarely the problem. Teams with extensive monitoring still can't answer ‘why is it slow right now’. Small teams and thousand-instance fleets report the same symptom for opposite reasons. And a surprising number of teams can't tell you what versions they're running - you can't observe what you haven't inventoried.
I'll show the findings, the methodology, and the selection bias, then hand it back: which of these gaps are worth building for, and which no tool will ever fix.