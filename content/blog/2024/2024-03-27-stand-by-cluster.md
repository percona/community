---
title: "Creating a Standby Cluster With the Percona Operator for PostgreSQL"
date: "2024-03-27T00:00:00+00:00"
draft: false
tags: ["PostgreSQL", "Backups", "Percona"]
categories: ['PostgreSQL', 'Cloud']
authors:
  - edith_puclla
images:
  - blog/2024/03/standby.png
---

In this video, [Nickolay Ihalainen](https://www.linkedin.com/in/nickolay-ihalainen-b8a35838/?originalSubdomain=ru), a Senior Scaling Specialist at Percona Global Services, explains how to set up replication with standby clusters for Kubernetes databases using Percona's open-source tools, including the [Percona Operator for PostgreSQL](https://www.percona.com/postgresql)

A **Standby Cluster** is a backup version of your main database. It's there to keep your data safe and make sure your database can keep running even if something goes wrong with the main one.

![Percona Demo for StandBy Cluster](blog/2024/03/standby.png)

For this demo, we use **Percona Operators for PostgreSQL** to create the clusters, which facilitates high availability setups and database management by automating deployment, scaling, and management tasks within Kubernetes environments.

Nickolay created a primary node and the configuration of replication to standby clusters for PostgreSQL, ensuring data redundancy and availability. This primary node has two standby databases in the same primary node.

Then, we have the **object storage (S3)** for backups, highlighting the importance of having offsite backups in different geographical locations to safeguard against data loss. This is where the primary node will access to make a data replication.

This demo also includes using **Patroni** to manage this process, enabling replication and failover between primary and standby servers, and **PgBouncer**, a tool that manages how applications are aligned to communicate with a PostgreSQL database.

Watch our complete hands on in this YouTube video:

<br />

<iframe width="560" height="315" src="https://www.youtube.com/embed/nqeGvvZ5G5Y?si=n3ho7xHJiT6F8u9v" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

You can find more instructions on how to [deploy a standby cluster for Disaster Recovery](https://docs.percona.com/percona-operator-for-postgresql/2.0/standby.html), and also you can [Create a Standby Cluster With the Percona Operator for PostgreSQL](https://www.percona.com/blog/creating-a-standby-cluster-with-the-percona-distribution-for-postgresql-operator/).

Is you have questions o feedback, write to us in our [Percona Comunity Forum](https://forums.percona.com/)
