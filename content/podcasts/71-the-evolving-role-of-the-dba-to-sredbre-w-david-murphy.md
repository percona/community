---
title: "The Evolving Role of the DBA to SRE/DBRE – Open Source Database Podcast 71 /w David Murphy"
description: "David Murphy covers the rise of not only infrastructure as code but databases and schemas as code"
short_text: "It’s been a year since we last checked in with David, we brought him back to talk about the evolving role of the DBA to SRE/DBRE.  During our chat, David covers the rise of not only infrastructure as code but databases and schemas as code.  We cover why database design matters more now than ever."
date: "2022-06-02"
podbean_link: "https://percona.podbean.com/e/the-evolving-role-of-the-dba-to-sredbre-%e2%80%93-open-source-database-podcast-71-w-david-murphy/"
youtube_id: "sZfKXLarYl8"
speakers:
  - matt_yonkovit
  - david_murphy
---

## Transcript

**Matt Yonkovit**  
Hey everybody, welcome to another HOSS Talks FOSS. I'm the HOSS, Head of Open Source Strategy here Percona Matt Yonkovit and today I am joined by David Murphy. David, what's up?

**David Murphy**  
I'm getting to travel again. I get to go to Percona Live. I'm excited by that because I actually get to leave Ireland.

**Matt Yonkovit**  
Yeah, I remember has had some weird lockdowns. Right, like so it like it ebbs and flows, where it's like, you're not allowed to leave, you're not allowed to come in. And so it's been a little more rigid. I think then that somebody other places.

**David Murphy**  
Yeah, I think they've had some pretty strict lockdowns. But as a result of those lockdowns, we've really compressed the impact on the emergency departments and stuff. And so I think right now, there was something like 400 cases in the whole island and not in the whole Republic of Ireland right now. They only recorded 400 cases or something like that yesterday. And so obviously, they're doing something right, because now we don't have masks and all of that kind of stuff. We can go to cinemas and restaurants and all of that fairly normally. But I think next month will be the first time I actually go beyond like a quick flight in Europe, but actually go transatlantic.

**Matt Yonkovit**  
Now that should be good. Because I mean, you were living in Texas for a really long time. So being able to see people that and visit family and friends. It's always a good trip back home to just visit folks.

**David Murphy**  
Yeah, and that was why when y'all decided it was gonna be in Austin again. I was like, great. That's two birds. One stone right there. Oh, yeah. Yeah.

**Matt Yonkovit**  
Now, for those of you who don't know, David, we've done a podcast before. So it was like really early on. So the quality might not be up to snuff where we are today, because now we're like, on an episode like 70. So we've gotten quite a few folks who have come through the doors here. But it's always good to catch up and see what's new and exciting in David's world. So, David, what are you doing now? What, sort of things are you working on?

**David Murphy**  
So I'm working in the same kind of consulting area that I was before the last time we talked. But where I was taking Oracle and modernizing that and bringing it to the cloud and doing a lot of infrastructures, code, and stuff like that. I've now moved out everything, Mongo into the cloud for the company. And now I'm looking at MS SQL and MySQL stuff as well. So that's a whole different beast when you start worrying about Windows stuff. And so I started looking more at how do I solve certain RDS problems with AWS endpoints, which we could talk about in a little more depth here in a minute. I think that's an interesting area of challenge, but it can be solved kind of problem. And then I've also been looking at the new RDS custom stuff. I don't know if you've been watching that at all. No, I haven't. And so RDS custom is a really interesting thing AWS has started doing so as RDS to manage service database can't really do a lot have very limited disk access to even export a file, import a file and this stuff. RDS custom is for MSSQL, and Oracle, I can't remember if there's a Postgres one as well. But what it lets you do is take more control of that stack from AWS. And so you can manage your HA, instead of them managing it for you. And so now we can start thinking about proxy SQL and other tools in that same kind of vein that used to be off-limits or a bit disconnected, for what you want to do. Also, things like Redmine, and stuff like that might become easier to use, because you can have local agents on the boxes rather than hope that AWS added agent support for OEM or whatnot that you needed. And so that's, that's a very exciting area for me right now. And then also, I'm venturing a lot more into databases code, as opposed to infrastructures code areas. So this is more of the schema as code. How do we manage versions? How do I put those into application versions? How do I start getting people to start using deployment users versus runtime users so that we even limit the database access if an application got infected in some way? How do we keep them from dropping a database table? AKA they came in through some sort of hostage-taking thing, but they can't actually drop a MySQL table or drop a Mongo table because they only have access to create insert or delete.

**Matt Yonkovit**  
So you're looking at tools for database code.

**David Murphy**  
Yeah, so I started looking at Liquibase and a few tools like that. I have been a bit disappointed with the open-source option of that field right now, the open-source options, while there are a few good ones for specific tech, you don't get a lot of multi-tech support currently. And so Liquibase does some stuff. But obviously, as you move up their stack, you need to start going and paying, paying them for some of the mores of the security-centric or team-centric type features. So that's not great. But I'm hoping that as more teams are evolving into the SRE and DBRE space, we're going to start seeing more and more of those tools crop up.

**Matt Yonkovit**  
Yeah. And not to do a plug. But Robert Reeves, who's the CTO of red Liquibase is going to be at Percona Live talking about Liquibase. And that could be an interesting conversation, fly-on-the-wall type thing to see what sort of things that the community might need out of those in the open-source space versus what's been their paid offering. Always interesting to have conversations around that.

**David Murphy**  
That could be interesting, even just in the Expo Hall, if we could get maybe a group of us that are from companies like that, but also users that are there consulting with big companies to say, Hey, these are the challenges I'm trying to solve, what is your thought on where the community is going? As opposed to where your company-specific?

**Matt Yonkovit**  
Well, what's interesting is I've actually got a podcast in the Livestream booth for guests to come in, and we can invite guests. So maybe I'll have you and Robert and a couple of other folks swing on by we can, we can all chat live on like, like deploying schemas as code. And that could be interesting. that could be a fun time. But it's an interesting space, because you are, right, when we talk about the evolution, we talked about this a year ago, and I've not seen it slow down, which is the evolution of everything as code everything trying to move away from the operational side of things you mentioned, RDS, you mentioned you're gonna be talking about TerraForm. There are so many different tools that are focused on the operation side, it leaves the kind of design development and architecture side a little bear right now. And I think that's where the next generation of tools, the next generation of innovation needs to come. Right from that area. 

**David Murphy**  
Yeah, I would say, if I had to break it down, where we've seen the most maturity in open source, especially in like the Ansible and TerraForm kind of landscape is all on building that piece of infrastructure, whether it's RDS whether it's an EC2 node. But then when we start talking about the Ansible layer, or the user data, or the cloud or net layer, whatever, tool, salt, whatever tool you're using there, there's not a lot of cohesive tool chains there for how do I go from, I have a base OS to I've installed MySQL too, I've installed my users that I need for my team, to I've installed the application users to the application schemas to any stored procedures, blah, blah, there's not a big toolchain on that, regardless of which database tech we're talking about. And I've honestly built a whole bunch of that, I think, think there's probably a good 6000 lines of Ansible code in the Oracle modules that we've written for Ansible. And that we're doing because I, me and my team, I shouldn't say make of me and my team, we've broken up everything to where everything's templated and modular. And so like, I can just slide around new things very quickly, I can drop a NewSQL file in a folder, and it knows what, what template it should it's in because of the name of the folder. And so when that template is called that file is called, and because of the name of that file, it knows what order to do it in. Obviously, that's good to a certain point. But then Liquibase is what kind of takes me past that point. I do well, how do I worry about how these files are changing?

**Matt Yonkovit**  
Yeah, and I mean, I think that just beyond even like the structures I think that there's a component there that we're not there yet. Because when we talk about schema, migrations, schema, migrations have long been a problem across multiple programming languages, applications, and databases just keeping those in sync is an issue. But I think there's even a deeper more theoretical issue at heart which is, and I like to call it the apathy of developers when it comes to anything database-related or data related. And I think that I have seen less skill set in the data architecture side less thought process into how the structures look how they interact and how data is pulled out and used. It's more of I will I'd like to just be a black box, where I dump things in and something happens behind the scenes. 

**David Murphy**  
That is absolutely a big problem right now is because we, we extracted out that kind of check and balance that might have used to exist in my having DevOps, what you have is a whole bunch of engineers that are very good at building lamp stacks or Java stacks or whatnot that they're doing. But then, to them, the database is still a black box, and they don't want to get involved in it. And to be fair, I think Azure and AWS, and Google have made this problem worse because RDS is so easy for them to run a simple little TerraForm module that is built-in RDS five lines of code, they don't have to think about it and they start pumping data into it. They're not thinking about what is my index structure? What is my schema structure? What am I trying to achieve with this database long-term? And then when it is falling apart, they come to the DBA team or DBRE team and expect us to make the wave a magical wand, and the problem will just go away. And like I have in my main customer in their one biggest Mongo replica set, they have 52 apps involved in that. And they're a microservice strategy. And I'm like, Well, is it a microservice, if you have a single dependent core database, instead of one database per application, or one data store per application? That is feeding each of those microservices, and then the management and the leaders and the architect software architects when I bring that up that way? They're like, Oh, yeah, this is really bad. And I was like, it's like, we'll help you.

**Matt Yonkovit**  
well, what's funny though, is you have the opposite as well, right where now I've seen So microservices require three, four databases, and then there's 1000 of them. And then all of a sudden, you've got 2000 3000 databases out there. And it's like, now you've got like this large environment, which great if you've got the tools to manage that environment, and you can make it effective. But then everybody comes back and says, Oh, crap, now I need data from all like 1000 in one place, and then they go, let's create a data lake. Oh, that's what we need. And then then, like, all of a sudden, like, you just start bolting on more stuff in it makes it way more complicated.

**David Murphy**  
I think the secret sauce there is like in my AWS accounts, I have a nonprofit account, I have a private account, I have a shared account, and then an AWS as a whole, I have a shared account. And then there's an app, prod, and app non prod account. And it's very loosely translated. That's how we have things set up. But the idea behind that is, we have Oh, and there's a DevOps tools account. And so the idea behind that is, that it's not hard to have some sort of reference data central system that multiple different microservices might use. But what they're using is that microservice, not that central dB. And that's a big difference is because then they can still have their circuit breaker pattern on hitting that API and have some default behaviors if they can't find a piece of reference data. And to where they can still operate if ref data was off for five minutes because it was patched or whatever. But most companies, I think you're right, they either aren't doing enough in microservice separation land or they're doing way too much. And they're not thinking about Central Services, which still should exist to empower everything else. Because for example, if we're talking about some sort of ticketing system, the ticketing system that understands where seats are in an orchestra that doesn't need to necessarily be running so that you can order a ticket, you just need to be able to know what ticket ID or seat number you needed, you don't actually need to be able to display the map. And so like breaking some of those connections is where a lot of people fall down. Because they think, Oh, well, I need this. But as well as me, Matt, that seat map probably could have been in Redis as a write-through cache, so that if anything changed in that seat map, the database still had it, but Redis had it in case the database was offline.

**Matt Yonkovit**  
Yeah, I mean, I think it's it's that architecture design side of things. People are moving so fast now it's, it's just crazy. It's like we are having an insatiable need to get code out as quickly as possible without thinking and I think you mentioned RDS, Aurora, and Azure, making it so easy, it kind of hurts everybody else. I've been bringing that up for a while now as a big potential issue. So I mean, I definitely see those problems kind of are becoming worse?

**David Murphy**  
I definitely agree. I've also had certain conversations with Amazon at different times because like, for example, their document DB service. Percona Server has LDAP support as dynamic users based on my directory structure and stuff. Document DB doesn't have that. And so like, How many times did some engineer decide to use document DB or RDS because it was easy. But then it trips over itself on some very fundamental security thing, that you would have expected a different design pattern to go in to manage those users. And now you're trying to bolt on a solution.

**Matt Yonkovit**  
Yeah. But I mean, I think this is, I mean, this is classic. A lot of people call it to code debt. I don't even think it's tech debt or code debt here. It's something that works doesn't necessarily mean it's correct.

**David Murphy**  
Absolutely. And I wouldn't call that tech debt because tech debt if you're doing it right, tech debt is an intentional decision to delay changing something or fixing something because it's not worth the cost. Now, it's worth doing in six months. Whereas what you're talking about there is unintentional debt.

**Matt Yonkovit**  
Well, yeah, I mean it's, it's funny and I've used this example before you can have something that works perfectly well, for years, until you hit some inflection point, I had a plumbing issue where I bought this house, it's brand new, no issues, no issues, no issues, it turned out that they didn't install the plumbing correctly. And underneath the floorboards, there was an issue and until it reached a certain point where it started to, like cause issues in the floorboards. I couldn't do any I didn't even know that it existed. And for so for multiple years, the plumbing was fine. And then all of a sudden, one day it wasn't, and it was like a huge repair. And I think that's what you have in this case.

**David Murphy**  
Yeah, it's funny, you use plumbing. As an example, I bought a new house just a year and a half ago, two years ago. And in one of the sink drains, they had cracked one of the fittings. Nobody noticed by accident until I accidentally left the water just trickling. When I went to a wedding for three days, I had no idea it was a thing. I come home and the entire living room, like the smoke alarm, has water trickling out of it because it's just, it was enough that it eventually got past that level of the trap and just started filling up my ceiling. And but it's the same kind of thing is those little drip effects, whether we're talking tech, or we're talking plumbing, they add up and people forget that lots of small things add up. That's exactly why we're talking about a microservice problem. Because if you have 100, microservices, that pain of having all those separate ones was annoying, but not bad. When you have 1000 of them. That's significantly worse when you have 10,000 microservices, forget it. You have to go re-architect, there's no way you're going to manage that.

**Matt Yonkovit**  
Yeah. And I think that the further you go along, the more difficult it becomes, especially considering how the average tenure for people at a tech job is less than two years. Which means that by the time that you know trickle problem occurs, the person who wrote it probably isn't there and the people who are there are going to be like, WTF, right, like, What the hell is this? like, I think that's a common occurrence.

**David Murphy**  
And I think I think there's also some atrophy that occurs there is when we run into these situations, you are going WTF, but then you're also going, why? Yeah, why did they do it this way? There's gotta be a reason I'm not seeing, but you don't have that person to ask anymore. And so I do think that's a big challenge. I think that's why companies are pushing so much on infrastructures code, though, because at least at that point, once infrastructures code, it is codified, that decision was made at this time, and you have a GitHub history, and you can kind of try to assess out what might be happening. And if you've done it, well, you have a link to some JIRA ticket or whatever your ticketing system of choices, that gives you an idea on okay, they did this commit for these reasons. Let me try to reverse engineer just this part of it rather than my whole application. And so I think that that's where that trend is coming from. But I think a lot of people underestimate how expensive infrastructure as code is because somebody could do something in two minutes by hand. They might need a week to codify it and get it done right? In infrastructure as code.

**Matt Yonkovit**  
And let's be honest infrastructures as code is Great if you do it right, but if you do it wrong, it just turns one problem into several.

**David Murphy**  
Or it creates a much bigger cascade. Let's delete everything problem.

**Matt Yonkovit**  
Yes. I mean, you look at a lot of major outages issues, and it does come back to hey, that we had this configuration, change it automated through 1000 machines. Oops, we got that change wrong.

**David Murphy**  
Yeah. I mean, I've had some of that where we've we've instituted some TerraForm, verify type checks in Jenkins and stuff to help us. And like one of the guys came to me and goes, Hey, David, your Mongo instances, they have this thing. And I'm like, Why does my TerraForm say I have missing variables, all of a sudden, who changed my modules what's going on? Now, because like none of the Mongos had been rebuilt. So obviously, somebody made a change, they merged to master it hadn't rolled out with anything. But whoever was going to do Mongo next was going to feel the pain when they're released, got delayed, because they went to go rebuild an environment and it did not play nice.

**Matt Yonkovit**  
Well, since the last time that you have been on the show, I've instituted kind of a rapid-fire round Of our conversations. I find that this is an interesting way to kind of and then the discussions and conversations and I figured, now would be a good time for us to go to the rapid-fire round, where I'm just going to ask you random questions on the top of my head that I've asked other people, or maybe you haven't asked anybody. And so let's go and see how this works. It's worked out pretty well for other folks. But it is interesting. So I am curious, as you look at the tech landscape now, what is the technology that you are most interested in learning or figuring out?

**David Murphy**  
I want to say, the snowflake kind of data warehousing. 3.0 space is definitely something I want to spend some more time with. Because it's flipping on its head, a lot of the preset ideas around data, lakes, and data warehouses and how we should manage that data.

**Matt Yonkovit**  
Hmm. Okay. Okay. And you probably have a lot of data that you're managing right now. So it probably makes sense to start thinking about that.

**David Murphy**  
Yeah, I mean, I work with an airline, I imagine all the data an airline has to keep and have access to, from payroll to fuel to who's flown when to fraud, to all of these things that they have to, they have to know they have to be able to attribute that data. But one central data warehouse is probably a really bad idea because that's a nice honeypot for somebody.

**Matt Yonkovit**  
Yeah. So worst technology you've ever worked with, and you want to tell everyone to avoid? 

**David Murphy**  
Oh, oh. I have to say, I'm gonna make I'm gonna get a lot of haters for this. I do not like working with Ruby.

**Matt Yonkovit**  
Okay. Like some people like it, some people don't. I mean, what is your favorite programming language? If you're gonna go write something today? What are you going to write it in?

**David Murphy**  
I'm going to default to Python. And then I'm going to go to Golang if I need to have a lot of multi-processing, or kind of child-parent subscriber kind of model stuff going on. And depending on the amount of thread concurrency I need, I might need to leave Python because Python is great. I would say, Python is my go-to tool-building language. And GoLang is my performance computing language.

**Matt Yonkovit**  
Hmm. Okay. Okay, fair enough. Fair enough. And so what was the last book you read?

**David Murphy**  
So are we talking technical book or any book, any technical? What was it called? It was like, I think it was called The End of witches, which was a really interesting history of North North Atlantic, which history in the United States and the religious undertones and how different starvation and food shortages and stuff like that played into that and it was a book, it was about a family that was not witches, but how they got ostracized by their community because they needed somebody to hate. Okay, and so that was really interesting. Technical-wise, I'm wanting to dive into the new Postgres cookbook that just came out not too long ago, or did it? Is it about to come out? I can't remember the exact date. That's probably the next one. I'm going to grab it at a technical level. 

**Matt Yonkovit**  
Okay. Okay. And what sort of television shows are you watching and partaking in now? Are you are you? Are you a fan of moon night? Are you a fan of the Halo series or any of those?

**David Murphy**  
I haven't actually watched either of those yet. I went on a witch kick lately. I don't know why I read a book on which is, and then there was this other show that I came across. It's got two seasons in it. It was on prime, it was called motherland. 

**Matt Yonkovit**  
Oh, I think I've seen a couple of episodes of that. 

**David Murphy**  
And the premise is really interesting because it's modern-day. But what happened is in the early days of America, a kind of timeframe colonial time. Witches were brought into the army as another division of the army in all the countries around the world. And this is about witches in the military, and kind of the family names that build up in military families and all of that kind of stuff going on with magic, which is a background story going on. Very interesting. There's an also has some very strong like, there are humans that are very anti-witch protesting and stuff like that. And so it has some very interesting dynamics going on. But that was an interesting one. I binged all of that, but the one that I keep going back to and rewatching right now is Picard season two because I'm really liking Picard season two.

**Matt Yonkovit**  
Has that gotten to it? Have not it's on my list. I'm trying to keep up with everything. But it's, there are so many good TV shows.

**David Murphy**  
Yeah. I would say this about Picard for you without giving you, any spoilers. It's got, Picard. It's got, Borg. It's got Q.

**Matt Yonkovit**  
Yeah, I've seen the I've seen the previews. And the problem with all these streaming sites is that there's to two minds of people, right, which is, one is we're gonna release it every week, or we're just going to release them all. I prefer to release them all. So they can just watch them. All. Right. And so I know Picard is one that is a drop weekly. Moon Night which I'm still really confused by is a drop weekly as well. But and the same thing with Halo. But it's kind of hard to like, sit down and be like, Okay, I want to watch this. You watch it. And then like, you have to wait another week. I'm like, Man, I'm so over that Netflix has ruined me forever.

**David Murphy**  
Did you ever watch the whole Expanse series?

**Matt Yonkovit**  
Yes, yes. Yes.

**David Murphy**  
Is that a good one? Again, seen that one? That's a really great sci-fi opera. Kinda.

**Matt Yonkovit**  
Yeah, no, no, it's, that's, that's a really good one. I really got into that as well. Kind of sad when that ended. you invest so much into these shows, and then all of a sudden, like, they end.

**David Murphy**  
But on the flip side, there are like, I think three more books in that series. So anybody who watched the expanse that likes it should pick up those books and read what happens after because there is more.

**Matt Yonkovit**  
Well, and I think the books and the shows do diverge. And a few places that are like in you should.

**David Murphy**  
yeah, you have to look up. But I think as far as the timeline goes, the books and expanse were pretty good about keeping a certain pace until that last season, which blew forward quite fast. yeah, it depends, because of some stuff. It's nothing like the source material. Other stuff. They tried to be a little truer.

**Matt Yonkovit**  
Yeah. All right, David, thank you for coming out and hanging out with us today. Chat is a little tech, little, little, little sci-fi at the end. They're all the fun stuff. Great catching up with you, and hope to see you and we'll see you in a couple of weeks at Percona live.

**David Murphy**  
Yep, I'll see you then. May be great to chat with everybody again.

**Matt Yonkovit**  
All right. And for those who are listening and watching this video, please subscribe, and give us comments. Give us feedback. Tell David, that you disagree with his Ruby reference. It's okay. We want to hear from you. Feel free to put comments in the links below. So until next time, we'll see you later.

