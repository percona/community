---
title: "Open Door MongoDB Chats"
date: "2024-03-26T00:00:00+00:00"
draft: false
tags: ["MongoDB", "Backups", "Percona", "Events"]
categories: ['MongoDB']
authors:
  - edith_puclla
images:
  - blog/2024/03/mongodb-open-doors.png
---

Let’s talk about MongoDB!
This week, **Jan Wieremjewicz**, Senior Product Manager, and **Michal Nosek**, Pre-Sales Enterprise Architect at [Percona](https://www.percona.com/), made two series of videos covering basic to advanced concepts in **MongoDB** and **backups**.
<br />
<br />
Le’s explore them together!

## Enterprise Scale Backups for MongoDB with Open Source Software

In the first video about enterprise-scale backups for MongoDB using open-source software, Jan and Michal discuss the challenges and solutions associated with backing up large datasets in MongoDB. They explore the difficulties of managing backups and restorations for huge data sizes, emphasizing the limitations of logical backups like **mongodump** and **mongorestore**, which can be time-consuming for large datasets.

They also highlight alternative solutions, including MongoDB Enterprise licenses offering robust backup tools, the use of storage-level snapshots, and [Percona's own backup solution for MongoDB](https://docs.percona.com/percona-backup-mongodb/index.html). This solution aims to simplify and speed up the backup and restoration process, especially for large, sharded clusters, and is designed to be efficient and flexible, preventing vendor lock-in and helping with enterprise needs.

The video covers the technical aspects of ensuring consistent, performant backups across complex database architectures. I recommend you watch the video because it covers basic topics from an expert viewpoint.

<br />
<iframe width="560" height="315" src="https://www.youtube.com/embed/sO-43bxaf7k?si=zgjHA6otYTmhBtYp" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Optimize the RPO and RTO for your MongoDB Backup Strategy

In this second episode of their discussion on **MongoDB backups**, Jan and Michal explore the critical aspects of developing a comprehensive backup strategy, focusing on **Recovery Point Objective(RPO)** and **Recovery Time Objective (RTO)**. They highlight the importance of these concepts in determining the acceptable amount of data loss and system downtime in the event of a failure. Michal explains that achieving a near-zero RPO requires significant investment, while Jan highlights the importance of documenting a backup strategy for job security and organizational awareness.

They also discuss the common oversight among smaller organizations that lack a formal backup strategy, often due to the perceived cost or a lack of major failures. The conversation covers the necessity of regularly testing backups and restore times, as well as communicating the current backup and recovery capabilities to higher management to align expectations with business criticality. This approach ensures transparency and preparedness for potential system failures, making it an essential practice for companies of all sizes.

<br />

<iframe width="560" height="315" src="https://www.youtube.com/embed/kAyGieor0Q0?si=KB_BGfyjNiCYe624" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Read our latest article titled [Using Percona Backup for MongoDB in Replica Set and Sharding Environments: Part One](https://www.percona.com/blog/using-percona-backup-for-mongodb-in-replica-set-and-sharding-environment-part-one/)

For more information, visit the official [Percona Backup for MongoDB website](https://www.percona.com/mongodb/software/percona-backup-for-mongodb). If you have any questions, feel free to visit our forum under the MongoDB category.
