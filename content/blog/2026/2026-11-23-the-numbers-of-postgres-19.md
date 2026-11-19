---
title: "The numbers of Postgres 19"
date: "2026-11-23T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_zsolt']
categories: ['PostgreSQL']
authors:
  - zsolt_parragi
images:
  - blog/2026/11/pg19-numbers.png
---


After talking about the [reverts](https://percona.community/blog/2026/10/15/apologies-for-delaying-postgres-19/) and then the [remaining features](https://percona.community/blog/2026/11/20/whats-left-in-postgres-19/) of PostgreSQL 19, I want to talk about another important aspect:
the statistics of the development cycle.

This blog post is also somewhat of an announcement: [hackorum.dev](https://hackorum.dev) now has a [new, extensive statistics page](https://hackorum.dev/stats).

Most of the data here comes from two of those pages:
the [PG19 page of the per-release statistics](https://hackorum.dev/stats/releases/19) and the [release-over-release](https://hackorum.dev/stats/trends/releases) view.

My goal isn't to blindly repeat the information already available there -- if it were, this blog post could end here.
Instead, I want to focus on two topics visible in the data:
mostly on how PG19 was different from the previous releases, but also on how, even without this outlier, PostgreSQL development is changing rapidly, and people will have to pay attention and adjust.

# The elephant in the room

Many metrics either stay mostly the same over the releases, or follow a linear change.
For example, we can see that the number of patch submissions follows a clearly linear increase from 11 to 19:

![Patch submissions per release, growing from 3,251 in PG11 to 8,478 in PG19](blog/2026/11/pg19-numbers-patch-mails.svg)

However, even on the release-over-release summary page, we can see that something seems off with 19.
For example, let's look at two other series, the number of commits and the number of changed lines in the commits:

![Commits per release, between 1,990 and 2,818 from PG11 to PG18, then 3,787 in PG19](blog/2026/11/pg19-numbers-commits.svg)

With commits, we can clearly see a slowly increasing trend over many releases: we went from slightly below 2000 in PG13 to 2818 in PG18, mostly following a line.

And then in 19, we see 3787.

The difference between 18 and 19 is bigger than the difference between 13 and 18.

![Lines changed per release, between 630K and 850K from PG11 to PG18, then 1.13M in PG19](blog/2026/11/pg19-numbers-lines-changed.svg)

If we look at lines changed, it is even stranger:
even while the number of commits was increasing, the number of changed lines remained mostly stable, apart from some noise.
Something between 600 and 850 thousand.

And then PG19, with 1.1 million, nearly twice as many as 18.

To be clear, this statistic shows the sum of the individual commits, instead of the overall change.
For example, if a commit adds 5000 lines, but then gets reverted, removing those 5000 lines, in the end it changed 0 lines overall, but this method counts it as 10000.

What this means is that previously, while the number of commits increased from 2000 to 3000, the overall size of the commits remained roughly the same.
With 19, the number of commits increased by 34%, while the overall size increased by 79%.
We not only had more patches, but their average size also grew significantly.

# The bug and vulnpocalypse in numbers

Where did all this extra code go?
Was it all ambition, trying to get way more features in than usual?

Partly, yes: the original feature set of PG19 contained many big items.
But there's also another topic, one I already touched on in an earlier blog post:
coding agents got better and better, to the point where they can find many more bugs that have been there for a long time in old software such as PostgreSQL.

Let's look at some data from the release detail pages:

![Commits per month in PG18 and PG19: PG18 drops to 61 by September, PG19 stays around 200 until November](blog/2026/11/pg19-numbers-commits-per-month.svg)

The above graphs show how many commits landed per month in 18 and 19.
Instead of 18, I could have used almost any older release, they all follow the same shape.

Can you spot the difference?

The part after the feature freeze is completely different, and don't forget that for PG19, it's even longer:
the PG18 graph ends in September, the PG19 one in November.
That's 2 extra months, and November wasn't even a full month: PostgreSQL 19.0 entered code freeze on November 14!

The usual, mostly linear decrease in bugfixes simply didn't happen:
PG19 received around 200 commits every month after the feature freeze, including November, which was only half a month.
This is mostly caused by LLMs finding more and more bugs: many bug reports and bugfix patch submissions openly state that the issue was found by a coding agent.

PG19 contains 969 more commits than PG18, and even if I ignore that the graph didn't start decreasing during the summer, 612 of those were committed in the last 3 months, a period that didn't exist for 18.

![Commits also backported to older branches, 424 to 622 from PG11 to PG18, then 1,075 in PG19](blog/2026/11/pg19-numbers-backports.svg)

Another way to look at the same question is the number of backports.
PG18 had 2818 commits, and 559 of them fixed bugs in earlier releases, so they had to be backported to the stable branches.
This 500-600-ish number is a stagnating metric, it was in the same range for a very long time.

And then we have PG19, with 1075.
As a rough estimate, we can say that of those 969 extra commits, at least 400 were fixes for bugs found in older code.

# The AI flood hit the mailing list

Lastly, still focused on the differences between 19 and earlier versions, let's look at these two graphs:

![Weekly patch submissions in PG18 and PG19, split between committers and everyone else](blog/2026/11/pg19-numbers-patch-submissions-weekly.svg)

These don't show what got committed into 18 and 19, but what people proposed to include in them:
patch submissions, which the commits were selected from.

PostgreSQL has a relatively small committer team:
people with direct write access to the source code repository.
Everyone else can only get their changes in through them, they are the gatekeepers and maintainers of postgres.

In earlier releases, we can see that a significant part of the submissions came directly from committers, usually around 40% overall, and around 50% after the feature freeze.
We can also see a clear downward slope at the end: fewer and fewer submissions every week.

In 19, those numbers are different.
The overall ratio of committer-authored patches is 32%.
And it barely changed at the end:
even after the feature freeze, only 34% of the patch submissions came from committers.

While these graphs don't say which submission is AI-written and which isn't, I think we can still conclude that the same [eternal September of open source](https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/) that hit GitHub and other more mainstream sites earlier finally hit the PostgreSQL hackers list, with a slight delay.
Similarly to GitHub, PostgreSQL will have to react and adjust to this change.
So far, the ratio we can see for PG20 is even worse, barely above 30%.

# A longer trend

The open source maintenance hell, the influx of AI-generated contributions, mainly started last year, and as we can see from these statistics, in the PostgreSQL case mostly this year:
most metrics followed their usual trend before 19.

That means if we look at the number of authors, patch submitters, or active people on hackers, we'll see a big jump in PG19, right?

![Commit authors per release, around 160 to 190 until PG16, then 225, 281 and 380](blog/2026/11/pg19-numbers-authors.svg)

Not exactly. We can see a growing trend, but it actually started earlier, with PG17.
Based on the yearly view of the statistics, already in 2023, during the early part of the PG17 development.

That doesn't entirely fit the AI era, as the first generally usable coding agents started to appear in late 2024, and they had very limited usability with the PostgreSQL coding style until late 2025.

I don't know what conclusion to draw from this, other than pointing out that many graphs shown on hackorum (and even more not shown, but available in the data) suggest that there was some kind of turning point around PostgreSQL 17:
previously stagnating or slowly changing metrics started following a steeper curve.

# A slow but steady increase

Finally, I want to go back and repeat the same graph I showed at the beginning, the number of patch submissions:

![Patch submissions per release, growing from 3,251 in PG11 to 8,478 in PG19](blog/2026/11/pg19-numbers-patch-mails.svg)

It might seem that there's nothing interesting to see here: it's a slow, steady increase.
We can see the same with the number of people on the mailing lists, the number of commitfest entries, and many other graphs.

It's a simple fact: even without the significant differences in 19, or the shift visible in some metrics starting with 17, the traffic on the mailing list, and with it the workload of the maintainers, is clearly growing.

So let's look at the number of maintainers over time:

![Committers per release, between 26 and 31](blog/2026/11/pg19-numbers-committers.svg)

Or to make this even clearer, let's look at the number of received patch submissions per committer:

![Patch submissions per committer, from 125 in PG11 to 274 in PG19](blog/2026/11/pg19-numbers-patch-mails-per-committer.svg)

I don't think this needs much explanation: the workload grows, the number of maintainers barely does.
One of the most important jobs of a committer is reviewing submissions, and the number of submissions per committer is now more than twice what it used to be.

# Time for changes?

These statistics are not a one-off: most of them are already available for PG20 too, based on live data, at [hackorum](https://hackorum.dev/stats/).
I will keep updating them, making even more information available, and sharing anything else I discover in them.

At least for me, the conclusion is already clear.
PostgreSQL and its development process are known for their stability and conservatism.
That's all good, but I think the above examples from the statistics showcase the problem:
the world is changing, and PostgreSQL will have to change with it.

![A small team checking every parcel at a narrow gate, while the queue keeps growing](blog/2026/11/pg19-numbers-closing-v2.png)
