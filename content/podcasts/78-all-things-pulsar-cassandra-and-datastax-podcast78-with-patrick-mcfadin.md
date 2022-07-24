---
title: "All Things Pulsar, Cassandra and DataStax - Percona Database Podcast 78 /w Patrick McFadin"
description: "The HOSS Talks FOSS is welcoming Patrick McFadin, Developer Relations at DataStax, for the second time. Catch up with open-source databases in general, design, and architecture. Learn more about Pulsar and all ongoing projects from Cassandra, and DataStax. Matt asked a few rapid-fire questions to know more about Patrick."
date: "2022-07-21"
podbean_link: "https://percona.podbean.com/e/all-things-pulsar-cassandra-and-datastax-percona-database-podcast-78-w-patrick-mcfadin/"
youtube_id: "1la5FQjYDTI"
speakers:
  - matt_yonkovit
  - patrick_mcfadin
---

## Transcript

**Matt Yonkovit**  
Hello, everyone. Welcome to another HOSS talk FOSS. I'm the HOSS Matt Yonkovit, Head of Open Source Strategy at Percona. And I am joined once again by our old friend from DataStax, Patrick McFadin, Patrick, welcome to another round of my podcast.

**Patrick McFadin**  
Another round, yeah, here we go. You really got this HOSS Talks FOSS like you got that down. That's amazing, Matt. So one title. Yeah,

**Matt Yonkovit**  
yeah. Yeah. So I mean, that's cool.  and we want to I've been practicing it for, I think we're at like, 78 episodes, something like that. So I've had a lot of time and practice on this now.

**Patrick McFadin**  
it's good. No, it's got a bit of a rhyme. And it's like, I was kind of bobbing my head when you said it. I'm like, it can be like your own rap someday.

**Matt Yonkovit**  
I think so. We're working up towards the HOSS Talks FOSS rap. Yes, just expansion possibilities are endless. That's all I have to say. Yeah. I'm looking at the marks now.  T-shirts,  beer, coatings. Tik Tok is the next step in the evolution of the HOSS. Right, absolutely positive on it. Yes, yes. So Patrick, Patrick, you are here to chat a little bit about open source, which is what we love to do we love to talk about open source. We know that DataStax has a brand new offering out there; you have dipped your toe into the streaming space, which is interesting.

**Patrick McFadin**  
The thing is that when you're talking about data, there's not just one kind of data; there are lots of kinds of data. And I like to bucket things in data in the Data World streaming, persistence, and analytics. And persistence is you, and I have been playing in the persistence world for a long time, like, store my data and make sure it's still there when I come back. But the streaming aspect is really interesting, too, because that's moving data from point A to point B, doing something with that data when it gets there. Or is it is it's moving through the pipeline. Way more interesting. But I think the reason the DataStax is involved in this is that they're even more interesting when you combine these things.

**Matt Yonkovit**  
Yeah, it is interesting because when you talk about like data, persistence, right? I've noticed that applications have become way more complicated in that they don't use just a single database; they don't use like a single service. So sharing data and getting data between multiple persistent data stores, potentially getting data between different services and different components, all of that lead to this ecosystem. That's kind of a Picasso painting, if you will when you look at architecture diagrams.

**Patrick McFadin**  
Well, and that's the thing that, I mean, you and I, we also spend a good amount of time over in the data and Kubernetes community. And this is, I think this is paving the way for a whole new generation of thinking around infrastructure, especially data infrastructure. I don't think we need new things as much as we need to be able to use the things that we have appropriately in better architecture. I do think we're dawning on this age of architecture first, and not like reinventing new products, and we will probably see major there are always updates that need to be done. But you're right, that's Picasso's painting; what if it was more of a little more coherent than that, like when we're architecting, a building, for instance, it has multiple things like a wall, and door, floors, ceilings, there's all these components, but an architect puts them together in a cohesive way, makes it look nice, but also functional, this building will not fall. And I think that's the shape of data architecture. Now, that's where we're at at this point.

**Matt Yonkovit**  
So one of the things that I've been thinking about quite a bit is, I think we've reached this point where we've got so many options in this space, it's confused things a little bit, right. Because when we talk about data persistence, there are 400 different databases now listed on DB engines. You look at the cncf landscape, the roadmap that the map that they have, it's like four pages now. I mean, it's like so large, and there are so many components that do similar things. It's just that you know one uses a REST API, the other one uses its own language, and then the other one uses something else, and like, it's like the differences tend to be relatively minor. So I'm thinking that we're reaching a point now where either we have to build the tool to help access these seamlessly, or we're going to look at some consolidation in the market, or maybe a little combination of both.

**Patrick McFadin**  
Probably both. And we're, it's interesting because we're now getting into, like when you're building out that open data stack. It's not just an open source thing, which is also important, but also this open communication. So how we communicate the open standards, because you're right, is, what if I want to change a component? Do I have to rearchitect and rebuild my entire application? Or is it just a matter of I swap this thing out with the same communication protocols, but then it has new features underneath that are different, that gives me like, maybe there's a different way it scales, maybe there's a, like a different processing framework, or how it consumes storage, all those things, but I don't have to rewrite my code that's so critical.  what happens when Oh, we have to rewrite our code? Well, that's a six-month project or more. Yeah, no one wants to do that.

**Matt Yonkovit**  
Yeah. Because I mean, once it's actually written in the foundations late, it's really difficult to change the foundation and then change everything above it as well. Right. So it's probably the most costly thing is that design aspect. If you don't design it, you don't build the infrastructure upfront. There are a lot of cascading impacts there.

**Patrick McFadin**  
Yeah. And that's I think that's where I hope that services deployed with Kubernetes, or deployed in the cloud using a service in the cloud are interchangeable now because we have these open standards of communication between them. And that's what we were talking about, like, DataStax, is doing streaming now. But we're also really strongly supporting Pulsar, Apache Pulsar, which is the underlying technology for our streaming. And so thinking in terms of like, yeah, we want to support the open source side of things, which is we feel as a really great project. But we also want to provide it as a service as well. So giving people choice and portability. You'd be like, Yeah, we don't want to rent that from you anymore. We just want to go spin up our own, then. Sure. So we have to support both of those equally.

**Matt Yonkovit**  
Yeah. And I mean, the interesting thing about like, the modern ecosystem is, it's about choices.  not everyone wants to manage their deployments. And I think more often than not, people are looking for that kind of like service infrastructure to make it easy on their development teams.

**Patrick McFadin**  
There are some things that we, we were really, I felt like we made some strong architectural choices on our own. And maybe I should talk a little about how we got into this.

**Matt Yonkovit**  
Yeah, well, so why don't we take a step back? And why don't we start? That's probably a good place to start. So Patrick, How, what, what led you to Pulsar? 

**Patrick McFadin**  
Exactly! Well, it's a funny origin story, man. Okay. Yeah, let's get some popcorn. Yeah. Well, from my journey of streaming and working with Oracle, I've been working with the messaging systems for a long time. I mean, this is these are not new in the industry. IBM had MQ series and active MQ, Microsoft, everybody's had these things. And then we made a move towards, like, rabid MQ is really important. Tip CEOs huge. Now every cloud service has its own messaging. So this is not a new thing at all. Right? And, of course, Kafka is the one that's kind of taking all the air out of that room right now. And that was actually might when I started doing more open source work with messaging platforms and working with Kafka. I'd done some content on O'Reilly about building like this Apache-based stack of doing Spark? Kafka, Cassandra I had, at the time, Bezos.

**Matt Yonkovit**  
Yeah, well, yeah.

**Patrick McFadin**  
For one out of four minutes. But it was that tells me how long ago that was, but at the time, it's like clear that you're building architectures to do this. When I started running into trouble with Kafka, that was what I was working with a lot in working with other teams. There's this thing that bothered me about it, and they were not getting addressed in the open source community. I was trying to work through that. And it was like, we were trying to force something to happen that Kafka wasn't ready to do. So in 2018, I met the team at a company called streamline IO, just a group of people from Yahoo and Twitter. That was, they were trying to this they have this thing called Pulsar, I'd never heard of it. And the thing that struck me immediately was that this was built with, with a different kind of it's like the next generation like they learned their lessons from the past. And like if Kafka was Hadoop, Pulsar is like Spark, like, you're like, Yeah, that was a great idea. But here are some things to think about at scale. So the thing that impressed me immediately was Pulsar separated the computer from the storage cleanly. So each one scales differently. And it was built on this idea of multi-tenancy and having like microservices in place, so you can build out this mat, you could have these horizontal scalars, at different layers with full multi-tenancy, that was a first principle for the system. And this is where we are, as an industry is; we don't want just to do one we want to do 1000 or have hundreds of 1000s of tenants, and a tenant could be a customer. So if you think of like, what that means for the future of infrastructure, it's a must now we're talking about cloud native everything. Pulsar was kind of an OG in that regard. He was building out the cloud-native version of messaging at the time. And so that was, that was that first thing, and so I just started putting all my energy into working with Pulsar and working with that team quite a bit. And Jonathan Ellis, co-founder, and DataStax, he and I spent a lot of time working with Pulsar folks. We were both pretty impressed with how it worked. And that's really, that was kind of the origin of how DataStax got involved with Pulsar because we knew. And here's the best part, the Pulsar integration with Cassandra seemed like such a great win; it was like one plus one equals three. Because Cassandra does a lot of things that it can do, well, Pulsar does a lot of things that he does well, but when you combine them, they do. Everything is so much better together and in a lot of ways. So we can talk about that in a minute. But anyway, that's kind of the big picture of how we got to where we are right now.

**Matt Yonkovit**  
yeah. And I mean, it's interesting because I think this moves us one step closer to what you mentioned, like the Cassandra plus Pulsar, it just makes sense. It's like peanut butter and jelly. Right, it kind of goes together; I'm seeing more of a shift in people's mentality, especially from a developer space; they're looking for that tight integration, where they don't have to worry about the compatibility layer and things working together. And so I see more of an emphasis on, I guess, the term that I've heard bandied around a little bit as like developer data platform or data platforms where it's more components that are kind of designed and built to work together that solve that kind of multi-data use case, right?  you mentioned like, you've got the analytic side, you've got the data storage side, you've got the streaming side some people might have additional search requirements, right. So there are all these components, if they're specialized, individual things for that I'll talk a little different, but it makes sense when they can come together and work together as seamlessly as possible.

**Patrick McFadin**  
Yeah, it's like buying a device that supports WiFi.  that seems like such a basic thing. But if, let's say that you bought a phone, and it only spoke on LTE and some proprietary Apple network, it's like, but if there's WiFi, okay, great, I can integrate it with all kinds of stuff. And I can have a WiFi router in here, my phone and my thermometer, and all these other things are also using that as a transport. So getting the transport right is important, because then you're not going to have that discussion anymore. You're not like, Well, what should we use as transport? No, you're just using it. You're not making trade-offs, discussions, and trade-off discussions some of the hardest ones to have in an application build cycle or an architecture cycle? Because that list on the whiteboard, it's like, well, here's all the things we could use. Here's all the pain we have to go through to use them. Or, here's the downside of using technology X. Just not having a trade-off conversation is such an accelerator for building applications.

**Matt Yonkovit**  
Oh, yeah. No, I mean, I think that's, that's the thing people are looking for. Easier to use, faster to deploy, and less proprietary knowledge. I don't want to say proprietary knowledge is probably a bad term, but like, like, having, not having to understand all the details, right, or have deep knowledge of the solutions that they're deploying.

**Patrick McFadin**  
Yeah. Well, then it's sort of like, well, Pulsar, and that's where Pulsar, I think was appealing is that they were everyone that was involved in the project came with a different point. To view but more than willing to work together. So it supports Kafka; for instance, it can speak to the protocol for Kafka. But there are also connectors for things like JMS, or AMQP. And other things that are already out there. So like the streaming product that you can read from us. If you're on rabid MQ, you can just move that over, and it will, it will work. If you're using like Tibco, or JMS, or something like that, you can just move that over. So again, it's not like you have to rethink it. It's like using these standard protocols in a way you already decided to do. The only thing that's different now is you're renting this, or you have something that scales much differently deployed in Kubernetes, it's it has a whole bunch of new features that, again, start eliminating the trade-offs. One trade-off is not, we have to re-architect their application now, just pointed over there. Now you have a completely different scaling system that works great for you for the next five or ten years that you decide to keep it.

**Matt Yonkovit**  
So do you think that so as we look at like a Pulsar versus a Kafka or if you're already running that,  I mean, like, obviously, the scalability factor is a big play? But are there other potential use cases that are introduced?  by switching over to Pulsar?

**Patrick McFadin**  
Well, I mentioned the whole thing around the multi-tenancy. But the other really interesting thing is the multi-datacenter. Again what the, in the Kubernetes community, this is just becoming a big deal is multi-cluster; how do we, instead of just having one cluster that is an island, we may have two whatever, we have three, and Pulsar, and I should mention that Pulsar is two things. Its Pulsar is at the top end, where the computer is maintained. And then it's another project as Apache bookkeeper, which is the storage layer. And there are such great names and the book, the services that run behind the Pulsar head is the bookies. Taking book bets, so the bookies have managed the replication well across multiple data centers. So you're already getting this, this just a completely different dr stance, Dr. Or maybe you're distributed your data across multiple regions, if you're in one cloud, like Amazon regions, or from two clouds. It's just built in. And it's not something you have to work hard at. It's there's a configuration, and it works. Because the Pulsar cluster spans multiple regions, just like a Cassandra cluster spans multiple regions, it's a topology we're talking about. And so it changes the way you do your architecture, you're thinking, Oh, I have a Pulsar cluster. And then I have topologies inside of it. In those topologies are that that's when we get into those great discussions about how do we maintain our system or uptime? Or SLA s that sort of thing? If the East Coast has a hurricane, or if somebody drags an anchor through the internet cable

**Matt Yonkovit**  
Never happens. Yeah.

**Patrick McFadin**  
How's it going? So how are we going to be online? And still, they're good?  real-world problems? Yeah. Yeah. No,

**Matt Yonkovit**  
I mean, I think that that, that scalability in that availability is so critical there. And it's interesting, because a lot of the technologies you mentioned, and like the MQ type of thinking and processing the message bus has been around for 30 years, right, like yeah, like, like, it's been around for a while. And it's that modernization effort, right? It's, it's rethinking what we've classically done and putting the modern spin on it it's about building something from the ground up that has the capabilities to do what modern apps need, which is, which is very cool. And it's great that as a community, you have people who are passionate about thinking about how can we do this better, right, how can we make this solve the issues that are real today, as opposed to taking your application and having to make it go back in use the technology that was standard 5-10 20 years ago, and potentially limit some of the effectiveness of it. And so that's, that's a really good powerful thing.

**Patrick McFadin**  
And you mentioned the different points of view that, like, one of the cool things about Pulsar that I'm impressed by is an Apache project. And Apache loves the idea of a lot of almost competing interests working together for one software project, it's this, it's an innovation turn because you with open source projects, if it's single-sourced, it can get very monotone. Like, oh, this is the only only one point of view. But the Pulsar project is very healthy in that respect because there are just a lot of different points of view being represented there. Some of them are like big scalars a tensor, and there are multiple companies involved in people who were selling it as a service. So, if you think about deploying, if you want to deploy Pulsar and Kubernetes, you are well covered I mean, our Astro streaming is all running on Kubernetes. So, of course, things that we are interested in doing and adding features or adding enhancements or fixing bugs in the project or around running in Kubernetes like you probably want to. So I mean a good healthy project like that is worth paying attention to because it's, it is a diversity of thought, which is important. And that is a cool part of Pulsar right now.

**Matt Yonkovit**  
And I mean, it seems like it has a very vibrant community; it's something that I'm looking forward to delving in a bit deeper into myself because I think that there's a lot of opportunities, especially in that event-driven model that everybody's looking to build and how you stream data from multiple locations is a critical component.

**Patrick McFadin**  
Oh, in the streaming part, that's what's fun. Some of the new things that are happening right now are like, we brought this to Astra, which is rental like to go is or as a service, but Cassandra has had the CDC this change data control, so whenever you commit data into the database, you can emit it. Now that we combined, Pulsar and Cassandra, whenever you set data into a table, you can have it emit to a Pulsar topic. So what's and that's, that's building in all these neat, now you have it in this you're putting the data on the bus, here's what's the destination, and we've already seen folks putting it into something like redshift or snowflake more of the back end operationally, like the data lakes were here, I just want to pour data into the sink for analysis later. Great. We can offer that kind of integration.

**Matt Yonkovit**  
Yeah, it's like, it's like, it's like a live stream. ETL in that regard, right. I mean, exactly. It's the extraction and which is, which is cool. It solves a lot of challenges there.

**Patrick McFadin**  
I'm excited to see what other projects will be when you look at the open source ecosystem; how's that going to enable better ecosystem integration?  what's next? Of course, we have Parquet, another Apache format from Apache arrow. So that's that Spark has its streaming product. Apache Flink. Flink is another Apache project that can benefit from this kind of thing. Like Pulsar and Flink are usually using the same sentence A lot of times. So yeah, I mean, it's a bit of a renaissance in the Apache ecosystem for a lot of these data products that are out there because it's just solving so many problems still.

**Matt Yonkovit**  
Yeah. No, it'll be a really interesting space in the next couple of years to see which projects solve, which use cases where they become popular how the features evolve. It should be fun to watch.

**Patrick McFadin**  
I'm watching it.

**Matt Yonkovit**  
Of course, you are. Of course, you. Yes. So, Patrick. So here's the fun thing. You might not know this because you haven't been on the podcast since like episode like seven. So it's been a long time. So I have started something recently. Okay. And what I have started recently is Matt's random questions that I have no idea what I'm going to ask. I'm just going to ask random questions to get answers from you and see what kind of answers I get.

**Patrick McFadin**  
This is like a Rorschach test. Okay, I'm ready.

**Matt Yonkovit**  
Yes, it is it. Although Patrick and I were talking ahead of time, we share an awesome love of science fiction books, so we've overlapped on several of them. So I was going to ask, what was the last book he read? You can say it, but you kind of told me, I guess, this last book you listened to?

**Patrick McFadin**  
Yeah, who has time to read anymore? And we listened to everything right. So what was the last book that I read? Boy, Yeah, look and see. It was to Helen back, which was the Megaforce. The last Megaforce book, I think, is the next okay.

**Matt Yonkovit**  
Yes, yes. A good science fiction book that Joshua recommended does out, and he also makes the Ember wars. So in case people are interested in that, what is your favorite movie, Patrick?

**Patrick McFadin**  
Oh, Blade Runner is by far easy. Yeah.

**Matt Yonkovit**  
Okay, so did Blade Runner like the second Blade Runner? Destroy the first one.

**Patrick McFadin**  
I liked the second one. I'm in that camp. So sorry. Yeah. I also like, I also like Revenge of the Sith. I thought that was one of the best Star Wars movies. And so yeah? Oh, it was wow, that was amazing. But yeah, I thought 2049 was a pretty good movie only because I think it still compellingly told the story. And it didn't ruin the first one I mean, if they did, the two movies stood alone, and in many ways, but it didn't ruin the story. So the first story held up?

**Matt Yonkovit**  
Well, I think I think not to do any spoilers, but it was just the first one that left me with so many open questions who have so many fan theories. And then they tried to like, solve a lot of them in the last one. Right. And so I don't know, maybe for me, it was like, I liked not knowing a bit. Right. And  some of the

**Patrick McFadin**  
Yeah, that's true. Yeah. You don't want to don't tell me what the answer is. I want to imagine it myself. Yeah, that's true. I mean, you have two very different movies that different people make with different visions. And I mean, anybody who's going to try to follow up Ridley Scott is

**Matt Yonkovit**  
Yeah, yeah. Yeah, definitely. So Patrick, if we're up, we're going to go hang out at a conference in the future, and we're going to go out to dinner. What are you going to order?

**Patrick McFadin**  
Oh, let's see, what am I going to order? If I'm at the conference, if we're conferencing, I try to eat as late as possible, because it's really bad. But what am I going to order today? I'm going to order just a small piece of steak. I just love my protein. How about that? Is that

**Matt Yonkovit**  
good? Okay, a small steak, like a petite small, eight-ounce, eight-ounce data.

**Patrick McFadin**  
Okay, protein is really important when you're on the road. Okay. I know you probably wanted something really good. Like, people say

**Matt Yonkovit**  
that they like noodles. They would sushi, like, and I'm asking because people are going to meet you at a conference. They're going to be like, oh, let's go to dinner and chat. And then they're going to know what to order you very much. Okay. 

**Patrick McFadin**  
It's the thing around conferencing. I like that you just tend to eat crap when you're doing conferences. So I try to be very conscientious about that. Because you do want just to let's eat like the melted cheese thing? Or the all-you-can-eat barbecue in Austin or something like that?

**Matt Yonkovit**  
Well, yeah, you almost have to; you're compelled to eat whatever the regional food is. Right. Like, it's like, yeah. Do you know? Yeah. So anyway, it's just, yeah, you mentioned Texas. I was at Texas open source Summit. And it's like, everyone's like, let's get barbecue had like you eat barbecue like 17 times in a row. Right. Right. So I get that, but maybe a more important question is what kind of drinks should people buy you? If they're at the bar talking with you? And like you're talking about Cassandra, Pulsar, and DataStax, you're having a good conversation about open source. What's your beverage of choice?

**Patrick McFadin**  
Well, it's going to be beer in a very dark beer at that. So Guinness is always a go-to for me if nothing is available, but I like variety. So I like to see what a lot of microbrews do with dark, like any dark ale. Now. Yeah, it's that kind of thing. Yeah.

**Matt Yonkovit**  
Oh, yeah. Those are my favorite as well. I mean, I think if I was going to pick one black Porter from the shoots, I like that. So it's nice. That's

**Patrick McFadin**  
a hardy Hardy brew. Yeah, you can stand up.

**Matt Yonkovit**  
That's, that's, that's it. That's the way that it's supposed to be right.

**Patrick McFadin**  
the fun side is that I did a meet-up at the Guinness brewery. It's James gate. Because there's a startup incubator. This is not I did not know this. There's a startup incubator in St. James gate in Dublin. And I went there and did a talk on, I forget why probably Cassandra, but I was like, this is the holiest of holy places, and I'm here.

**Matt Yonkovit**  
So fun fact, you might not know this. Did you ever run into the old Ruby conference called Ruby on Rails? 

**Patrick McFadin**  
I have heard of it. I never went because I was not a Rails person.

**Matt Yonkovit**  
Well, I was a speaker for a couple of years. It was generally in Bend, Oregon, at the McMenamins brewery. And so, you would listen to talks and drink all day. It was a weird experience. It's fun. But Ruby on Rails. I don't know if they've done it since 2016 2017 It's been a while, but it was quite the experience. So when you say you did it that again, it's very, I've seen that before. I often wonder, why aren't there more kinds of like fusion? Open Source conferences, right, like so like, some heavy metal music or something with some great beer and open source talks. Like, like, we need this. I think we need this as, as a community, we need to do almost like an open source festival vibe.

**Patrick McFadin**  
I am a big fan of that because festivals are what they should be. We're all celebrating we're out there. Eating is a good place to get together. I love that idea.  The Hmong October fest, did you ever go to one of them in October? No, no. It was that was that. So that's a red monk thing. And so that whole crew, very beer-centric, and it was in Portland, Maine. And it was like that kind of it was a beer festival describe. It was kind of mixed into a conference. And like there was an official beer tasting in the middle of the conference.

**Matt Yonkovit**  
This is great, though. Why don't we have that? Like, where is this? Yeah, we need a festival like this. We need open-source music. Beer. And the festival, right. The open source. Beer Festival?

**Patrick McFadin**  
Yes. Like lots of that's what

**Matt Yonkovit**  
we need. Yeah,

**Patrick McFadin**  
 you're inspiring me. The next conference. I have any influence in I'm going to turn it into a festival and I'm inviting you.

**Matt Yonkovit**  
That is awesome. I will be there. I will speak and drink. I will drink and speak. I won't sing. But you could potentially ask me to sing, I guess, but you wouldn't lie.

**Patrick McFadin**  
If you remember, we talked about the rap thing

**Matt Yonkovit**  
well yeah, I'm better at improv. I think so.  you never know, though. So there you go. Slamming to slam. That'd be cool. Oh, oh, I've never thought about that. But that's something that I could try. Right. So there you got Patrick wood. You're inspiring me again. Inspired. Inspired? Yes. That's what we do here from a DevOps perspective; we inspire people, right.  that's what we're supposed to do is get people interested and inspired. And I think that a music slash open source slash Beer Fest would inspire people. And I don't even know how to how to, like, recover from that idea. It's like so great. It's like, I can't go anywhere from there. It's going to be stuck in my head forever.

**Patrick McFadin**  
I recommend you go back and look at some US festivals Do you remember that? That was when he had all this Apple money. And he left Apple he decided to do like this computer and music festival. Look at the US festival. It was back in the day.

**Matt Yonkovit**  
I'm kind of old. Yeah, that's been a while. Like, I just googled it real quick.

**Patrick McFadin**  
 And yeah, that's funky. Were we like, I feel like that's the roots of what you're talking about.

**Matt Yonkovit**  
Yeah. Yeah. Like, I mean, it would be cool. I mean, I'm down for it. So I think this is going to be the foundation for our we're going to point back to this podcast episode. And the number in 10 years, we're going to say, the world's largest open source music festival started here.

**Patrick McFadin**  
It will be like, like myself, Yes, but better.

**Matt Yonkovit**  
It is not necessarily an open-source conference. It's a music festival. We're an open-source conference that happens to have music and beer.

**Patrick McFadin**  
It makes it better. That's what makes it better. So yeah, right. 

**Matt Yonkovit**  
It's technical content. It's learning and drinking, and partying. Do you know? And yeah, that order potentially. It's going to be awesome. I swear to God, I swear to God, I swear to God. Yes. Yes. So, Patrick, my last question. What is your favorite open source tool at the moment? Like, what are you using more often than not? What are you getting into?

**Patrick McFadin**  
What am I using a lot of right now? Well, I mean, it's, I feel like I use VS code a lot. Is that considered open source? Probably not.

**Matt Yonkovit**  
Yeah, no.

**Patrick McFadin**  
The other one that I use a lot now is a Kubernetes thing. That's a that's an open source tool. And I believe, oh my god, am I like burying myself with non-open source stuff? Oh, no, VS code is open, but it's not. It's Microsoft open.

**Matt Yonkovit**  
Is that a bad thing? 

**Patrick McFadin**  
I mean, but no, I use Lenz quite a bit for managing Kubernetes clusters. It's a pretty cool little tool. Yeah. And my all-time favorite is pandas. I use a lot of pandas.

**Matt Yonkovit**  
Okay, well, there you go. There you go. You could say anything there was no right or wrong answer, right. 

**Patrick McFadin**  
So I'm just, I'm just going through like, yeah if I'm, if I'm going, to be honest, it's anything that manipulates data.

**Matt Yonkovit**  
Yeah. Well, I can manipulate data, which leads me to say Emacs. That's all I have to say. Well, there is some emacs love out there. I'm going to, I'm going to say that there is

**Patrick McFadin**  
an operating system as an editor. That's great.

**Matt Yonkovit**  
Hey, to each his own

**Patrick McFadin**  
Not judging, just saying.

**Matt Yonkovit**  
Well, Patrick, thank you for hanging out with me and having fun here.  chatting a little bit about Pulsar and some of the things that are going on.  if you haven't checked out DataStax, go ahead and check out DataStax new Pulsar offering check out their cloud there as a service offering for Cassandra, you can sign up to injury; we have a free tier forever, which is pretty usable. Yeah, please. Yeah. And I think one of the things that I'm interested in seeing is how people start to potentially use Pulsar to do almost like a, like a, like an ETL process between multiple databases, right. So you're going to need the same data in Cassandra and Postgres, Mongo, and your Snowflake, right whatever, whatever you're using, and how do you make sure that it gets to those places, and I think that technology like Pulsar can help. So looking forward to that. Yeah. Well, thanks. So Patrick, thanks for hanging out. It's been fun. I try to make it fun. Yes, yes.

**Patrick McFadin**  
I'll see you next to the festival.

**Matt Yonkovit**  
Yes, the next festival. All right, everyone. Well, thanks for hanging out today. And if you have questions, feel free to drop them in the chat.  put a comment here. I can always relate something to Patrick. And if you want an open-source Music Festival, let us know because I think we can hook that up. I'm just envisioning this I'm thinking of the lineup in my head already.  before we go, Is there like a headliner that you would put on that music festival like, like if it were going to be open source and music, who would naturally come as the headlining,

**Patrick McFadin**  
In the spirit of open source, we would just let people do like commit into a GitHub repo with their favorite bands, and we would just vote on them. So I'm not going to go and try and get those people there. Yes, show crowdsourcing going here. This is not like no one person gets to make that decision. But this is like a group. We're going to make this together.

**Matt Yonkovit**  
Yeah, so who was it now I forget. Was Megadeth that one of the guitarists did a whole open source album?

**Patrick McFadin**  
It wasn't Metallica. We know that.

**Matt Yonkovit**  
Metallica? Yeah. Yeah. Yeah, they think it was something like God. Now it's going to drive me nuts. But there is an open-source metal album from someone who lives in the Nordics.

**Patrick McFadin**  
anyway, so that person on that's all I must say,

**Matt Yonkovit**  
I do. Right, like so. Yeah. Yeah, I do. But, Patrick, again, thank you for coming. I appreciate hanging out today, and we will chat with you next time.

**Patrick McFadin**  
Great. See you, Matt.


