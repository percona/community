---
title: "Setting Up and Using Patroni to Automate Failover in PostgreSQL - Percona Community PostgreSQL Live Stream"
description: "Learn more about setting up and using Patroni to automate failover in PostgreSQL with this Percona Community Live Stream of June, 16th"
draft: false
images:
  - events/streams-pg/PG-Stream-Week-6-bg.jpg
date: "2022-06-14"
speakers:
  - charly_batista
  - matt_yonkovit
tags: ['Postgres', 'Stream']
---

![Percona Community PostgreSQL Live Stream & Chat - June 16th](events/streams-pg/PG-Stream-Week-6-bg.jpg)

This is a part of bi-weekly Percona Community Live Stream. Our experts, Charly and Matt has talked about setting up and using Patroni to automate failover in Postgres.


## Video

{{% youtube youtube_id="dkp-3S3l8tY" %}}{{% /youtube %}}


## Transcript

**Charly Batista**  
And my frozen looks like you

**Matt Yonkovit**  
You are frozen though I don't know why Charly's frozen he just we just went live and Charly is frozen so I don't know what that means for us hopefully nothing is Too bad, right? Hopefully, Charly's Charly's video will decide to come back. Although now we're just getting the blank screen of Charly. But welcome everyone to our meet-up while Charly tries to figure out his technical difficulties. Believe it or not, he actually was here just a second ago. And we were chatting about this. He decided to log off. And now we're gonna get the double screen of doom here, which is always fun. So Oh, wow, look at Charly. Charly, can you hear me at least

**Charly Batista**  
Yeah, I can hear you. But it's blank.

**Matt Yonkovit**  
No camera for Charly. Well, that's okay. Charly, why don't you can log off I guess, try to come back, I will actually share. I wanted to talk a little bit anyways, to start with about our streaming event next week. So just because Charly isn't on right now that's okay. Hopefully, he'll be back shortly. So thank you for showing up for our bi-weekly Postgres. meetup, really appreciate it. Next week, we have Percona community live, on June 21, or 23rd. So this is going to be streamed on all the channels you're watching on now, just so you're aware, it should be everywhere that we are live. So Twitch, LinkedIn, Twitter, and YouTube, are all of those awesome channels. And so we will be streaming live every day, over those three days, a variety of different content. So if you're interested, you can go to the Percona community website. And on the Percona community website, we've got the agenda here. Each day, we'll start at that's, that's odd, but one, but each day should start at 7 am, Eastern or 13:00 CST. So if you're in Europe, should probably add UTC to this as well. But you can take a look at the calendar of events here. So what we've done is we've got a plethora of speakers, 35 different talks, all of them are going to be streamed live the releases, then the authors of these will be appearing on chat. So if you have questions, you can ask questions during this on our YouTube channel. Otherwise, this will be streamed everywhere, all at the same time. Now, Charly is still having some technical difficulties right now. So before we get into the replication setup, we are here just kind of fill in some time here. Charly, are you back?

**Charly Batista**
I had your kill zone here. Okay.

**Matt Yonkovit**  
So this session, so this session will be recorded, but also the Percona. Live, and community live will all be recorded as well. So there will be streams of one contiguous day for each and then we'll break those up into individual talks as well. So just an FYI. So let's go back to Mr. Charly here, now that I have done that. So hello, Mr. Charly.

**Charly Batista**  
How are you doing?

**Matt Yonkovit**  
Yes, I am doing well. I am doing well. So thank you for bearing with us for the few minutes it took us to get Charly back online and work. And he did freeze there for a few minutes and had to go through some technical difficulties. But yeah, so Charly thanks for hanging out. Now Charly's going to be speaking at Percona community live as well. I asked him for a session because we're asking people to pre-record the sessions for us so we can play them, and then have them live. But he hasn't yet. So everyone asked Charly, please, Charly, please, please record your session because he's gonna be talking about point-in-time recovery. You know that's, that's something that is definitely, we all want to learn about and look at as we're already getting our first Patrone question. So that's great. So people are ready and raring to go. And Pathak we'll, we'll get to that question.
As we start to initialize the cluster. That's probably good to make sure we keep that in the back of our minds on that. Right. So the question was, we often noticed that when we re-initialize the cluster and Patrone the target replica site goes in a loop after copying some amounts of data to the leader. The RE initialization starts from the beginning. So as we start to initialize the cluster, we could probably hit that question. That's probably the best time for that. And hello, hello, hello. to everyone out there in st land, so appreciate you hanging out. So Charly, Charly, Charly last week or two weeks ago, actually set up replication. And we did run into some problems. If you didn't see the exciting conclusion to that stream, it is on YouTube. So he did do, some troubleshooting to make it work. And it is working. So we're happy about that. So go out and check last week's live stream where we set up replication. And in the follow-up, where we actually fixed the broken replication that we set up.

**Charly Batista**  
I fixed Yeah.

**Matt Yonkovit**  
Yes, I did not do anything other than agonizing over the video and then bother Charly. Yes.

**Charly Batista**  
No, Jigsaw sitemaps. did a great contribution. So

**Matt Yonkovit**  
yeah, I did a great contribution. I added the nodes for him to play with. So yes, awesome. So today, today is supposed to be all things. Patrone. So Charly is going to take the cluster, that is the replica that we set up, and going to create a Patrone cluster out of itself. Charly, are you ready?

**Charly Batista**  
Well, always, Alright,

**Matt Yonkovit**  
stream. Are you ready? I think you are. I'm just going to assume they're going to say yes. So, Charly, let's get to it.

**Charly Batista**  
Okay, let's do it. Let's share my screen here. Ah, where's my screen here? I suppose you can see my nice terminal. Can you?

**Matt Yonkovit**  
We can, we can see. Yes. Great. Okay, cool. So nice square. It doesn't quite fit the window that I have. But that's okay.

**Charly Batista**  
Really, I can resize it. No, no, no, no.

**Matt Yonkovit**  
More of this. Oh, well, that actually made it better. It gave us a little bit more idle state. So there you go.

**Charly Batista**  
I told you I can resize it. So Charly has the power. Who has the doer?

**Matt Yonkovit**  
Charly has the power. Other light here because it's a little I need to be

**Charly Batista**  
okay. So what are we gonna do today? So just recapping what you did before. We have three machines, right? Running one is primary. But here I have this one as a primary. Let me connect my Postgres so it's wrong peachy. the occasion I'm using replication is locks. So I can check. So I have to auto wrap because replicating here, using replication is large. And this probably has to do with the question that we got in the beginning, Matt. Okay. So and we'll see what why I'm using replication last year, and what is one of the issues that it may help to prevent, right, so we have this, this is the primary. These are these another one here is another Africa. And you have a third one that you didn't name.

**Matt Yonkovit**  
I didn't yet but I'll make if you want me to, I'll go ahead and name it. It's too,

**Charly Batista**  
so good. So it's, it's IP six, six. All right, so we have the IP six, six, we have Charly replica and we have this one how to call this Charly dB. Awesome. So we do have those three, three nodes and they are replicating. So for example, I hope they're replicating. If I go for the database here if I create the table for each you with an integer primary key, always use primary keys. So I'm going to create a stable if we insert into teach you select X-ray seriously. I've only searched just one mineral, right. So we don't want to stress all databases for now. So if I count, I hope we're gonna have gone to two 1 million rows here. I'm gonna just copy this over. I'm gonna go for my this database here. Well, of course, I need to connect to the database test. This test and we do have over here this is The replica. So we have 1 million rows here. And you as well. Let's do a PL SQL. Of course, the database is tested. And it's the last. So our application is working, right? So we have our application it's working. And what we want to do now is to ultimate the failover process using Photron. Right. So to do so, we need, of course, we need to install the whole set of training. But Trani, how it works Patrone it uses at least the version we're going to use here Patrone, it's used a DCS, DCS is a decentralized database, to keep the configuration and to help the attorney to decide who's going to be the primary who's going to be the new primary if something happens. So what it does is use a protocol that calls wrapped raft protocols is the one that use it to decide who's going to be the new next primary in case of a failure, it doesn't allow action inside of the molds. So that's why we have an odd number of molds, here, we have three nodes, right? And we want that one of those needs to be elected to be the new primary, right? So then ideally, we should have an odd number of nodes. And also, one thing that you need to understand is how many nodes we can crash before we lose all the clusters. So if we have three nodes and one of the nodes crashes, we still have a way to do an election because the raft, the premise one of the premises is it has to have math plus one of the numbers of the roads, right? So three nodes in the cluster half are 1.5. So Q is larger than half of the node of the closers. So that's why if you lose one of the nodes here, we still can still have the closers do have consistency. However, if we lose two nodes of our cluster, the remaining nodes won't be elected as a primary because, we cannot take election anymore. We don't have the majority of the nodes to voting nodes to make an election. So this needs to be clear on the strategy. Okay,

**Matt Yonkovit**  
so Okay, so just to clarify, Charly, and this was a question that bitOK answered one of his several which we'll get to all of them, but just an FYI. We'll try to get to them in due course, but he asked specifically about if Patrone is set up with three nodes, one leader, and two replicas, can we discard or remove one of the replicas as it works based on the quorum, where it should be now? An odd number? How does it impact the quorum, and if I understand, what you just described, is, when you have three notes, if the primary fails on the three nodes, then one of the remaining two will be elected. Exactly. But if then that primary fails, the replica will not be elected, because it can't do that, because it doesn't know if it has a split brain is awkward. Okay.

**Charly Batista**  
So that's, that's the point. So remember, it needs to have a majority, if you have a cluster of two nodes, and one of them crashes. So you only have half of the remaining nodes, you cannot get majority for votes, right? So and then you just lose your cluster, that remaining node, what they lacked as a primary, you need to manually go there, and, and promote the node that node as a primary. But this needs to be to be taken into mind. The same happens, for example, if I have five nodes, so if I have five nodes, you can lose through two of them, you still have the majority of the nodes in the class, right? You still have three, is, it's the majority of all voting if you have originally five ones, right? However, if you lose another one, two out of five cannot make a majority of voting. Right? So this is this needs to be in mind when you plan your cluster. Because those problems can cause your node or your cluster to go down. And then you need to do you do a manual intervention and promote everything manner. So you can still go and do everything manually there. But you don't want to do right that's why you need to do some planning ahead. In our example, here in our case, we have three We can lose one of them. So if we lose one of them, we're good. No problem happens. So we still have the class, if you lose two of them, we were not in good shape, because you need to manually intervene and promote that node as a primary. Okay, that said, we need to start installing things, right? So the first thing that we're going to do here is ft get an update. That's why use makes sure our environment is up to date. We're going to do in all three.

**Charly Batista**  
So right?

**Charly Batista**  
I need to install etcd. So apt to get install etcd you may suddenly typo. Oh, thanks, thanks. Some distros. They don't have etcd as a package. So luckily, this version of Ubuntu it has, so I got installed here. So some distros we need to manually download and compile so they're more painful than others.

**Charly Batista**  
Oops,

**Charly Batista**  
I'm just gonna eat, right?

**Matt Yonkovit**  
Everybody's life into everybody's life, a little typo comes right. So it's, it's okay,

**Charly Batista**  
it's okay. So can we survive? We do. We have to recall, your package is broken. We, we get pulled out, we had to do anything for that package, and that's broken. So first thing that we're going to do is we need to do the configuration for etcd. And one thing that needs to be to be kept in mind is the configuration for each CD changer on 2.5 2.4. Something, the one that we're going to use here, is is valid for the version that we're using. Actually, 3.4 If I'm not mistaken. So up to version 3.3 something 2.4, we can still use those parameters, but it's changed on the not on the lease, it was on 3.4. I don't recall top of my mind. But etcd started using YAML file. For this version that we have on Ubuntu, we're not going to use MO file, I saw what I do is if I remember correctly, it goes for etc, the full. And here I have an etcd file. Right. So we have an examples. As we see here from the it's not an YAML file. For the examples, we have the parameter names your own capital using equals and thing for the new versions of etcd. It's lowercase, it's not using underscores using batch to separate the name, it doesn't start with etcd. And it's an YAML file. So keep that in mind. If you install the new version of etcd, you're going to have those problems, you need to convert what we do here for the configuration for the new version of etcd. Keep that in mind. So I got a backup this file. Always good to to backup the configuration of the original configuration file, we need to recover it back. So and I have here some notes that I going to use for now. So the first parameter we're going to give here is the node name that we have here. So I want to call them nodes PG one PG q and p three. So just for simplicity, right, so PG one is the primary PG two PG three arabicas. We tell the TCG what's going to be our initial cluster. And in our case, our initial cluster is this load, right so I'm going to use the IPO please note that I obviously don't know the A but we can get here. So this file we're going to use this file to bootstrap etcd. After we bootstrap etcd it's fine. It's not needed anymore. And here etcd uses two ports, one for internal communication between the nodes, which by default is Port 23, eight zeer and another one to come in. occasionally for the clients, in our case, but Trani will be the client. So by trying to reconnect with ECG to store and to get the configurations from pulses, so everything that attorney does, so we'll see the per 20 stores, the post was configuration need to be kept inside of etcd. So the state of this cluster here, our original state going to be new, it's going to be a new cluster. Because we're just bootstrapping here. Right, we got to tell the closer that we have a token per communication, so we're just going to use this, just for communication, we can use this just match is stream

**Charly Batista**  
etcd token.

**Matt Yonkovit**  
And it's just you make up a name consistent?

**Charly Batista**  
Exactly, you just make up a name that is consistent. So we will tell that we want to revise these the these nodes in the cluster. And we use the URL that we just created here. So the other nodes can can can connect. And we need a data directory data folder for etcd. This one is for etct. Right? By the fall. It uses var lib etct This is the one. Okay? i Yeah. So this is a folder that it's used by default. That's alright. So we're going to keep the things there. But I want to for this installation, as we're going to use these etc, the only four horses I got a call. I gotta put another one. Because if you if you check here, there is already a full folder inside here. Right? So inside of this folder, here's the data, the four CDs, which has its members, instead of members, it has the wall files that is the concept is similar the wall files for Postgres, right, so it has that files we're not going to hear because it's it's, it's, it's out of the scope for

**Matt Yonkovit**  
Now, Charly, do you have to create that directory for PGSQL? Or will it automatically be created?

**Charly Batista**  
Now? It dcdb automatically graded? Okay. Okay. Ah, I gonna tell etcd what's the well that the Orientals can use? So, again,

**Charly Batista**  
it's just there's one here.

**Charly Batista**  
And we also tell etcd, what is where etcd gonna listen for the clients. So in my in our case, here, we want to lease them this URL. But remember, the port is a different port. We also want to lease the unlock of holes, right? Because we'll see, we have some comments that we run to the configuration to check things on etcd. And we want you to be able to connect that on localhost, we don't want to every time need to send that rise of the IP node. So here we can, if we have more than one interface, we can listen different interfaces, it just comma separated list. That's all good. The last one, the same way, we advertised the URL for the other nodes. We also do for the clients. Right? So the API, you can buy that URL and the clients can have our two discovered things and find that we have an etcd not here. Okay. That's all you need for now. I want to make sure our etcd the the system D is using the correct etcd file so I want to find your our etcd. Bastion etcd I want to send all the

**Charly Batista**  
Okay, actually what's

**Charly Batista**  
interesting, Am I doing something you still prefer to do? I want you to see what is the system the configuration file for HCG The other night.

**Charly Batista**  
I just want to find it

**Charly Batista**  
oh, gosh, name. Yeah, I was doing something stupid.

**Matt Yonkovit**  
Fair enough. Yeah, read you're redirecting the some of the output hide the errors, right?

**Charly Batista**  
Yes. Yeah, it does. So here we started to see or indeed. And here's also the TCD. Oh, I could just copy here. This is what it wants you.

**Matt Yonkovit**  
You had it before, right? So?

**Charly Batista**  
Yeah. So

**Charly Batista**  
okay, what I want to say if what is the configuration file, etc these users, okay, it's it's running as etcd. That's okay. So when we install the system, it's already created. So this is the comment when we do and start and demo arcs. So for the gem on arcs, we don't have anything on environment. But it will use the configuration file. The environment here is the one we just created etcd before. So this will pass the configuration file for etcd. Right. So it's it free and start everything. I just wanted to double check that we were changing the right file, that was the only thing that I wanted to do. So if everything is fine, we can do systemctl. First of all, we're going to enable etcd. Always work. So if it fails, you really have something really nasty and bad on your environment. The problem is, you start etcd not always work.

**Charly Batista**  
Well. That's surprisingly.

**Charly Batista**  
It did two good things. Ah, can you double check that you have the ports? 2380 in 3379? Open? Because I'll need those ports open. Now,

**Matt Yonkovit**  
the course No, I will I do not have those. So. Okay, so one second, let me change the configuration. So all of them. Okay. Well, the 2379 and which 123 80?

**Charly Batista**  
Yes.

**Matt Yonkovit**  
Okay, let me let me go. So, although I'm over here, people's I'm not looking at the screen. That's why I am playing dungeon master for Charly.

**Charly Batista**  
Okay, I got to copy these guys here.

**Charly Batista**  
Most of them

**Charly Batista**  
what I'm doing copying is configuration from from the primary, I'm going to etcd on this is the first replica, right? So let us say am I gonna move etcd file to the backup file to CD dot backup. And it's not MGS and we are going to add it to the TCD file. And this one, I'm going to change the name CGT. So I'm not that's the only change I'm going for now. Actually, yeah, that's the only candidate right now because I just want to create the file with exactly the same configuration we did. So but the thing is, is we need to change some stuff here. And we're going to ask etcd to help us when we need to add a new member on etcd we can use the command line etcd CTL that's the common line for etcd to tell etcd when you want to add a new new member well, but before that, let's just make sure we have everything yeah, that we know we created. It's run Yeah, we do have C we created this node

name is Charly GB. So this is the poem. So it's we connected as a local localhost. That's why it's saying but it's also listen on the other port we can share using netstat. If we check here we will see etcd is listing

on those two ports right so I was expecting to into the lesson

on zero zeros. Well,

**Charly Batista**  
that's fine. So anyway,

**Matt Yonkovit**  
so Charly BB should be good in terms of the the firewall rules. And I think it should be the rest. I'm just double checking. So you should be you should be fairly good to go. If I wasn't an idiot, which sometimes I am, I will admit.

**Charly Batista**  
Yeah, it looks like we check checks.

**Matt Yonkovit**  
Yes, it looks like I'm reusing all of the are the same security group for all of your boxes. So changing the security should cascade down to all of them.

**Charly Batista**  
Okay, so what are you going to do here? Here's on the primary on the timing, I going to add the node called PDQ. Right. Okay. Oh, one thing that I've noticed here, see, it's, it's not listed on the post that we asked and the name of the nodes. See, it's trolly dB. This tells me that etcd didn't really read my configuration file.

**Matt Yonkovit**  
So why did your configuration file so Wait a minute. So what you're saying is, it should have

**Charly Batista**  
the node name. Remember, it's PG one, we set the node name as what you want, right. So for example, if a cat here, see, this is the name, it's PG one. But it got the host name. And we asked her to the cluster tree stash in both localhost five to listen on both localhost for the clients and also to list on the IP port. It's only listen on the localhost with 2379. And for the port two 380. It's also only some network hosts and we ask it to list on the port 238. So it just ignored our configuration file. Either didn't read our configuration file, but it just ignore. So what we're going to do is systemctl stop etcd.

**Charly Batista**  
Right. So

**Charly Batista**  
the there's a typo. Okay, it's gone. I gonna change here etcd. User, so I can log in, because it doesn't let me log in. They're gonna change. bash the shell

you guys say well, to run the command, it is CG. Want to tell etcd? Okay, etcd the pirate flags. I want to the configuration file, right? So we just need the TCG and config file. DCG

**Matt Yonkovit**  
says it's just a check the configuration file.

**Charly Batista**  
Yeah, I want you to see what what happens if something wrong here. Okay,

**Charly Batista**  
I need to update config file.

**Matt Yonkovit**  
You didn't have a dash dash

**Charly Batista**  
Oh, nice. This version is already using the JSON. I mean, the YAML file that what I told you before, it has changed from a lot of compression, compression, etc, the whole

So, what we need to do here

**Matt Yonkovit**  
change all the case, right? So,

**Charly Batista**  
yeah, only change all the things.

**Matt Yonkovit**  
So at some point, the easy to change to the animal. It must be before three two, then.

**Charly Batista**  
Yeah, I don't really recall on top of my mind, which version was.

**Matt Yonkovit**  
Let's see. I'll Google it. While you're doing that. I'm going to be helpful. Yeah, thank you.

**Charly Batista**  
are almost there here we go.

**Matt Yonkovit**  
Did it start?

**Charly Batista**  
No, we still have problems in our configuration file okay. Oh

**Matt Yonkovit**  
you didn't have the colon there.

**Charly Batista**  
Yeah, it's because I don't want to change your call because I have equal scenarios and I'm curious to write

seriously oh just in case well, we can have these right just to make sure it changes everything they it's a one YAML file now, right? So oops. Guy. Yeah, now it's about Yama file. Okay.

**Matt Yonkovit**  
Yeah, you just gotta get it just right. I saw the other day that someone was offering a certification in YAML so maybe you should become a certified YAML professional there Charly. Maybe that would have helped solve your problems. Yeah, yeah, I didn't even know that such a thing existed. So evidently for all those out there who are watching there is a certification for YAML I don't know how valuable that would be but

**Charly Batista**  
okay, now if you check the next stats again

**Charly Batista**  
so we will see okay,

**Matt Yonkovit**  
yeah, there you go. Yeah, by the way. Yeah, don't forget to turn off login for EDC. security best practices. So, right okay. I'm just saying I'm just saying they're all those who are following along we don't want them to leave potential loophole open

**Charly Batista**  
another thing etc CTL member least and see here we go. So we have the the right member name we have everything right here. And but the thing is if we do a systemctl start with that

**Charly Batista**  
system secure systemctl is etcd

**Charly Batista**  
on our our configuration Nope. Is something wrong with the system still always up and with your systems now

**Matt Yonkovit**  
mine configuration

**Charly Batista**  
I use I just installed etct And it's not ordering here. So what I got into you

**Charly Batista**  
is never do it at home. So is I forgot the parameters etcd

**Matt Yonkovit**  
our config file?

**Charly Batista**  
Yeah, it's config file. So

**Matt Yonkovit**  
by the way, I think it was three one where that change happened. Like it like in three two is is haha

**Charly Batista**  
Yeah, I really don't recall. At least a I had a problem with this before. And because or else we will take like, half of the streaming troubleshooting in that problem. Oh, what? Yeah. So util complained that I need to do a reload. Yeah, that's what I was looking for. And thank you. And here we do a restart.

**Charly Batista**  
And we if everything went well

**Charly Batista**  
there we go. Now we have from system CTL. It's not the best, the best way to do the best way would be CI to create an order on an alternative configuration file for system D and football for now. So that just work, right. This is not a best practice on how to change system D. So there are a lot of those things on internet. And just make sure this is not the best practice. Don't do it. Find that the proper way. Okay, we have one load here. What we need to do now? Is it ECG, ECG CTO, member edge. So we're going to add the member PG tube, right? This is the name.

**Matt Yonkovit**  
Now add the configuration. Do you have to add that to the vote? Yes. Okay.

**Charly Batista**  
Now we're just starting to add to these to the class for loop. We have another member we want to add here. Can you allow us to ask that member? Because if you try to stop the load now, the closer you say, I don't know who you are, I have no idea. I have nothing to do with you. So we need to add the member here first to the cluster. And we'll see that the class we will these nodes will give us some hints for what we need to change on the configuration file. Right. And the thing is, this also changes the new version. Let's ask for help. So city member edge. Okay, it is vgtu and nordnet. Okay, so that's fine. I thought that that had changed. We need the IP if this is the IP. And we're going to be on the path to 380 zero, right. So Dang, it added a member. But the thing now is if we check our member list here, you'll see that has no leader at this point. Because we have keynotes in the closer but one of the nodes they are down, right?

**Charly Batista**  
Let's fix this problem now.

**Charly Batista**  
Okay, they didn't change I didn't save. Okay. So, theoretically, we just need this to start the cluster. I mean, this knowledge, but I got to add a couple of more of those parameters. And funny thing is set. It didn't give us the instruction in YAML file, right?

**Matt Yonkovit**  
Oh, yeah, no, that's funny. So it outputs it in the old school configuration. So I wonder if it's fixed in later versions of EC etcd? Because I mean, even even the version you're using is a bit older.

**Charly Batista**  
Exactly. And this is what is confusing, because the Add Member comma should give you in the, in the new version of the the configuration things right. So and remember that if we try to start using this, this format will complain because it's not a YAML file. And that's true. Right? So let's copy over here. Because we can just change what we need to change. So of course, we're going to change the name add to the initial cluster here. We're gonna put the value that we have here. So it's not a new cluster anymore. It's an existing one. They advertise Well, of course, is this true? Let me as I need this once

**Charly Batista**  
you're

**Matt Yonkovit**  
you're basically using the exact same configuration with just a couple.

**Charly Batista**  
Yeah, just the Exactly. Actually, the change is just the IP. If we pay attention. I could just yeah, it's just the IP thing that we're doing. Right. So nothing else. And those ones here, we remove. And that's it. Ah, we need to do the change here that we also did for this guy we I wonder what happens to your boxes, they always

**Matt Yonkovit**  
this is a clone of your setup.

**Charly Batista**  
I just installed this back edge, and it's the thing broken around.

**Matt Yonkovit**  
I did not do anything. We, we had a couple of questions, but I don't know if now's a good time. I mean, like so. I mean, we obviously you've got a few backed up that we're here to get to as we get more to the database side. But last one is where can we where we can docs, where can we docs, where can you get the docs for etc.

**Charly Batista**  
It just said Yeah, yeah.

**Matt Yonkovit**  
I mean, like so yeah, you can?

**Charly Batista**  
Yeah, it has its documentation. It definitely the change I found on the documentation. So now we have guilds ATCG, CTL intil. member list if we check. It came with and it didn't use our configuration amazing. Even after it's changed. Enable, it didn't create the symbolic link. So now it created a symbolic link. That's why you should never use this word you. The Jenkins.

**Matt Yonkovit**  
Don't do what I do. Do what I say. Yeah, that's what Charly's saying.

**Charly Batista**  
Yes. Okay. Awesome. Now it's using our configuration file. And now we have a cluster we have two notes. So

**Charly Batista**  
good to suffer with the third

**Matt Yonkovit**  
suffer with a third. So while we are suffering with the third node, maybe I should play music maybe we should dance maybe I should string. No,

**Charly Batista**  
no. Music is fine. Last Yeah, please. No, no, no. Nobody deserves that.

**Matt Yonkovit**  
No one deserves that. Is that what you said?

**Charly Batista**  
I didn't say anything. I just say now please. News news because of this. Fine.

**Matt Yonkovit**  
Yeah, well, nobody then he said I shouldn't do it. Because no one deserves that. That's

**Charly Batista**  
just no no. Well, oh, we are recording right. So I cannot say yeah, you're

**Matt Yonkovit**  
just mean to me. That's that's out there on

**Charly Batista**  
the ship. Pay attention to our accent because we've been recorded. Yeah. Okay, shame on me. I apologize for that. Can you believe the backup this again? You believe it? I didn't understand what it said. But it can go over the record and increase the audit volume later. You'll know that right? No. Okay. So look, yeah, look, I just added a new one. But if we check the name release, now, the now the cluster is still up. Because remember, the risk now is two. Now we have majority of the notes in the class right out of three, we have three Q notes up and only one now. So now it's fine. It's the same as if we just lost this node, even though like it's not started yet. But this is how the cluster sees on how things work at the moment. Okay.

**Charly Batista**  
So,

**Charly Batista**  
let me pop the configuration here because you're gonna do this thing. We're gonna Just wrapped over here.

**Matt Yonkovit**  
Oh, and now you're gonna do global IP replace? I will make so much easier.

**Charly Batista**  
Yep. Yeah, that's true. Let me

**Matt Yonkovit**  
and while we're at it just going through some of the questions that we're going to want to get to shortly. And again, to distract, but that you you've got some grunt work to do. so let's see. So there was what's the downsides of running DCS besides Patrone on the same machine? We kind of talked about the YAML file, right. So although bitOK says that he's having some issues, tweaking the Amel to the TTL on the watchdog and doesn't seem to take effect after making the changes. I think that's, that's it?

**Charly Batista**  
Yeah, it doesn't seem to take effect, make sure that don't have the same problem as we have in here. Right. It's really, really the country the right configuration file, when you use systemctl. Maybe it's not going through the the configuration file, that would be the same problem we just had here.

**Matt Yonkovit**  
Yeah, and then he was having some issues with the initialization, which we talked about, we'll we'll get to when a Server VM goes down for a few hours and comes back online, the target requires the rebuild, because due to the timeline switch, there's also a missing wall file on the leader side, the results enable unable to make the target sink that requires reinet it makes a cluster, make the cluster resync. Just by having replication slots, the wall still remains missing on the leader site, when a replica site is down for a few hours. So it sounds kinda sounds like a configuration thing. So I guess we'll get to that. I think I know when I can ask about that. So how do we make Patrone more stable? All right, well, we'll get to a couple of those. Hopefully. Charly, just out of curiosity, this is our first time on Thursday. Generally, we're on Friday. What is your next meeting? Because I only booked this for for for the hour. I need to book start breaking this for longer?

**Charly Batista**  
Um, well, that's a good question.

**Matt Yonkovit**  
I want to make sure we're respectful of Charly's time, because we haven't even gotten to the postgres side of things here.

**Charly Batista**  
Right. Yeah, we're still doing BTCD things right. For that we're finishing the city doing but 20 Should be a lot faster. Oh, maybe?

**Matt Yonkovit**  
Famous last words. Never say Famous last words. Charly wouldn't haven't anyone never told you that.

**Charly Batista**  
Okay. Oh, this

**Matt Yonkovit**  
should be a piece of cake. Go walk in the park. that's that's definitely do that's going to do mu. Right.

**Charly Batista**  
That's That's true. That's true. Yeah, and let's hope it's okay. Well. As always secured. Whoa. Usually they start common takes time not the start is one. That took a lot. Time to to just check. We started up the node. Okay, if we check the members

**Charly Batista**  
that's too bad. Stolen started. Yeah.

**Matt Yonkovit**  
So why is it unstarted?

**Charly Batista**  
That's a good question. Let's check here. Well, because obviously, it's a steal, not using our configuration file. Why? So? daemon, reload Hey, okay, now it is. See,

**Matt Yonkovit**  
maybe it didn't reload before. Maybe it was just dismissed. I

**Charly Batista**  
know I did. And, well, if we go back to recording will be the Yeah, I did. But anyways, that's okay. See here, Gremlin. Yep, it's here. I have proof See, that actually did it before. All right. We have etcd running. So now what we need to do is we need to install the training. Alright, so same thing after getting all that running, so let me get this for now. I want to just run all them and in all three. So installing port 21 Always give a error message, but it works. So ah, I also mathrani is built using Python, right, so we need to make sure that we had the proctor connect or who paid for Python for both posts with an etcd. So I go and install psycho PG two.

**Matt Yonkovit**  
I already had all these boxes because I think I went through so yeah, yeah, I went through these boxes earlier to install Python and a few other tools.

**Charly Batista**  
Okay, cool. And we're gonna, we also need to install Python etcd this one here. So if we don't have those, sometimes we can have like weird message errors by trying saying that it's not able to connect to Cuban ads, for example. And it's, I believe it's a hard call coded message error. Actually what that means it's not able to connect with ECD, but it calls it the Kubernetes. And the first time that happened to me, it took me a lot of time to understand what was going on. Right. Okay, now, we need to go for pertronic configuration. So, if we are looking, looking off it will have created the Quattrone folder here. And oops. And then we have a sample file. Right, which puts Ronnie dot YAML sample. So another YAML file. And at least this is uses the same format that the two uses as a sample file not like it is at this point for etc. This is the one that the old format. So let's go actually create our our configuration file here. I do have my my, my sample files here as well. Okay, so the first thing we're going to tell is what is the scope

**Charly Batista**  
CCNs.

**Charly Batista**  
We are working here. So that's going to be the scope for all of the three, right, so these are informations that are going to be they're going to help a trainee to identify this whole postfix configuration inside of etcd. It has the scope, it has a namespace. And inside of that scope and that namespace, that namespace for etcd, we can put many different nodes, for example. So and all of those nodes, they are related to the same, the same namespace, the same scope of the Patreon word. And so it means that we can use the same etcd cluster to have to help different posts with clusters, because you can have different namespaces or you can have different scopes inside of that. So with different namespaces we can have different classes of Patroni using the same etcd when it comes to the question that you said optic one of the question, what is the is there any advantage of having etcd? On the same box or outside of the same box as a petroleum? Right? So the answer is it depends. For example, let's say we have all the nodes on the same data center. Like we we know that our data center the natural connectivity, our data center will go down and if it goes down all the notes, they're going to be off right we're going to lose all the nodes if the connectivity of the same data center goes down. So in that case, If we only use etcd, for Postgres or for Patrone. So it's fine to have etcd on the same box, right? Because losing the node itself if you lose both, because if you lose the whole box, for the cluster itself going to be the same effect, right, we won't have any problem. But let's say you're going to scale your cluster. So you don't want to have a single point of failure. And now you want to have multiple data centers, right. So you have three nodes on the data center Bay, and three nodes, or four nodes on the data center v.

So if you lose connectivity between the data centers, and if it's etcd, is our own each nodes, then you're going to have individual clusters on the data centers. And they you can have any split brain situation on each individual clusters, if they have enough number of voting, they're going to build their own cluster, then you have a split brain situation. In this case, there are many there are a few solutions are a very common one is to have another set of only etcd. Outside of those, those data centers, those GCS that you can compose the voting, or for for the classroom, right. So you have always had the majority outside is either one of the closer they really crash that the closer the network goes down. So it can vote, the audit, the audit cluster can vote with those etcd outside to to get the majority. So then you avoid a split brain situation in this case, right. So there are scenarios where it's fine to have etcd inside of the node by perceiving costs, or whatever is the case, it's okay like in our case, here, we all of them are on the same DC. So if we have the promise, we won't have a split brain situation here if the data center goes down, or if the data center loses connectivity. But in other cases, you really need to have ECG outside, at least a few nodes outside, it's good to have ECG on the local host, because it's faster for by trying to get communication. So pertronic can go just ask locally and see if something happens. So if that CD went down is not there is no closer. So for 20 just identify a lot faster than if you need to go to the network. So you let batani just talk to the local host is the city inlet etcd network and its city cluster to talk to all the nodes to figure out networking and segmentation, networking, failure, all those kinds of problems, right? So those are things that you need to take in consideration. And again, depends on your situation depends on your setup and depends on your budget, what are the problems that you will want to address? That you highly depends. Okay, so let's give a nice name here. Match scope. Well, there is an x ray scope. We just go and namespace I gonna use just G SQL. It's fine. The name is for this node. This is the big one. The etcd I wanted to whoops Thank you. I wanted that's much adaptation. I change it later. You connect to the host is the IP of this box that I never remember

**Charly Batista**  
and it just came to the same place

**Charly Batista**  
so here, we're going to tell Patrone it needs to connect to etcd on this host. And remember, the port is a 2379 you get the case if that's the local box, we can Yeah, we can because it's listening on localhost. We can we can for example, change the the other ones like us to give a it's an example. And then the helped me to we want to move So this is when we Bootstrap, the this note here, the class of batch running, we want to send some information to be storage on our DCS. Right? For example, I want to have a TTL of communication between the nodes of 30 seconds, right. So if something happens here, if an old loose kind of communication or whatever, if I send a comment, I want the commentary or something to expire in 30 seconds, that's the max that I want for for for the TTL. I want to have a look, wait. Because we're trying to keep trying to communicate, right, so I don't want it to try to ping out communicate instantly. But I want to have a look wait of 10 seconds, retry, timeout of also 10 seconds, all those those parameters, here they are on the documentation. Right, I got to just go to the most important ones for our purpose today. And for example, maximum

**Charly Batista**  
maximum lag

**Charly Batista**  
of a logger. I don't want by 20 to pick a node that has, for example, more than I don't know, one. I gonna use my calculator here, you probably can see because I'm oops, and my calculator is not working. I'm getting here, one megabytes. So if my node is like lagging behind the match remote and one megabyte, I don't want these nodes to be elected to be elected as a primary, right. Now, we can send some parameters for Postgres itself.

So for example, I want to use the PG rewind, if something happens, I want the 20 to use not me to use if something happens. And I also want pertronic to use is lots one it poor for replication. And we'll see. Remember that we got a question that he said they're trying to run for Tron is trying to to bootstrap a new node or when the node fails, or put another applica. And it fails. And then Patrone tries to bootstrap again and fails and try to bootstrap again. So one of the very common problems that I see is when you don't have properly archiving, and then you have a huge database. So pertronic gonna use a PG PG, PG forgot the name of the commons, the one we use it to, to build the replicas, base backup, database backup, is that yeah, would you base backup? So pertronic gonna use PG base backup, right? So the thing is, if we don't let the opportunity to use replication is launc, the PG it will run PG base backup using replication slots. If PG base backup takes too long to finish the the the copy when the replica is done, when you start replica, the world files wrap around, so not wrapped around the world file has been removed.

**Matt Yonkovit**  
Right? So it's gone so long your your your replication. Yeah, the wallflowers are gone, or they've been exactly. Okay,

**Charly Batista**  
then, and petroleum, we will identify that problem. But when we see that the problem, the logs that they derive, is not able to come online because they're missing all files. And so what pertronic gonna do, restart over again, the problem is, if you don't have those log files, or if you don't use replication is launch that kind of your internet loop, because it will always take too long to to build a replica, right?

**Matt Yonkovit**  
Yep. And that's exactly what bitOK was saying. He goes into a loop after multiple attempts to rebuild finishes successfully, but it continually reinitialize it. So that sounds very similar to what he was saying.

**Charly Batista**  
Yeah, and the easiest thing to do is just use replication as long. So the appropriate thing to do is to have have proper archiving. Remember, from the backup streaming that you have, we need archiving, they're very important. So the easiest way to do is to change by trying to use replication as well, so that you solve the problem of building the replica mathrani. If this is the problem, indeed, it will solve this problem. But the idea is

**Matt Yonkovit**  
10 seconds, I don't want to go too deep into it, refresh people who might not have seen that stream, what are replication slots?

**Charly Batista**  
In 10 seconds. Let me go to here. So where's the so when we build the replica, you can tell the database, we can tell that replica to ask to the primary to create these this lock here. And the replica will always tell the primary What was the last MO file that it it reads successfully rage. So it will prevent the primary to keep removing the wall files that are needed for the replica. This is very simplistic explanation for this problem, right. So if you create the replication is locked, it will be created on the primary, but is the replica configuration that just go here for the configuration of the replica. If we go here on the postgres out to.com, it's using a primary slot, I pulled it the name, it needs to be created on the on the primary in advance. So it will tell the primary if you look, I am a replica. And I'm using these this logic to replicate. So I tell you what I'm doing. So what was the last one file last lsn that there was able to successfully get, and you cannot remove anything after this. This will fire if you have no more files. And if I'm too slow to keep up. You need to keep those files. So and then the primer will do that.

**Matt Yonkovit**  
And you have a replica slot for each replica you want basically is what Yep, so every server should get its own slot in that case

**Charly Batista**  
is awkward. Okay, ah, we have here the configuration for Postgres. So we'll see that those those configuration here, they are going to be kept inside of the GCS and parktronic. We will use those data here to append to the configuration file. Right. So we'll see them. So now we can send some comments to too you need to give me one Petroni initialize the database. So for example, when it's building a new replica, it wants us here because we already have the the rap goes on

and we also want to have some PG HBA. It's horrible here because identification plays a lot. So I'm not going to put anything fancy here on the PGA because we don't have time, and I don't. So those are for when you wrap because so it will be appended if we create if we're trying to create a new one. Right. So that's that's it for now. Okay. We also want to have some some cluster information.

**Matt Yonkovit**  
Now, question for you. Well, so these augment what is already in the configuration file for like the post, Chris, or replace. So if you have won't keep segments set to something else in your configuration file, will it overwrite it?

**Charly Batista**  
That's a very good question. It won't change you the configuration file that we have. But it has its own way to to apply the changes. So we'll see how it goes. It doesn't change the the file itself, right the the file that we have there, but it does apply the change

**Matt Yonkovit**  
so it'll apply sensor dynamic. It'll apply it on the fly. Okay.

**Charly Batista**  
Okay, well then, so it's just another way.

**Matt Yonkovit**  
Ooh, suspense is building ever One suspend.

**Charly Batista**  
Alright, we're almost there. Bulls are informations, those here doing formations are good for

what's happened to my VM here? That's not so we use on 13. Right? The Connect address. Actually, we have it up here. We could also use localhost here is zero. Okay, at least now is back. So Tony needs to know where are the binary files?

**Matt Yonkovit**  
Because see, because anything's changed, right?

**Charly Batista**  
Exactly. Also, it uses a passport files for now let's use these ones, okay. And, okay, I will create bill, they'll him we have a few losers here. So one for application. Remember that we created the user applicator. And the password is that very complex passwords. You a Zed 123. We also have a super user. So the super users Postgres and the password, I don't really remember, but we can put whatever we want here. And then it can change. Hello, so we're going to call PG plus. Plus just big plus. We can fill some extra parameters. For example, to establish the Unix socket on bar run PostgreSQL. Of course, I want to change it for the VA, because I don't know what happens to your box. But it always remove this folder. And I think you're

**Matt Yonkovit**  
it's not enough, I have several desk, right. So that's what it's just the restart removes it.

**Charly Batista**  
Have a nice alignment here. It's not my bow, this is a problem for Charly's Box. And we finally have some tags. We're not going over those tags now. But 20 has a lot of nice features. For example, we can, it can use callbacks. So for example, if something happens on a failover, and you have an action to take on failover. Or if you want some specific action to be taken on a restart of one of the nodes. So Patani has a callback function. And we can tell here on the configuration. I'm not going to do everything here. So but can we can add the configuration here, they'll be the callbacks, the right would be something like just added callbacks here. And then you tell Khatron Okay, when do you want the callback when the callback on the load when the callback on restart on when the role change, for example, and it's been promoted as a primer or something like that. Right. So

**Matt Yonkovit**  
in this could be any file, like you could provide it with various calls. Exactly. Yeah. Okay. So yeah, so any activity so it could be, maybe you want to log something to a file somewhere, maybe you want to call Grafana or PMM and write an annotation and a failover happened, or, I mean, there could be any number of activities that you use in the callbacks.

**Charly Batista**  
Exactly, exactly. Another nice feature is that pertronic can use a watchdog service or watchdog provider To to help to prevent the split brain, right, or to help to prevent to recover from a crash because Python itself can fails. Right pertronic Is here to help us if posts with faves who are going to help if pertronic fails. This is the watchdog. Does the idea for the watchdog it comes from the hydro side? And it started, like when you have a hydro that's far far away, you don't want to go there. Every time that you have a hydro problem all you need to do is restart the hydro what you're going to do, for example, on those towers for mobile phones, right to have those towers that are usually on the top of the hill mountains and the forests are really far far away. If the hydro can fail, it can just get stuck. How are you going to do that? Just to restart the hardware. So usually you have another piece of hardware that monitors that keep monitoring that those those those very important ones. And if it fails, it's just to restart the 100. Right. So this is a watchdog. And if you have your hardware, I mean the physical hardware, you can have a physical watchdog. But on the cloud, or we also have software workbooks on Linux, for example, we have the soft dog once there's a software backlog, we're not going to install them for now because we're running out of time. So, what are you going to do here? Is I gotta at least try que. Well, we need to do to stop by 20. Right. So and to do so I got to do a system CTL system CTL is stop Oscars. Oh, we're not running with systemctl every No, no, no, no, no. If

**Matt Yonkovit**  
you've ever. Yeah. That particular problem. Oh,

**Charly Batista**  
that's that sounds good. That sounds good. Okay, we're not going to suffer from that.

**Matt Yonkovit**  
By the way. Yeah, it would be interesting to know the configuration file that you just changed. I think that there was a question here specific to that. If you make changes to that configuration file, how do you ensure they take effect?

**Charly Batista**  
That's one question at a time. Let's go now. Right. So

**Matt Yonkovit**  
go forward. Go go, go.

**Charly Batista**  
I got a run for 20 manually here. Okay. Right. So I tried it, and just a configuration file with the path it seems good but running various mathrani dot YAML file. Right? So it of course, for your misery.

**Matt Yonkovit**  
Of course, you plan for that?

**Charly Batista**  
No, I didn't. I was hoping it would work at the first leg just like it is etc. They were so awesome. So amazing. And it looks like a parser so our YAML file has a problem of course, obviously, it's a Yama

**Matt Yonkovit**  
YAML certified

**Charly Batista**  
Yeah, let me vm this file. So what we're going to do here is we're going to copy this file and paste in a text editor and you obviously cannot see it because I'm not sharing all my screens by that's fine. So just here and I going to make sure that we have the proper itemization for the YAML file

**Charly Batista**  
because that is a problem that an Okay this one's also this one's right okay, it should be okay

**Charly Batista**  
It should be all good here, users blah blah blah yeah grace the item patient was a problem was always

**Charly Batista**  
okay

**Charly Batista**  
let's clean up this

**Charly Batista**  
let's tell them to just based without trying to look a lot nicer here, right

**Charly Batista**  
still, hold on let's see it right. And we try again.

**Charly Batista**  
Well, at least it's a different problem. It's better to bootstrap the cluster

**Matt Yonkovit**  
it looked look at the directory; it's Postgres 11

**Charly Batista**  
Why did I just yeah

**Matt Yonkovit**  
yeah, you're on 30

**Charly Batista**  
Yeah, I went to the routine solver. It's easy to fix.

**Matt Yonkovit**  
Yeah, you just have it here.

**Charly Batista**  
Yeah. I thought they changed it to that one

like it open because it probably cubes to change. Well, okay, community

**Matt Yonkovit**  
has Postgres

**Charly Batista**  
Yeah. Why? What happened to our horse race

**Matt Yonkovit**  
using a password?

**Charly Batista**  
Oh, 3232, we need to change the password. So the password, we're using digipass? Three.

**Matt Yonkovit**  
And your replicator password might also be wrong.

**Charly Batista**  
I don't know; I change that one already. Okay. ALTER USER was reduced us?

Oh, it's a read-only transaction.

**Matt Yonkovit**  
Code you log in as?

**Charly Batista**  
It's because we're trying to read it read-only transaction.

**Matt Yonkovit**  
Oh, because it is a stop. Yeah. Yeah.

**Charly Batista**  
Okay, let me start this one. Now it's right about the transaction. So a

**Matt Yonkovit**  
well, no, you didn't stop. You didn't stop it. Did you? Is

**Charly Batista**  
when we stopped a Tronic. Does it stop? Oh, the wrong database? No, no. And the right database? Yeah.

**Charly Batista**  
Why it's a read-only transaction? Well,

**Matt Yonkovit**  
no. Did you stop ahead of running? Yeah,

**Charly Batista**  
no, I did account. We'll see.

**Matt Yonkovit**  
Oh, okay. I didn't see that.

**Charly Batista**  
So let me answer a few questions. Before we move on, remember that you're asking what help or trying to change the configuration. So this is to help a trunk change the configuration of our configuration file. Remember we have a post res dot conf. So Patrone with names to posts with dark base.com. Here are 20. This is our original configuration file. Okay. So it was renamed mathrani. And then, pertronic creates a postgres.com file. Oops, with the configuration you said and doesn't include here. So these are the parameters we change and inside of control so they will be the last one that the post is going to read so they are going to over-read the parameters inside of the Postgres database. I'll turn doesn't change anything inside of our configuration just leaves there. And but rename the file and put the new creation files inside of this one. Okay, fair enough.

**Matt Yonkovit**  
So a lot easier. So then it will take the original you had and then just append this at the end is that great?

**Charly Batista**  
Yeah. Yeah, that's so not here says that we are in, in a read-only right. So we probably have here a standby signal file. So let's remove this file. We don't want to be a standby because this is a primary, or at least supposed to be the primary. And we want to start now for the series just to make sure. Okay. And, oops. If we do it, yes, well, okay, now we have the wizard. So now you can run that. Now again. So robber,

**Matt Yonkovit**  
you're the one who said this should be easy.

**Charly Batista**  
Yeah, I said,

**Charly Batista**  
we have 10 minutes for me to finish here, at least this old with mathrani. Running. And okay, can open up tonight, it's fine, because well, we're not using much long. And it's acquired a session as a leader. Right? So it's fair to drop replication is not replica one, because well, it's okay. We don't care because the other holds are using this replication as well. So, for now, we're going just to ignore this; this is what's expected. But at least this guy is the leader. Right, these guys later. So what we're going to do is, we're going to use that very same configuration file that we just have here. I need to remember that I need to change this from 13. Let me change my notes here. I have. Yeah, I changed my notes.

**Charly Batista**  
I have everything changed here.

**Charly Batista**  
Okay, so I got to do it manually. The audit holds my order.

**Matt Yonkovit**  
And when you create on the other nodes, and then start putting in the other nodes, if the databases are not set up currently, or even if they are, it's going to overwrite correct because it's going to be out of sync, if you haven't been running replication, or it hasn't been started up

**Charly Batista**  
is awkward. So if it's, it's a new cluster, it's a new node, or trying to take care of running the PG base backup and building the node for you. Right? So if it's an old node, like this one, because these nodes are in the sink, one doesn't need to do anything. So it just needs to put this node as a replica of the primary. And this is what we hope Atronach gonna do for us.

**Matt Yonkovit**  
Notice I hope Yeah. Let's be honest; sometimes we hope for the best. We do the worst.

**Charly Batista**  
Yeah, yeah, exactly. So here we need to change the IP

want to get the IP, what is going to change the IP here? And they used to do right I do so I don't need to change anything

so left Mitch, okay, this is the right IP

so the training and the configuration file, right? And the configuration files etc. But trolley tiny, tiny dot YAML file and look

Oh, you guys,

**Matt Yonkovit**  
you set this up as PG one, right? You didn't change it to PG two. No, I did. Oh, shame for shame.

**Charly Batista**  
Yeah, it's the problem. Of course. Copy and paste.

**Matt Yonkovit**  
Yes. Yes.

**Charly Batista**  
Let's we will. Okay, I'll keep this open because I probably have to you. Oh, all right. All right, I'm PDQ. I'm a rapid QA

**Matt Yonkovit**  
failed to start Postgres. Yeah,

**Charly Batista**  
of course, it's Adi Republic, Epogen, something.

**Charly Batista**  
Okay, let's go to the logs and wipe it out to the timeline. It must be increasing sequentially. Well, of course, it's fine to start to stop posting because remember we didn't stop post, Chris.

**Matt Yonkovit**  
Well, I don't know. Did you set it? Did you start with replication running when this? This? Yeah. And also if you didn't, Did you change the password for Postgres? Because that's the other thing.

**Charly Batista**  
Yes. It's not that bad replication is

**Matt Yonkovit**  
our applicant. Okay. Yeah. So this one was a replica. The third box was not right because you didn't get the third box running as a replica before this.

**Charly Batista**  
It is a DD nanobot. Oh, okay. Okay, there you go. So, yeah, the other one is also rapid, correct? Okay. So they

**Matt Yonkovit**  
I should have gotten those changes.

**Charly Batista**  
They should be Okay, so

**Charly Batista**  
yeah, probably; let's do one thing. Let's do one thing. One. One thing. So Marilee was the grease. Man, stop. Right. So I just removed the wow. That there are no log files.

**Charly Batista**  
Because it just removes everything. And if we start by trying to here

**Matt Yonkovit**  
are you looking to make the start the copy?

**Charly Batista**  
Yeah, it's trying to bootstrap from the leader one. That's okay. Let's go to node number three. And let me make sure that I changed me

**Matt Yonkovit**  
to PG three, the feature

**Charly Batista**  
tree, and I get the right IP. It is 66.

**Charly Batista**  
So and my route your city you just see much money.

**Charly Batista**  
Before we start, let's get to the horse hack widget three, the IP six, six. Okay. Next Level. Everything looks fine. Fair enough. Looks good. I got just to save and exit because I might need you.

**Matt Yonkovit**  
So here's an interesting question. So when you're bootstrapping, what can you do? And I know the answer to this, but I'm going to ask anyways.

**Charly Batista**  
And you can just be doing

**Matt Yonkovit**  
you're going to be doing a base backup. Right? Yes, exactly. But you're going to be doing it from the primary or the leader. That's going to impact performance. Could you potentially bootstrap from another replica?

**Charly Batista**  
Yeah, it can; in this case, it's doing from the prime because we only have the primary on the cluster, remember? So that's, that's the main reason that we can even use PG backrest to crop Delta 20 to try to use PG backrest to copy the data, instead of using a PG base backup the whole thing faster.

**Matt Yonkovit**  
So you can do an existing backup then. Yes, we can do backrest. Okay. There you go.

**Charly Batista**  
All right. So look. Awesome. Well, at least this one worked. looks like.

**Matt Yonkovit**  
So where are we on the other one? The one that's

**Charly Batista**  
the other one. Okay. Just a second vacation

**Matt Yonkovit**  
slot. That That's right. That's still just the bootstrapping process. So

**Charly Batista**  
that's still bootstrapping.

**Matt Yonkovit**  
How do you see what the progress of that is?

**Charly Batista**  
Ah, well, remoteness isn't fishbase backup. So the thing we can do is check the file system. It's kind of awkward for someone. So if we go here hate annoying, I want it to be easy. I know. So let's go too well before go here. One thing that we can do is we can use mathrani CTL 20 also has a common line we can use the common to least well, let's do here are 20 CTL dash c, the configuration five is, etc. petroleum, at least to list all the nodes we have. So we have this one, that is the latter one, we have d3 is running C, and we have PDQ, breaking the wrapper. Now, we do have a cluster, right soul? We don't have all that old yet, because BGT is is is creating a replica. But it will, at some point, come up with problems. We have, like a few gigabytes of data here, and it takes some time. And we are already running out of time.

**Matt Yonkovit**  
So, Charly, what I think would be good is if we can come back and have you do a little video later on just to show the failover once that second node is up, so just so people can get a sense of how what that looks like, I think that would be beneficial.

**Charly Batista**  
No, definitely. Yeah, we can do that we can do, just like we did last time, right? So we can do a video, and then we will the video.

**Matt Yonkovit**  
Okay. Somebody has to. I mean, there were a couple of other questions. I think we covered most of them. But I think one of them was how to create a common virtual IP. And I believe that there are multiple ways you can do that. So the question is which one, so that might be a good blog post topic for us or follow up for that,

**Charly Batista**  
on that one. There is a huge problem with the cloud providers because, especially for AWS, that I know, we cannot easily create a very point you need to use their API, the usually the cloud providers, have an API for you to create those people like these, you cannot wait. Let me share my screen here. Again, if you'd like, if you have your box, you're not using a cloud provider; it can be just as simple as your IP Coleman and creating here, right? It's pretty easy to be straightforward to create a beautiful IP right here. But the problem is, with the cloud providers, it doesn't scale. I mean, it doesn't let you go to attach the IP here. And the IP interface here that you have, then it's external. So you need to create it using the API of the cloud provider.

**Matt Yonkovit**  
Yeah, so yeah, you have to use you could create either like a domain that has a floating IP or floating IP, and then you but you need to attach it to that particular box, or redirect traffic if you're using a proxy or something to the right thing, because I mean, you don't necessarily need a virtual IP, you could also use obviously domain name and have failover, based in DNS as well.

**Charly Batista**  
Among the solution options, Another solution would be to use a proxy, right? So also, the cloud service provider they have their proxy solution that has all the automation of all those things. And you can use something like not Ansible. How is the name? Goodness, My mind today is it's you have Ansible and TerraForm. You can use something TerraForm to do all the automation so that we can use the API and do all those chains, create the virtual IP using the cloud provider API, all this kind of stuff, and push them to the proxy. So it's transparent for the application. The best way is to use some some some sort of proxy that doesn't need like, if you're not on the cloud provider can use AJ AJ proxy, for example, to control those things. Right, then, but if you are on using a cloud provider, then it's better to use the provider solution.

**Matt Yonkovit**  
All right, Charly, thank you very much, sir. It's always a pleasure to see you. It seems like we got a bit more people online today. So I think Thursday is a little better than Friday, especially for them outside the US. So we'll try that now for the next session with Charly. I will not be here. So we'll have a guest. So it'll be Mr. Stokes, Dave Stokes.

**Charly Batista**  
I need to be gentle next time.

**Matt Yonkovit**  
You can be nice to Dave. And the same thing next week for when Marco is in his MySQL stream. Until next time, hopefully, like, subscribe, and leave us comments. say that you love Charly and appreciate everything he does. He needs that stroke. sometimes he needs the pat on the head, the pat on the back. So just tell him how much he's appreciated. For all the hard work he does. Until the next time I met, we'll see you in a couple of weeks.
