---
title: 'Rate Limiting Strategies with Valkey and Redis - Martin Visser'
description: Martin Visser outlines various rate-limiting algorithms, such as Fixed Window, Token Bucket, and Leaky Bucket, and provides technical strategies for implementing them efficiently using Valkey and Redis. 
images:
- events/2026-coh-martin-valkey-session-03/intro.png
layout: single
date: '2026-02-26'
EventDate: Thursday, February 26, 2026
EventLocation: Online
speakers:
- martin_visser
tags: ["Community", "Events", "Valkey", "Redis", "Security", "Performance"]
events_year: ["2026"]
events_tag: ["Community", "Valkey", "Redis",  "Online"]
events_category: ["Speaking", "Community"]
---

Traffic spikes and "noisy neighbors" can quickly saturate backend resources. In this session, **Martin Visser** (Valkey and Redis Tech Lead @ Percona) explores robust **rate-limiting strategies** to protect system resilience and ensure fair resource allocation.

Martin deep-dives into five essential algorithms, comparing their complexity and memory impact. He provides practical Lua and Python examples for implementing:
* **Fixed Window:** Simple but prone to boundary bursts [00:05:57].
* **Token Bucket:** Highly configurable for general-purpose API limits [00:09:10].
* **Sliding Window Counter:** A memory-efficient way to smooth out bursts using weighted averages [00:16:42].
* **Leaky Bucket:** Ideal for infrastructure protection by shaping traffic into a constant flow [00:20:37].

The talk also addresses real-world scaling challenges, including managing **cluster-wide atomicity with hash tags**, handling **hot keys**, and implementing client-side resilience through **exponential backoff** and standardized HTTP headers.

- 📅 **Date:** February 26, 2026
- 👤 **Speaker:** Martin Visser - Valkey and Redis Tech Lead @ Percona
- 🎥 **Watch the Recording:** [https://youtu.be/h9aqUIt71Ao](https://youtu.be/h9aqUIt71Ao)


***Watch the Presentation!***

[![Rate Limiting Strategies](https://img.youtube.com/vi/h9aqUIt71Ao/maxresdefault.jpg)](https://youtu.be/h9aqUIt71Ao)

<div align="center">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/h9aqUIt71Ao" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>