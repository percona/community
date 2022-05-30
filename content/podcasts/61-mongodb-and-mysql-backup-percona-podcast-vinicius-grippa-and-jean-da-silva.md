---
title: "MongoDB and MySQL Backup – Percona Podcast #61 with Vinicius and Jean"
description: "Having worked on multiple databases from MongoDB to MySQL, they talk about choosing the best database for the job. Join Vinnie and Jean da Silva at Percona Live"
short_text: "Matt Yonkovit, The HOSS at Percona, presents this friendly podcast with two engineers from Support at Percona. Both Vinicius Grippa and Jean da Silva are from Brazil. Get to know Vini and Jean as they suggest the must-do activities if you visit Brazil.  Jean and Vini then jump into talking databases. Having worked on multiple databases, Vinnie talks about choosing the best database for the job. Matt can't stop playing favorite open-source question-answer as well! Join Vinnie and Jean da Silva at Percona Live. They will present their talk Percona Backup for MongoDB - PBM short - The Backup Open Source Tool for MongoDB at Percona Live. In this session, they will highlight how PBM can help back up the large database."
date: "2022-05-02"
podbean_link: "https://percona.podbean.com/e/mongodb-and-mysql-backup-%e2%80%93-percona-podcast-61-w-vinicius-and-jean/"
youtube_id: "kM61hDY7oTg"
speakers:
  - vinicius_grippa
  - jean_da_silva 
  - matt_yonkovit
aliases:
    - "/podcasts/mongodb-and-mysql-backup-percona-podcast61-vinicius-grippa-and-jean-da-silva/"
---

## Transcript
**Matt Yonkovit:** 
Hello, everyone. Welcome to another HOSS Talks FOSS. I'm the HOSS, Matt Yonkovit. And we are here to talk to Jean and Vinny, about their time here at Percona about upcoming Percona Live talks about all things MongoDB all things, MySQL, and everything in between. Hello, Jean and Vinny, how are you two? 

**Vinicius Grippa:**  
Hey, Matt,  

**Jean da Silva:**  
I'm fine. 

**Matt Yonkovit:** 
You gonna talk at the same time, but I will direct traffic today. That's okay. Let me start with Jean. Jean, why don't you introduce yourself? Where are you speaking to us from?

**Jean da Silva:**  
Hello, everyone. My name is Jim. I'm from Sao Paulo, Brazil, Support Engineer here at Percona for two years long. And yeah, for me, it's thank you for inviting me to this podcast. So I hope the audience also enjoys it.

**Matt Yonkovit:** 
Jean, how did you get started in the database space?

**Jean da Silva:**  
Yeah, I mean, here in Brazil, I did the university for the database. So it just I started to work with that from university. And then I started as an intern, and then I moved on to my previous company, as a DBA. And then also had this opportunity at Percona. So I think it's three-four years working in this area. I mean, compared to, to you guys, it's small, 

**Matt Yonkovit:** 
Don't feel bad when you're this old. You forget everything. And now you probably have more knowledge than I do. That's okay. Vinnie, you've been on this show a dozen and a half time, probably like 20 times, right. You're an old hat at this. But Vinnie, where are you located? And maybe give everybody your little background? Your two seconds' worth of fame? 

**Vinicius Grippa:**  
Oh, well, first, it's a nice way logicians told that we are old. So we have a lot of experience. But yeah. I'm working at Percona for five years already. And it's still counting. I'm super happy with that. And currently, I'm in Brazil. For those who doesn't know, I was born here in Brazil. And I have lived in Europe for a while. But well, because of COVID. Things changed a bit and I'm back at my homeland for now. But already planning the next adventure. So we will see.

**Matt Yonkovit:** 
All right, so next time, if I come to Brazil, what are you guys going to have me do what like let's start there. Like what is the must thing to do in Brazil? For me when I go there?

**Jean da Silva:**  
I think we can. We can go to eat Feijoada. It's a good start here in Brazil. So it's very Brazilian dish. So  it's a freight. Yeah, it's that tasty food for us here. I mean, it's heavy. I mean, in terms of, but it's a very good, and then we usually eat Feijoada with Caipirinha, which is a very good combo. So yeah, it's a good start.

**Matt Yonkovit:** 
Vinnie, Vinnie, do you concur with this? Or do you is there some other thing activities that you're going to that I should do? Like it? Must I must do this?

**Vinicius Grippa:**  
Well, I fully support his idea.

**Matt Yonkovit:** 
Laughing, so I'm a little worried

**Vinicius Grippa:**  
No, no, no, I'm not mentioning the parties and all the hard stuff in Brazil and just talking about food. For those who love meat, be sure Oskari here in Brazil, to eat some traditional Brazilian meats. People love it the way it works here. So yeah, I think the two things you need to do here. It's eating and drinking.

**Matt Yonkovit:** 
Eat and drink. Okay, it sounds like a fun place. It's almost like Uruguay?

**Vinicius Grippa:**  
Yeah, exactly. 

**Matt Yonkovit:** 
Yeah, you're both you're both smile and nod at the exact same time. There you go. Our friendly neighborhood, Uruguayans approve as well. So that's awesome. So both of you have been at Percona for a little while. Now. Vinnie, your background and your experience is a little different than jeans. Jean, you're you're mainly focused on Mongo, is that right?

**Jean da Silva:**  
No, I also help with MySQL. Okay, great. But on the database on the daily routine, I usually talk take more Mongo issues, but yes, also, I also have the team with MySQL.

**Matt Yonkovit:** 
And Vinnie, you have kind of flipped back and forth between databases left, right and sideways. You've written a book on MySQL, you've really gotten into the depths of MongoDB as well. So you kind of know both sides of the coin there.

**Vinicius Grippa:**  
Yes. And if you guys are interested in knowing my favorite database, you will have to ask me in Austin at Percona Live?

**Matt Yonkovit:** 
Yeah, no, no, no, we're gonna ask you on this during our rapid fire questions session, I just invented it an hour ago, where I asked you random questions, and we see what your answers are. So that's going on there. So you have about 10 minutes or so to figure that one out. Yeah, and you're gonna answer Postgres, right? 

**Vinicius Grippa:**  
True. 

**Matt Yonkovit:** 
I think every time you say Postgres and angel gets his wings, so,

**Vinicius Grippa:**  
Yeah, it's true. No, but truth to be told, like, I really enjoy MySQL and MongoDB. They both have, but I don't have experience with Postgres. But from what I see and what I heard, it's a very good database as well. I think the best database you can work with is the one that you know the best. So it doesn't matter much if you work with a database that you don't have experience with. So you want to extract 100% of the performance.

**Matt Yonkovit:** 
So what sort of apps is you seeing being used for MySQL and Mongo? Where does that line fall? With your support activities, when people call you, are you seeing more? Web apps, mobile apps like, like, where do you kind of see the trends going?

**Vinicius Grippa:**  
For MySQL, what I have been seeing, for example, a lot of customers works similarly as WordPress, which means is that each user has a schema inside the database in its own tables. So it's kinda like you have several customers working on the same database, probably with the same schema or slightly different mobile apps. Gaming, we have a few gaining customers as well. They use MySQL as a platform for their production. When the game is online, and, and the players will replay. So the application is many in various.

**Jean da Silva:**  
Yeah, yeah, I think one of the things that we can see a bit in the Mongo universe is regarding about their database size. Usually, I don't see something similar in MySQL, of course, there are a lot of environments that we work in, but usually our Mongos customer, they have they have a huge replica set or even clusters. So I think they are going more with big data things.

**Matt Yonkovit:** 
Define big in this context because everybody has a slightly different version of big data. What does that look like for you?

**Jean da Silva:**  
For me, when I see a replica set with, I don't know, more than 10 terabytes of data, it's, it's huge for me. And then if we split that on our sharded cluster, it will be more easy to, to administrate. But also, in my perspective, more than 10 terabytes of data in a database is too much sometimes. So yeah, that's that's my perception on big things.

**Matt Yonkovit:** 
Vinnie, what do you have a limit? Is Jean wrong or right?

**Vinicius Grippa:**  
No, he's right. And like even for MySQL, huge databases are terrible to manage, because of backups restart times DDLs are very difficult to operate; it takes a long time and requires a lot of planning. Usually support we have kind of an entire no rule, we don't say much, but it's if your database is growing above two terabytes in a server, you should consider our origin or sharding, or something like that because it's a good limit where SSDs can perform relatively fast in this stuff.

**Matt Yonkovit:** 
Yeah, all kinds of operational issues become a challenge at scale. I mean, even with the Mongo, which has built-in sharding, and a lot of features for more of a cluster, which isn't something baked in necessarily to the MySQL ecosystem. You do have issues. One of the classic issues is how do you back up such a large monstrosity, monstrosity of a database like if you've got a 10 shards terabytes each How do you back that up?

**Jean da Silva:**  
Yeah, honestly, I think we are good in MySQL because MySQL has a lot of community too. For help to help you to deal with backups, but then when you go to the Mongo world, it's quite a problem because we only rely, I mean, if we are talking about the open source solutions, so if we talk about only the open source, we have the Mongo dump, more important, then the Percona solution, which PBM. So to manage this kind of huge dataset, it's, it's problematic. So then I see the tools for MySQL. And at something I really like, because you have XtraBackup, you have MySQL pump MySQL dump, we have a lot of possibilities to, of course, we start to be limited, because we are your database. It's huge. But I mean, we have options at least. 

**Matt Yonkovit:** 
Yeah, yeah. And I mean, so you actually, both of you have a talk on PBM. Coming up at Percona Live or depending on when this podcast is released. Maybe after or you did, as it might, I don't know, it could be before or after we do record and then release once or twice a week, depending on where this is in the queue, but we'll just assume it's coming up. And if it's not, you can make it come up by just going to YouTube and searching for it. So from a PBM perspective, are you going to talk to us about how PBM helps backup those larger systems?

**Vinicius Grippa:**  
Yes, we are going to present two types of backups that PBM is bringing to the open source environment, which willl help hugely the community for those who doesn't want to stick with Atlas, which is the enterprise and paid version of Mongo Inc, which provides a set of features, but everything has a price. We will show examples, how to do backups of these large data sets. And the great thing about PBM is that besides being open source like it, it expands your possibilities. Like if you want to save her a bit copying Amazon s3, Google Cloud Asier, it has native support, so you can integrate easily with your cloud environment.

**Matt Yonkovit:** 
So here's an interesting question. Jean, you mentioned all the fantastic community tools in the MySQL space. Why are those tools in the Mongo space?

**Jean da Silva:**  
That's the question. I asked myself since I started to work with Mongo. Yeah, that's something unclear for me, I talk I have some friends that work with Mongo. And I don't know, I don't know if it's something because of their approach. Honestly, I don't know. MySQL started as an open-source Institute, open-source, even they even though it's, it's from Oracle, but the root of the nature of MySQL, it's open-source, Mongo, since its beginning, its open source birth, as this path to the enterprise way. So I don't know, honestly, why we don't have such an approach in the MongoDB universe, which is, unfortunately, not good for the users.

**Matt Yonkovit:** 
I wonder if it's because the focus in Mongo tends to be on development teams, and focus on the development features and less on the administration. So they try to hide some of that. I mean, I know from my personal experience, when I was a youngster, dinosaurs roamed the earth. And I had to like, like, survive against velociraptors trying to eat me and stuff, and was a dB at the same time. Long ago. It was the pain that made me solve some of these issues, right. So you would develop a tool most of the toolkit, for instance, was developed, because we needed it to do our jobs. Right. Like oh, we're missing this thing. We need to go do it. And XtraBackup, for instance, was originally a paid-for feature by InterBase, who ended up getting bought by Oracle. And then it was brought to the open-source space by Percona. But it was that pain where you have something you need to do, you can't do it and you move on. I wonder, are the users and the people who are responsible now for Mongo instances, more developer architect-focused and less infrastructure-focused? I mean, is that part of the reason?

**Vinicius Grippa:**  
I would say so. We see, and that's the good and bad thing like the imago has done over 1215 years of age. If it's a relatively new database, so , and it has a really specific use, and we see like developers using it in a constant way to make, because your schema less , so you can store everything, it makes your development much faster, but also brings problems and this lack of maturity. I think it's the big problem with the people that are using it. And with the tool with the database itself.

**Matt Yonkovit:** 
Now, Jean laughed, he couldn't help himself.

**Jean da Silva:**  
No, it's my normal way.

**Matt Yonkovit:** 
When he said schemaless, you had a grin that was ear to ears. So would you like to clarify?

**Jean da Silva:**  
No, I mean, that's the way that Vinod described it, it's perfect. I mean, that the things need to be faster and schemaless the way that you don't need to get relations between extractor, it's easier to deal with. So yeah, I mean, let's work on the problem, then. Let's get started based on the site. So I don't know. 

**Matt Yonkovit:** 
Wait a minute, wait a minute, wait a minute. And so this is why I thought you were grinning. And I was gonna pick up on this, which is, I hear the term schemaless. And I laugh myself because I don't think that MongoDB is truly schemaless. I think that you actually do need some sort of schema or at least schema validation. And you need to validate the data that's in there. Otherwise, performance issues happen as soon as you start getting to scale. Am I right?

**Jean da Silva:**  
You are correct.

**Matt Yonkovit:** 
I am correct. Yes. Wait for the bell. Everyone ringing the bell? I am correct. I love it. When I'm right, we should just stop now. We should do a microphone drop right now. And like because I'm right. And I like to end it. I know. No. But no, no. I mean, I think that it's interesting. There are a lot of databases nowadays that come out. And they try to throw away the shackles of SQL or throw away the shackles of data validation. And realistically, I think the power and benefit of many of these, including Mongo itself, is the ability to add and remove data as needed, yes, and not have to worry about the overhead of managing those objects. But that schema validation still has to happen somewhere. If you're not doing it in the database, you're still doing it in code. And if you're not doing it either place, you're setting yourself up for a big problem. But even so, even if you're doing it in code, aren't you gonna run into index issues, performance issues, potentially, if you're just kind of throwing anything that you want into the database?

**Vinicius Grippa:**  
Yes, I like to say you can treat your database as your garbage, or you can put everything without any order. Yes, like, that's what we face in support of a lot of these issues. Because things read faster when the database is quite small, but they are schema-less without proper organization, it becomes a problem. And Mongo grows, the data grows the data much faster than MySQL, because we start, usually people use to start much more things. So it can become a problem really quickly. And as you said, Matt, I like to say like, it is better to build the plane on the ground. Let's not try to make improvements while he's flying. So that's what we need to do with MongoDB.

**Matt Yonkovit:** 
Good point, yeah. It's always more difficult to go back and change the architecture. Right? Although, a lot of times, you do have to figure out how to make that plane stay in the air. Yeah, which is what DBAs and data professionals and SREs are doing, right? We're trying to make that plane stay in the air as much as possible. Very important there. Now, as the database is specifically Mongo, but also others, they evolve, they add more and more features between every version. Mongo, for instance, didn't use to have transactions. Now it does, right. I mean, big changes in some cases where you go through massive architectural changes between different versions of databases. Sometimes it leads to performance improvements; other times it leads to degradation. Now, I told Jean that I was going to do this we appear to have a snafu on the Percona live schedule because Jean submitted an awesome topic about the performance difference between different versions of Mongo. And somehow, it missed the final schedule, and I gotta go figure that out. I'm gonna do that right after this podcast, I promise you, but here's the thing. I'm curious. What do you see In between those different versions? Are you seeing that? You were seeing linear performance improvements? Or are we seeing degradations?

**Jean da Silva:**  
We see some degradation. But again, there, there is a lack of documentation about that. There's a lack of blog posts and reserves on this thing. So since Mongo, I mean, our, our life in support, we have a bunch of customers that do an upgrade, and then come to us, Hey, I did an upgrade and why it's getting slow. So we see because there are some new features like the transactions didn't, didn't exist sometimes, some time ago. And there is a lot of validation that Mongo also starts to do in the new versions that it doesn't, that doesn't happen before. But again, we still lack this kind of resource, this kind of analysis. And we see that we see this, this loss of performance. But we can see in terms of numbers, how much is that we know that something around 10 - 15% of, if I mean, comparing Mongo 2.6 to 4.0, and then it's got is smaller between 4.2 and then 4, not 4, but its tool, performance degradation. But again, we don't have these numbers. And the talk that I submitted was to give some numbers to the audience to the public and say, okay, there is a loss or not.

**Matt Yonkovit:** 
Well, so I'm a stickler for benchmarks. I like benchmarks. I love data, I love to see things. So we are going to have that one way or another, it might not be ever gonna live, I might have to get you on a live stream. And we might just do it. In fact, we shouldn't do it live. We should benchmark these things. We should make them cry. We should see where they break. I love doing that. I love playing stump the expert lives. So if you want to come on and play stump the expert, we'll blow up some Mongo instances. I love blowing up MySQL and Postgres. I'm an equal database destroyer. I'm not trying to be a fanboy of one over the other. But we can do that. Now. We're going to start something that I started literally two hours ago, I recorded another podcast earlier today. And found that when I have multiple guests, it's often interesting to ask them the same question and see if they have any responses and see if they'll argue about it. So we're gonna go roundtable as quick as we can. And we're gonna see if you two agree with one another, and we're gonna see like, what sort of things are in sync and maybe get some different opinions. So, are we ready? Yeah. Okay, no. What's your favorite open-source tool?

**Jean da Silva:**  
A favorite open-source tool? PMM.

**Matt Yonkovit:** 
PMM. Okay. Vinnie, favorite open-source tool? 

**Vinicius Grippa:**  
Percona Toolkit. 

**Matt Yonkovit:** 
Percona Toolkit. Okay. Okay. Vinnie. Favorite MongoDB command?

**Vinicius Grippa:**  
Drop database.

**Matt Yonkovit:** 
Oh, that's what you don't run very often. Gee, favorite, favorite. MongoDB database command. 

**Jean da Silva:**  
Explain. 

**Matt Yonkovit:** 
Explain. Okay, okay. Jean, favorite Linux distro.

**Jean da Silva:**  
CentOS,

**Matt Yonkovit:** 
Does that even exist anymore? I mean, does it relate to your favorite distribution?

**Vinicius Grippa:**  
I will stick with CentOS seven.

**Matt Yonkovit:** 
Oh, my God, you guys are killing me because it doesn't exist anymore. Like, okay. But I have Marcos. And Marcos was on a live stream a week ago, and he's given me crap about why I would choose Ubuntu, and I'm like, and he's like, are you CentOS? And I'm like, it doesn't exist. I can't give him a rocky Linux so he's building everything with Rocky right now. But it's one of those things, but okay, so you're both CentOS fans, which I assume will just be because it's free Red Hat. Yeah. I mean, we'll just leave it at that. It's free Red Hat. Yeah, that's what it was. Okay. Okay. So the largest database you've ever worked on?

**Vinicius Grippa:**  
For MySQL, 15 terabyte databases on a single instance, with no replication, no backups

**Matt Yonkovit:** 
No backups? 

**Vinicius Grippa:**  
No.

**Matt Yonkovit:** 
Wow. Yeah. Okay. That's weird
What was the application? What kind of application was it?

**Vinicius Grippa:**  
I don't recall. I think it was a monolith. I was running for four years in the company. The machine was most rules we will have Read 28 cores, one terabyte of memory like was huge. It was Colosse. It was crazy.

**Matt Yonkovit:** 
Okay, Jean, the biggest database you've worked with

**Jean da Silva:**  
Mongo, I would say I work at this at ten sharded clusters with no backup as well because there is no backup solution 

**Matt Yonkovit:** 
How much total disk space was that?

**Jean da Silva:**  
I would say it's five terabytes. Not that much. But I mean, it's still ten shards.

**Matt Yonkovit:** 
Vinnie and Jean win three exercises. Yeah. Okay! Jean, what is the worst problem that you see customers, companies, and users make over and over again, in the database over and over? 

**Jean da Silva:**  
I think it's the way again; I see it's often in our daily routine. So when going to shard, they just go and shard by random keys. And that's not the way it works. And then it comes to us, Hey, is not working. And then we saw, okay, your key is not working for this. So how do we do that? I mean, in the previous version from Uncle, there's no way to fix that. I mean, you have to dump and import again. Okay, so that's the problem. 

**Vinicius Grippa:**  
I think it's pretty much what Jean said, like, not only for Mongo but also for MySQL, you have badly structured data. So you have a table with 100 varchar fields with 4000 characters and like 100 indexes, and people are complaining because why my writes are slow and why so hard my life is like it's bad design. That's a bad sign.

**Matt Yonkovit:** 
Okay. I don't know if I should ask this. But the worst outage you've seen doesn't have to be somebody you've done it Percona or outside Percona or customer; it could be anywhere worst outage that you have got seen. Or worst, company crippling event.

**Vinicius Grippa:**  
Well, I had a case where I work in with, with Mongo, like production systems, you don't have only one, one server, you work at least with three. And this guy, he was running his production, only a single server, the disk crash it. And then the database got corrupted; we had to run like two tools that go really into the physical files to extract the data. The guy was offline for days because there were no other options. And like, we could recover the 60s 70% maximum of the data. So like, mobile was not consistent before and after was even worse. So that was my crazy story. 

**Jean da Silva:**  
For me, it's, it's funny because it was on Oracle Database doing the upgrade. And, I mean, we had to open a bug, or I mean, we have to escalate the issue for the Oracle Support. And you had the day in the system down for a while, while the guys work on that. So was doing an upgrade on Oracle.

**Matt Yonkovit:** 
The worst that I've ever seen is, that someone did a data center failover and forgot to set up backups. Then someone dropped the database. Did that drop your favorite command there, Vinnie dropped the database and didn't have any backups because it hadn't run backups for three months. Yeah, yeah. Forensic data recovery took over a week and the company went out of business within six months.

**Vinicius Grippa:**  
Yeah. Yeah. It's designed for such things. It's crazy.

**Matt Yonkovit:** 
Indeed, indeed. I was going to do this. Vinnie. What is your favorite version of MongoDB? I see I changed it up. I asked. But I didn't I said favorite version of MongoDB. Like, like, what version do you think was like, Wow, this one was great. 

**Vinicius Grippa:**  
It was 3.6 had many improvements compared to previous versions, while the white diving gene was gaining traction and becoming more and more major. Also, on the sharding aspect. Mongo brought a lot of improvements. More, it was more stable and less problematic. So it's how it reached its end of life. But I think it was the big one. The three six

**Matt Yonkovit:** 
Jean, what about you?

**Jean da Silva:**  
Mongo or MySQL?

**Matt Yonkovit:** 
I'll let you choose either one. Vinnie chooses just Mongo. But you could choose.

**Jean da Silva:**  
I'll go with Vinnie and Mongo. Because, I mean, we share the same things here.

**Matt Yonkovit:** 
I shouldn't make you submit your answers ahead of time. Like, we can be like, oh, like how well do you know each other? 

**Jean da Silva:**  
Yeah, and for MySQL, I like the 5.7 version, because that is where I started in university. And then I also am still working nowadays, so it's very reliable, and that's such a good,

**Matt Yonkovit:** 
It's amazing how the versions and the tools you start with stick with you forever, right? And even though like new iterations and new features, you're like, Yeah, I still like that version. That's where I started. Yeah. Yeah. All right, I'm gonna ask you one more. And then we're going to, we're going to have to end it. And we're gonna have to catch up back at Percona Live. So what do you see is the most interesting thing in the tech space? What are you excited about? What are you seeing out there? Whether it's database-related or not? Doesn't even have to be database related? Jean, why don't we start with you? What kind of technologies or things are you really interested in learning about or experimenting with?

**Jean da Silva:**  
I think that's something I learned here in Percona, which is community support. I mean, I used to work in a private company and work, do things from there. And then, when I started to work here, Percona, it's nice to see how the community interacts with it. With the database with the problems, you go to the JIRA and then open it, I didn't have, that view when I worked in my previous job. So then I joined here, and I could see this open source world, which is for me, amazing. And happy to be part of it. 

**Matt Yonkovit:** 
Did you answer that because I run a community? 

**Jean da Silva:**  
Not all honestly, that's my get out of this. 

**Matt Yonkovit:** 
I mean, just you might get had.

**Jean da Silva:**  
No, no, I'm, I'm totally honest here.

**Matt Yonkovit:** 
Okay. Okay. Fair enough. What about you, Vinnie? What have you interested in? What are you trying to explore and figure out?

**Vinicius Grippa:**  
Yeah, people were gonna judge me. But yeah, I would like to learn more about groceries. It's been a database that has been largely used; then it's been the preference of people that try to get out from Oracle. Go to open source solutions. So it's the first database nobody goes to MySQL or Mongo. It's always supposed to. And I think it might have it is a great thing to learn.

**Matt Yonkovit:** 
Hmm. So we're thinking about doing 100 days of Postgres, Vinnie. Do you want to come along on that journey with us?

**Vinicius Grippa:**  
Well, I can try. But I'm really a junior guy. So you have to teach me the basics.

**Matt Yonkovit:** 
The good news is our good buddy Charlie, who also happens to be in Brazil. It just so happens, the big database community there is doing a weekly or bi-weekly live stream, where we're going to go through every part of managing and setting up and doing everything in Postgres. We're three episodes in, actually four because Charlie got a little long-winded on the second, we had to do two episodes, but there are really three episodes. So, Vinnie, you can come along the journey with me and Charlie, as we, we figure out how to do this. And maybe you can help me stumped Charlie once in a while, because I've got some workload that I like to throw out there. And he's like, What the heck is happening? I like to do that. I like to stump the experts.

**Vinicius Grippa:**  
Yeah, for sure. It's going to be a pleasure. I know Charlie, well, we worked together before he became the Postgres tech lead. So yeah, it will be a pleasure to be with Mr. Batista and Matt Yonkovit.

**Matt Yonkovit:** 
Well, I want to thank both of you for coming out. I'm really excited to see you in person. It's gonna be fun at Percona Live, I am sure. We're gonna have lots more conversations. I'm actually doing live podcasts from Percona Live, so you can swing by the podcast booth. We have a podcast booth, where you can come in and say hi, and get on the air. And you can have the dozens of dozens and dozens of people who like me follow YouTube. But all right. Well, thanks for coming on. And until next time, we will see you later.

**Vinicius Grippa:**  
Thanks, Matt. Thanks, guys.

**Jean da Silva:**  
Thank you. Alright, see you there.


