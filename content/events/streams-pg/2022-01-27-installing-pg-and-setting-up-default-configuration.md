---
title: Installing PG and Setting Up a Default Configuration - Community PostgreSQL
  Live Stream & Chat - Jan 27th
description: Check this recording for more tips and tricks on Installing PostgreSQL
  and setting up a default configuration with Matt Yonkovit and Charly Batista
images:
- events/streams-pg/pg-stream-week-1-january27.jpg
date: '2022-01-27'
draft: false
speakers:
- charly_batista
- matt_yonkovit
tags: ["Postgres", "Stream"]
events_year: ["2022"]
events_tag: ["PostgreSQL"]
events_category: ["Speaking"]
---
Listen out to this full recording of the 1st Live Stream dedicated to PostgreSQL hosted by The Head Of Open Source Strategy at Percona, Matt Yonkovit with Charly Batista, PostgreSQL Tech Lead at Percona. They took us through the installation of Postgres and the setting up of the default configuration.
This is a part of the bi-weekly Live Streaming series to discuss Postgres-related topics and go deep into technology secrets and tricks.

## Video

{{% youtube youtube_id="sQPBqD5zcno" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
And we are starting to stream right now. So welcome, everybody. We're on a few minutes early just to get people warmed up with the opportunity before we start to get on. So, welcome, wherever you are I hope that you are enjoying your day. And I'm just going to go out and make sure that YouTube has us active and everybody has us active. nobody's quite logged on just yet, but that's okay. So, Charly, how are you doing today?

**Charly Batista:**  
I'm doing well this morning. Good. Thanks, man. How about you?

**Matt Yonkovit:**  
I am doing pretty well, myself. I am. And I think that the fun thing about today is that my heat went out this past weekend. And so the heating guys downstairs. So it will be interesting to see if he decides to come up while we're doing a live stream. So you never can tell what is going to happen on one of these, right? That's true. I mean it's one of those things. So I do see we starting to pick up a person or two. So welcome those who are here. I appreciate you hanging out with us. today, and let's see. So today, Charlie and I are actually going to be talking about Postgres. Oh, Gonzalo here, Hi Gonzalo. So I'm glad that you found us. And you saw that we went live. we're also on LinkedIn, Twitter, and Twitch today. So welcome if you're joining us on one of those. Now, Charlie, today, we're going to be specifically taking Postgres from a bare-bones install, and trying to configure it. So it has some sane beginning values, we're going to be using PMM to look at the workload, and to see what sort of optimizations we can do out of the gate and see what sort of performance improvement we can get as we go. Now, for those of you who don't know, Charlie is the Postgres Tech Lead here at Percona. So he does all kinds of fun stuff, Postgres related. And for our discussion today, and for our stream, we're going to be using Percona as Postgres 13 distribution, as well as PMM. If you do have questions, this is in an open forum, feel free to ask your questions here. And if you do like this, and you want more content on how to tune, fix, optimize, do whatever with Postgres, MySQL, or Mongo. Go ahead and hit the like button, subscribe, put a comment in here. We would appreciate it. So Charlie, why don't I turn it over to you? And why don't we get started?

**Charly Batista:**  
Yeah, oh, thanks for the interaction, as sad they do today is for us to have a fresh installation. So let me share my screen just a second here. Okay. So the idea today is we have a box with a fresh PostgreSQL installed. Right. So this is a brand new one. With all the settings being the default settings, the only thing that we have is a Database preloaded, so we have some database here, right? If we go on to Postgres, we have a couple of the database that was gently granted by Matt, this is the database that Matt's application uses. And he went there, installed the database, he started using the application, and he felt the application was running too slow. Why is the database is running slow, people may ask is not Postgres is a fast database? Isn't Postgres is a good database? The thing is, when you just installed it, the postgres database, the fresh installation, the default settings are not optimal. So most of the default settings they've been defined long, long time ago, were one gigabyte of RAM, it was very expensive. Well, nowadays, a lot of folks out there they have terabytes of RAM, right, things are getting a lot cheaper, and also the size of the data they're scaling quite highly. So what is the idea of today's talk, we're going for some default settings, some of the most common settings that spot on this way that we should be starting to adjust our environment. So we are going to use PMM to help us understand what is going on in our box. So during those tests during the load Matt, we will be running some scripts, so his application, so we're going to have some load inside of the database. And we try to optimize to change the settings and see how the impact of those settings they do inside of the database. One thing that you need to keep in mind that is, it's not rocket science. I mean, it's not so complicated to do optimization. But it's not strictly math, there are no certain rules that if I change this parameter, I'm going to have, let's say 50% performance improvements. So in a lot of cases, we need to go testing and checking how things go, right. So this is one thing that you need to keep in mind. The settings that we are going to work on here, they're the basic ones, the default ones. So the idea for today's talk is okay, well, the main settings that we can go and take a look and change to get our database with raising both in speed and performance. Of course, there are a lot more settings that you can go over, but time doesn't allow it. So we're going to stick to four or five settings on the OS, the Linux kernel because we're using Linux for the database for the session. And then we are also going to go for four or five database settings. And to start adjusting the database for the box that we have here. And to start the database for the box that you have here, we need to understand what is the box right, we need to see what we have in the box. So shall we start?

**Matt Yonkovit:**  
Absolutely.

**Charly Batista:**  
Right. So as we said, we're going to use PMM to help us to monitor the database right? To do so we need to install the PMM client and PMM server. Well, Matt has a PMM server running as we can see here. So I do have a user here. So when we go for PMM, you will log in on PMM. After this is when you go for PMM, this is the first window you will see when they log in. And when we log in inside of the PMM. That is Percona Monitoring and Management tool. This is what we see. When you log in to the Percona monitoring management tool this is what we see when you log in that cannot be seen. This is the Welcome tool. Well, I don't have anything here on my PMM. Actually, we do have a couple of pieces of information that's only about PMM itself. So if we go for the game and dashboards, this all we have here that you see so I have some information that's about the PMM server. As we can see here. This is the box that holds PMM itself. For me to start monitoring my database, I need to add that box to the PMM. For me to add that box to the team am I going to use a tool that may be PMM admin. So as we are using in this case, this box is Ubuntu. So we should just use a suit app, install and add clients on Ubuntu. I've done that before so we can speed up stuff. And also everything that they're going to do here is we can be found on the PMM documentation, right? So I'm going to use this PMM admin config to edge this box to the PMM. See here I defined the username and the password, this username and password, @username and @password for the PMM server itself. I created some variables oId on each type, the password here, right and the host name is just the IP of that box. So I gotta add here. It worked. So it says that it was added and they start to run when the agent is running. It's registered to the PMM server. So now we have an agent IPM agent running all these boxes here. If I go to my PMM server now, let me refresh here. And after its refresh, I can get all my Postgres summary. This is the summary of my database here if I go, and this is the name of my box,

**Matt Yonkovit:**  
Now you have the box as well when you register it. 

**Charly Batista:**  
Yeah, we can. That's true. We can also change the name of the box, I left it like, as the full because I easily lost myself when like, I'm going to the PMM. And I always try to find the hostname here. But if you don't change this, just use the hostname, right?

**Matt Yonkovit:**  
Okay. Yep, yep.

**Charly Batista:**  
So in my case here, uh, well, this is not the dashboard, I want to show I only add the three metrics for my database. If we see here, we don't have much information for the Postgres that mean for that box? 

**Matt Yonkovit:**  
Well, this is because I started off and no workload is active, right?

**Charly Batista:**  
Yes. And also, I need to when we add the clients, we can, we need to add two things, this is going to collect the OS metrics, or sorry for that, this is gonna collect the OS metrics, right, the CPU, memory IO and this kind of stuff. So I can go here, for the system metrics, I can have, for example, this mode summary here, this is the OS metrics, this is the match that's collected. So I can see that my box has 32 gigabytes of RAM. So has 109 304 gigabytes of disk space and a lot of information from the OS perspective. And we also get a nice summer here. That's it, I have a Linux, you boon to the Kernel version, how many CPUs they have the memory. So that client will give us information about the OS, we also want to add the client itself, right for the database itself. So we are able to collect information from the database. And to do so we need to run this command here. So I just need to create a user inside of the database, this username and this password here, they're going to be the database username and the database password that PMM will use to connect to my database. So I just opened a new session here that you guys cannot see right now. And now we will create this user, this user here. so just a second All right. And I should have this up and running. Let's see if that works. So if that works, yeah, the services were added. So now I have the database itself, inside of the PMM. So if I go again, here for Postgres, if I want to have a Postgres overview, I should be able to get some data here from my database from my instance. So how many active connections do you have, how much memory of the database, the vacuum of information we have here for the database for Postgres inside of PMM. We can also change the view that we get on top here, this is what we've seen before, right? So more information about the database. So the active connections I have now don't have many. So, as Matt said, we don't have a load on this database. So we need some load to see things changing would be kind enough Matt to stress our database a little bit, 

**Matt Yonkovit:**  
a little a lot?

**Charly Batista:**  
 I stress a lot.

**Matt Yonkovit:**  
I'm happy to see it.

**Charly Batista:**  
I got a chance here. This is false. We are looking at the last 12 hours. But we are not interested in the last 12 hours from now. I want you to see the last five minutes of what happened in our database. So I want to change here, and I want a five seconds resolution. So it will update our dashboard every five seconds with information that we have from the PMM. Yeah. You can run the load

**Matt Yonkovit:**  
So, Charlie, one thing I wanted to ask about is setting up query Analytics. You configured PMM out of the box already and you set up that connection. Did you set up PG statements or pg_stat_monitors?

**Charly Batista:**  
Well, in this one, let's take a look. Let's take a look. That's a good question. I don't quite remember if I did, but let's show what query analytics is? Well, I have a lot of red information here.

**Matt Yonkovit:**  
Was that scrap?

**Charly Batista:**  
Yeah. I don't like red things, you know. But actually, we do have the required analytics here. So the box we're using is 130. Just to make sure I'm in the right box. Yep, this is lower. Right, but great. So we're collecting data ready, using the PMM stat statement in this case. So using your question, this is a nice thing that we have inside of PMM, the credit analytics. So it's a really nice tool to help us to troubleshoot query performance, even though it's not the topic for today. So we shall have another discussion on this topic just like a short introduction here. So it's a tool that collects all the metrics that are exposed by a PG stat statement, or the Percona tool PG stat monitor. Well, most of the information on the tools are the same, but the PG stat monitor brings us a bit more information than PG stat statements, for example. We can have the plan here, we can have examples from the queries that run so a lot more information we can extract from pg_stat_monitor. So but that's a topic for another talk. So let's go back to our instance, shall we? Let's go here for the Postgres. Oh, sorry. So I want to get my summary. Yeah. And here we have, well, we have some activities from our database. I see that you had a lot of uploads. In the beginning. We have some roll chains here. So roll updates, 1.5 updates per second, and some deletions as well. So it looks like there here's a look, this isn't doing a great job right around the connection

**Matt Yonkovit:**  
It's supposed to tax the system it's supposed to. And in fact, I can change the workload if you want to see a different workload.

**Charly Batista:**  
I would love to. Yeah, please. Let's see different workloads. So then we can compare with the remember, this is the full setting that we have on Postgres, right, we have the full shared buffers, we have everything's as before, let's get another workload to see how it compares.

**Matt Yonkovit:**  
So just so you're aware. Let's see, let me go ahead and I'm going to pull up what I'm running. So this is a 5050 mixed workload with 10 users who are doing general web work and 10 users who are doing a heavy insert, update, delete traffic. Okay. So that's what we've got going on right now. And we can make some modifications and changes to that. Go ahead and log in to my server again.

**Charly Batista:**  
yeah, you can see, we had a jump and number of connections and then the record came back.

**Matt Yonkovit:**  
Yes. So I'm put, why don't we try this one? And then when that's tuned, we can try and add some more workload to it as well. Because what I'm already curious about is to see Charlie, what sort of things you're going to be looking at changing from that default configuration. Because a lot of folks who are watching the stream or will watch it after the fact, what they're going to do is they're going to install Postgres, and then they're going to assume that hey is this working correctly? What do I need to fix? Like, what are the five or six things out of the box I should change, even if I don't know what my workload is, or if I just have a base workload? And then obviously, that workload can change over time.

**Charly Batista:**  
Alright, first things first,

**Matt Yonkovit:**  
I'll set up a changing workload, and then we'll adjust that in a second.

**Charly Batista:**  
Sure, first things first, to be able to solve a problem, we need to have a problem, right? So everything that we go for settings and adjustments, and tuning is because we're trying to solve a problem. What is the problem that we have here? So we need you to find out what's the problem first. So let's say you are complaining, that's where you can be, you can have the first workload, right, that's your work is too slow, and some kind of stuff. So we can take a look from the OS point of view, this is what I'm doing here, I am just going for the node summary. Because I want to see how the CPU is being used. I want to see if I have saturation on my CPU. I also want to see how my IO is being used if I have spikes on disk IO. All right. So looking here, it looks like my CPU is pretty much underuse. Right? And well, even though I have some say somebody has some spikes in CPU saturation, but it doesn't I don't see much here. But I see that the IO is going quite a lot from time to time, I have some spikes on IO here. And we need to understand this IO graph. Because look, we have some data, we have our zero bytes per second here. And we have some data below and data after. So below we have a page out and page in so we have writes and reads right? When we just installed a box and the database, there are certain rules that we need to take a look at. As you asked, without checking anything, any workload, nothing. I want to see what I have on my box. So if I want to see what I have on my box, I want to hear for my CCNA

**Matt Yonkovit:**  
what's on your box, you're talking about memory, CPU, disk, anything like that. Right?

**Charly Batista:**  
Exactly. It's just what I have.

**Matt Yonkovit:**  
It's all yours. I don't know what's going on there.

**Charly Batista:**  
Yeah, we need to find out

**Matt Yonkovit:**  
No, PMM agent running on this node.

**Charly Batista:**  
Exactly. And it is running. Let's take a look. Okay, it's running here. Well, let's install and force it to load again, right? So one thing that we can do, like it's saying, no PMM, running, right. So let's try to forcefully install it again, see I'm gonna add, for instance. And I asked force, so let me just check here if the IP is correct. Yeah, The IP is correct.

**Matt Yonkovit:**  
And I mean, I think the other thing again, like if we need to restart like anything else on the PMM side, let me know and I can get into that, sir. Sure.

**Charly Batista:**  
Let me try to Okay, forcefully run it again. Okay. It says it was installed. The status they started says everything is running. Okay, now we have a node exporter, right? So before we had, we needed to install the Postgres agent because it just let me see the status again. Okay. 

**Matt Yonkovit:**  
And yep, it's the same run as before. Go ahead and go back. And let's see if that picks us to reload, right. 

**Charly Batista:**  
And this is a nice thing to do with a live presentation error by demo, things can go wrong.

**Matt Yonkovit:**  
And in this case, it's still going wrong. Yeah,

**Charly Batista:**  
it's still going wrong.

**Matt Yonkovit:**  
One second, let me go ahead and see about that. 

**Charly Batista:**  
So the funny thing is, we get the information here.

**Matt Yonkovit:**  
So you're getting the information, but you're getting to no PMM agent running on this node, err, typically on the system. 

**Charly Batista:**  
on this information that we need now,

**Matt Yonkovit:**  
it's a really weird place to get it, right. I mean, exactly. All the places to get that that is not the one that I would have assumed you would get it on. Right, like so it would be kind of an all or nothing.

**Charly Batista:**  
That's true. So, this information here, just to get it from this information here, it rounds from pt-summary. Okay, pt-summary is working fine. Because this is the information that's supposed to go there. Right? Yeap. Right. So, okay, why did you try shooting? Why don't we have it here, let me move on. And as this is the very same information that PMM collects. So I use this to explain the idea, right? So I know nothing about your workload. I know literally not about your workload. But I can get a lot of information on your box from your server. And this is nothing related to Postgres at this page. Here. I'm not talking about Postgres. I am talking about the OS itself. Remember, in this case here, what are the things that are going I really would like to take a look at? So first of all, is the CPU okay? Why the CPUs that you have in your box, I see you have one physical CPU, four cores, and four virtual cores, so it's using hyperthreading, that's fine. And see here that you have different CPU speeds. It says that you have

**Charly Batista:**  
Have five CPUs working at this 2.49 Gigahertz, and then 309 Gigahertz. So what it means is you let your terminal decide the CPU speed of your box on the database server, we don't want that we always want the CPU to be running at the highest speed possible, which is in our case 300. Here, actually 3372. Now, this is the cache. Yeah, this is a 300 with hyperthreading and overclock. So we want the CPU to run as fast as possible. So we need to change. This is one thing that we need to change on the kernel parameters. We want to change it later. But let's keep the node we need to improve the CPU configuration so as to run it with the highest performance possible. Okay, the next thing that we're going to take a look at here is the memory. Okay, we have you have memory, you don't have swap allocated. This is usually not a good thing. 

**Matt Yonkovit:**  
You need to swap and it's not allocated then the OMM, starts killing things.

**Charly Batista:**  
Yeah. And the first thing that I'll probably kill is your Postgres. The Postgres is probably the one that's going to use the most memory. So what the kernel does, it looks out, okay, who is the guy that's using all the moment, the memory available? Oh, it's this Postgres. Kill it. Right, this is one thing that we really want to have is swap. Because it's better to have the database is slowing down for a few minutes. And we are able to troubleshoot the problem than have the kernel killing the database because it cannot slow down. This is the mindset is slow down your database, having time to fix the problems much better than having a Q dash nine on your database, and you can lose data, you can get the data inconsistency, a lot of problems out of that Q dash nine because this is what they care about the dash nine. So we need to allocate swap. And remember, we don't want the kernel to be using swap if it's not necessary. And to be able to do that this is the guy that we need to take a look the swappiness. What is this swappiness? The swappiness tells the kernel how likely it should use the swap. So in a desktop environment on my laptop, it's fine for a current swap because it makes things faster, actually, because my browser, for example, uses a lot of memory. So when I'm not using one of the tab of the browser, they can you can just put everything from the swap and let other applications to use that memory. Right. But we don't want that from the database. We only want kernel to swap on our database server. If we have a problem, that something really our case a lot of memory and prevents the colonel to kill the database. This is the only time that we want to use swap. Right. So we need to change the swappiness to one. No, yeah, you're allowed to use swap, but only when it's really, really necessary. So those are very important formation that we get from here. And in the end of this page, very important information. That's this the transparent huge pages.

**Matt Yonkovit:**  
And those are enabled by default, yeah,

**Charly Batista:**  
Is enabled by default on the Linux kernel. And for databases like Postgres, it's not a good thing. So what are why huge pages? Huge pages, it's a nice concept. Because remember, the memory is allocated and divided in pages inside of like for the kernel and also for the CPU. So every time that the CPU needs to access memory, the CPU doesn't read one byte, but as well as we might think, CPU, we read the whole page. So then the CPU will divide the whole memory we have into small pages. It was fine, until the point that we started to get a lot of memory available. So remember, the kernel works with something that we call virtual memory, right? The memory that we see, for example, let's do a ps. Yes. I just want to get I already had a lot of this guy, I just want to get whatever one guide here because they want to use lsof.

**Matt Yonkovit:**  
By the way, PMM is working with that PMM agent,

**Charly Batista:**  
Cool, nice. So when we do, we go here, we inspect things, we use tools like our source and our tools that we get the same memory addresses here. Actually, the address that we get from the memory here is not a real physical address. It's a translation that is done by the kernel. And this is what we call virtual memory. The free tool memory is memory that the kernel uses, the translation that Kernel does to make it possible, or the management better than memory. Let's put them this way. Because when you run an application, for example, when you run Postgres, the kernel will give postscript, the memory that Postgres needs. And PostGIS will believe it's the only application running on the kernel and has access to all the memory it needs. And this is the trick that kernel does to be able to work in this way it uses virtual memory. So the application doesn't really know how much physical memory we have on the box. But the kernel needs to translate that virtual memory inside of physical memory. So if we have one terabyte of memory, we can imagine how many blocks of all kilobytes this is full. Oh, for memory, the map of the memory address is going to be really huge, huge, insanely huge.

**Matt Yonkovit:**  
your system summary isn't updating because you're set to five-second refresh. So it's refreshing. Oh, okay. Because right now, the system's kind of bogged down. And so it's taking a while for the system summary to come back. And you can see a little spinning in the corner there.

**Charly Batista:**  
I'll change, I can change what that. That's a good one. That's a good tip, Matt.

**Matt Yonkovit:**  
Yeah, if you're, if your refresh rate is so fast, sometimes the data doesn't return. So yeah.

**Charly Batista:**  
And here on the top is where we change the refresh rate, that nice, we have here we have that. So the summary the huge page, they change the size of the memory page, from four kilobytes to a huge value. So we can have a huge block size of two megabytes, one, gigabytes, and so on. So then this memory map is not so huge, and the kernel can map the memory more efficiently, and mapping the memory more efficiently make things faster. So if it's made things faster, why are the transparent huge pages a bad thing. The first patent huge page, it's a bad thing, because it tries to make it automatic for the application. The application doesn't know that it happens. If the application doesn't know it, the application is not prepared to do things like that, it can cause a lot of page fragmentation, memory fragmentation. Remember, databases they usually work with are smaller and more basic, with more bytes inside of their memory cache, right? So if we have a lot of fragmentation, sometimes you have, let's say we have a huge memory. But instead of that huge memory, we have a lot of space. Like here, for example, let's say this is the page that I use. But this is something that I need for alignment. Well, in this example, here, I'm not using that much free, free page, right if I have here, but if I had like smaller pieces of bytes here, see that the space between one column and another column increases. This is what will happen with memory fragmentation when you are using transparent, huge pages.

**Matt Yonkovit:**  
And if you have memory fragmentation that's going to slow down the process.

**Charly Batista:**  
Not only slow down the process, but it can also cause memory problems. Because even though you have memory for some activities, exactly. So you might need for example, one gigabytes memory for one activity, and even though you have one gigabytes memory available, they split into small pieces like this one. You cannot allocate that one gigabytes memory. So the first thing that the kernel will try to do is swap. In our case, we have no swap, but the kernel going to do it is granted, it's running out of memory, it will just kill the database. So the transparent huge page can lead to performance issues, because you can have a lot of swap, because for the kernel, we just don't have memory, even though the memory is there, but the memory is not able to allocate. And in the extreme case, it can cause the om kill, they're gonna kill our database. So let's put it back. Let me open a text file here. So text editor, so what we have here so far, just looking at this, this information, just look up this information, we see the CPU is not running off high speed. So you need to make sure the CPU runs at it. Max speed. So we see that you don't have swap allocated. Right. Okay. No swap allocated, we see that your swappiness is pretty high. So swappiness is too high. Okay. And we see that you have transparently enabled each page. So those are four settings, from the last point of view that we definitely need to change.

**Matt Yonkovit:**  
Okay, so that's just the operating system. We haven't even touched the Postgres configuration. Yeah.

**Charly Batista:**  
And I have no idea about your workload.

**Matt Yonkovit:**  
So it doesn't matter what workload you're running, these four things are things that you want to make sure that you have set from an operating system perspective out of the gate.

**Charly Batista:**  
Exactly. So those are the four things that we definitely need to change to make our box healthier, right? Not all of them are going to make the database faster, but they're going to make the box healthier and more reliable. Because remember, you want your database to keep your data healthy and reliable. You don't want your database to forget about your data, right? You don't want to lose data. Right? That's not a good thing. That's a really bad thing. This is just looking at this information that we have here. Right we didn't even push anything we don't know about your thing. So how can we fix those things? So we have a couple of all those ones here. Let me just make some changes. We are using Ubuntu. Let's start with the transparent huge page. So to disable the transparent huge page we just run this command here will tell the kernel to never use the transparent huge page we don't want to use the transparent huge page. Okay, right. So the CPU Governor this is we want to tell the careful there's this guy that is the governor of the CPU that it's scaling the CPU so we can also have the CPU in high performance or we can save energy electricity is going down to the CPU we want our CPU for high performance. Alright, so for this swap, we need to create a file i Let me check here we don't have located but yeah we will create a file that's that I gonna go to do we can do later not for the swappiness we can tell the system CTL to change the swappiness of our box. So for swap allocation we need to do a DD to create a file and then allocate those guys. Let's run these ones to see we're out. Okay, remember you need to be root. Okay, seems you don't have this on. Ubuntu changed it. Okay, let's check CPU zero to see what we have let's just find

**Matt Yonkovit:**  
Did you want to grep the Governor? Is that what you wanted to do?

**Charly Batista:**  
Yeah, I want to find the file because it seems like it has a different name on your look to turn heads on. On Red Hat.

**Matt Yonkovit:**  
Yes.

**Charly Batista:**  
Let's let me do that abundance first and then Google for Okay, the swappiness is one now. Well, if the CPU is different, it might be as well. But no, we are in luck. And okay, so what I want to hello Google change CPU governor

**Matt Yonkovit:**  
Google has become self-aware.

**Charly Batista:**  
Yeah. Looks like it has its own utility okay.

**Matt Yonkovit:**  
And then there's just the CPU power frequency set.

**Charly Batista:**  
Yeah, exactly. Yep. Let me see if I already have this. We already have this utility here. Nope. And now you don't help us see you might find this utility that you look at on this toolset here. So this is what happens now. The tools are getting smart.

**Matt Yonkovit:**  
too smart. Step away from Skynet.

**Charly Batista:**  
It's sometimes worse. Right? Yeah. I hope we don't need Sarah Conor

**Matt Yonkovit:**  
yep. Because this is an AWS instance you're going to need Okay, yeah, you're going to need to install the AWS tools

**Charly Batista:**  
Okay. Oops apt!

**Matt Yonkovit:**  
Because yeah, I think yep.

**Charly Batista:**  
Okay, girl oh alright, buddy. Anything else you want me to do?

**Matt Yonkovit:**  
Well, keep in mind that the original apt get install command that you saw you didn't run here, right? So Oh,

**Charly Batista:**  
okay. Do you have a … Yes, because user space is not flawed. Oh, nice.

**Matt Yonkovit:**  
So this could be an AWS thing as well. They might not want you to set it, I don't know.

**Charly Batista:**  
It might let's go with the utility we might need. I  want to get Okay, it seems we need to create this guy. All right. And let's disable on-demand. This is the guy that tried to make things on-demand work. Like I said, we have mainly alternatives, we can run it as fast as we can, that is performance. Or we can run on power, save, and motivate. So the on-demand utility tries to find out how you're, you're using the box, and adjust on-demand, as the name says, so for the database, we don't need, you don't want to adjust on-demand, we always want it as fast as we can. Why? So it's without, with the best change for now, there are a lot of things that we can go on, we can go on, for example, for the IO, we can change the IO scheduler, and all these kinds of things that help optimize and improve performance. But now we want to go for the basic things, right, then the most basic things that we can find, and even for their scattered just to make sure that we understand. So the system summary also shows us here somewhere, probably on top. So we have a file system, it is also going to show us what the IO scheduler is, we don't have here if it's able to grab the information. I was not able to find it here. So it's using Amazon, the device the speed. Yeah, it was unable to collect rate information. And I can't find that it was not able to collect the IO scheduler. So in some kernels, it's able to collect the IO scheduler. So the scheduler works. They'll understand the IO subsystem, how it wants to write and read things, it's a bit more to what we're looking for today, we're not going so deep. Today, we're just going for the surface, right, the basic information. And those are the things that we already got for here. So only do those things, we make our box more reliable, right, and we might get a bit of performance improvement. But the idea, the first idea is reliability, so our box is more reliable. So now that I get more reliable, I want to start looking at Postgres and not for the first time, I don't want to care too much about the workload that we have, right, I just want to check the summary of my database. And just see from those four or five that we want, we can do it. And the first one that I like to take a look at is on the shared buffers, which is the full value for the shared buffers. They're huge. They're really small. Remember, it was defined when memory was expensive, and his cars, now we have a lot more memory. So in our example, your default value for the shared buffers is under 28 megabytes. So what is a good value for the shared buffer? Do you know what would be a good value for the shared buffer?

**Matt Yonkovit:**  
50% to 70% of your memory?

**Charly Batista:**  
Why?

**Matt Yonkovit:**  
Because you know that that will give you the ability to grow? I mean, typically you want your hot data all in shared memory, right?

**Charly Batista:**  
Well, that's true. And what is hot data, by the way,

**Matt Yonkovit:**  
Data that's accessed at a high frequency.

**Charly Batista:**  
Right? It might be stupid questions, but those are the definitions that you need to make before we start moving. Right. So yeah, we want our hot data that is frequently accessed and maybe change it in memory. And you said 50 to 75%, right? Yes, that's usually good for database systems, for example, MySQL, would be a really good approach. But by the full-on Postgres, we don't want to be the high because Postgres doesn't, even though Postgres has the shared buffer, it works more like catch from the OS. It relies a lot on the OS buffers. Not like MySQL, MySQL and other databases. It does what we call direct IO. So it just bypasses the kernel buffer, the left buffer, goes direct to the disk, gets all the data it needs and manages inside its own buffer. So, right, so it manages its own buffer and goes directly to this, the Postgres doesn't do that. Postgres relies on IO on the kernel. So we still have a lot of data inside of the kernel buffers. If we set the Postgres buffers too high, then we have a smaller buffer for the IO operations from the kernel perspective. And it might make your workload slow. Especially if you have a really intensive workload. If a write intensive workload, he might want to get your shirt buffer much smaller, like around 5% of memory that you have, because most of the things are going to go for the kernel buffer. And the kernel just decides when it wants to flush from front it's buffer to the disk. Right. Right. But you still Yeah, we still need to improve. I want you to give me this webpage here. That helps us with some settings. It's a really nice PG Tune webpage, right? It will show us some base configuration. But besides this, we need to understand why it's given the settings. So the database I'm using is 13. And using Linux for let's say, I'm using more web applications. We have 32 gigabytes, Max RAM, eight CPU cores, and how many connections Max we were sending?

**Matt Yonkovit:**  
Well, how many do we want right now? There's like 20 running, but we can go 50 100? So

**Charly Batista:**  
oh, let's put 150. Right. So I want to start the database. So okay, it will give some numbers here for us. Well, the first one is the max for action. So this is the number we gave to them. So it's not here. And the first one that pops up in my eyes is this shared buffer. That is exactly what we're talking about here. Okay. See, it gave eight gigabytes RAM for our case. So it's far less than 50%. Right? Indeed. And then the reason is exactly the one that I just explained to you. So in a web application on all app transactions, most of the operations that we have are mixed operations. We don't. It's not only a very write intensive operation, we also have a lot of reads. So from the reads, If we have the data closer to the database, which is on the database, shared buffers, it's much faster 

**Charly Batista:**  
The database can use that in a very fast way. And we don't compromise too much the OS cache. But keep in mind, those are the suggestions. It's by row means strict values. Those are suggestions that we can use. So we can start with eight gigabytes. So let's put this value here. So for our configuration, let's start with eight gigabytes, that's fine. On that pops up here is this effective cache size, you know what it does? And it says 24 gigabytes, it's quite high. It's not?

**Matt Yonkovit:**  
is it the file system cache? Estimate, cache that's available?

**Charly Batista:**  
Actually, it's, it's an estimation, correct that it's an estimation, but it's an estimation of how much memory in total the database can use

**Matt Yonkovit:**  
Yeah. So it's the shared buffers plus what's available for filesystem cache? Without what's left for the OS and anything else that's running.

**Charly Batista:**  
Exactly. And why is it important?

**Matt Yonkovit:**  
So you don't over-allocate.

**Charly Batista:**  
Why, but you will never over-allocate if you put a hard value of eight gigabytes memory here. This, we need to keep in mind, this value here

**Matt Yonkovit:**  
isn't true, because each connection is going to have its own memory as well.

**Charly Batista:**  
I agree. I agree. And so if each memory has its own connection, it's not so true for each connection. So yeah, you cannot really put a hard limit, right? Yeah. So that's not the case, it's not the point, this value here, it does nothing about memory allocation. It doesn't allocate anything. And it doesn't put any hard limit for memory allocation. This is a guidance for the optimizer to understand how much memory it can have. And if it's better to go with indexes or not indexes, if it's better to, to go do a full table scan. And if it's likely to get the data in memory or not, is just a guide for optimizing. Why did it change it might change is the optimized plan when you run your query, but it does not allocate

**Matt Yonkovit:**  
It doesn't make any modifications or anything else? No, nothing.

**Charly Batista:**  
And this is just for guidance on when you go for the optimizer. Right? So for the other side, the famous work mem, it does allocate memory. And what it does, so remember, we have a lot of operations that we do on Postgres, for example, the vacuum, or when we create an index, or we do some operations, maintenance operations. That's why as a maintenance work mem, right, so for those maintenance operations, we need to allocate memory. And this is the memory that will be allocated, it doesn't make your queries run faster. It makes your maintenance operations run faster, or slower, depending on the configuration. Right. So this is what it does. Right? So I'm gonna, oh, let's go. Yeah, I was about to skip this one. But let's go here. Because for now, I don't want to care about the checkpoints that are the target. Ah, I go to one thing that is usually not commonly talked about during the optimizations and running sessions is this guy here. And it can make a lot of difference from the queries and optimization. And I mean, the optimizer when I run inquiries, this is the random page cost. Do you know what it does?

**Matt Yonkovit:**  
I mean, it's just the cost optimizer change. Right? So it's going to push random pages to be a bit more costly. So it's going to favor some sequential right?

**Charly Batista:**  
Yeah, but why?

**Matt Yonkovit:**  
Because sequential reads are going to be faster for most discs and most systems?

**Charly Batista:**  
That's correct. But what does it have to do with the database?

**Matt Yonkovit:**  
Well, that means like I mentioned, it's the optimizer side.

**Charly Batista:**  
Yeah. But like, what is the result? Let's say what happens if I change this value to four? For example, that's if I'm not wrong is that the fool is for let's check our configuration. Here it is see

**Matt Yonkovit:**  
all random pages, you're going to get better with indexes or certain types of indexes. Okay, because you're going to do a deep dive into the index, right?

**Charly Batista:**  
That's correct. That's correct. So, yeah, the default is four. So to be able to really fully understand this setting here, we need to understand how Postgres stores data, and how Postgres stores the indexes. Right? So the Postgres it stores data, or the data files, it's just sequential data, it's stored. Right? So it doesn't work like MySQL, for example. It stores data, organize it based on a key on the MySQL primary key.

**Matt Yonkovit:**  
Right? So it's a clustered index that's basically used in MySQL.

**Charly Batista:**  
Yes, exactly. So it doesn't use cluster storage here. Right? So it's, this is the thing. The data that is stored on Postgres is not a cluster, it doesn't organize the data. So it just keeps right. And the data is just like we're doing here, on this file. 

**Matt Yonkovit:**  
So, it continually depends and that's why you go back and clean up old data, because there are spaces, that's what the vacuum does for you.

**Charly Batista:**  
Yes, and why do we have spaces? Like, for example, let's, let's put here, they have just put some random thing here data 02 data 03 , and data 05, right? So I have here data, I have 15 lines, right? And why? Let's say, let's imagine this is the data file for the customers, why? It creates empty spaces here, as we just described,

**Matt Yonkovit:**  
because it's faster to bark at for deletion, then come back later and clean it up.

**Charly Batista:**  
Exactly. For example, if let's say I want to update data 02 to data 20. So what Postgres does is, let's put its mark here, as deleted, right? So copy this guy, and then it's 20. But I still don't have an empty space here. Why? No, it's marked for deletion. And as you mentioned, we have the process that is the vacuum. In the case, outer vacuum, it will come here. I just vacuumed this table. That one was marked for deletion. It's now deleted, this line is now empty. Right? So but remember, the database reads everything in blocks in case of  Postgres, it reads all if I'm not mistaken. 16 kilobytes blocks. But let's say we have four lines. So I have 1234. So I have 12345 blocks, right? So on the last block, I have three lines, they're empty, it's all empty space. And they have one empty space here on block one. Right. So this is what happens with the vacuum. So on Postgres, every time that we do a select, it does a full table scan. What it does is it goes to the disk, reads all the blocks, puts in memory, it's pretty fast. Or if I do select, let's say I want the data live, right. It will scan all my table if block one there is no beta five block 02 there is no data five hops on what, three, I have data five, but it doesn't reach the whole block with the memory and keep going It's It's sequential, as you said, it's a sequential, sequential. And when it goes for an index, what it does, it creates a B tree index and most of the time, so when we create an index, like, for example, a B tree, it's not sequential anymore. Right? We have a random page. So we might have a 135976, whatever how the pages are organized. And so if I select and try to find the data five, and the data file is on line 13, let's say it's here, it goes to the B tree, it finds the line where it is randomly, remember, it's not sequential anymore. It's random reads, yes, find the line, then go sequentially for the line 13. And I read all my pages, so I'm changing sequential access to a random access. Whenever I use an index on Postgres, right.

**Matt Yonkovit:**  
Which means that in this case, random page cause, like we, like we mentioned, is going to improve the index in the usage is because it will prefer indexes, which changes the cost optimizer to prefer random pages or Index Scans over sequential

**Charly Batista:**  
Exactly. And this can change a lot and can improve or decrease performance a lot, right? Because we can just go for a select. Let's get to your database, do you have a nice selection that you can send to me? That they can run your database? Oh, yeah, I do. Okay, let's go. You have my square analytics? Yeah, I still don't. Yes. To wonder

**Matt Yonkovit:**  
That's really strange. plating errors. I don't know what's going on there. Unless there's an update that I didn't apply, which I guess.

**Charly Batista:**  
Yeah, I can always have.

**Matt Yonkovit:**  
I've never seen those before.

**Charly Batista:**  
So I'm going for this one. Right, so let's see the query distribution. It's not giving

**Matt Yonkovit:**  
Yeah, that you can, if you look at the query itself, you can take the thing and it should be fairly easy to reconstruct it. It just looks at the whole query. Like the what's the Yeah.

**Charly Batista:**  
Yeah, this is what I'm trying to do. Yeah. I need to buy a new mouse.

**Matt Yonkovit:**  
Yeah. Then you could just take the, there's only one value, so just pick a value like 1000 or something. For the parameter, and that should be fine.

**Charly Batista:**  
Oh, I can just put,

**Matt Yonkovit:**  
Yeah, that should be Yeah.

**Charly Batista:**  
Okay. So what do you want to do here is, let's run and explain where my database is. I suppose I'm connected here. I am using the testing efforts. Let's connect here. I need to copy my query again. So I want to explain. First, let's start to explain. Right. To them. Paste here. Paste it twice. No, it's fine. It's once. Yeah, so I have my next my explain here. So if we go here, it's doing a bitmap index scan and doing a hips, bitmap heap scan. Okay. We have those. Those guys here. We're still using indexes. Right? So let's understand. Where's the table? This is the table let oops the opposite. Let's see how your table is organized. So, on your table, you have the primary key, that's a B tree. And you also have the comment. That's another B tree. Cool. And what's your credit doing?

**Matt Yonkovit:**  
It is searching for one ai_myid. Yeah. Which is that second index that you had?

**Charly Batista:**  
So, I suppose the size of this table, let's just select

**Matt Yonkovit:**  
you misspelled count. It's always hard to have someone looking over your shoulders.

**Charly Batista:**  
No, actually, my keyboard See, sometimes it does work. And sometimes it is mistyped, and sometimes it types twice. Well, I bought a mechanical one that was quite expensive thinking that would be a good fit, but looks like it's not working at all. And just one runs in problem after the warranty expired. So yeah, you know how things work? Yeah.

**Matt Yonkovit:**  
So I see that you just joined. We haven't really got dug into monitoring, we did set up PMM. Early on just a quick setup, but we can cover the installation, a PMM if you want at another stream, but right now we're kind of bouncing between PMM and the shell here for everything. Yep. But we can definitely do some help and show you some ways to get PMM up and running in your environment. We might not be able to do it today. But we can get it done. Yeah, yep.

**Charly Batista:**  
So just to understand that parameter here. As we see here, this thing is quite large. Right. So we have a few $2 million. A million. Yeah, we have 2 million rows here. So that's fine. And in this case, look that we're only looking for one very specific ID, right, we're ready for one very specific ID we probably don't like. How many? Let's see how many rows it returns so all eight rows. Well, the worst case scenario that may happen is each of these rows here be in one single page inside of the database. So then it needs to go to the index, find all the pages and then go to the data file and randomly select those five pages right. It's not as it's not a bad because likewise the table name. So if we have here select oid... just doing max(oid).

**Matt Yonkovit:**  
Did you want my column the ai_myid

**Charly Batista:**  
And now I want the  ct_id I suppose Oh, yeah. Yeah, this is the one.

So what you have here, this is the page number. See this table here it has 49,713 pages inside of the data file. This is how many pages we have inside of this data file. And as I said, as you're getting eight rows from the index, worst case scenario, we need to find eight pages because each row is on a different page. Right? So 8 pages out of 39,000 pages. That's all bad, right? So we had a really huge performance gain. If we go for the index in this case, find out what's the information and then we come back to the data file. Because we are avoiding reaching 49,700 pages, first keeping them or using your index. That's why the database chooses to use your index because it's a lot better to go for the index and then come back to the data files. Because the cost is a lot more efficient. The thing is, we can make it look a lot worse. If we change it around on page costs, let's say we put up a 5000 for the random page cost. It will probably be a website probably from the database side, we'd say, man, it's so expensive, it's so expensive to do a random page that I prefer to go through the whole dataset, do a full table scan, and just get those five different pages here and do random pages.

**Matt Yonkovit:**  
Right. So this is why you want to make sure you get that one. Right.

**Charly Batista:**  
Exactly. Exactly. And to be able to get it right, you need to understand what kind of disks you have. In this case, as we are using AWS, we suppose you have SSDs and NVMe. And all this kind of stuff. Right? We have it really fast. So and that's why we put it here, the cost for the random page is almost the cost of the sequential page, which is why the change is not so high. So yeah, the database can favour a lot more going to the indexes than doing a full table scan.

**Matt Yonkovit:**  
Okay, so Charly, so what we've got so far is we've got several changes that you recommended for the iOS. Yep, you recommend changing the shared buffers to eight gigs. Which, we talked about, we mentioned, the effective cache, we could change but it's not going to really make a material difference other than on the optimizer slightly. So that's an option. The random page cost is one that we think could be a big win for us, just because the default is so high compared to sequential. Lowering that by default is probably a good thing.

**Charly Batista:**  
Yep. That's correct.

**Matt Yonkovit:**  
Okay, so given that, what other basic kind of changes would you recommend?

**Charly Batista:**  
Okay, let's just get some overview here. Remember that I saw a lot of IO. What was that? It topples. You're writing a lot of topples. Yep. Down here on the mode summary, right? We saw a lot of IO here, right? This activity. So one thing that we can change on Postgres is the synchronous commit. Okay. So, but remember, there is a trade off. So the synchronous commit will force the database to commit every time to the cache, to the kernel, every time that you do a commit or transaction, right is a trade off that we can improve performance. But you lose a little bit on reliability. So you might have for example, one second data loss depends on your configuration. So and but there's one thing that I really always discuss when we're talking about those trade-offs, because there is one setting on Postgres. I want to show the settings here. And I want to tell you never, ever change this guy.

**Matt Yonkovit:**  
The fsync never changed the fsync.

**Charly Batista:**  
Exactly. So did the full five syncs. So if you see it's just on top of the synchronous commit, right? Because they're highly related. So the synchronous commit, it's the level on how long the database will wait, all the data to be persisted in the disk. So say that we have 1234 I values here, right? We have synchronous commit off, so it doesn't wait for the kernel to reply back if it was successful or not, when you do the commit, right? So it what it does it, you, let's say you do insert in that table. So when you finish the insert, you do the commit, it will immediately come back to you. It doesn't matter if the kernel was able to write or not to the disk, the database doesn't care, you just want performance, right? So you have the local option, the local and the own option, they're mainly the same. So what it does is when you do the commit, it will ask the kernel and write this down, flush it to the disk. So they do not flush the disk to write to the kernel. And we wait back to the kernel to see if the kernel replies back with success or failure. So if the kernel replied back now, yeah, it's on the disk, then the database is fine for Yeah, yeah. It's on the disk. It's, we're good to go. So reply back to the application. The remote if you really want your data to be persisted, and you have a replication, you can tell to the Postgres look, every time that I call me, it's something I want you to send to the replication and wait for the replication to also commit to have this local one. So then reply back

**Matt Yonkovit:**  
To consistency between your replica and Your primary?

**Charly Batista:**  
 Yeah, yeah. So it guarantees that the replica, written to its buffer, is right. It didn't apply yet.

**Matt Yonkovit:**  
Which is the next step, which is remote, apply

**Charly Batista:**  
The next one. So the next one is a remote application. So it will send to the replica, wait for the replica to apply the commit and reply back. So as you can imagine, this is the slowest one, but it gives the highest level of guarantees that you have that data safely.

**Matt Yonkovit:**  
But right now, we don't have a replica.

**Charly Batista:**  
No, so we can. No, no, we can later on. Maybe not today, but in the next call. We can just read off and see how much impact we have. Right for the synchronous commit?

**Matt Yonkovit:**  
We'll probably want to set up replicas eventually. So if we go through and our goal for those who are watching or listening as we want to kind of walk through all the different stages. So we'll we'll show backups one time we'll show Tuning, so we're going to kind of roll through

**Matt Yonkovit:**  
Through different topics in the Postgres space here, with the same setup. So we're gonna save these instances in the next stream, we'll continue on this journey of figuring out, we need to configure.

**Charly Batista:**  
Exactly, exactly. And coming back, remember that I'd said to the Fsync, never ever touch this guy. So the Fsync instructs the kernel to flush the data to the disk. So it makes sure that when the kernel replies back the data, when the kernel flushes the data, it does safely flush the data. So if you disable the Fsync, you might have some performance, you're gonna have some performance benefits. And it might have the same performance benefits with the synchronous commit. The thing is, now your writes to the disk are not safe. And it's not atomic enough. When you write to the disk, you can have disk corruption. 

**Matt Yonkovit:**  
And it's really based on the disk having its own cache and its own systems going on and you're, you're basically relying on it to do everything for you, instead of forcing that right to be consistent.

**Charly Batista:**  
So, it's fine to, to work and tune and play around the synchronous commit, we can have like, it's good, but it's the to the Fsync configurations on all and I always enforced this, because I've seen a lot of tutorials and recommendations on the internet, well, just disabled Fsync, and then you want to have a lot of offense privilege. That's very silly, to say the least, how much you can lose your data. If you don't care about your role. That's true. So that will be done, which is available, right? You can have just everything in memory. But for Redis. I'm not saying that Redis, a bad 2x is an amazing two, is just a memory database. Right? So you don't care about all the safety of your data.

**Matt Yonkovit:**  
Yeah. So he wants to know, what about ZFS as it can eliminate bitrot and disk corruption issues?

**Charly Batista:**  
Well, I haven't played around with those things. So I cannot comment on them.

**Matt Yonkovit:**  
Reading, you might be able to get to talk to that. 

**Charly Batista:**  
We do. Yeah, I read. I've been reading a lot. tops on ZFS. And order a consistent file system, you know. But there's always a trade-off, right, always have a trade-off. And for the database, we usually trade performance to get reliability and consistency. Right. And this, but this is a long in huge fight between the trade-off of reliability, consistency, and performance. Right. But this is definitely a good topic. Another topic that probably we will step on later sooner or later is about encryption. How do we do encryption on a database? So how can we go for that? Because it's a pretty hot topic nowadays.

**Matt Yonkovit:**  
Charlie, you're jumping all over? Right? We get to that yet. But we might be able to want to ask him that question. So we have a kind of a resident ZFS expert, and he loves ZFS, and he just wants to play with it. So we could probably ask him his opinion. Specifically, you know it for Postgres. But he's written a couple blogs that are interesting, in case you want to check out ZFS on the Percona blog.

**Charly Batista:**  
Oh, cool. So remember that everything that we did here is independent from your workload, right? Even though we check in a couple of graphs here to see how the database is behaving, because we want to have a way to compare the before and after. So the good thing is we're using PMM and we can just go back in time, right? So we can compare. But at the moment, everything that we did here, they are independent from your workload, right. But they are good practice and recommendations. So again, there are no strict rules that you should, if you have 32 gigabytes of memory, use eight gigabytes worth of shared buffer. That's not such a thing, right, you need to understand your database off. That's the one that likes the recommendations we are using. After we do all of those things. We need to come back again, run the load test again, and then define tiling on top of those, those very same parameters. Because we can't, we can get worse performance instead of better performance.

**Matt Yonkovit:**  
Yeah. But I remember how I mentioned at the beginning of this that the heatings getting fixed and the guy's knocking on my door right now. So I'm trying to get my daughter to go let him in. which is always fun. But no. So let me go ahead and do that. And if you can maybe talk a little bit about the wall in any of the default settings, is the wall changing the Wall Settings, something that you would wait till you have more workload or would you do that out of the gate before you have really looked at workload?

**Charly Batista:**  
Oh, I usually like to have more, more workloads when going for Wall Settings. Okay, to understand a bit more,

**Matt Yonkovit:**  
So there's different things here, right. So the ones that you've recommended are pretty generic. And without the workload let's look at these things. So we've mentioned half a dozen settings for Postgres and the OLS. Those ones are all Hey, regardless of what workload, you should look at changing those, but wall and a few of the others, you're going to look at what are those, the workload before you change it?

**Charly Batista:**  
Yeah. One thing that I like to pinpoint here, let me see if we were collected here. So the checkpoints, right. So every time that we went to look for wall configurations, one thing that we really want to improve and optimize is the checkpoint, okay? We don't want to have checkpoints happening too frequently. But we don't want them to be too sparse either. Because if we have a checkpoint that is very sparse, if the database crashes, when it recovers, it can take longer to recover back, right? So it's, again, the trade-offs that we have here. But if you have the checkpoint happening too frequently, we're going to have a lot of IO and the database performance will suffer a lot, right, but they're dependent on the workload, they're highly dependent on the workload. But looking here, from the graph that you have, can you see that from? Let me get here instead of five minutes or 30 minutes? And you said that at some point, didn't it refresh? There we go. Okay. Okay, this is a better view than using proof. Can you see that at some point here, we have a lot more checkpoints happening and taking longer than from other points. So here, if we take a look at the problem, your application is writing more intensively during those times here. That's why we have a lot more checkpoints. And on this point, here, we probably had your application still writing, but they are not writing so much at the very same point. So then we are probably reaching the checkpoint timeout. Right. Right. So those are usually the things that we need to take a look at. So are the checkpoints happening too frequently? What is the frequency of the checkpoints every one minutes? or seconds? Or every 10 minutes every one hour? So are they happening too frequently? Because what we want to have is we want the checkpoint to happen at the checkpoint, timeout. Right? We want the timeout to be the time space that allows the application to evenly distribute the load of the data, okay. Because what happens is when I write into the database, it has a background, tranche or process that's working with the OS that is flushing the data to the OS, right. So if the checkpoint configuration is too minimalist, that guy is not able to keep up pushing during the time and then eventually, we'll get the trash hold. And then we have a huge flush, it's flushing too much. Right. These is the checkpoints and we want the database to just keep flushing slowly but at a nice pace, so that it doesn't need to be washed too frequently and when it flushes We don't see those high peaks. Those high peaks are not good either. Let's go for 15 minutes here. So those high peaks meant that the curve was not able to keep working. And eventually, when it pushed it a lot, it needed to do a lot of operations per second. So we want it to be as parsed. And as even as parsed as possible. So the database is just flashing, keep sending data to do ask, it's sending data to ask. And it can bounce faster. So I think we can leave it running for some time, and then we can come back. Okay, for most comparisons.

**Matt Yonkovit:**  
So what I'm thinking, Charlie is we're we're at an hour and a half now. So we should probably wrap this stream up. And what I'd like to do for the next stream is take the changes that you've recommended, and actually apply them. And as you look at the before and after, right, I think that's critical, because we've got things running. So what we'll do in preparation for the next live stream is we will start our workload a couple hours before the stream, let it run, we'll make the changes, restart the database during the stream, and then we'll watch and look at the deltas.

**Charly Batista:**  
That sounds great. And why do we look at the deltas, and then we can also go for the other parameters, right, like the checkpoints and the wall files, and

**Matt Yonkovit:**  
We'll have a workload and you can analyze the workload a bit more.

**Charly Batista:**  
Exactly. That will be a lot more useful.

**Matt Yonkovit:**  
And for those who are watching, appreciate you hanging out here. For those who are watching. Recorded, you might have missed it. We had a snafu with the configuration today, where we actually duplicated our streams. And so there was one string that was active, one string that wasn't. And so we need to figure that one out. So this is something that we apologize for, we also didn't stream to LinkedIn, even though we wanted to, because I don't know if this was a change setting or what, but I got an error that only a certain frames per second was supported by LinkedIn streaming. Now, I streamed LinkedIn two weeks ago, no problem with the same setup. So something has changed between two weeks ago, and today, where what I did stream didn't work anymore. So gotta figure that one out. That one's a little weird. So we'll come back. And we're going to continue to try and do these on a regular basis. we have a request to do a PMM installation from the start to the end so we'll go ahead and we'll get that set up as well. As well as continuing with MySQL, Postgres, Mongo streams that will show you how to install and configure what's important out of the box. And then we'll go through normal operations, like setting up replication or doing a backup, or doing something else. So Alright, sounds great. All right, Charlie, thank you for hanging out. And don't forget to subscribe to the channel. So you'll get notified when these things happen again. So thanks for hanging out everybody. Bye. Bye.

**Charly Batista:**  
Oh, thanks much for having me here. Thanks, everybody. Have a great day.