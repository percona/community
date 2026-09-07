---
id: SPEAK-2234
jira: SPEAK-2234
title: Avoiding pitfalls with Postgres and go
layout: single
speakers:
- yoann_la_cancellera
talk_url: https://golab.io/talks/avoiding-pitfalls-with-postgres-and-go
presentation_date: '2026-11-02'
presentation_date_end: ''
presentation_time: ''
talk_year: '2026'
event: GoLab 2026
event_jira: SPEAK-2010
event_status: Accepted
event_date_start: '2026-11-01'
event_date_end: '2026-11-03'
event_url: https://golab.io
event_location: Bologna
talk_tags:
- Golang
- PostgreSQL
- italian
- programming
- software-development
slides: ''
video: ''
images:
- talks/2026/2026-11-02-avoiding-pitfalls-with-postgres-and-go.png
---
PostgreSQL is probably the most loved database to work with Go, for good reasons!

As someone helping to scale many large postgres environments, some seemingly innocent choices end up being silent bottlenecks limiting the database possibilities.

In this talk we will discuss less common tips on how to keep your postgres running happy with your go application.

The goal is to guide you on how to stay flexible and prevent you from getting stuck in a position that would prevent you from scaling postgres in the future.

We will discuss:

dos and don'ts with transactions

avoiding session variables and temporary tables

avoiding losing performance to network round-trips

avoiding staying idle in the database for any reason

staying flexible with ORMs

being able to use proper cancellation