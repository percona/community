---
title: 'Cassandra Where and How by John Schulz'
date: Wed, 24 Jun 2020 12:20:22 +0000
draft: false
tags: ['Mayank Sharma', 'Cassandra', 'DBaaS', 'DevOps', 'Docker', 'Events', 'Open Source Databases', 'Percona Live', 'Tools']
authors:
  - mayank_sharma
images:
  - blog/2020/06/PLO-Card-Cassandra.jpg
slug: cassandra-where-and-how-by-john-schulz
---

If Percona Live ONLINE had graded its talks by skill level this year, John Schulz’s talk would have been essential viewing in the Beginners track. (You can watch all the event’s presentations now on [Percona’s YouTube channel.](https://www.youtube.com/user/PerconaMySQL/videos)) This talk was a good overview and meant for anyone who had heard of the Apache Cassandra distributed database but wasn’t sure whether it would be suitable for their project or not. 

Database-veteran, John Schulz has been tinkering with Cassandra for about a decade and to help anyone get started he gave a whistle-stop tour of the Cassandra ecosystem. He introduced Apache Cassandra by laying out some important characteristics of the database. These include the way Cassandra is designed to handle high-traffic volumes, especially writes, and is designed from the ground-up for high availability. John briefly talked about the ‘democratized nature’ of the database; how all its nodes are designed to be equal. However, while Cassandra is designed to scale linearly, he stressed that this ability comes with some serious caveats: “You have to understand the way it was designed,” John cautioned an audience of over 500 attendees. “You have to understand how you need to model data with it, otherwise its linear scaling will go out the window.”

Not relational
--------------

Cassandra has many strengths, but it’s not suitable for every use case. For instance, John said he would discourage using Cassandra for analytics as “it's not a massive parallel processing engine.” 

He also highlighted the fact that Cassandra uses an SQL-like language called the [Cassandra Query Language (CQL)](https://en.wikipedia.org/wiki/Apache_Cassandra#Cassandra_Query_Language), which despite its similarities is definitely not SQL. Similarly, while you can add [Spark SQL](https://spark.apache.org/sql/) to Cassandra and perform [JOINs](https://en.wikipedia.org/wiki/Join_(SQL)), Cassandra is not a relational database and shouldn’t be used as one. He also warned against implementing [locks](https://en.wikipedia.org/wiki/Record_locking) in Cassandra. Apparently, he’s seen many customers do this only to regret it later. In fact, he suggested that if using a lock is essential for your application, then perhaps you shouldn’t be looking at Cassandra. 

After cautioning his virtual attendees, John shared some of the circumstances and use cases where Cassandra does excel. As a general principle, Cassandra works best in environments where the database writes exceed the reads by a large margin and where the sheer amount of traffic would normally overwhelm a traditional relational database. 

By way of example, John said that Cassandra works well for tracking ad hit rates. The database is also popularly used in the IoT industry for capturing raw data from devices, such as fitness trackers and vehicles. Also, many phone companies in North America are using Cassandra for customer service and a number of companies use it to provide metrics collection as a service.

First steps
-----------

Before getting started with Cassandra, John strongly recommended setting aside some time to design your database: “Badly designed data models, produce badly performing databases.” 

He suggested a couple of resources that would help with that including an [overview of the topic from the Apache Cassandra project itself](https://cassandra.apache.org/doc/latest/data_modeling/). 

Next, he shared some of the questions you need to ask yourself before using Cassandra. For instance, what’s your main purpose for using Cassandra? The answer to that question will have a bearing on how you want to run Cassandra. That’s because the database offers plenty of options that range from a traditional data center environment to various cloud solutions. You can run Cassandra on your laptop, which is a good environment for tinkering with it. For a production environment though you can deploy Cassandra on physical servers, or inside VMs, or wrapped in containers. 

The next piece of the puzzle is to decide on a Cassandra flavour or distribution. John rounded up some of the most popular including Apache Cassandra, DataStax Enterprise, Scylla Open Source and Enterprise, Yugabyte, CosmosDB, Amazon Keyspaces, and Elassandra. He spent some time explaining them all and the key differences between them, but besides Apache Cassandra and DataStax Enterprise, he classified all other solutions as Cassandra API upstarts that look and behave like Cassandra, but aren’t exactly Cassandra under the covers. He was particularly excited about Elassandra, the mashup of Elasticsearch and Cassandra and pointed out that the former’s global index helps negate the limitations of Cassandra’s secondary indexes that are local-only by default.

At your service
---------------

You can run Cassandra on various platforms, though John recommended using one of the Database-as-a-Service (DBaaS) providers as he felt it made very little sense to do it any other way. He briefly talked about some of the most popular services including InstaClustr, DataStax Astra, Amazon KeySpaces, Scylla Cloud, IBM Compose for Scylla, YugaByte Cloud, and CosmosDB. 

The main advantage of these services, John felt, was that they get you a Cassandra cluster instantly. Furthermore, they also come with lots of useful features such as automatic backups, automatic repairs, as well as monitoring. However, if you don’t want to deploy Cassandra on your own hardware, John supplied a list of things you’ll want to think about. 

He suggested using an automation tool, such as Chef, Puppet, Ansible, to build your clusters. He also recommended using a log aggregator and monitoring the cluster in real-time. He cautioned anyone looking to deploy Cassandra to never run an installation with a single node. John says that while you can do this, you won’t be able to observe all of the interactions that go on between the nodes, which will eventually affect the real-world performance and behaviour of your application. However, John recommended running a cluster of at least n nodes where n equals your replication factor. This is a talk in its own right, but, in essence, he suggested a replication factor of at least three. 

In the final section of his talk he covered the two mechanisms for deploying Cassandra: inside a Docker container and with the [Cassandra Cluster Manager (CCM)](https://github.com/riptano/ccm). Written in Python, John says CCM makes starting a Cassandra cluster on your laptop or desktop, or even a Raspberry Pi, just as easy as using a Database-as-a-Service option on the cloud. He ended by detailing the procedure for both mechanisms using which you can spin up a Cassandra cluster in a matter of minutes. You can watch the whole of [John Schulz’s Apache Cassandra talk](https://www.percona.com/resources/videos/cassandra-where-and-how-john-schulz-percona-live-online-2020) through the link.