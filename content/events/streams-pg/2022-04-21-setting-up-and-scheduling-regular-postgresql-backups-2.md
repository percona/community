---
title: "Setting Up and Scheduling Regular PostgreSQL Backups (Part 2) - Percona Community PostgreSQL Live Stream & Chat - April, 21st"
description: "Learn more about backups setting with experienced Percona experts to ensure that your data is secure and safe on April 21st at 3:00 pm EDT  / 08:00 PM CEST"
images:
  - events/streams-pg/pg-stream-week-3-cover-2.jpg
draft: false
date: "2022-04-21"
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---

![Percona Community PostgreSQL Live Stream & Chat - April 21st](events/streams-pg/pg-stream-week-3-cover-2.jpg)

Join the next Community Live stream for PostgresSQL and learn about the best setting to protect and restore your data. This is the second part of the previous stream. Matt and Charly will continue to talk about database backup settings, frequency, and different types of backups. Come up with your questions and our experts will answer them live.

## VIDEO

{{% youtube youtube_id="7ZdQ4xjX464" %}}{{% /youtube %}}

## TRANSCRIPT

**Matt Yonkovit:** 
Hello, everyone, welcome to another Live Stream. I am Matt Yonkovit, the HOSS here, at Percona, Head of Open Source strategy. I'm here with Charly, my colleague. How are you doing today, Charly?

**Charly Batista:** 
Doing good. Good. Thanks, man. How about you?

**Matt Yonkovit:**
Not too bad. I'm hoping that everything is working. We're back at home. Last stream, we were at Postgres Silicon Valley, the sound was not great. We had to do all of our portable studio. So hopefully everything's working now. Give us a wave out there in stream land if you are hearing everything. Okay, and seeing this. Okay. Let us know that you're out there. Watch it. So we are here to talk about backups again. Because, Mr. Charly, he had some issues last time with his backups. What, Charly? What kind of issues did you have with your backups last time? Remind me?

**Charly Batista:**
Well, you mess up with the server. 

**Matt Yonkovit:**
It was an autovacuum issue that actually prevented our backups from working, which was interesting.

**Charly Batista:**
We had a few things, right. So it's a collection of events. So the database, we were waiting for the database to finish the flush of the data, and then the vacuum came in and everything start to slow down. And we had a lot of tables are waiting for vacuum. And so all this that many things. And this is one thing that we can have, you can expect in production, right. And that's why usually when we have backups, we want them to work, not doing the latrine the time that the database is working at its maximum speed. Usually. We schedule them to happen during the nighttime and this kind of stuff. So we do not put so much pressure on the database. Right. But we we work it out. Right? So well actually had a problem that the server was not responsive. And they needed to ask my sis attorney to restart the box.

**Matt Yonkovit:**
Right. I was interested in it. Yeah. So that's a whole another thing when an AWS instance goes wonky, what do you do? And one of the checks had failed. And it had we spent running since our last stream. And at some point, it lost some connectivity, which was definitely something so plus one, two, getting ha up and running. Right. 

**Charly Batista:**
We moving towards that topic. Eventually gonna get there.

**Matt Yonkovit:** 
Yeah. So okay, so Charly, you're here to walk us through the rest of the backup thing. At the last one, we had the backup running, the backup had completed. And so we were at the point where we had a backup to restore it from.

**Charly Batista:**
That's an important thing. I went there. And I checked the backup, I tried to restore the backup. And guess what? It failed? The backup was inconsistent.

**Matt Yonkovit:**    
Why was your packet? Oh, due to Charly?

**Charly Batista:**
Oh, that's a good question. You know, maybe something happens when there's the server just went, went crazy went out. So the thing is, we need to check the backups, right? So that's when bad things sometimes turn out to be good things. Right. So today, we need to do the backup again. So and remember that Yeah, last time, we started talking the whole process what PG base backup does, right it, we went manually and try to reproduce what it does, right? So remember that we executed the instruction, the Select to start backup and then we use it Arsene, to backup and everything. So that that's demand or process, right? So we went to the database, he told the database, look, I want to create a backup. And we gave to that backup, a label a name or an alias, let's put it this way. And then we have a consistent point in time. We could start copying the physical data, right using our sink. Well, it never finished. It never finished. Well. That's all we have that those problems never finished, the server went crazy and so the backup was inconsistent. Okay, now that we have a good understanding how the PG base backup sort of works, before we go to the PG base, back Crap, we gonna still do some manual things? I'll share my screen. Just a second. Okay, share your screen. So can you see my screen?

**Matt Yonkovit:**    
Oh, look, we've got a screen.

**Charly Batista:**
Yeah. Okay, what I was saying is, so let me go back here, let me connect to the database. Not this one. Okay, I connected to the database. So we did this PG Start Backup last time. And we try to cope and everything. So that is another way to simulate manually what PG base backup does. And we can use the replication up protocol to ask the database to copy the data. And this is what we're going to do today. So I hope it's going to be faster. And to do so we're going to use PL SQL. So I want to use the FPS club and tell the PL SQL that I want to use the replication protocol here, instead of let's put them this way, a normal connection. So here I'm telling the database look, I open this connection to the database. And I want to sort of walk through the replication protocol, not the normal protocol that we work with the database. Right. So this is one thing, when we go through the replication protocol, we have a lot of few more things that we can do. It's on the documentation. And one of the things that we can do, for example, is to check information about the system information about the server we're connecting to, for example, here, I want to ask the server to identify the system. So what it's going to do is it's going to tell us what is the timeline? Well, the server didn't do any recover. So we still the first timeline. This is the lsn lock position that we have. And this is an identifier of this instance of the server here that we stole. It will be important later when we start creating a replication environment. When we have a primary and different modes, we will see that every node will have its own system identifier, its own system ID. And they are used by the replication protocol. We're not going to go deep today. But this is something that you can do. Another thing that we can do here, we can tell the database that we want to do a backup, right? And remember that we are using a base backup, right? So what we want to do here is just to do it a base backup, a base backup. So I will tell that the label, what is the label that I want for my base backup. Let's put here, I don't know that back that one, so it's just a label. I can give him some instructions. If I want the backup to copy the wall, if they want the backcup to do a fast knock homage. I just forgot. I flush to the data. So I can instruct that but the backcup here to go for more. A lot of options. What I want to do is I want it to be if we need to do any flush here, the database to try to do as fast as possible because we want to have this backup to finish. I do want to cop the wall files. And if I just ran here, what we're going to have here is a stream of the because it's going to send into the system output. But I don't want to send the system output I want to send this to save to a file and this backup that's done here. It's not compressed, but It's use a tarball. So I can send everything for a tar five by four, for example, we have the folder backup. Let's call it just call it backup. One, I have some stuff here, doctor, right? So I got to send there before, let's go to our folder backup, to see if we have anything here. So we have those backups that we've blamed I've been before I go on to remove them, because we don't have that much space. So we all have 43 gigabytes available. And as we see here, the backups around 47 gigabytes, so we need to do some cleanup, right? So I'm just removing them. Okay, nothing here. Now we have enough space. And we can run here. So it is blocking because it's a blocking operation, right? So P escrow will only return when it finished. But if we go back here,

**Matt Yonkovit:**    
We wait. You just mentioned this as a blocking operation. So you can't run this on a live system.

**Charly Batista:**
Now it's a blocking operation for the TSP well, not for the command their command. 

**Matt Yonkovit:**    
Yes, that's what I call, just to be sure it's not like it's locking the entire.

**Charly Batista:**
Now if we go here, you can connect to the database. Let's see how many databases we have. Let's do a, the events, let's check whether the events we have here. So we want to we want to see that we have the backup somewhere here. Yeah, here we have the backup set. It's this Iranian is still active, we can even what are the database we have here. Let's connect to the database. Let's just create a new database, create database, the database test. So we connect to the database test. And then here, great table, T one, just ID integer here, right, insert into t 1x. From re T CDs 1212 300,000. So the database is still working. If I type correctly works, so the database is still working, the backup is running. So it's not a database blocking operation. Nothing is just that the command line here is blocked. Right? 

**Matt Yonkovit:**    
So it's just like I'm running in me you just gotta be careful when you use the term block this is this is gawking. Automatically assume that.

**Charly Batista:**
Yeah, so I watch here. Well, okay, CD backup. What I want to do here is we will see the progression, right? So the file is, is slowly progressing here. Remember, it's 4748 gigabytes backup, it will take some time to finish the backup. Okay, what I want to say to tell you is, this is exactly the same, the very same command that the PG base backup runs under than it. So under the hood under the table when you run a PG base backup. Mostly, this is what it's doing.

**Matt Yonkovit:**    
Let me ask you that because the thing that PG base backup isn't doing is it doesn't actually copy the files. That's why we had to go our sync them. So this is doing something a little different.

**Charly Batista:**
Well, no, no, no, no, no, hold on. Our sink we did last time is because we did everything manually. The PG based backup it does copy all the data, all the files that you have in our database. And that's why you can use PG base backup for example, to spin up a replica. If you need a replica. The easiest way to create a replica for in your primary is to use PG base backup to spin up a wrapper. The PG base backup will copy and transfer the data the whole data from your primary to the replica right. This is actually what it does.

**Matt Yonkovit:**    
Right. Okay.

**Charly Batista:**
It is this this command here this base backup command here. It what it does is it runs the SP You start back up. Remember that you were told that common the label name, this is the label name. Yes, some of the parameters here we also gave to him. Right? If one is faster if one it runs in parallel. So those are some of the parameters, they will be passed here as well. So the first thing that the colon does is to run, let's run this PG Start Backup. So it will run internally, it will create the backup the that the point in the backup structure. So now we are consistent. So if it needs to flush, anything to flush, and so everything happens here, right? So this is the first thing that it does. After that the PG base backup or this comment here, it will stream copy the files and the data, everything that's from the beta dir to in our case, we're sending to this file, right, we're sending here to this file, we're going to have a copy of our database inside of the of this file this doc file. It's a consistent copy. When it finishes, it runs a PG stop backup. Okay, so database.

**Matt Yonkovit:**    
So what you're saying is, this method automates most of the manual steps we did in the last one?

**Charly Batista:**
Yes, exactly. No, actually, it ultimately it fully automates the process, right? So because we don't need to do what we do the art thing, we if the only thing that we need to do now athletes finish, we need to  Anta because we it's, it's great in a tough file, we are creating a tar file, so we need to do and the PG base backup, we do it for us. Right? So the PG base backup will, when you run the PG base backup, we're going to run a PDB. After this, all it will do the whole process will have a full consistent copy of the database at that point. So we can stop this database and point the data here to this new database. That's the backup. So we're going to do that and start a new database there. Right. So this is one thing that you can do. Also, we can use point in time recovery using this strategy. This is important thing, we need to we can use PG point in time recovery. Right?

**Matt Yonkovit:** 
I do want to, before you get too far into that, while the backup is still processed, oh, it looks like it might be done or close to it. Yeah. Which is great. So here's something I wanted to point out to people who are looking at this command going, Okay, I'm gonna run this, this is something that is going to cause contention on the disk, it will slow down, whatever is running. And that is an important thing. For folks who are thinking about backups, especially those who are starting out in the space, and they're just learning about, you know, hey, I need to take a backup there, you will slow down your production workload.

**Charly Batista:**
No, that's true.

**Matt Yonkovit:**  
So just be mindful of that. By the way, folks who are hanging out, we are responding or throwing some chatter, but for whatever reason, things are being duplicated today. So we're seeing multiple responses from the Percona channel, in chat. So I apologize for the double or in some cases, triple messages. Lovely every day, there's something a little different. But back to back to the backups here. So okay, so do use this on a replica if possible. Do this during low usage times. We talked a little bit about when to schedule backups and how often in the last stream. I'm going to do some editing, you know, magic on that and do some smaller videos, because we went quite lengthy there. But okay, go ahead. Continue. Okay.

**Charly Batista:**
I have a question for you. Remember that the creative one database created one table inserted 100,000 rows in that table during the backup process. So if I spin up a mother Postgres replica, here, like, instance, here, we will we have that data.

**Matt Yonkovit:**    
Will it have that data in it? 

**Charly Batista:**
Yeah, probably.

**Matt Yonkovit:**    
Not unless you're replaying the transaction. actions, right? So if you set up the replica based on this and then you roll forward all of the transactions after then yes, it would have it. But if you are saying like I took a point in time recovery, or a point in time backup, I restore the backup. And during the backup, I did some work. By default, it wouldn't it would have to roll through those transactions.

**Charly Batista:**
Okay, here we

**Matt Yonkovit:**    
Can just say yes, you are right. And move on.

**Charly Batista:**
don't want to say, oh my god, you know, what are you gonna? What are you going to do, is going to stop the database now? Right. Okay.

**Matt Yonkovit:**    
By the way, if you love hearing me and Charly just bicker non-stop, I posted on my own personal YouTube channel today, the behind the scenes view of us trying to debug some Postgres database stuff. It's 30 minutes long of just us yelling at each other. It's, it's quite glorious.

**Charly Batista:**
Well, yeah, I wouldn't use glorious, but yeah, that is glorious.

**Matt Yonkovit:**    
Just say it's glorious, and move on.

**Charly Batista:**
Okay, let's move on. As you see, my database is not running. Just for the sake of double check. So, of course, to use a graph, right. So we don't have Postgres running. Here, we have the exporter for PMM. But we don't have the database run, right? So my database no running. Where am I? Okay, you're 13 These, these the main database folder, right? So this is what we have not. I gonna rename this main to old. So and I go on as extract. Gonna let me go here to the backup folder. Okay, I don't want to cry.

What we're gonna do here is just under this folder, this file. Well, it's taken some time. So are you going to untie this file, and I'm going to create a symbolic link to the postgres folder, right. So just replacing the folder, the original one from folder backup folder. Because as we are using a boon to here, it has some the parameters for the configuration files is pointing to DTC flash pulse degrees, and blah, blah, blah. And when I want to bother changing those things, it's easy just to change the file name. I thought you you improve the disk performance for this this box because your box is pretty small. I mean, the disk is.

**Matt Yonkovit:**    
It is. I mean be. It is named CharlyDB.

**Charly Batista:**
I can tell it's likeю

**Matt Yonkovit:**    
This is all on you, not me. It's all on you. 

**Charly Batista:**
Let me see. Now you need to stay here. Hang in here for like minutes. We can just open our file like this. Well,

**Matt Yonkovit:**    
I didn't tell you should prep for this ahead of time. I didn't say that to you. I said, make sure you have things ready to go. Make it so Allah Beatty. So people don't have to just sit here and watch because now you're stuck. Just giving witty banter, right. And so people as much as people love witty banter from Charly and Matt.

**Charly Batista:**
Okay, let's let's do an RV while we wait. Let's go to etc, possibly is the configuration what is the configuration through TMA? There is one thing here that I want to talk with you. So not the max number of connections. One thing that's important for us to do point in time recovery. And even for application when you're talking about replication are the wildfires, right? We need to the database needs to have the wildfires to roll for what the data as you just mentioned, or for the replicas to be able to keep replicating from the database. So the database we'll see save those wall files inside. Inside of this folder, PG wall, on the newer versions medicine, your versions, I think the changes on PG 10 or 11, I don't remember before the name of the folder was PG x log. And then they people found out that x log gets confusing, right is because you can confuse if the the log files, that is not the wall files, and then they rename it for PG wall that makes a lot more sense. So the database save or saving all the files inside of this folder here. The thing is, in our configuration here, each file is off 16 megabytes, we can change this, this is valid besides the parameter. And what I want to say is if we have 1000 files of 16 megabytes, we will end up with a lot of files, right? If you have a million of files all deep can grows quite significantly and fast depends on your workload. So we on the configuration file, asking the database to do a cleanup or to only keep certain amount of files or a number or age. So if you have more than 1000 files and the database, start removing the old ones, or if you have a file that's older than one day or a few days that database start removing on so the thing is, at some point, those files will be removed, right. And we need to have a way to keep or archive those files. So this is what on the configuration on the parameters. They call archive. So the archive mode, I've changed it already by default, this here is off. By default, the archiving mode is off, and why the folder archive columns is just empty. So I change it to one now we have archiving mode. And what we do is we caught those files when they were created when they sorry, when those files. When we create a new archive files were copying the old build files to this folder here we are using our sync to COP this is the full path. As we see the placeholder. Percentage p is the path of the file that we want to COP. This is the PG wall is slash filename. So this is the full path of that file, it will copy or in my case are seeing that that file to this folder. Right. So this here is enough for us to have archive for what we're going to do the point in time recovery. So we have those four files. But for that to work, we need to tell the database. What is the level of wall that we want to the database. As you can see here, the default is replica. So replica is enough to do point in time recovery. And even for replication, if we were build a replication, using physical replication, this is enough. That's why I didn't change anything here. Later on, we're going to change for logical when we start playing with logical replication. So we need to change this. What does it mean is it will put less or more data or less or more information side of the wall fires. Now the amount of data we're saving to the disk is smaller or larger. The mean or value, as suggested here is minimum. For the minimal you just save the NEEMO data for the database, the database recover from a crash. So if like you need it, restart this box, right? When you start restarted this box, the database was running. So it was a crash. It was a huge crash because it was the whole box. When they restarted when I started the database, the database needed to go and do a crash recovery. So we went to the World files to see if something that committed needed to be replayed, something needed to be rolled back. So all that crash, recover and clean map all the data files. It's done because we have that information on the world files right. So the minimal guarantees that we have that minimal data for the database recovering from a crash. But if we use minimal we cannot do point in time recovery and we cannot have replication We don't have enough data for point in time recovery. And we don't have enough data replication. So we need the wall level to be at least of replica, which is the default. So for now, the default is enough for us. So we can do the the point in time recovery as we intend to. And we do have WAR files. So

**Matt Yonkovit:**    
And right now, both the server is not, it doesn't have any real workload on it. Now, Charly, while you were sitting there, your SIS admin, Gus, the sysadmin. went ahead and added another disk to this box. So it's under SDS. So So So Gus did that for us? So you will have to mount him on that, but it should be. Yeah. So we should see that. 300 gay or 300? Gig one?

**Charly Batista:**
Okay, have this one. That's true. I won't have here. Should be.

**Matt Yonkovit:**    
That's not the same one. Right. There's two. Yeah. So there's two 300 Gig ones. So I think it's the second one, isn't it?

**Charly Batista:**
Тvm 00. Yeah. And this is nvm. zero and one. Yeah.

**Matt Yonkovit:**    
So this is solid state, this has a, a much higher reserved IO throughput. So our property just for you.

**Charly Batista:**
Thanks, sir. That's highly appreciated.

**Matt Yonkovit:**    
Now, now you can use it or not use it.

**Charly Batista:**
I will, I will. So like, not for now, let's let's let me finish the one thing then we go back here, right.

**Matt Yonkovit:**    
Hey, Mahesh said that he had the same question asked in an interview today. Which question was that? Was that about? Like the wall? Settings?

**Charly Batista:**
Oh, yeah, that's interesting. Well, yeah. What

**Matt Yonkovit:**    
Is the Charly, did you interview someone today? No,

**Charly Batista:**
It was not me.

**Matt Yonkovit:**    
Oh, okay.

**Charly Batista:**
Yeah, yeah. But I hope he went well. Yeah.

**Matt Yonkovit:**    
Yeah, let us all know, we want to know if you did well in the interview, and hopefully you did.

**Charly Batista:**
Yeah. And it's, and it's good to see like, some of the content we, we see here people are using out there right. So indeed, yeah, that's, that's good. Yeah, that's, that's pretty cool. Okay, at this point, we have this one here. I want to remove the backup ah, I'm not going to remove we're going to move the backup I got to be safer. Q Okay. So we have a physical copy of almost everything from our database. And I say almost is well, it's not everything and we'll see I missing here one file that's for configuration when we started it's used by PG CTL to start the database and we'll see that the database is going to complain when I tried to start with the girls but so okay. So what he wants to do here is a symbolic link backup and here I kept one two yr leap, PostgreSQL 13 Main. So, we have now our main folder. So if I go to that one, this is what we have. And theoretically, if I run here, a PG CTL. I only like to run a restart. So it should work right? Because this is the main folder, the data G so the configuration files are all pointing to these here. We have all the data it should work right. But he didn't and it said it doesn't have the postmaster PTS file. And remember that I told you it copied almost all the files. Now almost. That's almost Yeah, that almost it's what sometimes makes we look bad, right? But I was expecting this to happen. And as I was expecting this to happen, oops, not me, it is bold. What they're going to do is we're going to copy this file because I don't want to type it. I could, what apps file, I want to open the file, I knew you would ask this question before I open, so what it does, it has the command to it, the coma tree starts both with pointing to the folder where we have the configuration files. Because you belong to use a different end Debian use, put the configuration file in a different folder that's not inside the data dream. And Postgres is confused. So we have the, it's, you're going to use Postgres common to start the database. The dash d is the data G N dash c is the caterpillar Rifai, the configuration file. So those, this is just the common to be run that's put on this way by PG CTL. So I could just copy this here manually and start Postgres using. But I like to use PG CTL. Salt. And now it should. And it didn't start. Well. What is the problem now?

**Matt Yonkovit:**    
You didn't set the permissions?

**Charly Batista:**
Oh, I didn't set the permissions that Yeah, that's true.

**Matt Yonkovit:**    
Yes. Set the ownership in the

**Charly Batista:**
well, the only ship there for FOSC is because I'm using the user Postgres so

**Matt Yonkovit:**    
Oh, yeah, you did. But yeah, so probably, it's too permissive, isn't it?

**Charly Batista:**
Yeah, it is. It is that we say it's, it's saying that it's using 750. That's too permissive. And we need to use seven Oh. Right. 

**Matt Yonkovit:**    
Ыecure your latest. Yep. Please. Don't hack me in there. Don't leave my data accessible.

**Charly Batista:**
Exactly. It's, it's asking you please can you give me this favor? Well, I want to do this here and also in the backup the regional folder that is backup one. Okay, well, now we shouldn't be able to start right. Come on

**Matt Yonkovit:**    
Нou're missing the PID file

**Charly Batista:**
Oh, that's fine. Because here's this trying to stop. Just forget about it. It's the log starts here. Okay, it couldn't start the server. Let's check the logs right, it say that we should find information inside the logs that go to the log. I hope we don't have that many logs. Okay. 

**Matt Yonkovit:**    
The today's 21st should be like the last time we did this when our logs were like streaming errors. Yeah, by the way, this is if you check the server name. This is Charly dB. So anything that's wrong is officially Charly's? No, it's missing var run PostgresSQL right. So yeah, it is.

**Charly Batista:**
Yes.

**Matt Yonkovit:**    
So a problem in and of itself.

**Charly Batista:**
We could change the configuration, but then again, I'm lazy. I'm just create points in there.

**Matt Yonkovit:**    
Is it a permission issue then? Probably. We can't create that in that directory.

**Charly Batista:**
Probably. So is our is response greens pulse response. That was the last line Sorry, can I say it again?

**Matt Yonkovit:**    
It was right there. Here you got it.  What was your error again? So is that a directories of temp directory? That's creating?

**Charly Batista:**
Yeah, it's trying to use so. Okay.

**Matt Yonkovit:**    
You're going to try and create it, aren't you? Set Oh, it was a PG stat monitor here. Where? Yeah, isn't that a PG stat monitor thing?

**Charly Batista:**
No, no? Well, that's a good question. But you know, I got it just great is a Postgres? Oh, I just want to run my database. We can investigate it later.

**Matt Yonkovit:**    
You totally need to investigate that. Yes. And here we go. Yeah. So because I think actually that's preventing that from auto starting. that I think might be a good though. Yeah. Because the server installed by Charly was having some problems auto starting. And you know we need to go back and get that fixed.

**Charly Batista:**
Okay, I kind of didn't hear that. So

**Matt Yonkovit:**    
If I said it, I said it. The viewers out there heard it.

**Charly Batista:**
I have the folder test.

**Matt Yonkovit:**    
Yes, I see this. I see there

**Charly Batista:**
They have they would want.

**Matt Yonkovit:**    
I see this. I see this. Yes.

**Charly Batista:**
How is that possible? What happened? You told me it won't be here.

Like, I want to count because it's 100,000 rooms. I don't want to get it.

**Matt Yonkovit:**    
So the backup rolled through all the transactions, all the wall logs up until the end? It's all finished.

**Charly Batista:**
The answer to this question? I think we just lost it.

**Matt Yonkovit:**    
What do you mean it? We just lost it?

**Charly Batista:**
Yeah, it's because I cannot go back here. I'm using the screen. And they don't have all the the answer to this question is in the end of the backup process? Seriously.

**Matt Yonkovit:**    
Just explain it and it's fine.

**Charly Batista:**
Yeah, but I want to show you because you might not believe me.

**Matt Yonkovit:**    
I know that you are 100%. Wrong. Though. Now, if you think that Charly is wrong? And I'm going to say yes.

**Charly Batista:**
Look, this is they asked for that question.

**Matt Yonkovit:**    
Yeah. All required? Well, while segments have been archived, yes, yes, yes.

**Charly Batista:**
So we do have all the date. Remember, when we did the backup, the backup is consistent at that point. So the database keeps working and working and working working. So but we can roll forward the data if we have those world files, right. So remember, the database uses the world files to do a crash recovery. So if the database says okay, yeah, I have this data set. But I also have those more files. I can take a look. Oh, I have some transaction that's been committed inside of those wildfires? Well, I think I should apply them because they've been committed. So and then the database just applies those logs.

**Matt Yonkovit:**    
Wants to know, are we going to do another yet another backup? Yes, because one of the things that Charly has not used yet is PG backrest. And PG backrest is what we recommend to actually run the backups, because Ceri, Charly and his thoroughness is going to show you all the ways to run backups, and then tell you why you should never use those ways.

**Charly Batista:**
Oh, it's not that why you never should use those was that there are a lot of opportunities and cases that they're that sweeted to do some of those backups. But they are exceptions, right? Remember, we always have exceptions is not never because well never use never. Because we might have an exception, just like people say, oh, you should never use them because then it's not backup. Okay, but what if you need only one table inside of 100 terabytes database? Are you going to do a physical copy of 100 terabytes database done remove everything just because you need one data? It's better to use later. Right? And, guys?

**Matt Yonkovit:**    
Yes, of course. I mean, like there are going to be exceptions, right? Yes, yes. Yes.

**Charly Batista:**
Yeah. And another thing is you need to understand how the process works. Because what if you have a problem using PG backrest

**Matt Yonkovit:**    
All right, you don't you would, I mean, you would have to go do a backup some other method. However, if you have a problem with PG backrest and the data is corrupted or the backups are corrupted, that's a whole nother thing. But

**Charly Batista:**
to do so you need you need to find out if the problem if you're using PG backrest, you need to find out if the problem is the PG backrest itself or if the process of it, right so if you know all the mechanics behind that, you, you're able to start troubleshooting things, you know how the mechanics of a, a good backup works, it's easier to troubleshoot any tool you're using. Either doing everything manually, or using a nice PG backrest with a backup server is streaming with multiple connections and all those fancy nice things. Right. So and that's the main reason why we were walking through those things. Okay, the next step in to finish before we go to point in time recover is the PG base backup, right? So we need to do so we saw what PG based backups though, does by under the hood. Now let's use a PG base backup. And to do so we're going to use that nice new volume that you just created.

**Matt Yonkovit:**    
Nice new volume.

**Charly Batista:**
So I want to do before it really wash volume, create a need to do a while you don't have anything here AVG creates. I'm trying to remember here because it's been a while since Oh, so

**Matt Yonkovit:**    
So now

**Charly Batista:**
It has to decrease. Okay. Okay. So, okay, the name I got a call big data's here. Okay, then I can create the logical volume. I know. I gotta put here, the 100 gigabytes, we're going to call logical volume backup, and found the big beta i gonna use? Yes. XF s, because it's easier. And I need to create the file systemto read my manufacturers, and that's fine. So what we're going to do is we're going to leave the backup folder to old backup folder, we're going to create a backup folder where this is the best. And I got to mount this guy here on my backup folder. Okay, and there we have, I have the backup folder in that amazing, awesome new disk.

**Matt Yonkovit:**    
And yeah, so I gave you provisioned IO for backups. And then the regular the regular database is not using provision IO, which is silly. So you know, what you should do is you should restore to a provision IO

**Charly Batista:**
And that's why I only created this 100 gigabytes. This here because we're gonna use another 100 gigabytes for the database.

**Matt Yonkovit:**    
Okay, but you're gonna you're gonna, you're gonna contend, right?

**Charly Batista:**
Well, that's true. So you could have used the

**Matt Yonkovit:**    
Base disk for anyways, whatever.

**Charly Batista:**
That's okay. Yeah. Then let's do that. Alright.

Unknown Speaker  
This time urine.

**Matt Yonkovit:**    
This time I am right Uh, so don't doubt my superpowers.

**Charly Batista:**
I need to unmount

**Matt Yonkovit:**    
It just you just leave it as backup create another one. I mean, it's fine. Like, it's just, it was just a comment that, you know, if you're going to create a backup directory with faster disk, why not put the main database on the faster disk? It's a logical

**Charly Batista:**
That's that's ADCs. And that's this is what I'm doing now.

**Matt Yonkovit:**    
Also, don't forget to put it in fs tab to automatically have a restart.

**Charly Batista:**
I will, I will otherwise the

**Matt Yonkovit:**    
Database won't come back up and then we'll all be sad and the next stream and we'll sit around it's kind of staring at you going like whoa

**Charly Batista:**
Yeah, troubleshoot for like and now we just figured out it's not the volume is

**Matt Yonkovit:**    
So I am curious for those who are watching, would anybody watched Charly for two hours trying to troubleshoot a Postgres problem?

**Charly Batista:**
No, not at all I can make, I would not watch myself for 12 hours. Oh, come

**Matt Yonkovit:**    
People love Charly and the Chocolate Factory here, by the way, do you have any of that chocolate that you just carried on you?

**Charly Batista:**
Well, we always have some okay, it's up. I probably mess that up with some stuff here. Var lipo screws. Mine doesn't exist. Why it doesn't exist? It should.

**Matt Yonkovit:**    
You made it a link. A symlink.

**Charly Batista:**
Yeah, I know. And that's why it should exist. You moved?

**Matt Yonkovit:**    
Moved it. See. That's why.

**Charly Batista:**
Yeah, it makes sense.

**Matt Yonkovit:**    
Of course, it makes sense. Do you doubt my superpowers? I'm gonna buy myself a cape. I think I can make that happen. Right? Be cool.

**Charly Batista:**
The database is slowing down. I mean, the box is slowing down. I don't want my network

**Matt Yonkovit:**    
Slowing down the box is no traffic to it. It's you. I'm not even logged into the box. Charly likes to blame everything on me. He does.

**Charly Batista:**
And it's taken quite long to reply anyways. So let's start. Let me stop here. Okay, the database just stopped it. We just did a very nasty and dangerous thing here. We were playing with the data in the disk while the database is still running. Why is it that right? Yes. Well,

**Matt Yonkovit:**    
I didn't do that. I didn't do that. Yeah, I

**Charly Batista:**
Never do those things. This is silly, and can cause a lot of problems. It's stupid and silly. Right. So you if you want to move things around, please stop your database. Don't do like Matt that just asked me to do those silly things. And they agreed. Yeah, so don't do it. Right. Okay. So okay, why? Now? What are we going to do you please? And that's your fortune. All right. Now before you start complaining the screen

**Matt Yonkovit:**    
Says what does the screen say, Charly? Which screen? My camera. What is my camera say? I can't see your camera. You can't see in a little corner. It says it's Charly four. Oh, is arrows to you. So it is definitely Charly's fault. Hi, now Good. How are you? Thanks for joining us today. We're just going through and Charly was is restoring a backup to a faster disk on on an AWS instance. And in Charly's haste he forgot to shut the database down. And so let Charly you know show you is super magic as he restores the backup that he took because you know the database has crashed was all part of the part of the experience here

**Charly Batista:**
That's that experience.

**Matt Yonkovit:**    
Yeah, it's all part of the experience than the others and

**Charly Batista:**
Here we go again. Moving in here going and moving data from a very slow disk to another one that I hope it's a bit faster so I gotta I gotta have some water after that. All in a script right. So that that was we didn't purpose for people to learn what never don't

**Matt Yonkovit:**    
Do this. Don't do this. Yeah, so Daniel extra backup is MySQL only. PG backrest would be the recommended tool in Postgres. And Charly asked about you using PG backrest. I asked him earlier and he said he wanted to make everyone suffer through all these other things. First, do PG backrest Yes, well, yes. So people asking

**Charly Batista:**
Why not use barman and PG backrest? Ah, well, yes, yes. I,

**Matt Yonkovit:**    
Who sounds like he had a good interview today, by the way, so congratulations to manage. Yeah, he said it was it was good. So that's awesome. So why not bar man?

**Charly Batista:**
Okay, this is personal. I've, I had, I personally have few experience with Vironment, so I am not the right person to comment on those. But when I was researching, so PG backrest is a newer technology environment. So, it doesn't mean that Balmain is not a good technology, but I just choose because it was never a to speak in a language that like I can follow easily by typing a lot of Python, some C on top of it, so I am eager to do so. And that small in my case, I found easier to find documentation. And the people that I was working, they were outbreak and they feed you back fast. Right? So if you start a project, and you want to check it out, which one works better? So that's definitely something that he you should. And that is, in my case, there is no no much audit on those. Right. So I it's, they're both great tools for what I seem to be across has better integrations with new technologies, like I've seen a lot of tools and operators running the backup strategy using PG backrest on Kubernetes and thing because it's easier than to to integrate environment. So at least from that point of view that's it. Right so but yeah, well they again, they're great tools. I've seen all the companies using my environment and it's been working it's been there for for forever I really long time and does the job

**Matt Yonkovit:**    
Yeah, and yet again, we're you know, I kind of pushed Charly a little earlier on this as well as we were talking right. So obviously we would recommend using something like PG backrest or or even bar man but we weren't going to concentrate on PG backrest you know Charly, you know wanted to do that in the next session when I said oh are you gonna do PG backrest? He said no, I don't want to do PG backrest today it's so hard. I want to do this other stuff first and then I said fine, because I am a nice guy. But no, so yes, we would recommend that that's that's

**Charly Batista:**
fully true. That's all true. That's exactly what I read that I said you know, it's like I can see myself on those words.

**Matt Yonkovit:**    
Yeah, I think I have video of it. I think I do Yeah. Your your backups done so

**Charly Batista:**
Yeah, I'm copying and not copying I'm foreign leave also restarts me

**Matt Yonkovit:**    
Are you gonna do the point in time recovery in a second?

**Charly Batista:**
Yep. But to do so. Okay. I think a MSRP of something which does not support this folder yeah to Do the point in time recovery we need to have a database right right. And of course the database or at least well

**Matt Yonkovit:**    
Oh, what was that noise? That was a weird noise. Right. Which one you went out? That noiseI

**Charly Batista:**
So we have the database are, let's say, I go to my database I go to my database and that we have what's great here, the United State right? Let's say I have this table T one doesn't matter the name of the table so that they have 100,000 rolls from this to one and I was playing and I know that everything in POS was a transaction right? For example, if I do here begin and drop the table what do you think's going to happen if I do this here, man?

**Matt Yonkovit:**    
That if you drop the table without committing or with committing

**Charly Batista:**
Can I rollback this operation? Remember, this is a DTL

**Matt Yonkovit:**    
you should be able to rollback? That's right. I just pulled my cord out.

**Charly Batista:**
Some databases they don't allow, for example, my SQL DDL are not transactional. If you do a drop table in MySQL that's it it proper the table on Postgres Yeah, we can roll back. Roll back solve the table is still here. Right? Nice. But what if I do the drop table thinking I'm inside of a transaction but why could I not inside a transaction in more I just stopped at the table. Okay, that's that's quite bad, right? Indeed. And let's say

**Matt Yonkovit:**    
If I do a backup don't drop your tables.

**Charly Batista:**
Yeah, don't drop your tables. So if I can recover the table because they have the backup right and I just remember that I have the table on the backup that was a bad move. So I just did the wrong order. If I just recover the backup now I just recovered the table so only the point in time recover

**Matt Yonkovit:**    
Recover you should have deleted some data or added some data

**Charly Batista:**
Yeah, I should have added some data. Okay, let's just create the table in a backup again and then I got to add

**Matt Yonkovit:**    
The backup so he just that you already have the backup you could just restore the backup yet again

**Charly Batista:**
That's also works

**Matt Yonkovit:**    
Right I mean I guess it would be the whatever whatever way as fast it's

**Charly Batista:**
Faster Yeah, I think it's faster you should prevent me doing those things man you know how am I

**Matt Yonkovit:**    
The all of a sudden the Charly police How did I become the Charly police

**Charly Batista:**
Nobody should prevent me doing all these stupid things

**Matt Yonkovit:**    
There's only so much time in the day Charly

**Charly Batista:**
That was bad you know you should not say those things.

**Matt Yonkovit:**    
So here is a randomly stupid question that we should know the answer to. Right. So you cannot just restore the single table from that backup.

**Charly Batista:**
Because it while it's a physical backup, ah we if we need that very single table We need to do what I am doing here, we need to restore the whole database, do a dump and move to the database that we need that thing.  In inside of the database? Like an undo space?
Yeah, the thing. Remember, the thing is the recycle bin is a point in time recovery. It's what we're going to do now. Right? So actually, we will go back and try to get that only data that we need, right? The thing is once you commit your transaction, that's done the database, especially on a drop table, like just I did here, it's removed from it's literally removed the file from there once, right. So there are some cases that it's possible. Like, for example, if I do a delete the post grease marks those roles as remove, it doesn't physically remove those rows. And in certain circumstances, we can do really bad black magic, let's put it this way, and go inside of the data, the data file and change the marks. It's very dangerous operation and should not be done unless extremely necessary. Right. But for for file perspective, when I do a dropped table, it removes the file, well, we can still go to the to the file system and try to recover that file. So can in extreme cases, we can always try to do those unsafe operations, but as the name say, they are unsafe, right. So by that go for point in time recovery and make things.

**Matt Yonkovit:**    
So what you're talking about is a forensic kind of data recovery. Yeah, where you're using, you know, tools, like maybe like, PG wall dump, or PG file dump and looking for specific data and trying to mess with them.

**Charly Batista:**
Yeah, and some companies even have some in house tools that are built on top or the possible storage, how the works to you to try to recover those dates. What does it say? Yeah, those are forensic type of recover. They are dangerous. They did not. You know, there is no, there's

**Matt Yonkovit:**    
Also a plugin called trash can that I didn't know about.

**Charly Batista:**
Yeah, that's, that's new. I don't know.

**Matt Yonkovit:**    
I told it's from nine. I don't even know if it works now. But I just noticed that as I was searching around.

Unknown Speaker  
Oh, finally.

**Charly Batista:**
Yeah, everything that goes up from the old GIS to the new one. wine wine wine. Okay, we do have the backup, let's recover the backup. Let's write new data.

**Matt Yonkovit:**    
Surely don't drop

**Charly Batista:**
Your that's not my fault. Don't do. How is it? The fault? Just did wrong sequence of actions.

**Matt Yonkovit:**    
I'm going to bring you this message.

**Charly Batista:**
Okay, we need to do any we need to do anything in Max 15 minutes, right? Because I think we're running for one hour already. So we need to start legals. Yes.

**Matt Yonkovit:**    
Every time I do an hour stream with you, Charly, it goes an hour and a half. I don't understand this. Could someone explain that to me, you know, and again, if you if you were looking, it's all Charly's fault. So you know,

**Charly Batista:**
And I don't want to carry on the point in time recording for the next one I want to finish.

**Matt Yonkovit:**    
We must finish it. Because we're already, we're already booked until next year with Postgres sessions. If for those of you who aren't following this channel regularly, we are doing this every two weeks in recovering a different topic, unless we spill over a topic. So we have things like Ha to get to replication, we're talking about how to use Cloud instances Kubernetes we're doing query optimization, we're gonna do an Oracle migration. You know, stream where we talk about how to migrate from Oracle. We're going to do some database design sessions. So there's actually a schedule that is out through the end of the year already. And every time Charly does this, Gosh, darn it, it means an extra day. So we're probably into 2025. Now. Hopefully, hopefully, we'll end this series at my retirement party. Oh, yes. Those Chris 32 is out. Charly Are we finally done with our live streams at post? Chris 13?

**Charly Batista:**
That wouldn't be too long for my retirement either, you know, oh my,

**Matt Yonkovit:**    
Oh my oh, my gosh, likes the way that you're doing this though. He's saying that he appreciates the charm. Okay. He appreciates the Charly's. And that's cool. That's cool. I give Charly a lot of, oh, I can pull him if I want to. That's my job. That's my job. You know, I even like I said, I gotta sign I got the sign. It's Charly fault. In fact, I think I'm gonna put the sign. I think I'm gonna use this next time. And I'm gonna put it's Charly's fault on here and flashing letters.

**Charly Batista:**
It's always John's fault, you know,

**Matt Yonkovit:**    
Always happens, Charly. No, match. Yes, we totally know that we want. You've learned more as you see people who have to troubleshoot things. Like, for instance, the last livestream we did, we ran into the problem where we were running a backup and vacuum was blocking it. And I had never run into that before. And so seeing Charly kind of troubleshoot, and it took us a while. 20 minutes to figure it out. And it was like, it was something that was interesting. And you know, it is a little bit more because, you know, when you look at scripted demos, you sometimes don't run into these little tiny things. So I give a Charly a lot of crap. But it's all from love. It's all from love. We do it because we love it. And I'm always right, Charly. Oh, no, I Yeah, it's uh, ya know, I'm gonna totally bully Charly. Bully.

**Charly Batista:**
But. But the thing is, they strung up people, they just revert to situation, right. So yeah, I'm a smart guy here. That's why I'm being bullied. See? Oh, that's

**Matt Yonkovit:**    
Oh, you're you're bullied because you're the smart one.

**Charly Batista:**
Of course. You told me that was a faster Giesecke it took it took longer than the other one to to just,

**Matt Yonkovit:**    
Hey, hey, are you sure that you actually use the faster disk and didn't accidentally set it? Thank you, Anthony. The real time aspects of the sessions. He loves having the sessions real time. That's awesome.

**Charly Batista:**
This is using the faster disk. So I can't you're saving money or you

**Matt Yonkovit:**    
know, everybody's telling me I gotta stop bullying you. Somebody has to like, told you somebody

**Charly Batista:**
I told ya. Yes. Seriously? Do the surfer team. Oh, I know Linux. I know. Yeah.

**Matt Yonkovit:**    
I know Linux. No. So actually, people like this. Like I said, there's there's there's several other sessions. If you haven't caught up with us before. We've gone through the installation steps. We've gone through some tuning some configuration. So this is I think, our sixth stream that we've done. And, you know, like I said, I just posted a behind the scenes from the postgres Silicon Valley. So Charly bribes me with chocolate as we start to run into errors, which is, which is fun.

**Charly Batista:**
You know, great that right? No, it

**Matt Yonkovit:**    
Was error she created. But, you know, check those out. If you like, our witty banter back and forth, and you'd like seeing what Charly's doing. We do appreciate Charly and everything he does here, even though I give them a lot of crap for it. You know, Hey, Charly. Did we fix that before?

**Charly Batista:**
Yeah, we just recover the backup. Remember, every time that you do recover, it changed.

**Matt Yonkovit:**    
Well, yes. But one of the fun things about Charly. And again, if you watch the behind the scenes, you'll notice this when he goes to conferences, he brings copious amounts of candy with him like lots and lots of candy. And he has it in his pocket. And at the most unusual times, he just pulls it out and hands it to you. Like he'll be talking in the middle of a conversation about something and he'll just hand you a piece of chocolate, you know, and it's like, where did that come from? Oh, look, we have data

**Charly Batista:**
Back all the grapes.

**Matt Yonkovit:**    
Well, hey, Mahesh. Thank you for sticking around till almost 2am Your time. We appreciate you hanging out. Yeah, drop us a drop us a mail. message or an email, mash, and we'll get you a Charly and Matt t shirt. So if you want to, you know, drop me at haas@percona.com H oss@percona.com. With your address, we'll get you some some cool swag for hanging out with us till 2am.

**Charly Batista:**
So now we have same mistake. So now we have if everything went well 200,000 rolls, right, so our backup had 100,000 rows, and now we have 200,000 rows. And I was talking about what was talking about? Oh, yeah, I was talking about the old, not the drop table, I was talking about the beginning transaction, and it just forgot to run that again. And we don't have that table anymore. Right? So goodness. And now we have the problem. So if we just recover the backup, we won't have the data. Right. So I mean, we're going to have 100,000 rolls, but we won't have the 200,000 rolls. So what we need to do, now we need to do a point in time recovery, this is the things we need to do. Right. So but for us to be able to do a point in time recovery, we need two things, we need to have the base backup from the last time, right. And we need to have the wall files since that base backup, right, those are the two things that we need to have. We need to tell the database up to when we want to copy the data. So we need to tell the database when we want to stop copying that data. Right. So let me just go here. I need to to go here I need to go to data and move the backup server 012 point in time recovery. I need to extract these again. So what I'm doing now is I'm using the old backup to recover the data for I gonna stop the database, so it's going to stop the database I need to we need to find a way so how we get when we want to get what was the last operation that we want to stop when we want to stop the database we need to have a way or define the transaction or find out when we want to stop because as the name say it's point in time recovery we're gonna ask the database to go forward up to a certain point in time, right? We don't want the database to run everything from the start how we do that pass. Do you any cool.

**Matt Yonkovit:**    
Well, I'm sorry I was reading so there's there's a couple different ways you can get the like the transaction ID to stop at or you you can also use a specific time

**Charly Batista:**
Yeah, but what do we have this specific time? How we get that specific time or how we get that transaction ID.

**Matt Yonkovit:**    
You should can can you look through the log files or the wall files?

**Charly Batista:**
Yeah, we can do whatever we want. We are on the database lead Postgres main DGX wall we which one you want to look at? This last one here? We only have one actually have two here.

**Matt Yonkovit:**    
He Yeah, yeah, it would be the last one.

**Charly Batista:**
I don't know when How do I look at this log right being less what do I do?

**Matt Yonkovit:**    
Yeah, that won't work.

**Charly Batista:**
All yours a lot of you can't you can't I don't I cannot read those this language here but why not? Why can't Why can't you read that? I still need to study this language it's not I know a bit of English and I'll be the Portuguese some Chinese because I live in this world but that one it's new for me so how we get that data so tell us job information

**Matt Yonkovit:**    
I don't know I'm asking you and I'm saying tell us Charly I'm asking Charly.

**Charly Batista:**
That's why we have to help here we ask them for the help but you asked them the codes and display spots because right ahead logs for the bugging. That's good. So we've run did you all done with the options where are the options? Start and End? So they are the options right? So can you tell us about them? Which will Firewatch or okay we can tell the path the directory in which they have Verba which or okay that's one did you all them? Bash barley or screen 13 main nope Did you oh that should be right that's the path Yeah, that's supposed to be the path okay, we believe is this one last ask again? Oh ours help okay are on the timeline one so let's read the error message right above the two I have one thing we don't have digital data

**Matt Yonkovit:**    
okay, you have to set PGD Do you think by the way, Charly, if this is sending down the wrong path feel free to adjust

**Charly Batista:**
Yep, that's fine. Okay. I want you to follow, what is the start location? So we need to give it a start on location right. See how we can give the stock location for the wildfire

**Matt Yonkovit:**    
That I am not sure if…

**Charly Batista:**
That's a good question right can give the wall file we have this is the timeline.

**Charly Batista:**
That's interesting, I'm looking it up.

**Matt Yonkovit:**    
So Charly, is there a better way than using PG wall dump?

**Charly Batista:**
He could have the problem, we run the comments too close to each other. We could have, we could have found the record the time in if we have the logs enabled. So we could have the time that they dropped database, but we don't have those enabled in the logs. Usually that the easiest way starts I don't want statistics.

Okay, let me do one thing here.

**Matt Yonkovit:**    
So it should just be PG wall dump dash p then the directory and then the start file. I don't even know if you need to do a dash as.

**Charly Batista:**
The dash p is just is only when we don't have the PG data. We have the PG data.

**Matt Yonkovit:**    
So it's then going to put the wall file name. So the whole name Yeah, just trying to

**Charly Batista:**
Yes.

**Matt Yonkovit:**    
I don't think you'd even need to do dash s according to I was just checking out the docs. It just looks like PG wall dump dash PG wall than the start wall. And that's it.

**Charly Batista:**
Okay, the bash b i need to remove the dash P. Try that because it's there. What's that? Okay, here we go. We only have a checkpoint here.

**Matt Yonkovit:**    
But what about the other log file? So there was another one right? Yeah, it is. So that might have been a shutdown one.

**Charly Batista:**
So oh, goodness, here we go. And now we have delete. So those are the insert is the comment for the last. And after these commit here, we mess it up. What's the database, right?

**Matt Yonkovit:**    
Okay, yeah, I see the deletes. You've seen all the deletes there, right? So there's your lsn number that you want to restore to?

**Charly Batista:**
Yeah, This is the previous one and this is the one that won't restart up to this point, right? Yep. Let me copy this information here to my notes. Because we you need this information here my notes. All right. So now is what we need to do. Okay, we already have the backup, I suppose.

Hey, no, I don't have the backups because we don't have an office space,

**Matt Yonkovit:**    
well, you still have more space, you can add more space because you only used 100 gigs out of the 300 that I gave ya

**Charly Batista:**
Never remember the oh, I also need to be rude. That's bad. I'll be extend dash l was gigabytes

Okay, after that, I need to do X f s XF. Best grow s? And of course, still, when going. Okay, now we have

Okay, let's why, why we wait, we have the data that we need here. And copied. So after that being copied, we need to do have a way to tell the database that we were recovering, or we're doing a point in time recover, right, we need to tell a way to the database that we want it to go forward up to a certain point. Right. So we need to, what we need to do is we need to create a recovery file. I just create this file here, recover that console athletes, it's done we just copy the Recover file to the to the database. So in the recorder file, we need to tell what is the recovery target. So we as you said we can have the target in the time or the target in the LSM right. So recovery.

**Matt Yonkovit:**    
And we have the LS from the dump that we did.

**Charly Batista:**
Yes we do. And let me just double check if recovery target lsn recovery targets LS N

Okay, I'm opening the Postgres documentation here.

Yep, it's recovered target. It's my recovery. do you spell right recall? Very.

**Matt Yonkovit:**    
Yeah, that's right.

**Charly Batista:**
Equals work and get the lsn that we have here. We want to recover up to this point, this is the one that we copied. Right? So we also need to tell the database where to find the wall files, and what actually what the comment it will use to get the wall files that we have. Remember, we only have here, Q wildfires, right. But we don't have those wildfires from the backup

**Matt Yonkovit:**    
That we had, right? Because those were not part of the backup.

**Charly Batista:**
Exactly. But we have them on the archive. So and then the restore command, we can use a similar comment as we're using on the archive. And if we see here, etc, also agrees on the PostgreSQL command, the archive command, is this arcing here, right? So I'll just copy this comment. And what we want to do is to copy this do the opposite to copy the files from the archive to the place want to put them, right, it's just the opposite way. Okay, after the restore command, we want to tell to the database, okay, when you get to this point, what we the database is going to do. So the action that the database is going to do when it gets to the target is recovery action target. So I want the database to pause, I don't want the database to keep moving. And so when it gets to this point. And this lsn here is after the comment, actually is not the one that run in the comments. Just this is why they copied See, this is the one after the comment. I don't want to include the these Elesa I just want up to you the one people's so I want to tell the database that the recovery target recovery target in cluesive equals false I don't want to include that lsn in the recovery process, right.

**Matt Yonkovit:**    
So that's the LS in there though for the commit, or was that the one after the commit?

**Charly Batista:**
That was one after the comment. Okay, I copied the one after the college. Okay, okay. Just wanted to make sure.

**Matt Yonkovit:**    
Yeah, on the commit, it wouldn't come in.

**Charly Batista:**
That's true. That's true. I got the one out this is after the commit see?

**Matt Yonkovit:**    
Couldn't find the definition. Yeah, was this something like yeah, you might have hit something that you didn't expect.

Unknown Speaker  
Okay. Like maybe picked up something odd you need to finish the quilt right and find definition

**Charly Batista:**
That's weird. Wow, what's going on here?

**Matt Yonkovit:**    
I do not know what that is

**Charly Batista:**
Okay, my keyboard looks working fine insert and then when I go to okay

**Matt Yonkovit:**    
Is the arrow keys causing issues was that I see that that is a weird thing. But

**Charly Batista:**
Anyways, yeah, is the arrow keys I call them I like I'm just Yeah

**Matt Yonkovit:**    
Sometimes loses its mind, I guess what I just saw

**Charly Batista:**
Oh, we need to recovery targets closer inclusive equals false. 

**Matt Yonkovit:**    
So Mahesh was asking, can we just use the recovery signal file and make changes to the Postgres comp? On the DR side?

**Charly Batista:**
We can. This is the recovery signal file if I understood the question

**Matt Yonkovit:**    
You could put it in the you could hard code that into the postgres comp file though correct for startup if you're gonna start it up but then if it restarted then it would have the name and okay

**Charly Batista:**
That's so I have a problem near here targets. Action. 

**Matt Yonkovit:**    
Okay. Common actions misspelled.

**Charly Batista:**
Target impulsive, okay. Should be fine. Yes.

**Matt Yonkovit:**    
All right, you should be ready to go. Right. So,

**Charly Batista:**
Okay, yeah. So, okay, we're done here. Right. So this is the new data set for this is the backup that we don't have the data, right. So, what it's gonna do is this data here cantiere two, two bar leads. Force raises krauter teen men okay. So remember, we don't have that the data here right. So but if we do a database well restart here that was quite fast. I don't like when it goes that fas are they let's check belongs.

**Matt Yonkovit:**    
So, Charly, so you just restarted but did you tell it to use the recovery comp? 

**Charly Batista:**
I didn't know we didn't move the files. Good. Good. The fire is is elsewhere. So we're gonna do recovery, that cough to remain cool, very, very dark signal. Right. So we're going to signal the database that won't recover the the We want the database to recover from the last problem that we have. That is the junk database. Yeah, yeah. Now that's the thing. I don't remember top of my mind if it's recovered signal or recovery count, because smart house if not mistaken, his name. He mentioned about the cover signal, right? That's the thing. We're going to try and test now. So the database is stopped. I gone. We have those logs here. 

**Matt Yonkovit:**    
Let's see what it says. Yeah, recovery signal. Okay, the question is, will it still recover after you've restarted the database after a backup and then you shut it down?

**Charly Batista:**
Well, the database is not running.

**Matt Yonkovit:**    
That's the thing, but it was running. You started it. So was that gonna call? No Yeah,

**Charly Batista:**
I had a problem. See? It has a problem. Let's check the logs we do have a problem here. What is the problem now? Okay, database is ready accepting connections that this is not lottery. This doesn't seem to be the logs.

**Matt Yonkovit:**    
Now that's an old file, right? Yeah. Yeah, it must be out of order. Let's go back and take a look at the okay, what's the date in the server? The server dates wrong.

**Charly Batista:**
Okay. What's your SQL 13 The symbolic link is wrong

**Matt Yonkovit:**    
but you didn't recover to the slash data? 13 right.

**Charly Batista:**
We do. No, we recover to data, the ITR. Okay, now we have it correct. I got a CP recovery that signal to me. Okay, this is the new one. Okay, the database is stopped. Let's restart the database. And of course, we're missing this postmaster.

**Matt Yonkovit:**    
And this is where when you're setting up backup scripts or recovery scripts, this would always be automated. You'd want to always have this all scripted out ahead of time because you're gonna have to remember these commands now.

**Charly Batista:**
And we need to do the shell remember?

**Matt Yonkovit:**    
Yes.

**Charly Batista:**
There they checked here before we get this error, right let's just okay, that's a lot of problem well, actually, that's a problem that you don't know GCT ln Okay, now we have the logs finally. Oh, we should have a restore command and we have the restore columns. I probably misspelled nothing seriously nano restore common okay.

**Matt Yonkovit:**    
I mean, you don't need to use our Thank you mean you could use copy, you should probably check to see where those files are. Wait, go back to that real quick. Yep, maybe I saw an error there. Maybe I didn't I don't know. So backup archive is that where they are so looking under backup archive

**Charly Batista:**
Yep yeah, yeah. We have to.

**Matt Yonkovit:**    
So yeah, so remember just you don't have to use our sink you could use copy because you don't necessarily need that I mean, but even so it should have picked that up

**Charly Batista:**
Yep, we can use copy but just why not?

**Matt Yonkovit:**    
Well, I mean, I'm not saying you have to but restore command might have to go above the might have to be the first in the file. And I'm just spitballing so it might pick up the recovery target Ellis and then move down. I tried reordering just real quick. Doesn't hurt. It's an easy one to fix. It is

**Charly Batista:**
So common. Okay. Are seeing bla bla bla percentage F percentage p Okay, that's correct. Let me copy this one here and then it's better than not nine recover targets lsn I didn't type anything extra did I

**Matt Yonkovit:**    
Wonder if that wasn't doesn't need to be in quotes does it anyways just just try and restart and let's see

**Charly Batista:**
And here we go to restore command okay

**Matt Yonkovit:**    
I don't know why it's not picking that up

**Charly Batista:**
Let's try a different approach. Okay. What do we have here we have postman signal, let's make sure that database gonna start, okay, that database started so if I stop here okay, at least we know that our recovery dot c you know is the one causing the database to crash right so let's go over that signal restart command

**Matt Yonkovit:**    
Yeah it's not picking that up is for whatever reason oh wait a minute hold on let's see Is it is it down, yeah I don't I don't know that looks like it should be right in a watch

**Charly Batista:**
It is see PostgreSQL? 13 main scripts go back off. Okay, I have someone editing. Today I really need to find out what's causing this.

**Matt Yonkovit:**    
Instead of instead of M maybe VI will work

**Charly Batista:**
And here I always start the requirements okay. Okay, so you are Is there a star restart Okay. Looks like it restarted.

**Matt Yonkovit:**    
Take a look to see if there Recovery actually went through.

**Charly Batista:**
Yeah, I should have copied the parameters, because it's just lost the file just a second here. But I don't want to type this again, if I have

**Matt Yonkovit:**    
no problem. And thank you, everyone for hanging out with us. We're almost at our two. So hopefully this work. Charly didn't plan to be here for this whole time. So

**Charly Batista:**
Nope, I didn't. And themes, it didn't work. Because the table is not there.

**Matt Yonkovit:**    
Check the log file real quick in the logs. So my question to you, Charly, and I don't know the answer to this. And maybe you do, because you removed the recovery signal and started, does that do something to change that it can no longer be recovered? Because the log the wall files moved ahead with the start?

**Charly Batista:**
That's a good question.

**Matt Yonkovit:**    
Right? Do you know what I mean? Like so, ya know, if you're, let's say you've got, you know, your recovery recovers to log file for and you're saying, oh, I want to go to log file three, but then you start, it would then go to like log file 678? You I don't think you can go back.

**Charly Batista:**
Right. Yeah, we let's let's check the logs what it says.

Yeah, it's truly trying to recover from this log file. That was

**Matt Yonkovit:**    
Failed, right? It said, Yeah. file or directory, look at that. No such file or directory. So I'm guessing that it's it's not copied into the right place. It found it. But it's not copied to the right place.

**Charly Batista:**
Well, this is fine. This one here is the

**Matt Yonkovit:**    
RC cares, some file attributes were not transferred, see previous errors.

**Charly Batista:**
The thing is, we don't want those guys to be restored. The data that we have, or before these timelines, the xlsm are on the for E not for F. Right, that's one thing. So the data that you want to restore, they are not on those files, the thing here see the missing attributes? Okay. The your theory might replace something. What we tried to do? We don't no longer have the restore that signal. Right.

**Matt Yonkovit:**    
And, you know, I'm wondering if if that caused some of the issues. So what I, what I would suggest is, baby, we just tried to do this and come back, it's we're going to do the PG backrest. Week, which should take care of most of this, we should be able to come back with at least a answer on the next stream on like, Okay, this is what we did wrong. This is how you'd fix it. This is how you do a restore. And we could probably just do a little video clip that we can drop on YouTube without being live.

**Charly Batista:**
Yeah, okay, let's let's do this. My suggestion if you have time, so we can finish streaming now. And then I dig into the problem to see what happened. So we can recall that one, and then you do your magic on the video to make it as a short one. What do you think?

**Matt Yonkovit:**    
Totally fine. Totally fine. Because we know that some folks are really it's getting really, really late for them. Yeah, that's yeah, typically we this has been the longest stream we've had, which is good. I mean, people have gave us some good feedback. We thank you all for hanging out here. That's awesome that we still got quite a few of the same people hanging out the entire time, which is great. And I promise next time I'll be nicer to Charly. He's people. It's a

**Charly Batista:**
While yeah, if we straight if you save this one to YouTube, we need to split this video into because now it's been two hours. It's Yeah, well,

**Matt Yonkovit:**    
Well, it's automatically uploaded to YouTube. So we'll have to just edit it after the fact. So not a huge, huge deal. But

**Charly Batista:**
Okay. Okay, then let's let's do that. Let's finish this today streaming the live stream here. So let's keep recording figured out what was the problem? And then you do your magic to have like five minutes max, we do troubleshooting and get things right.

**Matt Yonkovit:**    
Yeah. And so, Anthony, you are absolutely right. And this is part of the thing is, you want it well scripted. But there's also tools that take care of a lot of this for you. And so we're trying to do it manually on purpose, and I gave Charly a lot of crap about that. But I mean, the idea here is, if we show you the steps, and we go through the pain, if someone tried to do it this way, they're going to see what we ran into and see what we troubleshoot it and hopefully save them some time. But the recommendation is, if there are tools out there, you will never do it manually. And yeah, you want to avoid the manual, unless it's like last resort. Because this is, yeah, there's what like, like 1000 pages in the documentation. It's impossible for everybody to know every setting in things.

**Charly Batista:**
Oh, this is yeah, and this is the thing, right? Everything that's manual is error prone. So we usually do silly mistakes. And then when come back for our seriously, I did that silly mistake. So yeah. And this is what how, why we should use the tools that we have in the market tool to do most of the automation of this process. It is good to understand how it works. Because, okay, we have an understanding, like right now, we have gained hints that where we need to look at, right. So it's something that happens with your automation, you need to be able to understand and to troubleshoot the problem. But you should not be done that manually. It doesn't scale. Even if you do everything right. It doesn't escape at the end of the day. Yeah, right. So no, yeah, yeah, it's good from time to time to go back and like, Okay, we we don't, we haven't done it for ages. And as people are pointing out things, change it from the 12 to 13 to 14. And it's always good to do and to remember those things and refresh them. But it should not be done manually. And that's why we're gonna max on the next stream, to have the PG backrest and do all the automation, all those kinds of stuff. And we got to have the server and everything done. So we'll see how much time we can avoid like save with those though the automation, right? That's the main thing.

**Matt Yonkovit:**    
Absolutely. Okay. Hey, we really do appreciate you all coming today. You are why we're doing this. So we appreciate it.

**Charly Batista:**
Yeah, that's my fault. It was supposed to.

**Matt Yonkovit:**    
I was told I don't to you. And now he's telling me it's my fault. He doesn't have one of these? I do.

**Charly Batista:**
So all right. All right. I gotta take something here on my,

**Matt Yonkovit:**    
Okay. Well, no, no, you guys, seriously, you know, this is these are live streams for you who are trying to learn Postgres, trying to understand how it works. And so we are very flexible. Bring your questions, hang out with us. Feel free to ask questions, you know, ping us offline. You know, I heard you know, some folks, you know, had mentioned, you know, that they were already in touch with Charly, which is awesome. And I had some people reach out to me and help them troubleshoot some MySQL things that we could go. So that's awesome. So, thank you for hanging out like this. Subscribe to it. Tell your friends, tell your colleagues, tell your wife tell your husbands, you know, and we'll see you in a couple of weeks and we'll go fix this issue.

**Charly Batista:**
Yep. All right. Thanks, everybody.



 