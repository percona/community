---
title: "Installing MySQL and Setting Up a Default Configuration - Percona Community MySQL Live Stream & Chat - April, 1st"
description: "Listen to this recording of Percona Live Stream of April 1st, 2022 to learn how to install MySQL and Setting Up a Default Configuration with Matt Yonkovit and Marcos Albe"
images:
  - events/streams-mysql/Stream-MySQL-1-cover.jpg
draft: false
date: "2022-04-01"
speakers:
  - marcos_albe
  - matt_yonkovit
tags: ['MySQL', 'Stream']
---

Watch out this recording from Percona Community live stream of April 1st. Learn how to install MySQL and Setting Up a Default Configuration with Matt Yonkovit and Marcos Albe. This is a series of live stream to discuss MySQL tricks with experts.

## Video

{{% youtube youtube_id="AMGNklpAjJ8" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
We might even be live right now. Marcos, we might be live oh we are live oh we see now we're live there we popped in. So Marcos has been power drinking right now to stay hydrated for the stream. So, yeah, he's been sitting here pouring as much as he can into himself to prepare himself because one of the most important things about streams is to stay hydrated during it. Right?

**Marcos Albe:**  
 Properly caffeinated, right?

**Matt Yonkovit:**  
Yeah, well, proper, properly caffeinated, but also stay hydrated, so you don't get dehydrated and have all kinds of other issues.

**Marcos Albe:**  
Make sure that your throat works properly, right?

**Matt Yonkovit:**  
Right, because there's a lot of talking and why not. So hello, everyone out in-stream land, we are happy to have you here on a Friday. It's Friday morning for me. So we are still early in my day. But for some of you, it might be getting close to the end of your day. So welcome to the stream. And thank you for following. And we would love for you to hang out with us over the course of the next several months or the next year, I have actually commandeered Marcos from the support team. So we've pulled him away once every two weeks, for the next 26 weeks. So for the rest of the year, Marcos is going to be my co-host. And we were talking about renaming the stream the m&m club, or something, for the Matt and Marcos show here. So we hope that we will continue this. But our goal is over the course of the next 26 weeks to do everything possible. With a MySQL database. We want to start with the basics today of installation, go through tuning, go through backups, go through high availability, setup, go through geographic redundancy, go through migrations, like everything possible that someone as a DBA, DBRE or developer might have to do with their database. We're going to show you how to do it. And we're gonna start today with what Marcos built. So if it doesn't work in three or four streams from now, it's all his fault. So he can't blame me. It's all going to be on him. So should be fun. Right? 

**Marcos Albe:**  
Well, I'll take that responsibility.

**Matt Yonkovit:**  
Yes, take the responsibility, Marcus. So, but anyway, we're happy you could join us, if you are joining us out there in-stream land we are excited, we're going to be in person in another five weeks or so six weeks or so we're going to be in Percona Live. So we would invite you to come on and hang out with us at Percona Live as well. Actually, I don't know if you knew this, Marcos, but they've given me a live stream booth for Percona Live. So I actually have a booth that will have like walls and stuff in the expo hall. So we can do live streams directly from within Percona Live. So we might I don't know if it's you or Charly because we're alternating every other week. I don't know who's gonna be on deck for that week but you can come on. Come on anyway. So we'll do an extra special if we don't have you on.

**Marcos Albe:**  
We can do a beer & sun stream.

**Matt Yonkovit:**  
Oh, yeah, we can remove yours. Yeah. We could get like the flutes and we can try each time and we can rate them. That could be fun. I don't know if he wants to do that. I mean, I don't know. Is that is that allowed?

**Marcos Albe:**  
You know, it sounds like an interesting plan. Yeah, I'm super excited about attending Percona Live one more time. That's going to be great fun. I was looking forward to this for the last two years. So

**Matt Yonkovit:**  
yeah, I mean, COVID Damn, Yo, COVID. Yeah, exactly. So people love to hear us banter back and forth, I'm sure. But they're really here to watch the technical stuff. So without further ado, let us start our journey of the next 26 weeks, the next year, the year with Marcos, the year of MySQL with how do we install MySQL. And let's start with that and we're gonna install it and we're going to configure it from scratch and we're going to talk about why we're configuring certain things based on the hardware. And this would be what we would recommend people go through as they're setting up a new instance and we'll go from there.

**Marcos Albe:**  
I will share my screen.

**Matt Yonkovit:**  
Let's see that beautiful shells screen there.

**Marcos Albe:**  
Oh, can you see Shells?

**Matt Yonkovit:**  
We see hello world. Now, what's funny is Marcos has a negative feeling towards Ubuntu so generally for the live streams, I've been defaulting to the latest version of Ubuntu, but he is such a fan of the band formerly known as CentOS that we had to find something that was close to it. So we chose rocky Linux for our distribution today. And this is running on EC2, it is a five, two XL, so it should be eight cores. 32 gigs of memory, if I recall. So.

**Marcos Albe:**  
So yeah, this is nice, because I really never did a setup on Rocky. So surprises might be ahead. I'm just gonna start.

**Matt Yonkovit:**  
Yes, I gave him a bare-bones installation. There is nothing here. Right? Like, he's going to have to do everything. I don't know what is set up I gave them I set this up yesterday. This is all about

**Marcos Albe:**  
You know, the real stuff.

**Matt Yonkovit:**  
This is the real stuff. So you're gonna see exactly all of the missteps, all of the goodness, everything. From the bare bones. This was selected the AMI hit the start button. Give him the key.

**Marcos Albe:**  
The first stuff I will do in a machine that I don't know as you gave me is like a basic description. But anyway, what we'll do is go ahead and just run pt-summary very quickly.

**Matt Yonkovit:**  
I don't know what the default is? Like, like, I don't know, like, I don't know, I have no clue what will be installed.

**Marcos Albe:**  
I'm happy with it. I'm happy with this.

**Matt Yonkovit:**  
Well, I mean, I'm wondering if you're gonna probably have to install it probably have to install if you want to use it, like the Percona tools, you'll need to install the MySQL drivers in the clients and staff as well.

**Marcos Albe:**  
Yeah, I'll do all of that.

**Matt Yonkovit:**  
It will be fun! screen not visible.

**Marcos Albe:**  
Is the screen not visible?

**Matt Yonkovit:**  
Oh, how was the screen not visible? Let's see,

**Marcos Albe:**  
I am showing the screen. I see it on my own.

**Matt Yonkovit:**  
Let me double-check that I just saw this, please. I'm going to check it out on YouTube. Just real quick, just to make sure that it's streaming the right way. It should be. Hold on, let me see. Yep. Oh, it's nice. I see the screen on YouTube? Not 100%? Sure. So I do see pt-summary. I see it in the stream. So I'm not 100% Sure. Hopefully, you can see this on the screen now. But I do see it on all of the different live-streaming platforms. I'm just double-checking, keep continuing on Marcos.

**Marcos Albe:**  
Okay, I will move on the first thing I do on basically any machine I get to work with is I will very quickly check pt-summary to know what the kernel looking at, have an idea of CPUs memory, and then have some idea about the size and file system.

**Matt Yonkovit:**  
I was right, right. So, eight cores and 32 gigs of memory.

**Marcos Albe:**  
And then okay, it's I just checked some very basic settings, we're going to go back to these posts into the installation to go through them a bit more. And then check if there's any load in there, the recent, we're gonna go back to this as well. So again, I just wanted to look at the basic hardware specs. Once I have that I want simply, first of all, I'm going to be doing all this with the Percona Server. So first of all, I'm gonna install our own repo. So here it comes. You can get this URL from our documentation online. This Percona release installed tool is called Percona release. And this tool helps you enable and disable the different repositories we have for our different products. In this case, I'm going to be working with Percona server 8.0, and we're going to progress through that and we're going to later set up high availability in different ways using the Percona server. So let's start and it tells me that in Red Hat 8 we Gotta disabled the DNF modules for MySQL. So yeah, I'm gonna say please do it. So, yes, I've integrated the smartness.

**Matt Yonkovit:**  
So for those who aren't familiar, the Percona server is a drop-in replacement for standard MySQL, it includes extra features. So we have to disable this standard MySQL or the one that would come with the installations by default. So we can then use the enhanced version that we have

**Marcos Albe:**  
correctly. As you can see here, this is all he did for me, enabled the Percona Server and Percona tools. So now if I do yum search Percona. And then it's hard to type.

**Matt Yonkovit:**  
Well, yeah, the problem is, like, honestly, like, when we, when we talk about typing, it's always worse when you're live on camera. Right? Like, if someone's looking over your shoulder, I find that like, I lose 90% of my typing ability.

**Marcos Albe:**  
Yeah, it's like 70% more chances to, to finger It's alright. You can see, a bunch of packet packages became available, I'm gonna be setting up a basic client-server, and I'm going to set up the back info. When this is one thing I tell always people, like when you're installing MySQL, please, please do yourself a favor and set up the debug info packages. Because when a crash happens, or you know database or any other system that you have to manage, and then you have to troubleshoot debug info is gonna make the crashes, more meaningful, when when the error happens, and you see a backtrace, you're going to get meaningful, human-readable output instead of hexadecimal gibberish. So that's the important part, then we'll shut up libraries are going to be automatically included. And I'm going to probably still connect, so a calculator. So I'm just gonna go ahead.

**Matt Yonkovit:**  
Yes, for those who are looking at the screen, there are a lot of other packages. And we can go through those as the streams come on. So for instance, MySQL router, or shell, the route

**Marcos Albe:**  
I can go, I can go very quickly, I think it's interesting to know. So the router is the MySQL router, it's a late layer, with four TCP brokers. So it's basically just forwarding packets back and forth. It does monitoring of the instances to which it's routing traffic. But it's not like proxysql, which is aware of the problem of this sub-layer four, so it doesn't know the protocol. But it is an essential part of the InnoDB cluster. And hopefully, we're going to look at that later, when we do the HA side of these exercises. Then the MySQL shell is the new MySQL client interface. It's the future MySQL, so now you type MySQL, and you get the command-line interface for MySQL. Well, this is an advanced command-line client, which supports JavaScript, SQL, and Python, if I recall correctly, and has really, really nice utilities to simplify many DBA tasks. And it's also an essential part of the InnoDB cluster, the Percona release, well, this is our release, this will create the definitions for our repositories and set up the Percona release tool to manage those repositories. Percona server-client brings all the client packages mysqladmin, MySQL, and a bunch of other client software that connects to the server and allows you to do stuff with it. Then the debug info is again, the debug symbols for the Server Developer headers, if you're if you want to compile stuff, or if you're developing modules, or whatever, you're going to need the develop development headers, and

**Matt Yonkovit:**  
you need some of those as you sometimes install libraries for different programming languages. So if you're using something to build Python libraries for MySQL, like that MySQL connector or something, or go those are potentially going to require the devil libraries.

Right. And then RocksDB is the of course RocksDB engine, it comes as a separate package. The server will let the server share its libraries that are shared between the server, the client, and other programs that might be accessed again, you know if you have PHP for example, the MySQL client is going to be used by the PHP site that comes with.  The shared compat, is to have compatibility. So these are other versions that were distributed with five, seven. So for the eight zero packages compat is the packages that we're sharing with five, seven. Then the test is the test suite. So all the MTR test suite TokuDB is the TokuDB engine. Again, this has been slowly being replaced by RocksdB. So if you're gonna, if you have to install, hi, ingest engine, please prefer RocksDB and will Xtrabackup. It's our backup solution. It's a binary backup solution that allows you to take called backups, non-blocking, fully consistent, and that will help that will be useful to stop replication and such. And will the test suite for the backups. And then MongoDB is our toolkit. And well, these are just I don't know what brings me those here. And the PMM client, which we want to actually then set up the monitors on the client-side to push data into the PMM server for monitoring. So that's about it. And I think we're gonna continue with the installation. And also, because why not? Oh, why not?

Why not?

**Marcos Albe:**  
I like it. I started

When in doubt, just right. Is that? Is that what you're saying? So that again, when in doubt, just install it.

Yeah, when in doubt, just install it is not going to hurt you. It should not pose a security risk. And it's going to make support engineers happy because they're going to give you commands. And it's not going to come back with a command not found. So yeah. Okay. Usually, there should be a procedure to pre-accept all the GPC stuff. I'm really not deemed the most illustrated sysadmin. So, pardon my French. I just said yes a good guy will have gone verify the fingerprint. That's what I'm saying. Right setup. Percona server brings some user-defined functions to do string caching, to speed up checksums for your data. This goes hand in hand with Percona.  Alright, that takes its time. It's a big, big package. Oh, it's still 27. Amazing. I thought it was kind of cool. It's under six.

**Matt Yonkovit:**  
It's the latest version.

**Marcos Albe:**  
In the IP. I think it came out years yesterday, it came out.

**Matt Yonkovit:**  
It was pretty quick. It was a pretty quick turnaround. Yep.

**Marcos Albe:**  
And this is one amazing release. Like hc 27 has a few features that it's the kind of stuff people have been waiting for for a long time.

**Matt Yonkovit:**  
You can't just say that and then not tell us what! you have to give us one or two interesting

**Marcos Albe:**  
Okay, I'll tell you what you can do. You can have two data centers and have one as you will have a group replication setup on one and group replication on the other data center. And you can have asynchronous replication in between those two, and you can automate the failover of the master. So if the node that was acting, as the source in the primary data center fails, the replica datacenter is gonna choose another source from the group as and this is the one that is new in HCL 27. And that completes the whole trip is if one of the replicas fails, another replica is gonna take over and continue replicating from the primary. So it's like fully automated. And like, there is metadata that allows you to know which one is the primary cluster and which one is the second cluster and you can actually use that with MySQL router and have like a pretty automated self-managed, cohesive group of nodes. So I think that's pretty amazing. You don't need any external tools to monitor or failover or change your read-only settings or anything like that.

**Matt Yonkovit:**  
Really though, what, what, and for those who are watching who might be new to this ecosystem, what we're talking about is, prior to this release, you could do these things. But if you did these things, it was something that required external tooling and external tools and setup and it was more of an arduous process, as opposed to automating it. So well you might already have had that kind of failover setup before now it becomes even easier and less fuss.

**Marcos Albe:**  
Oh, this is really, I did a demo for a customer the other day. And I think we did the whole setup for the cluster set in like 10 commands, of say, 15 commands, right, like, and everything was working with nodes all around. You have to be careful with some stuff when doing recovery. Like when coming back from a full outage, you got to do some careful steps, like Be careful steps. But other than that, it's really really resilient. Super good stuff. I'm happy Lefred convinced me to actually look into it in the most automated way. I was doing all manual, Lefred convinced me to look at it with even with MySQL shell, and use the whole ultimate experience was actually what's really good. 

**Matt Yonkovit:**  
you do that I'm gonna shut my blinds behind me because I'm not getting like the glare on my face. You can kind of see me in the sunlight here. They're shut. It's just that I gotta turn them around. So continue on and talk. And I'll be up here.

**Marcos Albe:**  
I'll continue on. Yeah, happy talking. Love to hear from my boss. So the packages are installed. These created a few directories, our data directory, of course. It's empty. So we're going to have to, it's going to be initialized when we started up. And it's going to have created our my.cnf. Which is pretty bare-bones just defines like, these two things, nothing else, we're gonna fill it up later. And if we do systemctl ... Sql, also, we get a pretty bare-bones system D unit it's nothing fancy or special. It's more Oh, well it actually brings. No, it doesn't bring any. Oh, it does bring this this previous unit version didn't bring this one. I thought I was gonna have to add it. Basically, if you want to use the clone plugin. To do some operations, you need for automatic restart to work. An automatic restart can only work if the MySQLD process is managed by someone. In the old times, it used to be managed by MySQLD safe now it is managed by systemD. And system D is always PID=1. So we can go ahead and export this environmental variable from the SystemD and say, Hey, your parent's PID is one. And we can see that's systemD precisely.

**Matt Yonkovit:**  
So Marcos, do you know who has joined us today?

**Marcos Albe:**  
 Who's here?

**Matt Yonkovit:**  
Andrew Moore.

**Marcos Albe:**  
Oh, man, glad to have you here. It's an honor. It's an honor. I hope to also see you live at Percona Live man, super nice to have people like you hear it actually makes us more nervous now. Now I know someone's gonna call me very soon. 

**Matt Yonkovit:**  
Well, he already asked a question, Marcos. He wants to know, is the performance impacted? And I'm assuming he's asking about the performance of the automated failover. I'm guessing that's what he's asking about but not 100% sure.

**Marcos Albe:**  
Okay. So performance impacted? Well, there will be like in any distributed system, it's timeout based, right? Like, it's the only way to reach some agreement is to say, Okay, we're only going to wait so long. And after that, we're going to make decisions. So there might be times when you run out of primary node ante until things happen, and there is no automated data center failover that happens manually. And but it's a single command. And that like, you could automate the one with failover. But otherwise, the impact for that setup is limited to the Group replication, Directory Sync, and mutually synchronous replication because the between data center is going to be asynchronous. So you also have to keep in mind, that the other data center, it's asynchronous replica with all the implications that pass Do if the link is slow, then the secondary data center might be lagging? If I don't know, if there is a network outage, then the primary data center is going to continue writing the other guys gonna be totally in the black it's gonna be totally blackout. And you're gonna continue to accept rights, which are not being replicated. But other than that, there is no performance impact. I hope that answers the question. 

We'll assume so but Andy will tell us if, if he has more, where he wants to play stump Marcos later, maybe Andy can help us with that.

I love that game.

**Matt Yonkovit:**  
Stump the Marcos. 

**Marcos Albe:**  
So start to spell checker status. We can see it's loaded. It's enabled, meaning it's gonna start itself next time we come up. We reboot the system, but it's not actually running. So let's start it 

**Matt Yonkovit:**  
That sudo o, o sudo. Sudo.

Alrighty, now, status. There you go. So this is working. And it's has everything service operation learned. Like she just old fashion, that thing is there. Where's the root? So how do you do? There we go. So when the server first comes up, it does automatically does something called MySQLD --initialize and that will prime the database. It will bootstrap the database. Remember, it was empty before and it will automatically generate a temporary password for our root user. So now we get to go there as -uroot. And I never know if that point is part of the password or not a CTS. 

Hello Jericho. Jericho has joined us

**Marcos Albe:**  
Hey, Jericho. Glad to have you here as well, man. We're missing you. Right. And I'm just gonna do now you have to change the password like you cannot continue to operate with that password. So you must change the password. This is a mandatory step in the installation process.

Okay, everybody's gonna see my password. "pleasedon'tcopythis123". All right.

**Matt Yonkovit:**  
Oh, you did not meet the password requirements. Oh, oh, what did I do MySQL's eight features that enforce password requirements? Always sort of those things that people forget about. So they try to do this like, easy password, and then it just

**Marcos Albe:**  
Yeah. So what I'm gonna do now just to make my life easier I will do it very quickly

**Matt Yonkovit:**  
If you enjoy watching Marcos, do yum installs and give us alike. We will try and get 24 hours of yum installs for Marcos in the future. It'll be great

**Marcos Albe:**  
It will give me more bare-bones, I will get to them.

**Matt Yonkovit:**  
Oh, I can create bare-bones boxes. Watch that, bet I bet there would be a few enterprising people who would watch the yum install the show.

**Marcos Albe:**  
So if someone gets to that file, the security issue is totally somewhere else. So I will not worry about that being plaintext. We could use login. I'm just lazy.

**Matt Yonkovit:**  
If you're not familiar with the .my .CNF it runs prior to you knowing the connection there. So it will pull out the password or pull anything else out. So if you wanted to go password lists, it still has a password. But that stores the password in there to make it easier. You can also put other client environment variable settings if you wanted to make some changes as you connect as well. I bet you don't have that straight. Yeah. Like this is this is a fret, like I said, this is the yum install show. Yes, yes.

**Marcos Albe:**  
Let me do it

So yeah. When you start, you actually are opening that file. Somewhere here, my subnet, and here it is. There you go. It's reading that and actually using that password.

**Matt Yonkovit:**  
All that yum install madness, just to show us that it did access the password, which is what we said, right?

**Marcos Albe:**  
Here this is that I have a running MySQL I can access. One important thing, I think it's one of the first things you should do is set up your time zones, it's in the manual, and every Support Engineer is going to tell you please do it to make your life and everybody's life less miserable. So if I do select @time_zone, so it says the system, if I want to do set time_zone='America/Montevideo', I think I can do that. So you're gonna have to use a tool, which is called mysql_tzinfo_to_sql . And this is going to decode or transcode the user share timezone info, which is your timezone database as filled. So there you see, it spits out a lot of SQL with information about the timestamps and the names. And you can pipe that instead of to five minutes or less, you just do pipe it to MySQL and because I already have my use of a password that goes

**Matt Yonkovit:**  
Realistically, you don't have to do the time zones. You can use a system if you want, but it's that means that each individual client can't necessarily set their own local timezone some stuff everyone will default to the server.

**Marcos Albe:**  
Yeah, and it's just handy. It's, it's handy and you're gonna be trying to follow instructions one day and it's gonna tell you, I don't know the timezone. So it's just, again, the easiest step. You don't have to do install anything else. You just have to run this one step. Get this utility where you have your time zone database and pipe it to MySQL and choose the MySQL database. So that is that complains about some, that's fine. I will have to investigate this one because I'm interested in lip seconds. But now if I go to MySQL, and I try to set my timezone so that works excellent.

**Matt Yonkovit:**  
That's very much hit for the installations are generally pretty easy. The question is, the defaults, though, are generally not okay. Right. So by default, you're going to get something that's Mac at the best, right? Yeah, I mean,

**Marcos Albe:**  
It will try not to overwhelm small machines, but it's gonna be underutilizing what machines we normally see in the running database. So and many things are still very conservative. Because InnoDB was created when we had 100 IO disks. This, so it tries to, I guess, in the mind of some engineers, those still exist. And they're often using it. So they still try to stay within the traditional conservative values for the default, they are not bad in most like, there are 500 variables, you don't want to tune the 500 Believe me, and some are best left alone. Like, especially please do not InnoDB IO capacity. It's okay like that. So other than that, there is one more thing that to do, right before we go into the My CNF. And it is because we're going to add this into it's related to my.cnf, basically, when you want to do select into outfile, or load file into a table, you want to have a limited source and destination for those files. The way to do that is with a variable called Secure File brief. And we're going to create a directory for it. So I'm going to do that just now. Okay, it's not there. You could do this anywhere, right? Like I just like the legal system there. Layout, according to the Linux standard layout, this should go there. Why did it do that? Go just go like this, because I don't like to use don't use dashes in your names. Because that is a special character. It is the minus character. And then MySQL is gonna converted to some hexa thing, and you're going to have to deal with it in special ways later on. So use underscore.

Marcos, we haven't another celebrity with us. Morgan is here.

Oh, my God. Well, now it's building up the pressure. Hey, Morgan, how are you doing?

**Matt Yonkovit:**  
So we've got we got to get Andy, we've got Jericho. We've got Morgan, who else will start running today? And by the way, this is week one of 26 weeks?

**Marcos Albe:**  
Oh, we should call Ryan.

**Matt Yonkovit:**  
Yes, yes, we'll have a party.

**Marcos Albe:**  
Sudo chmod with the same thing. There you go. And with that, I have a directory where I can later do select into outfile. And it's going to go end up here and MySQL is going to be happy to write into there. And it's going to be unhappy to write anyone else. So you cannot overwrite your ETC shadow, or you cannot read your set and set a password. So that kind of stuff. It's avoided with the Secure File grid and creating a directory for it. Okay. Now, we already know the service is good. And I'm just gonna very quickly go to the my.cnf.

**Matt Yonkovit:**  
By the way, Morgan is talking about how that manual is saying that the default config is for a 512-megabyte machine. Like from a usability perspective, it's probably better if we start to look at the installers and the setup, and the config tools that when things start it could get a little smarter, right like wouldn't it be great as the install happens when I say how much memory do I have? And how much weight do I have? 

**Marcos Albe:**  
Wait, InnoDB has the dedicated server option, which is automatically gonna dimension a few variables. I don't remember exactly. All off the top of my head, but I'm pretty sure it's gonna dimension open files, Max connections, buffer pool, and I believe the redo log size. Like, I'm not mistaken, I have only looked at it when it was just released. And they are mostly focused on customer questions and stuff. So that hasn't come up very often. But yeah there is a single variable, you can just sit there and said, InnoDB dedicated server, blah, and it's gonna try to be smart as you're asking for. So we're getting there, we're getting there. And you can also set up Percona with PMM. And the advisors and they're going to have some of that good advice for you to read the mention your settings. Alright, here it comes. I'm just going to remove so many comments. It says Read Only I know so many fonts. Okay. I'm going to quickly set up InnoDB, which is the thing that so I do have my notes because, in all honesty, I remember like 67% of these on top of my head.

**Matt Yonkovit:**  
Chichi 30% crib notes. Yeah,

**Marcos Albe:**  
Exactly, exactly. I think calling when you do like a small script to take the class like this

**Matt Yonkovit:**  
Well, so yeah, we call it to crib notes. We call it a cheat sheet. We call it. it just depends. Are you allowed to use your notes or not? Because if we're playing stump, the Marcos, then that would be the answer would be no, you are not right. Yeah. No, it's just that I'm trying to stump you. But if it's just for educational purposes, then absolutely. You could use your notes.

**Marcos Albe:**  
Okay, I'm not so am I allowed?

You're allowed to use your notes for this. Although if somebody wants to try and stop Marcos today, and if you can stump them, I'll send you a t-shirt. So feel free to ask a question.

Alright, I'm gonna do six, six. Usually, at night, it's I try not to go very high with the number, not much more than the number of CPU cores could be eight as well.

**Matt Yonkovit:**  
Can you? Can you explain?

**Marcos Albe:**  
I am dimensioning, the main memory area for InnoDB data indexes and access to the data structures. These will split that memory, so is 24 divided by eight. So I'm gonna have eight areas of three gigabytes each. That is intended to reduce contention on some mutexes that govern access to this data structure. So then innodb_log_file_size. And I'm just gonna go with two gigabytes. I don't know the workload. If I knew what the workload was, I wouldn't dimension this higher, perhaps two gigabytes for this is going to result in four gigabytes redo log total redo log space, which it's more reasonable than the 48 megabytes that the default suggests. So this is again, the same default for basic workloads. Again, I'm not sure what workload Mr. Yonkovit is going to give me later. So I'm just praying! 

**Matt Yonkovit:**  
You'll find out! by the way, again, people watching might not understand what a log file is. Can you give a brief explainer like,

**Marcos Albe:**  
I said a moment ago, that most people believe it's for crash recovery. But that is just a side effect. That is a consequence that you have to go through. Because the redo log, also called the right head log, it was again the sign it when your hard drive was at the most 100 IOPS and it was a spinning drive and it had a lot of latency to do random access. And sequential access was much, much faster. So what the redo log tries to do is say, okay, when you have like heavy write IOPS, I'm going to allow you to do sequential writes into the redo log. So because those sequential writes are much faster, and then later, when the right workload recedes, we are going to, in the background, slowly start to do the random writes into the final destination tablespaces. So basically, it's a buffer that it's converting what would have been random writes into the tablespaces. Into sequential writes, The problem is, if you crash, you're going to have to take all those rights that still are in the redo log only, and are not in the final tablespaces and apply them to each tablespace. So it's a performance optimization mechanism, which was again, decided with spinning disk in mind, but it's still useful to this day with SSD drives. Because steel sequential writes are much faster, in even in NVMe, drives, this is still totally necessary to have a large enough redo log file. Does that make sense to use?

**Matt Yonkovit:**  
It makes sense to me. And so there's, there's that often if you're in the MySQL space, the larger this size is, the more concern people have about crash recovery time. But I think with modern hardware that is mitigated somewhat, I mean, early on, when I started, if it was all rotational disk, and it was slow, it was Slow as hell, when you had multi-gigabyte, redo log files.

**Marcos Albe:**  
Yeah. And you can only have up to four gigabytes. So anyway, it wasn't that large. But yeah, not only some improvements have been made to the recovery process. But also, if you if you're serious about uptime, right, like, if you're serious about requiring some amount of nines for your uptime, come on, you must have high availability cells. And so when the crash recovery is happening here, you are copying whatever been looks, we're still not applied to that instance. And just starting that instance, while the crash recovery is happening. So there's a good blog post by Vadim, what is the large log file size? Well, there is no such thing as too large unless you're exceeding the limit, which is something insane.

That's, that's some interesting words, there is no such thing as too large.

No, but there is large enough. So what is large enough, large enough is that you going to be able to withstand the lsn growth, the write that is happening for the duration of your peak write. So if your peak workload that that's written for two, or three hours, and you write, I don't know, let's say, it lasts for two hours. So 7200 seconds, and you write one megabyte per second, well, then one-megabyte times 72,072 gigs, just do it it's fine. Because that's going to give you the guarantee that even if there's other stuff, stressing your IO, and even if you're doing a crazy amount of reads, you're gonna be able to keep your IO capacity low, and not force excessive flushing, that will ruin your performance for a diversity of reasons. So how much is large enough is enough to withstand your largest peak load. That is my opinion. Of course, this is a bit of an opinionated tuning. The results are good when we do that with customers, they are happy, so apparently is a reasonable opinion. So first log activity for me is, of course, related to these logs. And it's saying What shall we do when a transaction commits? Shall we flush the log to disk? Multiple settings Sudo is no don't do absolutely anything. let us carry on with the buffer. Then there is one which is plus a Fsync every time and the other one is two which is flash baton Fsync. So basically, with zero you will lose data as soon as MySQL crashes with 01 you will not lose data. And with two, you will only lose data if the whole operating system crashes. So that's like a relatively good summary. So I'm gonna choose one I like for durability, they pay me to preserve data. So I want to have it all when things happen. And then also related to this is innodb_flush_method. And this is quite boring bolded in the sense of explaining all the options for this is beyond the scope of today's talk. But basically, I'm going to tell you why I choose auto-detect, 0_DIRECT is gonna skip the file system buffers, the BFS cache, and we want to skip the BFS cache because otherwise, we will be double buffering, the stuff that we read into the buffer pool. So if you read, when you read from a file, the operating system is going to say, I'm going to keep this file in memory because I don't, I'm smart. And I don't want to go back to these if they need this file. Again, the problem is, that we are already keeping that file in memory in this memory segment. So we don't want OS to keep any of it, we will take care of it. So we say hey I'm just gonna go directly to disk and into my memory. Don't worry, don't do any buffering for me. And then final flash stuff. Innodb_flush_neighbors. I always mistyped the snake, or worse, T No, yeah, I always add a G there, that doesn't go pardon my English. And I say we have an NVMe drive. So I know, it's not necessary to optimize for adjacent writes. So neighbors are basically that the saying, okay, these pages are neighbors, they are in the same extent, if we write them sequentially, like if we write them all together, it should create more merch for those rights, making more sequentialized rights and improving performance. But for SSDs, it usually results in unnecessarily excessive flushing, and there is no such great advantage. So we tend to save it.

Then some other tuning for flushing, innodb_adaptive_flushing_lwm. The default is 10 and is the percent of the redo log that must be full. Before we start, we kick start the adaptive flushing. In InnoDB, there are multiple flavors of flushing, you have background flushing, which you know is the kind of flushing you want. It's happening in the background. Little by little, it's governed by IO capacity and how much data you have. how full is the redo log? But that's the kind of flushing you usually would like to see background flushing, then there is adaptive flushing, which says, hey this is starting to fill up. Let's hurry up. And let's not allow the redo log to become full. Because again, it is only an optimization mechanism. But we're also relying on the redo log for crash recovery. So we cannot let it become full because we cannot continue writing. If it's full, we need to wait for it to become more empty as we need, we need space in there to always continue writing. And as we don't want it to be too full, but not too empty either. So what the default is, then that will be 400 megabytes worth of stuff to flush before the adaptive kicks in. I usually set it to 20, which I found it's more reasonable especially when you start to use a very large log file size. You actually want to perhaps grow this up to 30% the risk is in my later try to flush more that we're going to tune the IO capacities. So it does not cause cross excessive questions later. The innodb_io_capacity makes this alone. Please leave it alone. But now you're I'm leaving it alone. I'm just putting it there for reference. So you're setting

**Matt Yonkovit:**  
The default value?

**Marcos Albe:**  
Yeah, exactly. Fair enough. And the innodb_io_capacity_max. The default is 2000. And I'm just gonna set it slightly lower. So there are, there's a good blog post from colleagues,  that describe the algorithms that govern flushing, and explains how these numbers are related to the flushing rate. So there is an equation that goes, that takes the IO capacity, IO capacity Max, the size of your redo log, how full the redo log is, and how much there is in the buffer pool. And with all that, it decides how much it has to flush. So again,, I know this is going to be divided by this when adaptive flushing kicks in. So instead of 10, I said a ratio of six, which, again, my experience makes it just more even Right? Like you get more even flashing instead of spiky and gone down spiking or down. So that's it. Then I'm going to set this one here, let me check

**Matt Yonkovit:**  
Yum, install with Marcos.

**Marcos Albe:**  
yum install, yeah,

I need it, I need a sound clip for that, like yum install with Marcos we can do something like that.

Alright, so NUMA control. Modern systems are mostly NUMA systems. Numa is non-uniform memory allocation. And it's basically if you have more than one CPU, so I should have known this because when I did it, somebody was already telling me something. So it was telling me a physical one. So but if you have more than one physical CPU, right? Each physical CPU, it's going to become one NUMA node, and each NUMA node is going to have its own memory back. And to make sure that memory is evenly allocated across both nodes, we will do innodb_numa_interleave, so I'm going to do it anyway. Doing setting these has another thing, which is it's gonna relocate them pre-populate all the buffer pool in a single shot. And when the server starts, this adds some startup time, but it helps prevent some fragmentation. Again, in NUMA systems, it's gonna help evenly allocate memory through the boat through all your NUMA nodes. And it's also an all these makes memory diagnostic easier later on, like, if you ever have, if you ever suspect you're suffering, memory leak, or if memory is bloated like this makes it easier to investigate where memory leaks are coming from. So I'm just going to do it, even if I don't have a numa, it's just going to do it. And then the innodb_monitor_enable=all. Monitor enable all is going to enable some table in information schema, which is called InnoDB metrics. And it's going to have a lot of internal metrics for InnoDB that help in advanced diagnostic, and we're going to be able to immediately enjoy some additional dashboards in PMM. When we enable this, it adds perhaps 1% overhead, something like that, it's quite low overhead. So I tend to enable it and recommend customers to enable it if it is the kind of people that do a lot of analysis like I have customers that I work with every month on performance issues. So that kind of people please enable it. Okay, enough InnoDB. Now we're gonna do some connections. max_connections. This is just learning how the maximum number of connection threads that are going to be able to be open on the server

**Matt Yonkovit:**  
100,000

**Marcos Albe:**  
I think 2000 is should be plenty enough like if you need more than 2000 realistically, InnoDB has a hard-coded limit of 1000. So like, you can have as many as you want. Not all of them are going to be doing work. So it's cool if you have like a connection pool and you want to keep a bunch of connections live on whatever, again, more than 2000. Like, you should review what's going on that you need. So many. Make sure you're doing something. Yeah.

**Matt Yonkovit:**  
And we probably should do a connection pool episode. ProxySQL or something.

**Marcos Albe:**  
Yep. multiplexing could bring this number down to 200 and still serve 1000s of clients. So yep, we could absolutely look into proxy sql multiplexing. It has quite a few limitations. Versus let's say, Hikari, CP, right, like Java connection pool, like hickory, or, I don't know what, what other tools do I use normally, I don't do much more than those, to be honest. But again, whatever pooling you're using, it's good because creating the connections requires a handshake with multiple network round trips. So not having to re-establish connections is healthy, or good for your performance.

**Matt Yonkovit:**  
We have a couple of other people who just stopped in to say hello, so hello to Mr. 73 357. Mag, and Gie, we're happy to have you here. Watch it.

**Marcos Albe:**  
Anyway, welcome, everybody. Okay, Max_connection_errors, I'm just gonna say something. So what is Max_connection_errors? Oh, this is how many errors consecutive error an IP address can have. Before it's banned. so I'm gonna say you can have, I don't know 10,000. Because sometimes there's a loop. And it will just be some people using the same username for the monitor for the cron jobs and for the application. And so if that if one of the cron jobs or the monitoring has some error, with the password, or trying to access from a not allowed IP, it's gonna block that IP and just, you're gonna have to go and reset it. So I just allow some margin. That's like if you try once per second that is like three hours' worth of trying. So that shouldn't be enough. Like if you have more than that, please fix your stuff.

**Matt Yonkovit:**  
Yes, yes. If you have more than 10,000 errors, fix your stuff, Marcos. That's wonderful. That one that's top-notch everyone let's get a mean setup with that if we have 10,000 errors, fix your stuff

**Marcos Albe:**  
It is good advice. I agree. It's solid advice. I don't think anyone would disagree with that advice. If you do disagree I want to know why?

convince me otherwise. So, max_allowed_packet is just telling us how large packets can be these will also govern things like the maximum size you can insert into a row because you cannot do an insert with a packet that is larger than maximum

**Matt Yonkovit:**  
What about with blobs or large objects

**Marcos Albe:**  
Then that goes into the packet as well right.

So if you are inserting large objects then this is something you need to adjust.

Yes, yes sir. Then some other limits will do the thread_cache_size this is also related to connections. This is how many lightweight empty threads it's gonna keep cash on the MySQL side so MySQL has to keep creating a spread. 

So pidstat -u -t -p is going to show us that only four one process and there you go. Beautiful you can see MySQL has a lot of internal threads. And I asked if the connections are created, it's gonna create threads for the connections as well. And I just realized that eight sudo has name-it threads. This is a feature request I did 457 In the Percona server, I love to see it implemented. This is super useful because we can like, I can see how much CPU each one is consuming. So I can immediately tell Oh, is the buffer, the buffer pool dump, the log writer, or whatever, right? It's allowing me to take it because I can do this for the disk as well. So I can see how much

**Matt Yonkovit:**  
So, next week when we start throwing workload at this, this will be a really interesting tool to use and see the different threads. So looking forward to that, because I'm gonna, I'm going to ramp up some crazy workload for you and we can take a look to see what, if anything's bottlenecking

**Marcos Albe:**  
I need to read the Yonk box. I'm gonna need the Yonk box. Are you taking it to Percona Live?

**Matt Yonkovit:**  
I will take it to Percona Live. Do you want me to? So so we can build a Yonk box at Perconalive.  So do we want to build a Yonk box at Percona Live? Do we want that as an evening activity, everyone builds one, and I would like to have one. If people don't know what a Yonk box is, I have a controller. I've got a couple there away from my desk. I just sent one to the Postgres conference next week. But it's like an arcade controller and the buttons and the knobs actually control database workload. And so it's almost like a Chaos Engine for your database where we can spin in two knobs and throw different levels of workload at the server. It's kind of a cool, nifty little way to visualize data. So next live stream we will be using said Yonk box to generate a crap ton of workload. I think it could say crap ton on the live stream, and I won't get in trouble of workload at this server so so the rocky Linux server will be hammered.

**Marcos Albe:**  
Alright, yeah, I won't the people at my, I'm gonna do a presentation about diagnosing the PMM. And I wouldn't just have the people take the knobs, while they're the public in the presentation to tweak the knobs. So I can go find the problems.

**Matt Yonkovit:**  
Oh, so you want to use it for your demo? Like, like your presentation? Cool? Yeah, I actually have multiple boxes, I'll bring a couple. And we can create somewhere where I can bring all the parts and we can do it as a workshop. If people want to do a Adreno workshop and learn how to code Adreno devices, and then connect it and manipulate workload. It could be great fun. For all involved.

**Marcos Albe:**  
That makes a good afternoon session. Absolutely. Yeah, definitely. Right. So thread_cache_size, again, I'm just mentioning something a bit larger than the default 16. Because the default is pretty low. And I would say eight times the number of CPU cores, it's relatively cool I don't think you're gonna have more than eight threads realistically ever doing anything, per core. So this should be good enough. And back_log again, this is kind of most of the time shouldn't be necessary. If you don't have like very large arrival rate, I'm just gonna make it a bit larger. And we are going to have to tune some TCP settings later. But I'm just going to put it here as a reminder that we probably might want to look at this if we have very high arrival rates for connections. Alright, that is that I'm going to set up something more that is very useful.

**Matt Yonkovit:**  
core-file

**Marcos Albe:**  
core-file, and there's lovely one innodb_buffer_pool_in_core_file

And no, we don't want it. So when we dump the proto file, we're not going to have to dump the 24 gigs of the buffer pool, which the vast majority of times is not necessary.  It contains potentially sensitive data and makes most of the customers we have, I guess I would say, the smallest machine I see daily probably has 64 gigs of RAM. No, that's like the small one. Big ones have like two terabytes of RAM, and you don't want to dump the server itself for nothing.

**Matt Yonkovit:**  
Yeah, and just so people know, when you're talking core file, when a crash happens, it's going to give you all of the diagnostic information that is needed to kind of diagnose that. If you don't have a core file, you can sometimes troubleshoot. But it's limited to what ended up in the log files.

**Marcos Albe:**  
And it also requires a bit more config on us. So you have to make sure you don't have a limited size for core_dump. So when you start MySQL, you start it as root, but then it runs as the MySQL user, you have to make sure that processes that are running in that form in that way, are okay to be dumped, that has a special setting, then you have to make sure that the path where the Core is going to be dumping, it also has enough space, it's writable, by mysql, and it doesn't contain a file with the same name, etc. So there are a few tweaks we can do in a moment. Those are again, very useful, because like this is not going to affect your performance in any way. But the day you have a crash, this is going to give you all the necessary steps to diagnose most of the famous most of crash incidents you might have, right. So super useful. then dictionary, table_open_cache. I have no clue about the dimension of the database, Yonkovit is gonna give me nor how many threads we're gonna have table open cache, it's a cache that keeps the file for the operating of the tables. And this is per table per thread. So if I have one table only, and I have 10 threads opening that table, I will need 10 slots in the cache. If I have, if each thread opens four different tables and has 20 threads, then I need 80. So this is dependent on the concurrency and the number of tables that those threads are opening, I'm just gonna set some reasonable number, this is somewhat reasonable for a good amount of workload, and then table_definition_cache. I don't think we're gonna have like 1000 tables. And this also has table_open_cache misses. And I'm just gonna make it 16, why not? So on eight, we have a to-do list. So this also is intended to split these cash into multiple pieces that are governed by independent mutexes. so as to reduce mutex contention. Next, also, somewhat related to these open-files-limit. So we have plenty of limits. These might required some OS tuning, we're gonna find out as soon as we restart the we should check the log and see if it complains about it, basically, is the limit of file system handlers, you can have open on the operating system that MySQL can have on the operating system. So if you have 1000s of tables and 1000s of users, concurrent users, you might need more than this. So we have customers that have 300,000 tables. Well, if you want to take a backup you need a much larger value. And then okay, and tmp_table_size. Let's make 32 max and max_heap_table_size. So one is limiting the amount of memory I want temporary tables to use in memory. And the other one is limiting the memory engine size for a table. Usually, you want both of these to be the same. So that's it. And then what am I forgetting? Okay, we said that I was going to set up security secure_file_priv. So now MySQL is all you're able to do load data in the file from here and select into outfile into here. Select into outfile is probably one of my favorite things in life.

**Matt Yonkovit:**  
Wow. That's one of your favorite things in life.

**Marcos Albe:**  
I'm a simple man. Yeah, yeah,

**Matt Yonkovit:**  
that is a little unusual. Gotta admit, I mean, I enjoy many things, but I wouldn't count SELECT INTO outfile in the top 10

**Marcos Albe:**  
Well, that's because you don't have to generate 1000s of SQL statements for your customers. But when you have to

**Matt Yonkovit:**  
Yeah, but even so even if I had to do that, I mean, like, on the levels of enjoyment whether it's music, music, movies like your food like,

**Marcos Albe:**  
What do you enjoy in MySQL?

**Matt Yonkovit:**  
Well, that's a whole Yeah, you didn't specify, you just said it was one of my favorite things in life. Does anybody else? I mean, like, I'm curious if anybody else out in user lands here who was either watching live or the replay? Is one of your favorite things in life, something within MySQL? If it is, let us know, I'm really curious. If it's just Marcos, or if there are other people out there who count one of these things out there as one of their favorite things.

**Marcos Albe:**  
All right. So I said this, I then said Do not allow local_infile. If you allow a remote client to do load, load file, load data with a local file, too. So you have the server and you have the client machine. If you allow local_infile, you're allowing files to be loaded from the client-side. So files that will not be in this directory. And that could be anything. So we don't reduce the surface area of attack, we did that.

**Matt Yonkovit:**  
By the way, Dave Stokes agrees with you, he just said, it's just you, Marcos, who counts MySQL as one of his favorite things in life. So I'm happy about that,

**Marcos Albe:**  
I guess I will simply go symbolic_links, which is also it's disabling the use of symbolic links for MySQL related files and data files. This is also a security measure. And again, it's just a good habit to disable. Once in a while a customer comes and tells me I don't have any more space here, I need to optimize the table. But I don't have enough space for copying the table. And sometimes, being able to do a symbolic_links could be useful. Now. MySQL supports a data directory modifier for the tables. So when you create a table, you can put the table in some other data directory or you could alter and make it into another directory. It makes it easier by the symbolic_links once in a while could be useful. Usually, just disable them. And save yourself from some security exposure.

Hello, Veer Veer just joined us. Hi, Veer! Welcome.

And now comes Yeah, please go ahead.

**Matt Yonkovit:**  
Oh, no, no, Dave suggests that we re-sing or redo the Julie Andrew song, my favorite thing for you. So maybe we'll have to do a parody of the MySQL fairy things.

**Marcos Albe:**  
I would be glad to do that. I could have fun with that. Do they have other things like yeah, you know what was my favorite thing? In five-seven? What was your that's actually used seven that you can actually use Ctrl C within the MySQL client without having been kicked out of the client? that made my life far less miserable.

**Matt Yonkovit:**  
Yeah, so your favorite things are Ctrl C without getting kicked out and the ability to write selected 12 selected out files Wow. Wow. Yeah, give me a glass of wine could be a favorite beer could be a favorite song favorite movie could be spending time with your family but selecting it

**Marcos Albe:**  
I do other stuff? Okay. I have 10 minutes for my next goal. So yes, we're running out of time. So, yeah, we're

**Matt Yonkovit:**  
20 minutes about. Yes, yes. But that's okay. Because you know what we love the m&m folks here, right, the Matt and Marco show, we just continue to talk, because we have so much to say.

**Marcos Albe:**  
So I'm gonna server_id gonna be enabling replication and binary logging, which is necessary for pointing time recovery later. So log_bin is enabling the binary log that keeps a record of every ride in the standard database, sever_id just keeps the server unique in your setup. And then I'm gonna say that in the binlog_format, there are multiple binlog formats. There the original one was the statement.

Server_ID that is the same combination as my luggage. Lock up.

You shouldn't say that in public. That's security like

They say it's a Spaceballs reference. Oh, ever watched the movie Spaceballs? Yeah, my luggage.

So, um, the summary, the binlog_format, the original was a statement and it record the SQL statement as it was executed on the source. But that introduces opportunities for inconsistencies when the statements were executed again, the replicas row is going to keep a binary representation of the row. So it should be identical, like, whenever you apply that binary image on the other side, the results should always become identical. And then binlog_row_image, just, if you have imagined, you have a column with a table with 10 columns, and then you do an update, and you only modify two, well, if you have row image full, then it's gonna record all 10 columns in the binary representation. If you do minimal, it's only gonna save the identifiers, the necessary data to identify the row, and the changes data. So it is potentially saving you a lot of disk space and network bandwidth. Then, sync_binlog again, I love my data. So I make everything very consistent. This goes hand in hand with what is its first to look at your ex-commit? Yeah. So we should, we should talk about durability later. But basically, if you're doing this, you should also do this. Because if you don't do it like if you say okay, I'm gonna just I'm gonna plus look at your estimate, every time I commit in, but then seeing being looked, I'm just gonna do it every 10 comments, what might happen is that you collapse, and then you're gonna have to revert up to 10 of the committed transactions, because if they're not in the binlog, then InnoDB says, hey like, we cannot guarantee these ever arrival to the replica. So let's just roll them back here. And you're gonna have some clients that did commit, they got the Okay, they think their data is there. But actually, the data was later rolled back automatically to do the crash recovery, so make it the same. Then gtid_mode, it's also an introduction, something that was introduced in five, six, basically, it allows us to have a global sequence for all the servers. Before we have binlog_names, and binlog_positions, and each different server in our replication topology will have a different binlog name, and could they will not match the positions will not match. So it was hard to failover when your master died and you want to failover to some other source server, you will have a hard time finding where you should start replication in the other server. This should make it easier. It does have its perks as well, but it is an I just said zero, and I wanted to make a blog post, then,

**Matt Yonkovit:**  
Because you have a limited amount of time. Let's move the OS tuning to the beginning of the next live stream in two weeks. So that way you don't worry about any change to the OS. We'll do that before we start actually tuning the real workload.

That sounds good

**Marcos Albe:**  
Okay, so enforce_gtid_consistency, it's basically enforcing that whatever writes happens, they must comply with all the gtid from the group. So you cannot replicate from a server that is non-gtid. If you have gtid mode enable, make this all actually, if you have gtid enable in a strict way, then this guy is going to tell you, Oh, you're replicating from a server that does have some has not gtid, please unable. expire_logs_days, this is telling us how many days' worth of binary logs I'm going to accumulate. Then master_info_repository, this became the default later, but I'm just gonna put it here is a reference for stable and relay_log_info_repository=TABLE. so replication coordinates must be sorted, and the connection information to reach the source must be sorted somewhere. So these used to be files that we also had to Fsync every time we commit. Now they are InnoDB tables. So they have the same durability as InnoDB has. And they will allow you to have so-called Crash resistant replication or crash receiving replication. If you do this relay_log_recovery. You said, ON. Now, it's when the relay lock, when the replica comes back, if you have syncbinlog, you have plus look at your estimate, and you have really long info repository equals to table, your replica is going to be in good shape, it's not going to be or delayed or ahead in the replication coordinates. So this makes replication more resilient. And then binlog_cache_size. When you have larger transactions. If what you're trying to write to the binlog is larger than this, it's going to hit this. The default is 32 kilobytes, I see it being exceeded all the time. And 64 kilobytes usually makes much better work. And that's enough configuration for today. I hope you enjoy that. Yeah. So that it was useful.

**Matt Yonkovit:**  
Everyone likes, subscribe, do whatever to tell your friends, your family, and your colleagues to show up? Because we would love to have you show up, ask us questions. We didn't get around to stumping Marcos today. Sadly, we're gonna have to do that next time. But to take a look at our upcoming schedule we actually do have a schedule. So if you go out to the percona.community website, you can see that today we're doing the installation, we're supposed to be looking at the workload and adjusting our configuration based on workload starting next week. But we'll start with kernel tuning parameters and some of the OS, things that we want to set up, then we'll be going to some alerting and some monitoring and automation things and backups, replication migrating to a new server, we'll do some Kubernetes work, we'll design some schemas, we're gonna have a lot of fun. And you can see that this schedule goes till next year. So we hope that you will join us during our lovely year of Marcos.

**Marcos Albe:**  
Indeed.

**Matt Yonkovit:**  
Alright, everybody. Thank you for joining. We appreciate you hanging out with us today. And we will see you next time. Next week. Postgres meetup. Join me and Charly. So this in two weeks we're back with Marcos so until next time see you

**Marcos Albe:**  
See you.
