---
id: "310674d0-91f3-80cf-981e-c0ba11e7f162"
title: "Everything you need to know about collations"
layout: single
speakers:
  - andreas_karlsson
talk_url: "https://www.postgresql.eu/events/pgconfde2026/sessions/session/7576-everything-you-need-to-know-about-collations/"
presentation_date: "2026-04-21"
presentation_date_end: "2026-04-22"
presentation_time: ""
talk_year: "2026"
event: "PGConf Germany 2026"
event_status: "Accepted"
event_date_start: "2026-04-21"
event_date_end: "2026-04-22"
event_url: "https://2026.pgconf.de/"
event_location: "Essen, Germany"
talk_tags: ['PostgreSQL']
slides: ""
video: ""
---
## Abstract

Outside of causing trouble for you when upgrading libc what are collations good for? PostgreSQL's collations have gotten a lot of bad press from the upgrade issues but they are also a powerful and important tool, especially for working with text in other languages than English.

This talk will give an introduction to collations in PostgreSQL, including how to use them, what they are useful for, how they work plus some common pitfalls and misunderstandings. You will learn, among other things, about the three collation providers (libc, icu, builtin), BCP 47, case insensitive collations, CTYPEs, what new features have been introduced in recent PostgreSQL versions and get a brief look into the future of collations in PostgreSQL.