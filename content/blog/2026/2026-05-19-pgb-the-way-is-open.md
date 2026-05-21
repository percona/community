---
title: "Backrest's back, alright!"
date: "2026-05-19T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'pgBackRest']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2026/05/Jan-pgb-back-alright.jpg
---

Events unfolded quickly over the course of a couple of weeks starting on 27 April 2026, when a [message appeared on the pgBackRest project announcing](https://pgbackrest.org/news.html):
 that the repository would be archived and active maintenance would stop.

![blog/2026/05/Jan-pgb-news-1.png](blog/2026/05/Jan-pgb-news-1.png)

For many in the PostgreSQL ecosystem, this landed like a shock. [pgBackRest](https://pgbackrest.org/) is one of the most widely used backup and recovery tools for PostgreSQL, deeply embedded in production environments across enterprises large and small. Now it was suddenly described as “[dead](https://mydbanotebook.org/posts/pgbackrest-is-dead.-now-what/)”, “[EOL](https://www.gabrielebartolini.it/articles/2026/04/why-the-cycle-of-open-source-sustainability-needs-to-be-virtuous/)”, or “[abandoned](https://news.ycombinator.com/item?id=47919997)”. The trigger was clear: its long-time maintainer, after more than a decade of work, announced he could no longer continue without sustainable funding and would archive the repository.
i
That message spread fast. The interpretation spread even faster.

And it was wrong.

## This wasn’t EOL

Open source software doesn’t simply “go end of life” in the way proprietary software does. There is no vendor switch flipped to OFF. No license revoked. No binaries disappearing overnight.

What actually happens is more subtle and more important:

- Maintainers step away
- Funding runs out
- Work stops

That’s not EOL. That’s a sustainability gap.

[pgBackRest](https://github.com/pgbackrest/pgbackrest) didn’t die. It hit a problem seen too often in open source world: a critical piece of infrastructure maintained by fewer and fewer people, until it ultimately depended on one person being able to justify working on it full time.

## The real problem

The message from the maintainer was not about abandoning the project. It was about reality:

> maintaining a widely used tool requires time, and time requires funding
> 

For years, pgBackRest was supported through corporate sponsorship from mainly one vendor. When that disappeared due to the Crunchy Data acquisition, so did the ability to keep investing the same level of effort.

This is the “[Nebraska guy problem](https://xkcd.com/2347/)” in action: software used by a large part of the industry, sustained by a very small number of people.

Yes, anyone can fork the project (and some already did), but:

- trust doesn’t fork
- community doesn’t fork
- sustainability definitely doesn’t fork

A fork without coordination creates fragmentation without adding real value and that weakens the ecosystem. What pgBackRest needed was not a replacement, but continuity.

## The danger of bad framing

Calling the project “dead” shifted the conversation in the wrong direction. 

![blog/2026/05/Jan-pgb-not-dead.png](blog/2026/05/Jan-pgb-not-dead.png)

Instead of asking:

> how do we keep this project healthy?
> 

the discussion drifted at best toward:

> what is the strategic solution here?
> 

and more often to:

> what do we replace it with?
> 

and

> what do we name our fork?
> 

That’s a natural reaction, but it’s not a good one.

Critical infrastructure should not be treated as disposable. Doing so erodes trust in the solutions we rely on and weakens the ecosystem. These foundational pieces should be treated as a shared responsibility so that the entire community becomes stronger.

## What happened next

Behind the scenes, things moved quickly, with coordination between David and companies active in the PostgreSQL community.

![blog/2026/05/Jan-pgb-news-2.png](blog/2026/05/Jan-pgb-news-2.png)

Conversations started across companies, contributors and the wider ecosystem. The goal wasn’t to “rescue” pgBackRest, but to do something far more valuable: to restore a sustainable model around it.

This is what open source actually requires: not heroics, but coordination.

## So what’s with pgBackRest?

It's all good. Well, better.

![blog/2026/05/jan-pgb-back-cover.png](blog/2026/05/jan-pgb-back-cover.png)

The short version:

- [Multiple companies coordinated together](https://pgbackrest.org/news.html#will-continue) to [ensure continued funding and support around PgBackRest](https://www.globenewswire.com/news-release/2026/05/19/3297383/0/en/open-source-stays-open-percona-sponsors-pgbackrest-to-keep-postgresql-backups-running.html)
- Engineering effort is now being shared more broadly to expand the contributor and maintainer base
- Discussions around longer term sustainability and governance in the PostgreSQL ecosystem accelerated significantly
- **Percona** played an active role in coordinating these efforts, contributing engineering resources, and helping bring organizations together around a sustainable path forward


![blog/2026/05/Jan-pgb-news-3.png](blog/2026/05/Jan-pgb-news-3.png)

The project was never closed.

## The way (forward) is open

pgBackRest’s situation is not unique. It’s a signal.

![blog/2026/05/Jan-pgb-back.png](blog/2026/05/Jan-pgb-back.png)

The PostgreSQL ecosystem depends on a wide range of tools that don’t have the same visibility, or funding, as the database itself. That gap is becoming harder to ignore.

There’s growing alignment on a few things:

- sustainability needs to be intentional
- funding needs to be easier to organize
- engineering effort needs to be shared

Whether that leads to an umbrella foundation or another model, one thing is clear: the ecosystem needs structures that support both users and maintainers.
