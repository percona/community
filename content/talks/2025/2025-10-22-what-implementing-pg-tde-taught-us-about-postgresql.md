---
id: "222674d0-91f3-8053-a28d-df125703a538"
title: "What implementing pg_tde taught us about PostgreSQL"
layout: single
speakers:
  - jan_wieremjewicz
talk_url: ""
presentation_date: "2025-10-22"
presentation_date_end: ""
presentation_time: "16:05–16:55"
talk_year: "2025"
event: "PGConf EU 2025 Riga"
event_status: "Done"
event_date_start: "2025-10-21"
event_date_end: "2025-10-24"
event_url: "https://2025.pgconf.eu"
event_location: "Riga, Latvia"
talk_tags: ['Security', 'PostgreSQL', 'Open Source']
slides: "https://www.postgresql.eu/events/pgconfeu2025/sessions/session/7191/slides/807/PGConf%20EU%202025%20Riga%20TDE%20slides.pdf"
video: ""
---
## Abstract

This is a firsthand account of bringing Transparent Data Encryption to PostgreSQL through  pg_tde . From idea to patch proposals, it’s a story of navigating PostgreSQL’s internals, Community realities, and trade-offs between extension and core changes.
Why weren’t existing hooks enough? What friction did we hit? How was the experience with the Community feedback cycle? What customer feedback shaped the final design and how did users react to the proposed solutions? Based on years of work to deliver a critical enterprise capability, this talk is a diary of what it took to deliver Transparent Data Encryption as an extension to PostgreSQL, from a product manager who lived through it.