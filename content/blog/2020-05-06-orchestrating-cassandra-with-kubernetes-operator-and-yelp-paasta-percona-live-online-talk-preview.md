---
title: 'Orchestrating Cassandra with Kubernetes Operator and Yelp PaaSTA - Percona Live ONLINE Talk Preview'
date: Wed, 06 May 2020 19:42:03 +0000
draft: false
tags: ['raghu.prabhu', 'Events', 'Kubernetes']
authors:
  - raghavendra_prabhu
images:
  - blog/2020/05/Social-PL-Online-2020-1.jpg
slug: orchestrating-cassandra-with-kubernetes-operator-and-yelp-paasta-percona-live-online-talk-preview
---

_[Percona Live Online](https://www.percona.com/live/conferences) Agenda Slot: Tue 19 May • New York 3:00 p.m. • London 8:00 p.m. • New Delhi 12:30 a.m. (Wed)_ _Level: Intermediate_

### Abstract

At Yelp, Cassandra, our NoSQL database of choice, has been deployed on AWS compute (EC2) and AutoScaling Groups (ASG), backed by Block Storage (EBS). This deployment model has been quite robust over the years while presenting its own set of challenges. To make our Cassandra deployment more resilient and reduce the engineering toil associated with our constantly growing infrastructure, we are abstracting Cassandra deployments further away from EC2 with Kubernetes and orchestrating with our Cassandra Operator. We are also leveraging Yelp’s PaaSTA for consistent abstractions and features such as fleet autoscaling with Clusterman, and Spot fleets, features that will be quite useful for an efficient datastore deployment. 

In this talk, we delve into the architecture of our Cassandra operator and the multi-region multi-AZ clusters it manages, and strategies we have in place for safe rollouts and zero-downtime migration. We will also discuss the challenges that we have faced en route and the design tradeoffs done. Last but not least, our plans for the future will also be shared.

### Why is your talk exciting?

The talk not only delves into the architecture of Yelp's Cassandra deployment on Kubernetes, and the operator but also the various challenges that we encountered and our approaches to them.  We also talk about how we have integrated this operator with our own PaaS (Platform-as-a-Service) called PaaSTA, and leveraged capabilities such as Spot fleets and Clusterman for significant savings in cloud costs.

### Who would benefit the most from your talk?

Attendees interested in stateful deployments - databases, streaming pipelines - on Kubernetes and orchestration systems in general, should find this talk interesting. Also, anyone using existing Kubernetes operators or planning on writing an operator should benefit from this talk.

### What other presentations are you most looking forward to?

Among talks on [the full agenda,](https://www.percona.com/live/percona-live-online-full-agenda) I am looking forward to the State of Open Source Databases from Peter Zaitsev to get a snapshot of the current trends and technologies in the database world. Lefred’s talk on the State of the Dolphin should be similarly helpful in keeping up with the state of MySQL which is a rapidly growing project. Finally, given our current focus on databases and Kubernetes, I am also looking forward to Comparison of Kubernetes Operators for MySQL and A Step by Step Guide to Using Databases on Containers talks from Percona and AWS respectively.