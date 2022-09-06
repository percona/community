---
title: "Setting up failover via a replica for PostgreSQL - Percona Community PostgreSQL Live Stream & Chat - June, 3rd"
description: "Listen out to this Percona Community Live Stream and learn more about Setting up failover via a replica for PostgreSQL"
draft: false
images:
  - events/streams-pg/PG-Stream-Week-5-cover.jpg
date: "2022-06-03"
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---

![Percona Community PostgreSQL Live Stream & Chat - June 3rd](events/streams-pg/PG-Stream-Week-5-cover.jpg)

This is part of our bi-weekly Percona Community Live Stream. Our experts, Charly and Matt talk more about database failure and setting up a failover on PostgreSQL.


## Video

{{% youtube youtube_id="DhLg4tMvHuI" %}}{{% /youtube %}}

## Transcript


**Matt Yonkovit**  
Hello Hello everyone how are you doing today? Welcome to another exciting episode of Percona's bi-weekly Postgres live stream. I am Matt Yonkovit, the head of open source strategy here at Percona. With Charly, our esteemed Postgres Tech Lead, Charly, how are you today?

**Charly Batista**  
Hey, Matt, I'm doing great. All right, uh, he's starting to get a little bit chilly these days, but

**Matt Yonkovit**  
it's getting cold there. It's not supposed to be cold there. I know. I know.

**Charly Batista**  
This is what they say to my wife. Yeah. Right. So we're in Brazil. But last week, it got like 456 Celsius degrees here. So weird times.

**Matt Yonkovit**  
Yeah. So So, Charly is wearing the official hat of Percona live. Now, I have to ask Charly, did you earn that hat?

**Charly Batista**  
Of course, I did. I had two presentations, one tutorial, and a lot of meetings on Percona live, so I deserve this one.

**Matt Yonkovit**  
You deserve that one. So but I thought you clicked on the buttons. That's what I'm asking.

**Charly Batista**  
Oh, also, I got all of them. And I was one of I was the holder of one of the buttons. And I made it quite hard for people to get one because I took some Brazilian Kinshasa it's kind of a ramp from Brazil. Okay, so if they wanted to get one of my buttons they would have to pay the price. It was a shock to the class.

**Matt Yonkovit**  
Wow. So I don't know if anybody's watching who did shots with Charly. But shots with Charly earned you a button which earned you one step closer to the magical. Exactly. Yes. Yes. So, um, so how was Percona live? Because I didn't go because I had COVID Damn you.

**Charly Batista**  
Well, on how I'm feeling, by the way, oh, I'm,

**Matt Yonkovit**  
I'm mostly better. Like, it's weird. Since COVID hit, there are one or two days where I'll wake up in my head, we'll just be like, underwater. It'll be like broccoli foggy for like several hours. But other than that, it's fine. like, it's been a while since I had a cough or anything going on there. So I think it's, it's pretty good. but, yeah, so I'm good. But I missed it all. So you have to tell me, how was it?

**Charly Batista**  
Not that I thought it was amazing. No, coming back, after two years without we're gonna live or at least the without Percona live on site. Right. So we had two remote ones last year. So now having all the experience everybody there and so talking to the cast when talking to other developers talking to the people from the community to the really amazing. So the quality of the talks, these years is pretty high, very high. I went for a few of them. And I really enjoy some of them. I got a lot of questions. Some people, they're amazing things. Like I went to a talk, where the presenter was showing the improvements they are doing for the storage subsystem on Postgres. Right. So, and it was really good. It was really interesting. A lot of really, really good topics. And it's so it was amazing to see people that we didn't see for a long time. So I met Hi, Missy come from a fanny pack. Oh, yeah, yeah, yeah. So I didn't see him for ages. And other amazing people like his vehicle was the one that had my shots. One of the shots. Of course, you got Yeah. Other people say they saw all of Kenya and a lot of other people. They've been there. So it's, it was really amazing to see all these faces that we don't we didn't see for a long time. Right. So it was a great experience really good.

**Matt Yonkovit**  
Well, just a week before Postgres fifteens beta was announced. And I know there was a talk at least one time, it might have been a couple on Postgres 15 features. So that's one of the things that I missed that I really wanted to go to. I wanted to chat with Brian cats a little bit about some of the stuff that he the community has been doing there. And I know his talk was on that. But I didn't get a chance to catch up there. I was so looking forward to diving into some of the Postgres 15 stuff.

**Charly Batista**  
Yeah, it was unfortunate for you, right, but the COVID thing, so yeah, that's, that's life. Sometimes it happens, right?

**Matt Yonkovit**  
So yes, yes. But the good news is, I'm going to be all over the world in the next few weeks. So next weekend at the southeast Linux Fest in Charlotte, then I'm off to Austin again, so I get to go to Austin even though I missed Austin, for the week for the OSS Summit, I'm out to Amsterdam for DevOps days, Amsterdam, and then gonna try and make it over to the data and Kubernetes there's a London meetup as well. So gonna be bouncing around here a little bit. So if people out there want to get a coffee or something, or in one of the cities that I'm going to be around, let me know, I'd be happy to sit down and love to hear what you, you all are doing. But enough banter because we're not actually here just to talk about Percona live and you know where I'm traveling to. And what sort of interesting things I'm doing. We're here to talk about replication, Postgres. So. So we've got a couple of things going on here. that I wanted to bring up. So number one, we're going to be moving this stream to Thursdays. There were enough of you that said, Fridays, we love you guys. We love that we love Charly, we love Chino, but Friday night at eight o'clock, when it is between my partner, my significant other, or Charly and I got to spend Friday evening with that. So, because for many of you in Europe, or an AIPAC, this is not a great time, we're going to be moving this to Thursdays, and we're gonna go two hours earlier. So that's something to keep in mind go ahead and check that out, I'm just getting a note that people can't see a couple of people can't see the video. So I gotta tell them, like, they're having problems getting pinged on the side here going like, it's not starting but I do see that we did get a comment already. But anyway, so we're gonna move this two hours earlier, and it's gonna be out Thursdays, starting in two weeks. The other thing is because this was such a big topic and this relates to the question, the question that came in was, how are we going to be doing failover streaming, replication, or logical, we decided to break this into two. So this week, we are focused exclusively just on the kind of standard tried and true simple replication. Whereas next week, we're going to focus for two weeks, we're going to focus on Patrone. And so we're going to be kind of flipping this, were in a couple of weeks, we were going to start looking at a couple of different topics looking at migrating between servers.
Instead, we're going to be looking at Patrone in two weeks and so hello from Brazil. Yes. Hello, Brazil. That's awesome. Charly's in Brazil; here in Brazil, I have not, but PG Brazil's coming up. So hopefully, you all can say hello to one another. But, so this will be standard replication, we're going to be setting up replication from the start getting it working, figuring out how to get it set up and going. And then we might be able to do some manual kind of interactions, but then we'll be working on the automation in two weeks.

**Charly Batista**  
Yeah, the idea for today is to set up the foundations, right, so we're going to put the foundations here for what we were going to use. We're for today we're focusing on tremor applications, right? So we try to break it and make things work again. So I hope we get a couple of troubles today. So we can go there and try to fix those things. And one thing that I want to show today, and to make people try to understand a bit more how it really works under the root, and some options that we can use for external replication. Because there is some challenges when your databases start growing, for example, we have a customer that they have a few terabytes of data on their database. And when they were trying to set up a replica, the backup for the replica was timing out. The backup was being done, but that's because they were not using log shipping because they are not saving the logs. When they were the cup finished. It was not able to start replication. So they tried for a couple of weeks and they were not able to fix the problem. So how do we fix that problem using stream replication? Are you Are we able to, in that case, they had two options. They could set up the locking sheet Right, so you save the locks. And the problem is to do that they had to shut down the database. So in that, in that case shutting down, the database was not an option. Is there any way that we can do the configuration from the client referral from the applicant, to tell to the primary blue, done, and remove the logs?
Because they still need those log files. When I say login, I'm talking about the wildfires. Right. So don't remove the wildfires, because well, we are not archiving them. That was a problem that they had, we are not archiving the Demo files. So but they still need to use those files and finish the replication. Right. So is there a way an easy way to solve the problem? Can we do something? Do we need to, for example, set up a cron job to do an arcing from time to time? What can we do to solve this kind of problem, right? And when we have a small database, that's okay. But like when you have like a gigantic database and a huge amount of data, that might be a problem that like, when you start scaling things, that might be a problem. And the idea for today is okay, let's go there. Let's start a synchronous Eastern replication. And we have time; let's go for synchronous replication because people have a lot of doubts about that how that works. Some assumptions on synchronous replication are also a problem. Because a lot of companies want to use sync synchronous replication, but they still want to keep the performance. Is it possible to have synchronous replication without losing too much performance? Right, so the idea for today is, okay, let's start diving into those things. Let's see how things go. And then for the next session, we do the whole automation using something like Petroni and make everything work like to start using our highly available classroom clusters. Does that make sense?

**Matt Yonkovit**  
make sense to me? I've been troubleshooting a couple of people's questions who have come in directly. So so so yeah, so I think setting that that basic stuff up, ensuring that you are not losing any data, ensuring that you're getting the wall files copied over and things are not going missing, or Mia, those are all really important topics. So yeah, let's dive into it.

**Charly Batista**  
Okay, let's share my screen here; just set

**Matt Yonkovit**  
the screen.

**Charly Batista**  
So you're able to see my screen,

**Matt Yonkovit**  
we are able to see your screen,

**Charly Batista**  
or hey, so I have cue servers here. Where this one is the primary. And they have another server here that we have Postgres installed. And we want to make this replica for the other one. So do we have a load on the server on the primary one? No,

**Matt Yonkovit**  
there is some load, I can generate load. It'll just take me a second to log in and do it. Yeah, that's

**Charly Batista**  
fine. I also want to take some time to do cleanup here. So I'm going to use

**Charly Batista**  
Screen bash.

**Charly Batista**  
SPG HD.

**Matt Yonkovit**  
So you see me turn in what do you see me turn I'm typing to someone. So just realize that I am not ignoring you all. And typically I want to look at the camera. But yeah, because the screen that I can do shell and everything is over here as opposed to over here.

**Charly Batista**  
Yeah, I also have the same problem from time to move here or here because yeah, those two different screams

**Matt Yonkovit**  
first-world problems. Everyone, right, so where's your

**Charly Batista**  
where's your stuff? RK I should have GIS data here. That's our data. This is as its implies Charly Spracklin even though it has my name is Matt.

**Matt Yonkovit**  
No, this is Charly's replica server. I am. Hey. Oh, people are asking if can you increase the font size a little bit. Well, definitely, yeah. Better. Oh, that might be like yeah, I mean, that's pretty big. But if it gets to be good. Okay. Well, when is that good? Is that good for you? Is that better? We'll assume yes. Okay, hopefully, I'll respond in a second.

**Charly Batista**  
Yeah. So what we have here we have all now you just did a clone right? Just kidding. Yeah, I just did what you did. Yeah, you're cloning that box inside of this box. We have an exact copy.

**Matt Yonkovit**  
Yeah, just I just created an image from the disks and then just start it up as a new image.

**Charly Batista**  
So that's like and wipe out everything here. So

**Charly Batista**  
This is our data here. So we've mounted the mount point on this volume here. So the extra volume we've got. And if I remember correctly, we have a VAR lead VGS, not PG backrest, but also degrees as well.

**Charly Batista**  
This

**Charly Batista**  
13

**Charly Batista**  
And here we have Yeah, we have main that's pointing to data news. So what we're gonna do is we're gonna link mine

**Charly Batista**  
I run a query and

**Charly Batista**  
see the data all

**Charly Batista**  
replica, just two different ages. Rap.

**Charly Batista**  
Rap bleep comes slow, okay?

**Charly Batista**  
By the replica

**Charly Batista**  
main. Okay, we have and then shall our posters.

**Charly Batista**  
So what am I don't think what I'm doing here is I'm creating the Data folder, right? So here I have a Postgres with an empty data folder. We only have a football school system installed here, version 13. And in this box, we have another four screws amongst us that run down. So I can connect to this instance here.

**Charly Batista**  
Okay,

**Matt Yonkovit**  
by the way, I'm gonna just use a little bit of workload, I'm not going to overload you.

**Charly Batista**  
Yeah, no, it's just fun, just for us to have some some some data something there. So yeah, we don't need to; you have that huge amount of data for now.

**Matt Yonkovit**  
Yeah, this will be kinda light.

**Charly Batista**  
Okay. So

**Charly Batista**  
if we do SLI from PG, and stat replication, we're going to see that we have nothing here. So no rap because nobody is replication. So select

**Charly Batista**  
star from PG stat.

**Charly Batista**  
Subscriptions, we don't have any subscriptions.

**Charly Batista**  
Select the staff from each. Replication slots, replication slots. So,

**Charly Batista**  
yeah, we don't have anything here related to replication. Right. So this is just a standalone box. We have some loads.

**Matt Yonkovit**  
Should be a little bit right now. Okay, so now it just started. Yeah, it'd be like five or six connections that are doing some five or six users doing some stuff. So cool.

**Charly Batista**  
Yeah, I can see some activity here. Nice. So we have this box, and we want to build a replica from this box to that order. Other boxes. So first things first, I need to see what's my IP. The IP of this box? Is this one? Okay. So

**Charly Batista**  
and

**Charly Batista**  
on the other one, just make sure they're in the same network. Yeah, they are in the same network. No need to be able to connect. Yeah,

**Matt Yonkovit**  
now I did. Just so people are aware of these two boxes, I did set it up. So these are Amazon boxes. So by default, it's fairly locked down from a firewall perspective. So they can access each other via Postgres across the wire. I only opened up shell or SSH, and the Postgres and PMM ports. So, in case you were Restlet, trying to replicate this and you go in and you're like, Oh, I can't connect from one box to the next. It's probably that firewall issue.

**Charly Batista**  
No, we are using here and using the local IP right, so I'm just seeing if I am able to connect well. I'm, yeah, I'm able to connect from this box from Ottawa. Good, so far, so good, no problems at the moment. So I gonna check here, my PG hp.com To see if I have the replication allowed here. So I have the replication protocol and a user named replicator. They are allowed to use the readies replication protocol on the whole network here.

**Charly Batista**  
Alright, so

**Charly Batista**  
let's see how that goes. So looks like I have everything that I need. What we need to do now is to copy the data from the primary to the replica. They are the ways that we can use to do the copy. So we can do an old, old, poor man backup, let's put on his way. There from the primary to Africa, if we could, for example, is stopped the primary, we could do a cold copy. So like Brexit, what you teach here, you just started the database, and then you clone the one machine to another one. That's probably the fastest way directly to have a copy of the box that you have, right? The problem is, that the database needs to be stopped, and the box needs to be stopped for you to have a consistent copy from one box to another one, right? So we can also use our sink for example, and do the same, right? But those cold copies, have a problem that we need to stop our database to copy the data, right? And Postgres has its own tool to create the backup. That is the PG base backup. That's the tool that we're going to use here. And it has a lot of options. If I like running here, we've bash, bash, bash, help us a D here, we're going to see that we have a lot of options here. So some of them are pretty straightforward. For example, the hostname, this is the hostname that you're going to connect the faulty username, the password, so we can Bowser the same options as when we connect to the database using PS club. And we have otter, two options, they're not so straightforward. Let's pause on this one. Because we can tell the two what we wanted to do. For example, we can ask the tool to open a stream to the primary and copy the whole files. So while we're copying the data from the primary, we also want to be able to copy the wildfires. So when we finish the backup, we have both the data that we need. And we also have the world files that we might need to queue up and apply when you copy the data. Because remember, it's basically our sin, right? So it copies it does the PG base backup, it will do a checkpoint on the primary to ask the primary to go check or wait for the primary with checkpoints. When the primary does a checkpoint, we have a consistent point in time that we can apply to all files. Remember, the thing when we did the point-in-time recovery, we need to have a checkpoint. So from that checkpoint, we can tell the rest of his life, I want to apply up to this point or I want to follow it. So the PG base backup we wait for the primary to do a checkpoint and after that shut pointed to start copying the data. So until after that point, after the checkpoint, the date is consistent. If the database starts and there are no audit wall files to redo the data, we still have the data that is consistent. After that point up the checkpoint, everything else can be rolled back. The thing is we don't want rollback. We want to keep applying and then start replicating from the primary right. And this is what the two gonna do. Let's do it. Like it's it seems complicated but doing it's a lot easier to understand. Right. So the option that we tell the two that we want to keep copying is dash x and trying to See here, capital X, it's here. So without a tool key, we want to keep copying the data. So it will open to connection. So the primary is like queue replication connections. One is to copy the data, the replication, it's the backup itself. And another connection is to copy the WAR files, right? So let's start building here, what we want.

We want the hostname to be my IP, of this, this note. Just a second, we turn on the heater here, and it's quite a lot.

**Charly Batista**  
It runs off.

**Charly Batista**  
So

**Charly Batista**  
this is what I going to use

**Charly Batista**  
another user, remember that we configured the user replicator. So I need to make sure that the user exists. So create a user replicator. And it should have the privilege of replication. And I'm not sure if it's, this is the privilege name, we got to find some and the password. For this example, we're going to use 123. Well,

**Matt Yonkovit**  
no one, no one will ever guess that password.

**Charly Batista**  
Yeah, it's, it's very complicated. And luckily, the user sees, so I don't know how to use a replicator. And I got to encrypt the passwords.

**Charly Batista**  
Right? 3210. Now it's encrypted.

**Matt Yonkovit**  
Now it's the same same same as my luggage. Well,

**Charly Batista**  
same as your luggage, okay? So the username is a replicator. We're using the default port, which I gonna put here, capital W, so it will ask for us to type the password, right to force them to prompt the password. The first option, remember, we're going to tell you is the x. We want it to copy. And there are three or four methods to three options. You do have the methods that we can use. In our case, we're going to use the stream. So another option that we can tell, to PG base backup is to open or create a replication is launched. Remember the problem that I said, for that customer had terabytes of data? So these bash acts might help to solve the problem? What if the workload is so intensive, that it writes so much data on the primary that the replica is not able to cough the wildfires before the primary removes the wildfires? So we're gonna still have some missing wildfires here, right? So this is just part of the solution to solve the problem. So it will try to crop the will file in but we still might have a problem if our workload is so intensive, that the primary writes too fast. And the replica is not able to keep up with that load. And then we just lose the wildfires from time to time. So to solve the problem, we can tell look, I want you to use a replication that is locked. So replication is law is something that you will be created on the primary. And that tells the primary law, we have some clients, replicas, they are connecting here for the application and they're using these is the law. And they will tell us, that when we can remove the wall files, the replication is locked to prevent the primate we move all files until the replica tell the primary that it's saved remove that both fives those two options, the solve the problem that they just explained, when you have like super intensive writing workload, and that's right, too much more files. And sometimes you're removed before your rank is able to copy those files. So but we have the other problem, you need to be careful that you have enough D speaks because there will always be hanging in there. Another problem is, if all the clients like if the clients that use the application is locked if they're offline, they won't be able to tell them that the primary to remove the will fires, right? So the primary never remove those options. And then you might have a problem that you have in your configuration file. Now I look, I have here, the retention policy of my files is one day, but now I have plenty of days of an archive of all files. Why is that being used? Why is not being removed? Amen. So one problem might be the replication slots, right? So and when you create a replication slot, we need to be careful with those situations, as well. So if you have a replication slot, and you don't have the if the clients are not using their reputation is Lattimore, we should go on the primary and remove the replication slot. I'll show you later how we do those things. So here we need to tell the name of the replication slot. I want to call

**Charly Batista**  
rokocoko. Well, just

**Matt Yonkovit**  
seems like a reasonable name. By the way, x y z. did throw a couple of comments a couple of them we'll come back to but said Max wall size should be greater than two as you said one for wall movement and one for backup.

**Charly Batista**  
Maxwell sighs. Actually, it's it's not the

**Matt Yonkovit**  
max Maxwell center. Yeah. Oh, yeah. Well, Sandler Exactly. Yeah.

**Charly Batista**  
So exactly. So because when we use these, this option, here we are, these PG base backup will open to connections to the primary. That's, that's a very good comment. If you open to connection, so the primary, right so if we, it needs to, you need to have Microsoft centers and not four centers on the primary to be able to, to surface all the connections that have been open, right? So and you need to keep paying attention if you have other applicants that we're using. So you need to go to the primary and increase the max awesome. That's a good point. Okay, replicant?

dash s, so let's go. Okay, oops, to be able to use the SS just with the replica name, we need to use this capital C. This is the greatest launch and this is this last name. So we can make it verbose. In our case, well, let's make it verbose.

**Matt Yonkovit**  
So we can see what it does with the magic of the live stream is. It'll be stored on YouTube forever.

**Charly Batista**  
Yep. As we make these verbals, it's also good to see the progress so we can ask you to tell us the progress right? So some progress information. And that's it. The last bit is to tell where we want to restore this data. So dash D tells to the to where's the folder? Remember, we create the VAR lib EGS

**Charly Batista**  
squirrel. The most were 1313 Main. Yeah.

**Charly Batista**  
Okay, here is where I want to save. And if everything goes well, we're gonna ask for the password. Remember, we have an encrypted password. And it failed. So it failed because there is no entry for these hosts using SSL off right. So replication hose using connection SSL on so we need to turn off the SSL so is there any option for us to turn off the SSL

**Matt Yonkovit**  
I don't know. Let's look at the main file. Let's look at the help there.

**Charly Batista**  
Ah If

**Charly Batista**  
we go to

**Charly Batista**  
SQL. This is my own prompt here. So we have our own key SQL, and we can use these Ss Elmo disable. And we can pass the parameters here. So I going to try it on, I've never tried using all PG base backup to see if that works. And let's try to do it. So just copy it here. So we have the host. Okay. Two main arguments on the common line for BGP is a backpack. Yeah, it looks like it didn't work. All right. So then I didn't want to change my pgdba. So let's ask Google

**Charly Batista**  
Did you base backup?

**Charly Batista**  
Let's just

**Charly Batista**  
change our budget.

**Charly Batista**  
And we just have a question for you. Do I need to restart the database when I change the PGH? PE file?

**Matt Yonkovit**  
I think so.

**Charly Batista**  
Are you sure?

**Matt Yonkovit**  
I mean, that's the networking config. Right. So what okay, what, especially if you're talking SSL.

**Charly Batista**  
What we have to do here

**Matt Yonkovit**  
to disable SSL?

**Charly Batista**  
Yeah, like?

**Charly Batista**  
You. Yeah, what do they have to do for that one? Should I just put one host here? That's replication, right? Replication protocol. Replica? Date? To?

**Charly Batista**  
Which is this IP?

**Matt Yonkovit**  
Yeah, so it should just be right. So you would just put host no SSL in there, as well. So I'm checking. I'm checking out the docs real quick. So it would be hosts with no SSL, three types of behavior. So instead of hosting its host, no SSL are great hosts bash or a host to get an altogether just no SSL. Okay. The database user IP, IP mask also that

**Charly Batista**  
we can disable it just for this one, right?

**Matt Yonkovit**  
Yes, yes, you can. You can define it for a specific address, supposedly, right?

**Charly Batista**  
Yeah, I'm saved. So now, I should restart the database. But can I

**Matt Yonkovit**  
do I not have to? I wonder if that for that client and see that the client authentication, so if it would

**Charly Batista**  
do reloads will not come

**Charly Batista**  
some? Yeah.

**Charly Batista**  
For some of the configurations, we don't really need to restart the database, most of the ones on PHP, if not all of them. I don't remember the top of my mind, we can just ask the database to reload. So there are two ways that we can do we can select the PG to reload here, or you can send a sick there a signal on Postgres to reload the configuration from the terminal like system reload or a sick day or something like that

**Charly Batista**  
we can send it to the post here. It's easier and more sacred, just sent inside of the database. So

**Charly Batista**  
while we still have a problem?

**Charly Batista**  
Oh,

**Charly Batista**  
SSL on

**Charly Batista**  
maybe the opposite. What is this wire we still have the same problem. No Game Three Four replication connection from host user replicator SSL. Whoa, whoa, yeah,

**Charly Batista**  
that's exactly what we teach. Just one question is because may not be using that configuration file.

**Matt Yonkovit**  
Oh, you think it's, it's doing another HBA? Confor not using it at all? Maybe. Oh,

**Charly Batista**  
look what we have here.

**Matt Yonkovit**  
Oh yeah, you're in a different location. Yeah.

**Charly Batista**  
That's that that that.

**Charly Batista**  
So

**Matt Yonkovit**  
what is it, Charly? Oh, see

**Charly Batista**  
we have a lot more things here

**Matt Yonkovit**  
so then it's host no SSL don't forget, so

**Charly Batista**  
I permanently.

**Charly Batista**  
Let's try without,

**Matt Yonkovit**  
Oh, you think you think that SSL is configured and it just we didn't add the? Yeah. I get the Hagen's Allah. How are you?

**Charly Batista**  
Okay, there's no one.

**Charly Batista**  
Here you go.

**Matt Yonkovit**  
Okay. Yeah, so we were just using the wrong configuration. So let this be a lesson to all of you. There are multiple locations where those configuration files could linger. It's always good to check. Yep. Or good to keep consistency, especially when the database servers are named after you.

**Charly Batista**  
Yeah, like, we are not using this file here. Right. So we don't need this, why? So then, let's remove this file here.

**Matt Yonkovit**  
So now everything's going to break, by the way.

**Charly Batista**  
Not Well, that's, that's the best. So remember, I told you, I hoped we would.

**Matt Yonkovit**  
So I don't know if people knew this. But the way that Charly is operating, and I'm just going to get a clue you all into this, is if Charly says, I'm trying to make things break and fail. When they do break and fail. He looks like a genius. And then he doesn't have the break or fails. He can be like, well, I knew it could fail. But I didn't want just to do those failures. I wanted something more meaningful. So he's got an adult. No matter which way he goes, it's awesome.

**Charly Batista**  
That's not true. That's not true.

**Matt Yonkovit**  
It is true. It's true, everyone. Okay,

**Charly Batista**  
well, that's let's, let's see how our application is. It's what we look for, it's hanging here. Remember that? I said, the PG base backup, we wait for a checkpoint. Yes. I have no idea. What's the checkpoint configuration for our server?

**Matt Yonkovit**  
I think you pushed it back because you set it up like you you've kind of deferred it quite a bit, I think, or at least.

**Charly Batista**  
I don't want to wait for that much. No, no, I must force a checkpoint. Hey, you might as well see. I'm just posting a checkpoint here. And that's why.

**Matt Yonkovit**  
There you go. Look. Yeah, here we go. See now?

**Charly Batista**  
Yeah, when the force of the checkpoint started copying. And that's why I didn't want you to put too much load. Because if you put too much load, you might have a huge checkpoint time.

**Matt Yonkovit**  
I think we've only got like five or six users right now. Okay, there's a workload. So it's, it's pretty light. Things Considered 26777 users on the system. It's not doing I mean, a lot of those are read users as well. So it's not like it's that much, there are just a few rights. So if we were to look at like the rewrite split ratio, it would be heavily read right now.

**Charly Batista**  
One option that I forgot here,

**Charly Batista**  
and it's quite useful

**Charly Batista**  
is dash r.

**Matt Yonkovit**  
So what does dash r do the right configuration for replay?

**Charly Batista**  
When it's finished the copy we have the copy of the file, but then we need to create the build configuration file for the replica to connect to the primary I don't remember all the options. I never do. Right. So what are you going to do? Okay, I got to kill her, but

**Matt Yonkovit**  
you're 37% Complete. What a waste. Yeah,

**Charly Batista**  
that well, it could be worse. It could be 97%. So Right. I going to wipe out data A replica star everything here. Remember that I told you about the replication being large? So we might have it here. Where's my select replication? Well, now we have a replication is locked with these names.

**Matt Yonkovit**  
So you don't need to recreate it. You can use Yes, already there.

**Charly Batista**  
Exactly. But the thing is, if, okay, now, if I run here, that kind of fail. I didn't suppose to because we're asking the dash c to create the replication slot with these names, and replication is a lot already exists. But because of the checkpoint here, right? Yeah, it failed. Because replications locked replicas already exist, right? So, in this case, let's try to remove this batch. See, we just want to use a replication slot. We don't want to create anyone.

**Charly Batista**  
So 321.

**Charly Batista**  
That's many checkpoints.

**Matt Yonkovit**  
All right. So then this should start, and we've got a question that popped up. We've ever we can kind of like while we wait for this, we can go back to a couple of the questions out there. And so working our way back, Jorge has said, is there an easy way to switch between the primary and the replica? When you're using streaming replication? And then go back? Can you toggle back and forth to which one is the primary?

**Charly Batista**  
Well, oh, yeah, we, if I understood the right that the question is, like, I have the node A, is the primary node B is the replica, right? I want to demote node A to erect node B to a new primary. And at some point, go move it back. Right. Is that the question?

**Matt Yonkovit**  
Yes. So okay, it's about making like be the primary and then returning later on?

**Charly Batista**  
Okay. Okay. Yeah. We do.

**Charly Batista**  
Postgres has a tool that is PG.

**Charly Batista**  
never remember the name, pg. VGA VGA?

**Charly Batista**  
is not here. Not to find that the nine find

**Charly Batista**  
us to most was has a tool. There's PG

**Matt Yonkovit**  
CTL. cluster there. Is that what your

**Charly Batista**  
nose? No, no, no, I just want to find the binary folder.

**Charly Batista**  
Oh, yeah. Because well,

**Charly Batista**  
PG, PG rewind. Right? So what happens is when you demoed the node like something happens to denote a, and then you promoted the node B, there is a common on Postgres, that is it's PG promote, you can go here and select PG to promote to promote something you promote or

**Charly Batista**  
promote?

**Charly Batista**  
Yeah, it's,

**Charly Batista**  
I think it's like a PG promotion. There is a common that you run on the node itself that you promote the node from primary, one replica to a primary. So that node will become a new primary, but it doesn't tell the audit node that it is now a primary. So at this point, you have two primaries if you don't stop the old one. You have to Primus habit split-brain situation.

**Matt Yonkovit**  
Yeah. So because the replication is a one-way stream design, it doesn't reverse it automatically without having tools or some sort of automation in place.

**Charly Batista**  
Exactly, it doesn't do. So what you can do is you can get this configuration file that you are creating here, okay, then, let's say the node one crashed the northern crash, so it's gone, you go to the node p node v n and select a PG promoted as a primary. So now we only have one node, and this node is a primary. So on this node here, you make sure that it doesn't receive any outside connection, okay? Just to make sure the application does not connect try to do anything because at this point if you just start up this node is going to be private put the firewall whatever you do not accept the connection. You go there, and then you change the configuration. We'll see the configuration here to tell the node is a replica. And we can use the two PG rewind, you put this note the old primary, all the same, time rely on Postgres. What is the timeline? Every time that we start a database it creates that time is like, to those who watch Marvel shows kinematic universe. So or watch it lucky, we have those lines in time, right? So and they might have different brains on the timeline. This is what happens to Posterous. So it has one timeline; when you promote a new node as a primary, it just brings the old timeline and creates a new timeline. Node A is started with timeline one, node B going to have timeline number Q, and progeria wind will get node one and put to use timeline number two from the node B. So now it can be a replica for lone node Q. If something happens, let's say now you have node B, that's primary and node A, that's rapid if node B crashes, and you need to promote node A, when you run the command to promote it to create timeline number three, so you need to run the PG rewind on node B, that was the old primary to join this new timeline number three, and it can you can just move back and forth between those two notes. So Postgres has a cute make those things work to make things easier to work on timelines. But we need to be careful because when you run the PG rewind to put on the new timeline, you might have some transactions that were not replicated. So all the transactions that were not replicated before that node crashes, when you run PG rewind, they're gonna be rolled back. Because if you put them on the timeline of a tree, and those transactions have not been replicated be just gone.

**Matt Yonkovit**  
Okay, fair enough. We are We completed the backup now. Right? So okay,

**Charly Batista**  
yeah, this is the file that I didn't want to create.

So not only these. Yep.

Yeah, this is the file. So on this file, here what we have. This is not the only target one. I'm missing one file here. Oh, I didn't include the dash PowerPoints.

**Charly Batista**  
No, you didn't.

**Charly Batista**  
Oh, Stupid me.

**Charly Batista**  
I cancel for that,

**Matt Yonkovit**  
though. You canceled, and then you got so wound up in the story of the dash c. Of the Create. And when it failed that you were like, Oh, I've got to, I've got to stop, and you reran so. So here, here's an interesting question. Can you just copy it? Or can you just create a configuration file without actually doing the full backup?

**Charly Batista**  
That's a good one.

**Charly Batista**  
I might be able to.

**Charly Batista**  
But I've never tried it. So it's a good time to try. Right? It might be I don't know; on top of my mind, I choose that one to research. Why I'm trying to do this here is to see if it creates in the beginning. So if I go for data

**Charly Batista**  
for Africa to

**Charly Batista**  
know, you're going to create by the end? Would you base back up? Sometimes you might help, but maybe not this time. All right. Let's try to we can Google

**Matt Yonkovit**  
I'm looking; I'm looking right now to see if there's anything like

**Charly Batista**  
I never remember those comments on top of my mind. That's why I always use dash r. So, okay, what we need for the files

**Charly Batista**  
replica

**Charly Batista**  
one, replica. So I need recovery.com. The one thing is some of those files they have the chance to change it. from version to version. We're on version 13 Right then, bye

**Matt Yonkovit**  
See a way to just write that file without doing the full backup.

**Charly Batista**  
primary connection who

**Charly Batista**  
he is host equals

**Charly Batista**  
I peed. Is this the last? Well, I don't need a department what the

**Charly Batista**  
four by for three cube users were using replicate for plus rewards in q1. It's been quitted

**Charly Batista**  
where RIS will restore Commons or Now, in our case, it's useless.

**Charly Batista**  
So empty we have for now because we're not maintaining archive when

**Charly Batista**  
our cases are also useless because we're not archiving anything. So this one here should be able to do the trick.

**Charly Batista**  
The thing is, they're all roots.

**Charly Batista**  
Yeah, because they run as the root users. So, not so much. But I can do shall show that Postgres

**Charly Batista**  
All right, so we have it here, but if you pay attention, we're missing a couple of files, right? We don't have here the post-Biscoff that five don't have here the PGH be that fire you the those five they've not been cooperating cooperate outage, because, on the primary, they are not on the data, G. So what did you base their cap does is to copy the data do you it's like it's kind of does an RC Right. So we need to be careful with those. And also when we have table space on the database mounted elsewhere. And we have seen links. So we might have problems. And this is something that we won't have time for today. But for the next session, an employee with EEG with positronium status things also wants to use PC-based backup. So one thing we need to do here is on the primary, let's try to create a movement to create some table space outside of the different data in here to see how that behaves when we do PG base backup, right? Let's put this put in here, and also, we do not forget because while those are things that we need to be careful about, we need to pay attention to make sure everything is being copied out. And especially when we're using symbolic links, all this kind of stuff sometimes messes up with the final result. So here probably you probably won't have much problem because we have on etc., etc., Postgres 13. Mate, we have the configuration files. So you just cloned the box. We have those files there. And we'll find out that they missing here because not only the recovery, but we if we go here we have the postmaster pts. So

**Charly Batista**  
if I do not put this file here

**Charly Batista**  
when I start my database, it won't be able to get the files from the DTC, or I need to pass in the manual. So I don't want to pass them manually.

**Charly Batista**  
And before you have this error, I want to go okay.

**Charly Batista**  
If everything's fine, what can I do

**Charly Batista**  
is I can use the copy

**Charly Batista**  
Did you sit? Yo, come on, we run here goes; well, you never fix it that the system

**Matt Yonkovit**  
I never fixed it. What this is this is your name all over it. Am I?

**Charly Batista**  
Oh, okay, so it almost started but we have too much room it's too much person.

**Charly Batista**  
So we need to

**Matt Yonkovit**  
do so you're trying to get your system hacked here? Surely you don't want to do that?

**Charly Batista**  
Yeah, no, I don't want to do that. So ch moves 700?

**Matt Yonkovit**  
Well, while Charly's working on this, I want to remind everybody in a couple of weeks that not only are we doing these live streams, we've got an online conference coming up. So June 21, through the 23rd, Charly's going to be speaking, I'm going to be speaking, I'm going to be talking about design principles in the database side. Charly's got a couple of different talks, including one about point-in-time recovery, I believe. And it is 100% live stream just like this. So it's going to be on all of the same channels that we're on right now. And so there are over 30 speakers, I think, from all different companies, and we're going to be talking Postgres, MySQL, Mongo, everything in between, so anything database related, so we've got a lot of topics, I'm going to drop the link in chat so that people have a copy of it in case they're interested in checking it out. But we hope that you can join us. All of that stuff will also end up on YouTube. So you can watch after the fact if you don't want to hang out life, but live, we will have people the speakers answering questions and chatting and doing things.

**Charly Batista**  
And here we go. It's failed because, well, it should be a muscle if it doesn't fail. It's not that's making the livestream.

**Matt Yonkovit**  
Well, remember, Charly has already prefaced his goal is to make things fail, because it makes it more interesting for you all and streamlined.

**Charly Batista**  
Because of this one, I have a guest who remembers the problem with the PHP file.

**Matt Yonkovit**  
Oh, you didn't fix that? Did you? Oh, there's

**Charly Batista**  
another box?

**Matt Yonkovit**  
Well, it's not I told you that fix that, like, so if you go back in those who have followed along in the six or seven weeks that we've been doing this, every time Charly runs into this problem because when he set up these boxes, it was misconfigured, a little bit. So every time he starts, we start with this problem. And we're like, oh, wait a minute, why did the server fail after we restarted after a week of being shut down? And we're like, oh, yeah, because you didn't create the right directory and didn't set this up properly. And so we've hit this problem every week. So Mahesh is here. Hey, Mahesh. And he says, Hello, Charly, but not Hello, Matt. I don't get this ID right. Like he doesn't like me. I feel so unlike. Okay.

**Charly Batista**  
It's it says there are some there's using a common inside of recovery crowd that's not supported anymore for this reaction. And these, remember that I said from bracket depression, something's changed a lot, luckily. Now, the replica CI has just finished. And we have the configuration file.

**Matt Yonkovit**  
Oh, so now we can look at the official configuration file. So one of the problems with software that's been around for as long as Postgres halves is, as it evolves, things break, right, so you just need to be better.

**Charly Batista**  
That's it this?

**Charly Batista**  
So see, we have a post without conflict. Well, it's quite different from what I just created. Right? So yeah, it is. And all okay, yeah, we do not use the

**Charly Batista**  
let me go here.

**Charly Batista**  
CTE, the recovery.com.

**Charly Batista**  
So, we do not use this guide here. This doesn't use this guy here anymore. It used the system by that signal is just a placeholder file. It's empty files, you see the size zero, to say that, look, this is a standby. This is not a primary one. So Good thing we're going to do we're going to speed these posts result.com, And it's done by that signal to the replica

**Charly Batista**  
and they're going to show Okay, and we now should be restart

**Charly Batista**  
and of

**Charly Batista**  
course, there's always something else

**Matt Yonkovit**  
my gosh, you didn't get Percona goodies. I thought we said I'm going to go make sure we get that to you right now, so hold on a second Charly continues But Mahesh says that he hasn't gotten what I promised him, which was some Percona swag a Charly's wearing your swag right now Mahesh see it's on his head it's just it's the Percona hat but we yeah we'll get you something I was thinking

**Charly Batista**  
more than expected

**Charly Batista**  
okay, this file other than Oh of course, because that it's wrong those degrees outro is we don't want to use this here just a statement

**Charly Batista**  
because this position is from the audit backup, remember? So oh

**Matt Yonkovit**  
yeah, because we were doing tests. Yeah, yeah. So

**Charly Batista**  
it won't exist for this one

**Matt Yonkovit**  
all right. So Mahesh, I just went to Danielle and Alex and asked them specifically Hey, did we ever, you know, get that sent out to you so we will work on that? We'll work on that

**Charly Batista**  
complaint for the timeline we mess it up with a lot better timelines do the three

**Charly Batista**  
so what I'm going to do here

**Charly Batista**  
is main

**Charly Batista**  
and she is one strive to get to work postmaster

**Matt Yonkovit**  
All right

now you have something a little different

**Charly Batista**  
Yeah, it's trying

**Charly Batista**  
to it's trying to recover

**Charly Batista**  
this guy, it will not work because we don't have those files here. It needs to ask to the primary

**Charly Batista**  
are we doing archiving on the primary?

**Matt Yonkovit**  
I thought we were because we were using PG backrest and doing point-in-time recovery the last couple of streams, so we should have set that up.

**Charly Batista**  
Yeah, the problem is

**Charly Batista**  
the problem is those files are not accessible here. So it's complaining because, oops, It's complaining. After all, it cannot access those files. Okay, now we have the problem of not accepting applications, Okay? Request timeline queue is not a child of the servers history

**Charly Batista**  
Okay,

**Matt Yonkovit**  
see, this is what you get when you mess with the sacred timeline Charly.

**Charly Batista**  
I told you

**Matt Yonkovit**  
surely that's what the sacred timeline is everyone just can't do.

**Charly Batista**  
What's the timeline I told you

**Matt Yonkovit**  
Hey, you're the one who brought up the Marvel movie reference.

**Charly Batista**  
Oh, that's yeah, it's a very good reference

**Charly Batista**  
probably Same same. Yeah. The latest checkpoint that's on timeline one, but one is not

**Charly Batista**  
in the history of the server.

**Charly Batista**  
Okay, let's go back to the primary where the primary, so let me see. Where are we doing? The need to see

**Charly Batista**  
or squeeze as well. SQL 13 Postgres go to archive Commons

**Charly Batista**  
we were archiving

**Charly Batista**  
two stones a one. Why does stanza East buddy suppose these big backup archive each one slug archiving?

**Charly Batista**  
The problem is we don't have the slides here anymore why they're complaining, so we're not supposed to need them at this point?

**Charly Batista**  
Where am I? Yeah.

**Matt Yonkovit**  
Charly, real quick. So if so, on the replica server, there's an Etsy Postgres config, right, and so that's going to have the recovery in it because it's a clone of the primary server so go back to the replica go under Etsy post-Yep. I can make drop now If this works, I can mic drop because I knew something Charly didn't, so I'm like, ooh, today's done, and go celebrate the weekend early woohoo, we might also have a recovery config file there so I don't know

take a look at that directory and see what else is under there. There might be something else that

**Charly Batista**  
actually, it might be something backup label stuff timeline

**Charly Batista**  
the request is still the same way the checkpoint is okay

**Charly Batista**  
one time remember the history of the requested timeline industry working environment

**Matt Yonkovit**  
let me take a look at myself I'll parallel work with you here, but people won't be able to see my screen while I goof around. Maybe I can double the second set of eyes sometimes, it helps it make make it go quicker

**Charly Batista**  
horse race me

**Charly Batista**  
so am I able to

**Charly Batista**  
etc etc etc

**Charly Batista**  
access

**Charly Batista**  
and you want

**Charly Batista**  
to do something, yeah so yes, it's let's see, is this

**Charly Batista**  
okay

**Matt Yonkovit**  
so what do you got going on now so what did you What do you think it is? I think it's, uh

**Charly Batista**  
yeah I'm I'm making sure we have all the one files there

**Charly Batista**  
this is one of the problems okay, system CTL classes

**Charly Batista**  
are seen

**Charly Batista**  
one is

**Matt Yonkovit**  
Hey, Charly, under, or is this under var lib Postgres 13? Yes, there's a recovery signal file go back to directories, and go back one more. Yeah, yeah. Is this going to cause any issues having the recovery signal in there? I don't think it should it

**Charly Batista**  
shouldn't

**Charly Batista**  
while we're concerned about demand

**Charly Batista**  
so yeah why

**Charly Batista**  
it's let me show the merge on the pseudo

**Charly Batista**  
okay

**Matt Yonkovit**  
so did it copy over the files? Or was it where was the wall files never made it over?

**Charly Batista**  
Multiple of them. Why would that

**Charly Batista**  
have we had? That's a good question.

**Charly Batista**  
So I'm not able to SSH to the other

**Charly Batista**  
box

**Matt Yonkovit**  
just why aren't you able to SSH to the other box wait, that's weird as what user because it's only shelling SSH keys

**Charly Batista**  
not anymore they just change its password authentication yes, see hold on

**Charly Batista**  
Slack a password authentication

**Charly Batista**  
so

**Charly Batista**  
each box is this one too. You will

**Charly Batista**  
so we have

**Charly Batista**  
a lot of files, and we don't need

**Charly Batista**  
all of them

**Charly Batista**  
it's complaining

**Matt Yonkovit**  
permit route login is what welcome said Because yeah, it's gonna deny root login even if if you Oh yeah,

**Charly Batista**  
yeah, yeah.

**Matt Yonkovit**  
But you could also just copy the keys over, which is what I'm doing. So they can just get to each other without a password which is probably just as effective

**Charly Batista**  
Yeah, it is.

**Matt Yonkovit**  
These are your boxes Charly

**Charly Batista**  
should be disabled

**Matt Yonkovit**  
now the question is for those who are watching, does it make it go by quicker if I start singing while Charly works? I mean, I could have

**Charly Batista**  
no police, no he's got no

**Matt Yonkovit**  
like a lady to fire red or Charly here, by the way, there are the keys are set up as well as long as you are the Ubuntu user between the two

**Charly Batista**  
Yeah, I need to be built

**Matt Yonkovit**  
you can use it once you're on the other box, right? So yeah, but

**Charly Batista**  
our sink thing, that's one thing, okay. This is one of the things that will go back to the default error message.

**Charly Batista**  
poster is

**Charly Batista**  
1313

**Charly Batista**  
Okay, all screens of the article

**Charly Batista**  
we want to record from here. We don't want to restart Chrome and

**Charly Batista**  
release the one thing here because it's just now common channel vacation cells a cell was a matter

**Matt Yonkovit**  
Oh, I wonder if those

**Charly Batista**  
you ever lived Oh,

**Charly Batista**  
yes.

**Matt Yonkovit**  
I think you think, well, so in your auto comp it was the recovery commands that were in there were from the previous instance. And then it added or appended on end the replication side, but did you comment them out? Did I see you just comment those out? Like the recovery, target lsn restore command, things like that, that I see those? Is that what you were doing?

**Charly Batista**  
These this for the latest backup,

**Matt Yonkovit**  
right? So, okay, but got to look at the latest.

**Charly Batista**  
See, this is the go under. They're

**Matt Yonkovit**  
going into there and go to the okay. So look at the autocomp

Okay, so you did comment out? Yes, it was okay, because all of those were from the previous iteration.

**Charly Batista**  
Yeah, and one thing that I probably should for now have to come out is

**Charly Batista**  
this guy here

**Matt Yonkovit**  
so well, so since when you Oh, we don't? Yeah,

**Charly Batista**  
we don't need those are going to make things simpler.

**Charly Batista**  
No binding, okay?

**Charly Batista**  
Yeah, when you're saying

**Matt Yonkovit**  
well, so the autocomp has what was leftover from the previous iteration. So if you were messing around with a point in time recovery, it's going to pick up all those variables. It looks like the base back backup tool is going to just append the replication stuff at the end so it's not going to overwrite anything else that was already in there

**Charly Batista**  
yes the thing is

**Charly Batista**  
Wait is still trying to go over the timeline number one

**Matt Yonkovit**  
is it possible that when you Is it possible that because you had those config files originally in there that caused some weirdness

**Charly Batista**  
it possible it is

**Charly Batista**  
it's shouldn't be unlikely

**Charly Batista**  
let's take a look on the ETC

**Charly Batista**  
close with those

**Charly Batista**  
so the only thing that

**Charly Batista**  
the things that it does here okay, this is the year the address

**Charly Batista**  
that's good go through this file here the socket Okay, or use an SSL it's working the memory for us as a matter of the shared buffers it's not it's fine

**Charly Batista**  
they're kind of mode

**Charly Batista**  
gonna disable for now because it's the replica replica maximal size the same as we have on the primary the recovery

**Charly Batista**  
the

**Charly Batista**  
are the log file

**Charly Batista**  
log collectors Okay.

**Charly Batista**  
Graphics we don't have don't have any stats on

**Charly Batista**  
include fire here three now.

**Charly Batista**  
I do cough that

**Charly Batista**  
shouldn't be empty.

**Charly Batista**  
Okay, it's empty. It's not in there.

**Charly Batista**  
So we don't have any extra files.

**Charly Batista**  
So this one is not included in anything else.

**Charly Batista**  
So anything that you have on all suites here either for this include G here that we copied our key are going to comment out here, just make sure we don't have any surprise. And everything else should come from the beta g. So the beta here what we have here, we have this backup stuff. So we don't need any of them. For now, backup whatever we can move to this folder, right.

**Charly Batista**  
We have

**Charly Batista**  
let me take a look on the postmasters

**Charly Batista**  
the options that we have here. Okay, we just tell

**Charly Batista**  
where to find a PostgreSQL dot conf.

**Charly Batista**  
What else and the postgres that came out

**Charly Batista**  
to call up the offended by the end.

**Charly Batista**  
You know what I gotta do? What's the name of it is recovered that comes

**Charly Batista**  
from the pool screws,

**Charly Batista**  
they got to move this file as a red carpet outside, right. So here we have the PG start statements, the shard library, so we don't need we're now going to be here.

**Charly Batista**  
So

**Charly Batista**  
the primary way using replication is large. So the applications log should make sure everything is has been they're

going to make it quite simpler. We have the username, the password hostname default. SSL shouldn't be a problem

**Matt Yonkovit**  
do we need a recovery target timeline in there?

**Charly Batista**  
No. Okay. Cheers. Ship No. All right. Well,

**Charly Batista**  
using comments, okay.

**Charly Batista**  
We move it back.

**Charly Batista**  
Look, we're not using this file here, right. So

**Charly Batista**  
actually move this file here

**Charly Batista**  
to GMP.

**Charly Batista**  
I also going to remove

**Charly Batista**  
the standby.

**Charly Batista**  
What I'm trying to do here at this point is to start this node as a standalone server. So we don't have recovery. We don't have standby. This is just a standalone server. Right? So it's not replicating from any server right. So we have a problem. Now, the problem is not related to the replication right.

**Matt Yonkovit**  
It's probably still related to the recovery. It took the backup and can't recover to the log file that it is looking for, for whatever reason.

Well, now we have a different problem.

**Charly Batista**  
When something is happening,

**Matt Yonkovit**  
something is happening

it's a lot of dots

**Charly Batista**  
in the province can still be

**Matt Yonkovit**  
there you go servers, oh, it's

**Charly Batista**  
started. At least we have something here we have a database. It's not a replica. So okay, the database is stopped, let's stop the database. So I don't want to

**Charly Batista**  
do anything on this database, right.

**Charly Batista**  
So

**Charly Batista**  
what are you going to do here?

**Charly Batista**  
Is going to CP

**Charly Batista**  
the

**Charly Batista**  
PostgreSQL? Not here.

**Charly Batista**  
But me. So why my link is not working now? From time

**Charly Batista**  
to time, your box just stopped working the VM

**Charly Batista**  
series that I

**Charly Batista**  
need to use? Try VI. Nope.

**Matt Yonkovit**  
So yeah, so So try it, try to start it again with that command. And if not, I'm curious, like, so. I was just browsing through the documents. And there's a comment in here that maybe you have to use the recovery target timeline, it says the default behavior of recovery is to recover the latest time of life found in the archive. If you wish to recover to the current timeline when the base backup was taken or into a specific child timeline. You need to specify current or the current timeline ID in the recovery target timeline. So because that's what you were getting was, uh, you were in the wrong timeline, right? Was the error before? Yeah, so I'm wondering if the dash r command in the base backup command didn't give you all the parameters you needed? So just try and start with this. And then let's see if we add the recovery time target timeline. Which I think if we set that to current

**Charly Batista**  
Yeah, we have it now. Right?

**Matt Yonkovit**  
Well, we don't have the current target in there. Right. So that we don't know we don't have

**Charly Batista**  
Yeah, this is just the

**Charly Batista**  
so we only have the primary connection info. And the primary is the last name. And we've just done by signal we're saying we are standby, right, so we don't have restore, restore. Come on. We don't have archiving anything for this one. Right. We're just starting. We want the server to be on standby and we're telling them where to go

**Charly Batista**  
so that makes sure that the stock

**Charly Batista**  
is not running. Let's start and yeah as expected, we probably going to get the same

**Charly Batista**  
error right

**Matt Yonkovit**  
yeah, it's Yeah, different timeline. So go ahead and try recovery underscore target underscore timeline and I don't know if we need current or latest

**Charly Batista**  
recover mental

**Charly Batista**  
multiple see recovery on your school

**Charly Batista**  
and I say that again.

**Matt Yonkovit**  
Sorry Yeah. Recovery underscore target underscore timeline try latest

**Charly Batista**  
but latest

**Charly Batista**  
before right.

**Matt Yonkovit**  
It says that's yeah, I mean, it's but that's what you need for The standby it needs to recover to the latest

**Charly Batista**  
what's wrong with them?

**Matt Yonkovit**  
Why why are you saying

**Charly Batista**  
it's because

**Charly Batista**  
reading is not working

well I can hear the Lord Yeah, when the service stopped working everything stops working now we have to use nano

**Charly Batista**  
okay, just

**Charly Batista**  
to make sure we get it okay all right

**Charly Batista**  
okay

**Charly Batista**  
let's start now

**Matt Yonkovit**  
nope nope

**Charly Batista**  
okay yeah we're running out of time

**Matt Yonkovit**  
surely How dare you run out of time?

**Charly Batista**  
Yes it's a need to draw in 10 minutes

**Charly Batista**  
so we're going to do what are you gonna do

**Charly Batista**  
is

**Charly Batista**  
I gonna go back

**Charly Batista**  
to your bar Okay. Chris

**Charly Batista**  
13

**Charly Batista**  
Okay

**Charly Batista**  
man right

**Charly Batista**  
right replicate you it's not replicate You mean because we mess it was one

**Charly Batista**  
CG meaning we name

**Charly Batista**  
PostgreSQL these important not working

**Charly Batista**  
so

**Charly Batista**  
practical one

**Charly Batista**  
let me just one option here to see if that gonna work

**Charly Batista**  
your ordinary

**Charly Batista**  
instead up late this year is

**Charly Batista**  
now

**Charly Batista**  
you're

**Charly Batista**  
Can you put that

**Charly Batista**  
I can do it here just quickly see at

**Charly Batista**  
home

**Charly Batista**  
too through it is that

**Charly Batista**  
stage authorize it actually Vaughn to get it on the coffee list to the bar on the screen it's not the crop disappear subdivision because it's a colder

**Charly Batista**  
okay now I can do

**Charly Batista**  
can police

**Charly Batista**  
on one two. So this is a search

**Charly Batista**  
for get crack your you your break.

**Charly Batista**  
So CP bash our stage stitcheries On

**Charly Batista**  
Stage Two

**Charly Batista**  
was

**Matt Yonkovit**  
all right, So Charly, you've got to go to a meeting you said. So what I'm gonna do is I'm gonna go ahead and I'm going to walk through the servers and just redo the setup myself. And if I can get it working, then I will go live myself and just kind of show everybody because it

**Charly Batista**  
also well But what I'm doing here is I'm doing the Our Sync for the restore command. So we can this can try to copy

**Charly Batista**  
the,

**Charly Batista**  
the data here, right?

**Charly Batista**  
So it's screens and

**Charly Batista**  
because we have this backup archive, blah, blah, blah, on that other servers, right? Or no, we're not archiving there.

**Matt Yonkovit**  
Yep, totally. So So I think this is one of those things that as we, we dig in deeper, sometimes we just like need to take a reset. So, let me just go back, I'll go through and try and get replication setting set up between these two servers. I've got a bit more time. So I'm just gonna go from kind of a zero sum, and just start over and walk through the process myself. And I'll make sure that I can get through and then once I do, like I said, I can go live, just as kind of a one off stream for folks and then walk through the process after I documented here. But so I think there was there was quite a few things, I think the last 20 minutes or so we just started. Let's try. Let's try. And sometimes it's better just to take a step back.

**Charly Batista**  
Okay. Can you not remove this for this two folders? And create a new one. So because I also want to go there, and to refine, understand what was the problem? Because people out there, they might hit the same problem, right? So when you have like petabytes of data, you don't want to stream the whole backup animal again.

**Matt Yonkovit**  
Right, right. I mean, in this case, it's a small database. So it's easy. Yes, exactly.

**Charly Batista**  
Yeah. So I want you after this, this, this meeting that I have, like, I feel nervous. I want to go back to this to the server to see what the problem is. So thinking with no camera, no lights on my face. So I'll think better. Okay. And then, I will record to try to fix a problem. And then I also going to do another video and explain the problems. Does that sound good?

**Matt Yonkovit**  
Fair enough. Fair enough. Fair enough. Fair enough. All right. So everyone, thanks for hanging out for almost two hours. Now. Do we need to schedule this for two hours, Charly? No, no, no, no. Yes. Yes, yes. But so in two weeks, we will be back on a Thursday. And our goal is to continue the replication stream and keep it going with Patrone. So we have to have this problem worked out before then. So we'll get this resolved.

**Charly Batista**  
We need to get this fix because this is the baseline, right?

**Matt Yonkovit**  
Yep. And then, in three weeks, we will be back with the Percona Live community online. So Charly's going to be talking. There are going to be several other folks talking. I dropped the link in the chat in case you're interested in that. But until next time, we appreciate you hanging out, and we'll get back to you shortly with the replication setup. That works. All right. All righty, everybody. Thanks so much.
