---
title: "Setting Up Alerts and Basic Automation for PostgreSQL - Percona Community PostgreSQL Live Stream & Chat - March 25th"
description: "Our experts Matt, Agustin and Charlie were live to show real use cases and answer all questions about setting Up Alerts and Basic Automation for PostgreSQL."
images:
  - events/streams-pg/pg-stream-week-3-march25.jpg
date: "2022-03-25"
draft: false
speakers:
  - charly_batista
  - matt_yonkovit
  - agustin_gallego
tags: ['Postgres', 'Stream']
---

Percona Community organized live stream to talk more about Setting Up Alerts and Basic Automation for PostgreSQL. This recording is from the live event of March 25th with Matt Yonkovit, Charly Batista and Agustin Gallego. This is a part of the Percona Community bi-weekly Live Stream series to discuss Postgres-related topics and deep talks with technology secrets.

## Video

{{% youtube youtube_id="f1NklbrVvYY" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Hello, hello, everyone, Welcome to another Friday edition of the Postgres Percona database meetup. I am here with my regular guest - Charly. Charly, how are you doing?

**Charly Batista:**  
Hey, man, I'm doing great. Thanks. How about you, man?

**Matt Yonkovit:**  
I'm doing well. So Charly actually has a special guest for everyone who's on. So anybody who's out there, give us a wave on chat. And welcome the special guest of the hour - Agustine. God, we've got to Percona Ian's Why do we have 2 Perconians in one room?

**Charly Batista:**  
Well, that's a good question. And I think we're asking me, right.

**Matt Yonkovit:**  
So let's do either like Agustine can answer. I know like you're on every other week. So, Agustine's like the special guest, I should just change the name. That should be the August, Matt show or something.

**Charly Batista:**  
Thanks. Thanks for that. It's okay. We're talking about alerting today, right. So I thought of inviting an expert and someone that really knows how to do those things, not like me that tried things. And Agustine is the guy.

**Matt Yonkovit:**  
Ah, that's what it was. Well, why are you together? Like you don't live in the same house or in the same town?

**Charly Batista:**  
We don't live in the same country, actually.

**Matt Yonkovit:**  
See, you don't even live in the same country.

**Charly Batista:**  
Agustine lives in Uruguay. And I live in Brazil. This is what we do when we need an expert. We go and find one, and it doesn't matter how far it takes for us to find an expert.

**Matt Yonkovit:**  
Is that what it was? Oh, okay. So your expertise?  Agustine, did you swim and run through like the country to get there? Or did you take a plane?

**Agustin Gallego:**  
Yeah, Charly came,

**Charly Batista:**  
I came to Uruguay. Oh, that's another thing. When you need an expert, you go and find one.

**Matt Yonkovit:**  
Oh, you go, you go. So okay. So Charly, you went to Uruguay! So you're really there for a team meeting? Right. 

**Agustin Gallego:**  
Exactly. 

**Matt Yonkovit:**  
So, how much of Marcos's barbecue. Have you eaten yet?

**Agustin Gallego:**  
Every day, every day,

**Matt Yonkovit:**  
Every day afterward? You just get together? 

**Charly Batista:**  
Yeah, it's been. It's been a week. Yeah, to give some context. Yeah, it's been a week.

**Matt Yonkovit:**  
Well, we're glad to have both Percona X Percona experts on. Today, we're going to continue our live stream schedule. We're going to be talking about alerting. We're going to be talking about setting up monitoring, some sane defaults things you should be looking at. We're glad that Charly brought along the expert, or the expert brought along Charly in this case.

**Charly Batista:**  
God knows what he's doing. Right? Yeah, yeah, have somebody

**Matt Yonkovit:**  
So, are you all doing something over the weekend? 

**Charly Batista:**  
Sorry, I'm gonna say that again. 

**Matt Yonkovit:**  
Are you doing something over the weekend?

**Charly Batista:**  
Yeah, we've been. As said, we are here for a team meeting. So we're probably gonna go out for some more barbecue, right? 

**Matt Yonkovit:**  
When do you go home? 

**Charly Batista:**  
You're like, it's an amazing place right in front of the beach. But it's raining here. So not beach for this weekend. But yeah, we are gonna hang out and do some stuff.

**Matt Yonkovit:**  
Yeah, so I don't I don't have anything going on this weekend. And I'm a sad, lonely person who just sits in his house all day. Although, the weirdest thing happened. My daughter is 20 now, and she hates all things sports or activity-related. She just sits in her room, watches TikTok all day. She marches around the house with their headphones on. I never hear anything from her. We went to a hockey game last night. And she loved it. Like she was like, she's like, Oh my god, this is so awesome. This is great. I don't want to leave. Like, generally when we go to a sporting event. She doesn't want anything to do with it. She sits on her phone the whole time. Right. She's like this. And yesterday, she was like, go! go!  She's so excited. So thrilled to be there. It was weird. So I don't know. Maybe she's like had a mental break or something. And now who knows?

**Charly Batista:**  
But that's a nice thing. That's a nice thing. Sports nice, though. Yes. So anyway. Well, let me see people like they stopped biking. I love it.

**Matt Yonkovit:**  
Oh, you love it. Okay, okay. Well, we can see we can find a hockey game. Charly and I are going to be at the Postgres Silicon Valley Conference in another week and a half or so. Exactly. Yeah, so that should be exciting, right?

**Charly Batista:**  
Definitely. I'm waiting for it. Yeah, looking forward to meeting you. And I know you're gonna buy me a coffee though, right? That's what he said. Like,

**Matt Yonkovit:**  
You were gonna buy me a coffee. I thought. Oh, me. Okay, I thought you were gonna make me pay for all the coffees or all the people you wanted to have coffee with.

**Charly Batista:**  
Well, that was kind of the plan, but like, now you're saying that I'm gonna buy your coffee. 

**Matt Yonkovit:**  
I feel bad for Agustine. He's just sitting here looking at the camera going. God, we please get to the technical side of things. Yeah, yeah. So so so in two weeks, though, we're going to do another live stream. And evidently, we're gonna have to do it in person in Silicon Valley. So, yeah, Agustine, you should come. Alright. So I invited Agustine. Hopefully, his managers don't care. Karina, I'm very sorry.  No, Agustine next week for you. Alright, so, let us go. Let us share your screen. Let us see what we're going to do. Let us continue our live stream. Let's talk about monitoring and other things on this wonderful Friday afternoon.

**Agustin Gallego:**  
Let me share my screen or just show the whole screen and let's move to

**Matt Yonkovit:**  
and I apologize for the font changes for Agustine's name. I blame Charly, he told me like 10 minutes before that I had to put Agustine's picture on here. And I'm like, Oh, no. So his font is a little off. But that's okay. Continue on.

**Agustin Gallego:**  
Yeah, okay. So, actually, alerting in PMM has come a long way. We used to have alerting only via the Grafana alerting, which meant that you would have to duplicate the dashboards or the graph you wanted. And because of a bug or lack of functionality in Grafana, you were not able to use the templating variables for it. So you would have to basically hard code, the hostnames which you wanted to monitor. So, it was a bit clunky and messy, and it required a lot of work. So, after that, we went with supporting the alert manager externally. So, you would have to have another container or another instance running with your own alert manager, would you go plugging them to PMM. And then finally, the latest design iteration of alerting is what we call integrated alerting which is building PMM itself. And it will allow you to, use all the functionality that PMM has already all the metrics that PMM has, you can generate prompt functions that can go against these metrics and alert you on any custom metrics you want to monitor. So for these, for this purpose, we chose to do it very simply. The idea here is to show the functionality and to be able to walk through the basic steps to configuring and setting up internal alerting. So nothing fancy. But we will show you how to extend the functionality even more with the custom exporters or the collectors that we have in PMM have. So yep, let's start. And the first thing that we will need to do is to activate the feature, because it's still not in GA, although we plan to soon have it released as GA, but for now, what we have sorry. What we have to do is to manually go to Advanced Settings, and manually make sure that we are enabling this feature. As you can see here, these are all technical preview features, which means that we are not currently recommending this for production systems. So this is something that you need to take into consideration. But if you choose to try this out, you just need to you have to manually enable it. After we enable it. We need to, we are going to see that a new tab here appears which is a communication, and we can set up the email or slack. Okay, the email is just your regular SMTP configuration and the slack you will need to create in Slack itself a webhook URL that you can then use here from SMTP What we suggest is that after you configure, you just create a test email that will send you a, let's say, a notification that you can then double-check, everything is working fine. 

**Matt Yonkovit:**  
is it just email and slack? It also pops up in the dashboard as well. Right? You can get to the

**Agustin Gallego:**  
Yes, yes, exactly, we do have a dashboard that will show you the alerts that are currently ongoing.

**Charly Batista:**  
Yeah, because the thing is, you don't want to say 24 hours looking at your laptop screen, right? So but you can still see that refer looking at you will have a monitoring role that people working, that's fine. But one of the ideas, it's you get the communication you'd get on alerting, either through email or his lack of now. And then later on, like, you can extend most features, right. So you can have auto-like, receive a message, or something like that. So if you have a problem, if you have another, you can start troubleshooting but faster.

**Agustin Gallego:**  
Indeed, and yep, let's go ahead and do that, Matt. And let's go to the dashboard that we have tailor-made for this. So this is what you would get when you get the alerts, this is where you see them. Okay. And then, as a way to understand how these dashboards work, the alerts have templates that you then use to generate rules, which then when they are triggered, generate the alert itself. Okay, so we have all of these access to all of these steps here. And then we are going to see how, of course, to create a rule based on the templates, you can only create rules that cover templates. So the first step is to make sure that we have the working template we want. But before that even is, if we want to get a notification, as Charly said, and you most likely do like to have it because you don't want to keep refreshing this all the time, you have to first set the notification channel for the alerts to be routed to. Okay, so since we have the SMTP configured, let's go ahead and generate a notification channel for let's just using PG.

**Matt Yonkovit:**  
That I see that when you chose email, what were the other options besides email?

**Agustin Gallego:**  
Yeah, we have Pager duty, we have Slack.

**Matt Yonkovit:**  
Oh, Webhook. I thought it said WordPress for like, it writes a blog for you when you have an outage on that extension. Right?

**Agustin Gallego:**  
And here we can have, I think if we delete this because we don't have many, the number of email addresses that you would want, in this case, just use mine. And okay, now we have the notification channel. And this means that when we get a trigger alert, we will also get the proper notification via this channel. Okay, so now, since this will be the, let's say the second. The third step is to make sure we have the templates we need to create the rules. Okay, in this case, we are going again, to do this very simply and straightforwardly. And let's just create one for the connection in use and move this away from here. And let's just create one for connection in use based on the existing templates we have, and then we have manually created one and I will show you how to do it. We have manually created one, or when the PostgreSQL service is down based on the custom exporter that we will show you.

**Matt Yonkovit:**  
There are a lot of them already built-in. Right. 

**Agustin Gallego:**  
All of them. All of these. Yeah. So these are built. Okay, they come. Yeah,

**Matt Yonkovit:**  
So, you already have a PostgreSQL down. Why do you need service down one as well?

**Agustin Gallego:**  
This one is using the metric, but we've figured out that it's like a chicken and egg issue and we are not. We are not exporting the metric zero when Postgres is down and we just created we are only having the metric on one when it's up. And then when it's down, there is no metric. So that the alert is never been triggered because there is no matching metric for it. Okay, I see. And if we took this, as an excuse, let's say, to show how to create a custom metric, with your own custom exporter for, let's say that, you want to alert on anything else that PMM doesn't support. And this is a way of showing the extensibility and the power behind the customization that you can make, and you can really alert on anything you want. It's just a matter of having the metric for it. Okay, to create a template, you would just add it over here. And we have a textbox that we can use just to type in, or we can choose to upload YAML file with the templates that we need. Let me show you. I have my notes here. So I should be able to Yes. So in this case, we've used these very simple templates that we are just checking our pg_custom_up metric with an interval of one second. And whenever this is different than zero, we are going to trigger the alert and send all the corresponding notifications.

**Charly Batista:**  
And I can see in your notes, that you have. We're all there for the documentation. Right? So indeed, we can also check the documentation for the templates, right? If you are in doubt about what those things they do, this is we have a place to find the documentation,

**Agustin Gallego:**  
Indeed. And we have the template section. And in one of the steps, we have a proper template that we can base on for creating our own. Right now we are only alerting on the float. So numbers basically, in the future, we are going to add support for 

**Charly Batista:**  
Varchars and yeah. 

**Agustin Gallego:**  
Exact. So let's go. Let's go back. So let's say we've added that text here, we click on Add. And what we would get is this user created a template alerting rule template, then, we have now both templates we want to use, the fourth step is to create the alert rules. Currently, we have none, as expected, because we haven't created anything. But let's go and undo it. So let's do the connections in use first, and PG Connections. And here, you can have the option of input variables, the arguments. So in this case, we want to select it triggers really fast, let's say that we want to trigger on 10% of connections used. And for a duration of one second, so it's actually very fast. As soon as we have 10% or more connections in use, we are going to get an alert for the for instance, in particular, that triggered that even more, we can have filters. And if you are familiar with how we have labels in the metrics, you would understand the power behind this and, these filters. Customization that we can do in here, we can say okay, I want to have alerts only for metrics that have these labels. In this case, we are going to show a very straightforward one, which is the service name, and let me copy from here, so I just make sure I don't make any mistakes. And we are going to say okay, we want this alert rule to trigger only for our PG primary node. Okay, we don't care about connections to secondaries. We don't want extra noise on our pages or in our emails. So we are going to filter these even more with labels. We'll show you later. Yeah,

**Matt Yonkovit:**  
Agustin, under the filters, so we could create arbitrary groups of servers, like Production Development, in different environments, and use that as a filter as well. So you might say, Only select all my production databases for this alert.

**Agustin Gallego:**  
Exactly, you got it exactly right. And we, we kind of covered that grouping available on as you said, Any, any labels that you can, that you can filter by in PMM, you can also filter by in here.

**Charly Batista:**  
Okay. And those values are similar to see like, I see this threshold and then and duration, well, where do those values come from?

**Agustin Gallego:**  
these are from the template

**Charly Batista:**  
So when you create the template, you can create variables inside of the template, and then use that the user can get a better configuration here.

**Agustin Gallego:**  
Yeah, let me check if the example has it, yes, here, the params. So these are variably defined , and you can have as many as you want. And these parameters then will or can be used in the..

**Charly Batista:**  
In the thresholds? Yes.

**Agustin Gallego:**  
Yes. Okay. In the description, and of course, in the alert itself, to give the kind of the percentage, the variable percentage that we want. And then yeah, we need to choose the which channel we can, we want to, yeah, to send it through, we can, we can have many here, let's say if we had Slack, PagerDuty, we can choose one, none all or a subset of any, and that we want. And in here, we can see the actual expression that is going to be used from coming from the template, okay. And then the alert will say this PostgreSQL has too many connections. And this is going to be defined by which node trigger the alert, okay, in your case, this will always be PG primary PostgreSQL, but it may be secondary ones, secondary two if you have, and if you don't filter by them, or as Matt said, if you're filtering by production, you may have many to okay, this is going to be active. Of course, we wanted it. And that's it, we created our first alert. And from now on, whenever we have more than 10% of connections used for more than one second, we are going to have a notification sent

**Charly Batista:**  
Now what good and do I want to stress that database server? Remember the one that we were using last time? So I got to start stressing a little bit here. 

**Matt Yonkovit:**  
is that your database? You're not going to use mine? My database is in my head. Yeah, you're gonna you're not gonna use mine. Mine's already stressed. Yeah, Charly, Charly likes to crash my databases all the time. He's like he comes in and he leaves.  once a week.

**Charly Batista:**  
I know you've got a lot of fun fixing.

**Matt Yonkovit:**  
But now I got Agustine here to fix it. And you won't crash mine. You're just gonna crash yours? Go for it. Yes, yes.

**Agustin Gallego:**  
Okay, so we go to the alerts, tab, we force a refresh. And look at this. We have our first alert because Charly's doing some nasty stuff. Oh,

**Charly Batista:**  
Agustine. Scott, if you didn't get the hours?

**Agustin Gallego:**  
So I'm sorry.

**Matt Yonkovit:**  
Oh, I was gonna say like, so. There are a lot of labels in there. Yeah. Can you pair those down? Come again, is there any way that you can limit the labels that are in there? I mean, like, that's a lot of labels and stuff. I don't even know. Or normal user would be like,

**Agustin Gallego:**  
And this is just like, the metric has these labels associated. And you, you would be able to use any, any of these in your filters. But yeah, there is no way to for now. But yeah, we can create feature requests, and, yeah, okay, I'll make a drop-down or something like that neater.

**Matt Yonkovit:**  
If we're doing feature requests. The other feature request I have is to be able to set the alert and warning threshold on any one of these on the same setup, as opposed to having to create two separate alerts.

**Agustin Gallego:**  
I didn't understand that. 

**Matt Yonkovit:**  
Go back to the alert. Yeah, for instance, you brought up feature requests. When you add on when you edit this you should have the ability to set the warning and alert threshold on the same page. Right, there should be a box that says like,

**Agustin Gallego:**  
Oh, yeah. It's very like for. 

**Matt Yonkovit:**  
Yeah, you want critical high notice in warning all the same page and you to be able to identify or not because otherwise, you have to set up four separate alerts. And all four of them would fire separately. And so that's a lot of extra overhead. Right? That seems a little silly to do that. Anyway, feature request time, Steve. Oh, Steve,  come fix my database fix PMM for us?

**Agustin Gallego:**  
Yeah, there's not much more to say about this.

**Charly Batista:**  
So I'll fix the problem.

**Matt Yonkovit:**  
Well, okay, while you're fixing the problem, Charly, here's the thing that I really want to get in the next 30 minutes or so. Okay. I want to understand the basic alerts that we should be setting up in production, and what those thresholds should be. I think this is a thing that we hear a lot about how to set up alerts and certainly, this is a good 101 overviews on how to get those running. But I think for most of the users who are out there, if we follow our live streams, we've set up the database, we've done some configuration, we've done some optimization. Now we're ready to set up some alerts in case something goes wrong when we're in production. So what should we be looking at? And what are those same thresholds? Agustine looks like, Oh, this is a surprise to me. Charly didn't tell me that I would have to do this.

**Charly Batista:**  
Ah, that's a really good question. Ah, and we have criticalities. Right. So, of course, the first thing that we need to take care of is if our database is running on the stall, right? Right. So definitely, those are the first things. So and some databases are more critical than others as it evolves. Like, if you know how many connections you are getting, and you have a threshold, let's say, Okay, this is my production database, I have a max of 1000 connections. So I can pull 1000 connections, I'm pretty much sure if over 90% of the number of connections, I still have a lot of room to increase, right, I still have 100 connections increase. If I have a database that can only get 10 connections, so 90% of 10 connections, actually, that's quite a lot. Right? So the threshold, will vary on your database, how much you can afford? This is what we always say. So, those are some important things. First of all, the database needs to be run. So if your database is down, you need to get an alert immediately. Right. So that would be the first hour that I would set up for my database, I need to make sure my database is right. The second thing I want to know if my database is being folded by connections, so if my database has been folded by connections, at some point, my users won't be able to enter. So that's a number of 90% of the threshold will be most of the time are good one for a critical value. So as you said, if we could have different thresholds, okay, I have 75% of the connections I got out. So it's getting dangerous but put a got a yellow. So 80% is orange, black man 2%. And then three things going down. Because if we overload the database with too many connections, that's a problem

**Matt Yonkovit:**  
Charly. While you are talking about this, Agustine, Why don't we just set up these thresholds as Charly's talking about it? Maybe that will help give us a visual as Charly talks? Right. So Charly, you said the first one that was important was, is the database never down? Yep. Right. So that is a yes or no question.

**Charly Batista:**  
Because he's going directly to set up , but It's a custom one. If you see, it's, it's accused. So and then like, something, okay, so don't play that.

**Agustin Gallego:**  
So we have added the alert, but let's see what's going on behind the scenes for these alerts to work, as we were saying before, right now, we are not sending zero for when PG up is not getting any data. So what we did actually used one of the customizations that we can do for extending the metrics we have in PMM. This is with the text file collector, we have two different ways of getting additional information from our database or server. And the first one is with the query collector, which means that we can just type in any query, and then the results are transformed into metrics. And then the other file is, the other one is the text file collector, which means that we have to manually generate a file that is going to be able to be parsed by Victoria Metrics in the format that Victoria Metrics expects, and then that is going to be used as a metric. Right. So there are actually several moving parts here on steps that let me connect to the primary, so I can show you, there are many moving parts here. And the first one is we need to have the script to collect the data and generate the file. The second one is the file itself. And the third one is just PMM. Automatically grabbing those metrics from the file, and exporting them to the server, to the PMM server, okay, so in this case, we just build the file. So this is going to be using a local recorder PMM. And we have the exporters, right? Here, we would have all of the exporters that we use for getting metrics. And we decided then to add our script here just for ease of use, okay. And as you can see, this is really very basic. And it doesn't, it doesn't do anything fancy, you could potentially build a script that does very fancy stuff. But in this case, we didn't need it because we have the tool from the Postgres binary folder that is PG is ready, which is kind of it will reply if the if it can connect to the instance or not. So, in this case, what we are doing is just executing this command and discarding the output. And we are getting this is bash, bash is a way of asking the status of the last commands run. So in this case, we are asking what is this? What was the exit status of PG is ready? And we are just writing that into our text file collector directory as a file that again, Victoria Metrics can understand us as a proper metric, okay, in, let's check a bit more what we have here.

**Matt Yonkovit:**  
So you're overriding that. So that's a single redirect. So, you're overriding that file. So, it's not going to keep history

**Agustin Gallego:**  
That is PMM. Servers, responsibility. The clients don't have any memory, the clients just read metrics and push read metrics and push. So yeah, the server is the one that will keep this history for us. Actually, if we, if you were appending to it, you would get to see what yesterday. Yeah, let's. Let's check. First, let me briefly mention that if you would like to have your own custom queries, you can do these in this directory tree. And you will have custom queries for the different database engines we support on the eye with high, medium, and low resolution we didn't talk about that, but we can.

**Matt Yonkovit:**  
I did a blog post in a video on that a couple of months ago, and cascade query, so it might have changed a little bit since then. But if anybody's interested, we can provide those links afterward.

**Agustin Gallego:**  
Nice. And yeah, in the text file collector, we’ll have three directories. High resolution is going to be called every high-resolution interval. In our case, we did it as low as we go, which is one second, by default, it is five seconds. But you can easily change that in the PMM settings. So our high-resolution directory will contain our pg_custom_up.

**Matt Yonkovit:**  
So super quick tip here. If your resolution is one second, you have to make sure your script finishes below one second. Yes, otherwise bad things happen. We ran into that on a live stream a few months ago, where we had a custom query that took longer than the interval. And so it was not pretty. Yeah, what actually ended up flooding the server because of it.

**Agustin Gallego:**  
What I did was to, in that case, I just wrote to a temporary file, and only after like, of course, it will be like it we'll be reading duplicate results while we don't have it. But it's a way of not having an incomplete file that can potentially have many errors.

**Charly Batista:**  
We stopped the database, just to see the result of the file, it's gone now. Okay. You see there?

**Agustin Gallego:**  
From the metrics here. Yeah. Yeah. So we're going to have it, it's changed already. And it's interesting to see these from PMM. Server. And if you're wondering how can we check if things are working fine, we do have a dashboard that we can use for this, which is called the Advanced Data Exploration, which lets you access all the metrics you have. You can just type here any or just custom any kind of string or substring. You can select it and select an instance from here, and you can have the actual values that these metrics were having. Right. So this is another way we can use to validate that everything is working as expected before we create the alert rules. So it seems like it's working. Let's go back to our alerting. Sorry, for our alerting. Dashboard. Have you started it?

I did. Okay. Okay. Do you want to find out? Yes. That's funny. That's.

And yeah, this was a critical PG download. Okay, just to stop it. And we have the metric, the metric the alert. And yeah, I'm not sure if it's safe to show my email right now, so I would rather not do it. But trust me that I'm receiving emails.

**Matt Yonkovit:**  
That's okay. That's okay. All right. So we've got that this one is down. Is there any sort of like, pop up, or anything if you're on another PMM screen that will show when this fires?

**Agustin Gallego:**  
What, sorry!

**Matt Yonkovit:**  
Like a pop-up or a notification that?

**Agustin Gallego:**  
Oh, no, no, yeah. 

**Matt Yonkovit:**  
No, it's either you get the alert through going to the dashboard or email or SMS or pager duty?

**Agustin Gallego:**  
Yeah, yeah. 

**Charly Batista:**  
For these, you need to set up a slack tool.

**Agustin Gallego:**  
Yeah, Slack. But yeah, it's nice. We could have a

**Matt Yonkovit:**  
Yeah, like, like, like a bell or something at the top that flashes or something that says you need to check your alerts. Yep.

**Charly Batista:**  
That would be another really huge feature request.

**Agustin Gallego:**  
Yeah, I will come to write this down. If we forget that.

**Matt Yonkovit:**  
We're coming for you, Steve. We're coming for you. Oh, yeah. It's recorded. Yes. Nice. Nice. Yeah. You can just point Steve to this and say, like, Steve, we just do everything we told you to do in this.

**Agustin Gallego:**  
And, yeah, I think that's basically what we wanted to show.

**Matt Yonkovit:**  
Well, I would still like to go through , and I want to get the same threshold for those who are watching. We've still got some time. So we said connections. You said Charly 90% is a good threshold for the number of connections. A warning was probably 75%. Right? Yeah. So  So that's a reasonable kind of like thing where when you have connections 90, is that a red alert?  You need to look at this and do something. 75 is, what else should we be looking at? So we've got connections, we've got it up and down. I'm a big fan, of CPU. Right? Like, so checking the CPU utilization?

**Charly Batista:**  
Yeah, definitely, we can go-to OS, like to manage CPUs and utilization. And also when you have main IOs, right, I use this is any indication. And when we have queries that are taking too long, so if you have queries, that run for too long, and have

**Matt Yonkovit:**  
But taking too long, how would you set that up? And this is a good one. Because queries can vary depending on what sort of query it is. Can we set an alert I don't think we can right now, but maybe I'm wrong? On a per-query basis, I think it's gonna have to either be like, all the queries aggregate, like so a latency number for like, the average query latency, or it's gonna have to be like, you'd have to specify like an individual query tag, right?

**Charly Batista:**  
Well, actually, this depends on your template, and also on the metrics you're collecting. And this is why this is beautiful with PMM, right, we can try to extend them. And this would be a really interesting exercise, maybe we don't have time for today. But we can work together with either set. And we have something set up for maybe next week or the week after that we do an exercise for this one where we build a personalized template. And also some metrics that we collect from the database. One other thing about

**Matt Yonkovit:**  
You are asking me or Agustine, because you and Agustine have to do all the work, I just need to,

**Agustin Gallego:**  
Like, I'm not saying in this Matt. Yeah.

**Charly Batista:**  
You. Okay, just say, Oh, please.

**Matt Yonkovit:**  
Well, okay. So here, here's, here's the thing that I am interested in seeing. So, I mean, obviously, for me query latency, I mean, for everybody, query latency is a big deal. So number one, we need a threshold. And I don't think there's one by default that's going to do this.

**Charly Batista:**  
No, it varies on your query. So yeah. One minute, you will not expect it to get for better seconds, right?

**Matt Yonkovit:**  
ideally, I think that the best we could hope for right now, let's just brainstorm for a second feature request time, Steve, is the ability to say, this system, all of the queries average, a 200 millisecond response time, or latency. That's the P99, latency of the queries of all of them. And if you can figure that out, you should be able to set a threshold in your alert to say, Does it go more than 150% more than that? So does it go to 300? And if it goes to 300, then send me an alert. If it goes to 400, it's critical, and page me something like that should be the basic, ideally.

**Agustin Gallego:**  
Yeah, well, that's my point, I think in click house, we can just query these because this is what we have in query analytics. So yeah, we can,

**Charly Batista:**  
we can sanitize the cracks, right? So when some bias occurs, you can aggregate them based on the spine of the value of the parameters. So if you have the very same activation, you can have a hash of each of them. And for that, you can have historical data. So for the period of time, we had historically, it has an average. So if it goes over the average, we can even calculate something. Like the deviation so if we have a factor of the deviation, it goes over the fact that aviation is a problem.

**Matt Yonkovit:**  
Right? Yes, I think oh, no, I mean, I, I get what you're saying.

**Charly Batista:**  
Right, maybe we still don't have all the tools to do it at this moment. But like I would, I think it's quite interesting. I would like to try.

**Matt Yonkovit:**  
So I actually have the query to do that, if anybody's interested. So yeah, so I actually have that. I mean, it's for the time-series graphs, but we could, we could get the overall fairly straightforward. In fact, you should be able to see this overlaid on the screen there. Yeah. So, so this is the query response time for this particular database, and so you can see that the JSON here selects Time Series from this. So it is possible to get that if we needed to see at it. Yeah, it's a little easier to see it this way. Oh, I can't, why can't I get that down? There we go.

**Charly Batista:**  
Pg_stat_monitor gives us the sanitized query. So we should be able to use it to help us with this task.

**Matt Yonkovit:**  
Well, so if you're talking sanitize query, then what you're doing is you're saying, let me see, you're saying like this particular query right here, we'll just pull it this way. This one, you're saying? Select any of these and see if they've deviated from the regular time frame. So we might have 1000 queries and use just the sanitized query to be the identifier?

**Charly Batista:**  
Yeah, that's the thing. So because we, we want to know about it. Right. So we don't care about the value of the parameters. Of course, if we like, let's say, for example, you have in your database, table users, that you have a billion of users 75% of all those users from the same CD, and we do a select on that table searching for the CD on that CD, the time gonna take a lot more than when you get the users that are on a smaller CD, right? So we do understand, but as when the time's advances, and you're still keeping an assertion from that, that user on that evil cache gonna pull you on, and we will have an average. And you see that the largest one will be quite high up on the above with the just forgot the expression, you just said. the deviation or the deviation going to be high, we're flattening them by the average. Right?

**Matt Yonkovit:**  
It is applicated thing, though, what you're talking about is I mean, like, if you've got 1000s of queries to try and do that with that's unique queries, unique sanitized queries, right, that that's a, it's a massive,

**Charly Batista:**  
this is the point that we only get the query, we don't care about the parameters. 

**Matt Yonkovit:**  
Yeah, but even so like, it depends on the system, like you're making an assumption that the system might only have 100 sanitized queries. There are some systems that have 1000s of unique permutations or even 10s of 1000s.

**Charly Batista:**  
And that's, that's fine. That's why

**Matt Yonkovit:**  
it's a much different scale problem, right?

**Charly Batista:**  
No, that's okay. That's okay. If you get to the point, then the number. So we need to start working on that one to solve.

**Matt Yonkovit:**  
Yeah, by the way, we've totally bored Agustine, he's like, please, please, can we move on? Can you stop talking about this? Yeah, let's move on. So okay, so here's, here's the thing, here's what I want. Here's what, okay.

You have just been tasked with being the DBA of this new system. What are those alerts that you're going to set up? And what are the thresholds like 5-10, whatever it is, just, let's go through because I want to get those out to the community. Because I've had this question asked more than once in the last few weeks, where people are actually asking like, okay, it's great that there's integrated alerting, it's great that I can alert but what the hell do I alert on? Like, what are the same thresholds? Yeah. And on top of that, for your connections. 70%. Is one second enough, or should it be like 10 seconds? Should you look at five seconds? Because if it's one second, you have one spike, everything goes to hell? So I think that's where people are looking for some guidance here. And I'm hoping to provide it is what does that look like?

**Charly Batista:**  
Okay, let's, let's put let's make a context, right. So, you have your website. And your website, you sell hats, right? So you're selling you have a selling website or selling hats website, right. You have around 1 million unique connections to 1 million unique connections per week. That is round. 100 million connections. Quick, not unique ones. But not unique users. So this is your website, right? So you have 100, connections, Max 100 connections for a database. On your database, you have 32 gigabytes of memory and eight CPUs. So we have a context, let's try to work on this context. Right? So in this context, if you have 75% of connections for more than two minutes or five minutes, I would say five minutes. So, you should get on out. Because well, it's not critical, though. But it can escalate. So if for 10 minutes, you have more than 75% of connections on your database, it means you're getting pushed, if it increases and if you have 90% of max data collections for five minutes. So then you start to do need to start to get something because eventually, we are going to run out of connections. Right? So we have, one metric with Q transpose. 

**Matt Yonkovit:**  
I would propose that for connections then that you might want three, because you can have multiple criticals, right? So if you were going to do the five-minute thing, and tell me if I'm wrong, I would much rather get alerted if it's a sustained amount of connections over a long period of time. I want a warning, or some sort of heads up that this happened, and it stayed up. But then I'd want it as it got higher to say you need to do something. But if it reaches 99%, I want to know, the minute that it does it or the second that it does it because if it hits, like it's going to run out in the next five minutes, I need to know.

**Charly Batista:**  
I agree. I agree. And I will put a smaller threshold because in your case, 99% all leaves you with only one connection.

**Matt Yonkovit:**  
Yeah, sure, like, whatever that is, but  like, I think there's some, some case to be made for bonus

**Charly Batista:**  
You should get to the point when you need to do immediately take an action. Okay, right. So we take it as 95%. When you get 95% of connections, you get an alert immediately.

**Matt Yonkovit:**  
Okay, so, connections, CPU, CPU. I'm gonna, I'm gonna say that I want to know about.

**Charly Batista:**  
Okay, hold on. Before we move out of the database

**Matt Yonkovit:**  
Yeah, keep on smiling. Agustine, do you have some time?

**Charly Batista:**  
Yeah. Oh, God, I have something like the database is down. This is one that is critical. And it should be needed

**Matt Yonkovit:**  
Database down, we're fine on I mean, I'm fine on the database down. Okay, I think everybody knows that you need to alert on that.

**Charly Batista:**  
A lot of people did up a lot of people that just forget that the victim is a problem. And they figured it out when the database goes down, and the cd goes down. So wherever they are, we have a number of connections. Right? And we should also be alert when we have a connection that's running for long enough, let's put it here and five minutes. Whatever. It's running for more than five minutes, it is a problem. Especially in your case, that is not an analytical database, your own database, anyone it ramparts. So what has been the browse for more than five minutes is a problem. And it should be out for that. So you need to start taking action right? On this. We don't we don't need to have three T and complex math, you just put in five minutes, whatever is over five minutes, you get an hour. So we have done we have a max number of connections, we have five minutes transaction. What else is good data from the database?

**Agustin Gallego:**  
 Yes. I will move to IOs.

**Matt Yonkovit:**  
Thank you, Agustin. I guess we could look at the number of locks or deadlocks that are happening. So if there's an excessive amount, those are possibilities, but generally, I found that those are more one-offs. And you're probably going to get a better sense from the application. Yeah.

**Agustin Gallego:**  
You don't have to cut an alert Everything like PMM also has, you can review it daily. And there are things that you can just check in your regular day-to-day operations that they don't need to have an alert per se. Right. Okay, let's move!

**Matt Yonkovit:**  
Yeah, I mean, I think the only other thing in the database, which we already beat up was, I would like to see a query latency number where we have some sort of metric that collects it. But quite honestly, from a query, metric perspective, or even from locks or anything like that, you will, it is always best practice to recommend that we have an alert on the front end application for the response time, right? So if you've got a website or whatever, you want to look at the average response time for web pages and things like that and look at the application response time, that should be one of those critical metrics you look at. And then if that starts to fail, then that's where you might look into the database to see if there's some contention or issues.

**Charly Batista:**  
Well, on Postgres, we also we need to be careful to vacuum, right. So if for whatever reason our outo vacuum stopped running, we need to be alert on that. Maybe I used to just disable all the watch on my database. I want to know if somebody goes there and disable my autovacuum. Well, he's from immediately alert.

**Matt Yonkovit:**  
Agustine told you to move on from the database.

**Agustin Gallego:**  
Never listen, man but

**Matt Yonkovit:**  
He never listens. I know. He never listened. Never, ever, ever. Reply. So okay, we're going to, we're going to go into the OS. 

**Charly Batista:**  
Okay, Did you check the vacuum thing?

**Matt Yonkovit:**  
I'm saying the top five things that you would tell everyone top 10 things, whatever it is. I mean, yes, you want to run vacuuming? Yes. You want to have auto vacuum set up by default. That setup though? So yeah, if you turned it off, shame on you. But we're talking about the bare minimum.

**Charly Batista:**  
So it's another one as well.

**Matt Yonkovit:**  
He really wants to be right. Doesn't he just have to be right?

**Charly Batista:**  
I just want to ask it, folks, if you don't remove my autovacuum,

**Matt Yonkovit:**  
We've already removed your autovacuum.

**Charly Batista:**  
We're just moving on to the CPU things. Okay, CPU, what is your recommendation for CPU?

**Matt Yonkovit:**  
So generally, personally, I want to be really thinking about CPU at the 60 to 70% range is when I'm going to start thinking about what's going on. And then once it hits above 80, then I'm really worried.  I don't want to run to the red line, I don't want to run to 99%. So I'm a little bit more conservative in that. I might not do much at 60%. But that's something that I'm going to look for. I'm also going to look for the trends. And I think that's big. So there has to be something where you're like, I'm at 75%, let's say CPU, you need to do something, or I'm at 90%. And you need to your hair's on fire. But I'm really going to start to think, hey, if I'm at 60%, did it increase?  120% over the last week, did it? Did it double it? I'm going to look for the difference in the Delta over some time period, once I know that we've reached a certain threshold. So that's more of a troubleshooting thing. From my side is, I'm gonna look at what is it today? If I reach some threshold for me to look, the first thing I'm going to do is it trending up in Did I hit this, or was it some random spike? 

**Charly Batista:**  
Okay, well, Charly's gonna tell me I'm wrong. No, I'm fine. I accept your roles. I just don't like

**Matt Yonkovit:**  
Except for the step exception. Okay.

**Charly Batista:**  
Now, jokes aside, I do not really consent that much about the percentage of CPU usage because, well, if it's about perception, I would like to have knowledge with like, if we, if we get 85% of CPU, I definitely would like to have knowledge but 95% Using your CPU doesn't necessarily mean that the server is going bad right? So it means that it's just using the CPU and can be for a good reason. And can be just replying as fine as or as better use as using 75%. Right. So , but yeah, I would like to have knowledge on CPU on 85% Definitely. Okay, let's get to what about. 

**Matt Yonkovit:**  
So, are you a bigger fan of load average?

**Charly Batista:**  
I do. I do like to take a look. And again, it depends on All the perceptions but yeah, usually the load average gives me more insights and more problems than just the average number of CPU percentage.

**Matt Yonkovit:**  
Like load average CPU, are you watching both you watching one or the other?

**Agustin Gallego:**  
I would, I would actually check the normalized CPU graph that we have in PMM, and the runnable on the blocked processes. But that can also flag-like, I'd be more worried about saturation than utilization.

**Charly Batista:**  
Yeah, that's that's the thing. That's the point

**Matt Yonkovit:**  
What about Wait, IO? Are you looking for Wait io?

**Charly Batista:**  
Well, this is about saturation, right. So if you had really high IO utilization, and if they're taking too long, that's a problem using having high IO is not a problem if you do not have latency. So I would like to find metrics that carry latency because if the latency starts increasing, that's we have a saturation problem.

**Matt Yonkovit:**  
Right? So you said, normalized CPU is normally CPU in the CPU graph. Agustine, where's them?

**Agustin Gallego:**  
Sorry, come again.

**Matt Yonkovit:**  
Where's the normalized CPU? 

**Agustin Gallego:**  
Oh, it's in the summary, like in the OS summary?

**Matt Yonkovit:**  
Oh, it's an EOS summary. So under the Node overview,

**Agustin Gallego:**  
No, the other one

**Matt Yonkovit:**  
All right. So you're, you're looking. There you go. Let's Yeah, yeah, so you're looking here.

**Agustin Gallego:**  
Um, below, there's the processes,, which will also have blocked on the runnable. Process? Huh? Yeah. Okay, that's like the rmb column from VM starts basic.

**Matt Yonkovit:**  
Okay. Yeah. So if I look at this particular box that has been running for a while, let me just let me get the one. That's awful. I'm gonna get the worst one. This is my worst offending one. So what you're looking at is the spikes here that hit 100% on the saturated. 

**Agustin Gallego:**  
That means that at least one core was at 100%. So that can mean one or all. And then you would use the yellow to see the amount of saturation and see that's like, the normalized part.

**Matt Yonkovit:**  
Okay. And herewith block processes, when we see that there's three or four, that means there's three or four waiting?

**Agustin Gallego:**  
On IO

**Matt Yonkovit:**  
Yeah. So that there you go. So those are metrics that you could set up, as well. So , but you're not looking that close at just the IO wait percentage in from the CPU stats anymore?

**Agustin Gallego:**  
Yes, yes. Yeah, but the first place, like if I'm thinking alerting the first place I check is blocked. Yeah. Yeah, but you got, of course, you can do as aside. Yeah,

**Matt Yonkovit:**  
Yeah. Um, so swap, obviously. I mean, I think when you get to like the memory stuff, your biggest concern here is you want to avoid OOM. Right, so you want to avoid getting killed. So that is a critical metric to check for. And I think that there's a long been a long-standing debate, weather swap is should be configured or not. And there are a lot of images that if you just add an Amazon image, they have zero swap setup out of the box, which is interesting because then that killer will come and kill your system as supposed to just being slow. 

So really what we're looking at is a number of connections, if we can get a query latency, great. I'm going to skip autovacuum Because Charly's just been drinking all day. We're going to look at some general CPU metrics, we're really going to look at the normalized CPU and the number of block processes we want to alert on that. it's possible to look at load average as well or wait for IO percentage, but those are more secondary to looking at a swap or looking at how close you are to actually be out of memory is also critical. And I think that the last one that I will say is silly for us to miss but so many people miss it is disk space, right? I mean, like I mean, it sounds so simple that I ran out of space but with all the logs and things that you can turn on  you can run out of space quite frequently

**Charly Batista:**  
Another one that we've missed we've been missing all the database is the ID wrap around? That's a very important one. And people also like to miss them a lot?

**Matt Yonkovit:**  
Well, that is one that if it hits you, it's bad. But it doesn't hit everybody, as frequently or at all. I mean, I think that of the people who have it, there's, let's just say like, in my experience, it's been a relatively small number of Postgres users hit the wrap-around, but when they do, it is very bad and very vocal. I don't know, maybe you have a different experience than me, but most people will get in, in mass. 

**Charly Batista:**  
That's the point-like, we have some customers that they really run up with under a lot of stress on the database. And that number exhausts quite fast. And that's why in our case, having a properly auto vacuum, and Id wrapped around is so important because we do have a quite good number of passwords, and they have a lot of transactions per cycle. And this number exhausts pretty fast.

**Matt Yonkovit:**  
Yeah, yeah. Yeah. And I think that the other one to keep in mind is if you are running a cluster, the status of the cluster matters. Right? So if you're running replication, is it up?  and that's just not an up and down. That could also be our Is it getting caught up? Is it caught up in processing things in a timely manner? Is there any sort of lag or delay there? Yep. Now, interestingly enough, I generally don't see a ton of networking problems anymore. I don't know about you. I mean, it happens, but it doesn't happen as frequently, as I've seen in the past.

**Charly Batista:**  
That's true. That's true. My Network has been quite reliable now. So it's pretty rare. When we run well, we do from now and then but is to see indeed, pretty rare when we have network problems.

Okay, cool. Oh, see, any things that we've been alerting are concerned about network recently? That's indeed true.

**Matt Yonkovit:**  
All right. So we don't have any questions. What was that? Oh, server

**Charly Batista:**  
Sorry.

**Matt Yonkovit:**  
Yeah. I was gonna end the stream. Do you want me to continue? Agustine, he really wants to go. You could tell in his eyes. He's like, it's Friday. Yeah, Agustine. He's like, I'm glad this is the only one of these I've had to be on. This is horrible.  like, Why do I have to sit here and listen to Matt and Charly? Oh, yeah, I get Yeah, I get you, Agustine. I can't stand myself, either. 

Yeah. So you get in this week, I get two weeks. So. So maybe we could commiserate afterward about our experiences. All right. Well, thank you, everyone, for hanging out for a couple of weeks. We'll be back. I don't even know what the topic is. In a couple of weeks. What are we supposed to cover? Does anybody know what we're supposed to cover? Let me go to the website. Let's Yeah, you probably should prepare for that. Right. You would think

**Charly Batista:**  
it's a good idea to get prepared

**Matt Yonkovit:**  
yeah. Well hey, we'll just see. Why not? So let's see events. So we're gonna go to the Percona community website here. If you haven't been here, you can come and you could see sad Matt and sad Charly right here. There we are. Chino and The HOSS. We're so sad. We're so sad here. So oh, look at this. We're gonna be working on backups next in two weeks.

**Charly Batista:**  
Whoa, whoa. Agustine knows a lot about backups.

**Matt Yonkovit:**  
Agustine, are you gonna be a regular guest? Are you coming back every week? Do I need to add you to the official rotation? Do we need to put your picture? Yeah, you want to come back? Perfect already. So no, no, come on. Like, we'll have you back. And you can do? How about Oh, you want to do some Aurora? We can do some Aurora would work with us. You can do some Redis work with us. This is all good stuff, man. Come on. Join us. Join us. Join us every other Friday.

**Charly Batista:**  
I know. He would like to get on those Kubernetes. Well, I pretty much where he would love to do those. Because how he that stuff? Yes, he does.

**Matt Yonkovit:**  
Okay, well, he'll, he'll be on the Kubernetes stuff. So, Agustine, there is a slot. So this is every other Friday. If you want, you can come back every Wednesday. And if you could just be me and you. Right, like, and we could talk about, like, it can be us complaining about him every other. Yeah, I think that'd be good. All right. All right, everybody. Thank you. We hope that this was helpful to see how alerting works and PMM, and what are the common things you should be looking at? If you have questions, feel free to reach out to us.  Subscribe to the button that's in below on YouTube, or wherever you're watching.  Like it. Thumbs up it asked questions on Twitter, we would be happy to answer questions. And we will send all the questions for all live streams to Agustine from here on out to our official guest answer. So thank you, everyone. We appreciate the time. We'll see you next time.

**Agustin Gallego:**  
Thanks, everybody.

**Charly Batista:**  
Thank you, Matt. Thank you, everyone.








