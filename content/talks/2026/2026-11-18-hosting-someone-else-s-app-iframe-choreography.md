---
id: SPEAK-2642
jira: SPEAK-2642
title: 'Hosting Someone Else''s App: Iframe Choreography'
layout: single
speakers:
- fabio_da_silva
talk_url: https://js-poland.pl/speaker/2026/fabio-silva
presentation_date: '2026-11-18'
presentation_date_end: ''
presentation_time: '15:40'
room: ''
talk_year: '2026'
event: JS Poland
event_jira: SPEAK-2085
event_status: Accepted
event_date_start: '2026-11-17'
event_date_end: '2026-11-19'
event_url: https://js-poland.pl
event_location: Warsaw
talk_tags:
- conference
- javascript
- polish
- web
slides: ''
video: ''
images:
- talks/2026/2026-11-18-hosting-someone-else-s-app-iframe-choreography.png
---
Most frontend architecture talks assume you control the whole page. This one doesn't. Percona Monitoring and Management (PMM) ships a React/TypeScript shell that owns routing, navigation, and auth — and then embeds an entire third-party application, Grafana, inside an iframe it doesn't control the internals of. The two apps have to feel like one product: shared theme, shared navigation, shared login state, no visible seam.

This talk walks through how that's actually built: a custom CrossFrameMessenger that turns postMessage into typed, promise-based RPC calls with timeouts and listener lifecycles; and the handshake that gates showing the iframe until the guest app has actually finished loading. I'll cover the race conditions this design has to defend against, how you test cross-frame code without an end-to-end browser suite for everything, and where the abstraction leaks.

You'll leave with a mental model for host/guest iframe architecture that applies well beyond Grafana — anywhere you're embedding a third-party app, a legacy system, or a different team's SPA inside your own shell.