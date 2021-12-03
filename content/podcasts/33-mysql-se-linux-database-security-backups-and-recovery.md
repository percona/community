---
title: "Variety of MySQL Topics, SE Linux,  database security, backups and recovery - Percona Podcast 33"
description: "Percona’s Hoss Matt Yonkovit talks to Lead Database Consultant at Pythian, Matthias Crauwels to tackle SE Linux,  ensuring database security, backups, recovery, testing, and more"
short_text: "Percona’s Hoss ( Head of Open Source Strategy ) Matt Yonkovit talks to Lead Database Consultant at Pythian, Matthias Crauwels on a variety of MySQL Topics including how to tackle SE Linux,  ensuring database security, backups, recovery, testing, and more. Mathias is a long time member of the MySQL community and has spoken at numerous conferences on MySQL related topics."
date: "2021-07-30"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-33-matthias-crauwels/"
youtube_id: "5kyRcYqNF8s"
speakers:
  - matthias_crauwels
aliases:
    - "/podcasts/33/"
url: "/podcasts/33-mysql-se-linux-database-security-backups-and-recovery"
---


## Transcript

**Matt Yonkovit:**
Everybody, welcome to another episode of the HOSS Talks FOSS. I'm here with Matthias Crauwels from Pythian, community member who has spoken at many Percona Lives and is a prolific blogger, and has established himself in the MySQL community helping a lot of different people, as he's doing consulting work around MySQL for Pythian. Hello, Matthias, how are you doing? 

**Matthias Crauwels:**
Hey, Matt doing well. How are you? 

**Matt Yonkovit:**
Good, good. And so how is the weather there in Belgium?

**Matthias Crauwels:**
It's a bit colder this week, it was very hot last week. But then it's also hot in the night so you couldn't sleep well. But now it's a lot cooler. It's actually pretty decent now. 

**Matt Yonkovit:** 
Well, that's good. And so I did want to give a shout out to Matthias’s guitars, which are cool. And as you watch this video, if you're watching live I have no background. So behind you know, as you watch the video, like it'll just be the floating background, my floating head, whereas you get the cool guitars. If you're just listening. And you don't see Matthias’s guitars behind him, which is way cooler. And it makes me jealous that I need to rearrange my office and how I record.

**Matthias Crauwels:** 
Yeah, my wife was a bit angry at the location that I put them in initially, because there's just stairs coming up. Right. But I thought it was cool to put them there. 

**Matt Yonkovit:** 
Yes. And now you have proof, it's recorded. 

**Matthias Crauwels:** 
Yes, I will show her that.

**Matt Yonkovit:** 
Yeah, yeah. So Matthias, maybe you just give people who aren't familiar with we haven't heard you speak the briefest of overviews about you.

**Matthias Crauwels:** 
So I'm Matthias and I live in Belgium. I have been working for pity for the last four years almost. And I'm a MySQL DBA. And I've spoken on many Percona Lives initially, mostly about high availability in the last few talks about other things like athletics, and backups, and things like that.

**Matt Yonkovit:** 
So you like to handle those topics that sometimes people are like, Oh, my God, those are boring, but they're so needed, right? 

**Matthias Crauwels:** 
Yes. 

**Matt Yonkovit:** 
Like, let's be honest, security and backups are two things that people don't like to think about. But they have to think about,

**Matthias Crauwels:** 
Yeah, it's not the most sexy of topics if you talk about this, but it's really needed. And especially the esta linuxtag, it came from something that we encountered in our daily work. And typically what we will do is… LeFred once asked me and told me, life is too short for us to Linux. And, and we, what we usually do is we turn it off. But then we had a compliance team coming back at us, you can't turn it off in our environment. And so we had to learn how to deal with it. And so I did some research about it and decided to write a conference talk about it.

**Matt Yonkovit:** 
Well, and that's funny, because I remember back in the day, so you know, those who don't know, I used to do what Matthias does, which is consulting. And so my job was helping customers and everything else. And I remember when SC Linux was introduced, and it was like, what is this? And why is it killing my database? And so yes, the old old old school was turned this off, because it just doesn't work. And I can relate to the life is too short for it. But you're right, compliance teams are now requiring a lot more security measures in order to secure their databases. Nobody likes to see their data leak. Now. Interestingly enough, most data problems, data leaks, security issues, end up not necessarily being something that would have been prevented from SC Linux. Most of them are because people are kind of know, that they don't know that they should set a password. They've taken backups and left them unencrypted on s3 buckets. You know, they've left their applications wide open. So it's more like they've got this giant neon sign that says, Come on in, enter here. Enter here. Yeah, yeah. Yeah. Back entrance for you know, like free data. Right and so, but as you started to look at some of those SC Linux things, what were some of the things that kind of surprised you.

**Matthias Crauwels:** 
And so for MySQL out of the box, it really kind of works. So the default isolinux that's deployed with most Linux in addition to that I tried, just allows the right things for my skill to be in place. So if you don't change like a data directory report, it should just work out of the box. The trouble starts when you start moving things around different locations like if some clients that we have liked to have their data in slash data, instead of var lib MySQL. And then that's where the problems start, if you have to use Linux and keep it down. So then MySQL one starts and you're like there, why won't you start? I did everything right. And the first few times, it takes you a little bit of time to figure out Oh, right. So Linux. And then usually you can then quickly turn it off to test. But then if you have to continue working on that, then you have to figure out the right policies and the right context, put everything in place that makes sure you apply everything correctly. So there was a bit of a search. I wrote a presentation initially for FOSDEM in Brussels, I think two years ago now. And then I also submitted for Percona Live, I think, last year, and then I presented a terrible system.

**Matt Yonkovit:** 
Yeah, and both talks are actually online. So you can get them on YouTube, if you're interested in avoiding any sort of issues with se Linux. Now, in your travels as a consultant, are there other things that you've seen people do or implement, from a security perspective to keep their data secure, in addition to sc Linux.

**Matthias Crauwels:** 
So Linux is still something that mostly gets turned off, in my opinion to just some customers that require it. Security wise, mostly, the databases are in a secure network where there's no entry from outside unless you have the correct VPN and accounts, or you use some kind of jump host to get access to it. But really special measurements for security, I haven't seen much. So we have clients that use LDAP authentication for MySQL, which is a convenient way of keeping your... Not having shared passwords, let's go there. So that's something that I was very surprised to find when I started as a consultant that many companies still use shared passwords for us as consultants entering, so they have created a Pythian account, and we all have to use the same account. And I, whenever we onboard people, I try to tell them to avoid that, because every time a consultant leaves, we have to all go change the passwords, and it's a hassle. So, so just create, like a personal account, if someone leaves, you can just log that account and nothing, nothing can access it anymore.

**Matt Yonkovit:** 
Yeah, and I think that for a lot of people depending on the size of the company you start to implement those, those additional things, like larger companies typically do quite a bit of auditing. So having a shared account really screws up the ability to audit, right? So you can't say Matt went in and deleted this data or did this stuff that he shouldn't have. And so keeping that shared account is not necessarily a good thing. But even a lot of applications have shared accounts. And the bigger that you go, the more that you start to see some of those changes. So encrypted backups obviously are something that is a recommendation, especially if you're going to push things out to the cloud. You know, like I mentioned, there's just so many s3 buckets that are just exposed where full backups of data.

**Matthias Crauwels:** 
People think that no one can access it, because no one knows the URL, but URL crawlers are very good these days. And they can figure out a lot of things. 

**Matt Yonkovit:** 
So, yeah, well, there's people who just that's all they do is they go out there, and they look, and now some of them are white hats, because they're looking for security issues. You know, and helping people avoid them. Other people are looking for data to resell bustling business,

**Matthias Crauwels:** 
It's a very big business with selling that data and trying to hold you ransom with ransomware until you pay a lot of money to a hacker for giving you the decryption key, which might not even work even if you pay so it's very, very dangerous. And we experienced that with one of our customers where they were running MySQL or Windows Server, and they were held hostage by someone who encrypted their file system, and they couldn't access their data anymore. And we said like yet they came to us, like, Can you help us? And we were like, yeah, where's your backups? And they were like, we don't have backup. So we were like, nothing you can really do at that point.

**Matt Yonkovit:** 
Oh, yeah, I mean, and that's unfortunate because you know, those security issues that caused that and you know, they've just been on the rise but once you have those, you know that that exposed entry all hands are off. Now I'll get back to you know, back in the day when I started at MySQL, one of the people who I had to shadow was Monte Taylor. And I remember Monte telling me the security in MySQL is completely secondary, or doesn't really matter. If you don't secure your operating system, and if someone gets access to your network, they're gonna get your data somewhere, somehow. Yeah. And that's, that's true, right? Because the MySQL setup on that machine that you mentioned, that Windows machine could have been totally secure, but they just encrypted the file system and the blocks, and there wasn't any backup. So what are you gonna do?

**Matthias Crauwels:**   
Well, what can you do at that point, there's just nothing you can do, you can try to brute force him to decrypt things, but that will take ages to do to get into that. So

**Matt Yonkovit:** 
Yeah, and it's often that human error that that kind of like somebody, somebody clicked up something they should know, somebody opened up something they shouldn't have. And it's caused a cascading impact across the machines and the systems. And I think that's where like your other talk, which is specifically on backups, and kind of the backup landscape is interesting, because not only do you need to secure your systems for the security issues and make sure you have a backup in case there's something that that gets exposed, and make sure that those are secure. But also, you have to ensure that you know, you've got backups for when there is an actual crash or something that happens. And you know, that it's critical.

**Matthias Crauwels:**   
It's just like the chat you had with Pep a few weeks ago, you were also talking about backups. And he was telling you like, you don't need backups until you need them.

**Matt Yonkovit:** 
Yeah. And he made the really great point that it's not about the backups, it's about the recovery. Yeah. Like backups don't matter.

**Matthias Crauwels:**   
That's, that's also one of my first slides in this talk about the backups. If you don't test your backups, if you don't try to recover them on a regular basis, you don't have backups, we consider you don't have backups.

**Matt Yonkovit:** 
Yeah, and I've talked about this before, when I worked, or I didn't work personally, we had a, when I was running consulting, we had a customer who came to us, and there are a really big social media company unicorn status, like billion dollars, right. And they had moved data centres from data centre A to B, a few months earlier, and forgot to turn on the backups. And after doing that, someone ran a Ruby migration, and it dropped the tables and recreated them or something similar to that, and wiped out their data. And they're like, Oh, my God, everything's gone. And they want to go get the backups working. And I remember we did a lot of forensic data recovery to get them up, but they were out for four days. And after a four day outage within six months of that they were out of business. Yeah. I can, and, I mean, like, that's, that's a crazy you know, story, a crazy impact. And, but it happens quite a bit.

**Matthias Crauwels:** 
And that's not a small company, where there's only one DBA, forgetting something that's just an entire organisation missing checks.

**Matt Yonkovit:**  
It's not that like again, they had the backup process, they had the backup scripts, it's just, you flick, you made a small change, or a big change in this case, but but you know, like moving from data centre, A to B, and datas, the the old data centre still have the backup for a man and you know, that data was updated. 

**Matthias Crauwels:** 
Same thing can happen on a small change, if you like, have one server, that's due for the commissioning, because it's out of warranty, and you need to move your database to another. If you forget to turn on the backup on the new database server, then you can run into trouble.

**Matt Yonkovit:**  
Well, yeah, and I've seen that as well as failover systems kind of flipped around, right. So maybe you've got a machine offline for maintenance that happens to be the machine that you use to take backups on.

**Matthias Crauwels:** 
Yeah, it's true, it's a problem. We always try to have at least a few locations where backups can be taken. And then we usually write the script to check whether the backup what's the most recent backup and where it was taken. And we keep track of that. And so if one of those servers fails, then another one is scheduled to pick it up. And also we have monitoring on the log files and to check the age of the log file. So if the file is two days old, an alert gets triggered then someone will have to go check to see or it will keep ageing them Yeah, but it is the only way to ensure that people follow up on those alerts. Because if you don't, and you just get an email, I'll check that next week because I'm working on something right now. And then next week, yeah, I was delayed or something or something else. And then, and suddenly, you're three, four weeks without backups. 

**Matt Yonkovit:** 
Well, this is where it gets kind of interesting. So a lot of people will forgo backups because they've got redundancy on the file system, and an external file system. So if the machine goes away, or the machine crashes, they'll just mount the EBS volumes in another location. And since Amazon will take copies behind the scenes of their EBS files, it protects your data. So what do you say to those people? Now, I know what I would say, but what like, when you when you run into a situation like that, what do you think?

**Matthias Crauwels:** 
Usually those kinds of setups are more for high availability, and not for disaster recovery, because this is when disaster strikes, when Amazon has a data centre burning down, it's not happening regularly. But if it happens, then then this, you still lose all that data, or less impactful than Amazon burning down a data centre might be a developer dropping a table, and it gets replicated through your entire system, and the data is gone. All of the servers, you might have a delayed replica, but what are the chances for you knowing within the timeframe for that delay, that there's something wrong? If you delete a table, can it be that your application starts chattering? And then you know, oh, something is wrong. But if you delete some records, and you don't immediately know, then then yeah, what do you do? 

**Matt Yonkovit:** 
This is where it's interesting, when you talk about the deletes. And you talk about that cascading impact. I think that like some people will have that delayed replica, they will have something that they can quickly failover to, but you mentioned a good point, which is people don't think of the recovery time that it takes to actually diagnose and figure out Yeah, right. It's not obvious within like, a five minute or a 10 minute window, that it's oh, the applications here, and what happened, where in the fact that you have to log in, check, what is going on, and then find out, it's table X was had its data deleted, or whatever, and why it had it deleted, and then stop the application and then like, I mean, all of these things take time. And I have seen this before where people have relied on a delayed replica. And as they rely on that delayed replica they'll have an hour delay or something, it takes them an hour and 30 minutes to find and diagnose the problem. And the replica is already like, it's gone, it's gone. Right? You know, so that whole recovery from that replica.,

**Matthias Crauwels:** 
Even if you're diagnosed before that, that replica is in trouble. If you stop replication there, and you have one, one server that has the data that's correct. But you need to redistribute all the data to all of the other replicas in your environment, in order because one server usually cannot serve the traffic. So you need to recreate a number, basically, an entire new topology from that one replica in order for you to get started fresh, and that might not take minutes with that might take hours or even days to get it fully, fully running and provisioned. So, look at the outage that GitHub, that's the big one in 2018, where they had a failover biorck share to the other data centre. And then they realised that like about 40 minutes in Oh, we have to fail back and it took them 12 hours to prepare the environment to get ready again. So it's a risk that that's there if you use automation, and if you get all the safeguards you have in place, but there's still always a risk if you do things in an automated way because automation can fail and automation can trigger other problems. 

**Matt Yonkovit:** 
Yeah, and I mean, I think that you know, that automation triggers other other problems is a whole nother area. I mean, I, I've done a lot of looking and digging into outages, especially in cloud providers, but also large SaaS providers over the last few years. And it's so amazing that as we start to automate more and more of our operations, which we have to because we're talking about 1000s or 10s of 1000s of machines you have to rely on that automation. It is so easy for you to make one small mistake that's replicated 10,000 times now. 

**Matthias Crauwels:** 
Yeah, I know, my comment about automation was not at all to stop people from using automation, because automation is the way forward, we have to automate ourselves out of a job as consultants, that's basically what we do. But yeah, the point is to have enough security checks to have enough safeguards to have enough points where you can say, Oh, stop right here, because this is going wrong. And that is the hard part of getting your automation to work the proper way. Nine out of 10 times it does perfectly what you ask it, but that one time? 

**Matt Yonkovit:** 
Yeah. And I mean, I think this is where it's really interesting, because I think that we've gotten a little less focused or a little, maybe a little lazy as a, as a society when it comes to testing and making assumptions on hey, this worked in this smaller environment, this worked in this that in making those assumptions that yeah, it should just continue to work. And when we look at like modern application design, you're looking at a lot of continuous integration, continuous deployment, you're looking at constantly deploying changes, and you're constantly deploying those changes, potentially across hundreds or 1000s of servers, yes, it's almost impossible to do a test on all the permutations. You know, with all the workloads across that size of an organization.

**Matthias Crauwels:** 
Yeah, we are currently working with a very sizable client, where they're where we are in charge of their testing environment. So they hired us to fix their testing environment, because their developers were really in trouble. Because the internal team cares about the production environment, of course, that's what brings in the money, what makes revenue. So keeping production running is their prime, target and their prime concern. But the testing environment is equally important. Because if the testing environment is just like done for a day, they might have X number of developers sitting there twiddling their thumbs, because yeah, we can't, we can't work because the database is that testing database. And, and even it goes one step further, because they have all of their systems replicated in their testing environment. And then they start, while they're developing, they just need their own database to talk to, but once they start going into integration, testing and running their CI pipeline, to see if their change will actually work in in the rest of the ecosystem, then there might be a database down somewhere on the other end of the system, which breaks their pipeline, and then they're still stuck. So it's a challenging task, to do proper testing to do proper setup of your environments. But yeah, it's really necessary. And the testing costs money, backups cost money. But in the end, if you don't have backups, and you have a disaster like that customer that I talked about with the ransomware they weren't at the business, because yet they lost all their data. So they couldn't, yeah, they couldn't provide any customers anymore. So they just just went bankrupt..

**Matt Yonkovit:** 
Yeah, I mean, and these are relatively small, in terms of like one little tiny system in a what could be a very large corporate network, but it has the impact of potentially making or breaking your entire organisation. Yep. And that's a really powerful, and really, and an exclamation point and why you need to be so certain that not only is that system really secure, but you have the redundancies in place to make sure that you can survive those relatively bad days. And not only that, think of the impact on your customer base. I mean, there's a cascading impact that I don't think people realise okay, so this one company went out of business. Well, maybe they had 300 employees, that's 300 families, that's potentially you know, a couple 1000 people who are impacted by that company going out of business, then their customers depending on what they're doing, that could be, you know, 500 customers who are relying on that for their business. So now their business is impacted for you know, how many of our weeks, the data that they used, or that they stored is no longer accessible. So they can't take that data and be portable, and move it somewhere else. And I think that we're building a very fragile ecosystem here. Especially when you look at some of these companies in the SaaS space when you're saying, like, Oh, I'm going to outsource my payroll or I'm going to outsource my benefits to this company, you're relying on them to not only secure the data, but also have those redundancies in place. And if they don't, then you might not get paid, I might not get paid, right.

**Matthias Crauwels:** 
You know, imagine that payroll company having that kind of issue where they're not available for four or five days where you cannot do payment processing. How many people are waiting for your salary to be paid? 

**Matt Yonkovit:** 
Yeah, so the cascading impacts are massive. 

**Matthias Crauwels:** 
Yeah. So a giant snowball rolling down the hill.

**Matt Yonkovit:**  
Wow, this has turned into a very depressing situation. Yeah, we need to go to a more interesting topic, right? Or something a bit more uplifting? So maybe we can end on this here. Because we want to end on the height. Is there something that you're starting to look at to play, test out, that's really exciting. I like to ask people about some new technologies and things they are learning. And have them share some of the interesting fun things. I mean,

**Matthias Crauwels:** 
I made a very blunt statement yesterday in our team meeting, and I told people, if you want to run MySQL on Kubernetes, you're gonna want to run Vitess. Oh, because they do manage the entire solution. The sharding is something you get extra. But you don't have to use it. If you run just your highly available cluster on Vitess, it's taken care of for you for high availability, it will do backups, it will do online schema changes, it will do all the things for you right now. So and that's something that I really am really interested in starting to use much more about. So that's the promising thing in the MySQL ecosystem right now. 

**Matt Yonkovit:**   
Cool. Yeah. And I mean, I think that gets back to that automation. And it gets back to being able to, as you said, automate yourself out of job, which I don't think will actually happen, he'll just automate the more mundane things away. Because I think that there will always be a role for troubleshooting and trying to find out why those applications are are being impacted by those Gremlins. You know, so I do think that Vitess is a great technology, it's something that a lot of people are starting to look into. I think that the whole operator movement in a Kubernetes space  will start to emerge even more over the next year. I think that having the capabilities to just automatically run kind of your own mini Database-as-a-Service is critical, because let's be honest, when you look at these cloud providers, their growth in the Database-as-a-Service base, it's really a powerful message for developers to say, I click a button, and it just magically happens. Now, as a former DBA, as someone in the infrastructure space, I go, Oh, my God, you click a button and you never touch it again. Haha. You know, like, that's bad, because everything's gonna change. But I do like the fact that we're getting more options to make it easier to get started and get rid of those boring things.

**Matthias Crauwels:** 
Yep, sure. Yeah, the easy tasks are already done by the cloud providers, and we just get the exciting challenges of fixing the difficult ones.

**Matt Yonkovit:**    
There. Alright. Well, Matthias, thank you for joining me today. I hope you enjoyed our chat. I did. And if you want to check out any advertisers talks, they're up on YouTube, or on the Percona channel, our Percona website you know, you can also check out Matthias’s blog on the Pythian’s blog space, so he does blog quite regularly as well. So thanks for joining. All right. Bye, Bye. Take care. 

Wow, what a great episode that was! We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.






