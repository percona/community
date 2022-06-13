---
title: "Database Performance, Availability, and Operations – Percona Podcast #60 /W Yunus and Kedar"
description: "Listen in on how they go about bringing stable performance, availability, and operations to new databases brought online"
short_text: "Yunus Shaikh and Kedar Vaijanapurkar are two of Percona’s Managed Service DBA’s, they help stabilize and manage 100’s of different customer systems.  During our podcast listen in on how they go about bringing stable performance, availability, and operations to new databases brought online.  Also hear about some of the tools and processes they rely on to stabilize environments."
date: "2022-04-29"
podbean_link: "https://percona.podbean.com/e/database-performance-availability-and-operations-%e2%80%93-percona-podcast-60-w-yunus-and-kedar/"
youtube_id: "P0zIf2Bwwts"
speakers:
  - yunus_shaikh
  - kedar_vaijanapurkar 
  - matt_yonkovit
aliases:
    - "/podcasts/database-performance-availability-operations-percona-podcast60-yunus-and-kedar/"
---

## Transcript
**Matt Yonkovit:**  
Hi, everybody. Welcome to another HOSS Talks FOSS. I'm the HOSS, Head of Open Source Strategy here at Percona, Matt Yonkovit. Today I'm here with Kedar and Yunus from our Percona team or our managed service team here at Percona. How are you two doing today?

**Kedar Vaijanapurkar:**  
Hey, I'm doing good. How are you?

**Matt Yonkovit:**  
I'm good. And I always like to talk to the folks here at Percona. Because as the team has gotten so big, I mean, and now we're well over 300 people, it's always hard to get to know everybody. And so just sitting down and understanding what everybody's working on what they're seeing. It's so valuable. It's so interesting. And so I'm excited to be able to have this discussion with you, too. And so, so let me start with Yunus. You've been here for a while Yunus Shaikh a few years now. Right?

**Yunus Shaikh:**  
Yeah, three years now. And so three years already completed enough

**Matt Yonkovit:**  
 Yeah. I've been here quite some time. But so you kind of had a lot of different roles before here. You were a bit of a sysadmin. You were a bit of a network security person. You were a bit of everything in your background, right?

**Yunus Shaikh:**  
Yeah. Yeah. I started my career in 2007. With the system and network admin, and then from windows, I switched on to Linux. And then when I came into the Linux, I started using MySQL database, I got interested in MySQL database, and then got the total career into MySQL now, after joining Percona.

**Matt Yonkovit:**  
Yeah. And so jumping into the Percona side, how was working at Percona different from working outside of like, how was that transition? Was it kind of jarring? Was it challenging?

**Yunus Shaikh:**  
Yeah, so remote work is like, totally Well, it was not new. But still, we, I had my previous companies who are allowed to do work from home for like, four days in a month, or maybe one week in a month. But working totally remotely is a different thing. Totally. And, like, here we can enjoy. Like, we can stay with my family, we can stay with the family and just keep on working. There is no, as the working in Percona is totally different from working in an office, right? We are at home , and we don't have anything like, we can do whatever we want. And we can manage our work when we can manage our time there is no there is nothing like we have to spend more than eight hours in a day , and we just want to complete our eight hours and just really live it and that that's what I like to from Percona that it is like very professional, remote working company.

**Matt Yonkovit:**  
Kedar, you're kind of the younger generation here. You've only been here a few months, right?

**Kedar Vaijanapurkar:**  
I've been here for four months, only four months.

**Matt Yonkovit:**  
Four months. So how did you come to Percona? Like, what was your start as?

**Kedar Vaijanapurkar:**  
Yeah, actually, my start was like, I was working on .NET platforms again, just like you said, on Microsoft side. And then a friend just was going on some new adventure. And I was like, Okay, let's do something. And I started with PHP, and all those things. And then somehow I learned MySQL and that's how when things grew further, I got into MySQL that way. Before coming to Percona I was like at Pythian almost nine years. And obviously, it was like, say, first remote job for me. And I found many interesting minds there.
I see inspiring people. And I learned a lot from there I guess , and I think everything we were using, there were a lot of things where Percona like Percona, tools and Percona. And you read Percona blogs, obviously, like, I do not know, if you're not reading Percona blog, what are you doing here? So, well, I thought of, okay, let's level up. And as far as I know, a lot of people here in Percona, where they're in Pythian, and where they're in other community companies, which are active in community, their companies, which are active in communities. So I think it was interesting to**Yunus Shaikh:** move here. And since I'm here in the past four months, I feel I say, as I said, it's a level up for me, with respect to the work with respect to the culture as well, I guess I didn't know the cultural difference here. And I think I met really well. And see, which is very important empathetic people who are who really care about, as Yunus said, the work-life balance, who do care about that. So I think I made a really nice choice. It was a good decision to move up here at Percona.

**Matt Yonkovit:**  
So you could be honest with me, though Kedar, the thing that you really wanted to do was come work with the HOSS right, like, all those videos of yours, all of the podcasts, you were like, I gotta get on that.

**Kedar Vaijanapurkar:**  
Not like that. I actually changed my line from Microsoft  to the open source community sites, just to meet you.

**Matt Yonkovit:**  
Okay. Yes. It is good. It. Thank you. I knew I had some responsibility for this. So 

**Kedar Vaijanapurkar:**  
I would say if you're in Microsoft, Oracle, any other technology, come join MySQL, come to  Percona. And your life will change

**Matt Yonkovit:**  
Yes, there you go. So, um, so you've been in this industry Kedar for quite some time as well. And I'm curious, and I'll start with you. And then we'll ask you the same question. What are you seeing on a regular basis? As you help to maintain these sometimes massive MySQL environments? What are the normal, common problems that you run into? What are some of the challenges that users are facing nowadays?

**Kedar Vaijanapurkar:**  
Well, that's a question I would need to think about a bit. But

**Matt Yonkovit:**  
So you want to make units answer first, and then you come back.

**Kedar Vaijanapurkar:**  
Oh, I can think a bit. And then I can say that, but it's like, see, on a day-to-day basis, very regular issues are about the way they have configured or say the users have configured their servers, which are very basic things, then, probably they have underestimated their traffic, probably the developers, which were not really efficient in writing their queries, or even designing their tables, which are so many so much basic things, which are like, one on ones of MySQL, which one should know, really, and when those things reduce to production, those are the things which really reduces your performances. So those are the issues we see more often, which are related to performance, and then we go forward from them, then we decide upon, okay, now you have performing servers. Now we think about how to get a step further. Okay, let's think about high availability. Think about monitoring, obviously, that comes first. But if it is not about performance, what will you do about it, then we will check about their status is how they are working. And so I think the basic issues come most often. And then when the work goes further, in the line, the way we work here is about reviewing their systems and their architecture. And then we go ahead and decide how we suggest our client with the best practices or whatever running in the industry right now. Which tool we are using, and how to go ahead with that.

**Matt Yonkovit:**  
Yeah, and so you start with fixing the problems that exist, but then enhancing the overall platform over time to bring it more into line with some of the best practices. That's right. And Yunus, what are you seeing, from a customer perspective, a user perspective, that's common issues.

**Yunus Shaikh:**  
So whenever the client comes in, get onboarded. In Percona, we most, the first priority is to stabilize their environment. So we review the servers as Kedar said that we will review the server's review what problems they are facing, how the traffic is and during the peak hours, how stable their server remains, and if there is any problem in the queries in optimizing this was like optimizing MySQL and we collect all the information in the initial stage and then we suggest what all improvements that can be done. So once the client is stabilized, then we, we recommend them for the improvement further like if we need to maintain high availability in their environment, how what all we can add in their environment, and then how the backups need to be there, or whether it should whether it needs to be uploaded offline for more safety during a crash or staging testing environment, then we keep on recommending and making the environment healthier. 

**Matt Yonkovit:**  
The thing that I would like if you could tell all the users out there before they become customers to fix this one thing, just fix this one thing, what would you tell them to pay attention to and fix now before they become customers? Or before it becomes a problem? Is there one thing that they should focus on that's overlooked? 

**Yunus Shaikh:**  
One thing they should focus on is the bad queries.

**Kedar Vaijanapurkar:**  
I would add one, add an index to your InnoDB tables, primary key add a primary key to InnoDB tables.

**Matt Yonkovit:**  
So both of you can answer this in whichever one feels comfortable. And here's the thing that I've experienced more often than not, you mentioned performance issues. You mentioned scalability. Kedar, you mentioned like the design side of things, when you do have a problem in the design side, it is much more difficult to fix that than if it is a configuration issue. Or if it's adding a new tool, necessarily to the environment. Because you have to fix the code, and that means you're gonna have to rewrite things. If you have to increase the memory allocation or tweak the TCP buffer, or the disk IO or things like that, those often can either be done live, or they might require a restart, but it's a single restart. Whereas when you have a design, change, if you're going to redesign your tables, if you're going to rewrite all of your queries, that requires all the teams to work together to make that happen, it's no longer, I'm going to make this adjustment, I'm going to focus on it. So in my opinion, like I've always looked at the design side of the database as probably the most important because if you get that wrong, it's so hard to change it later. So, is that something that you see often too, like, how long does it take, when you find that design issue? How long does it take people to to generally fix that?

**Yunus Shaikh:**  
So, the database design issue, if we have not come across this situation much, but I think if this design problem is there, then it will surely take more time to solve because we need to analyze the whole database to normalize it means if there is anything duplication or not getting stored properly, or the queries while pulling are taking longer times because of the database design, then we need to fix that design first. And it will surely take time because if the database is not properly designed, your application won't function properly, right. So, and there will be of course, a downtime if the database design has problems. And then for fixing that, again, it will require another downtime. So that will be like creating, like totally fixing it from A to Z it will be required if the design problem is there to understand it and then fix it.

**Matt Yonkovit:**  
Yeah, I mean, like, yeah, definitely a lot longer. And I mean, there are different levels of design issues, like obviously, schema design, or adding columns is an impactful thing. But I mean, also design of the queries. And indexes are also critically important. I mean, I think nowadays people really are looking for three things, right: They want the scalability, so they want to know that if they have 100,000 users, it's gonna work. They want it always available, right? Like there's no downtime, you can't have downtime, like name one website that can have downtime, none, although they take it and then they want their data to be protected and secure. Right, like so if you're available and scalable and secure. I think most people are happy. So go ahead, Kedar. Are you gonna say something?

**Kedar Vaijanapurkar:**  
Yeah. Since the invention of the cloud, like the Google Cloud or AWS cloud, like their technology, which has, which has, like, allowed opportunity for people to stop thinking about scaling problems, and just try to develop their whatever coming through their mind as a product, and then just give that in, like, give them an incredible amount of resources, like they do not care really, as long as they are ready to pay, you can just scale it out. And you can add things on top of it. But as you say, like the design issue, which is not only up to the database side, it also belongs to the application side. And if it is not thoroughly tested beforehand, moving to the production, and then oh, I forgot, we also needed a Date Time column so that we can update on based on that, that will take you back to the development cycle, then the staging, and so forth, so on. So that's like, that's going to waste a lot of time there. So yeah,

**Matt Yonkovit:**  
Yes, definitely. Well, I'm gonna try something with YouTube, because I want him to have one person on, but now I have two, so you get to be a guinea pig to try something new.

**Kedar Vaijanapurkar:**  
Yeah, sure. Okay.

**Matt Yonkovit:**  
Kedar, what's your favorite MySQL tool? 

**Kedar Vaijanapurkar:**  
The MySQL client.

**Matt Yonkovit:**  
Okay. Okay. Yunus, what's your favorite MySQL tool?

**Yunus Shaikh:**  
Pt online schema change

**Matt Yonkovit:**  
Okay, so I mean, like the MySQL client. I don't know if you can consider that a tool?

**Kedar Vaijanapurkar:**  
Well, it's an application. It's not the server. Right. 

**Matt Yonkovit:**  
It's not the server. But I think that the like, from a win perspective, I would think Yunus' answers are much more solid with the Spirit. Winning tool. Okay.

**Kedar Vaijanapurkar:**  
I was going for the controversy. 

**Matt Yonkovit:**  
Yeah, you were going for the controversy. Okay. So if you're going to back up a large database, okay, large terabyte size. How are you going back it up Kedar?

**Kedar Vaijanapurkar:**  
XtraBackup.

**Matt Yonkovit:**  
Using what, like, are you going to do differentials? How are you going to do point-in-time recovery? What are you going to use?

**Kedar Vaijanapurkar:**  
Ah, okay. Yeah, I mean, like, it's really, really large then probably I would do a full backup once a week and then incremental backups thereafter.

**Matt Yonkovit:**  
Okay, Yunus, any response? Anything you want to add to that?

**Yunus Shaikh:**  
Yeah, so. So the very best tool available is XtraBackup for the big database. And, of course, a full backup is needed at some point of time. And then we can do incremental for a few days. And then, for point-in-time recovery, we can keep taking a binlogs backup. And so, if there is anything point in time recovery needed, we can use the bin logs backup as well. And, yeah, that should be good. I think the logical backup will unnecessarily process a long time. So we won't actually have a logical backup.

**Matt Yonkovit:**  
Okay. Good, good answer. So, so now I'm going to ask you have to build high availability, are you going to build PXC or are you going to use orchestrator and async replication?

**Yunus Shaikh:**  
So, that depends totally upon the application. Sorry, Kedar; if you want to,

**Matt Yonkovit:**  
Yunus, you started getting the scope to go for it. Yeah,

**Yunus Shaikh:**  
No problem. Yeah, I can do that. So, it depends totally on the application users for example, like, if if the application has a long-running update or any, like long-running delays, updates anything. So, this will cause a problem if we are using PXC. So, choosing between PXC and choosing in between a synchronous and synchronous replication is just a matter means what you want actually, how is your application functioning. So, long-running updates, for example, will take a long time to finish on the first node. And if we are using PXC, it will again run on another all the nodes. For example, if three nodes cluster is there, the two nodes will again run the same updates and for example, the first node took two minutes and the other two nodes will take two minutes for that two minutes the cluster will just go do the flow control right. So because of that the PXC for for long-running updates applications, the PXC will not be suited. So they will always try to choose asynchronous replication. So these long-running queries are coming mostly from the reporting server not from the application actually, some people prefer to try it to build their replication and then try to use the analytics server or some server in the below chain, like for example in, they have set up asynchronous replication and then try to run the long-running queries in the below chain. And then there is another chain going on. So depends upon the usage of how the application will be, for example, if there are no long-running queries, I would prefer with PXC as well. So because it is all, it is also a good solution of high availability.

**Matt Yonkovit:**  
Kedar, do you agree? Do you disagree?

**Kedar Vaijanapurkar:**  
I don't disagree with him.

**Matt Yonkovit:**  
You guys disagree

**Kedar Vaijanapurkar:**  
We do not really, you cannot make us fight. He's an old ship here. Right. So I need to learn about his way of working.

**Yunus Shaikh:**  
If I'm wrong, please correct me.

**Kedar Vaijanapurkar:**  
I completely agree with him seriously, there is an additional advantage that PXC gives us with the consistency like let's say if some table is dirty, like, say inconsistent, maybe. Maybe there is some data that is missing, or somebody that feels it just discards it, and recreates it. That is something that intelligence really likes, you don't need to like an asynchronous replication, you just throw something at this replica and expect it to pick it up. And then you get duplicate key error, and then all the surrounding mess. And then you go ahead and use Yunus' favorite. No, I probably there's a second favorite tool for Yunus, pt checksum. You use them and you tried to sing them. And if it is large, Oh, okay. So PXC is smart enough to discard the naughty things out of the cluster, let it rebuild, and get refreshed back. So I think he has very well explained the solution there.

**Matt Yonkovit:**  
Okay. Okay, so you are ready for it? What was the best release of MySQL? In your opinion, is your favorite release? Do you have a favorite release? Like, when it reached 4, 4.1, 5.1, 5.7? 

**Yunus Shaikh:**  
I think the best one was 5.7. Very good for InnoDB. And then, but there are a lot of improvements in 5.7.

**Matt Yonkovit:**  
Yeah, yeah.

**Kedar Vaijanapurkar:**  
I say 5.0 because that's where I started. Okay. But yeah, I think the time when they introduced online schema change, that was really sort of interesting when they made InnoDB as default and engine and introduced online schema change. 

**Matt Yonkovit:**  
Great. Okay, well see, that was what I was gonna try. It was just rapid-fire kind of like topics thrown off the top of my head. We call it the Percona popcorn hour, because it's just like popcorn popping out of my head. I don't know what to

**Kedar Vaijanapurkar:**  
It is interesting, the way you prepare this and handle this.

**Matt Yonkovit:**  
What just by randomly thinking of things, and then throwing it out there and see what happens. Yes, yes. My preparation? Yes, we all have our methods, you never know where it's gonna go. You never know, you could tell me something that I might spend the entire hour on just the one thing, right, I might spend two hours on it. I don't know, I really don't know where this is gonna go. You just never know. But both of you have an upcoming talk. Or, depending on when this podcast is released, it might have been a previous talk. Yunus Shaikh we're recording this before Percona Live. But we do release them once a week. And it's on using orchestrator and using proxy SQL with asynchronous replication. So we talked a little bit about the difference between when you might choose async, and PXC, which is a good segue into this conversation. So I am curious , but prior to Proxy SQL being there, there were all these different tools. Oh, with an eminent the title to handle some processing and the routing of queries and the routing of traffic. What's your experience been with proxy SQL? Have you used it for more than just Orchestrator? What are some of the things that you might have seen it used for out there?

**Yunus Shaikh:**  
So, Proxy SQL. So we were talking before about scalability, right? So, scalability like Proxy SQL will support it very nicely. Proxy SQL is again, a very good tool for, like, if we point the application we don't have a point application to proxy SQL it will automatically split the queries with Read and Write as well. So in terms of scalability for example like, if we are using Proxy SQL in our application, then whenever we want to grow our reader servers, we can always add the keep adding the service. And the reader service will keep on increasing the readers just like we do in RDS, and Aurora, like increasing the readers. And that is, again, one advantage and then splitting the queries on the basis of query digest. For example, if there is a long-running query, you would just want to put on that server, you can do it. These are all advantages of using a proxy SQL. It also very nicely integrates with the orchestrator as well. When we do a failover with orchestrator, it automatically picks up like a proxy SQL is configured to automatically change the writer to the rewrite server, and it automatically chooses the new server as retry table and put it in the host group. And so the rights will go on that server, and then read will come start coming on the old master. So we don't need to make the changes manually in the application. And we are just only pointing to Proxy SQL. So that is also the main advantage that we don't have to change anything in any configuration in the application.

**Matt Yonkovit:**  
Yeah, so it's really helping to route the queries to the right place. And you can define what you're going to do once that traffic comes in, where to send it, how to handle it, adjust it, and make modifications to it if you need to. Now, you mentioned the orchestrator. And Kedar, I'm gonna ask you this. For those who are listening or watching who don't know what orchestrator is, maybe give us like the 10. Second, what is orchestrator?

**Kedar Vaijanapurkar:**  
Well orchestrator, you can assume it as a not as it is a replication topology Manager. Once configured, it will let you visualize actually, very well what is there in your environment master replicas there; it will allow you to very easily migrate them, I mean, a change that it will allow you to change the topology just by drag of your mouse and it will take care of the rest, it will also take care of stopping the replica, the demoted, Master, becoming the new replica and make it read-only. And make sure that the new master that has come up as read-write enabled so that the traffic can continue growing, moving while you work at it. So that's the orchestrator.

**Matt Yonkovit:**  
Yeah, so really, the combination of proxy SQL and orchestrator is really DevOps for DBAs. Really, it's automation of your failover is the automation of your query routing automation of some of those normally, backend activities that require a lot of work.

**Kedar Vaijanapurkar:**  
Yeah, that's right, it allows you to, as you said, about Proxy SQL, it allows you to integrate his hook scripts to perform whatever additional changes you want to perform after failover is rejected, or whatever keys or options are there. So you can take your actions accordingly. It is also nicely yet integrated with the console. And, and one more thing, which I'm forgetting, but it communicates fluent flawlessly with them and populate the information with it based on the Defined key values, pairs, and above all, it has also implemented the raft protocol clusters. So that it is also the tool itself is also say highly available, like if one orchestrator dies, you do not have to worry about the topology manager is still there it is being managed by two other like you say three is a minimum. 

**Matt Yonkovit:**  
Well, so you two are giving this talk, which is that Percona Live, if Percona Live has not happened, we encourage you to come out and check it out. And if it has, there shouldn't be a video that's available for you to stream if you are interested in more details on that. But Kedar and Yunus, I wanted to thank you for coming out chatting with us and telling us a little bit about the DBA team here at Percona. Sharing some of your experiences, answering my crazy wacky top of the popcorn questions always happy to have folks on and chat with me about whatever topics they're interested in, or whatever pops into my mind, you never know. Might not even be database-related in the future. I don't know. But I wanted to thank you both for hanging out with me today.

**Yunus Shaikh:**  
Thank you, Matt.

**Kedar Vaijanapurkar:**  
Yeah, thank you. 

**Matt Yonkovit:**  
All right. It was nice talking to wonderful. 


