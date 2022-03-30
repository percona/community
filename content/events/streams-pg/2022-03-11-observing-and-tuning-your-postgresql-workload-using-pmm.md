---
title: "Observing & Tuning Your PostgreSQL Workload Using PMM - Community PostgreSQL Live Stream & Chat - March 11th"
description: "This Live stream is all about tuning your PostgreSQL workload with Percona Monitoring and Management (PMM). This is a part of Percona bi-weekly Live Stream series dedicated to Postgres-related topics and deep talk about technology secrets and tricks."
images:
  - events/streams-pg/pg-stream-week-2-march11-upd.jpg
date: "2022-03-11"
draft: false
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---

Organize and access easily to your database data by observing and tuning your PostgreSQL workload using PMM. Our experts Matt Yonkovit and Charly Batista present use cases in a bi-weekly live stream about Postgres-related topics.

## Video Part 01

{{% youtube youtube_id="H2uNDbQ8lCk" %}}{{% /youtube %}}

## Video Part 02

{{% youtube youtube_id="SxQyC2RdBCg" %}}{{% /youtube %}}

## Transcript Part 01
**Matt Yonkovit:**  
Here we go! We're live! Hello everyone! Welcome to a specially exciting Friday live stream. Hopefully everyone is getting to the weekend. I am here today with our esteemed Charly, Charly, our tech lead for Postgres. How're you doing this week?

**Charly Batista:**  
Hey, man, I'm doing great. I'm doing great. Thanks. Yeah.

**Matt Yonkovit:**  
So Charly's going to be joining me every two weeks. Okay, so we're actually going to be going live every two weeks. With a specific Postgres topic. We've actually got 20 weeks mapped out. So 20 weeks of Postgres awesomeness. And we're going to be building upon all of the Postgres stuff that we've been doing in previous streams. So if you follow along, you come along for the journey, you're going to find some really interesting things, there's going to be lots of different topics, we hope that you will swing by every Friday, every other Friday, every other Friday at 2pm. Eastern. And we're going to also be doing this with MySQL starting April 1, with Marcos Albe, who's going to be joining us to go through the exact same things, but for MySQL, so if you are interested in one or the other, so every week, there will be something streaming from Percona. And we'll be able to cover whatever interesting topics of the week come up. And you'll be able to end the week on a good note with me, Charly or Marcos. So that should be exciting, right? I'm excited. I am. I'm personally excited about you.

**Charly Batista:**  
Yeah! that's totally, that's looks really, really awesome. And the good thing is, even though we have sort of an agenda, and so this is an open talk, right? So we can talk about what the audience what the people there and they want to discuss, like, for example, we are being asked if we're going to talk about PostGIS, right, well, maybe not today, because we haven't prepared but like, those are things that we were really interested to hear from what they want to talk to discuss.

**Matt Yonkovit:**  
Absolutely, yeah. And so we want to make this open for folks. And right now, we generally get more people who watch after the stream than we do during but that's okay. So if you do have questions after the stream, you can ping us offline, you can drop me a line. You can see my socials listed on the screen. Actually, I'm going to add yours, Charly, in future streams, because since you're going to be here for 20 weeks. Yeah, we should list where people can reach you as well.

**Charly Batista:**  
Definitely, I'm kinda unsocial on this perspective. So, but yeah, I know, I do have. I have the Twitter and Facebook things. But like, I really don't news that often I need to learn like, I'm an old person. I'm an older guy. 

**Matt Yonkovit:**  
I'm older than you. So you can't claim to be the old man on the street.

**Charly Batista:**  
It's the perspective right? So, there are aged people, and there are old people. Right?

**Matt Yonkovit:**  
I am aged. Is that what you're saying? 

**Charly Batista:**  
I didn't mean to say that. You're no but like, I better be aged. The old it's I think it's like just like whiskey or wine. You're not old, you're aged, so you get better and better and better.

**Matt Yonkovit:**  
Just take yourself deeper.

**Charly Batista:**  
Look, it looks how it looks like I'm actually myself now who the more they strangle bid, the more hook the gap. So I think I got to stop. Yeah,

**Matt Yonkovit:**  
Yeah, that's probably a good thing. Right. So to slow down a little bit on that. But we are not here just to talk about the weekend and talk about Charly telling me that I'm old. We are here to talk about tuning your Postgres instances and figuring out what sort of configuration variables you could, you should change based on what sort of workload is running. And I think that that is an exciting topic that many people have questions on. And we're hoping that you out there and userland are watching and you are eager to see how to do some tuning. 

**Charly Batista:**  
Yep. Yeah, definitely. Let's start here, right, shall we?

**Matt Yonkovit:**  
He just jumped right into, he just, yeah. This. So we have three workloads today that we're going to look at. So Charly created a system that's that has a decidedly Charly workload, which means that it's a box that's falling over and going to kind of fall over dead because it's old and decrepit. aged.

**Charly Batista:**  
That’s totally sad. That's yeah, that's a bad thing.

**Matt Yonkovit:**  
And I've got two separate workloads that I'm going to throw at Charly as well.

**Charly Batista:**  
Yeah. All right. So yeah, before I go, if your work a little bit, I have no idea haven't seen. That's, that's a good thing. So because of, it's usually how we do at Percona, right? So we have customers, they, they have a problem in their workload, open a ticket, and then sometimes we need just to jump in to help them without no background. So that's your workload. Well, my workload, even though I have some background here, and then not much in on my workload, only thing I'm doing here, it's a load test, I'm using pgbench. Really, really, really simple stuff, I want to show you the common in the field. But there is nothing special here. So as we can see, from this result, and get around 17 1800, sometimes 2000 transactions per second, right? So not impressive. And the customer, the user wants to know why our database is behaving slowly, slowly. This is not a super harder, I should say. But if we take a look, let's take a look on the specs of my heart are here. We have eight CPUs, we have 32 gigabytes, RAM memory, and we have 512 gigabytes disk. So it's a decent box, let's say that could do a lot better than 1500 transactions per second, right? So and then my customer might is, is asking why it's so slow, it's behaving so slow. So we need to go here and start investigating what problems we might have. So we have many, many different approaches. The one that we are going to use here is not the only one that we can use. And sometimes you can also find a different approach that works better for you. So this is fine, right? But one thing that we need to keep in mind is, whatever approach we use, we need to be methodic. Right, we need to use a method, and go to that method. So and this is what we're trying to go here. So but when I do start to investigate, usually there are three things are sometimes four they go first. So first things is CPU usage. So I usually take a look on my CPU on the CPU to see how it's being used. Well, the CPU is under 75% utilization here. There are some extra information I'm not going to look at now. But like just CPU wise, not a bad. It's a 75% utilization here, right? So if I go for my disk utilization, or let's, let's see memory, because I read here, so memories are bad. So we see, we here use a memory, like we use it memories, like just this small portion in yellow here, we still have a lot of free memory that we can use. If you take a look on the swap, we almost didn't use any swap, we see some sub activities, here and there, which is usually not good. We don't want to see those activities. But like, it doesn't seem to be the problem. Especially because, well, the server is behaving badly for a long time. Not only those those those period of times here. It's getting some IO but it's a database, right? It should read and write so it's writing, like reading more than writing on my database here. So and the disk load here, it's I we have some lazy load here but like the right load, it shouldn't be that bad. So what would you say, Matt? From what we see here? What do you do have a hint for what is the problem what where we should go just for that basic information here. Let me just say

**Matt Yonkovit:**  
A lot of memory you probably have things Yeah, and you are seeing some disk IO there.

**Charly Batista:**  
Yeah, we do have some disk IO, you see here. 

**Matt Yonkovit:**  
No, we're probably looking at some memory settings. and so that's where you're probably not, don't have enough being put into memory reading too much from disk.

**Charly Batista:**  
Okay, so if we go for memory settings on Postgres, we're talking about which do you do have on top of your mind? Which configuration? We go from memory setting? If you don't have it's fine. Like even, I sometimes?

**Matt Yonkovit:**  
Yeah, like you're talking like shared buffers, you're talking? A couple of others.

**Charly Batista:**  
Okay? Yeah, let's, let's take a look at the shared buffers, 

**Matt Yonkovit:**  
Charly asks me questions and tries to quiz me during live streams, just so everyone's aware. Like, like, everyone else is just like let me show you what to do. And I'm off like getting in answering questions behind the scenes. And then Charly starts throwing me like questions. And I'm like, what? I need to pay attention.

**Charly Batista:**  
Yeah, please. we need to keep it interactive. otherwise, people going to sleep out there. We don't want people sleeping. Right? So at least someone should be under pressure

**Matt Yonkovit:**  
Okay, so now I'm gonna go invite other people so they can be under pressure, not me.

**Charly Batista:**  
While you Oh, yeah, we are free to ask for help. Why not?

**Matt Yonkovit:**  
So who wants to come help me out? Live stream while I'm here trying to do this. But anyways, go on, Charly.

**Charly Batista:**  
Oh, yeah. You said shared buffers, right. So let's, let's take a look on the shared buffers. We have here eight gigabytes for shared buffer, which is not bad, right, like recommendations for Postgres is not used to match. I have 32 gigabytes of RAM for the OS. So if we have eight gigabytes, shared buffers, let's say the OS uses two gigabytes, so we are 1514 gigabytes for the kernel cache, right? No as cache, that's supposedly, to help us with IO. Right? So I would say this is value is not bad, like, for this box should should be fine. What else could you would you take a look? Well, if you want you to look at anything here, so I just change it from one dashboard. This dashboard is OS perspective, and this is the postgres dashboard. So just to make sure we're on the same page, so this is a postgres dashboard.

**Matt Yonkovit:**  
so one of the got a lot of connections, right? So each of the nations is going to consume quite a bit of memory.

**Charly Batista:**  
Okay, yeah, that's a good point, we got a lot of connections. We didn't take a look of how many connections you have. Right. So and yeah, as you mentioned, here, we are over, I would say 500 connections. Right. That's, that's, that's quite a lot for this box. Right. So and it may say something. So we did find one problem, we have too many connections for this box.

**Matt Yonkovit:**  
Right? Absolutely. So there should be some connection pooling or something there to limit those.

**Charly Batista:**  
Indeed, indeed, and we're going to try with the connection pooling later. Before we do any change, we got to adjust switch from direct connections to the connection pool to see if we get any improvement, right. Just like without changing any configuration. Just going to stop my load and point to a connection pool because I have here a connection I have a PG bouncer there, but just minimize configuration, listening on the port 6532. So we're gonna jump and see if we change anything. But before we do that, let's get the investigation. Okay, yeah, we do have two main connections. For this instance. We have like over 500 connections here. And if we take a look here on the activity itself, it doesn't look to have too many things doing because something is really putting my server on its knees right. And let's go back to the last

**Matt Yonkovit:**  
Yeah, yeah, it looks like you're doing quite a bit of checkpointing as well. So I'm cheating and looking at graphs in the background. You've got some pretty big spikes that are happening on a regular basis. Look at that. Big checkpoint stats but

**Charly Batista:**  
it does, yeah, it does. And some from time to time off also we just flush a lot of buffers like it's expected because of checkpoints right. So now you can ask whatever information for us to take a look here it's fine. We are investigating right so sometimes I myself just miss someone point on order. So order a couple of eyes. They definitely kind of out. Okay, we have Two things, too many connections, and we have a lot of checkpoints. Checkpoints are bad. Or they are not bad proceed. But like when we there too often they're bad because they bring problem with IO, right? And okay, one thing that I want to show you here, remember that I said there are some hidden information on the CPU dashboards. You see this red stuff? Yeah, this is the I O wage. And this is pretty bad. So what is the IO weigh thing on this graph? What is it telling me here? Can you explain to us like in one short sentence,

**Matt Yonkovit:**  
it's basically you are waiting for IO to complete before you can use the CPU.

**Charly Batista:**  
That's perfect. So the IO way is 

**Matt Yonkovit:**  
It was like it wasn't perfect, but you couldn't think of a good way to tell me it wasn't. And then you were kind of I'm pretty sure that Charly was trying to thought.

**Charly Batista:**  
I wouldn't have asked you that if I didn't have confidence on your own. And that's why I'm asking you do have confidence. You know. And that's the theme. So we're the CPU is wasting a lot of time waiting for IO. That's the main reason why our CPU is underutilization here. I will say, if you take a look, this green stuff here is the time that the userspace Postgres is using CPU. So it's almost nothing might even the kernel, the system's system time here is doing almost nothing. So and this huge amount of disk utilized, not utilization, but waiting time is killing our server. But this is the major problem that we have here. We have a huge IO bound system in this case, yeah, right. And this is killing our database performance. Well, we need to find a way to deal with those things. There are parameters on both screens that can help us and also their actions that we can do from the kernel as perspective, well, at some point, we cannot scale, and we need to either split the load between two different servers, or get better hardware for disk. It might we might get to that point. But we don't know yet. So for what the only thing that we know, at this moment, is that we're putting too much pressure on our IO subsystem. Right? Okay. Before we change anything, remember that I told you, I would change to use. Just show you this is the command I'm using here, right? I got to change just the port here. Instead, use the connection directly to the database. I got to use PG bouncer. So my PG bouncer has the configuration to only send a max of 100 connections to the database.

**Matt Yonkovit:**  
So you've already set up PG bouncer.

**Charly Batista:**  
It's yeah, I read have one. Yeah, it's there. So I can show you like in a second I feel. And well, if we take a look, looks like we got some improvement. Doesn't seem to be all it depends. 

**Matt Yonkovit:**  
It's significant. It's more consistent. Yeah, it is. It is.

**Charly Batista:**  
Exactly. So.

**Matt Yonkovit:**  
But you can see it in PMM with the different graphs, right?

**Charly Batista:**  
Mm-hmm. Okay, it's updating here. But even then, we still put a lot of pressure, right? It's still we still see here like from OS perspective, let's take a look on the connection. So the connection should drop. Yeah, it dropped here. See, this is when we stopped the load. And here is where we got the old back with PG bouncer. So we have less than half of the number is connected right. So the max number of connections sometimes we're going to have more here because the connection dies and it stays open for some period of time waiting for for for the kernel to release them. So, that's expected to see more on the max number of connections we put here, so that's fine.

**Matt Yonkovit:**  
When you start to look like for instance, even like your tuple activity there, you could see a pretty significant increase. Because you're not fighting for resources, right?

**Charly Batista:**  
That's true. So that's true. And if Yeah, that's that's a really good point. So even though we still have some limitations here, right, we still have the physical limitation, but now we are we don't have so many.

**Matt Yonkovit:**  
He was gonna say so many connections, but it looks like we have an internet hiccup. So I will just continue on for him for a second. Hopefully, it is not me. So, while we try to get Charly back here. Basically, what we're seeing is the number of connections where can the connection pooler? Okay, you're back? You disappeared for a second. And now you're back.

**Charly Batista:**  
Oh, so sorry. 

**Matt Yonkovit:**  
Oh, no, he's frozen again. Oh, the negatives of having internet on a Friday afternoon, right? Of trying to do the live stream. But no, so it is interesting because of the architecture for connections and threads within Postgres, there is a lot of connection and potential overhead. But tools like PG, bouncer, PG pool, are absolutely required to get the optimal performance on a lot of these. So we are seeing what's going on. Oh, and look Charly is back. Hello, Charly, welcome back to the live stream here.

**Charly Batista:**  
I just got the glitch on my connection here.

**Matt Yonkovit:**  
Oh, sorry. I was just saying a little bit about how Postgres is threading model and the connections make it. So if you do have a lot of users who are going to be accessing things concurrently, there, is it important to have either connection pooling or something out there to help manage those? Now, David Gonzalo asked, is there a recommended sizing relation between the maximum numbers of sessions in PG bouncer pool versus the CPUs in the database node.

**Charly Batista:**  
The max number of connections on from we have two different things of max number of connections on PG bouncer, we have the max number of connections from the front end. That is the connection that PG bouncer receive is from the Postgres clients. And we have the max number of connections that PG bouncers opens on the database. Which one is he referring to? 

**Matt Yonkovit:**  
Not 100% Sure, because the question is what the question is, right? So just when you're talking about setting PG bouncer, is there some magic formula for saying if you've got eight CPUs, you shouldn't have more than 80 connections set up in the connection in PG bouncer or something like that is there like some formula that we should be using?

**Charly Batista:**  
The thing is PG bouncer is single threaded. It use a synchronous IO to balance. So what it does is when it receives a correction, it puts in the pool, and then waits for the kernel to notify when something is back, just like normal synchronous io we have like a pool, or are io running on Linux? Right? So it all use Oh, it's only has one trash. So, it doesn't matter if you have 100 CPUs and your PG bouncer. If you just install your PG bouncer in use as it is it only uses one CPU because it's single-threaded. There are some tricks we can do to make PG bouncer to use multiple CPUs. But those are some tricks we need to do by default, like my here, my PG bouncer here. I didn't do anything, just using one. So, but because it does use a synchronous IO, it can handle really 1000s of connections. So because it doesn't get busy all the time with with the processing from the IO

**Matt Yonkovit:**  
But from the pool perspective is it something that you want to say like you've limited here to 200 I think connections? Is there, is there a limit to the number of connections you should allow to Postgres based on the size of the box?

**Charly Batista:**  
It is. Ah, so I did limit here to 200. Because my intention was to show the difference of what we get, if we have like, just around half of the number of connections from the resource perspective, ideally, we should not have more than usually like six trades per CPU concurrently. Right. So in my case here, I would say, ideally, I would put 64 Max connections as I have eight CPU cores. So I read put a lot of pressions here, because they're going to have an around eight process, so in average, but it's fine. So, we will then have two main context switching and so it's fine. But when we are moving for a number that's higher than that value, all the bowsprit is beside. So we can do the box start struggling with resources? 

**Matt Yonkovit:**  
Okay. Fair enough. We got a comment from Augustine, who said, our mics were a little hot or cold, depending on which of the US was talking. Hopefully, that clears it up a little bit. I made some adjustments if the sound went a little wonky. Oh, and Augustine says, much better, much better for both. So that's, that is good. So I'm glad someone out there is, is watching and letting us know. Yeah. If we're going to do this every week, we want to save these settings. So we don't have to go through that. But okay, so Charly, where we were looking at the connections, we dropped the connections, we saw that we were getting a lot more throughput based on that. 

**Charly Batista:**  
So take us from still have a problem here.

**Matt Yonkovit:**  
Yeah, we are still seeing too much IO.

**Charly Batista:**  
 Exactly. And if we keep the load. At some point, it will just get to the point it was before, right? Because when we added the PG bouncer, we're saving CPU ressource from the Postgres side. So now Postgres has more CPU to play to work. But the IO is still the same, right? So didn't do much. 

**Matt Yonkovit:**  
Not expect the connection pool to make a big difference on the IO unless you were saying I'm writing the IO with a lot of connections, right? So I mean, it's it is possible, if you reduce the number of connections that were running concurrently, you could also reduce the IO, just because you'd have less things hitting disk, but that would probably reduce your overall throughput to achieve that.

**Charly Batista:**  
That's true, that's true. Okay, yeah, from here, so well, I am really curious to see who is using that much of IO. So there are some tools on Linux there, they really help. So remember, PMM gave us a really good direction, where we go, right. And there are some really nice tools on Linux that we can use to find the problem. One nice thing that I really like on PMM is that we can extend PMM to use those tools. This is not the top for today. So we probably should get one-off, we schedule another one just to go for through PMM to see how we can extend them all just kind of stuff, right? So I'm not going to spend much well, because

**Matt Yonkovit:**  
That means generally you just sign up for two new streams, right? So you sign up for one in PostGIS, and now you've signed up one for extending PMM for additional Postgres metrics. So you heard it here, folks, we are now up to 22 weeks. So, if there's anybody who wants another topic or two, let's see if we can get to 25 weeks of Postgres content by the end of this stream.

**Charly Batista:**  
The good thing is that for that PMM one I can outsource. 

**Matt Yonkovit:**  
no, you sign up, you signed up. It's you. It's you. I already got you on a motorcycle graphics that we're using.

**Charly Batista:**  
Alright, that sounds interesting. So really good. Let's move back here before I say something more.

**Matt Yonkovit:**  
Yes, those who are watching like, like I saw Augustine was watching you can thank me that I didn't let Charly outsource this to you. So just be mindful of that I just saved you or maybe a couple of other people who might have gotten looped in here.

**Charly Batista:**  
Yeah, okay, I got to work my way later on. Okay, let's move on here. So I gotta check my IO top here, because I want to see who is destroying my disk. Well, on my IO top here, I always see this check pointer guys see, this guy here and this background, right? They're always here. And sometimes they write like 100 megabytes per second. Sometimes they write 320. They go zero. So those guys are always here, right? The check pointer in the background, right? Indeed. So well, we got another hinge. So we have problems about IO. And we have at least two guys here from Postgres that are really destroying my IO subsystem here. Okay, what can we do with those guys? So before we move on, we need to understand what those did this? Let's work for this checkpoint or here. Because you mentioned before, well, let's go back to the graph. We mentioned before, that from time to time, we do have some checkpoints activity, right. So we had a huge spike. Well, they're out of my graph. 

**Matt Yonkovit:**  
if you go back and look at the last hour, you'll start to see him show up. It's fine.

**Charly Batista:**  
I can simulate them, or we can even force them to appear here. Let's try to force them right. So as we know what checkpoint is. Oops, I just stopped with my

**Matt Yonkovit:**  
Yeah, well, that would definitely have an impact on those. Yeah, stopping.

**Charly Batista:**  
Okay. Oh, I shouldn't stop. So. Let me go here to. Okay. Can you hear me, it looks like my connection. Just. I still hear you. Okay, can you also see me right, because 

**Matt Yonkovit:**  
I can see you, although your screen went really tiny. So?

**Charly Batista:**  
Yeah, no, no, it also happened to me. I think this is the database server. It's not responding. That's why I thought my connection was lost.

**Matt Yonkovit:**  
So Charly is streaming, but his database connections dropped. Okay. Yeah. Internet, Gremlins, everyone. Always on a Friday afternoon.

**Charly Batista:**  
Okay. Okay, looks like I'm back. So I want to be Postgres.

**Matt Yonkovit:**  
By the way, where are these servers? Are these in AWS?

**Charly Batista:**  
AWS? Yeah, these are in AWS. And this is another thing that we should talk later because when we start using too much IO, and if you're not paying for that I was using AWS, they just reduce our IO right. So sometimes it happens.

**Matt Yonkovit:**  
Yeah, I mean, and I think depending on what class a box there's also other things right? Because you can get bursts. Yeah, you burstable CPU works great until you run out of your burstable allotment, and then all of a sudden, it dogs is that there's there's all kinds of gotchas in little videos

**Charly Batista:**  
Exactly. Yeah. So I got a fresh checkpoint here. So expect now my database we have like huge impact we should have. This is when I dropped the connections, but now the queries per second should really go down. Because see, from time to time, we have zero transactions per second. Because well, what I'm doing, I'm forcing the database checkpoint to flush all its cache to the disk, right? 

**Matt Yonkovit:**  
That's why you see the duration of like, look at the duration of transactions taking you to see a spike. So everything's having to wait.

**Charly Batista:**  
Exactly. So don't do it in production unless you have a really good reason. Right. So what we want to do here is we want to show what is the impact of each full checkpoint on the database side. It's kind of a stop the world and wait for me to write everything that I need to write to the disk. Is it still ongoing? So it looks like we have a lot of data, to write to the disk. So how does this work on Postgres, Postgres needs to write dirty data to the disk, but every, every time not only post all the database, every time that we do a transaction, let's say we do an update. So when we send a commit, that update is first the data source updated in memory, right. And if it's been updated in memory, it needs to be flushed to the disk. Well, there are many approaches that different databases, they use different approach. One thing that we can do is we can go to the data tables, like the data files, and right now, that data, well, that's expensive, because usually, the data files there, the data is just distributed randomly, especially for Postgres, right. So it's not saved in this sequentially, like one after another, let's say create the table user, and I have the ID, that is my primary key inside the table user. That doesn't mean that in the disk, the data file will be organized by the ID, it's not. When we're inserting Postgres tries to put one after another. But when we start updating things, there's going to shift in here and there. So it's inefficient to write every time. Another problem is if we start writing to the data tables from memory, if something happens to the box, in the middle of the process, we'll be left with inconsistent data on the data files, right. So it's not only inefficient, it's dangerous as well. So because it's inefficient and dangerous, most of the databases, at least the ones that I know, they use a modern approach, they save this data somewhere else. They usually have a either a circle a file, or they have a file that they pre-created that is sequential. So they will say that the first in their file, some database, use undo log files or database like post misuse wal files that the right ahead logs. So if something happens, why I'm writing the data to that files, and the data, let's say the database crashes, or the worst crashes or whatever something happens with the database. When we restart the database, the database can check back to the old files. If there is a transaction in the middle, it just rolls back the transaction. And the data files are still consistent later on the database transfer everything from the wal files to the data files, right. So those are when we're doing checkpoints. But you can tell but well, a crash can still happen during the process. So we still can have a crash now during the checkpoint time. Right? So then it didn't do anything for the safety. Well, if a crash happens, while the database is copying data for the wildfires, to the data files, when the database restarts, it will see that the data fires is inconsistent. But then it can find where was on the wildfires, because the wildfires are saved or kept safe. They've been written already. And it can redo that transaction and recover the data files. So this is a trade-off. If we wait for the database to do not flush or to do not just forgot checkpoint to do not checkpoint too often and keep a lot of data.

When the database crashes, and it recovers, it might need to read a lot of files to get the data of the database consistent to where it crashed before. So the recovery time when do they if the database crashes, and we need to restart the database is going to be longer and fun if we have more checkpoints. So, for the other hand, if we have checkpoints too often, we can see a problem that we're seeing here so we can put the disk really under pressure. So it can really create the problem that we were seeing here, that we have a lot, a lot of this activity, then we, we start struggling with the number of transactions that we can put to the database. So we need to find a way to balance both settings. And this is the first thing that we should go. So there are some settings. The first one is we can increase the wal size. And by default, if I'm not mistaken, there are two default there are two configurations for the wal size, there is the minimum wal size and the max wal size. The minimum wal size, it says if we flush your checkpoint, not flush, if to a checkpoint like I'm doing now. So it will write everything right. If you clean up all the wal files, we're going to start fresh from here. So then it will start creating the new files to start filling those files. So these these, these smaller the minimum wal size. So when the database starts fresh from the wal files, what is the size of the wal file? This is how we define is defined by the mean wal size file.

**Matt Yonkovit:**  
And then it grows from there. Because I think the default does 80 or 100. I think it's 80. Yeah,

**Charly Batista:**  
Yeah, it's pretty small. I think it's 80. Yeah, I think it's around 100 megabytes. Yeah, I think around that I don't recall top of my mind, we can double-check. And the max is one gigabyte. So for workloads, like the one that we had, here, those are too small, right? So I want to have larger, so I can afford a longer time during the recovery process, but my client can afford that. So then he told me, I want to improve performance. And we can afford, like we have applications. So if decide this, this database crashes, and they can do some order high availability operations and get things back. Okay. So then the first thing that we can do, and we should do is start increasing the wal size, right are going to increase, both are going to increase the main wal size and the max. And then you can ask me, okay, what is the best value? Well, what is the best value?

**Matt Yonkovit:**  
You said they ask you?

**Charly Batista:**  
Yeah, that's a good question. That's a good question. I had no idea. Because, well, I'm just looking at the database now. But we can check. So we can see how much we write recycle on the database, right? So we can check the log lsn, that was written wait for five or 10 minutes, and then check the logs LSN, and us just do the math, to see how much data where we are writing to the database on own batch, we choose the wal size that we want, like, I want 30 minutes of wal, I want one hour I can afford? I don't know, half a day so there's not really a strict definition for what is the best. So the best is, what is the best for your workload for your case. So maybe you cannot afford your database to go offline for five minutes. You have no other strategy, this is the only database that you have. And if something happens, you need to recover from the crash in Max five minutes. So your wal file cannot be larger than it takes for five minutes worth of data. Right?

**Matt Yonkovit:**  
With that. I mean, that assumes a single box. If you have failover set up, would you risk a larger wal file size and longer recovery? If the database does crash?

**Charly Batista:**  
You can but then you need to pay close attention to your application. Because if your application is lagging, and you want to switch over from your private application, you still need to wait for your application to go up to the speed right to recover from the lag. Right. So you need to be careful with the high availability, especially because most of the recommended setups on Postgres are asynchronous, there are synchronous setups there, but like it's not the subject of this talk. So let's assume you have an asynchronous replication. That's the most common one, then you need to really take in consideration the risk, if your application is lagging a lot behind me, the time that takes for your application to get up to this week, and you promote is larger than your primary to just read from the old files. 

**Matt Yonkovit:**  
Most people will have that automatic failover, though, right. So if your replication is lagging, you could failover and your primary could recover quicker than your replication can catch it. Yeah,

**Charly Batista:**  
That's true. That's true. That's why we really need to close eyes on those if you really, really want higher, high availability with levels of high level of SLA, the replication is something that really needs to keep eyes on it, it shouldn't lag too much. Because the switch over is really fast. Usually, people think the longer that takes on the process is the switch over, actually switch over can doing in seconds, or milliseconds depending on the latency of your network and configuration. So it's really fast. What takes long, is if your replicas is lagging behind of the primary, that can take quite a long time. And then your SLA, oh, five nines is just going down to the road.

**Matt Yonkovit:**  
So I don't know if you were gonna check the lsn numbers. But I do notice that they will go back down a little. I do notice that your transaction time, like as you were talking, it just keeps on going up into the right. Which is, which is good, if that's a metric of how much users or money you're making, but not so good. If it's the amount of time that transactions are taking. That tends to be bad when it goes up.

**Charly Batista:**  
Yeah, that's indeed, that's indeed. So well, up to this point, there's not much we can do. Right? So we did a we were forced into the checkpoint. So I gotta wait for the checkpoint, I'm not going to change to check the lsn because well, we need to wait at least one or five minutes. And as we're taking too long. So what are you going to do is I'm going to use one gigabytes, because I did the math before. We can show it later, probably next session, or if we have time by the end of the session, but it just, it's a simple select. So just select the current LSN. So wait a minute

**Matt Yonkovit:**  
What about synchronous commits or wal sync method as other ways to potentially reduce IO?

**Charly Batista:**  
It's a trade-off?

**Matt Yonkovit:**  
Well, I mean, everything's a trade-off. Right? From a performance perspective.

**Charly Batista:**  
Exactly. Exactly. It's a trade-off. Again, it depends on your workload, can you afford that, like a lot of applications, for example, they need to use serializable transactions instead of read committed because they cannot afford any ghost reads or anything, right. And they should afford to lose some performance. To get a consistent view of the data. This is the same for the write, so for the commits. And there is even more strict that we can go like, for example, all the replication, we can use synchronous replication doesn't need to be a synchronous replication, right. And even on the synchronous replication sides, you can have the synchronous replication when you just wait for the replica to acknowledge that received the data and didn't apply it or you can wait for the replica to receive the data apply, and then go back to you and then you send back to the application, the result if it's success or failure, right. So, all of those can drastically reduce the stress that you put on your IO subsystem can improve the high availability level, the level of high availability that we can give to our customer, but definitely they have caught the performance can drop significantly. Like for example for the replication things. So we now need to wait at least the round trip to the network round trip. So if we have the primary in New York and the replica in Dubai, for example, the natural round trip can can can cost quite a lot, right. But if they both are on the same data center using fiber and really expensive switches and all these kinds of things. So sometimes the network round trip is cheaper term they are able that we have here. So all those things play in consideration, right. So, there is no really a formula to tell what is right or not. But all of them we add everything every time that we add something or for improve its scalability or to improve safety or wherever we'll probably add in on the performance problem. So you drop on the performance. Right?

**Matt Yonkovit:**  
It's a trade-off. So you get better availability or better recoverability at the expense of performance.

**Charly Batista:**  
Exactly.

**Matt Yonkovit:**  
So, you're waiting

**Charly Batista:**  
Yeah. See the checkpoint? He's taking 99%?

**Matt Yonkovit:**  
Yeah. Well, so I haven't IO bound workload as well, if you want to look at it.

**Charly Batista:**  
Yeah, let's go. 

**Matt Yonkovit:**  
Well, your checkpoint on your workload is over, they're doing its thing. If you take a look at the 130 box, on the PMM instance, that I sent there's an IP 130 Because I didn't name them nicely, like Charly did, is I'm just a lazy turd. When it comes to naming things correctly. I believe that everything should just be an IP address name. I am not a fan of anything else. I just want like hardcore IP, six values and just remember them off the top my head, right.

**Charly Batista:**  
Okay, I just need to I just need to learn how to use my browser.

**Matt Yonkovit:**  
Yes. Looks like yes, browsing is hard. citizen or hot internet is hard.

**Charly Batista:**  
When you take too long using the internet. I don't think if it's zoom or something, but it doesn't. Okay. I got it back. Oh, cool. F 11. Oh, I need to remember my username and password, right. That's something that I don't. Okay, let's try to Okay, I got it.

**Matt Yonkovit:**  
Yeah, 12345 is not a secure password.

**Charly Batista:**  
Well, there are many stars on those, I can tell you for sure. 12345. At least up to nine.

**Matt Yonkovit:**  
The same as my luggage. 

**Charly Batista:**  
My password is encrypted is the other way around is 98765431.

**Matt Yonkovit:**  
Ah, so we do have a request to do some tuning on Read-Only workloads. Which Yeah, we can actually do that we've got I've got some some some workload, we can change over. The ones we're looking at right now are kind of a mix. So there are two workloads that I've got for Charly here. One is a kind of a 5050 mix for web workload. And this one is an if you look at the 130 bucks, this one is a much heavier right workload. And this one's going to be more of almost like an archival with some analytics. if you will. Why did you break it? Choose the database? Choose database? Choose database.

**Charly Batista:**  
Oh, I thought they just moved selected service. 

**Matt Yonkovit:**  
Yeah, I don't know. It's, it's kind of weird.

**Charly Batista:**  
But let me just put here to the last 15 minutes. Okay.

**Matt Yonkovit:**  
But know that that's a good one. So Charly are you're up to 375 live streams now.

**Charly Batista:**  
cool.

**Matt Yonkovit:**  
One a day. Would it everybody show up if we did one a day? Like or two a day or maybe we just have Charly-like work lives on. On Twitch on YouTube. That could be fun.

**Charly Batista:**  
Oh, we are on Twitch in Okay, that's my first one.

**Matt Yonkovit:**  
So your first Twitch experience you even

**Charly Batista:**  
Yeah, I'm the beauty in there. Okay, cool.

**Matt Yonkovit:**  
Yes, yes. 

**Charly Batista:**  
Well, I see that you have no shared buffers here. All right. Well, yeah, I can. Yeah, I can tell that your configuration is it's not cool. I was about to say a model word, but like it's not.

**Matt Yonkovit:**  
Oh, no, you're gonna call me aged again. Oh, Yeah. Oh, like, I don't know what I'm doing. 

**Charly Batista:**  
Yeah, it was because of this 128 megabytes for the 90s, you know?

**Matt Yonkovit:**  
So here's the thing. This was a box that was set up for you to configure in tune, but then you set up your own box last time, so I never went back and did any changes. So this is pretty much default out of the box.

**Charly Batista:**  
Yeah, I can tell. Okay, yeah, well, we have a lot of things to do. Right, we need to change the memory, we need to change kernel settings, the things that we did last time. Okay. Your checkpoint is quite cool.

**Matt Yonkovit:**  
I don't know. What checkpoint cool. I mean, I guess it's kind of cool. Because it is very uniform.

**Charly Batista:**  
Yeah, it's pretty. It's pretty.

**Matt Yonkovit:**  
It's pretty it is. Yeah. Yeah.

**Charly Batista:**  
See? And it's like, yeah. Well, we definitely see, you really have is like standards here. Do you mean patterns, I think we see patterns every see from year to year as well, here to order. So those are the checkpoints. If you see here, everything goes through the transaction increase increases, then checkpoint and goals and checkpoints. And if you look around your graphs, you're gonna see the patterns, they're all around your checkpoints. Right. So and definitely when we increase the memory, the shared buffers, we can improve that, because we're going to have buffer. So we can keep more data before moving them. Okay, where do you want to start? So I already told you, the shared buffer is not good, the checkpoints are not good. 

**Matt Yonkovit:**  
Do you want to recycle it and change those? Do you want to go in and change them? You can? Yeah, this is your box to play with?

**Charly Batista:**  
Okay, so I suppose again, I have access, right?

**Matt Yonkovit:**  
I did give you access last time. So, I did ask you prior to this. Look, oh yeah, your checkpoint failed. PG bench port. My workload is not PG bench. By the way, everyone. Although it does, I can make some wild and wooly changes if we want. If we want to make the workload really random. But right now it's running a uniform workload of so many writers and so many reporters, we can make changes. And if someone would like to come on and play Dungeons and Dragons Postgres with me sometime, I'll be the Dungeon Master. And I'll be changing variables behind the scenes, and then you have to figure out what I changed. It should be awesome.

**Charly Batista:**  
I have sudo, okay, now I can restart the database.

**Matt Yonkovit:**  
No! don't restart the database. It took me forever to get it started now

**Charly Batista:**  
All right. So okay, I am checking your, your graphs here. I see from the database that you need to at least start with the basic settings, right, this is the base that we do when installing any samples. So base configuration for memory, or shared buffers, base configuration for wal. And those are the base settings. Right? So this is pretty common, actually, that we have, especially when we have like a setup that is done by developer. So we should not expect the developer to go deep into configuration because all this is not there for you. Right? Or if not that there are not developers out there that understand a lot of the database things I have some peers on somebody that they are developers, and they do understand a lot about database. But this is not their field. So this is DBA responsibility. Usually, when we get a database like these usually set up for a developer or it was a bad environment. And then for whatever reason it was promoted as production, so we get really out-of-the-box installation. So everything is default. The first things we check are those configurations, the most basic settings configure tuning, we shouldn't even call the tuning but anyways, those are the first thing that we should check right. Take a look at the memory configuration. So shared buffers, how the caches been used, if the box has or not. Configuration for swap how the CPU, Governor, all those basic things to make at least, the database to perform up to the box, let's put on this way not to deal with the keyboard configuration that we have. Right. So. But then we need to know, like, for example, how much memory we have on this database we can use like just I did here and see that Matt doesn't have swap at all, which is bad. And we've discussed why it's bad last time who should have

**Matt Yonkovit:**  
It's the defaults when you spin up an instance? It's default?

**Charly Batista:**  
Yeah. Yeah. So don't stay on defaults then argued there. So. And I would say a better approach, or to take a look is to use the tools that we have, like for example, the PMM. So I can here on my node, I can have a node overview, and should have been opened here. Let me choose. its upgrade. Alright, have this one. Yep. It's not the right one. So and I want actually, what I want to see is on Node overview on the summary, okay. So we can get most of the information that we need from here, right? So for example, how much memory we have. So I can see that we have 32 gigabytes memory on this box. So I can see what is the swap message that you want? That's good thing, even though we don't have swap available? I can see the configuration folder as kernel like the dirt caches and things here. We can also see, take a look on the IO that you should have somewhere around here. What is the IO scheduler, so you don't have rage. So that's common, especially on AWS. Because they do not expose this information from from the VM level. You have transparent, huge pages enable here. This is not good, either. Okay, let's start from here. You have 32 gigabytes of memory. Right? So usually, for this recommendation, so out, I'd say like, if you go up to 12 gigabytes of memory in this box, it's not bad. Remember, I do not know your workload. Can you do it right now? Well, I'm looking for the problems that workload is causing, not your workload. Oh, right. So this is different. I'm looking at the problems he calls it, I see that you have how many connections, so not that many. So usually less than 100. Last 100 connections, there's not bad, but I have no idea what those connections are doing. So I can see that you what kind of activities, the read activities here. So not as bad and your transactions are taking quite long. So, I can have some hints of your about your workload, but I don't really know your workload in I only know what your workload is calls into the database, right? And this is this is the premise.

So usually, because Postgres doesn't do direct IO, and it relies a lot on the kernel to do buffer IO, we usually don't give too much memory for Postgres. There are exceptions. And for example, if you really have a really read intensive workload, it might be a good idea to give more memory to Postgres, then to the cache, because possibly scan can cache better information based on the tables and the data that you're using, though as always caches blocks, right? So kernel doesn't care. Those are just blocks that it got from the file system. And it's caching. So the cache on the database is more optimized. It's more, it's a specialist question. Let's put on this way, because it knows the data, it's caching. So there are some circumstances where it's better to have more memory for the database to OS cash, but they may try it off the workloads, or put a 60 75% of their workers I've seen, it's better to keep more memory to the OS cache down to the database cache. And that's why I usually start with smaller value, like, for example, eight gigabytes, 12 gigabytes, when you have like a box less than 100 100, gigabytes memory, right? So it's not formal. Like we have all the data is like MySQL, they usually recommend you're giving 75- 80% of the memory available memory to the database, right? It's not like this on Postgres, you can give like, up to 40%, if you don't have a lot of memory on the cache, but as the amount of memory on the box increases, 40% can be a lot like if you have 100 gigabytes memory on this box, that will be 40 gigabytes memory. It's a lot. It's sometimes it's most of the time it's better to have both cash for the Kernel cache than to the database. Anyway, too much talk, let's start changing. So I need to know the configuration user you're using? And you both, I guess that's it, etc. 

**Matt Yonkovit:**  
Yeah, it's under Postgres. 13. Main. Yeah. And I think it's going to be pg_ident.conf

**Charly Batista:**  
Actually, this is using usually is using this one. Okay, there you go. But we can, we can check later on Postgres. Just because I'm too lazy. Now. I gotta go here. So see, this is where we have your data directory, file, so we don't grab all those. Listen address? Well, your workload so far, you haven't complained about the number of connections. So we're going to keep the 100.

**Matt Yonkovit:**  
That's because I limited the number of connections, I could add more. But yeah, I knew I had a limit of 100. So I didn't go over. And you aren't your pool or bouncer, you are my you're my client.

**Charly Batista:**  
So I want to keep 100. All right. Alright, so let's go for the shared buffers, okay. I got to start very conservative, let's start with six gigabytes, right? There is no magic. There's just because I want you to give it I start with six gigabytes. Remember, I have to restart the database. This is one thing that you need to keep in mind. So now it's fine. Like our, my customer didn't say that I couldn't, I could not restart the database that well. So I'm taking it for granted that I can restart the database without problems, right. So if we need to increase, you can increase. But if you're working on production, be careful too, because you need to restart, like the database. So I got a small for now, four. megabytes for work_mem should be fine. And let's do just this one, let's let's just books. Only one, change the shutter buffers and see how that can impact in your load. Right? So I'm not going to change anything else, only the shared buffers. And we'll see how impactful this is a very good approach when we're working with tuning and optimization do not change too many parameters at the same time. Because if something goes well, you have no idea which parameter causes the improvement. If something goes really bad, you also have no idea what parameter get our database in bad performance, right? So every time that we going for 30 or something, change one parameter, test it out, see how it works, how it behaves, then we're going to understand what the parameters does. So I should suppose, have you ever used? You did use it here? So I'm restarting your database your as my customer, you're fine with that Matt? Okay, thank you. Shall I ask for a written approval? Yes. Okay. Well, I restarted.

**Matt Yonkovit:**  
Did it restart?

**Charly Batista:**  
Yeah, I got a check now. It says it's alive and I can connect to the database. 

**Matt Yonkovit:**  
Yeah, that's weird though, because the app didn't recycle.

**Charly Batista:**  
See? That's a problem with developers. Sometimes they take things for granted, you may need to restart your application as well. Right?

**Matt Yonkovit:**  
Maybe, let's see. It should have

**Charly Batista:**  
I know that my client doesn't have a connection pooling so that may be a problem when he restarting database.

**Matt Yonkovit:**  
I don't know. Did it actually restart or did it do like a just an act to return?

**Charly Batista:**  
No, no, it's restarted. Well, it's, I can do a stop. Let me stop here. Right?

**Matt Yonkovit:**  
Postgres still has workload on that box. 

**Charly Batista:**  
So it stopped. Now it stopped.

**Matt Yonkovit:**  
All right, hold on. Do it top real quick. Cuz I'm still seeing tons of Postgres. Just just just look at the processes real quick. Yeah, so we're Yeah, so it didn't start okay.

**Charly Batista:**  
Yeah, that's true. System D.

**Matt Yonkovit:**  
By the way, this is the box that you set up last time

**Charly Batista:**  
We created swap and we change a lot of things last time, do you remember?

**Matt Yonkovit:**  
Oh, maybe the other one is then maybe 111 is

**Charly Batista:**  
Okay, let's give it some time. Do you want me to do something and tell people never do that?

**Matt Yonkovit:**  
No. 

**Charly Batista:**  
Oh, because i can see you have a lot of movie JSON user connections here. Okay, let's spin theme things up. Right. So people that are watching never do that, especially in production. Really? Never ever do I'm going about to do here. That's said.

**Matt Yonkovit:**  
Anyway, it stopped now. It's done.

**Charly Batista:**  
Yeah. Whoa, almost. Okay, I'm not going to run. I just keep it here for posterity. We never know. Okay, yeah. You'll have some processes running. Yeah, Postgres is still running.

**Matt Yonkovit:**  
Well, that's, oh, no, here it is.

**Charly Batista:**  
Yeah, so I got to just send a secure signal. So this is fine. This one is fine to send a CQ signal to Postgres and the other process, because it doesn't forcefully kill them. Just ask them can you please stop? Sometimes they replied, No, we don't want to stop. And usually because probably is doing some OS activity. See this guy here? See the D is in to the reputable estate. It's doing IO. And probably everybody's waiting for this guy to finish his IO. And then it stopped. 

**Matt Yonkovit:**  
this one was heavily IO bouncer. So are you saying that the reason that it's not stopping is because it's waiting for the checkpoints to clear to stop?

**Charly Batista:**  
Yeah. But I wonder what happens if I forcefully kill them. Remember that we told Postgres is able to recover, right? Are we able to back up our words here? Okay, this one, this one is fine. This one is for the PMM. So, I forcefully killed Postgres, right? So now, Postgres is in an inconsistent estate, because it was still doing some IO, whereas when they stopped the database, it still has a, especially if you have a really IO bound workload. So even when we stopped the database, there are a lot of things in memory that the database needs to flush, the kernel needs to flush. So there's a lot of activity that the database needs to do. That's another thing that you need to take into consideration when you have a lot of memory and you give a lot of memory to the database. Sorry, they start up in the shutdown process, they might take longer because they still need to flush or that all that are IO and they need to finish up some a lot of operations that they're doing background, right. And at this point, the database is an inconsistent state because well, I just killed if q dash nine.

**Matt Yonkovit:**  
Shame on you.

**Charly Batista:**  
Now my fault, I asked my customer, he said yes. 

**Matt Yonkovit:**  
No, I never said kill. I said you could stop it.

**Charly Batista:**  
I did stop them. So it says Postgres, it says it's active at this exit. Okay. Let's try to connect. It's not really running. Anymore. Now we have a problem. Postgres didn't really start. So what do we do now? I hope you have logs on Postgres. Right. Yeah, I gotta check the configuration. Okay, yeah, we do have log, and it's the inside of the data dir folder lock. Okay. And the data G I saw something here it is. Yeah, this one. So we should go for this one. And we should have a log folder. Inside of this folder. We should have logs and which days today?

**Matt Yonkovit:**  
The 11th. Okay, last one there should be it right. 

**Charly Batista:**  
Yeah, let's take a look. All this is the shutdown one. Is not the one we're looking for. It should be this one. Wow. That's interesting. See the timestamp? 

**Matt Yonkovit:**  
Yeah, those are from earlier today. 

**Charly Batista:**  
Yeah. It didn't log they attempt to start the database. 

**Matt Yonkovit:**  
Okay, so systemctl might not be working right? That's possible. Yep. Or it might not be called Postgres SQL Server. It could be something else. 

**Charly Batista:**  
That could be

**Matt Yonkovit:**  
I think in this box, I thought I saw you monkeying around with PG up there PG start a PG start script. Did I? I thought so.

**Charly Batista:**  
Okay, let's let's do Oh, yeah, that's indeed

**Matt Yonkovit:**  
Yeah, because you were you were playing around with this before when we were doing some work on the previous stream, and if I recall correctly, on this particular box

**Charly Batista:**  
okay, let's see why. Okay, this is the one

**Matt Yonkovit:**  
Yeah, you're using PG Start. Prior PG start, stop.

**Charly Batista:**  
Okay, yep. Okay, now we're back. Yeah, the system G is having issues here. That's unfortunate. I like system G. So we have

**Matt Yonkovit:**  
Charly, user. Yep. Just user. That's all.

**Charly Batista:**  
Sorry Matt. What did you say?

**Matt Yonkovit:**  
I said that was just user error. We just forget the config earlier, I think when we were doing the last stream. Yeah, when we were shutting it down from the last stream. And we're done with it.

**Charly Batista:**  
Yeah, I'll take a look on that one later.

**Matt Yonkovit:**  
But the shared buffer is now up to eight gigs.

**Charly Batista:**  
It's yeah, it's six

**Matt Yonkovit:**  
Sorry.

**Charly Batista:**  
Yeah, I was gonna start but I wanted to save two gigs for later. So, you spinning up the load again?

**Matt Yonkovit:**  
Yep, give me one second.

**Charly Batista:**  
Let's see if it was anything.

**Matt Yonkovit:**  
The load for this is Charly heavy, right workload. That's the name of this workload

**Charly Batista:**  
you name it your workload, really?

**Matt Yonkovit:**  
I mean, after Charly it is Charly's workload so blame his workload.

**Charly Batista:**  
Let's take a look at this one. And I suggest we do if we just finish from here because I think we are more than one hour Right? Right. So we can keep going from here to the next session so to finish see it may not be able to finish everything in one session but you may have your 25 by the end of the day.

**Matt Yonkovit:**  
Yeah, well I think I think efficiently you're up to 793 live streams you owe the community here so that's what I mean

**Charly Batista:**  
all right. Let's take a look so my box if it's still waiting for the oh no the checkpoint is done. Thank God I didn't crash my box.

**Matt Yonkovit:**  
The workload on mine is running it's just gonna take a few minutes to start like doing it stuff right

**Charly Batista:**  
Yeah, well my workload it's back so what is my suppose this is my box there are too many boxes you know I'm confused Yeah, this is my box. See, it took just 15 seconds for this transaction to finish almost not slow it took a lot longer was there how many transactions that took at least 15 seconds, and see how many locks we had during that time. all right. So now we are back and we should see the IO wait everything is back as we didn't change anything or fluctuation on my box right. So one thing that I remember is that we want to change the wal size, the min and max wal size. So as we are advancing on time, I going to do it here. And okay, I don't need you. I need to restart my database. So let's stop this load here. I'm using Patrone on this database here. And I'm also using port 22. Do my day my configuration changes. So everything that I change it on my configuration, they are here you can see. So I keep the max  wal size is full. And you're right, it's eight megabytes of min_wal_size. So what we're going to do is, we're going to increase for one gigabyte, of my min_wal_size. And for this box are going to use five gigabytes of my max wal size. And this is not enough, we need to tell the database how we want the database to distribute that load over the time that we were given to the database, because while even though we have like a max wal size of five gigabytes, we can also have the the timeout for the I just forgot the name the checkpoint, right? So we need to give the database more time to process I don't want five minutes timeout. I think that's the default for the configuration. And I really don't remember if the name of for me to SharePoint time out on top of my head now.

**Matt Yonkovit:**  
I'm googling timeout the timeout parameter.

**Charly Batista:**  
Yes. I'm just using Google it's easier. Yeah, it's checkpoint timeout.

**Matt Yonkovit:**  
Oh, yeah. So checkpoint.

**Charly Batista:**  
The checkpoint timeout. I going to give it 3600 seconds, right. So it's in seconds if I'm not mistaken. And I want to give it one hour. I need to tell the database, how it can proceed. Because while even though I tell the database all the time out for the checkpoint for this five gigabytes here, it's, I want you to split the load evenly with the time I want you to wait more to wait less. So this is what we call the completion target on Postgres. There is a change on Postgres 14 If you're not sure not wrong, that, they put it hard coded to 0.9. So it will try to wait as much as it can to finish the checkpoint. It won't force the checkpoint to promptly finish. So and it's the name of the parameter is a checkpoint. Now I googling again, because they don't really remember

**Matt Yonkovit:**  
You mean, like the completion target or?

**Charly Batista:**  
Yes, the completion target. Yeah.

**Matt Yonkovit:**  
I mean, the default is point nine. It's point nine. The default is point five. No. Now, as of 14. it is point nine.

**Charly Batista:**  
It is okay. Sure. Oh, I'm using 13 by the way. I'm not sure if they put the full point nine.

**Matt Yonkovit:**  
it changed in and it's point nine in 14. And it's point five in 13.

**Charly Batista:**  
Yeah, I'm using 13 here. So I got to put point five. The only thing that we change is related to the wal right, so I'm checkpoints nothing else. Gonna save. Oops, I need to be rude to do this. systemctl restart Patroni. Yeah, it should take some time. Because we have a lot of things going on here. So it should take some time to restart the database. That's expected. So you got your load back? Yes. Okay. While you were waiting for my database to get back, let's go back to your workload. You're shredding it back. Okay. Yeah, I was just ALRIGHT.

**Matt Yonkovit:**  
I got it back. Yeah,

**Charly Batista:**  
I can see I can see that. No, that was my bad Okay, let's see what happened. Last week, we changed your checkpoint behavior. Button, just reload this here. It doesn't look, right Okay. Am I connected to the right place? Yeah.

**Matt Yonkovit:**  
130? Yeah,

**Charly Batista:**  
 130. 130. Yeah. So? And is this last 15 minutes, right? Since we change it, you're now you're writing more to your database. Let's just take a look on those. See, now we are doing more checkpoints. How is that possible? What happened was not supposed to improve your load?

**Matt Yonkovit:**  
Come on you once you free one bottleneck, the bottleneck shifts, right? I mean, so when you're reading off of disk, it competes for the checkpoint. So it's yeah, it's interesting. So if you look at like the worry throughput, the number of queries per second doubled. And the response time really stabilized. Although the response time is a little higher, it looks like. No, no, it dropped down, it dropped down quite substantially. Things are warming the cache.

**Charly Batista:**  
So now we have double the throughput right? requests per second. Yeah, that's good. So my customers getting happier. Because now we can do double the job at the same time, right?

**Matt Yonkovit:**  
Okay. Double the job, and the IO wait went down quite substantially. I mean, now you're in. But keep in mind, this is also warming up still. So after a restart, you won't get too aggressive checkpointing until after the workload has been running for a while, right?

**Charly Batista:**  
Well, you are getting very aggressive here, with a lot of checkpoints.

**Matt Yonkovit:**  
Well, but you're not as backed up is what I'm saying is like, over time, it what you'll see after a restart things can perform at a certain level. And then as system buffers start to fill up as you start to run out of space and get more aggressive in having to do background operations, then things start to slow down. So it'll be interesting because let me go look, I'm going to look at the last six hours. Yeah, so if you go if you look at like the last six hours of IO wait, for instance. Okay, so last, yeah, last six hours, just Yeah, six hours. And look at the IO wait, numbers like CPU, IO await. You can see like the first you see around 1500. You see that workload? They're like 1500 o'clock. So you're too early with your thing? You got to move it back to them? Yeah, right there. You see, you see the jump there. So it ran fine for whatever that was maybe like an hour. And then after that hour, then it almost doubled the io wait. So the workload ramps up and it takes a while. And so for that first hour, things might look hunky dory happy in terms of IO. And then after, but actually that's more like 15 minutes, isn't it? Maybe maybe 10 minutes. So then after a certain amount of time, bam, right, like IO just like spikes up. Which is interesting, because it's that warm up time. And it's kind of pushing everything. So I'm wondering after a certain amount of time here, if we'll see a spike again, with that IO, especially considering a lot of these are just very basic.

**Charly Batista:**  
No, we probably especially because the only thing that we did we change it was we gave more memory for the database. And actually, I'm expecting that the ramp-up going to be earlier than later.

**Matt Yonkovit:**  
Because of the disk because you're now freed up. Yes, regular queries to start pulling things quicker.

**Charly Batista:**  
Yes. So and that's when it comes to the parameter that we just change it on my database, right. So now we will We have to wait. And that's why my recommendation is okay, we wrap up for today,

**Matt Yonkovit:**  
right, he said for you wrap up for a year. So you don't want to do live stream.

**Charly Batista:**  
Here, here. Oh, I know I have really bad English, and on my pronunciation

**Matt Yonkovit:**  
Your year and I like what he wants to wrap up for the year.

**Charly Batista:**  
And we keep from here next session, right? So we like I'm not going to touch on my box. I'll leave it as it is. Right? So then we have the full picture of what we did. That's tiny little change. So next session, we can start the load like 1530 minutes. Well, even before the

**Matt Yonkovit:**  
So if you have time we can even just like whatever time you want to get on next week, just this random like, Hey, I got an hour, I got a half-hour to look at this again, we can jump back on.

**Charly Batista:**  
Sounds good.

**Matt Yonkovit:**  
I mean, because we don't need to announce that it's coming because most people are gonna watch off. Anyway. So

**Charly Batista:**  
that's fine. Because it's getting really lengthy is like one hour, one and a half hours, right. So you just

**Matt Yonkovit:**  
want to go to your weekend. It's Friday, everybody wants to go on their weekend. I want to go to my weekend. We all want to go for our weekend. It is late. We should let this be fun.

**Charly Batista:**  
it's raining dogs and cats here. There's nothing much that I can do all there, you know?

**Matt Yonkovit:**  
Yes. All right. Well, so we did see some improvement here. Like I said, I'm interested to see after the next hour, so yeah, whatever to see what the load on my site changes, probably. But we can come back and just let things run and see what happens.

**Charly Batista:**  
That's the thing. So let's we should let it run well, and it's been applied like one hour earlier. Next time, we get some time just to warm it up and see how that goes. And then we go back. And we compare we change the other parameters and give some time to run again. And as we have different workloads, you have to have one so we can change going forward between them while we are talking.

**Matt Yonkovit:**  
Yeah, absolutely. Absolutely. Absolutely. And we can also throw in that read-only workload that we had somebody ask about as well.

**Charly Batista:**  
Yes, yes. That's also a good one. And that's interesting to compare how they differ from each other. Right? Because yeah, one thing is right intensive workload, we have some type some problems that we see here. We might have total different types of problems.

**Matt Yonkovit:**  
absolutely. All right, everyone, thank you for coming along. Hopefully, you learn something this week. We'll try and do just a random kind of like, stream next week to kind of close out this topic. Before we get to the next topic in our lists, which I believe the next topic after this is starting to dig into replication setup. So we were going to do a basic config. And then we were going to go jump into replication setup and getting replicas. And how do we monitor lag and things? So we do want to get that to there as well. Oh, look. Nando has been hanging out with us as well. Oh, and Nando you were so quiet this whole time we didn't even know you were there. You're just you just lurking lurcher.

**Charly Batista:**  
That's the wrong guys.

**Matt Yonkovit:**  
All right. All right, well, we'll catch you next time then. We appreciate it. And check out our live streams coming up over the next few weeks and we'll catch you next time

**Charly Batista:**  
Yeah, and again, if you have questions or topics that you want to discuss here, just say no, right? You have Matt's social media so you don't have time because I'm not so social. 

**Matt Yonkovit:**  
But we're gonna make Charly social. By the time I'm done with him. He's gonna be he's gonna be mini-HOSS. All right. Bye, everybody. 

**Charly Batista:**  
Bye, everybody.


## Transcript Part 02
**Matt Yonkovit:**  
Yeah, we are coming live, everyone. Oh, we got echo. That's horrible. There we go. Oh, now no echo, no no echo. Hello, everyone, and welcome to one of the live streams. This is a very special live stream here. We didn't finish last week as we were going through some workload. And we decided to come back and take a look at what's going on on our two Postgres servers that we had set up last week to see what we can do to make some modifications and some tweaks. So yay for us. So we're excited about that.

**Charly Batista:**  
Yeah. Hey. Okay. Hey there, Matt. Yeah, we really left last week with some optimization. Right. So actually, we started taking a look on a server. So if I might share my screen? Yeah. I was just logging into your server here to see what we have. This is what they had from PMM. So we have some load, right? 

**Matt Yonkovit:**  
Oh, my, we have some load? Yes, we do. Yes, we do. And, and, and look at that beautiful, non-uniform distribution.

**Charly Batista:**  
Yep. Let's get just the last three hours to see here. 

**Matt Yonkovit:**  
Look, look, Gonzalo joined us. Hey, Gonzalo. Well, this is a stream we didn't figure many people would stop by because we didn't announce it on purpose. This is a follow-up to kind of finish our live stream from last week, and probably be good to put the two recordings together. So. But I do have a new hat to show off when before we're done. So that's important. I visited our esteemed CEO today, and he brought me a new hat. My dogs think it's a chew toy, though. So this is my new hat. We'll put it on in a little bit. To build the suspense to keep the audience watching us. Right, we want to have them pay attention as much as possible to the stream. So stay tuned for the hat reveal. It's coming up.

**Charly Batista:**  
So today is not only my suffering here to figure out the problem, your database, right. So we have this hat

**Matt Yonkovit:**  
My suffering.

**Charly Batista:**  
Yes, no, this is the life, your order, the customer goes there and do something like I know you probably did something.

**Matt Yonkovit:**  
You know, me, why would I do something? Oh, why would I do something?

**Charly Batista:**  
All right. Let's start. So what were we left?

**Matt Yonkovit:**  
Well, we changed the shared buffers last time. That was the big change. Yes, we did change , and we saw a significant increase in overall performance.

**Charly Batista:**  
Okay. So what you've seen during the week, and your load test, do you still have this performance improvement? 

**Matt Yonkovit:**  
So it is still performing better? But we are seeing some errors now.

**Charly Batista:**  
Okay, which are?

**Matt Yonkovit:**  
We're actually hitting connection limits.

**Charly Batista:**  
Oh, now we are hitting connection limits. But as I remember, you had a 200 connection, right?

**Matt Yonkovit:**  
I believe we only had about 100. If we go look at the top, I think Max connections was set to 100 on this box.

**Charly Batista:**  
Yeah, yeah. Yeah, we can check it. 

**Matt Yonkovit:**  
So you can see like right below you see the Postgres connections. You can see where it hits over. 100 Right.

**Charly Batista:**  
Yeah, it does. That's yeah. Sometimes, tries to go over a limit. And this is interesting how it is possible if you have a 100 connection limit, the graph here shows you 200.

**Matt Yonkovit:**  
This is a good question. Tell us, Charly.

**Charly Batista:**  
That's a good grasp. Right. So how is that possible?

**Matt Yonkovit:**  
So, tell us, Charly,

**Charly Batista:**  
that's my question, right?

**Matt Yonkovit:**  
There are idle connections, right. So most of them are said

**Charly Batista:**  
Yeah, the total number of connections here, see, we have like 89 actives, some idle transactions. And it should not go over the limit, right? It should not go over 100 connections, because it told the database to limit 200 connections, right? So what happens if I go to the database? Now? Let's connect here

**Matt Yonkovit:**  
It'll probably let you through, by the way, because I don't think we're at 100. right, this second.

**Charly Batista:**  
Okay. So if I, yeah, right now, they start activity just show like around 50-52 connections. So why do sometimes do we see this over-limit number of connections. Still my question any gas, and eat?

**Matt Yonkovit:**  
Any hint or guess, so you're making me pick? Again, I told you, of course, that I don't like that. I want you to guess where yourself. So there are actually a couple of things that I can think of number one, it can be a metrics issue. So because of how PMMs collect metrics, it could be counting metrics that are between cycles, right? So, you might see at the point in time, where it collects the Postgres connections merged with a second or third pole, and they might show is different. Right? So, that is a possibility. Sometimes, you'll see what we call metrics jitter and some metrics where you'll average two numbers together, and it will not make 100% sense. So that is a possibility.

**Charly Batista:**  
Especially for databases, like Prometheus and Deterra metrics. Sorry, it sometimes happens quite often. Yeah, that's one of the possibilities. And the other thing that you could 

**Matt Yonkovit:**  
well, if you look at the connections, next, you see the max connections actually do pass their stop at 100. So we are only getting up to 100 active connections at one time. This means that the other connections that are being listed are not active.

**Charly Batista:**  
That's too, and we have. Another thing that we need to take into consideration is this math comes from when a connection buys for the endpoint, what we have for client-server architecture, we should have two endpoints, right, we have the client, and we have the server. So we have the Postgres client and the post Server database. So from the TCP point of view, when you open the connection, everything goes fine. So, we have all those two endpoints, when you close the connection, they don't immediately close the front from the connection point of fill. Right? So, you still have it on all those endpoints, the connection alive for a certain period of time. It depends on how we collect the metrics, it can count as a still open or active connection, or from the database point of view. So even for the Postgres, that connection is now active, and more but still alive from a TCP stack point of view. Right. And this is important to notice and understand, especially when we have a proxy in front of the database. Let's say we have a PG bouncer, if we have a configuration problem from the Postgres side or if we have certain timeout limits, too short on the database side and database, the post we start closing the connections by itself, those quadruples, there is a client TCP IP client, TCP port, server IP and server port. They're going to be busy, usually for like two minutes. That is the timeout for the limit stack to release them. If we put if we have too many closing connections from the database site. And they all come in from the proxy. Eventually, we're going to reach the man Number of the connection that this allowed for the Linux kernel to accept from that node, in this case from the proxy. So even though we might not have any live open connections from the database, then the proxy will not be able to connect to the database anymore, because it's been restricted by the kernel. It's a common problem. Like, for example, websites when we have something in front of your website, like a proxy in front of Nginx, or Apache. So it's something that can happen quite often, especially for configuration problems. So if you have a misconfiguration, it can also happen to the database, right? And when we see something, why these it is worth, investigating if the problem was just about metrics, or if the problem is just what I tell you, it might have a misconfiguration problem here. Okay. Right. So we might have like something from your database causing connections, because the problem is, who closes the connection? If the application closes the connection, so is the application that needs to wait for the kernel for the OS stack to release that is spot on the connection timeline. If the server closes the connection, then on the server-side, it has worked. So and we might have this implication, right, let's keep just a note for now. Because this is not what we are for today. Today, we want to look at performance.

**Matt Yonkovit:**  
Well, all configuration. And obviously, if users can't connect, they have no performance. You can't deny me

**Charly Batista:**  
Whoa, depends. While, if my database has no queries, it's quite fast. I can tell you,

**Matt Yonkovit:**  
But users are what matters. Right? Users?

**Charly Batista:**  
I agree. I tried to escape that one, but

**Matt Yonkovit:**  
You can't escape that. Can't escape that.

**Charly Batista:**  
Alright. Yeah, but let's keep if it's a note. So this is something that works investigating. Right? Yeah. But right now. So if we look at the application, you're saying that we're, the application is hitting the limit? The number of correct, right. I don't think it's doing right now, because I can't see the graphs.

**Matt Yonkovit:**  
Yeah. So it was at a certain point, and then it backed off here. Yeah. Because what users couldn't connect to, they said, Screw you, guys. We're going to a different website. That's what they said. Yeah, that's what happened. They all hit they couldn't get on. And they went away.

**Charly Batista:**  
Which is, which is bad? That's poison. It's bad. Or okay. Yeah, it's not good. All right. So let's check here. How is Oops! Okay. So while I'm here on the database, I want to check some parameters, right. So usually, the most common way that people go is to do like something like show all, and check all the parameters here.

**Matt Yonkovit:**  
Right, a lot of parameters though, isn't it?

**Charly Batista:**  
Oh, they do. They do. We can also go here, on PMM, right! So we can, you can have something similar here. On the settings here, so this is a little easier to read. Yeah, I was about to say the same. It's a lot better to read. Right. So and we can have some, some settings here that we usually the most we can put here. Okay. So as a client, would you like to increase the number of connections? So, you wouldn't have the same problem again?

**Matt Yonkovit:**  
Yes, I want you to put it to 100,000 because I never know how many I'll need.

**Charly Batista:**  
I would love to put in 100,000. Like well, Buddy, I have like a wild gas that would not work with work quite well, for your setup to 100,000. Correct. What? It's just a wild gas. I might be wrong, but it's just a way of the gas. Right? Because, well, you have a 32-gigabyte machine right or a gigabyte box. So let's say we have a 32 gigabytes box. If I remember, right, yes, this is 32 gigs. Okay, so we have 

**Matt Yonkovit:**  
by the way, are you going to do math? Now I know, no. No math. Okay. Just gonna say if you're gonna do the math, I was gonna shut my camera.

**Charly Batista:**  
I was just I just want to say that we have some limitations for the number of connectors, but we have some things that they put physical limits for, for max number of connections, right? So for every connection that we get to the database, we need to use some portion of memory. Right? So then if you have 32 gigabytes of memory, or in your box, you need to have some memory available for those connections for each of those individual connections, so they have some buffers, like, for example, sorting buffers, the query buffers, all sold both buffers, they gonna use memory. Right? So, but you also have an operating system on your box, don't you? 

I mean, it's just a database.

No, yeah, full. And unfortunately, the operating system also needs memory. So we cannot use all the memory that we have for the database. Another problem, but this is the most common thing that people use to tell the users they cannot increase the number of connections because they have a limited number of memories. Right? But what if your database had 1.5 terabytes of memory Ram, would you put, would you be able to put like that 100,000 connections? One thing? No, let's say you have 1.5 terabytes, right? 

**Matt Yonkovit:**  
Wait, let me put on my thing. That's quite a lot of memory. Right. What am I thinking, cap? So do you think the answer is no, I don't think that that is possible? My thinking cap, says, hit some limits there. And by the way, if I had 1.5 terabytes of memory, I would have to be filthy rich. And so I would pay someone else to figure that out for me.

**Charly Batista:**  
Yeah, I don't know. But the thing is, some people like to do those, even though they have plenty of money to pay for someone else. They like to be bold and do things. And there's nothing wrong with that. If you like, you'd like such a person that you'd like to get your hands dirty, doing things. That's fine. Oh, well, I probably would also pay for someone else to do that thing for me

**Matt Yonkovit:**  
I knew that you were like me. Ah, yeah. So I mean obviously, the memory constraints at that many connections, and just managing that many connections are going to be too many. And I mean, any database is going to start to fall over dead pretty quick. As you start to open that number of connections. It's not just the memory that's constrained at that point, you've also got CPU concerns, and you're going to have weight conditions and other things that happen. So obviously, there is some limit, and that's why connection pooling. So critically important, especially considering that your active throughput is going to be limited by the number of cores and the number of things that are going to be active anyway. So unless you're going to match that 1.5 terabytes with a 10 million core box, you might not get the results that you want.

**Charly Batista:**  
That's a very important thing.

**Matt Yonkovit:**  
Of course, it's important because I wear my elephant hat, and it totally told me that that was right. Elephants are wise, right? Or is that oh, yeah,

**Charly Batista:**  
they are there. And they have a really good memory. Right? Of course, they have a good memory. So yeah, and that's, that's a very important thing. CPU. So when we're going for the database, we have a lot more to do with other than just memory and IO, right? I've seen people talking about IO, how badly it can impact performance. And again, again, they're right, yeah, IO can really be a huge problem when you have IO saturation, and I, and we've seen on the last talk, how badly can impact performance. Right. But well, we also start to get into the CPU saturation, it can be really, really bad as you said. Ah, we have the physical limitation, as it doesn't matter how fast the CPU is, the CPU is still can only do one job at a time. Right? So one CPU core can only do one job at a time. Right? So and if we get to that number of connections, let's say the 100,000 connections, so let's put we can put, I don't know 1000 cores, 1000 CPU cores in our, in our box, well, doing really simple math, every core needs to deal with at least 100 connections at a time. Right? So, that would put out a huge pressure on the CPU. And it will start to go really, really slowly. Do you want to do something? 

**Matt Yonkovit:**  
What do I want to do? You can play around with this box. That's fine. I just have to restart the workload.

**Charly Batista:**  
I just want you to change here. It's a mistake. It's only to see PostgreSQL. Okay. 13 main. Postgresql.com. I want to put here to 2500 2500 You are a madman. But I don't want you to put 2500 connections, you just want 1000. But it was the database to be allowed to accept 500. All right. So let's start slowly, just with 1000. If I don't make the mistake, we need to do a manual restart here, right?

**Matt Yonkovit:**  
Yes, there was something wonky with how that one was set up. We go back and connect the service CTL.

**Charly Batista:**  
Yeah, we yeah, we can do it later. But right now. So what am I going to do? Okay, this is the start. And okay. Do we have a stop here?

No. Is there any problem sending a cue to all those signals on Postgres?

**Matt Yonkovit:**  
Well, we talked about that before, it will have to recover from them. So it is not a recommended best practice to kill.

We covered that in the last one because you had to kill this instance before we didn't really fix this instance or change over to the other instance that is not kind of wonky?

**Charly Batista:**  
Well, that's fine. I just want to show you that we do have different signals. And we said, yes. Oh, yeah. I want to just send a CQ. Right. I don't want to send it because when we stopped the data is when he stopped Postgres, actually what it does is sends a CQ to the database. A CQ is is a gentle request to the database that just asked the database, can you please stop? Right? So actually, this is what the system does when I do the system D,  Postgres whatever service is stopped, it will send a CQ to that service anyway. Because well, the service might be doing something during that time. And eventually, it will just stop, right? This is what I want to do here. I want to do a CQ, I'm going to do a kill-9 because a kill-9 is it's a huge problem. And they got to ask you why a kill-9 is a problem for the database

**Matt Yonkovit:**  
Is it pulling the rug out of everything? Like underneath everything, it just our core crashes and shuts down. Right. It's like stop. Don't wait for anything. Don't wait, just wipe it clean.

**Charly Batista:**  
Yeah, why is that a problem?

**Matt Yonkovit:**  
Because there are still things in flight being written. There are operations that may be kind of in a wonky state. You want to kill as gracefully as possible or shut down as gracefully as possible.

**Charly Batista:**  
Yeah. Yeah, that yeah, that's, that's true. So for databases. Remember, we have a lot of caches on the database, right? For example, in this instance, we gave the database, six gigabytes of cache. If we're writing to the database, every time that we do a commit, we do an update, and whatever operation that writes to the database, it does not immediately write down to the disk. It might be in on some sort of cache for the database, right? And when we do a kill-9, as you said, it doesn't wait for anything. It just cuts off the edge, and it's gone. So if we have any cache or anything in the cache that still needs to go to the disk or needs to be asked to the OS to be flushed. It won't have time to do so that's why we always want to do to send a gentle CQ. to say it didn't do immediately because it's, it was doing its own cleanup. But now it's gone. You don't have here that the Postgres anymore, right. So that was a gentle ask the database. As you see here. There are some services they were doing some cleanups and some stuff that's still needing to be processed. And when it was done, the database just found that it was time to go and rest in peace. So that's why it's so important to do not to send a kill-9 to forcefully kill the database unless it's extremely necessary.

**Matt Yonkovit:**  
Yeah, last resort because the recovery is questionable. And so if you do a kill-9, there might be data loss or corruption or some other fun. Well, fun things happen. Actually, if you want to have a very eventful and exciting day, go ahead and kill dash nine of your database. Yes, everyone out there. If you're looking for some fun this weekend, go out to production and do a kill nine. And tell them Charly told you to.

**Charly Batista:**  
Well, and I can even show him. Yeah, they can take the just this would be the nice comment. And we'll kill everything that has Postgres. Right? Don't do it. Don't do it. But don't do it. It's just

**Matt Yonkovit:**  
Don't do it. Don't do it.

**Charly Batista:**  
All right now.

**Matt Yonkovit:**  
So is it, did you start it? Is if you started on it.

**Charly Batista:**  
Start, I'm starting now. Yeah, I'm just now, let me take a look here. Where is my instance? So okay, it's everyone may not, I want to be a bit faster. Let me put here the last 15 minutes. So it can see it better. Yep, we have an interruption. Just here. And it's back. It should be back. It is back. And here we have hiked. See some odd here? There you go. see we have we are up to almost 3000 connections. So what is the max connection that you put for your old?

**Matt Yonkovit:**  
I can put it as whatever you want. You want to see a lot of connections. Yeah. Wants to see a lot of connections. How many do you want to see?

**Charly Batista:**  
Alright, like, I think 1000 It's, it's fine. You have a big box

**Matt Yonkovit:**  
Yeah, the only problem is you're gonna run out of resources on the app server. Because I'm running a single app server right now. But this is actually a very easy change for me to do. Let me go ahead and

**Charly Batista:**  
Just want to know what happens if we have 1000 connections?

**Matt Yonkovit:**  
Okay, fine. Just give me a second. You are so impatient. Has anybody ever told you that your impatience is not fun?

**Charly Batista:**  
Well, I Well, honestly, probably markdowns.

**Matt Yonkovit:**  
Okay, so how, why don't I just go to, like, 150 or so real quick. And then we can adjust from there. How does that sound? Right? Because like I said, I'm not sure how much the app server that I'm using can spin up. Python threading.

**Charly Batista:**  
Limits, right?

**Matt Yonkovit:**  
Yeah. Yeah, I mean, this is where like, from a Python perspective or your application server, there's also going to be a limit there on how much can be thrown to the database, as well. And I mean, you get around that by building this out, like a Kubernetes, or a cluster or a containerized application where you can add more nodes. And that's fine. I can do that as well. It's just I so happen to have a single node right now that's running his workload, which causes some other issues as well. But I've been bottleneck gain this on purpose. So yeah, so right now, it should be that the number of connections should be increasing to at least a couple of 100. 

**Charly Batista:**  
And what problem that we have with Python is because it was not designed to be mute core, right. So even if you create 1000 threads in your Python unless you're using C Python,

**Matt Yonkovit:**  
I'm using processes, so these are spinning off individual processes. Okay. So yeah, so each one should be able to handle, but it's still gonna have some weight things, but you can look, those connections are increasing.

**Charly Batista:**  
It is. So we have more than 100 connections open here, and now it went down.

**Matt Yonkovit:**  
That's probably because, let's see. Yeah, it's probably because this workload randomized, so it will continue to change and evolve over time. But here, just Yes, I want to overwrite it. Because yeah, that's what happened. So now it should go back up to those connections in a few seconds here, it'll bounce back up. There's actually just a configuration file that has the number of connections for each type of workload you want. And I just randomly change that every five minutes or so to adjust the workload, so you get these nice graphs that go up and down. Because one of the biggest problems you see with benchmarking is when you have a consistent workload, it is a false workload, right? No one runs consistently at whether it's 80%, 100%, or 60%, you see spikes up and down based on what's happening in that timeframe. So I figured every five minutes randomization will work. I can also run it, so it is parallel. So one of the other databases we have up here has been running the exact same workload for a week, and you will see almost no deviation from its parameters, right? It's just kind of consistency across the board may be plus or minus, like a 5% change. So that's one of those really interesting things that you have to be mindful of and avoid. But look at that, look at your look and see just for you, Charly, I generated more, more and more.

**Charly Batista:**  
Nice. So

**Matt Yonkovit:**  
Everyone, Charly asked for more connections, just like we need more cowbell and most songs.

**Charly Batista:**  
And my question is, do we have actually more tuples with more connections?

**Matt Yonkovit:**  
Probably not. I mean, I think that there's a couple going to be a couple of limiting factors here, right? So because even though these are processes on Python, you're going to have the application server still has to receive the results and do some processing, which is going to take some CPU cycles as well. So in this case, by adding more connections, you could also be hitting your CPU limit on the database server, which means that more connections are just going to flood the gates here. So, take a look at what's the CPU right now. I mean, I'm guessing that's going to be pretty high. Yeah, I mean, you're hitting 100%, right? Yes, no, you are maxing out to CPU. So adding another 1000 connections here isn't going to do anything.

**Charly Batista:**  
And this is an important, really important realization, especially when it comes, to development. Right. So it's a really common part, the development teams, they say, look, the application is it is low, because well, the database is behaving is slowly can we have more connections to the database. So we open more connections, we have more processing in parallel on the application side. And I'll, it's pretty common that we do not realize that's open more connections doesn't mean that more data coming from the database, we just have more connections waiting for the data from the database side, right? Yeah. And as we are putting more and more load, the database is going to like the results are going to be stressed and saturated now, instead of being faster, or slower. Because we have a lot more saturation.

**Matt Yonkovit:**  
Yeah. Yeah. And I mean, if you go to real quick, go under like the dashboards to go to a custom dashboard. So if you go to the site and hit managed, so like the side menu bar, yeah. So go up one. Then go to manage. And scroll down. Believe Yeah, so there's a PMM test Postgres only dashboard. Click on that guy. Yeah. Now that's MySQL, click MySQL, go to MySQL. I have one for all that all databases that put these together, but the Postgres one alone is designed and optimized just for Postgres. Yeah. Yeah. So this is where if we look in your on 111, so you're gonna have to change the node to 130. We should be able to look at the response time here. And so we get this response time graph. It'll be interesting to see. If you go back the last hour if you notice any sort of like improvement or degradation in the response time itself. So you can see that there, there's a more sustained spike in that kind of six milliseconds. And we did get a pretty big jump in the number of queries per second, though, look at that. I mean, we're almost at 30,000. So we are processing more, but it is taking a little longer to process it looks.

**Charly Batista:**  
Yeah, that's the thing. And there are a lot more than a number of connections to improve performance. Right. So if we try to put more, also, we can be floating your network?

**Matt Yonkovit:**  
That's another big question. Yeah. I mean, I've seen that before where the network pipe, the bandwidth between two servers just gets absolutely saturated and bogged down.

**Charly Batista:**  
Exactly. And if you take a look here, see, if at some point it starts going down? Because this is what happens? Okay, we're starting fresh now. As we start thrashing, we don't have the cache to buy. So we take some time to warm up the cache. And eventually, as we have too many connections, so many transactions at the same time, the cache became too small. So we never actually get to award cache, because it's, it needs to be replaced too often. Right, right. So that can also be another problem when we have too many connections. And one thing that can happen is when we have a connection pooling in front of the database, is also to have an external caching system like Redis or Memcached. Fridays. Yeah, yes, exactly.

**Matt Yonkovit:**  
is anybody still using mem cache out there? I mean, I was when I was around. It was. That was the thing, right? I mean, that was kind of progress, though. But kind of my dating myself. Yes. I'm so old. They do. Like to Grumpy Old Men. Charly. Did you, by the way, did you see that? The new stream cover? For our stream? If you haven't, you can take a look there. Let's see. So what do you think? I thought we should caption it. Too Grumpy Old Men talking Postgres because we look kind of sad there. Right. I mean, I don't know what is. that's, I think it's, it's an interesting cover there for us. Definitely. Oh, yeah.

**Charly Batista:**  
We have a pool. Right. So.

**Matt Yonkovit:**  
Yeah, yeah, we can have a poll. We can have lots of polls. I don't know if we, I mean, like, so... Yeah. I mean, obviously, there are other things we could do so this is the other one that the team came up with? I don't know. What do you think of this one? Chino and the HOSS here? We can definitely?

**Charly Batista:**  
Yeah, I'm open to those ideas and new ideas.

**Matt Yonkovit:**  
Yeah, so Chino and the HOSS. All right. So anyway, back to our beloved graphs and charts. Now, now that we've taken that outside, we could play stump the Charly later on.

**Charly Batista:**  
Look how the latency is going here. And how the available memory is going down here. Right. Yeah. I think that the machine is getting quite big red?

**Matt Yonkovit:**  
Yeah, there's a lot of red on that, that that machine, they're in their late, like, look at that, right? It's just like, like, like, the CPU. It's like, ah, if blood-red, it's like bleeding out of its eyeballs.

**Charly Batista:**  
It is. Well, I quite like your dashboard here. 

**Matt Yonkovit:**  
Wait, wait, hold on. I just need to bask in that. At that moment that Charly quite likes my dashboard. Everyone. The stream has ended. There is nothing more I can do. I have made Charly like my dashboard. And he gave me a compliment. He didn't try and stump me. Oh, I'm done. Microphone drop. I'm done. I'm done. I retired.

**Charly Batista:**  
You know, that's not good for my image

**Matt Yonkovit:**  
That difficult to deal with that, that I sit there, boom, I know. So, Charly, this was actually built with the support engineers and who actually gave me details on what to look forward things. So I added everything that all the support engineers to this dashboard. I personally think this should be the default dashboard. I mean, I'm just going to tell you that right now that I'm like, this should totally be it right here, and it should just be done like this. Should be the default for Postgres. But I do not get that say. But if you're watching this later on, and you're like, that's an awesome dashboard, it is available on GitHub right now. So I can point you in the right direction, all this wonderful stuff, including the thing that's making this workload, is out there as well.

**Charly Batista:**  
Yeah, and this is one thing that I really like about PMM. It's extensibility. Right? So it's easy for anybody out there to get it and make amazing features and backward like this one. It's very extensible. One can say, oh, but it doesn't have everything. Well, maybe that's the trick. It doesn't have everything. But it's open for anybody to implement anything that they want. 

**Matt Yonkovit:**  
You see some cool,

**Charly Batista:**  
You can pull your coffee machine here and get data for you

**Matt Yonkovit:**  
But you want to see some cool, scroll up? Yep, scroll up to my query view. Okay, find a query that you want a little more information on, you might have to scroll to the right to get like the metrics. Great. Yeah, like, there you go. So if you wanted to look at like the one that has the highest average time or max time, like choose one, just yeah, look at this. See. So this is where you can get the heat chart for that one particular query, the response time just for that one query, how many queries per second that's running. And if you scroll down, you can see visually, how each one of those queries ran and get a nice little kind of like, histogram of that. So boom, mic job. Anyway, that was not why we were here. So Charly, back to tuning this instance. Okay, but thank you for the praise, I feel accomplished. I am retiring as King of the PMM, dashboards, and King of streams. Thank you all for participating. Charly, we're here to see what else we can do. Obviously, the workload has changed again. So that things have adjusted, as I said, users will come and go on the system. And during the busy times, you saw, we got up to like 300 connections. But like any other real production workload, you're going to have spikes. And you're going to have things that drop. Right. And I think that's one of the challenges of any sort of tuning exercise, is as you look at workload, what was happening five minutes ago, might not happen again, for another day, as I in that up and down sort of mentality means that having the ability to go back and kind of drill into any one point in time and see what was causing issues is really important.

**Charly Batista:**  
It is. it is. let's take a look here. Well, we see this period of time here that the database had quite a lot of connection

**Matt Yonkovit:**  
Bazillion I think it's a bazillion. I think that's the official metric for the number. It had a bazillion queries running.

**Charly Batista:**  
Yeah, that's accurate math busy. Yes, bazillion. Like,

**Matt Yonkovit:**  
It's very close to Brazilians, but not quite the same.

**Charly Batista:**  
Well, yeah, exactly. Not quite the same. So let's take a look here.

**Matt Yonkovit:**  
It's okay. Charly is from Brazil. So I can say Brazilian? Because he's Brazilian. Yeah. So the Brazilian is looking at bazilians of the query. It's fun, it's like a dad joke. Right? That's still fun. It's a horrible joke. Okay. Oh,

**Charly Batista:**  
You got me laughing? That's not the that's Yes. Yes. So let's, back here to do our job. Right. So one interesting thing that we can take a look at is when the load started increasing, actually, the number of tuples went down. Yes. Right. So, if you see here, we have a lot of tuples. When we have a lot of more active connections, well, looks like the data that's been out from the database did not correspond to the increased number of your connections. Right? So and we need to investigate why. Right? So usually, you want to look at the OS at the very same time, the same period of time. Right. So, okay, we did. we should have. Okay, let's take a look. Oh, come back. He's just in the field a lot. I want to see here my node summary. And I want to select oops, that is not this one. So let's make sure that we have exactly the same. That one here and yeah, so we're looking at the very same time range, right. 

**Matt Yonkovit:**  
By the way, Charly, I think that if you go back to the way you had the original time range, you can right-click on the node's summary and open up a new tab that will keep those consistent numbers.

**Charly Batista:**  
It would, it would be okay. 

**Matt Yonkovit:**  
I just wanted to let people know, wow, that had a load average of 63 on the box. By the way, did you see that? Oh, my gosh, that box is ready to fall over? Yeah, that's a pretty high load average.

**Charly Batista:**  
Why is it a high load average? How can we tell if a load average is higher low?

**Matt Yonkovit:**  
Well, so I mean, that load average is the number of runnable processes that are on the box, right? So or that's, that's available to be run. So if you've got, let's say, eight cores, a load average of eight is probably going to be okay, maybe give or take a little bit. But if you're 10x, that means that there is naturally a bottleneck because you have more runnable things than can run at any one time.

**Charly Batista:**  
Yeah, that's quite good. Of course, it's good. Also, another thing that you need to pay a thing to keep in mind these on Linux, the low, how low the average is calculated is quite weird. It also takes into consideration the IO process running. Yes. Right. So if you go for another Unix system, it's most of them really take into consideration the process running. And like, for example, the process on an interruptible estate that's just waiting for IO, they are not usually not taken into consideration for a low average, this doesn't quite happen on Linux. Right. So I honestly don't know if it's good or bad. But we just need to also take those things into consideration.

**Matt Yonkovit:**  
Yeah, I mean, like, but just looking at these graphs, I mean so not only are we at 100% CPU, but you're saturated. You're totally consuming all the cores. Now, interestingly enough, that process graph has a rounded curve, too. And it's kind of interesting. Like, it looks almost like, as a planet's like part of a planet like a horizon. It's a really interesting graph. From a view perspective.

**Charly Batista:**  
You're looking to the horizon, right? Yeah, it is. Yes. And we can start finding some answers here. Well, the first thing you said, All CPUs are saturated. Right. So definitely crashed the load average for our eight CPU cores of 63. It's not ideal. Definitely

**Matt Yonkovit:**  
Not ideal. Let's be honest. It's like it's horrible. That's apocalyptic. It's horrible. Yes, yeah. Yeah. If you're at, like that much. Yeah, that's apocalyptic.

**Charly Batista:**  
Yeah. So that's the first problem, right? So clearly, this box is, is not able to handle this node. Right. And here, you can see the context switching rise and up with something that we usually do not expect, when we have so many connections and the CPU is being smashed. We weren't we expect to see a lot more context switching. So usually, not all the time. But usually when I see this, this pattern here, from the box that smashed by huge remote. It smells like IO problems as well. So our CPU is starting to wait for IO. Things can also get quite bad. And if you see here, the IO latency, it's been crazy. See, we see up to 16 milliseconds, sometimes close to 20-30 milliseconds of IO latency. Right? So this is crazy. If we're thinking about like, you're asking for something to your own disk. Before you start getting anything back, you need to wait for 15 milliseconds. From the CPU point of view, it's like an eternity, right? So its date is never. Right. And that's why probably the main reason we don't see like so huge spikes here. If we take a look, when it's its increasing here. See, when the IO latency starts to increase, here, we see the number of context switching going down because now the CPU has nothing to do an audit and wait, why does it need you to switch and context? And when it's starting, get back? The data back from the IO then okay, CPU starts going, working quite a lot again, right? So this is interesting. So we have two main problems here. And at this moment, that huge number of connections didn't increase performance, because well, they are smashing our CPU. And they cause a lot of IO problems to our IO, right? So if you see here, actually the IO activity gonna slow down, because the I/O goes so high, it's so extreme that this doesn't process. Yeah, yeah. Ability to keep up with this. Right. So those are the results of what we did well, at this point. For this box without changing any configuration, so the better thing that we could do is to put a connection pooling like a PG bouncer or PG proxy in front of this box and limit the number of connections to the database. Right? So probably taking it back 200 150 Max connections to the database. Look at the TCP transmission here. It's also a bad indication. It's not that high. But like it was, it was lower before, right. So everything is starting to get messed up. And the network traffic is as expected as now we have 1000 connections, sending a lot of things to the database. We will get the network probably for that as well. Yeah, so for this investigation here. 1000 connections is definitely too bad, right? For two main reasons that we have. So but what if we put it back two to 500. Do we think that the box would be able to handle 500?

**Matt Yonkovit:**  
Well, keep in mind, while we had 1000 connections, we only ramped up here to around 300. So if you look at the overall number of connections here, we didn't even hit the 500 or 1000.

**Charly Batista:**  
That's a good point. That's a good point.

**Matt Yonkovit:**  
Yeah, see right there. So do you do see a couple of spikes that hit up to like 500, but it's very rare. Most of the time. It wasn't.

**Charly Batista:**  
Yeah, mostly. Yeah. Most of the time. We're below 300.

**Matt Yonkovit:**  
Yeah, so I only added about 300. Now again, I could throw 1000. But it was already dead.

**Charly Batista:**  
Oh, no, we will read crash. Yeah,

**Matt Yonkovit:**  
Yeah, it is unless we want to do that again. oh, no, it's Daniil. Welcome. Thanks for joining. Thanks for saying hi.

**Charly Batista:**  
And well, that's what we saw from the last point right, now let's take a look at the database. So, okay, I just want you to go back to Okay, here is where we started. So, when we start getting a load that is too high, one thing that we should expect is to increase the number of locks inside the database, right? So, there are many types of locks on the database but the overall number of locks, in general, should spike in Yeah, this is so this is around when the time that the load starts, right? So, if you see the number of blocks, they're not that bad. And then things start getting quite high here, right.

**Matt Yonkovit:**  
And if you compare that to now so if you draw out your graph and look now or look starting like just change to now. Just changed. Yeah, yeah. I'm trying to. Yeah. It's loading, there you go. And so if you come down there, you can see like, once those connections went back to a normal workload because keeping in mind, we ramped that workload up to 300. Whereas normally, it was running in the let's say, 50 to 120 range on a normal given day. You could definitely see that change, you can also see that there's a workload change that just happened as well. So you see, like,  so you can see that workload changes directly in that graph.

**Charly Batista:**  
Yeah, that's pretty clear. So that's pretty clear.

**Matt Yonkovit:**  
They look at, wow, we're finding out stuff.

**Charly Batista:**  
And these impact, we could see how impactful the raising of the number of locks was to the throughput that even though we have like three, four, or five times the number of the connects that we usually have the throughput went down.

**Matt Yonkovit:**  
a good way to see this is if you go back, to my tab. So go to the tab with my, yeah, there's one. And go ahead and refresh this real quick. Because yeah, we just want to see what the latest is. So we should see that, that kind of spike there. So go ahead and just highlight, let's say, the last since from 15-30. Yeah, the last hour should be good. So you see the spike in the DB connections up to that 300. If you go down and choose one of the queries, we can look at the histogram for that particular query and look at don't do an update, do alike select probably be easier, I think. Yeah, yeah, we can look at the throughput for though, or the latency for each of the queries. And you can see how long each one takes. And so we should be able to see that spike. Yeah. So you see like the spike started to go up with that 

**Charly Batista:**  
Response time here is increasing, it's crazy. Yeah.

**Matt Yonkovit:**  
And then it dropped back down once those connections went away. So the more connections, the more bottleneck the slower things got. Exactly, exactly. But, yeah, I mean, you could see that in this as well, where you start to scroll down, and then like, look at that one, right there. You see that one that just like, right at the top, it was like, Oh, my God, this is ready to die. And then it came down. And that's, that's kind of like what your end users are going to experience. Right? If this is a query, that's something roughly quite frequently.

**Charly Batista:**  
Exactly, exactly. And this is the point. Just increasing the number of connections doesn't make things faster. Yep. Yeah, and it can go the can goes backward, right, increasing rise into too much the number of connections can just degrade the performance. Horrendously. Right? As we, as we saw here,

**Matt Yonkovit:**  
Yep. Okay, so Charly, we're about out of time.

**Charly Batista:**  
Okay, I just said to you, oh,

**Matt Yonkovit:**  
just one more thing,

**Charly Batista:**  
You want to check the chat as well. Yeah, just a checkpoint here. If you see here, around that time, see how your checkpoints around like five minutes, then sometimes just, I just want to select. this is one thing that we can change in the configuration. And we can add users for your workload, we don't want a checkpoint of five minutes or every three minutes, right? So, we want the checkpoint to be more evenly distributed in your workload, because well, it can reduce pressure on IO, right. So, well, those here during that the big, the high number of connections that we have, we can clearly see how much more checkpoints how more frequently the checkpoints were, right. So, if we cannot reduce the number of connections, one thing that you definitely need to do from Postgres adjusts the checkpoints configuration. Because these we can reduce a little bit it won't make magic it, but it will help especially with the IO. Remember that when we saw the IO stat this one was somewhere here. Yeah, also got really smashed and the latency went horrible. So the checkpoints there contribute a lot to this problem. So if we change some settings related to the checkpoint, we can have just one section focus on the checkpoints and how we do that. I think that would be really good. So we could improve the problem. But you see I had a problem related to the CPU and a lot of IO when networking bandwidth came in, but like at least were tackling some problems that we some points that you can write. Yep. So this is one area that we definitely. another one that we just mentioned here, we won't have time to check today are about the vacuum. So the vacuum is a topic that deserves a whole talk when

**Matt Yonkovit:**  
One entire vacuum talk.

**Charly Batista:**  
Yes, so, but yeah, this is just another thing that we will probably need to take a look at. And can also help improve the IO issues that we had there. Yeah, those are all the last things that I wanted to share for today. I think we were on top of the hour. We discussed a lot.

**Matt Yonkovit:**  
We did. We did. And so Charly, let's go ahead and flip your camera back to just you. And we will bring you back in for the reveal of the Peter hat. So I went to lunch with Peter, our CEO today and he told me that he bought me this hat. This hat is evidently made of rain. It's a ram hat. So this is like rain for something. So I'm gonna put it on just for all of you, and he told me I needed to smell it because it smells like lotion. Well, the dogs get to chew toys. Oh, yeah. Oh, yeah. The dogs got really excited when I brought this toy. Oh, yeah. They were like they were jumping all over trying to get at it. Because this is like what you would like, they have these toys you could buy at the pet store. Like this, right? Yeah. It looks like a triple maybe from Star Trek so that they Okay, let's do the hat change. So you could still hear me, but I can't hear you for a second. So let's see. So, let's see. Evidently, I'm supposed to get it as low as possible. It doesn't really work with the headphones very well. It actually looks like a wig. I don't know. Yeah. I mean, like, maybe other people can tell me this. This. This actually doesn't look like a hat at all. It looks like a wig. It looks like a fancy dress with this.

**Charly Batista:**  
But before you put the headphones in there are some dresses, some hats, or Asia prior to Mongolia. And then that they have some hats there. It looks like those

**Matt Yonkovit:**  
Do they Okay, all right. Well, I think so.

**Charly Batista:**  
This camel flower. Something like that looks good.

**Matt Yonkovit:**  
You know, that's cool. I'm happy. Like anytime somebody wants to send me a hat I'll wear although, like I said this, this totally makes it look like this is my hair. Like on camera. I think this makes it look like I've got big white hair. 

**Charly Batista:**  
Does that look like a wig?

**Matt Yonkovit:**  
It does not look like a hat.? And Daniil was telling me like you got to get this hat for Peter. It's so awesome. It's so awesome. It's so awesome. And I got it. And now it looks like I'm wearing a friggin wig. I mean, okay, thank you, Peter, for the hat. As I said, I love hats. I have a hat collection. I've got like 1000s in the house. But this totally looks like a wig. When I look at it up to the camera. What does everybody else think? Comment? Does this look like a wig or a hat? I think it looks like a wig. And it probably has more hair than I have right now. Anyway, so maybe I'll just wear this for the rest of my days and people will just think I'm cool.

**Charly Batista:**  
Well, and it's probably quite warm and comfortable during winter, right?

**Matt Yonkovit:**  
Yeah, unfortunately, it doesn't get very cold here. Yes, Daniil. You saw the hat. Yes. Wonderful. It doesn't look like a hat. It looks like a wig. Like I'm like Mozart or something back in the day when they were the white wigs. Or I could Yeah, I don't know. But okay, so here's what's coming up. So next week, Charly is back with us at our regular scheduled time. As I said, this is not a regularly scheduled live stream. So if you see this, and you're like, What the heck did I miss it? No, you didn't miss it. We just didn't finish last week. So we wanted to come back, cover a few different things. Next week. What we're going to do is we're going to take the same instances, and Charly is going to come along and configure the alerts. And we're going to talk about what sort of things we should be monitoring in a production system. And what are sane thresholds for those production systems?

**Charly Batista:**  
 Yep. Yep. We got to start them. 

Wait, wait, Daniil. It's not gray. It's white. Why would I look like a gray-haired Marge Simpson? No white. This is white. It's not gray, maybe a white-haired Marge Simpson, but I think it needs to go like this. Hi. Yeah. And it goes like, a lot. Yeah, yeah. Yeah. Anyway, so yes, Charly, next week. Alerts. Alerts. Yeah. Be prepared. Be prepared.

I'll keep an alert about next week. Okay.

**Matt Yonkovit:**  
Yes. Great Daniil. You look forward to alerts, and maybe I'll wear this hat for alerts will alert you to this hat coming. All right. All right. Fair enough. And so for the two Grumpy Old Men, Chino, and the HOSS, we thank you very much for showing up today and watching the stream, and tune in next week for the discussion on alerting. Whoo. Alerting everybody. All right. 

**Charly Batista:**  
Keep eyes on it.

**Matt Yonkovit:**  
Yes, yes. Thanks a bunch



