---
title: "Learning MySQL Book with Sergey Kuzmichev and Vinicius Grippa - Percona Podcast 51"
description: "Sergey Kuzmichev and Vinicius Grippa wrote this Practical book guide for beginers and advanced users of MySQL"
short_text: "The HOSS Talks FOSS,  a Percona Podcast dedicated to Open Source, databases, and technology, starts the new year 2022 with a special episode to learn and improve knowledge about MySQL. Matt Yonkovit, The Head of Open Source Strategy (HOSS) at Percona, sits down with Vinicius Grippa and Sergey Kuzmichev from Support Engineer Team at Percona to talk about their book Learning MySQL: Get a Handle on Your Data"
date: "2022-01-26"
podbean_link: "https://percona.podbean.com/e/learning-mysql-book-by-sergey-kuzmichev-and-vinicius-grippa-percona-podcast-51/"
youtube_id: "BcQFv5mHZUQ"
speakers:
  - sergey_kuzmichev
  - vinicius_grippa
  - matt_yonkovit
---

## Transcript

**Matt Yonkovit:**  
Hi Everybody, welcome to the first HOSS talks FOSS of the new year. Yes, it is 2022. And what we have today is a very special episode where we're going to be talking to two of Percona's authors and super awesome support engineers. Hey, everybody. Hey, Matt. How's everybody doing today? So today, we've got Vinicius and Sergey. How are you?

**Vinicius Grippa:**  
I'm good. First Happy New Year for you too. And everyone that's watching. It's a pleasure to be here talking with you. 

**Matt Yonkovit:**  
yeah. Great to have you on Vinicius. Sergey, this is not the first video you've been on before.

**Sergey Kuzmichev:**  
It's not, it's really not. So Happy New Year, Matt. Happy New Year, Vinicius. It's nice to be here with you. It's a pleasure talking to you as always.

**Matt Yonkovit:**  
So I wanted to get both Sergey and Vinicius on because they have written this book. And this book is all about learning MySQL. And so if you haven't seen it, let me go ahead. And I will go ahead and I'm going to pull this up. And I'll share the screen. so it is available on Amazon. And it's all about learning MySQL, how to get started and how to do it right and properly. Right. So Vinicius and Sergey, what, what kind of compelled you to write this?

**Vinicius Grippa:**  
I think that the challenge of writing a book and of course, having something that will be left after I retire, like I wrote a book in my life, thinking well of life's achievements. And I was very enthusiastic to write about MySQL, it's something that I love to work with. So I put two passions together.

**Matt Yonkovit:**  
Yeah, and Sergey, your background is more Postgres than MySQL. Right?

**Sergey Kuzmichev:**  
Right. But that actually made it quite even better for me, because when I started writing this book, well, I guess I knew a bit of MySQL already. But some things I had to research and just learn myself. And the learning MySQL here was, from my side, kinda an outline of my path from learning databases to learning First of all, just databases in general, because you can't write a database without some generalities. But also MySQL in particular. Yeah,  with Vinicius, it was just really a bucket list item for me to write a book sometime. It was, I knew it would be a huge project, I guess we will talk about that in a bit. But when that opportunity came, I grabbed onto it. And yeah, I never looked back. It's really, really interesting to me, in general, to be able to take complex, complicated topics, put them into words, and just give them to the audience in a form that is easy to come to consume. That's what I wanted to do. And that's what I like to do.

**Matt Yonkovit:**  
Wonderful. And here's the thing, this is about Learning MySQL, but is it just for beginners? Can someone who's been a MySQL DBA or uses MySQL for years learn something?

**Vinicius Grippa:**  
I think so. The first chapters are focused on the ones that don't know anything about MySQL, such as how do I install for the first time on different operating systems, Linux, Windows, Mac, whatever. Because we know most developers like have their own database locally so they can do some tests, but the middle chapters and forward I think they are focused on the DBA that is already performing tasks, such as backups optimization, tuning queries, tuning the MySQL overall performance, so we think it's a book for everyone that is only MySQL ecosystem.

**Matt Yonkovit:**  
Okay, so it covers the gamut of everything, beginner to a bit more advanced.

**Sergey Kuzmichev:**  
Yeah, I would say that as a correct definition, right. So we start with some really, really, really basic stuff and we also stop with the by we do expect some database knowledge, maybe. But we will also help somebody who has never managed the database who has never worked with a database, I guess. So. A few chapters of this book could be like learning a database with MySQL, learning relational databases. But later on, we go on into my skull specifics for somebody who's already practicing and just wants to, might have to be confident or for somebody who's coming from a different database, maybe, definitely, like the second half of the book is gonna be quite interesting.

**Matt Yonkovit:**  
Now, Sergey, you had mentioned how difficult this was, it was a challenge to write a book. And I've heard and I've seen that it does take a lot of effort and a lot of work. Maybe tell us a little bit about that process for you.

**Sergey Kuzmichev:**  
Yep. So the main challenge, I guess is to have I will, I will talk from my perspective, right, then we will have Vinicius perspective.  How it came for me is, I still remember it was made the first 2020 Right, yep, I'll go to this date. And I just sat down, and I picked the chapter at random. Just so happened that the chapter was a chapter about backups. And I picked a part of the chapter. And I started writing. And that's been fine. It's been great. Like I wrote a part of the chapter on my first go in a few hours. And I was like, on top of the work. And then I realized that what I wrote will not fit into the book, because first of all, I wrote too much. And we didn't realize that just going ahead and writing stuff, without thinking about it, without structure, without ideas of how you want to see it, it's not gonna work. And I started approaching this from the other side, like, maybe a software project, or like anything you got on the stem, like the outlines, I started doing tasks for myself, I met and managed those like small pieces, breaking it down. And really thinking about this not just like I'm sitting and writing but around thinking, I started sitting and thinking, and making it simpler for me, because I knew what I wanted to say. And I just needed to put the words there. It also became an iterative process, because the chapter about the backups, I finished by June. But a year later, when we were closing the book line, and we were finishing, like the last chapter I wrote was about monitoring. And after that one, immediately after, I just went ahead and rewrote, like, 75% of the backup chapter. And I did the same, so a couple of others because these, this process of growing, of understanding how to write and understanding how to put the words out and understanding what is the books about like giving this book, a sort of a theme, and I don't know, vocabulary or like, how we want to how we want this book to look, it evolved. And so by the time I finished writing, I knew that was the experience that I have. I wanted to go back in time and kind of redo parts of it. And that's what I did. We also had help from our reviewers of course.

**Matt Yonkovit:**  
I can imagine. Vinicius, How was it for you? It sounds like Sergey started one way he kind of flipped around and to come back revisit was it a simpler process for you?

**Vinicius Grippa:**  
No, not at all. I've happened that Sergey joined me because alone I realized it would have been impossible to do it. And it was a roller coaster of emotions like the beginning Oh, I, I'm a writer, I will start writing a chapter. I started with chapter number one, which is the installation process. And I thought it was great my chapter and after the first reviewer it was like, thrash, I got very bad feedback. I had to come back and rewrite it like Sergey said I rewrote 90 - 80% of the chapter because it was not good. But when you get out of these, like, Okay,  I'm not too good. I'm not too bad, but they can do each and then it's when I started getting to the base of writing chapters review working with I think the biggest challenge for me was to get along how to write the book and have a look at the audience perspective, like how a reader would work with my books. So that's the main thing in it. I changed it a few times along the way.

**Matt Yonkovit:**  
Is that more of like, you're really gearing this towards you, as you follow the book, you get more advanced, right? So you start off, you're going to sit down, you're going to install so we can go through the install process, then the next step is how do you make sure that it's configured? And how do you design it, the database and then walking through, okay, now it's designed and it's running. So how do you make sure it's backed up and you walk through the different steps that you have to, from installation to kind of conception, and then through that operations process?

**Sergey Kuzmichev:**  
Right, but it's not that linear, but say, because we kick off with the installation, right, we then go into the design. Then we discuss basic primitive types and what you can do in MySQL let's that could be geared towards either somebody who has now never worked with databases before or somebody who's coming from other databases just what they are what is possible in MySQL like why there is like int and then there is a digit parenthesis switch be like surprisingly when I came into MySQL world, why would you have like a light like varchar you have varchar 40 Why do you have in 8? That's kind of that kind of stuff, none would go into more? Gonna continue with the theme that could be helpful for maybe not even a DBA but for developers like, transactions and blocking and then again, we go into more advanced topics but there is how I want people to approach this book? how I kinda like myself to approach technical books is treated not like a novel. It's not a novel. Obviously, we rewrote different chapters. So like, nobody dies in them. There is no plot, there are no plot twists, written the brand, no cliffhangers.

**Matt Yonkovit:**  
There is no plot twist, How can that happen Sergey? Make this like a choose your own adventure, there isn't like a mystery to solve at the end,

**Sergey Kuzmichev:**  
Choose your own adventure is there like you got to decide who you want to be an administrator or developer and you start your path, right. But really how I like to approach technical books and how I guess I saw people approaching this book is to treat it as like, obviously do go ahead and read the chapters that are interesting to you, or just the first chapters, but then probably just try to come back to other chapters, for instance, the chapter on backups, maybe you don't need to configure MySQL backups right now, right. But you can always come back later and open the book. However you have a digitally on paper, and look it up and read it or refresh it. So use it more like a source of information that you can just come back to read the top.

**Matt Yonkovit:**  
Let's ask some technical questions. Right. So we talked a little bit about the process of writing a book. and I think that that's good context. Because some people do want that, that's one of their goals. Vinicius, you said you wanted this as something for your long-term kind of career, you can look back, and you can say I accomplished it, I wrote a book I published. But for those who are reading the book, for those who are getting involved in MySQL, I think that a couple of questions come up. Number one, there are so many options. Why should people choose MySQL to begin with? Right? So if you've got all these options, you're a developer, you're starting out? Why choose MySQL?

**Vinicius Grippa:**  
Okay. I would say to myself why I chose to work with MySQL, at first. It's one of the most popular open source databases. So when I was starting my career, I didn't have a plate of options to work with like Oracle, SQL Server, whatever. So the market was bigger for MySQL, that was my first decision. And nowadays, MySQL is still the database that has been most used by developers. If we look at the DB ranking, it's the first one open source by a fire merging from the second one. So I think that's the point like for someone that is starting his career, his or her career is thinking about, like, how can I insert myself in the markets in the future, like in the book, I think was focused. I try to do these in the book. Okay, now,

**Matt Yonkovit:**  
Sergey, why would you suggest people start with MySQL?

**Sergey Kuzmichev:**  
First of all, why not? Second, my perspective was kind of channeling my experience that some people do stumble into technologists accidentally. Right? It does happen, you enter, you enter the workforce, you enter the auto industry, you get a job, maybe you are a developer, maybe you are, might an eye on IT administrator or something, and there is a database and you start using it is it just happens to be MySQL, maybe we're PostgreSQL. Or an Oracle? Like I, to be honest, I almost accidentally became who I am right now because I decided to go become an Oracle DBA, almost by accident. And it could have happened any other way. But yeah, a lot of people, I think, do not go and just think like which database I want to learn. First of all, universities usually provide courses that are based on brown, specific databases, right sometimes, and then you go, you get your first job. And that job might already have some infrastructure, some databases. And what I wanted to give on this book is like, okay, it made it doesn't give you an answer of why would you pick MySQL but if MySQL is what is there, or what speak what you decided to use, then here is how you will use it, how here is what it can do for you.

**Matt Yonkovit:**  
Yeah, Target, that's a very good point that you make in combining any of what you said, and Sergey MySQL does have a large amount of popularity, there are a lot of third-party applications that have chosen it as their basis for their database, right. So if you install Drupal WordPress you have certain options you can use, but typically, it is geared towards MySQL, or in many cases, MariaDB. And it becomes popular because it is kind of that de facto standard. And because it does have a wide install base, a lot of times when you're starting a new job, maybe you're coming out of university, it might be a database, that is the first database you get your hands on. And so it's oftentimes not just about choosing, it's about what has chosen you based on the technology and the applications. So let's assume that you have this MySQL database, you're starting out, you're getting started. What's the number one thing that people start out with, mess up? What's the one thing that they kind of like, forget, like, if you could point them to any one of the chapters in the book and say, You really need to read this one, or you really need to do this, which one would you say is the most powerful?

**Vinicius Grippa:**  
I would divide it into two categories, the ones that are not MySQL. So I would say chapter one, I saw people struggling a lot with wrong RPM packages, or I'm trying to install a Debian package all Centos because I don't know Linux. So these kinds of basic mistakes at the Linux level, I would say start with Chapter One. For those who already have certain experiences that they are trying to take, the next step is all about, like Sergey wrote a great chapter about monitoring backups. These are the things that when your database is in production, you need to worry about because things are good when they are running well. But when they go down, it's when the DBA needs to shine in. I think these are two important chapters.

**Matt Yonkovit:**  
Okay! Sergey. What about you? What's that one thing that you think people should pay attention to like the number one mistake that folks make when they are starting out?

**Sergey Kuzmichev:**  
I guess I would like to break it up into two pieces, again, for folks who are starting up designing a database, right? Or thinking about how to evolve their schema or how to write an efficient schema, then maybe look at the first half of our book. Right? So this will definitely give you an overview on best practices and how to better approach MySQL, how to better work as MySQL, how to understand types, and which ones to pick and what will not. So I'm properly designing schemas over-index databases and all that stuff. But guess what talks about that sometimes? All right, it was easy math. But yeah, it's a common thing, it's a common thing. But if, for instance, you stumbled upon a database that already has a schema and it's already populated. already running, then the one thing that you probably should try to pay attention to is yeah, a second here, we try to look at how to monitor your database and understand that it's fine. Yeah, backing up and making sure that it's restorable is also a really, really good side of things. It's quite far in the book, to be honest, right? Because you have to build up to it. There is so much involved just if we start structuring our book, by getting out the things that are most important we will do will be installation, backing up and monitoring, I guess, would be the first three chapters, and everything else would be like, next one's been more than stuff. But really, you have to put up knowledge on top of the other knowledge. So do definitely look at monitoring to definitely look at backups and recovery, because that will eventually bite you, as any database will crash. On an infinite timescale, any database will corrupt and you will lose the data there unless you have backups. And any database will also get stuck about performance. So that is really important. But I would really also recommend just assessing and trying to understand where you are with understanding MySQL? I'm not picking up anything in particular, but am trying to do a holistic approach. Just if you're reading the backup chapter, and there is something there that is unclear. Maybe in other chapters, we will help you understand that. Right. So perhaps the results are a good chapter and looking at transactions. And you probably should read that before understanding parts of the monitoring chapter because the monitoring chapter builds up on that because you can't understand parts of what are we looking at within MySQL if you don't know how it locks things? Right?

**Matt Yonkovit:**  
So I was looking at the chapters, and I noticed that you all had included a chapter on optimizing your database costs in the cloud. Why? Why does that seem like an unusual one for a book on MySQL. So I'm curious, what have you seen in that space? And kind of maybe gives us an overview of why that's important.

**Vinicius Grippa:**  
Sergey, we will for sure he has histories about this. But through fees met like it's really common. Like we know that everything the cloud costs money, disk, memory, CPU, whatever, so you need to use it wisely. And as Sergey highlighted, like, if you're really bad optimized queries, you are using a lot of your disk, a lot of your memory, maybe you need to oversize your server because the current instance is not capable of running what I need, because it's everything's around is running, not optimized. So you're wasting dollars with bigger instances to hold to process your data where you could do it better in saving money, like and I think that's the main idea. And based on support cases, these are very frequent, like oversized, and optimize it and all this kind of stuff.

**Matt Yonkovit:**  
Yeah, and, Sergey, what about from your perspective? I mean, do you echo the same?

**Sergey Kuzmichev:**  
Yeah, absolutely. Secondly, and also, I'm guilty as anybody using clouds of just pouring money into the fire, like you have something running slow. You can just pick a larger instance, you can add some, it's cloud, it's elastic, right? So, but you kind of have to understand that everything has its costs, and you don't always need to pay that much. Or maybe you did, but how do you understand it's, it's not about that you don't need to pay there is no magic there. This will allow you not to pay for everything like I am a big proponent of clouds. I like cloud environments, like the elasticity, I like the freedom they give you, the ease of use, but they also come with costs, which sometimes come like more than you expect that we need to understand.

**Matt Yonkovit:**  
Yeah, and it's interesting. I think that from a cloud perspective, this is where I'm interested in the people who are reading and using the book. The topics you cover are relevant whether you're running in the cloud or outside the cloud, and I think that one of the things that I have seen is from people deploying in the cloud, a lot of times they feel like backups are covered by availability. If you need optimization, you just add more resources. If there's this comfort level that you've outsourced to the cloud, when in fact, I don't think that's really the case, there still needs to be that design of your database, ensuring that the backups and the restoration is possible. And what's going on! How do you optimize your systems, how do you configure it properly? I think that's often overlooked.

**Sergey Kuzmichev:**  
Yeah, I think fundamentally, even if you're, even if we're talking about databases as a service environment, where the backups are automated and they are given the kind of under the hood, at the end of the day, it is your data and your responsibility. So understanding, for instance, that you should probably try to restore them every once in a while, it's a good thing. Because like, what will happen if the backups if the backup that you really need is not restorable, or you don't know how to approach and the worst thing that happens with so many abstractions built on top of other abstractions is that eventually, there will come a day when the abstractions will leak, when you will have to understand why your MySQL is stuck, right? So somebody opened the terminal, which is connected to your database as a service, which has auto-tuning, which has everything this amazing technology, I'm really, really like, not, not criticizing here, but there are things that happen, such as you just open a terminal, you connect to a database, and you lock everything up, just you ran a command, maybe you wanted to run it in your database, like a development environment. And now there is a production that is locked, and there is no processing out there. But from the cloud perspective, it's perfect, there is no load, there is no nothing, nothing is going wrong. So you have to be prepared for that. So not everything can be automated, not everything can be made. Superfast. So, at the end of the day, I am a firm believer that eventually you will face any issue that will require you to step in and understand what is going on inside. And the more we go. And the more our industry, I think goes towards automation. Building abstractions, which are good at going by that without criticizing them, are better. It's going to be for an expert for somebody working with the technology to understand what is going on inside of it. Because when Yeah, when bad things happen, somebody will have to step in and resolve them.

**Matt Yonkovit:**  
Awesome. So for those who are watching, and you are interested in a copy of Vinicius and Sergey's book, what we're going to do is as soon as we hit 100 likes or 100 comments in the YouTube video, we're going to go ahead and give away two copies randomly selected from those who post a comment. So go ahead, post a comment. If you're interested in getting a free copy of the book. We appreciate you subscribing and liking the video. And so Vinicius and Sergey, last question for you too. What are you writing next?

**Vinicius Grippa:**  
For now, I will be on vacation Matt, writing books, but I don't know.

**Matt Yonkovit:**  
Come on. We can like a MySQL mystery. Or a MongoDB we could do like the database superhero. It could be like a comic yet.

**Vinicius Grippa:**  
Oh, there is not an offer. But there are some Easter eggs there. These are some names of engineers in some of the chapters. So I think to us, kind of a way of thanking those who taught me along the way like for example, Marcos, Guli like there are names there that already stood eggs about I think it's nice, but who knows next. I would like personally to write something above learning MySQL. Maybe a high performance to MySQL or something like these, because these will help me to leverage my knowledge so closely.

**Matt Yonkovit:**  
Awesome! Sergey, anything you've got on your plate to write?

**Sergey Kuzmichev:**  
To be honest no! I now have a kid. So maybe I'm gonna write a children's book, who knows? Honestly.

**Matt Yonkovit:**  
Let's write a database book for children

**Sergey Kuzmichev:**  
Like we can turn Learning MySQL and a common book and be a SQL for toddlers. Right exactly like you got to be prepared like in the more in our industry right now. There's so much stuff to know and learn like it's, it's amazingly difficult. So you got to start like one year old. It's already too old. Today, I'm sorry. But jokes aside, nothing to be honest are, it's actually, it's not. I wouldn't say that I don't want to write anything anymore. But it definitely takes you some time to decompress. Because just the sheer amount of time you invest into doing this project, like, it took us more than a year to finish it. And that took us, me personally, it took a lot of weekends away, and you leave constantly for more than a year and leave with this fault in your head that whenever you have time, you probably should write a book or you should be kind of always mindful of allocating time for that and thinking about it. It's like it leaves with you. It is always there. And just having this freedom is Saturday. And guess what, I will do nothing like I will, maybe I will read a book that somebody else wrote. So this is really exhilarating.

**Matt Yonkovit:**  
You're gonna read that's quite a lot now, right?

**Sergey Kuzmichev:**  
But the whole process is really, really interesting and challenging and rewarding. And then I for sure will keep my eyes open on something. And maybe I will eventually write about, I don't know, maybe cloud and how to do databases in the cloud properly. That could be something to do.

**Matt Yonkovit:**  
Indeed, indeed. So if you haven't checked out the book, it's available on Amazon. It's available on other bookstores, I would encourage you to grab a copy, whether it's Kindle or not. And again, if you'd like a free copy, go ahead. And subscribe, like this video, and drop a comment down below. Sergey and Vinicius. I appreciate you hanging out. Thank you as always, and we will see you in another episode. 

**Vinicius Grippa:**  
For sure. Matt, thanks a lot for being here. 

**Sergey Kuzmichev:**  
Thank you, Matt.

**Vinicius Grippa:**  
Bye Bye.

