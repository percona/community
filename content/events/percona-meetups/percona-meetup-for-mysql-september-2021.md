---
title: "Percona MeetUp for MySQL Sept 2021"
description: "Join Community MeetUp for MySQL on 8th Sept, 2021 as part of a monthly regular event hosted by Matt Yonkovit, Head of Open Source Strategy at Percona."
images:
  - events/percona-meetup/cover-682.jpg
date: "2021-09-08"
draft: false
speakers:
  - marcos_albe
  - fernando_laudares
tags: ['MySQL', 'Meetup']
---


Watch the video record of the live-streamed Community MeetUp for MySQL we held on September 8, 2021. Matt Yonkovit, the HOSS, sat down with 2 MySQL experts, Nando Camargos and Marcos Albe, and discusses the ways you REALLY can make your database faster. They touched query optimization, indexes, the art of database design, hiding columns, and things that occupy Matt’s thoughts when he wakes up at 3 AM. 

## Video

{{% youtube youtube_id="hTSHb0NU_1E" %}}{{% /youtube %}}

## Transcript


**Matt Yonkovit:**
Hey, everyone, look at us. We're here. We're live. Welcome to our meetup. This is our first MySQL meetup. Hopefully, you're joining us on Twitch or YouTube. So if not, you can watch the recording here. We're going to do this every week a different technology. Once a month we're gonna have MySQL, then we're gonna have Postgres, we're gonna have a few other things. So Marcos is going to join us, but I think Marcos might have got stuck helping a customer and trying to solve some issues. So he's going to be a little bit late. So Nando has joined us, he's one of our speakers. And if you want to give us a wave over in chat, we should be able to see you on screen and say, howdy Ho. So hopefully you guys are all out there, watching the stream out there. Now, interestingly enough, I actually had an interesting weekend, Nando. I've been playing around with dashboards and stuff, with PMM and MySQL, and Postgres. Okay, and so, so this weekend, my server stopped working. Hey, Wayne, how are you? Glad to see you. So my machine, I've been running all kinds of crazy load, so I'm like oh, my God, what happened? And so I spent about an hour trying to figure it out. I left everything as the default location for MySQL and didn't rotate the slow logs. And so it pulled up the disk. And so everything just stopped working. And so it took me about an hour to figure it out. Like, I'm just.

**Nando Camargos:**
Well, it happens all the time.

**Matt Yonkovit:**
So easy, right? Like, how can you? Yeah, so a reminder for those using PMM, or this low query log, rotate your logs, especially if you have a heavy workload, I was just testing. So it didn't cause me any big grief, but it was something that I'm like, wait a minute, how come I can't run this suite benchmark anymore. 

**Nando Camargos:**
Those are the things that always come back. And we see it happening again and again, since forever, man. You see that alerting on the disk space is very useful everywhere.

**Matt Yonkovit:**
Well, I didn't set any of that up yet because I'm just trying to do some benchmarks and some tests, and just trying to move things a little forward. Oh, and guess what? Our second guest of the day has showed up? Oh, here he is. 

**Nando Camargos:**
Hello, Mr. Marcos.

**Matt Yonkovit:**  
Yeah, I don't think he realises that he is live. And so we're gonna see what kind of embarrassing things Marcos does now. Some technical difficulties. That's okay. You missed my story about me filling up my disk space on my test server, and making everything stall. And so I couldn't figure it out. So I was just, I was just lamenting oh, and look, Wayne says, Marco, that Margot's you've helped him on so many tickets. So it's me to see his face. Did you recognize Wayne?

**Marcos Albe:**
Absolutely. Yes. And thanks for joining us at this meetup and glad to help you.

**Matt Yonkovit:**
That's good. So just so everybody's aware, this is the first one of these. And so we want to do these on a regular basis. We figure we'll get a few folks here. And we're going to grow over time. As the reputation of this gets better and better. We'll get more and more people. But we're always going to be looking for people who are interested to share some interesting topics, they want to come out and share with us a few different things. We'd love to see you out here. And you can present here you know and talk but this is nothing that is scripted. So we want to hear from you. So feel free to put it into YouTube chat or in Discord. You know, you can have that pop in or Twitch. All of them should pop up here and we should be able to follow along. So if you have a question or you want us to dig into something, feel free, but we did start with a couple of interesting topics. So I heard Marcos demanded that Nando go first so that's okay. You know, so since Marcos gets what Marcos wants?

**Nando Camargos:** 
I think he's ready. Look, look at it. And he's he I think he's ready.

**Matt Yonkovit:** 
Oh, yeah, yes, yes. Hey, Mike, how are you? Mike Peyton is joining us if you build it, they will come. So that's good. So, Marcos, are you ready? Are you set?

**Marcos Albe:**
I guess I'm ready.

**Matt Yonkovit:** 
So Marcos, you're going to talk to us, you're going to tell us how to actually tune systems the right way. Right? Is that Well,

**Marcos Albe:**
Yeah, no, no, not precise. I'm not gonna talk about taming the database, because that's not how you really get the best performance. I mean, you can perform well, tell me, how do you team up properly, and good performance, if you do your queries properly. That is, to any database, the database is just as good as the queries we send to them. And that is really, what most developers mean when they are working with a database is they forget that the database, the only work that database does is running backward. In reality, in the database you have a bigger language, it's not an imperative language, it's declarative, you tell, hey, I want you to give me all the answers who are called Marcos and order them by the last name. And the database, how to actually fetch the data, it's, it has many ways to do it well to access the data through the primary key, or it could data through indeed, choose to sort the data on these or sort the data in memory. So it can end up with a different exam, right? And yeah, well, what we have to do is actually build the database better, that's the key to database performance, proper schema design, and proper query design. And of course, the right database for the job, you want to manage 10 terabytes, it's going to be painful that, like, reality, there's a that you can do with 10 terabytes. So once if you more easily write than read most of the pain camps when we are trying to read. So the number one thing, proper schema design with indexing, and that is I think, what, it's hard for developers, and which it's funny, because listening, it's a B plus three. And, and developers, I am sure most of them, they'll be plus threes and how it works, but they forget that...

**Matt Yonkovit:** 
The database design itself is almost a lost art because everyone just kind of throws garbage in garbage out now. I mean, like, nobody wants to think about that. And I mean, a lot of new databases are trying to mitigate, like even having to think about a schema. So they're trying to build in logic in order to prevent it from happening.

**Marcos Albe:**
Yeah. What are going to be the access patterns for the data, but you are a designer, how you are going to access the data, like am I going to be sorting by the database, achieve that sorting like, I have to make that sort of easier. And help with an index and indexing. I would say 80% of performance. Customers come to support big performances issues, more than a half of those issues are due to bad queries.and I will take more than that much

**Matt Yonkovit:** 
50% potentially?

**Marcos Albe:**  
Yeah, because it's always the ultimate answer, right? So the database system, why? Because you know, the disk is saturated? Why is it saturated? Oh, because it's reading pages from this all the time. Why is it reading pages full-time? Oh, because the buffer pool is too small. Too many rows actually need to satisfy the query. And that they are being read just didn't add an index. And so in the end the disk is slow, or that the buffer pool is too small, is that the words are reading inordinate an unnecessary amount of rows. So indexing is really, really the decoding of better performance, proper indexing, not over-indexing, over-indexing can kill your performance. But proper indexing and good query design and good access patterns are the centre for improving your performance. 

**Matt Yonkovit:**  
I know you were gonna say something. What were you gonna chime in?

**Nando Camargos:**
No, no, no, it's just that. I think another way to say it, what Marcos is explaining is this, you're trying to get a single result or a handful of results if you're out of your table with a query, right. But if your query, if MySQL in order to get those results, it needs to fetch over 22,000 or more rows, right, it needs to fetch that from the from the database in order to sort those and then aggregate with other queries, in order to get those two a handful of results. Think about the amount of work that is required, it is going to work, right, it is going to work. But that is an extraordinary amount of extra work that could be avoided if you had the schema optimizing or the query optimizer for the schema you have. Think that's that's an excellent point. Yeah.

**Matt Yonkovit:**  
You know, it's funny, I was thinking about this last night, I woke up at 3am. And I think about database things. That's weird, right? Is that weird? Does anybody else do that? I don't know. Does anybody else do that? I get that. But Marcos doesn't. And I feel. Yeah. So you know, so I was thinking about this, in the context of, I'm thinking about writing an article on sharding. And the necessity and the reasons why, and there's a lot of sharding, there's an old, old tech technique. I mean, it's been around for ages. But realistically, all databases really only have two constraints. And my theory, or what I was thinking is really you're talking about either it's a throughput issue, or it's a concurrency issue. And when you talk about indexes, it's kind of hitting both concurrency and throughput. Because as you hit the disk, you're limiting the number of people who can access that disk at once. And you're also definitely slowing things down. So you're really, it's all about optimizing throughput, and concurrency. And as you start to look at the different techniques on performance tuning optimization, it all boils down to which of those knobs do you turn. And how much in which methods do you use to turn them? Am I right or wrong? I don't know. Or is it just me? 

**Marcos Albe:**
This universal scalability law from what's this guy from the ruler capacity planning was his name. Oh, no, no. The book is called Guerrilla Capacity Planning. Oh, okay. And there is universal scalability. Law, actually, Baron contributed to me. That's the guy and beta. Concurrency is one of the denominators in the equation that defines the law. And the more concurrency, the more tension there will be, and that increases response times. Right. Like, who cares about his risk, replying to you very quickly. Nobody, right? That's boring databases are good databases. But when response time is high, then that's when people start complaining. And yeah, if you have concurrency, if you only work, and we all want to hit from the same place, then you know, like, we have to wait. And that way translates to slow queries. So, the urgency in assisting is a defining part of the performance. But if you again, if your residence time database is one millisecond, then you can have more queries. I mean, concurrency is that the effect of having parties running in parallel, right, and that they won't, they will compete for the resources needed to read the rows, or sort the rows or do whatever. So the longer the query takes, the more likely it's going to other concurrent queries running along. So to reduce it, you have to shrink the times for it, there is no magic bullet. But that will alleviate tension and sometimes split the new takes. Sometimes we can avoid the isolation requirements. But there is no magical solution to reading from this if we all want this. That's what we have to do this. So we avoid reading so much from this.

**Matt Yonkovit:**  
Something interesting, and I and I pinned it here, you know that no one really cares about query time, right? It's about the response time of the application. And obviously, the components of that application, which are reading from disk, it's the query response time, it's the things that are missing indexes, it's the crappy query, go for the things that are, you can get that live on the air if you want, that's fine. You know, you never know who's gonna call in. It's Wayne calling, and it's Wayne calling in to you to get on the show, he wants to ask you a question, I'm sure. 

**Marcos Albe:**
Yeah. Just open a ticket. 

**Matt Yonkovit:**  
But no, it is an interesting concept, right? Because so much of how well an application performs, is based on that initial design, and then initial setup. And it really sets everything up for the future. And this is where I think that for a lot of us when we talk about whether it's the cloud or you know, these other technologies that are all coming out to make things easier, they don't always solve the scalability issue. Because you didn't design it upfront, you didn't fix the issues upfront, that were going to cause you problems. So you would just end up having to throw more and more resources at it, which does alleviate the throughput issue and the concurrency issue, somewhat, but you eventually run out of resources that you can up.

**Nando Camargos:**
I think about this, Matt. Oh, you have your application or your development team working on your application, right? And the thing test is it and it works, it just works. And the queries are running fast because the response time is fast. And then you try and you change the test environment and try to put it on some load and some concurrency, right. And it's still reasonably fast. So the response time is there. But not always those stats are what you do in staging, they really reproduce what you're going to get in production when you launch the application. Or even more particularly, they won't match what we're going to see once your application becomes really popular. Right. So it's still interesting to review the schema and not only focus on the response time for your test but really, what is it that the query is doing or how much work MySQL is having to do to get the results you're asking from it?

**Matt Yonkovit:**   
Yeah, and I mean, it's interesting, because what starts off as fast can quickly become slow. Right? Right. I mean, and that's really the crux of the issue is, fast becomes slow very quickly when production workload happens. And Marcos wanted to say something I see.

**Marcos Albe:**
Data has that data has organic growth and you know, what six months ago was a perfectly fine prairie. Now, and it was scanty like a table scan, it was a scan in 1000 rows six months later, it's scanning 2 million rows, and now it's eight seconds. And that's just organic growth, changes in the database, changes in the source code all the same.

**Nando Camargos:** 
Well, the amount of data just change it. Yeah, it’s just growing. Yeah, yeah, that's another point.

**Marcos Albe:**
And Ryan Lowe, we used to have a talk that pulled money at the problem. And basically we tried to find the limits for both vertically by just adding more resources faster these more memory more CPUs, and there is that, they will simply not scale that, no matter what hardware you use, they will not scale, because they don't suppose if you do insert, select, and the Select will do a full table scan, and the table, it's a table that also gets updates, or also gets deletes, then all those updates and deletes are going to be blocked. And there's no way around it that fast your hardware is, it's just that the access pattern, it's about access better. So right. What you can be patient first in insert, select, I don't know, we could try to find solutions, find workarounds, but you know, throwing money at the problem, like adding more resources doesn't solve, and it will not solve other problems as well. So that I think it's important that the database, it's as the work we put on it, and and the difference between database that runs super fast and has good response times, to me, it's an a database that responds poorly, it's, again, mostly a difference in the design of the schema. And in the choice of access patterns, and how we design the queries, right. But they are examples. Another classical example is using master kill, right, trying to secure a processor. And we know it failed miserably due to lock-in issues. 

**Matt Yonkovit:**  
Do you think that largely at small volumes, most database performance are fairly similar? Like when you've got a reasonable workload? Like it's pretty small, choosing one database over another matter very little?

**Marcos Albe:**
Oh, yeah, yeah, if you have a few 1000 rows, and yeah, your operations, that doesn't matter, right, like, if it's a few 1000 rows, I don't think the database is gonna be pushed to its limits, right, and that all operations are gonna finish fast enough that even the contention and the concurrency problems are still gonna be mostly invisible, because that it will be hidden by the fact that operations complete personnel, so your response times are going to be fine. Not because there is no contention, or not, because it's not great in horrible temporary tables on disk. But just because the temporary tables are going to be small, or the table scan is gonna complete quickly. 

**Matt Yonkovit:**  
If everything's in memory, then most databases are pretty fast. And the difference between the one millisecond and half a millisecond might not be noticed if you've got only like 20 users. So, yeah,

**Nando Camargos:**
With twin uses, that is right, but even if you have a very small data set, but extremely high concurrency and a bunch of connections, just opening and closing, opening and closing, opening and closing this is a point where different databases perform differently because of the design. So there are weaknesses and strengths in the characteristics of the database management system, and then we can compare those.

**Matt Yonkovit:**    
Right, yeah, I mean, it's the concurrency versus throughput, right? I mean, that's really what it is.

**Nando Camargos:**
Well, it does come down to that. Yeah. But I have just an observation to make on what we are discussing, because what Marcoses is saying is absolutely the case, right, you should give proper importance to the schema in the query optimization, it comes to some situations where we have seen customers working with third party applications, where they can really just change the queries, there is still a chance of trying to improve the schema, right? Because the schema is hosted by the database. So you can add an index that could make a complete difference to the execution plan. But also, it is possible for those very long queries that require more time to execute. And due to high concurrency, you just see several requests just piling up inside the storage engine, right? InnoDB, for instance, allows you to limit the amount of queries that it will process at a given single time. Right. So you actually there is a setting where you can limit how many requests are being processed at the same time, why is this interesting proposition because then those queries are not completing a competing with everybody else for the resources, and they are giving more resources to complete, and then they just complete and go away, right. So you can process other queries, there is still very significant space for server tuning, right, Marcos in function of the workload you are dealing with.

**Marcos Albe:** 
Yeah, you can tune the database and, and there will be like, if you have a very heavy right workload, then tuning flushing, and properly, setting dimensioning, the redo logs, and properly dimensioning, the log buffer, stuff like that, like that, it could improve and we have helped with customers improve replication speed by properly tuning, flushing and making writes more agile, right, like, more lean. But in the end, again, there is always a limit for the concurrency right like that we know that we can add more threads up to a point where things stop scaling linearly. And actually, they have negative scalability, right, because the concurrency itself will hurt the performance. And you were saying that sometimes we don't have access to the third party application to change the queries. But we can use the query rewrite plugin in MySQL5.7, and newer, or we could use ProxySQL as a middle layer that's also free.  I know there is no for MongoDB. But you know, for MySQL, which still holds the most popular open source database, a chance to actually rewrite on our side without intervention from the developers. 

**Matt Yonkovit:** 
Complete rewrite, though, right? And I think that's what Nando, you were saying, as you know, you can add indexes. Now you've got functional indexes, you've got generated columns that you can do some things with, you can hide columns. So if the application is doing a select star and doesn't expect that extra column, you can hide it and add a column, even if you can't, like, there's little tricks you can deploy to get around some of those limitations. And I think more and more databases are kind of like realizing that there might not be complete control. So they're trying to give you more of those features.

**Marcos Albe:**   
Yeah, yeah. And like it says, hiding or hiding a column helps change the behavior of a query, and make it work when you don't have access to a developer that is willing to change the query itself, the duration of the query itself. Yeah. Again, I think the big takeaway is that, right? It's like, concurrency is limited. There is no eternal growth. resources in the physical resources... We have a customer who has a machine with 144 CPU cores and four terabytes of RAM.

**Matt Yonkovit:** 
In one machine, this is one this is not a cluster. This is one machine.

**Marcos Albe:**   
Yeah, this is one machine. This is one machine. It runs a single MySQL instance. With a 3.4 terabytes buffer, and you know where those 32 core machines are, since this 36, right 3036 36 core is 72 threads, 144...

**Matt Yonkovit:**  
I mean, like I remember when I had my like, Look, I got two core. This is stellar performance, me and my two cores and my four gigabytes of memory. Whoo, this is gonna rock, you know.

**Marcos Albe:** 
But this guy has four terabytes of RAM, but he's databases like nine terabytes. So, yeah, still listen to him. And they keep growing and growing and growing. Yeah.

**Matt Yonkovit:**  
I mean, I'm curious what other people have in their data centres. I know that I have seen like some people I have, I personally experienced this on occasion where you've got someone who has like a 200-megabyte database, and they've got like this one terabyte worth of memory 64 core box, you're like, hacker you don't I just want to have it in case it goes wild. Right. I just want to have that, in case it goes crazy.

**Marcos Albe:** 
Yeah. And, and again, the interesting thing that I was thinking about the other day, that and it's related to the ever-growing database, and is like, we tend to not be very careful with database growth. You know, people just say, I'm just gonna start it like, and they keep storing data. And later, months, later, years later, people come and said, What is this table for? or What is this table use it. And actually, nobody's reading that data. And it's been the stable indexer and backed up for months, right, and like, nobody's using it. And the other is that they don't summarise data, like they just keep archiving data in raw format, without making summaries and aggregating data, for later consumption. So every time you have to read the data, you have to read every day. And with the cheap shortage that we are undergoing, I was thinking that it might be a great time to have people rethink their behavior of careless microservices, that are forgotten in a cluster, and they are just thumbing their nose.

**Matt Yonkovit:** 
Are you not suggesting people clean up their crap?

**Marcos Albe:**
Yeah, that base, I think it's considering the cheap shortage, and seeing that CPUs and memory prices are hiking, I believe it's a good idea I do think it's a good chance to improve your cleaner, and save the massive like, the other day, I was showing the customer, how much money they can save in AWS by just optimizing and stop reading data that nobody you know, what the cap, the cap SQL cap fund grows, where you do select SQL rows from my table limit? 20. But if the query would have returned it a million rows, it still scans a million rows, return 20? Well, they were using that everywhere else. Oh, yes. So you know, like, there was no buffer pool, that will be enough. And, every thread was reading to 6 million rows, each thread for doing like, they will be reading to 6 million rows, how many rows just to return 20-14 and they could save 1000s of dollars. Like literally we did the numbers and it was $5-6,000 per month. This doesn't seem like much but it was just a single product, not all of their databases. This was just a single product with a single database. And that kind of savings shows they again, like the shortage of silicon . It's a reality and it will make prices go up. So using those resources you have in a smarter way might be in your best interest.

**Matt Yonkovit:** 
So the two suggestions that popped to mind based on this conversation, and I'm interested in your opinion, and those who are watching live. So number one. So should we get stickers or t-shirts that say you know, like, clean up your crap? Friends, don't let friends keep microservices on forever. Do you think we should do that? It sounds like, right, I would put that on my laptop, that would be cool. But I think that we need to advocate for DBAs and SRS that they should get like, 10% of whatever they save off of cloud bills when they optimize so so like everywhere. Everyone should be like hey, look, 5-6000 a month off of this one server? Well, hello, that's five 600 bucks in the DBAs pocket are there.

**Nando Camargos:**
In your where you should start for people watching this, you start, we're making sure you enable this little query log, right? Have it enabled and start collecting your azole queries. And then you can use one of our tools that PT query digest from the Percona toolkit, and start looking at the trends and see, what are the top slow queries you have? Right? Usually, they don't stop slow queries, they are consuming like they're responsible for 20-30% of the execution time. Right? So you start by trying to optimize those queries. So there's an easy way to go. Right. And if you are on a customer's wiki, you just open a ticket and we can help you with those.

**Marcos Albe:**
And I was all the data, it's a funny thing, but we you know, how in the European community, you can, each company has carbon credits, right? Like, yeah, so much carbon footprint. And if you have a negative carbon footprint, you can sell your carbon credits to other companies. So if we optimise the query and we are reducing the amount of energy, the same software is consuming, because that's what you get when you optimize a query, right. Like you can use less servers and shrink your carbon footprint because servers require and Percona could accumulate all the carbon credits because it will be I mean, I'd love to have that counter how much carbon emissions we have saved. I would love to.

**Matt Yonkovit:** 
If you can figure it out, we'll put it in PMM. That'll be our mission. But you know,

**Nando Camargos:** 
I think we should somehow if Trudeau met, we should summon Trudeau to work on. He's gonna love it. Yeah. Yeah, this is dear to his heart. 

**Matt Yonkovit:** 
So what does everybody think should we get a carbon footprint offset? By the way, Wayne says he has much love for the toolkit, which we appreciate. Thanks. Very nice, very nice. But no, I think we can do this. I think we can figure this out. So we'll get on that. And maybe by the next time around for the MySQL meetup, we'll have something that we can show. What do you think?

**Marcos Albe:**
Yeah, if we could, if we could figure out how much, what is the carbon footprint for a one second worth of platinum? Yeah off the shelf, average heigan server, right? Like what we see in databases nowadays, that will be super, super interesting. Because if you have the per second, then you can say, oh, if this query was running in 60 seconds, and now it's running 0.5 seconds, only it calculates the footprint.

**Nando Camargos:** 
There are estimations for that I remember seeing this 10 years ago, so there certainly is.

**Matt Yonkovit:** 
Yeah, yeah. I mean, I can see that. Like, if you can do it based on power. It looks like you know, one unit of carbon is equivalent to Yeah, so I mean, like, you can find it, it does exist out there. And so, yes, there you go. So we can do this. So, let's get that for the next PMF. Or we'll need to do that for the PMM meetup that we have in a few weeks or the MySQL meetup. So we'll get on that as well. But as we talk about this stuff I'm sure people are going like we're all over the place here. Wasn't someone gonna show a presentation?

**Marcos Albe:**
We're still focusing on query organization, which again, in my habit, it's the only way to truly have a scalable database. And you know, it's the difference again, between a slow database and a fast database, nobody's looking at us is always giving you good results.

**Nando Camargos:** 
Is it the only way or is the proper way, Marcos?

**Marcos Albe:** 
I wouldn't say it's the only way because again, you did there are some workloads that you cannot scale horizontally, right? Like, you cannot start sending critical reads to your replica? Well, if you have exceeded that insert workload update workloads which also require finding the rules, it has to update first, if not probably indexes, those will never stay. So, in all honesty, property indexing, it's a fundamental part of this. And now that you mentioned that it's through the, I always remember something he taught me years ago, which is related to skin and is we always see customers using big int, which is eight bytes for. Give me a good comparison point, which is big enough еo count the ants on the earth, you can count all the ants in the earth with the big int, and you still have some leftover. So when you're designing your schema, you can ask yourself, Am I really gonna

**Matt Yonkovit:**   
From a developer perspective, nobody wants to bite count anymore. I mean, come on. That's old school, right? Like, who wants to think about bites? Like, it adds up? I will grant you but nobody wants to think about it.

**Nando Camargos:**  
Yeah, that's a movement that is coming. If you look at, I'm not really looking to develop that much. But I remember with Ruby on Rails, which is a framework, right? You would have all MySQL it created with infer primary keys. And nowadays it begins so there you go. Most people don't want to worry about it but I do think it's, it's maybe an exaggeration, right? Which because, like Marcos has said that they actually use cases where you are going to make use of begging, or not the majority, they're certainly not. But I do understand your point, Matt.

**Matt Yonkovit:**  
And he's like, yeah you there's, there's no use case ever for it. And then he went to this satellite company that does GPS satellites and micro satellites, and they do like coordinate positioning. And they actually needed the big end. So they actually found a use case that actually did require it. But I wanted to point out, Fernando, when you said the word Ruby on Rails, Marcos, his face like cringed in a way that little fuzzy camera that he's got, I told you I know because he was having some bad memories. He was having some bad. I wake up at 3 am to think about sharding and scalability, you wake up to you know, Ruby on Rails.

**Marcos Albe:** 
Basically, man, the amount of times we have seen Rails failing to scale because all the metadata it pulls, DRM pulls from the data, so fields 800 times per second. And obviously, didn't steal. That's another advice for making MySQL faster. What is the fastest query you can run? Is the pretty that never runs, right? Like the burning, you don't run as fast as one. If you can keep a cache, then that's the password. And that it's again, something that ProxySQL provides. Right, in this case, people and so used to for the show fields example. And we have that. They couldn't believe it, right? Like they were like, how could the 800 operations kill the database? Well, the database has certain structures that are governed by a mutex and concurrent access to the mutex is problematic and even 200 operations per second can make it painful.

**Matt Yonkovit:** 
Alex, welcome, Alex, we're glad to have you here. And we have a question. You know, hello guys advise me, I'm getting a lack of this space on MySQL Server can't add physical disks, but have another empty server. How do I shard some of the databases to there, so I don't break all the dependencies. 

**Marcos Albe:** 
So application dependency, there is no universal sharding tool. There are sharding frameworks. But you don't just say they are, let's start this table. And there is a mechanism like there is in MongoDB, where the conflict server tracks where the pieces of the table are. In MySQL, there is no such mechanism to do it. So it's a very fair application. Normally, you can reclaim the disk, right there where you are. And you know, like we were saying before, try to find unused indexes with pt duplicate key checker. And using sysa schema, there is a function or a view that shows unused indexes. And then you could also try to find out data types, which are excessively large for your needs, like we were saying a second ago, if you have many primary keys that are digging, many, many, many of those, you most likely can make them an end, while before by difference, at first don't seem like a match, on a few million rows, they start to add up. But not only that, because every secondary key has a copy of the primary key. If you have, say, five indexes on the table, you're saving 24 bytes, not only for, and again, when you start adding millions of rows, they start taking up space. And so improving on the datatypes dropping, duplicate indexes running optimized on tables that have got many deletes all those conditions.
 
**Nando Camargos:** 
This is an important point, that one, you might have tables that have grown very large over time. And then the actual amount of data now it's much less but the table or the table space five just grows, grow up big, right? So if you Marcos was like said if you identify those tables, and you reviewed them, they are going to be optimized and come over much smaller, right just decides they should actually have. But you do need to have enough disk space to make a temporary copy of those tables when you are doing this operation. But maybe this one is something to really look at, because it's kind of an easy solution.

**Matt Yonkovit:** 
Yeah. And then back when I was in consulting way back, and but I've heard that this is pretty consistent those space-saving whether it's data types, or just making small changes 30-40% decrease in disk space is not uncommon. I mean that's, that's a pretty significant disk savings.

**Marcos Albe:**  
Yep. Well, the last stop will be archive data if you have tables that are growing and growing, but your data never changes, you could probably put data into my some pocket table that will allow you to keep it accessible. And that will be much more space-efficient enough to have a huge, huge overhead. This is humongous, right? 

**Matt Yonkovit:**  
There's also My Rocks, which also can help pack bikes as well. You know, so there are options with alternative storage engines. But one of the things you could also do is you mentioned some of the data, it might not necessarily be needed by the full application. Some of those, the data is often just there for reporting. So you've mentioned you have an empty server, it's possible to have your empty server, have your archive data or full datasets of some tables and shrink other things. So one of the other things we've also seen is you might have a year's worth of data on your primary server, and then on your secondary servers. You might have more than a year.

**Nando Camargos:** 
So yeah. And there's another tool from the Percona toolkit for this, which is pt-archiver, which can facilitate the archiving of data from one server to the other, for instance.

**Matt Yonkovit:**  
Yeah. Great. And so Wayne has a question. So Wayne  wants to know that he's he's working with a new cluster using ProxySQL and the orchestrator has a question. I have four tables, unique to each server, I want to filter out those four tables.

**Marcos Albe:**    
Yeah. So I'm not sure are those four servers working on this occasion, like similar replication? I mean, you have four masters. And each of them has a unique primary. Yeah.

**Nando Camargos:**  
Yeah, I think that's the scenario. Yeah. I think he can explain this to us, but I think he's talking about having four masters each with one different table that he wants to unify together. Is that right, Wayne? 

**Matt Yonkovit:** 
It is a primary replica. So it is a primary replica there. We can put the chat on. So we can see that come through as it happened.

**Marcos Albe:**    
I think you can see me using one master. 2 replicas, okay. So each of them has a unique table, and you want to filter out. So replicas, you don't want change in those tables to go to the binary log. And on the primary changes to that will take forever to go to.  The built-in reputation filters are the only option.

**Matt Yonkovit:** 
Yeah, because I mean, it's not going to go through proxy at all for those.

**Marcos Albe:** 
Right, yeah. But he wants to filter, he doesn't want to have the events for the tables in the below. And no matter what you're doing the proxy, if you send the right to the server to any of the servers. 

**Matt Yonkovit:**   
We have to do the replicate, ignore table, I think, but that'll still show up there. Right. Yeah.

**Marcos Albe:** 
Yeah. By the way, you are entitled to open that door. Glad to join you on a call and give you more and better advice. With with more details. And Alex, that Yeah, cool. Thanks. I made archives. You need to skip it with a bill on the brighter side. That's not the replica. 

**Nando Camargos:**  
He's writing directly to the replica. So I think that's the point when you clarify why I think you are writing to those replicas. Besides the replication flow that is coming from the primary, right, so there's unique tables in each of the replicas that are being written directly. And you want to unify this data? Yeah, okay. You see, the only thing I can think about is a multi-source replication, where you are going to have a third-level replica below your replicas, which will be a replicating from each of those three replicas on the second level, and you're going to be only replicating those unique tables from from the replicas into that third level replica.

**Matt Yonkovit:**  
But you could do it right, you could do a poor man's replica replication, right with ProxySQL where any rights to those servers, you just redirect to the other servers.

**Marcos Albe:** 
Yeah, no, but what he wants when the way to do what you want to achieve is to make that table leave in a separate database, and then use binlog InnoDB, and then you can ignore the database that only holds that table and that will prevent it from going to the So you will have to have the database table in a separate database, you could have a view in another database that is a one to one bypass to this table on the other database. So it won't change the restriction. I cannot think of another way.

**Matt Yonkovit:**  
Okay. And Alex does have another question and he popped in there. You know, Wayne's gonna open up a ticket but, Alex, one more question, more abstract, which advantages and disadvantages between keeping MySQL on hardware? So bare metal versus containers? Like Docker? Are you very excited about the Docker thing?

**Marcos Albe:** 
No, no, I was gonna say that. One of the big advantages of keeping MySQL Server work is that you're gonna make no, there's no disadvantage of keeping the server in hardware. The only disadvantage it has is that hardware is slow to provision. And it's your once you order that machine in the data center, or that you rented the machine, you are stuck to that box for some time. Right, like, heavily depends on your company's dealings. 

**Matt Yonkovit:**   
It's not just hardware provisioning. No, right. It's also the setup of the database. And making sure that it's consistent across multiple, no, I mean, like, there are economies of scale that you get, by using orchestration tools, whether that's, I mean, there are other things other than Docker, right, so having a container image like if you're running an operator for Kubernetes, or if you've got Ansible scripts or whatever, that set up, consistent images and consistent software on configs. You get those advantages as well. So it's not just hardware.

**Marcos Albe:**  
No, no, no. What I was saying is that the main disadvantage of hardware, right, is that it's like you, you're stuck to it. In a sense, you're stuck, right? Like once you have the database running on some hardware, like ordering more hardware place and setting up the database, it's difficult. Again, it all depends on how you will provision the containers because the containers also run on some hardware,

**Matt Yonkovit:**   
I think. Yeah. And I also want to consider how many MySQL servers you're going to be?

**Nando Camargos:** 
Yeah, that's a point. Yeah. Yeah.

**Matt Yonkovit:**  
If it's just like one instance if you need 12, every database,

**Nando Camargos:** 
We go again, about the micro services, right? Are you going to have a really small database for a particular service? And you want to two segregate those? Or is it really a big database that is going to require a dedicated server just to have enough hardware resources? I think that's also an important thing to consider. Great.

**Matt Yonkovit:**  
Wayne, thanks for showing up. Appreciate it. We'll see you next time. Got one more question. This is the last question we'll handle. You know, so can we save the password for the encrypted key ring file password variable encrypted in the configuration file? 

**Marcos Albe:** 
Unfortunately, I don't think that's possible. 

**Matt Yonkovit:**  
Oh, you get stored in another vault somewhere. If you wanted to do that.

**Marcos Albe:**  
You will have what we normally advise is to have encrypted volume that you mount when you buy bass and you then unmounted so you know the mean is protected. 

**Nando Camargos:**  
We were discussing this topic last week about Postgres but he also fits here. And people were discussing keeping the password on a file in the file system or even keeping the password as an environment variable. Right, which, if you do have root access to the machine, you're going to be able to see it inside the slash proc, right. And another thing that came up with is that you can kind of secure the firewall a little bit more with se Linux and or aappr more in-depth on Ubuntu. Right. It is also possible to do this and restrict the access besides the actual file permissions that you can set. Right. So I would suggest having a look at this because it is possible to restrict even more who can access the file could be just a MySQL, the MySQL the process that is running that can access it. But I haven't tested this myself, theoretically it is obviously fast. All right.

**Marcos Albe:**  
Well, great topic for another several month.

**Matt Yonkovit:**  
Oh, as per compliance and CIA guidelines. GSO team was requesting not to store any password configuration file in plain text format. So yeah, yeah. I mean, it's Yeah, so the options are,

**Marcos Albe:** 
Again, the way most customers in Percona have solved it is actually using a vault instead of a key ring file, which he will file with a client, you think you need to use a vault or another key management system.

**Matt Yonkovit:**  
Marcos, Nando, thank you for coming up. I know we scheduled an hour a little bit over. I want to be mindful of your guys' time, because you guys are really busy. You're out there helping customers, we glad you stopped by to help out some folks. You know, I know now I know you had a presentation, just in case we didn't have stuff to talk about. It turns out we had more than enough stuff to talk about. But I can give that presentation. I would love to see it. And absolutely. You know, so you know, we're glad everybody enjoyed it. And we hope to see you next week at our Postgres following. We get Mongo week, after that to PMM. And then we're back to MySQL again. And maybe we can Marcos and Nando to join us again, I'm one of those calls. You know, I've been talking to a few of our old buddies at different companies. So we'll see if we can get them here too.

**Marcos Albe:** 
Oh, nice. Nice. Thank you. And you know, again, invite customers to bring, bring their PMMs and do some diagnostics.

**Matt Yonkovit:**  
You want to fix my PMM.  This weekend, I ran out of space. So yeah, fix mine first.

**Marcos Albe:** 
I'll fix yours.

**Matt Yonkovit:** 
You can diagnose my performance issues. I purposely made bad queries for this. Thank you, buddy. We appreciate it. Don't forget to subscribe, hit the subscribe button. We love that you subscribe. We want to see you here. Follow us on Twitter. You know you can follow us on Twitch as well. We're everywhere where you are. So we do appreciate it. All right. See you everybody, everyone.





![Percona MeetUp for MySQL Sept 2021](events/percona-meetup/cover-1920-1080.jpg)

The Percona Community MeetUp for MySQL is a great opportunity for experts to share their knowledge and to the attendees to ask questions. This event is a part of a series of regular live online streaming with Matt Yonkovit, The Head of OpenSource Strategy (HOSS) dedicated to experts and users of database.

Join the Percona MeetUp for MySQL

* Day: Wednesday Sept 8th, 2021 at 11:00am EST

* We expect the stream to last 1 hour

* Location: on [Discord](http://per.co.na/discord)

* Live streaming on [YouTube](https://www.youtube.com/watch?v=hTSHb0NU_1E) and [Twitch](https://www.twitch.tv/perconacommunity)

Add this event to your [Google Calendar](https://calendar.google.com/calendar/u/0/r/eventedit/copy/NmpnMDJ1YjVrZ3BtajVuOWMzYjJxZDJkOGEgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn/ZnJlZGVsLm1hbWluZHJhQHBlcmNvbmEuY29t?sf=true)

## Agenda

Two excellent engineers will present their 15-minute topics live and also answer your questions afterwards

### How to REALLY optimize MySQL performance by Marcos Albe

1. How to spend money on hardware?
2. Tuning configuration parameters is not the true path to performance
3. The single thing that actually makes performance better, and a system scalable

Marcos is currently Principal Technical Services Engineer at Percona. Focus on MySQL, Percona Server, Galera-based clusters, XtraBackup
Enjoy performance diagnostic and troubleshooting in general

### Inspecting MySQL Servers by Fernando Laudares Camargos

1. The approach used by Percona Support to troubleshoot MySQL performance issues
2. Our favorite tools from the Percona Toolkit suite
3. How much of the work can also be done based on PMM data 

Nando is currently Senior Support Engineer at Percona. He played different roles along the way: analyst, developer, architect, consulting services around MySQL and open source software

**The Percona Community MeetUp is a Live Event and Attendees will have time to ask question during the Q&A. All kinds of feedback are welcome to help us improving upcoming events.**

## Come along if you’re a:

* User of MySQL

* Student or want to learn MySQL

* Expert, Engineer, Developer of MySQL

* Thinking about working with database and big data

* Interested in MySQL


