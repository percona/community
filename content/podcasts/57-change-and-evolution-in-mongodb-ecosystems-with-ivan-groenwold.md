---
title: "Change and Evolution in MongoDB Ecosystems – Percona Podcast #57 /W Ivan Groenwold"
description: "Overview of Ivan’s career before going deep into MongoDB ecosystems. Short preview of the topics that Ivan is looking forward to presenting at Percona Live 2022."
short_text: "Developers love MongoDB, and the changes and growth of the community has been awesome. The Head Of Open Source Strategy at Percona, Matt Yonkovit, sat down with Ivan Groenewold, Senior Architect at Percona to talk about all things MongoDB from growth, to challenges, to sharding. We take a look at an overview of Ivan’s career before going deep into MongoDB ecosystems: the evolution, change, performance, jumbo chunks, most common issues, escalation in mongo space, and automation. In addition to all of that, they tackle the topics that Ivan is looking forward to presenting at Percona Live 2022."
date: "2022-04-14"
podbean_link: "https://percona.podbean.com/e/change-and-evolution-in-mongodb-ecosystems-%e2%80%93-percona-podcast-57-w-ivan-groenwold/"
youtube_id: "WTrNoLgsTRg"
speakers:
  - ivan_groenwold
  - matt_yonkovit
---

## Transcript

**Matt Yonkovit:**  
Hi, everybody. Welcome to another episode of The HOSS talks FOSS. I'm here with **Ivan Groenewold**, from Percona. And we're here to talk about Ivan in his career, what he's done at Percona, the MongoDB ecosystem, and all the fun things in the database space. Ivan, how're you doing today?

**Ivan Groenewold:**  
I'm doing great. Thank you for having me.

**Matt Yonkovit:**  
So Ivan, you've been in the database space for quite some time now. Right? Maybe tell everybody a little bit about you?

**Ivan Groenewold:**  
Sure! So, I started my career actually, as a security administrator. So in the IT security department that's unusual, like most people start like as a DBA or something. But I did a couple of years as a security administrator first. Eventually, the company I was working for at the time, had a position in the IT department. So I moved over. And that's where I started to become familiar with servers, networking, and cabling staff. We did pretty much everything related to hardware and provisioning, and so on, we then had a really cool project where we have to start the data center in the new building from scratch and move everything we have over to this new building, which was quite complex. But also, it was a really good project to be involved in. So yeah, after a couple of years working as a sysadmin, I moved again, because there was positioning the database team that we have outsource at the time. And the company was they wanted to have a like an internal person with knowledge, just outsource everything. So I moved over to the Oracle DBA position. This is back in 2008 or so, a long time ago. And that was my first contact with databases with the Oracle DB. So yeah, I spent a couple of years there. And then eventually, I moved over to another company that was an E-commerce company. And they were having a mixed environment where there was some Oracle DB, but there were also other open source databases. And that was my first contact with the open source ecosystem. They were having MySQL at the time, there was a bit of moment to be it was earlier versions of MongoDB, like 2.0, or 2.20. 

**Matt Yonkovit:**  
Wow, that's really old. Yeah, early days

**Ivan Groenewold:**  
yeah. MongoDB have the old map search engine back in the day, which was memory mapped files. That's completely different world from the MongoDB we know, nowadays. So I spent a couple of years in that company and then eventually moved over to consulting. So after that, I never left the open source ecosystem anymore. So it's been over 10 years that I've been doing just open source dBs, I forgot everything about Oracle now. So for the last 10 years or so.

**Matt Yonkovit:**  
So you got involved in the MongoDB ecosystem pretty early on. When things were still being flushed out in terms of the architecture, it was still an early project, it was still considered a quote-unquote, startup. And now we know it isn't. It's a very established company with a very established technology footprint. What have you seen grow over that time period? Right. So how has that ecosystem evolved, from your perspective? What have you seen, growth-wise, maybe some concerns maybe some things that have changed or transformed over that time period that you're what was interesting to see? 

**Ivan Groenewold:**  
Yeah, I guess from the early days, things were quite hard. The map search engine was completely different from what we have today with WiredTiger. I think that was the biggest transition probably. And map b1 was memory map files, there was a global lock. That was like everyone's nightmare at the time. You wanted to avoid this, this global log as much as you could, but there's not much you could do about it. So it limited a lot, the concurrency of the database at the time, I think it's quite similar to what happened with MySQL, when at the beginning, there search engine and then went into the beat came over, it was like a revolution. Well, the same happened for MongoDB, when they brought wild tiger, WiredTiger over that introduce a whole new world of scalability and new things or the database. Also Percona started to become involved. So we now there are kind of backup for MongoDB, for example, which makes it really easy to have a backup in the shadow environment, or back in the day, we were dealing with stopping all of the nodes at this specific point in time. And then I tried to figure out how to take a snapshot of everything at the same time. So we have more tools from the community, also, that helps make our lives easier nowadays.

**Matt Yonkovit:**  
Yeah, and as that ecosystem has grown, you've seen that the use cases for MongoDB have expanded. I've often talked about this in the past, where I've started to see databases start off with a very specific niche use case almost right. So it's very specific, it's good at this thing. And then as time goes on, either the community wants more use cases, or companies want more market share. So they start to evolve. And you mentioned WiredTiger, for instance, it's taking what was a NoSQL non-transactional system, and it's starting to move into the transaction space, starting to provide things that were never built into the architecture. So as that ecosystem has evolved, more and more people have started to do things in Mongo. I'm curious, what do you see people do in the Mongo space that you're like, why are you using MongoDB? For this particular use case? Do you see that like, where you're like, you scratch your head and go, this is not really a good fit for the database?

**Ivan Groenewold:**  
Yeah, well, I think, MongoDB is trying to be a general-purpose database nowadays. So always trying to do what other databases are doing, like, for example, transactions. The support for transactions is more or less recent, I think they were introduced around the MongoDB 4.0, right. So I guess if you really need transactions, perhaps it's a sign that you should be thinking maybe about a traditional relational database? I mean, you can do it with MongoDB, but we'd normally , but it doesn't necessarily mean you should be doing it. Right. Maybe it's one of the things that can tell you that maybe you're should take a look at other type of technology. I don't know.

**Matt Yonkovit:**  
I mean yeah, I think like, for me that the most popular use cases that I always see Mongo, like out there, and a lot of SaaS companies, a lot of web companies with websites that are that have that native JSON data format, that are looking for something that's easy. They're looking for that scalability, and, that ease of use of having the flexibility in the document design. And so I see that quite often in gaming companies if you're building mobile apps, things like that, it's Mongo is still a very popular use case. But I haven't really seen it evolve into more of the corporate systems as much. It's more on the other web app the application side, things that are more consumer facing? I don't know, have you? Have you experienced that as well?

**Ivan Groenewold:**  
Yeah. To be honest, I haven't seen it for things like, for example, financial data, I think that is more suitable for traditional RDBMS. Like MySQL, for example. That kind of thing. Yeah. It's probably not very popular, or at least I haven't seen that a lot.

**Matt Yonkovit:**  
Yeah, and I think that from a Mongo perspective it has done a good job of kind of encompassing all these different use cases. And like I mentioned, I think the document storage really lends itself well to the web app and the mobile app type design, it lends itself well to a certain sort of workload. But I think one of the interesting things that I always scratch my head at is a lot of people adopt Mongo specifically because of that flexibility. And so they say, Oh, I don't need a schema, I don't need to think about validation of my schema or things like that. But you really do, don't you because as data grows, ensuring that you have some semblance of good data structures and validation, it becomes more important.

**Ivan Groenewold:**  
Yeah, definitely. And this is why also, they introduced this schema validation tool, eventually into MongoDB, I think because if not, you run the risk of having mixed data that you don't really know what it is like there, it can get out of control really quickly. It's one of one strain that you can really add new fields to documents without any schema changes that are sometimes painful in other databases, but at the same time that can become really complex and get out of control quickly if you're not careful about maintaining structure.

**Matt Yonkovit:**  
Yeah, and I think that leads to a lot of performance issues. And the problem with most databases is, you start off, you have a simple application, you have something that's designed to work from the ground up, you test it you have a few 1000 users, everything's fine. But then all of a sudden, you become successful, and you get 100,000 users or a million users. And then everything changes. And a lot of times with the schema validation or the design of the documents themselves, the indexing strategy, the sharding strategy, it all kind of is fine until you reach a certain inflection point, and then you realize, Wow, you really screwed up early on, and you should have fixed these issues, and they become bigger issues. Right. It's something that early on, it doesn't seem to impact you. But later on, it can really add especially at scale.

**Ivan Groenewold:**  
Yeah, definitely. I agree.

**Matt Yonkovit:**  
Yeah. And I think we see that with some of the newer features in Mongo, for instance, like the shard, rebalancing, things that they've they've introduced recently, go directly to try and fix some of those issues early on. And I think that's one of the key topics, that's always a popular topic at different conferences is, how to choose the right shard key or how to rebalance your shards what are the tips and tricks to make that faster? Because when you're talking about multiple terabytes of data, shard, rebalance is very painful. Very, very, very painful.

**Ivan Groenewold:**  
Yeah, we run into that with our customers a lot. And there's really no easy solution because nowadays, the balancer is not super configurable. So what we ended up doing sometimes is doing some manual operations to try and do the balancer job sometimes. Yeah, I think that is one of the areas where development still needs to do a couple of things to make balancing a bit more configurable to reduce the impact. And another thing is that the jumbo chunks, okay, that is really a pain. And for that, we also ran into that with our customers very frequently. I have a few scripts actually, that I developed and published in Percona blog, to help with problems with jumbo chunks, and also new versions where MongoDB sometimes having jumbo chunks that become undetected. So you really didn't know that you have a jumbo chunk. So in one of these blog articles that I was talking about, there's some instructions for dealing with that. And the same goes the other way around, when you delete data, and then you're chunk to become empty, there is no way to actually compact them together. So to reduce the number of chunks when you no longer need them. So I have to deal with that problem also, as well.

**Matt Yonkovit:**  
So just for those who are listening who might not be familiar with Mongo. Can you give us like a 10 seconds, what is a jumbo chunk?

**Ivan Groenewold:**  
So basically, when you start inserting a lot of data, and MongoDB doesn't really figure out that you inserted a lot of data, and it all goes into the same chunk, then it will grow past the size of the chunk, which is 64 megabytes by default. And that will cause the balancer to not move that chunk anymore. So it's just a lot of data that is there and MongoDB doesn't touch it anymore. So if you want to move that around to different shards, for example, then it's problematic because it's a big piece of data right? So, you want to avoid that most of the time.

**Matt Yonkovit:**  
So it gets pinned in one area and stuck there until you manually do something to fix it. So, as we talk about like data sizes, they grow Always things evolve. I'm curious, what are the most common issues that you have to deal with customers coming and asking for help or working on systems. Ae there common problems that you see over and over again, in the Mongo ecosystem that you really wish people would just stop doing?

**Ivan Groenewold:**  
I don't think there's really a mistake of people doing it, it's just the way that the database is working nowadays, like scaling up or down, the number of shards is costly, like there's a lot of data to be moved around whether you want to scale up or scale down. Again, this is the balancer's job to, like do all this chunk management. And I think it's, it needs a bit more work. Because of the configuration of the balancer, for example, the Ivorians that it uses, sometimes it can have an impact. So normally, you define your balance or window to be during the night when there's the least database activity, however, it can still have a significant impact. So I think there's room for improvement in that area.

**Matt Yonkovit:**  
Okay. I think one of the issues that I see crop up, is modern environments. Now, everybody wants their own databases, everyone wants their own setup, which means that you've got systems that are very large, but you also have lots of little systems as well. So you'll have a mixed environment, you might have one database, one setup that has terabytes of data. But then you might have 1000, small databases for individual applications, individual microservices, individual functions. And that presents quite a challenge. Are you seeing that escalation in the Mongo space as well?

**Ivan Groenewold:**  
Yeah, definitely, this happens the databases, and this is why automation is a key thing to get right from the get go. Because otherwise, you end up with different MongoDB systems that are configured differently or don't follow the same standards. So it's very difficult to manage when you grow, even though MongoDB has sharding from built-in. When you started growing, the number of shards, it becomes really complex and easy to go into the hundreds of servers without even noticing. So it's critical to have good automation and auto-monitoring. Right. That's where PMM kind of comes to, to help you, right?

**Matt Yonkovit:**  
Yeah, I mean, automation comes in many different forms. And I think that there's always different tools out there, you have a talk coming up on Ansible and TerraForm, at Percona live, but we also see the growth of Kubernetes as a deployment mechanism to deploy MongoDB we have an operator ourselves to help with facilitate that. But those aren't the only deployment tools and infrastructure and orchestration tools that are out there. do you have a preference? Is there something that you prefer? I mean, I know you're talking about TerraForm and Ansible? Because you did it. But have you gotten into the Kubernetes? Side? Are there other tools that you see that are really popular out there?

**Ivan Groenewold:**  
Well, I had the chance to try the operator a couple of times, I've seen really good results with it. I've see there is a lot of community interest in that. That still haven't been personally involved with many production deployments, I know that our other people at Percona have that kind of experience. I personally haven't had it yet. But according to their forums, in Percona, there is a real a lot of interest in most of the forum talk that been going on in the last couple of weeks has been related to the operator. So definitely did that's the way to go,

**Matt Yonkovit:**  
Okay. And so let me ask you this. And this will be our final thought for the day. as you look out at the open source ecosystem, you look at the new technology landscape, what are some of the technologies and the things you're seeing out there that gets you excited that you're really looking at like, wow, this is something interesting, I either want to learn it, or I want to use it more, or you maybe you use it already, but it's something that you would like to recommend to other folks as something to take a look at?

**Ivan Groenewold:**  
Well, I mean, I'm going to repeat myself here, but again, the Kubernetes is all around the place now. Everybody's talking about it or implementing something in Kubernetes. So I think it's the key concept to embrace for the next couple of years. Even if we're not SysAdmins, like we're supposed to be DBAs or consultants really working with databases, but Kubernetes is going to be a topic whether we like it or not. So it's better to start working with it. The sooner, the better.

**Matt Yonkovit:**  
Yeah, absolutely. Well, Ivan, thanks for stopping by sharing a little bit about your background at the MongoDB ecosystem, some of the things going on. I would encourage our listeners, if you haven't already, check out Percona Live, Ivan's gonna be speaking there. He has two talks. I will be there doing podcasts, live streams and all kinds of other fun things. So we would encourage you to come out to Austin. If you're in the area, you can take a look at the conference is scheduled right now for Monday, the 16th. Tuesday, the 17th and Wednesday, the 18th of May. It is going to be awesome. There's going to be Mongo content, MySQL content, Maria, DB, Postgres. There's all kinds of Kubernetes. We've talked about Kubernetes or some security topics, something for everyone in the data space, so we would encourage you to come out. But Ivan, thanks for swinging by. And we really look forward to hearing your talks at Percona Live.

**Ivan Groenewold:**  
Thank you, and thank you for having me.

**Matt Yonkovit:**  
No problem.

