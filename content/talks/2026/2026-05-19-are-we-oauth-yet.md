---
id: 2fc674d0-91f3-809d-93d5-e5b4a1419ccb
title: Are we OAuth yet?
layout: single
speakers:
- andreas_karlsson
talk_url: ''
presentation_date: '2026-05-19'
presentation_date_end: ''
presentation_time: ''
talk_year: '2026'
event: PGconf.Dev  2026
event_status: Accepted
event_date_start: '2026-05-19'
event_date_end: '2026-05-22'
event_url: https://2026.pgconf.dev
event_location: 'Vancouver, Canada '
talk_tags:
- PostgreSQL
slides: ''
video: ''
images:
- talks/2026/2026-05-19-are-we-oauth-yet.png
---
## Abstract

OAuth 2.0 support landed in PostgreSQL 18, but support in core PostgreSQL alone is not enough. To be useful to end users there needs to be support in the broader ecosystem: OAuth validator plugins, third-party database clients, CLI tools, database drivers, etc.

This talk gives an overview of the state of OAuth in PostgreSQL and the wider ecosystem. I will share my experiences with adding OAuth support to third-party code and with writing an OAuth validator, and share the pain points I encountered and what can be improved in core PostgreSQL including some improvements already in the pipeline. Finally I will explain how you can help out with making OAuth support in the PostgreSQL world a reality.

And a big thanks to everyone involved in adding Oauth 2.0 to PostgreSQL.