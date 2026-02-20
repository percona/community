---
title: ' MeetUp for MySQL - Database Tuning Secrets of the Stars - Dec 8th 2021'
description: Listen to Support Case from Hell and attend to Live Troubleshooting AWS
  RDS/Aurora, EC2 in this Community MeetUp for MySQL hosted by Matt Yonkovit with
  Marcos Albe and Fernando Laudares Camargos
images:
- events/percona-meetup/mysql-december-cover-1920.jpg
date: '2021-12-08'
draft: false
aliases:
- /events/percona-meetups/percona-meetup-for-mysql-december-2021/
speakers:
- marcos_albe
- fernando_laudares_camargo
- matt_yonkovit
tags: ["Meetup", "MySQL"]
events_year: ["2021"]
events_tag: ["Community", "MySQL"]
events_category: ["Speaking"]
---
Listen to this Community MeetUp for MySQL hosted by Matt Yonkovit to discuss Database Tuning and Troubleshooting with Marcos Albe and Nando Camargos. They reveal some Support Cases From Hell, Database Tuning Secrets of the Stars and stump the expert Troubleshooting on RDS/Aurora.

## Video

{{% youtube youtube_id="i4DG30guHmA" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Oh my goodness! Welcome welcome welcome all you out in stream land and what Welcome to a late late afternoon edition for most of us of the Percona meetup. I am your host Matt Yonkovit. And I am once again joined by Marcos and Fernando. Although it seems like in the late afternoon I have grown a lot of struggle and have a five o'clock shadow. And Marcos has lost all of his hair. I don't understand how that's going and, and he looks very confused and I can't get over how different he looks. He looks like he's trying to figure out but he doesn't quite understand where we live. What do you think? What do you think Fernando?

**Nando Camargos:**  
Yeah, I don't know if he's hearing at all.

**Matt Yonkovit:**  
I don't know either.

**Nando Camargos:**  
He's been doing a lot of Kubernetes lately. Maybe that's it.

**Matt Yonkovit:**  
spin up a new pod. Marco spin up a new pod. Oh, now we can't hear him. Yeah. Oh, we can't hear you. Oh, we can't hear you. You're here. No. Microphone. Are you muted?

**Marcos Albe:**  
No, I'm not muted. Hello. Hello. Are you alright? Nothing changed.

**Matt Yonkovit:**  
No, no, everything changed. Everything changed. Like, you've lost all your hair. And I can't look at you and like, like, there's so different. Like, I don't know what to do. 

**Marcos Albe:**  
I'm trying to look like Mark Callaghan.

**Nando Camargos:**  
Oh, it's Oh, it's closer than it was before.

**Matt Yonkovit:**  
Yes. So before I make fun of you, you're not sick? Are you?

**Marcos Albe:**  
No, no, no, perfect. Okay. Well, it's summer, and it's hot. And I just, I don't know how to shave and only get my hair out. So I had to do my hair on my beard. So it's gone. Nothing but nothing too bad.

**Nando Camargos:**  
Grow it up again.

**Marcos Albe:**  
Yeah, exactly. Exactly.

**Matt Yonkovit:**  
Yeah, yeah. I seem to remember. If you're familiar with The Simpsons, Omer Simpson episode when he was younger, had flow in here. And he goes, Oh, yeah, that will just grow back in? Oh, so I don't know. So you guys are doing some Kubernetes work I hear?

**Nando Camargos:**  
Yeah, we can do eight hours per day of training for Kubernetes. Super useful. Because one thing is knowing how to use something, something else is knowing how it works. So we're actually getting into the gritty details of how it actually is built. And I don't know the concepts, they become clear. In a lot of states. It's easier when someone with more experience shows you something. So now it's even we can again, we've been learning to use it, and we deal with it. And we solve and troubleshoot things every week. But in the end, it's not as in-depth as we'd like to go. So we're going where we were where we want to be actually.

**Matt Yonkovit:**  
Well, who's giving the training?

**Nando Camargos:**  
Oh, it's Laslow? What's his last name? I can remember his last name. And it's a Hungarian company. Yeah, they're friends of Peter Borash. So, really, really good quality. So I'll get to the link to these guys before we are in the stream. Great. So let me join from my computer. So I have a screen. And what can we do?

**Matt Yonkovit:**  
Marcos Marcos. Well, so the official schedule is, I thought that we would start with support cases from Hell, yes, so without naming names, we would love to hear some war stories. I'm sure that there are more than one or two cases or issues in the past that you've run across that you're like, Wow, that was a crazy hard or a crazy thing that happened, and everybody loves to hear those crazy stories. So I figured we would start this live stream with the support cases for Hell.

**Nando Camargos:**  
Sounds good to me. Um, so one recent streak of support cases from hell has been related to memory allocation. And people precisely run on Kubernetes very big nodes, perhaps 144 172 CPU cores. And they create many, many small instances, and they run many, many processes. And the thing is, they started experiencing memory out of memory kill, in the process. And well after lots and lots of investigation, I'm telling you evil, they spent, I don't know, 30 hours getting to the bottom of it. And in turn, it turned out that it was all over the internet. In the end, it was not, perhaps, so hidden, but we needed to actually confirm it, to actually prove it to the customer. And in the end, this GPMC, it will create eight allocation arenas for each CPU core. And then it will, if you have three bytes in one of those arenas, it will not be allocated. And then it also has a holistic way to preventively just leave them there, it just doesn't allocate, because it thinks they're going to use it soon. But when you have 44 CPU cores, and you have eight arenas per CPU core, you're just created, I don't know, 1100, or something like that, right. So it turned out to be a crazy waste of memory. So you can actually reduce this number of arenas with an environmental variable. And you can also switch to Jemalloc. And if you do switch to Jemalloc, then you have to disable transferring teaching pages, or enable an option that I was not aware of, and Sergey told me about it today is that it's called opt.php. Because otherwise, you're gonna have tons of memory fragmentation, and you're also going to get ...

**Matt Yonkovit:**  
And that's what because each, each, each instance has its own little area of memory. And so they don't know about one another. And so you just over allocate each one is basically what happened.

**Nando Camargos:**  
Yeah, the allocator created, again, 1100 plus allocation arenas, and, and actually, as the memory, I mean, as the memory was being created, needed, it will create more than all these arenas right up to up to that number. So it was just able to grow up to that number, that's the thing. It didn't do all of those immediately. But MySQL is memory-hungry. And if you get memory, it's just gonna use it. So it didn't use it, but then it released, right, like large temporary tables for a big union sorting stuff like that. And, again, we couldn't see a leak in MySQL like, and we did investigation through performance schema, memory introspection tables, and we couldn't see. Also, big memory utilization there or memory was always released. So in the end, it turned out that those memory arenas, even when MySQL, allocated the memory, the allocator would not release it.

Very well hidden.

**Marcos Albe:**  
That was, yeah, that was nasty. And then I have another one, which we are still investigating. We didn't go to the bottom of it. And this is probably one of the things I'm less experienced with, which is networking with border routers. And I imagine there's a border router somewhere in the problem because they have an on-premises, very heavily secured site. And then they have AWS instances, EC2 instances, and we can send packets, we can send packets up to 488 kilobytes or, but it's a something a number that is not even about to

**Matt Yonkovit:**  
Wait, it sends a kilobyte then shuts off.

**Nando Camargos:**  
No, it sends eight kilobytes, but it will not send 8.1 kilobytes,

**Matt Yonkovit:**  
So yeah, after eight kilobytes, it just cuts

**Marcos Albe:**  
 Yeah.

**Matt Yonkovit:**  
Is that virtual packet or anything like

**Nando Camargos:**  
No, we didn't get the TCP dump yet, because now I can tell you it's a government agency. And things are rather slow. And you have to be patient and deal with their way of doing things. So they have a team that will take the TCP dump. So they open the ticket with that. So that's not the hell is networking, and not being able to put your hands on the keyboard where the problem is happening. But yeah it's like, I recall a similar case, for a company that does fitness here. And they have a large chunk of servers in China, behind the Great Firewall, and they have similar issues. But that was the firewall change in MTU. And then, by changing the MTU, they were breaking the well, basically communications. When you exceed something, they will break down the packet, and then it will not, we rebuild it on the other side. So it will filter out some pieces of the whole packet. So anyway, that's something under investigation yet. But yeah, like those cases, they are quite elusive. Because again, you don't have access to all the equipment, right? There are routers and other equipment that is not even a computer running MySQL. It's pure networking gear, and we don't have access. So that makes it hard. That makes it tough.

**Matt Yonkovit:**  
So, before I ask Nando about his interesting cases here, I want to point out for the folks who are still joining that we've kind of doubled the number of people who are online. Yes, this is Marcos, you are on the right stream, he just looks way differently, and it will take you a while to get used to. So I just wanted to clarify that. So Nando what about you any interesting or challenging support cases that you can kind of share with us that are interesting?

**Nando Camargos:**  
One thing that is very nice and challenging at Percona, is that you get a bunch of different and challenging toolkits everyday, right, with different support cases. I think, to me, the most difficult part yet is when there is a bug in the middle, and you need to chase that bug, right? And you need to, for instance, there is a server crash. And with MySQL, we have that happening, in some situations. And until you get why this is happening, it takes time, right. So you need to work with the customer to produce a core dump. And then you need to get the right libraries to be able to resolve the core dump. And then you will look at the source code to see what it is actually doing. And this to me is a skill I'm still developing and quite a junior yet. And so these are those that are the most challenging to me. Right. Yeah. In general.

**Matt Yonkovit:**  
Yeah. Yeah. So I think that those are always the more difficult ones because it's hard to reproduce them. And it's really difficult to narrow them down, so I can understand why those can definitely be a challenge.

**Nando Camargos:**  
Yeah. And we have another one, which is this guy, who has ProxySQL, and he wants to set wsrep_sync_wait for one of his sessions. And he sends the set sync wait. And the proxy is not forwarding to the backend servers. And we cannot reproduce like we have the exact same configuration he has, and we can not reproduce. And we've been trying to chase that. And well, Nando was actually talking about that, right. It's like, we took a core dump. And now we are going to use the core down to ask support for code analysis. So we're not going to solve it through the core theme, but rather use it as support to get context for doing proper code analysis.

**Marcos Albe:**  
So reproducing is the thing, right?

**Nando Camargos:**  
Yeah. And then, yeah one hard thing is now sometimes we have tools that will allow us to do magic, right or do really cool data collection or stuff like that. One is our project.

**Matt Yonkovit:**  
And oh, yes, yeah.

**Nando Camargos:**  
And but I haven't found a single customer that told me like everybody wants to know that it contains sensitive data. I cannot send you that right. All right. I will try.

**Matt Yonkovit:**  
Well, I do feel bad because As we are right now while everyone's pushing to make things easier, we're making things easier at the expense of complicating the crap out of a lot of our applications and our infrastructure. Right? There are so many individual components now. And there are so many ways to slow things down to expose data to do all kinds of crazy stuff. And it goes so far outside the database in a lot of cases. Right? It's not just that database layer anymore. I mean, and so Marcos, you're pointing at me, because he has a story that he's thinking about, I can see,

**Nando Camargos:**  
These guys, they were doing a set. And these guys were some other company, right? They were doing sets 7000 times per second. And I told them, this is killing you. And they were like, No, how could it be? Right? It's like, well, no, it's not only the set but also the network round trip, and SSL encryption for the network traffic, and the threat handling, and the authentication, and everything. So, and then we did the frame graph, right? For only that frame, and where they were sending the set commands. And indeed, right, like the handling of the concept of the command for the set inside MySQL, it took, I don't know, 9% of all the time, the rest 90% was like overhead from getting to the server to actually send the query. And that that's the kind of thing, it's all it's hard to see at first, right? It's like, it's not there, you think it's equal. Hello, I experienced some workaround three wsrep_sync_wait is set. We requested a feature some time ago, Vadim, or Marco Tussa. I don't know who filed the feature requests that you know how you can actually set session variables through the query in a comment in the query? Well, unfortunately, wsrep_sync_wait can not be set through an account. But we actually want to do it because that will be perfect, right? It's like, I want this one query to be synchronous...

**Marcos Albe**
That is over ProxySQL, right? 

**Nando Camargos** 
Oh, no, no, I think he was this particular, if there is a way general, okay, you will always have, wsrep_sync_wait, because if you don't do the set session before then you have to send those 7000 set, set wsrep_sync_wait. So what we want to do is just send it inside the query. So while you're parsing the query, it will be set and then it will only take that 9% of the time, it will be that 9% overhead. And all the other overhead will be shared with the actual burn. So it's a big game.

**Matt Yonkovit:**  
So with that, I'm going to go back to my to take a step back from the wsrep_sync for a second and go back to where we were talking about the complexity and you mentioned, like the set 10,000 times a second. And that will bring me to my first “stump the expert” of the day. Yes, indeed, I have a graph to show you. And I want you to help me understand what we're seeing. Okay, this, this is a screengrab, or actually, it's PMM. And I will show you the events that were happening earlier today, as I was doing some testing. Alright, so let's go ahead and make this bigger. So you can see this. So hopefully everybody can see, the big thing that I want to show you is the queries per second and this is scrubbed. Now, I want to point out something, okay, for those who are doing benchmarks, and for those who are testing performance, there are multiple ways to measure either throughput or queries per second or transactions per second. Depending on how you measure it, you will see vastly different numbers. Now I am at the top. These two are both showing queries per second. One of them is scrubbed. The other one is not. Now I'll get to that in a second. But they are both the exact same workloads at the exact same time. But you look at the two queries, and you have two vastly different outcomes, right? Like, each one of these is the exact same workload run four times with one change. Okay. And so that one change. you can see on the left side, where it says scrubbed, it looks like the last two are much more or much faster and better. Whereas the right side looks like the last two are worse. Right? So interesting to point out, but I'll get to that in a second. So, same workload, exact same workload on each one of these exact same number of threads, exact same data, exact same system. What do you think? Is the difference between one-two and 3? 1234?

**Nando Camargos:**  
And on the scrubbed one?

**Matt Yonkovit:**  
Yes.

**Marcos Albe:**  
Well, it could be a buffer pool warm-up.

**Nando Camargos:**  
But it's two containers for each. Yeah. Good.

So you change it something you told me to change it something?

**Matt Yonkovit:**  
Yes, I actually changed that. There are two things. So I'll even give you this clue. This is my first bump here. So bump one and bump two, this is one change. Okay. And then that same change, with additional changes bump three and four. Okay. Okay. So, so whatever I changed to make this go up, I left it, and then I tested it again.

**Nando Camargos:**  
Can I kind of get it another? I need one more clue: is this read workload? Right workload

**Matt Yonkovit:**  
It is a mix. It's going to be 6040. And I'm going to tell you, I didn't change anything inside the database.

**Marcos Albe:**  
Anything inside the database? IO scheduler?

**Matt Yonkovit:**  
No, no, no. So you'll never get this one. So are you gonna give up or do you want to guess you want to get up? Yeah, you can if you want to look at the analysis if you want. Michael Coburn says he thinks it's a varchar. No, Michael, this is not something that you have seen. So he's assuming that I'm just recycling things I've already shown people but no, I am not doing it. Okay, I am gonna say

**Nando Camargos:**  
there's no change in the database. You mean, you didn't change anything in the MySQL configuration?

**Matt Yonkovit:**  
I changed nothing in the MySQL configuration. And, and keep this in mind? If you look at the numbers, okay, so the numbers here, so it is going from 2.9 1000? Or so 2900 queries per second to 4.4.

**Marcos Albe:**  
The number of clients…

**Matt Yonkovit:**  
No, number of clients is exactly the same.

**Marcos Albe:**  
You changed Networking buffers

**Matt Yonkovit:**  
No. Don't you give up yet?

**Marcos Albe:**  
It's nice to have like a hands with more things like until

**Matt Yonkovit:**  
Oh, okay. But we don't have 100 more days worth of time to give you guesses. So, okay, this first bump is actually running Python 3-10. And the second bump is python 3-9.

**Marcos Albe:**  
And there you go. 

**Matt Yonkovit:**  
The newest version actually has a regression, a massive regression in the MySQL connector. And so it's a huge, huge difference. And the reason why this is so interesting is when you see a performance degradation like this, that's probably one of the last things that you would actually check is like, who changes like or updates their, their, their application packages, and it impacts the database, exact same code base, completely repeatable.

**Nando Camargos:**  
In fact, this is one of the questions we usually ask Matt, something changed. So you didn't touch the database? Were there any recent upgrades in the application drivers etc? Drivers are not as often as one might imagine. But they are sometimes the culprit behind problems of performance like this.

**Matt Yonkovit:**  
And this isn't even a driver issue though. This is a this is the language itself, the very it's an upgrade, it's an upgrade from 397 to 310. And it was that large of a drop-off. I mean, that's a pretty substantial drop-off. Now with that, sticking on 397, I moved from the MySQL connector over to the MySQL client connector, a different driver for Python. And so that's what the second two bumps are. Now, what you'll notice is there is no regression between 3.9, and 310. So this is 3.10. And this is 3.9, its is almost exact uniform performance between the two. So the driver in this case with the combination of Python 3.10 causes the issue. Yeah, and it's in what's which other the other interesting thing is, with people who are tuning in when you when you're talking about, like hey, you know what tribe are using, but most people don't think about that. But even here you're talking a difference between 4300-4200 queries a second to 4849. In 100, just in changing the drive, and that's partly because MySQL built on lib C. So it's built on the MySQL C drive. Over, as opposed to the pure Python MySQL connector go.

**Marcos Albe:**  
I was going to say, it was like a year of native implementation. Yeah.

**Matt Yonkovit:**  
Yeah. So. So now, Marcos, now you said that, that the set command was run 10,000 times. Now, one of the things that I noticed in looking at this workload, and let me go ahead, and I'm going to pull one of these queries from earlier today. So let's go back about six hours. And let me show you some of these tests. And so you'll see that there is quite a few queries going on here, you'll see the commit. So there's, there's obviously a ton of commits in this. But one of the things that I also noticed is the MySQL connector does a ping every time you run a query executes, yeah, sit to verify the connection. Whereas the Python, MySQL client, which is built on MySQL DBs, driver does not. So you actually see like the numbers here called, must be added. So when you do so I have this scrubbed versus not scrubbed. So you look at the queries per second here, right? So you see these, these two, which, obviously, this is the same numbers, this, the difference is actually just the ping command. That's, that's, that's why there are so many queries per second. So if you look at like queries per second, you're like, Oh, yes. Python 3.10 is really kicking butt here with that MySQL connector driver. But it just happens to be that all of your time and the response time, because if you look down here, look at the response time. Oh, look, it's so much faster for this. You're measuring the response time of the ping command. Yeah, right. And so So here, you can see, you can see here like this, white line, that's the MySQL pain, right? And so versus the select. So I mean, it's, it's crazy. How much it does it? Yeah, here it is right here. So here's the ping command, it has been executed during this time window. And keep in mind, this time window is about an hour and a half an hour and 15 minutes. So what is that? That is 1 billion times? Yeah, so so it's been executed 1 billion times? You can't see it. But it's,

**Marcos Albe:**  
We always were customers about integrals. It's like the fast pace,

**Matt Yonkovit:**  
 but it's the fault of the driver. You can't turn it off.

**Marcos Albe:**  
Yeah. In that case, change the driver because

**Nando Camargos:**  
That's the thing of running in production at scale, right? What might not even make a difference when you are testing, even staging, when you put it on production? And the scale just goes higher up? It will be noticed.

**Matt Yonkovit:**  
Yes, yes. So. So the second thing that I have, and let me go ahead, and I have 

**Marcos Albe:**  
a common article of yours, that one about Ruby, like 12 years ago, probably but

**Matt Yonkovit:**  
one on rails? I probably Yeah, yeah, that's yeah, I probably had one on that I'm gonna write on this as well. I mean, this is a really compelling thing. And I've been running these tests. And I've been noticing that even workload changes. So the actual MySQL connector actually performs better in some workloads. with 310, then three, nine on a normal workload. So it's very workload-dependent. But it's a really difficult one to capture. And we're going to actually get into that in a second. Because part of me I don't know what the hell is going on. And part of the stump the expert, I'm stumped right now, is I'll show you, I've got that. So I built this benchmark tool to basically run workload on multiple systems, and I use the controller to do that and stuff. But one of the benefits of this is you can run workload in parallel across multiple systems and duplicate that workload in different areas. Okay. And so this is a mixed workload, with all the different types of workload that I have, and it's running on an easy to IO instance, and in Aurora IO instance. Okay, And I have the config diffs. And there really isn't a lot of config diffs. And I actually backed up the MySQL ADC too, I did a magical dump of everything and reloaded it into Aurora. So they are equivalent. They've got everything the same. They have the same class of box, actually, the Aurora, one has more memory and has twice the memory. But you can see here, this is the queries per second right now 563 queries per second on the EC2 instance, versus 77 on the Aurora instance,

**Nando Camargos:**  
Just select,

**Matt Yonkovit:**  
It's a mixed bag of everything. And so I mean, here, I can go back, let me go back. I've been running all afternoon, in preparation for this. And so you can see, you can actually see the dips here, right. And so these depths are probably going to correspond to Flushing is what I'm guessing. It's probably fair. So over these three hours, the average has been 738 queries a second with EC2, and 135 with Aurora. And what's really weird is if I change the workload, I can have these be equivalent. So like, if I run just a very standard, like read-only workload or very write-heavy workload, the write-heavy workload actually performs better in Aurora than it does in MySQL. Yeah, and I mean, part of that is, I mean, they've turned off the double write buffer, done a few other things. But it's a really weird setup. Because like 738 versus 135. That's a drastic difference. 

**Marcos Albe:**  
There's something right, what is the right way to approach this is, if you have less queries, it means some queries have higher latency, right? Yes. So what we need to find is, what queries have the highest latency? And then try to see what explanation we can find in a loader that makes that query slow. Let's go to query analytics.

**Matt Yonkovit:**  
So would you like to drive Marcos because you have access to this? If you want, I let you drive? If you want to, if you want me to I can.

**Marcos Albe:**  
Let me get there. And just one second? it's, I don't know, in all colors to me. No.

**Matt Yonkovit:**  
Yeah. And what's interesting, keep in mind, the exact same queries are run on both boxes with the exact same number of threads with the exact same data set. Now, the data set does drift over time, because it does add things and move things, but it adds things and removes things, and updates things on a consistent basis across all of them. It's just it fills in like a random comment. So I can't guarantee the random comment won't be the same on both. But even when the data was exactly the same, this difference still existed. And I do know that there are missing indexes, and that there are things that could be optimized for both of these, they are both kind of, in let's say, a craptastic state on purpose, on purpose, so we can fix them if we want and see what the difference is. But the fact that the craptastic state is so much worse on Aurora versus MySQL. perplexes Me.

**Nando Camargos:**  
But buffer pool configuration is mostly the same, right?

**Matt Yonkovit:**  
Again, there is more memory on Aurora. And just so you guys are aware. If you are really, really curious, which maybe you are, maybe you're not I don't know. Let's see. Can I move this over here? No, I gotta move this whole thing over. Alright. So this is the diff PT config diff, between Aurora and EC2 box.

**Marcos Albe:**  
Oh, the adaptive hash index

**Nando Camargos:**  
The number of buffer pool instances is doubled on the EC2 as well. The adaptive hash index set Yeah, I is unable

**Marcos Albe:**  
you told me that the right workloads were better. But that's your read workload that is killing you. And you know if you have range scans because you don't have indexes, that will make your adaptive hash index super useful. And it will give you quite an edge. I'm not sure if it accounts for like 4x kbps  but

**Matt Yonkovit:**  
So I wonder why they have that off by default. 

**Marcos Albe:**  
I don't recall if you can actually make it.

**Matt Yonkovit:**  
I'm actually looking and I don't even see it in the parameter list.

**Marcos Albe:**  
Well, but it has this one.

**Matt Yonkovit:**  
No, no, no, that's it's 2020 gigs versus eight. Okay. Yeah. So it's smaller on the EC2.

**Marcos Albe:**  
And also has disabled change buffering. Right?

**Matt Yonkovit:**  
Okay, so adaptive hash index, not available on Aurora. It looks like I can't find it in the parameter list.

**Marcos Albe:**  
It's mostly changed. Change buffering. It's also gone.

**Matt Yonkovit:**  
They don't look like they have it.

**Marcos Albe:**  
Disabled change, buffering will also have an impact, because as we have to update more pages in the tree, every time you write the commits are gonna have a lot of latency. And also, there's gonna be more locking on the tree, and that some of that locking is actually slowing down the reads.

**Nando Camargos:**  
several small things that might compute big differences. Well, right, the number of tread seats, it's just one on Aurora and four EC2 instances. They don't have that. Well. Yeah. Read IO threads as well, it's double on the EC2

**Matt Yonkovit:**  
But I mean, seven times you think any of those could be seven times?

**Marcos Albe:**  
Noticeable difference for particular read workloads? Yeah. Changing between traversing the b-tree every time to just go through the hash, right? Like, which is constant access speed versus logarithmic axis.

**Matt Yonkovit:**  
Yeah, and I and a lot of these are range scans without indexes right now, because like I said, it's kind of a craptastic thing. I know that Oh, I purposely processing

**Marcos Albe:**  
now then without indexes. No, because, yeah. All well, we'll make the primary key also hash. I'm not sure if I know, the adaptive hash index will for certain make secondary indexes a hash, but I'm not sure it will do it for the primary key. I believe it must do it because we're not now.

**Matt Yonkovit:**  
Anything's possible. I mean, I don't know. I don't know. I don't know. I didn't. But no, that's it. That's that list, right? I mean, there are a few things you could tweak. Obviously, there are some things like that aren't untweakable. You know you just have to accept what they are. It's really interesting. Because my first test with Aurora 8, just so you.

**Marcos Albe:**  
Also, you have freight handling. You have thread pools and versus one thread per connection.

**Matt Yonkovit:**  
oh, that could be a huge one, because I'm spinning up about 25 connections, like active like hardcore hitting the system. I mean, that's, that's, I guess, that number,

**Marcos Albe:**  
if you match the number of CPU cores, of the instances,

**Matt Yonkovit:**  
Maybe? Yeah, maybe. yeah,

**Marcos Albe:**  
What's hard, and, and I want to ask Alexander Rubin, because he's now I think he's still at rds. And I want to ask him if they could make available the flame graphs as part of the cloud watch flame rep for your instance, in cloud watch, because that's something we mean so much, right? Like, that's a very useful tool. And once again, as we use with great success on a weekly basis, right? That and backtraces the profiler. Those are tools we truly, truly need many times to do advanced performance diagnostics like this, and that it's not possible to do in rd. So I think I will reach out to him and check if he'd be willing, to push for that inside RDS because that will make it so much more friendly. On the other hand, I'm not sure what I would do with RDS and Aurora because I don't have the source code, because they're not open source. So like, I will not be able to tell what I mean by the name, you can infer things. But it's not the same as looking at the source code. But

**Matt Yonkovit:**  
Yeah, yeah, no, I understand. But anyway, there are some potential things there. It's just yeah, right. Now, if you look at the last iteration, it's 1000 versus 75. I mean, that's a massive difference. it's just, there's something that's, that's there that's with this specific workload. And I can change the workload now. And you'll watch it as you adjust. Like, I know that if I dropped a couple of the threads, the workload just soared. So there are things that are blocking and it's preventing things from getting through.

**Marcos Albe:**  
Well, the point that is killing you is selection, right.

**Matt Yonkovit:**  
Yeah, you wanna share your screen, and I'll try that.

**Marcos Albe:**  
We're, where do you share the screen with this thing?

**Matt Yonkovit:**  
The little laptop thingy.

**Marcos Albe:**  
Oh, he wants me to apply your updated settings below. if I reload it. Will I find that? Oh, yeah, no, please. No, it doesn't.

**Matt Yonkovit:**  
So it should request it. Oh. 

**Marcos Albe:**  
So do you see my screen?

**Matt Yonkovit:**  
Oh, hold on a second. It just came up. There we go. I'm gonna get rid of I hope I can get rid of Marcos too. Yeah, there.

**Nando Camargos:**  
We deal with this personality just from Marcos on a day to day. Yeah.

**Marcos Albe:**  
So I took the same time range you took in the last three hours. I selected the cluster here. I flew down here. Yep. I didn't bother with filtering by schema, because 97% is on that movie's check. And then I sort by credit time, and I look at the round one bit, and this guy took 3.08% of the load out of 61. Total. So I will go to that one first. And explain what is this gonna explain to us? So essentially an index scan.

**Matt Yonkovit:**  
Yeah, so to tell you the table structure here? There is a I don't believe there's a there's a index on here. I believe it's only on the rating index on the IMDb Rating. So if you look at that query itself. It's an order by rating. Yeah, it's ordered by the IMDb Rating. It's but it's a Select is on for a specific year and year is not part of that index. So it would probably be more efficient to have a year and IMDb Rating index. So let me go ahead and let me add that very quickly.

**Marcos Albe:**  
Yeah. I could not immediately explain why. I mean, it's reading a lot of freezing. Let me see. Well, reading so many 50.

**Matt Yonkovit:**  
Yeah. Yeah, it's limited to 50. It's limited to 50. I'm gonna go ahead and add that index now. So we'll see. And I'll do it on both instances. So that way we keep them consistent. And I'm gonna go ahead and edit the year and IMDb Rating. So that should take care of the sword as well. Right? Yeah. It's probably gonna walk up because that system is pegged to the max because that's how we roll here.

**Marcos Albe:**  
Yeah, it was certainly selected. Now, to explain why they are costing us so much.

**Matt Yonkovit:**  
Weird is like the other instance has it. Right. The other instance still has at that same query, and it's still doing the exact same

**Marcos Albe:**  
but, that's what I'm telling you. It's like taking action. explain why the selects became so costly here, I will need to do a flame graph to actually see where CPU time is going.

**Matt Yonkovit:**  
Oh, okay. Yes. Which is problematic with the Oh, what was that?

**Marcos Albe:**  
If this has a subquery, but no, it does not.

**Matt Yonkovit:**  
Yeah, it's a very straightforward query. It's not like it's, it's not like it's crazy, right? It's pretty straightforward, you know? Pretty straightforward setup.

**Marcos Albe:**  
You need to up tune your Max user connections for the given user.

**Matt Yonkovit:**  
Oh, are we getting PMM user error? 

**Nando Camargos:**  
I wanted to ask you, Matt, how many cores do the instances have for each?

**Matt Yonkovit:**  
So there are four core ones, one is 16 gigs. One is 32. Yeah, there are n fives I believe. extra larges? I think. So okay, so those things are running. But it's taking an insane amount of time because the systems are so busy. So what I'm going to do is, I'm going to reduce the workload for a second to let those go through. If you guys haven't seen my fancy pants tool, there's a JSON file that has all the workload defined and you change the JSON and then everything just adjusts to whatever's in the JSON.

**Marcos Albe:**  
Let me stop. And you can share, so you can show us

**Matt Yonkovit:**  
So, stop sharing for a second. So I can share and I can just throw over my shell. So there's a directory that has these JSON files in it. And here, if we just set the workload, there's different types of workload that that's in here. And we have the ability to change this to be basically like a website workload, which is Internet Movie Database workload, just like selecting some very minor inserts. We can report workload. So with analytics, we can also do comments, which is like a chat system. So that's heavier insert updates. We can also put long transactions if we want to see what the impact is if somebody's doing a select for update. That's what that does. And it holds a lock for somewhere between one and five seconds. And then we read only workloads and then we can do multi row lists. And then we can also, we have a special workload, which is if I want to stop experts, I can add things into the list of functions that I can throw things in there that will run under special workload. But just altering this file enables the workload to change.

**Marcos Albe:**  
Look at the load. Oh, no, no, no. What does that look like at the load on Aurora?

**Matt Yonkovit:**  
Alright, hold on. Let's see. So where are we? Oh, down to 12. Yeah, so we are pegged out here. So anyway, I haven't made this change yet. So let me go ahead and I'll, I'll stop sharing. And let me go ahead and drop down some of this workload real quick. So let's drop to zero. And so if I make changes to this file, this should go down pretty drastically, pretty quick. So if you're watching at home, let's watch. I just adjusted that file. I guess I can reshare my screen. We should see The workload take a pretty heavy dip there from an Aurora perspective, so I left that easy to one alone. See, that's not the right one. So let's look at this guy. He does the same. Yes, they are. But so I want Aurora, Aurora. So here we go. Let's see what we got here in the last 15 minutes. So queries per second obviously got dropped, because of the alter the number of connections, I'm guessing we're gonna be backed up for a while. Everything's gonna be locked. Let's see. Let me go.

**Marcos Albe:**  
How big is that table?

**Matt Yonkovit:**  
400,000 rows. I mean, this, the entire dataset fits into memory. The entire data set, it's so tiny, like it's less than a 10 gig total database,

**Nando Camargos:**  
then it doesn't really make a difference. They did double the memory that Aurora has, right?

**Matt Yonkovit:**  
Right. That's why it doesn't make any difference. That's why I didn't care. Aurora is a word kind of weird that way where you can't choose the exact same instance sizes. So we're starting to see a rebound here. And if I go look, did that finish? No, it's still running. So yes, so hopefully, that will clear out one of the interesting things when I set this up. Here's a fun factoid. So Aurora allows you to take an easy instance, an upgrade from or from a dump, or from a backup or from another RDS instance to move to Aurora. But the latest RDS instance is 8026. And so I had an 8026 running, this Aurora is built on 8023. So you can't actually do a migration from RDS to Aurora. Because it has a mismatched version, which is a pain in the rear. Because I had this running with RDS before eight came out. And so I wanted to do that upgrade and I could not, so I was like alright, so while that is running, did you see anything else Marcos that that?

**Marcos Albe:**  
You know, I can certainly screen but I haven't seen anything that will give me much of a hint. Let me share 

**Matt Yonkovit:**  
and we're back to Maco’s Screen. Right?

**Marcos Albe:**  
So this is the Aurora movie instance. Last three hours

**Nando Camargos:**  
you should probably look at the last 30 minutes to 15 minutes. Marcos if you're comparing the recent change,

**Marcos Albe:**  
Yeah, well, here it comes through. Now it's gonna be much cooler. Is thinking more rows.

**Matt Yonkovit:**  
Right now. Right now? It's because it's building the index, right? Oh, it's doing indexes. Oh, yeah. So yeah, 

**Marcos Albe:**  
No, no, I don't think that's the index. Rows deleted. Ah, maybe not. Maybe. Let's see the rows read. It plummeted from 2 million to 500. Okay, and let's see MySQL instance memory

**Matt Yonkovit:**  
All right, I'm just gonna, for the sake of time, I'm gonna force this to restart.

**Marcos Albe:**  
Hey, I doubled your qps man.

**Matt Yonkovit:**  
Yay. All right. So that's because I just restarted the whole workload. So let's go ahead and run and we'll run again

**Marcos Albe:**  
Look, do you have your admin commands? Hidden those workloads. But it's doing more work.

**Marcos Albe:**  
I think it's doing much more work.

**Matt Yonkovit:**  
Um, yeah, give it a second here. I gotta do let's see two, two, I gotta reset the workload, I've, because we, we changed it. Now I gotta go back. And oh,

**Marcos Albe:**  
you actually have it to the hand. Okay, I thought you were just showing.

**Matt Yonkovit:**  
Yeah, no, I actually get to see if I could just reduce it enough to get that. That's true. So now I just need to go back and reset it to what I had up to before we have these 

**Marcos Albe:**  
So we don't have much in performance schema this

**Matt Yonkovit:**  
Okay, so now, we should be starting back up now. So we've got

**Marcos Albe:**  
so. shut it exclusive logs appeared to be.

**Matt Yonkovit:**  
So we do have the indexes now added on both and the workload should be back to what it was a bit ago. But again, there's a bit of delay. So it'll take a minute for PMM to start to show the metrics.

**Marcos Albe:**  
More than double.

**Matt Yonkovit:**  
Yeah, I mean, so that was, which is the one index. But again, if we compare that to because we added it to both. If we compare that to the EC2 instance.

**Marcos Albe:**  
Yes, kill faraway?

**Matt Yonkovit:**  
So I mean, there's something else that's weird. With that particular workload,

**Marcos Albe:**  
there is something that its hash table looks like. And index three Read Write looks. And those fell sharply after we added that index. So apparently, our role is taking some synchronization locks. These are related to synchronization while doing the scans on select. 

**Matt Yonkovit:**  
Yeah,

**Marcos Albe:**  
 I mean, plummeted after we are the index. So they must have been related to that table scan to that index scan. And while it was doing the index scan, it was holding shared exclusive locks. Apparently, or what not rather, someone that wanted to acquire a sharded exclusive lock had to wait behind those locks.

**Matt Yonkovit:**  
Which could have been the alter table right to add the index? 

**Marcos Albe:**  
No, no, because again, this is all the time. This is true or false? Yeah, we Yeah, that the index was. I mean, we've been doing that for the last hour.

**Matt Yonkovit:**  
Yeah. Around here, right. Like you created the index here. Yeah. 

**Marcos Albe:**  
So, again, what code is leading to this? I really need to at least pull my profiler. Some samples of backtraces.

**Matt Yonkovit:**  
Yeah, but it's interesting. So if you know just looking at Aurora right now versus the EC2, just that one index triple The queries per second, we're getting about 215 When we were getting around like 70, before

**Marcos Albe:**  
you know, um, transaction. But this is so little piano. Because you know how in Aurora, if you do very large reads, on the secondary, you're actually blocking purging and creating a history list on the prayer really. Okay. So that might also have something to do, right, like, those long reads are actually meddling with the Undo. Because they do have an open consistency view. And while they're running, even if they're not within a transaction, they do require, did you have to repeat all read here?

**Matt Yonkovit:**  
Default, whatever the default is, I don't, I don't know what it is.

**Marcos Albe:**  
It must keep going ahead and deploy. We've committed it's that I

**Matt Yonkovit:**  
I could, ah, I'd have to redeploy code. But I mean, that is something that I could try. We could follow up and see. But look at that difference. I mean, there's a huge difference just with the one index, which Yeah, you want to properly tune, but still,

**Marcos Albe:**  
it was running fine before, like my beloved customer said, um, but I, again, I don't have the insight to actually give you a full answer.

**Matt Yonkovit:**  
But it is interesting to look at that and to see, like, some of the things that are turned off, right. So like, when we were looking at the list of differences there are things that are just disabled, and not available as part of Aurora. And it's so interesting that I can get that same workload like throughput with certain queries, right, like, so if I, if I change the workload to be identical to, like, just a website workload, perfect. Like, like, actually, Aurora just shines. It's great. But when I start throwing in some ones that are a little bit hairy, like, like the query where I'm saying, like, Hey, pick the top 50 movies, for a given year. I mean, that's not that here. He really, I mean, that's a common like we think that that's pretty normal. Right? So I know, you're gonna say something like, cut you off?

**Nando Camargos:**  
Oh, no, no, I was just curious, because said, we were looking at a PMM. And we were discussing that they are, he might have made a difference EC2, right? And we could have our answer right there. We just had to check that the graph is disabled.

**Marcos Albe:**  
You could disable MySQL. You have disabled on the Aurora, go ahead and disable all of MySQL to make a more fair comparison.

**Matt Yonkovit:**  
So add thread pools, try it, then go ahead and turn off. Change buffer, adaptive hash, yeah, adaptive hash index, and see if I can, basically instead of trying to get Aurora to match the MySQL instance, see if I can get the MySQL match instance to match Aurora. Yeah. Yeah. So the opposite way. Yeah. That's an interesting approach. Yeah, yeah.

**Nando Camargos:**  
Yeah, it's unfair, right? Because Aurora has its own optimizations that are done under the hood. And

**Matt Yonkovit:**  
it's true, it has some things that it performs better. 

**Nando Camargos:**  
Yeah. And that's what limits them to actually do all that MySQL is doing. Right. So yeah, yeah. But the comparison, I mean, the difference is, is very, very big, I wouldn't expect that much Matt.

**Matt Yonkovit:**  
Well, in this case, like, you would need to double the box size in order to get the throughput that you need minimum, and I don't even know if that would work, which means doubling the cost, right. Like, I mean, like, like if you're if this was your legitimate workload and you were running, the only option would be to upgrade. Yeah and it's, it's, it's interesting so as we're looking at these things, and I think this gets back to a theme that I'm kind of hitting on this year, I think that this is my, this is my new year's resolution, everyone. Okay, my New Year's resolution is that small things matter immensely. And it's probably things you won't even think about, right? and in the case of the Python thing that we were talking about earlier, right here I am running Python 310 versus 397. So it's like, that's a pretty minor upgrade. And there is that drastic of a performance difference. Same thing with I decided to use the official Python MySQL connector. Again, these are things that there are so many components in our applications. Now, to test all the permutations is nearly impossible. And you probably have four or five of these things that seem very minor that are probably just destroying your systems and you don't even aren't even aware of it.

**Marcos Albe:**  
Look, the first latch is what actually kills the workload.

**Matt Yonkovit:**  
Oh, here, I'm going back to your shared screen. Oh, sorry. Here. Yeah. Okay, so what are you looking at? 

**Marcos Albe:**  
Oh, man, I was looking at the wrong graph. Apologies. 

**Matt Yonkovit:**  
So you made me flippy turn you on for nothing. Like

**Marcos Albe:**  
I needed some attention. I spent seven hours listening to someone else's voice. Oh.

**Matt Yonkovit:**  
Is that when you have no hair? You pulled out your hair during that session?

**Marcos Albe:**  
Yeah, no I thought that the first latch that I actually had confirmed that it was affecting, but I don't see the impact on the MySQL questions now that I look back here. I turned Yeah. But it was looking. It was going down. But it was not going down so much.

**Matt Yonkovit:**  
Yeah, I mean, it has improved, right, with an index, which is great, which is what you'd expect. It's just, it hasn't improved to the point where it matches the other stuff. And like I said, if I mess around with the workload, I can get them to match. It's just that I have to change the workload.

**Marcos Albe:**  
We still see these two right there. They're still there.

**Matt Yonkovit:**  
What are they here? It's kind of fuzzy. I can't see what they are.

**Marcos Albe:**  
Say that again?

**Matt Yonkovit:**  
I can't see what those lines are. They're kind of fuzzy on my screen. I don't know. Okay. Yeah. Yeah.

**Marcos Albe:**  
InnoDB has a table that looks easy. Put them to make them larger.

**Matt Yonkovit:**  
Yeah, it's just, I think, a bad connection. Marcus. So yeah, you're, you're pixelated.

**Nando Camargos:**  
They shut off that display. Yeah.

**Marcos Albe:**  
Hash_table_locks, and index_tree_rw_lock, which are synchronization primitives. I don't mean, I don't get why we have a hash table. I need to look at what that's protecting. And the index tree is obviously protecting B-tree. And this is on the redo on the Undo. I mean. But yeah, I mean, these two were the ones that came down. And we kind of serve that throat to increase it when those come down. So I will blame those and go to the source code and find out what they are about.

**Matt Yonkovit:**  
Right? Yeah. Um, so interestingly enough, look, go ahead and from the Aurora instance switched easy to real quick. Like, like, yeah, so just the server's name goes to the Yeah. Meetup MySQL, ec2 go to those same graphs and see if those same locks appear there. Okay, let me go here. Yeah, let's see. I mean, if those are missing, or those aren't the ones that are popping up to the top, when you look here, it

**Marcos Albe:**  
its handler, which is one of the popular in, in Aurora. Client, but

**Nando Camargos:**  
The other ones not there. Yeah.

**Matt Yonkovit:**  
Well, yeah, the other ones aren't there. So those are new. Those are Amazon-specific, I guess, right.

**Marcos Albe:**  
No, no, I don't know. 

**Matt Yonkovit:**  
Yeah, I mean, like that, that, that, that. Oh, if you will? 

**Marcos Albe:**  
Yeah. Yeah, exactly how nice workload is on a specific

**Matt Yonkovit:**  
Yeah, that's what I meant. It's like, like, like that outcome appears there. I wonder if there's, yeah, I don't know. It's very strange. No, no, but this, this was actually really good to be able to go in and look at this stuff and see, like what, how you look how you tune, but it also highlights why some of these systems are so fragile, when it comes to the different database components and also the different application components, how they interact with one another. I mean, like I said, if I change the workload, and what I'm going to do is I'm actually going to Run like 10 different workloads, I just let them run overnight. So I'll run like an hour of reading, Only an hour of writing, only an hour of this. Now just let them run overnight and see where the performance gaps are for each one of these, and maybe narrow down a little bit more even to what's bottlenecking. I think the bigger concern or the bigger problem that I see is I wonder if this does have something to do with the thread pool or something just because the queries are the same. It's just they're getting blocked in and they're getting stuck at some of those slower queries. They're still slow and in EC2 they're just not getting blocked. So I'm wondering if it might be a thread pool thing. So I think I might try to disable the thread pool.

**Marcos Albe:**  
Again. Instead of that, do the READ COMMITTED first, I will repeat it first. Because again, there is this thing about how I would order replicates through the redo log.

**Matt Yonkovit:**  
And but would recommit still impact a read-only workload or, like it shouldn't flip it to read-only know,

**Marcos Albe:**  
you know, again, here we see that the read workload was fiddling with synchronization primitives related to read-write locks.

**Matt Yonkovit:**  
Well, this workload that we have running right now is mixed. So there are writes and reads so yeah, I mean, that's just the normal. Anyways, okay. Fair enough. We have a couple we have a couple things, try and see what happens. I hope everyone who's been watching has enjoyed this. This was, this was fun for me to dig into some of this. I don't know if, I don't know, Marcos and Nando if you found this educational and exciting.

**Marcos Albe:**  
Absolutely. I love this, this asked me anything, and like having open conversations, I really, really like these meetups. And I was going to tell you, in February, when I'm back from vacation, we should do those barbecue shows you have, I'm gonna have my barbecue in good order. And so I'm gonna be able to set up a camera there. And we can have these conversations well, also having some cooling.

**Matt Yonkovit:**  
So I don't think this has to do with a small buffer pool size, just because we've got a 20 gig buffer pool. And everything should be fitting into that buffer pool. I mean, like, it's a 10 gig dataset. So it's not huge. Maybe I'm but how many? How many buffer pools? Did it have that was it for this? Yeah, for instance? That still doesn't seem like I mean, even so with 20. That's five each? I mean, it's possible, I guess we could again,

**Nando Camargos:**  
We have a four-core so it's kind of Yeah. What else?

**Marcos Albe:**  
I mean, again I look at that. Everything else I looked at in InnoDB didn't tell me much. Right? Yeah, pretty much from the InnoDB metrics implementation. So the one thing we did find was in the performance schema. Hash table locks 30 Go. Thank you.

**Matt Yonkovit:**  
Yeah. But the only thing is that this workload, it shouldn't be reading from things outside the buffer pool. I mean, this workload has been running for like 12 hours. So if it's not warmed by now, yeah, there's another problem there. Right. I mean, the same thing with like like, it's the exact same time as the other instance as well. So, I mean, it's possible that it takes just longer to warm on Aurora. That's a possibility, I guess. Yeah. Anyway, Um, but thank you, everyone for coming. We appreciate you. We read the questions.

**Marcos Albe:**  
It really was. It was reading from disk. Yeah, I guess I didn't even check here because it was like, Man, you told me you have 20 gigabytes and the database is less than 10 gigabytes. it just simply didn't look at that. You are misleading me.

**Matt Yonkovit:**  
It is. It's not warm by now. And I did a load from my school dump and everything should be pre-warmed, unless you're doing something really funky.

**Marcos Albe:**  
Well, read requests is, oh, this buffer pool reads that. Wait, let me check buffer pool IO

**Matt Yonkovit:**  
Marcos doesn't want us to go. He wants to have to hang out all night. Yeah. I mean it's dark where you are you're like like, Let's go another hour. Who's up for another hour? We all are hourly.

**Marcos Albe:**  
I'm totally into it. This one has too many dashboards. sections in these dashboards?

**Matt Yonkovit:**  
Yeah. Yes.

**Marcos Albe:**  
No, yes. syrup's. So it's not really from disk. I don't know why.

**Matt Yonkovit:**  
So so yeah. So. So yeah, it should be like 100%. Yeah.

**Marcos Albe:**  
Yeah. So I don't know why it's showing us that.

**Matt Yonkovit:**  
Yeah. Unless it's trying to do something, like funny behind the scenes to keep the cluster in sync.

**Marcos Albe:**  
Yeah, but even it could be related to the way it replicates.

**Matt Yonkovit:**  
Yeah, I guess another option is I could create an aurora instance without a replica. Oh, I don't know if that would make any difference.

**Marcos Albe:**  
It probably does.

**Matt Yonkovit:**  
So, all right. No, it must.

**Marcos Albe:**  
It must wait for the other guy to say I didn't get the piece of redo log or, well, it's sharding storage, actually. Right. Yeah. I don't think that makes a difference. No, yeah. Gotta try it. Anyway!

**Matt Yonkovit:**  
All right. Well, thank you, everyone. And we hope you appreciate the bald Marcos and the rest of us trying to troubleshoot some interesting things. We hope you've learned some things. Obviously, we threw a couple of curveballs out there some things we're still not 100% Sure why things are acting the way they are. But we did have a pretty good call today so thanks for hanging out. If you haven't subscribed to the channel like us, reshare tells people to watch the replay. Maybe we can get somebody from Amazon to come and tell us you know what I did wrong and tell me that you're just an idiot Matt, you should do it this way. And I'll be like, cool. I can fix it, you know? But you know it is something that is interesting to dig into some of these problems and see them in real-time so

**Marcos Albe:**  
Reach out to Alex Rubin Have you had a Have you have seen in one of these episodes already

**Matt Yonkovit:**  
we can ask him we can you know we can have Mr Rubin calm and he can I control this and I can be like, Alex fix it. Yeah, but unfortunately working for Amazon. I wonder if the Amazon guys have a turbo button behind the scenes. Like, let me just log in here and hit turbo on that. 33 megahertz. Yes. Yes. But yeah. All right. Thanks, everybody. Good night, everyone. Right? Yeah, have a good one. Bye-bye.



![Percona MeetUp for MySQL December 2021](events/percona-meetup/mysql-december-cover-1920.jpg)

Our experts will reveal more secrets of the stars to resolve any open source database performance issue. Join this Community MeetUp for MySQL hosted by Matt Yonkovit to discuss Database Tuning and Troubleshooting with Marcos Albe and Nando Camargos. All along this 1-hour talk, you can participate and ask any questions and get an answer right away.

## Join us for an hour MeetUp for MySQL

* Day: **Wednesday Dec 8th, 2021 at 5:00 pm EST/ 11:00 pm CET**
* Live stream on **[YouTube](https://www.youtube.com/watch?v=i4DG30guHmA)** and **[Twitch](https://www.twitch.tv/perconalive)**
* Add this event to your **[Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NG9scmd1YWhhbDIzNnV1NTNvYTNpcjRjaXIgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)**

## Topic 

**“Database Tuning Secrets of the Stars” by Marcos Albe and Nando Camargos**
* Support Cases From Hell 
* AWS: Troubleshooting on RDS/Aurora
* Q&A: Stump the Expert!

**Marcos Albe**, is currently working as Principal Technical Services Engineer at Percona. He has participated to the [Percona podcast The HOSS Talks FOSS 22](https://www.youtube.com/watch?v=ZRVmdru5jTI)

**Fernando Laudares Camargos**, called Nando, is a Senior Support Engineer at Percona. He brought a talk about [Inspecting MySQL servers: The Percona Support Way at Percona Live 2021](https://www.youtube.com/watch?v=n1gWso3HDyw)

## The MeetUp for MySQL is recommended for: 

* User of MySQL
* Student or want to learn MySQL
* Expert, Engineer, Developer of MySQL
* Thinking about working with database and big data
* Interested in MySQL

**Go ahead and come with your friends!**

## All kinds of feedback are welcome to help us improve upcoming events