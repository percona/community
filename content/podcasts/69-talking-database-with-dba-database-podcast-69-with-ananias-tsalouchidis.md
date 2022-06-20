---
title: "Talking database with DBA - Percona Database Podcast 69 with Ananias Tsalouchidis"
description: "Learn how Ananias started in opensource database, most common problems and challenges that the managed service Team has to fix and more about DBAs"
short_text: "The HOSS Talks FOSS is a Percona video podcast dedicated to open-source databases. Matt Yonkovit, Head of Open Source Strategy at Percona - The HOSS -, sat down with Ananias Tsalouchidis, Principal DBA at Percona. Ananias is one of the most famous Percona bloggers with his post “When Should I Use Amazon Aurora and When Should I use RDS MySQL?”.  In addition to this blog post, learn how he started in opensource database, most common problems and challenges that the managed service Team has to fix and tackle the relationship between developers and DBAs. As usual in this Podcast, Matt asked random database and nondatabase questions as well. In case you missed it, Ananias brought a session about “Build a Powerful Alerting Platform by Integrating Alertmanager With PMM” at Percona Live 2022"
date: "2022-05-26"
podbean_link: "https://percona.podbean.com/e/talking-database-with-dba-database-podcast-69-with-ananias-tsalouchidis/"
youtube_id: "dmp-6mLORJA"
speakers:
  - matt_yonkovit
  - ananias_tsalouchidis
---

## Transcript

**Matt Yonkovit**  
Hello, everybody. Welcome to another HOSS Talks FOSS. I'm the HOSS Matt Yonkovit, Head of Open Source Strategy here at Percona. And today I am joined by a fellow Perconian. He's actually famous and he doesn't even know that he's famous. He doesn't know that I'm going to do this. He's just looking at the screen now in complete shock. Ananias is here today! And if you don't know, and he has, he actually has, and did you know this? Maybe you didn't? Maybe you did? The most popular blog in the Percona blog history. Did you know that? No, you didn't know that.

**Ananias Tsalouchidis**  
Me?

**Matt Yonkovit**  
You are internet famous! It's the most popular blog in the history of Percona. And we have the author here. So if you're not sure what I'm referring to, there is a blog that Ananias wrote that is when should I use Amazon Aurora and when should I use RDS MySQL? Oh, my it is the most popular blog that we have had on our blog. For years and years, every month, it gets great traction, because it's a question people want to know the answer to. So what better way to celebrate the upcoming Percona Live than to invite our own superstar to the podcast.

**Ananias Tsalouchidis**  
Thank you. Thank you.

**Matt Yonkovit**  
No problem. Now that I've thoroughly embarrassed Ananias how are you? How are you doing?

**Ananias Tsalouchidis**  
I'm doing great. Thanks for asking. And yeah, thanks for inviting me to this podcast

**Matt Yonkovit**  
Yes. So, Ananias, you are in the managed service team, you have been in the database world for some time now. Maybe tell us how you got started in the database space. And tell us a little bit about your career in why databases interested you in the first place?

**Ananias Tsalouchidis**  
Yeah, that's a great question and a long story.

**Matt Yonkovit**  
Well, we got two-three hours, we're good.

**Ananias Tsalouchidis**  
I think it's not enough. But I've tried to make that short. Okay, so this journey started many, many years ago. When I was a kid, I liked all these people with a computer during these times. And okay, that looks like something interesting. And then I decided to study computer science. But until then, I didn't have much experience with programming and the Linux world or databases and all this stuff. And I told myself, Hey, man, that's not possible. You're studying computer science. So you need to find something interesting to see what are the trends to see if you like that. And that's how it started. I started volunteering, managing some learning on my own about Linux. And then I started volunteering as a sysadmin for some projects, and then I got my first working experience, I believe so many people, it started as a developer, then it became a bit of DevOps. And then as a DevOps, I had to get involved in administrative tasks and databases, websites, and all of this. And this is when MySQL made me tell myself, okay, this is where you want to go. That's really interesting. This is challenging. So I was involved in a few projects. And then we started. This is how my career in the MySQL industry started. I then started gaining experience. Similar to many other faults, the MySQL performance blog was one reference, a great reference where I could find very interesting material benchmarks or ideas, all these crazy stuff that the blog hosts until today, and then I went to a few companies. I was involved in some national IT projects. And then anyways, almost five years ago, I joined Percona and I'm super excited for this opportunity.

**Matt Yonkovit**  
Awesome. Now, as part of the managed service team, your responsibility is to manage the team's responsibility, not you specifically, although you're part of that is to manage these complex environments for customers. So you are effectively their database experts. And we've got the sizes of environments from smaller to very large and large scale. And so we see all kinds of variety of issues and problems on a regular basis. So I always like to ask people this question, what do they see when they are managing lots of databases as a common issue? That they wish that the teams that are the developers or the customers are working with? Do they wish they would understand this or make a change? What kind of common problems occurs over and over again?

**Ananias Tsalouchidis**  
There are so many. Let's start, from the point where I can tell you that it is always the database queries doing something Croc, this is the most common Oh, no. So this is not working well. Okay, let's check the database, oh, our latency went high. Let's check the database and why this can't be fixed. And so that's one problem. And that's a, let's say, big problem. Because we know to understand what are the capabilities and the limits of the database, let's say not only MySQL, whatever it is, and how we should align our application and best practices with the database, and combine them together, implement the required changes so that everything runs smoothly. So that's one of the problems.

**Matt Yonkovit**  
You have to almost be a defensive DBA. Because you are blamed quite frequently anytime there is that slowdown or outage or anything, it's like, oh, it's gotta be databases, you start there, and you almost have to prove so it's almost guilty until proven innocent.

**Ananias Tsalouchidis**  
I won't say that. It's not guilty. Because yes, it's the database. It has a slowness. It's the database that is underperforming. It's the database that has an issue. But let's go, we have two options here, either fix the problem. That is priority number one, because this may be affecting from 10s to 1000s, of users and users. And there are other implications as well, such as business impact, and all this stuff. So you need to find a quick workaround and talk as fast as possible, without introducing risks are just jobs and take the best decision based on the situation that you are, in and what resources you have available. And whether the developers can help or you can do something on the database side. And then that is, what's a priority two, we have to work on this issue and figure out why this happened. And if my scalp was performing slow, was that because that was misconfigured was that because we've hit let's say bug or error case, or that was that we are adding too much pressure to the database. And we could reduce that pressure by doing some minor changes to the application or to our schema because we don't have an index. So our CPU gets saturated, and this is causing a domino effect, then there is a slowness, there are some requests that accumulate on the application side, and then all these requests go to the database again. So that's a really challenging environment. Because it's managed services. And that means you have full hands-on access to the customer environment. You get involved in numerous implementations and customers may have totally different setups for either the MySQL product itself, either MariaDB, Percona, Server, or MySQL. High availability, the infrastructure across cloud providers on-prem, different needs tap so the stuff that's a crazy one but believe me, that's the magic. That's the silence. That's the interesting part. Because you never get bored. You always have a challenge to, let's say to, to fix an issue to do coaching and mentoring because this is also part of the coaching and mentoring because when a company or a customer or a partner would say because I like calling partners because we work together for the best result, someone may be used to working on the same model for many years. So when they come to us, we may introduce saying this data that customers may not feel really convenient with or it that's something new, we can't easily implement this. And this is where the why starts. Because every time we have to find a better way. Okay, we understand that you were doing something in a way, x. Now let's see if this can be improved and do that another way. Because this way, you are going to have a more stable environment, you're going to have a more stable database, you're going to have a more performant database. You're going to save working cows, and human resources on your side. And all this stuff.  I can speak for hours. But I believe, I think I've given you

**Matt Yonkovit**  
No, no, no, I mean, there's Yeah, there is a lot to unpack there, right? Because I think that when you talk with users, you talk with customers, everybody's different. And I think this is part of the challenge of working for, even if you're working for a cloud provider if you're working for a service provider, you have so many distinct workloads, and you have potentially so many different variables that you have to troubleshoot and work within, and the skill levels of the users, the developers, the folks on the project teams, they vary greatly. Some developers are  I've been doing this for 20 years. Other ones, Hey, I just got out of college, hey, is my first app, I don't know what I'm doing.  I've never worked with a database before. And so you have that variety and the education portion of educating end-users are often overlooked. And I like to talk about this in a lot of my talks where a lot of developers don't think databases are cool. And so they ignore them. And they don't understand the internals. So they just use them as a black box, they throw all their data in, and they just kind of trust that it'll happen. And then when it doesn't work, right, they don't know what to do.

**Ananias Tsalouchidis**  
Yeah, that was my approach, because you've asked for, let's say, the most common problems, but I have to be honest with you. Sometimes it's a pleasure to work with customers, experience administrators, and developers, and all of these have their own contributions. And you may get different ideas and approaches that you could even think of so that's nice.

**Matt Yonkovit**  
And I mean, this is one of the great things, not only about working at Percona. But in the open-source space in general is being able to pull ideas from different sources and hear the different folks in the community or across different companies, what's worked, what hasn't worked, right. And I think that that is something that is often not appreciated as much as it should be. Because if you know that this caused issues in this other environment, or this, this type of approach isn't 100%. Right. And you have experience in it, that becomes really, really valuable. And I think that really helps people get better over time. And it helps the customers get better over time as well. Yeah. Yeah. So so I mentioned you had some blogs out there, the most popular blog ever. And so I was hoping maybe you could tell us like so. So the blog is hey, when should you use RDS versus Aurora. And we could probably even throw EC two out there as well, in your experience, because we support customers in all the different cloud providers across all the different databases of service. When Should people start to look at some of the more advanced features whether it's Aurora or maybe other databases of service providers?

**Ananias Tsalouchidis**  
Ah, yeah, that's a huge topic. 
I'm pretty sure you know that that's a trade-off. Okay. You, you, you get some benefits, there is something else that you may be losing. So there's no unique answer. Because that's a combination of, let's say, the product itself. Okay, I want to go to a managed solution. Let's call that managed solution. Let's see what it offers. Okay, high availability, backups, ease of management, I don't need to worry about DBAs. I don't need to have my own DBA team. I don't know, that's not a straightforward answer. Because it doesn't matter. Let's say if you have the database as a service, or if you run your own database service. Okay, it's there, it's watching. But there is always a need for someone to take a look. And maybe they're proactively asked if there is something that is going to be wrong in the near, let's say, next weeks or next year. Or there must be some kind of cost incident analysis or someone who will be defining best practices and best configuration set. So that's why I'm saying that this is a trade-off. There is no answer, believe me because there are some policy people or companies that want to have everything on the cloud because that's easier for them. But it depends on what we're talking about because the cloud is a virtual machine. But Cloud is the database service. So database as a service. I think it provides ease for day-to-day operations. And it's really valuable, because these are solutions that have been tested by 1000s, or millions of users and customers, and are aligned with business requirements. If you want high availability, if you want low latency, you can just have a drop-down that says, Okay, I want this type of this, that's great, you don't have to put an order, you don't have to wait, you're the hardware and the after the hardware may become obsolete within a few months or a couple of years. So it's like spending money that you then have to renew. There are always business needs that say, Okay, I want failover time to be failover times to be within a few milliseconds, right. And this is something that database as a service can sometimes offer. So you can have to create a budget, and put your needs in there, but what is hard for you, for example, if you can't maintain this on your own, or if you can't afford to pay someone to be on top of that, or if you don't want to do that, or whatever it may be the whole use of dynamic environments that you may want to spin databases on/off upscale downscale, then yes, that's a great decision to move there. But in my opinion, you still need someone that will be monitoring that, that we'll be doing some kind of hands-on if there is access to the infrastructure, that we'll be doing some kind of consulting.

**Matt Yonkovit**  
Yeah, so I totally see that where you've got a set of requirements, right. So do you have the skill set in-house? Do you want to do some things that does the provider? So there's a checklist?  and I think that for a lot of people they're looking at some of the enhancements that are in some of the more advanced or things. And so those are benefits to them, maybe it's faster failover or better performance at a certain case or another. So I get that, but some of you mentioned is interesting, and I want to key on that because outsourcing your databases doesn't mean that there is no work for you to do with your databases. And I think it shifts the paradigm, because as you say, oh, backups are taken care of now by the provider. Upgrades are taken care of by the provider. That doesn't mean your tuning is taken care of by the provider or your schema design is taken care of by the provider. So there is a list of activities that are just missed. And that's where I think that you need to be mindful and go in with eyes open because a lot of people end up deploying their databases, and they just trust that everything's done and they don't think about them anymore. because people think databases are uncool, right? Like, ah, I don't want to talk about my databases. So that becomes quite a problem. And it, it leads to more problems.

**Ananias Tsalouchidis**  
Yeah, that always needs for DBA. And I'm not saying that because I'm a DBA. But you gave a really good example. Or let's say we have backups. Okay, if something bad happens, someone should be able to restore the backup. And that's not always a wizard to do that. Okay. And you need to protect a few things. So yes, there are some decisions or if you have an issue, okay, the infrastructure for works. This is there was no issue, but someone needs to take a look at graphs to understand what these graphs represent, interpret the graphs to a specific behavior, and find out the what the root cause was, and what scenes is may be required. For example, that's, that's frequent. That's, let's say, we see, sometimes customers oversizing their infrastructure. 

**Matt Yonkovit**  
Wow, yeah, because the concept of bigger is better, bigger is better. I just want to get the biggest I can get.

**Ananias Tsalouchidis**  
why bigger, because we see high CPU time. Okay. But if you ever went through the real issue, because you may have, let's say, five queries that are not well optimized, or your schema is not optimized 100%. And you could simply create a few indexes, and that would solve the high CPU problem. So this way, you are saving 1000s of dollars or hours.

**Matt Yonkovit**  
Yeah, I mean, it could be a giant, giant sink there. So Ananias, I'd like to end my podcasts with a few rapid-fire questions. It's just to kind of get to know you the random Oh, don't get scared. I actually get scared. A few rapid-fire questions just on random things in the database and nondatabase space.

**Ananias Tsalouchidis**  
how much time for each one?

**Matt Yonkovit**  
It's supposed to be quick, like rapidly. So. So for instance, let me start. What is your favorite MySQL feature?

**Ananias Tsalouchidis**  
Replication

**Matt Yonkovit**  
Replication. Okay, fair enough. What's your favorite Linux sysadmin database tool? What do you what's your favorite tool?

**Ananias Tsalouchidis**  
That's not an easy question. 

**Matt Yonkovit**  
Oh, you don't have a favorite tool.

**Ananias Tsalouchidis**  
These are too many. I don't know where to focus. It's the bus itself where I can just log into a server and start doing crazy things

**Matt Yonkovit**  
You just like the shell that to you. Yeah, shell guy. Yeah. Okay. Favorite programming language?

**Ananias Tsalouchidis** 
Perl.

**Matt Yonkovit**  
Your old-school Perl. My least favorite programming language? Which one do you hate?

**Ananias Tsalouchidis** 
Python

**Matt Yonkovit** 
You hate Python. Oh, wow. That's heard by a lot of folks on the team.

**Ananias Tsalouchidis**  
That should just say between you and me. Okay. Don't tell anyone.

**Matt Yonkovit**  
I won't tell a single soul. And everyone watching on the internet. Don't say anything to anyone else either

**Ananias Tsalouchidis**  
I know. This is not the best answer. But I want to be honest with you. I prefer.

**Matt Yonkovit**  
Okay, fair enough. Fair enough. Fair enough. Fair enough. What is the weirdest bug or performance issue you've ever run into? Like one that just stands out? Is there one that you're like, Oh, that was really crazy? Yeah. Could be anything, you know? 

**Ananias Tsalouchidis**  
Yeah, I've come across multiple during my time in the MySQL world. I recall one recently that has to do with the way that the MySQL optimizer works. And if you have workloads with a few hundreds of values in an enclosed, then the optimizer does something crazy and the performance is really low. I don't know how to explain that

**Matt Yonkovit**  
I can include it in the video, right? Like we could always include that in a bit. Okay, okay, so we're gonna meet up at the conference in a few weeks. And if we're going to go to the bar after the conference, and I'm going to order you a drink what am I ordering you? 

**Ananias Tsalouchidis** 
Well, we see a whiskey.

**Matt Yonkovit** 
Okay, what's your drink of choice? And if we were to have a meal, like if we were to end up we had dinner together. What is your favorite food?

**Ananias Tsalouchidis**  
Okay, I think I have to stand up. Because you will see that I have many favorites food

**Matt Yonkovit**  
but what would you prefer? Like if I, if I take you to a certain am I buying you a burger? Remember a new pizza?  what am I buying?

**Ananias Tsalouchidis** 
Yeah, I think Meat. Meat.

**Matt Yonkovit** 
Okay, meat. Meat. Meat, meat. Meat is good. Meat is great. And finally, finally, what's your favorite book?

**Ananias Tsalouchidis**  
Favorite book? There are too many topics. Okay.

**Matt Yonkovit**  
Too many topics? Just yeah. Did you read the last book you read? What was the last one you read?

**Ananias Tsalouchidis**  
 I'm not a fan of books but have written a book about MySQL recently that got released maybe two months ago. I can give you the reference. And we can Okay, it's to the podcast.

**Matt Yonkovit**  
What do you remember the name of it? Was it efficient? MySQL? Was it?  getting started with MySQL?

**Ananias Tsalouchidis**  
No, no, no getting started. It's about the new MySQL. New features for MySQL eight.

**Matt Yonkovit**  
okay. I was just curious. I always like to get plugs where plugs are due. And we have got a few authors going to speak at Percona Live, which is exciting there. So but okay. Anyways, I want to thank you for coming on the podcast today. Hopefully, that wasn't too hard for you. I appreciate you hanging out and just answering some of the questions. Some are weird. I don't know where the questions will go. I just go off the top of my head.

**Ananias Tsalouchidis**  
Okay, so that was great. I really enjoyed that session with you. And again, thanks for hosting me. Yeah.

**Matt Yonkovit**  
No problem. 

**Ananias Tsalouchidis**  
For those attending Percona live, I'll be really happy to meet you in person. And I hope you find my talk. Interesting. There will be plenty of talks. Don't hesitate to reach me directly. If for any reason you want to do that. And until then, have a great time, everyone.

**Matt Yonkovit**  
Yeah. So, May 16th to the 18th. We'd love to see you there. And like, subscribe to this channel. We watch. We want to hear from you. if you've read Ananias' blogs, and you'd like them, go ahead and tell us if you want to hear from him more often tell me. I'm happy to talk about whatever. I just like to talk to people. I talk a lot. So help me talk more. Anyways, till next time, we'll see you later.

**Ananias Tsalouchidis**  
Yeah. Thanks, everybody.

