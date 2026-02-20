---
title: ' MeetUp for MySQL - Database Backup and Xtrabackup - Nov 3rd 2021'
description: This Community MeetUp for MySQL on November 3rd was a 1-hour talk dedicated
  to talk and answer questions about open source database backup, Percona Xtrabackup,
  Schroedinger Backup, and Q&A.
images:
- events/percona-meetup/cover-mysql-november-1-1920.jpg
date: '2021-11-03'
draft: false
speakers:
- pep_pla
- marcelo_altmann
- matt_yonkovit
tags: ["Meetup", "MySQL"]
events_year: ["2021"]
events_tag: ["Community", "MySQL"]
events_category: ["Speaking"]
---
Full recording of the Percona MeetUp for MySQL of Nov 3rd 2021. Marcelo Altmann and Pep Pla joined Matt Yonkovit to talk about Database Backup and Xtrabackup. In this video you will be aware of different database Backup solutions out there, Best practices vs. wrong strategies, Percona XtraBackup and more. As usual during the Community Meetup, They have answered questions from attendees live.

## Video

{{% youtube youtube_id="FMFu6aFZx64" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Oh, welcome, everyone, to another Percona live stream, today I am joined by two awesome guests to talk about MySQL. Marcello and Pep, how're you both doing today?

**Pep Pla:**  
Perfect, perfect. Perfect.

**Marcelo Altmann:**  
I am good as well, how are you doing, Matt and Pep?

**Matt Yonkovit:**  
Good. We are on three different continents today. How about that, right? Like this is this is this is a momentous occasion. This is I think the first time I've been on three continents, right? So we're in three different locations. We're live. We're here to talk about MySQL. And I'm trying to stave off a ton of questions from my mother in law today. Who has this habit of finding houses that she doesn't want to buy? But she'll send them to me and say, Is this close to you? Can I move by you? And she does this all the time. And so she decided to start that, like, two minutes ago, and I'm like, I am on a live stream right now. Oh, yeah. But that's not good. It's my mother-in-law. She wants to press it. But okay. So thank you for joining us today. And thank you, to those who are out in the live stream sphere here. We hope that you enjoy our chat. This is our continual meetup schedule. We try to do one of these a week, because of holidays coming up, we're gonna adjust the schedule. So stay tuned for that. Next week, we're actually going to be skipping a week, because I'm not going to be available to host and so we'll see how that goes. And then we'll just kind of rearrange some things for the rest of the year. But if you are here, thank you. This is an open forum, feel free to ask questions in chat, we will pop them up on screen, we will talk about them. We'll try and answer any of the questions that do come up from the community. We are here to help everyone out there, learn a little bit more about MySQL today. So Pep, why don't we start with you? Why don't you introduce yourself, tell us a little bit about you. And we can just kind of go from there?

**Pep Pla:**  
Well, my name is Pep, Pep Pla. I'm 50 years old, so it's quite a half a century. So it's quite an ice age. I've been working as a DBA for diverse technologies for the last 30 years or so. So I worked at Oracle, SQL Server and DB two. And around 15 years ago, I decided to do the Swift, the switch sorry, to, to open source technologies, and especially MySQL, and I am married, father of three kids, and I'm living in Barcelona currently.

**Matt Yonkovit:**  
So, you are a European continent person today so representing the continent of Europe, which is awesome. So, Pep, you've been very passionate about the database space and love MySQL, have had you stop by and chat with me on the podcast. So, I appreciate you being here today. I know you're gonna talk about some toolkit things. We're also gonna be talking about Percona ХtraBackup as a group, always fun activities there. But let me go ahead and have Marcello introduce himself a little bit to the audience today. Marcello.

**Marcelo Altmann:**  
Hello, everyone. So my name is Marcela Altmann. I am based in Brazil, in the South most part of Brazil. In terms of databases and work related stuff. I started with MySQL in 2006 as a lump developer, like it was what was in the stack, and I kind of improved from there. It was around 2011-12 when I actually became more expert in MySQL. I used to work for a company that was like the country code, top level domain in Ireland. And like one of the first tests I had to do there was to actually create a backup strategy. They actually had an issue a few years before I joined, where they suffered an outage, they had to restart a backup and they figured out the time that they were restoring it was not working. So it was a difficult time for them. So that was like the first task I had to do. And that's where I had to do a deep dive in research about mostly everything about backups and like, what's the backup? What it's important, what it's not when a backup can be considered a backup. And from there,

**Matt Yonkovit:**  
Right now you're doing a lot of engineering work.

**Marcelo Altmann:**  
Yep. So, from there, I moved to Percona. I started as a support engineer. And while I was at support, I got a case where a client was complaining that after restoring a backup, the slave was not behaving the same way as the master. And that was because the buffer pool was not warm up. And one of the first things I did as an engineer in my spare time was to actually adventure myself with Percona XtraBackup which MySQL already had, like the ability to dump the buffer pool, since five, six, but Percona XtraBackup was not aware of that. So the first thing I did as I was still a support engineer, but created the ability on Percona XtraBackup. So you could instruct it to dump the buffer pool at the end of the backup. So when you restore the backup, my sequel recognizes that file that has tablespaces and IDs, and it knows what tables or what pages it has to restore after you bring your server backup. So unlike for for things like Percona XtraDB Cluster, when you have to do like snapshot transfer, when you provision a new node like it, it starts, the node behaving exactly as the writer was, or so it was, first time I did something as an engineer in a year later, I actually moved from being a spare time engineer to actually become part of the C++, MySQL

**Matt Yonkovit:**  
Maybe you can explain to those who might not know why it is important that you would potentially restore the buffer pool during a backup process? What does that accomplish?

**Marcelo Altmann:**  
Basically, InnoDB works 100% in memory when you talk about reads and writes. So, of course, like you persist your data into disk files. But every time you have to do a read or a write, this particular page has to be in the buffer pool on this huge memory area that you configure like, as much as you have, the better the faster it will perform. But all the operations are done on this area in memory and then later they are persisted to disk. So as you can imagine, like memory, it's way faster than disk. So if you start your server, clean, every single read you have to do let's say for a select, you have to read 1000 pages, those 1000 pages will have to it will check on memory, it's not there, it will have to go to just figure out where this is in your disk layout. Read that page, put that in memory and go to the next page. So as you can imagine this is a costly process. But unlike the buffer pool, which has some algorithms in terms of what pages it should keep, they're like the most accessed ones. And had some protections in terms of if you do a full table scan, for example, it does not override like you're actually hot data that it's been accessed more often. But you have the ability then to get a snapshot of those pages, not the pages themselves just an identifier, so the server knows which base pages it should load. And then if you do that, once you are doing a backup on a master or in a case like XtraDB cluster on a writer node. Once you restart this backup, MySQL will identify this, this file and it knows like this specific file has the pages that I have to load. So it will start like a background thread that will start to read those days in just ahead. So while you are starting your server, there is this term of warming up so you are warming up your server before 5.6 there were ways to do that like issue a select star on all the tables and things like that. So you could populate your buffer pool with this data but that's not precise because you may be losing data that was not there in case of your data sizes. It's bigger than this size in memory. So with this feature on Percona XtraBackup, you will actually have your years later when they know that you are just provisioning, with the same pages in memory as your source was. And those things improved for pharmacy castigating.

**Matt Yonkovit:**  
Yeah. So basically, when you're restoring a backup, whether it's to a server that crashed, a replica development node, whatever. In the meantime, to actually get to the point where you work when the crash happened is fairly long, because nothing is in memory. So everything has to be read for the first time from the disk. So this process, this feature, this functionality, basically starts the backup and starts warming that memory, so you don't have to incur that first read penalty.

**Marcelo Altmann:**  
Correct. That's, you will have to read the data anyway. But rather than having, like your select, missing the heat on the buffer pool in the Select, like the client, wait for that page to be restored in just that which has been already done ahead once you started.

**Matt Yonkovit:**  
And that can be pretty big for a large dataset.

**Marcelo Altmann:**  
Correct? Yeah.

**Matt Yonkovit:**  
So. So have you used that feature? Like it?

**Pep Pla:**  
Yes, actually, I have not used it, especially for backups. Because, well, sometimes, obviously, this adds a little overhead in storage and backup time, because we have to dump this data. And so if it's a pure backup, sometimes I don't use that option. If we are rebuilding a replica, we have to consider if it makes sense or not. Because sometimes if it's a replica that it's used for different purposes, you are actually populating the buffer pool with data that it is not going to be used for. Obviously, if you are, for example, going to use the backup, to replace the source master, then that's an option you have to use for sure. Especially if the data set is massive, and the server has a lot of memory, if you have a huge buffer pool, the impact in terms of performance can be really very high, then the warmup time can be really very, very large. So it's an option that you can use. It's really very useful, but you need to decide if it makes sense or not. It will not harm you because it's by background processes. So you can use it by default. If you don't know, what will be the use of the backup.

**Matt Yonkovit:**  
So Wagner Hello, look, look, it's Mr. Bianchi here. He's Hey. Yes, yes. Wagner is a longtime collaborator in the community space. He worked at Percona. MariaDB worked at several of its companies. So Hey, glad to have you here today. Wagner. Hello to you out in live stream land. I appreciate you for stopping by. But Pep so you wanted to talk to us a little bit today, right on some of the tools. And some of these tools can be used to help with not only performance or troubleshooting but can help on these really large systems where you do have large buffer pools where you do have large datasets.

**Pep Pla:**  
Well, that one, well, the Percona toolkit is there are so many useful tools that it's really hard to tell which are the best.

**Matt Yonkovit:**  
But favorite, right?

**Pep Pla:**  
Yes, I think there are a couple of tools that are like ping comments. It's the PT summary thing. It's like when you try to connect to a server you run ping when you are connected to the server, and you have installed the tools. The first thing you do is run a summary, just to have an instant overview of what you are dealing with. And are really very simple tools. It's not, we're not going to discuss or talk about the different options of the summary tools. And being so important. So great tools. I'm surprised because lots of people don't know that. A couple of tools that PT, MySQL summary, and PT summary, that give you the information about your server.

**Matt Yonkovit:**  
I think that's one of those things, that it's like the hidden toolbox, right? That there's quite a few tools out there that not only you use from a support perspective or a consulting perspective on a regular basis, but a DBA could totally make use of any time or another I mean here I'm going to pop up just so everybody can, can see if you're not familiar with the toolkit, it's it is available on Percona. website, this is the PT summary that Pep was just mentioning, and there's also a MySQL summary, as well. But it gives you the summary of that box. But anyways, continue on.

**Pep Pla:**  
And, obviously, online schema changes for lots of databases. It's always the same, I have to add the column, I have to create an index, the table is really very large. I tried with the online, default MySQL tools, and I have logs, or it's failing because that my buffer is not my buffer for changes is not large enough. So it's a nightmare. And the bottom line schema changes, if it's a tool built for this, that does it perfectly. That has a ton of options. So almost every problem you can have. There is an option that can help you. Yeah,

**Matt Yonkovit:**  
I think that's where that there's, there's, there's a little Swiss Army knife tool for everything, especially for those who like to run on the command line, who might not have access to a graphical interface. A lot of people are moving towards, like, we have Percona Monitor Management, but Grafana toolsets or other tools that give more of the visual. But sometimes you don't have that access, sometimes you just have access to login and a shell and you need to get data quickly. I think that Pepe mentioned one of the most popular ones, which is PT online schema change, I can tell you that the most dreaded thing in any application deployment is the actual migration or the deployment of code to production when it has large tables, large data structures, because a lot of times altering a table that's a terabyte, that that can take hours, if not days in some environments.

**Pep Pla:**  
And I've seen weeks, weeks.

**Matt Yonkovit:**  
Weeks, yes. And I think that's where having some tools or something to help with those schema changes is important. But also to be able to quickly identify rollback two different versions is also critical. And I know other people have, I'm gonna sneeze I think in a second. Always one of those things in the middle. I think that other people have looked at tools like this as well like ghosts or other things to do similar things, sorry, muted while I sneeze, so you didn't get blown away. That's the issue with life is you can't edit out the sneezes. But there are different tools out there to do similar things. But I think having that in your toolbox as a  DBA, or an SRE is critically important. I think one of the other things that’s also often missed, or often kind of overlooked, is drift between replicas, right? And so one of the tools that's been around seemingly forever is the ability to check to see if your data between a replica and Primary are in synchronous. So things like PT table checksum, or the ability to sync up. So PT table sync, right? Those are, those are things you might not think about or realize, but it's so easy for someone to go into one of your replicas, and accidentally delete something, or potentially to have something fail, as replication moves data from one node to the next,

**Pep Pla:**  
And are sometimes so sorry. 

**Marcelo Altmann:**  
So or even like when you're provisioning eyes leave, like without GTD or this kind of stuff. It's, it's, I've seen a ton of support cases where you just started your replication from the wrong positioning or things like that. Yeah. In going to like to the backup subject, like once you have completed your, your backup, like, how do you ensure that you actually backup all the data like that your backup is consistent in this company that we had this backup lifecycle, as part of testing the Restore, in ensuring, marking a backup as usable, we use to restore the newly created backup as replica sync with Master in ruin PT table checksum to validate that actually 100% of the data that's supposed to be there, it's there. And the other thing you mentioned, okay, I have a drift. How do I fix this? To manually go and run checksum on every single table in select and dump jif? It's a nightmare

**Matt Yonkovit:**  
In a lot of data, yeah,

**Marcelo Altmann:**  
It's a lot of data. And normally when those things happen, like it's error-prone like you are under stress is someone like on your neck, when are we going to be back online, why these select works on master don’t work on on on the replica and knowing though, that you have those two there, it's like, ideally, it's like car insurance, you should never need them. But when something like that happens, it's always good to have that in your pocket

**Pep Pla:**  
I totally sometimes can have unwanted situations that I'm obviously always wanted. But what I mean is you have a crash in the source, then you promote a replica, and somebody starts the old server that comes in and starts accepting write. And all of a sudden you have your application is writing on two different nodes, you realize in let's say, three minutes, but you have 10,000 transactions that have been written somewhere, and you are not completely sure about the integrity of the data, having a tool, but then suddenly, you are really stressed having a tool that you can use and that you can use to tell your boss Take it easy. Well, it was a disaster, but we can fix it like I would say life insurance rather than car insurance.

**Marcelo Altmann:**  
Yeah. But one other point is that when you like you as a DBA will be prepared for that to have scripts ready. Okay, if I have a data drift here, it's and the chances are that you will have a bug or something on your script is very high. And those tools are out there for years. So they are already mature for this type of situation. So that's another thing to consider as well like there are tons of users that have already used it tested in maturity, the software itself.

**Matt Yonkovit:**  
Yeah. And Pep you came on to my podcast, and you said, Stop thinking about backups, think about recovery. And something that you said Marcello ties right into that, right? It's how do you test and ensure that those backups are consistent and you mentioned a really good practice which is sometimes restoring and to a replica and then doing that checksum to see did you capture everything. Can you do this process and it is a time-consuming process, you can automate those checks, right? Chaining these tools together is not going to reduce the clock time it takes, but it will potentially save you the time to sit there and type in the commands and wait for it to finish. But you can put that into an automated script that once a month pulls up the latest backup, restores it, and runs it up to a point in time. and then from that point on you can run a checksum and then you can check to see if the checksums match and if they do, you can call it green good and you move on, and that can be built into that process.

**Marcelo Altmann:**  
And one very important thing about backups, like the first thing, like, unless you can ensure that you can restart the backup, you don't have a backup. So it's just some files. And then also, like in a case of outages, it's always important to have those test practices that you do like in test environments to understand, like, what is the process to restore a backup in production? And how long does it take? So for example, in case of an outage, that I have to restore a backup, so you can communicate with the business saying, OK, to Restore a Backup, it's going to be at least six hours, it's going to be a day, it's going to be understanding how long it takes to complete the process. It's also something that it's really important to take into consideration and make it part of the lifecycle of the backup.

**Pep Pla:**  
Lots of people use logical backups, as a backup. And the problem with logical backups is that it can take ages to restore a logical backup, depending on how you create it, and how do you plan to restore it, it can take so long that it's not a backup, because it's not good enough to bring your business back in town, because it will take two weeks, so you can't, if you have any comments, you can say, okay, let's close those. And I'll call you in 15 days, you can't do that. So obviously, that time you need to recover a backup is even sometimes more important than recovering all the data. So you can escape some tables sometimes. Just to bring the race back as fast as possible. I like to define the backups, the untested backups as the shredding backup because it's a bunch of data you have, but you don't know if it's you're able to restore it or not.

**Matt Yonkovit:**  
Yeah. Let's take a pause. There are a few questions, a few comments. Let's throw them out there. Do we try to keep Percona Toolkit MariaDB compatible? The answer is there isn't a concerted effort. A lot of the tools do work. And Wagner actually did comment a little bit on that as well. and Wagner mentions that he has the Percona Toolkit, and it works very well. and once he started using it, he uses it everywhere, which I think that a lot of DBAs who have used the toolkit, it is one of their favorite downloads to use. and each one of these scripts Yes, it's a bit of science and how to apply it and use it and figure that out. But yes, the GTID format is the one that can kind of have some incompatibilities with MariaDB. But Wagner does say that the majority of tools do work there as well. Now, we do have this on can you use the toolkit on a Windows OS?

**Marcelo Altmann:**  
The short answer is no. It's like they are actually built-in using bash, perhaps like in the new versions that you can, like, emulate the bash. But what, when a customer has MySQL running on Windows OS, as you can still use the toolkit by having like a Linux virtual machine or Docker with these installed, and the majority of the tools that only require like, a connection to the database, like PT, online schema changes in those, you will be able to do that remotely from the

**Matt Yonkovit:**  
Yeah, so there are two types of tools in the toolkit, right? So you've got the database-specific tools, and you have the environment-specific tools, the environment-specific tools won't necessarily work the same way you might think. Now, I have used some of the tools using the bash and the bash like that you can install ubuntu on a Windows machine now. Right? And so it does run and I can bring up a terminal and do all the fun bash stuff and some of the tools do work. Some of them don't, right, it just depends on what's there. And so you've got that going for you as well. And I think Wagner says Cygwin. So which, which is the old way of doing it but I do the bash shell personally, because I've been running 10, right, we're on Windows 11. Now, 10 has been around for a while. But the database ones definitely will still work out of the box as well to do some of those things like checksum, or checking tables and things, or checking for indexes. Now, keep in mind, that toolkit was originally built like a lot of different tools, because we needed to get these things done, and we got sick of typing in the commands by hand. Right? I mean, that's really what this was all about was, how can we come up with a collection that everyone can go out there and use

**Marcelo Altmann:**  
and forgetting to command

**Matt Yonkovit:**  
a bigger thing, right forget the command and forget the other stuff, right? But, so they do work in a variety of environments, in a variety of settings, there's a tool to do a little bit of everything. Harry is happy that we say hey if you haven't restored the backup, you don't have a backup. It's interesting. So, I worked back in it seems like the dark ages, but we used to have to do quarterly disaster recovery drills, where it would be, it would not just be a restore the backup recovery drill, it would be a failover of everything to a secondary data center, try and restore off tape type of recovery drill, to make sure that everything happened. And I don't think that happens. as much anymore, especially with a lot of mediums, smaller size environments, I think bigger companies don't do that. But it is an interesting space. And, yeah a lot of people have made their own collections for checking replicas and doing checksums and different activities. That's cool. we're not saying toolkit is the end all be all to replace all of your custom stuff. But if you want something that has been battle-tested by 1000s of different companies, this is kind of our collective knowledge for people

**Marcelo Altmann:**  
Another thing, like the best tool that exists out there, is the one that works for you. Like if you have a bash script on your own, and that works you have tested, there is no reason to learn a new tool and over complicated things. So if it works, that

**Matt Yonkovit:**  
There is an interesting trend, I just picked up something on Twitter the other day about something very similar. It was, somebody mentioned, the fact that there's so much information from companies like Netflix or Microsoft or Google about how to run your IT organizations, people forget 99% of companies are not their size and don't need their stuff. Right. I think that that's one of the funny things that most people forget about, is like you hear about these great companies doing these awesome engineering feats, these feats of awesomeness that like, you're like, wow, I wish I could do that. But those are pretty unique in terms of the size of data, the volume that's coming in, and they don't work for all use cases. And I think that's something that people often mistake, like oh, well, I want to do whatever big company A does for backups, or for recovery or for performance. Well, big company A spent $100 million on that, can you? Probably not, so I think it's, I think it's worth noting. And, of course, there's Perl, I prefer Python, but I'm not going to get all persnickety on bash versus Perl versus Python. But you can, we can all have our own preferences. And I would recommend you all pick your favorite programming language and, and explore all the cool nuances that you can do. So Marcelo you were kind of in both worlds engineering and in the actual support space. So, you've seen a little bit of everything. What's the most unusual thing that you've seen in your time? Like, is there something that, sticks out? Like he's smiling? So he has something that immediately popped into a mind that he's like wow, this is one of these crazy situations. I like to collect stories and I'm sure people like to hear some of these stories and things they probably shouldn't or should do.

**Marcelo Altmann:**  
So, one of the things that I normally say that I advise everyone that wants to become a be a good DBA to not work for just a company, but to work in, in support of like a company like Percona, for example, because there are things you as a DBA, you will never do because there, there will be consequences of that. And you, you may not know how to come out of the situation you put yourself in. And one thing that popped into my mind right away is that I was in headquarters. I think the first time we met, and I was doing my shift there was a client that ran out of space. And he was using a database, named MySQL. And to save some space, he found a directory inside the data gear, named it, MySQL. And he said he never used that database. And he decided to delete that directory. So I think, I don't know. Yeah, if you use Oracle when you find a folder named Oracle, like, you will not leave that folder because like, that's the name of the binary you're running in search. So I, that was like the most, I don't know, the surprising thing I've seen a user doing.

**Matt Yonkovit:**  
Well, that is pretty. Pretty interesting. Right? like and what's funny is not doing like a drop database, but an rm. So when rm rf on the MySQL directory? Yeah, what I needed to clear up space, why wouldn't I clean up space?

**Marcelo Altmann:**  
I never use this database. 
**Pep Pla:**  
So yes, yeah, I've seen, I've seen people removing the InnoDB log. Because there are logs. So I have two large files in the home directory, that are just locked, I'm going to release some space. And I'll remove those files. And the good thing is that while the database is up, even after removing those files, you do not release the space. And the database is up and running, and everything is fine. But if you start the database, then you say bye-bye to those files, and it is not able to start anymore. So it's a ticking bomb, that probably the DBA who removed the files, as he was not aware, these files were important. I'll just remove the files and the space was not released. I'll remove something else. Yeah, a couple of hours later, when there's a switch of file or database stops, then all of a sudden,

**Matt Yonkovit:**  
Well, yeah, when you get here says he has InnoDB log files, right? They get removed, because who needs log files? Right? Log files could be removed. but no, that happens way more frequently. And those are the days where you really want to make sure your backups work. I think that is the craziest. And I've told the story a couple of times that I've seen in the backup space is you, you have your backups running in the wrong data center, and you've cut off access to that data center. And then two months go by and everything's fine. Something happens in the new data center, you forgot that you forgot to turn the backups on in the new data center after you flip. Oops, backups. Were running over there. But that data is two months stale. Is it the small things that matter? Quite a bit. Now, Harry had a question. So I wanted to get back to Harry's question. How do you know that your DB backup has been restored? 100%. How do we know that? Are there any scripts? Are there things that you can do? I think one of the things we had mentioned Harry earlier on was to set up your restored backup as a replica of the primary and then you can run a checksum to check to see if you know the data is intact. But what other methods have you, Marcelo and Pep done to check to see if the restore had actually been completed other than say it's done when you you know restore it

**Marcelo Altmann:**  
it's like I mentioned the one I actually used was PT table checksum. But this is actually a tricky question because I don't think there is kind of a right answer here because for example, the first 100 queries, okay, what if you were running MySQL dump and the dam was broken after the first 100? so there won't be a right answer here is it's really tricky. In my personal opinion, it's like provisioning, isolating, and doing a point in time recovery and running checksum will be the most guaranteed bond, but it's, it's hard to say that it will always be 100%.

**Matt Yonkovit:**  
Well, and I think I think it's one of those questions that I'm going to say the worst words in business, it depends. Nobody likes to hear that. But it's probably more accurate than not, which is like, are you doing like, point in time recovery? Are you rolling forward? What do you consider 100%, restored, right? Because if you take a backup, and you just restore it to the point the backup was taken, for some people that's 100%. For other people, they need to go to the second that they lost data. And even then, depending on how you've set up your database, you could be missing a second or more worth of data just because of InnoDB configuration parameters or other things or depending on how hard you crashed. So there's, there's a lot of variance when you talk about 100% guarantee.

**Marcelo Altmann:**  
And that something pops into my mind that once I switch it to engineering, one of the first things I had to work on was research regarding Percona XtraBackup locked DDL spare table. While I was researching a bug, we found out that the way like DDL per table was working before it could actually bring inconsistencies to a secondary index on the Restore, like your backup will run fine, your restore will run fine. If you query the table, by primary key, everything will be fine. However, if you query the table using a secondary index, there is no data there. So in like, that's why it's hard to say 100%. Like you can even like Runa check someone's case like these. And if the checksum is running on the primary key, it will not be able to spot this particular issue.

**Matt Yonkovit:**  
Yeah, and I mean, here's the thing, a lot of applications also make specific use of either unique data types, or even pointers back to file systems. So I've been working with people who have stored metadata directly in their database, and it points back to something like an image or a JSON file on disk. And a lot of times the metadata will be restored. But not that this is because there are two separate backups, right. And so you'll notice that a lot simpler as you get into sharted systems, the complexity of sharted systems becomes even greater because you have to do point in time across multiple sharded databases, which is a challenge. And a lot of engineering effort goes into databases that are sharded by default, a lot of times they can't even guarantee consistency across the board. And Harry to answer your question, specifically on the number of files or tables, that's not always going to be indicative, right. So looking at the number of table-level tables can restore. But the question is there one or two columns or rows that are missing? And as I mentioned earlier, we'll use InnoDB TRX. Commit setting, right, so there's a setting InnoDB, that if you set it to one setting versus another, it will force commit, so you'll have more consistency, but if you change it, you can make it so it delays committing data to disk so you can get better performance. Having that set, you could lose a second worth of data and you wouldn't even notice it. like it would come back up the database would be restored, but you couldn't roll to that second, so sometimes you can lose a second or two. Sometimes you can't

**Pep Pla:**  
There's something quite simple that will not provide you 100% Insurance. But you have to just look at the logs too often for warnings and errors, I couldn't write this file, sometimes the backup ends up done. But there's some information that tells you that we had problems doing these or doing that or reading that, that information. So it's important to check the logs, do a quick check, search for the most common error, warning, attention and things like that is also very important. And at the end of the day, it's really an old paper called reflection on trusting trust. And there are so many things that can fail or can be broken because sometimes you are making a backup from a corrupt database. Yeah, running finds the backup will not be in the same shape or, or you won't be able to see the same data just because the source of the backup was corrupt. So there are tons of things that can go wrong. But this doesn't mean that usually, backups go wrong. Usually, backups go fine. And even says Done.

**Matt Yonkovit:**  
This is why a lot of people employ a strategy for backups that is multi-tiered. Right? They'll look at file system snapshots, as well as logical backups, sometimes they'll do table-specific backups, any like that there are different kinds of backup methodologies in what you're doing. And I think that sometimes defense in layers is the answer for a lot of people.

**Marcelo Altmann:**  
And I believe like the In summary, we can think that we need to be prepared for the most non-issues, but you will never be prepared for everything.

 Yeah, and I mean, generally these are, these are so rare, and a lot of cases that you would have you take a backup on a corrupt system, and you don't catch corruption during the backup. It can happen but let's not scare people because you're talking about something that is so infrequent, you might see that once in your lifetime, it probably never in your lifetime.

One thing that we always favor in Percona XtraBackup development, everything that we know that it can fail silently, like, we know that people usually take a backup and on like prepared the backup, they only prepare when they need to restore. So we always try the things that we know that can possibly either fail or be prepared when you restore, we favor how things backup while you're taking it. So that is something that people will notice, like, okay, my backup did not complete, rather than it completed the backup, but it failed on the Prepare phase. So that's one thing we always favor, like trying to exit as early as possible in the backup stage.

**Matt Yonkovit:**  
Yeah, and I think that this is where we're trying to do a lot to protect things because backups are so critical. And it's important to note that a lot of engineering effort goes into testing backup and restore processes and the tools that are out there in space. But I think that it's mindful for everyone to realize that hey, there are going to be some odd things. Make sure you have multiple backups, don't just keep one, right? Like, don't just have like, I'm going to have last night's backup. That's it typically, like some sort of rotation for a week is a recommendation, maybe store once a month off-site or something if you're going to send up to s3 buckets, that's cool. But realize that that does take a fair amount of time for bigger datasets to pull back from s3 as well. So often having one online will be a best practice, but you also should encrypt those backups. One of the biggest issues you see with data leaks right now is unencrypted backups in s3 buckets. People take the backup, they dump them out there somebody comes, grabs the backup, tests your recovery for you, which is awesome, because, congratulations, your recovery work. And now the dark web has your data and they prove that your backup works. That is not recommended just in case anybody's you know wondering. That's not a recommended best practice for testing your backups. Okay? Just saying so you're gonna want to do things like that, um I if you're running in the cloud, I do like file system snapshots, if you're using LVM, I do like file system snapshots still I think those have their place, occasionally, especially for certain workloads. So, I mean, there's a variety of things you can do, you're going to want to make sure that you set things up. Now, Harry, to answer your question here. He's asking a lot of questions today. Thank you, Harry, for asking so many excellent questions. Are there pre-steps? So so there are a couple of things when you talk about pre-steps, there's the stuff built into Percona XtraBackup that does some checks, right, Marcello, there are some things that do to prepare the backup before it runs, but one thing that you have to be mindful of is there's a reason that people backup hot. And that's because the performance on a lot of systems is so critical. And doing some of these steps, depending on what they are, yeah, they can lead to higher amounts of consistency, but it can lock the database or prevent certain activities from happening in a timely manner. So right because when we used to do MySQL dumps all the time, and that was our main method of backup, grabbing a database level lock or a full lock, there was something we would often do. And then and those big datasets three days later, when people could start actually doing stuff again, in the database, we'd be like, whoo, we're done. But it would lock for a really long time. So what can you do? But thank you for the excellent questions. And the comments, if you didn't see there was a couple other the blockchain for consistency guarantees, which is interesting, I've seen that actually, that there are a couple of projects in different databases, to try and employ that not necessarily for backup, or guarantees, but for auditing, which is in which is another interesting use case, right? Because you end up having transactions that you're like, that was who did that transaction? Why did it go through? And how can we prove who did what? And so I think that blockchain has some interesting implications if used correctly. But again, there's overhead to each one of those kinds of protections that you implement. So that is something to keep in mind. So, we're all caught up on questions. But thank you, everybody, for the excellent questions. So we've got about five minutes, but we can go over if more questions come in. Marcelo, or Pep, was there anything that's that with? We tend to start these off with a few topics, but then we go where the audience takes us, right? we go wherever they ask questions, and we don't know where that's going to be. Was there anything that you really wanted to make sure that we told people about today? As they look up, and they go, No, not really?

**Pep Pla:**  
Well, we already said that, but you need to test recovery at least once. Just to have a set of scripts to be able to perform a recovery because you don't want to learn how to make a recovery while your data is stopped.

**Marcelo Altmann:**  
Lifetime advice.

**Matt Yonkovit:**  
I disagree because I like excitement. Doesn't like the excitement and the pizzas of learning all

**Pep Pla:**  
I had a workmate that had a sticker on his laptop that said real men make no backups if you like risk, don't do backups and it's like

**Matt Yonkovit:**  
ah, yeah, that's living on the edge right? So you know who doesn't want that kind of adrenaline I'm sure that's something that we all strive for. Marcelo, anything you wanted to close up on?

**Marcelo Altmann:**  
I would say from an engineering point of view like if anyone out there has features that they would like to be implemented on Percona XtraBackup or they have questions. We have a forum at percona.com where myself and other engineers and people from services are always engaged to bring your questions out there. If you have some feature or anything that we would like to see implemented on the tool, we have jira.percona.com, where you can raise a feature request. And those are always very welcome. And people that feel like it, we are open source. So just try to implement whatever you want yourself or fix a bug and open a pull request, we will be more than happy to review and engage with you from GitHub.

**Matt Yonkovit:**  
So we got a question from a hftmayo. I think I'm pronouncing that right. But hftmayo wants to know if there's anyone on one style now, I seem to remember, then a doctor Percona XtraBackup. Whoo like, like, Persona sticks in my head. Yeah. Who could that be? Who could hook it? Oh, wait, that is our one and esteemed guest. Here. I'm so so hftmayo. There are a couple of YouTube videos out there on our channel. So Mr. Pep here actually talked about this extensively. if you prefer video, there are also some blogs on our blog, that you can grab that as well. But let me see if I can post a link here into the chat for you. If you wanted to take a look at his specific series on that he did a Percona live Oh, that's the second one, I should have posted the first one. But you should be able to get the link. It's a two-part video if you really want to know the ins and outs of Percona XtraBackup and how to use it for your backup strategy. We also have a couple of podcasts where I sat down with Pep and a few others where we talked specifically about backup policy. So those are a couple of other good resources to get to. So I would recommend though but appreciate the question. Thank you very much for doing it. Now, for those of you who are still on and we've got 15 people right now watching. If you haven't liked this, like it, please, it helps us out and subscribes. That way you can get notifications when we go live again. and we would love for you to come back and hear us talk next time. So again, I said the schedule is going to be a little wonky between now and the end of the year just because of holidays and whatnot. Next time we're going to skip next week, and then we'll come back and we should be talking about Postgres. And then we'll be moving on to PMM, before hitting Mongo and MySQL again. So we try and rotate technologies and invite different people. And if there are people who would love to come on and talk live with me, this is not a Percona show. I mean, it is a Percona show just because it has our logo up there, and I work for Percona. But I love to have people who are not from Percona. So if you would like to come on. So yaki Wagner. Come on, you come on talk, I don't mind. Come on, come on, come on, or anybody else out there in the community. Feel free to jump in and have a chat with me. We'd love to hear from you and see what kind of cool things you're doing. And here's the thing. We can do this in multiple ways. When you come on. You can talk like we talked about today, if you want to show some slides, show some slides. You want to get down to the console accounts, like do we're here to showcase, answer questions, show people some awesome things. we're here for the community. So we do appreciate all of you hanging out with us. We know you have some choices for where you spend your time. So I'm glad it's here. But thanks, everybody. We appreciate it and we will see you next time.


![Percona MeetUp for MySQL November 2021](events/percona-meetup/cover-mysql-november-1-1920.jpg)

Backup is very important to reconstruct your database when loss occurs. Our Community Meetup for MySQL in November will be hosted by Matt Yonkovit, The Head of Open Source Strategy (HOSS) at Percona with participation of Marcelo Altmann, MySQL Software Engineer at Percona and Pep Pla, Consultant at Percona. We will talk about backup during 1-hour live streaming and answer questions right away. Let's tell you a little about our speakers.

Marcelo Altmann develops Percona Xtrabackup and is very experienced with MySQL backup solutions. Percona Xtrabackup is a combination of xtrabackup and innobackupex and can back up data from InnoDB, XtraDB , MyRocks and  MyISAM tables. Marcelo has spoken at many conferences, [blogged about MySQL](https://blog.marceloaltmann.com/) , and even participated in the [HOSS Podcast #21](https://www.youtube.com/watch?v=wUqxEqBIJlQ). 

Pep Pla has been working with MySQL in practice for many years and seems to know everything about backups, so we called him. He has already given a great talk at Percona Live 2021 and participated in the HOSS Podcast #23: 

* [HOSS Podcast](https://www.youtube.com/watch?v=sDG5BOAHJhY)
* [Dr. XtraBackup or: How I Learned to Stop Worrying and Love Backups I](https://www.youtube.com/watch?v=X-Ef0pyyBjM)
* [Dr. XtraBackup or: How I Learned to Stop Worrying and Love Backups II](https://www.youtube.com/watch?v=CamzaJGpnvA)

Join for an hour MeetUp for MySQL

* Day: Wednesday Nov 3rd, 2021 at 11:00 am EDT/ 5:00 pm CEST/ 8:30pm IST
* Live stream on [YouTube](https://www.youtube.com/watch?v=FMFu6aFZx64) and [Twitch](https://www.twitch.tv/perconacommunity)
* Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NjIzMGF1YTgyZnRzdTZqNmg1ZmN2bTZzZGNfMjAyMTExMDNUMTUwMDAwWiBjX3A3ZmF2NGNzaWk1ajV2ZHNvaGkwcTh2aTQ4QGc&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

## Agenda 

“Database Backup and Xtrabackup” with Marcelo Altmann and Pep Pla

* Backup solutions out there
* Best practices and wrong strategies
* Get the most from Percona XtraBackup
* The Schroedinger Backup

The Percona Community MeetUp is a Live Event and Attendees will have time to ask questions during the Q&A. All kinds of feedback are welcome to help us improve upcoming events.

![Percona MeetUp for MySQL November 2021 - Pep Pla](events/percona-meetup/card-mysql-november-pep-pla-1920.jpg)

![Percona MeetUp for MySQL November 2021 - Marcelo Altmann](events/percona-meetup/card-mysql-november-marcelo-1920.jpg)

## The MeetUp for MySQL is recommended for: 

* User of MySQL
* Student or want to learn MySQL
* Expert, Engineer, Developer of MySQL
* Thinking about working with database and big data
* Interested in MySQL

**Go ahead and come with your friends!**

Subscribe to our channels to get informed of all upcoming MeetUps.

Invite your friends to this MeetUp by sharing this page.