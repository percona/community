---
title: Percona MeetUp for PostgreSQL November 2021 - Autovacuum
description: 'Highlight and discuss the autovacuum in PostgreSQL: How to stop worrying
  about it and even love it!'
images:
- events/percona-meetup/postgres-november-cover-1920-2.jpg
date: '2021-11-17'
draft: false
speakers:
- sergey_kuzmichev
- matt_yonkovit
tags: ["Meetup", "PostgreSQL"]
events_year: ["2021"]
events_tag: ["Community", "PostgreSQL"]
events_category: ["Speaking"]
---
Listen to the full recording of The MeetUp for PostgreSQL of November 17th. We have talked about autovacuum in PostgreSQL with Percona Senior Support Engineer Sergey Kuzmichev. Matt Yonkovit, the HOSS at Percona, asked Sergey to resolve a database issue live.

## Video

{{% youtube youtube_id="PtWQFkTt1Bo" %}}{{% /youtube %}}

## Transcript


**Matt Yonkovit:** 
Hello, everybody, sorry, we double clicked on the video clip there. Look at how are you, Sergey? Welcome, Sergey, welcome, everyone, to another Percona meetup on our regular live stream Sergey, how are you doing?

**Sergey Kuzmichev:** 
I'm doing great, great. How are you Matt?

**Matt Yonkovit:** 
Good. Thank you for stopping by. We always love to have have you come out and chat with us and let's see.

**Sergey Kuzmichev:** 
It's my pleasure.

**Matt Yonkovit:** 
Vinny says that he loves you by the way

**Sergey Kuzmichev:** 
I know we wrote a book together. 

**Matt Yonkovit:** 
Yes, you wrote a book. How did that process look?

**Sergey Kuzmichev:** 
Oh, well, it looked like a lot of self reflection, self criticism, disappointment in your own powers, but then it came to fruition and now it's a great book. So yeah, but it's not about PostgreSQL. 

**Matt Yonkovit:** 
Unfortunately, it isn't, it isn't. But it is about MySQL, right. And so we were going for those who are here for the postgres content, we will get there in a second. But Sergey did write a really interesting book on MySQL, with Vinny and it's worthwhile mentioning, if you haven't gone out and seen that, take a look at Learning MySQL. And let me see if I can pull it up. It is available everywhere books are. And I'm going to, I'm going to do this if this is like an infomercial or quick, like, plug for the book, right? So let me go ahead and I'm just going to throw this up on my screen just so we can, we can see that. See. So if you're interested in learning MySQL, check it out. Look at that. It's on Amazon. And it's available everywhere, books are sold. So look at that. It's even got a five star rating. So check it out. Support our local folks. Oh, and look at that. Gonzalo is here just for the elephant hats.

**Sergey Kuzmichev:** 
I have a plush elephant Toy Box.

**Matt Yonkovit:** 
Do you? Where's your elephant toy? You should get it? 

**Sergey Kuzmichev:** 
Well, that's an interesting thing to grab.

**Matt Yonkovit:** 
Yes. So for Gonzalo we're gonna grab the plush elephant toy.

**Sergey Kuzmichev:** 
It's seen better days. Getting a bit worn out. But it is here.

**Matt Yonkovit:** 
Oh, and what is it from? It's from Postgres.

**Sergey Kuzmichev:** 
PG Day Russia 16.

**Matt Yonkovit:** 
16! Wow.

**Sergey Kuzmichev:** 
 That's kind of an old elephant. I can go to school. 

**Matt Yonkovit:** 
Ah, well, so if you haven't seen the book, like I said, check out Sergey's book, but we're here to talk about Postgres. And Sergey, for you. Postgres is something that is near and dear to your heart. Obviously, you were participating in the Postgres community back into what do you 16? So five years ago?

**Sergey Kuzmichev:** 
Yeah. Yeah, I wasn't doing Postgres before coming to Percona, where I picked up MySQL, which led to me writing a book about learning MySQL, because I was learning MySQL just not a long time ago. But before that, I was doing PostgreSQL. And yet before that, I was doing Oracle. So for a lot of US Open Source folks, I started with Oracle, and around 2010. And then in 2015, I went to become any you feel at the time the DevOps engineer, but I retained my DBA specialty, and I picked up the databases, and I looked after them. And those were PostgreSQL databases. Yeah, then I had to learn PostgreSQL the hard way. So I was an Oracle engineer. A week ago, I became a PostgreSQL DBA a week after I joined, so yeah.

**Matt Yonkovit:** 
 What version of Postgres was that by the way? 

**Sergey Kuzmichev:** 
That was 9.2, I think when I joined, and I left at 9.5.

**Matt Yonkovit:** 
Okay, so I remember way, way back in the day, like, I actually wrote a couple video games like web-based games. And I came from an Oracle background as well. And I used MySQL and Postgres, and I kind of switched between them a couple of times, early in the days, and that was my first kind of experience with Postgres. And the thing that always stuck with me was having to vacuum. And it was such a foreign concept to me coming from Oracle, right, because as an Oracle DBA let's be honest having to vacuum your database, you're like, what is that? What's that about? And it makes sense once you understand it, but you wanted to talk today a little bit about vacuuming auto vacuuming specific, though, but oh, maybe fill in those who are listening who don't understand what a vacuum is, and we'll start there. 

**Sergey Kuzmichev:** 
Yeah, well, yeah, that's for you. For me. The whole idea behind this stuff was really foreign. I'm really unexpected. Like, for instance, MySQL is much closer to Oracle and how it deals with the stuff not to come to the vacuum and to auto vacuum, I guess we should start with a bit more fundamentals and with the MVCC model or the multi-view concurrency, right, because the vacuum is a direct consequence of how PostgreSQL organizes the data in a way that multiple queries can read multiple row versions, right? So this whole thing is about that. And the thing is that unlike many other databases, PostgreSQL doesn't have an undo, doesn't utilize any form and undo and it just stores row versions right there in the table. That's right, for me it was quite kind of surprising to me when I started to work in this PostgreSQL, right. So

**Matt Yonkovit:** 
It is just so for people listening, but basically, what that means is you go to, let's say, you have a row, and that row has your name and address and you, someone in the system, is updating your address to a new address. In a lot of other databases, what they'll do is they'll keep the original address information, the changes in an undo space, that will eventually get cleaned up. Postgres keeps your old address in new addresses in the same physical location. Right. Sergey? That's, that's what you're saying.

**Sergey Kuzmichev:** 
Right! Exactly. Right. Specifically, if you have free space in the block, it will just be in the beach, it will store the next new row version in the page, right. And to do save, it has to, there is a whole machinery for storing this, like you have to account for the transaction that inserted the row, that transaction that deleted the row, or like updated the row because the update and PostgreSQL is just delete an insert, consequently, for the data model, and what happens with the row that you do, like when you say my address was changed, right? So I had address A, you updated it, or somebody updated it, and now it's address B, but there are actually two records in the data file, there are going to be two records for me. So why do we need that? How do we, how do we deal with them? Right? So we name that, because we all like our databases, modern databases, relational databases, for how they allow us to write queries. And kind of expect that if you run a query, you will get results. For the time the query starts, or even more was a repeatable read, you can expect the whole transaction to be consistent, right. So for that, you actually need those rows because maybe a transaction started before you update my address, it will see my old address, the new transaction that starts after you can make it will see the new address. So for a while two addresses are completely valid. So this is the whole basis, and the whole foundation for the vacuuming for autovaccuming for the whole machinery for those actions. So now there are two-row versions. Eventually, my original address will never be seen by anybody. We will come back to that in a while. But there are no transactions that started before you updated my address. Right? So nobody needs that one, the vacuum comes because we have basically an unused row. Nobody will ever read it. Nobody needs it. So what do we do, we could rewrite just the full table, just take the consistent data that is actually required, and write it down. But that's expensive. So PostgreSQL quite a long time ago. I actually don't remember when I was there, when I found it introduced the concept of vacuum. And the vacuum. And also like in which we will come to is the process that goes ahead and removes those versions. It actually does quite a bit more than that. But yeah, the gist of it is, it is basically garbage collection. So yeah, wilded at it. Yeah, so for maybe developer folks who work with languages that do have garbage collection. It is kinda like garbage collection, you have an object reference, an object that has no references, nobody can ever access it and just there it sits on the heap. Right. It's that.

**Matt Yonkovit:** 
Yeah, and I think that's a good explanation for that. Because I think the concepts there make sense once you hear them out, but when you hear like the process of vacuuming, it's like, oh, wait, why? And the fact of the matter is, that process is really required, otherwise, the database starts to fill up with those dead unaccessible rows. And it starts to cause bloat, and not only does it cause larger amounts of data storage, it also slows down queries, and it slows down other activities because you actually have to search through even the ones that are not available.

**Sergey Kuzmichev:** 
Yeah, and it also has an effect on your indexes, because indexes are not versions in the same way. In simple terms, you can think about the indexes, and possibly scale as having references to every row version. So when you traverse an index, when you come to a leaf page, without going to the table and reading every row version and checking it against your current view of the transaction, your snapshot, you cannot know whether the row that you read is gonna be available for you or not. And that, unfortunately, eliminates the Index Only Scan optimization, right? So the one we love, where we just store a bunch of data in the index, and we never really need to touch the heap, basically the table, but we cannot do that. If the table is all bloated. You have a lot of that rose. 

**Matt Yonkovit:** 
So yeah, no, and I think that's one of the critical things that a lot of people miss, and I know, eventually running a vacuum process, when it started, was a manual process. And it was a very heavy process. It's not something that you can do just in the background, without impacting the performance, because you're basically rearranging your sock drawers if you will, right you're rearranging how everything is set up. And that has an impact.

**Sergey Kuzmichev:** 
It actually has improved quite significantly now. So the major difference? Well, I guess we were talking about auto vacuum here. So the vacuum, as I said, is a garbage collection. So it comes and cleans up the table, if you run the vacuum on a table, what it will do, it will traverse the whole table, it will get all the topples, it will populate the array in memory, it will also rescan the indexes, and eventually you will get a table that has zero rows, ideally, not in every situation. But it's awkward. It's like gathering statistics manually; the statistics are universal for each database. So I like the statistics analogy, whether you're using MySQL or Oracle, of course, we just kill you, when it's fresh statistics for the table like it changes you need to adjust. Maybe you have a data skew, right? So running a manual vacuum is like running a manual stats collection, right? Oh, it might work. But you also might miss a point between the rounds, where the data change significantly. So you can schedule a right vacuum to run like every night of hours. But then in the middle of the day, you have, well a lot of transactions that update and generate a lot of dead rows. What you get done is a decreased performance for the rest of the day. Or you will also get a larger table because in the end working doesn't reorganize, right.

**Matt Yonkovit:** 
Isn't it really a trade-off though? So okay, so when you're talking about running vacuum more frequently, they can run faster? Yes. But there is a performance impact. So at a certain point, it's almost like what is the performance impact of having a lot of dead rows greater than the performance impact of running a vacuum?

**Sergey Kuzmichev:** 
That's a great point. But yeah, before I get into that, the good way to deal with the vacuum is to run the auto vacuum. And that's what I was going to say instead of running vacuum scheduled, you run the auto vacuum and auto vacuum is a bit more intelligent, it's still not really intelligent, but it isn't that intelligent. Now, it doesn't work by time, you don't schedule it, it works by the activity. So if even a certain amount of rows or a percentage point of the table changes, it will activate and it will process that table. Right. And then we come to your question, what is the trade off? Right? So there are two kinds of points on the spectrum, the one where you don't run a vacuum at all. And the one where you run vacuum, let's say after every row is updated in neither of those is good. Because nothing is black and white, and we need to try to optimize for everything. Right. So yeah, well, that's about its point.

**Matt Yonkovit:** 
Yeah, and I mean so that the concept of autovacuum. Right, is that it automatically runs, but in this is where I see that there is debate, and I've seen people talk about some of the downsides of vacuuming too often or frequently because it does slow down. Your production. So I've seen people actually take and delay that as long as humanly possible. But then they run into other issues, because you can actually, you know that there's some events that you'll actually run out of certain counters internally that can completely see Sergey knows what am I gonna completely seize up the system?

**Sergey Kuzmichev:** 
Yeah. But even before that, you will have significant severe performance issues, because you will have to run the vacuum, eventually, we will talk about the counters, right. And the counters are one of the grave outcomes of not running vacuums. But when you run an auto vacuum, or you run the regular vacuum, it needs to pull to topple row references into the main memory, a memory area. And that memory area is unfortunately, final, right. So you control it, you can set the worker offs, it's not work, ma'am, it's the maintenance work, right? You can set a pretty high, you can set it to two gigabytes, five gigabytes, unfortunately, it's allocated or in full. So once you run the vacuum, you will get five gigabytes of memory eaten up. And here, the interesting thing is, if you have more than rows that would fit into that memory area and not rows, but their references anyways, you will have to repeat the operation of the vacuum and on the table, it will like continue, because it will actually process the rows. But every time it does, it has to rescan every index on every document operation and scan all the indexes we talked to you a bit ago about indexes, right? And I said you don't, you probably don't want to have too many indexes, you probably don't want to have too many indexes, because your records and we'll have to read every single one of them in full. And probably many times if you don't have enough memory. And so that memory usage is proportional to the amount of dead rows, not the size of the table, thankfully, and say, Well, yes, if you delay your vacuuming too far, like you decide that I want to keep it on, I'm really on that row there, it's fine, I have all the space I need. Maybe I use a cloud and the storage is auto scaled, and it's cheap. Or maybe it's expensive, but I have the money. The problem is, once you run the vacuum, eventually, you will have to rescan every index desperately that will have an impact on the database. Right. And that even before we come to the question of visibility.

**Matt Yonkovit:** 
And I mean, so I think that the fear that I often hear is with auto vacuum, you don't really control when it's going to kick off so it can kick off in the worst time.

**Sergey Kuzmichev:** 
Yeah, it probably will. But

**Matt Yonkovit:** 
Sergey, thank you. 

**Sergey Kuzmichev:** 
Yeah, it will kick off at good times, it will kick off at bad times. So to kick-off, it's all the time, right? Because, like if you have I don't know, if you change million records every hour, and the tuner autovacuum to random tables, when the million table million rows are changed, the autovacuum will scan that table every hour. It doesn't know whether it's your busy hour or non busy hour. The question is, if you postpone it enough, will that be difficult? Or does the vacuum-like failing to scatter multiple indexes? Will that be in your good hour or bad hour? So as you can probably guess by now I'm pro auto vacuum like I like to run. I like it to run frequently. Although the right situation, like undoubtedly, I made a table but was really a megabyte size table, I allowed it to blow two gigabytes in size, because it's still fine, funny numbers, right? Even though it's 1000 times over half. And it had a lot of the drives, I don't care because as soon as autovacuum was executed, it could process it in a few seconds, right? But what I see is, I don't have a five terabyte table, but that's a great example, but a few 100 gigabytes tables, which is allowed to blow, which is allowed to get 20% of its rows. That right 20% Of The Dead rows in a 500 gigabytes table is well a lot of rows. I can't do the math properly. On camera, at least what is really a lot of rows and then when the auto vacuum will start and the math is difficult, because he like you can probably guess that 1000 TPS if you ran out a vacuum every change of 10,000 like radio sets will run every 10 seconds or so 20% difficult and will scale as the table grows, right?

**Matt Yonkovit:** 
But this is why there's two parameters for the autovacuum. Right? So you've got the scale factor and the threshold. So yeah, I mean, that's really what that's designed for, right is to ensure that you can do either a percentage or an exact number.

**Sergey Kuzmichev:** 
And they are summed. But if you set the ratio to zero, the the factor the the factor to zero, but the number two absolute value to your high number, like a million rows, you will get a scan every million rows, right. And those are configurable by table, right. So you can actually update every table, like if you really want to get really into fine-tuning the auto vacuum, which I don't recommend, because it rarely works. And you will forget about that. And it will wreak havoc for you and surely, but you can conceivably get ahead and fine-tune for each individual table in each database, right? So you can control the autovacuum. But the greater point here is what a vacuum actually is, apart from it using up some resources on the system. As my colleague, Jobin likes to say, the auto vacuum was really gentle. So it is optimized, the auto vacuum process is optimized to be really light on the system to do just enough job to do just enough to produce just enough loot to process services, right? So by default, it actually sleeps every 20 milliseconds. doesn't sleep every 20 milliseconds, but it has a set amount of work it can do. And by default, I think I can process like 200 pages at most, for 20 or 10. If it reads them from the disk, so not all the pages and then it sleeps for 20 milliseconds. So yeah, we'll have to read the data, but it will be doing it really, in a really based way. Really likely not like your I don't know, update on a table that likes updates every rep. So

**Matt Yonkovit:** 
yeah, and I think that I think that's one of the things getting those, those those tuned properly is so critically important. Right? And, um is and just to let everybody know, there is ways to fine-tune individual tables even.

**Sergey Kuzmichev:** 
Yes, yes, yeah. So you kind of chase, you can adjust the relational options. So every table in PostgreSQL has sort of a column called row options, you can alter individual table properties, you can set the scale factor you can, you can set when it will be when the rows there will be frozen. And yeah, you can do a lot of stuff, you can even disable auto bake them for a table. Like if you know what you're doing, you can just go ahead and disable auto vacuum on the table as well. That's probably never a good idea. At least I can think of any conceivable reason to do so. But you can write and you can disable it. Or you can disable it to vacuum everywhere and enable auto vacuum on a few tables. Okay, I'll do that. Probably the one. I can check. But you can override, you can disable auto vacuum.

**Matt Yonkovit:** 
So don't fear the autovacuum. 

**Sergey Kuzmichev:** 
Yeah, that's my point. Like, that is my point, the autovacuum. I have two issues, kind of the one issue I see is again, the good, good. I think a good analogy is table stats. When we talk about stats collections, a lot of people think that automatic stats collections are bad, because they skew the data and so on and so forth. And so they auto vacuum like a trance automatically, but it runs unpredictably. It runs at unpredictable times, it will produce unpredictable load, although that is not true, because you can actually calculate the load. At least guess it. So I don't think that you should ever disable auto vacuum. And I want to get to the point that he was bringing up with the visibility of the rows. But the other problem is running with the default settings, right until every auto vacuum execution is so hard on the system that it is actually a problem. Right? So the default settings and PostgreSQL. It's actually pretty common. I think it's universal for almost every setting of PostgreSQL. They are pretty good, you can survive for a long time with them, but they are not tuned by any means and they are suitable for, I don't know, a small development thing since maybe like QA environments maybe. But in production, at least in larger systems. You will overgrow the parameters pretty quickly. And let's say the default value of 20% of rows to be changed before the auto vacuum executes. That is quite a lot, right. So, you will get a substantial amount of work to be done by the autovacuum once it runs. So, maybe if you have a single outstandingly large table, you should think about maybe overriding those on that table, if you have a lot of large tables, then you can probably think about changing the parameters on the global level, not at the system level at all. Right. So because as I said, the rereading of the indexes, while the vacuum was running, happens proportionally to the amount of that rose. So, unless you have an infinite amount of memory, and you can set your maintenance work mem to like terabytes of memory, you will eventually run out of that memory, you will have to rescan the indexes. And that is what is causing major grief, right. And also, the auto vacuuming doesn't release the space. Because it cannot it cannot release the space and like the beginning of the table, where you have few that rows, and then there is a single row version, but the others are that you cannot give back to the operating system like it's just an empty page half full, but maybe if the page changes later, it will be stored in the same block. But if that block was still filled in it will have to allocate the other blocks. So by running autovacuum more frequently, you come up bloat more efficiently. So which one of them I wanted to touch on, like what will we see, actually, if we disable auto vacuum, right, Matt? I think you started touching on that point. 

**Matt Yonkovit:** 
Yeah, so what happens when you disable auto vacuum? What do you run out of?

**Sergey Kuzmichev:** 
 bad things you ran out of space, you run out of space, you run out of performance, and you run out of the transaction counters are actually the transaction counter visibility in the transaction visibility, although the last thing is no more thing, at least, when I started working with PostgreSQL the recommendations, which are still available, they're kind of they're still available, they have like huge disclaimers about running out of the XIDs, right? Because you cool people have corrupted their data. Because if we go back to the start of this kind of made up and me talking about the rows, I mentioned the transactions, they see the versions of the rows, they can see that rows, right, but then rows have an ID, each row has an ID of the transaction that inserted it. And in PostgreSQL, each transaction sees 2 billion of transactions before. So before and after it, okay, I will do like this, I have to hold myself because of my fingers. So what happens if we go past the horizon? Suddenly, there's transactions that were in the past and the rows, the rows that were in the past are now in the future, which is bad. We don't like time travel, at least not when it's a database, right? I wonder if we wrote something down, we want it to be always visible and never in the future suddenly like it never was there. And that is what will happen eventually. Thankfully, PostgreSQL will never allow that to happen. If it does happen. It's about a serious issue. But really, it probably won't happen. Whatever scale will shut down, it will prevent startup, it will make you run the manual vacuum to prevent that. But even long before that, it will actually run a special vacuum, a special aggressive vacuum to prevent a wraparound that has a few properties compared to the regular auto vacuum. And even before that auto vacuum will actually do the work necessary to prevent those bad things from happening. Right. The really simple term, what works that I mentioned, is freezing the rows. So when the rows are frozen, the ID of the transaction that inserted it is marked as always in the past. That's basically it. So that row that we processed is basically always visible for every transaction in the system forever. And ever unless, until we change it. So that is really important for PostgreSQL. Although not for reasons that people usually think.

**Matt Yonkovit:** 
Yeah, It makes sense. Now, by the way, I disagree with you. There are some times when I would like time traveling in my database, like when I can go back and get a bigger bank account, like when I have money, like, I'd love that. But I understand the concept and the concerns there. So that's completely understandable. So, for those who are watching, feel free to just throw out questions, or comments, if there are things that you want to ask, it doesn't even need to be related to this topic. We'd like to kind of go down the rabbit hole of whatever is top of mind for those out in the community. So don't be shy, feel free to ask the questions. Because if not, then I get to play my favorite game with Sergey, who is the expert. Oh, look. So as soon as I predicted, I stumped the expert, and I was going to throw some interesting questions. And let him look at some workload, we get a question. So let's go ahead and pop this up. So what's the question? From Dinesh I have a few tables of size. so terabyte, when autovacuum wraparound gets executed? It takes several hours to complete. I think it takes a lock on the table. Are there alternatives for this?

**Sergey Kuzmichev:** 
Right. So that is actually what I mentioned as a consequence for the database, which is from autovacuum, not executing like most people think when they think about autovacuum at least from my experience, they think about bloat. They like that it goes like this bloat months and then wrap around because it's really hard to get wrapped around and prosperous code like it's almost impossible. Even the developers discuss on the forums that triggering the wraparound condition is exceptionally difficult right now but what happens here is the tables are large. And I'm sorry, I don't know the settings. I don't know the setup. But I would guess that the settings are the default. And so for really large tables, the autovacuum will trigger after a lot of rows are going to be changed. But the age of the tables that XID counters have the visibility of the rows the age of the tables, which is what is triggering the wraparound issues, it doesn't change. When the table is updated, it's changed whenever a transaction executes a real transaction that changes data. And so you can have a table that doesn't change, which will get hold, and on which the wraparound protection vacuum will have to execute. And so and then auto vacuum to prevent wraparound is not really an auto vacuum. It's like the auto vacuum's evil caused them. It's like well, Luigi, or something because an auto vacuum, if you like autovacuum is nice. The auto vacuum was running, it's doing its thing and you need a lock on the table, you want to alter it or you want to do something so not only can release logs, it will just die off, it will print the message in the error log if you configure it to do so it will tell that it was aborted or canceled, right. But the wraparound vacuum, it's gonna execute until it's going to execute, right? Even if you cancel it, you can go ahead and cancel it to remove the locks. The autovacuum Launcher will just launch it again. And it's actually a pretty efficient way to release the deadlocks, because what I see sometimes is people execute DDL on the table. And what? So to answer this particular question, I think it takes a lock on the table to write it does, every vacuum does take a lock on the table. And that lock prevents you not from issuing DML. You can still update the table insert rows, but it will prevent you from executing DDL. And if you execute DDL or your regular auto vacuum will release the locks and die. The wraparound protection prevention auto vacuum will not release the lock. So you will have wraparound protection prevention vacuum, they will have a DDL and then everything else that is behind the DDL waiting to get a lock will get stuck. Because now you have a lock contention on the table. So what you can do in this situation, just as an incident resolution, you can just go ahead and kill the reference vacuum, you will not lose any work because it doesn't get updates on what it does. So it will just get restarted. So what are the alternatives for the wraparound auto vacuum? The alternative is regular auto vacuum.

**Matt Yonkovit:** 
Adjust your threshold and scale factor to yes exact more frequently.

**Sergey Kuzmichev:** 
 Yes, because again, the larger the table, the more rows have to change to trigger the autovacuum because of the scale factor, because you have that scale factor that plays into on the number of rows and I saw systems live systems in production, where some tables were never actually auto vacuumed. Apart from this wraparound protection prevention vacuum. Because of the wraparound prevention or vacuum or auto vacuum, it launches after 200 million transactions have started from the database. And 200 million sounds like a lot. But if you have 1000 TPS, I think that's like a month basically, you by now you have so many TPS on the databases, the databases are so loaded that he can run out to that 200 million counter pretty quickly. But the tables, the large tables might not have enough rows changed in that time. They will see that they will wrap around the auto vacuum. So my suggestion is do adjust B scale factor drug do try to adjust the scale factor for these large tables and make sure that autovacuum is running on them and not the wraparound production prevention vacuum. It is much better to have it. 

**Matt Yonkovit:** 
The default is 20%. Right? A scale factor of 20%.

**Sergey Kuzmichev:** 
I think yes. Yes. 

**Matt Yonkovit:** 
Which would mean that would be 200 gigs.

**Sergey Kuzmichev:** 
Well, it's not 100 gigs. It's two, it's 20% of the row. So if you have a billion rows you have to change. 

**Matt Yonkovit:** 
Yeah, you're right. Yeah. Think of it like that. Like if you've got a 1000 gigabyte system potentiall , you know 20% of that, you know? Yeah. Yeah. And follow-up question, does regular auto vacuum produce the XID count?

**Sergey Kuzmichev:** 
Yes, it does. Ah, the rest as the default is after 50 million rows after 50 million I'm sorry, rows transactions eventually after talking about vacuum, you get you have everything nice a few 100 million amongst friends. Yeah, so after 50 million transactions are executed. And basically, after the nature of the table is past 50 Millions, regular auto vacuum when doing its work, we'll consider we'll actually do the freezing for you. So it'll pick the rows and it will freeze them actively. And after 150 million rows, it's going to be even more aggressive. So if you do have regular auto vacuum runs on your table, you will not see the wraparound protection vacuum happen. The rescue cases that will happen there are some tables, which will never auto vacuum. Right, then those tables are pretty special. And PostgreSQL has some improvements recently for those, but the tables that may never get auto vacuum that may only ever have the rubber on protection vacuums are the read-only tables and the insert-only tables, because we are talking about changing rows. But if you are only inserting data, nothing is changing. So although I can well not trigger it, like whatever scale you set, just know it won't happen, at least until PostgreSQL 13, which improved that and now insert only tables are getting autovacuum specifically for that reason. And also to update the visibility map to index-only only scans work. But read-onlyonly tables aren't. So one thing I noticed is that, like you load a large table like from the dump and you use its a you just run selects on it. But eventually the wraparound back prediction vacuum will execute on the table might be kind of hefty.

**Matt Yonkovit:** 
Okay, Excellent. Thank you for the question. Dinesh. Appreciate you hanging out and ask him. So thanks for that. Are there any other questions? Because if not, my phone's ringing. Oh, I got a slow Postgres database that I nSergey’srgey help with? Oh, we're gonna look at this slow Postgres database, everybody. Sergey, are you ready? Yes, I am. Okay. So I am going to show you PMM. And you get the call that the database is slow. Okay. So I can either give you theURL, if you want, I can, I can send it to you. Or I can just share my screen. What is your screen share for now? How's that sound? Yeah, it just hurt. I think it's gonna be fine, right? So let me go ahead. And I'm going to get here. And, oh, here we go. And I could zoom in if it is too small for people. I always have a problem with getting screen sharehare just right, so we can see what's there. But let me go ahead, and I'll zoom in even a little bit. So let's see. So Sergey, my Postgresql server that's running right now is slow. Alright, are they? 

**Sergey Kuzmichev:** 
So! Oh, great. I like the PMM. Let's go

**Matt Yonkovit:** 
By the way, Sergey did not know that I was gonna do this. So this is totally off the cuff. And and you can't hold them responsible for any of this

**Sergey Kuzmichev:** 
This is all because you didn't ask me questions. 

**Matt Yonkovit:** 
 Yes. As if you would have asked more questions you could have saved Sergey from a fate worse than death, which is looking at my PMM instance. 

**Sergey Kuzmichev:** 
All right, do that. So what I would like to do is I would like to go on and check your operating system node. So if you go to services? Yeah. 

**Matt Yonkovit:** 
Where am I gonna go here, like the system node systems? It's a database, right? It's not the summary. Nodes. No, no, no, not an overview, right. Always mix this up. You want a summary?

**Sergey Kuzmichev:** 
I want a summary. Okay. Show me your node . Show me the node. Let's see. 

**Matt Yonkovit:** 
So how do I see no name? The name is 162? Nope, that's the MySQL one. So let's see is this though?

**Sergey Kuzmichev:** 
Does it have PostgreSQL? Yes, I think this one's the one to hold on a second. Let me just double-check. 

**Matt Yonkovit:** 
See, I should have prepared a little bit more here. But you know what, that's how I roll. You're getting the live on adulterate note for one that lives on. So this is my node here. 

**Sergey Kuzmichev:** 
Oh, right. And it's burning up.

**Matt Yonkovit:** 
burning up. Look at that. Look at that. I'm gonna go to the last hour. It is burning. 

**Sergey Kuzmichev:** 
Okay, so a lot of context switches. So let's see what's happening. Is it all CPU kind of scroll down? So I thought,

**Matt Yonkovit:** 
Well, let me start this up a little bit. Okay, so we saw some issues. That happened. You see, like the context switches start to change. Yeah. And the number of processes changes as well. 

**Sergey Kuzmichev:** 
So, yeah, so let's see what happened to the disk, I just want to understand where we are in regards to the CPU and the disk. So are your activities dropped? So you are CPU? CPU strain, so it's all CPU load that is causing this. So let us go to the PostgreSQL overview. 

**Matt Yonkovit:** 
Okay, we'll go to the postgres overview summary overview again, the whole overview.

**Sergey Kuzmichev:** 
Yes, I am. So let's see. It's easier for me because you are removing the annotations, which could say like I was doing that I was doing this. Yeah. I added the annotations. One funny thing is that it is kind of idle. Wait a minute. Was it 44? Sorry. Yeah, I think 

**Matt Yonkovit:** 
I need to rename these so that this is better. What's interesting is, we should file a bug that we should maintain the service name across when you switch.

**Sergey Kuzmichev:** 
I think dust mostly but maybe because we navigated to the overview, it got reset. I don't know. That's a weird one. But anyway, okay, so here you go. So let us see you have fewer idle connections in your reading a hell of a lot of topples. So can you scroll down a bit for me? Yes, read tuple activity is really, really high. But you don't have so many changes. And the transaction counters have dropped, which is maybe either because you have changed, you have a change in the workload, which switched from writing to reading. Maybe we're maybe because you're reading so much your right transactions don't get enough. And they're just not pushing through as many rows as they could. Right. And the duration of the transactions is really, really high. So we are talking a bit about the vacuuming and the sad wraparound and the whole thing. The auto vacuum can only any vacuum can only clean up rows that are invisible in the system. And by invisible, it means that no active transaction is able to see them and it doesn't really matter if that active transaction would read them the database doesn't know. So if you have a few hours long transactions, within those few hours, the rows that that transaction could see will never be vacuumed. So even if you run auto vacuum really diligently, you have exceptionally, really long queries or long transactions, which will make your database probably an OLAP. Right? Or actually, what's worse, a hybrid with LTP OLAP workload then you have nasty issues with the autovacuum PostgreSQL doesn't really cope very well with mixing glows. 

**Matt Yonkovit:** 
So the longer the transactions here Yeah, the more difficult you're going to have. 

**Sergey Kuzmichev:** 
Yeah, you will have more and more that rose you like yeah, it's gonna happen. So the auto vacuum kind of process so what do we see here? Well, I was just playing alone to our main theme, but yeah, the duration of transactions spikes from 10 seconds to like 15-20 which is not okay. Like it's not nice and you have idle transaction queries, which is also what I said those transactions are, haven't yet executed the comment. They're just not allowing our database to work. You have a lot of temporary files being created, and the temporary file sizes are growing. So, I would recommend that we take a look at your reading activity. So let's scroll down a bit. And then we will go to key down. Okay. Locks. Row exclusive snow, access Sherlock. Movies chase some tests, we won't see them nicely here, we even see the hot table here. Why will I guess? Because you have quite a lot of locks above, on the number of blocks panel. You are, I think you have access to a share lock movie, Json test, and we do some tests in either a database or a table. I don't really remember on top of my head, but so we have our probable hotspot in the database right there. Okay, so the buffers checkpoints are fine. So I guess you actually will have every workload, right now checkpoints that we can file on disk. So you're not checkpointing at all, or very limited. I mean, it does define like, every five minutes or so as we would expect. So it was pointing quite heavily before. So by checkpointing, you can easily support whether Postgres kills writing or not. Right. What I said above, when we were looking at it, I didn't know what happened because your right activity hasn't subsided on its own, or maybe you pushed your instance a bit too far. And your right activity suffered, and you just dropped, right by checkpoints, I would guess that he just stopped. Right. So maybe you naturally decreased. So I want to look at the queries running in your database. And for that, we have QM. 

**Matt Yonkovit:** 
And I'll need to so we're still selected at 44. So that's good. 

**Sergey Kuzmichev:** 
Yes. Because we didn't get into the overview. Yeah. Oh, yes. Nice. So we even maintain the last, our overview, and we have those nice sparklines. And those sparklines never lie, and they show us a huge spike, they never lie. Yeah, they never do. You have a nasty, nasty spike in the load. Right? About maybe 25 minutes ago, right? So if we go to the top row here, the top row is kind of not this one, the top row? And yes, it does. It does have its own sparkline. And does have its own, like query counts and query times and the load what's more load is like Q and A way of saying load average. And yeah, you can click on the total. So if you want to see the global overview, that's what you do. And it does show us that the query load is great for some reason, and as we see most of the load, at least right now, on their system is read only. So something happened to your queries. And thankfully, you have a kind of skewed issue, where the query number one is the one I want to look at, because it's sparkline is really suspiciously close to the outline of the general layout of the system, right? So I would imagine that this particular query is causing us grief. So I actually don't see the bottom half of your screen. So if you can scroll down a bit for me. Okay. So what do we have here? Row sound 300. And town. That's not a lot. it's 40 milliseconds, but it runs really, really often, right? 133 EPS? Yeah, all righty, then see, are no large query about apparently, it's enough to boost a lot of load. And the query counts, the query time has actually changed. Right? So you are actually sending fewer rows. But the query time has increased. So the sparklines are changing there. Yeah, sure. The blog dotars Is there it is changing. So maybe schema change? Or maybe something else happened, but I don't know. So let us see examples, just so that I understand. What kind of queries are we talking about? Example? Sorry? Sorry, the examples? Yeah. Probably have a schema there for the table. But yeah, let's see tables. All right. So what do we have here? What was the query ago? I forgot how it ran. title equals one. Guess what? You're missing an index. I think.

**Matt Yonkovit:** 
I'm missing an index. That's right. And you know what, you weren't the first one to spot that. So we had that pop up here. So what do you think should we add to that index?

**Sergey Kuzmichev:** 
Yes, yes, we should, actually. For this particular column, I would actually recommend that you create a hash index because, yes, because titles are usually checked for equality. And like the text columns, especially longer text calls, right? They are rarely checked for something other than equality. So it's like, as gladiator greater or equals the metrics maybe by its writing, but definitely not by its name. So maybe you could do a ski comparison, 

**Matt Yonkovit:** 
Is there a benefit, though, to create both a hash and a B-Tree?

**Sergey Kuzmichev:** 
Not on the same table? Not on the same column? I wouldn't say so. Because, but for the rest of us there are some comparisons, like where the title is like that. Yeah, for those right, but maybe, like comparisons, if you are going to be using the title with some fuzzy search, like you are putting in not metrics, but 83. Or try just instead of the full name, you probably need an index suitable for the text for the full text search. three will not help you if you do like beyond that, but if you do like percent or something percent, you're not using an index anywhere. But if you do have the beginning, it does work well for the beginning, right? So it really depends on how you are accessing. But if your question was whether you want to have two indexes, I wouldn't necessarily recommend that. Right? Yeah, there's your opinion. Yeah. No, because the auto vacuum would have to scan both of them. Right. And we don't want that. 

**Matt Yonkovit:** 
Oh, back to the auto vacuum. 

**Sergey Kuzmichev:** 
Of course, keeping it on topic. So yeah, if you always have an equality on the always, like, you always nail the title. For this particular case, a hash index would be great, because it only works for equalities. If you are doing like some stuff, either try regular B trees will work to a certain extent, or they'll want the genes and whatnot for the full text search. Although for short, calling Magnus probably may or may not help. 

**Matt Yonkovit:** 
So I added the index. 

**Sergey Kuzmichev:** 
Cool.

**Matt Yonkovit:** 
See the drop? Yes. See the drop be the drop. There you go. Look at that. Sergey, you successfully navigated, you successfully did this, this test. So congratulations on finding the needle in the haystack. And doing it in an efficient 10 minute wait, see, this is how we roll. We never know what I'm going to throw out there. I have all these knobs and switches on these databases. So. So when we don't get a lot of questions, I start to throw some curveballs and maybe next time I'll create that terabyte size table and see if we can get a wrap around it. 

**Sergey Kuzmichev:** 
Yeah, again, gather up around Skid Row lock addl behind it, and see how it looks, see how the feature bench suffers or something? Yeah, that's, that's gonna be fun.

**Matt Yonkovit:** 
All right. Well, thank you, Sergey, for coming along. Hopefully everybody enjoyed this. This was informative. feel free to stop by the next one, bring your questions. It doesn't have to be about the topic, we will go into details on anything that's Postgres related. and I think that that's something that's important for all of us to realize that this is your time, not just our time, we're here to try and teach you something to educate you. If you did like this, go ahead and subscribe, hit the like button on YouTube or Twitch. That tells us that you want to see more stuff like this. And if you like me throwing some curveballs at some people, and like giving them some tough, tougher technical issues to dive into, let me know. And I'll try that next time. We should be back. We're off next week. Because in the US, it's Thanksgiving. So holidays here in the US. And then we're back the week after where we will be doing a PMM focused meetup with Michael Colburn. So for all of us here, thank you for showing up. Thank you for participating. We really enjoyed having you here and Sergey, thanks for the overview on vacuuming and auto vacuum. It was great. 

**Sergey Kuzmichev:** 
Thank you for inviting me, Matt. Yeah, thank you everybody for watching. All right, we're to maybe some more riddles here. Aha. 

**Matt Yonkovit:** 
All right. Bye. 

**Sergey Kuzmichev:** 
Yeah, goodbye.


![Percona MeetUp for PostgreSQL November 2021 - the Autovacuum](events/percona-meetup/postgres-november-cover-1920-2.jpg)

We will meet to discuss the autovacuum in PostgreSQL. We will highlight all things related to it, you will learn why we need the autovacuum at all, how to stop worrying about it and even love it! Percona Senior Support Engineer Sergey Kuzmichev also will reveal his tips and tricks on monitoring of autovacuum related issues. The host of the 1 hour meetup is Matt Yonkovit, the HOSS (Head of Open Source Strategy). Come to chat with experts live and ask your questions about PostgreSQL autovacuum! 

MeetUp for PostgreSQL

* Date: Wednesday Nov 17th, 2021 at 11:00am EST / 5:00pm CEST

* Live stream on [YouTube](https://www.youtube.com/watch?v=PtWQFkTt1Bo) and [Twitch](https://www.twitch.tv/perconalive)

* Add this event to  your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NDd1YjZtaHZzOGVsb2pwZ3RxZ25pb25jNXEgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)


This week the topic of our event is "PostgreSQL back to basics: Autovacuum" by Sergey Kuzmichev.He will highlight:

* Why do we need the autovacuum at all?

* How to learn to stop worrying and love the autovacuum

* Monitoring for related issues


Community MeetUp is a Live. Chat on Discord to ask questions and get answers from Experts right away! Your feedback is welcome to help us improve upcoming events.

![Percona MeetUp for PostgreSQL November 2021 - the Autovacuum](events/percona-meetup/postgres-november-cover-1920.jpg)

The MeetUp for PostgreSQL is recommended for everyone who is : 

* User of PostgreSQL.

* Student or want to learn PostgreSQL.

* Expert, Engineer, Developer of PostgreSQL.

* Thinking about working with databases and big data.

* Interested in PostgreSQL.

**Go ahead and come with your friends!**

Subscribe to our channels to get informed of all upcoming MeetUps.

Invite your friends to this MeetUp by sharing this page.