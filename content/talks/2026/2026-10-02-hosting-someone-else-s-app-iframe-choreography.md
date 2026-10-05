---
id: SPEAK-2900
jira: SPEAK-2900
title: 'Hosting Someone Else''s App: Iframe Choreography'
layout: single
speakers:
- fabio_da_silva
talk_url: https://feit.stu.cn.ua/foss/
presentation_date: '2026-10-02'
presentation_date_end: ''
presentation_time: '11:55'
room: ''
talk_year: '2026'
event: FEIT STU - Free/Open Source Software in Education, Science & Business
event_jira: SPEAK-2636
event_status: Accepted
event_date_start: '2026-10-01'
event_date_end: '2026-10-02'
event_url: https://feit.stu.cn.ua/foss/
event_location: ''
talk_tags:
- Open-Source
- Tech
- software-development
slides: ''
video: ''
images:
- talks/2026/2026-10-02-hosting-someone-else-s-app-iframe-choreography.png
---
Most frontend architecture talks assume you control the whole page. This one doesn't. Percona Monitoring and Management (PMM) ships a React/TypeScript shell that owns routing, navigation, and auth — and then embeds an entire third-party application, Grafana, inside an iframe it doesn't control the internals of. The two apps have to feel like one product: shared theme, shared navigation, shared login state, no visible seam.This talk walks through how that's actually built: a custom CrossFrameMessenger that turns postMessage into typed, promise-based RPC calls with timeouts and listener lifecycles; and the handshake that gates showing the iframe until the guest app has actually finished loading. I'll cover the race conditions this design has to defend against, how you test cross-frame code without an end-to-end browser suite for everything, and where the abstraction leaks.You'll leave with a mental model for host/guest iframe architecture that applies well beyond Grafana — anywhere you're embedding a third-party app, a legacy system, or a different team's SPA inside your own shell.