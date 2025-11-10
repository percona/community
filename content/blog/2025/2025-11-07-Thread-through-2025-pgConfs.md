---
title: "A thread through my 2025 Postgres events"
date: "2025-11-07T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_alastair', 'Community']
categories: ['PostgreSQL']
images:
  - blog/2025/11/cover-map-blue.jpg
authors:
  - alastair_turner
slug: thread-through-2025-pgconfs
---

I recently got back from PostgreSQL Conference Europe in Riga, marking the end of my conference activities for 2025. The speakers were great. The audience, for the Extensions Showcase on Community Day on Tuesday and my Kubernetes from the database out talk, were great. The event team was great. The singing at karaoke was terrible, but it’s supposed to be.

After attending a good few events this year, starting with CERN PGDay in mid-January, I wanted to write something about more than just the most recent event. I see a common thread across presentations and sessions at a number of events over the year, that is, scale-out Postgres and particularly, its use in non-profit scientific environments.

### The (beginning and) end users

Far fewer data processing challenges require pooling the resources of many physical servers these days, with servers getting bigger and storage faster. Scientific data analysis and managing large, complex scientific facilities still do. I saw three presentations on this: Rafal Kulaga, Antonin Kveton and Martin Zemko’s on [managing CERN’s SCADA data](https://indico.cern.ch/event/1471762/contributions/6280212/); Daniel Krefl and Krzysztof Nienartowicz at CERN on [how Sendai queries variable star data](https://indico.cern.ch/event/1471762/contributions/6280216/); and Jaoquim Oliveira in Riga on [managing the European Space Agency’s (ESA’s) survey mission data](https://www.postgresql.eu/events/pgconfeu2025/schedule/session/7138-from-stars-to-storage-engines-migrating-big-science-workloads-beyond-greenplum/).

I admit a fondness for ESA’s GAIA catalog dataset. After I was lucky enough to do a proof of concept project on joining it with other catalog data, it has provided significant intellectual interest. Don’t let me get started on the possible ways to optimise computationally expensive inequality joins on horribly skewed data, unless you really care about the problem. My interest in a dataset discussed in two of these talks is not why the thread connecting them is worth commenting on. All three presentations had a lot of content on selecting or developing database technologies for the work they were doing. That’s worth discussing a bit further.

### Getting the details right

The thread of sharded, scale out, or Massively Parallel Processing (MPP) Postgres connects end user stories at my first event of the year and my last, along with stories of building this software at events in between. At PGConf.dev in Montreal David Wein gave a very condensed explanation of how AWS’s Aurora Limitless handles distributed snapshot isolation ([watch the lightning talk at on YouTube](https://www.youtube.com/watch?v=UrRkHSxP2xE&t=378s)), there was also an unconference session on handling the issue in core Postgres the next day. For an in-depth explanation of of what the distributed snapshot problem is and how it may be addressed, see [Ants Aasma’s talk from PGConf.EU 2024](https://www.postgresql.eu/events/pgconfeu2024/schedule/session/5710-high-concurrency-distributed-snapshots/)

The organisations with the data are looking for open source software solutions and bumping into issues around open core licensing, project contribution breadth, project activity levels, project governance. The Postgres developer community is working on the knottiest of the problems in this space, trying to get it absolutely right. In the mean-time, various forks and extensions are delivering useful functionality for the owners of these big, complex datasets.
Useful, but could do better

If this were working out for everyone, there wouldn’t be a story to tell. Sednai are building Potgres-XZ, which builds on TBase, which built on Postgres-XL. The ESAC Science Data Centre (ESDC) is facing a decision between two single-vendor projects, where one vendor doesn’t provide support for on-premises deployments. CERN procurement sought written assurances over license terms for TimescaleDB, since the CERN facilities organisation may be viewed as a service provider to their hosted scientific projects.

This pattern of licenses built specifically to avoid “AWS stealing our innovation/lunch/…”, (and it is always AWS set up as the bogeyman in these stories), is particularly unfortunate here, because it just isn’t true for Postgres. AWS, and Azure, employ big teams of community contributors to work on open source Postgres. The progress on statistics management, asynchronous IO, and vacuum in Postgres 18 are, among others, thanks to these teams’ efforts.

No matter how positive the involvement of the hyperscalers may be for Postgres, there are organisations who will prefer to run their own databases. On-premises hosting is a clear choice for organisations with big facilities capabilities, capital-centric budgeting, extreme requirements and predictable, always on workloads. Many of these organisations are publicly funded scientific projects. It would be great if there were broad-based open source solutions to meet their data management needs.

### Doing better, together

At PGConf in Riga the Percona team took a few, early steps towards building a joint effort to deliver the components of such a solution. I hope that the big, open managers of structured scientific data (or their subcontractors, depending on their engagement model) and a few vendors can come together to build event data compression, columnar storage, and all the other bits which can be implemented as extensions.

The current Postgres extensions and forks for scale out systems were built on older versions of Postgres, so they had to build features which now exist in core Postgres. Their implementation of partitioning, for instance, differs subtly from the capabilities now available in modern Postgres. As feature-specific extensions can take over capabilities which are currently intertwined with sharding (like compression in Timescale or columnar storage in Citus), users will be less locked in to vertical stacks of features, some useful to them and some not. Simple sharding can then become a proxy (like pgDog), an automation on DDL on a gateway server or even a core Postgres feature.

Which leaves those special cases where moving data between shards during execution is key to performance. This is mattering less with ever bigger servers, improving Postgres parallelism and tools like DuckDB - but when it matters it still really matters. Here the sons of the ‘plum - CloudberryDB and WarehousePG, forked from Greenplum when it closed source - work their magic (hat tip to Jimmy Angelakos for the “the ‘plum” contraction). Managing that particular capability will always be a big, complex code base. If the patches carried to make it happen shrink as Postgres and extensions fill the gap, we’ll have a more sustainable route to all good database things being openly available.
