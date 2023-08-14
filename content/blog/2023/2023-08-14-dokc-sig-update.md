---
title: "DoKC Operator SIG Update"
date: "2023-08-14T00:00:00+00:00"
draft: false
tags: ["dok", "kubernetes", "sig", "operators"]
authors:
  - edith_puclla
images:
  - blog/2023/08/dok-game.png
slug: dokc-operator-sig-update
---

Before our meeting, we started with a question to begin the morning: **What board game or tabletop game have you played that you would recommend to others?**

[Itamar Marom](https://www.linkedin.com/in/itamar-marom/) suggests that Catan as a good board game, which takes a lot of time, super annoying when you lose, but generally a lot of fun. So highly suggested!

Other members like [Hugh Lashbrooke](https://www.linkedin.com/in/hugh-lashbrooke/) and [Robert Hodges](https://www.linkedin.com/in/berkeleybob2105/) prefer Monopoly, where you must reach a higher level of monopoly awareness to enjoy it fully. The idea is that you can make pretty much any deal with anyone else within the rules of monopoly. That's when it gets fun.

Terraforming Mars and Meadow are other favorite games for members of DoK.

![dokc-game](blog/2023/08/dok-game.png)

Let's get into our agenda for this meeting.

For **our first agenda**, [Itamar Marom](https://www.linkedin.com/in/itamar-marom/) (From AppsFlyer and DoKC Ambassador) proposes joining more data operators' maintainers and developers in the community.

Itamar was analyzing the data technology map and saw that some workloads are very common and act differently from what is found in SIG Operator (Special Interest Group) in the case of Spark and Kafka. It would be nice to see the maintainers and hear their opinions, especially in meetings like our one with Google, where they have very different and exciting use cases.

We've had folks from these communities present at our virtual meetups. Bringing them to the SIG to learn, share, and find ways to collaborate would benefit the broader DoK ecosystem.

![dokc-game](blog/2023/08/kafka-spark.png)

[Jim Halfpenny](https://www.linkedin.com/in/jimhalfpenny/) from **Stackable** mentions that they have several operators for open source projects, including Apache Kafka, Apache NiFi, Apache Superset, Trino, and more. And they will love input from the community on the direction the operators should take. His aim is that our operators should play nicely with others!

[Melissa Logan](https://www.linkedin.com/in/mklogan/) was part of several discussions with the Argo community, and maybe there's a chance they could join us as well.

Itamar will prepare a proposal for this project in which the group can collaborate and will share it soon.

The **second item on our agenda** was **Carrier Hardening and Security Project** Update by [Robert Hodges](https://www.linkedin.com/in/berkeleybob2105/) (DoKC Ambassador).

This project is a guide to establishing a baseline for secure data management on Kubernetes by fortifying the database operators. The guide aims to identify the typical attack surfaces that exist for databases running on Kubernetes. It will establish a collection of best practices for enhancing their security using operators.

Robert is working on an August 12 talk at [DataConLA](https://www.dataconla.com/) on the topic: Tips for Sleeping Well with State-of-the-Art Data Management. It will contain the framing of the operator hardening guide.

Robert is playing around with a couple of approaches to divide up the problem space. One of them is to deal with security concerns as follows:

1. The database itself - E.g., setting passwords safely.
2. Kubernetes - Security it from outside attackers - E.g., encrypted client connections.
3. Data outside Kubernetes - Object storage used for backups, logs forwarded to log management systems.

![dokc-game](blog/2023/08/dataconla.png)

Robert Will share a draft of the talk in the **#sig-operator** channel for discussion.

The last topic on our agenda is ArgoCD and general CI/CD compatibility for operators by Robert Hodges.

![dokc-game](blog/2023/08/argo.png)

Robert created a public repository [Argocd-examples-clickhouse](https://github.com/Altinity/argocd-examples-clickhouse), example of ArgoCD application definitions for ClickHouse analytic applications.

In this project, you'll find ArgoCD applications and instructions to stand up a full analytic stack based on ClickHouse in a Kubernetes cluster.

Following suggestions from community members, a new Slack channel #topic-devops was created 🎉 .
This is a channel to talk about CI/CD integration, specific solutions like ArgoCD & Flux, etc.

To learn more about our meetings, join the [Data on Kubernetes](https://dok.community/). An Open Community for Data on Kubernetes. We host weekly live meetups where technologists share their stories, wisdom, and practical advice for running data on Kubernetes.
