---
title: "Database Monitoring Management, Alerting, Contributing MySQL, TiDB, and Waffles - Percona Podcast 04"
description: "Join the HOSS (Percona’s Head of Open Source Strategy) as he talks with MySQL and open source veteran Morgan Tocker about open source development, how we both got started in the open-source business, how people can contribute, and some of the cool things he has been up to."
short_text: "Join the HOSS (Percona’s Head of Open Source Strategy) as he talks with MySQL and open source veteran Morgan Tocker about open source development, how we both got started in the open-source business, how people can contribute, and some of the cool things he has been up to."
date: "2021-02-18"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep04-featuring-morgan-tocker-talking-mysql-tidb-open-source-contributions-and-waffles/"
youtube_id: "T2t0YeHMeqU"
speakers:
  - morgan_tocker
aliases:
    - "/podcasts/4/"
url: "/podcasts/4-database-monitoring-management-alerting-contributing-mysql-tidb-and-waffles"
---

## Transcript

**Matt Yonkovit:**  
Welcome to another episode of The HOSS Talks FOSS. We're here to bring you some of the awesome news in open source. Let's get started. We hope you enjoy the show. Hey, Morgan, glad to see you here. I saw you move back to TiDB. How are things going there? What are you working on? what's what's, what's the scoop?

**Morgan Tocker:**  
What's the scoop? I'm working as a developer, which actually, I haven't done, I think for 15 years or so. With COVID coming around, I kind of took the opportunity to do fewer online events and kind of figure out what I wanted to do and TiDB has always been a fun project for me. So I joined the SQL Engine team. And at the moment, I'm working on some security features, which is interesting. I never thought that I'd be working on security features that secure

**Matt Yonkovit:**  
Honestly, I want to protect my data. But Security does seem a little boring. I mean, like I mean, it. Maybe it's cool. Like, is it cool? Do you like it?

**Morgan Tocker:**  
I think it's cool, because it's sort of like a Time book. Maybe I might not always be working on it.

**Matt Yonkovit:**  
Okay, all right. Fair enough. Fair enough. Fair enough. I mean, you've been around the open source space longer than I have. And I've been here since like 2007. So you've been around. Yes.

**Morgan Tocker:**  
I think maybe I've got a year on you.

**Matt Yonkovit:**  
Oh, well. Yeah. Okay. But I mean, like you, you've had quite the career, you've been able to sample many different things in many different areas. So yeah, that's exciting. And I know coming back to TiDB, you were able to jump right in and do some hackathon work, which sounds pretty cool to tell me about that. Like I heard, it was like a giant prize, but they wouldn't give it to you. Even though your stuff was wasted. Period. Everybody else

**Morgan Tocker:**  
Right. Yeah. So last weekend, actually, we had a hackathon. I think it's an annual event that pickers organize. But no, I participated in hackathons before just small scale projects. Maybe you win a bag of coffee or something like that for participation. But no, not this one. The price, I know what it is in US dollars, I convert it to Canadian dollars. And it's like $20,000 First prize. Wow. This is like some serious entries. It's like a day and a half that you're hacking on a feature to try and improve TiDB and leapfrog it in some area that you might not otherwise be working on. 

**Matt Yonkovit:**  
So, is that like just for the company? Or do they open that up to everybody,

**Morgan Tocker:**  
They open up to everyone. So I had a team, there were four of us on the team. It just so happened the three of us work for PingCap, and no one from Tencent. So we chose to implement events, similar to the event scheduler in MySQL, but for TiDB .

**Matt Yonkovit:**  
Oh, very cool. Very cool. And, and I saw you were working on being able to backup directly from that event schedule.

**Morgan Tocker:**  
Right! Yeah, that was my, that was my sort of proof of implementation in a way. So MySQL has backup for the backup is an SQL command, sort of like an external tool, but in TiDB  the backup is just like the backup command or the restore command. And so combining it with an event scheduler just with a SQL command, essentially, you can schedule your backup schedule for every day at this time. And the backup can stream directly to s3 as well. So it's kind of like you're on AWS, configure the AWS command line, you set up the credentials for s3, or maybe if you're operating in Amazon, you use a profile. But then it's just the same command for everyone to be able to set up your backup and it just keeps on running on a schedule.

**Matt Yonkovit:**  
Yeah, it's very cool to be able to back it up directly from the SQL command line. Because sometimes you don't have shell access. Sometimes you can't do certain things. I mean, like nowadays, especially with all the security concerns people locked down things that are crazy. So yeah, it's a very cool project.

**Morgan Tocker:**  
That was kind of part of the idea, right? Like, you can do a cron job, it's not replacing that. But which machine would you put it on ? TiDB   server is stateless. So if you kind of install on one of their servers, then you're losing that property. You put on all of them. And then you have to add a property to make sure that only runs once. So it's just kind of architecturally elegant if the server can actually provide that feature itself. 

**Matt Yonkovit:**  
So with it being distributed, so does it then propagate to all the nodes to backup?

**Morgan Tocker:**  
yeah, the way it works is kind of cool. So you say the TiDB  server, which is the stateless SQL pod, started back up. And then it speaks to all of the TiDB   servers and kind of aligns the needle, if you will, of what the snapshot point will be. So very cool. Each of those servers actually directly streams that backup to s3, essentially, it doesn't pipe back through the TiDB    server. It doesn't have to.

**Matt Yonkovit:**  
Oh, wow. Okay, I think so then you'll get a consistent snapshot across all the nodes.

**Morgan Tocker:**  
Right! And you don't have to have, like, all of the space locally to be able to store a backup in what's database essentially designed to be very large. Because I think that wouldn't really work for clouds either.

**Matt Yonkovit:**  
Wow, that's, that's very cool. And when is that going to be in production? Come on, when is it gonna be in production?

**Morgan Tocker:**  
I think that's above my paygrade these days. Oh, all right. It's a hackathon feature. But actually, no, I mean, I like the actual backup command. I mean, it's already there. its entirety before, that's when it was introduced. It's the scheduling part that is above my paygrade, where,

**Matt Yonkovit:**  
Oh, well, well, maybe this will put pressure on me to get it in. Let's see! what we can, we can probably learn how to do that and use something similar in the MySQL General space.

**Morgan Tocker:**  
I think the pieces are there in MySQL, right? Like the Clune plugin works inside the server, it's possible to add a scheduling layer on top of that the event systems are already there. I would love to see something like that. 

**Matt Yonkovit:**  
So whether it's a hackathon or something else, how do people get involved in contributing code or starting to maybe look at helping out with hey, I've got this idea . How do I help get that implemented? I mean, you've been around this space for long enough where you've touched so many different components. I mean, that's, that's got to be something that you might have some advice for some people on.

**Morgan Tocker:**  
Yeah, I think for me, at least this time around, it's been a bit of a passion project. I have kind of got that opportunity to work on what interests me. But I think the same is kind of true for people starting out if you have good writing skills, take a look at documentation, this plenty of issues to fix in, in projects there. If you have feature requests, so you see feature requests, you can kind of validate them and help reduce duplication of existing bugs in the system. I think that's a good way to get involved. And then if you have coding skills, that obviously you can work on that too. But I don't want to start with that assumption, because I think that's just the natural way that people think and I think there's so many ways, ways, you know.

**Matt Yonkovit:**  
So, being a veteran of the space, what do you see in that, that kind of the open source space that either excites you or makes you really sad and want to cry? Either one, either one.

**Morgan Tocker:**  
Yeah, I mean.

**Matt Yonkovit:**  
Oh, I did, did I get a loss for words with it?

**Morgan Tocker:**  
I like to be a positive person, sir. There are plenty of things that are very silly that you don't want to touch. But I think what excites me is every time I see people understand, like usability of in the case of where we were trying to implement, backups, virus schedule, obviously, you could do that with Cron. And I think what excited me was when I chatted to my teammates, and we decided we want to work on this, and they all sort of had that same vision. I think, sometimes we kind of underestimate that simplicity wins. And every time I see that spark, I think that kind of excites me. And I think that expectation of how simple something must be, is kind of the Base is getting higher, and I get it. I like that challenge. I think that's really valuable for everyone.

**Matt Yonkovit:**  
Well, that type of challenge is something that excites people with that passion. I mean, that's really what drives a lot of people in the open source space, right. I mean, I think that's why I got started. I think everybody's looking for that niche. And to begin, you gotta start somewhere, right? And if you have an interest you want to like, this doesn't work, right? I want to solve this problem. I think that's often overlooked and that passion about a topic or two is what really makes the open source space so great, because you could just grab it and run with it. I remember my first hack, if you will, the first project I got into. What was that? Oh, you're gonna bring a waffle. Great. Oh, no, it was actually more awful a grid. But the waffle grid was pretty cool. Okay, well, the waffle grid was pretty cool. No, I actually built a patch to disable statistical, automatic statistic collection within InnoDB because I was working for a company that had oodles of tables and oodles of data and the index collection would refresh Too often in script all the query plans. So it was something to disable it and to make some changes there. And it was boring because it was like, I'm annoyed that this thing keeps on happening. Right. But the waffle grid was yes, it was a passion project for a while. Me and Me and Eve. Yes. I can't believe you remember that. But, yes. Oh, of course. Yes. It was the predecessor to all other clustered in memory databases. It was light years ahead of its time.

**Morgan Tocker:**  
Yeah, I'm sure times 10 is infringing on some patents of yours. Well,

**Matt Yonkovit:**  
you know, hey, hey, sir. Yes, that's okay. That's okay. It was solid. We actually had one person run it in production. Do you remember who it was?

**Morgan Tocker:**  
No.

**Matt Yonkovit:**  
It was Kenny Grip.

**Morgan Tocker:**  
Okay,

**Matt Yonkovit:**  
And I'm like, you ran this in production? And he's like, Yeah, I just thought I'd try it. It did work. You know. So it's like, Oh, my God.

**Morgan Tocker:**  
Do I find that I learned some interesting things? Like, I think originally, you're using the LRU. But it doesn't kind of work in a way that you kind of want. When you got to LRU sitting on top of each other. They don't work together, because something might be really hot in one and then it looks really cold to the other one.

**Matt Yonkovit:**  
Yeah, yeah. So there were some issues with that. We tried to rewrite it a couple times. And then we just moved on to other things. I mean, yeah, yeah. Although, it did generate a very similar thing, because someone took the code and moved it to Postgres. And they did something very, very similar to Postgres, which actually, I think still exists today.

**Morgan Tocker:**  
Yeah, I think the idea is solid, like, I apologize, my, my snackbar, I actually think that you could do something similar where you could run like, InnoDB on top, or something alike.

**Matt Yonkovit:**  
Yeah, and just so everybody who's listening, who isn't familiar with waffle grid, and went to the Wayback Machine to, like, look at what waffle grid was, it was a distributed second memory cache that we built for InnoDB, where, when pages would get kicked out of memory, they would actually go to a memcached D server. And so then we could pull off mem cache D, as opposed to pulling off disk. But now with SSDs, and the speed of SSDs. Doesn't really matter as much, right? Because that network speed plus a pole from an external memory. it's, it's questionable, depending on the speed of your disk and the setup. So it was a book before its time, and it faded quickly. Let's just put it that way. I'm sure we all have those closed projects that were like Oh, yeah.

**Morgan Tocker:**  
But I learned a lot in the process. And that's kind of where it's still fun.

**Matt Yonkovit:**  
Yes, I did. In fact, I remember Stuart Smith actually said to me and Eve like, after that project, we were, we were chatting, and he's like, Yeah, you and Eve are one of like five people who actually know what InnoDB does. At that time, which was kind of cool. Like, oh, oh, that's, that's very cool. And then, I stopped looking at the code, and then I lost all those skills.

**Morgan Tocker:**  
yeah. And I think for others, like, as I said, I, I kind of learned more about InnoDB by following your progress.

**Matt Yonkovit:**  
yeah, I think that's cool, right. I mean, that's the power of open source, though, if we can go out there and we can try cool things and learn from one another. And that's one of the things that kind of excites me and wants to make sure that other people do have the opportunity to learn from all of us. And whether that's the project in the hackathon that you're doing, it's something that we're doing at Percona. We've always tried to be very open about collaboration and sharing. So that's why I'm excited this year, because this year, the focus is really on what we can do to bring more collaboration, bring more visibility, to get people to learn from different ideas and help the community move forward.

**Morgan Tocker:**  
I have another suggestion on what you can work on.

**Matt Yonkovit:**  
So I'm waiting for your suggestion.

**Morgan Tocker:**  
You have more experience than you realize, like I think, as a database developer, implementer you might not have that production expertise of knowing what solution you're you're solving. I think the production people if they work on tools, like you can see in a tool if somebody really understands what the problem is. And I think this is why people have such great tools, right that they have experience in that validation.

**Matt Yonkovit:**  
well in the tooling is super important because it's it's, it's the problem solving, right? everybody's about like, troubleshooting, optimization observability now, right? It's the observability generation, because nobody can have one database anymore, they have to have all 1800. and so to find that needle in the haystack type thing is hard, right? I mean, it really is so,

**Morgan Tocker:**  
But I also have a suggestion for observability

**Matt Yonkovit:**  
Oh, no, feel, hey, we have as much time as you want to provide.

**Morgan Tocker:**  
Let me give you the pitch. Right. Okay. So currently you can see how slow vos pages load, you can see how fast queries off and you can use pt query digest, so you can use performance schema. But what if the database could give you a transaction analyst view, view with the transaction kind of being named. So you say for logging in these, this is the breakdown of queries, this is the time of the whole transaction. And this is the CPU time, essentially, how much time is spent on queries.

**Matt Yonkovit:**  
So you're talking about a kind of roll up based on the transaction, so if it has 10 queries that are part of that transactional state, there would be some tag or some mechanism to roll that up and consolidate it. And I mean, it's originally I think of that as almost like a tree structure, right. And so you've got transaction 123. And then if you click a button on the UI we'll go to the UI, it would then expand out and show you all the queries that were part of that. And then if you had any nested transactions, or anything, that it would kind of just continue to dive down. Yeah, that'd be kind of cool. I know that there are several projects working on commenting SQL code, and, and being able to inject things through , or through other mechanisms to start doing some tracing. Because I think it's also important to get back up. Yeah, even beyond the transaction, because the transactions are one level, but think of like like, like what New Relic does, or app dynamic does with some of the applications being able to say this function, or this page had this thing. I mean, I remember, I'm gonna date myself, way, way, way, way back, I actually went and did a consulting gig for someone. And they're like, oh, we have so many performance problems that they did testing for, like, accountants and lawyers, right. So you had to get certified every year, and their certification window for the year for, I forget what it was, was coming up. And so they're like, Oh, my God this thing takes like five! Yeah, it's like, for one week, every buddy in that industry has to take this test. And they're like, Oh, my God, this thing takes like, five minutes, and you go, and you look at all the queries, and they're all like 100 milliseconds, 200 milliseconds. I mean, there's nothing there. And it's not until you look that a single page generates 45,000 queries that you realize what the hell is that? Right. Right. And, and it's that aggregate view, and how you get that is super important.
