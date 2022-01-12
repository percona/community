---
title: "Percona MeetUp for PostgreSQL - Optimization of PostgreSQL instances - Dec 15th, 2021"
description: "We are interested what's been going on in Support, any challenging cases that we can share, RDS and EC2 live tuning with experts"
images:
  - events/percona-meetup/postgres-december-cover-1362.jpg
date: "2021-12-15"
draft: false
speakers:
  - jobin_augustine
tags: ['PostgreSQL', 'Meetup']
---
We have talked about what's been going on support side with Jobin Augustine, Senior Support Engineer at Percona, before starting to stump the expert with RDS and EC2 live tuning. This Community MeetUp for PostgreSQL is 1-hour live streaming hosted by Matt Yonkovit, The HOSS at Percona, to talk more about Optimization of PostgreSQL instances.

## Video

{{% youtube youtube_id="BZNw5HHXnW0" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Hello, everyone out there in internet land! How are you today? I welcome you to Percona's regular meetup, today we are meeting of course on Postgres. I am so happy to be here with everyone. Thank you to those of us who could join us today, we've actually got something a little extra special. I'm, we're testing out streaming live on LinkedIn as well. So we are not only on Twitch and YouTube but also on LinkedIn. So, I am happy to have people come on out. So, Rupesh, Hello, and welcome. So today, my guest is Jobin. How are you, Jobin? Oh, I can't hear joven Jobin. I can't hear you. So one of those awesome live stream things. You'd never know what's going to happen live, do you? So while Jobin is getting that worked out, let me kind of give you the rundown of what we have planned for today. We plan to talk to Jobin a little bit about what's been going on and he's been seen in the support community, see if there's anything interesting or new there. We're also going to be talking through some of the ways Oh, wow. Now I know that Jobin Yes, I can hear you. But I was listening to myself as well.

**Jobin Augustine:**  
Oh, okay, so I'll mute.

**Matt Yonkovit:**  
Okay, so. So just to give everyone, we're going to take some EC2 and RDS instances from install to configure. And so we have some workload running. So Jobin is going to help us out with that. So welcome. Jobin How are you doing today?

**Jobin Augustine:**  
Yeah, I'm good. I am doing good, sir. Today, my 50 centered and it's 10:10 pm at 10:30 pm. Here. Yeah.

**Matt Yonkovit:**  
Well, thank you for joining us late in the evening. So this is an after-hours version of the meetup for Jobin. So for those of you who are hanging out, and it's late, where you are we're glad to see you. So we are picking up a few folks, if anybody's out there in LinkedIn land, I would love to have your way up just to see if it's actually working. Because this is the first time I've tried to stream to LinkedIn as well as Twitch and YouTube. But without further ado, so Jobin, what's been going on always interested to hear if any interesting things have been popping up in the support side of things, any challenging cases that you can share, everybody loves to hear the more difficult things

**Jobin Augustine:**  
Yeah, in in support, we daily handled totally different cases ranging from wrong expectations still completely out of context problems, I say, especially those people who move from other database systems like Oracle or they carry certain expectations, and because they are familiar with certain things, and they are looking for the same thing across all databases, which may not be the exact thing here, which would be slightly different. And sometimes even migration might have been done with something slightly missing. So for example, the data type selections. So the Oracle may have specific data types in Postgres, the selection of data types is very crucial when it comes to performance. So for example, Oracle has numeric number data types. Postgres has different types of data types, or numbers, say a piece of four-byte integer or eight-byte integer, or variable-length integer. And many of the migration tools may deal with this in a generic way. And they may select a variable size that is tight because that is safest. We can store anything there. 

**Matt Yonkovit:**  
Yeah, and I think that's an interesting point is database design is kind of a lost art. Not many people think about it, especially with a lot of the migration tools. They just kind of thing let's dump and move it somewhere else.

**Jobin Augustine:**  
Yeah, yeah. In fact, that is the most crucial thing: the ultimate performance of a database will be designed by will be decided by the design, the right design. Based on these things the tuning can work only to a certain extent, that is. So this is damage control basically, the tuning.

**Matt Yonkovit:**  
Right? Yeah, yeah. Yeah. And I think that if you can start with a good design, you're way ahead of the game. Yeah. And so I've been doing some testing and some looking at the performance difference, when you choose different data types can be quite stark, it's very, very big. Yeah, it's huge. So, thanks for that Jobin. And one of the things that you might find, as we dig into the workload that we have ready for us here is some of the data types might not be optimal. So it might be something that we have to fix. I took a load from a database load from what we were running a few weeks ago at AWS reinvent. So I don't really know what state the scheme is in because we allow people to change data types to see what the impact is. So why don't we get right into this. So I have given Jobin access to a couple of boxes. And I'm going to go ahead, and I'll share my screen real quick. Just so everyone is aware, what we're going to be doing is we're going to be looking at two different boxes here. This one happens to be an EC2 box. And this is fresh as a daisy installation with the default configuration, and no changes. Okay, and so this is running a workload that I call the kitchen sink, which has everything potentially, that I could throw into it right now, which is it has some analytics queries, it's got some inserts, updates, deletes, it's got some, some locks, it's got a little bit of everything going on. In this one. The exact same workload is running on RDS, both of these are running Postgres 13. So these are set up out of the box without any changes. Now, one of the things to realize, if you are going to deploy by RDS, RDS does adjust the configuration for you. Right, so right off the bat, you're going to get a more optimal configuration for the hardware, based on RDS just because out of the box, they do some magic to say, Oh, you've got X amount of memory, we'll adjust these parameters by default. So that's where we are. And so Jobin, which one would you like to start with?

**Jobin Augustine:**  
Now, let's look at the RDS.

**Matt Yonkovit:**  
RDS one? Oh, right. So what's interesting is just to point out, out of the box, both instances are running. And again, this is all the exact same setup with the exact same code, the exact same structures, everything, the EC2 instances already performing at 1900 queries a second. And the RDS is at 1500. So you want it to go to the command line. So what I'm gonna do is I'm going to stop sharing my screen and allow you to share yours, if you'd like us to kind of follow along. So that way, I don't have to drive everything for you.

**Jobin Augustine:**  
Yeah. So, what we generally do, so let me explain that part. So when, when a customer approaches the default setup, we gather certain information about the environment, what are the parameters? And he did, they really modified some of those things. As you mentioned, some of the parameters are well-tuned for their environment, especially the memory-related parameters for RDS. But that is not correct for some other sets of parameters, for example, the disk-related parameters. The RDS has a Disk System, which is EBS volumes, which is more like SSDs. So we need to tell Postgres that we need to treat this disk, similar to SSDs, where the sequential access is almost the same as random access. So we need to tell Postgres, so those parameters are not modified. And the most completely off parameter in RDS instances, the number of connections,

**Matt Yonkovit:**  
Okay, so why is that?

**Jobin Augustine:**  
I don't have any clear reasoning behind why RDS gives such a completely offsetting by default,

**Matt Yonkovit:**  
So is it too high or too low?

**Jobin Augustine:**  
too high. to the same high, we can check that this environment will probably be running into 1000s. In a 32 CPU machine or 64 core machine, it will be sometimes even 5000, which anyway the Postgres won't be able to handle. And is not just not able to handle the Postgres performance degrades as the number of connection because there are some pre allocations in terms of semaphores, and things like that. And the locking mechanism complicates and the snapshot management is directly proportional to the number of connections. So, as we expose ourselves to a lot of connections, there could be a lot of idle connections sitting there. And the general thinking is that the idle, idle connections won't consume the resources. But that's not entirely true, the idle connection can cause a lot of contention in the system. So the very first thing, which we do for RDS instances is correct all these basic sets of parameters to something reasonable. Okay. Yeah. And the RDS things, it's a little complex to set in normal Postgres, we can set the parameters like ALTER SYSTEM, come SQL command interface interfaces there, but in RDS, we need to create a parameter group and change it.

**Matt Yonkovit:**  
Okay, so, do you want me to open up the parameter groups and say yes? Or do you want to look at the shell first?

**Jobin Augustine:**  
Yeah. So I can demonstrate how we generally analyze the environment.

**Matt Yonkovit:**  
Okay. Okay. There should be a green button in the middle. If you see

**Jobin Augustine:**  
okay. Yeah. Let me pull it to the side. Is it visible now?

**Matt Yonkovit:**  
Yeah, it's a black screen.

**Jobin Augustine:**  
Oh, I think I have a problem with sharing. Sorry about that. 

**Matt Yonkovit:**  
No problem.

**Jobin Augustine:**  
Because of this new Linux, it runs well, and yeah, it was working in Zoom. So I thought it would work everywhere. Huh. 

**Matt Yonkovit:**  
Okay. Well, well, while we're looking at that, if you want to play with that a bit. I mean, PMM. And just to take a look, you mentioned the number of connections. So the maximum number of concurrent connections right now in RDS is set to 1691. So 1600 connections.

**Jobin Augustine:**  
So what is the instance type you have?

**Matt Yonkovit:**  
This is a 2XL. Hmm, so eight cores? Yeah, 32 gigs of memory.

**Jobin Augustine:**  
Yeah, for eight cores. This many concurrent connection is way too high. Because in Postgres every connection is a separate process, the back background process, this is a number which the system may not be able to handle at all.

**Matt Yonkovit:**  
So do you think that they did something behind the scenes? Maybe though, could they have implemented some sort of pooling without telling us?

**Jobin Augustine:**  
Oh, no, no, this is at the policy level. Yeah, the pooling comes extra. Yeah, okay. So this is the one of the most important things which we should be modifying in the RDS instance. And generally, this will result in very good improvement in terms of the performance and the connection. Okay, yeah. And, and another parameter which we can see the planners estimate of the cost. For a non sequential prejudice. It's four currently.

**Matt Yonkovit:**  
So where's that? Oh, this one right here. So we're highlighting a little bit. Take a look.

**Jobin Augustine:**  
Yeah, this is the actual parameter name for random Pay Page costs. It's Four means the sequential access is four times costlier than random. Random access is four times costlier than sequential access.

**Matt Yonkovit:**  
If, if I'm going to create a new options group, yeah. The ones that I would want to address would be the concurrent connections and the planner estimates. Yeah,

**Jobin Augustine:**  
yeah. 

**Matt Yonkovit:**  
Okay. Okay. So did you end up? A kid trying to get your screen share to work there?

**Jobin Augustine:**  
It's not that easy, because I may have to reboot the machine.

**Matt Yonkovit:**  
Oh, no. All right. Well, that's the issue that you get with that, that live streaming, right. So okay. So let's go ahead, and I'm going to create a new parameter group for RDS here. So, you can see my fancy pants. Yes. Ah, okay, so I want Postgres 13. Right. Yeah. Yes. And so I'm not doing a cluster. So I could just name it whatever I want. Right? Yeah. Okay. All right. Jobin, your name will be forever linked to this parameter group.

Alright, so now you said now what am I looking for, from a connection perspective?

**Jobin Augustine:**  
Max connections? The first one.

**Matt Yonkovit:**  
Okay. So Max connections. So here is the least ID, here's the formula for them to to get that. So let's go ahead and edit that parameter. And what do you suggest we set it to four,

**Jobin Augustine:**  
sigma b, then maximum four times the number of CPUs or maybe eight times? Not more than that.

**Matt Yonkovit:**  
Okay, just to make it easy. Let's go ahead and we'll just do ad sets. 10 times. Seems reasonable. Alright. So alright, so well, we'll go ahead and we'll adjust that. What else do we need to find?

**Jobin Augustine:**  
Random page course. Does Random Page cost? All right. Yeah. Yeah, you can see this way. It's one,

**Matt Yonkovit:**  
one. Alright. Okay. And what else do you want to look at?

**Jobin Augustine:**  
The checkpoint-related things? Checkpoint timeout.

**Matt Yonkovit:**  
Checkpoint timeout. So what does checkpoint timeout do for those who are watching? 

**Jobin Augustine:**  
Yeah, so the Postgres periodically does a checkpoint where it will synchronize or flush out all the dirty buffers to this, and synchronize all the data files. And that information will be added into the control file saying that up to this point, the data database is protected from a crash, okay, the recovery the next, if at all, our recovery is required. The next recovery can start from this point onwaRDS, up to this point, everything everything is synchronized. Yeah. Okay.

**Matt Yonkovit:**  
And so what would you want to set that to because

**Jobin Augustine:**  
in a production system, we generally give half an hour. So this is specified in seconds. So we can also specify 1800 1800 Yeah, yeah. So half an hour. What's the default on that? It's five, five minutes. 300. Okay. Okay. And it's weird that they don't put the defaults in there. Yeah. So, there is a criteria for selection, say, if there are frequent checkpoints, and if crashes are very frequent, then the recovery time will be less. Okay? But in a Postgres, like, database, crashes are something very rare. Very, very rare, right. Okay. And the system should be more tuned towaRDS the performance rather than under crash recovery.

**Matt Yonkovit:**  
So in this case, what we're doing is we're the same, give us more performance, give us more throughput. And then if it crashes, we'll let it take a little longer. Yes, yes. Okay. All right. So what else should we be looking at?

**Jobin Augustine:**  
The max_wal_size? Okay,  yes.

**Matt Yonkovit:**  
It is 1048.

**Jobin Augustine:**  
Two GB. So we should increase that to something bigger in a production system generally. How much? Well, we should expect to jump right in an hour. Maybe? Say 40 GB. 

**Matt Yonkovit:**  
40. Wow. Yeah. Okay, well, I'm not gonna get 40 Exactly. I'm just I'll to go 40. Yeah. 40,000 Right. Right. Yeah. Yeah. Yeah. Okay. So, let's go ahead and we'll change that now. How would we check to see how much wall-size we're going to use in our estimate? 

**Jobin Augustine:**  
So, we can collect that information using the current value lesson number we can collect. There is a clear-cut analysis possible. 

**Matt Yonkovit:**  
So, can we get that from within

**Jobin Augustine:**  
That takes time because say in every hour, especially in the peak hours, so, before the peak hours, what was the lesson number, and after what is the lesson number? 

**Matt Yonkovit:**  
So, she had to just kind of calculate that by hand. Yeah.

**Jobin Augustine:**  
We can find out how much value is generated,

**Matt Yonkovit:**  
because this has been running for a day now. So there was a workload in the past if there's something you wanted to go back and check. So, we actually have the capability to take a look deep in the past if we needed to. Okay, all right. So, back to the RDS console, what else should you be looking at changing?

**Jobin Augustine:**  
I think this submission to get started

**Matt Yonkovit:**  
What about like shared buffers?

**Jobin Augustine:**  
Obvious does it correctly almost correctly 140 is what we generally recommend to get started and these calculate that part pretty much decent,

**Matt Yonkovit:**  
Щkay, worker memory.

**Jobin Augustine:**  
Yeah, so, the work mem in the production system, so, that generally depends upon the number of connections. So, a thumb rule is starting with the 32 MB size okay. And see this parameter has a side effect this is the memory allocated per operation say that if there is a sort operation or join operation in a query per operation per statement per session, so, if there are a lot of complex queries running at a time, so, every operation will be allocating this much of memory. So, if there is a lot of concurrencies that this can consume a lot of memory altogether

**Matt Yonkovit:**  
Okay. Okay. So, so,

**Jobin Augustine:**  
We recommend adjusting this value to the work mem at lesser scope level. Similarly, if there is a query that requests a lot of complex sort operations, we can set it at the transaction level or a session-level. So, only that query can allocate more memory. So, when we set it at a global level, what happens is it will be applicable for all the sessions.

**Matt Yonkovit:**  
Okay. So, if that's gonna happen, what would you recommend? Yeah, just a 32 gig or 32 Max right now just leave it

Anything with auto vacuum we should be working are focused on

**Jobin Augustine:**  
so auto vacuum defaults are very gentle as I am allowed a maximum of three workers. Okay, and

**Matt Yonkovit:**  
the default is autovacuum on shouldn't be on. Okay, because I thought that the parameter wasn't set in default. Postgres, so maybe that's just maybe I'm wrong. I'm okay. But that's it, huh? So alright. And so for that. So now we've got our parameter groups with Jobin. So now I will go over to RDS. I would like to find my Postgres RDS. I probably should stop the workload, what do you think? Should I stop the workload? Before we rebounce it? That would probably be helpful. So one second, let me go ahead and I'm going to shut that down from running so to. Oh, hold it off. So now if I go back in

**Matt Yonkovit:**  
To PMM real quick, I should start to see all those connections die off. So let me go back to my Postgres dashboard. And this guy should start to see the CPU. That's EC2 instance, let's go RDS. Yep, it has started to die off already see the number of queries per second drop off. And guessing in a couple of seconds, the CPU will die off as well. But the number of queries has definitely dropped off. Alright. So now I should be able to go in here. And I go into configuration and modify this guy. Right. It's taking its own sweet time. By the way, I don't know if anybody noticed, but AWS was having some issues today. So I did see that there was some downtime there. So we're going to change that to Jobin. We will continue and we want to apply this immediately. Alright. Says it's available. But wonder, were any of those parameters? Restart required?

**Jobin Augustine:**  
Yes, Max questions definitely require a restart.

**Matt Yonkovit:**  
Okay. So I'm wondering if it just didn't show me because I didn't refresh. Oh, there we go. It's changing now. There we go. So we'll give that a second. And we will watch that off-screen. So now, let's go into the EC2 instance. While we're waiting for that one. Now, obviously, some of the parameters that were set for RDS out of the box aren't going to be set on a default installation of Postgres. So if we go and we look, within PMM, take a look at this summary. Again, let's go into the EC2 instance that I've got, we can look at the same settings. This one has a concurrent connection set to 200. I might have changed that. that might have been me changing that. I did. But shared buffers are 128 Meg's so yeah, we're, we're Meg's so there are definitely differences.

**Jobin Augustine:**  
Yeah, yeah. So the max connection is more realistic here. The other one was 1000. The default is 100. Yeah, but the shared memory things should be adjusted to have 1/4 of the available memory on the system. Okay.

**Matt Yonkovit:**  
Okay. So let me go ahead. And this one, we can use an old-fashioned shell to change it in the configuration file. So yeah, yeah.

**Jobin Augustine:**  
You can connect and say ALTER SYSTEM. That's it.

**Matt Yonkovit:**  
Oh, yeah. Well, yeah, we can do it that way. But then, I'm the one who has to type it all. So that's gonna

**Jobin Augustine:**  
be fun. No problem. I'll let you know.

**Matt Yonkovit:**  
Alright. Yes, Jobin stupid being nice to me. So let's see. So go ahead and I'm gonna log in real quick. And then I'll show my screen. Okay, so here we are in Matt's magic shell window in the UK. Wonderful red. And I'm gonna go ahead and I'm gonna zoom in here, just so people can see a little easier. All right. Why do you want to do

**Jobin Augustine:**  
How much is available memory in the system? 32 gigs. 32 gigs. So we shall allocate 04 sorry, 08GB for shared buffers.

**Matt Yonkovit:**  
Okay, so we can know. What's the command

**Jobin Augustine:**  
ALTER SYSTEM set the underscore, just type press tab it will fill Yeah. Equal oh well it Oh, okay, there we go. In single choRDS 08GB Yeah. Semicolon, enter. Yeah.

**Matt Yonkovit:**  
What now? Okay.

**Jobin Augustine:**  
So we are going to make the same connection as RDS or we can.

**Matt Yonkovit:**  
So ALTER SYSTEM. set max

**Jobin Augustine:**  
underscore connections. Yeah. Equal to put you at research, right? Yeah. Is everything across? Yeah, it's not enough to single quotes. Yeah, it's a to take. Yeah, and the checkpoints ALTER SYSTEM. Set checkpoint timeout and checkpoint, underscore, checkpoint, checkpoint, underscore, timeout equals 1800 1800. Okay, and the max wall size

**Matt Yonkovit:**  
up so if I type correctly. Anyone who has to live stream and type it's always a pain, right? Alright, and what did we set that to before?

**Jobin Augustine:**  
Yeah, 40 GB okay.

**Matt Yonkovit:**  
What are we going to look at?

**Jobin Augustine:**  
And Shall we check the? Okay, this is an EC2 instance with the EBS volume, right? Yes. Okay. So this also we can modify for the random page ghost. So you can check the first show randomly. Yeah, semicolon is for? Yeah, we can modify this alter system Yeah, yeah. So let's give a restart to get all this. changes into? Yeah. All right. systemctl, restart PostgreSQL

**Matt Yonkovit:**  
Yeah. Okay. I was gonna use service, but

**Jobin Augustine:**  
Yeah. Restart. Starts Postgresql. At

**Matt Yonkovit:**  
What was that? Well, we're gonna have to do it. Yeah, if

**Jobin Augustine:**  
there are multiple instances, we can clearly specify with the at. Right there. It says the system still can have sub-services. Yeah.

**Matt Yonkovit:**  
Yeah. This is just the one. So

**Jobin Augustine:**  
Yeah. So you can connect again and check the parameter changes?

**Matt Yonkovit:**  
And we should be able to do Yep. And then. Of course, yeah. Yeah. Okay. So we went ahead and made him check those. So those are the basic ones that you would recommend we do. Now. Let me go ahead. And before I kick off the benchmark, again, this probably would have failed. Let's see. So this one is the EC2 instance. So let's see if I got all my Python stuff running, I do, but several of them died. So that's cool. Let me go ahead and kill it. And I'm going to go ahead and start that up again. So we can get some interesting workload going there. And then let me go back to EC2 and refresh or the RDS and let me refresh. So interestingly enough, the RDS instance is still showing modification. So how hard to tell what's going on there. So just, yeah, an FYI. So it's still being modified. Yeah, we can't go back and restart the workload on that guy. But let's go ahead and let's take a look at what has happened. If we refresh, we should see the setting changes in PMM now. And so yep, there are 80 connections. We didn't Change the work size, which we did in the RDS size, but okay, so we made some minor changes there. Let's go ahead and let's go back to my, my favorite dashboard. And let's see what we get here. So before we were running around 1.9 1000 queries a second, or Yeah, yeah. Or 1900 queries per second. It looks like right now we're running around 2100. So we did get a little bit more. So we'll need some time to verify that that actually did bounce up. Yeah. That'll be interesting to see, especially over time, some of the wall changes there would only work after a heavy right load is when you'd see the difference, right?

**Jobin Augustine:**  
Yeah. And as the cache pumps up, there could be some changes as well.

**Matt Yonkovit:**  
Yes, that is true. Because this was since we did bounce, all the cache would get cleared. Yeah, except the file system cache. Yeah. And our RDS box is still chugging away.

**Jobin Augustine:**  
that's one major pain point in RDS, not just bounds. One of the biggest challenges that customers face with the RDS upgrades? Because Ah, okay. Yeah. So, for example, if we want to upgrade from Postgres 12 to 13. Yeah, even if it is a multi-terabyte Postgres database, if the DB has shell access, the DBA can just run PG upgrade, which actually, does the hard link have hard links between the data directories. So it's instantaneous, even a multi terabyte database can be upgraded in seconds, or hardly one minute because it's just manipulating the hard links. But we don't have a similar option when we deal with the RDS because we don't have shell access. The only option is to click the button and wait for it.

**Matt Yonkovit:**  
Right. I mean, we're already up and running. And we're seeing workloads back on the EC2 instance right now. Whereas on the RDS instance, we're still waiting for the modification. Which is, like I said, taking its sweet time. But yeah, so that's, that's, that's working there. So, that wasn't a lot of parameters to change.

**Jobin Augustine:**  
These are just very basic things because we know that the RDS uses EBS volume, which I would just say is kind of like an SSD. So, we know some of the information in advance. So, these are the basic things that we are doing with that advanced information, but we may have to do a lot more tuning once we start understanding the type of work workload. So, just this for example, just for example, if we know that we are going to deal with the oil AP system okay. We should expect heavy queries, very complex queries, but a number of sessions will be very less the connections may be very less, but the queries those connections will be firing will be heavy. So, if we allocate more resources per session say go for more parallelism parallel execution parallel queries, what are things we can give to that session, we will give more work ma'am. So, we shift the resources from other places to the very small set of connections which is doing a lot of queries a lot of complex queries, but when if we know that we are going to deal with the OLTP system, we do the reverse, what is important for us is more concurrency. So even I tend to switch off parallel execution really, yeah, because when we have parallel execution, few sessions will be consuming a lot of resources. In terms of memory, suppose you have a 32 core machine A few of the sessions are taking set four parallelism, so that means four worker threads per query. So that alone will consume a lot of resources. But at the same time, other sessions will be starving for resources. So the CPU or memory. So when it comes to the OLTP system, the preference will be for more concurrency that could be a larger number of sessions. And we need to make sure that the concurrency is handled properly, rather than individual query performance or its execution.

**Matt Yonkovit:**  
Okay, yeah, and I mean, I think that's where it's interesting. So that was a little bit of a thing. I saw a blog on D zone, where it's like, MySQL is faster than Postgres the other day. And it's funny because for this one particular workload is really a super unscientific test for somebody hit a page load refresh, it's like, look, it's faster. But it's, it's testing, number one, a generic application out of the box, with the default configuration, basically tests the default configuration for a single, like like, like, like workload that is probably really unrealistic, which is a horrible way to test in and of itself. But there are so many parameters and adjustments that you can make that are very specific to that workload. Now, the workload that I'm using in this test happens to do everything. It's very rare that you have a database that tries to do everything. Right. But it's interesting to see under those circumstances when it is kind of like that, everything in the kitchen sink, workload is there certain things that break or certain things that cause issues? Because each one of the parameters that are out there could really adjust some of the throughputs that you're seeing based on that workload. And so if I have a read-only workload, that's very different than a write heavy workload, a mixed workload is going to be very different than the analytics workload. And so it's hard to make a generic statement that this is better than this. When that workload could change in a lot of applications. Let's be honest, the workload changes potentially from hour to hour.

**Jobin Augustine:**  
Yeah, yeah. Yeah. And see, just comparing the performance numbers of databases won't give us any conclusion. That's the same. For example, I know MySQL itself. The old storage engine gives different performance characteristics than the InnoDB, right? The new one, yeah. And say, Forget about all the databases, even a flat file may give a better performance than all these database engines.

**Matt Yonkovit:**  
Well, it's well, so it's funny, we did a server build challenge, like, several years ago. And when I was running professional services, we had all the consultants and I said, here's $1,000, build the fastest machine, you can benchmark MySQL on it. And we'll see who gets the prize, which happened to be hats with propellers on the top. And when somebody puts in the debit, they have no storage engine, which basically it does, it just writes to debit. All right. And I like how fast it is, it's so fast. it? I mean, like, yeah, it was the fastest charger, but they cheated. So they lost, and they didn't get that. But there are ways that you can make things like that up here. Faster. Right. And I think that that's one of the interesting challenges. And here's the thing, right, depending on that workload change will potentially dictate quite a bit on what you see in your benchmarks. Yeah,

**Jobin Augustine:**  
Absolutely. I remember you, you have done a benchmark where the full page rights were switched off you, I think, I hope you remember right. Okay. So, the full page rights is a safety mechanism. But there is a big penalty for that. After the checkpoint, any block which is getting modified will be fully written into the Val files. So that results in a huge IO. So right, the performance penalty for full-page writes is really heavy, but never do we recommend turning it off. Except if there is a fault-tolerant file system like he said, FS or something like that. Don't worry, we won't say Okay. To not. So there are other areas like synchronous commit, okay! Where we can tweak a little bit And there are there specific parameters available in Postgres to tweak many of those areas to get really appealing numbers from the database.

**Matt Yonkovit:**  
Yeah. And so this is where it's difficult to sometimes use those generic benchmarks and say, like hey the look at how fast this one is, versus this other one, that those tend to give you false results. Yeah. Now, our benchmark, or RDS, just finished configuring and updating configuration 15 minutes later. So I just started the kitchen sink workload again. And so it is running now, it just hasn't had enough time to do anything. But I can say that. So far, it looks like on the EC2 instance, we have adjusted those simple configuration changes, right? which, which weren't really, I mean, that there weren't that many, there were just a few, you can see here, this is the throughput for those, you can definitely see a pretty noticeable change in that throughput for the exact same workload. Right. So here you're in the 1900s, and now you're in the 2300s. so that's it, it's nothing to sneeze at, right? It's, it's, it's something that it's a pretty reasonable now, this is fairly untuned. So still in terms of like queries and things like that, but that is an interesting result. So when you install things out of the box, even a little bit of tuning can add some substantial benefit in a lot of cases. Yeah, yeah. Let's take a look at that RDS. So obviously here we are down here. And it does look like there was a substantial change in the RDS site as well. almost over a 25% increase in the throughput, right, for this particular workload. Yes. And let's just double-check something here. Let me go ahead. And I also,

Let's do it! Let's see. So, these are the number of useful functions that were completed per second. The web workload was about 13 seconds, and then this is a chat workload of 24. So yeah, so those are actually improving as well. So, so anyway, so so those, that small amount of changes did make a potentially sizable impact or a noticeable impact anywhere from 20 to 25, to even 30%. In some cases, just by the handful, and no, I mean, really, what did we change six things?

**Jobin Augustine:**  
Yeah. So the, one of the assumptions was that when we take a RDS instance, everything is pre-tuned and well configured. That's not the case. That's, that's a point which we need to take away. There are still there are areas where we can further fine-tune and get more performance.

**Matt Yonkovit:**  
Yeah, obviously, I mean, here, you know that, again, minor tuning, without touching cores, we're talking configuration a 20 to 30% Jump, depending on how that work plays out over the next couple of hours. But it was definitely a noticeable change. So, thank you, Jobin, for coming. I don't see any questions if anybody has any questions, comments, things that they want to jump in on now's the time, to throw one our way. We do appreciate you hanging out. Jobin next time we'll get your screen share to work. So that way we can have you kind of drive as opposed to me trying to drive based on what you're saying. which is always a difficult position for both of us because you're like, No, no, do this, no do that. But I think it worked out pretty well. if you are interested in more content like this, go ahead and subscribe, like leave us a comment, tell us maybe something that we could do better next time, we would appreciate the feedback. But Jobin and this has been great. And next time, we'll try and throw a few more curves your way. I could play dungeon master back here where I'll make some adjustments while you're trying to tune the workload. And then you'll be like, what happened? Oh, my God, and we'll break things. maybe I'll crash an instance or something to make you fix it.

**Jobin Augustine:**  
Perfect.

**Matt Yonkovit:**  
 All right. All right. Thank you everybody for hanging out and we will see you next time. We're off for a few weeks for Christmas. And then on New Year's, so the holiday, so whatever holidays that you guys are, you folks are all celebrating out there in the YouTube, Twitter, Twitch verse. Appreciate you coming back at the New Year and we'll see you then.

**Jobin Augustine:**  
See you, everyone. Thank you for joining!

**********************************************************

![Percona MeetUp for PostgreSQL - Optimization of PostgreSQL instances - Dec 15th, 2021](events/percona-meetup/postgres-december-cover-1920.jpg)

Come to chat and stump the expert with your questions about Postgres during the Percona Community meetup for PostgreSQL. This is a 1-hour live streaming meetup hosted by Matt Yonkovit, the Head of Open Source Strategy. This time, we will talk more about Optimization of PostgreSQL instances with Jobin Augustine, Senior Support Engineer at Percona.  

Join us for an hour MeetUp for **PostgreSQL**

* Date: Wednesday Dec 15th, 2021 at 12:00 pm EST (6:00 pm CET or 10:30 pm IST)
* Live Chat: on [Discord](http://per.co.na/discord)
* Live stream on [YouTube](https://www.youtube.com/watch?v=BZNw5HHXnW0) and [Twitch](https://www.twitch.tv/perconalive)
* Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NnJzbWd1ZGJqOGhudTZlOWJtcGJ2NWNsdmQgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

## Topic

Optimization of PostgreSQL instance by Jobin Augustine

* RDS and EC2 live tuning with experts
* Tips and tricks from Support Team - optimizing PG instance with PMM 
* Q&A: Stump the Expert!

Community MeetUp is a Live. Chat on Discord to ask questions and get answers from Experts right away! Your feedback is welcome to help us improve upcoming events.

The MeetUp for PostgreSQL is recommended for everyone who is : 
* User of PostgreSQL.
* Student or want to learn PostgreSQL.
* Expert, Engineer, Developer of PostgreSQL.
* Thinking about working with databases and big data.
* Interested in PostgreSQL.
