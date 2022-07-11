---
title: "All Things Opensource Data Warehouse -  Percona Database Podcast 72 /w Robert Hodges"
description: "Robert Hodges, CEO at Altinity, joined Matt Yonkovit, The Head of Open Source Strategy at Percona, in this open-source database podcast. They started with how Robert get started and how the Database has evolved along the time that brought him to ClickHouse/Altinity. Robert gets deep into Opensource Data Warehouse with some details behind Clickhouse. As usual, enjoy the session of rapid-fire questions to know more about Robert"
date: "2022-06-07"
podbean_link: "https://percona.podbean.com/e/all-things-opensource-data-warehouse-percona-database-podcast-w-robert-hodges/"
youtube_id: "U9OrBfrBwis"
speakers:
  - matt_yonkovit
  - robert_hodges
---

## Transcript


**Matt Yonkovit**  
Hey everybody, welcome to another HOSS Talks FOSS, I am the HOSS Matt Yonkovit, Head of Open Source Strategy here at Percona. And I'm here with Robert Hodges from Altinity. Robert, how are you doing today?

**Robert Hodges**  
I'm doing great. Thanks for having me on the show, Matt.

**Matt Yonkovit**  
It's wonderful. Now, Robert, you have been in the open-source space for a long time, you've been around the database space for a long time. I remember back in the days, you over at continuant, and you've kind of evolved into Altinity. Now, how did you get started thinking about databases?

**Robert Hodges**  
 it's I was in the military, and from 1980 to 1984. And about halfway through, I was working as a programmer for so-called Air Force Intelligence. And about halfway through by my hitch, our unit bought a database, it was called M204. And, to make a long story short, it was the coolest piece of software I'd ever seen. All I could think of was when I got to get a job. The company that wrote it, it was a company called Computer Corporation of America and Cambridge, I didn't get a job, I ended up going back to the University of Washington. And instead, a few years later, I got a job at Sybase. That was my first industry job, and where I really learned, began to learn databases, and it's been fun and, and interesting, and, and ever since.

**Matt Yonkovit**  
 Well, the database industry has evolved immensely over that time period. I mean, we have gone from a very multipurpose database you mentioned Sybase or Oracle, where you kind of have one database, and it has to do all different kinds of workloads to now write almost a database for every workload.

**Robert Hodges**  
That's, that's right. Although what's funny is, yeah, there's just this huge, well, there's a huge number of ways that you can access and use data. And, in fact, the first database I worked with them to afford was pre-relational, as some call it inverted file access method. Didn't have SQL, actually programmed it using COBOL, which was kind of interesting. But yes, so in the 90s, that was sort of the heyday of the relational database that as you say, the singing-dancing, SQL database, but even then, there were, there were other databases contending against the relational model, for example, I worked on something called Brahms, which was an attempt by Sybase to rewrite their flagship SQL Server database into an object-relational database. I didn't succeed. And as a result, Sybase kind of faded away. But there's always been this, these, this constant sort of efforts to bring in new technologies, I think we're things really changed in the first decade of the 2000s, with the advent of NoSQL, eventually consistent, eventually consistent databases. And at that point, we, and very, very large amounts of data, and that's something that I think shifted move the needle, and got people looking much more seriously at other sort of non relational databases, and then new ways to do relational databases as well.

**Matt Yonkovit**  
So what kind of brought you to ClickHouse, like as Altinity, that's their expert area of expertise, like what kind of led to that?

**Robert Hodges**  
 It's actually really simple. One of my best friends is a guy called Alexander Zaytsev. And I've known him I think we met in 2003. In St. Petersburg, it was like about four, maybe five companies ago. And he was running a lab in Moscow. And I was a manager for the product that his team was working on. So we got to be friends. We moved on to other companies and remained friends and a few years. A few years ago, he said to me, Hey, Robert, I know you like databases, there's a really cool database you need to come to look at. And at the time, I was working on VMware, it was after we had sold continuant to them. And I was sort of like, yeah, yeah, sounds great. I'm busy here, which and but I eventually came and looked at it. And sure enough, it was really phenomenal. It's, it's a really, really great database. In fact, the best way I can explain it is it's kind of like MySQL, only it's for the analytic queries. So MySQL is great for transaction processing quick queries, and very high rates of concurrency ClickHouse has a lot of the same things that make MySQL, great. Like it's just one process. It talks. It's open-source. It talks in a really friendly dialect to SQL, but it works on analytic queries. So once I got into it, I got hooked and I ended up leaving VMware, working for free for six months for Altinity. And then just really getting sunk into this great, really wonderful database.

**Matt Yonkovit**  
Now with classic open source, there are many different deployments and use cases people do some crazy eclectic things with open source right. You never know what kind of weird things wild things cool things are gonna happen. I'm curious, like in your experience, how have you seen ClickHouse be deployed? are there some really interesting examples that just kind of jump out and like, wow, I never would have thought of that? But it's kind of cool.

**Robert Hodges**  
Yeah, absolutely. In fact, what's kind of cool about about analytic databases, and in particular analytic databases like ClickHouse, is they actually enable entirely new businesses. And I'll give you a couple examples. One, there's a company called MCSE, which has a video content delivery network, they are the good people that bring you the Super Bowl when you're streaming it on your browser. Now, what they do is, as those downloads are streaming across the internet, through their content delivery network, they're collecting a bunch of metrics that like, hey like, are you doing rebuffering? Do you have errors? are is there like, do you know what do you appear to have capacity problems, and that stuff is being fed into a data warehouse in real-time so that as the folks are running the Superbowl, they can actually go in check the quality of the streams that are being delivered to all their users, identify problems, find the root causes and fix them in real time. This is something that simply wouldn't exist without this database, without a database like ClickHouse that one can load this data really quickly, and two give you answers back in a second or less, so it's an entirely new business. Another one is, is real-time marketing. So there are you'll go to a website, after a while, they'll say, Hey, do you want to have a isn't it time you took that pop up or took that ad blocker often signed up for the website that may be backed and is in some cases by a data warehouse that is loading data, in real time. And then where they're asking questions, literally, as a page is rendered, to say, Hey, is it time to put that is it time to ask them to become a member. Again, a business that wouldn't exist without this technology.

**Matt Yonkovit**  
But, Robert, now, hold on. So you're telling me that you are behind those annoying pop-ups that say, like, remove my ad blocker? Is that what you just said?

**Robert Hodges**  
it's a yes, I know. And this is something I have to explain to my children, that I'm making the world a better place by enabling ads and things like that to be shown more quickly and efficiently. But it is interesting that what you are seeing here is that businesses are dependent on being able to analyze what's happening in the real world and react in real-time. And I'll give you a much more serious example that I think is, is probably more relevant. And I think is obviously a little bit clearer that it's a benefit to users at large that security. So one of the things that happen is if you have exploits going on, you may suddenly see a like a service running out in the cloud, all of a sudden making DNS requests to a server that's, that's known to contain malware. So what happens in security systems, and we have a bunch of these folks as customers are, that they're loading logs. And what they're doing is they're then scanning these logs in real time and looking for unusual patterns of use. Again, being able to end And so what's critical is when you're, when you're running these systems is two things. One, you must be able to scan that load and analyze the data very quickly. And then when you actually detect some sort of exploit that may be ongoing, you also need to be able to look not just at the stuff that happened in the last five minutes. But going back into history may be going back up to a year or more to understand the context and how what you're seeing now developed over time. Datawarehouses like ClickHouse which operate in basically give you real-time responses across enormous datasets allow you to solve this problem. And I don't say I can't think of anybody that wants things on the once things on the internet to be less secure so this is really wonderful use case and again, one that the ClickHouse enables.

**Matt Yonkovit**  
No, and I mean, I think as technology has advanced we've gotten an insatiable appetite for real-time data. Nobody, nobody has patience. Let's be honest, we lacked patience.

**Robert Hodges**  
That's right. It's there's like one of the early users or ClickHouse, they used to have a problem that they would describe as, hey, it's just too much We'll figure it out. In other words, I would be sitting there for like an hour to run a query to find something. And by the time that query gets back, I've forgotten what I even asked. On the other hand, if you could ask questions as an analyst and get like about security about your network about marketing problems when at web analytics, and if you can get an answer back in two seconds, that's an entirely different level of, of engagement that you can have with data and allows you to develop sort of recursively develop real insights into your business.

**Matt Yonkovit**  
Yeah. And I think that as we have moved into this environment where everybody wants things now, they wanted immediately, we've also had this inflection point where everybody has their own little piece of the pie, everyone's using microservices, everyone has their own little databases, their own little infrastructures, which means that now we have all of our data, we have more of it in all kinds of different places. So we've taken the data that we need, and we spread it out across 10,000 systems. So the analytic systems, whether it be ClickHouse, or something else that can pull those together and analyze them quickly and efficiently, I think is a key part of that infrastructure.

**Robert Hodges**  
They are absolute, because a lot of what that it is exactly as you say, you need to fetch the data out of sometimes 1000s, or 10s of 1000s, or even hundreds of 1000s of sources, put them in a single place where you can start to ask questions. The other thing is that we're starting to see analytics, particularly real-time analytics embedded in just about every application. And this is the other thing, where were these open source sort of very capable open source. Data warehouses are really wonderful because remember, when MySQL arrived, it enabled millions of people to run relational databases, you can't say it didn't really take, it didn't really take business away from Oracle. What it did was said, hey, everybody who runs a website can have MySQL backing it up. And so so the same thing was happening with data warehouses, that every application that wants to present analytics to their users, they can now have one of these open source databases sitting behind it, and they can give people this access to this information that they need.

**Matt Yonkovit**  
Now, Robert, I know, we are a bit short on time today. But I'd like to kind of go into rapid-fire mode on these podcasts and let a few questions fly and see what comes of them. So I want to move to that phase real quick here and throw some interesting and odd questions at you. So number one, let's just start with what was the best last book you read?

**Robert Hodges**  
The last book I read? Actually, I can tell what I'm reading right now. Okay, it's the Wii comp to brag Milan, by Dumas. So and I'm right in the middle of the the various machinations of the courtiers at the court of Louis Quatorze, the Sun King, and it's a wonderful book, I've been reading it for I was on a business trip to Armenia. I've been reading it in one plane after another and now, I'm sort of reading it at night when I wake up from jetlag. That's my current book.

**Matt Yonkovit**  
Okay. Okay. Well, that is a first I haven't had anybody say that on the podcast yet. So you get the cake for that one. Now, if we are to meet up and we will in a couple of weeks in Austin, and you talk and people are come up and say, Hey, let me buy you a drink. In here all about ClickHouse. What drink? Are you going to order? What is the beverage of choice? Well, there's no question that a double IPA, but double IPA. Okay, if it's available? Yes. Okay. Is there a particular IPA that you're looking for?

**Robert Hodges**  
Actually, that's a great question. It will, in that case, always be something local. So I don't know the name yet. It's going to be an Austin, I don't want to drink the Sierra Nevada or something like that. That's we've got that in California. I can get that any day. I want to see what the I want to see what people are drinking in Texas and try something new.

**Matt Yonkovit**  
out of all of these technologies that are out there, out of all these different things, what is the most exciting thing that you see out there that you're really interested in that you think is going to revolutionize the technology space?

**Robert Hodges**  
Well, I'm kind of hoping it's Kubernetes. Yeah and this is funny because Kubernetes gets a huge amount of hate. Because it's complicated. And but what I think is interesting is that right now we have this huge pendulum swing to the cloud, which is basically centralized computing. And but this, we've seen this pendulum move back and forth over the last few decades of computing. And the thing is that there are in fact, an awful lot of applications. Since where people like to be able to choose where they run them, they don't necessarily want to pay huge bills to Amazon, they have security reasons for running in a particular place in a particular way. And they may have data that is resident in a particular location. Kubernetes is a way of having a common platform that just works everywhere. There are some things about it, like networking sort of external networking, they're different. But in general, if something were if an application runs on Kubernetes, running my closet, which is about 10 feet, that way, it will run up in Amazon, it will run on digital ocean, it will run pretty much anywhere you want. So why is that interesting? Well, I think we can run databases now. Anywhere that we want, but still have that cloud experience. Everybody wants the ease of use of the cloud, and they want the ability to spin things up, spin things down, not have to really worry about all the underpinnings, but they also want the freedom to run it wherever they need to.

**Matt Yonkovit**  
It's a very common answer. I mean, a lot of people are excited about what is happening in the Kubernetes space, and how that's evolving. I think that's something that we all are paying attention to.

**Robert Hodges**  
Right. Right. And I think that just within the database field, I think then thenre's just there's one of the things that is just been really amazing about databases is the innovation just doesn't stop. So we're continuing to see, like in data warehouses, we're, we're seeing the evolution with ClickHouse, we're seeing SQL evolve, we're seeing the ability to deal with structured and, and together with semi-structured data. every time you turn around, there's something new. So I'm really excited in particular about the way that databases are evolving, and then enabling new types of businesses, and enabling people to solve new kinds of problems. So that's also something that really excites me. I've been doing this for almost 40 years, and it never gets old.

**Matt Yonkovit**  
If there is one thing that you can get through to IT folks maybe VP CIO CTOs. If you could tell them one thing that they need to fix or focus on or not avoid, what would that thing be? What's that big issue that they should be thinking about?

**Robert Hodges**  
Yeah, so what would be the big issue? That's a tough one. Because there are so many things that if you build systems, there are so many things at any given time that are broken. I think that one of the things that I see and think about a lot, is, how much should I be, depending on SaaS services, I hope this doesn't sound too obscure. But right now, it's really common to say, Hey, I gotta get out to market. So you end up building a system that works, but it actually works, because it points to 13, or 14 Different SaaS services that you've connected to. This is a complete rat's nest. And I think what people it's kind of like the supply chains that you had for things like the Boeing 787 project, which kind of undid came on done because they had such a complex supply chain, we're seeing this in software supply chains. I think people some of the events that are going on in the world today, are beginning to make people think a little bit more about the software supply chains. And just do you really want to build these applications that have all these entangled connections to services running all over the internet? I think actually, the answer to that is no, we need to build systems that are simpler. And we also need to just take responsibility for having more of the code just baked into the application, as opposed to depending on these complex services. So that's, that's something I definitely think people need to think about. It's going to become more clear over time that those they're building systems that are essentially unmaintainable

**Matt Yonkovit**  
Yeah, I mean, supply chain issues within the software space are critical. And we see that every day, especially with some people's new king, some of the open-source software they've even developed for

**Robert Hodges**  
exactly, in fact, is and like, you build these systems, what happens when somebody takes away or nukes like a little JavaScript library that you're depending on, the same problem with, with SaaS services, one of the SaaS services goes belly up, all of a sudden, you may not get any notification at all. And all of a sudden, bang it happened because your application doesn't work anymore, and you lost all your data. So!

**Matt Yonkovit**  
well. Well, Robert, thanks for hanging out with us today. I appreciate you sharing some thoughts given us a little bit of detail behind ClickHouse. And it was great having you on

**Robert Hodges**
Thank you, Matt. It's a pleasure to see you at Percona Live

**Matt Yonkovit** 
 Yes, yes, everyone who's watching this, go ahead and like this video, subscribe to it,  and do come on. Percona Live. We appreciate you hanging out with us today.


