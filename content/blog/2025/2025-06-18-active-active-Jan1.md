---
title: "PostgreSQL active-active replication, do you really need it?"
date: "2025-06-18T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2025/06/jan-aa1-cover1.jpeg
---

## Before we start, what is active-active?

**Active-active**, also referred to as **multi-primary**, is a setup where multiple database nodes can accept writes at the same time and propagate those changes to the others. In comparison, regular streaming replication in PostgreSQL allows only one node (the primary) to accept writes. All other nodes (replicas) are read-only and follow changes.

In an active-active setup:

  * There is no single point of write.
  * Applications can write to any node.
  * The database needs a way to sort out conflicts when two nodes try to concurrently change the same data.

That last point is the hardest one. PostgreSQL was not designed for concurrent writes from multiple nodes; it's not a distributed database and does not leverage proprietary dedicated storage capabilities. So, every multi-primary implementation has to solve the issue of conflicting concurrent writes somehow. Some resolve conflicts using timestamps or priorities. Some push conflict resolution to the application. Some avoid it altogether by writing to separate subsets of data.

While simple in concept, implementing an active-active configuration is challenging.


## pgactive to the rescue?

Last week, Amazon [open-sourced its active-active replication extension](https://aws.amazon.com/about-aws/whats-new/2025/06/open-sourcing-pgactive-active-active-replication-extension-postgresql/), pgactive ([https://github.com/aws/pgactive](https://github.com/aws/pgactive)). While [the extension has been generally available on AWS RDS since October 2023](https://aws.amazon.com/about-aws/whats-new/2023/10/pgactive-active-active-replication-extension-postgre-sql-amazon-rds/), there are unfortunately not many stories about it being used in production available. To be fair, I was not able to find any 😟

We often see both users and customers come asking for active-active or multi-master. These terms, while different, are so often used as synonyms that we've come to expect that. So, though I understand that every multi-master is active-active but not necessarily the other way around, for the sake of clarity, if I use one or the other term throughout this post, they will refer to the same concept.

As it is an open-source extension now, it immediately raised my interest. It seems that it could cover this ask from users I often speak with about their pains and needs. As a product manager, when I hear an ask, I always try to understand the reasons—whether it is a requirement, a need, or actually a solution that addresses one. For multi-master, my strong opinion is that it is a solution.


## Key question: do you need it?

I like the opening of [the talk Johnathan Katz gave on PGConf Europe 2023 in Prague](https://www.youtube.com/watch?v=Es9ZNbgVUsc):

> The first thing I always say on the journey to active active is: do you really need it? Because it definitely solves a lot of problems (…) but it’s very hard to manage.

That is exactly the first question I ask when I hear someone asking for active-active. We have seen teams introduce active-active replication for the wrong reasons. Here I have to pause. Yes, as database experts, we have strong opinions about what are the right reasons for using multi-master. It’s not a silver bullet. It's not "cool infra." And using it without a good reason tends to hurt for a long, long time.

So, what are the reasons to use active-active? I do not claim to be able to cover all scenarios, but I hope this post raises enough eyebrows and sparks enough discussion to eventually have solid reading material for anyone considering active-active that will help them make an informed decision.


## What are “good” reasons?

These are some of the situations where active-active might actually make sense. While there may be more, here’s my top 5:

1.  **Business continuity across regions: extreme HA needs (99.999% uptime)**

    Just to remind everyone what 5 nines mean, I will refer you to [this message](https://x.com/BenjDicken/status/1925946372034802097):

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">uptime → max monthly downtime:<br><br>99% → 7.3 hours<br>99.9% → 44 minutes<br>99.99% → 4 minutes<br>99.999% → 26 seconds<br>99.9999% → 3 seconds<br>99.99999% → 1/4 second<br><br>where do you land?<br>how much time/money would you invest to add a 9?</p>&mdash; Ben Dicken (@BenjDicken) <a href="https://twitter.com/BenjDicken/status/1925946372034802097?ref_src=twsrc%5Etfw">May 23, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

    26 seconds of downtime a month, that’s 312 seconds a year. Yes, 5.2 minutes a year.

    Now think about the cost of delivering that sort of reliability. I find [this Wikipedia page](https://en.wikipedia.org/wiki/High_availability) surprisingly helpful in conveying how little time for maintenance and failures is left with enough nines added.

    Consider what it would take to absorb failures across data centers or cloud regions without rejecting writes or failing over manually. Active-active can help here because failover becomes instant and transparent; write traffic just shifts to surviving nodes.

    But again, the cost will match the ambition. Do you plan HA within the same server room with separate power and networking? Or are you aiming for full geographic separation, to stay online even during a [country-wide outage](https://euromed-economists.org/countrywide-power-outages-across-spain-and-portugal-what-happened-and-why/#gsc.tab=0)? These decisions massively influence the architecture, and together with your uptime goals, they define the cost. At this level, every part of the solution should reflect real business needs, because every layer of complexity adds expense. You can't overstate the value of planning and proper analysis when building systems like this.

2.  **Write availability during regional failures**

    If your business serves a global customer base and absolutely must accept writes in more than one region, for example, to maintain uptime guarantees or continue operating during a regional outage, then active-active might be the least painful of the painful options.

    This is not about low latency. This is about keeping write traffic flowing even when something breaks. That includes:

    * **Cloud infrastructure outages**, such as full region loss or core service failure from your cloud provider:
      * [AWS us-east-1 outage in June 2023](https://www.crn.com/news/cloud/aws-outage-downs-other-websites-apps) affected 104 services. A [Parametrix Insurance report](https://assets-global.website-files.com/64b69422439318309c9f1e44/6554bcf27d66c0c9135d3509_Parametrix%20Insurance-%20Cloud%20Outage%20and%20the%20Fortune%20500%202023.pdf) estimated a 24-hour outage in this region could lead to $3.4 billion in direct revenue loss.
      * [Google Cloud outage in June 2025](https://apnews.com/article/18ad53dca0385a83ca5a4e219bcb3a9d) impacted Spotify, YouTube, Twitch, and others.
      * [AWS S3 outage in 2017](https://aws.amazon.com/message/41926/) was caused by an internal mistake and [disrupted GitHub, Slack, and more](https://www.theregister.com/2017/03/01/aws_s3_outage/).

        <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Joys of the <a href="https://twitter.com/internetofshit?ref_src=twsrc%5Etfw">@internetofshit</a> - AWS goes down. So does my TV remote, my light controller, even my front gate. Yay for 2017.</p>&mdash; Brian (@Hamster_Brian) <a href="https://twitter.com/Hamster_Brian/status/836666914344611841?ref_src=twsrc%5Etfw">February 28, 2017</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

    * **Name resolution and routing issues**, such as DNS or BGP failures that take your services offline even when your backend is healthy:
      * [Dyn DNS attack in 2016](https://www.thedailybeast.com/massive-internet-outage-disrupts-services-for-google-amazon-and-more) brought down Twitter, Reddit, and Spotify.
      * [Facebook DNS and BGP misconfiguration in 2021](https://blog.cloudflare.com/october-2021-facebook-outage/) made their domains unreachable and left millions of users in the dark.
      * That day, Twitter (rest in peace) [greeted the internet](https://www.aljazeera.com/news/2021/10/5/hello-everyone-twitter-pokes-fun-at-facebook-owned-app-outage):

        ![Twitter](blog/2025/06/twitter1.jpeg)

    All jokes aside, these are serious risks. If this kind of failure is unacceptable for your business, and you are willing to take on the operational weight and cost (we will get to that), active-active may be the right tool.

    But be honest about what you are solving. If your system demands strong consistency, every transaction still needs coordination across nodes. For example, if a user in Australia writes to a local node, and the other node is in the United States, that write still involves a round trip to the United States before it can commit. That round trip adds latency, not removes it. While it may be 150-200ms on average for the Australia to USA round trip, it adds up with volume.

    The real benefit of active-active here is not performance. It is write availability during failure. If your business cannot afford to reject writes when a region goes dark, and you are prepared for everything else that comes with this decision, this might be one of the rare cases where active-active makes sense.

    Just be clear, what you are solving here is not distributed latency, but write continuity when something fails.

3.  **Migrating legacy architectures**

    If you're part of an organization moving away from systems like Oracle RAC or GoldenGate, where distributed write semantics were either built-in or at least promised, you may face business or political pressure to deliver "the same thing" on PostgreSQL.

    In these cases, active-active might be the shortest path to satisfying the checkbox. But it’s almost always a transitional compromise, not the destination. As any compromise, that's not going to be all pleasant. The technically better (but less politically correct) move is usually to re-architect for clearer ownership of writes and better separation of concerns.

    If you can push for that path, do it. If not, be aware of the cost you’re inheriting.

4.  **Application performance (not database performance)**

    In the end, what you are really trying to improve is not the database throughput, but the end-user experience. Active-active may be worth considering not for improving database internals, but for reducing perceived latency in globally distributed apps or smoothing responsiveness during network transitions.

    In rare cases, this might justify active-active if the application can route users to their nearest region and issue local writes. But your app must be built for it. Deterministic conflict handling, [idempotency](https://serverlessland.com/event-driven-architecture/idempotency), and careful session management are must-haves in such a case.

    If your database is fast, but the user still feels lag because the write travels halfway across the planet, active-active might help. But this should be a last resort, not a default choice.

5.  **Local HA in disconnected or semi-connected environments**

    In edge computing, retail stores, ships, or military use cases, you might want each node to function independently to address intermittent connectivity. In such scenarios, you will still be able to write locally when the network is not available. When the network comes back, the changes are going to be synced. While conflict avoidance may be the strategy you go for, in the end, it’s going to become a cost of conflict resolution.

## What's next?

In the next blog post I will focus on the bad reasons to consider active-active replication and on the cost that should not be forgotten. Stay tuned!
