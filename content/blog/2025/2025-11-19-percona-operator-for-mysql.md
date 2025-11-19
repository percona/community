---
title: "Percona Operator for MySQL Is Now GA, More MySQL Options for the Community on Kubernetes"
date: "2025-11-19T11:00:00+00:00"
tags: ['MySQL', 'Opensource', 'Cloud', 'Kubernetes', 'Operators']
categories: ['PostgreSQL']
authors:
  - edith_puclla
images:
  - blog/2025/11/init.png
---

We’re excited to share that the new **[Percona Operator for MySQL (based on Percona Server for MySQL)](https://docs.percona.com/percona-operator-for-mysql/ps/index.html)**  is officially in General Availability (GA)!


This release introduces native **MySQL Group Replication** support for **Kubernetes**, providing our community with another open-source option for running reliable, consistent MySQL clusters at scale.

This is about more choices for the community. Each MySQL replication technology addresses different real-world needs, and now you can choose the one that best fits your workloads.


![MySQL Operator for MySQL Intro](blog/2025/11/introm.jpeg)

## What This Means for the Community

With this release, Percona now supports two **fully open-source MySQL Operators**:

### 1. [Percona Operator for MySQL (Percona Server for MySQL)](https://docs.percona.com/percona-operator-for-mysql/ps/index.html), New and GA

  - Group Replication (synchronous)
  - Asynchronous replication (Technical Preview)
  - Native MySQL experience
  - Auto-failover
  - Kubernetes-native design

### 2. [Percona XtraDB Cluster Operator (PXC)](https://docs.percona.com/percona-operator-for-mysql/pxc/index.html)

  - Galera-based synchronous replication
  - Strong high availability
  - Auto-failover
  - Battle-tested for mission-critical workloads

**These Operators complement each other; they are not replacements**. They give users the freedom to choose the right replication model for their business and technical priorities.

*This GA release is a step in that direction,  and we will continue publishing technical blog posts to explain when to use each Operator, how Group Replication works, and how this all fits into real-world Kubernetes environments*.


![MySQL Operator for MySQL Intro Chart](blog/2025/11/two-operators.png)


## Call for Community Testing and Feedback

Asynchronous replication is now available in Technical Preview, we invite you to:
- Test it in your clusters
- Share your feedback
- Open GitHub issues
- Contribute docs or examples

Your feedback will guide the next features we bring to the Operator.

### Explore Percona Operator for MySQL:

- [Docs Percona Operator for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/ReleaseNotes/Kubernetes-Operator-for-PS-RN1.0.0.html)
- [GitHub: Try it, test it, open issues, or contribute](https://github.com/percona/percona-server-mysql-operator)
- [Announcement Percona Blog](https://www.linkedin.com/posts/percona_the-percona-cloud-native-team-is-happy-activity-7396585512536473600-bFZR/?utm_source=share&utm_medium=member_ios&rcm=ACoAAA_uTn0BQWSwnqQ-mUMcVZ7icaVGYa4mlVs)