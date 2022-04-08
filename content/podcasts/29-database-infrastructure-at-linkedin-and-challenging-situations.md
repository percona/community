---
title: "Database Infrastructure at Linkedin, and Challenging Situations - Percona Podcast 29"
description: "Karthik is passionate about distributed, scalable and highly available databases and is eager to share his knowledge and experience with us."
short_text: "Karthik Appigatla, Staff Engineer, Linkedin is the guest of the HOSS in this episode to talk about the database infrastructure at Linkedin, challenging situations that arise from running databases at scale, the evolving role of DBAs and DBREs, and dive deep into his recent Percona Live talks. Karthik is passionate about distributed, scalable and highly available databases and is eager to share his knowledge and experience with us."
date: "2021-07-13"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-29-karthik-appigatla-staff-engineer-linkedin/"
youtube_id: "pwkg477XhTE"
speakers:
  - karthik_appigatla
  - matt_yonkovit
aliases:
    - "/podcasts/29/"
url: "/podcasts/29-database-infrastructure-at-linkedin-and-challenging-situations"
---

## Transcript

**Matt Yonkovit:**
Hi, everybody, welcome to another HOSS Talks FOSS. I'm here with Karthik from LinkedIn. Karthik has presented at several Percona Live conferences about LinkedIn scalability challenges, some of the things that they've done with MySQL, some of the cool things that they've learned, and shared with us over the years. Hi, Karthik, how are you doing? 

**Karthik Appigatla:**
Yeah. Hi, I'm doing good. And you?

**Matt Yonkovit:**
I'm great. And so you gave a couple talks at Percona Live. And I know that you've been at LinkedIn for quite some time now. Maybe just give us a little background on yourself. 

**Karthik Appigatla:**
Yeah, sure. So I'll just talk about my whole career, how I tend to be a DBA and then how I tend to be a database reliability engineer, I will just describe our aspect to become a database. So back in 2008, when I was out of college, I joined Yahoo. So I joined as a service engineer, where I was I mean, now the service engineers are called the srs. So at the time, they called us service engineers. I was responsible for handling Yahoo's data pipelines. So I've been working there close to one and a half year, and then all of a sudden, we had a database issue. So while troubleshooting that issue, I developed more interest towards the database. And I moved to a database team. I was just starting, it was easy to move the teams. So I started when my SD was around 5%. The first thing that I have done, when I started, I upgraded to 5.1. 

**Matt Yonkovit:**
That was a big jump from 5.0 to 5.1. That was a pretty significant difference. 

**Karthik Appigatla:**
Yeah. So I remember that. It's just because of the partitioning feature in MySQL, we wanted to go with that upgrade. And I had to convince all my managers that we need to have this feature. So that was a massive scale. We had to upgrade several matrix 10s of databases, not hundreds of databases, but 10s of databases, and later have worked for the Yahoo ad serving platform as a database administrator for close to three years. And then later, I thought that I wanted to get more hands on with databases with a wide range of technologies. We were using only the traditional MySQL but so I wanted to explore more. So I joined the Piscean consulting company. So there I got a chance to work on a wide range of fields like I worked on MariaDB,I worked on Galera, I worked on Percona Server. So, a lot of things have worked on. Then I moved to Percona, when I was amazing, even though I spent only one year, but it was amazing. So higher chances to work with great startups. So at the time, like a lot of startups, where I was consulting, I was part of the remote DBA team. And I was consulting for other like prominent startups all over the world, as well as in India as well. So it was a great journey. And I learned a lot. And at the same time, each client comes with a different set of problems. It's not unique all the time, you have to be on your toes all the time. And the clients are demanding as well. They expect top class things from me so I had a very good time. 

Later, I moved to a startup when I stayed there only for six months, and then I moved to LinkedIn. So I have been with LinkedIn for close to five years. So in these five years, 
I transferred myself from DBA to the DBE like database engeneer, but more importantly reliable, a reliability part more. So in these five years,  when I started there were only probably 100 to 200 databases. But over these five years, like the number of databases more than 2000 databases, I think it's like more than 2700 by now. Because the number of microservices are increasing crazily, each microservice invents a database and the database team is very small. We had only like three to four guys in us and only like two to three guys in Bangalore. So it was very challenging for us. So how we scaled was like, we automated everything like, right from provisioning or like if anyone wants to do SDM upgrade or anything. So we have automated. So it's like we build our internal cloud for the databases like, probably I can compare with what RDS provides for clients of how, what scale provides for each client, we provide the same thing for our internal teams. 

**Matt Yonkovit:**
So you have your own kind of internal databases, a service for your development teams? 

**Karthik Appigatla:**
Yes, yes, yeah, we developed it from scratch. So yeah, it was a very good journey. Like I still remember, like, when we were manually creating the databases, when I started at LinkedIn, now it's like SMB click, they get everything, they get the high availability, they get automated backups. And they want a nice, like schema where you can just submit a request, and it will be done. And, like, there are still improvements, though, like if they want to recover, one click, stories not get done, but that is in progress. And we have an ETL pipeline to any other stories, and we have that change in the capture. And we want from MySQL, we want to take you to some others to be updating on chapter five, where it captures the changes, and then wherever you want.

**Matt Yonkovit:** 
So what did you use? Did you use any sort of virtualization? Are you using whether it's Ansible? Or Chef or Puppet for orchestration? Are you using any of the containers, anything? Like maybe just give us a glimpse into that system? What are some of the technologies that you're using? 

**Karthik Appigatla:**
Okay, so for the databases, like, since we, the number of databases are so high, and we posted the physical bare metal server. And we don't use the containers or anything we have, like, bare metal servers, and we potion the databases based on the capacity, like something requests for, like, let's say, 1k qbs, and we have a cost factor for each. I mean, like, it's not thought factoring, I forgot the name. But we estimate the capacity of each server. And like, let's say that the server can take 10k qbs. So if, if something because 1k, and something, sometimes requests for only 100 qbs, so we provision all of them on a single physical server. And for security reasons, we maintain the isolation, we leverage the MySQL privileges, to make sure that the one database does not talk to the other. And we have the query analyzer tool as well, which provides, like what queries are run, and it also provides an estimate of how much CPU are they actually using, it's not based on exact other queries, but we, we take care of how much GPS like sometimes even though the GPS is like 100, they take huge CPU. So what we do is like, we move them to another cluster, where they stick under, of course, the disk quota implementation is like quite simple, like the question for, let's say, like, one terabyte, and we extrapolate to like, next year's like, how much like 1.4 GB or 1.5 GB and based on the disk, we have we this person, it's like, straightforward thing. And on top of that, we provide like, the best practice the whatever the best practices that they can do.

**Matt Yonkovit:** 
Okay, and so for that environment, that's a pretty big environment, some of your bigger systems, they're running Vitess, correc?. Because one of the talks that you gave was about scaling LinkedIn, and it was specifically on using Vitess. So tell us how Vitess plugs into that. 

**Karthik Appigatla:**
Yeah. So we have a system for the informed, which gathers almost all the events of all the infrastructure events, basically. So we have hundreds and 1000s of servers all the time, and there'll be a lot of deployments happening on all the systems across LinkedIn. And each deployment is taken as an event. Not only deployment, some teams use that for alerts as well. Like if any alert comes, some activity that might be done on a particular portion what activity is done. So we calculate all these things like, which is a huge, huge set of data. So like, obviously, like a single server cannot scale. So when they were initially launched, we were having them.
But all of a sudden, since everyone liked the service, the other teams signed up for this. And in a short amount of time, we had to quickly scale to the so that we thought of looters, because because of many factors, the primary factor is like, it doesn't require any code change from the development team. Because like, they will still work fine. And another thing is like, they want the transactional as well as, like, relational features, they want to still join on few tables. So because of all these factors, we started exploring with us, and it was quite obvious choice for us to go with. And it worked out well, under the time we replication was at the native status, so we could not use it. So we implemented our own  replication strategy, how do we go to that and then come back if something fails. But luckily for us, we never had to be unlucky. It's been blind.

**Matt Yonkovit:** 
Okay, and 2700 databases is a very healthy environment. What are some of the challenges that you run into trying to manage and maintain that size of environment? Like, what are the common things that continually come up that you have to do? 

**Karthik Appigatla:**
Yeah, so I'll tell you like, I'll go a little bit technical. I mean, for example, we co-host databases, right? So, the main challenge that we face is the abuse from the lines, like, sometimes they miss a web. So the updates, like 1 million records, or 10 million records, and we have literally no control on what they do. And they just start the transaction, and then don't end it. So it was under lock space, and it affects the replication lag as well. And apart from that, it it becomes a noisy neighbour for the other businesses and they start complaining, hey, our database is slow, like, what happened, then we had to follow up with each and everything, like all what has gone gone bad. It's very tough for us. 

**Matt Yonkovit:** 
So it's really chasing performance problems. At that point, it's oh, this is slow that the system is impacting other other applications and trying to find the needle in the haystack. 

**Karthik Appigatla:**
Yeah, yeah, it meant chasing the teams is one of the last things that we wanted to do. And at certain times, we can't kill the connections or the like, even if you kill what happens, it rolls back the transaction, which is even worse than letting it go. So yeah, we are trying to use ProxySQL or some other technologies like that, where it has very limited capability where someone accidentally misses the where clause, or you will not let it go or something like that, we wanted to explain what it's like. In the like, we're very far I would say, I can't associate the timeline with that. But this is one of the big challenges that we have. Another other challenge that we face, is the query plan changes sometimes because data is used. And, again, like we don't have any control on the query plan. Sometimes if it changes, if we want to force a new query or logic to do indexing, we need to go to the application, change the query deployed on all the hosts, it takes at least like a half an hour to one hour of time. So that also we are trying to solve probably using ProxySQL or something like that, where it can, it can automatically detect and then I mean, it doesn't need to detect at least it can rewrite the query for us a lot of time. And also we are exploring the other options as well, we wanted to prevent this problem before it occurs. Like, can we have a test server where we find all the queries and see the patterns in the query data, so that we are aware of not even scratching the surface of that, but this is just an ideation phase itself. 

**Matt Yonkovit:** 
Yeah, I mean, there's a lot there because I mean one of the great things about enabling your your developers and users to create their own systems to be able to add systems on their own automate most of that is it takes away a lot of the the routine work of setting things up or installing or configuring, but then you've enabled a lot more development teams to work faster, and they throw those problems at you quicker, when you've got to try and solve those, those those issues that pop up because you're enabling the developers, they're developing, and sometimes they don't always get the things right. So there does need to be that closed loop.
You mentioned, you moved from a DBA to a DVRE or a DBE. Has your role really changed that much? What responsibilities like, but when you look at those two roles, a lot more companies are moving away from hiring, quote, unquote, DBAs, and more are looking at SRS or DVRs.
What's the difference? You mean, you've lived in both worlds? What do you see as the difference between those two? 

**Karthik Appigatla:**
Yeah. So I mean, from my side, when I, if I talk about me, when I was the DBA, I was looking at only one system, I was making sure that one system is up all the time, and then making sure that the performance is not impacted. But when I moved to DBE role, instead of looking at the system, or a single system, I was like managing hundreds or even 1000s of servers, and accounting for the I will build the systems and even make sure that they are reliable, not just a single system, but the whole environment. That's the major difference. I no longer run many, or all the commands or anything, it's all automated, I don't no longer run a backup or anything like it's everything is automated at a system level, even the point in time, where everything is like, we have like a lot of tools to automate that. So that's the major difference that I see. 

**Matt Yonkovit:** 
So it's about managing masses, lots and lots of systems, but it's also being a performance detective, if you will. Right. So trying to find the needle in the haystack, find that performance issue. Right. Yeah. Props, you come onto my show, and you get props. So, but no, no, I get that. And it is a move that people have continued to see, because you mentioned with the microservices with the individual applications, all recording their own databases, you're no longer having 10-20 databases that you maintain, you have 1000s. And it's just it's it changes your mindset, and how you have to work because you have to automate or you'll die of overwork, if you don't automate. And so I get that. Now, you did mention HA, and high availability. But that also goes along hand in hand with scale. And I know, one of the things that you've talked about is synchronous replication versus asynchronous replication. And so you can't really do synchronous at LinkedIn, because of the performance. Correct. And so you're, you're still advocating async? Maybe tell us a little bit about that. 

**Karthik Appigatla:**
Yeah, sure, I can talk a lot about this. We face is day in and day out. And we, we actually have both models. Like we talk to the developers every day and explain about the problems of synchronous replication, like sometimes they demand, we want synchronous for this application, but we explained the challenges. So light, I mentioned in the talk, we are limited by the speed of light, here like a lighthouse at a constant speed, and you are on one side of the globe, and on the other side of the globe, it takes roughly around like point five milliseconds, I guess. But we can't tolerate that kind of latency. So that's why we definitely need to have a single replica, but again, the biggest problem that comes into mind is the conflict resolution like how do you resolve the conflicts and there are multiple rights. So, like last night, or when is like a very commonly used strategy across other databases like all across all other distributed systems. But the problem is, MySQL does not have the native capability to to give any sort of conflict resolution, or even, for example, if you take delivery, like there is no option to disable the certification process, because the certification process itself or takes a lot of time it has to communicate with all the nodes and get back from all the nodes. So that is it certified. But that takes a lot of time, there is no option to disable that certification process. Even if my application says it's my authorization to deal with the conflicts or it's my authorization that I will take care of my data. But any synchronous replication, or anything that does not let you do like Dave, I mean, because that is their product. And it has to be they give more weight as to the consistency part. So that's an option to do. So that's why we had to take away the native replication, we have to go with the Kafka route, and then I have additional application nodes to detect the conflicts. And then the additional applications we have as writers and then insert into the database on the other side of the globe. So this is all like, very high overhead for us to maintain these systems. Unlike probably, if MySQL had natively provided conflict resolution mechanisms, that would have saved us a lot of hardware costs and the maintenance overhead system. Or even if Galera cluster cannot give you an option to disable the certification process. And it can also like it also detects the conflicts of the primary key level, rows back instead of doing that it can have an intelligent way and say that, okay, this transaction, I can I can skip this transaction I need to override. So that kind of features like, it's a bit then.

**Matt Yonkovit:** 
Yeah. And you gave a whole talk on this at Percona Live, where you talk about the implementation that you're currently using. And you talk a little bit about what you'd like to use, correct? 

**Karthik Appigatla:**
Yeah, yeah. 

**Matt Yonkovit:** 
And that is available for everyone who's watching this. Now on YouTube or on Percona website, you can go to get it for free. Go watch that you can also watch about scaling you know, at LinkedIn as a whole so Karthik does do two talks for at Percona Live one on the the colocation,
replication and one on Vitess and LinkedIn. But Karthik, let me give you the final word. And I always like to ask people what are they seeing what is going to change, maybe how they work in the next couple of years? Like what kind of new interesting technologies or things? Are you exploring? What sort of things are you really interested in right now?

**Karthik Appigatla:**
Mostly, like, I think,flexibility across databases is the next thing that probably I guess, for example, if you're using MySQL, suppose you don't like MySQL, you want to move to some other system? Like it should be, like, very seamless to move to the other database.

**Matt Yonkovit:** 
So from seamless moving from MySQL to Postgres or from Postgres to Mongo, or from Mongo to Cassandra? 

**Karthik Appigatla:**
Yeah. Because of the changing of licences. We don't know, which licence changes or what, when do you want to move? We are not too late. So probably like, that is a thing that I'm guessing I might be wrong as?

**Matt Yonkovit:** 
Well, it's interesting, because data portability is a big deal, especially with companies looking to prevent getting locked into a certain solution. But as we enable developers, developers often don't care about the database technology itself. They just care about, I want to put data into an API. And then whatever's the optimal solution, whatever, as long as I just do the same call, I want to think about it. Yeah, so that abstraction layer, you could change the backend of the database system, from engine A to engine B. And it would be perfectly fine from a development perspective, but it might save you a lot of costs, resources, hardware, because that might be stored more optimally in a different database engine than it is currently. So I can see the value in that.

So you're going to develop it. Is that what you're doing? Is that what I hear? You're going to develop that technology to move things around seamlessly?

**Karthik Appigatla:**
Yeah, I wish to do that. 

**Matt Yonkovit:** 
Well, Karthik, thank you for joining me today. I appreciate you sitting down. I appreciate you talking at Percona Live. It was great to have you there. Hopefully you enjoyed the show this year. It was great. A lot of people, a lot of different sessions. So thank you very much. Yeah. Thanks very, it's very nice talking to you.

**Karthik Appigatla:**
Yeah. Thanks very much, it's very nice talking to you.

**Matt Yonkovit:** 
Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course tune into next week's episode. We really appreciate you coming and talking open source with us.
