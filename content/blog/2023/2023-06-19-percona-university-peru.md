---
title: "Percona University in Peru 2023"
date: "2023-06-20T00:00:00+00:00"
draft: false
tags:
  [
    "percona",
    "university",
    "peru",
    "kubernetes",
    "peterinperu",
    "operators",
    "databases",
  ]
authors:
  - edith_puclla
images:
  - blog/2023/06/pup-all-10.jpeg
slug: percona-and-data-on-kubernetes-meetup
---

**Peru** is a country in South America home to a section of the **Amazon** rainforest and **Machu Picchu** ⛰️, an ancient Incan city high in the Andes mountains. [Percona](https://www.percona.com/) decided to hold the first event of **Percona University 2023 in Lima**, the capital of Peru, on June 10.

[Percona University](https://www.percona.com/blog/percona-university-is-back-in-business/) is a series of free technical events organized by Percona in various cities around the world since 2013. **Percona** uses these events to share its unbiased expertise on open source databases with the community, users, and organizations. The last [Percona University was in 2022 in Istanbul, Turkey](https://percona.community/events/percona-university-istanbul-2022/).

Something charming was designed for this first session of Percona University; there were all kinds of stickers and prizes at the end of the event.

![pup-stikers-01](blog/2023/06/pup-stikers-01.jpeg)

The talks were related to **open source databases** and **kubernetes**. Let's summarize them:

- Let's start with [Peter Zaitsev](https://www.linkedin.com/in/peterzaitsev?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAQH8EBHFDyKi6meRnMSE5FNzSJilakYJQ&lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3BdslLban%2BQgGG1jwigOsRaQ%3D%3D), who talked about the [Cloud of Serfdom vs. the Cloud of Freedom](https://docs.google.com/presentation/d/12d27qQN0EIh3v-ssoZwzSR6ulXg_EcuO/edit#slide=id.p7); why open source will win in the Cloud Age, spoke about the relationship between Cloud and Open Source, showing the historical changes in the impact of the **Cloud on Open Source** and examining the current state of affairs, and advocating for a specific approach to using Cloud and Open Source together.

- **Peter's** next talk was about [17 reasons to migrate to MySQL 8](https://docs.google.com/presentation/d/1AFjeTePOWYRyap1lmLa84kcfB0klBSQx/edit#slide=id.p1)
  MySQL 8 was different from previous major MySQL versions, as it underwent significant changes from its initial release in 2018 to the version in 2023. Many features were introduced through subsequent minor version releases. In the presentation, Peter focused on the most important Modern MySQL 8 features that had emerged since the initial release of **MySQL 8**.

![pup-peter-02](blog/2023/06/pup-peter-02.jpeg)

- The next on the agenda was [Michael Villegas](https://www.linkedin.com/in/mvillegascuellar?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAYosmwB_V8dLwgDO5dFwIsOtx_BSTIwYXA&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3BgaPel2l9SCeCz6vJLRN4Fw%3D%3D). He talked about Useful tools from the [Percona Toolkit for DBAs](https://docs.google.com/presentation/d/1NX2c_DS9ussvc6VZmFT-4-wk28SIuKVs/edit#slide=id.p1). This talk was aimed at DBAs and developers of any level of experience responsible for MySQL database administration. They learned how to use some very useful tools within the [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit) to solve common problems within their databases. Michael showed these tools allowed them to save time and effort in resolving these issues.

![pup-michael-03](blog/2023/06/pup-michael-03.jpeg)

After the following talk, we had a coffee break provided by Percona, it was an opportunity to chat with Peter and network with other attendees.

![pup-breakfast-04](blog/2023/06/pup-breakfast-04.jpeg)

The next talk was by **Peter Zaitsev** about **Advanced MySQL optimization and troubleshooting using PMM**. Optimizing MySQL performance and troubleshooting MySQL problems are two of the most critical and challenging tasks for MySQL DBAs. The databases power their applications need to handle changing traffic workloads while remaining responsive and stable, ensuring an excellent user experience. Additionally, DBAs are expected to find cost-efficient solutions to these issues. In the presentation, Peter Zaitsev showed advanced options of [PMM version 2](https://docs.percona.com/percona-monitoring-and-management/index.html), which allowed DBAs to address these challenges.
![pup-peter-05](blog/2023/06/pup-peter-05.jpeg)

The next talk was for [Edith Puclla](https://www.linkedin.com/in/edithpuclla/) (me). I did an [Introduction to Kubernetes Operators](https://docs.google.com/presentation/d/1URi6oNC3fZKd2mCAZ3CGZ_CTkAkzIHWW/edit#slide=id.p1). I provided a simplified overview of **Kubernetes Operators**, focusing on making the concept understandable for those new to the subject. I started explaining Kubernetes and why they are relevant in managing applications, then we go for Kubernetes Operators example, the reason behind that, and the benefits of using Operators.

![pup-edith-06](blog/2023/06/pup-edith-06.jpeg)

Our last talk was about [Deep Dive Into Query Performance](https://docs.google.com/presentation/d/10mzZu-N_mv_4zpD3-6LVXN0Lv01ws7tn/edit#slide=id.p1) by **Peter Zaitsev**. In this presentation, Peter explored this seemingly simple aspect of working with databases in detail. Peter answered questions like when you should focus on tuning specific queries or when it is better to focus on tuning the database (or just getting a bigger box). Peter also showed other ways to minimize user facing response time, such as parallel queries, asynchronous queries, queueing complex work, and as often misunderstood response time killers such as overloaded networks, stolen CPU, and even limits imposed by this pesky speed of light.

![pup-peter-07](blog/2023/06/pup-peter-07.jpeg)

The event was well received. Many graduates, professionals, students, and open source enthusiasts attended the event.

![pup-team-08](blog/2023/06/pup-team-08.jpeg)
![pup-public-09](blog/2023/06/pup-public-09.jpeg)
![pup-all-10](blog/2023/06/pup-all-10.jpeg)

And also nice to share moments with Peter and his fans.

![pup-lunch-11](blog/2023/06/pup-lunch-11.jpeg)

We also thank [ESAN University](https://www.ue.edu.pe/) for providing us with the venue for the event.

![pup-team-12](blog/2023/06/pup-team-12.jpeg)

Don't miss our next [Percona University event, in Istanbul](https://learn.percona.com/percona-university-istanbul-2022)!

See you at **Percona University Peru in 2024**!
