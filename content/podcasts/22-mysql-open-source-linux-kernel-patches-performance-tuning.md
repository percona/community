---
title: "MySQL Open Source, Linux Kernel Patches, and Performance Tuning - Percona Podcast 22"
description: "In what will become a recurring feature we “Grill Open Source” talking about BBQ, Open Source, MySQL, and real life fun! Join Marcos and Matt for this fun walk through food, open source, Linux kernel patches, finding difficult bugs in code, performance tuning, and of course all things MySQL"
short_text: "The HOSS sits down with Marcos Albe Principal Support Engineer at Percona and official BBQ master of Percona. In what will become a recurring feature we “Grill Open Source” talking about BBQ, Open Source, MySQL, and real life fun! Join Marcos and Matt for this fun walk through food, open source, Linux kernel patches, finding difficult bugs in code, performance tuning, and of course all things MySQL"
date: "2021-05-28"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-22-with-marcos-albe-principal-support-engineer-at-percona/"
youtube_id: "ZRVmdru5jTI"
speakers:
  - marcos_albe
aliases:
    - "/podcasts/22/"
url: "/podcasts/22-mysql-open-source-linux-kernel-patches-performance-tuning"
---

## Transcript

**Matt Yonkovit:**
All right, everybody, welcome to this special episode. And we're going to change this up. Now typically I have a podcast called the HOSS Talks FOSS. And we're still gonna have that. But with with Marcos here, it requires a little bit more panache, a little bit more jazzing up, because as many of you know who work at Percona, but some of you might not know, Marcos is the Percona official grillmaster and the official BBQ master of all things Percona. So, today, we're going to bring to you something new, we're gonna try it. We've never done this before. It's grilling open source with Marcos. And eventually we might actually do this where we live stream while we both cook, which could be kind of fun. But right now, we've got Marcos here, Marcos. Really happy to have you. It's great to have you here. 

**Marcos Albe:**
Yep. Yeah, it's great to be here. I really love the idea. And grilling open source indeed sounds like a fun project. So super happy to participate. 

**Matt Yonkovit:**
So Marcos, tell us about the painting behind you. 

**Marcos Albe:**
Oh, that's a classic batik. It's a kind of painting done in autoglide. This is done by a guy called Parrisha. He's a friend of the family. And it's a style made with wax.

**Matt Yonkovit:**
Wax?

**Marcos Albe:**
Yeah, it's what's painting. 

**Matt Yonkovit:**
I've never heard of that before. 

**Marcos Albe:**
But for the painting, it's this one's made of wax, actually, it says. So it's kind of like how you call the technique with the where you go with a large stick over with the wax, and you just print out some parts. So you have a mode with the parts you want to colour. You put on some blocks with that colour, and you brace it, and then put another layer with another colour and so on. Wow. Yep.

**Matt Yonkovit:** 
Yeah, they're very, very cool. Very cool. And so. So Marcos, you've been here at Percona for ever? Almost 11 years? 

**Marcos Albe:**
Yes. 11 years. 

**Matt Yonkovit:**
Yeah. And you've been in support? Almost the whole time. 

**Marcos Albe:**
Right. I think the whole time. Well, I was there before support was created. And I am an original member of the original support team. Yes. 

**Matt Yonkovit:** 
Do you remember how support was created? 

**Marcos Albe:**
I remember it was this being discussed. And one day, we were in Cancun. And they said tomorrow, we're gonna start taking support contracts. And basically, two days later, we had our very first support email. I was there with Fernando. It was a very simple thing. And yeah, we started taking support tickets in Cancun during the old company meeting in 2010-2011.

**Matt Yonkovit:**
What's funny is, like, a lot of our stuff started that way. So it's very, I mean, it's the small startup. It's the small open source thing. I remember when Peter started doing 24 by seven, like consulting, you know, he came to us all and I'm like, a Monday. And he said, by the way, on Thursday, we're all gonna do 24 by seven, everybody needs to take shift. Right? And it's like,
What? 

**Marcos Albe:**
That's when it's a seascape need, right? Like this? 

**Matt Yonkovit:**
Yes, yeah, shortly thereafter. That's how I came to work on it. Yeah, a few a few of us actually started in that. You know, we were consultants. And so I did, like 3am shifts, or like the overnight shift occasionally, because everybody was scheduled. 

**Marcos Albe:**
So, yes, Peter wasn't scheduled. 

**Matt Yonkovit:**
But he was. Like, all the executives had shifts as well. So it wasn't just like one person. It was everybody. And it was all equitable across the board, which I think actually helped, because it wasn't just making everyone else do it. 

**Marcos Albe:**
You know, that's one thing about startups and open sources that you have to sometimes grow in steps, and you don't have the funds. You know, like in a Buddhist rabbit company, like Percona. You know, you can say, let's hire 24 persons to just do the night shifts, and let's fill up a schedule of people. And it had to Buddhist rabbit. So yeah, everybody has to put some effort. And I guess that's also kind of goes hand in like that, adventurous spirit goes hand in hand with open source and it fits very well with the culture.

**Matt Yonkovit:**
Yes, yes, it does. Now, speaking of adventures, we mentioned that you're the Percona grillmaster. So what kind of eclectic things have you tried that either like you found like I don't think I like this, but you really you did when you when you go out and you make some some good barbecue. 

**Marcos Albe:**
Well, I'm gonna tell you one that you're gonna hope you're not cross it out. But we eat entrails right. Like, we eat what we call chin to lean. It's like the thing into, into since yesterday. intestines. So yeah, that's something you said yeah, I'm not sure I'm gonna like that. But you know, those are like, but then one day you know, I was like, we also eat the secrets, right? And those you know, which I usually also like, but then you also have the testicles. And that one is well like, I'm not sure I'm gonna like that. And finally one day they told me now you should prepare them and have some fun. It was like, Okay, I'll try it. And yeah, I was actually pleasantly surprised. They are flavourish. 

**Matt Yonkovit:**
So when people come down, do you like to grill like the intestines or the testicles? Or that? 

**Marcos Albe:**
Yeah. Especially sweetbreads are super good. Like, it's super, super good. And yeah, sometimes I will tell people, I will never give them surprise, right? There's like, I will tell them what it is. and convince them that it's actually super delicious. And when they see the platers go away in a second, they actually get convinced. So they usually try it.

**Matt Yonkovit:**
Yeah, it's weird, because depending on where you live, it's a little bit different. Like, what people generally eat and what people are willing to eat. It's just not something that you typically eat here, like in the United States.

**Marcos Albe:**
Then tongue, cow tongue. You know, like, slow cooking. That was something also that it was like, I'm not sure it was like, I don't like the look of it. But yeah, it is like actually in slow cooker is really, really good. Really good. Well,

**Matt Yonkovit:**
You're well, so that's good. Because like, like I said, all the little different individual pieces there. You know, it's interesting, because we just don't try him here. But as you try those different things, you've had to support many different things in the open source space as well. And so over the years, you've had numerous support cases. What typically do you see as one of those, like challenging things that continually comes up? Like, what do you see that from an open source perspective that causes people pain?

**Marcos Albe:**
Well, from the open source perspective, I can tell you what causes pain, all MySQL like, usual things that usually are hard to diagnose, like memory leaks, or some weird crashes that are super hard to reproduce. But, now, there's more and more tooling, right? Like, some years ago, like I would say, five years ago, it was hard to do some performance diagnostic, because we didn't have perf. And we only had  all profile. And it was so heavy. And now we have perf, that improved performance diagnostic a lot. Now we have BPF Trace, which you know, it's the trace for Linux. So that's also a great move forward, right, like BPF and perf have been really instrumental to solving many complex cases, especially perf. Because BPF there are only few customers that are running. So perhaps that's one thing that I could say that it's hard in the open source environment. Moving people to newer versions, big enterprises, they use open source, they now abrasively news, they they are sure that's the way to go. But they're super conservative, and they are still running 2.6 kernels, right. You know, like I have, I don't know, 5.14-5.16 in my laptop. These guys are running 2.6 32 with 1000 patches literally probably 1000 patches on top for the field, right. And some stuff is backported. Some stuff is back ported in an incomplete way. But yeah, that's hard. And sometimes people don't believe you. If you tell them oh that alternate your NVMe drives, they're probably not gonna give you all their juice because there are no problem schedulers. I use schedulers for those. And you know, the drivers for scuzzy. They didn't have the multi cue stuff. So it was like, yeah, you need to upgrade and, and that's kind of hard, like getting people to upgrade, people's running MySQL5.5, Mongo, 3.2. All stuff that its end of life. And because I don't know, I'm not sure how it works in the non open source world, because I was never on the other side of the trench, right. Like they never work in a company in an enterprise that actually was using paid software, like Oracle or whatever. So I couldn't tell how they behave when something reaches the end of life. But I can tell you in the open source world, it's not uncommon to see people going way beyond it.

**Matt Yonkovit:** 
Yeah, I mean, I mean, it's out there, it's open, they figure eventually they can they can fix it if they need to, I guess.

**Marcos Albe:**
Yeah. And it's free. And it's kind of perhaps also people. It's cautious. And they want to wait a few rounds before upgrading. But obviously, they're overdoing it. So, like, a few releases, right, like, a few rounds, a few releases. And that's one thing that yeah, it usually gets in our way to complete diagnostics. What else is hard? It's, it's hard to, to monitor, it's hard to monitor the world now. PMM is solving a lot of that for us. And Grafana, of course, works fantastically. But monitoring 5000 instances, 4000 instances, it's still hard. Finding, get into the problem.
It's still not pleasurable. 

**Matt Yonkovit:**
Yeah, so Marcos as you talk about some of these problems, are there some open source tools that you just that you love, and that you use all the time? To help with you know, some of the stuff you're doing? 

**Marcos Albe:**
Yeah, gnuplot, okay, and a small helper tool that is called Fiji. I lose, I have got, like I do a lot of 
offhand analysis, so we don't have access to the customers monitor. And so we need to get some text form of the matrix of the data, the data collection, we get pg_stat, or show global status samples. So basically, text based metrics, have to parse 1000s of samples, like, like, a day worth of samples. And well, I use awk, sed and all the bash toolkit. 

**Matt Yonkovit:**
Those don't count, come on. 

**Marcos Albe:**
I know,I think I never remembered the name of the actual column, because I have a lot of references around it. But it's something to work with that tabular data. And if you can summarise per column per row, average, whatever, it has a lot of tools that allow you to work with, but yeah, I do a lot of that. I do a real lot of that. What else do I use, I use keyhole, there's stuff I like, from open source projects, like MongoDB has this FTDC, full time data collection subsystem where it's permanently recording the activity and the metrics of the database, the performance metrics of the database. So whenever you have a problem you always have information to work with. And there's a small project called keyhole, that you can feed the data that you know, mount that as a data source for refiner. And then you can easily inspect the previous time of the database which is key for performance agnostic, right, having the data from when the problem was happening. Well, other than other tools I use, that is open source. Well, I use KDE, I don't know I might my desktop has been open source for more than 13 years now. Let's see if I am 11 at Percona, I would say 14, almost 15 years, I've been using a Linux desktop. So everything I use is open source. You know, it's like at home.

**Matt Yonkovit:**
At home, did your whole family use open source then? 

**Marcos Albe:**
Yeah, yeah, the kids do have Linux there. We do have a Windows instance as a dual boot to run some games.

**Matt Yonkovit:**
To gaming you got. No, that's the only...

**Marcos Albe:**
Yeah. Actually, I was reading this article from ESR... And Proton, that's the name of the technology like, where mostly, you can run Linux stuff natively on Windows, right?. So you know what, like, this guy says what's gonna happen? Like, at some point, Windows, now you can run as natively on Linux. Right? It's an elf binary. So these guys says, Well the most natural thing for Windows, whose business is now mostly running on Linux, because of Azure.  Most of the money for Windows for Microsoft comes from Azure. Now, it doesn't come from Windows, and even they have a monopoly on the desktopmarket. They no longer make so much money and maintaining the beast at Windowses and, and also integrate at the same time with Linux, because they need it. Because now it's their main business. It's running on Linux. So the natural thing is to make Linux kernel the Windows kernel. it doesn't look like they're going towards something like that. I imagine Ballmer revolving on thumb, it is great. 

**Matt Yonkovit:**
Oh, yeah. Because Linux is the cancer. Right, right. Yeah, I get that. That was a famous quote from him back in the day, that was a famous quote, It is interesting that, like, you start to see these companies who are so anti open source now they're like, it's the only way. Yeah, but then it but then you have a flip where some of the classic open source companies that are out there are now trying to go more closed source and proprietary. 

**Marcos Albe:**
Well, yeah, Red Hat's moved with Red Hat set IBM move with Red Hat. 

**Matt Yonkovit:**
Yeah, you mean Centos that moved to what is it called… Streams, stream key as streams and continuous deployment or whatever? 

**Marcos Albe:**
Yeah, yeah, it's that that's that well, obviously, that's the beauty of the open source world, right. Like what happened, like there when the guy sent three new projects for kid that tried to provide a replacement, and just I think it was this week. Have you had the last name of the project? 
One of the forks just had a better release this week. You know, like, oh, right this week, so it's not ready for production. It was right in the message of the day. It was the large message of today, saying don't try this in production. But they are already providing an alternative. 

**Matt Yonkovit:**
There's Elmo, Linux, I'm looking Elmo, Linux gets support options. Though, that looks like the biggest one that keeps on coming up when I look for it. Rocky Linux?

**Marcos Albe:**
Rocky. Okay.

**Matt Yonkovit:**
Yeah, it looks like right now. You've got Elma Linux and Rocky Linux are the ones that most people are looking at right now. 

**Marcos Albe:**
I was looking at Rocky. And the most interesting to me.  And yeah it's like, that's the beauty. It's like the community and the people that depend on the things they were not locked in to Red Hat for Centos. They just took the code and said, screw that. I'm just going to use it the way I want. 

**Matt Yonkovit:**
But isn't this what people fear? Like it? Aren't these companies fearful of that? I mean Red Hat a little different. Right? You know, and obviously, with IBM, it's a different company. It really is. It's not necessarily Red Hat. But when you look at other companies who are Oh, we're going to change the licence, we're going to create more as in the enterprise only space. 
Does that hurt? Like the community? Is that something that I think for me, it turns me off where I'm like, I don't want to use that anymore. 

**Marcos Albe:**
I don't want it to be a rhetorical question, right? It's kind of Yeah, okay. Yeah. It's like, if I am using a product and you change the licence, like it happened with Mongo, the change they did didn't affect most users. But they certainly affected their freedoms. Now, those users no longer have one of the freedoms they used to have. And so that that point is they can also change other freedoms tomorrow, they changed it, one that didn't affected you, or apparently, but they could change another one's from and they can when they come up with new features, oh, look, the article I gave you today it's like, you can see great improvements going into the enterprise version, and not into the open source version. And Mongo has done that since the beginning. MariaDB is doing it now with the redo log options, advanced redo log options and yeah, that actually hurts people, when things are geared towards pushing customers into an enterprise option. Like, it's good if customers want to pay for an enterprise service, because the service you can get from multiple providers. And that is like the keys, like that's not vendor locking. 

**Matt Yonkovit:**
It's the portability. Yes. Yeah, no control of your own destiny. 

**Marcos Albe:**
But now, if I give you an option, that only works in in the enterprise version, you if you go away, you no longer have the option. There was a famous discussion in MongoDB, when the lookup
was implemented, look at is like, join four documents. And initially, that was going to be only in the enterprise version. And some people, some very well known people from the community came out and said that's shenanigans, like call shenanigans. Please don't do that. That's a horrible attitude. Finally, Ten Gen, but back end then it was still Ten Gen, I guess, came out and said, Okay. But they can do whatever they want. This is where compromise is not with open source. 

**Matt Yonkovit:**
Yeah. And when you start to see people, take what is kind of proprietary, like a way of running a business and then start applying it to open source to generate more money or to get more revenue. You have some weird things. And I just read this article, and it is not open source related, but I like it because it articulates one of the issues that you have. So McDonald's, everybody in the world knows McDonald's. Okay. Have you ever gotten a McDonald's ice cream cone? So you know, they've got the machine, you go to the machine, you you pull the handle down, and it makes the ice cream come out. So there was this article on Wired this past week, where they were talking about that machine. And it turns out there when you franchise and McDonald's, you have to buy that machine from one company. And that machine is notoriously bad for breaking down, it overheats, the consistency gets wrong, things go a little wonky, it causes all kinds of problems. So it is something that you lose money because it's broken and you got to pay a tonne to have one company come out and fix it. So this company that you know, like people who own a McDonald's figured out they were trying to fix it themselves because they couldn't get the repair guy out there. They found a secret menu that like you know, it's almost like the Konami Code, up, up, down, down like like yeah, you do it on this ice cream machine and all of a sudden it says like, oh, would you like to reset this would you like to like you can fix the machine yourself you can change temperature you do all the stuff that you couldn't do before and they're like, Whoa, this this exists and you can fix all this on your own. So they built a device that allows you to make the changes to the things you can fix your machine that you purchased and bought yourself and you know now they're getting like lawsuits threatened they're getting like you know, like you know that there's all these letters that are going back and forth between McDonald's and franchises. Don't use this because you risk your franchise, you risk your customer base, you're going to destroy this, this is proprietary you know, software or you know, tooling and machine. So that right to repair, which actually is is a is a you know, like a classic right?  That's where it's prevented in the ice cream machine business. And this is where it's, it's interesting because you look at a lot of the proprietary software that we have, you buy it, you instal it, you rely on it. And then if you don't continue to pay the licence, you have to rip it out. And Oracle for years was famous for their audits, right? Like, the audit, like companies left, right and sideways. And like, you've got 57 installations, and you're licenced for 56. You owe us $100 million in fines or whatever. You know, it's not a good situation. 

**Marcos Albe:**
So, two things. One is, I've been reading a lot about something because I have a friend that has a John Deere tractor. 

**Matt Yonkovit:**
I have this happen to John Deere tractors as well. 

**Marcos Albe:**
So yeah it's like, and I've been reading forums about people that are reversing the CPUs in the engines to be able to actually remove it to actually not depend on John Deere’s stupidly expensive aftermarket. 

**Matt Yonkovit:**
Yeah. And just just for people who are watching, just to clarify, explain what the John Deere thing, because they might not know.

**Marcos Albe:**
Oh, well, the details is that basically, the tractor won't start, you run out of tractor. And if you don't call John Deere, there's nobody like, nobody that's going to have an interface to black to the engine, and actually be able to diagnostic started or do anything else. And so they're reverse engineering, that interface, so they can have other people fix it. And because the prices they charge, it's cheaper to buy a new tractor, sometimes, than to continue repairing the same one over and over, because it's also buggy. It's not only that it's expensive. It's also buggy.

**Matt Yonkovit:**
Yet, and so people have tried to hack around that they've gotten threatened with lawsuits as well, there's all kinds of crazy things there. Because it's all about keeping control. What's what's interesting is, with open source, we started with open sources, collaborative, use it how you need to use it, share it, be open and maintain that control and know what's happening behind the scenes, and we just get further and further away. Now, what's interesting is the companies who are out there, and they're built a lot of their infrastructure on open source, they're now having to become the maintainers. And the champions of open source look at Facebook, right? Facebook has more open source projects, and given more open source code than almost any other company out there. And they're not an open source company. 

**Marcos Albe:**
Oh, no, no, they have tonnes of proprietary hardware, firmware and software. But yeah like your example, with McDonald's, like the guys found a way to actually fix those machines. And they started sharing, because they somehow knew that sharing, someone will come up with an improvement, the fix a cheaper way to build that toy, that will plaque to the ice cream machine and fix it. So that's community as well, right? Like, that was a community in action. And that's the one great thing and, and that's why I think Facebook open source that stuff, because it knows that it's gonna have collaboration from others, and it knows it's the right thing. It's no, it's gonna, it also helps them build reputation, its technical reputation. It's goodwill, right? Like you're having genuine goodwill towards the open source community, which is, it's a good asset to have, right? It's like, if you want to hire people from that community to work with you, 
better have good reputation among the community, like who will go work for Amazon, right? Like, they don't have the best reputation. So they have a harder time hiring people from this union. 

**Matt Yonkovit:**
Yeah, and this is where it's weird because you see companies that started on the open source level: Elastic, or Mongo or these others, and they're like, running the opposite way. And then the cloud providers are like Microsoft are like, Whoo opens the doors and like they're crossing over and I wonder if that's because early on the days of open source, it was kind of the anti establishment. And not only was it the anti establishment. You know, it was the alternative to the big providers, like, like, you don't want to run Windows, you run Linux. Right? 

**Marcos Albe:**
It was the communist alternative.

**Matt Yonkovit:**
But it was that and you could make a business run being the alternative? Well, when the alternative becomes the standard? What happens? Yeah, it's a different. 

**Marcos Albe:**
And the thing is, many, many companies find it easier to profit with a product than with a service. And, and that is like, there's no product if the product is only open source, right? Or there's less enticement for customers to purchase and pay recurrently for a product, if there's an open source. And that's how people ends up paying, right, like, someone builds a super good, necessary desirable feature. And you pay for it because it's easier to implement with yourself. And there goes open source, right? But yeah, yeah, it's, like, times back. It was like, the anti establishment, right. It was like the way to fight. How could a small business make France to big businesses? Well, this is like a key advantage, right? This is like, okay, I am the rebel, I have little money, I have good ideas. And now I have a way to carry on with them. You know, I have an operating system, I have a web server, I have a database. I have programming languages and I have all the tooling necessary to develop and create useful projects and put them out there. Make them scalable, for basically free just with my fingertips. And that is like, what actually catapulted open source into the fame, right, like in the 90s, because that it really allowed, like, I had my own business. And at some point, I was considering purchasing Informix licences. Right. And it was like, there were like, 20k each. So I, at some point, Fernando Epar told me Hey, why don't you look at MySQL, rights? Like, it's a sufficiently good alternative? It was early three, CO. You know? So, it, I was like, Okay, I'll take a look. And it was like, more than enough for my needs. Super simple to use. And bam, it ran on Linux. I was already on Linux, I was already using everything else open source. So we went with it. And we saved tonnes of money that allowed us to run for months and months. And that was like, the first hand experience I have with. Yeah, it allows small companies to do stuff that otherwise would be impossible. 

**Matt Yonkovit:**
The entire internet was built that way. The internet, as we know, it would not exist without MySQL, Linux, Apache. 

**Marcos Albe:**
Oh, no, no, no, absolutely not. It will be all big firms. Right. Yeah, yeah. So. Yeah. And, and there was something else I was about to tell you. And now we're lost track. So it was along with the John Deere thing. 

**Matt Yonkovit:**
It's okay. But I mean, like as the technology kind of moves faster in, databases, for instance, they're becoming mostly a commodity. I mean, like it's it's something that people just kind of view as  I need it, I don't want to think about it. Right? I want someone else to think about it. And that leads to a lot of things with either Databases as a service or cloud providers or Kubernetes type. You know, how do I how do I just let somebody click a button and do it?

**Marcos Albe:**
Yeah, yeah, that's obviously I think Peter likes to say that Database as a service is the future and that's where we're heading to. I agree that for many needs DBaaS is the answer, like development teams, QA environments, user exit, user acceptance, environments, for production. I don't think those are as a service, right, like, I mean, I speak with large customers. And they come to me, and they tell me I want to go to Kubernetes and ask them how many clusters do you have? Like, only six clusters? Do you plan to have like 20 more in the next year? No, I think we're gonna stay with things for the foreseeable future. So it's not there where I see the DBaaS thing going, but rather, on the backend, right, like on the on the back in the back office, like people doing development analysts that want a copy to run the reports, stuff like that. Right. And for that, of course, like testing, backups, testing backups, it's an amazing use case for database service, right, like spin up a database, posting these backup, I just to make sure the database comes up, shut it down. Right. Like, it's certainly since the backup verification service. Right. So that's a good one. And that kind of functionality, I think it's amazing. And yeah, open source databases have now become a commodity thing. Yes, I think there's like, a limited amount of flavours to choose from. And we know very well, what they are there will establish they have well defined communities processes like, they are no longer toys, they're no longer seen as toys by anyone. They have been deployed in production for a long time. And people rely on them. So they know, they're reliable. They know what are the use cases are. Yeah like, you could have a menu and click click, click and deploy yours. But again, I personally don't see the production use of it. You know, like, I don't see databases going up and down all the time you production rather.

**Matt Yonkovit:**
Yeah, but I mean, The isn't it the desire, though, for the elastic resources? Right. So you've got a three node cluster, and you need to make it six nodes or seven nodes, and then you need to shrink it back later. Yeah, that seems to be something that that happens more frequently. 

**Marcos Albe:**
Yeah, yeah. So yeah, of course, if you have a peak of load, where you're gonna be reading much more, we can fix it with something elastic. And, of course, it's going to depend on
what kind of replication you have. What's your data set size like. Think about it. I have customers that have data sets in the 11 terabytes, 20 terabytes. How do you spin up instances on the fly terabytes,

**Matt Yonkovit:**
Snapshots?

**Marcos Albe:**
Those lengthy snapshots anyway, and you know, that snapshots don't count for free, right, like 11 terabytes of snapshots is bound to feel any right on read buffers, right. So, the technologies there could be useful. I think it's very, not niche, but you know, you have to consider multitude of things to actually make it safely. Right. 

**Matt Yonkovit:**
So it's not an easy button. You just can't do it?

**Marcos Albe:**
No, no, for example, whether you use group replication or Galera, for example web scale, just web scale. Well, yeah, right, exactly. Mona's web scale, but you need to pay for the hardware, and you need to have time to create the new shardes. And, and again, all those provisioning operations, they do have a cost, they are not magically appearing out of nowhere, they must be taking logs somewhere, or they must be doing some heavy copy on the network, some heavy IO somewhere. So, again, you could make it a solution for some use cases, I'm sure of it, but for, for example, nphc and group replication, they being virtually synchronous solutions, the more nodes you add, the more complex the inter-node communications become. And we know there's an scaling limit for those classes. And adding nodes just out of the blue, right, could make your cluster more unstable. So again, yes, the scaling out is a solution to be considered for many scenarios, just that it's for use case basis that it will be good or not.

**Matt Yonkovit:**
Well, I mean, I think that's like everything right? You know, so you've got to remember there is no one size fits all answer. 

**Marcos Albe:**
No, and that's, that's, that's what I was saying about like, yeah, we now have this array of open source databases that solve different problems Mongo, Reddis, Postgres, MySQL. They have really different use cases. And that's like, where I agree with you. It's like a commodity, right? Like, we no longer have to be investigating or doing considerations or evaluations or anything. These words, this is what the word consumes. We're gonna keep doing it for a long time. You know, B3+ has been there for five decades. And it's not due to lack of smart people in the industry, that we haven't come up with something new is just super hard. LSM is a good alternative, but has shortcomings. FT fractal trees are also another alternative that also has shortcomings. So different use cases. And yeah, people know what's available and know what to use. So yep, that's what I call a commodity.

**Matt Yonkovit:**
So let's take something for let me ask you this and this will be the final question on our grill in open source today. So I'm going to rip this right out of the headlines. Okay, this is right out like, pull it out. So I don't know, have you been following the Linux kernel patch game thing that's been going on with? 

**Marcos Albe:**
Oh, yeah. With the Wisconsin university? 

**Matt Yonkovit:**
Yeah. Yeah. The University of Minnesota. So researchers decided to put security vulnerabilities in PR requests. Yes. See if they can make it through.

**Marcos Albe:**
Greg Cohen was furioas. 

**Matt Yonkovit:**
Oh, yes. Very, pretty much so. Yes. And so. What do you think? 

**Marcos Albe:**
Well, it's a bad joke. You know, I know, Greg gave the university a series of steps they should take on, but I haven't read the steps. I know, the University came back and told him Well, we apologise. And he said, No apologies are not enough. I already told you what to do. And until, until we don't do that, but you know, I haven't read what he demanded. But I think it's a horrible joke. I think it's like playing with fire in a gas station. Right? It's like, Yeah, kinda. But you know what happens if someone, a malicious actor, notices the patches? And they are not noticed by the integration team that will put them in the mainland kernel? And then they actually go live? 

**Matt Yonkovit:**
Isn’t it but is the point, right, like, so it's an interesting debate, because think of it like this. Okay. a hacker isn't going to tell you that they did this. And the fact that some of the requests, I guess made it through, I think there was like a percentage that they said made it through it was like 20%, or something that's telling in and of itself. So condone the action. 

**Marcos Albe:**
It goes like this, how does this work? Nobody reviews all those patches, right? There's what we call a web of trust. Like, if I give you a patch, if I give you a patch and you will say, Hey, I know Marcus. Marcus is a good coder, if there are no loose pointers. And if there is bad syntax, or in general, it looks reasonable, and it passes the tests we wrote for his code, then I trust Marcos is not introducing malicious, I could introduce bugs, but not malicious code. And that if I introduce malicious code, then I'm breaking the web of trust that must exist for a project like the Linux kernel to exist to be possible. Because there are so many teams that are contributing code. And there are only a few guys that are taking all those patches from these teams, and that's how they do because they trusted someone in the team. They have a human link with someone in the team.

**Matt Yonkovit:**
But isn't this the point? No, Marco's like, like, isn't this the point? Right, like, think of this? Okay. You become you have some spy from some country that you don't want to have, like get access to secrets. And you know, or something. Yeah, Uruguay, those, those those Uruguayans? Yes, yes. Who just wants your data. You know, if you establish yourself as a credible person, I mean, that's kind of like a tactic. Right. You know, then what you're saying is you could submit a patch that basically gives you backdoor access to every Linux box running at kernel.

**Marcos Albe:**
Yeah, so I know that there's no perfect security. Right.

**Matt Yonkovit:**
But, but but this is this is the argument that proprietary companies make right is like, Hey, I control that. And I know what's going in. They that's what they say,

**Marcos Albe:**
Well, but I could make the same argument. The guy that finally builds the package, can goes wrong, and write and just introduce malicious code. At the very end, he is the last guy reviewing, how can you tell that the last guy doing the last commit pulling from GitHub and compiling everything into a deliverable binary is not the the guy going rough?

**Matt Yonkovit:**
It's possible, but it does bring up like, again, I don't condone the University of Minnesota stuff. I mean, it's horrible, but they did it. But the fact that they could, is troubling, and on a level that it's like, it makes you think. I mean, is there something that needs to be tweaked with the process? I don't know.

**Marcos Albe:**
Yeah, I mean, more code reviewers and people from the community doing more homework and voluntary work. How do you call it? Oh, my God.. Pro bono, right, like, people from companies like Percona, perhaps people from companies like Dropbox or Facebook does have a team of kernel developers. But you know, people from companies that use Linux that depend on Linux, they could devote some small, very small decimal digit percent of their income to contribute to the Linux project, and put hours on doing code reviews, I cannot think of anything else that will help. 

**Matt Yonkovit:**
Yeah, I mean, maybe additional tests like, like automated tests to test those, you can always work around those. 

**Marcos Albe:**
I couldn't imagine, like automated test, automated test that will go against new, new backdoors or flows. 

**Matt Yonkovit:**
Right. But I mean, you would think that, I don't know, there should be some way and I'm just totally stream of conscious brainstorming, there should be some way to do some sort of, like, analysis of the code and look for anomalous things that have been introduced or like, like different patterns, and the development styles or something, like, maybe something to flag even if it can't, like, say this is definitely it, but it's something that needs extra eye.

**Marcos Albe:**
Perhaps some AI looking for patterns of things.

**Matt Yonkovit:**
Except, but yeah, I bet you, right, more people, right? 

**Marcos Albe:**
Yeah, I mean, that would be a great career. But what I'm saying is people that it's interested in learning See, and kernel internals, that would be a great way to learn, and they could do reviews. And it's a great way, a great way to put your name out there and be part of the largest software project in the world. Because I do think the Linux kernel mass, at this point, be the largest software project work, you will be putting things on Mars and stuff like that. So it's quite cool, right? Yeah, it's a very nice way to spend some time. And if you have 2000 people doing it like, which is not that many, but versus the amount of people using the Linux kernel, right? Yeah. Then well certainly catch a few of those.

**Matt Yonkovit:**
Yep. Well, Marcos, thank you for sitting down talking grilling and open source at the same time. And you know, hopefully, people find this interesting and want to hear more. And if you do give us some topics to tackle or some dishes to make if you want us to grill up some tasty or oddball treats. You know, we can try that on a future episode as well and live stream it. But Marcos, thanks for joining me today and have a great one.

**Marcos Albe:**
Thank you, Matt was really, really fun talking with you and discussing about open source is one of my great passions. So super happy to be here. And I hope people do like it and that we'll be cooking something.

**Matt Yonkovit:**
Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course tune in to next week's episode. We really appreciate you coming and talking open source with us.





