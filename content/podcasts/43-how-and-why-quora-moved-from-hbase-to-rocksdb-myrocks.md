---
title: "How and Why Quora Moved From HBase to RocksDB via MyRocks - Percona Podcast 43"
description: "JMatt Yonkovit, The HOSS at Percona, sits down with Nagavamsi (Vamsi) Ponnekanti, Software Engineer at Quora."
short_text: "Matt Yonkovit, The HOSS at Percona, sits down with Nagavamsi (Vamsi) Ponnekanti, Software Engineer at Quora.  During the show we dive into the details on how and why Quora moved from HBase to RocksDB via MyRocks.   We also learn about the need to reduce latency and improve predictability in performance in large infrastructure and database systems.   Vamsi highlights some of his favorite features and tools and gives us tips and tricks on database migrations."
date: "2021-10-01"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep-43-nagavamsi-ponnekanti/"
youtube_id: "Eky7zXFY3yM"
speakers:
  - nagavamsi_ponnekanti
aliases:
    - "/podcasts/43/"
url: "/podcasts/43-how-and-why-quora-moved-from-hbase-to-rocksdb-myrocks"
---


## Transcript


**Matt Yonkovit:**
Hi, everybody. Welcome to another HOSS Talks FOSS. I'm here today to talk about MyRocks. And you know, RocksDB with Vamsi from Quora. How are you today, Vamsi?.

**Nagavamsi Ponnekanti:**
Good. Thanks for inviting me.

**Matt Yonkovit:**
Yes, so Vamsi I saw this blog post you did and was very intrigued by it. I know Vadim sent it over to me and said, like, wow, you should really have Vamsi on the podcast to talk about his journey to using RocksDB, because it was so interesting. And I read through the blog and came up with some interesting questions, some things, but I figured it'd be a good place to maybe just tell everybody a little bit about you and your background.

**Nagavamsi Ponnekanti:**
Sure. So I'm Vamsi. I joined Quora, maybe two and a half years ago, around December 2018. And I'm an engineer in the core infrastructure team at Quora. So yeah, my focus has been more on databases. But the team itself deals with databases, caches, content delivery networks, monitoring a bunch of other stuff. So yeah, and before Quora has been working at Pinterest, Facebook, and so on, but I've been doing similar stuff like databases stuff all in on. 

**Matt Yonkovit:**
Okay. So databases at scale, because all of those are fairly large infrastructures. Yes. Right.

**Nagavamsi Ponnekanti:**  
Sure.

**Matt Yonkovit:**
So tell me maybe just give us a little bit of idea on Quora's infrastructure? How big is it in general?

**Nagavamsi Ponnekanti:** 
Yeah, so Quora has more than 300 million monthly active users. So yeah, I think. Yeah, bbrf, a much smaller company in terms of the number of employees. So yeah, less than 300 employees. So yeah, I think from that perspective, that that is a lot of opportunity for impact, like for anyone who is working at Quora, so yep. 

**Matt Yonkovit:**
So in Quora does kind of question and answers, right? For those who aren't familiar with the business?

**Nagavamsi Ponnekanti:** 
Okay. Yeah, the mission of Quora is to share and grow the world's knowledge. So the at the heart of Quora is questions because the question and answer is a very good format for sharing knowledge, like, so Quora is trying to connect people who have the knowledge and people who need the knowledge, and also to bring together people with different perspectives. And yeah, so in the last few years, Quora has also launched spaces and subscriptions, which basically allow people to also make some money from the knowledge that they are sharing. 

**Matt Yonkovit:**
And I saw that your stack in it had quite diverse, you had MySQL, you had HBase, Redis, Memcached? You know, a little bit of everything it seemed.

**Nagavamsi Ponnekanti:**  
Yes, like, yeah, so it has grown over time. And so we initially started off with MySQL, so that users questions answers, were being stored in MySQL. But at that time, now, we had not implemented sharding in MySQL. So we brought in HBase. Mainly if say generated data, you might be having offline jobs, which generate some data. But then you may need to access the data with very low latency from the web, the product, so so for those cases, we brought in HBase, because those data sets could be large and, and also HBase provides some of these features like time to live and so on. So if you want to get rid of data and automatically if they have if it has not been updated in the last week, or last month or so. So HBase provides those features. And so we brought in HBase. And of course, caching is something that everyone needs to do to reduce the load on their databases. So we use mem cache, and then Redis Cache is being used mainly for the data structures that it provides, right? If you want to cache less or these other data structures, that's when the Redis Cache becomes attractive. So yeah, so I hope that answers some of these questions about why by using all these, yeah.

**Matt Yonkovit:**
So your background is kind of across all of these but you have used quite a bit of MySQL, correct? Sure. So when you're managing like a MySQL or a relational database at scale, what are some of the tools that you've used?

**Nagavamsi Ponnekanti:**  
Yes. So like, often not people need to, at some point build a some form of sharding. So that's, I would say that that becomes necessary at some point. And besides that, the usual, the backups, and then the MySQL replication. So those things are needed. Definitely. And yeah, so here at Khorana, we built internally some tools to allow us to monitor like, what queries are running on MySQL and stuff like that. Okay.

**Matt Yonkovit:**
So you've built a lot of your own scripts and infrastructure to support the environment, because your environment has real specific nuances and differences. And I'm curious, so you've got this big environment you're, you're managing it. And so there's, there's a decision point to try and move away from HBase. So you brought it in, at some point in the history of Korra. Someone brought it in, and now you're looking to remove it, what was kind of the driving factor to consider moving away from HBase?

**Nagavamsi Ponnekanti:**  
Yeah, so the read performance was one of the problems. So the machine learning related use case alchemy about which we wrote a blog post, a different blog post as well. So they were complaining about the performance issues, the read latencies, and stuff. So that was one thing. Then the other thing was, we were using both MySQL and HBase. Both of these are very complex and very different from each other. So practically speaking, no, there is no knowledge or tool sharing that can happen between these two. So like, no, nobody ever wrote it tool that works for both MySQL and HBase. Right. So yeah, so that was double the complexity when we had in your engineer, or even if you hire an experienced engineer, and they may not be familiar with both MySQL and HBase. So yeah, these were the two main reasons like the read performance, especially the P99. Performance, read performance, and the fact that MySQL and HBase are so different, and both are complex. Yeah.

**Matt Yonkovit:**
You know, you mentioned P99. And that's something that a lot of us in the database space is familiar with some of our listeners might not be maybe tell us in your words the importance of what that P 99 is, and just so listeners understand, when we talk about P99. What we're talking about is the latency that 99% of the queries come back as so you kind of throw out the 1%. outlier. And you look at that 99. So why is that important to a company like Quora?

**Nagavamsi Ponnekanti:**  
Yeah, so one reason is that often applications managed to the product may need to make multiple database requests, they may need to retrieve multiple data items from the database. So yeah, so the P99. of them. If the P99 is slow. Now, we may be thinking that, okay, only 1% of requests are slow. But from the application perspective, now, it might be much larger than one person, because they are making multiple requests, and they're trying to retrieve multiple data items. Right. So that's one thing. The other thing is, we have to remember that there are different users, and sometimes these power users, and they might be running into this pay 99 latency issues. And they are also very important users for us, right? So we don't want to be making them unhappy. So that’s another reason those are like the two sides. Yeah,

**Matt Yonkovit:** 
You really want consistency across your query. So people can understand that they're going to get the same user experience when they're accessing application, there are no surprises. But you can also make some predictions on when you might need to add hardware when you might need to change configuration when you might need to tune so having the consistency really does matter, doesn't it?

**Nagavamsi Ponnekanti:**  
Do you mean consistency of performance?

**Matt Yonkovit:** 
Yeah, yeah. Sure. It might be a better word. Yeah.

**Nagavamsi Ponnekanti:**  
I think, yes. I think that predictability and consistency of performance also matter. Sure. Yeah.

**Matt Yonkovit:** 
Because I know that there's nothing worse than having a user, let alone a power user who is all of a sudden, like, I normally run this in a minute and now it's taking you to know, 10 minutes And those are just Oh, those are so hard to deal with.

**Nagavamsi Ponnekanti:**  
Sure.

**Matt Yonkovit:** 
So, you're looking at this move to try and improve your read performance. And you've got you mentioned that the data set in HBase is quite large. You know, that was one of the reasons for originally moving to HBase you know, you ended up choosing my rocks in MySQL solution, did you did you evaluate other solutions when you were looking at this?

**Nagavamsi Ponnekanti:**  
So we have been seeing RocksDB become very popular in the industry, right. So Facebook has adopted RocksDB, Pinterest has adopted RocksDB, Instagram has adopted RocksDB in different forms. So the question was not like whether or not to use RocksDB, but it was more like okay, which RocksDB base system to use, right? We had multiple choices. But as I mentioned earlier, now, we have MySQL and HBase, which are two very different systems. And so we wanted to avoid, again, bringing something that's very different from MySQL. So from that perspective, my rock seemed attractive because a lot of the tools and that we have are based on tools, and also the internal knowledge and expertise, hopefully, they can be meaningful sharing of that with my dogs. But if we, if we use let's say, Cassandra, for example, then we don't have any internal Cassandra knowledge or experience. So if you use Cassandra, then we need to build that expertise, right. So just to give you an example. So from that perspective of my rock seem attractive. Yeah.

**Matt Yonkovit:** 
And that's what I've seen that over and over again, with a lot of folks at different companies, where they can do a lot of what they need to do with multiple tools. So they choose the one that's they've got the most expertise, or the best chance of success with, try and consolidate there. Because a lot of databases nowadays, handle data differently. And there are different use cases for them. But there's a lot of overlapping use cases. And if you fall into one of those overlapping, it's less about the technology and more about how comfortable you are, and how quickly you can deploy and be successful with it. In my opinion. I don't know if that's your experience, it kind of sounds like it is.

**Nagavamsi Ponnekanti:**  
Yes, definitely.

**Matt Yonkovit:** 
Okay. And so so so you have MySQL running. And now you're going to start adding the the my rocks portion to it from the MySQL perspective. Is that a completely different workload, and are using InnoDB? There, are you also looking at my rocks for that workload?

**Nagavamsi Ponnekanti:**  
So we have separate MySQL instances using InnoDB and rocks dB. So there are some MySQL machines, which have InnoDB tables. And then there is a different set of my rocks machines, which are using rocks DB tables. So within the same MySQL instance, we don't use both InnoDB and rocks dB.

**Matt Yonkovit:** 
Okay, well, what's the dividing line for you? When would you choose to use rocks versus InnoDB?

**Nagavamsi Ponnekanti:**  
Yeah, right now, the dividing line has been more like a key value store use case. So those key value store use cases which have been using HBase. And which might use HBase. In the future. Now, those are being put in my Docs, whereas the SQL use cases are continuing to go to MySQL, yeah.

**Matt Yonkovit:** 
Okay. And are you also sharding MySQL? Yes, like, so. Yeah. The InnoDB side, I mean, like, so are you doing both rocks and InnoDB sharding.

**Nagavamsi Ponnekanti:** 
So that our sharding logic, not that part is kind of shared in the sense it says similar logic, which is a query? Yeah. So be based on the sharding key we hash it and that that logic is sort of that's in the application. And it's kind of shared between MySQL and my dogs. So yeah, so MySQL. Also, we have sharded. So we did two kinds of sharding. One is like vertical sharding, where we can keep different tables on different MySQL instances. And then, more recently, we also built horizontal sharding, where they could split one logical table into multiple physical tables. And these physical tables could be on the same or different MySQL machines. So yeah, and those are available to my rocks as well. This again, goes back to what I said earlier that some of the tools and stuff that we have built for MySQL are sort of reusable for my Dogs? So whatever sharding we have been, yep, sort of reusing that for my rocks as well.

**Matt Yonkovit:**  
Okay. And so, so this migration from HBase, to MyRocks setup. How hard was it? Was it was fairly straightforward.

**Nagavamsi Ponnekanti:**  
So Well, I mean, it took some time. And so I mean, I had some previous migration experience as well. So in that sense at a high level, we were doing similar, we followed the standard approach of, okay, you start double writing things to my dogs and an egg base, and then you do the backfilling to get the old data onto my rocks, and then you do their reads the dark reads to compare if you're seeing similar results with between the HBase and the new mitoq system. And once you see that, okay, you are getting same results. You know, if you feel confident, at that point, you cut over to my rocks, very the production starts reading from the, my rocks, but you again, keep around the ability to go back if something bad were to happen. So So in that sense, even if even after you have cutover to my rocks, you continue to do a double writing to HBase. And that way yeah, so hopefully, yeah, if there's an issue, you can go back, and so things are hopefully you find Yeah.

**Matt Yonkovit:**   
Okay, so yeah, so you you did that approach where it was, do everything in parallel, once you validated failover and leave it up and running for a while in case you fail, but you do need to failback. And so you're now in production now with my rocks, correct? Yes. So what kind of differences? Have you noticed what I mean? Like, like I saw there were some pretty significant performance improvements, right?

**Nagavamsi Ponnekanti:** 
Yes, like, so. Yeah, we have been migrating table by table. And then we mainly we, we started using the higher-up’s tables, like, because there was a long tail of lookups tables, we did not want to worry about them at the beginning. So yeah, so the hike UPS tables, we started migrating. And so the main thing that we saw, the P 99. Latency is a lot more stable. So with HBase, we would see that okay, the P 99. latency, if you watch that graph, for a few hours, you often see it goes up to sometimes more than one second, two seconds. So yeah, so that the P 99. Latency has been much more stable. With my Doc's. That's one thing that we have seen. The other thing is, yeah, we also saw the actual p 99. Latency number is much lower. So we had like two kinds of use cases. One is where the bulk load and tables where the writes happened only through bulk loads. And then there were other tables where the writes were happening on a continuous basis, regularly. So generally, the bulk loaded tables we saw even higher improvements, sometimes maybe 10 times the P 99. Latency was better. Wow. Pardon? Yeah, the reason

**Matt Yonkovit:** 
why I said, Wow, 10 times. Yeah, that's a lot. Yeah. 10 times. Yeah.

**Nagavamsi Ponnekanti:**  
So I think the reason for that, one reason is that with my rocks, now, the way we are doing, we are handling these tables we write to a different instance than we read from so that then the bulk load is happening at high speed. Now, the read performance, hopefully is not affected by this bulk load. So, yeah, that I think, the higher performance

**Matt Yonkovit:** 
and so one of the other things and I don't know that I know, from a rocks DB perspective, it's, it's fairly efficient on space. Did you? Did you happen to save more space, physical disk space, with this migration as well?

**Nagavamsi Ponnekanti:** 
I think HBase is also good with compression. So, but anyway, that space was not the main thing that you were looking for the space saving. Yeah. So I would say maybe comparable space. And only thing is with HBase. You know, it already keeps three copies of data. And on top of that, we needed a slave cluster like HBase slave cluster, where some tables are to be kept there for dumping to hive and so on. So there, yeah, so that we are with the hierarchy. We just keep three copies. That's it like, not six copies, like HBase. Yeah. So but then those six copies were not being maintained for all tables. It was only for a few tables. Yeah. Okay,

**Matt Yonkovit:** 
and you know, so it seems like there's been quite a bit of work here, from a management perspective. I know that you mentioned using replication and some other things before but for for this use case, for your, your, my rocks deployments, you're not using standard replication, you're actually doing the sharding. And it sounds like you have the shard sets, where you're loading data into individual shard sets and just replicating the data yourself with with your data loads is that correct? So,

**Nagavamsi Ponnekanti:**  
that is that is only for tables, which need bulk load so, so the tables that need daily bulk load, they are being put in separate Micic my rocks machines. In those cases, we are not using replication, but for other tables my rocks tables, which have direct rights now, continual writes, they use a replication. Does that clarify?

**Matt Yonkovit:** 
Yeah, yeah. No, yeah, that it was just interesting that reading somehow you were doing some of that basically going to shard set one, and moving all the data to the other two shards, and then loading that one, and then moving the flipping your traffic around. So it was a very interesting approach to doing those bulk loads, so you wouldn't have to incur the penalty of replication between the nodes. That was that was kind of interesting. And telling that you probably have quite large data loads, that could potentially impact things. Now, you mentioned using time to live, and this is not something that's generally available in MySQL InnoDB. Right. So how is that used in the application? You know, maybe tell us a little bit about that. Because that's a feature that's kind of unique in the MySQL ecosystem to my rocks, correct?

**Nagavamsi Ponnekanti:**  
Right. That's, yeah, that's available in my Docs, but not available in MySQL. So yeah, I think that is mainly, like, if there is some generated data or something we may choose to keep it around only for some limited time after that, maybe the validity. Maybe it's no longer valuable. And so we just automatically drop it. So yeah, it's more for like, data that are either generated or, I mean, certainly for user data, like questions or answers. We don't want to have this time to live. It's yeah. That doesn't answer your call.

**Matt Yonkovit:**  
If it was like metrics or cash or anything like that session data for an individual you log in sessions, you might have a time to live.

**Nagavamsi Ponnekanti:**  
Yeah. Or they might be offline jobs, which are generating some data, and then maybe that data can be generated again. So yeah, maybe, yeah, we might want to keep it only around for some number of days. And yeah. Okay.

**Matt Yonkovit:** 
And overall, you seem pretty happy with the results so far? I mean, is so maybe tell us this migration and getting things moved over? What was there anything that was really surprising? You've used my rock for a while now. So it might not be surprising this time. But as you started using my rocks in the past, what are some of those features that you look at? And say like, that's really cool. Or do I really like that?

**Nagavamsi Ponnekanti:**  
Yeah, I think because suddenly, compared to InnoDB the RocksDB as much better compression. So that, certainly, I like that. If the data set is large enough, suddenly, you want to have it compressed, then yeah, some of these features like the time to live and so on when the application needs it. That's good to have some efficient way of purging old data. Then the other thing I also like is, if you need if you have tables where the right rate is higher, so traditionally, MySQL, the InnoDB was optimized for reads. So if you have some workloads where the write rate is high enough, that's another thing area where my Doc's tends to perform better. So yeah, those are some of the things that I like about my Roxy.

**Matt Yonkovit:**  
Okay. And you did, I saw you found a few bugs. So there were some things you wanted to work on a little better. You know, so hopefully, some of the folks out there whether it's Vadim or Yoshinori are gonna watch this. And so if there's a couple of those things that you want to mention, like, hey, it'd be even better if it kind of sounded like the Bloom filter was a pretty big deal for performance and you might be able to squeak out a little bit more performance with Yeah,

**Nagavamsi Ponnekanti:**  
yeah. prefix bass bloom filter Yeah, that was one of the things then RocksDB has a multi gate, but MyRocks is not using multi gate. That's what we was we were told. So since often request a bunch of keys with key values to earn them. So yeah, I think if my rocks were to leverage the multi get in rocks dB that can give better performance. And then for InnoDB, it is handler interface is supported. So if someone is doing a simple request trying to get it off all these SQL parsing overhead and stuff now, we can use this handler interface and get,

**Matt Yonkovit:**   
You're going really old with that because they use the handle interface used to be a big thing, and InnoDB. I have not looked at that and years. But I remember when people would use that because there wasn't there was a handler interface.

**Nagavamsi Ponnekanti:** 
Yep. And something like that being made available for rocks DB would be even better. Because I think a lot of key-value store use cases might be using rocks DB storage in general. So there, you may not need the overhead of all the sequel parsing and stuff. So it might be even more useful. Like for RocksDB.

**Matt Yonkovit:**  
Right. Okay, and Vamsi let me finish with this. Any advice to other people who are going to be looking at rocks? Or looking at my rocks? Anything that you learn knowledge to pass along to them? You know, that would be useful?

**Nagavamsi Ponnekanti:** 
Yeah, I mean, I would say the usual standard things in a sense, you're starting off a little bit small, in a sense, pick some a table or some representative use case and then experiment with that. And then, yeah, have this year, do these shadow reads and validate what you are seeing like both in terms of performance, as well as in terms of correctness Shadow rates are going to help you validate both those. And then yeah, and also, it's very important to have the ability to go back, like when you are trying new systems you might also think about what happens if like, if you switched over to the new system now, and you are serving production traffic and something unexpected happens, make sure that you can quickly switch back as well. So yeah, well, once you have some of these standard things then hopefully you are in a good shape. Yeah. So

**Matt Yonkovit:**  
Yeah, great. Well, MZ, thanks for stopping by and sharing your story about migrating to my rocks. And some of the reasons why, if you want to follow along, and some of the journey there, the core engineering blog has quite a few articles on the infrastructure, including how they do sharding and see some of the benchmarks and some of the things that they ran into with this migration. But thanks for stopping by.

**Nagavamsi Ponnekanti:**  
Yeah, thanks for inviting me. And as I mentioned Quora, we have a lot of users not have scalability challenges. There's a lot of opportunities, and we are hiring as well. So if anyone is interested, yeah, yeah. If anyone isn't absolutely, yeah, we have opportunities in many areas like data, whether it's databases, caching, machine learning, product development, and you name it, likely, we have opportunities in all the areas. So yeah, thanks for inviting me.

**Matt Yonkovit:**
Yep, appreciate it. And if you are looking for something, want to do some big data challenges definitely take a look at the core job boards there and see what's available. If you'd like to hear the rest of that interview, head on over to YouTube, or go ahead and pull out your phone pull out your favorite podcast app. We are available everywhere. Just search for HOSS Talks FOSS, and you can get this episode and a new episode every week where we talk about all the things happening in an open-source and keep you up to date.





