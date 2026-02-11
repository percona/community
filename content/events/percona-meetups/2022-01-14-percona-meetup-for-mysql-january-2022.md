---
title: ' MeetUp MySQL - Troubleshooting Database Outages, Slowdowns, and Security
  Issues - Jan 14th, 2022 at 12:00 pm EST'
description: Full recording and transcript of the Percona MeetUp of Friday January
  14th, 2022 at 12:00 pm EST with Matt Yonkovit and Marcos Albe
images:
- events/percona-meetup/2022.01.14-MySQL.jpg
date: '2022-01-14'
draft: false
aliases:
- /events/percona-meetups/percona-meetup-for-mysql-january-14th-2022/
speakers:
- marcos_albe
- matt_yonkovit
tags: ["Meetup", "MySQL"]
events_year: ["2022"]
events_tag: ["Community", "MySQL"]
events_category: ["Speaking"]
---
If you missed the meetup of Friday January 14th, 2022 at 12:00 pm EST with Matt Yonkovit and Marcos Albe, here is the recording as they talk about why complexity is driving outages, slowdowns, and security issues.  Matt play stump the expert and see if Marcos can improve my MySQL workload.

## Video

{{% youtube youtube_id="s9y0wawM8cM" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Well, welcome, everyone. Hey, we started the live stream a couple of minutes early here, we're testing out some new software. So we figured we'd get everybody a little bit of time to log in, check out what we're doing. And normally, we have a video to start this off. But we wanted to see if we could just jump right in here, see if people can see us, and see the new format that we've got going on. So hello out there in-stream land. And hopefully, you can all see us out there. And if you can give us a wave, we would appreciate it. But we're going to be starting in a few minutes here. Hopefully, you had a wonderful holiday season. But Marcos, this is the first live stream of the new year. So how are you? How are your holidays? What did you guys do?

**Marcos Albe:**  
Oh, well, the holidays were really great. So we have a small house near the beach like, I don't know, 50 miles from here, but it's quieter. And we usually spend Christmas and New Year, okay, a bunch of friends rented the house next to mine. So we shared it with them. And normal regular stuff barbecue went to the beach. I burned a lot of vacation days, I had a nice day. So, what's good for me, really good time. And I have very good, strong hopes and good feelings for 2022. I think it's gonna be a better year. And I hope we finally can see something closer and closer to normality as it was before. So I am glad to also be the first guest in your podcast this year.

**Matt Yonkovit:**  
Yes. So this is exciting for everyone who's joining us, it's a different time, it's a different location, we're actually trying to use new software. So we're actually going through OBS this time, which is a little different. We've gone directly through restream the last few times. Now, we're directing everything through a proxy. And we're doing that so we can get a little more screen real estate play around a little bit more with this. So there could be some hiccups as you watch this. So please bear with us. Let us know in the comments. If this is something that worked, or if there were issues, also, you can go ahead and drop us a line in chat, you can see that the chat is scrolling down at the bottom of our screen here. So we'll be able to see that and give you some feedback as well. So we see that there are a few people on so Marcos, uh you mentioned kind of what you did over the holidays, I did absolutely nothing but sit on my butt over the holidays. So it was kind of just a stay at home, do nothing, although, with the way that COVID is kind of going back and forth. That tends to be all you can do sometimes. So we've got Apachephp saying, Hi, Marcos, hi Apachephp, and we've got Yannis, who is here as well. So that's awesome. Yes, so. So anyways, welcome, everybody. Thanks for hanging out with us. Again. We're trying a little bit different format this week, and a different time. So thank you for ending your week with us. Hopefully, you are getting ready to go off for the weekend to enjoy your weekend time. And thank you for hanging out with us as you do that. So Marcos did some fun, fun stuff. Because this is the first stream of the new year there's some news to catch up on. So I figured why not catch up on some of the awesome news that we have seen or not so awesome news that we have seen over the last few months. And let's take a look here. Here we go. So if you have been following the news, you probably can't get away from the Log4j vulnerability. Right. Marcos, I don't know about you, but this has been kind of a hot topic.

**Marcos Albe:**  
Yeah, yeah. Well the first few weeks after the release of the CB, as we did got Heluva of tickets coming, asking whether Percona products were affected and if any of the services we use to provide customers with service were affected. For example, we use ServiceNow. So glad we are in the clear, but how that goes, once you find the vulnerability in one of them, in a piece of software, it will immediately be under very heavy scrutiny from the security community. And so they get funding more and more flows. And that tends to happen. And I don't know what to tell you, it's gonna take years to fix, I'm sure there are people that are running affected versions that have not even a clue that this is happening. And they have some server running CRM I bet that is SugarCRM, and there's one other big CRM that is built on Java, um, I would bet they use Log4j, like I need to check, right, but something like that companies, small companies that use open source. And they don't have an IT department perhaps, or they hire a contractor to do work when they need. So I'm sure there are hundreds of 1000s of installations still affected, it's really a horrible situation. I don't see a solution unless everything will have automatic upgrades for security flaws, or something like that.

**Matt Yonkovit:**  
Yeah, but so, so but here's the weird thing, right. So this is one of those, everybody uses a library, not everyone understands what the library does, or has visibility into that library. Everybody thinks like I'll just use this, this piece of software, they embedded and then they start to trust it. This is similar to a lot of things, they think about how much we put place trust in, whether it's drivers for your favorite language that connect to MySQL, or cloud providers like you like how much infrastructure behind the scenes might use stuff, like, you just don't know, and there are so many layers upon layers, and applications use this kind of like best breed tools from all these different libraries and components, and they bundle them all together. Any one of those could potentially cause this type of an issue.

**Marcos Albe:**  
Yeah, to me, that are two points of view. And I guess there has to be, we have to find the middle. And there will always be some compromise. But it's like Linus Torvalds, he used to say, like, if we gained in into the security guys, we will have never released Linux 1.2. So like, you can't stay on the same libraries for 20 years, just because they're stable, and they got fixes, you do need to move forward in adopt new structures and new, like you said best of breed tools, while at the same time trying to be somewhat conservative on your production environments, and perhaps how things longer release cycles? I guess, there should be some consortium made by some larger cloud providers, that they could just spend time doing analysis for security for the benefit of the community they benefit from because they benefit from cloud providers, large cloud providers, they benefit from the open source community. And this is a topic that comes up often right, like, what do they give back? Right, so they do give back? I'm not saying they don't complain, perhaps they could give back a bit more. And like you said this is something they use, and what's the worst part in my mind is that you cannot tell what patches they have a blind on the infrastructure or not. Right. Yeah. obscurity, but also, like, so much obscurity that I'm a bit afraid sometimes. So? I don't know. Yeah. It's a good situation.

**Matt Yonkovit:**  
But now, let me like here now we're starting to see that this is like, Oh, my God, open source is so vulnerable. it, this is a national security issue, this is something that we need to start to regulate. Right now, I'm seeing Google calling for new government actions to protect open source projects. Google wants to work with the government to secure open source software. So there's this big push in, and we see this quite often. We saw this with solar winds when solar winds, which is not open source, had a plan or ability where everyone lost their minds and called for additional regulations and things. This was something very specific, that caused a lot of people to take notice and all of a sudden, oh my gosh, look at it, think about how much open source software that we've deployed, and how much of it we don't even know what it does, we just deploy it.

**Marcos Albe:**  
Okay. So we know how to build secure software, like it just takes a lot of work. And it's, I'm sure like, developers will love to follow this book, and learn more about security and do the things right. But there are many times pushed by Capricious. And I like to say imaginary deadlines like something, someone came up with a deadline without really taking into account a lot of things that take time, like security. And so developers are forced to follow again, crazy deadlines, they don't follow best practices, and many times they don't have the training open source has been done by hobbyists, people at home, you don't know if the guy has a degree or not, or the guy could have the best intention and still be introducing a fat bug, right? Back buffer overflow. I remember Linus saying that a lot of his work was creating macros in the kernel. So that other kernels developers will not botch it. And

**Matt Yonkovit:**  
yeah, defensive coding, right? 

**Marcos Albe:**  
Exactly. So we know how to build good code, we just don't, and there has to be a reason for that. And the reason is the scarcity of resources to produce code, because I don't think it's a lack of money, because I do see companies giving out very good salaries and a lot of money. They just come because they can find people. So the job market was insane at the time. And it's because there's such a lack of developers and technicians at large. That makes it impossible to produce quality code. So if the government wants to help, I guess they should focus on education.

**Matt Yonkovit:**  
So let me ask you this, how much of this do you think is because a lot of really popular open source software is really underfunded? Right, like so I know a lot of people who have created projects or

**Marcos Albe:**  
I don't think WordPress is underfunded. But the quality of the code leads quite a bit to be the siren.

**Matt Yonkovit:**  
Well, so I mean, okay, so there's two components here, right. So there's the libraries that people rely on. And let's talk specifically about whether it's JavaScript libraries or Java libraries, there are all kinds of open source libraries out there, that they're maintained by a one or two persons group who are doing it because they love to code. And they are not, they don't have deep pockets. Right. And so that's, that's something that happens quite regularly. And it does expose some concerns. Now, this one came up the other day. And, yeah, I don't know if anybody saw this specifically.

**Marcos Albe:**  
I empathize with them. Empathize, but that is basically blackmailing.

**Matt Yonkovit:**  
So let's, let's explain to those who are watching what this is. Okay. So there are some very, very popular JavaScript libraries out there that you could get through NPM colors and faker. And those awesome projects. Yeah, it's downloaded. I think they said like 20 million times a month or something ridiculously large. And a lot of people do continuous deployment, continuous integration, where they're grabbing the latest releases to make sure that things are up to date. Well, the maintainer decided that he was going to break these and so he introduced breaking changes to cause all of this to break because he was sick of giving people his software for free. which is a whole different angle than the Log4j which Log4j was an unintentional thing. This is completely intentional.

**Marcos Albe:**  
Let me give you my opinion because again, this is my opinion, not Percona. So we are an open source company. And we know that our company's making billions of dollars out of the software, we release Oracle doesn't say they released MySQL, they know that our company's making billions of dollars out of it, we make a business out of their software. And they don't release breaking code. I think it's wrong.

**Matt Yonkovit:**  
Of course, it's wrong, right

**Marcos Albe:**  
To get a six figure salary like this guy claiming demanded, you can go into the job market, and you might not have all the time to devote to that, or perhaps you will find someone that will hire you to do just add on something else but if you want to keep your code and do all your code, then you have to start a business where you sell support, or you sell licenses for embedding, or you can be up straight up front and said, Well, my, my sources no longer code, if someone wants to maintain it, fine, I'm gonna start selling licenses. It's valid and you're, you won't be considered evil. If you do, If someone wants to be maintaining an open source piece, they can pick up the glove, and just continue doing it. So you're not evil, because you stop doing open source and you decide to sell the license, it's fine. Everybody has to make a living. Right. So but releasing broken code, come on?

**Matt Yonkovit:**  
Well, yeah, I mean that that's a real low blood that hurts, right? And I think that this is, it leads to this fear around open source. I mean, with Log4j already out there. I've seen a lot of people jump on that and say, Well, this is why you have to be leery of open source. Right? And that's not true. Right. But when somebody goes out there, and does this, it makes us all look bad in the open source community. Right, because, oh, who else is gonna do this? What if, and this furthers that discussion about government regulation, right, which is like, Oh, do we need to regulate this? And we don't need open source to be nationalized like, Oh, this is, uh, this is now a natural resource for the internet protected

**Marcos Albe:**  
The state schools on any software, right? I mean, not open source. Like, what if I make an open source library?

**Matt Yonkovit:**  
Yeah, there's all kinds of craziness around that, but I mean, yeah, yeah. It's something that I think we need to be mindful of. 

**Marcos Albe:**  
Again perhaps what the government can say is, if we're gonna adopt a library, then it has to go under certain scrutiny, to be approved. 

**Matt Yonkovit:**  
And yeah! like a certification or like, like, you've stamped approval, like, like this, this is, this is this version, right. And you almost have to go version by version, because in the case of Faker and colors, right? That was the version that worked, it probably was stable. They introduced something that caused issues boop. And it's those small things that I think everybody's just gotten used to updating and it works. It doesn't always work.

**Marcos Albe:**  
Oh, well that's not true. Like, things don't always have to work like in databases, we tell people to be very worried about upgrades and to take them seriously. 99% of the time, they just work and people are happy, and things work better and have fewer bugs in previous versions. But we later find more bugs in that version. And you'll never know new bugs are introduced. And QA has come a long way since I started doing development 20 some years ago. Like, I do see better quality code that I don't think you are going to get back free software anytime soon. It just takes too much money and too much time and effort. Again, there's a compromise to be made, right? Absolutely. And testing, long burning periods in QA and user acceptance environments. Those are going to go I guess.

**Matt Yonkovit:**  
Absolutely. So I'm curious if anybody out there in chat land or who's watching the stream, either live or after? What are your thoughts? Do we need more government regulation on this? Is this something that people really think is a concern? Is it something that we should do more of? Do you have any ideas, questions, comments, we'd love to hear from you. Feel free to fill in some of those comments, if you'd like. Now, what we're really here for though, Marcos, we're really here for MySQL, right? So we love to talk open source and it benefits us to talk a little bit about that news. Because even if you are a DBA or a sysadmin or SRE, these security vulnerabilities and these these issues, continue to cause issues problems for folks. And you might get asked, so we wanted to start with that. But we are here to do some awesome workaround MySQL. So let's delve into that. So what I have done is I have set up a very basic MySQL system. It's running some workload. And it's basically defaulted. I did turn on the slow query log, so we can collect queries so that I did do that. And I and I connected it up to PMM. But it is largely unconfigured. Okay, so it is kind of like you have just slapped down the install, you have started it up, everything should be in the default configuration. And what Marcos has agreed to do with us is to go through PMM go through the configuration and set it up. Like he would set up a new system to make sure that it's actually set up from the beginning to reasonable defaults. And he's going to tell us why some of these different configurations matter and what he's looking for. So that's what we're here to do. So Marcos, would you like to take it away, my friend?

**Marcos Albe:**  
Yes, sir. So let me share my screen then. And bring this guy. Alright, so here we are. And my friend, Yonkovit, told me there was MySQL here and to go to MySQL summary, which is my favorite dashboard. And I'll find some instance here.

**Matt Yonkovit:**  
Thre is the MySQL one. Yes, that one. There you.

**Marcos Albe:**  
Oh, workload. Great. So right away, I saw the latest version. It's good, little workload, I don't know if that's good or not. Current QPS is not something that 's a benefit, right? It's a liability. Rather, you don't want to have that many QPS. If you have left QPS, because your cord is too fast, very fast. And a very small buffer pool. We should see if that is actually bad. Obviously, you have plenty of growing rooms. So that's also good.

**Matt Yonkovit:**  
Yes, sir. Because like everyone else on the planet, I went out and I got a box 10 times larger than the size that I need.

**Marcos Albe:**  
I've seen that I've seen

**Matt Yonkovit:**  
Just in case, just in case.

**Marcos Albe:**  
Yeah, yeah. Because they were going to scale. So I'm going to do some reactive configuration instead of I could open the mycnf and just taking what, I believe it's the proper configuration for this machine. But what I usually will do is go through the workload, and observe bottlenecks. And then provide configuration advice to get rid of those bottlenecks that is what we normally would do. And it's what I'm going to start there. And then if I might add some other stuff at the end. 

**Matt Yonkovit:**  
By the way, Marcos, I have Yes, some semblance of an idea. And how many transactions and how many user interactions that should just handle if it is configured somewhat reasonably, but I'm not going to tell you what it is, we're gonna see how close you can get to it.

**Marcos Albe:**  
Oh, okay. Okay, I like that.

**Matt Yonkovit:**  
And feel free to jump in with those who are watching at home or on your phone or wherever, if you have questions, feel free to stop us and ask us any questions that are going on.

**Marcos Albe:**  
Alright, so the thread cache, good use has threads created here, and they're just a bit larger, slow queries, it looks like you have a sloping log with long query time equals zero. So what it's gonna happen is once we get to the three 4000 words per second, these might start impacting performance in a way that is gonna show in the latency papers. So, I will rate the limit on the Percona server, I will go ahead and set a rate limit. So you can keep one very tiny consideration, but instead of capturing every query you will capture, like one every 10% or one of the 5% or get array feeds so it won't have young sources.

**Matt Yonkovit:**  
So, what sort of impact does that have on the system when you set this low query time to zero and just let it collect everything?

**Marcos Albe:**  
Well, those rights are synchronous. There is no buffering. So when you have three 4000 Synchronous writes, they just, so how much does the right thing, let's say you have a reasonable drive, and it takes 15 microseconds. So that's like the 2000s. So 2200 of those writes will make one millisecond you're gonna start seeing parties that were sub millisecond, start increasing their time. So at some point, again, the lock on file, it's also going to become hot you cannot just write competently, like, there has to be some sort of ascension will be good this, and that's gonna start to add up as well. So that is the kind of impact you will see it's, again, other latency to the query, if there is so much added latency when you have 20,000 frames per second then you might be adding 100 milliseconds to your parties so they're gonna startup, then mutexes become hot. And the thread cache will also be bleated and you will be creating threads, that's also expensive. And the table open cache, it's also perfect per table. So the more threads you have the larger table open cache you need. So that's going to become saturated for mutexes, more file rates. what, as you climb up in concurrency, and you approach separation, then things become unstable. And if you don't do anything to go into a spin-off death, right? Okay, probably gonna end up with very long semaphore weights and the server.

**Matt Yonkovit:**  
So the bottom line is, while it is important to collect as many query details as possible, you don't want to collect too many because it can impact performance and have the opposite effect of what you're trying to do. You're trying to tune the system, you might add 20% workload to the system, just to keep up with that query workload.

**Marcos Albe:**  
The same goes like, there are things that are hard to monitor that are hard to instrument. Because imagine instrumenting, memory location, everything in the computer's memory allocation, you're basically instrumenting, everything that happens, yeah, it's, it's insane, you're like, you're going to be adding billions of events per second. So even if you do it with BPF, and you do kernel aggregation, and everything, it's still a killer. The same goes for waits in the performance schema like, performance schema, you have transactions, the transactions are composed of statements, the statements are composed of events. And these events will suffer. Yeah. So you can estimate the first three. But the last one, if you instrument all the waits that MySQL can track, there will be some that are too much; they're going to collect millions and millions of events. And that's going to be worse than no monitoring. So it's better to leave perhaps with the illness you have than to take away your lever to see if it's good. So this is a bit of that, right? Like, you want to actually do a monitor and get detailed data. But too much detail. It's a burden on the server itself.

**Matt Yonkovit:**  
Yeah. We have a question from am William specifically on that: Is there a preference between the slow log or the performance schema?

**Marcos Albe:**  
Oh, good question. So, performance schema does have some limitations. And it's an important one sometimes, which is it doesn't keep track of row level lock waits. Unexpected, but that's what it is. And also, you might lose events, because the performance schema is based on fixed size memory structures that you have to really mention. And if you keep track of your show, global status or if you use PMM

**Marcos Albe:**  
You're going to see that there are last events to show global status. These last events, if you see them growing above zero, it means, hey, I didn't have the chance to actually record everything about these metrics, because I didn't have space when the event came in, I had to discard it, basically, it will discard the event. So you're not gonna see everything, or you're, you will, most of the time see everything. But it might be that you don't see anything because you have too much traffic. It's nice, because it's in memory, it doesn't hit IO so hard. It happens naturally, as the events are executing, you can see live things in the current, there are a series of tables that are called current, those will show you the in-flight events that are useful when doing complex performance diagnostics. And again it's just you do a select star from, I can never remember the name of the table, but it's a simple select star. And you get a good profile. So if you do that, as something regular, like you log into the servers, and you want to check performance very quickly, and what your credit profile should look like super handy. If you want to do more detailed monitoring, and you want to have pages per query in an easy way, like you could do it with performance schema, but then it's going to not be perhaps, to have third party pages and this log is sometimes easier to do that, especially with Percona server.

**Matt Yonkovit:**  
And are the overheads for each comparable?

**Marcos Albe:**  
Performance, a schema is going to have limited overhead, because it's going to discard that.

**Matt Yonkovit:**  
So it's going to get rid of certain things under the workload. So it's kind of throttle,

**Marcos Albe:**  
Go out to some limits

**Matt Yonkovit:**  
It's like, oh, like we mentioned throttling the slow log, like when you said, you're going to put some throttle on that. It's basically built into the performance schema.

**Marcos Albe:**  
Basically, yes, yes.

**Matt Yonkovit:**  
Thank you for the questions. AM Williams? 

**Marcos Albe:**  
Very good question, indeed.

**Matt Yonkovit:**  
So okay, so we've got that you want to rate load the slow queries? What else do you want to do? Let's continue our walk through here.

**Marcos Albe:**  
Yes I, as you can see, I go down, and in turn on and off metrics from data series from each of the graphs. That's because sometimes it's hard to have the same. Oh, my God, lost word. Definition, no, it's my lost word. So something's only happening once per second, other things happen a few dozen times. And they are morphing. And you don't see the spikes. So the same magnitude, right, the thing that manages that is the word. So to see the spikes, what I do is I turn it on and off. And so they're going to be each on their own magnitudes. And they're not going to care if there were larger spikes of some other metric. So I go down on each one. And what I try to do is find things that I know are bad query patterns, or, bad under dimensional or over dimensional things, that are the results that are unique there. This winter. It's called, oh, my God, I forgot the name is sufficient for MySQL performance. And he says something that it's very good analogies, like, the workload is the light. And MySQL is the prism. And the metrics are the reflection of the light, right, is the composition of that light. So it's like that, like, the metrics I see here are the result of the workload. So, the thing is try to understand if that is okay, if I do sort merge classes I can tell you might be doing very large sorting. So I will try to find queries that will respond to these, I might try a slightly larger sort of buffer size, not too much larger that have very weird effects on that buffer. And as I go through the metrics, I will look at the values in the configuration to try to understand the prior if my hypothesis is correct, Right. Or I will try to look for the workload to understand if my hypothesis is correct. So it's a back and forth between looking at this, the metrics, and looking at the configuration and the actual work. So I, again, I do hypotheses, okay like, I look here and say, again, what would be said, okay, yeah, I was looking at threads made that and I look at this, and I could say, Okay, it's because you have a very small thread cache but then perhaps I will look at the workload, and it will see that there's a spike in arrival. So your thread cache might not have been insufficient for your general workload, but just for this period of time, that was problematic. So I tend to look at both and also working with the customer asking them, okay, what is your expected workload, right, like, like, do expect to have like thread 30 concurrent running queries, or it's like, you normally will only have like, five, so, or I will go back in time and look at other times to see what it looks like.

So, going down okay. Nothing looks like this case, this peak is killing me, I'm just going to ignore it.

**Matt Yonkovit:**  
So the first peak there, yeah. It's the start of the workload, right. So, yeah, so that's, that's kind of normal. Right? When as you as you look at that,

**Marcos Albe:**  
But yeah, it's not at all unexpected. It's just that if you have that peak in the graph, again, it's going to dwarf the rest of the values. And, then you cannot clearly see where the peaks happen in this smaller scale. 

**Matt Yonkovit:**  
Yep. So you want to narrow that down and get rid of that timeframe? 

**Marcos Albe:**  
Just go out of the sun now the scale is for most of the workloads

**Matt Yonkovit:**  
Did I lose Marcos?

**Marcos Albe:**  
Last oops, Marco so yeah, yeah, I have a black out you still see my computer? No, you cannot see it let me

**Matt Yonkovit:**  
Well I can see your screen or I can see your screen your screen is still being

**Marcos Albe:**  
That me who the Personal Hotspot here just one minute

**Matt Yonkovit:**  
This is the fun stuff with live right there you are again Hello. Welcome back. See and this is what happens live right is sometimes you run into these these these little issues

**Marcos Albe:**  
Just one second down the second

**Matt Yonkovit:**  
One, though, is I just adjusted the workload a little bit too so I might have caused this outage I might have stressed the system so much I might have brought down the power in some countries

**Marcos Albe:**  
There was some Christmas movie where the guy turned it on. We need to power on.

**Matt Yonkovit:**  
Yeah. Yeah, that's National Lampoon's Christmas Vacation. Yes, sir. Yes. Great movie for those who haven't seen it.

**Marcos Albe:**  
Old movie from the 80s brightly

**Matt Yonkovit:**  
Yes. Chevy Chase.

**Marcos Albe:**  
I can not. This is killing me.

**Matt Yonkovit:**  
it's always worse when someone's watching over your shoulder.

**Marcos Albe:**  
Yeah. 

**Matt Yonkovit:**  
The pressure is on to jump back on and get things moving.

**Marcos Albe:**  
Okay, let me get back to that meeting from my computer. I got a connection error. And then bear with me please. Man, and it's literally 40 degrees. So 105 Fahrenheit

**Matt Yonkovit:**  
Yes. And here I am in North Carolina preparing for an ice storm snowstorm which we never get. So. So there you go. So, AM William, we will try and answer your question. But can you describe how you might assess if your network hardware or your stack is saturated and performing, as you would expect? So, as we go through, we'll try and keep that in mind as well.

**Marcos Albe:**  
Yeah, yeah. I'll show you where I look for network saturation. There's one metric explosive here. And then I think we can see others through. Let me go there. So you don't see the memory is so large here versus the InnoDB buffer pool that you can see that the buffer pool is not visible. And that's what I was talking about the scale. Play turns on each one individually. Let me turn off the audio for my ups.

**Matt Yonkovit:**  
Okay. So we are on backup power. That's how dedicated we are to you as we experienced power outages. And we still continue the live stream. Yes, sir. That's right.

**Marcos Albe:**  
There you go. Oh, let me refresh this last one hour. So you said you would increase it. Oh, what happened here? Less listens.

**Matt Yonkovit:**  
I said I changed the workload.

**Marcos Albe:**  
Yes, sir. Oh, you didn't increase it, you just changed it? It's very subtle. What have you done Sir Yonkovit?

**Matt Yonkovit:**  
Well, you just continue that down your path, and it will eventually catch up to you.

**Marcos Albe:**  
Yeah. So mostly deletes. That's, that's so your workload. Selecting them deletes your database is gonna run out of rows very soon. I think almost this is probably being sir. Set. So we discussed this in a previous podcast. This is your Python.

**Matt Yonkovit:**  
Yeah. It's the pinging that I like to say to make sure that the server is still alive.

**Marcos Albe:**  
Yeah. So right. I'm really only and oh, you're reading more rows. Let's go with more rows

**Matt Yonkovit:**  
Do you never know what fun will happen next? I feel like the Dungeon Master of a d&d game. Right. So I can purposely Oh, what, I need to switch back to this way to show yeah, that's a little easier to see that screen. Alright. Ah, sorry about that, everyone.

**Marcos Albe:**  
So it looks like the updates plummeted. And it's possibly because they are the updates itself are scanning more rows to fulfill the aka

**Matt Yonkovit:**  
Continue, continue your configuration changes, you're looking at things to change the configurations.

**Marcos Albe:**  
Well, of course, like if I see these and it's so that such a small buffer pool, I will immediately go

**Matt Yonkovit:**  
Here and change the buffer pool. Right.

**Marcos Albe:**  
Duplicate music is and yeah, we just got to verify that our pages coming from this

I would go to my SQL interview details so looking at the last one hour, hello. There we go Disk IO. Disk IO review t

**Matt Yonkovit:**  
There could be some locking going on right now.

**Marcos Albe:**  
Yeah, I will find out

**Matt Yonkovit:**  
Just over the last 10 minutes, right? It was your power outage that caused it

**Marcos Albe:**  
So I've seen great Whoops, that's a lot of f6 Roll up blocking. There is no blocking. Let's go to the last place to make the average better there. The amount of bufferpool requests is slow. This is more for write workload to write this is your right ahead log your redo log. And basically, everybody believes it's meant for crash recovery. But that's just a side effect. The redo log, or better called the write ahead log, it's meant to transform what would have been random writes into serialized writes. And then the random writes will happen in the background without interrupting the report. So very small, when it fills up, it will help your workload.

**Matt Yonkovit:**  
So right now, you've suggested increasing the buffer pool rate by doing a rating or load throttling on the slow query. And now you're talking about changing the redo log size?

**Marcos Albe:**  
Yeah, I mean, again, I guess we should have more than 10 minutes worth of data to give you more precise advice. Valley looks like those things that will immediately change like this is, by today's standards, pretty small.

**Matt Yonkovit:**  
Well, and so and so Marcos, how big is the dataset?

**Marcos Albe:**  
How big is the data set? Um, I will go so I'm not sure if your bmm has it enabled? Most of the time we don't see it enabled? Because it will take too much. Movie Json test. These have total, so

**Matt Yonkovit:**  
I can't remember. Now that's No, it's It's right that they didn't index it. So the graph is right there. It's the graph. See, so you're, you're you're at about 11 or 10 gigs. Yeah. So So 128 meg buffer pool with

**Marcos Albe:**  
You are the first customer in a long time that has this enabled security, because most people can not use this because they have 1000s and 1000s of tables. Well, when it is zero, it is better. But in five, seven, and before, this will have caused a lot of contention, because it will have to read the reference from the disk. So it was a pain. It was a painful thing to do for more than a few 100 tables. So 9- 10gigabytes. And your buffer pool is 128 megabytes, I will dimension to something like 16 gigabytes to give you some growing headroom. So yep, that that will be I wouldn't have done the query manually on information_schema, to be honest

**Matt Yonkovit:**  
There's nothing that prevents you from going to the shell, Marcos, you don't have to stand up if you can.

**Marcos Albe:**  
Oh, well, let me look at the blog by our fearless leader. Donor size. Plot. Yeah, there we go. Our fearless leader wrote this else ago

**Matt Yonkovit:**  
2008 Wow. It still works.

**Marcos Albe:**  
Still works. It was a good party. Why did the query go like this? Let me stop playing so you can structure again with everything my screens are? This is ...

**Matt Yonkovit:**  
you root and then the password should be good. Yeah, there you go!

**Marcos Albe:**  
All right. So much news. For me. screamer Yeah. Oops. That's just kind of the slowness I was talking about.

**Matt Yonkovit:**  
Well, so keep in mind that the system is relatively busy.

**Marcos Albe:**  
Or let me do something for you.

**Matt Yonkovit:**  
So I'm wondering, like it's interesting, Marcos. I often like myself personally. I look at the system before anything else in a lot of cases. Yeah, so

**Marcos Albe:**  
So what I see is you're killing the disk, of course. And when people tell me Marcus 6% is not killing anybody? Well, but that's for all your CPUs. Oh, great.

Um, so you have how many students here do chorus, and a bunch of them are running, one of them is running turbo once or run it up to speed. So seven out of eight, it means you could have like, someone waiting, 50%, something like that. So let's see. So you can see, actually, there are some guys winning 20 and 50%. And all of the threads are IO wait actually. And it's more IO await than actual userland CPU. So it's dominated by Wait, if you do. better, that's better. So I see. It's writing bonds, you should get a better drive by? And what are the rates? This is so weird IO Stats

**Matt Yonkovit:**  
Why is it weird IO Stats?

**Marcos Albe:**  
It's from the 5155 10, they changed the layout. So the order of volumes is somewhat different. So I was just looking for the games. And it has these, which I don't know what it is, to be honest. I will look at the man for this. But the one I look for is this one, this is our go to metric to tell if a device is saturated. 

**Matt Yonkovit:**  
So what is that? What is that,

**Marcos Albe:**  
That is the average size. And it's when it goes above one, you can tell that it's saturated. So where does that number come from? It's not very simple. It's kind of convoluted to explain, but basically you could look at it thinking it's, if you were in a supermarket and you have multiple cashiers, and you get to the cashier, and either there is one that it will be able to take your request immediately. Or you have to put yourself in the queue. So if we looked at the cashier situation every time, right, we can see whether we always see people in the queue or and if they wait that whole amount of time or not. So let's say a look every 60 seconds. And then if I only had to wait 30 seconds to get into the cashier, then the queue size was still one five. And if I have to wait the full 60 seconds, then it was one there. If there's more people in the queue than the queue, then that has to wait for a few minutes, then it will grow. So what is saturation? Saturation is not linear, right? At some point it has a needle and it drops. But it's not that things don't scale linearly, or not to infinity at least say scale linearly apart.

**Matt Yonkovit:**  
So when you see this, what do you think we should be tuning?

**Marcos Albe:**  
When I see this, okay, again, we want to alleviate the IO and larger if you have a larger buffer pool, the pages are going to remain in memory and then you're going to be doing less read IO but I can see that you don't have any me that goes that all you do is write and write and write and write. And why is that because probably you're flattening. crazily, right, like, you're probably flushing too much. Why? Because your redo log is so small, that it has to be empty too fast, it gets full too fast. And when it gets full, InnoDB gets desperate to empty the redo log, because it cannot continue to operate if it's cool. Because otherwise it won't break as a guarantee of durability. So what I will do is, I will have to restart the instance with a larger redo Log. Can I do that Sir?

**Matt Yonkovit:**  
Of course, you can. Right, I can restart the workload when you're done.

**Marcos Albe:**  
Right? Oh, nothing here? Nothing? Nothing?

**Matt Yonkovit:**  
Well, no, it's just in a separate one. Under the MySQL d. And my is gonna be the MySQL, mysql.d is under the yeah.

**Marcos Albe:**  
There you go. Ah, much better. Of course, this is somewhat suicidal, like, don't want to keep only one day worth of bin logs, unless you monitor your databases on the weekend, you have someone to react within a few hours.

**Matt Yonkovit:**  
So for this, it's a test system running. So I want to get rid of the bin logs as they write them. So I don't, but it's right there.

**Marcos Albe:**  
Okay, so I will do innodb_log_file_size. And here comes the question, right? Like, what is the big log file? How big should the log file be? We can look at checkpointing and flushing. To quantify it's so now, logins. never remember that that graph is just an instant PMM dot one, it is easier to spot the graph. But basically, what we want to see is how much you're writing here? Well, I think you should probably do more than this. Basically, what I will do is the regeneration rate is okay how much I write to the redo log. And you want to make this type large as reasonably possible. What is Reasonable? Reasonable is an amount of time that will allow you to write at that rate for the duration of your big workload. So if you have a big workload, we used to say one hour, but it doesn't mean much, right? Like why one hour, it usually is enough to withstand most bigs. Like it's a good rule of thumb. like, if you don't know where to start, start with one hour. But if your big workload usually is three hours I will dimension it to withstand three hours of non-stop battering all redo Log.

**Matt Yonkovit:**  
So if you've got 100 kilobytes a second, you want to then say what that will be over an hour?

**Marcos Albe:**  
I will multiply it by 3600. And then I will multiply it by three and 200 kilobytes, that's 3.6. That's 10 gigabytes. So there will be four mentioned.

**Matt Yonkovit:**  
Wow, that's a really big, redo log size, isn't it?

**Marcos Albe:**  
No, no. You fear that the only thing you could fear is their recording times, right? I mean, we're not going to be arguing about 10 gigabytes of disk space. Now in the 21st century. And the if you fear the record, storytimes.

**Marcos Albe:**  
First of all, having big redo logs doesn't mean you're going to have that amount of databases to recover. Because when you do recovery, you only have to do recovery of the pages. True. True. So of course, having a larger redo log, the purpose is to allow more pages during the heavy write periods. So what I'm saying is, okay, first check, if you can wait, like you should do some testing to see if the recovery times are acceptable, just like you do for backups, right? Like, you said, Okay, we want to recover our backups within one hour. Like, I want to recover the instance within experience, then you should generate a lot of free disk pages and go through the crash recovery, to see how long it takes in your system. It's not hard to do, I mean, building up the pages. And it will allow you to estimate how bad it will be. And then if the time of recovery is unacceptable, you should consider having a taser that is semi-synchronous or Vitaly synchronous stuff, where you can failover to the next instance, when this one crashes, so while the recovery is ongoing, you can failover. What are the following options? Well, you could get faster drives, or you could try to convince your developers to write less. But if you want to do it, I mean, it all depends on your right rates. It Okay,

**Matt Yonkovit:**  
So let's make it 10 gigs. I mean, I what?

**Marcos Albe:**  
I think I did the wrong math. I did. I must have done

**Matt Yonkovit:**  
otherwise.

**Marcos Albe:**  
So let me see. 100 kilobytes, it's 10 to the four right. So that's over because of one hour, over the course of my big word liberation. So that's one. long video, yeah. So sorry. I added an unnecessary sealer. So very good. Okay. So I will make it 100 megabytes because we have two files, so two files, 224 megabytes each. That's, that's, um, what else do you normally tune along these to flush to throttle flash rate, you have a good stepping here, I need to be IO capacity. 200 is very reasonable, and is what everybody should have. Unless they have proof, they need more. So normally, people will set this to 10,000 5000. Because

**Matt Yonkovit:**  
they're like, Oh, of course, I want faster.

**Marcos Albe:**  
Yeah, just eat all the capacity you can. But actually, you're just forcing the flushing to happen too early. And the guy will be happy to flush a lot. And again, you want to keep beauty pages, beauty pages are the performance optimization, not flushing more. So these pages are a performance optimization. Because imagine you do an update, imagine you have a hot roll somebody mentioned a popular video that is getting lots of hits, and you update the views counter 100 times per second. If you have a very high capacity, you're probably gonna ride that road 50 times per second to disk. If you have a smaller capacity, you probably are gonna run it once every few seconds. And then you're actually only doing one write for hundreds of updates, because all the rest were in memory and on the redo log. But then when it goes to the final tablespaces only one of them is going to do the latest one after. And so that's a very big optimization. And again, sometimes you can write the whole page, when you go to this, you write the whole page. So if you're affected by neighboring rows within the page, if you delay the flushing, you are benefiting from flushing this single page for multiple row changes. So it's important not to tune this up, unless you need it. And when you need it, when you have a large enough redo log, and you still see the antique pointed bytes approaching the max checkpoint age, then you will want to increase this and it's gonna impact your eye. Okay. Um, I don't know if I want to tune everything right from the hip, but I will do it. 

**Matt Yonkovit:**  
which is probably the most used and most recommended setting, right is the buffer pool size. Because that's going to dictate how much memory you're using basically,

**Marcos Albe:**  
In your case, you have a 10 gigabyte data set, but you were hitting a small portion that fit in the small buffer pool we have, because we saw no reads. And we saw no reads for the buffer pool. So let's see. You can see bytes in which this column remains ridiculously low write bytes in bytes read into memory. So your IO is pure writing. So I'm gonna tune it, because I do see you have the dataset. And whenever you want to operate on it, you will need it. If you want to take a logical backup, then you want to feed your data, set the memory if possible, or as much of it as possible.

**Matt Yonkovit:**  
So you want me to add more disk IO. That is what you want me to do.

**Marcos Albe:**  
Oh, no, no, wait, wait, wait. Oh, you don't have any more control? 

**Matt Yonkovit:**  
Oh my god, it's just for you.

**Marcos Albe:**  
You have a single NUMA node so we don't have to worry about balancing NUMA. I'm just going to create a few peripheral instances. The buffer nicely faces eight matching numbers of CPUs up to I will say 30 to 64 If you have a large enough buffer pool is a good idea. I also said that the thread cache size was a bit too small and tries to

**Matt Yonkovit:**  
Mention the sort cache size 

**Marcos Albe:**  
You have a thread cache of nine that's very small. I will make it 32 which is perfectly reasonable and actually matches the number of threads running often. Sort merge passes you have perhaps one every few seconds oops so for the system I'll just make it slightly slower the light comes back. No, he has power. I'm just going to visit slightly, that's alright. So let me go back to my tuning and assert Yeah, sort of emphasis on civic life instead of All right, what else? Am I missing? No. There's more tuning we could do here. I would normally, unless we're already at huge sizes, I will normally over mentioned this. So I would say, six 768. I will do it.

**Matt Yonkovit:**  
So you mentioned a lot of app syncs.

**Marcos Albe:**  
Up sorry, say that, again,

**Matt Yonkovit:**  
You mentioned a lot of app syncs when you were looking through all.

**Marcos Albe:**  
Yeah. But then I will always try to keep their syncs if possible. Because those are providing durability guarantees. So what I think is more reasonable is to first try to tune for full durability, and see what the system can help, then I will turn and say like, we are absolutely killing the system, we are going to have to decide whether you want to relax durability, or purchase more memory or faster IO, or convince the developers to do something different. Many times there's something different could be deleting old rows, or convincing the company that retention periods should be shorter. I don't know so many things to do. But that depends on the case. But yeah, I could relax. I just don't think it's ideal. Okay. It continues. Go for it. Of course, it's something we often do. And if you do flash lager to equal two, you will only lose data if the whole system goes down, right? So like, if the Linux server goes down, if mysql-d goes down, then it's very, very, very unlikely you will lose anything. So back to this innodb. So this is 10 by default, and what it's telling you is that as soon as we have 10% of the redo log form, you should kick the adaptive question, so there are two different algorithms, background flushing, adaptive flushing, right? We prefer to click on flushing lacing, we like to be lazy. But when things start to feel a match, it's better to allow the inactive flushing to begin, which is what uses innodb IO capacity max. So once you

**Matt Yonkovit:**  
hit that level, then all of a sudden, it's like, okay, get rid of it as fast as possible to catch up.

**Marcos Albe:**  
Yeah, don't let this fill up. Because otherwise, the whole workload is going to have to stop. And if we let it fill up more and more, then when we realize it's too late, you're gonna have to, to flush very heavy batches. And that might be worse. So we want to start not immediately, but not too late. So that's why I am increasing the log file size a bit. And so what I'm gonna do is say instead of one 10% is for the admin 20%. Okay, so, what this gives is if you have recurring picks of loads that are not so huge, and those happen throughout the day, all the time, this is going to allow the background flushing to get rid of the dirtiness without ever kicking in and flushing. And if adaptive flushing can sane, it's still not going to be so gross, right? It's not gonna do crazy questions like, massive amount of pages flushed per second. Um I will put in to be a prosecutor. Because I will not say it's 200 but your capacity Max is 2000. And I know off the top of my head, that part of the algorithm is dividing IO capacity max by your capacity. So the range of DMVs is going to tell how far you're flushing. So I would say innodb_io_capacity instead of making it 2000 To start, I would make it Once again, I will later look at my stats, these can be tuned on the fly. So I start low and I tune as we go by observing the workload and making sure that the checkpoint age, which is the amount of activity, basically, and that the history list don't grow about that they're kept at a certain rate, like they're going to increase, his kisser list is gonna increase a bit if it doesn't go into the hundreds of 1000s, it's fine. And checkpoint he is going to grow up. If it doesn't, if it doesn't go into the 40% of the redo log, then we're good. So again I let things grow. And I saw that they don't grow beyond certain points. And that's the sweet spot. Okay, if I keep things continuing to grow, I will push this up. And that's it. I'm gonna start your instance, sir. I'm sure. You had some table hits? Let's see. Yeah, you had a few misses here and there. I guess as concurrency increases, we could see more of this. So I'm just gonna increase it a bit,

**Matt Yonkovit:**  
Which is the table cache?

**Marcos Albe:**  
Oh, yeah. Talk table open cache. You couldn't have 4k, which is reasonable for many workloads. But you had some misses. You obviously had some misses. Very few, I admit. But we prefer to have none as the dictionary can become pretty contentious. And this is actually forcing you to read things from this. And then I think about them again, so why not have a slightly larger cache? I don't see the consensus, let me

Okay, you already have 16 instances. So that's more than enough. And we said, slow.

**Matt Yonkovit:**  
You want to throttle the slow.

**Marcos Albe:**  
And never remember these variables.

**Matt Yonkovit:**  
So it's not just all of us who don't remember all the exact variable names?

**Marcos Albe:**  
Yeah. Or three different databases. So rate_type, and rate_type. So rate_type is session, I like it to be going. Cuz if it's, it's gonna log, it's gonna put in the log one out of x sessions, and sessions of the group of credits. Thread is sending in a connection before it connects and disconnects. So it's cool to see the whole transaction, if you're looking to understand all transactions. If you want to understand the general workload, I believe it's best to set this to a query. And I'm going to set this to 10. So I'm going to be recording one out of 10 queries, a 10% is usually a good sample. And it's going to allow you to have 30,000 - 40,000 queries per second before it ever becomes noticeable. Oh again, this is workload-dependent. Adjust for your needs, but 10 is normally okay. It's gonna reduce the amount of stuff you see on your query analytics or in your slow query log for the periods of time where the workload is slow. So just keep that in mind this is not that your server is not doing any work, it is that you rightly collect for too far.

**Matt Yonkovit:**  
All right. All right.

**Marcos Albe:**  
You got to override it

**Matt Yonkovit:**  
Yeah, you need to do too so it's interesting because some people think they have to set a ton of things but a lot of times it's just five or six very specific things that can make all the difference it doesn't have to be a ton

**Marcos Albe:**  
I'm gonna sudo.

**Matt Yonkovit:**  
That means I'll have to restart the workload in a second

**Marcos Albe:**  
Well, it's creating the redo logs and it had to do while it was stopping. It's hard to flush the pages so no, it's running. Yes, it's running right see oh, there we go. Resume Writing increasing

**Matt Yonkovit:**  
So what'd you do? What did you do and what did you break?

I kill the workload and restart it 

**Marcos Albe:**  
Oh, you just restarted the workload. 

**Matt Yonkovit:**  
I'll have to because all the connections dropped so because obviously you shut up the database and I don't have it smart enough to reconnect on restart so I just need to rerun it is not a big deal

**Marcos Albe:**  
Oh my god I love writing.

**Matt Yonkovit:**  
I'm not writing. I don't think I'm writing unless the system didn't go down Oh What are you seeing what sorry. 

**Marcos Albe:**  
Why are these? Oh okay. What's that? Where's mysql? Oh, no. 

**Matt Yonkovit:**  
There you go. I'm sorry. 

**Marcos Albe:**  
Okay, so let me see if I can do that again because it's not writing more than before, let's be more precious. What's your favorite? I rewrote this tool in C++ because it is no

**Matt Yonkovit:**  
Max you rewrote maxed. yeah! I abused Max several times

**Marcos Albe:**  
it's lovely to it is whatever alright so but sent oh just get stuck here

**Matt Yonkovit:**  
Did it restart or did the restart fail

**Marcos Albe:**  
now the restart must succeed we'll check very quickly

**Matt Yonkovit:**  
Well, I guess the workload is running now. They did kick on

**Marcos Albe:**  
No, no but I see a stall here like it's just nosedives. Everything. And it is

**Matt Yonkovit:**  
Marcos finding an issue.

**Marcos Albe:**  
Wow. Now you're building all your pages. Like everything is.

**Matt Yonkovit:**  
Well, I mean you. So is it

**Marcos Albe:**  
now? Nobody? How much is free? Okay, still warming up? Yes.

**Matt Yonkovit:**  
It'll take a while to warm up, right?

**Marcos Albe:**  
Yeah. Yeah. So these are pages read from this. And it's also creating new pages, right? Because it's not reading from these, but they are no longer free. So it's creating new pages. Those are for the inserts. And it continues to insert. And it continues to scan. But everything else drops. Well,

**Matt Yonkovit:**  
keep in mind to warm up, right. So the app needs to warm up. So it's possible that you were going through the loading process again right, because it has to warm up the app.

**Marcos Albe:**  
You're right at 60 megabytes per second but it's. So we could reduce this certainly

**Marcos Albe:**  
We'd like to sit and there was a bending of the sink here. It seems it was only ever solid here.

**Matt Yonkovit:**  
Marcos has the look of an intent and intent investigator right now. He's squinting and his, his deep diving. Marcos is in his element right now. He's looking at the data. And it's and he's dividing the secrets of the data that's coming from the global status variables.

**Marcos Albe:**  
That's a lot of rows of data. Those are big updates. Okay, then

**Matt Yonkovit:**  
Marcos loves so he's a challenge and a problem everyone.

**Marcos Albe:**  
Yeah, I love it.

**Matt Yonkovit:**  
I'm using my golf voice. So it's all quiet. Mr. Marcos.

**Marcos Albe:**  
Alright, let me produce one more of these samples where I

**Matt Yonkovit:**  
He really-really wants to know so looking enters. This is what he lives to do is solve problems.

**Marcos Albe:**  
There are more threads running.

**Matt Yonkovit:**  
Go ahead and refresh this. Look at the inner DB buffer pool size at the top. It still says one hour. Yeah, why does it say still? 128? Ups. That's weird, right? That's really strange. Does it just take what it was? It doesn't take real-time. You think? Yeah, now it was 16 I saw it. 

**Marcos Albe:**  
Yeah, I think it's whatever it was for the longest period of time. 

**Matt Yonkovit:**  
Oh, that's horrible. Yeah, PMM team. Can you fix that? Please?

**Marcos Albe:**  
Alright, this is this comparison now. That work? Oh, come on. That did it.

**Matt Yonkovit:**  
There you go. Yeah, your mouse click was faulty. I claim user

**Marcos Albe:**  
Selection let's create it. That's good. 

**Matt Yonkovit:**  
We're up to almost 1000 flow queries a second.

**Marcos Albe:**  
Yeah, even with a radius so your profit must have increased by a bit. Let's take a look at the last one hour. So started some 10 minutes ago. Yeah. Oh, your workload did increase so well, that's good. It looks like you're doing more work than you were before. 

**Matt Yonkovit:**  
so we get rid of some bottlenecks

**Marcos Albe:**  
Apparently, let's see,

**Matt Yonkovit:**  
Apparently, I mean, that's a pretty significant jump.

**Marcos Albe:**  
Yeah. I mean, we went from 15 selects for 200 selects to three points. We came here hesitant. But yeah, it does look like it had a notorious improvement. Suddenly, you are now sending more and more things and admin costs and settlements in the eye the updates are no longer there. The way my updates

**Matt Yonkovit:**  
I shouldn't have taken away your updates. Hold on a second. Your update should be still running it's the same workload

**Marcos Albe:**  
And yeah it was reading 10,000 rows per second or whatever. And now it's reading

**Matt Yonkovit:**  
hold on Darius. Maybe I started the wrong one. Hold on. Let me double-check.

**Marcos Albe:**  
It's reading a helluva of Rose, I will immediately send you to improve your query.

**Matt Yonkovit:**  
Well, so I can tell you here's an interesting thing. It's running the same workload. It's running my kitchen sink workload.

**Marcos Albe:**  
Yeah, it's the kitchen. That's what it says eating.

**Matt Yonkovit:**  
Yeah. So you can see, okay, so if you look at that, it'll show how many threads for each. So like, you'll see the different types of threads. Now, there is like, if you highlight over that CVI IU, that's inserts and updates. There's 10 threads running inserts and updates. So there should be inserts and updates running.

**Marcos Albe:**  
Inserts update 10.

**Matt Yonkovit:**  
Yeah. So that's 10 threads that are dedicated to that type of workload.

**Marcos Albe:**  
I can see the inserts. So I'm glad we did that. I'm glad we tuned it down the slow query log,

**Matt Yonkovit:**  
Because so how many queries a second, are we getting total? So if we're getting 1000, slow queries? Yeah. Well, yeah. So 8000. That's more of what I normally see is around that. 8000. Yeah.

**Marcos Albe:**  
Yeah, yeah. Okay. Okay.

**Matt Yonkovit:**  
Yeah. So you were in the 200 to 300 range. And look at how much you spiked that up by making those small changes there. Yeah, yeah. So Marcos, you mentioned the next thing up is query tuning. And maybe that's what we should do is take a snapshot of this instance. I'll save it. And we can come back on another live stream in the future, and we can then go right into the curriculum.

**Marcos Albe:**  
I love them, yeah, it's a good time to stop. We've been here for like 90 minutes. Yes. So yeah, yeah. So much for having me was super fun. Took me a while to figure out what you were writing so much. No, at this point, I just let me add one very quick thing. If we look at innodb details, we're gonna have to retune this one more time, but because now the generation rate demands those 10 gigabytes I was telling you about earlier. Ah, you, we could get more out of this one yet.

**Matt Yonkovit:**  
So you think we could even get a little bit more input?

**Marcos Albe:**  
I didn't say 1000. I said 200.

**Matt Yonkovit:**  
Did you actually think you might have put, like, go back to the config real quick? I think I know what you did. I think you just meant that you doubled up InnoDB Oh, yeah.

**Marcos Albe:**  
Oh, that's why I was writing so heavily, man.

**Matt Yonkovit:**  
Oh, yeah, you have to be careful with that syntax. Man. You have to be careful. But that's okay. Everyone, we hope that you enjoy this live stream. This is our Friday afternoon live stream. We were doing this before, last year. Marcos, if you want to oh, wait a minute here. Hold on a second. So, we hope you enjoy those. If you have some times that you're hanging out, we do have our latest blog, I wrote this blog post with some surveys. We would love your help with these, if possible. It would really help us out quite a bit. Actually. Each one of these is just a quick one or two-minute survey. And if you do fill them out and let us know how you feel about any one of these Percona products, you can potentially win a T-shirt. So hey, T-shirts, we love T-shirts, don't we? T-shirts are awesome. So I'm going to go ahead and I will put in the chat for those who are following along this link. We would love for you to swing all by and check it out. But Marcos, this has been a pleasure. Hopefully, everyone out in streaming land has enjoyed this. If you're watching live, thank you for hanging out with us. If you're going to watch the recorded version, let us know what we can do better in the comments. And if you haven't subscribed to the Percona channels, please feel free to and like this video if you'd like to see Marcos come back. Right because we are all about voting thumbs up or thumbs down on Marcos here. Let's see if he doesn't thumbs down Marcos? Yes, he doesn't want that. He wants your admiration, Marcos, we all have admiration for you. We appreciate you. Thank you for hanging out with us and we'll check you out next time. Thanks, everyone. See you next time.


![Percona MeetUp for MySQL January 2022](events/percona-meetup/2022.01.14-MySQL.jpg)