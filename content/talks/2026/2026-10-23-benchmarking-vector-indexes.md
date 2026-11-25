---
id: SPEAK-3394
jira: SPEAK-3394
sync: skip
title: Benchmarking Vector Indexes
layout: single
speakers:
- evgeniy_patlan
talk_url: https://buildevcon.com/events/vector-in-databases
presentation_date: '2026-10-23'
presentation_date_end: ''
presentation_time: '14:30'
room: ''
talk_year: '2026'
event: Vector in Databases
event_jira: SPEAK-2671
event_status: Done
event_date_start: '2026-10-23'
event_date_end: '2026-10-23'
event_url: https://buildevcon.com/events/vector-in-databases
event_location: ''
talk_tags:
- ai
- databases
- vector-database
- Video
slides: ''
video: https://www.youtube.com/watch?v=Nd1MBup7t80
youtube_id: Nd1MBup7t80
images:
- talks/2026/2026-10-23-benchmarking-vector-indexes.png
---
A queries-per-second number without recall does not tell you whether the index returned the right rows. At Vector in Databases on October 23, Yevhen Patlan showed how to measure vector search so you can check the number, and why a database is not a library.

ANN-Benchmarks already sweeps recall and throughput for libraries. A database adds an optimizer that can skip the index, a cache, storage rules, and filters that run with the vector predicate. Vector Bench, in Percona Lab, builds each engine from a pinned version, runs it in its own container on the same CPU cores and the same data, and writes a report plus a manifest so you can repeat the run. The client sits in a second container. Otherwise the data set held in memory gets counted as database memory.

He compared HNSW implementations with each other, not HNSW with IVF, so the difference is the engine rather than the algorithm. Recall is a setting. On one index, ef_search 10 returned 3,678 queries per second at recall 0.959. ef_search 800 returned 409 queries per second at recall 0.999, about nine times slower for a closer answer. Both figures are the same index. Compare the curve, not a single point.

He also called out two ways a published number goes wrong. Putting one engine's bulk index build next to another's incremental build is not a comparison of engines. A silent full scan is exact and slow, so it looks like a careful index unless you read the plan. Every driver in the harness runs EXPLAIN and checks that the plan uses the index.

Watch the recording for the full session. If a measurement looks unfair to an engine you know, he asked you to say so. The project is Vector Bench in Percona Lab on GitHub.

[Recording](https://www.youtube.com/watch?v=Nd1MBup7t80)