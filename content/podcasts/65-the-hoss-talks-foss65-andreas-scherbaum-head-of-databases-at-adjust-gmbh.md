---
title: "The HOSS Talks FOSS 65 - Andreas Scherbaum, Head of Databases at Adjust GmbH"
description: "The man behind the blog PostgreSQL Person of the Week in Percona database opensource podcast "
short_text: "Heard of the PostgreSQL Person of the Week?  You should have!  The man behind the blog and effort stops into to chat with the HOSS about all things PostgreSQL-related"
date: "2022-05-10"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-65-andreas-scherbaum-adjust-gmbh-at-head-of-databases/"
youtube_id: "QL0ZsmVBWuA"
speakers:
  - andreas_scherbaum
  - matt_yonkovit
---

## Transcript

**Matt Yonkovit:**  
Hey, everybody, welcome to another HOSS Talks FOSS. I'm the HOSS, Matt Yonkovit, Head of Open Source Strategy here at Percona. And today, I'm joined by an extra special guest from the Postgres community. Andreas Scherbaum. Andreas, how are you today?

**Andreas Scherbaum:**  
Hi Matt!  I'm doing good. Thank you. And good afternoon to you

**Matt Yonkovit:**  
Thank you very much. Yes, I appreciate it. And for those who are watching, you'll see that Andreas has a shirt that says, not money, not fame, but ice cream. So he works for ice cream, not money and fame, which is great because that's all I can afford to pay. But as we have people who are listening, not just watching, I figured I would give them the rundown of the shirt. Now, I noticed in this camera, you also have this wonderful elephant poster behind you, that I have not seen on our previous recording because of the way that it was. So, that in memory of Postgres or is that just a cool elephant photo you like?

**Andreas Scherbaum:**  
That actually two pictures of an elephant. Oh, one picture is just an African elephant. The other it's a poster with a Postgres sign

**Matt Yonkovit:**  
Ah, okay, there you go. There you go. Now, Andreas, you have a very similar story to my story in terms of how you got started. In your career, I got started in the mid-90s 95 through 97-98, working at an Internet service provider. And I found out that you did as well maybe tell us how you got started in Postgres. And what kind led you to Postgres in the beginning?

**Andreas Scherbaum:**  
From 1996 to 97, I was working for an ISP. And we also started doing websites and not only static websites, but dynamic websites, obviously, PHP came up, and then we were looking for a database with my colleague on MySQL, we weren't entirely happy with it. And we looked a bit further up on Postgres. I joined the IRC channel, of Postgres, and then I got stuck. I'm using Postgres.

**Matt Yonkovit:**  
Ah, yes. So you kind of fell in love early with Postgres. And you started working and contributing towards that over your career, and really focus there. And your career has gone from many different companies in the Postgres space, and you have done lots of contributions over the years. I've seen videos and presentations you've given previously on various Postgres topics. You've worked for pivotal EMC, Greenplum, it'd be kind of everything in between, right? 

**Andreas Scherbaum:**  
Yeah, I mean, it's all one big company in the end, because it was acquired by VMware, but was a spin-off of VMware and EMC and I worked for EMC and joined Pivotal and EMC and pivotal again, long story short, but I was working on what 10 plus years for Pivotal, and VMware.

**Matt Yonkovit:**  
Well, let me ask you this. What about databases, it just kind of like got you hooked. I mean, a lot of people go into development, they like to code things they like to maybe do sysadmin work. What about databases kind of stuck out in your mind and just kind of clicked early on?

**Andreas Scherbaum:**  
It's not much about databases about data. So I loved it. I love to work with data. I love to make sure that data doesn't leak, collect, and verify everything. I love to automate things when they all play together somehow because I got to love Postgres because it takes care of the data we have.

**Matt Yonkovit:**  
What at a certain point, you started getting involved in not only the IRC community, but the local communities in Europe, and you have grown , and you have you are on the board of Postgres Europe. I'm curious, how did that all start?

**Andreas Scherbaum:**  
This started was one Italian guy popping up on an IRC channel in early 2007. Announcing they have a prosperous country event in Italy, who wants to come? This Postgres conference took place in Porto in Tuscany, so very nice city, if you have a chance, go and visit it. Nevertheless, I jumped into my car picked up another guy on away and we went to Porto to attend a very beautiful conference over two days, because they had also live translation for everyone. And lots of good conferences and the party Linux User Group, which was the organizer of the conference, had an office doing any wall city wall of Pato record, sit outside in the evening, play music, have some swings. That's how we started discussing okay, how can we take this any further, happy ones later, at FOSDEM 2008. We found it Postgres Europe got to France Selectric for board of directors. That's when I joined. And then one year later, we had another Postgres conference this time the first European conference also in Porto. Ever since then we are moving around busy Postgres Europe conferences in different countries in Europe. And we also started creating a couple of local conferences. Like, we have the first FOSDEM day. And the first time therefore many customers tend every year, we have PG day, jumping around in Finland, Sweden, Norway, and other Denmark, we have PG day Paris. And Paris, obviously, we have PG day Germany, quite big. And then we also help local user groups, sort of any of the local user group wants to honor conference, we can have some infrastructure, payment systems, this kind of stuff, reservation system call for paper system. That's everything we developed for our own conferences and trade shows for other user groups.

**Matt Yonkovit:**  
Well, and the good news is now that COVID, has died down a bit, a lot of people are starting to travel again. And so we get to go to these conferences in person as opposed to just doing the virtual portions, which I really do you enjoy meeting people in person and getting to know them. Right. I think that's something that I, I always had gravitated towards, and I really missed the last couple of years. I don't know about you.

**Andreas Scherbaum:**  
Oh, absolutely. I missed it sounds good. I missed the holiday trip for conferences, even more than music by himself. So we had Nordic and Paris PG Day, just a couple of weeks ago, we will have Postgres Conference Germany in May, right before Percona Live. I'm basically going to Postgres Germany, and I'm flying to Austin. Postgres Europe in Berlin in October.

**Matt Yonkovit:**  
Yeah, no. And I mean, it's great that we can start to visit and see people do a little bit of travel, get out there and learn what's happening. And I think that one of the things that I always look at conferences for is the ability to learn new things and figure out where users are experiencing some pain. And I don't know if you've gotten an opportunity over the last few months or since conferences started up or even just talking to people in the community. I always like to hear what other people are hearing in terms of what are users asking for and what are their pain points nowadays? What are you seeing in those trends around users? And what kind of problems do they have? 

**Andreas Scherbaum:**  
Oh, well, we talk to users as well. We have preparations for the conferences. We also have local meetups mostly online, still online these days. When we talk to people, we still have our mailing lists slack, and our telegram groups. So we still get good feedback, what do people talk about the other indicator I have for myself is I want this Postgres because Person of the week interview and one of the questions I have is what is your personal pain point in Postgres? And the answers for this are quite different.

**Matt Yonkovit:**  
What's the most interesting answer or the one that made you scratch your head? When you have someone answer that question?

**Andreas Scherbaum:**  
Most answers I get to discussions are actually about vacuum and Postgres.

**Matt Yonkovit:**  
Yes, yes. That tends to be a universal complaint, right? 

**Andreas Scherbaum:**  
Yes! This is the pain point. I mean, it got improved over the years, but it's one of the major pain points in Postgres, especially if you want high-traffic databases. If for us and our company, we, we don't struggle with it, because we know how to deal with it. But it's still something you always have to take into account.

**Matt Yonkovit:**  
Yeah, yeah, a lot of companies do weird things, either setting-wise or even turn it off, then they run into the sad wraparound issue, and then they really cry. And I think that there's quite a bit of work and pain around the auto vacuum and the vacuum processes that could be helped

**Andreas Scherbaum:**  
The project of expanding transaction IDs to 64 bits. So maybe this will help to see wraparound offsets get implemented, not so much the consuming disk space because you will say one of the auditor spaces if you disable auto vacuum and don't want a vacuum, but maybe it tips for some pain points.

**Matt Yonkovit:**  
Yeah. And it's weird because depending on the users or the audience, or who's, who's out there that they think of this is a necessary evil. But a lot of them would rather waste the space than have to deal with the performance hit. And I know some companies who do weird things like they'll turn that off, they'll let their database grow, and then they'll say, oh, backups take too. long, so I'm not going to back this up anymore. And I'll just understand that I'll have to go to a replica or, or do something crazy. It's like, why would you ever do that, but their data just keeps on growing and they don't want to deal with it. So I think that that's an issue that we can all kind of commiserate with. One of the things that I've really kind of been tracking and looking at is the impact that the kind of developer-driven database trends have driven, right. So right now we're in this space where cloud-native slash microservices are all the rage in applications, which means everyone wants their own database, right. And so the number of people who have hundreds or 1000s of databases in their data center is just growing exponentially. It's crazy. But the developer's skill set isn't keeping up with the database knowledge. And so they're just looking for easy point and click deployments, which hey, a lot of companies are doing their database as a service or doing these different things to help with the automation of the operations. But it doesn't help them with the design and the architecture of the databases and the applications themselves. And I've noticed that those are generally lingering. And when they hit, it becomes a really significant problem. And when I mean, when I talk about that, I'm talking about data types, I'm talking about schema design, I'm talking about best practices, if they decide to store JSON, they don't quite understand how these things work. And so they just implement and then hope for the best. And a lot of times that causes issues. Have you seen that as well? 

**Andreas Scherbaum:**  
Oh, I've seen that quite a lot. I mean, if you start a small database performance, it's negligible. So you don't really care about it. If you have one data type variable, take a couple of milliseconds later, you don't care. If your database is going and you're talking gigabytes, or even terabytes and table size, then obviously, you have to care because it was a bit slower. And then change exists afterward. It's really, really painful. Not only in Postgres, but it's also painful in every database, if you make this kind of mistake. But yeah, you can do it while you operate a big database, a large database size of 100 gigabytes or more knowing a little bit about a database design you're doing, in my opinion.

**Matt Yonkovit:**  
Yeah. And this is one of the things that I know that you have given a few talks on data types and advanced data types and how to get the most out of them and how to choose the right one. And in fact that Percona Live, you've got a talk coming up on advanced data types. So that's really exciting for people who are looking to get a bit more detail on how they can design those systems, choose the right data types, make use of some of those things are out there like JSON in a more efficient manner. I think that's a really good topic. And I'm really looking forward to seeing that pop up on the schedule.

**Andreas Scherbaum:**  
Yeah, so this talk on datatypes is actually a follow-up to another talk. I have basic data types, in Postgres. I learned the same thing you mentioned that people want to know, a little bit of data type. So there's an integer and varchar, what else is there? What else can I use? That's for many people who don't really are deep into customers; that's where it stops; then we have so many different basic data types in Postgres. So you can use and make good use of it and improve your performance and design. I created a talk out of it became very popular. And then I created another talk on advanced data types out of it, where we talked about things like, okay, how can you use JSON? How can you use arrays? How can you use range types? And also, how can you create your own data type. If you do? Well, a good Postgres, as we do in my company, mine, wherever, you occasionally have to create your own data type to store data more efficiently, faster, better. And that's what we are doing. So Postgres is where he is at extendable, that you can also create your own data type. And that's what I'm showing in this talk.

**Matt Yonkovit:**  
Yeah, I mean, that's a really powerful thing. Because I think from a developer perspective, and again, this is where I separate application developers from DevOps folks. And people who work on back end code, because from a front end or an application developer a lot of times that they're just not they're not seeing the impact if you will. And one of the things that I did, and I'm gonna geek out for a second, and I'll show you maybe you've seen somewhere, have you heard of the Yonk box? Let me ask you, have you heard of the Yonk box? No. Okay, so I'm the Yonk, it's my last name. But so I have this big problem articulating the value of proper design and Postgres functionality to developers. And so we would go to conferences, and we've got Grafana up and our PMM tool up and it's showing like look number of queries, latency, everything else. But developers are just walked by, right? Because they're like, Yeah, whatever database is, we don't care. So I built this, okay. And so what this is, is a controller that controls the database, this actually controls Postgres. So you can't really see, but the buttons do things like they'll execute a backup, they'll do a vacuum-like if you hit the button, it'll do a vacuum. It will change data types on certain columns. So there are these toggle switches. So you can turn it to varchar versus an int, or a big int, or different types of things there. It will also change the workload. So if you want to look at analytics workload versus a write-heavy workload versus just a regular website workload, so I put this giant controller out there. And I've actually got a bigger one. But it's in the mail coming back from Postgres, Postgres Silicon Valley show. But it's so funny because people will like they like buttons. And so they'll be like, oh, so if I hit this button, what will happen? And then all of a sudden, they hit the button, and they see like, the database go down or something, and they're like, What can I do? And then I can tell them the story, right, and you make it a little real to them because it's often hard to get through from a development standpoint. So I really encourage those who are interested to check out the Advanced Data Types talk, or the basic data types, talk at other conferences, because that is so important. And believe me, I know firsthand how that impacts things.

**Andreas Scherbaum:**  
Most talk are on my website, so if you search my blog, I have a link to all of my talks there.

**Matt Yonkovit:**  
Yeah. And one of the other things you mentioned earlier that you do is the Postgres Person of the Week. Right. And so that is really cool. How did that get started?

**Andreas Scherbaum:**  
I've seen it, that it's not originally all my idea. I've seen the Python folks doing an interview regularly. And back in 2019. I've seen this popping up in my Twitter stream. And it was literally in my head. And then we've been over New Year's Eve in Rome, Italy. And I was joined by definitely Magnus, one of my two close, close friends. And we were sitting in a hotter cafe and I was pondering this idea talking with, okay, what can I do for you? And then we came up with the name and cover names back and forth and where we went back from home. And it took me a couple more weeks to figure out all the technical details. I asked a couple of friends. Can I interview you for this? And then that's how it started. And that's going strong for two years now. I have 108 interviews up as of today.

**Matt Yonkovit:**  
Wow. Okay, so just out of curiosity, how does one become the Postgres Person of the Week? Is there a committee?

**Andreas Scherbaum:**  
Yes, no committee, all I have is a list of swear, not some sick names. I actually have a talk about this now. What I learned from interviewing in the Postgres community. It's up at situs Khan as of today, so they have the recording process, if you want to go and check us out, search for situs Khan. Let's talk about this. What I'm doing is everyone I'm interviewing, I also asked, Can you recommend a couple of other people I should interview? Get a long list of like 350 Something names now? And then I slowly go over this list as everyone happy people say no, most people say yes, some people say yes, and don't do anything, that's fine as well. But I always tend to have like five or six interviews next shoe, I can publish. 

**Matt Yonkovit:**  
Excellent. So what did you learn? So you have a talk on it. So you should be able to tell me, what you learned from these interviews? Well, maybe just give me a short answer, like what is a couple of the interesting things you've learned from talking in these many people?

**Andreas Scherbaum:**  
About 60% of people say Postgres instead of PostgreSQL. I should went over all the answers, and I checked, which name people use. Everyone is up and about. Two people say to change the name. But everyone is fine using either Postgres or PostgreSQL. No biggie. And, but a majority actually uses Postgres these days. What's a bit surprised, but why not?

**Matt Yonkovit:**  
If we keep on shortening it, I might just end up being PG.

**Andreas Scherbaum:**  
Because I have a couple of other things you could search for PG on Twitter. I'm sure

**Matt Yonkovit:**  
I'm sure. Like, but yeah, it's I don't know, it's it. It's an interesting data point for sure. Now I am also curious maybe you, you can answer this in your travels. And as you've seen different deployments, you've seen different things. What's what some of the more crazy or interesting deployments or usage of Postgres, that you've seen out there in the ecosystem? 

**Andreas Scherbaum:**  
You see deployments where people don't change any configuration at all and wonder why your backup is failing. You see deployments in the terabytes. So I've seen databases doing like 30 terabyte in Postgres, usually. We plan as a shared nursing distributed database. So we've seen actually databases in a petabyte range, where you just stick more and more legs together, and it's all one big database, and you have to coordinate all of this. But mostly, it's just your go-to database somewhere that isn't a cloud or locally, couple gigabytes of data, a couple 100,000 rows, entry points, have a dozen terabytes. That's what is the majority we see.

**Matt Yonkovit:**  
Okay. Okay. Well, now, I'm going to shift gears just a little bit. And I like to throw some small rapid-fire questions out there. Just to see what, what kind of answers I'll get and sometimes this works well when I've got a couple of people in the room as well, but I'm curious. So, favorite Postgres data type? What's your favorite Postgres data type?

**Andreas Scherbaum:**  
Int, big int. 

**Matt Yonkovit:**  
Any reason why, just because you'd like big numbers, or?

**Andreas Scherbaum:**  
No, because if you choose integer, you more often than not have to change to big int anyway.

**Matt Yonkovit:**  
Oh, okay. Okay. Fair enough. Last book you read?

**Andreas Scherbaum:**  
That's one of the Pendergrast the woman. Its agent novel. Agent, Pendergast,

**Matt Yonkovit:**  
Okay, interesting. And your favorite version of Postgres? What was your favorite release that you have been part of our work done?

**Andreas Scherbaum:**  
It's always the latest one. The latest one? Okay. My latest one, oh, include the minor release? So do your upgrade.

**Matt Yonkovit:**  
Of course, yes. You want to make sure your systems are secure and bug-free as much as possible. Now, do you have a favorite feature or thing that has come out in the last couple of releases, or maybe will be coming out shortly?

**Andreas Scherbaum:**  
So he can replicate sequences at Postgres 15. This was a major pain point that you could not repeat the settings for sequences up to now. And that's changing and pivoting. That will be good. 

**Matt Yonkovit:**  
Yeah, no, definitely. What are the number one tuning parameter people mess up? Or don't get it right?

**Andreas Scherbaum:**  
Shard buffers

 **Matt Yonkovit:**  
Share buffers? Okay.

**Andreas Scherbaum:**  
Okay. Because more often than not, they don't change it. Postgres by default is tuned for small memory usage. So if you just install it with just one fine on any books, you install it, but if you don't tune it, you will see performance penalties, go and change shard buffers.

**Matt Yonkovit:**  
Fair enough. Fair enough. So Andreas, I want to thank you for hanging out with me for a little bit today, chatting with me giving me a little bit about your background talking to me about the Postgres European community and some of the work you're doing there. I do appreciate having this time to sit down and chat with you.

**Andreas Scherbaum:**  
You're welcome. I am looking forward to seeing you in Austin.

**Matt Yonkovit:**  
Yes. And I promise you to ice cream for doing this. I swear. I'll buy you a giant bucket of ice cream. Thank you so much. I appreciate Yes. Okay. Yeah, so those who are listening or watching, go ahead and make sure you like and subscribe to this. We appreciate any feedback you might have. If there are guests you think we should have, please let me know. I would love to talk to anybody in the Postgres MySQL Mongo, open-source. Hey, I'll talk to anybody. I like to just talk to people. That's just me. I'm a talker. So go ahead and recommend those. But we appreciate you hanging out with us today, and we will look forward to seeing you next time.

