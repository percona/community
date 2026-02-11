---
title: Percona MeetUp for MongoDB Sept 2021
description: The first Percona MeetUp for MongoDB on MongoDB sharded cluster best
  practices and future Kubernetes Operator features.
images:
- events/percona-meetup/mongodb-cover-1362.jpg
date: '2021-09-22'
draft: false
speakers:
- vinodh_krishnaswamy
- ege_gunes
- matt_yonkovit
tags: ["Meetup", "MongoDB"]
events_year: ["2021"]
events_tag: ["Community", "MongoDB"]
events_category: ["Speaking"]
---
Matt Yonkovit hosted the Percona MeetUp for MongoDB on September 22nd with Vinodh Krishnaswamy, Support Engineer at Percona, to talk about "MongoDB sharded Cluster- best practices" and Ege Güneş, Software Engineer at Percona, to discuss "Cross-regional replication for MongoDB with Kubernetes". Check full video on youtube by clicking the link below :

## Video

{{% youtube youtube_id="s7v8hAC55iw" %}}{{% /youtube %}}

## Transcript


**Matt Yonkovit** 
Good amazing that's a cool whoa

Hello everybody welcome to another Percona live stream we are at the top of the hour so thank you for joining us today I've got Ege and Vinodh with me from Team Perconaю So hello guys I'm gonna go ahead and I'm gonna turn on the chat so we can see anybody who pops in here and asks us some questions. So um a few things before we begin this is our third meetup This one is focused on Mongo so every month we'll have a Mongo focused one every month we'll have a Postgres every month we'll have a MySQL every month we'll have an observability and monitoring one as well. So you know, hopefully, you're here to join us live. If not, you can check this out on YouTube and if you're watching there, feel free to reach out. We'd love to have you as a guest. So come on and chat with us later on.

But you know, I wanted to actually start with a topic that has nothing to do with MongoDB or databases or open source in general. All right, now, you might hear some construction stuff going on around the house here today. I don't know if you will, it's hit or miss. So yesterday, I had a slight plumbing issue and now they're tearing up my floor downstairs. So you know, I might get called away and so you know, we might have a time when I disappear for a second. We'll see. But I decided to work my plumbing issues into technical talk. And so this is my challenge for today. I wanted to make an analogy that was interesting and relevant to today's topics. So at first I thought, I thought hey, here I've got a bathroom that basically had some plumbing issues. And so they had to tear out the floor, take the toilet out, take all this stuff out to fix it. And I thought about using this as a good analogy for high availability. So we failed over to our second toilet, and our second bathroom down the hall and we had, we have sharded bathrooms like the half bath with no shower and the full bath with showers. So we've shard it. So we have different feature sets. So I thought that could work. But then I found out what's actually the problem, and it took me in a completely different direction. So it turns out, and I don't know, Vinodh or Ege, do you either know much about plumbing? Or are you guys plumbing experts at all?

**Ege Güneş**  
No. 

**Matt Yonkovit** 
Okay, so I was not aware of this. But it turns out that from a plumbing perspective toilets sit on, like, what they call this bowl ring. And then there's like this inner ring that's made of wax or something. And I didn't know that that's something that I didn't know. And it turns out that when we bought this house, couple years ago, it was a new building, and they actually never completed it. They missed some of the parts, and they missed some of the setup. And so what's been happening is that part actually keeps the plumbing from leaking. And so over time things started to leak, and between the floor and the sub floor you know, little by little water and other things started to get in there, because they missed this relatively small component that was supposed to be put in there. So for a couple years, it worked no problems, no issues, there was no signs of any issues, anything like that. And then all of a sudden, one day, it just you start to notice, like the floorboards buckle, you start to notice water, you're like, what the heck is going on? So you call the plumber, they come out, they go, Oh, wow, this has been happening for a while, he just didn't notice it, because it was all kind of below the surface. And this kind of reminded me of one of the big problems that I see in databases right now is, how many times do we sit there and say hey, you've got these problems, it is a scalability issue, there's, there's an issue with your your application performance, there's an issue with your availability, and it turns out that the application was never designed properly. And in the case of my toilet like you literally had something that worked for two years without a problem. But it reached a point of saturation, or a point that it became such a critical issue, that it overflowed and started to cause other issues. Right. And so from that perspective, we have a lot of databases that are out there, a lot of databases, infrastructure developers are out there, they're developing all kinds of cool things. A lot of times, you're not thinking about the design aspects of it, it works for a couple of years, they probably move on to another job. And then someone has to come along, and they're like, Oh, my God, why did all this stuff break? And you realize, Oh, this was never designed to handle this the way it was, it's, it was a, it was a bug that it worked for two years, right? It shouldn't have worked for two years. And you know, when we talk about Mongo, and today, our topic is really Mongo. Mongo is designed for developers, right? You know, that's its core audience, it is so easy to use, it's so easy to get started. But one of the things that I continually hear over and over again, from a Mongo perspective, is hey, people don't think much about the design, because it's just you take your JSON, you throw it in the database, and you run with it so it's designed to not have to think about those database components. And so I'm curious, your experience in that you know, I know what happens in MySQL, I know what happens to Postgres in MongoDB. How often is that design causing issues?

**Ege Güneş**  
So Vinodh, you want to start?

**Vinodh Krishnaswamy**  
So a lot of times, like in MongoDB, the design is the main part of when you're actually looking for the performance. Okay. So as Matt said, like, if you're going to have a bad design or bad topology, then you're not going to, maybe you're not going to see the consequences immediately. But later you will be seeing like, for example, you, you may see your queries running faster when you're actually implementing the application for the first time. But in some days, after some, after getting some new data into the database, you may see some kind of issues because that is because your data is not actually distributed properly in the shadow cluster. For example, here, when you're not having your proper or the cluster is not designed in a way that your data is scattered properly, okay? And your load is not also going to scatter properly, okay. And in that case, when you're going to have the application or getting the data, for example, if it is going to write or get going to get some data fetching the data, so it, it cannot go into the right place and get the data and come within time, which is expected, okay, so it may cause because in long run, your data is not actually sharded properly, so that what happens like because of the wrong shard key, okay, and because of your queries, which is not using the proper shotgun in the photo, so that can cause your query scatter across all shots, okay? And when you're designing your application, and the topology very properly, you can put your query into the particular shard where your Mongo is and can directly go into that particular shard and get your data and give it to you back within no time. But when it is not designed properly, your data is going to scatter across all shards, which is going to make it difficult for your application or it hits the performance very hard.

**Matt Yonkovit** 
So, Vinodh, this is like a classic Mongo problem, right? So in older versions of Mongo, because they just introduced this, you used to have resharpening be a significant issue from a shard perspective. Yeah, right? Because you would get these imbalances where one or two nodes would have, like so much hot data, that it couldn't handle it. But there was a whole art to trying to get that to like to be distributed properly. But now they've introduced this new feature in the latest versions of Mongo. Have you tested that out? Have you played with it? Can you tell us a little bit about the resharpening capabilities and the new Mongo? 

**Vinodh Krishnaswamy**  
Yeah, it's been a pain point in earlier version, like when you when you find out of when you found that your shard key is not the proper one, you want to reach out that one, okay, or if you want to change the shard key, in earlier versions, you need to actually drop the collection and recreate with a new shard key okay. And as you said, like in 5.0, there is an option which we can reshard or which we can redefine the Shard key online itself without dropping and recreating the Shard Key. The problem with this here is like, even though you have the opportunity to reshard, your collection, at the pain point, is very high. Okay, for example, if we have data, for example, if we have data of 10 GB or 20 GB, it would be faster. But if you have data in terabytes, you just think about the pain point where it would take a long time to reshard. Also, you would need at least 120 percent of the data size or the empty disk space inside the office level. Okay, so it would take that much at least that much space to get recreated. Okay. And that's there. And again, the other main point here is like when you are actually doing the shard key changing, okay, and you need to actually or slow down all your application load to the database, so that it won't actually interrupt with the process of changing the Shard Key as well. So to avoid these pain points, it is better to have that descent before coming into the production. That means like before doing that, do your r&d and choose your shard key properly before itself.

**Matt Yonkovit** 
So Sharding is an art in and of itself. But I mean, just from a database design perspective. You know, I continually hear from a Mongo perspective, often, people don't think about adding indexes, sometimes they don't think about the actual structure of their documents. And those two are very critical things that people often overlook. Do you have any experience running into problems with those?

**Vinodh Krishnaswamy**  
Oh, yeah, a lot of problems. Because in my support, like I have seen a lot of cases where people have faced issues with that hot shard, okay. Hot shard in the sights, in the sense like, all your data application request goes into the particular shard. For example, if we have, like 20 shard in your shadow cluster, okay? But all your load goes into the particular shard, which makes that shard unresponsive for some time. Okay? That is because all your data which you needed by the application  exists on that particular shard, okay, we call it a hard shard, okay. So in that case, it is important for you to split up your data across many shard, so that or you can split up your load as well, too many shard, okay, for that, you need to make sure that there are ways that you can actually split up these things, you can pre shard, or else you can pre or defend your chunks, so that you can put your data into multiple shard earlier itself, for example, if you are going to insert or put a new rights into the shard cluster, it's going to get into one shot, and the balancer is going to migrate everything into the other shots. If you are going to pre define those chunks, the data, whichever you're going to write will go into the respective shardin, in previous stages itself .

**Matt Yonkovit** 
shards aside for a second, just from an you know, like, from a performance scalability design issue, shard without shard, it doesn't matter. I mean, like that, that actual document design is often overlooked, right?

**Vinodh Krishnaswamy**  
Ah, yeah, that is because it's not like our DBMS, where you have a predefined structure. So okay. And the other thing is, like, when you're facing the issue, only you will come to know, okay, you need to create an index on that. Okay? So it's only when you're having the problem, you come to know, okay, this is the problem. So we need to create an index, then only you are going to get advice from us, I'm going to create an index on that. So instead of that, do some testing on the application side, and then create an index previously itself, so that you will have no issues on that. Also, you can plan, like a bulk update, okay, or bulk inserts, so that it won't cause issues much into the application side. 

**Matt Yonkovit** 
Okay! Ege, you are an application developer. Formerly, you used to be an application developer, correct? Yep. And so from your perspective, tell me a little bit about your experience from a developer perspective in Mongo.

**Ege Güneş**  
So to be honest, I have myself defending against using Mongo in many times, 

**Matt Yonkovit** 
Why wait? Why would you do that?

**Ege Güneş**  
As a web developer, before, many developers, as you said, love Mongo, and they want to run away from this relational database. They don't want to have the strict schemas that have these foreign keys, and they might run away from them, they want to have a JSON document and put all things to that. But in my use cases, that was the cause of the application in the data. So we need to duplicate all the data. And yeah, we need to update this document. So we need to update this, a Mongo doesn't have to mess with that. That is not the case. So I am against using a Mongo or no SQL database in general to escape from the relation database, a prospect but some data is more suitable for Mongo like you have. And let's say you have a collection of products. And you need to be flexible. That schema with text with prices and specific fields for different countries, maybe it's really a nice match. So this problem, but to run away from a relational perspective, is an anti pattern.

**Matt Yonkovit** 
Yeah, and I think that this is a common thing. Right. So this gets back to that, again, the designing discussion that I mentioned, which is some people just you know, it's the old school mentality, I used to work at an Oracle shop and it was an Oracle shop, which means any database, any workload was Oracle. Right? And I think that people still fall into that trap sometimes where it's like we have this in our environment, we must use it, but really, the great thing about the current database landscape is there is a database, probably for every job you want to do. That's also the most scary thing about the current database landscape is there are so many of them. But you know, you look at the differences between let's say Cassandra, MongoDB, Redis elastic all of these different databases that are out there, they solve different purposes and have different use cases. And each one is really designed to handle a specific workload and you know, sometimes choosing one just because you want to escape the other because I don't like them. I hate this database, because I think that that is the wrong mentality. And that sets you up for that design decision that maybe a couple years down the road is gonna come back and bite you. Right? And I think that that's a mistake we've all fallen into, in the past, because we all have our prejudices on what we consider a better database, or what we're more comfortable with. And in a lot of cases someone who is a MySQL DBA is gonna choose MySQL, someone who uses Mongo, all the time is gonna choose Mongo. They're not necessarily the right one to use for that particular application. Yeah. And so!

**Ege Güneş**  
Yeah, I was wrong from an application perspective, Mongo can be a wrong choice, maybe MySQL, maybe a wrong choice for some use cases. But from an infrastructure standpoint, Mongo is really a nice database about scaling, about replication, about sharding, as you know, it is because I think it will yield from this, this idea from the first and it's a really nice database of scale to manage I think. So I do like Mongo.

**Matt Yonkovit** 
Said that really what you see in one of the awesome things from a Mongo perspective is how easy it is to run the infrastructure.

**Ege Güneş**  
Yes, so I will be talking about this new feature in our operators called cross region replication. I may say cross class replication, so it's a synonym for me, please don't confuse it. You can have two clusters, one in Cubase. One, maybe on Cubase, maybe on prem, some Linux servers, or a bunch of Linux services, and you can configure replication. And I can't tell how easy it was with Mongo. It was a really nice experience, because we did the same features in our PXC operator, and it was harder than that. But that's one of my teammates. This feature is mpfc in a recent release, and I reviewed the code. It's much more complex, it was much more complex PXC but Mongo, it was just a, put them in the same network that's configured with authentication, this SSL case. And so that replication was really easy after that. So Mongo in that perspective, about this replication, we even support shirts with this feature, and it was easy to do. So I really liked Mongo after that feature. 

**Matt Yonkovit** 
And so when, okay, so what we're talking about here is you've got two clusters across vast reaches of time and space you've got one on, let's say in Europe, one in South America, right? So you've got these two clusters, and you're talking about being able to set up geographically redundant clusters across two geographic regions. 

**Ege Güneş**  
So Mongo has this concept of replica sets to configure replication as a primary, have a primary and a secondary is to poop all these different regions in the same replica set, so they can replicate data between them. And all the rights Continuously replicated in all these regions, all these data centers.

Okay, and I think, what Ege is telling, like, it's a great feature that a MongoDB can replicate across multiple regions and also there is a feature called zones, okay, orders are in replica set, you can use tag sets, or it's in shadow cluster, you can use zones, okay? With using that you can actually redirect all your data load to the specific region. So instead of going into the, for example, if the application resides in South America, if we want to access data from South America, you can redirect all those load to South America regions MongoDB instances by using these tax zones, okay. And by using that you can actually split up everything. And then also you can keep specific data only into the specific region. 

Unknown Speaker  
You don't need to.

**Matt Yonkovit** 
So if you want just your South American users to hit those, yeah, that's okay. And that means that both sides are live and accessible, you can read and write from either side. 

**Vinodh Krishnaswamy**  
Yeah, you can do that. Yeah, that's why I told you, writer, it's, by using zones, you can do that. When you're using a replica set, there is no other way you have to replicate to all the nodes. But you can use tag sets to redirect all your load to the particular nodes that you can do.

**Matt Yonkovit** 
Okay. And so this is a tech preview right now, right? 

**Ege Güneş**  
Yes, we will be releasing this feature as a tech preview, because it's complex features. And we don't want people to rush with their production clusters, a treat, and we needed to limit the functionality of these replica clusters. If you deploy them with our operators, we need to limit the functionality of our operators like backups and restores. The Smart update feature is because the smart update is a feature to upgrade your Mongo database to the next major version. And this restarts of your database not without a minimal downtime, it adds many context switches in clients. So we need to limit this functionality. Or this leads to and we are releasing as technical preview, but in the next releases, and if people will, using it, start using it in the testing environments, staging environments, and they can provide feedback for us. And the featured image in the next release. 

**Matt Yonkovit** 
And so Okay, so this is designed right now to be in the Kubernetes operator, but not everyone runs in Kubernetes. So people are afraid to run Kubernetes. Other people find it daunting to potentially move to Kubernetes. You know, maybe tell us a little bit about that process if you know, is it easy for people to move, easy for people to get started with Kubernetes and Mongo.

**Ege Güneş**  
Who gets started, it's easy, but too many people have this production environment currently. So this feature is primarily designed for those people, because migrating to commands is the scariest part and you probably you have a big data like gigabytes, maybe terabytes of data and taking them of it and putting some a object storage in some clouds is a really scary a I was a DevOps engineer before Percona. And I wouldn't want to do that. Because it will be a big downtime. But with this cross class replication I think you can replicate the data. And then you can minimize the downtime when you're trying to migrate, it's a nice thing to do and people don't need too much to just try out the real data. They can try Kubernetes with real data, they can read replicates, and they can see the performance on Kubernetes. They can stop replication at any time and to see how their applications behave. So it's more than easy now to migrate or try out Kubernetes.

**Vinodh Krishnaswamy**  
Yeah, even in support, I have seen a lot of customers start using Kubernetes even though I have seen a customer who is using integrated PMM. With the hands out I'm monitoring the MongoDB instances from Kubernetes. So people are started moving into Kubernetes nowadays

**Matt Yonkovit** 
Okay, and Vinodh so we talked about these geographically redundant setup in Kubernetes. And I know that you have a passion for sharding, because you've already talked a little bit about sharding earlier. Is this something that you're seeing the geographically distributed shards yet?

**Vinodh Krishnaswamy**  
Oh, yeah, I've seen that like, because even I have seen a customer who is using that zone, okay. So that he's having some data in Asia, and Europe as well as in I think in the American state or something, okay. So, the only thing is, they need to properly mention the zones that tax it. So when they are actually inserting the data, it will go into the respective shard. And also when you are using the rate preference, there is a thing called rate preference, you just need to mention the proper zone ID so that it will redirect to the respective instance in that region. So that is fine. But one little pain point here is like, you need to have a proper headset there. Otherwise, what will happen, if you are going to lose some data, or lose some instance, you will not have a backup 

**Matt Yonkovit** 
Let me ask you a question about that. This is an interesting question. So I think some people get this wrong. Is sharding in and of itself a HA strategy?

**Vinodh Krishnaswamy**  
No, not at all. So the thing here is the people think that deploying the schodack cluster itself is a HA, no. So it's kind of a Mongo if there are three, there are three components, movies, con conflicts, and shard. Okay, within that conflict server and shard, you need to put everything into a replica set. For example, if it has three shard, shard, one, put it in a replica set, shard two put it in a replica set. So something like that, you need to configure servers, you put it in a replica set, so that even if one of the servers goes down, you can have another server to take over that one. So you need to make sure the shard cluster is the one part, and I think a replica set to that, is there another part.

**Matt Yonkovit** 
Okay. Okay. And so you know, so you know, so there is two components here, you can have HA without sharding, you can have sharding, without HA, and just because you have sharded data doesn't mean you have high availability, because if one of your shards goes away, then everything is kind of worked. Yeah. Right, unless you have the HA setup. So it's an important distinction, because we have gotten that question before on our community channels, where it's like, do I need a HA? Or do I just need sharding? And it's not an either or decision, you probably might need both?  So okay, so so Okay, so you're setting up the sharded cluster? We talked a little bit about the shard key? You know, how do you find out if your sharded cluster is overloading a single node or if it is imbalanced? Is there some way for us to identify that?

**Vinodh Krishnaswamy**  
Yeah, totally. That's why it's very important to monitor your sharded cluster. Okay, so PMM is a very good tool, a great tool, actually, to monitor these things. Okay. And when you're actually having this slowness in the application side, you can go into the PMM and check where your queries are going and whether you can check whether it is ending up with one shard or as if it is targeting one shard? Or is it broadcasting to every shard, for example, sometimes what happens when you are not specifying the shard key URL if your shard key is not or is the proper one, it may broadcast your request to all shards. So that would take time to gather all the data and put it into one place and do the operations for example, if you are doing shardING, or if you are doing grouping, it has to gather all the data. So it has to do all those things. And when you are getting the data to the application, it will be very late. Okay. So that's where PMM comes very handy for you to identify these things. And other than that, there is a ftDc of which is available in every MongoDB instance. So you can go on then get that ftDc data and check the data and you can see whether what happened begin to see

**Matt Yonkovit** 
So let me know, like so when we talk about that imbalance, right? So there's two types of imbalance really, right. So one is you have an imbalance with the data for that particular shard is busy. But you could also have it where the one node in the sharted replica set is busy as well. Is that correct? If you don't have connection pooling setup properly, you don't have load balancing set up properly, you could overload one node of a replica set of a sharded one. You know, data set, is that correct?

**Vinodh Krishnaswamy**  
Yeah, kind of like, for example, like, the application setup mostly is like, when you're not getting the data within proper time, it will recreate the request orders, it will recenter requests again. So when one of the shards is actually overloaded, and the application is waiting for that data, it will resend the request again. So it will create. The consequence of this is like, instead of getting the request within one shot, it will be put up over and over again. And it may grow without any infinity times. So that's what the connection pool setup or putting the cap is very important. And within that time. So when you're actually setting the Mongo connection pool, for example, that task executive pool, and when you're putting cap on that, when your application is requesting more than what it is set up, your MongoDB will not be overloaded, because your mongo is not going to get more requests than it is set. Okay, so that's why this connection pool comes in handy.

**Matt Yonkovit** 
Okay, okay. So, um I don't see any questions popping up in our chat. So I wanted to give both of you the opportunity. Like we talked about a few different things, we kind of touched on your topics. Are there things you would like to share with the community that you haven't got an opportunity to talk about yet?

**Vinodh Krishnaswamy**  
One of the main things is like a backup. Okay, so because a lot of customers

**Matt Yonkovit** 
consistent backup is a problem, especially when you have like, a bajillion nodes that you're trying to get consistent across all of them? It's a good point. Yes.

**Vinodh Krishnaswamy**  
So what happens like a lot of customers I have seen or having issues without having a proper backup, okay. So for example, having Mongo dump is they think like more having more dump is enough for them. But it's not for, especially in a sharded cluster environment, because it is important for you to take consistent backup across every shard, so that when you are doing the Restore, it happens properly. Okay, so taking backup is important. And testing is another important point. And make sure that the Restore happens properly, so that you can rely on that backup method. Okay, so that's where our PBM comes handy. That's a backup for MongoDB which is a very good tool and you can use it for replica sets as well as for your sharded cluster. So you can have multiple, you can take multiple backups with that. And even you can have an incremental backup with that, which we call it as a PITR, which is point in time recovery backup. So which attains the OP log on takes backup from our blog for every 10 minutes, so that you can restore to your up to your point, okay, and when you want to do a restore, you can restore up to your point where you want if you have that backup properly. Okay, so this is important for you to have a proper setup. So deploying the setup is not only important, having a backup is also equally important for you to restore when you have a difficult time testing the backups, right? 

**Matt Yonkovit** 
Testing the backups you don't want to test your backups Do you backup well have you tested backup? That's a terabyte?

**Ege Güneş**  
Yeah, it can be heart four terabyte backup. But right like 

**Matt Yonkovit** 
So we tell people to test your backups but if you've got a ton of data, how do you do that?

**Ege Güneş**  
So I don't think I got a terabyte backup before but I am certain minutes. 

**Matt Yonkovit** 
So it's 100 gigs to me. Right? Like so I mean,

**Vinodh Krishnaswamy**  
like I won't talk about Mongo for this, but i a i had an NDB cluster in before and it was a scary story in as you image. So we have like a 10 gigabyte backup and we test them every week, like we restart on a NDB cluster in some NDB cluster and check the latest data. And if we are okay, we set okay because there will be a time you need to restore in a rush and you will see you can't. So I think it's really important to have them have them tested but 400 gigs, a terabyte of data, I am not sure how to treat them properly in a timely manner. If you have time, it's easiest, but

**Matt Yonkovit** 
time and resources because I mean, in some cases, that's a lot of extra CPU and disk resources as well. You know, and that promotes a backup testing backup perspective, we've preached this a couple times. I've had a couple people on podcasts over the last few months, where we've kind of deep dived into this topic. But you know, when you're talking about backups, one of the other interesting things is not just about testing, it's about understanding the importance and frequency of a sound backup strategy. You know, I'm going to tell everybody, I could be snarky just ask the question. high availability and backups are two very different things. replicas are not a backup. And the thing that I see people forget, is, when you put garbage into a system, or you delete stuff in a system, those get replicated. And it's so important to understand that, because when you say my system is too big to backup, I'm just going to rely on replicas. And we have had people that I've talked to who say that they go, you know what, it takes us forever to do a backup, we're not going to do it, we've got a HA, if we have a problem, we'll just go to our replicas. And that mentality is going to lead you to many nights being canceled by alcohol and you know, crying in the corner. You know, it really is so don't do it. You know, it's very important to realize that those are two very different things.

**Vinodh Krishnaswamy**  
So one incident came into mind when you were talking about that one. So the one of this particular or cases where the customer was having a 1.5 terabyte of for uplog itself, okay, which is kind of transaction can about uplog, right? Right, right. So that collection is about like 1.5 terabyte and they had to failover the primary and they had to terminate the Mongo D. And they thought like, it would come up within like a half an hour or 15 minutes. But what happened, like it was actually doing a reading the uplog for nearly like a one week back. And it took nearly five to six hours for that particular instance to come up. Okay, this is an unexpected event. And again like, they thought, like, okay, we will have this note for a failover kind of thing. But again, for six hours, the replication was done. So you have,

**Matt Yonkovit** 
I think that this is where I've seen this before. And I like to kind of phrase it where your good intentions destroy you. Because there are so many people who don't fundamentally understand the technology that they're running, they do things that logically makes sense, right? I've got an overloaded system. Let me just try restarting it. And so what ends up happening, right, so you know, you've had this overloaded system, all of a sudden, you've got to refresh, recover, you've got to do all this stuff. Like, like, and you take a problem that might have been a problem and you make it 10 times worse. Yeah, I've seen that so many times, right? It's it's, it's crazy how often that happens. And it's that over engineering or overthinking that the solutions sometimes patience is the best option. Even though no one wants to be patient when some of these problems happen. Other times you're gonna have to, you're gonna have to bite the bullet and do some things that might be a little risky when it comes to restarting or doing some other things. But yeah, I mean, I understand that if you've got a 1.5 terabyte uplog, that's gonna be some nasty stuff. Yeah.

**Vinodh Krishnaswamy**  
Talking about disaster stories I want to tell other things that can use a it's cross-region replication. Besides migrating to Kubernetes, you can also configure a Kubernetes cluster or if your primary is in Kubernetes, you can configure it as a regular PSMDB cluster as disaster recovery sites. Right now it's not automatic in the operator but we have some plans to do that. But if you configure these two clusters or more than three a to even a and the primary is it fails in some reason like hardware failure or network failure. You can failover to a replica cluster you need to do some stuff to failover to configured replica sets because you have most of the most will be gone and you need to do some forcing to move a replica set coffee after the manual intervention you can have a relatively up to date data up and running easily with this new features of PSM DB operates.

**Matt Yonkovit** 
So you're talking about you have the cross geo setup, but then you can also failover the replica set so it's like a double failover

**Vinodh Krishnaswamy**  
and you can you can make a some notes be selected as primary and replica clusters and maybe you need to update your client applications to use that's a new primary or maybe you have some a stuff that you can move the IP to a to to the new cluster to new replica clusters and you can have this disaster recovery a scenario

**Matt Yonkovit** 
awesome All right. Well it looks like we don't have any questions in chat today. That's okay. I want to thank both of you for swinging by we're gonna go off now to our all company meeting here at Percona and we're going to celebrate the retirement of Tom Basil, a long time perconian, so we're gonna have some fun with that. But we appreciate people watching this and hopefully you know, there were some interesting tidbits for you. Feel free to reach out over discord or over chat if you have questions. And if you have ideas and things you want to see in future meetups, we'd love to hear about them. Alright everybody, thanks.

**Vinodh Krishnaswamy**  
Thanks. Bye



![Percona MeetUp for MongoDB Sept 2021](events/percona-meetup/mongodb-cover-1920.jpg)

MongoDB is a database which came into light around the mid-2000s used by companies and development teams of all sizes. The Percona Head of Open Source Strategy - HOSS - and experts organize a series of regular live online streaming Community MeetUp for MongoDB to share their knowledge and to answer attendees' questions.

Join for an hour MeetUp for MongoDB

* Day: Wednesday Sept 22nd, 2021 at 11:00am EDT (5:00 pm CEST or 8:30 pm IST)

* Live streaming on [YouTube](https://www.youtube.com/watch?v=s7v8hAC55iw) and [Twitch](https://www.twitch.tv/perconacommunity)

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=MDdsOWozZ2dxZ2Rxcmg1czhja2RiNjZ1cTUgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

## Agenda

Our experts will cover following topics:

### "MongoDB sharded Cluster - best practices" by Vinodh Krishnaswamy
1. How to deploy a cluster for proper HA
2. How to use Balancer effectively
3. The most common issues that people run into when or when not sharding MongoDB

### "Cross-regional replication for MongoDB with Kubernetes" by Ege Güneş 
1. Technical implementation of the feature
2. How to migrate your MongoDB cluster to the Kubernetes?
3. How to set up a disaster recovery site on Kubernetes?

## About event
The Percona Community MeetUp is a Live Event and Attendees will have time to ask questions during the Q&A. All kinds of feedback are welcome to help us improve upcoming events.

The MeetUp for MongoDB is recommended for: 

* User of MongoDB

* Student or want to learn MongoDB

* Expert, Engineer, Developer of MongoDB

* Thinking about working with database and big data

* Interested in MongoDB


Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=MDdsOWozZ2dxZ2Rxcmg1czhja2RiNjZ1cTUgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

Turn on the YouTube reminder on the [YouTube](https://www.youtube.com/watch?v=s7v8hAC55iw)