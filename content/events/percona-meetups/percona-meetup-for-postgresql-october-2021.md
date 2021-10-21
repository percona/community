---
title: "Percona MeetUp for PostgreSQL October 2021"
description: "Community MeetUp for PostgreSQL dedicated to performance improvement, monitoring to prevent performance issues, and troubleshooting."
images:
  - events/percona-meetup/postgres-october-cover-1362.jpg
date: "2021-10-13"
draft: false
speakers:
  - charly_batista
tags: ['PostgreSQL', 'Meetup']
---

Community MeetUp for PostgreSQL was live stream on Oct 13th at 11:00am EDT to talk about how to improve your database performance with appropriated tools for monitoring and optimization. Here are the full recording and transcript :

## Video

{{% youtube youtube_id="rAuz1usu9Z4" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit**
Oh, the abrupt start, I started the soundtrack a little, a little later than normal so we didn't get the full five minutes of awesome retro 80s soundtrack in. But I am excited to be here with Charlie. What's up my friend?

**Charly Batista**  
Hey, Matt, how are you doing?

**Matt Yonkovit**
I'm doing great. I'm doing great. So thank you everyone for joining today. We've got the Postgres meetup. This is one of the weekly meetups that we do on different database technologies and different open source technologies. We are glad you came and you know for those watching live welcome for those watching recorded welcome. A lot of people are at coop con this week, so it's always exciting. , we just actually released our operators for Postgres. So we've got a few people out there, walking around talking with folks shaking hands. I wish I was there, but I'm not. But I'm glad I'm here with Charlie. Right. So. So Charlie, thanks for joining. , we I know we've got some topics that we wanted to cover. For those who are online, feel free to come on over to chat, I'm going to pop the chat up to the, to our right here. And you can ask questions, they'll show up live here. appreciate any of the questions, and we'll dive into questions as time goes on. But I wanted to start with personal stuff. Because why not? , and so, Charlie, I don't know about you, but being on call is hard. Right? I mean, it's a hard thing. And I used to be, I used to be a DBA who had carried the pager around and got called all the time. And we all have shifts now and so whether you work in support or you work in managed services with Percona or , anywhere else we're fortunate where we really don't have to have that pager kind of philosophy and I never had to carry a pager and 10 years, I think, you know

**Charly Batista**
what? I think it's more Yeah, at least 15 years ago.

**Matt Yonkovit**
Yeah, it is. I mean, phone pager yeah, I mean, yes. Okay, I just dated myself for everyone on the thing that I said to a pager? Yes. I actually did carry a beeper, Yes, but later morphed into phones that went off constantly. And so I'm really tired today. You probably can't tell because I had a ton of coffee and soda this morning to pep up with caffeine. Because , you are always on call when you have kids and dogs. Now my daughter's 20 right so she's no longer considered a kid but she still lives at home and she loves her dogs and unfortunately, she buys these boxes that get sent to her that have like all these dog treats and dog toys. She did that over the weekend she got a new one and she's oh here we go throw the toys and she's got these treats and our biggest dog he's an Old English Sheepdog. He has a very sensitive stomach so she's been giving him these treats all day long and you know two o'clock in the morning dog starts whining and crying because it's got an upset stomach and you know in my daughter she's 20 she knows that like the dog is going to you know have issues but so I was up at 2am , with the dog but I did get a chance to dig into some PMM code at 2am so I didn't make the most of my experience but thanks thank God we don't have to have you know that kind of patron mentality anymore that's always a rough thing.

**Charly Batista**
Yeah, it is it is. I mean, when I started working in IT industry 20 some years ago I remember or department was one of the first in the company that we got a mobile phone back the time it was a huge Motorola it was a really big one well, we had to carry the mobile phone right and it was so awkward when we bought the call not located right in the middle of the street and then it got the call with that giant thing. And everybody looks at you and you're like oh my goodness.

**Matt Yonkovit**  
Yeah. Well, and when you got those calls, how often Was it something that was actually broken versus slow?

**Charly Batista**
Oh, yeah. Mostly back that time it was mostly broken. and some things. This is the thing when we went to work on the database as You'll never want to get caught, right? Especially when someone calls you and for the look, but the production is gone, right. And the company that was working it spread to the company so that they used to like to have a branch, they're solid things, the database was down so that the shop was just stopped oh, and it was really on fire. So and then you just got attacked and just found out and, and we didn't have what we have today now is just login SSH, and then wherever it will just fix things right. But back then, that didn't happen. We had I remember that we had the doors dial connection, I used to have the US robotics more than it was also a gigantic one. But I had 56-kilobits per second connections.

**Matt Yonkovit**  
Oh, I hit a 14.4 when I first started, so I guess I shouldn't say that because now everyone's gonna look up when that was a standard. So all that said it's funny, you mentioned like, there was no SSH, I remember having to go in every Saturday night to the data center and go hit restart, like buttons on all of the systems right, and, and that was horrible. Right. But, yeah, so I think that that's something that we have now, today in modern times people still, unfortunately, have to get called in the middle of the night, a lot of us saris are always busy. And a lot of times those are not necessarily those outage-type things. Because there's a lot of automation for failover high availability, there's a lot of different things out there for making sure databases stay up. But we get a lot of that kind of slowdowns. Diego said he'd rather have a dog call at 2 am than a customer calling at 2 am. Yes, I think that we do see that all of a sudden, you'll get the call, oh my gosh, the system is slow. And of course, if you're in the position of being an SRP, DBA it's always the fault of the database. First, let's be honest, it's never the application. Right? And I'm pretty sure that's a universal truth. And that watching can probably justify or, like, commiserate with me. So we wanted to talk a little bit about from a Postgres perspective, what are some of those things that we can do to prevent that 2 am phone call when the system is slow? Because we've got some high traffic, maybe performance, slowdown, some other things? So, Charly, you've been doing this for as long as I have. So why don't you start telling us a little bit about some of the performance gotchas and things to do and not do?

**Charly Batista**
Well, when it comes to performance and database, it's trickier. I would say, we need to start from the very, very beginning, right. And one thing that I've seen all over those years that like when I work with the database, is usually the people are, they spend a lot of time trying to turn in the database they have, like, they go for the configuration, and it's not on Postgres like I've seen on my as growers, and in a lot of other databases, they say, Okay, yeah, we need we were planning for the new system. So we need a beefy machine for the database. Let's buy a beefy machine. Now we can talk about 1.5 terabytes, right? So 300 cores, and yeah, you can have a really beefy machine for the database. And then they go, Okay, what do we do with this, this box, right? So you have this insane box, and we need to do a lot of optimization. And people usually spend a lot of time trying to optimize memory, you're trying to optimize CPU and all this kind of thing. And that's all great. That's all great. Especially because most of the database configuration on it, comes from the core configuration. They're all set up, all settings. The settings from when we use those when our robot is 56 kilobytes, right. So they can integrate, they do not follow what we have to buy. So it's possible that you can have, let's say, 5-10 times performance improvement when we do a really good configuration for your box. And then you get fine for some time. And the system is working and everything is working fine. And when you reach the point, even if it's amazing, your system, or your databases start forming really bad, and then they go, they go, a lot of companies that have a lot of miners do what they do, okay, let's improve the machine, let's improve the box. And so when eventually things have started slowing down. And one thing that I don't see most of the companies doing is trying to understand why the performance is struggling

**Matt Yonkovit** 
So, is it more that they're trying to fix the symptom than it is actually so So, oh, it's slow. Let's just do whatever can make it fast and never fix why it ended up

**Charly Batista**
Let's add more memory, right, let it go. Let's add more memory and more CPU. So let's make things faster. But yeah, the thing is, it's not scalable, it's totally not scalable. At some point, you're going to have 100 terabytes of memory and your database is too slow.

**Matt Yonkovit**  
Is this a myth or not? So in the Postgres space, Postgres works really well on General hardware scrape out of the box for general workloads. But when you start to get these massively sized boxes, sometimes it's just not optimized for it. I've frozen Charlie into freezing right now. Isn't that always the case? Oh, Mr. Charlie, oh, oh, you're back. Wonderful. Wonderful. So I don't know, but I was feeling that air I was gonna start singing to you've saved everyone from that. So everyone can thank Charlie for that. So, Charlie, my question to you as you mentioned about getting these bigger and bigger boxes. And one of the things that I have heard, and you can confirm, or deny that, at the larger sizes, the scalability for Postgres doesn't it's not like you go two times the size, and all of a sudden, you get two times the performance. Because Postgres works really well on the smaller systems and the moderate range systems, but as you get bigger, there, there are some limitations.

**Charly Batista**
Well, yeah, it's true, not only for Postgres, SQL's scalability is not linear, right? It's not linear, you're going to reach at some point that your performance doesn't scale linearly. So it starts to drop and the curve starts going up, especially on Postgres, a huge limitation on Postgres is how to use the resource, for example, Postgres relies a lot on the operational system, right? Yeah. So when I say Postgres relies a lot on the operating system it is that even though Postgres has its internal memory buffer, it's a little subsystem that is delegated to the OS. And most of the caching for the buffer itself is delegated to, to the west. And if you're not careful enough, you can have a lot of data inside of Postgres buffer from and on the cache. So, you can have performance drops. That is usually you get a huge improvement on performance on the pharmacy, when we really understand your data model, right. So, you understand or later model, you will start to desensitize your data model to add the index when the index is needed, remove the index when the index is not needed. Because sometimes they just say, okay, it is low and another index, and then you realize that Postgres doesn't use that index. , just to make a comparison. It happens because the implementation of Postgres decided to do so for the storage subsystem. So MySQL, for example. They use a primary key to order the table, right? So on Postgres, they use heat tables, heat files, so it's just a collection of works one after another that they file on the post, which is really simple how it stores on and on file. And then it's super, it's much cheaper if you just need to do a full table scan because you can just open the file and go from the beginning to the end of the file. So linearly, you do a full table scan, it's much cheaper if you need to go to the index. So you're needing your index to really be a good index for the optimizer to decide to use the index on Postgres. Because when you go to the index, you need to read the key order, if it's like, for example, a B tree. So you're going to have a lot of random IO on your disk. And those random IO from the disk then needs to be translated to find the page inside of the paper itself. So you when you're doing an index scan on Postgres, were just changing the pattern of the access from a sequential scan, that's the full table scan on a Postgres switch to a random IO on when you are using the index, what is not what happens on MySQL, for example, MySQL always does a run a lot of random scans. Because of the fights of Beta, I'm talking about no InnoDB, the file is saved on index order. So it’s always done, that's why on my SQL a full pick was going so much more expensive than it happens on Postgres. Right? So and then, yeah, for example, when we had a customer, they were having a lot of performance issues. And we revealed all the configurations and the setup. And so they were getting the best for the box, knowing that the setup that they have, they have in the back of the box, but was too slow. So then we just did a couple of changes on the data model on some tables, we just had that change a couple of things, and we got around 20% improvement of the curves.

**Matt Yonkovit**  
That's a big improvement. All right. And, um, I actually have a test. If we have time, maybe at the end, I can do it to show everybody. But I've set up something where I've got a benchmark thing that we've been running at demos and things where we use this thing to control like Postgres. And what this right here actually changes is the primary key to varchar. And this one changes it back to an end. And so we can watch it on PMM. Like when we do that we can run a workload and we can say like, what does this look like? When you know you're running here with the integer, you flip that to varchar. What happens? So any guesses on what the performance hit was on my benchmark? Just out of curiosity?

**Charly Batista** 
Well, it is easy to understand, like, yeah, of course, it's gonna drop, especially if you need to rent a range scan, right?

**Matt Yonkovit**  
Yeah. So any guesses? Like just how much an x 5x 30x 20x 100x?

**Charly Batista**
Well, no guess!

**Matt Yonkovit**  
Oh, come on you play the game. Alright. So I'll tell you what, in the test as we were doing this, we were seeing anywhere from like a 20 to 30% or 20 to 30x difference at that percent. Yeah. , and so I think that's one of those things that you need to think through. So we do have some questions popping up here. If we wanted to take a couple. So first one, from Guinness, does anyone have a good way to limit the memory? A single database user is allowed to consume in the single query? And, I mean, and Charly, you can jump in here. But I think that that question is interesting because the answer is really not rubbish. Because even if you limit like the user what, what's available to a user, the file system cache could still consume quite a bit of memory. And the system itself is not going to discriminate where it's pulling data from so if you've got a terabyte size table that one user happens to be reading from, you could potentially limit, some of the sizes of some of the caches that the user itself is but all of that terabyte of data that's potentially being queried is going to end up in the main memory pools. Right.

**Charly Batista**  
Exactly. Exactly. And this is the thing that we need to understand when we are working with databases, there are so many things that go beyond the database itself. Like even though you can limit conserved resource consumption inside of the database, sometimes your database just asks more for the West, because it needs us and the West has more to give, it will be given to the database. And those are the things so we need to separate the layers. Okay, what is the database layer, this is the layer that the user interface is the database. But there's a lot more who's behind that database layer in the west, for example, and I have a question for you. Do you know why when you change the integer to varchar, the performance drops? So significantly?

**Matt Yonkovit**  
There are actually a couple of reasons. I mean, and I'll theorize, and you can tell me if I'm right or wrong, right? Number one you're going to be consuming more memory, potentially quite a bit more memory, especially when you look at something like a UID, or something that is a 32 character field, as opposed to a byte field, which is going to be four, right? So our integer field, which is gonna be four, is a substantial difference in just the memory consumption as well as a substantial difference in the disk space. So I think that those two are definitely something that impacts it. But there's also CPU overhead of comparing and checking the two character fields. And I mean, so so you do see that as both a limiting factor. Now when I did, I used to do the same testing in MySQL.  And actually, I can put that same test in MySQL, and we get a similar performance impact, probably a little worse in MySQL, because I was using that in MySQL, each index has the primary key in it, yes. Which means more space?

**Charly Batista**  
Yep. Well, yeah, those things definitely play along. And also, there is a third one that has a huge impact is the organization of the b-tree itself. So when you choose a UID, for example, your index is not sequential. It's not sequential. So it may look okay, it looks okay. Because in the engine organizing the index, right? But when you have a comparison, a ranch comparison, and you do not have sequential keys that were assertion on the database, it needs to do a lot of random IO. And remember, like, even though, okay, the base in memories is, this is much larger, we have a lot more CPU comparison, but like CPU and memory, it's still way faster when we talk about IO, right? So because you do a lot of random IO, and even an SSD is random, I use at least two or three times it's overdone sequential IO. Yeah and all because like one of the big things that play on SSD, that's probably random IO will never be as fast as sequential. So when you have sequential sequential data, you can prefetch blocks. So if you prefetch that and put in memory that is much faster than just waiting for the CPU to request the next block, and you're going for, for like primer blocks. This is one thing that plays a lot, and also on SSDs. But people think I've moved it from spinning disk to SSD, everything is going to be much faster. Now I don't have random, IO issues anymore with Well, not true, right. And as you said, on databases, like MySQL that has clustered index, they are even worse because you need to carry the primary key for all of those indexes. Yeah, another thing that usually we don't pay attention to when we are designing a database on Postgres is what we call padding. Then when we're saving that data, what Postgres does, it has a word size of eight, eight bytes, that it tries to save all the fields to align with the CPU word size. So if you have, for example, a column that ID is an integer or big integer that has eight bytes, it's gonna occupy 1-word size, right? So if the next one is varchar the CPU doesn't know how many bytes that can occupy. So then it means it can because it's varchar, you can change the size, it can improvise a lot of by a lot of space. If it's at the end of the table, there's no problem because it's used as many words as it's needed. But if it's between two, everything that is not in the length of eight bytes, you'll be bettered to be of eight bytes. So I had a very small experience already with one table, while it was out of seven columns, and all columns were of different types of integers. So there are more columns, right? And I sorted a million rows. Like just put the data randomly and like just like we do modeling, like ID, data updates, Boolean values, or just like you're modeling your database, or just to put the data as it looks, looks, okay. I got, the final size of the table was 75 megabytes. And then I just reorganized the very same table, putting the pet on the optimal position of the columns, and I started the same date, they did an insert selection to get the same data from the previous table, and it was 55 megabytes. So there was a 32% difference in the size of the data just because I reorganized the data.

**Matt Yonkovit** 
 but space is cheap

**Charly Batista**
It is! but remember, it goes to memory and the CPUs need to work on this.

**Matt Yonkovit**  
Yeah, well, and so so Hamid had an interesting comment about, asking if it's a clustered index because a lot of people don't use clustered indexes because they don't even know that they necessarily exist, right? So a lot of people make that mistake, where they're just gonna go create an index, and they're gonna be done with it. So that is an option that you can look at clustered indexing to improve performance. We did have another question from Duleep. And I wanted to be mindful of some of these questions because some of them are good. So there is a question from Dileep, which now actually just disappeared. So I'm gonna go ahead and throw this on the screen. They're trying to insert a 10 million record into a foreign table by using postgres_fdw, and it's taking time for three to four hours, is there any fast way to test it? Now, I mean, I wish Ibrar was here because he knows everything there is to know about foreign data wrappers, right. So he tends to be one of the go-to guys for that. And I think that he said he was asking, ``What kind of tools are you using? But I think a lot of this is for testing, it depends on the outcome of the test that you're looking for. Are you looking for a realistic test, like one that's going to be in production? Are you just looking to generate test data, to get something that you can play with? Because I think that when you start to look at trying to speed up load processes, there are definitely things you can do, things you can disable, you can look at what extensions you might be running and see which ones might be impacting performance, seen about disabling some of those? , I think that you can also look to see if you just want the data, it's probably going to be faster to take the data, and then load it and not go through the foreign-data wrapper, if that's possible, as well, Charly, any suggestions?

**Charly Batista**
Well, for the tools that we can use, well, I like to use this batch, right. So to generate some tpcc test, a single tool, there is one tool that I also like a lot, the hammer dB. So it's very interesting to when you need to generate a massive amount of tests for the database, you want to test performance improvements. And they have a really nice drive for Postgres. It's a pretty good one. And there's the PG bench. The default one for the community of people who are like depends, as you said, depends on what is your goal, what you want to achieve on the test, right? 

**Matt Yonkovit**  
I think from a I think the leaps point was that they're specifically trying to test I don't they're trying to test the 10 million insert, load, or if they're just trying to get in rows over and then test against 10 million rows

**Charly Batista**
I saw another question. The guy asking about the best thing to talk to you. Yeah. Well, this is the postgres_fdw. Well, there are many things that can be impacted. First of all, I want to take a look is network. Are those two databases on the same box? Or are they in different boxes? So how is the networking playing a lot, right? So because when you are looking for optimization, we are trying to follow the 8020 rules, right? you're wanting to try to get the 20% optimization that gives you 80% of profit, right? Then usually you go for that. The first thing is that you go to other things and usually, network IO. And the network in this sense is the slowest. Right? So the first thing we'll take a look at is the network.

**Matt Yonkovit**  
Especially the foreign data wrappers, if you're selling data, let's say out of Oracle or some other database somewhere else. , you might have that in a completely different data center.

**Charly Batista**
So yeah, that's the first thing that let's say, okay, no, they are in the same box. Okay, they are in the same box. If you do a select how long that's gonna take you guys to pull the data from the day from one of the databases, it's all on the order database, do you have the indexes or the indexes enabled, maybe you can just disable the indexes all the shacks by now if the table has a lot of shots, so sometimes it plays a lot, a lot of impacts, right, disable the sharks, do the load, and then just enable the shots again, they recreate the index and helps kind of stuff, right.
Those are usually the ones that cause more problems when we are moving data from one place to another one.

**Matt Yonkovit**  
Okay, so let's see what else we got going on here. So I did see a couple of other questions come in. So I'm working my way through. Diego actually said this path thing is interesting, but why can't Postgres just rearrange the columns under the hood? By default?
Would be nice. Let's be honest, it would be nice.  


**Charly Batista**
Yeah, that would be but, the thing is, it is complex. Especially because you might have a logical reason to have the table on using that sequence, right, that sequence of columns. So the thing is when you put too much intelligence inside of the tool, the chance that something bad happens is too hard. Right? So then, okay, you need to spend a lot of time to develop that feature. That's something that's pretty much easy for the user to do by itself. But how much does it worth to try to add bugs and complications inside of the database itself, if you can use just like the user can be clarified, created by itself?

**Matt Yonkovit**  
And I think that as Hamid points out, that there already have been some optimizations as, as new versions of Postgres get released, a lot of these things start to get better and better over time. And this is where a lot of times the difference between one or two versions and Postgres can make a massive amount of difference in performance for certain workloads. Right. 

**Charly Batista**
That's true. That's true. For this case, specifically I haven't tried on the post was 14, but it still plays a lot on 13.

**Matt Yonkovit**  
No, okay. Okay. And so Hamid you know if that's a 14 improvement! I'm not 100% sure. I remember seeing that in the list. But it was a pretty big list of features. So I mean, I think it's easy to miss some of those. And it's right, it just came out, yes. But I have two blogs and two blogs on it already. So Hamid also has said that Sysbench pG bench HammerDB good tools. Orlando wants to know, and so let's just jump right into Orlando's question here. How and when do you tune the hash memory multiplier?

**Charly Batista**
Well, that's a very specific one.
hash map multiplier. I don't remember the top of my mind.

**Matt Yonkovit**  
As we all go Google hash multiplier to see what it is like. 
I am not 100% Sure Orlando personally.

**Charly Batista**  
Okay, I see. It's used to compute the maximum amount of memory that hash-based operations can use?
Well, thing is, in situations that you, you can use some Postgres can use hash operator operations, like, right, so for example, when you do a full table scan and you need to compare two different valleys, a Postgres can create two hash, they can create the hash tables and compare those two different tables for a join. For example, It's cheaper when you have hash tables identical. So, if you have good indexes, most of the time, you won't need to care about the parameters, the full value.
So  I would go to check why the database is great into many hash tables. So probably because there are no good indexes, and most of the operations are probably going to be because, as I said, it's going to bring some joints or some comparisons and just create the hash table to compare to make it easier. And this is also happening on another one when we have a lot of bitmap operations on Postgres. So there are many ways that the database can compare the data when you join tables, or when we are going for a full table scan, right? So one is to create the hash tables. And MySQL does that a lot when compared to two tables on a joint. Another one is on the bitmap operations. So the database, it can get the data from one table and create a map of bits from that data to make the comparison faster and easier on the database. So if you go to your logs, and you see too many hash tables, but that being created, or too many bitmaps operations that you created, it may be possible that your database design is not optimal, may be possible that you need to reorganize the indexes that you have. So to make the performance a bit better. So before, as I said, before, going, tuning all those many parameters, it's very to understand why your database is performing badly, right? Because the game is much higher. And again, when you turn one parameter for the database, you tend to parameter for all the loads that you have on that database. Yeah, so it's not just one query or, not, it's for all the lines

**Matt Yonkovit**  
Let’s get back to the theme that I mentioned earlier, which is, database design is, is so overlooked, and everybody that I talked to, ultimately ends up coming back to that same conclusion that the number one problem that most people run into is they didn't necessarily think through all of the different implications of how they design something or a table. Right, and how they design their structures. And because of that, they end up spending more they end up running into problems. And it's very easy to overlook some of those things. , I, Charlie, I know you've been doing some work with JSON, I did some work with JSON recently, and the JSON B data types and JSON data. And I've seen users who just implement those raw, and expect good performance.

And they add maybe the wrong indexes. Maybe they don't use some of the generated indexes or functional indexes that you can add. So there's, there's this missing component, and then they just kind of throw everything in, and it's just a dumping space for their systems, which is never going to perform optimally.

**Charly Batista**
Yeah, I have an example.
When I did a consultant for a big corporation in China a few years ago, they were moving their data from a proprietary database to Postgres. And on the way, they were also changing the application key using JSON inside of the database. So they had two complications, right, the first application was moved to the data from a proper database to Postgres. And another complication is you start using JSON, the JSON B file inside of Postgres.

They are having horrible performance, horrible performance on Postgres site. And when we start looking at the problems, we saw that they had one gigantic table with five columns, and that table with five columns, they had 160 indexes on the table. 160 indexes.
Yeah, and the thing is, one of the columns was a JSON B column. So they were using a B tree index to index independent fields inside of the JSON, right?
So then you can imagine how the writing performance will be impacted. Because we need to remember that every time we write to the database, the index needs to be updated. Postgres has this amazing feature that they call hot updates. So when you do an update, and this update can be in place on the same page, it doesn't need to update the index, so that's fine. So but the problem is, how much percent of your page are filled on your database?

**Matt Yonkovit**  
JSON B columns as well? But Jason, will it ever be able to do it? because as we talked about, like JSON, so if you've got a column and you're updating this column, if I recall, correctly, JSON, the update, it replaces the whole document, so it's always never going to fit on the same page, it's probably going to spill over, right?

**Charly Batista**  
Yeah, that's the thing. And that's, that's the thing. And that's what I say. So Postgres has this amazing hot update feature, right, but only happens when the new beta fits on the old page, right on the same page, so it doesn't fit on the same page. So the index needs to be updated. And if you have on the table 100 indexes. So you need to update all of those 100 indexes. Right? So when the performance goes really badly, and this is when the thing comes, okay, we are designed, what is the best option that we can use for this design? Right, JSON is an amazing thing, right? It can help a lot, it can make the developer’s lives much easier. And even the database, if you will,
we’ll use the can make life easier as well. Right? So you can go for the Gini index and our audit acknowledges that we call to go the whole way talking about that. And to change. So what we did, we remove all those indexes, we just, in that case, we apply the G index, we did some tricks, and then we got like 40x improvement performance. 

**Matt Yonkovit**  
Yeah, and I think that's the thing, right is if you properly index, and you don't over-index, and, a lot of times, it is more cost-effective, when you're looking to store JSON, to make sure you've got either generated columns or indexes on this specific thing you're, you're going to pull out quite frequently or even, I'm going to, I'm going to be a heretic here to normalize some of that. So when your app is writing to the database, it pulls some of those columns out, maybe stores them in different tables, optimizes them slightly differently and does some lookups.

**Charly Batista**
Well, that can be done, but we again need to be careful. Because remember, the random and sequential. So what happens is the database cannot read a couple of bytes, a couple of kilobytes from the disk, right? Every time that was something from the disk, it needs to be at least one block, right? So if you don't know that, the normalizer, great, then split the data in between many different tables, you need to ask at least one block for each of those things. If you have a huge table, but I haven't columns on the table, all of that fit on the same or the same block. So then your IO pattern is much better than having a lot of things. So it can make things a lot faster, just because you have way less IO.

**Matt Yonkovit**  
Yeah. Hamid follows up on your example. So yeah, so , just it, yeah, it's an interesting thing, because there are these things that you can have work 90% of the time, fine, but then the other 10% of the time it hits a limit. I think that that's actually a design principle if you will, and I'm gonna go storytime for everybody. And so I had recently so we moved into this house two years ago, or two and a half years ago, and so brand new house, it was built by builders. And so we've got a little half-bath so just the bathroom with a toilet and sink downstairs. We had a plumbing issue. Just recently, where we noticed some of the floorboards started to warp, and we noticed some water. So we call the plumber. And the plumber says, oh, when they installed this two years ago, they didn't install it, right. And it actually was missing a part that was very significant. So there's been a slow leak underneath the floor for two years. And it reminds me of this type of design principle that we often forget, which is, just because something works doesn't mean that shit isn't flowing underneath the floor. And I think that's where, like we from a development perspective, and from a perspective of designing applications right now we're so busy, it's so easy to get something to work, and then just release it, that we often forget that as workload changes, as data size changes, as you know all kinds of new versions come out. It might not work the same way. And so there isn't this effort to go back and necessarily retest or re-verify the decisions you made originally are still valid. And right now, I think I saw the average tenure for a developer is a year and a half to two years at any company. So by the time that something does break, or really go bad, they're probably not there to even experience it.

**Charly Batista**  
, one thing that I've seen over those 20 years ever been work is every time that we when we face a problem, sometimes it's a very complex problem, and also high level, we need to go deep, then we always end up to the basics. , you always end up to the basics on the basic concepts on how memory works, for example, on how is the subsystem gonna work on how the CPU does its job? I've seen so many misunderstandings, rather, the people have on those things that I will say, a lot of problems that's been causing on the database sites on application sites are just because a lot of bodies out there, they don't really understand how the implications of how the memory design or modern hardware they work, right? Yeah, for example, the thing that I just said, the database, it cannot give you a couple of bytes. Even you go, you go to the database, select ID from table user, where ID equals five, okay, ID is an integer on this example. So four bytes, right? So you won't get that one, you're going to get the whole page. If the on Postgres, for example, the page is eight kilobytes. So you're going to get eight kilobytes. If you do that first thing, select many, many, many times on just increasing ID. And, for example, your example that they use the not a sequential primary key, so you need to get that base from the index as well. Right? If it's not sequential, what if you have a split in many, many pages? So sometimes your select that you suppose you could be fit just one page, I get him 100 beats from the database? And then you ask Why so slow?

**Matt Yonkovit**  
There are so many of those gotchas in the design aspect. , I remember, back in the day, I worked at a large e-commerce site on their stuff. And they were using to know where I'm framework and the ORM framework did select star and everything by default. And so as they were querying things, they only needed one column. And they ended up saturating the bandwidth, because they were selecting, like blobs, and text objects that they weren't even using. And it was all sending it over between the application server and the database server, and they actually flooded the network. I mean, it's, it's not easy to do that, especially when you're looking at gig or 10 gig connections between a lot of these, but their traffic was so heavy and those objects are so large that they actually bottlenecked on it. I mean, and I think that's where understanding and getting back to one of the things you said fixing the root cause, not fixing the symptom is super important and critical. 

**Charly Batista**
Exactly. And yeah, and that's another amazing example. Because that's another thing that a lot of people did you did they do not realize is whatever that you select from the database needs to go through the network, right? So whatever you select from the database needs to go through the network. And what is your select time is the Select time, just the time that that database takes to get the data and put it on the network account? Or is the Select time the whole time that the OD doodle activator is guided, and the data is ready for application to use? Yeah, right. Because sometimes the database takes milliseconds, right to just to fetch the data and put it on the network. But the network is slow. Or you as you said, you're putting so much labor inside the network that the bandwidth is saturated, right? And the database is low.

**Matt Yonkovit**  
Yep. So we're approaching the top of the hour here and want to be mindful of time for everybody. I don't see any new questions but wanted to cover a couple of things for everybody. So if you're not aware, we are running a survey, our annual surveys going on right now, which does help not only us, but it helps everybody in the community because it is an anonymous open survey that anyone can grab the data for. It's all open, but nothing is collected. That is PII. So I'm going to go ahead and I'm going to add a link here into this just so I can make friends with everybody who wants me to make sure we talk about that. , so if you do have a second, we'd appreciate it, it takes about 5-10 minutes, that that really does help us. And it helps anybody who's doing research or trying to look into some of the trends on the open-source database side. Also, you may or may not know so So I have this job in the community, and I'm supposed to help connect with you find folks out there who are on this channel. And I would love feedback on what's working, what type of topics you want to hear. , you can say Charlie was awesome. And Matt, you were a dud replaced, Matt, that's okay. I need feedback on, what, what you want to hear from us. And what's working? Well, what isn't? I like to talk. So I can talk all day long, whether you guys want to hear me talk or not. And I'm pretty sure that you want to hear some awesome technical stuff. And topics are always good. We also have I mentioned earlier, our Postgres operator. So if you haven't gotten the chance and you are running on Kubernetes, I would recommend you take a look at it, join up on our discord channel if you need some help, or you want to ask some questions on it. Happy to help out there, I hang out there, several people from engineering hang out there from our service team hang out there, love to hear from you see what's working, what isn't there. And Hamid mentioned that the PG stat monitor is in beta. So we're hoping to get that ga and if you haven't tested that out, that's another great thing to test out. If you want to get involved and, help with some of the development on any of those projects, feel free to reach out to me.
, we'd be happy to chat with you there. And I also do a podcast that is number one in Tunisia. So I am awesome. , I have a big following. They're trying to move into some of the other markets. So we'd love to have you subscribe to that. So go ahead. And, if you're watching on YouTube, or Twitch, like us, subscribe. Really appreciate it. And drop us a line and tell us what you want to hear about, either on a podcast meetup. You want to see a webinar. Tell us we're open. We're here for you guys.
But, Charlie, I wanted to thank you and thank you to everyone who tuned in today. I think this was great. We'd love to hear more from everybody in the community as we go forward.

**Charly Batista**/**Matt Yonkovit**  
Yeah, thanks. Thanks again for your patience. It was amazing. So it was a great talk. Good. Good questions here. Yeah, it's always great to be here. I hope you meet here again soon. 

**Matt Yonkovit** 
All right, well, well, let's get, everybody, out in the community space to say like Charlie should be doing this full time this should be his job is just one to four hours a day, seven days a week. , he'll get on the live stream. I'll send him one of those old pager phones pagers, and he can just get

**Charly Batista**
whenever they get bored because I also really like to talk.

**Matt Yonkovit**  
Thank you everyone for coming. Appreciate it. And we'll see you next week.

**Charly Batista**
Thank you all. Thank Matt again.



![Percona MeetUp for PostgreSQL October 2021](events/percona-meetup/postgres-october-cover-1920.jpg)

The next Community MeetUp for PostgreSQL will be dedicated to Performance and Troubleshooting PostgreSQL. Matt Yonkovit, The Head of Open Source Strategy (HOSS) at Percona, is hosting the talk with Charly Batista, PostgreSQL Tech Lead at Percona, for one hour live streaming followed by Q&A. This is a part of our regular monthly event to talk about databases.

Join us for an hour MeetUp for PostgreSQL

* Date: Wednesday Oct 13th, 2021 at 11:00am EST

* Live Chat : on [Discord](http://per.co.na/discord)

* Live stream on [YouTube](https://www.youtube.com/watch?v=rAuz1usu9Z4) and [Twitch](https://www.twitch.tv/perconalive)

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=Nm9yczkzZTFvYmN2OWVuZjY5Z2o5bnR0N2JfMjAyMTEwMTNUMTUwMDAwWiBjX3A3ZmF2NGNzaWk1ajV2ZHNvaGkwcTh2aTQ4QGc&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com&scp=ALL)


This week, we will focus on **Performance and Troubleshooting PostgreSQL** with Charly Batista. He will highlight:

- Percona approach to performance improvement.

- The tools we use to monitor and observe customer environments.

- How to prevent performance issues BEFORE they occur.

- How some of our customers have learned and benefited from Percona optimizations.

Community MeetUp is a Live. Chat on Discord to ask questions and get answers from Experts right away! Your feedback is welcome to help us improve upcoming events.

The MeetUp for PostgreSQL is recommended for everyone who is:

* User of PostgreSQL.

* Student or want to learn PostgreSQL.

* Expert, Engineer, Developer of PostgreSQL.

* Thinking about working with databases and big data.

* Interested in PostgreSQL.

**Go ahead and come with your friends!**

Subscribe to our channels to get informed of all upcoming MeetUps.

Invite your friends to this MeetUp by sharing this page.


