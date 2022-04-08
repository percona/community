---
title: "Percona MeetUp for PostgreSQL Sept 2021"
description: "The first Percona Community MeetUp for PostgreSQL for an hour-long talk. We will talk about PostgreSQL Data and Database Security and discuss driving factors for increased PostgreSQL adoption."
images:
  - events/percona-meetup/cover-meetup-postgres-682.jpg
date: "2021-09-15"
draft: false
speakers:
  - ibrar_ahmed
  - jobin_augustine
  - matt_yonkovit
tags: ['PostgreSQL', 'Meetup']
---

Full video recording of the live-streamed Community MeetUp for postgreSQL we held on September 15th, 2021. Matt Yonkovit, the HOSS, sat down with Jobin Augustine, PostgreSQL Escalation Specialist in Support at Percona, and Ibrar Ahmed, Senior Software Architect at Percona to talk about “PostgreSQL Data and Database Security” and "Driving factors for increased PostgreSQL adoptions".

## Video

{{% youtube youtube_id="B_U3rYue0iQ" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:** 
Hey everybody, welcome to another Percona live stream. We are here with Ibrar and Jobin today. I see that Jobin might be having a little bit of an internet issue right now. It looks like the connectivity for him is a little wonky. So Ibrar Can you hear me okay?

**Ibrar Ahmed:**  
Yes, I hear you loud and clear.

**Matt Yonkovit:**  
Ah, wonderful, wonderful. So, hopefully Jobin will join back in a second. It looks like he's going to have some internet issues, always when you're going to go to the live stream. So I'm going to go ahead and shrink him for now. And hopefully he'll be able to pop back up shortly.  it looks like  your ears are holding a little stronger. So hopefully that works for us. And then when jobin joins back, we can get right into it. So how have you been this week? Ibrar?

**Ibrar Ahmed:**  
Yeah, I'm pretty good. I'm pretty good. Good. Yeah.

**Matt Yonkovit:** 
So this is our second live stream. A second meetup. The first one is on MySQL, this one specifically in Postgres, we have a few topics to talk about. So looking forward to seeing if we get a few community folks to swing on by and say hi, as well. So right now, I'm going to go ahead, and I'm going to hide the chat until a few people start to chat there. And so that way, we can get both of us in gloriously larger pictures, which is always great. And so if you don't know, if you haven't been here before, we're here to just talk about open source, we're talking about databases, we're talking about whatever pops up in terms of the community here. So we're excited to see what happens. So, Ibrar, we wanted to talk to you specifically, you mentioned Postgres security as a topic, that's pretty hot. And we can't turn around without seeing someone have a database that gets breached data that gets left open somebody has issues with their security. And then we've got Jobin back as well. So, he better maybe tell us a little bit about how we go about to secure our database environments.

**Ibrar Ahmed:** 
But let's go and the database security that most of the people think about when they think about that is database security, mostly they are focusing on only the authentication, that if this skill is their user, that's enough, with their data is good. But that's not the case, you have to secure your whole database not one way. In security, if you have one breach, that means your database is not skilled. So you have to secure your database, in all means yet, you have to store prospecting data, you are building your data, you have to secure your data. That's all you need to get all the expenses, you'd need to secure your computer where your database is hosted, you need to secure your whole network. And you have to secure your applications to which application or using that database. If you have any loopholes in one of the areas, then your data database is not secured. Because if some captured your data from the network, that your database is not secure. It's just not the responsibility of the database to secure your data over the wire also over the disk also. So you need to secure the database at home.

**Matt Yonkovit:**  
Yes, and I mean, I think that this is one of the things and jobin  thank you for joining us back. Just so everybody's aware, we are having a few network connectivity issues this morning. And this afternoon here, depending on where you are in the world. So hopefully that will keep up. But back to this discussion specifically on security. This is a lot about security in depth, isn't it? When we talk about securing a Postgres environment you mentioned  the different areas that you have to look at. And it's not just about  a single user, but it really starts first just with that user and making sure that you've got strong password authentication, you've got the right sort of credential set. And then from there, once somebody logged in, you have to make sure that the right roles and permissions for that user are set so they don't have overly broad permissions. And then from there you have to worry about what they have access to. You have to make sure that if those are okay, that your systems are patched and you don't have any CVS or vulnerabilities  so  that's, that's an issue. And then once you know your systems are patched, if someone gets onto the server itself, you need to make sure that they don't have the ability to sniff packets and see what kind of traffic is being transferred, that they don't have the ability to look at the data files directly. So you have to encrypt the rest. So it's about starting with the simple stuff in working your way down. But it's not just one thing, right?

**Ibrar Ahmed:**  
Yes, there is just not one thing that's absolutely right. You have to secure your database, by all means, and when I'm talking about the security, I'm telling my most of the customers that first disable all the securities or not securities, you just enable all these cookies. Sorry, I guess I said the disabled don't do that. I just just enabled all this right here, get in? Yeah, don't don't get it or get it, start losing some of the information that if your user wants to do something that gives him the access, deny everything first, then allow him one by one. I heard that people are doing that, allowing everything and just start deriving some of the features from the user. Don't do that. Just deny everything. And whenever there is a request that he cannot want to access something just allow him.

**Matt Yonkovit:**  
Okay, so what kind of features does Postgres have to help us with the security side of things?

**Ibrar Ahmed:**  
Yes. In security, we have triple A authentication, authorization and accounting. And PostgreSQL has authentication, Postgres will have our three ways of authentication. The first Postgres will have its own authentication system, where you can map Postgres to authenticate the user. The second integration method Postgres will use is a certification that PostgreSQL will give the username and password to the operating system, and then the operating system will authenticate that to the external server. So it will connect to a third external authentication server as they open up any server so you can connect that and authenticate from that. And that's that application point of view that post tester has a good any authentication and authorization Postgres could have a transaction that you can grant and revoke the services from the user and even you can also revoke some of the privileges from specific rows might not hold the table, row level security so that's a very cool feature actually. So when we are talking about the accounting PostgreSQL have some accounting like you can PG stat statement Activity Monitor, you can, you can get that information. But the PostgreSQL where the PostgreSQL is some kind of weak in that it says secures your data at rest, PostgreSQL doesn't have our table level encryption.

**Matt Yonkovit:**  
So there's no table level or field level encryption, you could do that in the application.

**Ibrar Ahmed:**
Field level exemption is there, because there is a country module which is called PG crypto, you can you can trip your column, but there is a no cholesterol level or table level equation, they are imposed their score, there has been discussion that people are submitting patches, they are community that they want to have that in pG 15. Hopefully, that theory will be the pg15. But hopefully.

**Matt Yonkovit:**  
Okay, so we have our first question, actually, from Harry, who is concerned because over the last five years, he's read on almost a weekly basis here about how data was stolen and breached? Are there some common sense policies, or things we can do to make sure that our data is safe? And then he has a couple other questions, which we'll throw up here in a second.

**Ibrar Ahmed:**  
Yeah, actually, some common mistakes people make are doing that, what they are doing, they are doing, giving the access of the database to the user. There are so bad, you can give your application access to the data. And you can only give the access to the people directly to the application. It says your database server is not publicly exposed. The first thing you have to be very careful about. It should be Within that VPN, that if you have a VPN, where you're in one mode, which is a database node that is totally hidden from outside the world, but your application, which is outside the VPN, can attack your database server directly.

**Matt Yonkovit:**  
So Ibrar we're having a little bit of connectivity issues here and there. So we're catching maybe every other word that you're saying a couple things, but let me just try and rephrase.  so I think that there's a, there's a couple things there that are important for us to get. And so  a couple people mentioned that your connection kind of dropped halfway through. So number one, you want to make sure that your database is not accessible, just publicly accessible, that is a huge thing. It's a huge vulnerability, there's generally no reason, especially if you have an application in front of it to leave your database out there. Right. And so I think that that is an important point that you were trying to make, I think one of the other things that you mentioned, that is really, really important is not over giving permissions, right, so everyone should have a set of permissions, and they should have the minimal set of permissions that they need to get their job done. And so  making sure that you have limited those permissions is very, very important, because over permissioning people gives them the opportunity to do things that maybe even if it's not malicious, they do by accident. Right? Oh, I thought I was dropping the test database, I accidentally dropped production. True story that actually happened to a very large company that I've worked with in the past where we did some consulting, they called us and oops, our migration ran in the wrong place, and dropped our production database. Not a good thing. Right. And so having those permissions is critical as well.  Jobine, what do you have some common things that you've seen as well, from the security thing to common sense practices there. Now, we're not getting any sound out of Jobin. So, a couple other things. Well, well, well, Jobin works at a sound apology for the technical things this morning. So a few other things that we've found. And both of you can chime in here.  be sure to watch out for critical CVS, make sure that  you're taking patch management very seriously. A lot of times people don't think about it, because  they set it, they forget it, and it's installed and it's running. But there are several CVS that are popping up jobin Yeah, yeah. Oh, yeah, you're joking.

**Jobin Augustine:**  
Yeah, yeah. So one common mistake is everyone concentrates on the front door, or those usurper privileges, all those things, but they forget about the backdoors. Say, for example, the backup might be happening to some file system. Maybe slightly old, but it may be kept open for vulnerabilities that backup servers. So the encryption and the safety need to be across the board from the application server database server, backup server standbys. So the entire analyst enter system is secured, so that I can get exposed from anywhere. So just concentrating on the primary database, user accounts won't really serve the purpose, things can get unnoticed.

**Matt Yonkovit:**  
And that's especially true. And we've seen a lot of differences between database breach and data breaches. And it's a fine line, because a lot of times you see in the press that there is a data breach, and they talk about MySQL or Mongo or Postgres or something. But it's not necessarily with a running system. It's with the backups, a lot of people and I'm guessing that a lot of people who are gonna watch this video, probably running on like an AWS or an Azure or Google Cloud, and they probably back up to something like s3. And people put their backups in unprotected s3 buckets quite a bit. And that has caused some of the world's largest breaches. Right?  I think that that is something that is common, if you will over and over again that this happens. And so you have to be careful when you talk about that backdoor. Part of that backdoor is where are you exposing that potential data? Another thing you mentioned, like the backup servers copying data from production to test.  how many people have taken a database and are taking a dump of tables that have some sensitive info and upload it to their laptop, bring it home, lose the laptop, something like that. I mean, that happens. happens. So you mentioned that there is no encryption at rest. So for some of this, is that something that we're starting to see some work done on in the Postgres community?

**Ibrar Ahmed:**  
Yes. I don't know yet. Since last one year, the community has been working on that. Some patches are there, the complete patches are there, but we are hoping to get it in PostgreSQL? 15 hoping to get it in Postgres at 15. But right now, only column level encryption is using PG crypto.

**Jobin Augustine:**  
Okay. Okay. Yeah, I have a different take on that. Because this is a common requirement to have data at rest encryption. But this is the great line of data trust doesn't clearly say whether that work needs to be done by the database, or the operating system or the storage. So there is this, this debate about the data at rest encryption is continuing for years, I think, at least for four years. Now, we are discussing this. But the community, and especially the user community, thinks that doing that at the database level, has a lot more overhead than doing it, something behind the scene, especially when data needs to be brought into the shared buffers that also need to be encrypted, which needs to be managed by Postgres. So the encryption goes through all the layers and the overhead gets too much. That may not be worth implementing. But at the same time, it is very easy to push this down, down layers like operating systems or storage. Nowadays, most sand devices, drives have encryption chips At the hardware level. And they do things almost as good as doing without encryption. The overhead is so minimal, even not noticeable. Yeah. So pushing the encryption overhead to the lower layers is something which we can generally advise. And like Ibrar said, it may come in upcoming versions. But I'm still slightly pessimistic about that.

**Matt Yonkovit:**  
Well we'll see, because I mean, I think everybody is concerned everybody has the concerns about performance, scalability, and security. Right. So the big ones out there. And I think that we're seeing more and more of these happen, Harry mentioned he asked why do we think this is happening? And  speculating, is this just because systems get those that are complex? And my answer to this, as always, I don't think it's because systems have gotten too complex. I think that we've tried to make things too simple and easy for folks. I mean, it's weird as it sounds, everybody wants the easiest way, but they don't want to understand those potential configurations or potential areas that they do have to secure. If you look at those security breaches that happen. Most of them aren't some deep hack that exists by someone exploiting some rogue code in the very back end. 90% of these tend to be something that someone just didn't set up properly. Right. I mean I think it's, I think that's the critical thing there. Now thanks, everybody for the questions there on that.  We've got another question from Pavan. So you can see it if you guys want, if my logical replication is broken, what's the workaround that I will continue without dropping the subscription? Now that's an interesting one. So Jobin, can you jump in here? 

**Jobin Augustine:**  
Yeah, yeah, that's non problem, the lack of continuity of logical replication. Yeah, those patches were submitted a few years back and it was rejected, just like our TV stuff, but not just for the sake of reduction sake, but there are technical reasons behind that. And now to the best of my understanding, and now some of the high availability solutions like patrone with the latest versions are addressing this problem. There I am made to test that, but at least I went through their documentation and it looks like they are solving this problem of failover of logical replication slot? Yeah.

**Matt Yonkovit:**  
Yeah, and so so. So there is a solution, but it's only available in patrone. You haven't seen it elsewhere and other  technologies or other extensions?

**Jobin Augustine:**  
Not yet. There are a few workarounds. I published a blog post about the same problem. And one of the comments which I got was from a guy from Yandex. And he developed a linux extension, but I am with a certain if sunbirds, it works. It solves some of the problems, but it's not a widely accepted solution.

**Ibrar Ahmed:**  
Some of the other companies have already fixed that problem they know their own for and as far as I know, that enters from the community has already submitted a patch in the community, but it's still not accepted by the community.

**Matt Yonkovit:**  
Okay. Okay. So this is an interesting question. Now, you mentioned and I'm gonna take this a little bit of a different direction. You mentioned like the extensions out there, and how they could be potentially patching or solving them in a little bit different way.  How often are you seeing these?  Like, extensions come out, they solve a specific problem, but they cause more problems than they solve. I mean, does that happen quite a bit? Like I've heard, like hey, if you're seeing some weird problems, you should probably start with looking at your extensions and start disabling them to see which one it is. Is that something?

**Jobin Augustine:**  
Yeah. Yeah, so if you look at the extensions, there are extensions, or the tools around Postgres, which are widely used, or the big community follows. So for example, PG repack, it's a real hack into Postgres to just create a duplicate table and stop the origin table, it happens transparently. But it's a hack. But this extension has been around for so many years, it's one of the most popular, even though it is a little hacky. It is widely used and widely tested so we don't have a problem in using it in production, because at least we know hundreds of companies using that. So that validates the quality. Yeah, and since there are big communities around, they'll validate everything, as each and every chord changes, the quality assured by the community, they monitor everything. Yeah. But that won't be the case, with the extension, which is not so popular or not if there are not many users, and as you said, Postgres has so many extensions, 1000s of them. And I remember there are extensions for you and playing chess.

**Matt Yonkovit:**  
Play chess within the database. Very popular with some people, I don't know. But it is something to think about, I guess.

And I mean Ibrar, you've done a lot of extensions yourself. And I mean, I'm sure that it's kind of a mixed bag with what you've seen out there in the community space as well, some better than others.

**Ibrar Ahmed:**  
Yes, I have been working with the extensions quite a lot. Most important thing is that everybody is making an extension, if you just see the foreign data wrappers, I think hundreds of foreign data wrappers are there. So you need to trust all the data extensions, which is widely adopted by the community, as you can see some of the names from the community person, some of the names from the party person, you will have to only trust on those extensions. And for other extensions, which are created by a single person, an unknown person, don't trust that extension.

**Matt Yonkovit:**  
Yeah. Yeah, no, I mean, it's, it's, it's, it's often like there's so much it can be overwhelming. I think at one point, I went out to GitHub, and liked the number of Postgres related projects numbered, like over 100,000. So figuring out which one actually will work and which one is abandonware it's, it's a problem in and of itself, right. So, I saw Praveen mentioned that he felt that patrone wasn't a good solution. I would totally encourage you to jump onto our Discord.  you can chat with our folks there as well if we want to get deeper into specifically that particular issue, and what we might be To do and maybe have some discussions with some of our engineering staff on potential fixes within the Postgres community. Harry wants to know if there's a generic checklist for PostgreSQL DBAs. on security, I believe we do have a blog on security practices 101 somewhere. I think that Robert might have written it, I have to look. But you do either review now, do we have a blog or a checklist for like, these are the security kind of things you should do in Postgres?

**Jobin Augustine:**  
I think. Yeah. IV. And we took the publish some blog posts on

**Matt Yonkovit:**  
Yeah, I think we do. Um, I'm looking right now. Let's see if I can find something. Yeah, we do. Postgresql database security published this year. Yeah. I saw that. Oh, no, actually, there's an Ibrar, Ibrar, you publish something. So I didn't find something that you published, I believe. Oh, any bars frozen again. So

**Ibrar Ahmed:**  
I have published many security blogs on authentication and different types. 30, but not exactly a checklist. Right? 

**Matt Yonkovit:**  
Not exactly a checklist. Okay. Yeah, I swear that I saw a checklist on our website here.

**Ibrar Ahmed:**  
Yeah, it's from Ben. Yeah. I got the blog.

**Matt Yonkovit:**  
Yeah. Let's see. So yeah, and I mean, there's a few older ones as well. So we can drop a few in the chat here for folks, if they're interested. That one's a pretty good one. And we've got the one from January here, that. And there are a couple of percona live videos as well out on YouTube, from different speakers from outside of the postgre space are outside of the percona space as well. So I noticed like there were some Amazon, there were some other folks as well. So I think there's quite a few resources. But I would encourage you, Harry, to check on a couple of those. So there you go. Pavan is a big fan of PG repack, by the way, so shout out to PG repack for everyone. Right? And oh, he sent me another one. So here's another one. That's a good one. Oh, yeah. Here's the Postgresql missteps and tips. Ah, thank you. Thank you for that there's another one of those for you who are watching. And when you go back to do the replay, those should still show up in the comments. So you should be able to get those and check those out at a later date and time as well. Yeah, it's great. And you can

**Ibrar Ahmed:**  
Also search on YouTube. My name is Ibrar Ahmed. I have also presented in some conferences about security tips and tricks.

**Matt Yonkovit:**  
Yep. So Harry, hopefully that sets you on the right path. Feel free. If you don't, or need some more, jump on to our Discord. I'm there, you can ping me if Eva or Jobin around and we can chat and find what you need to get you some help. So happy to have that as well. So another question. Oh, there are some white papers also published by EDB as well. Yep. There's lots of references out there for security. So  definitely  everybody has a little bit of a story there. And I'm sure we can help you find ones that are relevant to you. So we've talked a little bit about some of the other topics we've had on security. we've answered a couple questions, talked a little bit about a few things. But the other thing we wanted to talk about was, we've seen this massive growth in the Postgres space this year and job and this was a topic you were wanting to talk a little bit about.  We've seen that Stack Overflow has the fastest growing database in Postgres. The Most Wanted databases Postgres, the most loved, I think Postgres is number two behind Redis. I think they're almost equal though, right? So, tell us why you think that is what's going on here. Why is it all of a sudden, like it's actually not even an oversight, all of a sudden, you'll get the last five years every year. Postgres just gets bigger and bigger and bigger and bigger and bigger.

**Jobin Augustine:**  
Yeah, it all started from this time. It is around 2013. September, then that was a big bang for Postgres. And then after that, say this, this graph, you're able to see my screen, right?

**Matt Yonkovit:**  
Yep, we zoomed in. Yeah. So we lost the chat. But we can definitely Yeah.

**Ibrar Ahmed:**  
Yeah. So after that the graph looks almost straight, straight line, but actually, it's not a straight line, because the y axis is a logarithmic scale. So this straight line is actually an exponential curve. So, from 2013 onwards, there is no going back, we are on steady progress, capturing more and more users' user base increasing, and that is visible not only in just the surveys, even on Postgres conferences. Earlier, very few people used to attend conferences. Now the Postgres conferences are a big event. So yeah, the community is growing. Yeah. Like you said, For many years, even decades, the product was not in that limelight. Yeah. So but from 2013. Yeah, things are totally different.

**Matt Yonkovit:**  
Yeah, definitely. I mean, that's a big difference, right? So we've seen that growth continues to just escalate and grow a lot of it. Do you think that  and I'm gonna go ahead and unshare your screen for now. So we can see your face again, let me know, if you want to reshare it. And we do have a comment that I'll get to in a second, every time I turn the chat off, the comments don't reappear on screen, so that they're there, and I can see them, and I can show each individual one, but you don't get the log of them. So I will leave the chat up in case someone wants to jump in on this topic. But Praveen, I did see your comment, and we'll get back to it in a second. And so, a couple things.  We've seen this growth at the same time, and we've seen proprietary database growth kind of shrink. And so  we've often seen that the Oracle kind of going down, correlates a lot to Postgres going up, because a lot of those refugees from a post Oracle environment like to look at the feature set and the devalue that Postgres provides. How much of this do you think is driven by people fleeing, like Oracle, or maybe DB two, or SQL Server?

**Jobin Augustine:**  
A big chunk of users coming to Postgres are from Oracle background. Yeah. Because for many years, maybe decades, Oracle was ruling the database world, especially inside enterprises, they have a huge user base. And now there are multiple pressing requirements, for them to go out of that case.

Matt Yonkovit  
Yeah. I mean, I think that's, that's always like part of this right, is, is that migration, but I think that, I also think that a lot of people have found that Postgres being so open has enabled a lot of companies, cloud providers third party companies to adopt Postgres and develop services, develop features develop entire applications using it without having to worry about funny licensing or other crazy things.

**Jobin Augustine:**  
Yeah, you have a really important point, the cloud providers, they are, they're making a big impact in the Postgres community. And because Postgres community assets won't market, because it's open source, you use it, or if you like it, but that's not the case with cloud companies. So when they look at the customers, they look for an opportunity to move them to cloud to, to their open source, database hosting, and they do a lot of marketing about that, that's really driving and they do invest in posts they use by contributing as well. So there is a graph, which is very small to read, but there is AWS Google and Microsoft, they are contributing in a big way. So all the cloud companies are contributing to open source, and they're really solving tough challenges.

**Matt Yonkovit:**  
Okay. Yeah. And I think, yeah, I think that it's important to realize that a lot of adoption is really about how much we've been able to make it easier for users to get access, feel that they can get quality software where they need it. So just enabling that entire ecosystem to not only be able to download and use it themselves, but have those options for them as a service, I think has really spurred a lot of growth. Now, we did have a couple of Go ahead.

**Jobin Augustine:**  
Yeah, so now, Postgres is the software I use, more or less like a database kernel. It's, it's a, it's the center of the centerpiece. And we have a lot of things around that. Maybe sometimes even bigger than Postgres. At least a few years back, when somebody was to ask me whether the post GIS community is bigger or posted, this community is bigger, I used to doubt whether they are bigger or post, because those user bases are so big. And we know many enterprise users adopted Postgres because we have a post years extension, because he has communities behind that. So now, I don't have that doubt. Postgres is bigger focus communities. And that is the case with the many other solutions, as well as a Postgres kernel, don't have the ability to shard so but we have extensions created which will which will enable this kernel to have a sharding capability, the situs data extension, situs is acquired by Microsoft him, but yeah, they're still continuing the development is wonderful extension. Then the kernel becomes a totally different beast once we have those extensions enabled. So just like an exercise, this is a database kernel. That's the same operating system.

**Matt Yonkovit:**  
So we got another question from the community out there. I mean, again, it's very active today in the chat. We appreciate you hanging out there with us, asking us some questions. When can we expect multi master replication in the native community? postgresql? Do we have this on the roadmap? Oh, like you're just saying, nope, nope,

**Jobin Augustine:**  
Nope. Never, never. Never like Why? Tell us why we won't have Yeah. So because I don't see the multimaster Assa T is not solving any problems. So, first of all, look at the multimaster environments, the solutions, we have, say, if we have two masters, for example, if we want to have a multi master either, we need to have a shared disk, which is what our IQ does, which is a shared disk cluster. The Oracle RAC is a shared disk cluster. So at least not multimaster is the only one disc database is nothing but what you stored is only a single place it is stored. And the multiple instances there are mapped to the single stories and other solutions, where we have nothing shared architecture, or actually, there are multiple storages. But the data gets copied from one machine to another. So basically, every node does the same thing, what the master is doing so because the data needs to be replicated to another storage, so if you have shared disk storage, it's a single single database anyway. But if you have a multi master multi node, copying the data, it is not scalable, because it needs to do every node needed to do the job of all other nodes.

**Matt Yonkovit:**  
But is it like so let me let me throw this out there, right? So you look at some of the new SQL solutions, if you will, right? Where you've got like a sharded work set and you're talking about sharding, both of  you're gonna have multiple shard sets, and you're going to have multiple quotes, unquote primaries, where they're accepting rate rights from different components and you load balancing. It's not quite the same as a multi primary setup, right, where you've got multiple connections being able to write to just any one because what you're doing is you're saying, oh, you're writing to the shard set, and that could be on three servers. And then you could have three other servers with a different shard set. But I think that's becoming more common, right? Which is, which is a little bit what situs does, right? It's, yeah, the science extension.

**Jobin Augustine:**  
Yeah, yeah, you're correct. And sharding is a solution. Sharding really solves problems. If you look closely, everything which scales up is ultimately a sharding solution. Even if, if you closely look at the big data solutions, like Hadoop, the underlying architecture is pretty much the same shard. The sharding sharding solutions really solves the problem, but not multimaster that's not multimaster you

**Matt Yonkovit:**  
Ibrar You also were like very No, never never. We're never like why were you like that? Like I heard Jobin what drove it, but I would hear the reason why you were so negative on the multimaster.

**Ibrar Ahmed:**  
If you are focusing on multi master replication, then it will make your life more complex, then you can easily design your database without multi master replication. If you design your database to use a multi master application, and in my opinion, most of the people who were asking for multi master replication are coming from the Oracle background. They are very used to us to have multi master replication in Oracle they now want to say to Postgres but in my opinion, if they design their code, or design their code project, without multimaster myopia, it's much better than multi master replication because it will make your life more complex.

**Jobin Augustine:**  
Okay. Yes. Okay, yes, sorry. Sorry. Yeah. Just to add to the ibraaz point, many of the multimaster solutions were designed on pre CAP theorem age the CAP theorem, and you mentioned about the no SQL solutions, they are able to scale better because they look for eventual consistency, and that that's the real solution. That's the real solution. And it solves the problem. But many of the existing multi master solutions are designed and developed at an age where there was no knowledge of capitalism properly. And what really ended up is more outrageous. So interestingly, I personally, I have done a survey, because I was working for a big organization, I knocked down all the outages, and protected the graph for years, I mean, not what will cause the outage. So the multi multi master solution which the vendor supplied, those machines tend to cause more outage and more incidents, because there are more failure points. Nowadays, we count the failed single point of failures. So if there is a single point of failure, we can call it a high availability multi master cluster anymore. So for example, if there is a warning disk or a quorum solution, or if there is an interconnect, which needs to heartbeat each other, so all these things become failure points. And if they're, if they're single point of failures, then things are actually things that go against our expectation, he is overall at the higher level, we will feel that this is a high availability solution. But if you really count the numbers, those solutions will end up in more outages. In real numbers, just count the numbers we see and I have done that exercise personally. And why I'm done is because of the CAP theorem, because I want to look at whether this CAP theorem is really true in reality.

**Matt Yonkovit:**  
Yeah, yeah. And so um so there's a little bit of that. So Kishore had a question, but there was a couple follow up specifically on this. So Pavan had actually will, will show what could be said he's, he does come from the pure Postgres background, but he's impressed by the shared nothing architecture, like Cassandra, which, again Cassandra is an eventual consistency, right. So  you're you're, you're making some trade offs there. So I think that that's an important thing to consider as well. So something to just be mindful of. We've also got a comment on what we suggest instead of multimaster? And I think we might have covered that a little bit here, which, when we were talking about what to use instead of multimaster?  There are sharded systems. So sharding is a reasonable approach whether it's with situs data or something else. We've also got some other options. Does anybody want to say any of the other options that you might consider over a multimaster?

**Jobin Augustine:**  
Yeah, so um, We need to concentrate on the problem first. Okay. So a multimaster is proposed as a solution. So don't go and pick the solution. First, let us concentrate on the problem. Are we looking for high availability, then choose a solution which solves all the single point of failures, okay, that we have petronius wonderful on that. And if you're planning for scalable scalability, that's, that's a, that's a problem. Scalability is a problem. And the solution is sharding, or they even read replicas. So look at the problem first then the solution. So we have a solution for everything. But we don't have a specific answer for specific, so which do exist in dollar systems? Because we are not concentrating on the solutions, we are concentrating on the problems.

**Matt Yonkovit:**  
Yeah, and there's an interesting point here from Praveen who jumped back and mentioned, like, the Cassandra is running Netflix at a scalable site. And that's definitely like, so here's the thing, right? So there are all kinds of different database technologies and all kinds of different database engines out there, there's I mentioned some of the new SQL, you're hearing quite a bit about cockroach, you're hearing quite a bit about youbike, you're hearing quite a bit about ping caps type dB, all of them take that cloud native, scalable approach. But they're built from the ground up to be able to have some of those trade offs in the backend, they take the Postgres protocol, both cockroach and gigabyte, and they implement it over their own kind of back end storage in their back end database infrastructure, which is, it's a little different, it's still it's the, quote, unquote, compatible way. So it should work. But there are trade offs in application design, when you're looking at that sharded system, or how you're setting things up. One of the things that, and I'm going to go really old school for everybody, and I'm going to go outside the Postgres community for a second. Bear with me, I know you guys hate it when I go to another database, but I'm just gonna, I'm gonna bring up the NDB cluster for MySQL, okay. So if you're not familiar with NDB, a cluster for MySQL, it is ancient, it's been around forever. I mean, I was doing stuff, years and years and years ago. But basically NDB clusters structure is very similar to a lot of these sharted databases, where each node would get a portion of the data. And then you would have replica sets where you've got two replicas both have that portion of the data, the sharted data. And so it was insanely fast and scalable, for the workloads It was good at. And the problem is, once you start to get outside of those workloads, then you have to make application design decisions. And you have to change how you're accessing those databases. Because the same things that you expect to just work out of the box out of a Postgres or MySQL, or one of these other relational databases don't always work the same way. Because your data isn't all on one server. It's not aggregated, it could be across dozens or hundreds of servers, and then it needs to be filtered back. And then it needs to be aggregated over and over again, until you get your result. So  a lot of work has been done to make those better in this modern generation of the new SQL applications, but it is something that hasn't been completely solved. And the people that I've talked to, who use some of these new technologies, and they're awesome, trust me, I've seen them, they're spectacularly awesome at what they can do, and the scale that they can achieve. It's just that they say, look, you can't lift and shift, you're not going to take what's working today on Postgres and just drop it in over here and just expect it to work 100% because you're gonna see that things that worked well before might not work so well. So you're gonna have to make some changes. And I think that's an important thing to note. So I wanted to pull that out. So, a couple other things we did get this question from Kishore, we were talking about extensions a little earlier. And my face is down here. I can't really see myself. I'm kind of below the comment. So hopefully, there we go. So, Kishore asked, What are the common extensions that most Postgres solutions are deployed with? If there's 100,000 of them, how do you determine which ones are safe and vetted by the community? So is there a list somewhere of like, these are the most popular extensions and these are the ones that we would recommend.

**Ibrar Ahmed:**  
I got it. Yeah. Okay. So there are some lifts to list off extensions you can use that are shipped with the PostgreSQL pantry module. These are the most trusted extensions, because it is developed by the community. So you can trust them, I think it's a 50 to 55 extension or they are in the country module PostgreSQL, it's not installed by default, you have to install that extension. And one of them was a common name, our PG statement PostgreSQL, this kind of extension is there, you can use that. And other than that, some other extensions are there. But whenever you want to use some extension, you need to make sure there are some people from the community working overtime out there. Because some big companies are also behind that, like Percona have their own extension PG stat monitor, this persona is also sporting that they have a big company named percona. Behind that extension, like 20 that are like intervals dB, like second quarter normal, not second quarter right now. But

**Matt Yonkovit:**  
Okay, so we're breaking up a little bit there. But I think like, just to recap for those who might have not caught all of that. So I think that the number one thing is to use the extensions that are shipped with Postgres that are available in the official packages. If you're looking at other

**Ibrar Ahmed:**  
not packages a Matt, they are not packaging, all the extensions, you need to install that using PG accent.

**Matt Yonkovit:**   
Okay, so things are in the Okay, that's fine. Sorry. Thank you for the clarification, but also look for who has developed it, and who's supporting it, and what sort of support you can get if there's commercial offerings, if there's companies that are well established in the database space, it's going to have a higher level of quality because there's an engineering team behind it. If it's a product that companies  want, like you're designing, it's another good one to look into. But be careful, those that you don't recognize names, you don't understand what's there, unless there's a very specific need. Yeah. Jobine!

**Jobin Augustine:**  
Yeah. Yeah, so you're correct. So the extensions, which come along with the Postgres as part differently in different operating systems, for example, in red hat and sandos, itwill be a separate country package rpm. But it's part of the Postgres ecosystem, as he mentioned, it's developed and tested properly in the community. So whether we install the same control modules from the RPM packages, or the source is not important, but one thing it shows is that it is widely used and widely installed. So those extensions, we don't have any hesitation to use. Yeah. But as Matt, you mentioned, the popularity of the extension is key for other other extensions. One trick I used to play is to look at the GitHub star rating. So whenever people like a certain project, they'll click on the star, so yeah, that is, that's a good indication of how popular the project is!

**Matt Yonkovit:**  
don't run things in production that have zero stars and that were just released. That's good. Common Sense advice. Like I just uploaded the first version ones out there. Right.  don't don't do that. We seem to have lost Jobine  internet flakiness. But Pavan had another question here: failure and failback. Using logical replication, is it possible? Just like streaming replication? Ibrar, can you answer that Jobine is?

**Ibrar Ahmed:**  
I don't think so. I don't think so. Yeah, I don't think so. It's possible. Maybe Gavin can can Yeah, more comments on that, but in my opinion, it's not possible.

**Matt Yonkovit:**  
Okay. Okay. Well, I mean, we're about at our time anyways. So thank you for the questions everyone. We do appreciate you hanging out with us for the hour here. We hope you found this valuable.  I want to thank Ibrar and Jobin for stopping by and hanging out with us for an hour. Just talking about different questions, seeing what's out there. A lot of topics we Didn't get to, that I would have liked to discuss. So in another month, we'll bring on some more folks. We'll have some more discussions around Postgres. We'll see how it goes. And hopefully you enjoyed this. And if you have, if you want to talk about this, you want to come out and chat back and forth. Let me know, hit us up on discord and we'd be happy to set up something and have you tell us what kind of cool things you're doing. So, thank you, everybody, for hanging out with us. Thank you.


![Percona MeetUp for PostgreSQL Sept 2021](events/percona-meetup/cover-meetup-postgres-1920.jpg)

PostgreSQL counts more than 20 years of community development.The Percona Community MeetUp for PostgreSQL is an hour-long talk hosted by Matt Yonkovit, The Head of Open Source Strategy (HOSS) at Percona with experts to talk database. It is a series of regular live online streaming where users can ask any question.



* Day: Wednesday Sept 15th, 2021 at 11:00am EST

* Location : on [Discord](http://per.co.na/discord)

* Live streaming on [YouTube](https://www.youtube.com/watch?v=B_U3rYue0iQ) and [Twitch](https://www.twitch.tv/perconacommunity)

* Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=N2pmaDgxdnZwaHE1ZW5wam5mdDE5NDZuN28gY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

## Agenda

Our experts will cover following topics:

### "Driving factors for increased PostgreSQL adoptions" by Jobin Augustine

1. Adoption growth of PostgreSQL
2. How Community-driven development is helping PostgreSQL?
3. Feature-richness database with ANSI compliance and PostgreSQL Echosystem.
4. What is triggering massive migrations to PostgreSQL?
 
### “PostgreSQL Data and Database Security” by Ibrar Ahmed

1. Introduction to Database security.
2. How does PostgreSQL handle AAA (Authentication, Authorization, and Accounting)?
3. Security Best practices

The Percona Community MeetUp is a Live Event and Attendees will have time to ask questions during the Q&A. All kinds of feedback are welcome to help us improve upcoming events.

The MeetUp for PostgreSQL is recommended for:

* User of PostgreSQL

* Student or want to learn PostgreSQL

* Expert, Engineer, Developer of PostgreSQL

* Thinking about working with database and big data

* Interested in PostgreSQL

Add this event to your [Google Calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=N2pmaDgxdnZwaHE1ZW5wam5mdDE5NDZuN28gY19wN2ZhdjRjc2lpNWo1dmRzb2hpMHE4dmk0OEBn&tmsrc=c_p7fav4csii5j5vdsohi0q8vi48%40group.calendar.google.com)

Turn on the YouTube reminder on the [YouTube page](https://www.youtube.com/watch?v=B_U3rYue0iQ)