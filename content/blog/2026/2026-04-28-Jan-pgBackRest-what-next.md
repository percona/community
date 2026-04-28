---
title: "pgBackRest is archived, what now?"
date: "2026-04-27T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'pgBackRest']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2026/04/Jan-pgb-cover.png
---

[pgBackRest](https://github.com/pgbackrest/pgbackrest) is an open source backup and restore tool for PostgreSQL. It’s fair to say it’s one of the most popular options, widely used across the PostgreSQL ecosystem.

On 27 April 2026, pgBackRest maintainer David Steele announced on [LinkedIn](https://www.linkedin.com/posts/davidsteele_after-a-lot-of-thought-i-have-decided-to-share-7454442611911655424-mVMS?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAD3qpgBKSXefFXDYJlyIbIdar9mZh-NYBw) and in the [GitHub repository](https://github.com/pgbackrest/pgbackrest) that the project is becoming ~unmaintained~ archived, starting with:

> TL;DR: pgBackRest is no longer being maintained. If you fork pgBackRest, please select a new name for your project.
![](blog/2026/04/Jan-david-li.png)

If you’re reading this, you’re likely either affected or at least concerned. In this short write up I will do my best to calm your nerves, present short term as well as more long term ideas and options.

## Where are we now - the status quo
pgBackRest is a critical part of the PostgreSQL ecosystem, and nobody seriously expects it to simply disappear. What happens next is now up to the community.
One possible outcome is the emergence of multiple forks of pgBackRest. That raises the risk of fragmentation or, put bluntly, ~Clone~ Fork Wars.
![](blog/2026/04/Jan-forks.png)

That said, there has already been a significant amount of discussion across the community, and one thing is clear:

The PostgreSQL community acknowledges the problem and wants change.

The challenge now is twofold:
* What can we do immediately to stabilize the situation?
* What direction should we take long term, without overcomplicating the short-term response?

## What is Percona planning
Percona includes pgBackRest in the Percona Distribution for PostgreSQL as the recommended backup and restore solution. From our perspective, it remains the most mature, enterprise-ready and reliable option available. While alternatives like WAL-G or Barman are well regarded, our recommendation remains unchanged.

To emphasize the message: 

> the current situation does not impact our recommendation.

Percona will continue supporting pgBackRest. What that support looks like in terms of maintainership and collaboration with other organizations is still being actively discussed and will take time to solidify.

The immediate priority is to avoid fragmentation. We want to ensure we don’t end up with multiple independent forks maintained in isolation.

If you are a Percona customer, you remain fully supported. Please continue reporting issues through standard support channels. For our community users, we encourage you to use the [Percona Community Forums](https://forums.percona.com/), we will do our best to help there.

## The power of open source community

In an era where we often hear about companies reducing teams due to AI-driven cost optimization, it’s easy to forget that software is still built and maintained by people. This is especially true in open source.

Two observations are worth calling out:
1. People need sustainable funding, work cannot be assumed to be purely voluntary.
2. A healthy open source project should not depend on a single company or individual.

The current situation is, to some extent, a result of the opposite model. pgBackRest development was largely driven by a single company and later single maintainer, David Steele, with sponsorship from Crunchy Data. While others have contributed (e.g. Stephen Frost and [pgstef](https://github.com/pgstef), the project effectively relied on one primary maintainer.
I think it’s fair to say we’ve seen a fair share [xkcd \#2347](https://xkcd.com/2347/) posted all over the internet over the course of last 24h. So here’s one more
![](blog/2026/04/Jan-comic-neb.png)

To avoid repeating this pattern, we — along with other vendors — are deliberately taking time before jumping into forks or immediate solutions. The goal is to find a sustainable, collaborative model rather than rushing into fragmentation.

For comparison, it took the Linux Foundation 6 days to respond to the [Redis license change](https://github.com/redis/redis/pull/13157) by [launching Valkey](https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community). While this situation is different as there’s no license change in pgBackRest, it illustrates that meaningful coordination takes time.

This is exactly where the open source community can demonstrate its strength.

## What are the long term options?

This situation is particularly surprising to me personally, as I recently referenced David’s proposed transparent funding model in [my talk](https://www.postgresql.eu/events/pgconfde2026/) at [PGConf.DE](http://pgconf.de/) just last week.
![](Jan-david-money.png)

The idea, distributing funding across organizations that rely on the project, seemed like a promising path toward a more sustainable ecosystem. In hindsight, it appears that adoption of this model was either too slow or insufficient to support ongoing maintenance.

Looking ahead, several long-term options are being discussed within the community:
* Establishing a foundation-backed project (similar to models used by [Codeberg](https://codeberg.org/) or the Linux Foundation)
* Creating a coordinated, multi-vendor stewardship model
* In more extreme scenarios, moving critical tooling closer to the PostgreSQL core ecosystem

These discussions are ongoing. If you’re attending [PGConf.Dev](https://2026.pgconf.dev/), this will almost certainly be a major topic, especially in the extensions ecosystem track of community sessions in the [Canfor](https://2026.pgconf.dev/schedule/tuesday) room on Tuesday.

## So what should I do now?
![](blog/2026/04/Jan-what-now.png)

In short, nothing but wait. Yes, this means:

> Keep on using pgBackRest as you did!

If your company is relying on pgBackRest, now is the time to engage. If you have capacity for this, please join the discussion (we’ve kicked off a thread on [Percona Community Forums](https://forums.percona.com/t/pgbackrest-archival-discussion/40725?u=jan_wieremjewicz) if you are looking for a place to join this topic)

Rest assured that you can follow the updates from us, we will be messaging about the progress made in regards to establishing the future for pgBackRest.

One thing to clear is: are there any immediate risks?

> Not new ones. There is the uncertainty that this is not a comfortable feeling. Rest assured that the longevity of the solution is not in jeopardy as we do have an obligation to our customer and user base to make sure the project is continued.

