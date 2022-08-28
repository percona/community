---
title: "Setting Up and Installing Backups With pgBackRest - Percona Community PostgreSQL Live Stream & Chat - May, 6th"
description: "Learn more about setting up and installing backups with pgbackrest in this Percona Live Stream for PostgreSQL"
draft: false
images:
  - events/streams-pg/PG-Stream-Week-4-pgBackRest.jpg
date: "2022-05-06"
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---

![Percona Community PostgreSQL Live Stream & Chat - May 6th](events/streams-pg/PG-Stream-Week-4-pgBackRest.jpg)

Listen out to this full recording of the live stream dedicated to PostgreSQL hosted by the Head Of Open Source Strategy at Percona, Matt Yonkovit, with Charly Batista, PostgreSQL Tech Lead at Percona. They took us through the setting up and installing backups with pgBackRest
This is a part of the bi-weekly Live Streaming series to discuss Postgres-related topics and go deep into technology secrets and tricks.

## Video

{{% youtube youtube_id="L0ft6RtGE7Q" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit**  
oh, here we go hello everybody out there in stream land we are glad you are joining us wherever you are. Hopefully, everything is working for everyone. It looks like there was a little bit of a snafu with some of our setups today. So if you didn't get a notice that the event wasn't scheduled it was and now it is back on. Hopefully, there isn't too much lag. I'm noticing a bit of a lag in the screens here. So welcome. Welcome. We are here for our regular bi-weekly live stream. So today we're here with Charly yet again. How are you doing today, Charly?

**Charly Batista**  
Well, I had a tough night, but I'm feeling a bit better.

**Matt Yonkovit**  
Oh, oh, I hate it. When there's a tough night. I know. Yesterday you had some technical things you're working on around XID wraparound which is never fun. So you know that that's one of those things. That is never a good thing at all. But, I know, we want to wrap up our backup series. And so today, we're really, really focused on backups. And so we've done two other streams on backups. This will be the third hopefully the last, the last one. And today we want to talk specifically about PG backrest.

**Charly Batista**  
Right. Exactly. Yep. That's Yes,

**Matt Yonkovit**  
yes. And so if you are out in stream land and are watching if you could give us just a howdy Ho, just to make sure it's working? I would appreciate it. We just want to make sure that things are, are going okay, you can hear us. I don't see anybody yet. Let's see it live now. I'm just gonna go out there and just give ... through my own chat just to make sure it's all coming through. So all right. So Charly, why don't we go ahead and get started out there? Hello came through. So yay, chats at least working? Why don't we go ahead and get started, Charly, now you have done some prep work for this particular stream correct?

**Charly Batista**  
So, let me share my screen here. We're gonna share your screen so

**Matt Yonkovit**  
and just be mindful, I might be monkeying around with Charly's little tiny video here in the corner. Because before the stream I had to reset some stuff and things just didn't look quite right. So hopefully that works. Okay. So yes, So Charly, we see your screen and you are now 100% In short,

**Charly Batista**  
yeah, I mean, thanks. So the first thing we do here is to install the backrest. So on the Ubuntu version usually pretty straightforward right on what we can do an ap-get-install pgbackrest that's it we have it installed and that's it done.

**Matt Yonkovit**  
We hope you enjoyed our live stream everyone

**Charly Batista**  
well actually your box is broken there was a message error message there but that's fine. So weighing

**Matt Yonkovit**  
it is not my box that was broken. It was your box it was broken. Mahesh is hanging out with us again today. He says Hello Charly. He doesn't sell say hello to me. But that's okay. I said hello Mahesh. 

**Charly Batista**
I do hello that I say hello to you so you don't feel lonely. Yeah, so yeah, so long we poor by a poor guy, poor guy. So we got it installed here. Now we need to go through the configuration right so the configuration file for the PG backrest it's by default on Ubuntu is /etc/pgbackrest.conf So this is the default configuration file. This is all we get when we install it here. So can you see properly here on the edge? Because I can't I cannot release you're gonna see that is our here I don't know if you Okay, yeah, you

**Matt Yonkovit**  
can you can, you could barely make it out. But it is their

**Charly Batista**  
choice there. Now it's better for you to see right I apologize about that. But just realize that I was checking the configurations here and they are missing. Okay, now we can see. So are they A few things that are very important or pgbackrest. We're going to go through them here, while we are configuring our backup on the configuration files. As we can see here, we have sort of sections, right? So we have this global, they give us this example for the main something. So we have some defining variables here, right? So, when we are creating a configuration file for a PG backrest, we can define some global variables that work for everybody. And we can have some specific configurations for backups that we want to create. Those are specific configurations, PG backrest calls it instance. I don't know why they use this name, but this is more the call. So for example, this one is an instance name, it may be on the styles that configuration we're going to put the information that is specific for that backup, for example, here on this server, your database installation is on var lib Postgres version 13. Nope. The main is pointing for this slash data slash main it looks like it doesn't exist.

**Matt Yonkovit**  
I can tell you why. You want to know why.

**Charly Batista**  
This slash. So Mr. Charly,

**Matt Yonkovit**  
remember how he's laughing? But remember how on our last stream?

**Charly Batista**  
Yeah, it was working. We recover the database.

****Charly Batista****  
No,

**Matt Yonkovit**  
no, no, no. I can tell you exactly what's wrong. What's wrong?

**Charly Batista**  
If you have no database,

**Matt Yonkovit**  
you created a mount point. And you didn't

**Charly Batista**  
put on the auto mount Fs that's okay.

**Matt Yonkovit**  
Yeah, you didn't you didn't set the FS tab.

**Charly Batista**  
Okay. That's okay.

**Matt Yonkovit**  
you just need to mount the device. And then you can start Postgres and you should change the FS tab. Hey, Gonzalo.

**Charly Batista**  
Ah,

**Matt Yonkovit**  
you take a screenshot of Charly's face there is he's going like, wait, wait a minute, there's no database. It's like, yes, Charly.

****Charly Batista****  
The backup for these databases doesn't exist. Right? So yeah, we have the backup system. It work about twice the database that I got.

**Matt Yonkovit**  
It's okay, we will all forget to set the Fs tab once in a while.

**Charly Batista**  
Okay.

****Charly Batista****  
I suppose now I have something here.

**Charly Batista**  
I still don't have any backup data.

**Matt Yonkovit**  
Have you actually created a backup device in the data device? I think

****Charly Batista****  
it takes a look. Maybe? Yeah, the day. It's 11 gigs

**Matt Yonkovit**  
you are used as 190 gigs. So there should be data.

****Charly Batista****  
Okay. Hold on.

**Charly Batista**  
I only have one logic.

**Matt Yonkovit**  
Yeah. You said there's nothing under there. But there is no. Right. There's to be like, Look at the like, do it.

**Charly Batista**  
Okay, yeah, it might be. Well, explain to me, okay, yeah, it was Linux. I was inside of the folder probably. And when I mounted and I saw I needed to leave the folder and come back. Okay. So at least a really

**Matt Yonkovit**  
Yes, center yourself, Charly center yourself. Yes, that was not it's a little mistake, but it can cause you to have all kinds of heartburn. Yes.

**Charly Batista**  
Oh, yeah. I almost had a heart attack. Okay, let's go back. Let's check. I would recommend you

**Matt Yonkovit**  
take the moment to put it in the fs tab. So when we do the next stream, you don't have another heart attack. You lose a year every time that happens, like yeah, into what drains from you. Did and while Charly's doing that I'd like to remind you all who are out there in stream land or who is going to watch this video. After the fact, if you are coming to Percona live Charly will be there. And so you can come out and say hi to Charly say hi to me we're going to have a little podcast booth set up in the main section. And so if you are interested in coming out CNS that will

****Charly Batista****  
be awesome don't forget to ZFS Yeah, no,

**Charly Batista**  
I just want to get the

****Charly Batista****  
the footpath here.

**Charly Batista**  
I usually don't. I'm just being lazy here. Don this I like to work with the UID but I don't want to get it. It's fine

****Charly Batista****  
the six address has to discarded what should work No,

**Charly Batista**  
we just want the false ones.

**Matt Yonkovit**  
It won't work you have a typo?

****Charly Batista****  
Why have a typo? Where What's your mount point

**Charly Batista**  
I'm just checking if you actually have mentioned

**Matt Yonkovit**  
I'm not being a jerk. You missed the boat

and Mahesh is gonna tell me to be nice to Charly. Yes. I'm sure he will. Yes.

**Charly Batista**  
So of course it's the busy side of Okay. worked okay Don't be lazy put the right tax but for now, we just won't work and Rebecca

**Matt Yonkovit**  
Yeah, yeah. Postgres it'll be down now. Right so don't forget that either.

**Charly Batista**  
Yeah. But we have a script in our problem in our script for the post with you right so you've never said that right? So I never

**Matt Yonkovit**  
fixed it. It is on Charly

**Charly Batista**  
we want to start well interesting so it probably well, we have the postmaster opportunities. Right. And it's pointing to DC minecon That's correct. Why it says

**Matt Yonkovit**  
is the directory not permissions for your symlink because it is your symlink is your sibling word?

****Charly Batista****  
That's a good question.

**Charly Batista**  
I don't think so. That it might be it's a good question Okay, I'll possibly is 13 is also Postgres may both screws.

**Matt Yonkovit**  
There's also another master ops file there.

**Charly Batista**  
Yeah, this is outside this is a backup. Okay, off the backup just to make sure we have enough backup right? Okay, here is fine data. It's false as well. Inside it is everything possible. Okay, let me just sit in the error message again. See? Yes. Okay. Fine. I am waiting for blah blah.

****Charly Batista****  
Stopped

**Charly Batista**  
could not start server Okay, at least change it for we're inside of Maine

****Charly Batista****  
six logs. Check the logs. I suppose this last one seriously, again,

**Charly Batista**  
never create this way for the always.

****Charly Batista****  
This appears, I suppose

**Charly Batista**  
I should change this configuration on the Postgres file later.

****Charly Batista****  
Yes, indeed.

**Matt Yonkovit**  
That's what's preventing it from starting up. Anyway.

****Charly Batista****  
Yes, it is.

**Charly Batista**  
Well, there's always something else

okay, I just want to have fresh logs bold and I am sure that I'm getting the right one

****Charly Batista****  
okay.

**Charly Batista**  
This is a folder. What's supposed to be this one? This folder exists, why it's not able to create this number why

****Charly Batista****  
in a lot? Okay, so

**Charly Batista**  
if I try to create a poster is it? Yeah.

****Charly Batista****  
Can

**Matt Yonkovit**  
I think it's looking for that as a directory isn't it? Couldn't create the drag directory?

**Charly Batista**  
Yeah, probably Yeah, you're right, you're right well, I can do it here. So I don't need to change the ownership.

****Charly Batista****  
Now you can start it right.

**Charly Batista**  
Now we have a database backup. Yay. Yay. I just forgot what I was doing. Okay. Yeah, I was checking which folder the data is in. Well, we are talking about Yes.

**Matt Yonkovit**  
Yes. The last 17 minutes were brought to you by gremlins. They are always in your database.

****Charly Batista****  
Yeah, always.

**Charly Batista**  
So here, then when you create a stanza, this is the configuration for our backups. Let's this is the easiest way to think about that. So I can have different backups of my cluster, right? Usually, we don't need that runaway. Like usually, whatever. Each instance that they have here, for example, we have these posts was running on port 5432. I just prayed to an instance to back up these databases. So we can have a PG back REST server that's taking care of all my databases. That's what for example, if we had here, topology, where we have a primary and queue replicas, so I could have a backup server using PG backrest and the backup server will take care of the backups. We could back up all three servers, we could back up just only one replica because usually, we don't want to put that stress on the primary right so we could back up on one replica we could back up two replicas. And the PG back backrest can also take care of the world files, the archive and files. We will change our configuration here 2.2 PG backrest remember, the last time on the backup, we were streaming the archive files to one folder using our scene, right? Remember that so today we're going to change that we're going to change it from our sync command to use the PG backrest Okay, so to do that, we need to create our stanza right I want to call my style we can name it whatever can give it whatever name you want to give it. Do you have any special names that you want me to give you? The last lesson get something more fancy like eg one

**Matt Yonkovit**  
Wow, you're going fancy. You're going all out there, I don't know if I can, I can hold both.

**Charly Batista**  
I like the big one is quite nice. I like which one I want to use and which one is okay. So, we also need to tell the database I mean not the database PG backrest where your backrest can find the database bath right

****Charly Batista****  
so just a second here I'm having some okay issues

**Charly Batista**  
Okay, now it's working. This is the problem Are those wireless devices sometimes just go?

**Matt Yonkovit**  
Do you want me to buy you a nonwireless device?

****Charly Batista****  
Well,

**Charly Batista**  
I mean, if you want me to give me one device, I'll be pretty happy to do that. That would

**Matt Yonkovit**  
be okay. So I need recommendations for the best keyboard for Charly for the live stream so I just got Carly or Charly a nice pair of headphones and a sound card and and a microphone and a new camera too. So he's going to be all in.

**Charly Batista**  
Well, that would be amazing. Like if I could if we could get a setup like that, man. I could stream lights.

**Matt Yonkovit**  
It's never a week. It's ordered. It's ordered. You're gonna pick it up at Percona life.

**Charly Batista**  
Whoa, thanks a lot. I appreciate that. Yeah,

**Matt Yonkovit**  
you wouldn't you and Marcos both although your video quality is better than Marcos is Marcos. Marcos is I don't know what's going on with his

**Charly Batista**  
my cozy is using a really old MacBook, probably if the one that I the last one that

**Matt Yonkovit**  
he doesn't use a MacBook he did. He hates Mac. I knew but

**Charly Batista**  
he has one MacBook for those things. He used his Linux device to work, but he has one really old MacBook device that when he does not need to do those things, he uses those ones. Okay, what are you doing here I am getting this the database path. The data gap is not the database the data gap is half a year. Either in our case is virally post ms 13. Main

****Charly Batista****  
searching

**Charly Batista**  
because of the PG backrest, we need some files when accessing the database, right? So one thing that I also advise is to create a user or to take that backup or user that has the right privileges, I don't really remember the top of my mind. So for our exercise today, I'm just going to create a new user that has a super user provider so it's easier. But for now, like what we have here is the PG backrest going to use this folder here as our repo for the backup. So as we just put it on Main, all the backups that we create using these instances of piggyback were gonna saved here, I don't want to save you remember that we have something on data backup, right? I want to create a folder there just mainly after a big rush rest. So I going to create this folder. And they're going to do it as you want to. Not you want to post with the user because I want everything that we do to be okay,

**Matt Yonkovit**  
you don't have the backup directory.

****Charly Batista****  
You need to

**Charly Batista**  
don't I think they had that

**Matt Yonkovit**  
one. It was B I think you call it BK up or something?

****Charly Batista****  
Oh, maybe? Yeah.

**Matt Yonkovit**  
Gorgeous. New. New. P ITR. Yeah, yeah. Just before you do any exercises here for this though, make sure you clear out some of that space because you were at 190 gigs used.

**Charly Batista**  
Oh, we actually have. I know. Okay, I need to be rude. We have a space available, right? So

**Matt Yonkovit**  
you can add another 100 gigs if you want.

****Charly Batista****  
Yep, yep. See,

**Charly Batista**  
this is my keyboard. Sometimes it doesn't work. Sometimes it's just going to add that extra 200

**Matt Yonkovit**  
I'm going to go buy you a keyboard right now. A wired keyboard. You're are you using it? Are you using it? You're not using a Mac? You're using a Windows box, aren't

**Charly Batista**  
you? No, yeah, I'm using Linux, not you know you're

**Matt Yonkovit**  
using Linux. So yeah, so it's okay. I just needed to make sure I got you

****Charly Batista****  
the right keyboard. I'm doing a

**Charly Batista**  
mountain point. It's on. Okay, I just added extra 200 gigabytes. So now we need to do it. FS right. Next, FS not extents, it's Grow. Grow Fs Yeah. All right. Cool. Now we have 200 gigabytes. Pardon? Yeah, almost 200 gigabytes are available on that volume. So we are fine with disk space. Let's go back here. Okay, we have this folder. So what we have here we have the folder that we're going to send the backup, and we have one, b stands that this is our first stanza. So I'm not going to do anything here, I will just try to check if this is going to work. So, to do so, we need to create the stanza. Right, so we need to go PG backrest. Let me find them here on my notes because they don't remember all the parameters

Yeah, it's done I'm running as root, right? I don't want to do it as I wrote because, or else I need you

**Matt Yonkovit**  
ever written Postgres user?

**Charly Batista**  
Yeah, because all the folders and everything got to be created if it was going to be created as word and I need to. To change such good systems. They start the name we are using Did you want the fancy name, right? So I want to log the information anything that comes to my console here. With the info the various the logs, they have different how we call different not levels. You can define if your font like the info,

**Matt Yonkovit**  
the air warning, so you can define much detail. Yeah, how to get rid Yeah, yeah. Isn't PG backrest just Python? It's written in Python, isn't it?

**Charly Batista**  
I know it's if I don't mistake it's Perl.

**Matt Yonkovit**  
I thought it was Python. Because yeah, anyways, got me. Yeah, we

**Charly Batista**  
will see now because, remember, we only stole the PG backrest. I didn't install the drivers for Postgres, and if it's pearl back on a failure because it won't be able to connect to the database.

****Charly Batista****  
Right. So

**Charly Batista**  
and it was

****Charly Batista****  
aborted.

**Charly Batista**  
It was unable to find a primary cluster. Why was it unable to find a primary cluster?

****Charly Batista****  
And the clue is well,

**Matt Yonkovit**  
is it a configuration error?

****Charly Batista****  
You didn't tell it like you didn't give it the details.

**Charly Batista**  
What do you mean you didn't give the details?

**Matt Yonkovit**  
I have not used the PG backrest. So you're asking

**Charly Batista**  
Okay, okay. Okay. Okay.

****Charly Batista****  
Well, I

**Charly Batista**  
bream not premature, but I really believe that it's on vital Bytom, so let me the problem is this. Even though we are on asking for info level of information, this information here doesn't say much, right? So it can probably be the driver's number. So let me stop here. Stopped libs dB. For all I think, that's it to be PG. O. D.

**Matt Yonkovit**  
Do an app cache or App Cache, and then you can search

**Charly Batista**  
for lib G Okay. Well, that's quite a lot to do did I type anything wrong? Musta had to add an arrow Yeah, I must have some Bible. Okay, let's try again.

**Matt Yonkovit**  
You got an error on the install, didn't you?

****Charly Batista****  
What is on here?

**Charly Batista**  
Yeah, Uh, it, it's something with the package library here is broken.

the primary cluster cannot be perky unable to find primary cluster only able to log into Mark can log into SQL. We're using Postgres. Okay, let's let me try auditing. Yeah. So the z, that you backrests,

**Matt Yonkovit**  
the hash says, PG hba.com?

**Charly Batista**  
What is that? Sorry?

**Matt Yonkovit**  
My hash just suggested that it could be something with a PGH pa.com.

**Charly Batista**  
Yeah, can be something related to the user and authentication. So the thing is, usually, when is an authentication issue, we will get the authentication issue to the authentication error there. Right. So it will tell us that that was these authenticate, it was not able to authenticate the user. And this is one thing I'm trying, and I will force it here. And wonder here. Did you have one user? I got just to use whatever user Charly doesn't exist.

****Charly Batista****  
So save. And

**Charly Batista**  
here, now we should have saved it was not unable to connect to the database. So because the user trolley doesn't exist, right? So this is the error that we get now that I created that user. So we at least know that the PG backrest is following the configuration file that we have. And it's trying to connect to the database. And this is a good thing if it failed pre-authentication, is because this is a message from the database. So it gets it has the database driver because if I didn't have the database driver, it wouldn't be able even to try to connect to the database and get that message from the database. Right. Okay. Now that we know the user Charlene is not there, let's try using it for screws. Right? And let's see what we get

****Charly Batista****  
it doesn't carry

**Matt Yonkovit**  
so do you have to put the stands I was just looking at the user guide, and it does not do dash stands at

****Charly Batista****  
all? Well, ah, well, okay.

**Charly Batista**  
We can try to create all of them. That's fine.

**Matt Yonkovit**  
Yeah, I mean, just the demo I'm just looking at the data.

**Charly Batista**  
Because you're going to create, yeah, we only have one standard, right? So all create that one. Yeah, it does require this stanza.

**Matt Yonkovit**  
So, okay, so but when you're doing the Quickstart it says you first have to create PG create cluster first you create closer to here.

**Charly Batista**  
Then the documentation you

**Matt Yonkovit**  
PG backrest user guide right now. Okay. And yes, indeed, it says Quickstart is set up the demo cluster, and then it has sudo PG create cluster than the version that district

**Charly Batista**  
to create the database cluster, PG create DB is now

**Matt Yonkovit**  
configure the cluster stanza.

**Charly Batista**  
Yeah, because that's the database process we read have the database. Okay. Let's see. So configure, so yeah, on that one, you first need to know that that's what we did. We made sure that we have the database because you need to create the database, and then when the database is run I need we also need a database to be running because well we need for the backup purpose, we need the database running right

**Matt Yonkovit**  
yes

**Charly Batista**  
let me just double-check here that this path

it might be a problem with the path pointing to a symlink

**Matt Yonkovit**  
that will work with the slash data new

**Charly Batista**  
well yeah, it would that lead change it

**Matt Yonkovit**  
I mean, if it's the same link, yeah, it is. Yeah.

**Charly Batista**  
It might be a problem with

****Charly Batista****  
oops, not this one. Is data No. Here we go, still the same one aborted with

**Charly Batista**  
exceptions zero 65 Okay. Exception zero 65

****Charly Batista****  
Let me take a look okay, actually

**Charly Batista**  
all the people had this problem

****Charly Batista****  
okay

**Charly Batista**  
based on pause here saying the problem is on the labor pick kill

is the socket file name

we didn't change the socket address, did we? I'm

**Matt Yonkovit**  
not sure we can take a look

****Charly Batista****  
okay, but no, that's another

**Charly Batista**  
Yeah, in this example that I see here, it states that it was not able to define the socket file.

****Charly Batista****  
Okay, let them do

**Charly Batista**  
three user back cap as a super user goes, I'm lazy. I don't want to check the end with this very complicated password, right oh yeah, I need to tell it's the password

**Matt Yonkovit**  
okay. Oh, it's

**Charly Batista**  
a read-only transaction, my database is in read-only mode interesting. Interesting when I wanted my database, that's a good question why my database is needed only mode. Okay, let's

****Charly Batista****  
try to

**Charly Batista**  
let's go for the great news so because we are in a recovery mode

****Charly Batista****  
Ah, well, that would explain a lot.

**Charly Batista**  
Okay, now we need to restart the database

**Matt Yonkovit**  
Yeah, so if those joining us this time, we put this in recovery mode, the last stream but didn't clean that up.

**Charly Batista**  
Okay, now I can create the database. Okay, before trying to use this user, I will change for this user later. But

**Matt Yonkovit**  
am I? Let's see if it clears up here.

**Charly Batista**  
Yeah, if it does something related to that recovery mode, Okay,

**Matt Yonkovit**  
ready to change back to the?

**Charly Batista**  
I will. Yeah. So it looks like there was not a cheat sheet if the same link.

**Matt Yonkovit**  
So here's, here's the funny thing here, everyone.

**Charly Batista**  
And now we just create the distance. Yep.

**Matt Yonkovit**  
So everyone who's watching here's the funny thing is a lot of times, it's the simple things that get you. Right?

**Charly Batista**  
Yeah. Try to create a new user and check if you are the web in recovery mode.

**Matt Yonkovit**  
Clean up the old, old stuff; I guess, right?

**Charly Batista**  
Yeah, yeah, indeed. So we have the stanza it's created now, we just saw the PG backrest, I look, I have this configuration, I want to use this configuration, and this configuration is pointing to this database. So, every time I refer to this guy, this is done as a PG one; it will use those configurations. And we will do that in the processes, right? Remember that I told you that we are going to change the configuration of the database to use the PG backrest? So you remember that?

**Matt Yonkovit**  
Yes. Your AD FS you were asking one of those rhetorical questions that you didn't expect an answer to.

**Charly Batista**  
Oh, that was a valid question. Okay.

**Matt Yonkovit**  
And they're all questions are valid, Charly?

**Charly Batista**  
Yeah, I'm trying to remember where the configuration is. It's on. Or which one, of course, raises the pulse without a cough? Oh,

**Matt Yonkovit**  
it sounds fancy, right? Yeah, it's the Postgres Postgres SQL, the 13

****Charly Batista****  
main and, okay.

**Charly Batista**  
All right. So I want to change the archive command.

****Charly Batista****  
And it's, I will just duplicate this one.

****Charly Batista****  
So what are we going to put here,

**Charly Batista**  
we want to call the PG back ranch. And the stands we have, it's a tricky one, right? That's why you need to do fancy names because it's easy to remember. And we want to work drive. And let's go back here. If I do PG backrest, help it to give me the comments we have. So what we want to do is to push the wall files to the archive, right? This is what we want to do. So then this is the comment that we will use there is archive push; I will copy and paste because they have this problem with the keyboard, and also, sometimes they just missed it. And they blame the keyboard for those anyway. So our archive mode is on. So we are archiving, and they're caving command; we're just use the PG backrest. I have to put some time out here.

****Charly Batista****  
I'm going to put my ad off

**Charly Batista**  
five minutes timeout. It's okay, right 300 seconds, it's I think it's if it takes more than five minutes to archive one file, so something is really, really wrong. And they want to know that's it; that's all the configuration that we need to do here for Postgres to be able to archive the files. But before I do anything, I just want to share what we have on those folders as a backup. So see, when we created that stanza that still has the PG backrest already started creating the folder. Holder folder reference and architecture here. So inside of this, the backrest that's created by so we are at we have this archive folder At the moment, we don't have anything because, well, the Postgres is not pushing through the archive. Anything here. So when we restart the Postgres, and you start some load on that on that database, we should have started to have some archiving here, right? Also, regarding the folder backup, we should not have anything here because, well, we don't have any backup at the moment. We haven't started it. Exactly. Today, we want to do those backup things manually, right? So I want you to keep the call today under less than one how when I went and a half, so we're going to do the backup manually. We're going to create a full backup, we're going to create an incremental backup. And we're going to see the archiving process, and then we're going to recover our full backup and probably incremental backup, as an exercise for today. And we're going to call it a day. Does that sound good?

**Matt Yonkovit**  
Sounds good. Let's roll. Let's rock and roll. Okay.

**Charly Batista**  
So I need to restart my database. Because change the config just changed the configuration. So that's okay; it's restarted. Can you start the load on? On this database? Man? Oh, you

**Matt Yonkovit**  
want load? Oh,

**Charly Batista**  
yeah. Like we wouldn't have I didn't know that you wanted to load. It doesn't need to be that load can be a load

**Matt Yonkovit**  
of servers. So I just need to go straight to the observers.

**Charly Batista**  
I suppose it doesn't take more than 30 minutes, right?

**Matt Yonkovit**  
No, it won't take more than 30. Everyone's a critic,

**Charly Batista**  
horrible entertaining people, I don't know, good jokes, all the jokes that I'm backing up,

**Matt Yonkovit**  
just, I mean, yes, I'll generate load. But it's just going to take me a few minutes to get over here and log into my 17 security systems. In my okay, my 18-factor authentication. I don't know if anybody else has 18-factor authentication. I do. It's like, every mouse click requires a new authentication.

**Charly Batista**  
Okay, let's create a four backup. So we can always rely on the help to set up so that we have here right so, and we're going to create a fallback a backup now. So we can create a backup at any point, for example, that we don't have a load that must be faster. So we should always tell the PG backrest, which stands for which configuration which instance we want to backup; remember that the stencil has the configuration for that instance for the backup we're doing. So in our case, we're going to use TG one to see how important that was to use a fancy name. We want to create a backup. Right? But we need to tell the database we can tell the database what type of backup we want to create. And what type of backups can we have? Do you remember?

**Matt Yonkovit**  
Differential? We can do differential. We can do incremental or false

**Charly Batista**  
or false. Yeah, exactly. So and right now, we need to start with the full backup right, so if you don't have anything, let's just ask you like

****Charly Batista****  
okay

**Charly Batista**  
okay, yeah, help back up. So, we can send some parameters or do the PG backrest, right? So we can tell what type of backup we want to use, for example, if it's full with differential if it's incremental, so, the first one that we need to execute is a full backup my M See, there are many, many options here that we can tell him do the PG backrest right. So then the type that one, for now, is full. So let me tell you, there is stanza is each one we want type equal hole, and we want to do a backup so

****Charly Batista****  
it should work.

**Charly Batista**  
It sets the option for retention for

Yeah, it's telling us that we don't have retention; we don't have a configuration for the full retention that we want for the backups; it might be a problem because we might run out of space. If the PG backrest doesn't do some rotation the backups are based on the retention policy that we have. So it's a good idea always to have a retention policy; when you're doing the configuration and those policies, you can get all just the standard that we have just this rapport that we are recreating here, right? So it will take some time. And I'm glad that it's taken some time because I want to check here what is going on. When I typed the post, Chris was here. So we do see those guys work and say that the PG backrest they're working here, will open a connection to the database, right?

****Charly Batista****  
So these these

**Charly Batista**  
the full commons that it was, it was running here, like the to execute to do all our backup. So we don't have much I can't see our connections here. Your application is connected here, man. Oh,

**Matt Yonkovit**  
um, so I just started it up. Okay, I don't know if it's going I

****Charly Batista****  
was it just you see any now?

**Charly Batista**  
Oh, no, it is No, but I can see the archiver field on this file.

****Charly Batista****  
Which is not a good thing. For suppose

**Charly Batista**  
my backups are going on here.

****Charly Batista****  
So okay.

**Matt Yonkovit**  
So it is trying to

**Charly Batista**  
connect. Okay, yeah. Now I see one connection. Yeah, it'll

**Matt Yonkovit**  
it'll start with one, and then it will ramp up after it warms up.

**Charly Batista**  
And move Jason user movie. JSON test database?

**Matt Yonkovit**  
Yes. Nope. And now it's starting, starting to roll, starting to roll.

****Charly Batista****  
The limits? Yeah, I can see

**Matt Yonkovit**  
of like I said, I had to go through the 18 levels of authentication to get there and then start it up. So yep, that's fine. It now you should see.

**Charly Batista**  
We're not connected yet or something. Now I see. Yeah. And they see that some of the queries that were persecuting have some furloughed workers saw the need to be able to parallel lines, the execution, our backups to the union. So next time, we use the option variables to have more information about the backup. But yeah, so this is the first time, so the first thing that we need to do is to have a full backup, right? So this full backup, we create a backup that is consistent in time. So we will, the database will be consistent that on time that the backup is started. Right. So we started the backup, I don't know, let's say at my time now is 354. So it will be consistent at 354. Things will keep working on your applications to keep writing. So many transactions are coming in. Those transactions are creating all files, right? So if everything is fine, we will be archiving all those files, even though I saw that nasty message that told me there was a problem when archiving one file. snugger. But let's suppose everything's working fine. So when we finish the backup and application, your application keeps working. So we can restore another database with these backups that we have, and with all the wildfires that have been archived, and we will get the data that is consistent on time, like at 354 when it started and then all the transactions that have been applied after that time. So this is sort of incremental backup, right? So if we just think about that, if you have the full backup that we get in the beginning Then, if we have the archives, we already have, by default, an incremental backup, you can restore just the full, and then you can move on time on the grid on the archives. And you can stop at any point. Like if you want to make a point-in-time recovery, just kind of stop at that point. And so this is a read a lot, a lot more than we had before. Right?

****Charly Batista****  
Yes, oh, and

**Charly Batista**  
also, the PG backrest can walk, can do real incremental backups, can get the difference from what has changed it on time, and then it can also do a differential backup. So depending on your policy of backups, you can just take a full backup on Sunday, let's say, and then take a differential backup every day. So a differential backup starts quite small, so on Monday, it will be just the very same thing as the incremental one. But then, when things move, it will always check in from the full backup, it's always checked from when it's the full backup was done, and then do the diff from the full backup to what we have now. That's why it's a differential. Right? So they have advantages and disadvantages. So the main advantage of the incremental backup is that if you have the full backup and have the differential backup of whatever they want, you can just recover. You don't need to go for the whole only incremental backup, the incremental backup; let's suppose you have a backup full backup on Sunday, and your database crashes on Friday; you need to recover the full backup from Sunday. And then the incremental on Monday, Tuesday, Wednesday, blah, blah, blah, after Friday, right? And if one of those incremental backups is broken, then you were screwed because now your chain is broken. Everything after that day, let's say your full backups are fine. Your incremental backup on Monday is okay. But your incremental backup on Wednesday is broken and has a problem. And something happened. And it's broken. So from Wednesday to Friday, everything is gone, and you cannot recover. Because your chain of backups is broken. So this is one problem of incremental backups; we need to make sure all of them are consistent, and all of them work, right? So then we need to have something a policy or a tool that, from time to time, recovers the backups and tests all of them if to make sure that they are working, okay, they're working fine. Because the thing that you don't want to go through is to need to recover something from the backup and then find out your backup is broken. Right? This is not what anybody wants to go through. So that's about it. And for the other side, the incremental backup, the differential backups, you don't have that dependency. So you don't have a chain of backups you have one full backup, and then the difference airflow for the period every time that takes a backup. So if something happened on Friday, in this example, the only thing that you need to do is recover the backup, the full backup on Sunday, and then the differential backup from Friday. And then you got everything that you have. So that's amazing, right? So but the thing is, as the day passes, those differential backups, they get, they get starting to be larger and larger because you're just accumulating change on the period. And with differential backups, you lose, not lose. Because if you have the double files, it's fine. But with the differential backups, the ability to make a point-in-time recovery is tricky. If you are not careful to keep all the wildfires, that is the word doubling the things, so you just lose the ability to make a point in time recovery because the point in time recovery is for the full backup. Right, so you need to. There are also some strategies that you can look up you can do from the friendship of like those are very complex, and it's pointless because you need to give the devil files wherever they anyways. So that's one of the main disadvantages of the differential backups, so as you say, we have advantages and disadvantages for both strategies. And which one use will highly depend on what you need, right, what the company needs. And for the backup strategy.

****Charly Batista****  
Well, it's taking quite

**Charly Batista**  
a while probably to take, yeah, the,

**Matt Yonkovit**  
the, how far along we are. So I mean, a lot of times, people will be in production, they'll have a backup running and get stalled. How do I check to see what it's doing or where it is?

**Charly Batista**  
Well, the way we started here, I didn't; it was very silly because we didn't configure it in logs. And also, I forgot to put the info here, the to info, remember. So we have little visit visibility here. Because of the way we started, so we don't have much log information because I didn't put the plug information here. And that was silly. Or from my side. That said, we can have a poor man's check-in, right? So I can just go here to data.

We are quite far from

**Matt Yonkovit**  
Yes. That's slow.

**Charly Batista**  
Yeah. And it's not supposed to be that far because now we are using the new disk with the higher IOP is that what you have, right?

**Matt Yonkovit**  
yourself. But yes,

**Charly Batista**  
yeah, Indeed. Indeed. They are correct. So what is my suggestion here? My suggestion is okay, or read one hour over, right? So we can do what we did last time. So we can finish this offline, recording, right, and post the video because the main idea for today was to show people that PG backrest is not complicated. Like I've seen a lot of people when we talk about, oh, you need to go with a triennial PG backrest. And they say, Oh, that's a lot of complication. On my setup, I don't want to deal with those things. And as we can see here, of course, we didn't go to the server's configuration. And that it's still quite simple. It's not much harder than doing this, this configuration. We only have like two configurations file, one for PG backrest and one for Postgres, right? And then, we have a lot of benefits using those tools. And this is the message that I wanted to show today that it's not complicated. It's not complex, right? It's easy to set up those things. And we can get it running as it took like 15 minutes because we had a problem from we mess it up before, right? So we spent more time with our cleanup here than going through the PG backrest things. Right. So yeah, my suggestion is it did to take longer we'll see it

**Matt Yonkovit**  
is it only added another 500 Meg's since

**Charly Batista**  
Yeah, it's just pointless this thing here entertaining people with no, no, no. Razzles

**Matt Yonkovit**  
everybody wants to be entertained by Charly and Matt. Pretty sure that's whatever I'm here for.

**Charly Batista**  
I got to make a version of myself, then. So I have a challenge for you math challenge for me. Yeah, it's not related to the backdrop. It's just I have this query here. By the way, have you read the tale of two tables? I suppose you know they write it if it's a family one. It's from a British writer from the 18th century or something like that. The tale Actually, yes. Yeah. The same thing, right? So

**Matt Yonkovit**  
cities tables.

**Charly Batista**  
Yeah, so I have a tale of two tables. By the way.

**Matt Yonkovit**  
We have a question before you get there, is it recommended practice to use PG backrest in a Patrone cluster configuration?

**Charly Batista**  
It is I do have an I might be able to show you something here just a second.

****Charly Batista****  
Hold the line.

**Matt Yonkovit**  
Charly's going to stump Matt today with his tale of two tables question. It's not hard to stump me sometimes. So

**Charly Batista**  
it's, it's what happened with my keyboard. It's like it's massive now.

**Matt Yonkovit**  
Like the keyboard Charly blame the qipco So

**Charly Batista**  
what is I have hopes I have this resistance now not nice as I have this cluster here. So I can do

****Charly Batista****  
Patrone CTL C,

**Charly Batista**  
not C attorney

****Charly Batista****  
coffee waste.

**Charly Batista**  
So I have this classroom; we can see that this replica has a problem, just saw that. So I have this class where I have a leader and two replicas. This leader is being disclosed are being maintained at Viper 20, As you can see, right? So, if we go here and check my Patrone ad

so, my archive comment on mathrani Here is being made by the PG backrest; we can use the combination of Patrone and PG backrest. And actually, it's kind of advice to you to make use of them. Right, they can help each other. And this one in this case, here I have no, I hate, but this is a bad thing unfortunate. Resita uses nano I hate Nano. So, as I was saying it's really advisable to use both of them. And then if you like, Okay, what is the best apology that I can use? So that's one thing that can vary. If you don't have money, let's say okay, I have a really tight budget, I have a tight budget, but I'm able to have three nodes, just like the ones I have here, I have three nodes, right? So I have the configuration of etcd. My etcd is installed on all the nodes; every node has one etcd. And one of those nodes. This is a replica that is lagging here. It has a PG backrest server; it's acting as my backup server. So the backups and everything I have storage attached here. So it has coordination. It's extremely the world files from the leader. And the backup it's doing for the order node. Right. So and this is a very simplistic topology. But if we lose this leader here, this replica can be elected as a new primary. So it's fine. In this case, the replication lag, it's minimal, and it will be elected almost instantly. I need to fix this replication lag because, well if let's say this guy goes down. This one is electric. I obviously will try to understand what the problem is if we put this guy back to come back as a replica. But if the new primary goes down, let's say I would like to have this new world I rotation here. These nodes will, in my contribution, never be elected because of the replication lag is too high. So I asked it, but 20 I don't want to elect an old that replication lag is more than five megabytes because, well, I don't want right. So but yeah, answering the question. It's very advisable to use the combination of mathrani for the high availability and things and the PG backrest to also help with not now is not available only availability, right because it's on the backup and strategy things. I hope that answers the question.

**Matt Yonkovit**  
Fair enough. Thank you, Seattle one.

**Charly Batista**  
So my question to you what I have here is I need to just a second I need to get my I need to connect to another box here that they just don't remember that

****Charly Batista****  
Come on, keyboard help me

**Charly Batista**  
It's fine. I can use my box here. It's okay. So I have to connect to my database here.

****Charly Batista****  
Oh, no, I think I

****Charly Batista****  
want to connect to my database here. Okay.

**Charly Batista**  
So I have two tables here. This is a pretty simple thing. What is Mike doing?

****Charly Batista****  
Don't I have

**Charly Batista**  
I don't have the diagram; I thought of the hand diagram here. That's awkward. I have two tables here that are both tables here. See, I have the table method format the data in Hey, I have this table method object. So here on these meta objects, I have, obviously, a reference for the metadata. But the method data has a self-reference; it has a parent. Right? So my question, and I want to build this, see this nice report here. So, where I have the ID of the method, I have the whole hierarchy. So, in this example, here, Q. H is the Child Child, four is the Father, and two is the grandfather. And just this is just how it, it shows the names of them. Right? Just like you're going to go to the supermarket, you have the category, the suit category, the soup, and then you have the product, right, just this kind of of

****Charly Batista****  
hierarchy.

**Charly Batista**  
And I have the count how many metal objects, each of those, they have insight. Right? And my question is, can I get this report using only one?

****Charly Batista****  
Trip to the database? With only one, What did the database

**Charly Batista**  
select one trip to the database; I don't want my application to do a select to get the method notice a lag to get the objects in another select to make the hierarchy. So I only want select.

**Matt Yonkovit**  
So yes, it will probably be an ugly SQL statement.

**Charly Batista**  
Oh, why do you think it's going to be an ugly SQL statement? going to be an amazing one?

**Matt Yonkovit**  
Okay, I believe it will be an ugly SQL statement.

****Charly Batista****  
But look, it's not that ugly.

**Matt Yonkovit**  
Yeah, I mean, anytime you do a union and several others? Oh, look, you've got some examples there. Right. So that's interesting. Yeah. Because

**Charly Batista**  
this is the analysis of the problem I got, let, let me; let me step back a little bit. They're going to give you some context. So I'm sending those challenges on encouraging, right with things that usually people they don't see every day, or actually, they do, but they do not perceive the prob those problems every day. So those are everyday problems just looking for another perspective, usually those kinds of problems, they've been solved on the application side, right? For the application guys, they go to the database file, open five append connections, or select the database and just display it nicely on the application. So and that thing causes a lot to the database; the application usually looks like, every trip, it takes a few milliseconds or seconds. And it's very costly to the database. And they are asking people, okay, can we make it better? Like, for example, this example that I gave to you. So can I go to the database and run these here? IE, I have here, if I'm not mistaken, a million rows, or 100 million rows. And my question was, can I do each? Can my select run in less than two seconds? Some people sent an ad nice reply. And yeah, it can be that I challenge them. Can we improve and run it in one in less than one second, or something people did? And I challenge that? Can we run it in less than 500 milliseconds? I got one running with 160 milliseconds. Remember, we started with just seconds. And now, with 106 milliseconds, it's more than an order of magnitude. And the challenge is you cannot create an index. The only index that we have on those tables is the primary key. And the configuration of the database, you should use an instance on Amazon that is the free instance and just install the Postgres, no configuration changes, just with the post-default selection of the Postgres database, right? So this is to show people that we've optimized we can, we can get an amazing result.

**Matt Yonkovit**  
So how many people out there have tried Charly's challenge?

**Charly Batista**  
I challenge you guys to go start with this one.

**Matt Yonkovit**  
So is it on your GitHub? I was trying to?

**Charly Batista**  
Yeah, yeah, it's on my GitHub. Okay, I'll channel slash 2.0.

**Matt Yonkovit**  
You've got challenge one. Okay. So there we go. So, I am going to try challenging one, although I wonder if there's a more effective data structure that could clean that up, like the data structure or the schema that you design might not be optimal for the output? is the first thing that I thought of?

**Charly Batista**  
Well, that's, that's, we, that's, that would be much more advanced than approach, right? You might be right because the idea is to start going with the daily, daily life things. So if we go for, for example, our ERP or whatever supermarket system that they give some automation, right, you're going to find those kinds of Office cameras, that's pretty common, really, really come on, like when you have a self-reference, right? So it's just a self-reference from a table to have a child? And then, okay, how do I get all the hierarchy of that reference from that table? And usually, it's done by the application, go there and get the parent. And then, with the ID of the parent, they select the child; if there yes, the child. So when they go to the database many, many times, if you have like a hierarchy, we've

****Charly Batista****  
then

**Charly Batista**  
how to call, then generations, you're going to go to the database ten times,

**Matt Yonkovit**  
but it's a very old-school design methodology. Right? I mean, like, if you think about somebody designing something, let's say, in JSON, it's designed, where you can have those hierarchical things already called out. And so if you stored whatever data you're trying to do whatever metadata in that, I think you could, you could split where the hierarchies in there, yeah, but

**Charly Batista**  
then that's, that's, that's right. But what at what cost if you want, in that case, if you want to get everything you want to get your whole JSON, that is one terabyte and again, just push to the application, and then the application needs to loop in and process somebody.

**Matt Yonkovit**  
It depends on what data you're trying to get out of it. So I'll take this as a challenge, Charly, okay,

**Charly Batista**  
I want to count like

**Matt Yonkovit**  
Zack, the same thing you are with a better schema. And we'll compare. Okay, I'll mark it down for you. We're going to take a break because our next stream is supposed to be during Percona life. So we're going to have to take a break because of that. So we won't be here in two weeks because of Percona live, although Charly might stop by and we might do. How do you go from the show floor? But yeah, we're we've still got probably another hour to go before that backup done.

**Charly Batista**  
Yeah, yeah. Well, yeah, we better do what they suggested sole goal. And then we finish and wrap up. And

**Matt Yonkovit**  
so what do you think? Can I design a more optimal hierarchical schema as a challenger? Charly's challenging me. What about you folks out there? Can you write Charly SQL in one statement? And can you get it below? What was the current record holder? Half a half a second?

**Charly Batista**  
100 650 milliseconds?

**Matt Yonkovit**  
150 milliseconds. So can you do it? We want to hear from you. And if you can beat Charly's record there, we'll send you a t-shirt that says I beat Charly's record.

****Charly Batista****  
Just for you guys.

**Matt Yonkovit**  
All right, Charly, Charly. So we'll do what we're going to do is for PG backrest here because we need to come back here and wait for the backup to do it. We'll come back, we will record a follow-up session and post on YouTube with not only the final product, but we will go ahead and do a restore in an incremental backup as well. And so we might have to clip those a little bit just because

**Charly Batista**  
of the festival, Ward is clipping.

**Matt Yonkovit**  
But we'll make sure that we put those back out there for you all to see that, that we did do it. And thank you for putting up with us once again on a Friday afternoon. We appreciate you hanging out. And hopefully, this was somewhat educational. I know I haven't used PG backrest before. So it was interesting to see it in person here so

**Charly Batista**  
well, and it worked well. What didn't work

**Matt Yonkovit**  
well, to be determined because we can't see you forgot to do the turbo button. Right. So you didn't do dash fast, which

**Charly Batista**  
I need to figure out why this box is suitable to qualify. And I don't

**Matt Yonkovit**  
understand why more people don't use dash-dash fast in their configuration files. It just seems everything. All right, everybody. Thanks for hanging out, and we will see you in another few weeks. So it should be three weeks for the next one. But you might see us at Percona live doing some fun things from there as well. appreciate you all hanging out.

**Charly Batista**  
Yeah, thanks, everybody.


