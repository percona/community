---
title: "Tigris Data - Percona Database Podcast 75 /w Ovais Tariq"
description: "After Percona Live, Ovais Tariq, Co-Founder & CEO - of Tigris Data, joined Matt Yonkovit, The Head of Open Source Strategy at Percona, to give more feedback about the event. Ovais explains more about the back end of Tigris Data, the trend in open source, and upcoming talks in the community. Learn more, join and contribute on tigrisdata.com"
date: "2022-06-16"
podbean_link: "https://percona.podbean.com/e/tigris-data-percona-database-podcast-75-w-ovais-tariq/"
youtube_id: "0WsfiKiqz_k"
speakers:
  - matt_yonkovit
  - ovais_tariq
---

## Transcript

**Matt Yonkovit**  
Hello, everyone. Welcome to another HOSS Talks FOSS. I'm the HOSS, head of open source strategy here at Percona, Matt Yonkovit. And today I am here with Ovais Tariq. Hello, Ovais. Welcome back to the HOSS Talks FOSS.

**Ovais Tariq**  
Great. Thank you, Matt, for having me here. The last time I was here, we had a wonderful conversation about databases. And how we manage data at Uber and that to be back here and really miss you at the conference is looking forward to meeting you in person.

**Matt Yonkovit**  
Yes, I know, right. So for those who don't know, I got COVID Like, the very week before the conference, so I couldn't travel. So it was horrible. Because you spent all of this time and energy and you want to meet all of your friends and all the people in the community. And then it's like, I'm stuck watching on Twitter. It's very sad and depressing. So. So now I need to go out and do more conferences to make up for it.

**Ovais Tariq**  
Yeah, definitely. You definitely have to do that. No. Look, I can tell you that the conference was a success. For me personally, it was great to be back in the community in-person meeting people and the schedule, the speaker's everything was great. I got to learn a lot. A lot of new things. So it was great to be there.

**Matt Yonkovit**  
Yeah, well, I'm glad to hear it. because the only one that you could blame for that would be me on the schedule. So I'm happy that the schedule is good. Yeah. Good speakers. Good lineup. That's good. I like that. I like the feedback. So, I was I did you see, Photoshop myself into Photos? Yes, there are some videos floating around. That I just ended up in mysterious places. So I'm just gonna say they're quite great. If you go look on Twitter for those. Always, always fun. But always you mentioned. Yes. Last time we talked you were at Uber. And now you have your own company now. And your company is called Tigris data. Tell us all about Tigris data, and tell us about what your aim is when we're talking.

**Ovais Tariq**  
Yeah, I would love to I would love to do that. So tigress is still connected with my history with databases. And based on my experience over the last 15 years, working at Uber, working at Percona, another company. So it's about building a user-friendly database, that makes it more that makes it fundamentally easier to consume and use databases for real-time applications. And the idea is to move away from an unbundled approach that the industry is going towards more of a bundle approach where the developer doesn't have to think about taking up multiple database systems, putting then stitching them together, and in and managing things like data pipelines, and data movement across the system, different systems. So simplifying all of that, and really providing what I think is the right service experience for databases.

**Matt Yonkovit**  
So it's really you mentioned different databases. So under the hoods, is it handling where data goes to which tours sort of database, which type of database, and its routing things?

**Ovais Tariq**  
If we think about data access patterns in general, and what applications typically end up using, they're a couple of things that come up to be common one is the OLTP system. And you could be using a SQL database or a document database, and then you need a real-time search. Because you want the users of your application to be able to do keyword searches, and fuzzy searches, and be able to personalize, their experience that way. And then, because microservice architecture is so common these days, and that's the way to build scalable applications, even driven development has become very important, which essentially means that streaming is very important. That's the way that different services communicate. So these are the three distinct data access patterns that I think are very important for every application. And what we are trying to do is cover these three data access patterns. But not by saying that there is a single storage engine that's able to serve all of that because that would simply not be possible. But have, instead a single platform that supports different these types of data access patterns, while abstracting away the different storage engines that are used to make it happen.

**Matt Yonkovit**  
So it's like one engine to rule them all. And then behind the scenes, you can pick the proper things without the end-user having to understand the underlying platform

**Ovais Tariq**  
one platform to rule them, rule them all in the context application. So the user is interfacing with Simple, easy-to-use API's. And those APIs are backed by a smart query engine, which knows where to which storage engine under the hood, to route the traffic to. And then the platform shows data structures, those distinct search engines are consistent and in sync.

**Matt Yonkovit**  
Now, you mentioned easy, right, like, so I'm curious, right, like, so API's that's good for developers. But for DBAs, it's like API? Isn't that what SQL is? It's just, that it's the API to the database. So why are you focused on ease in the developer experience? What brought you the focus?

**Ovais Tariq**  
Yes. Yeah, easy. databases traditionally have been difficult or hard from a usability perspective for developers, especially when, when I'm writing an application depending on who you talk to, right. I mean, if you're talking to DBAs, NFIB, and my DBA had them know, databases already know and all that you need, right? You just don't know how to use it. Yeah. But if I put on my application, application developer, and it's, it's oftentimes a little hard to reason about data modeling, oftentimes a little hard to map between how I'm building my application, which tends to be more object focused. And then mapping it back to SQL, I think that tends to be a little harder. That's why we see things like while I'm being used, right, which is essentially providing a way for the developer to be consistent with how they are writing the application code and accessing the database in the same way. So that's what I mean by my ease of use and simple API is that our focus is for the developer, to not have to think outside the code, right. So as you're writing an application code, you use the application code to define your data model. And then you use your favorite programming language and a favorite programming language construct to be to access to the database, you don't have to think about a separate language, and add a different way of you don't have to think about separate language, or you don't have to think about a different approach to storing and accessing the data. So that's essentially the approach that we are taking, which means that if for example you're using go, you would define your data model using the Go constructs, right. And then you will have APIs that are similar to any other function call that you would have, which you'd use to store and access data in the database.

**Matt Yonkovit**  
And then behind the scenes, you're doing all of the scaling the operational stuff, just handling it all?

**Ovais Tariq**  
Yes, scaling it, keeping it efficient, making sure it's reliable handling all of that, yep. Backups, all of the operational stuff. So the idea is to keep the infrastructure abstracted as much as possible while providing the right level of visibility. So not having it as a black box, we're still making sure that all the operational concerns are taken care of.

**Matt Yonkovit**  
Yeah, and I mean we joke a little bit about, like developers like, not thinking that databases are horrible and hard to use. But they do think that databases are horrible and hard to use, like, I mean, I kid, but I always tell people, developers hate databases, most of them hate them like it's a necessary evil, and they want to avoid it, if they can, they do it because they have to store data. But they don't want to. That's why I think that we're seeing kind of a renaissance in technologies that help developers feel more comfortable interacting with their database layer, right. So having the ability to have the security, the availability, everything baked in, that's great. But then also giving them an interface where it's just natural to whatever programming language or APIs are used to? It just makes sense.

**Ovais Tariq**  
Yes. And that is essential, the route that we are taking as well, you put it really beautifully that as much as we as database engineers, don't like the fact that application developers don't always love the database. That's, that's simply true. Right. And that's why I think it's important to take a cue from the application framework side, there's been a lot of interesting stuff that has happened on the application framework side, like lambdas. And making it a higher level so that developers are thinking more about business logic and not having to configure and run web servers. I think we need to take a similar approach on the database side or data site in general and no focus starts from the developer experience. And what is the developer what is the day-to-day tooling that developers using they are using some programming language right? How do I make this seamless for them not have them learn something new?

**Matt Yonkovit**  
Now, you're doing this as an open-source project, as well as eventually commercial. So what, are you looking for code contributions? You're looking for help in that space? like, what what are you looking for, from a community perspective that our listeners or audience? How do they get involved? Right? And what sort of help could you need?

**Ovais Tariq**  
Yes. So we are building it as an open-source project. I, myself am a big open source proponent, and my career has been dependent on MySQL for the most part, in other open source technologies. And we are building this, we are building Tigris data as the open-source solution. And there are multiple reasons for doing that. One of the reasons is from a transparency perspective, especially when you're building a data and database product, it's important to make sure that it's clear to the user in terms of how we're building the database because that's what's going to store the data. Right. So transparency is really important there. Then the other aspect of open source is what you touched about the community aspect, right. And I think that community is really important when you when you're thinking about building a developer-friendly product, how do you build a developer-friendly product, right by basing the roadmap of the product on the feedback of the developers by doing things that are really that the developers or the users of the product really think that this isn't making their life easy, and I think that's where the community comes into the play. And I'm, I'm really focused on making sure that our product roadmap is essentially driven through the community. Right. So that's, that's one core part of it. The other part of it is contributions, which is essential, which is again, the power of the open-source, which is all of these smart people around the world. Getting contributions for them from them would make the product a lot more robust. Right. And that will also make it clear

**Matt Yonkovit**  
Power of the crowd

**Ovais Tariq**  
and there's, and that's essentially the important reasons why we are going with Open Source to You have the community support, so that we are making the right product, while also have the community support to actually build out the product in the right way.

**Matt Yonkovit**  
Awesome. Yeah, no, I mean, that's great, right? I mean, I think that having the ability to tap into the community and to work with the community, drives a lot better code, it also drives good feedback, and it helps you with your product roadmap. I mean, it's it is kind of the facto standard. Now, what's interesting is you are in the open-source space, and I'm not familiar with your plans for the future, but we're seeing a lot more people adopt open source as a means to tap into the community, but then their end product ends up being the as a service model. So a cloud-based solution that hey, this is where we make our money. Sure, you can go grab the code, do whatever, but we have the behind-the-scenes cloud as the deployment method if you will. And we're seeing that more and more with a lot of big companies, whether it's in the MySQL space, or the Postgres space and Mongo space, whatever, where it's almost like cloud-first, with the open-source being more of that kind of marketing type of thing to get the interest in galvanize. So I'm curious, what are your thoughts on that? I mean, is that a trend that you've seen?

**Ovais Tariq**  
I definitely see that more and more happening, definitely see that trend. And the way I think about it is I think that that is essentially using the community for your own gains, but not actually giving back to the community, right. So it's especially if you have built out an open-source product and they have different variations of how these companies are building out the business they, for example, the deployment code is not open source, right. So, yes, the code is there, but how do you actually run it in production that is not open source, right. So is it is the product really open source and then the second part we see is other types of licenses which essentially mean that the product becomes open source when has actually grown old, right? Like, okay, this will become open to somebody for three years to three years. Well after two, three years, they're going to be so many security holes, so many bug fixes, who is going to actually use open source products I definitely agree that I see this more and more as a marketing ploy, and not really contributing to giving back to the community and making the community more empowered, which is why the approach that we are taking is that everything is going to be open source, we are doing the development open source. And that also includes the deployment mechanism that the deployment pieces, for example, we are, we will be using Kubernetes to make it be able to run this system. And everything around there is going to be open source. And we would eventually end up having a hosted version of the product. But the hosted version would not be any different than what is open. So it would just be thought of it as an installation of the product that is available on consoles. So, this is not to say that the hosted version is not needed, hosted version is still needed because not everyone would be able to host it. But I think that like when utilizing the community to grow your product and take it forward, in order to give back to the community, you need to make sure that we actually make the open-source part usable, you provide it in a way where people can actually use it and run it if they want to.

**Matt Yonkovit**  
So it's an interesting thought. So I was Kubecon was also this week, and being at home stuck with COVID. I was like I said, I watched basically Percona live through Twitter, which meant I picked up on all the Kubecon things as well. And there was an interesting thread that I started to see throughout some of like the conversations at Kubecon, which was there are the most popular topics are the user topics, not the contribution of the deep kind of like open source topics. And that really got me thinking like, and we've done some surveys here Percona about this as well. I think the generation of developers and users isn't necessarily as tied to open source as a must as much as it is a checkbox. And they really more care about like the button, right? Like, oh, look, I'm just gonna click the button and you say it's open-source, so I'm just gonna trust that it is, but I don't really understand underneath the hood, or really care, and I'm not going to contribute, I'm just going to use. And I think that that's a really weird trend, and I don't know what to make of it yet. But it getting to kind of like the hey that the different model here and contributing back to the community. I wonder if we've kind of tricked people into like open sources is a term, it's just another one of those like, it's like scalable, it's web-scale. Right like, is it turning into something like that now, where yeah, we all love an open-source who've been in the community for a while, but for a lot of folks, do they understand didn't care anymore? That's, that's tough?

**Ovais Tariq**  
I think that on our part, we need to do more education. So people understand what truly open source means. But I think that the other part too, it's essentially the cloud and the impact of the cloud, right? Because more and more people are now used to clicking the button in the cloud, just having the solution available to them right, then not having to run it themselves. And that is a completely fine expectation because most of the products don't tend to be infrastructure, especially products, right? And giving the user the ability to not have to worry about infrastructure is important. That's, that's how you enable people and enable a lot of developers to move forward with their businesses and their products. So that is definitely one reason why it is this way. I do think that people care a lot about open source. And especially when the last few years, we have seen more and more trends or open-source, we being something really important when, as part of building our product. And we have been we have talked to a lot of users of databases, right. And one thing that has always come up is the open-source part that they would very much prefer to have something that's open source. And in some cases, if it's not a console, they wouldn't even consider it. Because like one of the things that you were mentioning that open source, there's definitely the transparency aspect and community aspect of open source. But the other aspect of open source is quality. Having a product open source ensures that the product has longevity, the product has more quality. And that is something that people see when they use an open-source product.

**Matt Yonkovit**  
Well, with this push-button kind of environment that we're in now, where it's it's all about how do we just make developers forget about the infrastructure, right? What are the pain points that developers are facing in the data space now? Like, what are you seeing as the critical issues that keep on popping up? I've got a few that I've seen over and over again. But I'm curious, what are you seeing in the space? In terms of hey, now that we've solved or we've got solutions for high availability or for uptime or like, scaling a bit. What, sort of pain points do developers care about?

**Ovais Tariq**  
From a usability perspective and developer experience perspective, I think the biggest pain point for developers is actually related to the unbundled architecture approach or unbolted product delivery approach that the industry has taken, where instead of the developer having an end to end solution, we provide the developer with Lego blocks, a lot of options. And then we expect them to pick the right option and connect the right Lego blocks and connect them in the right way, while learning each of these Lego boxes individually, while operating, managing observing these individually, and that is the biggest pain point that I see that from an architectural perspective, The Lego-based approach or unburdened approach, if I'm building a platform myself, like the way I'm like, Tigris, that makes sense because that's the way to build scalable architecture. But when I'm building it from a user perspective, the user should not have to worry about many Lego blocks, and how do I stitch them together? And how restrictive in the right way. And I think that that is the biggest impediment that I see. Envision minus search developers are seeing these days, that they would very much want to have an end-to-end solution that works for them out of the box.

**Matt Yonkovit**  
Yeah, and a lot of times the database side of things is a secondary thing. Right. So there are solutions for a lot of deployment methodologies, and methods for the application side, the tools, and the application. But from the database perspective, it lags behind a couple of years. So it's a magnitude more difficult to handle.

**Ovais Tariq**  
that is exactly where I think that we are trying to innovate how can we push the database industry forward? And start thinking about it more from a user perspective, and not necessarily from our perspective as database developers

**Matt Yonkovit**  
So pushing the database is space forward, there's, there's quite a, quite a big ecosystem out there. There are a lot of database companies, what do you think is the next big thing in the database space? Like, where do you see, like, the space evolving here right now we started to see some New SQL-type applications and databases start to pop up, we're starting to see the emphasis on the developer,

**Ovais Tariq**  
We see more and more emphasis on developments, for sure. And we will see the industry go back and circle in members back in the article days when the oracle was able to handle there are different types of use cases, we will see more. And that's what I refer to as a bundled approach. So we'll see the cyclical back there, where you'll see more and more of this unified solution. So are that work out of the box. So I think that the industry is going over there. And then the other thing that is important is, I think that there's going to be a blurring of the line between the early database works is a back end that can also run some business logic, which you have been so in the database industry would remind you of stored procedures and stored functions, right. So I think that we will see more lines between application frameworks and databases. And we'll be moving more towards a back-end approach whereas applications are moving more towards a lambda style architecture, we will see more and more business logic getting pushed down to the database, and we would be seeing a push more towards a unified solution. That's more on the delivery aspect of things. And I think that there is a third aspect of it as well. Due to increased focus on data privacy and regulations. The other important aspect we will see is distributed database is being distributed instead of the centralized approach that we saw emerge. And over the last decade, we'll see if more of a decentralized approach and pushing of the data close to the user during the processing goes to the user, instead of bringing everything to a central place.

**Matt Yonkovit**  
it's an interesting point that you made that there's this technology, technology's cyclical we'll that goes on. And I think most people don't realize that a lot of technology that we use today was really invented like three-generation ago or four-generation ago and we just rediscovered verdantly and repackaged it. And a lot of the ideas that we come up with for new things they've existed before it's just we're rediscovering it's an interesting space. And you can learn a lot from how people have done it in the past. And I constantly see the pendulum swing one way, and then people go like, Oh my god, we're so distributed. We're crazy. We've got all these things. Now let's go back and consolidate. And then we get to consolidate. And it's like, why are we spending all this money on these monoliths' big things? Let's go back and go and distribute again. So you get this back and forth. And I think you're gonna continue to see that happen. Because in the tech space it's just a wheel, you got to wait long enough, and eventually, it'll come back around, and the popularity

**Ovais Tariq**  
you do see the circles and in the tech space in general living if you look at the programming languages moving from dynamically typed languages to statically typed languages. So there's definitely, this is definitely something that we see. But I think that whenever a new iteration happens when we go back in the cycle, we do come back in a better way. Because technology has generally moved forward. Yeah. So when we come back with me, we come up with a more efficient solution or solution that will take us powered further.

**Matt Yonkovit**  
I definitely see that it's something that is an interesting thing to see. But yeah, so Ovais. I like to play if you didn't, you didn't get this opportunity to play this game with me last time that you were here, which I like to now I've started this thing of just asking a lot of rapid-fire questions just so people can get to know my guests. It's actually a pretty interesting, fun way to just hear about you and learn a little bit about Ovais. And so these are 100% random questions off the top of my head, and I do not know what I'm going to ask. Okay, so I'm just for warning. Are you ready?

**Ovais Tariq**  
let's say yes.

**Matt Yonkovit**  
Okay, okay. Growing up as a child, what was your favorite food?

**Ovais Tariq**  
My favorite food was Barbecue.

**Matt Yonkovit**  
Yeah, barbecue. Okay, okay. Okay. and now what is your favorite food? We're gonna take you out to dinner. What kind of restaurant or place?

**Ovais Tariq**  
we gonna take barbecue

**Matt Yonkovit**  
Oh, yes, sir. Okay, so you haven't changed much at all? Okay, that's okay. That's okay. What's your favorite vacation destination

**Ovais Tariq**  
That's an interesting one. there are a lot of places in California. So you know it, we keep visiting it, but I haven't been to the Mediterranean, but that seems to be the place that I would want to go to and probably would be my favorite destination.

**Matt Yonkovit**  
Okay, all right. Fair enough. Fair enough. the last book that you read?

**Ovais Tariq**  
I read last is by the snowflake CEO. Okay. Yeah, I definitely recommend people read it. It talks a lot about execution and delivery. And essentially, execution delivery is what separates a successful company from one that's not successful, so I highly recommend reading it. Okay,

**Matt Yonkovit**  
fair enough. What about your favorite movie?

**Ovais Tariq**  
The Dark Knight series Batman The Dark Knight series. Not this one. The one Oh, that's, that's my favorite. Okay.

**Matt Yonkovit**  
Okay. So is it because of the Joker Heath Ledger? Or was it I think it was a whole series.

**Ovais Tariq**  
Heath Ledger for sure. Okay. But in general, I just really liked how emotional it wasn't. It really gets me emotional. Whenever I watch it.

**Matt Yonkovit**  
Okay, well, there. Yeah. Maybe you could be the dark night of the database base. Right. So you can fight for data justice. That'd be cool. I don't know, we could create a comic book character somebody out there create Ovais into a comic book character for us. We would appreciate it. So out of all the database releases that you have been part of and all the different databases. What has been your favorite?

**Ovais Tariq**  
Yes, so of course MySQL 8, I think was a leap forward. So I think that was a big step forward. MyRocks. I'm bringing in Rocksdb to the MySQL space and And then, but I think that the one that I liked the most was the work that we did at Uber building, building Uber distributed document database and taking that into production and building out a scalable system. That was one of my best experiences, I will say.

**Matt Yonkovit**  
And finally, we'll end with this one. What is the absolute dumbest piece of code you've ever seen moved into production? Like like, you scratch your head, maybe had to fix it? Maybe you were gonna Percona and somebody got called in the middle of the night to fix it. Maybe it was somewhere else you worked? What's it like something that's so like, to even today? You're like, what? How did? How did they do that? That's just awful.

**Ovais Tariq**  
Yes. Well, I am. I am a perfectionist. So there are so many examples that I can think of where it was just so hard for me to understand how this got into production, and I ended up rewriting it. So yeah, hard to come up with a single example. But yeah, I'd definitely say that a lot of lots of such cases. And in fact, when I look at my code, a year later, I see the same thing how the hell did this go into production

**Matt Yonkovit**  
Okay, fair enough. Fair enough. All right. Ovais. Thank you for coming out. For those who are interested in Tigris Data, you can go to is it tigrisdata.com.

**Ovais Tariq**  
Tigris dot Dev, if you want a shorter one, and tiger says and TIGRIS is okay.

**Matt Yonkovit**  
Okay. And I would encourage you to follow the advice from the team on LinkedIn and Twitter and all of the socials. And thank you for hanging out with us today telling us a little bit about Tigris Data and talking to us about the

**Ovais Tariq**  
it's been a pleasure. Coming here again, and thank you so much for setting up this podcast I've been following it. And it's a great, great learning experience. So I'm super happy to be here and looking forward to being here again

**Matt Yonkovit**  
Yes. And oh, vice. I think I think you might have seen I ended up being number one in the data open-source database market podcast in Tunisia. So it's growing in popularity. I have that number in Tunisia. I'm just, I'm aiming for number one in the rest of the world.

**Ovais Tariq**  
 This is definitely one that I find. I'm gonna get one. anyone who's listening to really follow this podcast

**Matt Yonkovit**  
Awesome. Awesome. All right. Thanks, Ovais. I really appreciate you hanging out.


