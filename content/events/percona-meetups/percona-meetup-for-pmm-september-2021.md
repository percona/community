---
title: "Percona MeetUp for PMM Sept 2021"
description: "This week the PMM MeetUp is live broadcast from the Open Source Summit (OSS Summit) in-person conference. We will discuss PMM and answer questions."
images:
  - events/percona-meetup/cover-pmm-682.jpg
date: "2021-09-29"
draft: false
speakers:
  - michael_coburn
  - matt_yonkovit
tags: ['PMM', 'Meetup']
---

The Community MeetUp for PMM was an extraordinary one-hour Live Broadcast MeetUp from the OSS Summit on last Sept 29th, to talk about open source databases, observability and monitoring MySQL, MongoDB, PostgreSQL with PMM. Percona experts Matt Yonkovit and Michael Coburn has made a PMM Demo. Check the the full recording by clicking the video here:

## Video

{{% youtube youtube_id="2WSsmhzsVXg" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit**  
Everybody, welcome to the OSS summit. We're here for our PMM meetup. This is the first time we've done one of these live. So hopefully you can hear us and there aren't any issues. If there are go ahead and just hit us up in chat we're trying something new today. So thank you for joining us, though. I've got Michael here. Hi, Michael, how are you? 

**Michael Coburn**  
Hi Matt! I'm glad to be here. 

**Matt Yonkovit**  
So you can see we're in the booth. We're here before anyone else's, it's Oh, eight o'clock in the morning here in Seattle. And we've got our booth demo going. You know, for the booth today, we've also got the controller where we are controlling all of the MySQL and Postgres workload that we're seeing behind us. And so what we wanted to do a little bit is just talk through this. So if you can give us a shout-out in the chat, if you can hear us, we want to make sure that everything's working. Okay. Look at that Wayne is here. Hey, Wayne, glad to see you here. You know, as I said, this is gonna be a little bit of a different show, for us typically, doing this from my office, I'm gonna go ahead and get that situated. But you know, glad to have everybody here. And let's see what we got. Yep. All right, you guys can? Can you hear us? Is that here you can hear us? Or is that a no, you can't. That would be a little bit louder would be nice, they said. So we can do that. We actually have the power with these microphones to increase the volume here. So let's go ahead and let's see about that. How's that? Is that better, everybody?

Alright, cool. So what we wanted to do here is we wanted to show you some of the things that we've done with PMM here at the show, and show you how you could potentially do these yourself. So Michael has PMM up on his screen. So what I'm gonna do is we're gonna flip over to his screen, which is going to be mirroring what's up here, because it's really hard to see what's behind us. But if you are not familiar with these meetups, basically, these are designed to be share information, tell people how to work on certain things. We'd love to have people who are using PMM in the field out there, come on the show, and just share things. This isn't about anything that is scripted, it's all unscripted. It's just us talking and sharing and answering questions as we need to. So Michael, let's go ahead and let's flip over to you so you can kind of show off some of the things you're doing. And so right now we're running with this workload. And it looks like we are just doing a little bit of Postgres workload, about 5000 queries per second. So go ahead and take it away, Mike, sir.

**Michael Coburn**  
Thanks, Matt. So what we've got here is we've got a customized dashboard, which is part of PMM stands for Percona Monitoring and Management. And this tool is designed to give you a visualization approach to how your database is performing. Thanks to this beautiful box that we showed earlier, we're able to dynamically control the workload, and then we can reflect that workload through PMM. So what we're seeing at the top row here, we've got three different main characteristics of how you can look at your database, we're focused on how many users are connected, you see that in the top left screen here, db cons. In the middle, you can see how many queries per second are running against your database. And on the far right side, you can see the response time, all of these factors are important because there are limited resources available to any given database. And what we can do, I will be able to dynamically adjust the workload by turning some of these knobs here. If you can see, it's probably a little bit faint on the back, but you can see that the screen is actually being modified just a little bit. And what I've done is I've turned us up to about 30, different workloads running at the same time. And what we're going to do is we can already see that we've got these purple lines being drawn, these vertical lines, these are called annotations in PMM. And the usefulness of these, well, there's a multitude of different places you can use it, we've decided to show it as the workload modifies that it will reflect a line, and then you'll be able to see the deflection point in your graphs and be able to attribute those deflection points to something significant that occurred, working with some customers at Percona. Oftentimes, they'll want to use it for when they have a code release, that's a popular time to do an annotation. Or perhaps if your cloud provider has any type of event, you might want to annotate that on your graphs. The point being is a nice line can describe to you some external activity that occurred, and how did that impact your database performance. And so I'll talk really quickly over some of the different things you see on the screen. Some of these graphs take about a minute or two to update. And that's because of the different data sources that are being used within PMM. So at the top, I showed the three most important graphs down below, you can see that we're providing a view of query analytics, a little bit different than the other section of PMM

This one here is one that Matt pulled together and is able to show not only just queries that are running or having executed but some other characteristics about them, such as their count, their average run time, their max run time, this is really helpful stuff. If you can plot that at the same time, over the database characteristics, what is the response time changing? And now we have a long list of the different queries that are running. One of the neat features, though of this actual dashboard here is we can pop into another window. See, I think I need to switch over to that window as well.

**Matt Yonkovit**  
 Yeah, because you're not sharing your 

**Michael Coburn**  
That's right. That's right. 

**Matt Yonkovit**  
So they have stopped sharing if you want to stop sharing, and reshare. So Michael is going to quickly stop sharing for a second and flip over to the one. So just share Chrome, I guess that's the whole screen.

**Michael Coburn**  
Okay.

**Matt Yonkovit**  
Now, you might see us multiple times, oh, I gotta let go ahead.

**Michael Coburn**  
There you go. Sorry about that technical glitch. So we're back. So we've got this kind of secondary dashboard here that lets us drill into each of the individual queries. And what's really cool about this is it'll give you per query statistics over the performance of this one query. So we can look at the response time here on the right-hand side, how has this query been modified over time. And then the number of times that the query has been running as described by the database queries per second, the graphic that I liked the most. And I think we might be able to come back to this later as the workload is changing. This view shows us every minute, what has been the performance of this query. And what's cool about this is in a standardized environment were not too much is changing, you would expect that your query response time would remain fairly standardized. But we can see in some instances, that their increases are considerably larger in some cases two or three apps. And what we can describe here is that we've made other changes within the environment, we've added and removed indexes. In the case of PostgreSQL, we've done some vacuum operations, etc. So all of these external factors will impact individual query response time, even if you haven't changed that query in and of itself. And so this is a great tool for people to be using to visualize the performance of their database environment. 

**Matt Yonkovit**  
And so now you see the workload that you changed a few minutes ago is starting to pick up.

**Michael Coburn**  
That's right, that's right, we can see as I modify the number of workers, obviously, that increases the number of connections to the database. Right now, we're still able to increase the volume of queries. And we actually are able to see that the average response time is coming down. So generally, that's a good thing, you've increased users on your website. The thing to pay attention to, though, is that most resources in the world are finite. And what we're also doing on this dashboard is plotting the CPU utilization. And we realized that we don't have very much more headroom here, we're gonna we're floating around 90%. So there's only going to be a limited amount that we can go any higher here. 

**Matt Yonkovit**  
So I wonder if we have cleaned up yesterday's because we were able to get 15 16,000 queries a second with this workload. So I'm wondering if maybe we let's, let's, let's see, if we have or you put a challenge to me, we're gonna put a challenge to Michael is going to try and tune this Postgres instance, which Michael likes because MySQL better he's not the Postgres guy that he used to be. So we're going to see what he can do to maybe get a little bit more performance. 

**Michael Coburn**  
Okay, let's see what we can do. First, we're going to increase the number of workers on the application. So I'm going to be a little bit crazy here, we're going to go from 30, maybe we'll take it up to 50. 

**Matt Yonkovit**  
Now wait a minute, you were already 100% CPU bound.

**Michael Coburn**  
That's a good point. 

**Matt Yonkovit**  
So you're going to add more workers to 100% CPU-bound workload. That seems weird. 

**Michael Coburn**  
That's right. That's right. And I don't know where this is gonna go. This may or may not work.

**Matt Yonkovit**  
He's brave. He's brave. 

**Michael Coburn**  
One of the cool things that we can do with this, this deck here in front of us is actually got four different types of workloads on it. The first knob that I keep touching involves primary key and secondary key lookups and a minimal amount of writes. So if I really want to just tune for making things as fast as possible, get the number of queries up, it's going to behoove us to be using the primary key as much as possible for any type of queries, I'm going to try to turn off some of these excessively long queries and probably turn down the number of rates, that's the first place I want to go. Generally, databases will perform more quickly on read-only workloads. And they will for writes reads mean, first, maybe fetch it from disk the first time, but otherwise, you're often working on a memory-bound workload. And reading from memory is obviously faster than reading from a disk. If you turn that around, and you talk about write, it'll be very difficult for us to really scale writes any faster than reads, because there are additional operations involved in order to persist the changes that you wanted to make in the database. 

**Matt Yonkovit**  
But a lot of those, a lot of those are going to be offset right. So you're only bound in a lot of cases, not by the actual instrument. A lot of it's checkpointing, which, if you've set your settings properly, could take a really long time. So you might actually get good insert throughput, right?

**Michael Coburn**  
Well, each database technology is different. Postgres and MySQL have different types of checkpoints. Right? Yes. One of the things that come to mind with regards to Postgres defaults to the vacuuming process. Hmm, yes. And that one can sometimes be challenging in terms of what, what behavior, or what impact that's going to have on your environment? Yeah. So in our case, sometimes you want to be able to schedule that. Sometimes you might want to be able to demonstrate in terms of a live demo, what the impact of running a vacuum during a business period if you're trying 

**Matt Yonkovit**  
Oh, are you going to? You're going to do that?

**Michael Coburn**  
 I'm a little bit interested in seeing what would happen here. So you won't be hidden? 

**Matt Yonkovit**  
Yeah, hold on. So we'll have to go up to the top. Okay, so let's see what your changes did thus far. So what do we get here? 

**Michael Coburn**  
So you're still well, I'm ready to flex a little bit, I got to about 14,000. 

**Matt Yonkovit**  
So yeah, so 14,000. So, he turned off some of the workloads because there's some long-running transactions. If you didn't see this guy. Here, we'll just go ahead and flip this over. So you can take a look at what he's doing. You know, we've got these different knobs here. And each of the knobs, when you turn it will increase one sort of workload. So there's reporting workload, there's this heavy insert workload, and then there are long transactions. So here's the original, he had all of these turned up, because he just likes to touch buttons. That's just how he rolls. But before getting more throughput, he turned off some of the workloads. So he created a little bit. Basically, what I'm saying is he wanted to crank buttons. And then he didn't want to fix the buttons that he cranked. So never great there. But hey, whatever. Alright, so let's go ahead and look at what happens when you run a vacuum. And right now, obviously, Postgres has an auto vacuum. So you know, and there are thresholds you can set, but you can run the vacuum on its own as well. So, go ahead and hit the vacuum button, there's a vacuum button on this thing, 

**Michael Coburn**  
finger coming in, 

**Matt Yonkovit**  
you can see it on the side, clicked away. There you go, it's been started. Alright, so now he's going to run a vacuum, we're at 14,000. So part of this, and part of the cool thing, how you can deploy and use PMM in a production system. Hold on, I'm gonna flip us over so we can talk while that's running. And we'll come back to the screen is, one of the cool things about using PMM in a production-level system is you can use it to do benchmarks and tests and test different code releases, right, so you can see what the impact of certain activities are if you added an index removed an index in test, you can then you know, run your workload and see what those differences are, you can check different code revisions, right. And so one of the powerful things about Grafana, that we include in PMM, is the ability to do annotations. And so you know, every time we click a button, every time you deploy code, you could write an annotation that says, this code was released. And that provides you with a really powerful way to see what happens over time, right? So you go to bed, you don't know what happened overnight. But if your code is instrumented and it's calling the annotations you need you're going to then potentially be able to find that needle in the haystack a little bit easier. Now, let's flip back to your screen because I see that some things have changed. Right? Look at that.

**Michael Coburn**  
What happened to our database queries per second is what I want. Yeah. 

**Matt Yonkovit**  
So scroll down a little bit, because I think it's like, that's the interesting thing. We went from 14,000 to 3000. And it's going to bottom out, actually. So you can see that the queries per second there is just like, plummeted. I mean, it's gone off the charts slow, because we're actually vacuuming and cleaning up the table that is mostly being hit by the workload regenerating so I mean, it's definitely something that you see that impact. And that's it's something that people intuitively now everyone says, not talk to me about vacuum settings again, but from a vacuum perspective, it definitely can impact performance. And that's why making sure that those auto vacuum settings are set. And there are some companies who actually tried to delay a vacuum forever like, we just can't afford to do it. And it just gets longer and longer and longer. And there are all kinds of other consequences that you can.

Okay. All right. So why don't we flip over to some MySQL workload because you're more comfortable with that? The vacuum should finish in a second. Why don't we give that a second to wait. But, Michael, you used to be the product manager for PMM. You've been around PMM forever end ever. And we've seen this deployed all over the place. What are a couple of interesting things that people might not know about PMM? Or the capabilities of PMM?

**Michael Coburn**  
That's a fair question. Again, this is unscripted.

**Matt Yonkovit**  
That's how we go. It's unscripted. 

**Michael Coburn**  
One of the great things I think I like about PMM is that once you get it deployed, you can instantly be useful with it. That means you can be making observations yourself as a database administrator, or as an application developer. And what I love about that is it enables a conversation between those two teams, which are often very close together but are often looking at different types of tools to measure database performance. A common thing that I hear from a database side is that queries might get thrown over the wall. And they're just left with a little bit of extra work and the database administrator side. And what PMM allows you to do is to highlight the differences and maybe offer some recommendations towards indexes, or some other query tuning opportunity, and share that back with the development team. And what that enables you to do is to make modifications in production. And if you're, if you're deploying this to multiple different environments, you can also use them in a pre-production environment, you could be having this conversation and while it's still in dev and staging it 

**Matt Yonkovit**  
A lot of this is extensible, right? So I've been digging more and more into PMM. And so dashboards you see are the custom dashboards that I built myself. This is all you know, you are capable of building dashboards, how you want to present the data. And so that's an important thing for you to understand is just because out of the box, it might not have the graphs in the right way that you want the right colors, it might not have the right data, even maybe you find some things more valuable than others. It's really extensible, you can write your own exporters' because you know, if you've written things for Grafana or Prometheus, it's fairly straightforward, you're going to be able to do things very quickly.

And staying on that theme, I like that with the extensibility. There are two main ways you can take an existing PMM deployment and make yourself even more productive. For example, if you already have MySQL, or Postgres deployed, you can use what we call custom queries. And what that lets you do if you can write a select statement to fetch a metric out of your database, so you can turn that into a series that you can then plot on a graph.

So is that gonna just plot every row that's returned? 

**Michael Coburn**  
Well, it depends on how you write it. So you could be writing something that's unique about your data set that Percona is never going to know. For example, you could be counting different types of users that might be logged in. So the answer to a select query against the user table saying, or how many admins are online right now? or How many?

**Matt Yonkovit**  
So I'm gonna put them on the spot? Can you do that? With the database? We've got to run right. Now I'll even let you switch to MySQL because I know you're more comfortable with MySQL, do you think that you could do something like, I don't know, let's count the number of comments that have been entered into our chat system in this workload, I think we can do that, oh, I think we can, we're gonna do some live like extensibility stuff here with PMM, which is great. So let's go ahead and let's just jump back over to the screen showing this and just to show you vacuum finished. So obviously, all you know, traffic went back to where you would expect it. We also have the capability, like I mentioned, to drop indexes, built rebuilt, materialized views that are running, we also can deploy schema changes. So we play with that one with MySQL in a second. But we wanted to test the difference between different data types. And so we can test and see visually what happens when you use a VAR char versus an int as a primary key, which we all know there's a lot of performance impact there. So we'll show you how much after Michael shows us how to make some extensibility changes now he's going to start to click the button so I'm going to flip over to the machine and so you can watch it. Watch him flip, right this is where he's gonna switch to MySQL now. Well, let's reset the Postgres first so okay, red button what you tell everyone not to hit I just hit the red button. 

**Michael Coburn**  
And you know what's amazing is how many times FTP but not to touch it. And what did they do? They touch it, they touch it? 

**Matt Yonkovit**  
Yeah, Peter touched computers like oola. What does this do? What does this dude do right here? And so you know, what that does is that full stops all of the workload, just so everybody's aware, it, it totally stops everything and resets it all. So right now, you can't see on the screen behind us. But we have the log for the controller out, and it has set everything in MySQL. And we're inside load functions. We've loaded actors in all the titles. So that way, when we generate workload, we're not searching for a title or something, we have a list. And then we randomly select actors or directors or other things. So all of this is based on the Internet Database, all open data that you can go get and play with yourself. This is also all on GitHub. So if you want to replicate what we're doing, you can do it as well. It's on my GitHub. And I'll leave a comment with that in the comments, so I'll just put the link. So, Michael, you're now on MySQL, and I'm going to spin this, I'm going to spin some dials here, I'm going to give us some workload. Because I like to do spinny. Things like that make master we're gonna also add some of this, the insert, update, delete workload here is also where most of the comments and chat occur. So there's that. So we can't see your shell. So I don't know if you wanted to share that. You're just sharing your no PMM. Now, so why don't you share your whole? That's probably safer, share it all. He's going to share everything.

**Michael Coburn**  
Yeah, we go to your screen.

**Matt Yonkovit**  
Okay. to get back to where you want to go. And Alright, so here he is, here's his shell. Hopefully, he doesn't type in his password or anything that he doesn't want you to see him. But yeah, let's go ahead. And let's, let's take a look at that show. Okay.

**Michael Coburn**  
All right. So we're talking about custom queries. And what that really means is, if you can read a select statement, you can start to visualize some data. Where are these files located, they're under quite a lengthy path under user, local Percona. And then under here, we've got other products often that are installed, you'll be looking for the PMM to the directory, and then I believe it's under collectors, that's easier to see. And we want to do custom queries. I'll talk about the textbook collectors in just a moment. But custom queries are where we want to start. In our case, just checking, we've switched over to MySQL. So let's go there.

Okay, we're almost done. Look, we're already quite deep, about six levels. And I'll speak quickly about this, we've got three different resolution levels, it really means how often you want to collect the kind of data that you're interested in. So high resolution will generally get it for you every second low resolution, we'll get it every 60 seconds. And you might want to do that because the data is changing frequently. So collect more, but there's a cost usually associated with queries, or maybe you don't want to overload your system. So let's go into the high one because we just want to have fun here. In here, you'll notice we've already got a couple of different examples. We're going to modify an existing example in the queries mysqld. Oh, okay. And I'm the vim guy. I don't know about you, Matt. Are you? Yeah

I'm sure that that killed some people. Oh, yes. So you didn't have permission, I did not write. Got the password right? The first time. Good, good. It's a big day for me, right?

**Matt Yonkovit**  
The good news is this box gets wiped after this conference, we get to reset. So if you accidentally do that finger, that ultra-secret password we used here.

**Michael Coburn**  
So what I'm going to show here, we're going to keep this simple. And I'm just cleaning up an existing example. What I want to be able to demonstrate is we're going to take a select statement, and we're going to run it and it's going to return a metric series and a label. Anytime you want to have a query run, you probably want at least two of those fields, one of the metric series is the actual number that you want to be able to plot. So I've shown where we will be editing, I'm going to jump out of here and I'm going to get into the MySQL instance, unless you know off the top of your head, what the schema is. Could we write it without even looking at the database? How brave is that? Maybe that's to

**Matt Yonkovit**  
show people what you're going to do. It just makes it easier for posterity’s sake, because this will live on the internet, as you all know, things on YouTube live on youtube forever, because they never get deleted. And so in 1000 years, when aliens discover the remnants of human civilization, they'll find your video and know how to do this. You will live in infamy forever.

**Michael Coburn**  
So let's first let's take a look at what tables we have in here.

**Matt Yonkovit**  
And so you’re going to want to use the user comments table.

**Michael Coburn**  
So here we go. So we've got the option of using a few different types of labels out of here. And I think we're gonna want to look at what did what was the challenge

**Matt Yonkovit**  
Let's, let's, let's count the current active comments that are out there. So, we're going to just say like, hey, at this data point, this point in time, how many comments? Right? 

**Michael Coburn**  
Well, we're just going to count the Tables then if I'm not mistaken, I don't see yes. So you're going to have to table and give it a time. 

**Matt Yonkovit**  
So we're gonna make it super easy. I'm not really challenging you to wait until the next challenge, which was super challenging, I'm sure.

**Michael Coburn**  
Already you can see I'm challenged on getting my we're not making any typos here. But the table name back in, we'll just get a real quick count of how many rows are in this table? Well, it's quite big. So we've got about 4 million rows in this table. And if I'm not mistaken, our workload will be modifying this up and down, 

**Matt Yonkovit**  
ups deletes, right. So it's probably overall, as this runs, it's going to get bigger and bigger. Just like your data. Your data probably never gets smaller.

**Michael Coburn**  
Look at that. So I just ran the Select a couple of times, and I already have some differences there. So this is going to be a really good place for us to start to be able to demonstrate this

**Matt Yonkovit**  
right? You should see it go up to the right. You know, because even though it's deleting, it's only deleting comments that were in the last five minutes because somebody posted something they go, who I really shouldn't post that, right? So I'm gonna go ahead and delete it

**Michael Coburn**  
exactly right.

**Matt Yonkovit**  
So the five-minute regret rule, if you will.

**Michael Coburn**  
So with that information, what we've done is we've quickly composed a select statement, we'd encourage you, obviously to make it more complex, depending on your needs. But we'll start with a count of the number of rows in a table. I'm already in the directory where the high resolution has been now, now that I noticed it takes around anywhere from two to five seconds. running it every second may not be a great idea. I'm going to back out here. Yeah, because I don't want to swamp the server, right? Yeah. Do you want to be sure that I don't cause an outage? Maybe? Or

**Matt Yonkovit**  
That's true. That's true. Is there anything we could do to speed that up? 

**Michael Coburn**  
Well, I guess we could have maybe an index.

**Matt Yonkovit**  
What are we missing?

**Michael Coburn**  
Well, in this case, the primary key is already defined on comment ID and it is an integer value. I'm not sure what else we could do here really to make this one much quicker. Would you have any ideas?

**Matt Yonkovit**  
I'm asking you as the expert to stray throwback on me, but I invited him I'm the facilitator, I'm the host. So I'm supposed to make him look good or bad. Unit depending on**Michael Coburn** the mood?

**Michael Coburn**  
Well, I'll leave that for something we can debate a little bit later. Okay, what I'm going to do is I'm going to move it into a lower resolution environment, because I probably exaggerated with causing an outage, what would end up happening is you'd have one query, maybe stepping on the next first one wouldn't finish it would be running additional?

**Matt Yonkovit**  
Well, it would basically cause a pile-up, right? Because you would always have it and I think your cue list of those will just get longer and longer and longer. That's correct. And so you would see the rest of your performance. So there you go.

**Michael Coburn**  
So we'll come back into the low resolution.

**Matt Yonkovit**  
low resolution every minute. Yeah, we

**Michael Coburn**  
may play it a little bit. A little more aggressive here on the medium side. 

**Matt Yonkovit**  
oh, crank that one up.

**Michael Coburn**  
Let's get this out of the way. I can't see. There we go. So okay, so we're looking at the crease. Oh, I'm sorry, I need to be doing this as root. Get it? Right. Okay, so how does this work, there's a special format, it's a YAML file. And easiest if you just use the existing example to get you started. So what I've done is I've just removed the leading comment and markers, the hash symbols, the very first component is what the start of your metric series is going to be named. So in this case, I'm not going to use my scope performance schema, I'm going to remove the performance schema component. And I'm going to put it in, oh, I don't know, OSS demo, it can be any text string. What this is going to illustrate is that in just a moment, you'll be able to go into PMM and discover this metric series. And it's going to start in our case, my school OSS demo, right? Make sense? Okay, so I've started that. And then in the query block, you could imagine I'm going to remove the existing one. And I'll paste in quickly. The select that I had written already from the given table. And then I'm actually going to fix this just real quick, I want to give it an alias. So it's a little more complete. Count CNT. And then down here, you want to give it what is the matching column that's coming out of it? It will be called CNT.

**Matt Yonkovit**  
So would it be beneficial in this case, to use a more descriptive thing? Or does it matter at all? Like, comment count, or, because if you have a lot of cnts you might be counting three, four different things might be better to differentiate that way.

**Michael Coburn**  
That's a really good point. That's a really good point. Because what's going to happen here, it's a series of appending names together, right? So in this case, if I just left it cnt, the full metric series would be called my school OSS demo cnt, that you make you raise a good point that maybe not very, it's not very self-descriptive, so I wouldn't know what I'm counting. That's right. That's right. So let's call that comment cnt. And we'll fix it up down here. Oops, down to for comment cnt. Okay, great. You've got one last decision point to make, you can choose to use either a gauge or you can use a counter. And this is an important determination because it impacts Prometheus how the database system is going to be able to plot your number. In our case, this count we know can go up or come down. So those gauges are things like temperature, temperatures go up and come down. trade that off with a counter a counter is a number that's always incrementing. So if you look in MySQL, for example, How many users have connected over time, that will be a number that just keeps growing over, over and over? So at least the different formulas that you can use on your dashboards?

**Matt Yonkovit**  
So this could go down in theory, so it could go up and down? Most likely, it will always go up. But is it quicker?

**Michael Coburn**  
Yeah. So we'll provide for that just by giving it a gauge. And then the last part is this description. I'm just going to leave it alone. For now. Really, all that it does is it provides a helper for when you want to look directly at the output of this exporter. It's kind of a low-level thing that you don't need, it doesn't impact the performance. 

**Matt Yonkovit**  
Fair enough. Fair enough. Okay. 

**Michael Coburn**  
So that's it. So you've made your modification to this file.

**Matt Yonkovit**  
So how do I, how do I get it to work now, start collecting to just pick it up?

**Michael Coburn**  
You simply just save your file and exit. And automatically the PMM client is going to start using this file that has new entries in it and start fetching this metric series for us.

**Matt Yonkovit**  
So it should be fetching it did medium mediums, how often?

**Michael Coburn**  
I believe it's gonna be every five seconds, 

**Matt Yonkovit**  
Every five seconds, this is going to be collected. So how do I get that? 

**Michael Coburn**  
Okay, well, let's validate if we've done everything correctly. 

**Matt Yonkovit**  
Yes, because**Michael Coburn** Sometimes, we need validation.

**Michael Coburn**  
And it's a live stream. So let's just make sure that we did everything correctly, we have this kind of hidden ad, there is a dashboard called Advanced data exploration. And what I'm gonna do is I'm just going to pop this in another tab. And what it allows you to do is to explore the different metrics series that are in your database system. So you'll find many of the common MySQL that we use on different dashboards. In our case, I'm going to start searching for a MySQL OSS demo. I'm crossing my fingers that it's going to be there. See if we can find it here.

**Matt Yonkovit**  
I don't know, Michael, then crossing your fingers apart?

**Michael Coburn**  
Oh, it's not there yet. It's not there yet. Well, all is not lost. What do you do, you go to the logs. That's the first place. 

**Matt Yonkovit**  
Fair enough, show us the logs, take us to the log files.

**Michael Coburn**  
Now the beautiful thing about the PMM client, it's available as a Debian package or as an RPM, or you can download and use the tar files. And of course, like all of Percona software, it's open-source free to use, so you have access to the source code. happily take your prs, if you want to go deep and send us some fixes. The point I'm trying to make is that it's also integrated with system D. So in our case here, I'll be able to look using journal control to see what's going on with this client. CTL I want to describe it as the unit called PMM. Agent. Okay, hit enter here. Oops, not if I spell journal control incorrectly, though. Oh, my gosh. No. Okay, journal CTL. There's an L.

**Matt Yonkovit**  
That would make a big difference. 

**Michael Coburn**  
certainly wouldn't work. Get the password, right. Okay, there we go. Oh, here we go. What do we get?

Make this a bit smaller here?

**Matt Yonkovit**  
Oh, my gosh, it's so tiny. It's so tiny, too tiny. Yeah, well, I think it's fine for those watching at home. But it is kind of, so what are you looking for?

**Michael Coburn**  
So what I'm looking for really any errors here? I'll describe quickly what I'm seeing. And then we'll see if we can decipher if there are any problems coming back. You're gonna get two kinds of errors logged in here, or sorry, not even necessarily errors. We've got the two different kinds of exporters running. Generally, you've got an exporter that's connecting to the database service. And that's called MySQL, the exporter. Okay. Okay, that gets you anything MySQL  related, Okay, sounds like the other one. Depending on how you've orchestrated it. You'll either be fetching your query logs from the slow query log, or you'll be getting them for performance schema. Hmm. Okay. Okay. And what that enables is, it'll provide a view of which are the slowest queries running in your environment. And that's what you see on the analytics dashboard.

**Matt Yonkovit**  
And when we talk about Postgres, that's going to come out of either PG statement or the new PG, PG, stat monitor PG. So either one of those, so similar locations, just different sides for each of the databases.

**Michael Coburn**  
Okay, so they come with two different kinds of logging formats. These earlier ones are up here, where they're showing the level info database version that's coming from the mice with the exporter. Generally, MySQL, the exporter, works quite well. It's not very chatty unless there are any errors. There's only ever this repeating what version where you're running. Okay? Okay, the slow query or the performance schema source also is relatively low volume, but what I like about it is it'll show me status. So in this case, it's showing me how many buckets of data had to be sent up, back up to the PMM server. Okay, so you're generally looking for numbers that aren't zero. We want to make sure in our case, we've got 15 or 17 buckets. That makes sense. So this is the healthy-looking system. What I'm looking for is actually something that isn't sticking to this 15 or 17 buckets are the same data-based version in here, I'm going back quickly here in the logs. And I'm looking for anything that says I'm unable to connect to the database and run a select statement that is an account. Let's try one more time. I'll do it with the dash x key. So I'm at the bottom.

**Matt Yonkovit**  
When we'll get to your question in a second.

**Michael Coburn**  
Oh, Matt, you're not gonna believe this. I don't see what the error log is for. For this failure here.

**Matt Yonkovit**  
How do you know it failed?

**Michael Coburn**  
Well, how do I know it failed? Let's try searching one more time and crossing our fingers. Maybe everybody at home can cross your fingers for me as well. Oh, man. Okay. Yeah, so my,

**Matt Yonkovit**  
it's okay. I can be within six feet of him. He has the green bracelet on to green bracelets on. So he wants hugs.

**Michael Coburn**  
Oh, Matt, I've got some sad news. I don't immediately see why we're not fetching back this dataset. Hmm.

**Matt Yonkovit**  
Did it, save it properly? Check maybe the permissions on it. I mean, maybe you exited without saving it. So it didn't get the medium. Yours is something that could be running. Or that it's not running those. Those things do we need to restart anything we refresh the browser,

**Michael Coburn**  
when in doubt, refresh, restart. I'll just check the logs one more time here and see if we see anything. Okay, we can see that things did get restarted, we can show that it's running on the Newport with a bunch of other Victoria metrics data coming back. And let's check one last time. And maybe if we don't have it working here, we'll move on to another example. I'll refresh the dashboard.

**Matt Yonkovit**  
But this just means that you have to come back and do a video where it actually works. That's right. That's right. Because I can't have like a video that goes halfway through and like**Michael Coburn** like, hear everybody do this. And it doesn't work. 

**Michael Coburn**  
I mean, what if the aliens are looking at it like you were speaking, right? 

**Matt Yonkovit**  
No, it needs to be here for posterity’s sake.

**Michael Coburn**  
So here we go. Alright, so MySQL, OSS? breaking my heart. It's just not there. I owe it to him. 

**Matt Yonkovit**  
Where is the data stored?

**Michael Coburn**  
In this case, it's stored in a system called Victoria metrics, which is a fork of Prometheus.

**Matt Yonkovit**  
Okay. And can you go to Victoria metrics and search from there?

**Michael Coburn**  
We used to be able to do that the paths changed when we did a migration from Prometheus to Victoria metrics. But let's give that a try. Let's see what we can do off of that. I'll take the URL, put it in a new tab here. And we'll call it Prometheus. Oops.

**Matt Yonkovit**  
one of the other things that I know you can do within the dashboards, right is you can do a query inspector. So you can look through that.

**Michael Coburn**  
Oh, you're right, you're right, we do have the Explore function within use this button up here, I think it is that explorer on my screen.

**Matt Yonkovit**  
And Michael has 17 minutes of battery life left before his battery dies. You know,

**Michael Coburn**  
here we go. So we'll explore. This is a great little, little way that you can just jump right into looking at not only your metric data, but also lets you explore the clickhouse data.

**Matt Yonkovit**  
Yes, yeah, it's it provides a nice, nice interface for that. So are you going to look under the metrics that are you going to look under one of the other ones?

**Michael Coburn**  
Yeah, I'm just going to show the different options here. The default is going to be metrics. That means Victoria metrics, okay? Okay. So that means anything you start putting in is going to be reflected from your metric series, your time series. So if I start putting in MySQL, it's already gonna do a look ahead and find any matching metric series names. Many of these we're using on different dashboards to highlight and draw different graphs. But as soon as I get a little more specific, and I put an OSS, yeah, it's showing me that it's not in the Victoria metrics database. There's a disconnect between the client!

**Matt Yonkovit**  
so what's going to happen is Michael is going to go off. And you know, when he gets it right, before the end of the day, he's going to come back and he'll record a video and we'll post the supplemental here because that's what we do here as we close the loop. So he got me interested in a feature that I hadn't done because I hadn't done the customized cualquiera yet. So I wanted to see how to do them. And so you know, he showed me a little bit there. So we have been running MySQL workload now for a while. So, Mr. Michael, you want to go ahead and show us one more thing before we go and answer some questions. So we mentioned a little bit earlier than we are doing some schema changes and looking at potential code deployments and things. So if you recall, I mentioned here, these buttons are actually some fun buttons. Well, fun in the sense that we've written a lot about this over the years about the differences between an integer and varchar performance. So you can see that, what do we got, what's your current queries per the second count? Oops. So so we're at about 4400, we can make that go higher if we wanted, but we'll just use the 4400. For the time’s sake, what we're going to do is we're going to flip on, and we're going to change everything over to use a varchar primary key just on one of the tables. And as opposed to an integer. So that's what that's going to do. So this, click right here, you can't see it on the screen behind us. But it actually wrote to the logs that, hey, I'm making this change to change this particular table to be forced to use a UID or something similar. And so what we're going to see in Michael's computer that hopefully won't die, is we're going to see the drop in performance.

**Michael Coburn**  
And that's a really good point you raised about the bar chart change here, we're not changing the data itself, it's still going to be a number, but it's going to be evaluated as a string. And why this is a little significant is that there are many databases. Clients or frameworks really, as they work with a database, like to choose clever primary keys. A common one is a 36 bytes UID value, right? guaranteed uniqueness. You know, from a perspective of usefulness, it's very, very helpful. But there are two main problems with that one, it's a string, and we're going to show you the impact of it. And two, it's quite large. Right? Right. So 36 bytes. One of the unique characteristics of MySQL and InnoDB is that every single primary key is part of all secondary keys. So that means the wider your primary key, every additional secondary is going to be that much wider. And that leads to increased memory and more disk activity. So you generally want to keep your primary keys as small as possible.

**Matt Yonkovit**  
Yeah, we've seen a big drop in the queries per second and the response time, but that was specifically because of 

**Michael Coburn**  
Oh, I just lost it.

**Matt Yonkovit**  
Oh, my gosh, he lost it. Oh, dear. Oh, well, so we're going to his, his, he didn't charge his battery.

**Michael Coburn**  
And yes, yeah, I left my charger, and I left my charge 

**Matt Yonkovit**  
so so we can look at the graphs behind us a little bit. It's a little bit harder to see. But we should be able to zoom in once we get these things going. So Oh, yeah, so the time here is at the right time, okay. So you can see here, I'm going to zoom this in so we can see. So these are our queries per second. So obviously, what we did here, this annotation that you see here, if you hovered over it, it would actually show you that the primary key changed, or the start to happen. So we have, it's actually done. So the log does show that it's done. So we're going to see what that query per second ends up with. Now, again, this is the exact same workload, this is the exact same thing, except for just the varchar primary key versus the integer. Right, so a very small change. So imagine if you're going to go deploy new code, and you want to test version A versus version B, because let's be honest, a lot of the problems we see from our, in our support or managed service are because people didn't design the database, right? They didn't think about it, they just chose whatever was the default. And that leads to a lot of those UID type situations. But if you have something that you're going to deploy new code, you can run a test before and after. And you can compare those and that's what we want to see. And so in this case, you see a bit of rebound here, right? So these are in one-minute buckets. But you see this up a little bit. So let's give it one more minute here. And let's see, because it should stabilize. But remember, this particular workload was about 4500 queries a second. And so we can come back. And now we got another data point here as well. So let's go ahead and let's go back to the general. So these, these graphs right here, which you can read the numbers there should be big enough. You can see that this is the peak. Over the last 15 minutes we peaked at 4512 queries a second. Here we have the average is 3091. And you can see right now we're running 421. So This particular thing was over a 5x decrease in performance just by making that small change. Now, if we alter the query workload a bit, add in a little bit more aggregates, add in some inserts, updates, deletes. And we throw more threads, what we'll see is what we were getting yesterday when we were doing this 30x difference in performance, right? So it was massive, we were hitting 16 17,000 queries per second, you make that one small change, and all of a sudden, we're down to 500 queries per second. So anyway, that's what we have for you today. Wayne wanted to know if we're going to be working on a client for the ARM architecture. And that's something that we have talked about, I don't know the current status of it. I don't know if anyone is online, on the live stream here from the PMM Team. You know, be happy to get back to you on that Wayne on Discord. If that's helpful. I don't see any other questions. But if you do have other questions, we're here at the floor show it is still pretty early. So no, not many people have shown up. The show floor doesn't open for another hour or so. So we're still a little alone. There's that moving some things around, adjusting some things here. But it's just been awesome for most of the morning. So what do we get? We get another one here. Let's see. Wayne says Cool, thanks. So I'll check on Discord. Well, we'll get back to them offline. And Michael promises you that he will get this fixed today. As soon as he gets a plug for exactly that. You should have waited until your laptop died to say, Oh, I can't do anything else. Oh, it'll look way better. I'm just saying next time try that. But everyone, thank you for joining. If you've watched this live wonderful, if you're going to watch this later, also wonderful. If you have suggestions on what you'd like to see us show you in PMM if you'd like to come on and show us some cool things you've done in PMM come next time, and you know we'll dig into it. And for you know for all of us. Thank you for coming and we're Matt and Michael, and we're live from OSS, and we'll see you next time.

**Michael Coburn**  
Thanks, everyone.



![Percona MeetUp for PMM Sept 2021](events/percona-meetup/cover-pmm-1920.jpg)

Matt Yonkovit, The HOSS at Percona, will host the Percona Monitoring and Management (PMM) from the Open Source Summit in Seattle. We will talk about database monitoring, discuss PMM in detail and also do a tour of the Summit during a one hour live stream with Michael Coburn, Principal Architect at Percona. You can ask questions in-person or virtually and get help.

Join us for an hour MeetUp for PMM

* Day: Wednesday Sept 29th, 2021 at 11:00am EDT (5:00 pm CEST or 8:30 pm IST)

* Live streaming on [YouTube](https://www.youtube.com/watch?v=2WSsmhzsVXg) and [Twitch](https://www.twitch.tv/perconacommunity)

* Live chatting on [Discord](http://per.co.na/discord)

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=MGlsMTZwMDNrYTYyMTE4OTgzYjQ2cHFkbW4gY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

## Agenda 

This will be an extraordinary one-hour Live Broadcast MeetUp from the OSS Summit, to talk about open source databases, observability and monitoring MySQL, MongoDB, PostgreSQL with PMM, enhancing, customizing PMM and Grafana, and finding those tough database problems. Our experts Matt Yonkovit and Michael Coburn will make a PMM Demo and answer all your questions in-person or virtually.

**The MeetUp for PMM is recommended for:**

* Everyone who is managing and monitoring MySQL, MongoDB, and PostgreSQL performance.
* Everyone who needs time-based analysis data. 
* Users of PMM.
* Students.
* Experts, Engineers, Developers.
* Each person who is thinking about work with databases and big data.
* Everyone Interested in PMM. 

**Go ahead and come with your friends!**

Subscribe to our channels to get informed of all upcoming MeetUps.

Invite your friends to this MeetUp by sharing this page.
