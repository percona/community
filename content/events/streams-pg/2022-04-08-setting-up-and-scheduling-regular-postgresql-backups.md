---
title: "Setting Up and Scheduling Regular PostgreSQL Backups - Percona Community PostgreSQL Live Stream - April, 8th"
description: "Learn more about backups setting with experienced Percona experts to ensure that your data is secure and safe"
images:
  - events/streams-pg/pg-stream-week-3-april8.jpg
draft: false
date: "2022-04-08"
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---
Learn about the best setting to protect and restore your data with Matt and Charly. They are talking about database backup settings, frequency, and different types of backups. Follow us on [Twitter](https://twitter.com/PerconaBytes) and get informed of all upcoming meetups



## Listen to the recording here

{{% youtube youtube_id="3OeX-gsdwFc" %}}{{% /youtube %}}


## Transcript

**Matt Yonkovit**  
Hello everyone out in live stream land. I am, Matt. And do you know who is not here? Charlie? I am in Jose. We are at the Postgres Silicon Valley Conference. We are waiting for Charlie to show up. He's going to come in hot, I guess and direct from a talk on PL, Java. If you can, believe it or not, hopefully you can hear me all. We had to improvise, because we're both here in San Jose. So we are using a streaming setup that we haven't used before. So hopefully you can hear me Give me a wave if you can. Or if you can't, or if I'm just sitting here and mining. That would be not a good thing, either. While we're waiting for Mr. Charlie, I will play you a clip of Mr. Charlie, because why not? So we've been recording some video here. It's been a pretty good ad experience at the Postgres Silicon Valley Conference. And Charlie is going to be setting up backups as soon as he gets here. So it'll be a few more minutes. He's running a little behind from his session. But when I did talk to him about the backups yesterday in a session, here's what he said. It's so cool. We're here with

**Charly Batista**  
again. Yeah, here we are. Once again, Balkan about PL, Java. I'm trying to let people don't use it. By the way, that's gonna be my talk. And I got to try to convince people to use it for those wonder here, and within the talk, they're gonna ask you what are you gonna talk about your job? So much for here? We'll Yeah, y'all. Maybe not?

**Matt Yonkovit**  
Yeah, not gonna be there. No. The question for you, though. Charlie is, are you ready for the livestream tomorrow? Oh, we have. Yes, we have a live stream tomorrow. You are supposed to be setting up backups.

**Charly Batista**  
That's true. I totally forgot about that. Live Streaming.

**Matt Yonkovit**  
Yeah, it's scheduled.

**Charly Batista**  
And we cannot rollback. Right? It's one day.

**Matt Yonkovit**  
Advertising you been on the live stream now for quite some time.

**Charly Batista**  
All right. All right. Once is committed is committed. And we do not have backups. So we cannot do a point in time recover?

**Matt Yonkovit**  
 Well, no, you're gonna have to do the backup on the server. The server you broke that didn't break the server. No, that's the server. You broke it. It won't start up automatically. It's first, it's looping. Wow, was that looping? I think that was looping. But guess who just joined me? I was I was stalling for time. Of course. Hopefully the sound is okay, as well. So please let me know about that. But somebody just showed up in the room. It took him a little while longer. But look, there's Charlie right there. It's good. This is your camera, Charlie. So you can see. You can't see you. No, no. Yeah. Why is that bad? Oh, well here. So this mic, you need to turn it on. Like pin it to your thing and turn it on? No video. You're not seeing video.

**Charly Batista**  
Godson you're not seeing any video? Okay. How is the audio? Oh,

**Matt Yonkovit**  
I don't know. You gotta tell me. How's the audio everyone? When are we starting? Huh? So we are started. So one second. Let me go ahead. And while Charlie's getting everything plugged in and ready to go. I'm gonna go ahead and come back to restream real quick and see if I can. Oh, could you log in? Hey, it's not that cheese. Oh, pizza. So

**Charly Batista**  
now I can see. Okay, well, it's working on YouTube. Well, it seems we're going on YouTube.

**Matt Yonkovit**  
Okay, so yes, it's working on YouTube. I think it's working on LinkedIn as well. So hold on a second. I think those those folks who are joining us now are from LinkedIn, LinkedIn land, so I'm gonna go over to LinkedIn land real quick. While Charlie tries to get things up. Are you mirroring your screen by the way, I can see if I can pick it up.

**Charly Batista**  
I have no idea how to mirror my screen.

**Matt Yonkovit**  
You don't know how to mirror your screen. Like it's just like an extra monitor. Just do an extra my eye. Yeah. But it just Okay, so I'm gonna put it over here.

**Charly Batista**  
On displays To display Oh mirror I see here now, but really, it changed my resolution.

**Matt Yonkovit**  
So I'll post the comment. Strange. Here. That is weird. So Charlie's still getting set up, but some people are having some difficulties with LinkedIn. Which is weird. 

**Charly Batista**  
So can you see my screen? One second? Oops, okay. Right. Let me close this here okay, let me just connect your own database.

**Matt Yonkovit**  
Say hello, Charlie. Hello, Charlie. Josh. So,

**Charly Batista**  
if asked me to speak a little Charlie, I'm just holding your instructions. 

**Matt Yonkovit**  
Yes. Okay, sorry about the delay, everybody. Audio is good on Twitch. Awesome. We'd love that the audio is good on Twitch. Love to hear that as well. And now I'm gonna go ahead and I'm gonna see if I can get Charlie's screen up and running hold. Like I said Charlie was coming in direct from a PL Java talk, which, that's exciting. That's what I have Charlie, screen up. Hey, boo. And now I have you in your browser? Hi. No,

**Charly Batista**  
I was just checking your Wow. Okay. Okay, hold on. i Okay.

**Matt Yonkovit**  
Hopefully there were no passwords and that that to us flashed on your screen? Oh,

**Charly Batista**  
just addresses. We don't use password. We use keys. So.

**Matt Yonkovit**  
Okay. Wonderful. That's excellent.

**Charly Batista**  
And I hope you've added my key. So the databases,

**Matt Yonkovit**  
these are the same systems that you've screwed up before. Though they're the same systems that you screwed up before.

**Charly Batista**  
They're the same system that we're going to fix them. Right.

**Matt Yonkovit**  
Okay, so obviously, Charlie here is struggling with the basics of SSH. So I'll give him a second. While he's doing that we did a few recordings while we're here. And Charlie and I broke the Yonk box. If you don't know what the Yonk box is, it's a controller with the different workloads. It's done in our booth right now. The cool thing about the Yonk box is it actually goes to 69. So five nines is a thing of the past. It's got all these knobs and switches, you take a look at 69 It's awesome. Ooh, that's really tiny. On your shell, by the way, like, tiny, I will fix it. Just fix the show that paint job. But So Charlie broke it, and then he tried to blame me. Like, and then he tried to bribe me with candy.

**Charly Batista**  
So you have to bribe anybody. 

**Matt Yonkovit**  
Yes. You had to bribe everybody. Yes. I invited other proponents to come up here but no one wanted to come up. They were afraid of being live there. Okay to be in front of like the hundreds of people here but like, they don't like the fact that they could be on the internet. I don't understand that.

**Charly Batista**  
Yeah, I don't understand that either.

**Matt Yonkovit**  
Yeah, you should just have to get to the DB box. You won't need to get any other ones. Are that EC2 dB. That is the box that is running the demo downstairs. Okay. Maybe if you want to back it up while people are messing with it and really screw up now. Why is this delayed? What's going on?

**Charly Batista**  
For now? We only it's better now?

**Matt Yonkovit**  
It? Here that? I think that's good. I think that's good. What do you guys think? If the font is too small, just give us a shout out and I think it's good for my end. I see it. It looks fine to me.

**Charly Batista**  
Okay, shall we start? No. Okay,

**Matt Yonkovit**  
so we Okay, so we're going to play a game here. In this game is called how much chocolate does Charlie have on his percentage?

**Charly Batista**  
I'm not going to play this game. It's not fun. No, it's totally fun.

**Matt Yonkovit**  
 So Charlie has this thing. Whenever he comes to the US or he travels. He brings tons of candy. I don't know why. But like, every time he's talking to someone, he just starts passing out things like like, yesterday. He's just like, your have some candy. And he just starts pulling things out of his pocket. And it's like Santa's secret bag of toys. Just more than more than more candy comes out. So Charlie, do you have candy right now? I can I just just one piece for the camera. Just one piece for the kid.

**Charly Batista**  
I got to use the Fourth Amendment.

**Matt Yonkovit**  
So the Fourth Amendment is the right to bear arms right now. That's the second amendment of exactly No, no search and seizure. That's the fourth document

**Charly Batista**  
and the first one that don't have to do anything. The first the First Amendment says you don't have to do anything, as I tell you anything that can compromise. So I don't really remember the ipsilateral things that yeah, the first one. Okay, no,

**Matt Yonkovit**  
no search and seizure evidently. Okay. So Charlie, I still remain welcome. We hope that you have fun at your PL Java talk.

**Charly Batista**  
That was nice. I might have one or two chocolate, just answering your question, because I

**Matt Yonkovit**  
didn't have a man of the people, your man of the people,

**Charly Batista**  
I might have one or two. But that's it. That was a good talk. We, we tried to enlighten people why they should use or not use and how they should use or not use PL Java code. Well, that can be quite problematic. And I hope that they they enjoyed the presentation. So for today, we have backups. Right?

**Matt Yonkovit**  
I got. That's right.

**Charly Batista**  
So one thing that I would like to to do before we start doing the backups is just to give a a short introduction about backups, right? Because we we have different what say strategies of backups when it comes to a for not only database, but Postgres, so we can do what they call logical backups. Some people they even say it's not a backup. That's debatable. And it's better to have something to do not have anything, right. So the logical backups, are they the dumps, the traditional dumps, it's very common, it's very common in in MySQL, or even non would be exposed. And also commonly an enforcer is how a lot of people, they they do backups using the dumps. So it's one strategy.

**Matt Yonkovit**  
But that's only for smaller database, it's really bigger the database, the more

**Charly Batista**  
problematic that is, it is it's true, it's

**Matt Yonkovit**  
a dump is basically just dumping all the SQL commands to recreate the database.

**Charly Batista**  
Yes, it is. Well, you can dump the structure to create the whole structure, and then you can dump the data doesn't, you don't really need to dump the insert, you can dump the full data . So it's, it's less problematic. But yeah, as you said, it's more for a small database and doesn't solve all the problems. But are we still, right? So this is one strategy. And there's nothing wrong to use that strategy that works for your business. So everything should be decided on your business. And remember, backup is really important for business continuity. So this is why you should have backup, shoulders, shoulder the back a little bit to talk about these and think why why it's important to have backups, or well, everything.

**Matt Yonkovit**  
I think that everyone realizes that it's important to have backup yet why? Because you need them

**Charly Batista**  
out why? Why do we need that woken circle? In a circle? It's important to have backup. And you need them because it's important you need

**Matt Yonkovit**  
them. Because when something bad happens, you might need to go back to its disaster recovery. I mean, like everybody knows disaster recovery, right? So you drop a database, you drop a table, somebody deploys some new code that does something wrong, you get hacked, a system crashes, your drive crashes, how do you recover? How do you restore your business to where it was before?

**Charly Batista**  
But let's say you do your backup at midnight, but at midnight, you have a backup? Yes. What happens if you drop your database, then PM?

**Matt Yonkovit**  
Well, then obviously, your backup has to go all the way back. That's why point in time recovery so important, our

**Charly Batista**  
OK and that's why we're talking about strategies now. So if we do a data on Postgres on Postgres, if you do a dump, you're not able to do a point in time recovery. Right. And that's why it's important to have the right strategy. And that's why it's important to understand why you need backups. If you didn't, if you would not talk about okay, what happens if we dropped the database at 10pm and the backups are doing at midnight every day. So, you will realize that you you need a point in time recovery, right.

Those are important points, important things that we need to understand need to realize, before we go further, then back to the strategies. Yeah, dump is still one strategy, it's better to have something it's better to lose data from midnight to 10 Don't lose all the data that you have. Right? It's it's less wars, let's not say better, it's less worse is less evil, to lose something to lose everything, right?

**Matt Yonkovit**  
Yes. I mean, like worst case scenario is you have to go back to something that's 12 hours old, 24 hours old versus nothing, you're gonna go back 24 hours. Exactly. So it can still be the death of a business. If you're dealing with financial transactions or something it

**Charly Batista**  
can, it can that's, again, why you need to understand your business as well. So what the strategy needs. So okay, this is the dump. Let's move on. Now we have another strategy, another tool that we can use that it comes with Postgres. We can use a tool named named PG base backup, to backup the database to copy the database. And that's going to be a physical it physical copy. That's a physical copy. Well, before we go, that we can do a physical copy to the database without doing anything, the Postgres has a comment that we can use the if I remember correctly, it's backup start or PG Start Backup something is a comment on that you can run on post, we can use vs route run. So what it does, it creates an entry on the Postgres logs, right, the verifiers on the logs, the wall logs. So to tell look, we're going to flush everything up to this point. And we have this mark here, this entry on the logs. And up to this point, the database is consistent. So then we mark. And when it's done, you can physically copy you can use city or seeing whatever bash command or Windows common depends on the OS you're using to do a physical copy from the database to another place, so we can do that physical backup. And when the physical copy is done, we just dealt repressors there is us there is the stat backup, that is the end backup. So adulterated food and done with the copy. So just create another mark, and it create another mark. And a backup is, is consistent, and pine. So up to that point when you created the first start, so your backup is consistent. So that's a physical backup, right? But you need to be careful, because we need to tell the database to start the backup, we need to copy things. And then you need when it's done, we need to do to the database that you finish with the backup. So you can put the another mark on the log files to run things.

**Matt Yonkovit**  
So we have a question actually. So x, y, z A wants to know, with RPO of a 15 minutes, how could you restore a single database using PG based backup.

**Charly Batista**  
You cannot restore a single database use it's a physical backup. So if you want if you really want the data from single database, you need to restore the whole backup. The thing is, the physical backup is immediately restored. Right? You don't it's not like that, because you have the data file. So you have everything. So when you unless you need to do a point in time recover. That's the next thing we're going to talk about allows me to do point in time recover. When you do a physical backup, you have the database is just the time for you to do a system CTL post restart, and you read. So remember, we have that that mark, right? So suppose we take five minutes to copy all the data. During those five minutes, Postgres is working, your application is working while inserting deleting things. So the data will be the way continue to work. When we're finished with a copy in, we spin up the database, the database needs to rollback everything that's extra, up to that point when it created them. All.

**Matt Yonkovit**  
Right, but for an RPO of 15 minutes, when in Ha strategy, maybe be a better like,

**Charly Batista**  
Route, usually. Yes. But the problem is, let's say let's say you drop in a database. Yeah, then yeah. The war to work. So if you if you have a job, let's say you have a primary and two replicas, if you drop a database, that drop will be replicated for the Raptors. So then that would not work. If the problem is okay, the data is the primary crashed, and it's a lot easier and faster to just promote one of the replicas as a new primary time recovery, a new instance and have the backup and everything. Yeah, that's faster and more resilient. But they got this, the backcap isn't a strategy for a different type of disaster,

**Matt Yonkovit**  
right? Yeah. Because garbage in garbage out. So if even if it's Not a table got dropped or an object? It could be data somebody accidentally updated. They could do something like that. Exactly. Now, I'm curious. From an from a ha perspective, or from a recovery perspective, the concept of delayed slaves is very popular delay replicas, excuse me, delayed delayed replicas is very popular in MySQL. Is that something that's an option in Postgres? Yeah,

**Charly Batista**  
it can be done. You can you can also have the lubricant postfix. But, and then it comes again, what is the delay that you need to have in your replica? Because if you're if you didn't have a person keeping constantly eyes on what happens to the database, or if we have, let's say, we have a delay replica of one hour, and it took you two hours to realize that something wrong went wrong. It didn't solve our problem, right?

**Matt Yonkovit**  
You're always pushing the limit. Right? So it's like you do it. If you do 15 minutes, and you crash it 30 If you do it, yeah, I mean, it's, yeah, it's

**Charly Batista**  
a band aid. And the thing is, we need to make sure that people understand it's a band aid, because I've seen a lot of implementation using delay replicas to replace backups. Yeah. And he's

**Matt Yonkovit**  
right. And that's always a problem, because there are two separate use cases. And it's very hard to choose which one is the right. And a lot of people implement both. Yeah, no,

**Charly Batista**  
it's, it's, it's good, the more you have for resilience, it's good, right. And I

**Matt Yonkovit**  
think that depending on the size in the demographic of the system, it's really going to change your approach. Because if you've got a system that is 10 gigs, it's very different than a terabyte in terms of like, what your options are currently. And when you talk about like, a, an RPO time or something that's really tight, there are things you can do with smaller database, you just can't do bigger ones, right? So you can backup every hour like, you can have it standing by ready to go and you just roll through the last hours worth of transactions or something for a point in time recovery. I mean, there's there's options that you could do that only make sense with the setup of your system. And that's

**Charly Batista**  
why a good strategy should always come to mind. And when you have a good strategy for disaster recovery, backup is just one of the pieces. Yes,

**Matt Yonkovit**  
yes. Right. Absolutely. So

**Charly Batista**  
when we're thinking of a high availability, you need to have the option to propose one forward, we need to have the option to recover a backup, because we have many different types of, of problems, or disaster is a disaster. So maybe you have three database nodes in our AWS region, and the whole region goes down. That's probably Yeah, yeah, it happened in the past last year. So it's not something that you can tell I will never happen, because it did. Yeah. Right. So if you do not have any strategy for those kinds of problems, then you run out of business.

**Matt Yonkovit**  
Indeed, you do. Indeed.

**Charly Batista**  
So and let's say you have the backup, you have, you have the backup, you have the three nodes, you have a Dr. site. But if they're all the same region, if the full version goes down, you lose everything.

**Matt Yonkovit**  
Yeah. Yeah. I mean, that's totally obvious. Right. Right. And yeah, so this is where that that becomes critically important. Let's get back to the backup backups. Because I know people are people really want to see us go through that process of setting it up and configure it. But you've only talked about two backup methods. And I think the third one is where you're gonna go with this.

**Charly Batista**  
Well, we Yeah, I was told Yeah, I now the next one is the evolution of the second one, right? So yeah, each of these backup bait bases is the one that we want to implement today, because we need to understand how PG based backups works on Postgres. Actually, I want to do both, I want to do the manual one as we have a small database, so we can do the manual one, because what PG base backup does is just does the automation of what to do manually. So the PG base backup, it goes to, to the instance that we're backing up, it opens the backup, it creates that line, right on the logs to tolerate a nice look, and that cannot. And then the PG base backup, it copies all the data for whatever price we were telling the PG base backup to copy. And when it finishes, it goes back to the database and finishes the backup. Right. So instead of doing that manually, it does automatically for us. So that's an evolution of the process is an automatic automation of the process, right? Yep. And it's important to understand how those work because on the next session we're going to talk about PG backrest. Because it's it's a really nice to that does. Mostly this does the same thing, but with a lot of improvements. And with PG backrest we, if we have time today, we're going to do a point point in time recovery today using PG based backup, because we need to understand how that works on on the database. And on the next section, we're going to also do the same using PG backrest. And one thing that is cool that's really nice on the PG backrest is because you can have a database backup server, you can have a backup server on the PG backrest. And it can coordinate the backups. Why no have backups from the replicas and have backups for the primary. And if you have multiple sites, you can store all those backups on the same site. And PG backrest can also duplicate those backups. Okay, there's a lot of automation, but this evolution right so let's start easy. So i gonna I need to connect your database, or Charlie dB, you just realize it now.

**Matt Yonkovit**  
He's out in the Charlie DB node. Everyone

**Charly Batista**  
got arms? Curt No.

**Matt Yonkovit**  
Well, that's because he broke it last time. And I changed the name just so I totally

**Charly Batista**  
fit all our codes. I didn't crash anything that was all my fault. It's your database. Even though you call Charlie dB. It's still

**Matt Yonkovit**  
Nope. Name. It's like putting your name on a toy. Once you do it, you own it.

**Charly Batista**  
So one thing that I'm going to do here, I want to go for the Postgres SQL to documentation here for Postgres backup. So Backup and Restore. This is the truffle. So the source of truth for things that we use on posters, right. So everything that you do, it's always good to to go for the documentation. The post use documentation is really reach. Sometimes the language is not the most accessible one, sometimes it's hard to understand. But the documentation has almost everything that we need to understand for four football stories. And as I usually stop people after Google being vented, I don't remember anything on top of my mind. So I need to go for the comments. So what we want to do here is the file system level backup. Oh, just to show here, here, we have the dump stop still started for the backup, it's not the best one, we're not going to do a dump. today. We're going for the file system level backup. So the most common things to do is to just copy the data, right? So a question for you. Is there any problem to just copy the data dear? Let's say do this 30 year old are synced from data D to an OtterBox? Well,

**Matt Yonkovit**  
of course, if it's shut down, and everything is cold, then that makes it a more feasible option. Okay. But if it's hot, then data is going to be inconsistent when you bring it back up. Why? And it won't even come back up because things are in flight and they haven't been written. And as the data is being copied, you're gonna get things at different points in time across all of your data files.

**Charly Batista**  
Yeah, that's where possible, the thing is, it's also possible for you to be lucky enough to to get the consistent data at that point. But that's a lottery.

**Matt Yonkovit**  
Yeah. One in a million.

**Charly Batista**  
That's a lot. Yeah. I

**Matt Yonkovit**  
mean, I guess it would be if your systems are maybe there's a little bit better chance than one in a million. Yeah, but I can't imagine anyone would know.

**Charly Batista**  
That's that's the thing, because I've seen people being lucky. They weren't using that as a strategy. And to tell me for Luke, there is no problem we can copy the database at any time at any point.

**Matt Yonkovit**  
Wow. No one watching has anyone watching tried to do a backup that way? Like I can't believe that don't get

**Charly Batista**  
fooled, because it's just a lot or just sad. It's one in one gig. Right.

**Matt Yonkovit**  
And I think you're exaggerating that people actually did that be good qualified.

**Charly Batista**  
I've seen horrifying I've seen. So yeah. And that's why we are the need to shut down the database. While we don't want to shut down the database that's bad for Okay. Every time you need to shut down a database, it's not good. But we we need to. Okay, the comments I'm looking for are all this here. That's hot backup.

Making I don't want to make a base backup. I don't want to archive at now. Not yet. Here is PG stop backup. This is the guy that was looking for. Do you have the loading on the database to have the whichever database the load? Yeah, there's load. Okay, so we Have right? So if

**Matt Yonkovit**  
we went to PMM right now, you would see that there is a significant amount of load on that box.

**Charly Batista**  
Okay, I trust you. Because I don't want to back up an idol instance. Right. So we want to show people that I'm gonna go double check,

**Matt Yonkovit**  
but pretty darn sure I'm darn Darn tooten. Is that is that a phrase that you would Darrin today? I mean maybe I'm just in your cowboy mode or something.

**Charly Batista**  
old dude. I'm

**Matt Yonkovit**  
not that old cheese. Oh, pizza, like just killing me, man. Charlie, you're almost my age. So you're old men.

**Charly Batista**  
know one thing doesn't change the other. Yeah.

**Matt Yonkovit**  
All right. So I can tell you right now there's about 75 connections active, we're doing about 4000 queries a second. And response time is around shoot anywhere from five to 10 milliseconds. Okay, getting on the quarry. So when you back up, we can actually go through and take a look at what's happened in there. For instance, yeah, if, if people are interested, I'm happy to show the PMM screens before and after as well.

**Charly Batista**  
Okay. So what I'm going to do here is I'm going to use the PG back base backup. So as we saw in the pre rolls page, we're using three parameters. The first one is the label. This is what tells the database look, I want to backup and I want you to call this point here, this label, it's where how can I were given it a way meaning that backup right for for the data is we can go back in time and check the configuration later that defies actually the to see what the label is. So let's start doing those things. For this one here, I need to connect my database, actually your database, su dash Postgres,

**Matt Yonkovit**  
you said your database, that was mistake.

**Charly Batista**  
PS quo. So I go on here, and I gonna label each as backup 00. Right, as we can do more backups. So it will take some time. Remember, we have load any needs to flow, Shani to make everything consistent at this point in time, remember this expression, the backup is consistent with this very point in time.

**Matt Yonkovit**  
Right. Right. And only this point in time. Yes.

**Charly Batista**  
And also have loads probably have a lot of things that needs to be flashed. And can you check the PMM the checkpoint? You might have a spike of the checkpoint on your PMM

**Matt Yonkovit**  
I'm guessing I will but I have to go there.

**Charly Batista**  
Yep. And if you could show people, I would appreciate

**Matt Yonkovit**  
it. I'm going to show people Oh,

**Charly Batista**  
yeah, they want to see the checkpoints and all we want to see

**Matt Yonkovit**  
is driving me nuts here. So one second.

**Charly Batista**  
If you take too long that the PG stop backup gotta

**Matt Yonkovit**  
remember as it has a history so that it doesn't matter. Like your your backup could finish. Yeah, and it would not impact us at all. So you're sure? Yes. So no, there's actually no checkpointing right now. But it could be that I just need to just time let me make sure I'm on the right instance.

**Charly Batista**  
Yeah, that's also a good one to know. Ah,

**Matt Yonkovit**  
yeah, these are checkpoints dates are zero right now and I'm on your I'm on your I'm under the Charlie maybe men. So right now checkpoint stats are pretty darn stable. Oh, but could you be waiting on other things to finish up? It could because it is a pretty busy box.

**Charly Batista**  
One thing that I want to check here let me connect to this box like you did set

**Matt Yonkovit**  
it up. So if there is a problem

**Charly Batista**  
I don't know anything

you don't have IoT up here yeah, that's quite easy box.

**Matt Yonkovit**  
Yes. Look at that box. Go. Look at that box. Go. So it's it's rockin and rollin. Right.

**Charly Batista**  
It's that and right apt cache. Good afternoon. I yield. Okay. apt get install.

**Matt Yonkovit**  
Now I can also turn off the workload if you want. But I don't want

**Charly Batista**  
it's fine. Well, when people are backing up their system they do not stopped application.

**Matt Yonkovit**  
So, Charlie, yep. You realize you're on a different box am I? You're on a different look at your to look at your two tabs. You got one 131 connector, you want to leave it there. So yeah,

**Charly Batista**  
I got it. I got it

**Matt Yonkovit**  
for Charlie.

**Charly Batista**  
Thank you Okay, do we have a top on this one? Well, if t get just the keys,

**Matt Yonkovit**  
though, and then x, y, z A also wants to know, can you encrypt your backup while it's happening? Not using the PG base backup but you can with PG backrest Yes, we can use we can encrypt using PG, PG backrest is an option. If you want to encrypt while taking a backup but not

**Charly Batista**  
well, you can have some workarounds because it can bite the PowerPoint to

**Matt Yonkovit**  
backup through.

**Charly Batista**  
But that would be horrible.

**Matt Yonkovit**  
Like, yeah, that's got to be a lot of latency here. Yeah. So I would say there are tools for that. But if you want to use just the base, I think that's going to be a problem. Because right

**Charly Batista**  
here, remember we're doing manually here we are not using PG base backup. At this point, we are doing our seek or TA whatever thing Yeah, so we can encrypt that. We can use PGP to encrypt the file

**Matt Yonkovit**  
staying. It's not encrypting in flight. It's encrypting. When it's done.

**Charly Batista**  
You can pipe them to the PGP. And it's still

**Matt Yonkovit**  
Yeah, it's still a roundabout way.

**Charly Batista**  
But it's possible answering yes, it's possible.

**Matt Yonkovit**  
Okay, fair enough. Fair enough.

**Charly Batista**  
Well, your box has some problems here.

**Matt Yonkovit**  
This is not my box. This is Charlie dB.

**Charly Batista**  
dB stock not found what that means.

**Matt Yonkovit**  
So for those of you just joining us this week, and you want to learn about backups, this has been a five week journey with Charlie, where we actually started the first live stream of him installing Postgres. And then we went through configuring it, we went through setting it up, we went through doing some tuning. Last week, we talked about what we should be alerting on and monitoring on and we talked through the alerts. So that was two weeks ago. So we're now at the point where we're going to do backups. And then in the future, we'll do replicas will do ha will do all kinds of other stuff. So whatever Charlie is seeing here is something leftover from one of those other streams, therefore, Charlie's fault.

**Charly Batista**  
I'm not going to comment on that.

**Matt Yonkovit**  
Oh, I know that kind of hurts. So So here, not some candy.

**Charly Batista**  
I have my own veins. Thank you. it's very unpolite to give the candidate what you asked. Yeah, well, no, I

**Matt Yonkovit**  
have more candy. You want some candy? I'll give you my candy.

**Charly Batista**  
Okay, that works that we're now now we just hurt my feelings. Because so where's your backup? I mean, the backup might be done by now. No, it's not see, the checkpoint are here. It's taking a lot of time. Also us with the background writer, they're writing things, we have a lot of things that need to be flushed in memory, and, and all these things. And one thing that you might be suffering is the IOP is from AWS. Right, as we start seeing it, as your instance has limitations, or

**Matt Yonkovit**  
Yeah, yeah. Yeah. Great. Yeah. So the checkpoint

**Charly Batista**  
is going to be 959 7% of the aisle. Right.

**Matt Yonkovit**  
So it's a busy box, but it's also eight, this is SSDs with 1000. Yeah, so, I mean, it should be a fairly decent box, eight, eight cores. 32 gigs of memory. Yes, Ronald, mo, rodelle. Long time. Yeah, you can go back, you can watch the other ones there on YouTube, LinkedIn, or wherever you're streaming twitch. We also do this for MySQL. We're a little earlier in the journey on MySQL than we are on the Postgres side. So, and if we run out of time, today, what we're going to do is we'll come back and we'll do a special live stream to finish up the backup stuff. Before the next one.

**Charly Batista**  
Do you want to speed up stuff stopping the log just for the purposes of the, the Okay, so, but right

**Matt Yonkovit**  
so that I usually asked me because he didn't set this box up, right to go in and reduce the workload a little bit. So I'm gonna go ahead and do that for him. Give me a second here, Mr. Charlie, while I go into the magic workload, and do this what you're the one who asked for some assistance because By the way, there is nothing but love between me and Charlie. even though we joke we joke because we we like that. You should see some of the videos we got coming out yesterday when he was breaking stuff in here. Like what was it was it well, pretty good? Yeah, it was pretty good. All right. No, what's going on with this? So

**Charly Batista**  
I think it's not working, though I mean, what are you talking about? You just ask what's wrong with this?

**Matt Yonkovit**  
Yes, yes issues what do you have

**Charly Batista**  
water here?

**Matt Yonkovit**  
I have water. But you don't have water?

**Charly Batista**  
No, that's I'm asking. I have some some stuff here. So what is that?

**Matt Yonkovit**  
Of course it's chocolate. Like I said he brings copious amounts of chocolate in here. Do you have water? I do.

**Charly Batista**  
My chocolate. Thank you. It's like

**Matt Yonkovit**  
$5 A bottle that feed the bulk say yeah. Sheep water because because I couldn't get it. There's nothing around here for for that. Right.

**Charly Batista**  
So one day we're going to be a boss and be a boss. Oh, yeah. When you're a boss.

**Matt Yonkovit**  
Yeah, you get to buy the fancy water. I'm sure that's what that was. Yes, I gave Charlie my only bottle of water that I had in here. Because he was parched down.

**Charly Batista**  
For the talk about childhood stuff.

**Matt Yonkovit**  
Hey, you chose that topic?

**Charly Batista**  
I well, I chose the topic was the committee submitted the topic but yeah, they Jas

**Matt Yonkovit**  
Okay. So. Alright, so the workload should be dying down now. In a couple seconds.

**Charly Batista**  
Okay. Yeah, I still have 100% checkpoints in background writer.

**Matt Yonkovit**  
Okay, so. Oh, there's an auto vacuum. Oh, wow. Auto vacuum rotten. Yeah. PJs on test, of course. Because that's just a massive table. That's our biggest table right there. So workload should be dying down, though. I mean, I mean, I didn't feel it out. I can do about that. Let's

**Charly Batista**  
let's just give it a few minutes. So as we are waiting here, let's go back and talk about the backup strategy is right.

**Matt Yonkovit**  
Yeah, by the way I got sits we're waiting for a backup. What does the hos mean? So rattled the house is the head of open source strategy. So that's my official title. So I can do what was it? Didn't say anything. You said something. I'm gonna go back and listen to it on video. I don't know who caught that. But. So the Haas rhymes with fosse so I can do the Haas talks Fosse. And that's why I have that title. Only because it rhymes. It's personal branding. It's worthwhile. Yeah. Like, I don't know if you knew this, but Charlie's official nickname is Charlie and the Chocolate Factory, because he just keeps on pulling chocolate. Chip. So yeah, I'm just gonna kill the workload. For this, I mean, it's partly I just wrote it down to like nothing. But obviously

**Charly Batista**  
committing idle. Well, that's good. That's happening. Because from the backup strategy, you also need to take in consideration how long the backup gonna take? Yeah, yeah. Right. So you don't want to run your backup during the peak load? You always try to run the backup, when it's not big. Well, this is why you

**Matt Yonkovit**  
would also go to replica. Yeah, right. And so backing up on a replica versus primary primary, that might be something as well. So So Charlie, how big is this database? Now, because we've been running this for over a week. Now. It might have grown to a significant size, but it shouldn't have grown that much. But you're right, there is probably a lot of transactions that need to be flushed for the backup to work.

**Charly Batista**  
Or is there a database?

**Matt Yonkovit**  
You're the one who set this up? And you try to remind him of that. I don't know why he forgets that. Like he forgets that he's the one who's I'm just the facilitator. I'm the horse. I'm like, the the fun guy. He's the guy who is supposed to like do the work on these things. While

**Charly Batista**  
we have the eight gigabytes of NOC data, but inside of the big O,

**Matt Yonkovit**  
we get another question, what does the checkpoint or do while the backup is running?

**Charly Batista**  
That's a good, that's a good question. But to answer that, what is the checkpoint? That's my question for you what's a checkpoint?

**Matt Yonkovit**  
checkpoint is one of your going to flush the pages out of memory into into disk, you're going to make sure that it has arrived in the data file correctly, right. It's going to clean up the transactions that have been going on

**Charly Batista**  
Yeah, and if we go, if we talk how the database works, they do not save the data inside of the data files. When you do we commit the transaction, right? Because that's unsafe. So if something, let's say you're inserting the data, you're inserting the data, the user and a password and something. If something happens, when we are writing that transaction to the data files, you get a data files, the data files are inconsistent. So the database or the database, they use any strategy that they first write that thing for a lot of files, in the case of Postgres, that wall files, and all we do OGS or so they're the binary logs, right? So they start you that database use, they can vary, but like their binary logs. So usually, those logs are sequential the database, they pre create those files, because a lot faster to write sequentially than randomly. So you write those data to those logs. And then when you commit the transaction, at some point, the database needs to get those data from those walks and apply to the database. Right, right. So the checkpoint, this, all those things, they forge everything that is in memory, to the disk. They also depend on the strategy of the database, they will also copy those data from the transactional logs to the data files. And that's why sometimes it takes so long, but sometimes it's so expensive, because well, how much memory you have here you have like, eight gigabytes memory for, for the data for the database, right? It's allocated eight gigabytes memory should not be that slow. But we have if we have some a lot of transactions, that not being pushed to the data files that can cause a lot of time for for them to to copy that data files.

**Matt Yonkovit**  
So and so that it's 50 gigs now, right? Is that what you what you just did? Yeah, it is pretty big.

**Charly Batista**  
Well, but it's 50 gig. If the log files and the data files. This is true, by just not only the data set, the data set, probably going to be half.

**Matt Yonkovit**  
Yeah, by the way, we had it we had a request to include an Oracle to PG migration discussion in the future. So maybe we'll bring in a hobby or something.

**Charly Batista**  
Yeah, that's that's, that's a good bulk.

**Matt Yonkovit**  
 always a good topic, we're also going to have if you're interested in that topic. Percona live is going to have a workshop on that coming up in May. So there's going to be a tutorial like a three and a half hour tutorial, or a three hour tutorial on it. And then there's also going to be an hour session. Tutorials aren't going to be recorded, but the sessions will be in they'll be available in the month or so following what did you do?

**Charly Batista**  
Stupid? What did you do?

**Matt Yonkovit**  
All right, you heard it here. First everyone. Charlie just said, I am stupid. Not me. He said he's stupid. Okay, which implies that I'm the smart one here, which is awesome. I'd love to be the smart one. I like to be the person who's Yeah.

**Charly Batista**  
So let's go back. Let's go back here to understand what the PG Start Backup does. We have three parameters, right? You have the label. So it's just a nickname for the backup. And we have another cube parameters. We have this one that says fast. And that Wallace says exclusive. What do they do?

**Matt Yonkovit**  
I'm gonna guess that exclusive is going to wait for it to be idle.

**Charly Batista**  
Yeah, let's let's see if you can read. Well, they do.

**Matt Yonkovit**  
Yes. So So you tell us because it's so tiny on my screen that I can't read. So just tell me what it is what I mean, like it's tiny on my screen because my screen is limited.

**Charly Batista**  
Let's go here. If the optional second parameter is given as us as a true, it specifies executing PG stock back up. It's as powerful as possible. Yes, we put false.

**Matt Yonkovit**  
So it's going to wait, this force

**Charly Batista**  
an immediate checkpoint, which will cause the spike in IO, but it's low in everything but got to be as fast as fast as possible. The optional third parameter is specifies whether to perform an exclusive or non exclusive backup. Yeah, we don't want an exclusive backup. That's true. So we should put as a false, right. So but now we're waiting for the we're not forcing the checkpoints.

**Matt Yonkovit**  
So you're waiting for all the checkpoints to eventually catch up. And then You will take it when they are caught up, which could take

**Charly Batista**  
them minutes. I don't remember the configuration can take one hour, if I remember correctly. So, so let's cancel.

**Matt Yonkovit**  
So by just canceling that it will cancel it, it won't queue it up. It won't leave it in a state that is there's like one just sitting in the background. Let's check it out. You don't know.

**Charly Batista**  
Oh. We're going to find the answer quite fast. If it works or

**Matt Yonkovit**  
not. Yes, we'll find out quite fast if this works or not.

**Charly Batista**  
And let's see what the truth changes. Well, we don't want an exclusive one, but we want it to force the checkpoints. So let's check again the IO top. And here we go again. You still have the just out of arco.

**Matt Yonkovit**  
It's working its its tail off, isn't it?

**Charly Batista**  
Yeah. Well, at least the shag pointer. It's on top here as well.

**Matt Yonkovit**  
Well, yeah. But the discreet for the auto vacuums at like two Meg's a second. Yeah. I mean, it's not a huge amount, but it's still pretty high compared to everything else. So that's plugged along.

**Charly Batista**  
Yeah, and probably these guys preventing my backup for now.

**Matt Yonkovit**  
Shows you auto vacuum.

**Charly Batista**  
By the way, we are going to talk about vacuum

**Matt Yonkovit**  
later, right? Yeah, well, yeah, there's a whole thing on auto vacuum. For those who don't know what an auto vacuum does. Auto vacuum is going to run the vacuum command, which will clean up dead space. So there's there's rows and things that have been removed from the tables, and they will just leave those space, they basically mark them as deleted, and then you have to come up and clean up that space eventually. And part of the issue that you have with the Postgres system that's very active is sometimes the auto vacuum can be delayed, delayed, delayed, delayed, and you can configure that. But when it starts, then it gets pretty aggressive. And it can cause a lot of blocking conditions. So that is a potential issue. Now, here's the fun thing, part of the workload that we're running, it's part of the Yaak box. So there's eight different unique workloads. One of them is designed to actually stress autovacuum. And it's it's a it's an audit system where it logs like every request coming in, and it does some other things for 15 minutes. And then it deletes every, like everything older than 15 minutes. So it constantly adds and deletes things. So we are probably a prisoner of our own design in this particular workload. But that's cool, because this is what real people would face when they've got a real world workload, right. So if they're out there, and they're doing a heavy amount of writes a heavy amount of changes to their system, they're going to have these types of problems. And they won't have the ability to shut off the workload, which is something that we were able to do. Yeah.

**Charly Batista**  
And here, for example, you for Shaq that would just start activity, we can see the outworking is doing the IO here quite aggressively on your table. Now, it's going for the normalized users.

**Matt Yonkovit**  
Yeah, so it's going through all of the different tables and going through the vacuuming.

**Charly Batista**  
But we see the background activity. Okay. Well, and well, you asked me the cancel, right? Because I cancelled here. You asked me if that would run in parallel, if left running. Alright, let's answer your question. And by the way, we

**Matt Yonkovit**  
do have another question when that one's done.

**Charly Batista**  
Well, you just ask the question, because I need to type here. Oh, which parameters?

**Matt Yonkovit**  
Which parameters? Does PG base backup use more if I'm taking a terabyte size backup? Now I saw it's taking more IO. What if Postgres has 1000s of queries per second? Now, the server that we started on had 1000s of queries per second, but that's beside the point. So

**Charly Batista**  
what which parameters? I didn't? Can you repeat the question?

**Matt Yonkovit**  
So it's which parameters does PG based backup use more? If I am taking a terabyte backup? So I'm guessing like which one should I set for if there's a terabyte size? Now I saw it's taking more IO. What if Postgres has also a 1000s of queries running?

**Charly Batista**  
Got all the backup? We will always take a lot of iron right because we're you're copying they did later. So what can be done is we can increase the value for IO that can be flush, just like MySQL, remember that has the 200. I ups, I don't recall top of my mind the name of the parameter. But you can tell to Postgres, how fast or is low is your RDS so it can flush more, right, more or less aggressively to the disk. The checkpoints. So, ideally, we don't want to have checkpoints quite often. So we usually try to see how much data we write every 30 minutes or every one hour to make sure we have the checkpoint every 30 minutes every one hour. And during that time, the background writer will try to alleviate the checkpoint to try to distribute the data that's doing to the checkpoint. So when you get to the checkpoint, it's not a huge checkpoint, right? Even if you have 1000s of transactions per second. So he's still writing us as fast as he can to the disk. What you, you talk to the database. But look, I don't want to have checkpoint too often. But when you put a target to the checkpoint, that's the checkpoint target, you dealt with a database. I want you to try to split as even you can the checkpoint during this one hour,

**Matt Yonkovit**  
right? Yeah.

**Charly Batista**  
So this can help. Those are the things that you can change the configuration on the database to alleviate a little bit for for for those things. Yeah, we can reveal those configurations to see how that goes.

**Matt Yonkovit**  
Okay, but here's the thing you just checked, there is no backup. So did the backup finish?

**Charly Batista**  
No, no, no, no, the backups here, I just select Limit one because they wanted to call out the I don't want to see everything here. I just want to see, oh,

**Matt Yonkovit**  
I shut everything off? I don't know. So whatever you see is probably going to be legitimate back end stuff.

**Charly Batista**  
More or less, more or less? Yes. Yeah. What I want to say here is okay, select the database name. Well, the application name I want to see the went into started. Everyone just see when the crisis started. It has changed. What is the event it's waiting for its estate. And the query itself wrong. Just stop activity. So we want to understand what's happening inside of the aurora database, right? This is this is a view it's not a table. This is a system view that shows the activity of everything is happening inside of the database. So we can start here to see what is what is happening. For example, see, we this is a select we just did. It's active. It was run by the PR squirrel. It's not waiting or anything. But what is the waiting ever is the last one button just change the put the waiting event and they stayed in the beginning. Because the query is too large. It's gonna be hard to see. Okay, the wait event, we don't have waiting event here. We have some operations waiting for the autovacuum to finish. So this is when they started. What is our backup? So PG Start Backup. It's waiting on the checkpoint to be done. Alright, and do we have a checkpoint here?

Well, that was just to show people that yeah, it's running and it's waiting. You asked if we would have if I cancel them. We would have to there I didn't run right. So we maybe it was finished. We can cancel and run again. And and just check here again to see if we have to. In this case, yeah, we don't have because remember, it's blocked. It's still waiting for the checkpoint to be done.

**Matt Yonkovit**  
So the checkpoints probably stuck on

**Charly Batista**  
the DBQ. Yeah, it didn't even start says waiting for the checkpoint start.

**Matt Yonkovit**  
Yeah, yeah. So where are your backup is blocked. So we've we've effectively found that we're waiting on auto vacuum for everything to free up. So this is one of those.

**Charly Batista**  
Can we kill all to vacuum? Who Whew.

**Matt Yonkovit**  
I mean, you could disable it, but if it's already running, I don't know if you couldn't kill auto that sound good. I don't know. That's like so you can disable auto vacuum, which is not recommended. And you can run vacuum on your own. But But I don't know if you can kill it. If it's active. You could probably kill the database.

**Charly Batista**  
No, I don't want to kill them. I'm

**Matt Yonkovit**  
just saying like, like, you could like to get rid of autovacuum. But that's a good question. I've never I've never tried. But yeah. Can you kill autovacuum? Let's google the question.

**Charly Batista**  
Yeah, we can. But how

**Matt Yonkovit**  
are you asking? Because you don't know. Are you asking? Because you want to make me look stupid? I

**Charly Batista**  
don't know. But I also want to make you stupid.

**Matt Yonkovit**  
Thank you. I appreciate your candor there. You can disable the auto vacuum for a specific table. Danger and killing so let's see. Yeah, you can't you can't I don't we can't Yeah, well, then why?

**Charly Batista**  
But it's a rhetorical question. But how can we kill Healthwatch Do you want to know how Yeah, of course I want to know how I wanted to see what happens if we kill off the vacuum here

**Matt Yonkovit**  
it's select PG terminate back end and then though

**Charly Batista**  
the backend IG Yeah, but you do that? Yeah, how do they get the back end? I do. Well, we need we need to keep okay, I It's Select Select PG. back and kill right. Now, what is the common

**Matt Yonkovit**  
PG terminate back end oh and terminate terminate underscore terminate underscore back in and then the minute now that's it should be canceled back end it should be instead of terminate. Looks like I was just looking at this and somebody had asked why doesn't this work and no, I guess terminating canceled vote does there's a small chance that before canceling the call to wrap around the emergency shutdown of the database.

**Charly Batista**  
Yeah, no, that's that's the wraparound. That's not all. I believe. Yeah. That's good. That's good. You're reading you're trying to understand how that works. Oh my god. Here's one send you since this is just good. Now I need the the ID How do I get the ID?

**Matt Yonkovit**  
Well, isn't that in your recording that you didn't run? It's like what are the columns you ignored? Isn't that the

**Charly Batista**  
soul? It's what it's it's the PID here that we mean?

**Matt Yonkovit**  
I don't know if it's the PID or the dad ID. Which one has it?

**Charly Batista**  
Is the PID?

**Matt Yonkovit**  
Is it the PID? Charlie, you can just execute the commands. Charlie drives me nuts. Sometimes I tell you what.

**Charly Batista**  
Hold on. I need to find a k x ID what does that mean? I'm gonna Google what to get the oh, let me show you something here. Before we go that remember we did IO top all the way

**Matt Yonkovit**  
back and X ID represents the transaction identifier.

**Charly Batista**  
Remember when I showed automatisms ah, well done. I didn't have the chance to kill

**Matt Yonkovit**  
the vacuum finished. Yes. Okay. Yeah. All right. There you go. So done. So we've got the backup done. We had

**Charly Batista**  
that up let's go on. Sorry. Apologize. That was

**Matt Yonkovit**  
all I was gonna say. So we got that done. The vacuum eventually finished its background process. The checkpoint need eventually caught up evidently. So we had a kind of a multiple whammy effect which could happen very easily in a production environment. If it's scheduled even like a scheduled backup. You might schedule it for midnight. Yeah. And it might not actually happen till three o'clock. So that's something that you want to be mindful of and definitely came up with the workload

**Charly Batista**  
back, please. Of course, because we want to backup with workload, how much workload Do you want? 50 per sounds like we're backing up at midnight.

**Matt Yonkovit**  
Like we're backing up at midnight, midnight.

**Charly Batista**  
Well, the auto vacuum is finished, because you're attracting them to kill

**Matt Yonkovit**  
it. You want to kill the auto that's a different topic for a different day. Don't stay on topic, you're supposed to be showing people how to use backups. And all you've done right now is show people how not to do backups. I mean, we've we've we've actually, we've actually had quite a bit of non non backup time here.

**Charly Batista**  
Your your box

**Matt Yonkovit**  
is not my box. No, it's not my box. Box, your box. It even has your name on it.

**Charly Batista**  
But it's a good thing that we need to go through the vacuum stuff.

**Matt Yonkovit**  
Yeah, no, it it actually is a very good real world example of why vacuum causes such craziness, if you will, I think that's often overlooked.

**Charly Batista**  
Yeah. And remember, it went faster from it would have been done without killing the workload. Right? Right. So if we didn't kill the workload, I'd still right into that fabled outwork him could take even longer. And that's it's important when you're designing the backup strategy to take in consideration those things.

**Matt Yonkovit**  
Yes. By the way, we're confusing people. All see the latest comment? You've confused them?

**Charly Batista**  
And I don't see a lot. Let me see the common

**Matt Yonkovit**  
Oh, yeah, it's getting confused. Can you repeat how it's done and start from the beginning?

**Charly Batista**  
No, that's easy. So I can just run the the stop here. Let's just get the back. They stopped backup. So what we need to do is, or K, select PG stop backup.

Okay, we'll look for the database. We just finished one backup, right? Even if we didn't copy anything, now we're back to be starting point. Let's do they. They start back up. Kevin, if the same name.

**Matt Yonkovit**  
What do you think? The probably? Does it overwrite it or not? That's my question. I don't know that. You know the answer. So why are you asking me? Sure. Should I just press enter? Yes, just press Enter. And then you could see what happened? Yeah, I just started a

**Charly Batista**  
new one. Yeah, and it overrode it. But overall, what? Where is this information?

**Matt Yonkovit**  
The previous backup, right?

**Charly Batista**  
Yeah, but why? Where is this distort? I'm inside of inside of the Data folder. Right here inside of the Data folder. We have this big wall. And inside of this big wall, we have a load of files. Not that many.

**Matt Yonkovit**  
There's a decent amount, right?

I mean, what is it is? Yeah, I mean, it's not massive.

**Charly Batista**  
Yep. So what happens here see these information here that the PG backup says, These is the last, we can find the wall file and the transaction ID that was writing the last one that was committed and flush to the database with this information.

**Matt Yonkovit**  
Right? Yep. By the way, yes. question did come in a bit ago. When will PG base backup support incremental backups?

**Charly Batista**  
Well, it technically does. You said technically, yeah, we all know worse, we're gonna run through those things.

**Matt Yonkovit**  
Okay. Okay.

**Charly Batista**  
All right. And what is the difference? The difference found incremental. And what is the other one? Differential or differential? What is the difference between differential incremental

**Matt Yonkovit**  
you're going to track The incremental changes versus whatever the delta is between the two points.

**Charly Batista**  
Can you elaborate on that

**Matt Yonkovit**  
one, you elaborate it, I'm trying to get your frickin workload up.

**Charly Batista**  
was a really did not and it's not right.

**Matt Yonkovit**  
Now incremental is you're going to track the changes that are happening. And so if you have like a change to a record that is like it goes A to B to C, you'll get A to B to C, and then the differential if it goes A to B to C, the differential would be A to C. Okay. Does that make sense? No, it does. Right? So it's it's

**Charly Batista**  
okay. Yeah. Elaborating on your answer. Yeah, that's correct. So let's say,

**Matt Yonkovit**  
Wait, you knew the answer, but you play dumb. Stop that. Knock it off your thread? I'm throwing things at him because I'm in the same room.

**Charly Batista**  
That's driving me nuts. Yeah, your workload is back. Okay. Thank you. No,

**Matt Yonkovit**  
thank you.

**Charly Batista**  
Okay, let's say we have a backup on Sunday. Yes, we do a backup on Sunday, we full backup, we backup the full database, just like we're doing now. Okay. So on Monday, we can just do a backup of the changes that between Sunday the full backup and Monday. So only what was changed. We don't need to do a full backup again. Right. On Tuesday, we can do again, all what's changed it from Monday to Tuesday. And then so those are incremental ones, right by increment. Tin them gradually. We always compare with the previous backup. Yeah. So if we need to recover, we need we have to recover the full backup. And then Monday, Tuesday, Wednesday, whatever how many incremental we have. Okay, where's the differential? The differential? We take the full backup on Sunday. Right? Right. So on Monday, we compare what was changed from Monday to Sunday. On Tuesday, we compare what's changed from Tuesday to Sunday. And Wednesday on Friday, we called power was changed

**Matt Yonkovit**  
from five to differentials actually get bigger over time. Yes, incrementals. You have to roll through the incremental so you're going to

**Charly Batista**  
you have paused all the pills are the incremental backups, the backups, they are faster to do the backup.

**Matt Yonkovit**  
Yeah. Right. Okay. So want to see,

**Charly Batista**  
okay, let's do here we were we have space through the root filesystem, as in our case, we do have 137 gigabytes. So I just gonna I'm running as a root. I ground I just create a folder name and backup. My simple so and I gotta do the chown Postgres because they want to use Postgres for that folder. Okay, su dash post Greece. Okay, now I go on to create a backup for today. What is today is whatever just call backup one. BK p 00. signed off. Back. So here is where we want to put our backup, I want to do the verse the most simple one with our sink or var out front of our lead post race 13 going to copy everything inside of Postgres 13 to backup zeros or one. So that's it. I'm doing the backup. Right, I could comprise and thing but the simplest way is just copy files. So those are my backup, as I told to the database that I want to start the backup. Now it's safe for me to physically copy the files, even if the database is running, even if you have the the workload running, so it's safe for me to just copy the backups. Okay, right. So, okay, we have to wait for it to finish. We're talking about incremental and differential right. So what are the pros and cons? Well, the incremental as I was saying, it's faster to backup. But as as us further you go from the base backup or domain backup, the more pieces you need to recover, right? So then it is the recovering process is is lower, because you need to recover the main backup and then the backup the 12345, or how many days you have for the incremental ones, the differential backup, they start growing as the time passes. So the backup from the first day gonna be quite fast, the second day gonna be slower and slower and slower because you have more data. Because you compare, always compare that day from the full backup. But the thing is, it's a lot faster to recover the backup because now we only need to recover the full backup and the day that the last day all a fix whatever they want to recover from that timing point. Right. Those are the pros and cons that we can use for for differential and incremental backup. I told you, it's possible to use incremental backups with PG backrest. So you can do a full backup like we're doing now. And you can use your files to do a point in time recovery. It's incremental. So you save the wav files are ready for also the wall files. So when you have incremental backups, if you

**Matt Yonkovit**  
just rolls through the wall files to catch up,

**Charly Batista**  
yeah, exactly. So it's technically possible.

**Matt Yonkovit**  
Your backup is still running? Yeah, it's

**Charly Batista**  
50 gigabytes that copied? It depends on the speed of all the LTO disk. If that's as low as it is quite as low

**Matt Yonkovit**  
for vacuum. We cleaned up any of that. It'd be interesting.

**Charly Batista**  
We should have looked. Yeah, we can do. I mean,

**Matt Yonkovit**  
thank you most working hard. You never know. You'd never know. Well, you never know. So okay, jelly. So we're running the backup now. And we'll see how the backup ends and what we got to do to end the backup in a second. So if we wanted to backup just the wall files, okay, how do we do that? Is that? What's the process for that?

**Charly Batista**  
Well, the database, Postgres has a process that can help us to do that. Right. So that's the archiving. So, and ideally, we should have archive, the archive mode should be configured to archive the the, the Demo files. So what it does, it's as we are writing to the disk, the database, just run a comment that you tell in the configuration file, we can go after we finish here to see. And the colon can be just an R C, or CP, as simple as that so and the database will continuously archive in the wildfire in our behalf. So it can be just done automatically. And that's the ideal to do. We should always have the archiving mode on for at least for the primary. And we should have its archiving for safe reports. And I know I have a question for you. Oh, no,

**Matt Yonkovit**  
no more questions for me. Ah, okay. I gotta talk coming up. We have there.

**Charly Batista**  
We have the guiding mode on besides the backup and point in time recovery. And so what is the other point, which is important to have the archiving mode on on Postgres

**Matt Yonkovit**  
stage? State your question again?

**Charly Batista**  
Okay. Why is archiving important for Postgres archive into all files besides the backup? Why is it important to to copy the world files to a safer place to backup

**Matt Yonkovit**  
them? Well, I mean, those are needed for crash recovery. Right? Yeah.

**Charly Batista**  
But let's forget about crash recover. And those are backups. So what's weird about backups? What's the auto situation? They're important?

**Matt Yonkovit**  
Compliance, maybe. So he has this he has this answer. Look at the smug look on his face. Just answered the question.

**Charly Batista**  
The replication

**Matt Yonkovit**  
Oh, well, yes. But we're not talking about replication. Yeah. No, no, I asked, and why

**Charly Batista**  
are they important? And so if you give people more reason to use, then people gonna start to use that.

**Matt Yonkovit**  
Oh, science. Yes, yeah.

**Charly Batista**  
But why are they talking for replication? Because that's

**Matt Yonkovit**  
how data is going. It's going to replicate the wall files over and start replaying them basically on the replica.

**Charly Batista**  
But why should that keep them? That's my question. Why should they archive them? What is archived? Impossible. Archiving is just copying the wav files from the folder is to a safer place. So why should we archive them for application purpose? Why why is it DataPort

**Matt Yonkovit**  
Because replication is async, and while files could be deleted or reused or changed in the primary, right, yeah. But yeah, you

**Charly Batista**  
have a replication lag. And that well file that you need has been replaced or deleted or

**Matt Yonkovit**  
rattled, said pointing time recovery as well. But I mean, like, that's your backup, and you're saying no to backups, but whatever. Yeah. Yeah. Ha ha ha thing? Yeah. It's the replica.

**Charly Batista**  
Yeah, the replica. So if if your replica, their replication lag increases, and you need to apply that will files. So depends on your configuration that you have on the primary, the primary can claim up to all files, right? And the replica depends again, on a configuration can clean up too fast. There are other points that prevents but that's not the thing. So if you remove the the wall files, the replica is not able so then you need to rebuild the replica. That's why it's important. Yeah. Because yeah. And you still coffin I need a faster disk, man.

**Matt Yonkovit**  
You're the one who told me to put workload on it. So

**Charly Batista**  
this is not nothing about the work. Well, this is the disk. This is all?

**Matt Yonkovit**  
Well, no, because you're contending for this guy. You're writing to the same disk you're reading and doing everything for if you could have, you could have Why does as the person say he didn't bother? Why didn't you give me an extra disk? You could have asked

**Charly Batista**  
for one? I want an extra disk. Can you give me an extra? Yes. Okay. So next session, we're going to have an extra this that we want to backup.

**Matt Yonkovit**  
You own this box? It is Charlie dB, no matter what, like, you can do whatever you want. I don't have

**Charly Batista**  
access to your AWS account to add an extra disk. It's I know, it's he's trying

**Matt Yonkovit**  
to make excuses. Everyone. Don't listen to Charlie. So he had to access.

**Charly Batista**  
Can you attach a new disk? To this?

**Matt Yonkovit**  
I will? No I will. Okay,

**Charly Batista**  
thank you. So yes, there gonna be a disaster. Well,

**Matt Yonkovit**  
okay, so we've got to put some boundaries on here, because we're approaching an hour and 30 minutes here. Because at

**Charly Batista**  
first, we are waiting for our cube. So it never finished because the disk is Swizzle. And now we're going to copy the data because it never finished because

**Matt Yonkovit**  
I'm gonna put a snap poll out here. For those who are watching. I give Charlie an instance and tell him to set it up. And now he comes back with all these problems. Is it a hos problem? Or is it a Charlie in the Chocolate Factory problem? Well, please put them into your comments. I think this is a Charlie problem. Because I gave him this and said, What do you want set up? And he didn't ask for it before. He's the one who configured it. So what do you think? Is it? Is it a Hoss problem? Or is it a Sharlee? Problem? I'm both fairly,

**Charly Batista**  
it has nothing to do with configuration. If you gave me a box with a higher IO PS because you're saving money. Without this harpy enough your pocket, man.

**Matt Yonkovit**  
We're like, we're like two old people arguing with one another, right? Yes. I know. Hopefully, hopefully, you you don't just feel the anxiety. You feel the love in the room? Do you need a hug, Charlie? Oh, well, yeah,

**Charly Batista**  
we had we have a baby in between. But I will I will give you a hug. I would. That's really good water by the way.

**Matt Yonkovit**  
All right. So boundaries. Like I said, we're going to have to do another live stream on backups. So and so what we'll have to do is we'll have to either work it in and bump the schedule back one or working in next week. Because what we want to do is we definitely want to do look at the incremental and differentials.

**Charly Batista**  
Yeah, we need to finish this and we need to show people that works, right. Yes, that's just stopping. Now. There's nothing fancy is just copying things. Yeah.

**Matt Yonkovit**  
Cooking shows where like, they make it they put it in the oven. And then one second later, they pull it out because they already baked one. So we should totally copy the cooking shows, right? Yeah, we should it by the way, no one voted for Charlier means I'm just so disappointed. So I'm gonna I'm gonna say I win because I get two votes. This is my string. Your box my straight.

**Charly Batista**  
Yeah, well, let's let's do that. So we will have to wait for it to finish. Okay, so I'll just expect to explain what's next up. So when it finishes, we need to go here and just do the PG stop backup. That's it. So

**Matt Yonkovit**  
the backup is done. Yeah. So the the question came in. Are we just waiting or moving a hot backup to the other disk right now? Yes. Yes. So what we've done is we are moving a hot backup now. You know And this is just going through the process of doing it. Yeah. and because we use the same disk because Charlie didn't ask for another disk. It's taken.

**Charly Batista**  
That's, that's, that's my fault. I'll pick that one.

**Matt Yonkovit**  
But yeah, so we need to come back to this, we need to get this scheduled out. So my question is, and this is a question that I get a lot is, should we be backing up? Daily? And if we're backing up daily, should you know how what what sort of retention? Should we look like, online? And should we be pushing things out to s3 on a nightly basis? Or should we leave things on disk? What's the recommendation, general recommendation and guidelines around it?

**Charly Batista**  
It totally depends on your business and on your regulations, right? My recommendation, the baselines would be to have a full backup, weekly, right, and do incremental backups daily. So the rotation is, as I said, it depends on your the regulations, and how much money you want to spend. But usually, it's ideal to have backups, at least for a couple of months, executed three months, if you do not have any regulation that requires you to have that backups for one year. So maybe you don't have here. But then you recommend to keep even if you don't have those regulations to keep at least for a couple of months. So something happens in you might need to go back and pass on member COVID data, right. So that that's an important point. But for my recommendation is have a weekly full backup. But on Sunday, you have a weekly full backup. And then you can use incremental backups daily. So the backup process doesn't take that long and doesn't pack that much in your business.

**Matt Yonkovit**  
And this gets back to what we were talking about the beginning of the stream, which is the smaller databases, you have a bit more flexibility

**Charly Batista**  
you do you can do full backup every day. That would be if you have a one terabyte database. It's for all that seems a lot of data. But yeah, you can do a full backup and then the small incremental backups, you're not copying one terabyte 50 gigabytes, you can do full backup every day, right? It's just like being incremental backup for the guy that has one terabytes.

**Matt Yonkovit**  
Yeah, and I think that the best practice I've generally seen, as keeping at least one full, and all the incrementals, or even seven days were on disk somewhere that you can do really quick. Yeah, and then everything else can go to s3, for longer term storage, because s3 is slow to recover from that's, that's, that's

**Charly Batista**  
a really good point. That's a really good point. So you have a really fast disk attached to the box, not the same disk as the box, I would not recommend to have the same disk as the box. Because if the disk crashes, you will lose your backup. That's that's the main thing for the

**Matt Yonkovit**  
very astute observation.

**Charly Batista**  
So you have a fast Apache disk to the box, and you keep the whole week worth of backups, or if you have a full backup, and incremental is what you keep back. And the fact that it keeps that doesn't prevent you keep pushing, pushing them to s3, right? So they're just the measure, if you need to recover really fast, you have the in hand. So it's easy for us to record from that fastest that's attached to the box. Yeah, that's a definitely a very good point.

**Matt Yonkovit**  
Yeah. Now we did get a question, is it now capturing the current transaction in the backup

**Charly Batista**  
might be, so what happens? Remember, the transaction, they firstly stay in memory. And that's why we need to have consistent backups. So the database they're flushing things from memory to disk, and eventually they're going to the disk. So we have the consistent backup up to the point when we run this command here. Everything that was in, in the database up to this point is consistent.

**Matt Yonkovit**  
So so everything else is just waiting and staged.

**Charly Batista**  
The new transactions, they're just going to the disk, they might be or might not be in the disk, there is a chance that they have been replaced it and they've been to the desk. Yeah, there is a possibility. But it's again, it's luck.

**Matt Yonkovit**  
So let me ask you this question. What happens if you don't use the stock backup?

**Charly Batista**  
That's a good question. Nothing fancy. So I'm still pushing things to the database. So but well, I don't have a good answer for you for your question. I will have to research.

**Matt Yonkovit**  
That's a really good question. Because like, if you just leave it up, what is the downside I need

**Charly Batista**  
for that question. I didn't remember if we need to keep that connection open. And if you close the connection is also I was, I don't remember the top of my mind. I don't want to try it now because we're doing the backup. So I don't want to repeat. That's something that we should test. And I'll take a look on on the source code to do to better understand that question.

**Matt Yonkovit**  
Okay. So generally, what I'm going to ask you to do is, maybe between now and the next stream that we do, if you can go through and do a few incremental backups, what we'll do is we'll create a few videos of you doing incremental, and if it does take a while, we'll condense that down. And then we'll play them. And then we'll talk about it live. Right. So it might be a little easier. It's like a showdown, right, like, so we're not going to wait the three hours to bake a cake or whatever, we're going to take the cake out of the oven that we started three hours ago, some some some, because I think that that works. Any other questions? We thank you for hanging out. I know it's been long, and it's probably been a lot of back and forth. This is a bit unusual for us. We're generally not live in person. We've generally got things kind of set up ahead of time. So it's a little smoother. I actually had to create the live stream environment today because I'm on my laptop. And this is not what I normally live stream from I live stream from a machine at home that has everything configured in the big microphone and everything. So we hope everything worked out. Okay. But but we'll we'll get a secondary schedule on the backup schedule side of things. Although it was kind of interesting to see the issues with auto vacuum. So that's,

**Charly Batista**  
that was definitely yeah.

**Matt Yonkovit**  
Yeah, the backup is still going. Yeah, it's, it's loaded. And and we are still copying with our sync. So yeah, so we haven't stopped it yet. We haven't issued the stop command. So the Our Sync is just copying, and copying, and copying and copying. So all right. Thank you all for joining. We appreciate it. We hope you join in next time. Don't let Charlie dissuade you from coming back. we love it when when things go right. But it's probably more educational when things go wrong.

**Charly Batista**  
I love when it goes wrong.

Unknown Speaker  
No, you don't hear no. Yeah, I

**Charly Batista**  
do. I don't care. Because it's bad to go around here. Turn on production. But

**Matt Yonkovit**  
we do appreciate you hanging out with us. And until next time, we will see you later. See ya. Oh, how do I validate the consistency of the backup? Oh, we just got that.

**Charly Batista**  
Oh, you're finished? That is streaming. We just

**Matt Yonkovit**  
got it. You want to answer the question? We just got just got How do I validate the consistency?

**Charly Batista**  
That's not easy way to validate the consistency of the backup using the method that we are doing. Because we remember we are just copying we're so to validate the consistent of the backup, we need to recover the backup.

**Matt Yonkovit**  
Yeah. You have to test your recovery. Exactly. Yeah. I mean, unfortunately, when you have terabyte size systems, it's really

**Charly Batista**  
hard. But you do is to restore and oh, yeah, we do. You, you you should have the discard when you're planning for time to time you do validate the whole strategy and to make the backups, right they re doing are invalid. And they are recoverable. Yeah,

**Matt Yonkovit**  
yeah. Yeah. And Kamal came in it'd be great if we could do archived tomorrow. I don't think we can do it tomorrow. But next week. Yeah. Tomorrow's travel day for many of us, because we're at the conference. So. All right. Thank you, everybody.