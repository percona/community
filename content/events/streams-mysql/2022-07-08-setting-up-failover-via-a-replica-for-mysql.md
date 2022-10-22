---
title: "Setting Up Failover via a Replica for MySQL - Percona Community MySQL Live Stream & Chat - July 8th"
description: "Get some tips and tricks to easily set up a Failover via a Replica for MySQL with Percona Community MySQL Live Stream"
images:
  - events/streams-mysql/Stream-MySQL-5-Marcos-with-Dave.jpg
draft: false
date: "2022-07-08"
speakers:
  - marcos_albe
  - dave_stokes
tags: ['MySQL', 'Stream']
---
![Percona Community MySQL Live Stream July 8th](events/streams-mysql/Stream-MySQL-5-Marcos-with-Dave.jpg)

This Community Live Stream is talking about Failover and Replica for MySQL. Our experts Dave Stokes and Marcos Albe took us through the setting to make it easier.


## Video

{{% youtube youtube_id="c5tj-0THNLI" %}}{{% /youtube %}}

## Transcript

**Dave Stokes:**  
Oh, one. And there we are.

**Marcos Albe:**  
Hey there. Hello, Mr. Stokes.

**Dave Stokes:**  
Hello, Mr. Albe. Good evening, good morning, good afternoon, good, whatever, wherever you are. This is, a live stream on setting up failover via a replica for MySQL, I see we're live on Twitch, not sure what's going with YouTube, but we're gonna go as we are, and we'll post the recording later. Send your Elevate is a support engineer for Percona. I'm a Technology Evangelist. We both been around MySQL for many, many, many years. And today, we're gonna teach you, or he's gonna teach you, I'm just gonna ask questions, and all about failing over for a replica with MySQL. So, what MySQL versions should I be using to do this?

**Marcos Albe:**  
Well, we're gonna be using eight, zero. And I think, you know, after some two years of GA, plus, it has become quite a solid version. And it has some quite advanced features for replication. We're not going to be looking into group replication, which is the My Favorite bit of it, but we're going to be looking at traditional binlog basis replication. So it's going to be 804. today. I hope that is what you were planning to use. So shall I start my screen sharing? Sir?

**Dave Stokes:**  
Yes, please.

**Marcos Albe:** 
All right, let me do that. Do you see my terminal? Oops, I guess so. Something, if you're telling me yes, I cannot hear you. But I hope we can see me.

**Dave Stokes:**  
Yeah, we can see it.

**Marcos Albe:**  
Alright, thank you for confirming. So I have here, a server that we have been putting together over the last couple of sessions. And I already have the replication beats that you should configure. Let me show you what those are. Basically, I have a labeled binary log, I provided the server with server ID and with those two things, you should already be all set for replication, I did add a few more details. Like I choose a big format. To improve the reliability of replication. I choose to have minimal binlog row image, meaning I'm gonna say the minimum amount of data possible on those binary logs. I choose to have full durability of the binary logs. This has performance implications and durability implications, basically telling us how often should we sync the bin logs to disk. This is every one transaction GTI demoed. If I want to use the global transaction IDs or not, I'm going to be using those and I'm going to enforce consistency of those my binary logs are going to be rotated every 14 days. So for that, and if these will act as a replica, then replication information will be stored in tables. I have here the intention to set up crash safe replication and I'm going to set a slightly larger below cache size. And with those you should be very much ready to run at a decent replication setup. So again, I already have my replica running. Sorry, my source running and I already producer.

**Dave Stokes:** 
I think they might have been purged.

**Marcos Albe:**  
So I will go ahead and set up the replica which is going to be the whole setup again. I haven't done this yet so you can actually see me doing it. So in case you miss it our first episode, you're gonna have the chance to see how I set up the now. So first of all, I am going to set up the app. First of all, set up the repository for Percona packer this actually, this is also going to install the Percona release tool, which allows us to manage the many Percona repositories that we have. We have repositories for Postgres, Mongo, MySQL, for our tools for extra backup. So this is going to help us manage those repositories. And for example, I'm going to say so you can see all those are available repositories that you will be able to manage. I'm going to do Percona really sit up vs Percona server, it's EDA. Great. So you can see it automatically disabled, the MySQL repose so there are no conflicts. Pretty smart guy. And basically I'm going to install conservers shell think that's it server debugging for client sharp Okay, when this guy's done, that's a big package what alright, this should be done very soon, I hope. Basically, what I'm doing here is I'm going to create a public key and I'm gonna make it available on the other node as an authorized key. So that is going to allow me to use secure copy. So in case you use secure copy in your servers, and you don't know how it magically works is the keys that are in your dot SSH folder. It's good to know.

**Dave Stokes:** 
Okay, this is faster.

**Marcos Albe:**  
So again, I'm going to copy this vertically just to make sure we have the right and authorized keys there we go. I should be able to do this. I did something slightly wrong. On a regular setup, I will be worried and I will be removing the key from my work. Not today. Let's make sure this thing comes up system steel or SQL trying to access missing tables face. Looks good yeah that was one strange message make sure typos unexpected.

**Dave Stokes:**  
Sounds like that normal account when you type in system control start.

**Marcos Albe:**  
Say that again.

**Dave Stokes:**  
There's always that moment of hesitation retyping.

**Marcos Albe:**  
I can troubleshoot it. I hope I can troubleshoot it

**Marcos Albe:**  
You know anyway it's complaining about some table space I have to bring in the backup from this guy. I'm gonna take a fresh backup on this one. I'm gonna copy to the replica. 

**Marcos Albe:**  
I see. So your friend Mr. Matt Yonkovit, he gave me a smaller machine.

**Marcos Albe:** 
That's not funny, Matt is not funny. So there you go that was it hope

**Marcos Albe:**  
Okay, because that data became corrupt. So if you are ever at loss of where your MySQL D is sending the log you can always do this check the PID of MySQL D and then proc slash that PID slash ft slash two and yeah this login they're just not doing it are gone, and the simple D there's the image. 

**Dave Stokes:**  
Wel, she tends to make inappropriate comments if they're watching this is Sue she's a seven-year-old black mouth occur and is very opinionated and will talk

**Marcos Albe:**  
And he said, opinionated MySQL user. Okay, I have an empty data directory I do initialize and secure it's using my configuration, so that should be fine. I mean, getting these kinds of error during initialization is okay. 

**Dave Stokes:**  
Thanks goodness it's Friday.

**Marcos Albe:**  
All right, I don't know what was a lingering instance in there that's it. So anyway, I'm going to have to stop this instance and I'm going to bring over nice backup from here which is gonna take backup target skirt like it, try to explain a stream it's gonna take you one more second, but should be worth.

**Dave Stokes:**  
So for our home audience, this is making a backup on the source.

**Marcos Albe:**  
Release. I'm going to first set up Percona XtraBackup here. So XtraBackup I give it configuration so it has details like socket and not the directory and the location of whatever where so take the backup I say take a backup use four threads compress it and stream it as an XPS stream. It and see listed on the NINE and a NINE and then sent to express stream exness See think aesthetics. I'm pretty sure. So this guy is going to be listening on this port. And it's gonna push whatever it takes on this port to XV stream who is going to extract into this directory. So if this guy's gonna stream and pipe it to this Netcat who's going to push it to that port? I'm not sure it's open. So, that board is not open. I can try three, three or six. So this happens a lot on customer setups, like they have firewalls. If and then we have to use 3306 port which tends to be opened by the SIS admins. 

**Dave Stokes:**  
Who are new to MySQL that is the fourth default port number for last six. So since MySQL is running on that machine, we're just gonna borrow it for a little while.

**Marcos Albe:**  
And now you can see it's copying files from the other guy. The biggest the file the longer the longer it takes to stream of course. So you might not always see things being pushed you can sort of leave and always do it is to have some idea of where it's gone should be done any minute now. So you can see it's growing.

**Dave Stokes:** 
Okay, it's done.

**Marcos Albe:**  
Yep. Up so now I can do XtraBackup there says decompress there's the target.

So Kubernetes is the compression algorithm and program we use to decompress the QP files that are produced by XtraBackup dash compress the package is available on the EPL repository so you have to use yum install April release.
 
Okay, you know what I'm gonna do I'm just because it's gonna take me less time to just gonna stream it again without compressing. So normally, this should come from our records.  It was in our tools report. Look, once I enabled the Okay, I always forget this report. So it's there in case in case you have to set it up yourself, don't give up like I did. And you can just Percona release the tools. That's going to enable the report, and then you can successfully find good press. So don't be like me. Okay, this is done anyway, that was fast. Now I can do XtraBackup. So once you take an extra backup, the backup is a data directory in a crashing state. And it has all the necessary pieces to bring that crashing instance into a usable instance. And that's the Prepare step, what the prepared status target here equals source. Yep. So copy back is going to look into your configuration file into my CNF. And it's going to find where your file system, the different pieces of the backup should go. So normally, you have everything under valid MySQL. But you could have your redo logs in a separate location. And you could have your system tablespace in a separate location, your undo logs in a separate location and so on. And copy back will find the location of each of those and move the files into the appropriate locations for your backup for the кestore to work correctly. So like it at least complain of something back up, Jesus will be back not copy backup.

**Dave Stokes:** 
Yeah, I'm sorry.

**Marcos Albe:**  
Typing and speaking at the same time, it's not something I do very well. So you can see it's copying the different pieces into the appropriate directories is going to take a minute one thing I have not mentioned about XtraBackup, and MySQL or Percona Server eight zero is make sure your version of XtraBackup matches the MySQL version. So if you're using MySQL eight, zero 27. Make sure you're using XtraBackup Eight zero 27. And because there have been changes in the binary format of the redo log, it is important to have a matching extra backup binary. Because, again, it the redo log format which is a very important part for extra backup has been changing over eight zero versions. And that breaks compatibility of the tool. So again, if you're using XtraBackupwith eight zero, make double sure you're using matching version for your server.

**Dave Stokes:**  
Can I use a later version of extra backups?

**Marcos Albe:**  
You should be able to yes that so bigger tool version with a smaller server version should work. If you come to me with a failed backup that setup I will tell you, please try with a matching version first.

**Dave Stokes:**  
By the way, folks, Percona XtraBackup is free, and it is open source and lets you do hot backups.

**Marcos Albe:**  
One of my favorite tools in the world, I give you my word. Okay, this guy has copied everything in place but these files are owned by root that is not good. So shown recursive MySQL. Oh, look, let's see var log.

And you can see the guys complaining about me starting the MySQL D. with C, it's an unset. system called, there is some system code I'm not allowed to run with SC Linux. So I'm just going to sit in force zero. And we will get a horse and then restart your server and it works. So we do have sc Linux compatibility guidelines. You can find them on our documentation. We might go back in one of the podcasts to security I assume. So I'm gonna save it for that podcast. Because it's a lengthy presentation. So I always tell customers if someone is reading this file, and it can see your password with these permissions. The problem is not on the MySQL security or I'm having this password here but something that allowed someone to gain access as root and reach your home directory as root so you know by that time whether he has the MySQL password or not doesn't make any difference he's going to have whatever he wants so doesn't make the case.

**Dave Stokes:**  
We will take a guess at that point.

**Marcos Albe:**  
So he's guy is at the same position that they are again you can see this the GA d sequence is the same as in the primary so I should be able to do a very simple set up

**Dave Stokes:**  
For those curious folks out there, yes, this is all documented. Yeah. So if you're having trouble following you, you set up the client for replication or the account for replication give us the privilege so if you'd like me and a hard copy or something under the screen while you do this, it's possible aid and comfort obligation client.

**Marcos Albe:**  
Sounds ugly, because we're going to be using DDD, we don't need to take care of, you know, log file and position, which was the old way to set up replication, you will give that coordinate per as master log file and master log posts. But when you're using GTD, what you will do is will set the DVD version. So in the backup I brought I have the binary log information. So I will take this. Let me show you it's going to fail. And I'm going to be it's going to fail. Because normally oh because I still have nothing in the GDD executed. Usually you have to do reset master because you cannot set global GT ID purge. If you have any DDD executed to reset the GT ad executed you have to reset master dangerous danger removes me looks. So if you're going to do reset master, make sure you don't need to be in locks on that machine. 

There you go. So I was missing a privileged, I'm sorry, I always forget to only granted replication client. So if I do show databases, now I have only the movie database and all the system stuff. I'm gonna create. So we have working replication setup, and we just quickly verify it by creating a table on the primary, and then verifying that it shows up on the replica. Now I'm gonna create a silly very silly true. So I have to replicate, let's say client that is sending continuous traffic, which you know, is what you normally will expect on a production server. Now, if we wanted to failover to the replica, now, the replica is a synchronous replica. So you must think that there is always some inconsistencies you don't have to rely on? Oh, it shows? You know, it shows? I don't know.
 
So, you know, it shows sedo Is that does that means it's fully up-to-date, and that I can simply move my traffic to this node and be done with it? Well, not truly. The bear replicates always delayed, and it's by its own nature, it must be delayed because things got committed on the souls first, then we're pushing it to the binlog. And the Beenleigh was copied to the replica and then apply it on the replica. And, you know, laws of physics tell us that, that has must take some time. And that's the replica is always delayed, at least some little bit, you know, it looks quite up to date. And this, you know, it looks up-to-date and you know, there is barely any delay, but I will assume that it's always delayed. With that in mind, when you're doing an a synchronous failover there is no such thing as a zero downtime. Failover that it's simply not safe. It must be some synchrony is synchronicity or call this time right? A point where you stop the rights on the source. Verify that the replica has every single right that was ever done on the source and then move the traffic to the replica not before. In either cluster, you could actually have multi master setup, right. And with the multi-master setup, then there's a guarantee of free of conflicts. So you can actually push the rights to the other guy, start writing. You might get some conflicts, you might say, hey, this key is a duplicate this key, you know, what's already committed elsewhere, rollback, but you can immediately move the traffic there, and be sure that you're free of conflict, which is what you care the most. Because if you introduce a conflict here, you are generating a split brain. And that is the most, you know, painful situation you can go into, I believe me, it's better to lose a few 100 commits, than introduce a few 100 commits into a split brain, because then you don't know what data is what data and it could have corrupted, silently corrupted or make silently into introducing inconsistencies in the data. So split brains are, in my opinion, the worst situation, I think, if it was my setup, I would prefer to lose some data, rather than introducing an inconsistency like that. So the thing is, when you have a built fully synchronous setup, like Procore, next really big cluster or MySQL InnoDB cluster. You can immediately failover in a blind way, relying on the mechanism that will prevent inconsistencies. So you are free of conflicts, you know, you're free of conflicts. So you're good, you might get the clients, the application might get some, hey, there is an error here. This transaction is invalid, retry it because there was a conflict. And it was prevented from introducing a split brain. So in those cases, you can do it. But when it's synchronous replication, then you can't because again, by its own nature, it's always delayed always. 

**Dave Stokes:**
Of course, you want to set it to one, Marcos.

**Marcos Albe:**  
So basically, I made the instance Read Only these guys should be complaining. So at this point, you're you're suffering a blackout. You know, like, the application is not able to do anything. And depending on how your application reaches the MySQL instance, you'll have to do a bit different things. In my case, I am connecting, I'm doing the absolute cheapest option which is connect directly to your MySQL. We're also going to see it's the least convenient of the options. So this guy is now read-only, and I can do show status and check My position, I can go to the replica and we will show master status. And check that the position is exactly the same at this point, I know it's safe to move the rights, there will be no inconsistencies. If I push it the traffic here. So at this point, I will do set global read, only consider and super read only consider on the replica. And that will allow traffic to come in. So what do we do with this guy. So let me explain what's happening. I have a root user, and I'm using the right password. And if I access through here, I'm using the same password. It's only localhost. So my user, my root user is only localhost. And you can see it's telling me I don't want root from this IP to login. So MySQL will restrict logins based on the source host. So what we need to do is to either create a separate user, or alter this user, I'm going to create a new user and the password for that. So use the same password.

That guy is able to send traffic again. And that's basically the most important part is block your traffic and make the instance read only at that point, the other instance is catching up with the latest bits from replication, right? So you need to take a look, where did you stop it taking traffic, you do that with shoma status, you verify your GT ID sequence and then on replica, you again run show master status. And you're going to verify that the replica has applied every single transaction at that point is safe to make the replica read write. So you allow it to take writes and at that point, you move your traffic to this source to this writer node and It should be safe and consistent. So those are like the really important bits, then normally, you will not have your application connected to MySQL directly, you will have your application connected to proxysql or H A proxy or MySQL router, or some other device could be a big F, big IP f5 or some other load balancer that your company uses. And then you will not want to do this kind of, of restart of the application, the application will always connect to the same IP address. And that device will detect which node is read write. Which note is read-only. And it's going to push right traffic to the read write. So we're going to be seeing that we're going to be building up on that on the following podcasts. So continue to join us and we will be looking at proxysql. And probably we're going to be looking at orchestrator. I'm not sure if senior young COVID Has that in his plans. But I will be joyful to show you that. And there's not much more to show like it's a really simple thing. The complicated thing is to get into the mindset of block the traffic, make sure things are consistent, and only then unleashing the the traffic to the new source. Or perhaps if you're using a proxy, then your proxy is going to be doing it for you. But always block first, both sides must remain blocked at some point. And that is the important part. Both sides must remain blocked at some point to guarantee consistency of the data sets before you move. Write traffic to the replica. At this point, what is left to do is to make sure this guy's not going to come up as writers. 

**Dave Stokes:**  
You don't want your old primary coming up and saying hey, I'm primary still and exactly.

**Marcos Albe:**  
And he's one more step you can do. And depending, you know, different people, that's different things with this, which is this guy is still a replica. Right? It's not able to connect whatever, but this guy's still a replica. And if this guy comes back, and it had straight rights, I don't want those rights to have reached this note. So this is preventing this guy from taking rights from a source that we are, that was not intended to be a source, because this guy's a sorcerer. So some people have Master Master active passive setups, so that people, usually we'll leave the replica set up in place, and just flip the rolls. That's also perfectly valid. You just got to be more careful. That's it. It's like this matter of being careful and making sure the rights only ever go to a node that is fully consistent. Once a node is fully consistent. Push the rights onto that one and make sure the other guy doesn't get rights. So only one guy A lot, only one note at a time can ever get rights. And before it gets rights, it must be fully consistent that those are basically the rules. And that's it. I now have nothing else to show. People on our stream have questions or you have any questions for me.

**Dave Stokes:**  
No, I don't see any questions on YouTube. We did have some problems with the YouTube feed originally, but now we got it going. And see, so we are now doing well. So folks, if you have any questions, comments, or any topics you want us to cover, please let me know. I'm at Stoker on Twitter, david.stokes@percona.com. And we'd love to have any feedback you have. 

**Marcos Albe:**  
It was an interesting setup to date, like, yes. Having lost my troubleshooting skills.

**Dave Stokes:**  
Yeah, well, you show them off to great applause today for me. I mean that I for folks who have never done a live demo before this, why don't do live demos, at conferences, whatever will happen does happen. Everything will rattle when a fire alarm you have to clear the building and come back. But thank you for tuning in and a big round of applause again to Marcos and we'll see you for the next edition.

**Marcos Albe:**  
Have a good day for everybody. Thanks for having me. Bye bye.






