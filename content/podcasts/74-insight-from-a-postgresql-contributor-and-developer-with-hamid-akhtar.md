---
title: "Insight from a PostgreSQL contributor and developer: Ep 74 of the HOSS talks with Hamid Akhtar"
description: "Join the HOSS as he talks with long-time PostgreSQL contributor, community member, and current SR Software Engineer at Percona, Hamid Akhtar.  Hamid and Matt dive into PostgreSQL development processes, talk about the future of PostgreSQL and talk about tuning, monitoring, and Observability with pg_stat_monitor."
date: "2022-06-15"
podbean_link: "https://percona.podbean.com/e/insight-from-a-postgresql-contributor-and-developer-ep-74-of-the-hoss-talks-with-hamid-akhtar/"
youtube_id: "a_-0Sh6N2BQ"
speakers:
  - matt_yonkovit
  - hamid_akhtar
---

## Transcript

**Matt Yonkovit**  
Hey everybody, welcome to another HOSS Talks FOSS. I'm the HOSS, Matt Yonkovit, here at Percona. I am here with Hamid Akhtar today, our Senior Software Engineer involved in all things Postgres. How are you doing today Hamid?

**Hamid Akhtar**  
I am doing very well. Thank you for having me.

**Matt Yonkovit**  
Great. Great. Great to hear now. I mean, you have been in the postgres space for oh, gosh, over 10 years now, right?

**Hamid Akhtar**  
Just over 10 years.

**Matt Yonkovit**  
Yes, yes. Yeah. And so you've worked at other companies, like EnterpriseDB. You've worked in the postgres space in a variety of different roles. And so and love Postgres through and through.

**Hamid Akhtar**  
Yeah, I mean, I'm beginning, I started off, not really liking the community and not really liking the software. But then gradually, as you work together and understand the ecosystem, that's when you establish a respect for people who put in so much effort and time and give so much back to the community in form of open source software that you begin to appreciate the amount of effort and dedication people have for this project, and the projects around it. So it's really how this project has evolved over the years, that I see and appreciate it more. Looking at it from like, in fact, my first experience was back in 2007, when I joined EnterpriseDB as part of the database core team. Then there was a gap. I rejoined in 2011, I think. And that's really, when I started to really dig into Postgres, I understand. From looking at it, I mean, from 90 onwards, and supporting all different kinds of environments. I mean, not just Linux, but HP UX on Itanium, Solaris park, you name it, and you you had it.

**Matt Yonkovit**  
And there's a lot of eclectic things you have to do to get some versions and some OSS to kind of match up, right. I mean, that's, that's kind of a pain.

**Hamid Akhtar**  
That is I mean, the the other thing that the community did, I mean, they could very easily go the easy route of just picking up GCC and building it on linux unix based variants. But the effort was done to ensure that you use the most optimized compiler and the tool chain on a particular OS. So you have for example, on PowerPC, is you have their tool chains for IBM by IBM. So you the advanced tool chain, so you basically use those specific environment specific options, take the pain, keep out a lot of sweat, while trying to figure out why it's not working on this environment, what's working, what's not. But that's really the good thing about Postgres is that it's not taken the easy route in any way. It's taken the big steps, the big challenges, and it's gone through and come through pretty well.

**Matt Yonkovit**  
I mean, it is a tried and true stalwart of the database space now. It continues to grow in popularity, and more and more folks are turning to it over a proprietary solution.

**Hamid Akhtar**  
Yeah, I mean, that's, I think the openness of the community is what really helps. It gives people the confidence that they, they're never left. At anyone's discretion, they always can go back to the source code, they they have the option to know what's running on their system. There are no hidden things in there. So it gives people a lot of confidence that what's going on what's happening, how they can manage, and there's always a fallback option of somebody just picking up the source code and looking into and doing things.

**Matt Yonkovit**  
Yeah, it I mean, it enables you to kind of delve into all kinds of different areas and figure out what works, what doesn't work. And then as people have needs, it evolves and people can contribute code and they can contribute tools. And that's where a lot of the work here at Percona has started. Right. So we look at Percona is evolution and part of the Postgres space and you coming in, what have you been working on here at Percona for the community?

**Hamid Akhtar**  
so one of the project that one of the big projects that we're doing here, pg_stat monitor, so I start with that. And it's a project that I expect to grow significantly, and even maybe in parts gets picked up by the community, whether that becomes certain features become part of PG stat statements. But it's a project that has a lot of potential. I've spoken to a number of people from pretty significantly large companies who are, who liked the project, who want to use it. But so it's, it's really, I think, the GA is expected in fact today for PG stat monitor. So it's a big day in terms of pg stat monitors release.

**Matt Yonkovit**  
Well, today as of the recording, because this will be probably a couple of weeks after it's released. So it'll only be out there once. Yeah,

**Hamid Akhtar**  
Exactly. So yeah, so I mean, it's really a big project in terms of how you observe query and performance and Postgres server. But beyond that, what I've been really working on is I'm working on a couple of patches. So hopefully, I'll be able to cook up something. There is one for agents back. There's one for Postgres server. There's small patches, small fixes, small improvements. And then obviously, it's just about some level of evangelism, whether that's through talks, or whether that's through blogging, and highlighting the features. The key features and performance related features are really, what kind of really challenges me in terms of improving how good we can make the server run. So go ahead. Yeah, I was just going to say other than that, I mean, I've I've had pretty decent experience with packaging and installers with Postgres. So, in fact, in the past life, I had one of the organizations I was leading the team, which was responsible for shipping out the one click installers for Postgres, the official installer, so we were always there, building those installers for all different platforms, making sure that on Thursdays between one and two UTC, were able to ship out an update stack builder catalogs and publish those installers. So it's, it's always kind of like a great organization, the community that it works together ensures that things come together. There's a predictable pattern out there that people can depend on. So it's evolved, and it's improved. And yeah, I continue to look into the packaging side of things. Not really that actively but just reviewing it from rpm perspective. So yeah, there's good things out there.

**Matt Yonkovit**  
Good, good mix. Well, let's go back to PG stat Monitor for a second because for folks who may not know what PG stat monitor is, let's give them kind of a little baseline. It is an extension to Postgres that allows you greater data and statistics on your queries that are running. It's a little different than PG stat statements. So PG stat statements, is a tool that does something similar. But I think the big differentiators that I've seen within PG stat monitor are really the focus on not only being able to look at what queries are running, but looking at them in time series buckets, so you can look at them over the course of time, you get more statistics. In fact, there's like 19 additional fields that are available in PG stat monitor, and the ability to get things like histograms of the query. So you can see if hey, 90% of the queries run in 100 milliseconds, the other 10% run in 10 seconds. That's something that's kind of important. And you need to understand.

**Hamid Akhtar**  
Yes, in fact, this is one of the things I'll be discussing in my talks about query performance insights because PG stat monitors started off on basically PG stat statements. So it kind of inherited a lot of the details from it a lot of the statistical information, but then based on that, it kind of stitch together a bigger picture with time series, and beyond that the connection related information and as you mentioned, histogram, the plan and the plan with the parameters. So the other query with the parameters so that you can actually dig into what what has happened. Those are really key things when you look at PG stat monitor as an improvement or as an observability tool, because the thing with PG stat statement is that it's brilliant in terms of the statistical information it gathers, but where it lacks blacks behind is that it's an accumulation of data. Anomalies over a period of time can disrupt those statistical informations whether they say, a query that runs in one second, and for some odd reason, because of a log because of some other issue, it took an hour. Now, that means completely offset all your statistics. But in a time series data set, if we disrupt that one bucket, that one window of time, but it will not disrupt the other data. So that means that you still have a better picture as to how that query is behaving. So you don't have to reset your entire statistics, you get that piece of information. So that's, that's where I think the observability improves. It's more like, when I discuss it with people, I say it's more like the source tool on Linux, which can help you identify based on time of the day, what how the system was behaving. So you just have that statistic. And so information is on, say, the day or the time when you think that when expect whether there wasn't other load on the system, and it should run fine. Rather than just having an accumulation of numbers. So it's, it's really, I think, a good starting point. And a really, it's kind of something that people will eventually be using, quite significantly in their environments.

**Matt Yonkovit**  
Yeah, and I think that this, this goes hand in hand with the change that I've seen in modern applications, right. So observability is the name of the game in most environments. Now, because people aren't running a single server, they're running hundreds. And that means that if you've got hundreds of Postgres instances, the odds that you're going to be able to go in when there's a problem and find it immediately, are pretty slim. So it's really about finding that needle in a haystack or finding the one thing that's causing the issue. And it's that one thing that was causing an issue maybe 20 minutes ago, or an hour ago, which makes it even more difficult, especially if it's a transient problem. So the more details you can get, the better off you are. And that's why tools like Grafana, or PMM, or data dog or fill in the observability tool of your choice, have really grown in popularity because of the environments we're in.

**Hamid Akhtar**  
Yeah, and obviously, this obviously, directly translates into cost savings, whether you are on a cloud or on premise, whether it's reduces load on your hardware, eventually, that's where you want to go. Because if you have hundreds of systems, and you have a 10% performance degradation, and you're not aware of it, that adds 10 new nodes into your system, that's a significant overhead. And even on Cloud, I've seen people who think that their costs should be half of what they are currently paying for.

**Matt Yonkovit**  
Does anybody really say that? No, no, we're paying a fair cost? No, of course not. They want less money, right? They want to spend less money. So there's always pressure to spend less, I think that's a universal constant let us spend less money.

**Hamid Akhtar**  
True, that's very true.

**Matt Yonkovit**  
But no, going hand in hand with this type of change in environment. You mentioned the one click installers that you've worked on in the past, that's all changed. And now, there's so many tools like databases of service tools in the cloud, where it is one click. And it's not only installing it, setting everything up and getting it running and configured out of the box. And now you've seen that kind of extended down to Kubernetes, as well and running up operators that run Postgres. And it's all about enabling an end user or developer to click a button and start that up. Which means if you've got 1000 developers, they all want their own instance, that's 1000 databases that you have to deal with.

**Hamid Akhtar**  
I mean, the pain with one click installers was far greater than just the packaging because with installers you had to build all the third party dependencies, so they will eventually discarded on the Linux platforms in favor of native packaging. So with now this replacement of Kubernetes and Dockers and being available and just simply downloading and doing Run command, and you're up and running with the service preconfigured. That's that really helps a lot because one of the pain points that people had was how do you run the server, make sure it's configured properly for my use case and, but I think credit to the documentation as a wall Postgres significantly From the time when you it was a challenge to now when it's very organized. And I mean, the reason why I give so much credit is because I've seen the evolution I've, I've worked with the people were actively involved. And I've seen how they kind of push through things to make sure that everything got structured properly. So and how people were mad when we used to miss a timeline, even by 30 minutes of not releasing the installers, there was like everyone's on our back. So it's, I think this is this is how the ecosystem has evolved. It's about structure and predictability and allowing people to just engage with that community because you can depend on them. So with operators and Kubernetes, it's now at a different direction that things are moving towards whether that away from the old kind of philosophy of just in stop being able to install things, but again, that's the new technologies that are going to prop up. And the community is always going to support that. So it's Yeah, I think that these are, these are really good things that help community growth.

**Matt Yonkovit**  
Yeah, I mean, more people using it, more eyeballs, more contributions. Better polish, right? I mean, I think it all make sense, because you get better through more people using it.

**Hamid Akhtar**  
I mean, it's, it's, it's about, well, a few years ago, I think there was one complaint about Postgres community was I was very harsh, it's a you rude. It does not accept criticism, it does not take in things. But that's, that's not really the case, as you get involved with things. And people accept things, people accept features, they work on things, they do a lot of improvements. Yes, they need to be a little conservative with things. Because it's a database, the database by very nature has to be a bit conservative in terms of the feature set that they incorporate, and the risks of stability that they introduce in context of that. So they have to be very watchful of what they what they accept as a part of a patch, but they don't. And obviously, it's, it needs to be very remain very predictable for people. So not just that random, there's going to be a lot of features that are required. But again, they take it one step at a time, I have been, for example, looking at the BTree index evolution, whether in PG 13, for example, from deduplication. That was one attempt that improve b-tree indexes. But now in PG 14, they have what they call is deduplication. But it's in a very different way. It's called bottom up deletions, which is about removing the Virgin duplicates that are no longer visible. So that's effectively preemption of index growth, so the bloating side of things and then manage the indexes kept small and efficient in PG 14, and then you have page deletions that are better optimized. So there's a lot of work that goes on behind the scene.

**Matt Yonkovit**  
Yeah. And I think each of the releases of Postgres, you see the incremental improvements across all of these, and not a lot, not all the features are, like, the groundbreaking ones, like, Oh, my God, now we have all of this, this cool new technology to start using a lot of it is just improving what's already great. So, so taking what's good, and making it great that there's a lot of work there. And the polish is just, it's getting better and better every release.

**Hamid Akhtar**  
Yes. I mean, at times, for example, in one of my talks, upcoming talks, and I had looked into, for example, there was replication conflicts. And when I was looking into how the locking works, it was 1000s and 1000s, of lines of code. And I did not anticipate that when I started looking into that, I thought it's going to be a smaller lock management system, not too complicated. But as you dig into it goes in to functions and functions and functions and functions. And you end up with a huge call stack of functions that are just dealing with how the locking works. And eventually it throws up an error for a conflict in the database after a lot of function calls but I mean that's, that's the amount of work and effort that goes into just making any small thing work from a user perspective. It's just a very small number, but in terms of how much effort it goes into, and making sure that it remains stable, it does take quite a bit of effort. And obviously, a lot of people, a lot of eyes help, whether they dig into the commit first and we review those patches or whether they actively participate on the hackers mailing list, or they report the bugs on the bugs mailing list. It's a lot of people involved in getting this thing to the users in a shape that reliable and dependable.

**Matt Yonkovit**  
Okay, well, so what I like to do is, I been doing this the last several of my sessions, I go into what I call rapid fire mode. So I throw a whole bunch of questions at you, and we see how you answer to get to know you a little bit better. And to just hear a little bit of a different perspective on a few different topics. All of the questions are random, they just pop out of my head, I don't know what I'm going to ask until I ask it. So we're gonna go through, and we're gonna do that, to close this out today. So the first question that I have for you is, as you look at the postgres ecosystem, what is the most exciting thing you see coming down the roadmap? What what, what maybe feature technology or tool do you see that you're really interested in and think has a lot of potential?

**Hamid Akhtar**  
I have a biased opinion here, I think, working on a particular tool for a lot of time. I think the pg stat monitor has a lot of growth potential to be very biased here.

**Matt Yonkovit**  
There's no right or wrong answer here. That's okay. That's okay. So when you talk about like the engineering side of things, what are your favorite tools? What are your favorite tools that you use in your day to day work?

**Hamid Akhtar**  
Well, it was used to be WIMP, and then Visual Studio Code came in on my Macintosh. And that's with supporting the make file system and being able to give me that IntelliSense that I've been using forever. I think now, now I'm back to using that Microsoft tool. Okay, so I think that I really enjoy. Okay.

**Matt Yonkovit**  
Okay, what's your favorite command line tool.

**Hamid Akhtar**  
I just use bash, I just have a lot of one liner,

**Matt Yonkovit**  
bash, minor bash,

**Hamid Akhtar**  
bash, I love just making that complex piping scheme to ensure that I end up doing something crazy whether it's usually a shell command, followed by something something grep said, then x args or an awk.

**Matt Yonkovit**  
So you take a really complex program and write it in one line, is what you're saying.

**Hamid Akhtar**  
I love that complexity. 

**Matt Yonkovit**  
Yes, we love bash. Yes, there's nothing wrong with bash, I'm telling you, there's nothing wrong. At the time.

**Hamid Akhtar**  
I have written the smaller compilers. I'm very happy with it.

**Matt Yonkovit**  
So what is the biggest problem? You see users running into with Postgres nowadays? Like, what's the thing that they just always get wrong?

**Hamid Akhtar**  
What it's about really configuration. There's not, I think that there are general guidelines. But when you look at people and the use cases that they're trying to implement, their configuration is never or hardly ever optimal for their particular use case. So they just go by the general guidelines, they configure it in a way that never optimal, or they don't use certain features, whether say, for example, should you have an unlocked table? Do you really need logging for a particular table that improves significantly the performance? And should you use some other kinds of tricks, just to improve the performance? So I think it's, it's really, the versatility of Postgres offers that very challenge of configuration and configuring it optimally for the environment as well. And that's where people just run into things, whether that's the kernel optimization, or disabling hugepages and the costing of the CPU, for course, it's just about really looking at those small things and being able to optimize things then for the use case.

**Matt Yonkovit**  
Okay, when you're not hacking on code and working on building something cool and interesting. What are you doing at home?

**Hamid Akhtar**  
I'm usually either playing FIFA, so Oh, okay. Soccer, or F1. So, we, me and my son and I, we usually have a competition or one of my nephews. So we were just playing something we're watching something Oh, yeah, and this, I'm just trying to spoil my seven year old with a few things and my wife running after me. It's that story usually.

**Matt Yonkovit**  
So do you let your son win? Or do you like, beat him? So he has something to work towards?

**Hamid Akhtar**  
If he is going to make a crying face?

**Hamid Akhtar**  
I can't really do it.

**Matt Yonkovit**  
Okay, yeah. Okay.

**Hamid Akhtar**  
I have to be very smart. Playing with my younger son. So yeah, I mean, it's, you have to use to win it.

**Matt Yonkovit**  
Well, of course, right. So so yeah. So you can still lose and win at the same time. It is possible. Everyone, it is possible. You heard it from Hamid. And you can hear it from me as well. Yes. Sometimes you just have to give give a little to get a little there. Yep. So Hamid, thanks for hanging out with us today. I appreciate you giving us some insight into PG stat, monitor the postgreSQL space, a little bit about where you think things are going, and of course, answering all of those random questions that I threw in at the end.

**Hamid Akhtar**  
Oh, those are those are really well constructed questions at the end. I love those. Yeah. And I'm glad I came out unscathed.

**Matt Yonkovit**  
So it's fine. It's great. It's great. So um, everybody who's watching out there or listening, please feel free to like, subscribe to the channel. Do all the things that let us know that this is interesting content, and give feedback to us in the comment section. And thank you again, Hamid. And we will see you at Percona live in a few weeks.

**Hamid Akhtar**  
Sure. Thank you. Thank you, Matt. It was really a pleasure having this conversation with you. Thanks. 

**Matt Yonkovit**  
All right
