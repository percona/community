---
title: "Welcome to PGConf.EU Valencia!"
date: "2026-10-09T09:00:00+02:00"
tags: ['PostgreSQL', 'pgBackRest', 'Community', 'Conferences']
categories: ['PostgreSQL']
authors:
  - stefan_fercot
images:
  - blog/2026/09/pgconf-eu-valencia-preview.png
slug: pgconf-eu-valencia
---

[PGConf.EU](https://2026.pgconf.eu/) is right around the corner! This year, we're heading to Valencia for three days of talks on October 20-22, followed by the Community Events Day on Friday, October 23.

![PGConf.EU 2026 in Valencia](blog/2026/09/pgconf-eu-valencia-welcome.jpg)

I'm excited to get there for several reasons, and I'd like to share some of that excitement with you all :-)

## A first look behind the scenes

I'm currently serving as PostgreSQL Europe Vice-Treasurer, and this is my first time on the conference organising team. And I must say, seeing the work behind the scenes gives me a whole new appreciation for the event.

Moving to a larger conference centre, with more space and comfort for attendees, speakers and sponsors, is a real challenge. The whole team is working hard to make it a great experience for everyone.

Kudos to [everyone involved](https://2026.pgconf.eu/organisation/), especially Martin Marques, our local point of contact, who helped bring PostgreSQL Europe to Valencia!

## Let's talk about pgBackRest

Of course, I won't just be wearing my staff shirt. I also have the pleasure of presenting a talk about my beloved backup tool: [pgBackRest in HA setups: deployment patterns that work](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8238-pgbackrest-in-ha-setups-deployment-patterns-that-work/).

If you've read my blog or attended one of my talks, you probably know that backups, disaster recovery and high availability are topics I enjoy quite a bit. This time, we'll look at how to deploy pgBackRest in HA environments.

pgBackRest can fit many different setups: a dedicated backup host, backups taken from standby servers, or data sent directly to cloud storage. Yet many users only use a fraction of those possibilities. We'll explore deployment patterns and how to choose an architecture that fits your environment and recovery requirements.

The session is on Tuesday at 16:05 in Audit 2. If you're curious about the topic, come along :-)

![Stefan Fercot's talk card](blog/2026/09/pgconf-eu-valencia-pgstef-talk-card.png)

I'm especially excited because I won't be the only one talking about pgBackRest. David Steele, the project's author and lead developer, will be there too! Together with Jan Wieremjewicz from Percona, he'll present [The Monday We Learned Who Maintains Our Backups](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/7963-the-monday-we-learned-who-maintains-our-backups/), revisiting what happened in April when pgBackRest was marked as no longer maintained, and what followed.

Their session is in the same room at 14:45, in the slot before mine, with a tea break in between. A good afternoon for anyone interested in pgBackRest!

I'm also really happy to see David again. I first met him at PGConf.EU in Milan in 2019, and we haven't had many opportunities to meet at conferences in recent years. Whether you already use pgBackRest or are just considering it, Valencia will be a great place to ask questions and meet the people behind the project.

## Too many talks, too little time

With three days of talks across multiple tracks, choosing what to attend (and, inevitably, what to miss) won't be easy. Here are a few of my personal picks:

- [**Is PostgreSQL On My Raspberry Pi Faster Than Your Cloud Instance**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8058-is-postgresql-on-my-raspberry-pi-faster-than-your-cloud-instance/), by **Chris Ellis**. Chris always brings a bit of fun to his talks, so I'm always happy to attend them!

- [**Community Moments That Shaped 30 Years of PostgreSQL**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8066-community-moments-that-shaped-30-years-of-postgresql/), by **Valeria Kaplan**. PostgreSQL turned 30 this year. After attending the [roundtable retrospective at PGConf.dev](https://2026.pgconf.dev/session/670) last May, I'm curious to see which moments Valeria has chosen to share.

- [**Autovacuum Is Running. Is It Actually Working?**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8120-autovacuum-is-running-is-it-actually-working/), by **Teresa Lopes**. Everyone loves autovacuum, right? As Teresa puts it: _"The problem is not vacuum. The problem is misconfiguration."_

- [**Exercising PostgreSQL Performance Enhancing Patches**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8341-exercising-postgresql-performance-enhancing-patches/), by **Melanie Plageman**. Evaluating the performance impact of a patch is far from straightforward. I'm looking forward to learning more about how Melanie approaches it.

- [**What is Patroni, really?**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8275-what-is-patroni-really/), by **Alexander Kukushkin** and **Polina Bungina**. Have I mentioned that Patroni is my second-favourite tool? This is probably my must-attend session on Wednesday.

- [**A demo only tour through PostgreSQL 19**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/7904-a-demo-only-tour-through-postgresql-19/), by **Daniel Westermann**. Daniel expected PostgreSQL 19 to be out by the conference. His forecast looks pretty close: the release is currently [planned for October 29](https://hackorum.dev/topics/253972). Either way, a tour through live demos sounds like a fun way to start the last day of talks.

- [**Postgres Before PostgreSQL: Stories from Inside the Original Berkeley Lab**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8310-postgres-before-postgresql-stories-from-inside-the-original-berkeley-lab/), by **Ellyne Phneah**. There's always room for more PostgreSQL stories, especially when Ellyne is telling them :-)

- [**Can We Skip Recovery? The Architecture of On-Demand WAL Replay**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/7858-can-we-skip-recovery-the-architecture-of-on-demand-wal-replay/), by **Srinath Reddy Sadipiralla**. Recovery is a topic I keep coming back to. I'm always curious to hear different approaches and explore what might be improved.

- [**Identifying bottlenecks in Postgres workloads**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8186-identifying-bottlenecks-in-postgres-workloads/), by **Andres Freund**. From my years as a DBA and PostgreSQL consultant, I know how much time can go into finding the actual bottleneck. I'm looking forward to hearing how Andres approaches that investigation.

- [**What Actually Goes Wrong with Postgres on Kubernetes**](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/8319-what-actually-goes-wrong-with-postgres-on-kubernetes/), by **Natalia Marukovich**. Running PostgreSQL on Kubernetes comes with its own challenges. I'm interested in hearing about the things that go wrong and what we can learn from them.

And those are only a few highlights! Check the [full schedule](https://www.postgresql.eu/events/pgconfeu2026/schedule/) and pick yours.

Of course, I'll also try to leave some time for what is, in my opinion, the most important track: the hallway track ;-) Catching up over coffee, asking a question after a session, or discussing an unexpected problem is a big part of why I enjoy these technical events. Tuesday evening's _PostgreSQL Europe Reception_ will be another opportunity to continue those conversations.

## A day for the wider community

Friday, October 23, is dedicated to the [Community Events Day](https://2026.pgconf.eu/community-day/). Now in its second edition, it brings together events led by community members, with room for broader discussions about PostgreSQL and its ecosystem.

One discussion particularly close to my heart is **"A Postgres Ecosystem Foundation?"**

We rely on so many projects around PostgreSQL to operate our databases, connect our applications and extend what the database can do. I feel that bringing this wider ecosystem together could help both the people maintaining those projects and the users trying to find their way through it.

The road towards a foundation may be long and winding, but I'm looking forward to discussing what it could achieve and how we might get there.

## Meeting my new colleagues, too

Having recently joined Percona, I have another reason to look forward to Valencia: many of my new colleagues will be there.

I'm excited to meet them in person, spend time together during our planned team meetings and activities, and catch up around the sponsor booth. [Percona is a Gold Sponsor](https://2026.pgconf.eu/sponsors/), so we'll have a stand at the conference. I've also heard there will be plenty of stickers... 🤫

## See you in Valencia!

If you haven't decided to join yet, have I convinced you? And if you'd like to explore the city beyond the conference venue, the website has a [things to do in Valencia](https://2026.pgconf.eu/things-to-do/) section too. So many good reasons to make the trip :-D

I'm looking forward to seeing familiar faces and meeting plenty of new people. Between organising duties, talks and the Percona booth, I might be moving around quite a bit, but don't hesitate to come and say hi if you catch me!
