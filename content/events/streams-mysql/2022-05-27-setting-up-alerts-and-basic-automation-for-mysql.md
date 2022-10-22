---
title: "Setting Up Alerts and Basic Automation for MySQL - Percona Community MySQL Live Stream & Chat - May, 27th"
description: "Increase the performance of your database with our experts. Matt and Marcos will show how to set up alerts and basic automation for MySQL on May, 27th at 9:00 AM EDT  / 03:00 PM CEST/ 06:30 PM IST"
images:
  - events/streams-mysql/Stream-MySQL-05-27-cover.jpg
draft: false
date: "2022-05-27"
speakers:
  - marcos_albe
  - matt_yonkovit
tags: ['MySQL', 'Stream']
---
Percona Community live stream for MySQL is back. Matt Yonkovit and Marcos Albe talked about Setting Up Alerts and Basic Automation for MySQL during the session of May 27th. Check full recording and transcript! Follow us on [Twitter](https://twitter.com/PerconaBytes) and stay tuned to all upcoming Percona events.


## Video

{{% youtube youtube_id="0fhiioT0Tbg" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**
Hello, everybody. We had a little bit of a delay there. We've been fighting with some new equipment because guess what happened? Marcos went to Percona Live and I shipped a whole bunch of new equipment to particular stuff. Yes. YouTuber stuff. So Marcos has officially entered the realm of YouTube influencer. I didn't know if you knew that but he is now our official YouTube influencer. I know that sounds awesome and everything so that's just super exciting. So everyone give Marcos a you know, some YouTube blob, you know, wave to him say here, you know, he's your favorite YouTuber. And hopefully, we can make him as popular as Mr. Beast. Do you know who Mr. Beast is?

**Marcos Albe:**  
My kids will be so proud of you. They will be so grateful.

**Matt Yonkovit:**
It will it that you're super popular in the YouTube space. Yeah, I mean, like, like, you want to be Mr. Popular. I know. But my evidently my neighbor works for Mr. Beast. So you know, like he's a famous YouTuber does all kinds of stuff like bazillions of people. So evidently he does something for him. I don't know. Like once in a while, Mr. Beast thing as he gives away like Lamborghinis. He'll go pick you up in like, you know, an Uber. So you know your order Uber, and he'll show up in a Lamborghini. And then he'll drive you to your house and give you the car. Like he does stuff like that. So once in a while, my neighbor like all of a sudden Lamborghinis will show up in his yard. And I'll be like, Oh, I know what's coming up. There's gonna be somebody getting the free like, you know, something out there. So anyways, yeah, yes. Yeah. Oh, yeah. So um, so Peter, if you will give us a Lamborghini, we will be glad to give it away. Or a Tesla, or whatever else. Whatever car will go Uber and then we'll maybe we can do is we can Uber. And we can tell people like, Hey, if you answer like 10 trivia questions during your Uber, you get to keep the car, we could do that, you know, like, and it could all be MySQL related. We can see how many people can can can do that. So that would be that'd be awesome. That'd be awesome. Anyways, we are time bound today, because I do have a podcast at the top of the hour that I gotta go record. So we only half an hour. So thank you for joining us for this hour. We appreciate it. Today, we are going to talk all about alerting thresholds and setting up alerts and other things. And our esteemed expert, Mr. Marcos is going to show us what sort of things we got going on, I put together a little slide deck on some of my best practices, which if we get time, we might go over. But I will turn it over to Marcos and just make fun of him throughout the session. So Marcos over to you, what will you show us today.

**Marcos Albe:**  
So basically, today, we're going to look at the integrated alerting in PMM. I'm also going just quickly to mention the other options you have there. But integrated alerting it's right now our favorite method to do alerting with PMM. It's not too hard. It does take a few steps, which, which is what I'm going to be showing today. But it's quite flexible. It's based on prom QL and metrics QL. So you can query your Victoria metrics database and get all the information you need to build complex alerts if you would like. And that allows you to also you can set up back end channels to send the notifications with some flexibility. So it's pretty nice. And let's so let me share my screen. Let's do it. Let's get started with it right on the screen. So I'm alerting. It's here in PMM is this little bill that sounds like an alert. But before we do any anything here, we need to go to configuration. Let's go to settings. And then within Settings, we're going to look at advanced settings here, the second option on the left. And here you will see the option to enable integrated alerting. I already have it enabled so I don't have to save anything but by default this is going to be off and then You're going to have to do apply changes over here. Once you do that, this little tab will show up, like the first time you load this without integrated alerting, you're not going to have the communication tab. After you integrated after you enable, they do apply changes, you might need to come here again to settings and go to communication tab. This is where you will set up the backend communications. So this is gonna allow us to push out alerts. So for email, very simple, we set up an SMTP server. We said who is pushing the alert, like, what is going to be the sender? What authentication type in my case and using login, my username, password, it requires encryption, and then it will allow me to do ups. And do a quick test. Oops, okay, I need to enable the email. I already have it elsewhere. I know it's working at this before. Okay, just in case, I might come back here to fix it in the worst case. But this is the simplest mechanism. And of course, it's look, if you look closely, it's not asking me for recipients at this time. This was just for testing. So this is just like our SMTP server, but it's our mail office. So this is not like a fixed set recipient thing. So that's the one of the nice part. And then you can set up a Slack, I was trying to set up a communication channel with Slack, but didn't go to get the approval from ideal time. But basically, you go through a very simple process where in your workspace, you can create so-called App. And the app can have a web hook. And the webhook is gonna give you a URL. And that URL is what you actually use here.

**Matt Yonkovit:**
And you can do other webhook things as well. So if there's other monitoring systems that allow webhooks or you want to integrate, you can do that as well. 

**Marcos Albe:**  
I think anything that supports webhook, which is a simple post, nothing with a fix of structure. Yeah, you could do that as well. Exactly. So I have my email set up. The next thing is going to integrate. And here comes no alerts, my system is working flawlessly luckily. So it's a bit weird, but I will tell you start from the right, you know start right to left here. The first thing you want to do is actually set up notification channels. We first set up the communication channel, which is how we are going to send notifications now we're gonna set up notification channels which is to whom we are going to push those so if I would like to add one I will be able to choose you know could be pager duty, other workweek or slack like we configured before. Again, I'm just gonna use email. The one alerts email you want alerts all support no I'm not gonna do it but you know you could add the support I'm just gonna add Matt

**Matt Yonkovit:**
You're going to add me Oh, he's gonna He's gonna spam me everyone. I'm gonna get spammed. I'll take one for the stream.

**Marcos Albe:**  
Yeah, please. You're going to join support this will Yes. So now that I have a channel I will be able to use that channel to deliver alerts I could also you know create another one that is email to alerts on duty ups and that will be only worthless because

**Matt Yonkovit:**
Thank you for sparing me those.

**Marcos Albe:**  
So, you're not on duty, you know I'm sparing you from the duties. So now I have multiple alert channels, I could go ahead and say let's create template rules are based on so-called templates that allow us to not have to redefine the whole room again. So it's an abstraction that will allow us to create many routes later. That is the guest. Many are already building for proxy, SQL Postgres, for the node itself. For MySQL, MongoDB. And in usually, you can just go ahead and come here to alert rules, and you can start adding an alert with one of those, let's be clear those up. So I'm going to use MySQL. MySQL connections to use MySQL. So I'm going to warn when there are more than 30. And if it has to be this is so this is the threshold for the alert. And so I'm going to say when there are more than 30 connections in use? 

**Matt Yonkovit:**
If you look at it, it says it's a percentage, is it a percentage?

**Marcos Albe:**  
Oh, I will show you that in a minute. That's a beautiful mistake. Let's see. I think we should report some documentation back. Because when I create the alert, you'll see where these are coming from. And you will be able actually to understand what it says percent, it's Percona limitation. And I will explain where it comes from. Okay, so

**Matt Yonkovit:**
I'll hold on, I'm holding on everyone, I'm holding on to myself, while I wait for Marcos.

**Marcos Albe:**  
So here it says, duration in seconds. So what I'm asking is that this check, this threshold must be exceeded for 300 consecutive seconds, let's just make it 10 For demonstrations. And I'm gonna say it's a warning. And here, I could create filters for my notes. So basically, in my notes, I could add, for example, services, I'm just gonna do go with an easy one. But you could make it by cluster, you could make it by node, you could make it by service type. By environment. So they are,

**Matt Yonkovit:**
But so for the filters, the filters are not SQL filters, just so people who are used to SQL, these are not SQL filters. This is what this is

**Marcos Albe:**  
This is matrix QL. Yes, basically, matrix, which is victory matrix. For any language, very similar to property, hell, if you're familiar with rocaille, you're not gonna have any issues getting there. And there is one other thing I'm going to show you. And you know, that is, I think one of the main things that people get wrong, and it's so easy to get wrong. That, you know, I even I got it wrong the first time, so I got it. So yeah, fitters are just allowing us to say this alert is good only for these nodes, or this environment, or this type of dynamics. Super useful, right? Because I don't want to check if I have mix at MongoDB. And MySQL, I don't want to check Max connections the same way it I don't want no I'm not able to check Max collections in MongoDB. The same way I checked Max connections in MySQL. So I will say service type MySQL. So in this case, I just I'm just gonna say I want it for my macros to be my SQL database instance. And here we can see the formula. Again, this is prom QL, or metric scale. And you can see it's comparing with something called threshold. And this is basically what is going to be emailed to us when, what the alert goes off.

**Matt Yonkovit:**
So that's interesting. So looking at the expression, it's taking the last five minutes. So the maximum over the last five minutes. And then it's dividing by ignoring job.

**Marcos Albe:**  
So this is a single expression. Oh, okay. Yeah. Okay. So ignoring job, give me the max. So

**Matt Yonkovit:**
so it is looking for Max connections divide, or is looking for the total or the maximum number of connections that were active divided by default? Yeah. So it's making the percentage. Which you set it not you set it to 30 connections, not 30%. Did you say it?

**Marcos Albe:**  
Yeah, yeah. So yeah, I got that wrong, because I was thinking in my alert, I'm bad, my bad. So this actually took a look at the template expression, because yeah,

**Matt Yonkovit:**
So those who are listening, I want to point out something there's an interesting debate here on percentage versus hard-coded numbers.

Unknown Speaker  
Can I give you my opinion? Can they give you anything? Yeah, of course, use absolute numbers.

**Marcos Albe:**  
Because if someone decided that Max connections will be 50,000, you know, 30% of 50,000, it's a lot of connections. It's 15,000 connections, that's gonna be a lot. So and it's still 30%. So ratios and percents are usually alive. They usually lead to bad things. less than ideal stuff, in my opinion,

**Matt Yonkovit:**
But away my finger at you. Because I think there's, there's a use for both. And let's debate this for a second, because this isn't that sort of thing. So let me give you a couple of scenarios where I see this. So there's pros and cons to either way. And when you look at a percentage threshold, let's use the user connections here, you're making an assumption here that you will know, or be able to set a threshold that is universal across your nodes. What if you've got 100 machines, and all of them have Max connections that vary, because some are busier than others, some are analytics, they have different workloads, a percentage in that case, could be something beneficial, especially if you're really focused not on getting alerted that your systems busy. Still, you're going to hit a critical threshold that's going to, you know, kill you, right. So, you know, once you hit max threshold, or max connections, things break. So you want to avoid that. So there is some benefit to saying like, Oh, I hit 90%, whether that 90% is nine out of 10, or, you know, 900 out of 100. You know, like there is a benefit, but there's almost like you need a secondary, because, you know, yeah, when you're you've hit nine out of 10, one more connection kills you, when you hit 900, out of 100, you get 100 more. So really, you probably wanted to set the threshold, the 95 for that. But I would rather get alerted than not in cases where I've got a lot of massive systems and then adjust each one individually. So I see that there is a benefit for percentages, but there they are when you're handling lots of nodes, and you can't get control of all of them, and you are looking to you know, that Max that's gonna kill you and push you over, I think that that can be something useful, that kind of gives you my opinion, of course, you could give me your opinion,

**Marcos Albe:**  
How I will try to structure my learning performance problems are related to hardware resources. And well, sure, hardware resources, now they could change. You could have hot black memory and hot black CPUs or whatever like that. Normally, normally you will have a fixing machine for especially for a database right I'm talking about. So what I will do is I will level my notes with the disk capacity with the memory capacity, the number of CPUs and then I will create alerts that are based on the hardware because what you're going to saturate this hardware and then I will create filters to apply those alerts with the proper dimensioning to the proper heart. Might think so might not work at too big of scales. But I believe that for vast majority of the people, I'm talking about people, 500 nodes, 1000 nodes, you can perfectly do this, you're not going to have 1000 different nodes Come on. So I think it's better because it's easy for some thresholds to be changed by humans. So if I told you, Max connections 30%, and then, you know, I go sneak back in your back and said, Set global Max collections equal 90,000. I just blew out your server. So that is the thing is hardware resources are fixing, and can be easily labeled. When you are installing could even be automated, so much. So that could be automated that when you're deploying your PMM agents, you can add those levels to qualify, what piece of hardware do you have there? Automatically, you don't need to have a human do it. So you will get those levels for free, basically. And then you can use it in the future. So I could say, Okay, I want 30 connections for the eight CPU cores, machines. And I want 1000 connections for the 144 cores machines. Does that make sense? To like, or what do you think about it?

**Matt Yonkovit:**  
You Yeah, you could do that? I mean, I guess you could if you tag them. So what you're saying is tag the different size instances and then set the alert threshold for those different size instances. Because as the environments do grow, we're losing control over individual nodes, right. So if you've got an environment where developers are, let's say, you're an RDS, right? So you're an Amazon, and you're looking to monitor, and you want to set up alerting thresholds, you might have 10 different development groups, and they might have 50, different instance types. You know, it's entirely possible. So, you know, yeah, you can put, you know, filters in there then that say, like, you know, hey, you know, we this, this sort of tag or this sort of, you know, system, but I think you could also potentially do that in the template, like, so if you go down and look at the Victoria, you know, metrics there. 

**Marcos Albe:**  
You can make this expression, for instance, like, say, a piece of the CPU or a piece of the memory.

**Matt Yonkovit:**  
Yeah, what were even, like, even hard code the value in here, like, like, like so. So if you're gonna use a percentage, like, like, in this case, right, so a percentage, let's say you wanted 90%, you could say 90%, it's over 90%, and has less than 100. Connections left, or has less than, or has, you know, more than a certain number of things. Right? So you could say, like, in here, put an ad statement, and then say, take the max minus the max variable, so that the maximum number of active connections minus the configuration variable, and say if that's over 100, and over 100, or under 100, and over 80%, then alert. So you can make it a little more intelligent by mixing things in here as well.

**Marcos Albe:**  
Because if I Ristic built into the plate, I mean, never looked into it, to be honest, never looked into it. Yeah. Yeah. Because again, it sounds interesting. What is wrong? Is that right? Like, it's like the rule of thumb of 75% memory for the buffer pool. And then I see people with 784 megabytes of RAM using 75%. And they have like, 180 gigabytes free, right? There's like, Sir, do you have a lot of memory free? You don't want to have all that memory wasted? It's a lot of money. And it was oh, I was following that percent.

**Matt Yonkovit:**  
Yeah, yeah. And I mean, like a net, like, if you're going to do a memory, you would, you'd be saying, like, what's the maximum that I want to allocate for the OS, and you'd say, maybe it's like 32 gigs, once you hit 32 gigs, everything above 32 gigs could be to the database, you could put that directly in your template expression as well, that says that you know, if you know, the memory is above a certain threshold, then just, you know, send this alert that you know, you've got this free memory that's not being allocated, regardless if it's at the percentage or not.

**Marcos Albe:**  
But again, personal touches are dangerous in that applying them blindly will lead to bad situations, either because you're wasting resources or you're getting too tight on resources. So, my preference and because we follow a methodology to do diagnostics, which is based on resource utilization saturation errors is to do the alerting based on the resource utilization rather than on an arbitrary okay. So, yeah, I was wrong about this percentage I was thinking about my role in my role I did fix it. So, the expression we will apply to is this one here. And this is what we are going to get emailed. And we will see where to change this in a moment, you cannot change this here. So, I will simply add this. And there it is, we have a warning. You're gonna get spammed very soon.

**Matt Yonkovit:**
I don't know there's no workload running right now. Right? 

Unknown Speaker  
I'll get some workload. Oh,

**Matt Yonkovit:**
Marcos is getting us some workload There you go.

**Marcos Albe:**  
And look at floods connected 14 That is more than 10%. So we should all be getting alerts Any moment now in 10 seconds from now. Hope

**Matt Yonkovit:**
And you should be able to just look at the Yeah. So yeah, that should be in the Alerts tab. Or in your email eventually.

**Marcos Albe:**  
Here, you can do this actually quickly to check what is a rule? Because this name might be shenanigans that knows who put the name of getting alerts, like this. Status threads connected, right? Oh, over five minutes. Oh, my God, that's going to take some time. Okay, let's leave it there while we go elsewhere. So we have an alert that should trigger. And I'm gonna delete this one. I'm going to add an alert rule. Alert rules. As we said before, they're based on prom QL and metric school. Here I have one I wrote last night. I hope you can see it there.

**Matt Yonkovit:**  
Yep, yep, we can see it. 

**Marcos Albe:**  
It's a simple YAML format, you can give it an arbitrary, no space names. So I'm just gonna say alert of hype threads running, which is a critical concurrency metric. It's telling us how busy the database got this diversion of my plate. Here is a human readable summary. And then an expression. This is how you go to the next line. I want the max by service name for this variable. And the thing is largos. How do you know that's the right part of

**Matt Yonkovit:**  
Marcos? How do you know that's the right variable name?

**Marcos Albe:**  
Oh my god, I will show you right now. The way you find out what are the right variable things is to come to this little compass here and go to Explorer. And here you can browse all the metrics that are available in total metrics. So what I do is I type the name of the variable I know if it's running and there you go, it brings up the whole thing so that

**Matt Yonkovit:**
You know, okay, and look, you can see the spike from when you started that.

**Marcos Albe:**  
So this is a metric I want. But it's showing me here that is, you know, I only have one note. But you can see all the criteria by which you can filter things. So if I actually want the max

**Matt Yonkovit:**
by,

**Marcos Albe:**  
Let's say serve. Right? I think that's it. And so, okay, that looks good, right? It's still showing me the same value in this case, because I only have one node. But if you have multiple nodes, then you might be filtering out the ones you want. So that's how I came up with this. And then I say, these should be greater than this. And these square brackets, square bracket dot notation. It's actually the placeholder for our parameter params. And you define params, like this. You said name threshold. And you can say it's max Fred's running, or, you know, just a simple prompt, like this is basically your prompt for the input of the threshold. So because it's a parameter, you're expecting a human to fill in this parameter. This is the prompt for the human. The type, you want. The range which, within which you expect this value to be, and a default value. You could have unit it will be the percent. In this case, I'm not doing a percent, I'm gonna just do fix it numbers. That's fine. It goes how, of what you will do threads running like thread cache size. Perhaps do it like that, like said, all threads running is bigger than thread cache size. But it's not necessarily true that that is a problem. People have to do to have CPU cores. I guess I can do that as well. We can take a look at building one of those. And then I said, by default, I want this threshold to be exceeded by one minute to trigger the alarm by default disabilities and warning levels. I don't remember what levels are for to be honest. But I am assuming I can later obtain more my alerts by level. I never saw decent use of the materials. That's the thing.

**Matt Yonkovit:**
So I want to point out something for everybody who you know, like, like for the timing here, the one minute, this is an important metric, because if you don't get the timing right, you are going to over or under alert. Think of it like this. Okay. It is entirely possible and we'll use CPB CP is very easy for you to have a second or two where you are 100% utilized on the box. And then it drops down to nothing. Do you want to get alerted? If you're if you know, I don't think you can go down to one second here. But if let's say you could, would you want to get alerted every time it hit? 100%? Or would you want to get every time it hit a sustained, you know, 100% over a minute. And that's a critical thing when you're setting up alerts to avoid too much noise.

**Marcos Albe:**  
This is like to avoid so-called false positives, right? Or to avoid skipping entire alerts because you thought okay, 30 seconds is fine. And actually, by second 15 your database was going down because of the excessive load. So yeah. Balance here. It's that is adequate for each metric. It's important. Yes.

**Matt Yonkovit:**
Yeah. Yeah. And it could even be workload specific. And so for those PMM engineers who are out there, a feature request for you is potentially to allow for some templates around some of these right so maybe some default values were like you know, you can say certain size boxes or certain you know, environments you could tag them. Or maybe you could use labels that way where you say like, Hey, if this is a, you know, a high memory box, maybe I only care about looking at, you know, 32nd thresholds. Whereas if this is an analytics box, I care about, you know, 10-minute thresholds. Yeah, or whatever any, you know, an easy way to kind of like, deploy this template, but then have like, some of those metrics change without having to rewrite the whole template, because at this point, you'd have to redo the whole template to change that number. Right.

**Marcos Albe:**  
Am I right, though? No, no, you get that.

**Matt Yonkovit:**
We can change it in individual as we set it up. Yeah.

**Marcos Albe:**  
When you do the alert, you said the duration?

**Matt Yonkovit:**
Well, the duration, okay. Yeah. Okay. It's there are two separate things. There's also when you were looking at that other one, it's looking at the data over a certain period for that metric. So if you go, just look at the Victoria metric definition says it's gonna be an average of five. Yeah, so in that, you can't change unless you change the definition.

**Marcos Albe:**  
Yeah, here is the change. Yes. Okay, then fair enough for how long this is true for how long the moving average window will have to hold for the alerts to trigger 10 seconds.

**Matt Yonkovit:**
So Marcos, we have about 20 minutes left. And, you know, so we want to go ahead and, you know, build this template. But I think the other thing we people, really, really want to know, is what are the key things they should be monitoring and what you know, like, if we were to give them a checklist of things, what would they for Golden matrix? Yeah, so go ahead and build this and then we'll, we'll get to the metrics. Okay.

**Marcos Albe:**  
So again, and the final bit is just an annotation that says summary. What is going on and description this will go to so let's try it. I will create an alert template we will add it and if it has any syntax error or anything it's going to complain here for example, that say the two little parts rule template I broke it. Oh my god.

**Matt Yonkovit:**
Did you do that? No. This bad I don't know.

**Marcos Albe:**  
I give you my word. This was working. Couple of hours ago let's see. Oh, perhaps they will have supinator. Again

**Matt Yonkovit:**
You must have a special character and then you didn't have

**Marcos Albe:**  
I must have a seal a special character because I don't see anything. I'm solid. This is good. Like yesterday, I have a single dot here. And that was ruining me. But I don't see

**Matt Yonkovit:**
you can go look at the other one that you created yesterday. That's that's already there. And that should be the same one. Right.

Unknown Speaker  
Now these

**Matt Yonkovit:**
I mean, so yeah, so there must have just been there has to be some special character. Maybe at the beginning. Yeah,

**Marcos Albe:**  
There has to be some top or some weird displays. You can see it's the same.

**Matt Yonkovit:**
I'll take your word for it. All right, thank you. Don't blame Marcos, everyone. He's a YouTube star.

**Marcos Albe:**  
Yeah, just a YouTube guy. So there is a difference. You can see I actually added some more here. So here I only have service name. And here have no name service and service type of service. And then name threshold. So everything is exactly identical. Okay, I'm not going to change anything. So I'm going to use this template basically will have resulted in saying you're going to have an entry in the Milton plates and your the name you gave it blah, blah. So other rules now I can actually create an alert rule that is based on thread concurrency MySQL I'm just gonna say MySQL. It's running or is six because you can see that the percent is gone. Suddenly, the coma is not the percent is gone. This is prompt, I said in that, that template, this is how long I want it to be, it's going to be instant, right? Because I'm not average. So this should be instant in this case. So I'm gonna say, I just want to use for 15 seconds, and severity warning, and I'm going to do service. Service. Workers. And I'm going to choose a channel to all do the engineers. Because it's just a warning, if it was a critical alert, I will be mailing to everyone. And, again, this is the template we have. And let's add it. And we already have an alert here that it's firing. So this activity firing started, like 1028 is now 1041. And still getting given us alerts, we can go ahead and silence it. So that will stop sending us emails, because at this moment, Matt and myself, not only myself should be getting emails. And if we wait a few more seconds, we're gonna see these other triggering.

**Matt Yonkovit:**
Yep. While we're doing that, Marcos, you said the four golden metrics.

**Marcos Albe:**  
My experience is that, sure, those are good to have. But I never solve issues with those, I just realized there's an issue, which is I guess what you want to do with alerting. So my EC, you see, one is concurrency. Right? Like how much concurrency Do you have? That is one very important. throughput, right, like sustained throughput. Don't go under these don't go over these. And latency at I need to set up that here. You had that? Very well done. I remember, I suggested you could build a graph based on performance schema, latency metrics, I will ask you for that panel to integrate into these payment because that is one lovely panel. So, you know, if your query latency is changing, that is likely a bad thing. Yeah, yeah.

**Matt Yonkovit:**
Well, I mean, I mean, while changing is not necessarily if it's getting better. It's not a bad thing, right. 

**Marcos Albe:**  
Well, if it's getting better because the slower credits are not running. A good database is a boring database must be always boring, right? And to be boring, you have to be stable, have a constant throughput and constant response times. So usually, if I will see that response times are suddenly all the better without me doing nothing. I will freak out. Yeah, something happened.

**Matt Yonkovit:**
Oh, yeah, totally.

**Marcos Albe:**  
Perhaps the queries are very fast because they're failing, or because someone deleted the data. And then the last alert, that's the hard one, like, Well, I would say uptime, or being actually up, right, like those would be availability, concurrency, throughput and latency. Perhaps those are like, my favorite for matrix that I will keep an eye on. Things should not change in that reality. Oh,

**Matt Yonkovit:**
Let's look at my list. Real quick. I'm gonna go ahead. I'm gonna overrule to No, I got it. I got it. Look at that. Look at that. I've already kind of like popped up over your screen. Oh, whoa. Even though you're sharing screen I'm sharing. Yeah. So we talked a little bit about percentages in the fallacies, you know, In why looking at a percentage isn't necessarily a good thing. But it can be a good thing in some scenarios, so you're gonna need to be mindful of that. But growth rates, for me matter quite a bit. And so let me give you an example of this. Let's say that you have a threshold will use your concurrent connections. And you have it set to, you know, I don't know, let's say you have it set to 9000, or 90%. And you've got 1000 connections, right, you know, or 10,000 connections. So you would, you know, obviously, hey, I want to be, I want to be warned when I hit that magic threshold. But what happens if you go from 10 connections to 1000 connections in one day? Something pretty drastic changed in one day, and I want to be made aware of it. So for me, I mean, I don't even I want to look at the things that are going to cause a break, which is going to be things like, we're going to exceed the max threshold. But I also want to understand, massive or unpredicted growth, you know, the mantra of any SRE that's out there right now should be predictability, predictability, predictability, you mentioned boring databases, a good database, you know, what if you can't predict the growth rate. You're seeing excessive growth, even if it means, you know, the system isn't bogged down? It is a massive red flag for me.

**Marcos Albe:**  
Oh, yeah. Something bad is about to happen. I've seen it with backups. Like, you know, someone had like 400 gigabytes backup, and the next day, they have like, 700 gigabytes back. Yeah. It's crazy. You don't realize that four weeks?

**Matt Yonkovit:**
Yeah. I mean, this goes to everything. So so so for me, there's almost there are two sets of alerts, right there is it's going to break or it's broken, fix it. And there is the predictive measure of somebody needs to take some action, because this looks really abnormal. And that's where the growth rates come in, for me is the abnormal side. But it's also with those growth rates, it's also about understanding the baselines and what your expectation is. So you mentioned latency or throughput. And here's the thing, if you know that, overall, your system generally has 10,000 queries a second, and it is generally running an average latency or p 99. latency of, let's say, 100 milliseconds, just throwing a number out there. If all of a sudden, like you're at, you know, something different than that, up or down, even, let's say, let's say you're 20%, higher or lower than that, that's something to me that triggers there has been a significant change in workload, especially if you've been running that way for months or potentially even years. Right. So if all of a sudden you go from 100 milliseconds to 200 milliseconds, obviously, 200 milliseconds is still probably acceptable for a lot of workloads, and you know, a lot of queries and you might not even see a bump in CPU. But that to me is like, oh, I need to look, you know. So that's, that's important.

**Marcos Albe:**  
Can help you establish those baselines, it's one of the things that you have to do first, when you set up monitoring, right, just like, learn about your baseline, learn about the patterns of your workload. I remember Barack saying that, when they first started setting up, what was the original name for barons pivot cortex, like they started doing pivot cortex and a lot of situps. And they they started seeing how spiky all the workloads were. And that's how people was not aware of all the spikes. So it's not a bad idea to invest some time in establishing the patterns of your workload, the spikes that are actually already there, that you don't know about, and some good baselines to then set up alerting. Establish a growth base. Yep.

**Matt Yonkovit:**
Yep. So I'm gonna look so so for me, I break these down and take these with a grain of salt. But the normal metrics that, you know, we're setting thresholds for our CPU, disk space swap, network throughput, IO latency on the OS, right? So these are things that again, if I've got a baseline, I understand I'm going to be looking at what the deviation is the growth rate is, I'm going to also have some, for lack of a better word, oh, shit metrics, right? So if I'm hitting a consistent 90% CPU, that's an O ship metric for me. Whereas I'm also looking at when I go from 50% CPU to 60% overnight, and that is sustained that I'm like, oh, that's that's like Curiosity metric for me that I need to get. But you know, these are standard ones that you'll see measured quite a bit. But again, you know, when you get to stuff like disk space, this is where that percentage can really hit you, in the side of the head, right? You know, 10% of 10 gigs is a lot different than 10% of a petabyte of data. So again, you've got to have those, those growth rates, that consistency there. From a query perspective, and this is where, you know, Marcus, we talked about getting that dashboard. Deviations from the normal are the important ones, but also net new things. So you know,

**Marcos Albe:**  
When new things arrive, you will have an explanation for those right, like, you will know, okay, we release a new version. We got, I don't know, this feature that was not enabled until last week. Now it's enabled. So you like, you know, I remember, I think it was Dijkstra, who wrote like a some security book, where it says that the team's in an IT company, they should not be so decoupled, like, the operations team should know about what the development team is doing. So they can understand what the workload should look.

**Matt Yonkovit:**
Yeah, no, no. And I mean, I agree with that. The problem is, it doesn't happen. I

Unknown Speaker  
know, I know. I mean, I think we're advising people here in general. So I'm just giving one more piece of advice.

**Matt Yonkovit:**
So this is where it gets interesting, because I think with smaller teams, you have that the larger the teams, the more in, the more kind of isolated they are, the more difficult it is. But also, the larger the environment, the more difficult it is. So think about like, you know, again, go back to that kind of you are an SRE, you have 1000 different development teams that are working on their individual things. And your job is to just troubleshoot, you might not necessarily be totally in tune with what releases are happening and what's in each one. Especially if there is a continuous deployment type of model where code is constantly being updated. So it can get kind of weird, but looking for those unseen queries and looking for new things. So PMM does have the capability to track new queries and things. So that's something that is useful.

**Marcos Albe:**  
I remember doing that with PT query digest. And it was quite nice for DBAs that, precisely, they didn't have any insight into the release processes. And they were not looking at the release notes of their software. So the applications hit them with new queries. And they were they didn't have a clue. Yeah, we did that with critical digest. You can do the same here. Yeah, it's a must.

**Matt Yonkovit:**
Yeah. And so you could like I put a question mark here. I've seen this a couple of times, when there is a couple of queries that are supercritical. You can look specifically for that particular query and look at the latency and target just the one or two that are really critical.

**Marcos Albe:**  
I will alert all critical queries, or Canary queries, right? Like, I always give the example like, if I have a float of banks, right? And I have a report that will allow me to dispatch the bank, you know, and that report is slow. That is really holding my business back. So one credit must always be No, under five milliseconds. Yeah, I will totally alert on that.

**Matt Yonkovit:**
Yeah. But yeah, so I mean, query side, you know, we definitely want to look at that, obviously, we talked a little bit about configuration metrics, and these you could probably put more on, but I was lazy, ran out of time. So you can blame me on that. But, you know, things like, you know, hey, you know that the max connections are set wonky, or your buffer pool set wonky, or your log file size is not correct.

**Marcos Albe:**  
These, it's already there. I will show you in our next episode.

**Matt Yonkovit:**
Are we talking about advisors? Yeah. So

**Marcos Albe:**  
We already have advisors for these kinds of things, integrate. But these are gonna enjoy those without any additional uninformed.

**Matt Yonkovit:**
Yeah. So think of these though, is as any metric that if you've got a gold standard for what configuration variables are, things should be or an idea. If there's deviation, you want to know, these are not necessarily going to be critical drop everything, but they're probably things that you would set up to look at. So it's a checklist, it's a checklist. Things are so a few other common ones, deadlocks, so you know, a deadlock in and of itself isn't necessarily bad, excessive ones can be potentially bad. So something to keep in mind long. Running are stuck queries. This is another one that I see quite often. So we're talking about, you know, on some of the other query metrics, not necessarily what's running now, but in aggregate, right? So we're talking about, you know, you mentioned like the dispatch query, if that gets, you know, oh, it's doubling in time, you know, that could be executed a million times, what we're talking about here is, is there one query that's been running for over, let's say, five minutes, or something like that, and a lot of people will put this sort of metrics in there, and we'll sort definitely alert. And that's more of an emergency hair's on fire, you need to go take a look at this, especially in conjunction with other metrics. So if you're seeing a lot of deadlocks during that time, because it's stuck on this long query, if you're seeing high CPU, high IO, that's a trigger as well. Table database growth rates, obviously, Marcos, you mentioned backup growth, you know, like, you know, the backup size group, you know, there's all kinds of implications for larger databases and that growth rate. So something to keep in mind. And of course, replication is critical. Yeah, yeah. I

**Marcos Albe:**  
Think we haven't yet even set up a replica here. So I avoided talking about that. But yeah, of course, if you have a replica set up, the metrics for the replication stuff will be another right, like,

**Matt Yonkovit:**
Yeah, typically, it's about and lag. Those are the two big ones generally. But I mean, there are others. And then, you know, other things that as a DBA, or an SRE that I would be paying attention to, from the database perspective, or any sort of like auditing alerts, which could be triggered on things that are more security related, right? So somebody dropped a table, somebody did you know, something else? Maybe somebody ran a MySQL dump that shouldn't have new users created? Those are often things. Yeah. Those things are things you want to look out for in application response time. Let's be honest, the queries matter. But it is a component of the overall application response time, right? And so I have run into situations where all the queries are fine, but one particular page or function has 14 million of them. And so then all of a sudden, that page is awful. So you're going to impact that pain still? And how do you find that out, and then obviously, backup restore and failure, those are also issues and things we need to look at. But, but that is all that I've got for that. So you know, I think Marcos, we are good for today. If you want to stop sharing your screen, we can jump to our main thing I'm just going to make, I'm going to make Marcos jump a little bit but No, everyone, thank you for hanging out today. You know, do appreciate you swinging by and chatting with us. You know, we're doing this every other week, we're hitting another topic. And next week, we're going to do Postgres with Charlie. So Mr. Chino, but we are out there, go back look at previous live streams, check out some of the other activities we're doing. We hope that you'll join in if you do like the content here. And go ahead, like, subscribe, follow us and put in comments on what you'd like to see what topics you'd like us to cover. We would love to hear from you.

**Marcos Albe:**  
By the forums, if you have questions, actively answer the community, and get community feedback.

**Matt Yonkovit:**
And yep, and so for the hos and for our YouTube star Marcos, thank you for hanging out with us this morning. We appreciate it. We'll see you next time. 


