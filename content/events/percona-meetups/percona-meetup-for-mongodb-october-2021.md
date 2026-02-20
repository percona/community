---
title: Percona MeetUp for MongoDB Oct 20th, 2021
description: Community MeetUp for MongoDB highlighted solutions for your common problems
  with MongoDB including backups, scalability, security and also some MongoDB5.0 features
images:
- events/percona-meetup/MongoDB-cover-october-1920.jpg
date: '2021-10-20'
draft: false
speakers:
- kimberly_wilkins
- andrew_pogrebnoi
- matt_yonkovit
tags: ["Meetup", "MongoDB"]
events_year: ["2021"]
events_tag: ["Community", "MongoDB"]
events_category: ["Speaking"]
---
This video from Percona MeetUp for MongoDB of October 20th talk about backups, scalability, security, MongoDB 5.0, and more. Full recording with Andrew Pogrebnoi, Principal Software Engineer at Percona, and Kimberly Wilkins, MongoDB Technical Lead at Percona, hosted by Matt Yonkovit, The Head of Open Source Strategy at Percona. 

## Video

{{% youtube youtube_id="YnQu2Ock2d8" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit**  
Hello everyone. Welcome to another Percona meetup this week is our MongoDB meetup week. So, glad to have everyone with us. Here joined with Andrew and Kim. So hello, hello. Hello. So, welcome everyone who is virtual Welcome to those who are watching us recorded.  Thank you for coming and following along. Oh, and there's Kim. Welcome, Kim.  here we are, another fun and exciting week. So before we began the MongoDB fun, I was just at a conference, this is actually the second conference in the last two, three weeks, three weeks that I've been to Kim, you were at an open source summit with me. And so we're starting to get back to in-person conferences, which is always fun.  so I don't know about you, but I like to get in person and talk with people. It's always fun and exciting. And it's definitely one of those things that tried to figure out which is the best angle for the three of us. I think this one is. But yeah, yes, much, much better.

**Kimberly Wilkins**  
Yeah, Matt, I mean that you're right, it was nice to get back out there, it was a little kind of interesting because it's the first one out in like two-plus years. So it was good to get out there and to see people and I think this will kind of get things started up back again, right? Because it's definitely different. Especially if you're like talking and presenting to people and on a topic, because you can see the reactions, you can gauge what they're most interested in and kind of go down that path.

**Matt Yonkovit**  
right? Yeah, it's hard when you're virtual, especially when you're not seeing the participants, right. So we might have 100 people watching this, and we might say something. And you won't see that reaction. Or they might say, tell me more. But we don't see it.

**Andrew Pogrebnoi**  
The funding, the funding seems good if you like you have like a three participants, but when you alone, and you just send in your monitor, and then your camera, and you're just talking it's like it feels felt a bit of 

**Kimberly Wilkins**  
because you're staring at yourself, and you're talking to yourself, so yeah like, I don't know about you, but sometimes I find myself going like, Oh, did I have my hair?

Right? Yeah, exactly. All right. Am I looking at the correct camera? Right? supposed to be the laptop camera?

Yes. Right. So you've got all these different ones.  it's a challenge, but I was at all things open this week. Oh, look, someone's eating borscht and listening to you couldn't do that at a conference. That is true, you couldn't eat borscht. And check us out at the conference. So lovely that you're able to do that. Welcome all across the world. And that's one of the nice things about virtual and hybrid events is you can reach out and talk with folks no matter where they are anywhere in the world, which is very cool. But I was at all things open this week. So if you've been to Africa, with all things open, it is a 100% open source conference very focused on the community here in LA, but also worldwide. And it's interesting. So based on the two conferences we've gone to, it looks like about 20 to 25% of what a normal conference would be, that's who's attending in person. So it's still not back to normal 100%. But it is fun and exciting and engaging to do that. But as I was there, I was able to talk to quite a few people. And, of course, everybody there loves open source. But this is a very developer-focused conference. And there were a ton of students, like a lot of people from colleges, and people going through learning how to be engineers learning how to design applications. So a lot of them are like, ooh, databases, yuck. But almost all of the students were like, oh, Mongo, we know Mongo, we use Mongo. And so it's interesting to see that there's this kind of reaction to something like a database but then Mongo there Oh, yeah. Mongo so you're talking about that kind of inflection or that that face right it's the whoo databases, ah, Mongo. And there is that reaction? Why do you think that is like, I have my thoughts on why Mongo is so popular in that kind of student developer crowd, but maybe, Andrew, what have you seen from the Mongo community that makes it so attractive to those developers?

**Andrew Pogrebnoi**  
I don't know man. As for me, it's surprising as well, because what, for me, is not the basis of what could be more exciting than not the basis of probably compilers or but on the other hand if I Like, what could be more exciting than distributed databases? Yes. So Mongo was to offer this. But again, I don't think that this is the case. I think it's probably the younger generation, the students, they are feeling that this is like, some, all technologies that like the posters made in, like, in New Orleans, in the late 80s, and early 90s. The same with MySQL, and mid-90s. And, like, so probably this is like, the technology that started before these people were born. And like, this new kind of fresh technology, may be feeling more appealing, and more, like refreshing and more like, closer to that generation on one hand. On the other hand, it's like, no big deal, the easier entrance to this technology, you don't have to know all this like SQL. And you don't have to understand this, this whole new world, and all this new language, and if you like deeper, like all this AC, what is transactions, what is this level of is isolation and stuff like that, you just, you just installing and using it, and we spread the offer?  this, like, API's everywhere, JSON. And again, it's like, very appealing, and things that people could understand and easily like, so yeah,

**Kimberly Wilkins**  
it's definitely easier for people to get started with. Andrew, I did not introduce you properly. Can you introduce yourself to those who are watching? Who might not be familiar with you? maybe tell us a little bit about yourself where you're from just so people get a sense of your background? Yeah.

**Andrew Pogrebnoi**  
Yeah, sure. Sure. Yeah. My name is Andrew. I'm a Principal Software Engineer here at Percona. The first project that I used to work on in Percona was databases in the cloud in Kubernetes. Yes, and since then, I switched to TBM Percona. backup for MongoDB. And I found that like, again, this project, more interesting and appealing to me. So since then, I've been working on the PBM, Percona backup for MongoDB. Yes, yes. So basically, this is like distribution. backup for Mongo. fully open source, as always. Yes. And quite neat. I'm originally born in Ukraine, but now I live in Cyprus. 

**Matt Yonkovit**  
Okay, great. Maybe introduce yourself? Well, well, while we're at these introductions,

**Kimberly Wilkins**  
yeah, it's **Kimberly Wilkins** on MongoDB. tech lead her. And so I've been working with MongoDB. Since I know, late 2013, early 2014. Before that, I did a lot of Oracle. So for me, it's kind of different things right? For me, the developers are one in a way, right? Because before in Oracle and the relational database, you have schemas, and the developers have to fit within these schemas. But then you get to MongoDB, and it's a quote, unquote, schemaless. But if you do that, of course, you're making mistakes from the beginning. But you do put structured, semi-structured, and unstructured data. And you can figure out what to do with it later. And so that's one of the things that made it significantly easier for developers to just, hey, let's throw this in Mongo, we can put whatever information we really want in there. And we can figure out how we're going to use it later. We can use it however you want. And so I think there are a lot more developers and our DBAs. And so that's kind of like one of the historical, quote, unquote, battles between that. But I think that Manuel did a really good job early on with the developer community, and getting them on board and live and some of that's kind of changed over the time, but they're working back towards that. So. And I think that that's super important. Like, for example, in our comment here, I found out that I'm going to be when I decided to become a developer, he started to learn front-end development, mobile app development. Those are some of the things like mobile apps, your product catalogs, all these different types of use cases, chat messages, etc, that are perfect for Mongo with the semi-structured unstructured data, right?

**Matt Yonkovit**  
Right. Yeah. And I think that's where it's become really popular, especially in colleges, universities, because there is an easier barrier to entry. It makes a lot of sense from a front-end perspective, to keep things very close to what the app itself is doing. So that base, the base on the format of the JSON format, makes it very easy. The transition from one to the next. Now, Andrew, you mentioned you're specifically working on PBM, he used to work on some of the Kubernetes side of things, which means you've been in all of the new, exciting worlds.

So you're at the cusp of the cloud-native movement there. And one of the things that are super interesting about Mongo, and this is one of the things that when you think about a classic database setup, you don't generally think about, its now that we get to this cloud-native environment where it becomes super relevant. And what that is, is, we've got copies and clusters of data that are spread across multiple nodes, all over the world, potentially, or all across different servers, which means that backups become kind of a tricky thing, as you think of a backup on your PC, on your Mac wherever, and it's like, oh, I'm gonna run the backup tool, and it's just gonna back it up, it's gonna take care of it, everything's good. But now, you might have 5-10 different servers all with a piece of the data. And when you run a backup, the backup could be at a different point in time on every single node,

**Andrew Pogrebnoi**  
Yes, yeah, you're right. And this is, this is like one of the reasons why I switched to this project because this is that it has some amount of like, challenges and complexity that that's related to that method that you mentioned total, right, that one thing that you have, like one standalone, like, database, and you have to do backup, it's like pretty straightforward, you just do backup, and that's it. With Mongo, when you have, even if you don't have like sharded cluster, if you have just a replica set, still, you have, let's say at least three nodes, and then you have to decide which of these nodes is gonna be taken backup from. And, again, this is not good, as you mentioned, distributed all across the globe, it could be like, in different regions or even on different continents. And, and if we add to this, like, the new layer of complexity is like the sharded cluster, that's when you have like, these replica sets, but the set of these replica sets, if you will, and they are, again, could be spread across the world, or part of this could be spread across the world doesn't matter. And then you have to decide not only which nodes are gonna take backup on each replica set, but you have to be sure that every node on every shard, not that every node but at least that one node on every shard, is gonna make the backup. So this backup is gonna be consistent. And then you start thinking, Okay, how can we be sure that this backup is gonna be consistent across all of these shards? So yeah, it's, it's, it's really challenging.

**Kimberly Wilkins**  
Yeah. And I think that's one of the things we often take for granted. Because when you run a backup command, it's generally just a backup command. It could be in some databases, easy backup, right? You just type backup, and then like the name database, and it just happens.

And that's super important, too. Because if you think of like, historically, the backups, right, from the logical point of view, you have logical many physical backups, right? And historically, you primarily, we primarily did logical backups, right? We did them from within the database. But as these database sets have grown, as the data sizes have grown over time, then that's much less practical, right? Because it takes a long time to take that back up, as the size grows. And then it also takes a long time, if you need to do the point time recovery. And that's why physical backups become more important. And like Andrew was just talking about a minute ago, it kind of leads us to the point-in-time recovery options that we're talking about, right. But your logical backups for Mongo specifically, because that's what we're talking about, that's going to be the ones from within the database, it's going to capture everything within the database, including like the config database and the information there, and everything from within the database. And, and historically, that's going to be your Mongo, dump your Mongo restore commands, right? But you can really, really, really take a long time to do those with terabytes and terabytes and terabytes of data. And not only that, the Restore is going to take but it's also going to have a negative impact on your performance, right. So as we scale we need to be able to address that. And that's where the physical type database is.

Oh, Kim just went mute. Yeah, we just lost all your sound

Oopsy Daisy, Hi, my partner. So that and that's where I think my hand is a terabyte two terabytes. As the data sizes have grown, it's become more and more important that we're able to do the physical sizes. Because if you're doing the logical backups, and we're this large terabytes and terabytes of data, it takes a while to back that up. But it also takes a while to restore that. And then during this time, you're doing multiple writes, or you could possibly impact performance. So going back to the replica sets that Andrew was talking about a minute ago, you can do it on other members of the replica set, not on your primary, you can do it on one of your secondaries. As long as you're not doing too many secondary readings, you can add a hidden node there to do the additional steps. And then to where Andrew was going a minute ago, then we're talking about the physical backup. So yeah,

but wait, I know that there's going to be somebody who watches this video. And I'm going to play the devil's advocate. I wish I actually need like a, like a like my soundboard setup, which I don't have with this. So I can play some like eerie devil's advocate music or maybe pop on my head or something. But playing the devil's advocate here, with all of the redundancy, why do I even need the backup isn't MongoDB supposed to be resilient

MongoDB is inherently resilient because of the election because the replica sets right itself. But especially if you're talking about multi-zone, multi data center, multi region backups, you never know what's gonna happen, the latency, right? And so you do need to be prepared, you do need to. And that's one good thing about logical backups is that you can do a backup and restore just to a collection level or just to a database level instead of the complete instance level. So if you wanted to test something just on one collection, for development purposes, then that's a great thing to do, right, as opposed to having to do a complete restore of everything. But you always think about backups, you always need backups. Because what happens if you lose an entire data center, or what happens if you lose two data centers, or what happens if you have your replica set or you have your chart, and you lose your primary and it doesn't election and if God forbid, you had an arbiter if you have a primary, secondary and an arbiter, and that's all you have a running that in production, okay, and then you lose your primary, and then you only have one secondary, and then it's catching up. And the arbiter is not in data bearing node. So everything's important about the architecture, but um, you are, you are taking precautions, and you really just have to have that in any kind of production.

**Andrew Pogrebnoi**  
And we not even haven't talked about the human factor because, okay, you can have as much resilient database as you can have in the soil, like images with like, bulletproof data center, but it doesn't protect you from the human factor. Oh, we are human, we make mistakes. And if somebody has access to your database, like either No, developer DBA. Anybody potentially, somebody could like, just keep like,

**Kimberly Wilkins**  
Do you mean somebody might delete some data?

**Andrew Pogrebnoi**  
Yeah, sure. Why more,

**Kimberly Wilkins**  
or with 5.0, dot 05, dot 0.1 5.0, to two, and backported to four, four dots, to four to three, all the way to 4849. There are bugs that were introduced by backporting, these things are data and potentially data impacting that could cause corruption and are missing documents. So okay, you decided to do an upgrade, because Hello, upgrade to the latest and greatest, that's what you need to do. And even if you still do only on four-port, whatever. But if you upgrade to that, and you've corrupted data, and you've already migrated it, the changes have already gone to your secondaries, then you're in trouble. And you have to do a validate command across all collections and all of your databases, and that's very impactful. So yeah, backups are a very good thing before any upgrade. Obviously, you want to take an extremely solid backup.

Well, and this is an interesting point getting back to Andrews’s point here second about the human factor, right.  If you know for those who aren't necessarily DBAs, or have that kind of sysadmin background, think about it as you replicate data and you have these copies of data sets on different servers. If you change some of your data on server A that change moves to server B and the server sees which means that like, so if you make a change to, I'll just use something very easy. Let's say you're tracking bank accounts and you say, let's zero out my bank account on server A, that gets zeroed out on server B and server C eventually. And if you didn't mean to zero that out, you don't have the redundancy to the other servers, because they all have zero now. And that's where backup matters. Now I'll give you an example. That is a real-world example that I've used before and talks about.  where this is not Mongo specific, but this happens in every database, right? Regardless of the redundancy and things you put in, there was a company that we worked with, way back in the day, they gave us a call, they were an internet unicorn. So if you're not familiar with an Internet unicorn it means that they're worth a billion dollars, right? So a billion dollars plus. So a very, very large company, a darling of the tech space, and this were years ago. And they actually did a that they had all this redundancy built-in, they had replicas and primaries, and they had failover, and clusters and everything else going. And with that setup, they moved data centers, so from the data center, A to B, migrated, because they wanted to switch providers. And on the second data center, they forgot to turn backups. So they had all the redundancy, everything was copied over. And if one of the nodes failed, everything was perfectly fine. But one of their developers released a new version of the code. And accidentally in that new version of the code, it was a migration process to Ruby on Rails. It recreated the tables. And so it dropped all of the objects and recreated all of the objects empty. Yeah. Yes. And there is no recovery from a failover perspective. Yeah. Right.  and, and I think that that is something that you have to be mindful of. And that particular company, we used to do a lot of data, forensic recovery, which is, even if you delete stuff, you can still get it back. From the Linux file system. It's just not a fun process. So we spent about four days doing forensic data recovery on Linux, to pull back some of their data. But they had a four-day outage on their website. And after that, they were out of business for six months.

Yeah. And yeah, with today's always-on online, immediate access, immediate results, we can't have that you cannot have that as a company, right? I mean, it's not the same time, it's not a green screen date. So although we do have a green screen here, it's not the same as the mainframes in the green screens where you can take that much time, right, and this goes back to the point of there is still a place for the logical backups, right? Then per database where you can restore the collection. So we had some talk here about backups can also be a form of compliance. Yes. Right, you must be able to recover, you must be able to have your backups in place so that you can recover. And you have to most, the majority of the time, you need a median time to be able to recover right.

**Andrew Pogrebnoi**  
Now, and the other thing, you probably want, in some cases have the ability, you don't like to travel in time, but for some time, I mean, to have because let's say your data changes your like, account changes or some other advantages, okay, maybe you have logs for all of that. But, like, in general, this ability to, let's say, to be able to travel in time, and to see what the state was, like, it's not that like, I think, widely inspect the US, but still for some type of businesses, for some companies. Again, it could be, I suppose, even like, some obligations that are applied.

**Kimberly Wilkins**  
Yeah, and I mean, that point in time, every. Andrew is very important and part of the thing that's in PBM is that point in time recovery, right? And so, how does that work?

**Andrew Pogrebnoi**  
Like in general, we just use like, let me make like a bit, step back and step back and explain, in general How does replication in MongoDB works. Basically, in the replica set like canonical replica set we can imagine it's one primary and two secondaries. And the primary is the right read node and from like secondaries, the followers you can only read the data. And basically, what's going on that again, this replica set elects primary. So let's say Imagine if you’re primary gone because of some network issues or whatever, it is just the other, as one of the secondary, is going to be reelected as the prime. And so, basically, whenever you write to the MongoDB replica set being like replicated to the, to the secondaries and this is done by the like oplog, like operation lock basically, it's like some kind of like broadcasting protocol when the followers that like secondaries just subscribe to, to the primaries, let's say events and basically primary sense all the events that happen in the system, but again, only even that concerns any changes of the state. So basically some rights and updates. And basically, again, one of them along with the data, Mongo primary MongoDB would send this like the cluster time, this is some internal I can try to explain it more if you will. But in general, this is some kind of ensuring this set like ordering in time. Now of the events that the cluster knows that, again, the replica sets Mongo replica set has like, what's like casual consistency. So basically, the even that are related to each other are guaranteed to have some sample so you can see your write you can read your write, you can read your read, so that and so on. So basically, this is like, so every, in the oplog when the mass primary sending this data to the secondaries, it also contains this like cluster time. And basically by this, by reading this data and reading this slide Last time, we can, we can recreate the, like the chain of events that's happened in class. And we can know at what time what even happened and basic and one of the cool features of oplog is that in deponent, I always mispronounce this word, basically, you reapply this, the same, the same event, and it leads to the same result, you can reapply the same event like 100 times to change nothing it's going to be the same so you just can, like reapply it. And data is gonna be fine. So basically like in general, we just read in this oplog, storing this oplog and like again in a special format that we know that which part of the upload relates to which time and date and basically what we are doing then we just apply in, let's say if you want to restore to some point in time which are supplying the backup and then we just like replaying all the events that after the backup to the point of sale.

**Matt Yonkovit**  
Where this becomes important that the case that I gave earlier with the unicorn who didn't have the backup and they had, basically their tables got wiped or their collections got wiped because of migration. This is where you would say the migration happened at 10:05 pm. We want to go back to 10:04 pm. And restore on that. Yeah. Because one of the problems with a lot of backups, when you do like a full backup, is it's at whatever point in time you ran the backup. So if you ran it 24 hours before you had an issue, you lose 24 hours worth of data without that kind of point in time recovery capability,

**Kimberly Wilkins**  
right? Yeah. And it is for those people who are more used to like relational databases, for example, Oracle, you can think of it like it's like the SEM the system change number, right? For the point times, you apply the redo logs, just like the oplog, right? So the like it, right? Exactly, right. And so by having behind by having a point in time, the larger backup sets, you want to make sure that you can then oplog the output. And the other thing you want to do, of course, if you're planning and you're scaling, and you want to have the shortest possible time to recover, is to make sure that you're taking your backups frequently enough, right. So that if you have a, I don't know, 5-10 terabyte database, whatever, that you're not going to apply 50 million or however many upload changes, to get back to the point in time, right? So that's the other thing as a business, you need to determine what your absolute maximum amount of time is that you want to be able to take to recover, right. And then you'll take more frequent backups if you have to be able to recover more rapidly.

**Andrew Pogrebnoi**  
And this is, this also leads me to another point that I wanted to discuss that you have to have even with like a point in time recovery, you have to have some decent like frequency of like backups. Still, not only, of course, this is 100% true that you don't want to reapply all the chain of the event because you can maybe just you mentioned you have some record which is like a change like 100,000 times from zero to one from zero to one, and you just you have to like make this 100,000 of our rights operation just to came to this like one byte of data. And but on the other hand, Now, imagine that you have one backup, let's say that you made like, two weeks ago, and you have the oplog and you want to restore to some like to one hour back, you're starting to restore and it appears that this backup is broken, it doesn't work. And that happens and that happens and then you basically screw up what you because in order to apply a pull to apply, you have to apply it on top. And if you don't have a base backup, it's not gonna work. So like again, some people probably may think that okay, I'm doing backup, I'm fine, I'm protected. Of course, this is much better than not doing backups at all. But I suggest keeping in mind that you have to test your backups because again

**Matt Yonkovit**  
So let's do a PSA right now. So hold on. I'm gonna do this PSA right now Okay, so I'm gonna go if you're watching test your backups

**Kimberly Wilkins**  
always test your backup just like test your code before you put it in production. Like Yes, definitely.

**Matt Yonkovit**  
Yes, test your backup people.

**Andrew Pogrebnoi**  
Yes, yes. And this is like it's so many layers in that because like again, from my obvious sin that if your backups don’t work, you want to know beforehand before you like relying on that and building because again, nothing is bulletproof. You could work, probably something went wrong during the backup. Probably something during which I don't know the heart right? But this backup was solid. sector and stuff like that. And on the and along with that, if you're like from time to time testing your backup it is just usual and a comfortable procedure for you. And you are more or less familiar with that. And when the time happens, you already have to restore like in production from the backup. It's so stressful. situation and you don't want to add an extra layer of, of stress by dealing with something that

**Kimberly Wilkins**  
 you need to combine them, you need to know exactly how long it's going to take you to recover a four terabyte database. Okay, I'm going to play you need to monitor your backup logs, right? You need to make sure that they're actually completing successfully.

**Matt Yonkovit**  
So I have to be Captain Obvious here for the people watching this question who did not come in, but I'm going to ask it on their behalf. How in the heck do you test it? multi-terabyte backup on a regular basis?

**Kimberly Wilkins**  
Well, if you don't, you will be

**Matt Yonkovit**  
What do I mean? Like, like, like, it's so large, like,

**Kimberly Wilkins**  
it's very large. But you know what, if you have a very large production environment, you should at least temporarily spin up a very large staging environment, occasionally, to test your backups, it should be a part of at least a monthly process, right? And I think that most companies don't do that. But like one of the things, right? Yeah,

**Andrew Pogrebnoi**  
I can feel it, I can relate to it that, like, if you have like, multi-terabyte database, it could be painful to test it, but believe me, it's gonna be more painful. If you lost production data, 

**Kimberly Wilkins**  
it's gonna be more painful, and it's gonna be very expensive to your business, right? To compare the cost of temporarily speeding up, especially, in today's times of cloud, temporarily spin up the resources required to recover and test recovery of this database, as opposed to don't doing that. And then something happens. And you are down for 4-6-8 -10-20 for however many hours, right? Yeah.

**Matt Yonkovit**  
So what if, like though like, like so so a lot of the automation and things that are out there are designed to do backups for you or keep your data up or now we've got databases of service, some people running on Atlas, other places, do you start to worry about your backups, then you start the test.

**Kimberly Wilkins**  
So most of the time, you will, you will test those when you spin up a development or QA environment, right? Because you will want to be utilizing real data, or at least a subset of real data for that. So yes, you should still test them. Because even if you do a total file system copy, right, if you do a physical file system copy, and that gets you to a particular point in time. But if you want to get past that point in time, then you will still need to apply the oplog like Andrew was talking about later, or earlier. Right. So you should still be doing it, right. So

**Matt Yonkovit**  
Andrew, you need to leave in a couple of minutes. So I want to remind you, maybe give us a few final thoughts before you log off the stream here. From a backup perspective, any tips and tricks that you want to convey to those who are watching?

Yeah, it's like, they're on PBM, right?

**Andrew Pogrebnoi**  
Like, anyway, if, like, if somebody's going to take how excited like one scene from this, I would like that be the thing that just like, check your backups and test your backups. And again, you can start not to like, at least it's much, much better just to check what happened to your backup, let's say, because again, in PBM, we put a lot of effort, we are not guaranteed 100% that all your backups gonna be fine, we finish all your backups, and no errors gonna happen because like we're not. But we put a lot of effort into this, like feedback. And to be sure that if something spoils the integrity of the backup, if something went wrong, so we would notify the user that the user is gonna see that this backup failed, and they shouldn't rely on this backup anymore. So let's say let's just start from checking the logs and checking the data of backups and be sure that it's everything alright, but of course, I strongly encourage everybody to test backup and to put some effort into this.

**Matt Yonkovit**  
Yeah. As much as it's hard for developers sometimes to think about the backups about the infrastructure, they want to write code. It will really help them out if they do check those things out. Occasionally.

**Andrew Pogrebnoi**  
Yes. And you can think of this from another perspective. Okay, you can maybe write some code for the optimization of this testing process. Yes. Oh, yeah.

**Kimberly Wilkins**  
Yeah. And PBM Percona Backup for MongoDB allows for the point-in-time recovery, right? You shut up and you do point time PBM backup triggers, then it starts capturing your changelog, the equivalent of the OP log, right, so that you can apply the changes for both the replica sets and also for the shard clusters, right? So it's similar to the redo logs, and the incremental backups should go along. So you always want to take your larger backups, and then your incremental backup so that you even get to where you want to be faster. Right. So Andrew, can you tell us a little bit more about basically, how PBM does those types of things, right? Because you're the one that codes a large majority of these features? Yeah,

**Andrew Pogrebnoi**  
I'll try, but I'm probably gonna drop off. 

**Matt Yonkovit**  
Yeah, he has a personal obligation. So he needs to bail on us, which is cool. We can come back and we can do a bit more.

**Andrew Pogrebnoi**  
Yeah, maybe we can make another iteration of this. To talk to talk. Or maybe I can come to your podcast, Matt, and to talk about what you can arrange Oh, yeah. I have Parker. Yes. And I love to talk about this, like, guts of the system of PBM. Particularly, and to dive deep to some okay, yeah, just use the technical stuff. But let's close and watch for me for like, just try PBM. Just drop us some feedback. If you want to find some bugs or some issues, we would love to hear from you and deal with them. So yeah, just try it out. Try it out.

**Matt Yonkovit**  
All right. Thank you, Andrew, and we swinging by here, chat with us, we'll have you on another episode of either the podcast or the live stream here. And we'll get a little bit deeper into the weeds.

**Kimberly Wilkins**  
Sure. So I was pleased. pleasure. Thank you. Thank you. Yeah. Yeah. Like, and then there were two, right so then, the other thing is again, the best practices type of things, right? You take your backups, test your backups, do the incremental backups test them, make sure they're doing everything that you need to do. Make sure you have your settings correctly. But just all those things are the important things. The other thing too, that PBM does, it does allow you to backup to s3 and s3 compatible storage sort of places, right? So you don't have to do it all on-prem, or local, whatever. And that's what I was talking about a little bit before, you can split up the resources temporarily to test the backups and then and then get rid of them so

**Matt Yonkovit**  
and to do these levels of backups with Mongo without PBM. And the reason we built PBM was you had to pay Mongo for the ops manager and the enterprise thing. So that's why we took functionality that we felt should be in the open-source base and added it to PMM. Or Yeah,

**Kimberly Wilkins**  
yeah, yeah. And that's what we kind of do. In general, we take the community version of Mongo, and we try to add features that are enterprise-level, in our own ways, right? So yeah, okay. Yeah. So that's, that's the backup snapshots, just the different things, again, the sheer size of backup sets and data sets these days, it's super important to plan for these things ahead of time, and to think about these things. So

**Matt Yonkovit**  
I mean, let me throw out to the developers out there. So my big thing this past few months, and going into next year is about how much database design impacts the long-term scalability of systems. And as we talk about some of these large backups and these large scale systems, one of the biggest issues that I continually see and this is not backup related, specifically, but is a lot of testing that occurs ends up testing at a micro chasm of what is actually the production size. And people go through, they build new features out and they build it on a 20 gig data set. And then when they get up to a multi-terabyte data set, they don't know why it doesn't work the same way. And that's something that I think my PSA, looking in the camera, everyone is everyone realizes that as the workload changes as the data size changes, things will change in how the database, whether you're running Mongo, Postgres, MySQL, Oracle SQL Server, at scale, different decisions are made internally by the database by the optimizers. And you can have something that works today that tomorrow is completely broken.

**Kimberly Wilkins**  
Yeah. And Matt, a big point of what you just said is we've been talking about data sizes, we've been talking about these big data sizes. But we also have to think about the number of write operations, the number of reading operations, the number of ops that are hitting the database, the ops that are hitting the disk, the network impact, right? Because taking these backups of these large sets will also impact, right, and network operations. And also impact cost, right? Because you're sending network traffic outside of your containers, or your zones or your regions, etc, then that's network costs in most of the large cloud providers, right?  all those things come into play.

**Matt Yonkovit**  
Yeah, yep. Absolutely. Yeah. Um, so I'm looking, we don't have any, any questions. But we did have quite a few people just make some comments here and there, and we appreciate you hanging out with us today. Um, Kim, is there anything else you'd like to cover? We've got about a few more minutes if we wanted to cover a few extra things? Or we can, we can end it if nobody has any other questions?

**Kimberly Wilkins**  
Well, I mean we talked a little bit about scaling, I mean, scaling is always important. There are always things that you're taking into consideration, whether you're talking about backups or not. And the ideal developer audience, schemaless, but you still need to think about your database design. It's not schemaless. Because if you go into that, even with five, zero once it's actually stable and running correctly, and you can change your shard key on the fly, the thing you have to think about, when you're changing that shard key, you're going to be doing more right activities. So that's also going to be a performance impacting writing. So you always have to think about where you're going to do your backups if you want to know if you want to do second secondary, but also just whatever other changes you want to do, right?

**Matt Yonkovit**  
Yeah, absolutely. I mean, that's a key thing, right?  performance changes or changes to things can be changed for the better or for the worse, right? And a lot of times performance issues and scalability issues in any application are whack a mole, right? So this is not database-specific, right. Um, I have seen numerous cases where you have an application, and you have a bottleneck that is choking some sort of like, throughput to the system, some sort of, like can like, like the number of threads going on, and you open that up and you go from like, great, we were bottlenecked and we only were able to do 10 things at a time. Now we can do 30. And yeah, you've just made the system way worse, right? Because all of a sudden, 30 things happen. 

**Kimberly Wilkins**  
it changes in the engine behaviors of the databases, whether it's Mongo or another one, but changes in maga, specifically, chunk management movements, Jumbo chunks, were the jumbo Chuck's right there by the end that was a big change that happened in a portable version is where they moved it from from the Mongo S to the Mongo D, and all of a sudden, the MongoDB actually knows what size it is the primary the MongoDB. Hey, this is a jumbo chunk, we need to split this. And so you're getting more splits, you're getting more migrations, there's more writes more impact to the database, but fewer jumbo checks, better chunks, better-balanced props away. So you always have to think about the things that are the improvements and how your application specifically behaves. And how you think that those changes will impact you. Before you even consider Hey, should I upgrade or not. Don't always go for the latest, greatest, fanciest thing. Think about your application, how it works and how your customers and your users use it.

**Matt Yonkovit**  
Right right. Yeah. Always good advice. Thanks for swinging by and stopping by the meetup. We appreciate all of those who are watching either live or offline. You know the recorded version of this if you have future topics you would like us to cover, if you'd like to be a talker speaker on this just come on and chat with us about something you're passionate about. We do these every week we've got a MySQL one the first of the month or the first week of the month, then a Postgres one the second week, then Mongo, the third week, then we talk about PMM and observability in the database base, the fourth week so next week, we're going to be having this same time, same day, it's going to be on observability and monitoring so if you're interested in those topics, feel free to swing by we're going to be talking about some other things but please do come out and don't forget to check out my podcast, the HOSS talks FOSS, always love to talk to people there as well. So if you're interested, that would encourage you there. But thank you, everyone, for stopping by. We appreciate you hanging out with us for about an hour and we'll see you next time.

**Kimberly Wilkins**  
Great. Thanks. Thanks, everybody.




![Percona MeetUp for PostgreSQL October 2021](events/percona-meetup/MongoDB-cover-october-1920.jpg)

Now that MongoDB 5.0 is out, the Percona Community MeetUp for MongoDB in October will highlight new features of this release. We will also talk about backups, scalability, and security. Our experts, Andrew Pogrebnoi, Principal Software Engineer at Percona, and Kimberly Wilkins, MongoDB Technical Lead at Percona, will join Matt Yonkovit, The HOSS at Percona, to answer all your questions.

Join us for an-hour MeetUp for MongoDB:

* Date: Wednesday Oct 20th, 2021 at 11:00 am EST / 5:00 pm CEST / 8:30 pm IST

* Live stream on [YouTube](https://www.youtube.com/watch?v=YnQu2Ock2d8) and [Twitch](https://www.twitch.tv/perconacommunity)

* Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NThiMGw5Mmw0azkzZzc3a2s5ajZvMGNvcnVfMjAyMTEwMjBUMTUwMDAwWiBjX3A3ZmF2NGNzaWk1ajV2ZHNvaGkwcTh2aTQ4QGc&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com&scp=ALL)


Your attendance to The MeetUp for MongoDB is highly encouraged if you are:

* User of MongoDB.

* Student or want to learn MongoDB.

* Expert, Engineer, Developer of MongoDB.

* Thinking about working with databases and big data.

* Interested in MongoDB.


**Go ahead and come with your friends!**

Subscribe to our channels to get informed of all upcoming MeetUps.

Invite your friends to this MeetUp by sharing this page.