---
title: 'Percona Live Europe Presents: Need for speed - Boosting Apache Cassandra''s performance using Netty'
date: Mon, 22 Oct 2018 08:34:35 +0000
draft: false
tags: [ 'DevOps', 'Events', 'MySQL', 'Percona Live Europe 2018']
images:
  - blog/2018/10/apache-cassandra-logo-3.png
authors:
  - dinesh_joshi
slug: percona-live-europe-presents-need-speed-boosting-apache-cassandras-performance-using-netty
---

![](blog/2018/10/apache-cassandra-logo-3.png)

My talk is titled [Need for speed: Boosting Apache Cassandra's performance using Netty](https://www.percona.com/live/e18/sessions/need-for-speed-boosting-apache-cassandras-performance-using-netty). Over the years that I have worked in the software industry, making code run fast has fascinated me. So, naturally when I first started contributing to Apache Cassandra, I started looking opportunities to improve its performance. My talk takes us through some interesting challenges within a distributed system like [Apache Cassandra](http://cassandra.apache.org/) and various techniques to significantly improve its performance. Talking about performance is incredibly exciting because you can easily quantify and see the results. Making improvements to the database’s performance not only improves the user experience but also reflects positively on the organization’s bottom line. It also has the added benefit of pushing the boundaries of scale. Furthermore, my talk spans beyond Apache Cassandra and is generally applicable for writing performant networking applications in Java.

Who’d benefit most from the presentation?
-----------------------------------------

My talk is oriented primarily towards developers and operators. Although Apache Cassandra is written in Java and we talk about Netty, there is plenty in the talk that is generic and the lessons learned could be applied towards any Distributed System. I think developers with various experience levels would benefit from the talk. However, intermediate developers would benefit the most.

What I'm most looking forward to at PLE '18...
----------------------------------------------

There are many interesting sessions at the conference. Here are some of the interesting sessions -

#### [Performance Analyses Technologies for Databases](https://www.percona.com/live/e18/sessions/performance-analyses-technologies-for-databases)

As I mentioned, I am a big performance geek and in this talk Peter is going to talk about various methods to data infrastructure performance analysis including monitoring.

#### [Securing Access to Facebook's Databases](https://www.percona.com/live/e18/sessions/securing-access-to-facebooks-databases)

This is an interesting session from a security standpoint. Andrew is talking about securing access to MySQL. As most people know Facebook has a huge MySQL deployment and as security and privacy has become a prime concern, we see a lot of movement towards encryption. This talk is going to be particularly interesting because Facebook is using x509 client certs to authenticate. This is a non-trivial challenge for anybody at scale.

#### [TLS for MySQL at large scale](https://www.percona.com/live/e18/sessions/tls-for-mysql-at-large-scale)

This talk from Wikipedia is along similar lines as the previous one. It just goes to emphasize the importance of security in today's climate. What's interesting is that Wikipedia and Facebook, both are talking about it! I am curious to find out what sort of privacy challenges Wikipedia is solving.

#### [Advanced MySQL Data at Rest Encryption in Percona Server](https://www.percona.com/live/e18/sessions/advanced-mysql-data-at-rest-encryption-in-percona-server)

Another security related talk! This one's about encryption at rest. This is interesting in and of itself as we tend to talk a lot about security in transit and less often about security of data at rest. I hope to learn more about the cost of implementing encryption at rest and its impact on the database performance, operations as well as security.

#### [Artificial Intelligence Database Performance Tuning](https://www.percona.com/live/e18/sessions/artificial-intelligence-database-performance-tuning)

I think this is an exciting time for the database industry as we've not only seen large increase in data volumes but also user expectations have gone up around performance. So, can AI help us tune our databases? Traditionally, the domain of an experienced DBA, I think AI can help us deliver better performance. This talk is about using Genetic Algorithms to tune the database performance. I am curious to find out how these algorithms are applied to tune databases.