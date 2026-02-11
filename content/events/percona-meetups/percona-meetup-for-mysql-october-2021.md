---
title: Percona MeetUp for MySQL Oct 6th 2021
description: The Community MeetUp for MySQL on oct 6th, 2021 was a part of a monthly
  regular event hosted by Matt Yonkovit, Head of Open Source Strategy at Percona.
images:
- events/percona-meetup/mysql-october-1362.jpg
date: '2021-10-06'
draft: false
speakers:
- wayne
- vaibhav_upadhyay
- matt_yonkovit
tags: ["Meetup", "MySQL"]
events_year: ["2021"]
events_tag: ["Community", "MySQL"]
events_category: ["Speaking"]
---
The Community MeetUp for MySQL on Oct 6th 2021 was about MySQL basics for prod environment starting from the system level and monitoring with PMM or Zabbix and backups. In addition, it was a great talk how to enable MySQL Audit Logging and to view the output. Watch the video here!

## Video

{{% youtube youtube_id="KULzKh2H8XA" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit**  
Hello everyone welcome to another live stream we are live on Twitch and on YouTube today I am glad you joined us. And so we should be seeing a few more folks here join today we're, of course, going to be talking about MySQL. It's near and dear to my heart. I've worked with MySQL for 20 years now. And I'm joined today by Wayne and Vaibhav, who are here to talk to us about some of the awesome things they're doing in the MySQL space. We're going to hear about MySQL auditing, and how you can set up MySQL and production to be successful. And we're gonna be taking questions and seeing what people have to say. So welcome Wayne and Vaibhav. How are you guys today? 

**Wayne Leutwyler**  
Doing great. How are you? Great, great, great, man.

**Vaibhav Upadhyay**  
We'll be doing well.

**Matt Yonkovit**  
Yeah, yes, I'm well, so um, maybe if we can start with you, Wayne. Maybe give us a little introduction about you. I know you have spoken at several conferences. We were just at the open-source summit. You did yours virtually. I was there in person. You did a talk there. Maybe give us a little background on yourself?

**Wayne Leutwyler**  
Yes, sure. So I've been playing with MySQL since version three as a hobby database, and then professionally in the last 15 years. Columbus, Ohio, or pal Ohio. Where do you want to call it? We're just outside of Columbus a stone's throw away again, wife, kids, and six cats and two dogs, and I'm just a great big old nerd. He is what I love. Well, that metal music. I'm definitely a metal music fan. 

**Matt Yonkovit**  
So, what are you listening to now?

**Wayne Leutwyler**  
So today I was listening to archenemy. Okay, before we fired up. So I had to turn that down because it's a little extreme. But it's one of my favorites. Any metal genre that's listened to? I love it.

**Matt Yonkovit**  
Really? Okay. Well, awesome. Awesome. Well, great. And that's something we do have in common. I'm a big nerd and love to go to metal shows whenever I can. But generally, I have to go alone because my wife doesn't like it. So yeah,

**Wayne Leutwyler**  
 I've got one coming up on the 27th of November 1, one I've been to since the pandemic, and it's a band called ginger out of Ukraine is going and I intend on being inside that mosh pit the whole time.

**Matt Yonkovit**  
Oh, so Windows machine and MySQL?

**Wayne Leutwyler**  
Yes. So hopefully, dedication and passion.

**Matt Yonkovit**  
That's great. Wayne, thank you for joining us. And Vaibhav Why don't you tell us a little bit about yourself? Yeah,

**Vaibhav Upadhyay**  
I'm working as a DBA lead and production support engineering team for the company called Tech Mojo. And really excited to be here and using MySQL for almost like 9-10 years, or maybe a little more than that. So yeah. Really excited to be here.

**Matt Yonkovit**  
So we probably started about the same time. So were you in MySQL three-dot something guy? 

**Vaibhav Upadhyay**  
Yeah.

**Matt Yonkovit**  
That's when I started way back in the days.

**Vaibhav Upadhyay**  
Yeah. Okay, good.

**Matt Yonkovit**  
So, um, hey, Vaibhav, why don't we start with you, you wanted to talk to us a little bit about your experience in running MySQL in production. So I figured it would be a really good place to start Talk to us a little bit about your experience and tell us some of the things we should look out for.

**Vaibhav Upadhyay**  
Okay, so, as we all know, MySQL is a, the most popular open-source database that people frequently use across the globe. And starting from the smallest application to the biggest application or product that we are using on a day-to-day basis. So there are certain things when we use MySQL in production, especially, there are certain things which I would like to highlight that folks who are starting their career as a DBA maybe, or maybe they just started using MySQL can maybe this tips will be useful for them hopefully. And so a couple of things like there are certain basic settings when we use MySQL on Linux or Ubuntu or any operating system. So, apart from the code with the core thing is like installation and configuration on the, on the very basic fundamental manner, wherein certain voice level settings that need to be taken care, for example, open file limits, which is which plays a very huge part when, when when you have a lot of concurrency on for your application. So that has to be taken care of very well. The safest bet for that setting is to set it as higher as possible, rather than just setting it to one zero to four.

**Matt Yonkovit**  
The downside to that, though, is if you set it too high, have you run into any problems? If it's too high, though?

**Vaibhav Upadhyay**  
Yeah. So I mean, there is the downside of it: you'll end up consuming more resources. And yeah, there is no, there is no right value for that, it depends upon the workload of your application. And as in when you play with that setting, and then you decide whether you want to go with 5000 50,000 like or, or in some cases even higher than that. So, it typically depends upon the workload of the application. Yeah, so one of the settings is that another set, I would suggest or would like to talk about is swapping, which is another really important, I would say, setting for the production, at least, by the way, I'm just talking about production, but it applies everywhere. It depends upon how heavy you're using, whether it is your production environment or your door environment. So, swiping swappiness is something that one should be, because, by default, it comes with a 60. Right? And, and, and you land up eating memory if you are if your, your, your application is very heavy in terms of concurrency. So, again, there is no independence, for every setting, there is no, every setting will not have a specific right value, it really depends on how your overall architecture and worry application is behaving, your, the way the database has been consumed. So let's say setting up with the lower value, maybe to start with 15 or 20 and then gradually to go towards five, and maybe towards even lower than five, but not zero, for sure. Because once you go there, then there is no you're not having that room to get the attention of the problems.

**Matt Yonkovit**  
Yeah, so, And for those who might not be aware of what swappiness is, it's telling the operating system how much memory to reserve for file system cache and other things. So you're not able to necessarily access or use all of the memory as efficiently as the database would like. So sometimes setting that too high can cause issues. Vaibhav, when you're talking about some of these settings, right, so make sure that the system is set up. I think that there's a lot of very basic things that you should go through. And I'm curious, do you see a lot of similar issues over and over again, that maybe your developers deploy new applications, and they kind of fall into the same patterns of oh, they missed this thing?  Are there certain things you tend to see quite often?

**Vaibhav Upadhyay**  
Yeah. But as in especially, you see a lot of this kind of issues on the forum as well where user come across and, and all this kind of challenges where, okay, we are having performance issues. That's a general statement, right. And when you try to dig down, you find things are going wrong at a lot of places. And one of the common things which I've observed is, is memory, the way the memory is being consumed by the database indirectly by the application. So, yes, I mean, I come across a lot. But as and when I'm contributing to the forums, and people learn or learn a lot from the Percona forum as well, I'm sure anybody who is a MySQL DBA will be hugely relying on Percona forums, tools, and the ecosystem that Percona is built for. So yeah, we learn a lot. And, we face quite frequently this kind of issue, which revolves around memory.

**Matt Yonkovit**  
Okay. Okay. And is it because maybe developers are not using indexes, their queries are kind of bad. I mean, like, What is there? Is there a common theme that you continually See?

**Vaibhav Upadhyay**  
Yep. I mean, yes, it happens, especially in the lower environment. We try to restrict it to the lower environment as much as possible. So we learn from that, and we ensure that we deal with those things. So yeah, sometimes indexes are missing. Sometimes we are joining different tables and having different character sets and not using the efficient index. Sometimes you're using the wrong index. So yeah, I faced this kind of challenge quite frequently. But as I said, noise and when we learn, we look back some of the things when you face this kind of issues based on your past learning, you'll end up checking those things first to ensure, okay, this is the this is something which is already taken care, and to look for next problem where it is exactly to trace down, where is the exact issue? So, yeah, I mean, quite a lot missing indexes, not using proper indexes, not at all having the indexes.

**Matt Yonkovit**  
Yeah, those are always tough ones. Because it seems to me and this is maybe just the theme that I'm going through at the moment, I've been really trying to push database design matters more than you might think, lately. Because a lot of people that I've been talking to, whether it's on meetups like this, or on my podcast the system as you kind of mentioned, there are some certain settings, whether it's the number of open files, or it's the swappiness, or you're talking about configuration parameters, like the InnoDB, buffer pool size, or things like that, those are very common, and once you have a good DBA team, they can dial those in for a lot of applications, and they can tweak things as need be. But I keep on hearing over and over again that code gets deployed that hasn't been properly tested. It hasn't gone through the process of getting vetted. And so I think that for that, it's something that we see quite often if you can plan for the knowns but that code deployment, new releases, those types of things, they tend to cause more issues than you might think. Have you experienced that as well?

**Vaibhav Upadhyay**  
Yeah, yeah. A lot. It's real-world out there. So even at times, like for, as you rightly mentioned, right? I mean people are testing, you are in a hurry of releasing new features for the product for the, for the, for the application. At times, you face this kind of challenge when you're having a bug fix also, right? You want to fix certain bugs, but you forget about thinking from the performance side, and then, hopefully, when you test those things on the lower environment, testing environment, and have a good DBA team around, they can trace that, if you have tested well, and if you have reviewed it with, if you don't, then you will land up having unpleasant surprises and production,

**Matt Yonkovit**  
of course, right? That's always a challenge. Yeah. Wayne gonna say something I saw, he starts to move,

**Wayne Leutwyler**  
Do you find that there is a disconnect between the developer community and the DBA teams, a large disconnect, where there's not a lot of communication that goes on between the two? And those problems on the back end from the database, and the application point of view could have been resolved earlier? If there was more communication between the app developers and the DBA teams?

**Vaibhav Upadhyay**  
The question is for me?

**Wayne Leutwyler**  
yes, yes. 

**Vaibhav Upadhyay**  
Okay. Yeah, I do find, however, at the same time, I feel that this gap is getting reduced day by day, as in more as a DBA you involved not only communicating frequently with them for the issues, but also, things which they don't know, you try to educate them, and try to share your knowledge, in terms of how you're solving the social issues, maybe not directly related to them, maybe something which is internal to the mod corps towards the DBA part, but still, you try to share and as in when that I think if I look back five years back, this gap was very huge. And when I present the, when I look, when I think about this gap, it's, it's getting reduced. And, and, and they're more aware of now, but the key is the communication, how we as a DBA team, how I'm solving those issues as in when I'm finding it so that they ensure that this is not repeated in the next release, even for any other application or module. So yeah, we try to have a common knowledge base and communication as frequently as possible. So we share our knowledge and how we have fixed this issue. So yeah, we end up experiencing new issues, then repeating the same old ones.

**Matt Yonkovit**  
So it's an interesting point because I've seen a couple of different things. So the longer teams work together, I think the easier it becomes, right? So if you've been working with a core group of DBAs, and developers who have started to build those connections you definitely can get some good scale and you can start to rely on and kind of teach each other. But I keep on seeing more and more. I mean, I think I saw the average tenure of a developer is less than two years at a company, it's like 18 months, which means that they move stuff into production, and they never see like, potentially the first update to it. Which is kind of crazy if you think about it. And I mean Wayne to your question, I've seen a bit of the opposite when it comes to some of these newer companies, especially when you have that high turnover, a lot more companies are starting to move away from having dedicated DBA teams even. And you end up having maybe an SRE, who's responsible for the entire stack. And isn't necessarily just the database expert, right. And so that becomes even more challenging, because the pressure for a lot of startups is turning the code around, turning the code around, release, release, release, release, release. And it just happens so much so fast. A lot of times, things just get thrown over the wall. In fact, I've talked to several people who I said hey, what's the biggest problem that you guys face? And they are developers! I mean, it's just the first thing that developers write like, and it's like, well, is it really developers? Or, well, we never see the code before it goes to production. Or we don't have a say in whether that code can go to production. So it might be a really poor design. And it just kind of gets thrown over. And what's your experience there Wayne?

**Wayne Leutwyler**  
Same thing, just the same exact thing. There's no communication between the DBA teams and the application teams, there is a segment of duties, the application teams, they design their tables, they design the database, they do all the fun work in the back end, but without consultants and DBA. They move it into their development environment, and it starts to fall apart, they then reach out as a fire drill to the DBA team, Oh, it's not working the way we want it we got to go prod tomorrow. And we're seeing all of these issues. And in those six months of development, a DBA was never involved.

**Matt Yonkovit**  
Well, so at least you got them to move it to the test. There are a lot of people who do continuous integration, deployment, and deploy immediately into production and stuff now, which I've seen that causes immense problems, as well. Right. But yeah, I, I feel your pain, because I've seen that quite a bit as well, where you do have that, especially with more diverse groups. I think if ideally, you want to be tightly coupled with the development teams. But I keep on seeing. And I don't know, Vaibhav, if you've got a lot of development teams you support, if you've got smaller like groups. I mean, there are some companies that might have 1000s of applications, and each one has a different development team. And there might be like, 10, DBAs to support 1000s of developers, right? Which is like, how do you do that? Yeah. How do you get those scales? So I don't know. Do you have fewer application development teams that you're working with? Or do you really like to spread out?

**Vaibhav Upadhyay**  
No, I would say like, it'll run about 50 Developers team versus 3 DBAs.

**Matt Yonkovit**  
So yeah, you're getting some pretty good scale there as well. Yeah. And I know when your environments are pretty big and complex, complicated with all kinds of different systems.  I think the other thing that I see, and I don't know if both of you are seeing this as well when we're talking about production, and we're talking about databases, I'm seeing more companies just end up with non-standardized technologies, right? So and again, this is this, this has a lot to do with how organizations are set up. But it could be this team only wants to deploy the MySQL community, this team wants to deploy a Percona server, this team wants to deploy MySQL enterprise, this team wants to use MongoDB, this team wants to use something completely different. And like, they all kind of like a fight. And  Wayne, as you said, sometimes it's like, this has to go into production tomorrow. And you're kind of stuck with some of those choices, sometimes.

**Wayne Leutwyler**  
That's true. And I know one of the things that I like to do, where it is all possible, is set down that base set of standards. This is the version that we're using MySQL or Percona. Server. These are the versions that we're using. These are the support teams that will support you. These are the standards that we've designed around the DLS, the basic database configuration, and let them take that and go with that and then build the wrapper around it. So at least if the DBA team is getting 18 new servers, and the next two days, they're going to know that those 18 servers are going to be built the exact same way at the OS level at the MySQL configuration level. And then if they start hitting problems, they can start adjusting for the MySQL that might need to be adjusted, but also work with those application developers to go, Hey, you got this query, and it's pulling back 200 million rows, but you don't have any indexes. an index here to speed things up for you. Yeah,

**Matt Yonkovit**  
Anyway, so we kind of went off into a little side tangent there. And I wanted to finish some of your tips and tricks for getting your system ready for production. So we talked a little bit about a few settings. But as your applications are getting deployed, as you're having conversations with your development teams or other DBAs, what are some of the other critical things that you're looking at to make sure that is set up to make sure that they have smooth sailing and success when they deploy?

**Vaibhav Upadhyay**  
like, so, as Wayne rightly pointed out, basically, there are two-three areas where we try to focus basically, especially when rolling out any deployments or anything, no new database server or anything. So, one, as Wayne rightly said, to have a production standard, which which you have set irrespective of anything, there are certain standards, which are in general like, which we follow, like, as I mentioned, like whether it is happiness, which is open file limit, there are certain really small things, like, for example, having a system that installed, right, you want to ensure that you are having one-minute interval, SAR report, not completely relying on your ga monitoring tool, but at times you are just logged in there, and you don't want to switch your window to see what is happening on the CPU, just to check on the monitoring. So, these are very minute small things, but we try to follow those production standards whether it is for database Even it is for the application servers, right? So this kind of thing. So, another thing also to ensure like having a smooth deployment or rolling out new database are rolling out new features, new applications, we ensure that there are three aspects that we try to focus very closely, one is proper sizing, or choosing the hardware, not overly spent, not understand using the right version, when it comes to MySQL we obviously five 5.6 and have a lifecycle, but again at least have minimum 5.7, having basic configuration really, right, whether it is related to spreading out your binary logs versus your data directory in a different partition to have a balanced IO, whether it is having an ensuring it is under the monitoring, by the way, we use PMM. So ensuring that it is there, and, right, and that's the best tool that we have, honestly, in open source, undoubtedly. So. Yeah, and ensuring that we are having at least bare minimum testing, you can't really simulate your production load so having bare minimum testing in place, ensuring the new, maybe stored procedures or queries are reviewed by the DBA Team, okay, ensuring, so let's say you you may be lined up, we may well end up having 100 things which is deployed, which are going to deploy in the next deployment, but we try to ensure out of these, what are the most frequently used a call, or a feature, or, or a query that we know, this will be called multiple times for every single call this will go into it. So we try to focus on that top five, top 10. And we ensure that, okay indexes are in place, what is the size of that table that you're going to call, how frequently you're going to write this table, or how frequently you're going to read this table? This table needs a design change because you're going to introduce this new feature, right? We try to take care of all these things, but not completely, we try to bucket it into, as I said, like what are your top 10 calls in this deployment, right top 10, heavy items, it may be a small change, but we know this will go into impact in a big way. Even if something goes wrong, it will go on to blast. So that's how we try to take care of it. And again, once we deploy those things, we try to analyze them over a period of a few days. 345 days one week, to understand the pattern. And to compare using PT query digest, to be honest, we use it very frequently, which really helps us to understand how we are versus how we were before that look.

**Matt Yonkovit**  
So so you're deploying standard configurations, you're trying to stick to a standard configuration, and then you keep on iterating. Even when in production, you're checking for those changes on a regular basis. Yeah. I mean, I think that's always good advice. And I think it's undervalued sometimes that just because things worked yesterday, doesn't mean they're going to work today. Yeah. And I think that , that, that, that is a very good thing, and I have a story that I could tell later on about that. And I'm working on a presentation on real-life anecdotes that can teach us good design principles. So so stay tuned for that one.  So I'm curious, are you using anything for your configurations? Like are you using either an Ansible or Chef or Puppet or are you doing anything Kubernetes related yet? Or is this just kind of like, you just have a standard configuration, you deploy you kind of build from scratch?

**Vaibhav Upadhyay**  
No, at this point, we are building from scratch, but we will be moving to Ansible in the future, like, in a few months, but at this point, it is manual. And, and, and we have fixed most of the issues, which revolve around either capacity or, or whether it comes from configurations, which we have learned from our past mistakes, as I mentioned the smallest thing, the biggest thing, what should be your buffer pool? What should be your estimate settings, what should be your isolation level. So all these things are based on our past experience, we have learned, and we have standardized that configuration. So we know, at least in these areas we will not be having these issues, we'll be more than happy to deal with new issues to learn new things. And that's how it goes.

**Matt Yonkovit**  
Okay, good. Now, one of the other things that we have to get right, and that has to be standard is security best practices. And that's why Wayne's here today to talk to us about one of those really critical things, which is auditing,

**Wayne Leutwyler**  
logging, auditing. 

**Matt Yonkovit**  
Yes, so so way,

**Wayne Leutwyler**  
why should I use audit logging? Why do you use audit logging? Yeah, it can be a great forensics tool to dig through.  if you've got queries acting awry, you can kind of see how often they're going. But it can be a better forensic tool, that if data starts disappearing mysteriously, or users start disappearing mysteriously or passwords start getting changed, and you don't know where it's coming from. Use of the audit log will give you a forensic tool to help you narrow down where that's coming from. And it will help you home into who potentially even done it and then you can go dig from there as to why they would have done it. We live in a world with data so important now that if you don't have some kind of data auditing on, you could potentially be doing yourself a disfavor. I recently had a situation where if it weren't for the audit log, we would have taken days longer to figure the issue out. And that was just it was incredible that we could just find it as quickly as we did and then put it to sleep. So I'm having been at that point a big proponent of it, but I am now just because of one incident that really waited in my mind that how important knowing what's happening to our data really is I know a lot of folks who do use auto logging and they pretty much just turn the auto logging over to their audit and compliance side of the house and let them deal with it and they don't look at it they don't to just say okay, here you wanted it. So now you can have it. I think it can be used for a little bit more than that. And I think people should, especially if they have important data that they don't need to see disappear or they need to keep a consistent check on an auto-logon is great for that. 

**Matt Yonkovit**  
There are really three things though, from an audit perspective.  you mentioned the troubleshooting aspect of it, something weird has happened. So how do we do that? The compliance aspects are another one that you alluded to there as well, right? So you've got that compliance and let's be honest, every big company now is all in on security and compliance and you can't, you can't do anything without having security and compliance. Kind of Like checked off, but I think that maybe like the third one of that, that kind of like tricycle if you will, is, you know really just about understanding some of the patterns that are happening that might give you a bit more insight or observability into what's happening right so you can troubleshoot those problems or security breaches, you can have the compliance issue for compliance. But I think that some of those patterns aren't necessarily obvious until you start to see them and say, like, why is somebody doing this on a regular basis? Why are they changing these tables every week? Why are they doing these things?  you start to see some of those kinds of weird ones.

**Wayne Leutwyler**  
Agreed, agreed. And if you can start to narrow those down, you can definitely get control over the situation a little bit faster. Let me so I wanted to talk about the whys, I think we covered the whys. But we could go deeper into the whys. But let's, let's go to turn it on how you know how I would go about turning it on and then look at how we can actually parse data. Now, I am a big fan of interactive. 

**Matt Yonkovit**  
Alright, so what we're gonna do is we're gonna go and move us to the bottom, so Wayne can get as the screen goes. Or maybe we'll move as an aside, I never, I never know with this setup, where it's going to get the best screen,

**Wayne Leutwyler**  
okay, should see my desktop, my Raspberry Pi console.

**Matt Yonkovit**  
Right? So there you go. All right.

**Wayne Leutwyler**  
So this is my little raspberry pi, six production servers that I use here, this little guy does everything for me. When I enable audit logging, I like to do all my skills off, I will enable the audit logging plugin, I like to set it to JSON for the output. And then I like to use Jq to parse that out, which gives me more flexibility to parse it in that manner. Changing the format of the log is not dynamic, you can enable the audible while MySQL is running, but you can't change it to another file format. And by that, 

this server is running five and got 70 because I can't build data on a Raspberry Pi just yet. So these are typically what I use when I put together a box for myself or for a customer who may come to me and go Hey, how about some best practices. And these are no by no way the gospel. I think one that is overlooked a lot is the ability to make this plugin permanent. I don't want somebody to go out and disable that plug. Yeah, malicious things, and then re-enable it. So this one is really key. Another thing that I like is it like I said, I do want to parse it with JSON, I prefer to parse it with JSON easier to read easier to dig through easy to query against

**Matt Yonkovit**  
Wayne, are you loading that JSON anywhere else, like whether it's elastic, or open search, depending on stalled or any other tools?

**Wayne Leutwyler**  
So we would in a bigger situation, I would definitely recommend it will be dumped someplace else will be queried, easier than a command-line query that I'm going to do here. So I know that a lot of companies that I've dealt with, are dumping it into data like where they can then start digging through it, which I think, is actually a great thing.

**Matt Yonkovit**  
Yeah, and I'm sure that when you talk about the compliance team, giving them just raw JSON probably makes them scratch their heads.

**Wayne Leutwyler**  
Yes, it does, it does. So we dump it into a manner that they can get to it, and have an easy query from it, instead of having to pull their hair out. I've actually seen some compliance teams that I've interacted with, actually about writing their own tools to parse the JSON data themselves,

**Matt Yonkovit**  
I think it just depends on the level of skill level in the company. Exactly

**Wayne Leutwyler**  
exactly. So again, these are the main ones I'm using, I pointed out the forced permanent, we don't want to download it, once you put it in, I set a one gig size, before it will rotate to the next one. And then just for demonstration purposes, I just remember, retain four logs in a production environment, you will probably have to retain much more than that. And you will have to probably have your compliance team telling you, hey, you've got to keep 30 days worth on the server. And anything older than 30 days, you have to dump to the repositories that we can parse through a flavor if necessary. Alright, just for a test environment here. I just kept it pretty straight and simple. And as they rotate it one gigabyte the size. You'll notice in here, you don't see me filtering. I don't believe in filtering your audit log.

**Matt Yonkovit**  
So are you worried that the size is going to get too big or that the potential impact on the server performance could hurt you?

**Wayne Leutwyler**  
I have not seen it has an impact on the servers yet. In any of our situations where we've had to say Oh, it's the audit log was turned off. I haven't seen that. To date, and, I've been involved with audit logging for at least eight years, and I'm in no situation.

**Matt Yonkovit**  
So out of curiosity, and I think, generally any sort of logging, especially when you're logging things in mass, there's some overhead, right? It's, of course, negligible, right? So 5% 7%, I've seen 10%, depending on somewhere in that range, I think this gets back to a production best practice that we didn't talk about, which is probably don't run your servers to the red line. At 90%, and you turn on audit logging, it probably could impact you. But if you're always running at 40% 45, or 46, probably isn't going to negligibly impact things. 

**Wayne Leutwyler**  
Agreed. And that's one of the things when I do speak with folks who want to do this, I'm like let's look at where your server is today. Yeah, let's look at your performance. And if, if this is going to ship you over, it might not be the best idea, we might want to tweak some other things or look at some other items that we can pull your overall performance back a little bit before we add this in, right. And again, filtering. If you speak with folks who do audit and compliance as their primary job, they will tell you, they don't want to see any filter. Because filtering defeats the purpose. If you're filtering out a specific user ID, if you're filtering out specific tables, you're defeating the purpose of the audit log that needs to happen to record every transaction that goes on and filtering out, not a best practice should not be done. Because if you filter out a particular user, right, let's say you filter out the user ID view for pet PMM. And someone happens to get that user ID, they could start to do potentially malicious things with that ID. And if you're not capturing what that is do guardians do and you might not find where something malicious is occurring. 

**Matt Yonkovit**  
So yeah, there's those blinders on then, right?

**Wayne Leutwyler**  
Exactly! I mean, if you're auditing, don't filter and audit everything. So, this is the general idea of what I do. In my test box in this For this demonstration, this is not gospel, everyone would configure it a little differently. The things that I think should be gospel would be Don't let it be unplugged. And don't filter anything,

**Matt Yonkovit**  
okay? So that so Wayne's Wayne's two commandments,

**Wayne Leutwyler**  
yeah, my two commandments are don't filter anything and don't set it up. So you can disable it because you just open and close it for yourself.

**Matt Yonkovit**  
Good advice to live by.

**Wayne Leutwyler**  
Thank you. So this, this particular box of mines, and running for a bit of one more thing. So when you make all these changes, you might see an F file, you will need to bounce your server, bounce your MySQL instance, so they can get picked up. That's why I typically do things like this at the beginning of a server’s life. Or if it's someone who comes in after the fact and goes, Hey, we didn't enable us in the beginning, but we need it. Now, I might take a maintenance window to put these in, and then restart the MySQL instance at that point, so they can pick them all up. I know that a lot of standard builds will have some sort of audit logging already put in it ready to go when it comes out of chef or Ansible or wherever it comes from, it will already be there. And then if you're worried about potential disk issues or discipline, give it its own file system, give its own file system, let it do its thing over there. And then you don't have to worry about impacting the data file systems that are working heavily as well. So if you can segregate that out, I definitely recommend separating that out just to keep that level of performance from being impacted. So this particular server, it's my weather database

**Matt Yonkovit**  
Your weather database. So

**Wayne Leutwyler**  
I have two workstations, one of our greeno, one of the Raspberry Pi, and they feed this database. So we're going to jump into and you can see here that I currently have one plus two others. Those two others were from phone reboots, so there's really not much. So we're going to look at this first one, we're going to do a quick little peek in it. And I'm going to use a combination of Jq grep and sed to narrow down to a specific item that we want to look for. So let's say this in this first demonstration. Let's say we want to look for inserts on a particular table. Or just all inserts that are occurring on the database. So I can run for that ... sorry about that. Insert Oh, crap.

**Matt Yonkovit**  
It's okay, whenever there are lots of people watching, okay? It's a rule, it's a rule, you have to like have merge something, like, Oh, no, I can't. Right? 

**Wayne Leutwyler**  
OK, so we're going to just pull on anything that was inserted in this particular string that I got set up here. So as you can see, it is filtered by all the insert statements that are in that particular log file. So you can clearly see here that this one map was a holdover from my talk in Percona lives this year. I named the table Percona so that I would make sure that when I did my demos, I had the right data. And it's still there, it's still there. And it's still being fed by my Arduino weather station. That's been up since April. chugging right along. So again, you can see here all of the data that I captured was just from the answer state. And that in itself is you can get developers patterns here, you can develop what's going on here by looking at this. If you just wanted to look at the entire audible without filtering it down. It's really simple enough to just do.

**Matt Yonkovit**  
We had a request to increase the font size, so I switched our view here. I don't know if we'll be able to see the whole thing. But you know what? I mean, it's a little easier to read now I think, but I can't remember. Okay, I think we're okay. Here we go. I think it's the same, but

**Wayne Leutwyler**  
Okay, so on my side. Okay. So if you just wanted to see everything without any filtering without any grepping, you could just do this audit log and pipe it to Jq. That's still my name. If you could pipe it to Jq. And you can see everything that's going on. Jq is a great JSON parser with a lot of tutorials, a lot of things written about how to bring data out. So if you want to go this route, you want to turn JSON. Jq is a good parsing tool. There are other ones that are out there as well. I'm a command-line nerd. So I like to stay in the shell as much as I can not get into the GUI world if I don't have to stay here caterwauling. So this is pretty cool. We saw everything that we want. We've seen everything that goes on in your database, but let's do something that would be considered destructive.

For demonstration purposes, I put this horrible security hole back on last night, at the root at the localhost back end. So we could demonstrate with that one today what we're going to do to it.

**Matt Yonkovit**  
Go hack Wayne's weather station. Yeah,

**Wayne Leutwyler**  
yeah. And you have about two minutes to hack it. So hurry. So I'm going to do just a drop.

I'm gonna jump out. And we're going to bring my auto log command that we are querying. And I'm going to change it to

**Matt Yonkovit**  
Yeah, we're unfortunate because of the screen. We're kind of like, not able to see what it was. Oh, can you throw up that command? Just again, real quick? Yeah, just so people can see it? Yeah. Because when we're down at the bottom, it cuts us off. So yeah, no, okay. There you go. 

**Wayne Leutwyler**  
you can see right here that I updated the command to look for the word drop. As you can see, the user route was dropped. Right?

**Matt Yonkovit**  
Right now, now Wait, here's the thing, right? That's great that we can identify it. But if we had proper security, we should have prevented the drop from ever happening, right? Correct.

**Wayne Leutwyler**  
If we have proper security, we know drops are from happening. I was a privileged, elevated user. So I could do that. And I did it that way. So with that, we could see in the audit log that it was dropped. And it was dropped from so the PI User at the local host, ran that drop statement. And that's nice because you can actually say, oh, Johnny, at, sir at client x, y, z, ran the statement at this particular time, why don't you write a write back to the person who did it? And find out what's going on? It's

**Matt Yonkovit**  
one of the layers of defense, right? You know you want to, this isn't a replacement for security practices that prevent those things from happening. It is if they do happen, how do you find out who and how do you go slap on the wrist?

**Wayne Leutwyler**  
Exactly. And I know in some larger organizations, there are a lot of shared IDs that are supposed to be shared, and then also have the proper level of security on them. Sometimes they might get set up incorrectly. Some might not verify what permissions they gave those shared IDs. That shared ID might have the ability to change a password. Yeah, so if 16 people know the password to be john doe, and then somebody comes in overnight and changes the password to Jane Doe. Now we've got nobody who knows what it is except for that one person. Right? We can jump in, we can see who did that because they had the right to do it, we can see who did it, we can go back to them and go, okay, we need to change this back to john doe. Because we don't know why you changed it to Jane Doe. But everyone knows that as john doe. It's being used that way. Let's put it back.

**Matt Yonkovit**  
Make sense? 

**Wayne Leutwyler**  
So those are the kind of that's my, that's my song and dance for today. Just the ins and outs of it, why to turn on, why to use it, and how you can actually look at it. I will follow this up with a more detailed blog post. Cool about the next three weeks. On the Percona community blog, I followed up with a detailed blog post so that people can get more information from it.

**Matt Yonkovit**  
That's great. That's great. And I think that everybody should have that thought process of security in-depth. Right?  you need to make sure not only do you have the things to catch them when they happen, but it’s also like it's just like performance tuning when you talk about this, right? When the problem is happening. You want to fix it, and you want to have the information to fix it. But ideally, you want to prevent the problem from ever happening in the first one, right? Because once the problem is happening once the servers are on fire, that's like hey, it's great if you can fix it, but getting on fire in the first place is not a good idea.

**Wayne Leutwyler**  
No, no. And this is just one way to help you put that fire out quicker if in case it does happen.

**Matt Yonkovit**  
Yes. Yeah. So um, so we had a few comments, no questions so far, but we will throw out Happy birthday wishes. So we have Ranvijay is saying October 6 is his birthday. So happy birthday. Happy birthday. It just happens to be my anniversary today. 20th anniversary, so as well.

**Wayne Leutwyler**  
Which is, that's a great milestone.

**Matt Yonkovit**  
Yes, it is. And so, we also have Veer totally wants to be part of Percona and work on the extra DB cluster operator and we're I would encourage you to reach out, you can check out our careers page or if you want to hit me up on discord, I can connect you with the right people, always looking to add people to the team. We also have a comment here. Question on the auto log native MySQL feature or Percona feature it is a Percona feature. You can get an audit log as part of MySQL enterprise as well as pay for MySQL enterprise.

**Wayne Leutwyler**  
Just another good reason to use Percona server because it's right there with it when you get it. Yes, and it's really helpful.

**Matt Yonkovit**  
All right. I don't see any other except some thanks for the birthday wishes from Bangalore which is always wonderful. But everyone, thank you for coming today Wayne and Vaibhav. I appreciate you stopping by hopefully we can do this again sometime you know, have a bit of a conversation on things. Love when we have you know people talking about some interesting things or Doing and appreciate the anniversary wishes. Oh, we have a question right up Wayne's alley, whoa.

**Wayne Leutwyler**  
IoT devices connected directly to MySQL, I use Arduinos. For most of all of my connecting to MySQL from an IoT device, there is a great set of libraries that are out there written by Chuck bell. They are connector libraries from MySQL from the Arduino. So if you use the straight Arduino C code, you have them. Let me see if I can grab that link or click and drop it in the chat.

**Matt Yonkovit**  
Okay. Yeah. And I mean, it's interesting to connect directly from the devices. I wonder if it gets it depends on what sort of devices if they're deployed in the field, could that potentially be a security risk. Do you want to go through a proxy? Right? Do you want to go through some application middleware?

**Wayne Leutwyler**  
So I would in my initial talks, when I've done this, one of my goals was to do away with that middleware in places where it was doable. And since all of my projects are internal to my network,

**Matt Yonkovit**  
right? Yeah, yeah.

**Wayne Leutwyler**  
But Chuck Bell does have some security built into these drivers he has written. Okay, man, where do I paste that?

**Matt Yonkovit**  
Oh, ah, there should be like a chat thing. Shouldn't

**Wayne Leutwyler**  
there? Like, see the chat between us?

**Matt Yonkovit**  
Oh, well, he put it there, I can put it on the main. Okay. But yeah, there should be a chat. I don't know, since I'm the host here. I get all kinds of super special access. But there I just posted in the chat there. 

**Wayne Leutwyler**  
Like I said, Arduinos. To do it, you can do this by directly going to the database. Chuck bell has written some great connectors. I've yet to reach out to him to see what his future plans are for more security. Actually, I probably should, since I've presented on this several times this year to see where he's gonna go.

**Matt Yonkovit**  
Yeah, yeah. And  I've been using the arduino for some devices and doing some demo stuff. But I'm not going directly to any of the databases, I'm using that kind of proxy layer, where I've got a controller which intercepts whatever I'm doing on the devices and then translates it into what I want to do.  so I think that's it, it just uses six, one after the other. But I also have to work with Postgres, Mongo, and MySQL. And I'm part of my thing is, I'm going to extend that to actually interact with AWS instances. So when you get it I think I got one of the devices around here somewhere. Oh, well, you can never have it just handy when you want it. But basically, when you turn, turn a knob, you can increase the instance size for AWS. Right. So if you want to see what moves to the next biggest box just turn the knob. And we can see, like performance on the different size boxes using the same workload and stuff. So I think that'd be pretty cool. Yeah. So all kinds of geeky stuff. Always fun. But I appreciate both of you coming out hanging out. I see there are a couple of comments from Veer on his desire to work for us. Here. I'll, I'll take a ping the folks here at Percona about your application, tell them to reach out to you also if you wanted to just drop me a note on Discord. Our discord is, is available and I'm always on that as well. So in case you need the link, there you go. discord link, right there. Feel free to grab that as well. And join. Oh, look at that. Now we got a question on blockchain for my SQL. I have not seen anything for blockchain either. Yeah. Yeah. Yeah. So I think that's something that's potentially coming. I'm sure that people want to blockchain the world. So  I don't know that there is some interesting work that I've seen in Mongo and some other places because they want to guarantee transactions for security. So they built it there. And so there's that. Now, Veer, you want to know how you can contribute to projects, there's a couple of different ways. So obviously all of the code is available on GitHub. You can push, pull requests out there, you can submit bugs, you can submit fixes and patches. So if there are enhancements or things, I would encourage you to do that to go through that channel. We also have our engineers all in Discord as well. So you can reach out and ask questions and engage there or on the forums. And we'd be happy to have you there.

**Wayne Leutwyler**  
I can't say enough about Discord. If you're not on it, get on it. A lot of good questions get asked, long-duration gets shared. Yeah.

**Matt Yonkovit**  
And so Oracle did something with blockchain and Oracle 21. So I think it's everything in the kitchen sink. Right? So we that that kind of model. I'm sure that eventually, something could show up and MySQL. Although if Oracle's doing it, they'll probably reserve it for their MySQL service, or enterprise version. But that's just my thoughts. I have no inside knowledge of that. That's just you know me. But all right, everyone, thank you for coming. I appreciate it. And we will see you next time next week. We're talking about Postgres. Hope you show up there as well and looking forward to hearing from you guys in the future. So thanks for

**Wayne Leutwyler**  
Thanks, Matt



![Percona MeetUp for MySQL Oct 6th 2021](events/percona-meetup/mysql-october-1920.jpg)

Percona Community Team organizes the MeetUp for MySQL every first week of the month. It is an hour of live streaming dedicated to experts and users to discuss MySQL databases. Matt Yonkovit, The Head of Open Source Strategy (HOSS), invites experts to share their knowledge. Come up with your questions as they like to find those tough database problems.

Join for an hour MeetUp for MySQL

* Day: Wednesday Oct 6th at 11:00 am EDT/ 5:00 pm CEST/ 8:30pm IST

* Live stream on [YouTube](https://www.youtube.com/watch?v=KULzKh2H8XA) and [Twitch](https://www.twitch.tv/perconalive)

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=NjIzMGF1YTgyZnRzdTZqNmg1ZmN2bTZzZGNfMjAyMTEwMDZUMTUwMDAwWiBjX3A3ZmF2NGNzaWk1ajV2ZHNvaGkwcTh2aTQ4QGc&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com&scp=ALL)

## Agenda 

We will meet experts to cover two different topics:

### “MySQL Basics for Prod Environment” by Vaibhav Upadhyay

1. OS basic parameters to be taken care (system level).
2. Monitoring configuration (PMM or Zabbix).
3. Using the right tool for backup.

### “MySQL Audit Logging” by Wayne Leutwyler

1. Why use it?
2. How to enable it?
3. How to view the output?

The Percona Community MeetUp is a Live Event and Attendees will have time to ask questions during the Q&A. All kinds of feedback are welcome to help us improve upcoming events.

## The MeetUp for MySQL is recommended for: 

* User of MySQL

* Student or want to learn MySQL

* Expert, Engineer, Developer of MySQL

* Thinking about working with database and big data

* Interested in MySQL