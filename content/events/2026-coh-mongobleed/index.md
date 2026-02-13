---
title: 'PSMDB and MongoDB MongoBleed: impact, mitigations, and patching strategy - February 24, 2026'
description: In this session, Ivan Groenewold will break down CVE-2025-14847 (“MongoBleed”), a high-severity MongoDB memory disclosure risk when zlib compression is enabled on a network-reachable server. He’ll share the quick mitigation (disable zlib), how to verify it, and next steps for patching.
images:
- events/2026-coh-mongobleed/ivan_intro.png
layout: single
date: '2026-02-24'
EventDate: Tuesday, February 24, 2026 · 16:00-17:00 GMT
EventLocation: Online
speakers:
- ivan_groenewold
tags: ["Community", "Events", "MongoDB", "PSMDB"]
events_year: ["2026"]
events_tag: ["Community", "MongoDB"]
events_category: ["Speaking", "Community"]
---
Discover how CVE-2025-14847 (“MongoBleed”) can expose **MongoDB** to high-severity information disclosure—allowing an unauthenticated remote client to extract fragments of uninitialized server memory when zlib network compression is enabled on a network-reachable instance. 

In this interview, we’ll break down who’s at risk, why zlib is the trigger, and the fastest mitigation: disable zlib while keeping snappy/zstd. We’ll also show how to confirm the fix (server options, logs, and PMM metrics) and how to plan upgrades to patched releases.

- 📅 **Date/Time:** 24 February, 16:00 PM GTM
- 👤 **Speaker:** Ivan Groenewold - Percona Tech Lead, MongoDB
- 📍 **Online**
- 🔗 To Be Confirmed


***Join our Community Office Hours!***

![Percona Community Office Hours Ivan](/events/2026-coh-mongobleed/ivan_intro.png)