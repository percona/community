---
title: "PingCAP, HTAP, NewSQL, and TiDB - Percona Podcast 39"
description: "Liquan Pei, Senior Software Engineer, Database Kernel at PingCAP sat down with the HOSS Matt Yonkovit to talk about PingCAP, HTAP, NewSQL, and getting deeper into TiDB."
short_text: "Liquan Pei, Senior Software Engineer, Database Kernel at PingCAP sat down with the HOSS Matt Yonkovit to talk about PingCAP, Hybrid Transactional and Analytical Processing ( HTAP), NewSQL, and getting deeper into TiDB. 
PingCAP is founded by the team that built TiDB, a world leading Open-Source distributed NewSQL database, for globally scalable HTAP which is compatible with MySQL, and enables companies to painlessly scale their business while keeping the underlying infrastructure simple.
."
date: "2021-09-03"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-39-liquan-pei-sr-software-engineer-database-kernel-at-pingcap/"
youtube_id: "C8Hldu7nHP8"
speakers:
  - liquan_pei
  - matt_yonkovit
aliases:
    - "/podcasts/39/"
url: "/podcasts/39-pingcap-htap-newsql-and-tidb"

---


## Transcript

**Matt Yonkovit:**
Hi, everybody. Welcome to another Hoss Talks fosse. I'm here with Liquan Pei from PingCAP. How are you today?

**Liquan Pei:**
I'm pretty good. And then pretty excited to take this conversation with you. 

**Matt Yonkovit:**
Great. Great. And so tell us a little bit about PingCAP and what you do there. For those who might not know about PingCAP or TiDB. 

**Liquan Pei:**
Yes, PingCAP is a company founded in 2015. And it starts with a project called TiDB. TiDB is a NewSQL or HTAP database, for people who don't know about HTAP is short for a hybrid transactional analytical database, which means that you can process your RTP workload or AP workload a single system. And since then, on since it's funded, and it starts with building an open-source project, and it has attracted, I think, over 2000 stars. And it has already over 1000 contributors to the project. And it has been used by many companies, I think we now have over 1500 companies that have adopted it in production, I think KDP is a new distributed architecture with was inspired by co Spanner. And is has layered architecture. Yeah, we can go into more detail about that. And I'm doing a jumping capping on 2020. But I've been knowing this company for a long time ago. I know the founders since the year of 2017. Where when I that time, I was at Pinterest. And we have a project and we call it like real-time indexing. And actually, that's a good fit for TiDB with did a quick kind of like a demo at that time. I think that is how I know about TiDB at that time. So that is kind of like some of history with TiDB. Now I'm here working as a database engineer. But I do know in startups, especially while we are still early stage in the United States. I also wear multiple hats. And it helped with recruiting a lot. Either interviewed maybe a couple of hundreds candidates last year and this year. And then I also worked very closely with a few customers is that for especially some key customers in North America. 

**Matt Yonkovit:**
Yeah, and many of the former people who I've worked within the past have gone on to work at PingCAP, many from the MySQL space because PingCAP’s,  protocols are MySQL protocols, they've made sure to mirror those. So there's a compatibility with existing MySQL workloads. 

**Liquan Pei:**
Yes, that's a good point. I think when we build that, I think I think we keep in mind that we want to be MySQL compatible. I think that is kind of our original goal. Because we know that MySQL is kind of the most adopted open source database. And it has a lot of usage. And I think when the founders building stuff, they want to make the migration easy from MySQL.

**Matt Yonkovit:**
Yeah, and we've seen that in this NewSQL space, you've got type dB, you've got Yugabite, you've got Cockroach, Yugabite and Cockroach have chosen the Postgres protocol versus the MySQL protocol. So depending on where you lie on whether you prefer Postgres or MySQL, there is a solution for you. But maybe tell us a little bit about what NewSQL is because people are using MySQL today, they understand it, why would they need to move to the next level to this NewSQL version that has more features? What did they get from doing that? 

**Liquan Pei:**
Yeah, I think that's a great question. My understanding of NewSQL is really combined advantages of the relational database, which has transaction capability and the SQL interface and scalability of NoSQL, right? Because no, NoSQL excels at scaling is pretty easy scale, you can add nodes and you can handle more customer data and handle more traffic, right? That is kind of what NoSQL excels at. Whereas for a traditional relational database, you have the transactions, right? This simplifies a lot to developers because they can safely retry when something fails. Whereas if you don't support transactions, then you have to do a lot of additional work in order to make things correct? Yeah, that's one point. And the other thing that I think is much easier, right? It's very expressive. You can do a lot of computations using SQL, you can do scans, you can do group bys, and do joints, and then do analytics, right, then do a lot of things. Even you can build machine learning libraries using SQL. So I've been working at the premise company that they called Greenplum database, and they actually build machinery library on top of SQL. So you can do a lot of things with SQL. So this definitely can speed up the developer velocity. So I think that the benefits, Hi, we're traditionally scaling SQL database is pretty hard. And people choose to use sharding. And once you go there, and the application needs to be aware of the database sharded, and you lose the transactionality, across shards. So I think with the NewSQL, the sharding is transparent to the user and the user still think you are working with a single node database, by the database underlying can be scalable, you can add new nodes, and then you can move the data around and automatically and by adding new nodes, you can scale the database now serving more traffic and store more data. So I think all from the benefits to the developer is that, first of all, they're still working with SQL, and they're still mostly thinking is a single node database, then they have like higher developer velocity, for the maintenance corner view, and you don't need to manage this sharding. And, and I think that is kind of the benefits. 

**Matt Yonkovit:**
Now, one of the interesting things about TiDB is it is, currently a completely open-source product, so anyone can go out, try it, use it, and get the benefits of this NewSQL for themselves. But you can also contribute to it, you mentioned that you have 1000s of contributors worldwide. So it's a bit of a different model than a lot of companies are falling a lot of companies right now tend to prefer some sort of proprietary -ish, or not quite open source license, if you will.
 So that's one of the exciting things about that. And that can help definitely drive adoption. But, um I talked with Morgan on our podcast, Morgan Tucker. Not too long ago, he was talking about some of the hackathons that the engineers at PingCAP have put on for their community. And I was curious, have you? Have you been participating in those hackathons as well? 

**Liquan Pei:**
Unfortunately, I did. And but I will allow to increase a predict. I think it's a pretty fun fact, actually, I watched a lot of like videos, and a lot of articles talking about a hackathon, for example, using GPUs to have to accelerate or AP processing and building a crud graph database on top of TiDB. Right? or building filesystem on top of TiDB, there's a lot of interesting ideas. And also, there are some features that I think customers really want like the TTL in tables, right? This is a lot of customer want. And a lot of interesting stuff. So, yeah, I would love to do that. But I think the challenge with me is the timezone issue really, really in the US. I think there's a lot of events actually in the APAC region. So that's kind of what if I miss those things, I think I hope that we can have a hackathon in the local timezone so that I can really positively participate. But there are a lot of interesting things out of it, for example, for the GPU, kind of like acceleration and Vidya also expressed some interest in knowing more about it, and see whether we can collaborate in some sense.

**Matt Yonkovit:**
So your job is working heavily. You mentioned, you're doing a lot of different hats, because you're a startup, but officially, it's working on the database kernel itself. Is that yes, yes. What? So what sort of work are you doing recently? What sort of interesting things are you looking at? 

**Liquan Pei:**
Yes, I think one thing I was now looking at is kind of like something some new features in the database, for example, or to whether or when should we how to partition entirely? Yeah, and how to make TiDB more cloud-native, there's something actually we are, I was involved in the discussion. 

**Matt Yonkovit:**
So yeah, so you're talking about cloud-native in terms of like, being able to run on Kubernetes AG, automatically spin up new nodes, re shard replication as you need to? 

**Liquan Pei:**
It's just part of it. Also, I think another thing we need to look at is that how do we build a database that leverages, so cloud primitives, for example. I argue example. For example, right now the takeaway is using a raft to do data replication, right? And the one that notices down when I add a new node to the system, you actually need to copy the data from the existing node to the so that you can serve the traffic, right? Yeah, isn’t it like architecture, but then in the cloud, you have x rays, and you have other like the cloud services available. And then you can leverage that to simplify those replications. So for example, you don't have to replicate all the data, you can probably replicate your logs, right? That's enough. And all the rest can be done through the s3, right? You can use s3 and then to download. And another thing to leverage as the cloud is typically on, the takeaway is doing compactions because they are building a RocksDB. And periodically, they need to do compactions to kind of make the data better form that will say write to deduplication to make things like more structure. So and that is done traditionally, in the same type of intervals, as in the notes serving the traffic. And then when you do compaction can have an impact on the online traffic, right? However, on the cloud, you can do things differently, you can actually do remote compaction, you can, okay, so consider that as your dedicated machines. And then we can ship those files in those machines and do the compaction, ship them back. So at the end of the day, though, the machine service traffic will consume much less CPU when doing these compactions, you actually offload the compaction, dude adequately resourced, and is added without, it causes like a much more stable performance to the online traffic. So that's a consequence, the benefits of the cloud-native architecture. Right. 

**Matt Yonkovit:**
Okay. So I mean, yeah, I mean, it sounds like a lot of the stuff you're working on is kind of twofold, right? Obviously, the performance and scale are always important, but also those operations, making it easier for things to happen behind the scenes, I know that trying to spin up new nodes is always a challenge. And yes, if you can hook into some of the things that are already available in the cloud, whether they're block storage you know, copies or do snapshots or take your backups from s3, wherever, that those are always good things and obviously, anything that you can do to speed up some of the backend maintenance is also going to be helpful. But when we talk about like use cases, and you mentioned, TiDB has you know, 1500 customers, and probably 10 times the number of users. I'm curious, is there a use case that you see that this is really popular with? Are there one or two different industries or different workloads that TiDB really excels at? 

**Liquan Pei:**
Yes, yes, sure. I think we have, like, customers in the FinTech space. And our customers, I think I want to maybe give it to two use cases, I think, why are in the FinTech domain and the other in maybe in the SaaS domain. So I think for the FinTech that there's nowadays more and more like 
I would say that either online banking, or there's b2b or customer-facing payments, right, for example, one mobile square cash app, and the other. I believe companies in different parts of the world, for example, there's a company called the new bank in Brazil, they are offering credit cards. And there's another company in South America, they are offering also similar to the new bank, they're offering their credit card to Spanish speaking customers. So I think for those companies on they are they want to offer good experience to the users right because they are dealing with a larger user base. Yeah. And I think they have the challenge of scaling their business. For example, one of the customers we have is in Japan and they are an online payment company and you can basically send money to each other, and that they have met the challenge they cannot scale during peak hours and especially during promotions. And then they are suffering a lot about that because the scale of the database they are what they were using cannot scale the rice and then they have the basically cannot do the promotion. They may stop. So they decide to use TiDB. And you can scale both reads and writes. And then once they migrate to TiDB, they no longer suffer any outages when they do promotions and TiDB can easily handle three times of their current scale, this is one of the examples we have, which are the entire online payments and offering a service to the consumers and they can do a lot of transactions at the same time, because of that is a consumer-facing

**Matt Yonkovit:**
FinTech is an interesting space because it's one of those spaces that when you look around the industry today, everyone is concerned about ensuring that not only do they have performance, but security and in FinTech, it's one of those things that security's even further along, so maybe tell us a little bit about some of the things that you're working on from a security standpoint to make sure that the code that's going out there, and the feature set can handle a bit more of a secure environment like that. 

**Liquan Pei:**
Yeah, sure. We have like, the TLS, between all the components on the client and the cluster, okay. And also, we have an encrypted string at rest, which calls a TD for, for us of note file storage layer. And then we have also an authorization and authentication system in the TiDB. layer and, and beyond that, I think we also offer an audit log for the users that they know what happened in the database. So here are some features we provided in the database itself, on the cloud services, have that we probably, I should have mentioned that we also offer hospitality, we call it the cloud. And for that, we have actively kind of like doing compliance stuff. So for example, we have past stock two, type two, and also the ISO 2731. Recently, and to show our continued investment in the security.

**Matt Yonkovit:**
Okay, okay. Yeah, I mean, it's, it's always interesting to see because the bar for not only performance, but security keeps on becoming bigger, higher and higher to clear. As these systems become more critical, especially in some of these ancillary spaces. Yeah. But from an engineering perspective I am curious like, what are some of the interesting maybe fun things you've uncovered looking at the code base for for for TiDB VR, there are certain things that surprised you when you started to dig in. Were there things that you thought were very interesting. Or that you think is pretty unique?

**Liquan Pei:**
Yeah, I think a pretty unique thing is, is on is usually we work with the distributors, and some, some pretty simple things can be really complicated. So that's one thing I will come up with sample code, I'll say the binlog alternative capture, right? And I think if people have spoken to the MySQL, and they should be familiar with the binlock, right? can be used to do data replication set up like a slave muscley. Sorry, the primary-secondary like architectures, right. Yeah, so totally interesting. And I think for a tissue database, like TiDB, and then if you do in alternative capture, there's a lot of like interesting problems you will never think of when working with compared with working with a single node database. For example, how do we support distribution options and all the transactions can happen on different nodes right. And then you start doing an actual data capture or binlog then gather this data from different machines right. If you want really want this data to be useful, you do need to output the data in the international order. So that you can build like a primary-secondary architecture with your dr system, right. However, then, there is a challenge is that because everything is distributed, you get a lot of things like your in the order of modifications, but not in the order of commits, right, you can start a transaction and the transaction can be very long and then commit to the very late right and say multiple lines in the email don't know when you receive everything right? Because everything is distributed, you don't know. Okay, whether I have received all the updates for this transaction, right? Then this really becomes pretty interesting. So I think, for the distributed kind of transactions are actually utilize research actually, from big data, I think there's, I think there's a paper called Nayad, published by Microsoft, that actually building a data flow system. And using the result timestamp. And the idea of random timestamp is that, you know that before this, once you receive this, it's like a watermark in the stream processing system, telling you that once you receive this event, everything before this timestamp has been received by the downstream, then you can know, that they will know that all the events are using all the events, that you can find them downstream, other than that you cannot send downstream. And this is pretty fascinating. And without this idea, you cannot really reconstruct your transaction order. Right. So I think this is something I really like.

**Matt Yonkovit:**
Yeah, that, that that's interesting I mean, in, when you think of a distributed system, and a distributed SQL system for those of us who have been in the database space, you're used to being able to monitor nodes, even if there are multiple nodes in the cluster. But because of the distributed nature of the transactions, it can lead to other issues, not just with the trying to piece together the transaction logs, but also the observability has in the monitoring, and being able to figure out which potential node might be having issues or trying to piece together that has to be a challenge from a back end perspective as well. 

**Liquan Pei:**
Yes, I think I totally agree with you. So I think that shallow-rooted criticism is like, you have to deal with failures, right? So we had two failures, and you need to make sure that your system behaves correctly with those failures. So and then, then, and then also, because it is kind of like, handling a lot of things at the same time. Right? Yeah. So those are understanding what happens is pretty challenging, especially where  support like, SQL queries, and also we support complex SQL queries and figuring out what consumed the most resources is kind of challenging.

**Matt Yonkovit:**
Yeah, and I mean, I can imagine that it's, it's hard enough sometimes to find the problem area and yeah, and also that there are backed by, there's a lot of, kind of, like background works, like compaction, like the garbage collection. 

**Liquan Pei:**
Yeah. Like, like the synchronization between the column store row store, rather, there's a lot of back backend, and then the replication, then the transaction logic, right, we've kind of like a lot of things going on the same time. And, and beyond that, there are constant failures, you do need to move data around. And you don't need to understand the environment in the oldest kind of dynamic in this very dynamic environment and, and ensure everything is correct. Even with that oldest dynamic, right? Imagine the case that you still want to support a family right for the transactions, given that they suddenly move in there is causing the failure failures through constantly retries. So there are the readers please read and watch. Right? So that you can know what really I do really like?

**Matt Yonkovit:**
Yeah, I mean, I, it's fascinating, because as you start to go in as a database person, as a, as someone who's running this to be able to understand, where a problem is, where, where the issue is, is always that interesting step that, you know, from an engineering perspective, you try and fix those without escalating them up or letting people know about them. But eventually, someone's looking for. 

**Liquan Pei:**
Yeah, that's the beauty of the database will hide a lot of compasses inside, right? And for the user, see? Okay, I think we are just running SQL. And I think for a lot of like I say, I've been working with people from other from like, working mostly in the upper level, in private companies. So they are really mostly dealing with running SQL queries, not running, writing SQL queries. They will think that SQL systems are pretty magic. And about I mean, for database person is really like they had a lot of complexity there. 

**Matt Yonkovit:**
Very cool. Well, Liquan, I want to thank you for stopping by and giving us a little bit of an overview of tie DB and some of the things you're working on.

**Liquan Pei:**
Always good to catch up. Appreciate you stopping by structure. 

Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram, and LinkedIn and of course tune in to next week's episode. We really appreciate you coming and talking open-source with us.





