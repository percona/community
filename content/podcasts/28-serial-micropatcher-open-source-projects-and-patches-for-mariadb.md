---
title: "Serial Micropatcher of Open Source Projects and Patches for MariaDB - Percona Podcast 28"
description: "Daniel is a self-professed serial micropatcher of open source projects. He is passionate about all things performance, understanding how things work, and has worked tirelessly on porting coding for POWER Systems."
short_text: "Listen in as the HOSS talks with Daniel Black, Chief Innovation Officer at the MariaDB Foundation. Daniel is a self-professed serial micropatcher of open source projects. He is passionate about all things performance, understanding how things work, and has worked tirelessly on porting coding for POWER Systems. He was formerly a DBA consultant for Open Query where he started writing far too many patches for MariaDB, a tradition which he continues today, and ultimately led him to become the Chief Innovation Officer at the MariaDB foundation."
date: "2021-07-08"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-28-with-daniel-black-chief-innovation-officer-at-the-mariadb-foundation/"
youtube_id: "3w7mMsSYn3Q"
speakers:
  - daniel_black
  - matt_yonkovit
aliases:
    - "/podcasts/28/"
url: "/podcasts/28-serial-micropatcher-open-source-projects-and-patches-for-mariadb"
---

## Transcript

**Matt Yonkovit:**
Hi everybody. Welcome to another HOSS Talks FOSS. Today I'm here with Daniel Black from the MariaDB Foundation, the Chief Innovation Officer for the MariaDB Foundation. How are you, Daniel? 

**Daniel Black:**
Good. Thanks, man. Working up, got my coffee. Welcome to Canberra winter. 

**Matt Yonkovit:**
Yeah, and it's really early there. Right. So what time is it?

**Daniel Black:**
Only 7:30am.

**Matt Yonkovit:**
Okay, so the sun is just picking up? 

**Daniel Black:**
Yeah, yeah. 

**Matt Yonkovit:**
Okay, true. Okay, and are you on your roof? Is that what I see you on?


**Daniel Black:**
My hammock, standard outdoors thing. I tried to actually do presentations outdoors, as you probably seen in some of them, just to add a bit of a variety. And this is my casual backyard look.

**Matt Yonkovit:**
Yeah. So you had spoken recently at Percona Live, but you've been speaking at conferences for quite some time. I think this is probably your sixth or seventh Percona Live that you've spoken at? 

**Daniel Black:**
Probably, yes. 

**Matt Yonkovit:**
Yeah, you've done quite a bit. And typically, you tend to really go deep into those nether regions of the bugs, the code, you find those hidden problems and like to expose.

**Daniel Black:**
Yeah, absolutely. So it's a fascination, or I got far too much when I was employed as a DBA. And sort of ended up looking far too much code. And getting to the end of the day is like: “Oh, I can't build the client this, but it was fun anyway, but yeah, I'm glad I've got a job where I can actually do both”. 

**Matt Yonkovit:**
Well, yeah, that's awesome. That's awesome. You did quite a bit of work at IBM as well, before the MariaDB Foundation, right? 

**Daniel Black:**
That's right, let's say for four years. 

**Matt Yonkovit:**
Okay. So that was a lot on the power platform. So kind of making MySQL work. 

**Daniel Black:**
Yeah, MySQL and MariaDB on power. A lot of it was generic, it was just making use of all the sudden, you got 256 virtual CPUs and, and once you get to that level, you start to see problems that you don't kind of see on laptops and other kinds of development environments. So it's good to get out just performance testings and find little bugs. And a lot of them actually got in is like generic improvements. So they helped all platforms which is really good when you're trying to actually set a fix that people got power. It certainly helped power and it certainly helped everyone else as well. 

**Matt Yonkovit:**
Now, I'm sure that going through all of those, the code and trying to optimise on a large scale machine like that, you probably run into some things that you're like: “Oh, my God, I don't believe that this actually did this”.

**Daniel Black:**
Yeah, yeah. And “Who wrote this?” or “What is this bit of code?” So yes, there is a bit of that. It's a code base with a unit 20 plus year heritage, there are some bits that you not go in and people just haven't got a need to look at it again. And you look at it again and this a system call that it does this or glibc does a memory copy… Okay, there's no need to actually implement your own. 
There's a bunch of custom mutexes as like, okay, they may have been needed one stage, but in some ways… This part of standards now, so we won't move on. 

**Matt Yonkovit:**
And that's one of the weird things with software as old as MySQL and even Maria now has some age on it, because it's been around for a while now. The machines and the hardware, and that the kernels change drastically over that time period. I mean, the original MySQL was written when single core machines were mainstream. And you had 128 megs or 256 megs of memory on your big boxes, right? Yeah. My favourite line of code and all of InnoDB was when hecky hard-coded 100 IOPS per second. And the comment was “This is all modern disk will ever do”. So I mean there's a lot of those issues, that kind of lurk there. 

**Daniel Black:**
I saw Marco actually exasperating on another hanky comment the other day.

**Matt Yonkovit:**  
Oh, did you see it? Which was it?

**Daniel Black:** 
It was something like this a hardware bug or something else is like, you're just guessing and you put this in an error log message, come on. Let’s get back.

**Matt Yonkovit:** 
So when you're going through and trying to modernise, I mean, that's a tough process. Because  there's the mentality of sometimes when it's not broke, don't fix it. But at the same time, there is quite a job, a lot of stuff there. So as you approach these, is it more of as the problems crop up that's when you start to like look at those another regions of the code? Or do you just go on vacation and print out the source code to look at it as a nice book?

**Daniel Black:** 
Yeah, roll around on the beach... I mean, sometimes it's going through and grabbing perf files and looking through and other times, it's like I'm looking at a performance from elsewhere. And it's like, oh, what's that meant to be doing? I mean, another one I have not got for ages is this randomization function is like... this is using a bunch of constants. It's got some global lock on a variable, because of statement based replication, and we've got to support that. But really, it's like get a random number, it shouldn't have a concurrency problem. I haven’t tackled that one. But yeah, there's certainly that kind of thing. There's also a lot of code base, that's like, okay, we're gonna pack this down byte by byte right beside each other. And so modern CPUs and part of my time at IBM sort of aware that that's not always the best way. So, yeah, it's a bit of just coming across things and playing a bit of experience and playing a bit of perf knowledge. And, yeah, seeing what can be done. 

**Matt Yonkovit:** 
So in your toolbox today, I mean, the tools have evolved as well. What are your favourite kind of tools that you use to debug and find some of these issues? Like, what are you using nowadays, 

**Daniel Black:** 
I'm still using fairly old school, like you see, makes your GDB's, and that kind of thing to get through it. On the performance stuff, I guess, perf has been around for a while, but as a sampling, it still does a pretty good job on things. As we're going through in doing kind of benchmarking, some times like BPF trace, just to get that kind of timing between different points of OI speed of what exactly is going on between things to get measurements, between points on latencies, and that kind of thing, that sometimes perf doesn't show up as well. And that you need more CPU analysis. And there's your flame graphs and stuff as you need to try to communicate how horrible something's really are. 

**Matt Yonkovit:** 
Oh, yeah, no, I got that. So you still do spend some time in your current role doing that debugging, right? And performance tuning? 

**Daniel Black:** 
Yeah, absolutely. I mean, probably not as much as I was before. But certainly, the issues of bugs coming in every now and then it's good to just go through and work through the interaction with the customer and client. Not customer… Just general community user and see what they're going through, try to get the right information out of them and try to go through and sometimes it's: “Oh, Jesus, yep, you right. That's easily fixable”. Just before 10.1 end of life, late last year was like looking at if you kill off a MariaDB process under some conditions, you weren't actually getting an error message. Sorry, an error response in the SQL error is like, yep. Okay. Quick, last little fix into 10.1 release. That was while looking at another bug. 

**Matt Yonkovit:** 
So what are you spending your time on? Like, so? So you're doing that a little bit? It's kind of backed off a bit. So as the Chief Innovation Officer, what kind of things are you working on nowadays?

**Daniel Black:** 
I was doing a bit on system D socket activation, which was a little bit that I started years and years ago when this was the my days it was Oh, dear, we are running out of money, but, Jesus, it is fun writing it. So this is about when I actually added the system D support into MariaDB, this socket activation was an additional add-on. And what that means is the system can listen to the socket. And when it gets connected, it can spin up the instance of MariaDB. So not a total everyday use case. But if you're doing a MariaDB instance for a user, that's, I guess, one way to in a multi instance, to spin it up that way. It's probably about five years, a little bit too late there that containers and clouds get that way. But it's another approach of doing it and keeps the abstraction at that kind of process level. 

**Matt Yonkovit:** 
Yeah. And you mentioned containers, I mean, everybody seems to be investigating running on containers, Kubernetes. That's the new exciting thing for most people. So, how much work are you delving into there to try and tune and optimise?

**Daniel Black:** 
Recently I actually took over the MariaDB docker library container. So, a lot of work there, I am
doing the sensible thing, that prompt is like writing a test suite for the lead entry point. So I finished that this week. So that's all integrated into the GitHub actions there. Got a starting point, now I can feel a bit more comfortable actually ripping about parts and changing that, to just preserve the compatibility. But as you look into things like that it's the same sort of thing, you see that you're doing in this entry point a lot of workarounds for either Debian packaging and the MySQL is still DB script that is very ancient, and probably could actually use some more modern features that sort of map to how it's used in containers, but also just packaging scripts in general.

**Matt Yonkovit:** 
And so like, when you talk about those types of tools and trying to update some of those packages, I know, Maria DB is very eager to work with a community on contributions. What sort of things are you looking for help with? How can people get involved?

**Daniel Black:** 
We’ve got a GitHub account, and you could just send a request to there and we'll work through and merge code, we get a lot of code actually contributed from distro maintainers. The NetBSD’s, the FreeBSD’s is just to add that little bit of extra portability to make them happy and get that working. There are things like what I mentioned, that are just improvements and things that can get going. There is also, I guess, good a knowledge base where you can write documentation. We've got a Zulip channel, MariaDBorg, where you can just like a Slack channel, it's a chat programme, where you can come in and talk to us about bugs, features, that kind of thing, or just SQL problems, really. If you get us at the right time, we'll happily look through those and, and get a bit of insight into what you're doing.

**Matt Yonkovit:**  
Cool. Yeah. Now, changing gears just a little bit, at Percona Live this year, you gave a talk specifically on using MySQL dump, as a or MariaDB dump, in this case, as a way to migrate back and forth between MySQL and MariaDB. And we know that many people use Maria and MySQL interchangeably. And so I don't want you to give your whole presentation.
But that is recorded and it is available. And maybe give us a little bit of an idea and why this topic was interesting about it and why have you seen people try to do this.

**Daniel Black:**  
So, I guess people use the backups for ages and the MySQL dump has outputted a table of like mysql.users. And it's got these rows and columns of what constitutes user data. But as we're seeing in the development of both MySQL and MariaDB, that these tables actually changing, quite common. So the aspect of dumping out a one version and importing into another version, especially if you're doing a partial import, or an additive import, that's not actually mapping up to the table structure. And B, if users have actually gone through that and started to work out which column means what I mean, that's just a bunch of hurt that users don't really deserve. So this, like the SQL syntax, like create user that sort of provides a portal way to create a user, strangely enough, isn't that sql was made - portability? So yeah, what I did with MySQL dump, and in the later versions, 10.4 plus, MariaDB dump is an alias because having two things in the ecosystem of the same name is, it's just confusing enough, especially once they start to become different. So added those features. So we've got MySQL dump or MariaDB dump test system equals, all users stats, various aspects all in that MySQL system database, and now it puts in a portable form.

**Matt Yonkovit:**
Okay, that enables you to move it back and forth with ease. 

**Daniel Black:** 
Yeah, absolutely. And so the objective in outputting some of those was to write the SQL. So it's portable, because there are some minor differences. And what MySQL and MariaDB done for ages is that they've had an executable comment syntax. So we've got in this version there. You're allowed this syntax in versions before it, and so made extensive use of that to bridge the portability gaps between the two.

**Matt Yonkovit:**
Cool. And let me leave you with this. I always like to ask people, what are they seeing? I like them to look into their crystal ball from their technologist perspective,what are you seeing coming down the pipeline technology wise, that you're excited about? What are you starting to get interested in? Are there certain things that you're really looking forward to kind of deep diving into?

**Daniel Black:** 
Yes, absolutely. It's a lot of maintenance, like, more cause, more memory. And it's like, how do you deal with that, but there's also, okay, we've got larger workloads that are growing beyond their eye speed, or beyond their memory capability, beyond the number of CPUs, so really interested in seeing how that transforms the code base and, and starts to take advantage of things such as Postgres and MySQL have done and starting to use multiple threads for a single SQL query to break them up and to do sorting to divvy up the layers. As you know, there are now more than 100 IOPS possible on disk. So, running it in a single thread... Yeah, we can do better, we can do better. And things like NVMe, is they've got huge capabilities to do asynchronous IO, on disk.

**Matt Yonkovit:**
And then I think the faster that technology gets whether it's just disk IOPS or memory performance or larger memory footprints or even quantum computing, which is around the corner. All of that drastically changes those restrictions that you started our discussion with, right? So, those things where we say like, Oh my god how could you hard code something for 100 IOPS a second? How could you put in this weird mutex? All those things, we're gonna say those again in five years or 10 years just because the technology has leaped so far. Right? Because we're gonna be like, why aren't you using this feature, this function that the capabilities of the system? Why are you handicapping yourself? 

**Daniel Black:** 
Yeah, and on other hardware features… I mean, numa have been around for ages. Do we do anything specific better? Not really. That there's probably avenues to start to split that up. Assisting that in the glibc development this week or last week, there was version four of a futex (2) system call that actually has numa capability. So you can do locks. But I say I'm doing a lock, but I know it's only on these particular nodes. And that allows you to write much more scalable code up in that way.

**Matt Yonkovit:**
Well, Daniel, thank you for sitting down with me today, talking to me a little bit about what you're working on, where things are going, talking about some of those crazy bugs. And if you haven't checked out the Percona Live session, it should be available on YouTube, under the MariaDB community room. But Daniel, we appreciate you hanging out with us today. 

Wow, what a great episode that was! We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.
