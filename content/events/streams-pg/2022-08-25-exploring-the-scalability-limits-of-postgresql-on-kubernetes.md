---
title: "Exploring the scalability limits of PostgreSQL on Kubernetes - Percona Community Live Stream August 25th"
description: "Catch up with Percona Community Live Stream, and explore the Scalability limits of Postgres on Kubernetes"
draft: false
images:
  - events/streams-pg/PG-Stream-Cover-Week-12-August-25.jpg
speakers:
  - charly_batista
  - dave_stokes
tags: ['Postgres', 'Stream']
---

![Percona Community PostgreSQL Live Stream & Chat - August 25th](events/streams-pg/PG-Stream-Cover-Week-12-August-25.jpg)

Join us at Percona Community Live Stream, and we will explore the scalability limits of PostgreSQL on Kubernetes with Dave Stokes and Charly Batista. Come up with all your questions and get an answer right away.


## Video

{{% youtube youtube_id="Ij5TLLv6xuo" %}}{{% /youtube %}}


## Transcript
**Dave Stokes**  
It should be starting up. Let me see if it started on Twitch. There we go. Okay, folks, originally, we're supposed to talk about the scalability and limits of Postgres on Kubernetes.

**Charly Batista**  
We have an expert.

**Dave Stokes**  
Okay, so we are calling an audible, and we are changing that. And there is a conference, Charlie, once you tell us where the conference is, who's there? What are you speaking about and introducing the team?

**Charly Batista**  
Well, yeah, it's great having you again. So we have the Postgres conference in Brazil. It's PG conf Brazil. The PG con Brazil is the largest one in Latin America. Right. So we are coming back after those long years with COVID. And so it's great to be here together again. And conference and talking to people again. And we are here with some friends from Percona. So let me start here we have Marcello. Hello, everyone. Okay, doing? Well, we have Fernando. Hello, introduce yourself from the console at the Percona. professional setting. And we have Lara. Hello. I'm from the support team. Yeah. Those are the guys that helped us to make the database world a better world live right. To make it. It's awesome. So we're going to have talks here from Percona. This year at the PG conference. So my thought would be about disaster recovery. So, okay, I drop it into my database. Now, what? What can we do to recover the database? After you drop the database? What can be done? How can we solve those things? How can we fix the problem? My colleague, Agustina, is not here yet. Who else is going to talk? He will talk about how to deploy the database on the cloud, right efficiently. So if you need to spin up a database for a quick and fast test environment, I've used it for the development environment, even on some small productions or things. So how can we do that? Quickly and easily. That's going to be his talk at the conference; the conference is going to start tomorrow. I'm not sure what I got. I got to double-check with them. But we're probably going to have a lot of recordings here. A lot of talks are going to be recorded and streamed, and I highly recommend that because a really great box here high-level talks a lot of people from all around the talking here on the conference this year. That's our introduction. So why do you want to talk today a great bit around here about the conference? Okay, I got my unit back. We're setting up our booth a little bit, one of the conferences out there

**Charly Batista**  
and we have the main room here as well. For these this the main conference room so our about Augustine talks in my talk is going to be held Yep. So it's a nice environment. So we have plenty of space. We hope we got back here, we have a space to do something here for the conference for the databases or for the organizers. We have extra we almost got an accident. A lot of sessions here held on those were small.

Yeah, I think so as I said, we're going to start tomorrow. So we have here with all those amazing companies AWS, VMware timber from Brazil, Percona, Timescale for Linux amazing companies they're amazing conference. We have this guideline down here. This is one of the organizers. Realize now we're talking to the world. So, please, we have this bi-weekly call live that talks about the honorable database. And today, as we are in the conference here and showing them that they're going to have an amazing conference now held in Brazil. Yeah, also Percona guys. Yeah, not only for Percona guys, but yeah, we do have
 
Hope to see you. To see our friends tomorrow. Oh, in fact, tonight at Veeder, we're going to have dinner with speakers. And our super speakers. Yeah, we'll have gifted Brazil lots of chances. Tomorrow starts with Bruce Momjian is our guest, and we make the first speech tomorrow. And also, we are creating Brazil Association posters. And we will do this tomorrow, too. So we have a lot of conference talks. Interesting, including the guy who is hanging the phone. That's, that's, yeah, that's it. So we'll be the right time for deer and good talk

**Charly Batista**  
And that's it. So yeah, this is around the conference here. And hi, dinner. Do you guys have questions for us today?

**Dave Stokes**  
hopefully, you can hear me now. Yeah, now I can hear you. I would embarrass Bruce Momjian by a talk in Brazil 10 years ago or so. When we were booked out there in July and didn't realize it was winter in the southern part of Brazil, but just the highlights of your talk or tomorrow?

**Charly Batista**  
Yeah. Let me get my fireplace because it's a bit nice. Yeah, but definitely. So what we're going to talk about tomorrow? So Augustin going to talk about deploying efficiently applying databases. So he built this tool that helps with deploying the databases. So and you can easily deploy a Postgres database. And you can deploy a cluster, I'd say, with primary and cue replicas. And it's quite helpful when you have, for example, a test environment that you want to build quickly or for developers. We want the database running really fast, right? So we want just to apply the database. And you can use this tool; it's open source. It's on GitHub. And he going to talk about and I can show how those things work—using his tool. My talk going to be on Saturday, the day after tomorrow. So I want to talk about disasters. I sort of like thought about this. So I'm going to talk about database drop. So the title of my talk is okay; I dropped my database. Now what? So what can we do? Right? So can we use backups? Can you use a point-in-time recovery? And if it can use a point-in-time recovery, how can it work? How does it work internally, right? So we try to scare people, so they don't drop tables? Drop database Right And unless extremely necessary. That's that idea. So you need to be scared about that drop in the database. That's not good. That's not good. So, and also you try, to show them some alternatives, some ways that you can recover from a disaster. Okay? disaster happens badly. So I'm doing my maintenance at 1 pm. I don't have enough coffee. And instead of drop table a drop A table B, oh, how can I recover that? So maybe you have a bug in your system. So you just realize that the system is deleting, not dropping the table, but deleting rows? Right? And you only have the backup from yesterday, midnight? Well, now here is around 1 pm. So from midnight, one game, you have like 13 hours, you may have 13 hours of data loss. How can we get that data back? Is this going to be the one we're going to talk about? I going to drop one database, top on the table to sit chocolate Look, don't do it. Don't database. But Frederick is over, I hope it works. I don't really like live demos because it usually, you know, it usually doesn't work. But I have good faith. I have good faith. And that's going to be the topic for tomorrow.

**Dave Stokes**  
I always wondered why the database vendors never put in failsafe; you know, you type in dropped database, it comes up with a pop-up saying, Do you want to drop this database? Well, are you really, really sure? Yeah. Well, you got it lined here for your legal team? Yeah.

**Charly Batista**  
I run out of time; you need the right database. Now I agree. I agree with it because it's surprisingly, crazily easy to top a database, right? There is no confirmation. In some databases like Postgres, we have some advantages because everything is transactional in Postgres. So if you are lucky enough to open the transaction before you do the drop database, for example, you can just roll back. That's okay. But other databases don't have that facility, like drop operations or creating operations, DDL operations. They are not transactional in a lot of other databases. But still, if you don't open a transaction, you're not in the database that offers you the facility. But it's an opt-in; you need to opt to use that facility. And I thought they were those operations that they should have a lot. They should become engaged to do it, right? It shouldn't be hard to ask you like five, or seven times; you should ask again. Do you want to drop? Yeah, that's great.

**Dave Stokes**  
Well, MySQL used to have something called I Am a dummy, or novice node, where you could set up a capsule model; automatically, they wouldn't let you do things like drops or run. SELECT statements without a where clause. And I always thought, you know, that's like training wheels on your shell account. And I kind of liked that, you know, and, you know, maybe you don't get the drop, you know, okay, well, we'll just let you ignore that table, you're not really dropping, and other people can keep using it until someone you know, some adult comes along and signs off on it.

**Charly Batista**  
It reminds me of when I started developing a long time ago, one of the first projects that I worked with was with clipper, right, write, and then they used, the name of the database; they have an internal one that the language you use it, I forgot the name of the database. It was very simplistic. But they have those features that you couldn't from the interface, you couldn't drop or delete the table. So all of those operations they are weren't large operations. So it was a debate in the database. Debate based

  
two, or three. Yeah.

**Charly Batista**  
And all of them are logical operations, right? So you send the deleted drop comments that you just mark as dropped. If you want to drop it, you need to access the administration interface and do a back so that you remove so if you did mistakenly drop it into that. Just don't let your face alarm. I need to get my back. Right got a good safe

**Dave Stokes**  
measure? Well, ironically, many years ago, I had a friend who was doing small business development and database products that he found called Vulcan. And the guy who wrote Vulcan called him up two weeks later and said, we're changing the name of the database to it sounds a little bit better. And for many, many years, this guy, he was the last consultant in Southern California on the database to. And it was amazing how much real business got done on this tiny database. And now we have these huge databases. And they're still letting you shoot yourself in the foot by dropping tables. Now, in the real old days, if you were doing something dumb on a computer, and these were slow disk drives that spun around, you could help the machine and keep it from doing that. But that's not been the norm for close to 35 years now. Sadly, showing my age. What are the other talks going on at the show?

**Charly Batista**  
We had many talks, like your father Dallas, who said we have one from Bruce. We have some folks from VMWare and AWS, they're also going to talk about, we're going to have talks about how to use explaining, right, so this is one that I'm interested in, and how they explain works on posters, and how do you really read and use to explain things? A lot of it's, it's confusing. That that's the right word to say on all screens and external ports is really confusing. And a lot of people they, don't really understand how it works. And it's not like MySQL, for example, that you read it explain on the top, down, right, on the post this it's organized by the island nation. And if like, it's, it's confusing, right? Well, that's my take on it.

**Dave Stokes**  
First of all, to find out what indexes are being used. I have a talk next month in Amsterdam at the uptime conference on explaining, explain. And for someone who comes from a MySQL background, predominantly, I thought, Boy, there's a lot of neat information in here. I mean, Yamo output, who does Yamo output from explain, but I was kind of mystified. Okay, what indexes Am I using? And how do I force an index? There's no forcing of an index. Awkward. Yeah. So you basically turn off the type of join that they're doing, you know, turn off hash joints and, and try it that way. And there are no optimizer hints. I was watching a talk this morning about the lady who's writing the norm interface, which is not a RM type piece of software. And she says, Don't ever do that. That's a horrible thing to do. And since she has, has more experience than I do, I have to defer to her. What are the exciting things at this show? I mean, first log jam. That's Mr. excitement in the Postgres world. I mean, what else is going on there?

**Charly Batista**  
People started arriving today, right? The conference really starts tomorrow. Most of the people were going to start arriving today. Evening time. This city is close to St. Paul. It's not really in in some policy, but it's in the state of St. Paul. So it's around two hours driving here from the sample airport. So it will probably take some time for the people to start arriving. But we have a lot of things planned for the whole conference building this and organizing all the chairs around here. Do you see those? I don't know what they call those things. I think for people to lie down here and leave or whatever. Sofas Yeah. Yeah, they're not sofas

Yeah, yeah, I have no idea. We have other rooms here. For the books and some training. For the conference, we're going to handle your earlier we
want to have this, and also we're going to have what's

**Charly Batista**  
Ah, you know, it's like roundtable discussions and everybody has some voice if you can just come here, hey, I want to talk, and we'll get like five minutes and bring your thing. It should be a lot of fun. Right? I'm having like a really good expectation. We probably going to have some sort of shows or I don't know, he had on this fenced area. That building is here. Probably music or kind of things. Yeah.


**Charly Batista**  
Oops. Oh, I Well, many years ago, I was at a physical show. ups and yeah, yeah, it was.

**Dave Stokes**  
It was amazing how much music there was there on the show floor, including an impromptu sing-along, but I've never had any other show. So

**Charly Batista**  
those are the guys.

  
Yeah, it looks like skilled labor there.

**Charly Batista**  
Somebody has to work right. And I'm so happy that sometimes not me. Somebody has.

**Dave Stokes**  
Yeah, well, it's nice to know our support engineers have backup skills beyond databases.

**Charly Batista**  
Yeah, that's true.

**Dave Stokes**  
So what sort of swag Do you have? Looks like you have boxes of swag back there. Anything that we do?

**Charly Batista**  
Good, good question. We do what we do here. So we have some squeezes for chronic squeezes here. And different columns. I think we have four or five for once; we still have some stuff to drive here but for Cana much very nice. Yeah, they're pretty cool. It's a nice we have some bends and all the things. The tickers that are on the way

we have some nice Oops, my bad you can clearly see that I very cute with this camera, right? We have it looks like I'm switching connections here. We have those last things we have

looks like we have a shallow connection here. I see myself going green and coming back on the connection. Yeah, yeah. Yeah, when when it comes. Okay, we're going to move our booth a little bit more here to be more stable connection. But we don't have a lot of stuff for the event. So we're going to have a monitor screen here to show a PNM demo. Right. So idea, ideal for showing some kind of demo. Also, talk to people that applied and the build and all this stuff. And I have really good expectations.

**Dave Stokes**  
So what is the Postgres community like in Brazil? Is it growing? Is it popular? Or is it?

**Charly Batista**  
And here we go again. Yeah, well, yeah, every time I move to another place looks like we have those APs and switching the connections. And it's just okay. So now that the community is growing, one thing that we're going to do during the conference is we're organizing the border for for the community, right? So we want to have the past tense, the GPS and all this kind of stuff. So we were organized, as well, for the for the, for the community. So we will have an official community. Because at the moment, we have some people that they take the initiative and organize the conference, for example. But we can point that we need to have more formal, something more formal, just like we have the PG us the PG Europe and PG angels and those things. So we're also organizing the PG Brazil. The user group results. This is one thing that we were planning to, to take out of the contract from the conference. contrast. So you're going to have a couple of thoughts, a couple of meetings with people that are interested, we're going to go for both teams. So and that's the idea. And also, another idea is that you start to learn in the event, the conferences more in Ireland, for example, we want to decide the places for the conference for the next couple of next two years. Okay, we're going to be held the next year and the week after. And so we start planning a lot better. And also marketing and everything, right. It's growing. And actually, I'm surprised by the number of attendees that we're expecting for this year, that's around 300. Especially because we're coming from COVID. Right, we're coming from COVID. In Brazil suffered a lot from COVID. It's not a huge track, right? And it's a community conference, it's not held by a large corporation, we don't have that a lot of money to do marketing and all this kind of stuff. And we still got like, around 300 attendees, it's really good it's say something, say something about the database, it says something about the community of the database that you have, right. I'm really happy and happy that we were getting those popularities around here, we want for the next events to make it more healthy.

**Charly Batista**  
The people there are not so close to the central areas, right? So to make the conference more for the, for the people itself, because one of the main points of an open source project is to be able to achieve those people that they have, what results, they don't feel like they need to get on the market and all this kind of stuff, right? So if you can share knowledge, if you can share unities for those people, I think there's one thing we need to do. And I try to so that some great people helping, as you see the events is getting like really well done. So it is a lot of it's a lot of the year I helped the committee choose in the box. We have amazing ones, really good thoughts. Are they such four really good people around the world, like people well-known people from the community? We have people coming from Europe, US, Asia, whatever. Been our forte. It's been exhausting. But it's, it's great when you see things happening. It's really

**Dave Stokes**  
cool. So next year, we could be in Porto Alegre or Bahia or cocoa gap and a beach.

**Charly Batista**  
Yeah, well, I heard. Yeah, that's the idea. You're right. Not only some boat. It's not that I don't live simply. Yeah, not that I don't live simply. But if you could go live from my library, you know, some beach plays warmer place. Now. We are just as you mentioned, we were in the wintertime here. So if you could go for Brazil, that's a lot warmer, that would be perfect.

**Dave Stokes**  
Okay, well, I have my vote. Anything else you want to cover

**Charly Batista**  
today? Okay. Well,

**Dave Stokes**  
thank you very much for giving this insight to the Postgres Brazil conference. We'll be back in two weeks on something a little more serious. Probably not too much more serious, but there will be. So if you're in the neighborhood, drop in and see Charlie, if not, tune back in two weeks. And thank you, sir. It's always

**Charly Batista**  
great talking to you. It's always a pleasure to talk to you

