---
title: "Percona MeetUp for Percona Monitoring and Management PMM Dec 1st, 2021"
description: "Live streaming from AWS re:Invent in Las Vegas to highlight PMM features for open-source database monitoring: MySQL, PostgreSQL, MongoDB"
images:
  - events/percona-meetup/cover-pmm-december-1920.jpg
date: "2021-12-01"
draft: false
speakers:
  - michael_coburn
  - matt_yonkovit
tags: ['PMM', 'Meetup']
---
Percona Monitoring and Management (PMM) is designed and constantly updated with useful features for monitoring and optimizing your database performance. The Community MeetUp for PMM of last Dec 1st, 2021 was live streaming from AWS re:Invent with Michael Coburn, hosted by Matt Yonkovit. Together, they have resolved database performance issues and stump the expert.

## Video

{{% youtube youtube_id="Ax5McTZifmw" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Hello, everybody, and welcome to another Percona meetup. I am Matt Yonkovit, the HOSS at Percona, and we have Michael Coburn once again, joining us for his monthly slot to talk about PMM. And to use PMM, to do some interesting, cool things. I hope that you are all having a wonderful day. If you haven't seen this week, AWS is re:invent and Michael is not in his normal digs. He is actually in a hotel room. And I am surprised he is up at this hour. Because he is in Vegas. And so Michael, how late were you up last night?

**Michael Coburn:**  
Well, Matt, they say what happens in Vegas stays in Vegas.

**Matt Yonkovit:**  
Actually, they say that. And then what if there's a second part of that? What happens in Vegas stays on YouTube or Twitch or Tik Tok, or wherever you are streaming from. So there you go. There you go. So how is the show bet?

**Michael Coburn:**  
The show has been great. We have been hearing reports that it's around 20,000 people. So down from past years, but still, that's a lot of close friends of mine that seemed to show up.

**Matt Yonkovit:**  
A lot of close friends, all 20,000 of them.  What surprised me? Michael's a mover and shaker in the  tech space here isn't he?

**Michael Coburn:**  
No, we've been having a really good time. We've been having a good time so far.

**Matt Yonkovit:**  
So, anyway, we are here to talk about PMM today, but before we get there, you guys have been showcasing PMM in the booth. Right? And so how's that been going?

**Michael Coburn:**  
That's been quite a draw, we actually have a nice big monitor behind us that helps us describe the problems that database servers experience using PMM. And to stimulate their load, we've got a certain type of device that you might know something about that you helped to set up?

**Matt Yonkovit:**  
Well, so I heard a rumor. Okay, so everybody who's watching has been paying attention. I built these Yonk boxes, the arcade controller to control things, and I did not go to Las Vegas this year. So I sent that box alone. And when I shipped said box, I put it in a nice box. I wrapped it nicely. I had tested it for the week ahead of time, everything was perfect. We completely re-architected it. So it can run parallel workloads across multiple servers and multiple cloud systems. And so we're really excited about shipping it off. Steve, our VP of engineering, got it out of the box. You got it set up for you guys. You were sitting in the sponsor room, you were checking that out, you were playing with it, it was all good. So it shipped working. It arrived working, you tested it working, then I heard you carried it to the show floor and it stopped working sometime between when you left the room. And when you got to the booth. There was a moment where I denied this.

**Michael Coburn:**  
I was the said carrier of the device. This did happen.

**Matt Yonkovit:**  
And therefore Steve was on the phone with me going like, Why isn't this working? And I'm troubleshooting remotely, to try and get this thing to work. Which is always fun and exciting in and of itself. Right?

**Michael Coburn:**  
Mm-hmm. So the good news is, we could get it working. It works. 

**Matt Yonkovit:**  
So if there is any doubt, we can always blame Michael.

**Michael Coburn:**  
That's nothing new either. Yeah.

**Matt Yonkovit:**  
So um, so as people have been playing with the box, we've had people come by. They've been clicking buttons, they've been turning knobs, they've been changing the workload. And now the beautiful uniform workload that we started with, does not look so beautiful or uniform anymore. So for those of you who are following along we've been doing this where people can come up they can break the box, basically. And so right now, we are getting ready to go to the show floor in an hour or two. All right, right. And, before Michael gets there, he needs to figure out what is wrong with all of the setup to make sure that it's ready to go for today. So we thought today, we would play a little bit of stumped the expert as people on the show floor and some other people may have messed up some workload and we'll let Michael show you how he will troubleshoot  said instances

**Michael Coburn:**  
so really putting yourselves on the spot here.

**Matt Yonkovit:**  
Yes, yes. So, here we go. So, Michael, I am going to show you my screen and then I will let you take over the screen if you want. You know just so you know all the shells are set up. So if you go to have the app servers, hopefully, you have the links to the app servers. So you can log in and go to the shell if you need to. Hopefully, you won't. But we have three boxes, one running easy to one running the world, running rds, MySQL, all of them on MySQL 8, or variants, all running the exact same workload, with the exact same application infrastructure. Okay. And so all of them should be in parallel, I can't guarantee that something wonky didn't happen. And maybe things got out of sync a little bit. But I did check if all of them have the same number of threads running? I just don't know beyond that. So here we go. Let's take a look at what we've got in the PMM Mystery Box. And oh, by the way, just so everyone else is aware. There may have been a new code deployed this morning with some new workload that Michael may not have seen before. I'm not saying there was. But I'm not saying there wasn't

**Michael Coburn:**  
really taking up the pressure. Not sure, Matt, but nobody.

**Matt Yonkovit:**  
So here we go. And so the first thing that is kind of interesting walking in here, and I'm going to go ahead, and I'm gonna go back this up. Let's go back three hours. All right. So here we have our graphs. And so you can see that the average workload in terms of queries per second, it's higher on EC 2 than Aurora. And RDS I can tell you when we started this, they were the same, or very close, let's say they were within 10% of one another. Okay. I can also tell you that right now, the current queries per second between these three, Aurora is performing slower than rds, MySQL, and EC two. All of these have similar boxes, not exact. These are all four core 16 or 32. Gig, Aurora, unfortunately, they don't have an M five, extra-large. So you had to go with the R six, which has 32 gigs versus 16 gigs of memory. But this is not a IO-bound workload, in terms of like the dataset, the dataset all fits into memory for all of these or it should. It may not after today, but that's beside the point. So there we have it. So you see this graph? And Michael, I am the person calling you saying, Why did my app take a tank from yesterday. And if we go back even a little further, we can look back at yesterday. We'll go back 24 hours. You can see that we were actually running pretty high yesterday. So let's go back to this guy. This is before any of the changes, and before people got kind of in there. So you can see here that things were around 1000. That's actually pretty low. Let's go back two days, and let's see what we got. Ah, all right. So this is where we started before people started monkeys. Okay, so we've gone back in time, we've done the Wayback Machine. And you can see that this particular box with this workload with this dataset, was doing about 4000 queries a second across the board, we had kind of pegged out the CPU. You can see the different database response times, but it was a busy box. And this is more about the optimal load that we could have gotten to. Okay, so now going back to the last three hours, you can see that we are way off from there. So Michael, fix it.

**Michael Coburn:**  
Fix it. Okay, easier said than done, I'd say.

**Matt Yonkovit:**  
Tell me what you need to do. Tell me where you want to start. Tell me where we can go.

**Michael Coburn:**  
Okay. Well, I think the first one is one of the angles we usually want to look at when we're examining database performance or the types of queries that are running and we want to look at that tool.

**Matt Yonkovit:**  
Why don't I let you share your screen and you can drive so that way but now you've set up the problem becomes a solution?

**Michael Coburn:**  
Alright, let's see if I can share the whole screen here. I guess you can see. There we go. I've already taken advantage of going ahead and getting onto the shell of this host here. So this is our MySQL server running. And we can see that it's got a bit of a load on it. Is this easy to instance? This is easy to do.

**Matt Yonkovit:**  
So we are at 100% CPU

**Michael Coburn:**  
for a core machine, isn't it? Yeah, so doing 400%. So while the first conclusion is that we've maxed out CPU, where do we go next? I normally would want to take a look at the queries running inside the database server, and see if they're hitting certain types of locks maybe where the contention actually is. So what I want to do is usually start at the MySQL client. I think I know the password is the one we've been using all week.

**Matt Yonkovit:**  
If you're, yeah, well, so no, if you go from the app servers, it's already set up to do passwordless. It's got to be saved so just go to one of the app servers. If you need those, I'll send them to you in Slack.

**Michael Coburn:**  
Yeah, it can be the app server one, that's the one that I'm missing.

**Matt Yonkovit:**  
And don't cat my CNF. It has the password. And of course,

**Michael Coburn:**  
oh, yes, I'm streaming live, aren't I?

**Matt Yonkovit:**  
 You're streaming live. So not that it matters. These are dummy boxes with a very easily guessed password between them. And it's you have to be on the box in order to do it. So I mean, it's not as big of a deal. But let's remember IT security for it's important. 

**Michael Coburn:**  
That's right. Okay, so let's take a look then. 

**Matt Yonkovit:**  
And you have this cool tool called PMM. And this is the PMM meetup. So using PMM to do some of this would be cool as well. Just saying. Let's get on to the fact that I am giving Michael a lot of grief this morning. I shouldn't because he is in Vegas.

**Michael Coburn:**  
you've got your own trip this week to Where are you going to be?

**Matt Yonkovit:**  
I'm good. I'm staying home. That's it. I'm home. I'm home. I'm not going anywhere. There is another conference, but we have 10 Perconians at the Postgres New York Conference. So we've got plenty of coverage there as well. Thank you, everybody, for joining, we've got some people who are stopping by and saying some good vibes and the Yonk box rocks, and people who are happy to show up and do this. So for those who have just joined, we are playing stump, Michael. We've had 1000s of people stopped by the booth in play with the workload with the controller. And so now Michael has to fix the box and make sure it's in a state so they can use it today. And it's not going to start off where they don't know what's wrong.

**Michael Coburn:**  
All right, Matt, I'm gonna ask Could you pass me the app server IP address?

**Matt Yonkovit:**  
 Oh, Michael! Oh, you're killing me, dude. Alright. So you want the EC2 Or do you want the wrong one because there's app servers for each one.

**Michael Coburn:**  
Let's see EC2. Okay, I'm a big fan. If I can get a shell I feel like I can analyze the problem better. It feels more real.

**Matt Yonkovit:**  
Oh, my goodness, Michael. All right. No, feels more real. Does anybody else feel that way? Like it is it who out there who's watching prefers shell versus having kind of a user interface and a tool. I know that everybody has their preferences. But I am super intrigued by what people out there prefer. While I get that and send it over to Michael and his fancy pants, Slack conversation and he gets that set up. There you go. Now you have it. So anybody who wants to throw something out there Gonzalo says hey, Hi! Gonzalo is one of the Perconian in New York right now. He's trying to organize people to go eat. I saw it this morning. So hopefully, they find, some good places because New York has a lot of good places. Marcello is all about the shell. Of course, Marcello, you're about to show that's not surprising.

Oh, look at this. And Len says, Hey, why don't we have an easy way to include a way to shell into nodes via the PMM UI? Built in SSH client Yeah, we've got a lot a lot of love for the shell the way of the shell did you get in Michael?

**Michael Coburn:**  
I'm on the server. Just confusion.

**Matt Yonkovit:**  
Just type in MySQL just type in MySQL. 

**Michael Coburn:**  
just supposed to be that easy. 

**Matt Yonkovit:**  
I set it up to be that easy.

**Michael Coburn:**  
Okay.

**Matt Yonkovit:**  
Did you get it? Oh, you need to log in as Ubuntu. Now try. 

**Michael Coburn:**  
Oh, just I think it inherited

**Matt Yonkovit:**  
I guess it doesn't just sudo dash su should do it. I think right now Ubuntu as Ubuntu is a boon to sorry, this is yeah, that the demo gods are kind to us today. Lead says yes. We're trying to troubleshoot. And we haven't even gotten to the more difficult part.

**Michael Coburn:**  
wait, it's gonna get harder Matt. Don't say that.

**Matt Yonkovit:**  
It's gonna get harder. It's gonna get harder. We haven't even gotten to the log in part. And  I did warn Michael I said hey, use this before we get there. So why is that? What's going on there? It should pick up the home environment. Hold on. Hold on, Michael. Hold the call. Let's just double-check to make sure that I didn't do something stupid. Oh, gosh, you and then root. Or it's actually no, it shouldn't. Hold on. Oh, wait a minute. I sent you the wrong box. That's why I'm an idiot. Everyone blames the Yonk. I sent him to the exact same box that he was already in. Which is really dumb of me. This is where to get to? Yeah, there you go. Michael. Sorry. This is why live streams are awful. And we hate them. I'm just teasing. This is the power of the live stream. Okay.  you end up having to suffer through people. Yes, everything fails 99% of the time. Yes. Did you get in at that time?

**Michael Coburn:**  
Since tabs are free let's open another one the hyphens? We can solve this.

**Matt Yonkovit:**  
Yeah, you should be able to, and then you can do your thing, you can su over and then it should pick it up. there you go. All because you needed to look at that. So, like, you could have just used PMM. 

**Michael Coburn:**  
But we're gonna get to that. What I wanted to do is show both ways of being able to access the visibility or the activity going on.

**Matt Yonkovit:**  
Yeah, get to it.

**Michael Coburn:**  
The first thing you want to do is to see what's going on in the box. Show me some processes. Oh, it's busy. All right. I hope this doesn't break the view too much. I'm just reducing the font to ditch.

**Matt Yonkovit:**  
Yeah, I think you're okay. Might be a little easier. No, that looks worse. So we'll go back to that. By the way, you should hit the hideout at these studios. Yeah, yeah, that way. Yeah. It's kind of hiding some of it.

**Michael Coburn:**  
Okay, so we see activity, I'm just refreshing it every second or so. And really what I'm looking for is making sure that I don't see any literally long-running queries here. And I don't for the updates that were showing up at the bottom, but I do see some long-running selection up here at the top. And so that leads me to believe that we've got some contention that we don't have a stock query, I don't see anything saying it's metadata lock, etc. But I do just see long-running queries at this time. Okay, another angle, I want to view it just because I'm a bit of a nerd, and I'm already in the database. I'd like to see what the storage engines are doing. So we have this command called Show engine InnoDB Status. X slash because otherwise, it looks really gross. And I want to look at the transaction section here. There's a lot of buffer pool stuff and my pay goes away. Oh, look at that many transactions. And do we have any? It looks like we had dreadlocks. But these were,

**Matt Yonkovit:**  
It was yesterday. Yeah, please, already just fine. Because we turned off all of that. We have specific queries that deadlock there's a whole button to do that.

**Michael Coburn:**  
Mm-hmm. Okay. All right. So I'm seeing that we've got some queries that are running here, I'm going to take an example of one of them. Because usually, when queries are running slowly, there's an opportunity to examine them and determine if they're using the right indexes. And so what I want to be able to see is if I can get the full select data here, look, that one looks nice and long-running 64 seconds. Let's take that. To explain it, it's gonna tell me I'm in the wrong schema. Searching schemas is great. Oh, wow, look at that. We've got a query that's doing just shy of 400,000 Row accesses. I wonder if there's an opportunity here to improve on that index? Says it tried to use the primary key but decided to do a full table scan? That's not great. That's not great at all. Matt, what have you done?

**Matt Yonkovit:**  
I didn't do anything. This is this is real people. Who did this?

**Michael Coburn:**  
Which table? Are we here? Oh, it's just Table A? A is table movies normalized? Data? Let's see what the table definition is. Table A doing just to join?

**Matt Yonkovit:**  
Michael, you froze?

**Michael Coburn:**  
Hey, can you hear me?

**Matt Yonkovit:**  
I can hear you. But you are frozen on your screen?

**Michael Coburn:**  
Yeah, I didn't touch anything. I'm just

**Matt Yonkovit:**  
In fact, I can't even I don't see the system being updated either. So your shell is shell us? Dear. Oh, the pain of the live stream here?

**Michael Coburn:**  
Yeah, the restream window doesn't look happy either.

**Matt Yonkovit:**  
This is what you get for hotel internet. So let me go ahead. And while Michael is trying to fix his thing, I'm gonna go back to PMM. And I'll show you what Michael was going to show you but with the PMM interface. So here we go. So what he wanted to do is he was looking specifically at the queries that were running. And so this is where query analytics comes into play. And so from a query analytics perspective, these are the queries that were going on in the system. And so trying to find that needle in the haystack is generally a challenge. So we do have this average query time. And Michael, are you still there? Because your face is just completely frozen.

**Michael Coburn:**  
I'm still here. Yeah,

**Matt Yonkovit:**  
you might want to, you might want to bail and come back. I'll let you back in. Let's put it that way.

Alright, so as you can see here, he was looking at some of these queries that were out here. And there are several that are running pretty down long. And so let's take a look at this one in particular. There's Michael again, look who's back, he is back. So you can see that this particular query has been running for a minute, 17 seconds, it's taking 7% of the total load on the system. And you can see that the query itself here's this fancy pants setup. You can see what the EXPLAIN looks like. You can see that it is doing a full table scan on A and A in this case is

**Michael Coburn:**  
See a movie's normalized meta?

**Matt Yonkovit:**  
Yeah, it's the movie's normalized meta, which I couldn't get the system for. But I don't mind that it's not showing up. That's interesting. But that is one of the main tables that's out there. And so when you see it's joined on the AI, my ID and the BAI, my ID. And we can take a look at that. Michael, are you still you still have your shell up? Yeah, let's go ahead. And let's do a description on that particular table. Okay.

Yeah, so take it from here. Okay.

**Michael Coburn:**  
So we're looking at Table A movies normalized meta, and it wanted to use the primary key, but it chose not to use no key. The primary key: Oh, Matt, what have you done here?

**Matt Yonkovit:**  
I didn't do anything. Sure.

**Michael Coburn:**  
Well, I blame you, because who made the schema? If not you?

**Matt Yonkovit:**  
It was the users. It's always the users. It says this list.

**Michael Coburn:**  
Oh, boy, some of you paying attention at home InnoDB works much better with primary keys that are integer-based, not that you can't do varchars and maybe even blobs, but I certainly wouldn't recommend it. So let's, let's see if that's actually the problem, though. Right? Our primary keys AI my ID, and it's a varchar32. So it's got to index that whole 32 string of 32 characters there.

**Matt Yonkovit:**  
Indeed, so what do you suggest? Hmm.

**Michael Coburn:**  
I wonder what's actually being stored there? Let's look. See what is in that field?

**Matt Yonkovit:**  
You might want to Oh, yeah, you might want to just select that column, because there is JSON in there.

**Michael Coburn:**  
Yes, quite large.

My ID, that it looks like it's a number not really a varchar. I got a few of them. They're actual integers in there. Probably the first. Yeah, I might articulate that we have an option here, an opportunity to convert this to an integer, an int, let's say or maybe even something larger. But

**Matt Yonkovit:**  
as the developer who I just asked, developer, is this an integer? Yes, it is. Then why did you store it as something else? Just because maybe in the future, I don't want an integer. But

**Michael Coburn:**  
Well, we should be building our apps for today. Not for tomorrow yet. So does that explain why though it did a full table scan rather than using just the primary key? I'm not sure. I'm not sure if I guess what I'm getting ahead of myself is I'm offering improvements without knowing that it's actually going to solve the bad explanation that we're looking at here. So let's park that idea just for a moment. Because if we have to run an alter table that usually involves some sort of coordination with the app team and maybe an outage for a short period of time, or you could be using PT online schema change and do it without blocking any activity. So let's see what else we are doing so we have 32 rows being retrieved and we want to see if maybe we could get that down in something lower Zhan Table B, B is the normalized cast. And we've got two times B gets pulled in here on AI actor ID. So that one creates a table on release cast items.

Joining on AI actor ID which is an integer. Are there any indexes on that? We do. Good that's covered. Is there another one? AI my ID Okay, so they've got two separate indexes. So that's good. So what I'm looking for is the tables being joined twice. Each time it does a join it needs an index to cover it and they're different indexes and they're in the right places and the right orders. So that's

**Matt Yonkovit:**  
Michael But Michael, look at that table definition

**Michael Coburn:**  
redundant indexes here but what am I missing?

**Matt Yonkovit:**  
Look at the AI my ID

**Michael Coburn:**  
ah, Ah, ah. So what we're doing I see what you're getting at here, we've got an integer on this table for AI my ID. If we scroll back up just a little bit on this side, the other table it's a varchar. That's not good. We want to have a tightwad.

**Matt Yonkovit:**  
small, insignificant potential difference. Except it's more than insignificant.

**Michael Coburn:**  
In the last section, I just want to evaluate. So that's two things we've got to take away. We've already recognized that the first table of varchar was optimal and now we're seeing that it's in fact, quite negative because now we've got a type mismatch between the two tables when they get joined. Yes. Okay, so the recommendation already, I think I'm, we're moving towards here is get it into integer and see if we can now have a material it's quite good query.

**Matt Yonkovit:**  
Let's go ahead and do it. We'll do it live. Yeah. All right, go for it. Okay, not that willy nilly. But you know

**Michael Coburn:**  
I hope I don't go to the docks, but I might need to change columns. we don't want to drop, we want to change. Table change shall be changed. Everywhere Change column name,

**Matt Yonkovit:**  
And for those following at home, I'm going to go ahead and put this in this is what I would recommend you do to fix it. Michael, you have this now on the slack as well. There you go.

**Michael Coburn:**  
I think I got the same syntax. Did I get lucky? So we end up with here

**Matt Yonkovit:**  
so this will take a couple minutes to update that. And I'm going to go ahead and I'm going to in the background execute that on all of our hosts. So we've got three hosts all the exact same setup and so I'm going to keep moving along on these as well. So we're gonna go ahead and do that real quick fun fun fun until there is no more fun

**Michael Coburn:**  
oh, and I should have asked if we didn't stop the workload the good way.

**Matt Yonkovit:**  
Yeah, but for this test. We're good

**Michael Coburn:**  
no users were injured in the migration of the tape.

**Matt Yonkovit:**  
Well, I mean, some users might be injured you should go check out PMM let's see what the that workload in PMM is doing

**Michael Coburn:**  
It's already started in the browser Matt.

**Matt Yonkovit:**  
Oh, Michael, you're killing me, dude. Get it? 13 Yeah. Should be 13. No, that's the internal IP Yeah. Yeah, that guy. For those following it, oh, Alright, so here we go. Yes. Yeah. Proceed to these

Yes, Steve, the injury count is zero because now the show isn't open. So no one's going to see you fix this Michael

**Michael Coburn:**  
Okay, yeah, there's the three boxes around a little bit of a shorter period here.

**Matt Yonkovit:**  
Yeah, so you'll see all the, like, things start to drop and lock and things, right. So, which is expected as these are wrong now I could shut off the workload if we wanted. Because if you look, it's probably all locked. Right? And they're waiting for things to complete before it gets its spot in the queue. By the way, this is really mean of me to make you do this on a day after a show when you've been out.  like we've been through the hard parts.

**Michael Coburn:**  
We've been together a long time, Matt, it's okay.

**Matt Yonkovit:**  
It's okay. It's okay. It's okay. So anyway, so those, those are running. So the other thing that is really perplexing to me is the fact that there has been such a drastic difference in the Aurora performance since yesterday, which really makes me scratch my head.  if you go back and you look at the last like six hours, you'll see that that performance difference is quite substantial, right? Like I mean, even before the drop, you can see that the EC 2 instance was really kind of rocking and rolling. And that Aurora and RDS has been pretty stable, but Aurora seems to have really taken a tank

**Michael Coburn:**  
Was the workload adjusted on all three? That's what you had mentioned earlier.

**Matt Yonkovit:**  
The workload is identical to all three on all three boxes right now. And so it's all the same workload. Okay, and the altar store for your altar tables should be done. So they completed on my, on the two other nodes as well. Oh, yours is taking its sweet time.

**Michael Coburn:**  
We do have considerably higher IO weight, you see two bucks. This spike?

**Matt Yonkovit:**  
Well, that's what you're, you're on right now. Right. So this is the last 15 minutes. So that's to be expected, though, when it's gonna have to redo all the indexes. Yeah, right. Because when you're changing the primary key and you're modifying the column I mean, that's gonna hit every record in all the indexes and all the tables. Mm-hmm.

**Michael Coburn:**  
It's painful. All right. It's the value of choosing the right primary key type

**Matt Yonkovit:**  
What's weird for me is that I mean that one I'm wondering about too, so the configuration is pretty stock out of the box. The only thing I adjusted before I shipped these off was the InnoDB buffer pool size. So I'm wondering if there are some other opportunities there to tune

**Michael Coburn:**  
see if I can get a second window on this box

**Matt Yonkovit:**  
well, you should be able to get a second window that's more

**Michael Coburn:**  
like this guy right here

yeah. Stuff just factions the bottom we've still got our altar running up here. Still a little poking around

So enter to be is configured for at the moment. Make sure the buffer pool is appropriate. Didn't know what the size of the memory was in this instance. But see if it's bigger than 128 meg for the buffer pool.

**Matt Yonkovit:**  
Our buffer is a 16 gig instance.

**Michael Coburn:**  
Okay. Yeah, it looks like you've configured it, maybe for eight gigs. So that's good. It's bigger than the default. See what else we got? Okay, so some other performance-related ones are how often InnoDB might need to be flush to disk. And that's controlled by InnoDB flush log at transaction commit. Okay. Well, this is always an interesting discussion with people, when you set it to one, that means after every transaction commit, it's going to do a write to disk, which is the most durable way of persisting your data. But that comes at a performance penalty or performance trade-off. And so we have the option to set that to zero or two. And that means that it's going to less frequently write to disk and therefore be able to get more transactions completed. So that's an opportunity for us to improve performance.

**Matt Yonkovit:**  
Interestingly enough, the defaults for Aurora and for RDS are also set to one, which is, which is interesting. So we're not seeing as much IO weight there. So there might be some optimization on the disk IO, that they do internally on rds, and Aurora, as well, because what I've seen classically over this, this workload the last couple days is it's been about twice as much on the easy to box as it is on the other.

**Michael Coburn:**  
One, if the quality of the EBS block storage has anything to do with it, too, that is

**Matt Yonkovit:**  
a possibility as well.  I didn't do anything fancy, I didn't do anything reserved.

**Michael Coburn:**  
But Amazon's got different levels of GP-based and then IO-based desktop, there are about five different EBS tags you can get. So make it easy to spend money. The other one that controls a lot of disk writes is related to the binary log, it's set to one but I didn't check to see if the actual binary log is on. And that's through log, then it is on Okay, so we're doing additional rights here to be able to set up a replica if you so desire, or give you a bit of an audit of many different good reasons to have the binary log on. Right, it's got the ability to control it so that it can be written to disk to persist after every transaction commit. And that's the state that we're in right now. So this box is tuned for very heavy persistence or high reliability but there's a performance trade-off there so if you said to me as my customer will make well can you make this box faster I've got a couple things but if you said well I want faster and durable I'm not sure we've made too much progress just yet. Stopping the system alter we are blocking we've got updates waiting for the metadata lock and this is a sign that we're running while something has locked that table and we should be able to see the altar up here somewhere

**Matt Yonkovit:**  
So what do you get? right there there is awaiting you see waiting for the man okay so what's what else you got going on?

**Michael Coburn:**  
We've got just the updates holding there are no inserts on the table. Wait, even the selectors are waiting to hear. We're not being very nice today to the users of this application today.

**Matt Yonkovit:**  
So why don't you go ahead and kill the altar. make sure that clears up

**Michael Coburn:**  
nobody's left and waiting on metadata.

**Matt Yonkovit:**  
All right. So I think I wonder if this has to do with the column, is it I don't know. I mean like, so I ran on all the other boxes with the exact same, you know thing and we've been running that flipping between varchars and integers. And that dozen times a day without that same lock. But the difference is I'm not using unsigned. Not that it should matter. But I am setting that as an auto-increment. So try an auto-increment. Not that that should make that difference. But that's that, you know what I sent to you guys, so let's see what fun and exciting things that that does. So you can see it copying to a temp table.

**Michael Coburn:**  
There we go. There's the altar.

**Matt Yonkovit:**  
But so the other two boxes are adjusted. And so they do have that. So jump over, go back to your let me go ahead and I'm going to close you out for a second. Because, Michael, what time do you have to be at your booth?

**Michael Coburn:**  
Oh, I've got another hour after our Okay, good.

**Matt Yonkovit:**  
All right. So we can go a little over if people are interested, we'll get more people who watch this after the fact. So. So we're gonna go to one of the boxes that aren’t running that altar right now. So I've got this main dashboard here. So I'm going to look at the Aurora box. And so going through here, again, looking at the queries, I'm going to zoom out a little bit too. So I can get a better idea here, we can see that we've got several of these queries that are definitely taking longer than they should. We did fix the integer problem. So the varchar energy problem. But when we look at the volume, the top volume getter is this guy right here. And so looking at him you've got one second, you've got almost one second each, which is pretty long. And if we go back over a 24 hour period, we can see that this was running in, like 200 or 100 milliseconds before. So this one in particular kind of worries me a bit. And so I'll play spoiler here, I know what's wrong. But if we go look at the query counts for the last couple hours here, we can see that I do that. We can see that the query counts. Where is that guy? So that's great counts per second. Oh, this guy right here, I should add a total count. Just so it's easier. Don't have a total count. Okay. Here we go. So this guy, right, here we are, we can see that from an example perspective, it's pretty straightforward. It's just searching for a title that in this case, Two and a Half Men, what a lovely landing strip. That's the episode from 2011. Then we got here. It's just doing a full table scan. So that particular table is missing an index on the title. So I can go ahead and I'm going to add that index to the title. So we needed to find something that needed to be dressed. And I'm gonna go ahead and while we're doing that, so create a title. So that's off and running. So that should alleviate some of those issues right off the bat. So hoping that we'll see that particular query come down from that 900 milliseconds down to  a couple 100 so that that right there is like a 10x improvement on that one.

So that's one of the other fixes that I know should play a part in that as well. So and then I'm going to go ahead and reset

Let's go back to this guy here. We did annotate. Like when I ran that I made sure I ran that we have a script to annotate that. So that's part of the Buildbox. So what you see is these queries should start to decrease in the amount of time that they take, once these create indexes are finished, oh, it says that it finished. So that's good, right? All right. Let's see what happens if the number of queries per second jumps up substantially. So again, we're at 514 queries a second on this particular box, takes about a minute for this to update. And so we can see here even like, this guy should start to pick up here in a second. And you can also see that the response time has started to dwindle drastically. So this isn't just about queries, though, because I want to get to a couple other examples in a second. But this one is a pretty straightforward one to start to look at. And even if we go in and look at this guy, again, you can see that the last iteration, so he saw over the last five minutes, this was 900 milliseconds, 900 milliseconds, 900 milliseconds, 800 milliseconds, 62 milliseconds. I mean, that's a pretty substantial decrease from what it's there, right. And so when we look at this guy, now, we should start to see that dwindle here as well. And it is, sorry, here we go. We can also see that now that the index is added, it went from a full table scan to not doing a full table scan, and you can see the drop-off here in the little spark chart, which is handy dandy. Now back to this guy, not refreshing that often. So obviously, we went from 400 queries a second, up to 900. So we've doubled the queries per second with that particular change, which is a pretty substantial difference there. And if we go back, and we look at, let's go, and we'll take a look at my comparison dashboard, all of these should start to kind of flow in and start to pick up. So now, RDS is the slower one, which we can take a look at to see what's been going on on the RDS side and add the database dashboard. Let's go to the rds side. So this one is still kind of laggy. I don't know why that one is laggy. It did create the indexes. That is interesting. So from a consistency perspective, this one is around 13 queries a sec, or connections. And if we look at Aurora, ooh, Aurora is double that. So this one might have another bug. This one's at 25. So I'm wondering if maybe some of the connections when we were messing around, had died and didn't get restarted properly. So that could be work that's definitely a workload change, right? Because when we were looking at rds, Postgres or not, Postgres sorry, rds MySQL. That's why it was wrong. I was in the wrong one. So yeah, they've all got about 25 to 30 active connections, and the number of queries per second on this one hasn't gone up measurably. That is a weird thing. So the question is, why not? Right. And Looking at that last five-minute mark, it actually went down. Which is weird. So the question it did execute. So that is a very strange thing that didn't get reset. So, Michael, why wouldn't? Why wouldn't RDS MySQL get reset? Or have the same impact?

**Matt Yonkovit:**  
Back, same cable definition now. So I can guarantee that those two matches look all the same to me. Alright. So from those now the question is what's has the, what's taking the time, right? And what happens to be taking the most time on the RDS MySQL here over the last couple of minutes is this particular query which is fairly consistent so this one is looking for actor name and cast. So that particular one has been taking the most time, about two seconds. The next guy here is another reporting one. So these are all reports that are taking a long time, which is generally what we would typically see. So I don't know why that is the same way. So let's look at the one that does have like twice the throughput. So this is where it's kind of weird. Like, if we look at total time over here, for the EC2 instance, for instance, and we look at the last five minutes we can see that there's a lot more going on. But those reporting queries are not running here, or if they are, they're not having the same impact. So that's interesting and of itself, right? So why aren't the reporting queries like coming in here? Why aren't we seeing them at the same ferocity or the same impact? And so if we go over to QAN, again, and take a look at QAN, we should be able to just select the MySQL 8 instance. And we should be able to look at the load again. And so we're looking at the load here. Again, I'm not seeing those aggregate quarries. So there is this so that is this the one that we were looking at? Oh, look at that. User PMM has exceeded the Max user connection resource. Whoo. So Michael, what do I do to fix that?

**Michael Coburn:**  
Well, it's happening because we set an intentional limit of 10 As per best practices so that you're serving towards your server. So it's trying to prevent you from doing bad things right now. You can either alter that user to increase that count above 10. Or we can eliminate the reason for the blockage. Why do we have 10 connected users?

**Matt Yonkovit:**  
That's an interesting question. Like, like how would I figure that out?

**Michael Coburn:**  
Well, there is a dashboard PM, User Details dashboard. That would give us some insight on Well, if you're running Percona server only you might need to use your stat loaded to see Is it loaded oh it's off. Okay. Well, we have this whole dashboard that can show you how many connected users and plotted over time it's pretty neat. But the variables are off so the dashboard won't have anything else we can do. There's either the schema or performance schema or we can sample the see the users that are connected see right here I think user summary connections

**Matt Yonkovit:**  
here I'm gonna let you share your screen and I'll drop off mine

**Michael Coburn:**  
Okay, so is it me Sharing now

**Matt Yonkovit:**  
you are sharing.

**Michael Coburn:**  
You see me falling into the matrix. That was weird. Okay. Okay. So current connections on the human user only show three on the EC2 box. So,

**Matt Yonkovit:**  
So it was a temporary thing you think?

**Michael Coburn:**  
I think I was a little transient there. Because what happens in Query analytics is some things are collected over time and some things are on demand. And on-demand at least we run our explanations in our tables. So those who expected the database servers available and there's no blocking of logging in. Let's see if we can get past. Yeah, there we go. That's good.

**Matt Yonkovit:**  
So that was a transient thing. That's weird, that's a weird bug, like a weird thing to see, right?

**Michael Coburn:**  
We were overwhelmed by the server. Right? It was responding to the fact that we had too many user connections. But yeah,

**Matt Yonkovit:**  
could that be the number of end-user connections to the number of people logged into PMM? Or is that the number of things coming from the PMM server to the database server?

**Michael Coburn:**  
 Yeah, it's the database server. It's the ladder. It's how many users called PMM are logged connected to the database

**Matt Yonkovit:**  
And so would that be like so if one thing backs up, then the next one backs up? And it just keeps on piling up?

**Michael Coburn:**  
I think this is what I had done well, two things here, one, you normally are going to have your monitoring, a user connected doing monitoring stuff, and nobody else is going to use that account. So if you see this actual alert, you probably have something legitimate to look into. And part two is I was using the same user, and I was running an altar. And then I ran an explanation which blocked waiting on the altar. So I know at least I was consuming a couple extra connections there. We do that, let's do that. What I want to do is I think we always maintain two or three connections from the PMM user. So you've got seven open slots after that. So I guess somehow somewhere we consume those additional seven. Oh, this is good. So the altar is completed down here at the bottom. 15 minutes. 

**Matt Yonkovit:**  
And during that time, it actually killed off some of the long-running queries as well. And some of the app users failed. That's why we weren't seeing those queries log in. So some of the app server apps actually just went bonkers. And so I just had to restart the app. workload and yeah,

**Michael Coburn:**  
okay, so if the altar is finished, we can see it there. And the CPU look Okay, and so the CPU is back right back up. It's pegged. Now we're getting higher throughput. Can't tell yet. Well, I'm looking at the Yeah, the my scroll eight on EC2 was the new index we hope that we're going to have better throughput is the expectation here

**Matt Yonkovit:**  
that is the expectations here correct

**Michael Coburn:**  
Does it look like it flatlined over a little bit more here okay what else do we see? Well, I oh wait it's back down to where it really ought to be. Wait, you see, that's weird. I only got RDS and Aurora on this dashboard

**Matt Yonkovit:**  
for what for the IO weight? All right. Yeah, yeah. Aurora doesn't collect IO weight. One of those weird things is like you can't get IO stats from Aurora don't ask me why I mean it's like a reduced work set

**Michael Coburn:**  
weird so it throws up a label though and PMM for it and easy to start showing up here weird okay. Oh yeah, so the response time is any better? are under us a millisecond here on EC2? Oh, knots up into the tents. Oh, it was less because we were still running the altar. But if I put an hour probably in a 10 millisecond response time. Yeah, there it is. Eight, nine. Okay, so response time is back pretty much where it started before the altar was running. So I think we did a good thing, but I don't see the impact. I don't see that it's had a material deflection on either QPs and pinned on CPU again.

**Matt Yonkovit:**  
Yeah, I'm sorry. Oh, wait, is there

**Michael Coburn:**  
right now? Nothing.

**Matt Yonkovit:**  
On the EC2, there's no

**Michael Coburn:**  
But it's also not showing up in the graph here. Let's do it from the disk screen.

**Matt Yonkovit:**  
Because IO weight still has CPU cycles available to do other work, right? So it's waiting, it can then use the CPU for other things. So we could add more threads and see what happens as well. I mean, that is an option.

**Michael Coburn:**  
I'm a big fan of these overview dashboards. We have the lake I want you to compare, see what you find. Let's see what we get. I don't need 12 hours, so that's too much. And it should be all of our nodes. Well. It's too many. Let's look at just the databases. we're talking about a desk which is down at the bottom. Okay, so latency looks like that leaves you on Aurora? Half a second. Is that right? I asked for my money back. That's brutal. Too bad.

**Matt Yonkovit:**  
Oh, Michael, don't say that. It's like I said, I left everything by default. Right. So there's probably a lot of room for improvement.

**Michael Coburn:**  
That emitted from the AWS conference.

**Matt Yonkovit:**  
Well, and on top of that, I don't know if Aurora passes back the same granularity in the same information across the board. Right. So some weird stuff. There's some stuff that's missing.

**Michael Coburn:**  
Let's drill in on a row because I'm just really curious about what's going on here. Yeah. Okay. There's something wonky with that other dashboard. Here, it's telling it to millisecond latency.

**Matt Yonkovit:**  
Yeah. So this is what I noticed. So there are actually some graphs that are collected at different granularity, so the graphs don't show up correctly. And part of the interesting thing is the metrics from the API perspective that come from, which call it that come from CloudWatch. They're not necessarily the same for RDS as Aurora. So the names and stuff don't match. And so, therefore, like, you try and build a graph that shows similar things, or add different metrics together, and sometimes one metric doesn't exist in Aurora that that exists in RDS so

**Michael Coburn:**  
Well, it looks like Aurora is doing what it needs to be doing. So it just seemed to be fine.

**Matt Yonkovit:**  
So just to be on the safe side, I did cycle all of the app servers as well. Because with some of those changes that were blocking, I did notice that there were some deadlocks and some other things that caused some of the applications to kind of go a little walk. So play those are going to pick up here in a second. Although I'm not seeing any, I'm seeing negligible changes.

**Michael Coburn:**  
Yeah, EC2 box looks like it's still got resources available here on the discs, we did thrashing pretty hard at him up to 150 or so make per second.

**Matt Yonkovit:**  
Yeah, I mean, it does it at certain times, there are certain activities that can really impact the search server and the system. And I mean, that's kind of the intent of this. So okay, so what I need to do is, I need to get this reset for your floor show. So I'm going to say, we kind of stumped the expert a little bit today. So I'm going to go ahead and I'm going to unwind some of the things that I can reuse some of this later, but just so you're aware, I did deploy a small archival job this morning, which would run every 10 minutes, but it's like a 32nd run. So I was hoping we would catch that. And so now there's a history table. if you will. And so that history table does get populated and doesn't get read from occasionally. So that was one that was going to cause some spike Enos on every 10 minutes, and I was hoping that we would catch that. But obviously, that didn't transpire. So I'm going to go ahead and kill those guys right now and get rid of the loads and those other ones. So if you do a search inquiry analytics here just just do like a search for a query named history or that has a history in it. And you can see what that is. So there were a couple of different deployments that would come up. So that's one of them. And Michael, can you maybe zoom out on your window a little bit just so people can see it a little easier? So yeah, so look at the example for this one. So this is one of the ones that has a voting count history, which every 10 minutes, just selects everything out of the voting count and puts it in there. So then you can graph what it was on an hourly basis or whatever. So you can see vote counts, per hour, basically. And so that was added. And I left that on optimized. So there is that. And then there are a couple ancillary queries that go along with that as well. Yeah, that was the big change that I made. Everything else was caused by the end-users at conferences doing like, a lot of knob turning and a lot of changes. Right. So

**Michael Coburn:**  
Do we have a picture of the box? Do we have to show that with our audience?

**Matt Yonkovit:**  
Um, I thought I should, there's one on Twitter, I think, or maybe in general slack, if you took a look there, but so so there's that, and I'm gonna go ahead, and I'm actually just killing those extra jobs off to see if we can get it back to where it was. Because I think that we had a pretty consistent workload yesterday, right. And for those who are still hanging around, which there aren't many, this is where we're trying to just get everything back to where it was at the start of the show, make sure that everything is working there. And sometimes you just find these wonky things. Over the weekend, I was working with this, and I actually upgraded Python from 397 to 310, and saw a huge regression. And it's these little things that matter, quite substantially that you aren't aware of, that this could have such a drastic impact on the system. And I think that that's one of those things that you have to be mindful of, is a lot of times these little things matter. And in this case, I think that some of the changes to workload and some of the other things that we were letting people play around with. did its job, it showed that there were easy ways to potentially break systems. And that's what we did, right.

**Michael Coburn:**  
We're able to do so that's right.

**Matt Yonkovit:**  
Yeah. So I just reset everything, Mr. Michael. And let's see, we are way over what our plan time was, but that's okay. I've got the time of course. And you need to get to the show floor in another 45 minutes. That is very strange. Yeah, well, it's back to Yeah, it here. It will share your screen again. So it's back to EC2 still doubling up what the RDS and Aurora were doing, which is still problematic. And that's the other one that I noticed yesterday, even after the workload so this is without anything that I've added, without the curveball that I tried to throw you. This is where those Aurora and RDS instances just appear to be struggling more and that's where I'm like, I don't I don't quite understand why. And when I go look like when I go look at RDS specifically just RDS

**Michael Coburn:**  
 we've got, one thing that occurs to me would be to compare the configurations using PG config diff.

**Matt Yonkovit:**  
I'm also wondering if maybe the scheme has gone out of whack or something. I mean, it doesn't make sense that you would see such a drastic difference, like a 2x difference, like we weren't getting that initially. So something had to have changed. Between the two, right, like so. So the fact that there is literally like, 1100 queries a second versus 500. And we are pushing through the exact same number of connections and things on these, it makes me question if you will. Does that make sense?

**Michael Coburn:**  
Yeah. Good sense to me.

**Matt Yonkovit:**  
And that's where some of the things when you're using like, PMM for troubleshooting, especially if you're comparing two different environments, this is where I would set this up to compare rds, and Aurora, if I was going to, like, I want to know, what kind of performance am I going to get, I want to work on the workload there consistently for a few weeks, and I want to see these differences. Now, those who are watching aren't going to have like a box at all, you're just gonna randomly click buttons and like indexes drop and schemas change, and workload is maneuvered around. So you're not going to have that same issue. But it is super interesting to see these breaks. So hold on, let's see, by the way, Barrett's saying he's at the booth already, he's like, what's the laptop password? Oh, leave alone. She's gonna start playing with the box over there.

**Michael Coburn:**  
Don't touch the buttons

**Matt Yonkovit:**  
Alright, so let's see what we can do in the next 10 minutes before Barrett needs to go off and do this. But I think that checking to see if you know that the schemas are aligned is one potential thing that we could do like I said. The workload is the same, we're seeing the same number of connections between the two and that is super similar. So the question is, what else could potentially be there? And honestly, there really isn't much like from a boxing perspective that the things that I do that we allow for to happen on this thing right.  you can drop an index on year drop on year and actor drop on title you can change from varchar something else you can do some copy so the fact that that that performance regression is so severe is just so strange and it looks like it's all on the actor type queries it's all on the analytics Yeah, I mean it appears to be all on analytics which might be I'm curious so go to clan and in clan just search for count star or average IMDb Rating Alright, so go ahead and sort by the query, the count or the query name if you can. Basically, you should see all three of those boxes side by side right. So which is cool which is what I want is I want to see all of the ones that are that select acronym your account that you see you see that one too like there's each box should have its own record. Yeah, but

**Michael Coburn:**  
This is the aggregate of all three. Yeah, I have to deselect on the left I think one at a time to compare them.

**Matt Yonkovit:**  
Yeah, so um, but if you look at the three of them, you actually see that they look like the query time is identical on all of them. So it doesn't look like that's causing the issue. Wait a minute,

**Michael Coburn:**  
hold on a sec. Oh, yeah, one outlier there. There's 11 seconds versus three seconds.

**Matt Yonkovit:**  
So wait. So all right, so I found this guy here. Let's see. So it's, it's this one. So here's an example. Okay, so here, I'm going to go ahead, and I'm gonna, I'm gonna, I'm gonna take over for a second. All right, so, this guy is the example here, right? So this one, you can see the query times, the running, and all the boxes. But on this particular box, here, 20 seconds is the query time, 18 seconds, and then seven seconds. So that would be a pretty drastic difference between the two or between the three different boxes. So it's that particular query that's causing the issues? And it's grouped by your acronym? I'm guessing your acronym. I'm guessing the acronym is missing. Hold on a second. I'm guessing that's what it is. I'm guessing we're still missing an index. normalized? Yeah, I think that yeah, normalized actors. Because if we look at the explanation here, we've got a full-on. So yeah, so we've got the full story here. On C, which for us see is the normalized actor, so it's doing a full scan on that. Whereas this one here, yeah. So look, look. Yeah, that's what it is, Michael. So the index has got out of sync in those boxes. So see here, right here, like we've got, this one has an index on the actor ID. And that one is not using one on the actor ID. So that's strange. So yeah, we're missing an index. So I think if we add that index, we can fix it real quick.

Let me get to the show. And I'm loading from here.

**Michael Coburn:**  
All right, you go, you could do that. And we're still alive. So hey, live, everyone. Thank you for sitting with us and troubleshooting all of this stuff. This is how things go sometimes is figuring out how these inconsistencies can show up but hopefully, people learn from us fumbling around this morning. But we appreciate you hanging out. And until next time, next time, we should be up next week, Marcos and Nando are going to becoming. And I'm going to give them a broken box and let them fix it live so their box won't even start.

So we'll say you're really gonna put it to the grind.

**Matt Yonkovit:**  
Yeah, yeah. So Alright, everybody. Thanks for showing up. I appreciate you hanging out.




![Percona MeetUp for PMM Dec 1st 2021](events/percona-meetup/cover-pmm-december-1920.jpg)

## 1-hour MeetUp for PMM

* Date: Wednesday, Dec 1st, 2021 at 11:00 am EST (5:00 pm CET or 9:30 pm IST)

* Live chat on [Discord](http://per.co.na/discord)

* Live stream on [YouTube](https://www.youtube.com/watch?v=Ax5McTZifmw) and [Twitch](https://www.twitch.tv/perconalive)

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=N2ZqcmFxYnBiZjNrN2JuYjMxaHNjdmgxN2wgY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)


## Topic
Live stream from AWS re:Invent with Michael Coburn:

* Tour of the AWS re:Invent celebrating 10 year anniversary 
* Latest news on PMM (Percona Monitoring and Management)
* Demo of database monitoring and performance optimization
* Q&A


## Attendance
We welcome everyone! Come and benefit from the MeetUp if you are:

* Developer, Engineer, or DBA working with business-critical database environments

* Student or someone who wants to learn more about open source databases

* Interested in monitoring your database performance with PMM

