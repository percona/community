---
title: Observing & Tuning Your MySQL Workload Using PMM - Percona Community MySQL
  Live Stream & Chat - April, 29th
description: Increase the performance of your database with our experts. Matt and
  Marcos will show how to optimize and tune your database workload using Percona Monitoring
  and Management on April, 29th at 9:00 AM EDT  / 03:00 PM CEST/ 06:30 PM IST
images:
- events/streams-mysql/04-29-2022-stream-mysql.jpg
draft: false
date: '2022-04-29'
speakers:
- marcos_albe
- matt_yonkovit
tags: ["MySQL", "Stream"]
events_year: ["2022"]
events_tag: ["MySQL"]
events_category: ["Speaking"]
---
Percona Community live stream for MySQL is a biweekly events with Matt Yonkovit and Marcos Albe. This is the recording for the session of April, 29th. We have talked about Observing & Tuning Your MySQL Workload Using PMM (Percona Monitoring and Management). Follow us on [Twitter](https://twitter.com/PerconaBytes) and stay tuned to all upcoming Percona events.

## Video

{{% youtube youtube_id="4ccEZZtjqWg" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
We're live and you're singing… Marcos was here, you know, singing the song of folks on the PT stock song. Yes, he was singing the PT stock song. 

**Marcos Albe:**
I didn't know there was a blondie song.

**Matt Yonkovit:**  
Which one that it's barracuda?

**Marcos Albe:**
No, no, no, no me or no, I'm gonna find you. How's the name of that song?

**Matt Yonkovit:**  
Yeah, I know, I know what you're saying.

**Marcos Albe:**
I can't remember the name. But you know, it basically describes Stoker. 

**Matt Yonkovit:**  
Okay, well, thank you for that. Hello, everyone.

**Marcos Albe:**
If someone gets your song for you.

**Matt Yonkovit:**  
Hello, everyone. Welcome to our regular live stream. This is actually only our second with Marcos, Marcos, you have fallen behind Mr. chino. He's like

**Marcos Albe:**
I was wanting, suddenly seek and chinos always fostered by myself. So Well, the problem is in a rush, yeah,

**Matt Yonkovit:**  
Oh, look. So someone says no video for LinkedIn. Which is not great. So one second. So it's sort of why LinkedIn sometimes causes some weirdness with streams. So I'm gonna go ahead and just jump over to LinkedIn real quick while we're chatting. And I will pop in a link to YouTube, for the folks over there. So hopefully, they're seeing it, they might need to reload their LinkedIn as well. We have like 14 people hanging out there. So some people are saying no video, which is weird, but that's the YouTube link if if people are there, I'm seeing us on LinkedIn. Which is, which is weird. So I just popped into there, and it is working. But yeah, so So Charlie says it's working for him. So Charlie showed up. So the good news is, we're on like week three of backups with Charlie. So if you hurry up, and you can get the backups working quicker than Charlie, we might be able to beat him and catch up. So this is going to be a race between you and Tino. Just I can

**Marcos Albe:**
Do that. I can do that and explain it to you. So I'm making key mounts.

**Matt Yonkovit:**  
Oh, and I will Yeah, yeah. So we'll do two. Next week, we'll do two we'll do a MySQL on the morning to catch you up. And then we'll do one in the afternoon with Chino. I'm still going to be doing backups. Like we're going to do PG backrest next time. So definitely something to look forward to. But today we are here to do a couple of things. Number one, we are going to be installing PMM. And so for those of you who have never installed PMM before Marcos is going to walk us through it typically already have PMM installed. Still, because I have it on an Ubuntu machine, Marcos typically is like oh and boon to I don't like him due to you know, Charlie, it is not my fault. Okay, it is your fault, Charlie, your fault. It's always Chino’s fault. Like I have a sign that says that. Where is that sign? I have it around here somewhere. It actually says, Look at this. So I had to make this for the last Livestream. 
It's Charlie's fault. See? It's Charlie's. Oh my god. Yeah.

**Marcos Albe:**
I hope you don't make one of those for me. Yeah. Lance, it says Marco speaks. Oh, okay,

**Matt Yonkovit:**  
We can have a, I think I'll make some T-shirts. And if you're at Percona Live in a couple of weeks, maybe I'll have it's Charlie's fault, but Marcos will fix it. I love it. Anyways, alright, so we're gonna install PMM. Today. Marcus doesn't like Ubuntu. So I got him to do rocky Linux, which means he has to set it all up from scratch because I don't have it already pre-set up for him. Which is cool, because we probably want to see how to install PMM anyways. And what we'll be doing then is connecting it to the box that Marcos had set up on our last live stream, the installation in the setup there. And I'm going to start doing some workload on those boxes using my own toolkit. And then we're going to tune that workload. And so Marcos has the base configuration from last time, then we're going to get PMM installed so we can look what's going on. I'm going to add a ton of workload. And then we're going to see what Marcos looks, looks at to do tweaks to tweak it towards the workload that's running And that's it. That's what we're doing today. So hopefully, that's all interesting to you all out in stream land. You know, and, you know, I think that's it. So Marcos, you want to sing a song before we go, you know, we started this, and you were singing?

**Marcos Albe:**
Oh, no, no, to say for that, I, but I will certainly explain to you once. 

**Matt Yonkovit:**  
Okay, so share your screen. Yes, why not? Why not share that screen and we will get started feel free to ask questions. I'll be paying attention to the chat. I'm probably going to move this way because I have my shell over here. And I was a very bad person. Last night, I was watching the NFL draft and didn't get the app server working on against your, your box. So I need to configure that now. So I'm, I'm here, but I'm actually getting the, you know, some of the components here working so. So Marcos should go for it.

**Marcos Albe:**
Yeah, I'm on it. I just would love to get out of the screen, which I accidentally insert. How do you do that? Normally, okay. I'll just kill it and get another session. That's easier. 

**Matt Yonkovit:**  
It's not a boot because you clicked on the Ubuntu one.

**Marcos Albe:**
That's my because you know, there is no red hat.

**Matt Yonkovit:**  
No, oh, well.

**Marcos Albe:**
So let me get there one more time. Okay, so basically PMM has two components. The main one is the server that will provide us with a web interface, and it will centralize all the agents and then we will install the agent on each of our nodes. So my favorite way to install PMM is by using Docker, you could also use a Amazon, or virtual appliance, but even when we are in Amazon, I prefer so first you create that data container. So the data container allows us always to keep our data in place and then upgrade the server container without touching the data. 

**Matt Yonkovit:**  
As somebody said that, they're getting low video quality. That's interesting because we are officially streaming according to Restream at 1080 p. Which is interesting. So I don't know what's going on there. That's weird. Yes. That is weird. That is very strange. Yeah, so I just doubled you can make one. That's okay. I can make this larger. Yeah, hopefully people can still catch the video resolution there. Yeah, so Charlie's getting 10 ATP. So it must be something local on a couple people's clients. Charlie, I'm glad you're here to fix it. I take back 92% of everything I said about you.

**Marcos Albe:**
Alright, so that got my data container installed. Now I'm gonna install the server itself. I'm gonna say volumes and gonna use the previous container I created. And I'm just gonna name it demon server. And here's the image Percona PMM server with a tag of version two. So it's gonna get the new latest two point something version. And we are there you go. And then we can do Docker lips. You do and it's the app starting, let's wait for it to start to ensure everything is healthy. Good. So we have a healthy server that is always good. I'm going to find the IP database of this guy, I will need it later. So here we are. And I map it ports. So 443 From my container, it's going to be 443 on the world on the outer world, and 80 as well. So I should be able to reach those through this IP address. And then to my MySQL. First, I'm going to create a user for the PMM.
And it's going to be identified with a super secret password. And I just limit the number of connections it can create. So in case anything goes wrong, it's not gonna you know, deplete our connections, so, and then I'm gonna grant a few basic rights necessary for operations. That's that, and then I'm gonna make sure I already have my Percona release setup. Percona release is our repositories plus tool. I'm just going to make sure it's up to date. Great, that's good. And I'm gonna solve GIMP, two clients.

**Matt Yonkovit:**  
Awesome. By the way, we've got a lot of, hey, hey, hi. Hey. So hey, everyone. It's Dreamland, thanks for hanging out. And checking us checking out what we're doing. By the way. Good news, everyone, the workload is officially running on the box. So we will have something for Marcos to tune in a second.

**Marcos Albe:**
Thanks. I like that.

**Matt Yonkovit:**  
Although I was getting some issues with the long-running transactions that I tried to introduce to the system, so that might be something I need to do bug. So I just turned it off while I was running.

**Marcos Albe:**
Right, so I have my clients. Gonna configure the instance with the server. So I am using the server IP address here. And I'm not going to check. I'm not going to be checking for TLS. So it's using SSL, but not verifying the certificates. Now I'm going to my SQL Server, so this register the node with the server, the first command PMM admin config will register the node with the server, and it's gonna set up the Linux monitoring, and then I am going to my sequel service. 

**Matt Yonkovit:**  
And I don't know, did we configure the slow query log, the last time we were here to collect the appropriate amount of data for this?

**Marcos Albe:**
I'm not sure. But I have my settings handy. And I will make sure they are in place at the moment, because

**Matt Yonkovit:**  
one of the things just for people out there who are watching, you'll want to make sure that you have the slow query log setup properly. Otherwise, you won't get any quant data, unless you decide to use the performance schema as opposed to the slow log. So you have two options, right? So you can perform.

**Marcos Albe:**
Quiz question for you.  Why don't you want to use the performance? You know? Or why would you rather use this local?

**Matt Yonkovit:**  
Well, so in the current version, we actually have a bit more data in the slow log, right. And we're going to have the capability to store more of it.

**Marcos Albe:**
Well, to think I started this low look for two reasons. One is you can rate limits, and you know, reduce the impact while still having access to some blood analysis for years. Look, where is he? And the other one is lock, row lock. Time is not accounted for in performance schema chunk. So that's that's, that's sometimes it's quite important. And I prefer to have the full picture with row lock times rather than not have it. So yeah. This is why I prefer to slow load. You can always use the performance schema it's better than not using anything so yeah. 

**Matt Yonkovit:**  
And if you're RDS you're kind of forced into the performance schema.

**Marcos Albe:**
Yeah, of course, because he must have local access to the slower the agent, the PNM admin agent must have local access to the slow log so you can ship them. And my friend, Matt Yonkovit was asking me if I have everything tonight. So I'm gonna do so.

**Matt Yonkovit:**  
Which is why I asked, I didn't know if it was on or not.

**Marcos Albe:**
No, no, but we're gonna make it, we're gonna make it. So. So global slope equals on. This is our these are all dynamic log output, let me check. So you always want to make sure that log output is going to log to a file, instead of going to a table. In this case, it's already in the file. I also want to make sure that long query time is reasonable. So what is reasonable? Well, if you want to capture all your traffic, and that is what most of the time we will want to do. To do a quality audit, or to investigate specific performance issues. I will say that, you know, for regular production use, you know, to always leave that there and just not have to worry about your slow query logs growing too much, or capturing inordinate amounts of queries that will add latency to the queries and whatnot, I will say 100 milliseconds, it's a very long query. You know, like, if your queries are taking more than 100 milliseconds, you should take care of those less than 100 milliseconds. Again, you are investigating some specific performance issue. Again, this is a ballpark figure that I think it's a good starting point. So here's you.

**Matt Yonkovit:**  
Here's the one thing though, with those settings, that worries me a bit. And this is where there's, there's always trade offs, right? So assuming that your query workload, if you're, if you're saying like, okay, let's set this to 100 milliseconds, you miss out if the queries generally take, like 10 milliseconds, you won't necessarily know, right? Like that, it went from 10 milliseconds to 100 milliseconds. And you won't be able to get that kind of historical rise and fall, which can be problematic, because you don't get that level of detail.

**Marcos Albe:**
Okay, here's what I would like, if a customer comes and goes, counsel tells me Marcos, I have my running Ms. SQL, what is the best way to permanently audit course? Okay, what I will say is a, let's find your QPS, you know, let's establish what is your, you know, big queries per second? And what is regular workload, not the big time, but you know, like something intermediate QPS. And then I will also establish what is an average with average response time, you know, I will say, okay, you know, 95% of your queries return in three milliseconds or less, and 99% of your products returning 10 milliseconds of less or less. So then you can say, okay, long query time, 15, it's, you know, really capturing the 1% of lives. Or I could say, long party time, 10 milliseconds is capturing, you know, that 5% of slow queries and allowing me to skip 95% of my queries from the slower Does that make sense to you? Because I believe that is the right approach, but I don't have a workload here. 

**Matt Yonkovit:**  
You do, okay, you haven't worked.

**Marcos Albe:**
Okay, then you know what, let me condemn. I think I only shared my brows knife. Did I only share my screen? Or? Let me try and if I do you see my browser?

**Matt Yonkovit:**  
Yes, it just pops up. It just popped up.

**Marcos Albe:**
Fantastic. Let me

**Matt Yonkovit:**  
No, no, you're using the internal IP address for Amazon. You'll need to use the external one. By the way, you might want to Yeah, that's the internal IP. So go back to the I sent you the domain. It. Oh, okay. Yeah, use that.

**Marcos Albe:**
I'll use that. Yeah.

**Matt Yonkovit:**  
Yeah. So yeah, you're using just the internal private IP address. By the way, when you go back to your MySQL box, if you could please increase the font size a little bit.

**Marcos Albe:**
Absolutely will do. So it's complaining.

**Matt Yonkovit:**  
Yeah, it's gonna complain because you don't have a valid certificate.

**Marcos Albe:**
Yeah, the TLS certificates are bogus. So we're gonna just gonna say, I know these guys, just personally. It's unsafe, oh, my God.

**Marcos Albe:**
Well, we're and admin admin is your default password always. And then you can change it, I'm just gonna skip it.

**Matt Yonkovit:**  
Don't share the super secret admin password that's the default, whatever. That's just horrible, like people are gonna go, you're gonna be like, ooh, look what I can do.

So yeah, we're looking at the last 12 hours. So it's kind of wonky, he can't really see the graphs. But I think if you change the last, like, five minutes, or something, you'll get a better kind of, let's do something. Yeah, there you go. So you see a little more activity.

**Marcos Albe:**
I don't have so in type seven, I would have installed the query response time plugin for Percona server in eight, zero, you don't need it, because performance schema has a response time table, so we can fetch the latency for the queries from there, but I need to enable some instrumentation. And I will have to go look into my notes, because I never remembered those top of my head to be honest. So I will not immediately have that information. So what I will do, what I will do is I'm going to say enable this locally log and learn a bit, and I'm going to enable it fully. Now I know how many queries per second by hat that allows me to at least enable with long query time equals zero. And then rate limit to have a log of a decided number of queries. So I wouldn't say I want to log 1500 queries per second, which is already quite a bit. That's, you know, should be pretty reasonable. to, to, to do a performance audit. So I would say I'm gonna do one out of grace. So one out of five queries? I think, yeah. It's gonna result in 1500 or so about that. Okay, so let me go back to my pm and you wanted this. Yeah, there you go. The larger shoe thing. So lower the slow rate limit. Global are your I need to ask you something about your application cancel? Does it reconnects, or does it not reconnects? So every time it's going to send a batch, of course, does it reuse the connection or in disconnect and connects again? 

**Matt Yonkovit:**  
Hmm, I can also find out that some things will disconnect and reconnect, but most of them will stay connected.

**Marcos Albe:**
Yeah, okay. Yeah. Connections. Yeah, it's okay. Yeah.

**Matt Yonkovit:**  
So I have the option to switch it to make everything reconnect if we want every time. But I right now, it's just set to default, which is going to be to reuse per thread.

**Marcos Albe:**
Okay? That's important. Because when you're configuring these, if I just do, you know, like, if I do this, if I do set global, and I do set global, lowest low rate limit equals five. It's not going to be something use for all sessions that are connected, it's just gonna be usurped by new connections.

**Matt Yonkovit:**  
So which we can restart all the app server to so that's not. Oh, no, this is Percona Server,

**Marcos Albe:**
My theory, we have stuff for keeping your application app and do whatever we want to or will very much so what I do is I'm saying use global control for this variable. And then even those already connected sessions are going to obey the new value, the same we are going to do for long query time, because otherwise, I will be some, some sessions are going to have long query time equals zero, others are going to have long query time equals 10. So to make sure everybody has the same, we do that, then we do so we can see. And that should have us. That should give us, again, all the queries, and it's going to be one query every five. So every five queries that are executed, I'm going to just keep records of one. Again, we're doing 7.5k queries, this is gonna be about 1500 queries per second, give or take, right, which I know it's relatively safe, up to 3000-4000 queries per second. It's relatively safe or reasonable in modern server, assuming SSD drives, you know, 1632, CPU cores, whatever, that should be a reasonable amount of plugging. Again, these are figures we use as reference to know okay, this is way too high, this is way too low. And if you go to query analytics, calm, and I'm just gonna say give me the last five minutes.

Look at that we have placed and so on the left, we could filter by schema by node by service client host, whatever. In this case, I think my load is movie Jason. My user, the application user is movie Jason. Yes, it is. So well. I can see all the times recently for you know, top queries are all those 10s of milliseconds. This is really bad now, 100 milliseconds, 125 milliseconds, that those are pretty bad. But of course, this guy's the absolute winner with three and a half seconds. So I will take care of that one first. And then I will take care of this other one with 647 milliseconds, why not take care of the second most heavy query a because it's commit? So we're going to have to diagnose what is slowing down the commits. And B because it's easier and likely more prone to give you good gains to optimize such a slow query than optimizing one to 138 milliseconds, which is still slow. But again, this one should be that easy to optimize, right? Like I'm, I'm pretty sure it's using open and string comparison. So it's not able to use me. So what would you like me to do to diagnose the workload first? Or would you like me to diagnose the course first,

**Matt Yonkovit:**  
Let's start with the workload, the configuration itself, let's start looking at the box just to see what's going on. Before we jump into the queries. I have the capability to adjust the workload to whatever sort of workload we want to see. And in fact, I might randomize the workload a little bit here as we're talking as well, just to make it a bit more realistic because right now you're getting a consistent workload as opposed to something that will change.

**Marcos Albe:**
Alright, I like that. Okay. So my favorites. So when I sit down on a PMM and you know, the customer is already telling me hey, Marcos, you know, we have a problem on this node started at this time. Those are the first two things I need to know right like, which node I should be looking at, and what time the problems is started. So, the first dashboard, I will take look is my SQL instance summary. I will make sure I have my the proper node selected. And then I will start going one by one on very much every panel. So what I'm looking for, of course, are anomalies and I don't know what's going on like They only told me things are slow, that's how it usually goes, they told me, it's as low. And so I have very little to lose, sometimes they will tell me some more tools, but if not, what I do is go search for anomalies on every panel. So sometimes it's good, or most times is good to enable individual metrics or each panel, because they're gonna show a different picture. Because look at these connections, it's only in the 20s 30s, so it's more fit by the max connections. So, when I certainly when I turned on everything, I don't see anything like these the connections are changing, like you can see 2826 3029 Whatever, but I cannot see. On the other hand, when I enable long connections, I can see and you know, sometimes you will find a very large spike, you know, perhaps it was all the time 1212 And suddenly you got 14 and 14 connections, they could push enough load to make a problem. But again, you will not see the 40 connections, if you have a 2000 line reference here. So turning on and off, every metric is many times necessary. The same here, right, like a board that connects in this case, I can see all zeros, so I can ignore it. But you know, otherwise, if you see a few, and you know, the time when the problem happening, then enabling just aborted connects will allow you to see the spikes. Then the freights connected and average threads running, these are pretty important like this is telling me like the way these changes and the way connections change, are telling me about the arrival rate and the residency time. And these are telling me about actual concurrency this is when someone is asking you how much concurrency your database is having or is withstanding or is serving, and I'm not sure what word would you like to use that concurrency in my sequel is threaded running? So

**Matt Yonkovit:**  
How many are active at any one time? And typically, it's going to be difficult to get more than, like, that's the active ones that are consuming CPU resources, right?

**Marcos Albe:**
That is correct. 

**Matt Yonkovit:**  
Very difficult to get above the number of cores.

**Marcos Albe:**
Well, it's impossible, right? I mean, you can always have some additional processing with hyperthreading. If you don't count your hyperthreaded CPUs as cores, so a 16 cores with 32, hyper threaded processing threads, it can probably do 32 Perhaps it can only do 20 Plus, it heavily depends on how fast your memory is, and how much different data those threads are accessing, et cetera. But yeah, you know, number of threads running greater than number of CPU cores, that is very likely to become problematic.

**Matt Yonkovit:**  
I can see you're pushing more load. Oh, you're the dungeon masters pushing more load. Oh,

**Marcos Albe:**
He's gonna start trolling me trolls from all angles. So okay, I haven't taken a look at the resources yet which you know, at this point, I will need to take a look. So at the very bottom of this panel, I have a node summary. And it's gonna tell me a bit about the system. But it's not giving me CPU cores. I thought it happened here. So I'm gonna have to go to System No. Summary so beautiful city used to so with the amount of Malaga now I'm looking at the wrong one.

**Marcos Albe:**
That's much better. So it's abuse. I like to appear, so I can also see the speeds at which they are running. And I can see the amount of cash on each one. Something is a bit off. Here it says two here it says eight. I have to guess this is delayed. Alright,

**Matt Yonkovit:**  
Eight hours go go to the last, like, change it to like the last five minutes or 15 minutes.

**Marcos Albe:**
There's for Bucha later, there you go.

**Matt Yonkovit:**  
For whatever. It's weird because some of these summary screens? I don't know, when it takes the snapshot at something we'd reached, probably ask because if you look at like a 12-hour period, and the system wasn't running, or it was on a different class of box, does it show you the first iteration or the last iteration or the average?

**Marcos Albe:**
Yeah, that's, that's a good question. Like, yeah, usually, you know, in a more stable system, you will see this and you will know, it's okay. But yeah, this, we just started a couple of minutes ago. So it was prompted, and changed. Anyway,

**Matt Yonkovit:**  
I'm actually getting errors in the application. You're getting

**Marcos Albe:**
Errors, what kind of errors your customer, I can see, I can't connect, oh, you're aboard. You're getting connections aborted outs.

Unknown Speaker  
Let's see, let's see.

**Marcos Albe:**
And thread cache, you're creating threads, this is usually bad. Creating threads can be slow, depending on your P threads, library, and whatnot. So you're exceeding the amount of thread cache, you should increase your thread cache size, and also getting the right away and

**Matt Yonkovit:**  
Not assigned requested address. It can't connect to the server

**Marcos Albe:**
Not assigned connected address that's funky. I will take a look at that. Temporary objects, it's you know, your workload is starting to create more slope, temporary tables on disk. This is making your queries as low joins, test changes. So you're getting network issues. Now you're getting Could you repeat the error, please?

**Matt Yonkovit:**  
I'm getting cannot sign excitement requested access. It is a MySQL connector interface error. 232003 can't connect to the server. 

**Marcos Albe:**
What else internal memory? System memory. This guy is perhaps is swapping or use something that will be very bad. They can tell him cash buffers, no swaps. No cyberspace being used? 

**Matt Yonkovit:**  
I don't think they're swap setup at all. Did you set out?

**Marcos Albe:**
Yeah, I know. No, I can see you have only 200 megabytes of free memory. You're using a ton of cash.

**Marcos Albe:**
Let's you know what? There is one metric that we don't have. Okay, it's not the scanning pages. So it's not memory pressure. That metric we don't have it in VMM I'm sorry. Memory available so still has memory. That's good. So are you getting those errors continuously? Or is it like one connection every few hundreds.

**Matt Yonkovit:**  
Are getting it's coming through on a fairly regular basis? It's interesting. It's only when I increased the workload quite a bit

**Marcos Albe:**
So it's not happening now because you decrease the workload at some point you see if it's no, I got a few that popped up. All right.

**Matt Yonkovit:**  
There with the workload is definitely different.

**Marcos Albe:**
So you have some iOS that could die, if you have too much I await and the server is busy enough in the connections are gonna timeout while they try to connect so load very our TCP retransmits, that's pretty bad. That's basically how it works like.

**Matt Yonkovit:**  
So are have we saturated the box is the CPU was the CPU like maxed out and it couldn't

**Marcos Albe:**
Well, I don't see the CPU maxed out the normalized CPU load these two, you know, it should be like four or eight. And there is never even fully saturated CPU core, it's always you know, in the fifth below 50% For all these papers, there is some again, there is some here. And that is there is still little IRQ. And again, you know, my main suspect could will be badly tuned and disappear stack, which I can go ahead and tune for you if you would.

**Matt Yonkovit:**  
Not that I mean, let's continue our job.

**Marcos Albe:**
But again, you know, what, while this looks like a small amount of retransmits, you have to think 200 milliseconds retransmits. That's telling me there's something wrong in the network, or in the TCP stack. Because we why things take 200 milliseconds. And what is worse, the second retransmits for the same packet is going to double I think it will double the amount of weight. So it's going to wait 400 milliseconds. And that is like it's going to grow, it's going to try 1516 times, or 15 times I don't remember I think is 15 retries, plus the original 16 Total feet plus 15 retries. Like the last retry is going to be like handled in 20 seconds. So if there are packets that will have four, four retransmissions, I think you know that tag is going to be waiting for more than a second. That's still not enough to timeout a connection in which the default timeout is 10 seconds. But again, shows that networking, you should take care of that. We're running out of space. That's not enough disk space. 200 gigs, that's fine. All right, let's take a look at MySQL and see what we find here. Let's Clements updated. So fated planet stables Aquarius, like types you're doing thing or settlements? What are you doing? T**Matt Yonkovit:**  
Probably it's the Python driver, Python driver will do pings to make sure that connection is still available.

**Marcos Albe:**
Yeah, you're, you're doing 5000.

**Matt Yonkovit:**  
That's because every command so here's, here's a fun thing with the Python driver. It's not fun. I can change the Python driver, actually, it's configurable. We can remove those. We can see what that does. If we

**Marcos Albe:**
Want I will strongly suggest removing those. Because, you know, it's thinking about it. And I recall Barton taught me this and then he wrote a very good blog post about it. Why would you want to go try and see if the connection is open before connecting. So why don't you just try to connect and handle the error? And then you know, just do proper error handling basically, don't don't don't pink, you know, just do your action and catch the error and if needed, go ahead and connect. That is basically the idea, right? So really having 4000 beings If is just annoying for the server, and it's not helping you having more stable software, so just do proper error handling, that will be my advice. Okay, you're reading 2 million rows per second, I would think this is going to break things like this will probably

**Matt Yonkovit:**  
No, why would I do that?

**Marcos Albe:**
I don't know why I would do that. I wouldn't do it if I was. And also 600k 620k, it's a small box, out of the experience. And this, again, is out of looking at many servers from customers, I know that a single thread normally depends on row size, your memory, the type of CPU, the scan, whatnot, but normal, big number of rows you can read on a single thread is about 600k 500k IDs, you know, and that should be like, nice server one that you know, like something from like, last year or last two years. Other servers, I think they can do less because they have a slower memory. But you know, 500k rows per second, it's something that I know will probably keep a single thread busy 100% of the time. So again, these are big numbers, you know, like 800k, it's a big number, you might be using more than one CPU core. And again, memory is much, much slower than the CPU. And let me you know, we also do not have these in,

**Matt Yonkovit:**  
By the way, if you check those admin commands, I just flipped it over to use a different connector. Wow. But the different connectors. Really, Kevin caused me more issues than less.

**Marcos Albe:**
I can see the thing admins went down. Yeah,

**Matt Yonkovit:**  
Because I switched to use the C client.

**Marcos Albe:**
It might be giving you errors that you are having more focus. 

**Matt Yonkovit:**  
Yeah, no, I'm getting more of those connection errors, though, like that are timeouts. So it should start those threads over? So it shouldn't matter so much. But yeah, you are definitely seeing like eight?

**Marcos Albe:**
Yeah. Just see a few aborted connects No, and aborted clients, either. I don't see either of those now.

**Matt Yonkovit:**  
Yeah, I'm still getting that same error. That's interesting. 

**Marcos Albe:**
Boots, again, it has more threads running, you know. So the change was 46. Right? You get that right. And so you know, what you could do? And that will do a favor to everybody is use PMM annotations.

**Matt Yonkovit:**  
I could, but I don't have your PMM server up and running. So I couldn't write Oh, to it. Ah, darn. Yeah. But yeah, so everyone's PMM annotations are good. 

**Marcos Albe:**
Let's look, look, you're sending more select scans, you're sending more select range. And in general, I can tell you are having much more network throughput, like three times more, or two and a half times more. So it might be giving you errors. But again, you are delivering more work. And of course, we have to fix the errors, but you're pushing more to the set. And I don't see I guess I still don't see a single aborted connection after that. So I see the abort that connects there. I think that's when you change it. Things, so you have to reconnect. Yeah. Yeah. So you still get 2003 error.

**Matt Yonkovit:**  
Yeah, same thing. Let me see the retransmits.

**Marcos Albe:**
Because you know, with this amount of network traffic, I will speak retransmits will go up.

**Matt Yonkovit:**  
Yeah, so I got a call. Oh, no look. Actually, the retransmits went down, which is interesting because it's the exact same workload. All I did was changed the Python driver

**Marcos Albe:**
Yeah, the Python driver is terrible. Well, which one? 

**Matt Yonkovit:**  
Well, the one you will use, the one I was using, the one I was using quit using that one that I was using.

**Marcos Albe:**
Yeah, quit smoking.

**Matt Yonkovit:**  
So So Marcos, what we want to really do, though here is based on what's running right now, what should we be looking at changing in the configuration? And what should we be looking at from a query perspective? So let's, let's jump right to that. And we can debug the errors and things later on. Now that I can I can, I could check after the stream here. And what could be potentially causing the issue, you can report back later.

**Marcos Albe:**
Okay, so, you know, I look at the CPU, and now I see 71% CPU. And I saw those status scans coming through. And there's a lot more inbound and outbound. So I don't think this is all queries, you know that your number one problem is queries. So I will try to find out what is making those queries slow. But again, 75% user CPU, that's telling me, You must be reading millions of rows, because, you know, user CPU is either sorts, or very heavy contention on some new topics could also lead to this, or you're just scanning rows like crazy. Most common is you're just scanning rows like crazy. Now, the CPUs are starting to get more saturated, you can see that they're approaching one and you know, it's close to number of total CPUs, fives, well, not that close. But so memory utilization. Still, I have some free memory, it's doing much better after you took all that you have it's even more seemingly don't use the Python. On the one Medusas?

**Matt Yonkovit:**  
Well, I actually have three different Python drivers, I tested the different Python drivers throughput to see what would work best, this is actually the best of the three, which is the MySQL client driver, which is based on the lib C. But you either way, it's interesting that the impact under extreme load of those pings was that much. I mean,

**Marcos Albe:**
Oh, yeah, you know, you were doing it was literally, the server still has to process the command, right? Like you are going through the server, it has to process the connection, and process the command. So even when it's only doing ping, it is forcing the server to do it 5000 times per second, right? So 5000 times per second, it must take 200 microseconds at most. And that will consume a full CPU. But you know what? It's not only the 200 microseconds, but that will also deplete one CPU, perhaps is doing 500 microseconds, and it's depleting more than one CPU. And then your application is waiting for the ping to come back. And then it has to wait for the full network round trip. So you're adding a ton of latency to your application is not my signal, adding it is the network and your decision to take a full round trip before doing anything with the server. So that will certainly throttle your throat. That makes sense, right? Yeah, absolutely. And load average is now yeah, you know, double the number of CPUs. So now the thing is busy. And again, the number one thing we saw was useless view. I will. Yeah. So before you were in the one, eight, now you're like 2.5. It's not a two-fold increase, but it's a nice 60% fold increase, essentially. And

**Matt Yonkovit:**  
We should be doing more inserts and updates as well. I think.

**Marcos Albe:**
Ya, let's turn on everything. Isn't doing less come at me,

**Matt Yonkovit:**  
Obviously, because it's not doing those ping commands.

**Marcos Albe:**
Yeah. And insert. It's just, it looks like we changed it here, remember? So it's doing about the same. You're changing the shape of your workload once in a while, like this is doing more updates.

**Matt Yonkovit:**  
It's a lot more updates. It's always like there were no almost no updates before. Yeah. Wondering if maybe they will then

**Marcos Albe:**
Show commands are marginal amounts. So you can even skip those. But come update, if it's an update with a word condition that is using a bad index or is not using an index that will cause a lot of red run next. Because it's index scanning, most likely. And so are we doing a lot

**Matt Yonkovit:**  
Of what about like, are we doing a lot of check pointing? Because if we have a fair amount of insert, update, delete traffic, so

**Marcos Albe:**
I will get to the right part. But you know, I prefer to take care of the read part first. Okay.

Unknown Speaker  
So, yeah,

**Marcos Albe:**
You know what? Reading enough, we'll talk more rights than writing. Why? Because we're going to be doing LRU flushing. So when you do LRU flushing, you are forcing rights, because you're reading too much. How about that?

**Matt Yonkovit:**  
Right? Because you need to, you know, clear out. But here, here's the thing, you're only going to do that if you are bound by memory, right, like so if you have a dataset that won't all fit in memory, this dataset should 100% fit into memory.

**Marcos Albe:**
Yeah. And uncheck look, this looks pretty healthy. I'm gonna turn. So we have four gigabytes, I created four-gigabyte redo logs. Remember, I told you that was like, you did pretty reasonable. So and it's flushing, but it's only 200 pages per second?

**Matt Yonkovit:**  
Can you zoom the time in? last 12 hours? Go to like last night? Oh, yes, sir. It's just a little harder, sir. Absolutely. Compared to the last hour, before we made those changes, I want to see if anything happened there. Yeah, so there you go. So the system, I mean, like, not much has happened since we, we switched the drivers. So even though we're getting throughput, we're not doing as much. I see this spike here.

**Marcos Albe:**
We could adjust how many cycles it will have to use to create an average for flushing. But again, you know, that looks. The again, the average, you know, 130, that's pretty healthy. Like, I wouldn't complain. Let's focus a bit more here. 260, that's like, very, very reasonable. Like, that's what I would love to see my server doing all day, right. 200 300 pages per second flush, right? Isn't

**Matt Yonkovit:**  
This is a little bit of a misnomer when we look at this short of a timeframe? Because a lot of times flushing doesn't get really aggressive till after a few hours of workload.

**Marcos Albe:**
Yeah, I mean, these will slowly that

**Matt Yonkovit:**  
Going and see what happens, basically. 

**Marcos Albe:**
But you know, I wouldn't worry more if I see this growing linearly, but this has plateau here. But yeah, absolutely. It can happen, then later, when we start to do change, buffer merging. And when we if we have some large transaction, and then we have to purge a very long history, or you know, suddenly you do insert select, that is massive. All those could lead to a big spike that will take time to recover. So yeah, of course, this is best viewer with in the long run, and you know, looking at peak workload times, but again, the peak here was like, one minute. And again, it wasn't so extreme, either. It was 500 pages. It's, it's not small, it's eight megabyte writes. So these are eight megabytes you're writing per second. So randomly write eight megabytes. Reasonable mother drive, should not sweat it. Right. So I don't think this is bad, per se. And again, my experience is most people suffer from poor read experience. And the rights are either just compounding to the problem, or they are a side effect of reading so much, and they don't fit in the buffer pool. In this case, we don't have a lot of flushing because yeah, we have a massive buffer pool. that is not caring about the. So we still can fit all our pages into memory. So we don't have to flush. But that is, you know, an experience that based on my experience, most people suffered from horrible reads. And, you know, like, by now we are doing millions of reads per second, you know, is like, average, let's say, let's run 46, right? Oh, I am 46. Fantastic. So 1.8 million 2.5 Millions, 3.3 million, 4 million for, let's say 4.2 million rows. I told you that, you know, reasonable CPU will do 500k rows per second. So this is saturating 10 CPUs, give or take. And again, these are all estimates. And I indeed see load average shirting. So my estimate is not so insane. And with that, I will immediately Yeah, go to the query as it takes. I will see that this query, which is horrible, we said before, and then

**Matt Yonkovit:**  
Hmm. How do you make this bigger? Oh, my God, you can't, okay. So query time distribution, blah, blah. Explain.

**Marcos Albe:**
And it's reading 100k rows per run, multiplied by 26 2.6 million rows every time this thing will run. So why so bad? Let's see the example. Of course, it's just me five years worth of data. So there is very little filtering. And I don't think there is a real way to improve on this. It's ignoring. There is an index on here, apparently, let's double-check that oh, well, let me go there for a second. This one is so I think. And hear, and so it has an index on the ear. But it's not using a bit, it's just going ahead and not using it, because the range it will have to scan from the index is huge, and then it will have to go to the table anyway, to fetch some other metadata. The normally submitted data in my actual name is coming from actors, right? So what I will say is if we wanted to improve this query, very quickly, is IMDb Rating coming from the table as well. IMDb Rating, so yeah. So what you do here, we have a row that has a few bar charts. And more here, more here, more here. So this is a fat row, this is a very big row. And we are only actually using gear rating, and AI. These are small columns, four bytes, eight bytes, four bytes. So if I create a composite index with those columns, I'm going to have according to the index and I'm going to be saving myself a lot of these grids. I'm going to read the same amount of rows perhaps, or perhaps some less. But especially I'm going to be reading less from disk. So let's make sure I am right IMDb Rating, AI my ID and ear. So I'm gonna go ahead and I'm going to create that index set, I'm going to do it create a table now AI, my ID is the primary key. Just an FYI. So usually, that's going to be on any index, you know, I always have to look at. So in certain condition in certain situations is gonna use it, and then in certain situations is not going to use it. And then sure, if for the join is going to use it, let's leave it out. And we're going to find out very quick, if it's students in it or not. You're going there is setting whose name also.

So there is a setting whose name escapes me, that tell us if we want to use the hidden part of the key or not. But again, there are situations in which it will not use it. And I always have to look back those because those are the edge cases that kill me.

**Matt Yonkovit:**  
Come on, come on. How big is the cables? Not huge. But the problem is, it's under extreme load right now. So I mean, I could stop the load to speed that up.

**Marcos Albe:**
No, no, no, that's fine. That's fine. Probably get timeouts anyways, right now? And most likely, yeah. I thought it was going to be shorter with 400k rows. But those are pretty, as you mentioned, beefy rows. Yeah. For sure. Now, one of the other options to fix this particular query, is if you understand the data a bit more, if you go back to this, right, so let's look at this query. We are basically selecting all of the actors. And the movie ratings for those actors from between a few years. If you look at a movie database like this, you have movies from the early 1900s, like black and white movies to modern movies, but you were only looking at a five-year span. And because the cast of each of these movies is going to be pretty big, because you could have 100 200 actors for each movie, right? So cast is actually the bigger one. And actors is also you know, pretty, pretty big. Because you could have lots of actors in there as well. Yeah, of course. Yep. And so what you might do if this is causing you a significant issue, is actually to duplicate data. So for instance, if you had the years that the actor was actually active, so Robert Downey, it was more like, yeah, no, Robert. Yeah, Robert Downey Jr. was not active in the year 1900. So if I'm searching for, you know, 1900 movies, it won't appear. Right. Same thing with like, okay, you know what I mean, that will require, yeah, but that will require rewriting part of the application, the query, yeah, yeah. So I'm trying to so first step is see how far you can get by only adding indexes or tweaking the optimizer or whatever. Yeah, sometimes dropping an index will fix things. But again, the goal my first goal is always to try to get the curiosities to perform better. But yeah, what you're saying is, yeah, we could say, okay, just give me actors that were born before 2010 And that were alive. Until 2015, you know, so if it was dead before 2010 They could not be in the movie.

**Matt Yonkovit:**  
Yeah, I mean, like, this is where it gets back to understanding like the queries themselves. I'm gonna go ahead and I'm just gonna slow down the rate of throughput so that quarry can finish the table company. What? A little better there.

**Marcos Albe:**
Yes, probably not looking nice on this side of the words.

**Matt Yonkovit:**  
Yeah. So I mean, like, like I said, I just kind of dropped things. So hopefully that will free things up for that particular query too. And obviously, most of the servers that we're going to be looking at aren't going to be doing, you know, millions and millions of rows on such a small box either. You know, that's something that we've generated.

**Marcos Albe:**
Instantly. Yeah, that's good. What is that?

**Matt Yonkovit:**  
Okay, go ahead and run that. Explain. See if it picked it up, you can run the explain command line. Right. So

Unknown Speaker  
I'm just gonna copy it from here.

**Matt Yonkovit:**  
I don't think that will make that big of a difference. I don't know if it'll change the explain.

Unknown Speaker  
Yeah, look, it's

**Matt Yonkovit:**  
You're writing it is using the year right.

**Marcos Albe:**
It use an index. And it's using where it's using temporarily, because it's mixing the group by from multiple tables, so there's no way to avoid that temporary table?

**Matt Yonkovit:**  
Well, I mean, yeah, I mean, you could break it into like, a to park where he as well. You know, to that, that might actually speed that up as

**Marcos Albe:**
Well, potentially, right. So glue by ear first and then know what?

**Matt Yonkovit:**  
Well, I mean, like, so. So you don't necessarily. But like, like, you could do the aggregate after, so you could build a temporary or built like a transitional table. Again, it requires code. 

**Marcos Albe:**
Yeah. But it's also got always going to be doing some sort of temporary, because there is no again, if you have data from two tables, how do you know, aggregate by then, like, you must have some intermediate representation data to do the aggregation map.

**Matt Yonkovit:**  
So go see if you can find that query and PMM now and see what happened.

**Marcos Albe:**
There. Let's take a look. Let's say last five minutes. Let me bring this down. Still, okay, the load that is going down, but still, it shows up. As pretty big. Plans gonna be fresh. No, still looking at the old one. Now it's worth it.  So it's not it's never filtering. You know what let me tr like skiing six foot so let's say that you seen it now. Now let's see now. What else could I do to actually force you? This is late. Let's how many words you don't want to wiggle those rules?

**Matt Yonkovit:**  
Yeah, it's a quarter of the data. It's interesting. It was a lot of movies between 2010 and 2015. Wasn't there?

**Marcos Albe:**
Prolific, prolific ears I could adjust the costs.

**Matt Yonkovit:**  
Now, interestingly enough, go back to the original query and change the dates real quick and see if it picks up that query using different dates like search and choose like 1910 to, you know, 1940 or something or 1930. Something crazy that shouldn't have like, nearly as many um, yeah, so it actually is still. There's only 36,000. That's interesting.

**Marcos Albe:**
So I know what I could do is the following. And let me bring up a text editor. So if I have this let me bring the query. I don't think this should be faster let me compare this how I what I usually do these kinds of things are hard to do from PMM so what I do is I do pager define some flash status, slick select No pager let me restore the dates slow query so let's see if my version is any better It's the magic of the SQL queries.

**Matt Yonkovit:**  
This query is specifically designed to be bad anyways. No, no, I know.

**Marcos Albe:**
Suspecting, I was expecting that one. Yeah, as you said, you know, like, we could go ahead and try to cut down and oh, I don't have any birthdates or anything like that.

**Matt Yonkovit:**  
No, there's nothing in there. We would have to add it, we'd have to duplicate it. Right. That's a whole other.

This query though is not run as often as you would think. Go back to the list.

**Marcos Albe:**
Reading 5.7 point 856

**Matt Yonkovit:**  
Rows are returned. Go up, like just look at the returns 1 million rows. Yeah, yeah. Yeah. So it's, it's, it's returning a ton of data in and of itself. So obviously, limiting the amount of data that you return is critical in this because the question for all those who are designing or building an application like this is? This is the critical question to ask your developers when you see this. What are you trying to get? Right? Oh, yeah, you're not going to take a million rows and do something with it.

**Matt Yonkovit:**  
Well, you're it's selecting some subset of that data. And this is a very common issue that I've seen where you return a significant amount of data when you only need 10. So in this case, it could be being used, like you have limit 10, it could be being used to say, who was the most prolific actors? You know, who had the best ratings in this time period? Right? So between 2010 and 2015, who made the best movies? Right? Like which actors? That's a reasonable request. Right? And so if you're trying to get that, is there a better way to get that?

Was there anything that you saw on any of the metrics that lead you to believe we needed to tweak or adjust? Based on what workload is happening now?

**Marcos Albe:**
Let’s I didn't say anything like that and immediately stood off like that, again. Let's see SQL. Come on. Max, these is connections, they'll be this looks healthy. Again, there was a spike of threads created, but it was a small. So perhaps average spreads running 16 It has peaks of 40. We have we said we have how much it was built. It's eight CPUs. You know, I will take a look and see if there are mutex contention. So we could perhaps tune into the be concurrency change parish? Where is it? Contention? You know, little to no, absolutely not, there is no contention at all. So, you know, adjusting prep and currency will not help. So what else can we see here? Temporary tables, temporary, these tables, this is probably from your show commands. So you can ignore that

was no curious. We'll select this will all be related. Merge passes? No. So we cannot adjust the sort of buffer to do and against the looks with simple questions that. Again, those set options, I will remove them. This is even more, the Set option is even more expensive than the ping. Because it has to parse the SQL, the ping is just the command and it's already a command

**Matt Yonkovit:**  
Options are running the window.

**Marcos Albe:**
Well, it's like no, I cannot tell immediately from here, I will have to go to query analytics. And I will have to how can I search by here. Set names sit out of me.

**Matt Yonkovit:**  
Ah, it's set. auto-commit. That's interesting.

**Marcos Albe:**
So, again, this not only will add a full network round trip to your application. And believe me, that's super expensive. That is perhaps the most expensive things you can incur. And but it's also adding authentication, handling, query parsing, query execution. It's the whole show, right? It's a full query, you're running one more query, whether you like it or not, whether you think it's super cheap. It's not cheap. Because again, authentication requires another round trip. Because if you're doing DNS resolution, right, for that single query, you have to do make sense. No, yep. Yep. Yep. So it's incredibly expensive.

Unknown Speaker  
Where were we? What is my

**Marcos Albe:**
adoption? It changes Almost every other second, this is trying to trace, okay? commits are 1000 per second, that's okay, it was super slow commits today were super slow. We could perhaps relax durability if we wanted to. Let me remove filters, how they remove this filter that loops over it. So commit still slow, right? I know how can we lose it, let's commit. And then minimum 14 microseconds maximum 100 milliseconds, that's insane. But six point is 69 milliseconds. It's really, really high commit time. So at this point, I will ask myself, do I have saturated audio and write latency? It's one millisecond. So apparently, it's not what is adding to is not all the time. Curious, I will speak more, right latency with latency is also pretty low, one millisecond. And the average is 400 microseconds, which transmits the hog. So we have full durability, right? Like that needs to be sure we should.


**Marcos Albe:**
So I could relax your ability and see if that permit goes away.

**Matt Yonkovit:**  
That's a live changed make it let's see what happens.

**Marcos Albe:**
Let's make two. So by sending it to the F sync on the redo logs is going to happen once every second more or less. But if my sequel crashes you and you started, we started immediately it's likely going to survive. But it's not going to survive a full always crash. Of course, if you set this to zero, then it will not survive even the MySQL crash. And with one it it's fully acid compliant, and it should survive any crash. So let's see it first and we should see more commits now. Let's go on up.

**Marcos Albe:**
It went up. Because it can do more. It literally can do more per second because they are faster.

**Matt Yonkovit:**  
But you traded on durability for that.

**Marcos Albe:**
I traded off durability for that. Yes. Yes. Of course, there is always business decision, right? Like can the business tolerate one second's worth of data loss? Can the business does the business care about the data we are saving on this database or not? Like that's basically if you're moving money, you probably don't want to change that

this was the ALTER TABLE probably though this one should have been much earlier.

**Matt Yonkovit:**  
Now that was reconnect on my part. You're working on these strange?  Strange. It's not strange. Okay. It's great. Well,

**Marcos Albe:**
It has very large steps.

**Matt Yonkovit:**  
Yeah, but when you look at the dips exist on every one of those graphs.

**Marcos Albe:**
Yeah, it's, it's it just goes back and forth. Again, leads or salutes. Okay, these are all marginal. So when you start to see that the average is 200 Ops 770 Ops, you can ignore those like, I will start looking at the ones above. I think a you know, yeah. 100k. So, again, you're doing a lot of work anyway, right? Like still, you have an order by descending. And this is forcing you to read, breed, breed, and that's not fit for v3 Basic indexes. In eight zero, we can create reverse indexes to satisfy this query. So we could find this query and Create, you know, different index on it.

**Matt Yonkovit:**  
Okay. Well, let's end this for today. So our next live stream is actually now that we've got PMM set up, we've taken a look at the workload as it's running. We've kind of showed people you know, some of the graphs and charts, you would generally look at the places you would go. The next one is for us to set up. Alerting. Oh, alerting. Oh, my. Yes. So now we've got PMM setup, what we want to do for our next stream is come back and set up same alerts on this machine. So what should we be looking for when CPU arises above x, the number of connections above why? What are those things and we should be going through and setting them up. So everybody knows what they should be getting alerted on when these conditions occur. And we probably won't run the box is heavy as it is right now. Right now we've, you know, I purposely tried to push as much as I could, but we'll probably, you know, do something that's a bit more reasonable. And then we'll adjust the workload up and then watch the alerts fire.

**Marcos Albe:**
Yep. And just for the record, like we can see, this guy is, you know, shrinking the average.

**Marcos Albe:**
They think the committee went from six plus to 370. So it's working. Yeah, we should let the average run for a bit longer, before arriving to some conclusion. But yeah. Again, it was a very heavy read workload. That's hard to tune without rewriting queries many times. So we did what we could. So I hope we can help you more next time.

**Matt Yonkovit:**  
All right. All right. Well, thank you, everybody, for hanging out with us today. Hopefully, this was educational. Hopefully, this gave you some ideas on what you can use PMM for how to get it set up and working. And we'll be doing more of these live streams over the next several months. There is a schedule on the Percona dot community website. If you are interested in seeing what's upcoming. We're going to be covering backups. Ha, you know, every sort of nuance of MySQL over the next 20 or so. Streams? Yes, that's a lot of streams. And, I promised Marcos I would get him a new camera and set up for his thing to help with some of the live stream stuff. By the way. Marcus, did you see that? Did you see the championship belt? Yeah, I

**Marcos Albe:**
Saw I saw the post on LinkedIn. Well, yes, sir.

**Matt Yonkovit:**  
So we got the championship belts here. I got two. So we'll just leave it here. And because are those going to be awarded for kind of life? Now? This one's jovens. Then Sergei has won over there. We have other awards for Percona Live, so but yeah, so official Percona championship job and won it. So.

**Marcos Albe:**
All right. Yeah. Yeah.

**Matt Yonkovit:**  
All right, everybody. Thanks for hanging out today. We appreciate it and we will catch you on the next stream. Feel free to ask any questions that you have. And we will try to respond to them in the chat or in the next stream. Thanks a bunch. Have a good day.