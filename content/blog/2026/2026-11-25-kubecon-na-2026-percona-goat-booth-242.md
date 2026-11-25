---
title: "KubeCon NA 2026: The Percona Goat at Booth 242"
date: "2026-11-25T00:00:00+00:00"
tags: ['cloud', 'kubernetes', 'events', 'operators']
categories: ['community', 'cloud']
authors:
  - george_kechagias
images:
  - blog/2026/11/kubecon-na-2026-team-photo.jpg
---

Just got home from KubeCon + CloudNativeCon North America 2026 in Salt Lake City, and what a week it was! At Percona, everything we do starts with our community and our users, and KubeCon is one of the best places to meet them in person. If you walked past booth 242, you couldn't miss us: a crew in neon yellow shirts, a life-size mountain goat in a Percona scarf, and a banner promising "Making databases on Kubernetes boring since 2018."

Here's how the week went, in the order the camera roll tells it.

## Monday: setup, and the goat arrives

The hall was still half cardboard when we got in on Monday. Before the monitors were up or the shirts unpacked, the most important piece of booth equipment came out of its box: a life-size mountain goat, the unofficial mascot of a KubeCon in Utah.

![The mountain goat unboxed at the Percona booth during setup](blog/2026/11/kubecon-na-2026-goat-setup.jpg)
*Setup day. Priorities.*

He'd spend the rest of the week wearing a Percona scarf and making friends across the expo floor.

That evening Kate Obiidykhata gave the first Percona talk of the week, a lightning talk at LearnKube Day.

![Kate Obiidykhata speaking at LearnKube Day](blog/2026/11/kubecon-na-2026-kate-learnkube.jpg)

## Tuesday: doors open

Tuesday morning the welcome banner was up, badge pickup had a queue, and the expo hall opened.

![KubeCon + CloudNativeCon North America 2026 welcome banner](blog/2026/11/kubecon-na-2026-welcome.jpg)

We were in the neon yellow Percona shirts, which made us easy to find and impossible to miss in photos.

![The Percona team in neon yellow shirts at booth 242](blog/2026/11/kubecon-na-2026-booth-shirts.jpg)

Nothing makes us happier than contributors to our open source operators coming by to say hi.

At the booth we ran "Databases on K8s. Solved live.", a set of live demos built together with [Solanica](https://solanica.io) and [Coroot](https://coroot.com). Short animations showed what the Percona Operators do for you, from multi-region replication and volume resizing to a PostgreSQL 17 to 18 blue/green upgrade, snapshot backups and encryption with a single `kubectl apply`. Then the live part: Percona Monitoring and Management staying healthy through a node loss, Coroot tracing a failing service back to its Postgres and Valkey dependencies, and [OpenEverest](https://openeverest.io) running PostgreSQL, MySQL and Valkey side by side in one UI.

![Live demo screens at the Percona booth](blog/2026/11/kubecon-na-2026-demos.jpg)
*The booth demos, guarded by the "kubectl delete stress --all" hoodie.*

Later that afternoon I gave a lightning talk, Closing the Gap Between Ready and Usable in a DBaaS Platform, at the booth of the [CNCF Platform Engineering Technical Community Group](https://cloudnativeplatforms.com). Thanks to the community for hosting the lightning talks! The slides are [on GitHub](https://github.com/gkech/presentations/tree/main/kubecon-na-2026-ready-vs-usable-slides).

![George Kechagias giving a lightning talk at the Platform Engineering booth](blog/2026/11/kubecon-na-2026-lightning-talk.jpg)
*Ready is a promise the platform makes. Lightning talk at the Platform Engineering booth.*

Tuesday evening Valkey and Percona hosted After Hours Drinks and Networking at Lake Effect. The cocktail list had a Thor and an Odin on it, which tells you someone on the events team had fun with the menu.

![Cocktail menu for the Valkey and Percona after-hours event](blog/2026/11/kubecon-na-2026-cocktail-menu.jpg)

![Attendees talking at the after-hours event at Lake Effect](blog/2026/11/kubecon-na-2026-after-hours.jpg)

## Wednesday: breakfast with Percona and Valkey

Wednesday started early with Breakfast with Percona & Valkey. Round tables, coffee, and people who actually run these systems comparing notes before the hall opened.

![Breakfast with Percona and Valkey welcome screen](blog/2026/11/kubecon-na-2026-breakfast-screen.jpg)

![Attendees at round tables during the breakfast](blog/2026/11/kubecon-na-2026-breakfast-tables.jpg)

Back on the floor, the goat went visiting. He found SUSE's Geeko and they got along fine.

![The Percona goat meeting SUSE's Geeko](blog/2026/11/kubecon-na-2026-goat-geeko.jpg)

By lunch the whole crew was at the booth for a photo, goat included, plus the sign that summed up a lot of our conversations: "GitOps runs my databases now."

![The Percona team with the goat at booth 242](blog/2026/11/kubecon-na-2026-team-photo.jpg)

## The conversations

There's nothing like chatting with our users in person and hearing their feedback firsthand. A lot of people stopped by with their own setups and real questions, and we got to dig into them together right there at the booth. Some were already running our operators, some were in the middle of a proof of concept, and some were just starting to think about moving their databases to Kubernetes. Every team's path with their databases looks different, and wherever they are on it, we at Percona are here to help them get the best out of their databases.

Setting up and running Postgres on Kubernetes came up in almost every conversation, with MongoDB and Valkey close behind. We also talked about what's new in Kubernetes itself, like in-place pod resize and volume snapshots, and how databases running on it can make use of them. And we got to share recent and upcoming developments in the Percona Operators, and to hear our users' suggestions for what we should build next. Those ideas are already on their way to the team, so if you shared one with us, keep an eye on our [public roadmap](https://github.com/percona/roadmap). Or better yet, contribute to the operators yourself by opening a GitHub issue or sending a PR.

## Thursday: last day

We packed up booth 242 with one last team photo.

![The Percona team's last photo at booth 242](blog/2026/11/kubecon-na-2026-last-day.jpg)

I feel so lucky to be part of the amazing Cloud Native team at Percona, building open source database software for our users. A big thank you to the Percona Community team, especially Laura Czajkowski and Kyle Flanagan, for making the week happen.

Thanks also to everyone who stopped by, asked us something hard, took a hoodie, or got their passport stamped. If we promised you a follow-up, it's coming. And if you didn't make it to Salt Lake City, the operators are all on GitHub: [PostgreSQL](https://github.com/percona/percona-postgresql-operator), [MongoDB](https://github.com/percona/percona-server-mongodb-operator), [MySQL based on Percona XtraDB Cluster](https://github.com/percona/percona-xtradb-cluster-operator) and [MySQL based on Percona Server for MySQL](https://github.com/percona/percona-server-mysql-operator).
