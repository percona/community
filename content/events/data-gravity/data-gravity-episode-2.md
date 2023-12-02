---
title: "Data Gravity Episode 2 - Sonia Valeja and David Gonzalez - PostgreSQL for Jobseekers Book"
description: "Joe Brockmeier talks to Percona's Sonia Valeja and David Gonzalez, about their recent book PostgreSQL for Jobseekers."
images:
  - events/data-gravity/Data-Gravity-Episode-2.jpg
draft: false
date: "2023-11-15"
speakers:
  - sonia_valeja
  - david_gonzalez
  - joe_brockmeier
tags: ['Data Gravity', 'Podcast']
---

In this [episode](https://datagravity.podbean.com/e/data-gravity-episode-2-postgresql-for-jobseekers/), Joe Brockmeier talks to Percona's Sonia Valeja and David Gonzalez, about their recent book PostgreSQL for Jobseekers. They talk about the inspiration for the book, why they focus on jobseekers, and what's covered in the title.

[Episode 2 Page](https://datagravity.podbean.com/e/data-gravity-episode-2-postgresql-for-jobseekers/)

<iframe title="Data Gravity Episode 2: PostgreSQL for Jobseekers" allowtransparency="true" height="150" width="100%" style="border: none; min-width: min(100%, 430px);height:150px;" scrolling="no" data-name="pb-iframe-player" src="https://www.podbean.com/player-v2/?i=tfi7a-14ceb7f-pb&from=pb6admin&pbad=0&share=1&download=1&rtl=0&fonts=Arial&skin=1&font-color=auto&logo_link=episode_page&btn-skin=7" loading="lazy"></iframe>

[All Data Gravity Podcast Episodes](/events/data-gravity/)

**Joe Brockmeier:**  
Good afternoon. Good evening. Good morning, whatever time it happens to be for you. This is Joe Brockmeier, Head of Community at Percona. And you're listening to Data Gravity. Today, I'm going to be talking to a couple of folks that I happen to work with at Percona. David and Sonia, let them introduce themselves in a minute. They have written a really excellent book for people who are looking for jobs related to Postgres. And we'll dive into that a little bit more. But first, I'm gonna start with Sonia and ask you to introduce yourself to the people at home.

**Sonia Valeja:**  
Thank you, Joe. So, as Joe mentioned, my name is Sonia Valeja. I'm working in Percona. Since last 1.5 years. I am a part of managed services and managed services in Percona as opposed to SQL DBA. And I am playing around PostgreSQL database, breathing PostgreSQL database since last 10 years.

**Joe Brockmeier:**  
All right, David, let's kick it over to you.

**David Gonzalez:**  
Hey, how are you? Hi, everybody. My name is David Gonzalez. I'm Mexican DBA, obviously, based here in Mexico, and I've been around in Percona, since two years and seven months or something like that, and I've been working has PostgreSQL DBA in the minor services area, the same as Sonia. Currently, I'm filling the position of tier two. So handling some escalations and some planning for the customers and stuff like that. And yeah, working with Postgres since almost nine years, something like that. So happy to be here. Thank you.

**Joe Brockmeier:**  
All right. Thanks for joining me. So let's talk a little bit about this. This is a unusual angle, although unfortunately, it looks very topical at the moment with so many people looking for work. Why approach Postgres from the angle of jobseekers.

**David Gonzalez:**  
Yeah, the book is called PostgreSQL for Jobseekers. In fact, I have a copy right here. And yeah, this is the book that Sonia and myself wrote. So we decided to abort those topics that we are filling in this book, because we think that Postgres is a very, very powerful tool that can be used in a wide variety of projects out there in the IT community. So we really believe that the information that we are trying to give here is useful for those people trying to find their first job position in Postgres. We are trying to explain the different topics of Postgres since the installation up to more advanced administration topics. So yeah, that is what I have to say for this. So yeah. Go for it.

**Sonia Valeja:**  
So as David mentioned, we have tried to cover starting from installation to advance administration of Postgres SQL, along with whatever he said, I would like to add one more point over here is still as per stack overflow survey, Postgres SQL today is used as one of the top five databases in the industry. And it is one of the most used open source our DBMS we have today in a market. So and there are a lot of people who want to reduce their cost by reducing the usage of licensed products. So PostgreSQL is a great fit wherever people are seeking for RDBMS in open source. 

**Joe Brockmeier:**  
I think one of the things that people really look at from Postgres, though, not just the cost savings, but also I like to say that open source is free as in kitten, because there's no license fee, but still managing a database, you still have lots of costs that are associated with the care and upkeep of such a thing, but I think really the thing that companies are looking for from Postgres is control of their data use. Do you see that?

**David Gonzalez:**  
Yeah, absolutely. Absolutely. So you can design multiple and different ways to handle your data. You can go for the most simple problem If we needed to have a table for a single web application, for example, to the most advanced and enterprise tier solution with Postgres, you can take the control of the data and avoid the login, for example, when working with the exclusive cloud vendors, so you can decide where you put your data, how you handle your data, and how to implement the solution. So the flexibility that the Postgres core has, and the multiple functions that you can add, with the prophetical solutions that we have from the community, such as extensions, or external tools that can provide enhancements to the core functions of Postgres makes the possibility or opens the door to design the solutions in a very imaginative way. So, yeah, definitely, Postgres is an option, if you can handle the data the way that you want. 

**Joe Brockmeier:**  
What do you think about the whole data freedom versus costs thing? 

**Sonia Valeja:**  
With Postgres cost is one of the important aspects, when, when people are looking for the database or any IT solution with respect to their businesses, when they run their businesses. So, after COVID people have understood the importance of money, that is one of the major thing which PostgreSQL is, you know, helping over there, not only the cost at the same time, it is having a vibrant community, it the development is going on since last 20 plus years, so almost more than two tickets. And with this vibrant community, the product has become too stable, like PostgreSQL database as itself has become too stable. So be it a smaller application beat a bigger application or beat whatever kind of financial crash, critical applications also today prefer to use PostgreSQL as their back end database. So even I have heard like, there are some testimonies where NASA is also using PostgreSQL database for some of their applications. And this is not the only factor where cost is, you know, justifying. It's the stability also, which this database has, it justifies itself in the market.

**Joe Brockmeier:**  
Alright, let's talk a little bit about the angle for jobseekers. So is there anything that you've covered differently? Because you're aiming at jobseekers versus somebody who's already in the workplace working with MySQL? There is a different angle to the book that you'd like to talk about, like what would I learn differently from this book than another say intro to Postgres book.

**Sonia Valeja:**  
Still, so, along with the like, we have covered the basic topics, which a jobseeker would be looking for, when he or she is finding a job in the market. So, those basic concepts are explained in a very easy to understand language, like the way I am speaking, when you will read the book, you will feel as if somebody is speaking to you, that is one aspect wherein you know, it attracts the jobseekers. At the same time, we have also covered few advanced topics, which are very much useful for DBAs in their day-to-day work. So beta replication, beta backups and restores are also one of the important chapters, which we have covered over here is how a person can build their online presence by contributing them contributing some part of their work in the community in the post to sequel community. So this makes the book a bit different from any other documentation or any other work, which you will be reading. Great, yeah.

**Joe Brockmeier:**  
David, any other thoughts on that? 

**David Gonzalez:**  
Yeah. Something that I want to add here is that just has Sony explained, we try to cover the topics on the blog in a very simplified language that you could understand even if you're not familiar with Postgres or database technologies, properly speaking, what also we work in both on the topics and take the reader in the easiest way when the easiest path to find around the design of the solutions, because if you're new in the Postgres war, or working with In databases, you can feel overwhelmed with the amount of information that is over there, you might try to figure out how to use solution should look like. But you go to internet and try to find something specific for, I don't know, high availability, or what is the best, which is the best backup solution for Postgres. So you might encounter that you have a variety of solutions, or number of manuals and tutorials about how you should put the things and in their fields, in a fierce encounter with the technology, you might have faced that you are overwhelmed with the information. So the idea in this book is to put all those topics in a path that you can follow and understand comparing some of the solutions, you can make a decision while reading the book. And imagine how you can implement that in your own environment. So that is all the aspects that you can find in the book.

**Joe Brockmeier:**  
All right. Let's take a step back for a second here. So you both mentioned a fairly long career with Postgres. Was that your first database? Or did you start out like Sonya, did you start with SQL Server or something like that? Or how did you get, how do you get your toes wet with DBA work in the beginning?

**Sonia Valeja:**  
So initially, there was a project, which was given to my company where I was working, was to migrate from Oracle to Postgres SQL. And in that point in time, I'm talking about the year 2012. In that point in time, people were breeding Oracle, like anything. And in my company, there were no worry in my team was ready to work on something else. But Oracle, and I was a fresher that point in time. And I was like, finding a work in database, whatever you give me, but you give me database. That was the thing, which I was in the need when I was searching for a project in my company. And then they told me, okay, you perform this POC from Oracle to Postgres SQL. And if this POC goes, well, you can work in database, but database will be your first choice. And I was like, Yes, I'm ready to do this. As long as it is database, I'm ready to go ahead. And with that process, in fact, I started working as opposed to SQL DBA. And later on, over the course of time, I learned Oracle, because there were a lot of migrations, which I did in my initial days of my career. So with that, I learned how Oracle works, because if I don't understand how it works, I will not be able to migrate it properly from pillar to post to secret. So PostgreSQL was the first database in my career. 

**Joe Brockmeier:**  
All right, David, how about you?

**David Gonzalez:**  
Yeah, maybe the initial steps in the databases were kind of similar has experienced with Sonia, because I fell in love with databases during my college studies. So I stopped practicing databases with Microsoft SQL Server was the first thing that I started looking at when databases come to my life. And I really felt that that is the path that I want to follow, I really enjoy the angle of the solutions, their way of thinking that you need to put in, in play some sort of solution for an application from the perspective of the backend. And when I had the chance to start working with databases in the real world was has Oracle DBA, I started working with Oracle, and I stick to that technology for over five years, almost. So I started as a junior DBA. And I was acquiring some knowledge and experience working in at least two different companies. One was our data center and the other one was a bank. And both of them have the core of the services running on Oracle. So I got a lot of exposure of Oracle and I think I learned a lot of the mindset for the debit DBA working as an Oracle DBA but other time during my study in the bank. Some braids start rising up about to migrate from Oracle to Postgres for a start development, developing new application and features now imposes the idea or the main purpose of that was to reduce costs, but surprisingly, nobody wants to touch Postgres, all the Oracle DBAs were very reserved on that technique. And that is my thing. So I was the one that raised the hand, and hey, I can do it, and I want to do it. And immediately I found out that Postgres is a beautiful technology, I really like it, I found the similarities between Oracle and Postgres. And I started working with very happy, and I was very happy doing it. So I moved to my next company. And from that, my first technology for work was Postgres. And since now is the thing that I like to do.

**Joe Brockmeier:**  
I've noticed in my career there are kind of two kinds of people, there are the people who learn a technology and want to ride that out the rest of their career. And then there are people who are just, you know, goblins, they're just like, give me whatever you've got, I'll learn it, I'll, I'll figure it out. And that often, I've noticed, corresponds really well with open source. The people who are just, you know, eager to learn and eager to adapt, often thrive with open source, and you need that attitude to thrive with open source, because it's always evolving and changing. So we're getting close to the end of our time. Is there anything that you want to add that I haven't asked, always the least ask people? Okay, what haven't I asked you, that you wish that I had asked? And I'll start with David?

**David Gonzalez:**  
Yeah, probably something that I might add for the conversation is, if I learned something new, while working in this book, because definitely, I did. So probably that question could add something to the content. What do you think?

**Joe Brockmeier:**  
Okay, so you have you learned some new things while writing, while in the process of writing the book?

**David Gonzalez:**  
Yeah, definitely. Because, well, even when I have been working with authors for almost 10 years, nine and a half years, something like that, I really have working with what the projects have, you know, for example, you receive a project with a customer. And the idea is to bring the application to the best performance, or to improve that deployment in the best way. So usually, you have that those boundaries in between, you have to move, right. But usually you don't look, there are all the range of possibilities that you have. And the possible suffered. And while working in the book, for example, I write about a topic related with extent studies, the extended statistics, that is something that is there, that is something that is very powerful. And usually you don't see that in the real world, because they know probably, you need a very deep understanding of your project of your data, know how is related within the different tables and objects, and how to you can exploit that to bring a benefit to the service. So what's very interesting to got that topic and perform some laboratories in order to understand the capacities of that feature that Postgres has, and obviously, bring that to the content of the book. So was something that I really enjoyed doing something that was new, kind of, because I knew that that thing exists, but I haven't used it before. So yeah, it was a really nice experience. And I hope you can enjoy reading that in the book.

**Joe Brockmeier:**  
Alright, Sonia, bring us home.

**Sonia Valeja:**  
Yeah, yeah. Likewise, David said, whatever it was, most of the time I was researching 70% of my efforts are in the research. Even though I've worked for almost a decade in Postgres sequel, I was breathing posters equal, but still, I have a lot of I've done a lot of testing creation of the environments and stuff like that possibilities, which I mean, and it has a gist of the overall experience, which David and me combined. I mean, if you combined it, it is more than two decades, if you say so. So, all the experiences which we had with our customers, we are, I mean, we have refined it, drilled down and simplified it in a manner that you know, a person if starts working after reading this book, we'll be able to relate it very nicely.

**Joe Brockmeier:**  
All right. I'd like to thank both of you for being on the show. And I would like to encourage folks if you're listening, whether you're actually out looking for a job, take a look at the book. I think you will learn quite a bit. And I want to thank David and Sonya one more time for being on the show. And I want to thank everybody for listening. Thanks a lot and have a great time.

**Sonia Valeja:**  
Thank you.

