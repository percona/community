---
title: "Percona’s 15th anniversary, MySQL, MongoDB, PostgreSQL /w Peter Zaitsev and Vadim Tkachenko - Percona Podcast 41"
description: "Over the last 15 years Percona has been helping, enhancing, and helping millions in the Open Source ecosystem!"
short_text: "This year marks Percona’s 15th anniversary!  Over the last 15 years Percona has been helping, enhancing, and helping millions in the Open Source ecosystem! Matt Yonkovit, the Percona Head of Open Source Strategy (HOSS), invited the two founders of Percona, CEO Peter Zaitsev and CTO Vadim Tkachenko, to talk about the beginning and the evolution of Percona all along those 15 years. We cover the early days of MySQL, moving into MongoDB, jumping into the PostgreSQL community, and handling the modern landscape.   Listen to the technical and business challenges as Percona evolved from an idea to 2 geeks starting something new to a successful bootstrapped company with over 300 employees and thousands of customers. It has been an interesting ride! Hear all about it and what  the next 15 years of Percona will look like?"
date: "2021-09-19"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-41-peter-zaitsev-and-vadim-tkachenko/"
youtube_id: "xV8oZaThYyI"
speakers:
  - peter_zaitsev
  - vadim_tkachenko
aliases:
    - "/podcasts/41/"
url: "/podcasts/41-percona-15th-anniversary-mysql-mongodb-postgresql-peter-zaitsev-and-vadim-tkachenko"

---


## Transcript

**Matt Yonkovit:**
Hey everybody, welcome to an exciting, this is a very exciting episode of the HOSS talks FOSS, because I have with us the founders of Percona, Peter and Vadim, who are here to celebrate our 40th episode of the HOSS talks FOSS. That's what we're all here for right? Now, actually, we're here to talk about Percona’s 15 years, 15 years in the open source space. 15 years, we've been around 15 years, Peter and Vadim have been looking at each other cross eyed and funny for 15 years we've been here, and we thought it would be good to get together and talk about some of the good old days, some of the reasons why Percona exists, why we were started, and tell you some of the things you might not be aware of. So, hi, Peter and Vadim. 

**Peter Zaitsev:**
Hi, Matt.

**Matt Yonkovit:**
So, what you might not know is Vadim spent copious amounts of time on camera before we hit record fixing his hair so we thank you for getting you know looking nice and proper. And of course Peter was you know, I don't really care what I look like so that's always good, so wonderful to have you both.

**Peter Zaitsev:**
Well, I listen to you on the podcasts and that and I think many people will do the same and in that case, it doesn't matter.

**Matt Yonkovit:** 
Well I'm going to find a really unflattering picture of you for the podcast like you know screen just so you know people will be interested like what the hell is that I think those of you wearing

**Vadim Tkachenko:**
You should know Peter is handsome, so…

**Matt Yonkovit:**
Vadim,your bonus isn't necessarily tied to flattery on Peter I don't know like after 15 years I thought you might realise that but maybe you don't.

**Peter Zaitsev:** 
Yes, yeah, well, I can only imagine Vadim peeking out those things Peter, you are what do you say? Some good words about me right? Handsome handsome right? Out of a context right?

**Matt Yonkovit:** 
There you go. So 15 years while 16 years ago, you both were writing down the MySQL performance blog. And you had some sort of conversation about like, let's go start your own company. How did that happen?

**Peter Zaitsev:**
Well I worked for MySQL AB at a time and that is a regional company behind MySQL product before it became over owned by evil Oracle right but even in MySQL AB things have been changing. Right then I joined MySQL AB, I think that was a very sort of let's say, romantic community slash customer focused company really wanted to build their open source database and change a wall, the end by the time I was thinking about leaving it was their venture funded company which was focused on well we want to make sure we make our investors and found in the founders rich and if you happen to change your wall to in that case, it's kind of a good ideation but that is not a first priority and the fact some of the things that MySQL was doing and I think was was changing, right like I remember like specifically for example, talking to one of MySQL consultants who was and it was talking like Why are you pushing this MySQL cluster ndv everywhere he doesn't work with those workloads, he says well you know what we have is kind of mandate from our sales team on wherever to sell NDB and that is what we are going to do right and customers be damned if you will, right. And I found then this thing happened and there are some other decisions in the company would so I would find myself kind of changing my stance maybe from talking about us as we in MySQL AB to really talking about today because I wanted really to distance that from some business and technical decisions which was company was making which was really a signal for me internally what that is a time to leave and do something else. All right, and maybe fix in Percona some of those wrongs, which I was seeing happening in MySQL AB at the time.

**Matt Yonkovit:** 
So as that was happening, Vadim Peter brought these things up to you. What were you like? What did you say?

**Vadim Tkachenko:**
Well, for me it was much simpler actually. Yeah, I think I don't remember exactly what meeting it was, maybe it was an internal MySQL meeting, company meeting, or it was some conference. And yeah, we failed in the same room as Peter and Peter like, hey, well, why don't we start a new company? Well, anyway, yeah, okay, why not? Yeah.

**Matt Yonkovit:**   
Somehow for those who don't know Vadim, just him saying like, why not? Just seems to fit his personality, like he's a very go with the flow person. So you'll hear him say, like, okay, a lot so you know, we do have an internal drinking game, every time the team says, Okay, we have to take a drink. Unfortunately, we're filled with drunks now, that Percona because of that, but

**Vadim Tkachenko:** 
On a more serious note, I was a performance engineer at the time, and MySQLin the workout was medical performance. And maybe, at the time, I was still a young and naive and didn't share all that custom error range venture capital theory, but what I saw at performance side, MySQL could use at the time some performance improvements, but it really did not kind of touch did that raise interest from that time MySQL engineering and service system. So it was kind of also internal motivation to improve MySQL, to help her get a better experience with MySQL? 

**Peter Zaitsev:**
Let me add some history context here, which I think is kind of irrelevant. Shortly before we left, right, I think maybe kind of a year or so before Oracle bought InnoDB. Right. And, as you well know, now, right in odb, was actually their best engine, in, in MySQL, and frankly, a lot of my SQL value came from, and MySQL management team at the same time, I say, Oh my gosh, now our worst competitor, owns one of the most valuable thing of our value proposition in the InnoDB, right. And instead of focusing on what the customer wanted, is making InnoDB better,  MySQL with time took decision is kind of to put InnoDB sort of on ice and just make, make sure there is no improvements in that and try to kind of de emphasise storage engines and say, well, we will have many storage engines and energy will be just one of them. Right? If somebody somebody mentions the Falcon project, right, very, which was supposed to be the storage engine, which will be much, much better than InnoDB, right? And there was a lot of those kind of stuff where there was this kind of internal enterprise politics to showcase a better face to investors, rather than focus on what MySQL customers really wanted, which is MySQL and InnoDB to work very well together.

**Matt Yonkovit:**  
Yeah, and I think that that timeframe was very interesting, because that was kind of at the advent of when MySQL's popularity was starting to really rapidly grow as well. And so you had a lot of companies who just didn't have you know, they were running MySQL for big performance, and they just couldn't achieve the performance that they needed.

**Peter Zaitsev:**
Yes, I think from technology landscape, right there are a lot of companies which were maybe started a little bit before that think about like Facebook and Twitter, they are have been reaching the hyper scale and they needed their database to a very efficient, right, especially on the new hardware, which was coming up and remember around that time, which have changed from a CPU is becoming faster, two CPUs becoming wider, you will get much faster cores, but you need to work on those like a 4, 8,16, 32 cores better. And that in any software frontier, it requires some architecture changes, which just wasn't done in InnoDB. Again, because InnoDB was supposed to be kind of crappy storage engine which was supposed to be replaced by their glory Falcon.

**Vadim Tkachenko:** 
That was one of my striking stories. Again, I was a performance engineer. workout of performance evaluation and the time like new brand new Intel four core CPU, four cores was like, top notch. And what happened on four CPUs, InnoDB actually was slower than on two CPUs, Intel. And they just was like, very striking point for me as assumption is wrong here.

**Matt Yonkovit:**   
Yeah, so we it was. It was a time when there was this opportunity in MySQL didn't want to address the problems that existed. So you both decided to found this company to kind of fill that gap. But I mean, it's still a scary job, right? So you're working for a company, you're going to start something new? I mean, how did you go about building that reputation? And becoming the Percona we know today like, what was the those? That initial year? What did that look like?

**Peter Zaitsev:** 
Well, so for me, I think it was very interesting, I think we had this story, right off two geeky dudes go and try to start a startup company. And in general, I think there were a lot of people a lot of kind of filled from what I later held right from MySQL management team and other people in the industry saying, well, let them kind of play as many geeks, we don't really understand what it goes into there. Ryan, the company always kind of a hairy stuff, selling things and collecting money from a customer, so maybe it kind of flake out for a couple of years. Right? Or, and then go take a job. Right? I think that it was a lot of a reaction, what I heard, and to me, it was kind of interesting, right? Because if you think about Percona origin story to how we do business, it is 15 years of proven overseas people, which said that Percona could never ever possibly work wrong. Right now, of course, 15 years, right, then hundreds of staff members later, right? There are less people who can say credibly, right, what, what they're doing is impossible, right? But there were a lot more of those folks at that time, right. And how we started the company, if you will, right? Our idea was really to see how we can really do things with focus on the customer and a customer, customer needs. As I mentioned, in MySQL, I thought what a lot of a consultant professional services, right, were really often seen as kind of glorified salespeople, who have their big allegiance and pushing you product, right, and then maybe on the secondary solving the customer problems. And from MySQL standpoint, I found that is actually very common in the industry, right? My SQL in that case was the norm. What we are trying to do is say, Hey what we are really going to do is act as I know, as a lawyer required to act by law, right? This kind of put your needs aside and really the sort of fiduciary, right for the customer where we're working. And that was, really, I think, the main value we focused on when we started a company. 

**Vadim Tkachenko:**  
We initially started as consulting companies that we we found that customers are more likely to interesting customers were found in us, I think first Well, now frankly, I don't remember but let's say 2-3-4 years, we didn't have actually sales team on staff. Customers were coming to us and I think he can even build a queue for us to come to them. That's in the again, if you look in Percona, there's a little series we have water Percona stands for that originates from performance consulting. So initially, our roots were as a consultant where they would come to customers, fix problems, and help them to get a better experience is MySQL.

**Peter Zaitsev:** 
And I think what is interesting is even more with that, right? Initially at the corner, we were really telling folks Hey, you know what you should not buy support, instead we at Percona would offer you emergency consulting. And then at some little premium, you could call us, essentially 24 by seven and get your problem solved, and especially the startup companies, they found that to be immensely attractive. And I think for us, it's also kind of very interesting, right? Because you can really be a hero, remember you somebody's website being down, they call you, right, and you just wake up in the middle of the night, you log into somebody's servers, and boom two hours later, right? Or 15 minutes later, wherever it is, they're up and running again, and we are so happy you say there, have a bake, and you feel yourself as a hero, right? There is a lot I would say, like adrenaline in that business, which I think for some folks is really exciting, right. Especially at certain stages in life.

**Matt Yonkovit:**   
Yeah, I mean, I think that I remember back in those days, because I started pretty early, I think I was here before we actually had sales as well. And we had to do a lot of our own selling, right, like somebody would call and you'd have to get into the credit card page to put in the credit card or you would have to do different things. So it was definitely a small company, and that small company mentality early on but you're right, it was a lot of people who just came word of mouth and that was a very disruptive model, but it was really a very, very similar model to pay what you need right? It's that consumption based model that currently exists in the cloud for performance tuning and help.

**Peter Zaitsev:** 
Finish up so even in addition not having a sales team or not having a marketing team we didn't have our website for a long while right so if you did for first quarter while we just had MySQL performance blog, and we made this link redo MySQL consultant and put it in red and that actually was you know good enough for us to to get more of work event the event you ever need.

**Vadim Tkachenko:** 
Well maybe you can look it up again, we should probably have prepared it, but maybe you can look up our first you know design of a MySQL performance blog. 

**Matt Yonkovit:**   
Yeah, yes. Yeah. And I mean I think that's something that's interesting when you look back there you know, you'd say like it is you know, definitely different than what the expectations are today right? You know, you've got you know, something that is very different it looks different it's not even close to the same thing it's very very here and I just pulled it up and let me go ahead and I will share my screen we'll just do this live because that's what we how we roll and look at this here it is in all of its glory. Let us present Percona 1.0. Yeah, so so this is what the company was built on over the years and you know you can you can go back and you can see that even like into let's say 2008 Let's see is is loading hey look 2008 it's here but now we've got Call now for emergency, we got a button up at the top so and we do MySQL consulting. 

**Peter Zaitsev:** 
That's insane.

**Matt Yonkovit:**  
Yep, that actually went to the percona.com services page show so this was actually after looking at that doesn't even load right because it is that old but yes so there you go that is the initial website back in the day when you look at that you see this this website you two both had to spend a lot of time doing the consulting yourself. This was not like you didn't have a team of consultants. This was you both just going out and doing work.

**Peter Zaitsev:**  
Well, that's right. I would even say this kind of this right. So one of the reasons why I approached Vadim, about starting a company together is because Vadim is really, really smart. And he can also do like, about anything, he can figure things out. So in the early days of your corner, it would be me doing my talk and talk and talk. And then I would turn to it and say, my team I just promise this thing, right? And he will just figure it out, and do it. And at that point, I think, Vadim’s English was not so great, right? So that's kind of worked, I think very well for for both of us.

**Matt Yonkovit:** 
But you went, and you did a lot of work for a lot of big companies. Maybe you don't have to tell us names. But there's got to be one or two stories that it's like, this was a weird thing. This was just a, it was an unusual situation, or it's something that really kind of stands out from those first couple years.

**Peter Zaitsev:**
Okay, Vadim, do you remember something?

**Vadim Tkachenko:** 
Now I'm trying to recall weird thing.

**Peter Zaitsev:**
I'll tell you something. So I go to wine, winery companies. Right. And we have a conversation about MySQL performance. Right? And they say, Well, you know what, we actually figured out how to make sure of it in MySQL to make it run fast. In a way, let's say, at least our developers understand that. We have just three basic rules and say, oh, wow, that is explained interest in three basic rules, what are they? And they tell me it is no joints, no joints, no joints. That was a very unused figure in this case. That is really before technologies like MongoDB really became popular, right? And they found out using MySQL basically as a sort of glorified key value store right? A little bit more than that it gives you have a very uniform performance profile, but of course, you lose.

**Matt Yonkovit:**
Well, if you're gonna do that, you might as well use InnoDB. And then you'll get a great performance, right?

**Peter Zaitsev:**
Yeah, that's what that was an interesting one. So Vadim, do you remember something?

**Vadim Tkachenko:** 
No nothing that comes to my mind.

**Matt Yonkovit:**
We're so boring, Vadim. You just don't even remember any of them. 

**Vadim Tkachenko:** 
Yeah, like I was there to say it, I just said I was seeking hours and hours fixing customers' problems. And Peter was talking to customers. 

**Peter Zaitsev:** 
I think there are a bunch of interesting things in data recovery.

**Matt Yonkovit:**
Oh, don't bring up data recovery. That's such a painful memory.

**Peter Zaitsev:** 
Yeah, it's very painful. But it is, I would be very interested to see what kind of misconceptions people have about why we justify not having the proper backups, right? 

**Vadim Tkachenko:**  
Yeah, I remember a story about data recovery.

**Peter Zaitsev:**  
Okay, what do you remember? Okay, go for it.

**Vadim Tkachenko:**  
I go for it. Okay, so I worked with the customers. And at that time, they had four terabyte of data, at that time as it was huge for terabyte of data in MySQL. And every so often, they deleted the data they needed. And yeah, we had to go and somehow recovery, MySQL, bring an instance, back to life, and every time I spoke with them I needed to have backup. And they will, they were like, Whoa, but it's four terabyte we cannot afford. It's very expensive. We cannot afford another four terabyte to copy. To have another copy of four terabyte, we can live only with one copy of four terabytes of data. Yeah, I think eventually they went out of business. 

**Peter Zaitsev:**  
If it's cheaper not to have a backup, then you're probably not pricing your data recovery correctly.

**Matt Yonkovit:**
Wow. Yeah. And I mean, those is always great to hear those technical war stories. But coming from the technical world, both of you, I'm sure that starting the business early on, when it was just a couple of you was straightforward, but as time went on, then all of a sudden you have to get involved in stuff that you don't really Don't have the background in right, like So you mentioned sales, you mentioned marketing, you mentioned like these different areas all of a sudden as Percona grows as a company, as a technical co-founder, both of you, what were some of those surprising things that you're like, this just doesn't make sense? 

**Peter Zaitsev:**  
Well, let me start with the finest store. Right? And, like, a lot of people know, right, I do not like the bureaucracy, and I consider a lot of things bureaucracy. So one of the things you need, when you want to sell stuff, right, is your customers expect some sort of contract. I actually went to Jeremy Cole, who ran another consulting company, Proven Scaling, at the time, and asked him Hey, Jeremy, would you mind sharing your contract, so I don't have to write one. So he graciously shared one with me. And I just replaced Proven Scaling with Perconar, right, and also because the company, the first Percona company was incorporated in London, right, there's another long story Why? I will just replace that with laws of the United Kingdom, instead of the state of Delaware. And everybody was fine, until I went to sign a contract with was like a BBC or some big corporation. And their lawyer responds to me and say, Well in your contract, you say, through his law of the United Kingdom, but you don't have laws in the United Kingdom, we have laws, or either English laws and Scottish laws are different. So which one do you prefer? I said, Oh, that is so freakishly lame, right? In this case, probably. But yeah, well, in the end, they probably accepted us as a people who may not really understand much of the law, but can be good in getting the technical stuff done.

**Matt Yonkovit:**  
So over the years, I'm sure that there have been a lot of those. But you know, as you hear other people who are people who are starting businesses, maybe they're starting open source projects that they want to turn into a business. What are those early days suggestions for you that you would give them like, what advice would you provide? Like, what would you say to them? You know, hey, you're starting off, make sure you do these three things, or that you try to focus here, what would be your advice?

**Peter Zaitsev:**   
Well, I think, for Percona, we have to understand that tremendous amount of luck we had at that time, right? Because as you mentioned, MySQL was growing very rapidly. We also actually started at the time with the MySQL AB which would be like a primary vendor was doing a lot of stupid things. It was kind of ranging from not making InnoDB as good as it was to for example, they would start to require to have a support contract in order to get consultant so if you don't want support contract what want to get consultant, then you go to companies like Percona and you're welcome before with hands, right, then you had the lock of MySQL being acquired by Sun and Sun acquired by Oracle, which had a lot of those while this kind of digestion process completed, there was a lot of stuff, right, which really allowed the corner to grow. Very successful, right. So what I wanted in this case is kind of like, right product - right time, in this case was very important for us. 

**Vadim Tkachenko:**  
And I think we never should  remember MySQL as a product and the source code was already popular at the time. It was crazy proper. If to start totally from scratch. I think that's a very hard offering. And well, most of you probably will need to work to make your project, product popular first, and adoption is the name of the game here. And after that, after you get users, you can look how you can programme a business on that.

**Peter Zaitsev:**  
Yeah, and I think just to add to what Vadim is saying, if you think about Percona, we have a unique experience and unique business, right? Because we have not tried to start some database technology from the ground up, right, we started by making MySQL better, and then continue to make MongoDB better. And now Postgres better, right, but we do stand on the shoulders of giants, or there is an existing community, right? And really, serving that community's needs was very important for us to get Percona on the map, right? And we get a lot of business through word of mouth, right? As I think you already mentioned.

**Matt Yonkovit:**   
Well, you mentioned Mongo and Postgres, so let's go there for a second at some point . Your node in the MySQL space, you've got this great reputation for fixing MySQL, and then all of a sudden, let's do Mongo. Talk to us about that, like tell us about that experience and the reasons?

**Peter Zaitsev:** 
Well, if you look from a high level of personal kind of, high level kind of point of view, if we were to really help customers what those customers need. And if you look at the time, there was a new generation of developers coming up, which wanted something simpler than relational SQL databases. For them things like MySQL, and Postgres, were too complicated way exactly wanted that if no joints, no joints, no joints, right? And also something which could scale relatively, relatively easy, right? If out the manual, sharding, right, and so on, and so forth. Right. And MongoDB was a technology, which fits that pretty well. It was also actively marketed to the MySQL community, right? So we thought we would have some customers, which would kind of be crossovers, right for MySQL, and MongoDB. So that's how we solve both business opportunities as well, from us really to expand our toolbox to to be helping customers.

**Matt Yonkovit:**  
Okay, so as you expand the toolbox, and as you started to grow, what sort of challenges did you see kind of pop up and happened? What was something that was unexpected to you that you thought this would be an easier road than it was? I mean, like, what, what did that look like?

**Peter Zaitsev:** 
Well, yes, I mean, I think of what, really, we kind of thought maybe about my MongoDB ecosystem as similar to MySQL ecosystem. Right? And it was, it was very different in the end, I think what is interesting about MySQL, and kind of ranging from maybe from an early stage, to croods is MySQL was always empowering the community, but not really trying to control it too much. Right. There were, for example, a lot of MySQL independent meetups. MySQL conference was always something where a lot of companies were involved, right? You would see even kind of a lot of free spirited discussion inside the company and company meeting right then you may also work from icicle IV, you remember how somebody could say, to our CEO, that is kind of the stupidest thing I've ever heard still keep a job. MongoDB I think it was always watched, they have a good reference to that I held as a reluctant open source company, right. And you can see that even as event to IPO, they, for example, do not talk so much about the open source, but saying well, we use this kind of a freemium model, and it's called Open Source, right, but actually we are proprietary software company as, as any others right or the claims by MongoDB CEO, we say well we didn't really open source MongoDB to get help right and co-created with our community. No, we just open source, right because that's how you get more users, right? There were also a lot of changes in the community aspect, like for example, all the majority of MongoDB user groups have been MongoDB controlled, right? And they would not allow us to participate or monitor your conference. Well, Percona is not welcome, because we just wanted to have a very clear message, right? Even though there have been some third party, let's say MongoDB focus newsletter, very good sponsored ones, but then hear from him and say, Well what? Our biggest sponsor is MongoDB. And they stalled. What if they ever let you sponsor his newsletter? Well, pool the sponsorship. So MongoDB would use a lot of ads, kind of a very heavy handed anti competitive approaches, right. I think MongoDB is more Oracle than Oracle, right? I mean, in terms of using that scatter of heavyweight techniques, not just that it was also very interesting. From what I know, the MongoDB would have a heavy anti-compete in employment agreements, and from what I heard, they will pursue that aggressively. So there are people who leave MySQL AB, right, often would stay in, in MySQL ecosystem, right? And work in a variety of roles in the MongoDB case, very often would go and work on entirely something else just not to deal with the thought, right? Which has been a restriction hires, right, so that it has been a lot of fair, I would say heavy rains in MondoDB areas.

**Vadim Tkachenko:**    
And not to forget the biggest elephant we have - this licence change, I think MongoDB started is a big way of licence, open source lands licencing games, namely to change your licence

**Peter Zaitsev:** 
That's right, that that was not at the time of early Mongo development. But yes, I mean, I think we have very finding ourselves in kind of an interest because we are about real open source but yet we have a product which had to change your licence to SSPL which is not open source licence which is a richer source available and frankly, if you would make that decision right now we would not have going to MongoDB but now we have the many hundreds and 1000s of people in customers and community who rely on Percona products for MongoDB and Percona commercial services for MongoDB. So despite MongoDB ditching the open source world, we are continuing with our having MongoDB now portfolio.

**Matt Yonkovit:**    
Okay, so you look back over 15 years, it's a long time. Certainly there have been people who have influenced you and had you know, a great influence on percona success whether they're people we've hired or people who you've just met in the community so when you look back at 15 years maybe give us some names tell us who has really like maybe inspired you or helped establish what we are today you know, what what are those hidden contributions that people might not be aware of?

**Peter Zaitsev:** 
Do you want to name some names, Vadim?

**Vadim Tkachenko:**  
Well I think we absolutely should mention really just say Baron Swords, Baron I think help us a lot more Percona and Percona name and also we use tools developed originally by Baron and it was market now now it's named Percona toolkit, it so I think you're absolutely further recognised about him towards. Baron was a primary driver at MySQL performance.

**Peter Zaitsev:**
Yeah, I mean, if you like from my standpoint, right, like one thing I want to recognise there are Michael Widenius at the MySQL founder right who was a big inspiration, kind of and mentor for me, I think we are kind of a little bit on the different sides of sort of like the competing companies right now. He is great. Another on the business side, I would mention Paul Vale, that is the CEO of Vision. And I was very impressed how open he was, in this case, like, I remember, well, when Percona started, he actually tried to hire me to run MySQL, sort of like our open source database.In beef, and various Hey, I just go to do myself, right. And then He always was very much sharing his business techniques, and so on, so forth, even if you can beat it sometimes, right? I remember on one of Percona, maybe like a MySQL user conference, we'll sit down, he will just open up his accounting system. And he showed his kind of revenue expenses, right, and how it was strange. And I was like, Wow, that is a you know, something. Something amazing, right? And I remember he was telling me things like, Well what, like, we're vault is big, if you think about Percona, and PC, and we don't really compete with each other too much. Like, we mostly compete with bigger consulting companies, right, or MySQL, Oracle, wherever, right? And I think that taught me a lot about like, especially if you speak about like, different smaller organisations, it's much better for you probably don't compete that much, right, you should really see how we can work together. And I think what I liked from him, which was kind of very inspirational for me saying, Well, you know what, in the end, I like to see the business as a game, right? Let's say if he would play soccer together, right? Like, I will try to beat you on the field. Very hard. But as we kind of end the game, we can all go, yeah, go play beers together, right, and maybe even give each other some advice about how to play the game better. Right. So I think that it was a lot of business inspiration towards openness and supporting our players and ecosystem, right, even if that kind of competes with you.

**Vadim Tkachenko:**  
Well, Peter mentioned the business side, I probably would like to mention on the technical side, and probably not many will recognise his name, but I think his contribution is that's exactly what started Percona Server and what exactly who put her Percona Server for MySQL on performance map. And this is originally where purchase and the engineer is, yes, before we can afford that. Fortunately, he is not very active in the community. And again, probably only very few people will recognise his name, but the time he factors will definitely be caught. And we worked with him on how to incorporate cutting that code into Percona Server. And that's in my opinion, water kick started all our software efforts in Percona and originated Percona Server, therefore, oh, for MySQL.

**Peter Zaitsev:** 
Well, let's Yeah, let me add some other technical name. Here, I think which is good. It's the origin of both technical and business is Mark Calgon. Right. I think he was very helpful for us, both from origin. virus corner. So software, right, as well as kind of giving us some business advice here and where, and I remember then Mark was with Facebook, he would have done like a keynote for Oracle, right? And he say, oh, tell me Well, you know what, I dropped the P word. Meaning what he would mention, I mentioned Percona in his in his keynote, right, which was not really something what folks like Oracle probably want to mention a keynote. 

**Matt Yonkovit:**    
And you mentioned Yasumi. I remember Yasumi quite well, because when we would go to Percona meetings, he would be the one who didn't go with us to community events or do like team building because he'll be in his room coding, right? Like you'd be just like, he was just the smartest dude, right? He was just so smart. And you know, I think Mark has also a great one to call out. I mean, there's 1000s of other contributors or people who have contributed to Percona. 

**Vadim Tkachenko:**  
Absolutely. Yeah. I was catered to someone to feel left out. But yeah, a lot of people contributed to success.

**Peter Zaitsev:**
And let me mention one more person who I think is an internal in this case, right? This is Tom Basil. Tom Basil is a person who was my boss at MySQL, right? In this case, he was a pretty organised person I knew, right, who can help to rain a little bit more cows. And I remember one of the meetings,  I went to the MySQL developers meeting, or was invited. We kept kind of open at that time, and tTom was out there. And I think I was kind of joking and say, well, Tom, MySQL gig doesn't work out. Why don't you come and join us? Right? You know, it's like, you often invite people to come and visit your house, which you know, and never go into, to make it out there. And then things changed to like, who bought I think for Tom, and then for, for Percona, and a year later, he was asking say, well, Peter, remember, you mentioned me, you may have a job for me. Right? We're into joking. And I told him no, no, no, of course not. Even if I totally was. Right, and that's how we hired Tom Basil, he was CEO at Percona and variety of other other roles, right. And I think especially in the early Percona days, he was really fundamental and kind of getting more of that administrative stuff figured out.

**Matt Yonkovit:**  
I love how you say administrative stuff, it's kind of like, Ooh, it's kind of like you got gum on your hand or in your shoe. And you're, I don't I don't want to do any of that stuff.

**Peter Zaitsev:** 
Yeah, I totally don't want it right. Well, I mean, Tom also remembers, like, I remember, and he would get back to him for so many years. I remember on one of those first meetings, and he was probably one of the only non-engineers left. And I'm saying, hey, my dear engineers, and here I welcome Tom Basil, the useless overhead. And he was like, ah, Peter, how can you call me this way? Yes. I say no, no. Just a while here.

**Matt Yonkovit:**   
Yeah. So let's leave it with this. This is my last question to both of you. Where does the next 15 years lead Percona and the industry? And videos you're gonna throw up? I see that.

**Vadim Tkachenko:**  
Yeah, that's you're finishing the bizarrely boring question. Okay. Can you can answer?

**Peter Zaitsev:** 
Yes. Welllet's just steal the quote from somebody what, it's hard to make predictions, especially about the future. But anyway, right. Yeah. So I mean, if you if you look in this case, well, I think one of the things that you may be getting on, I think it is very interesting question right now, right, that integration, look kind of situation if open source in the cloud, and some of that kind ofI don't know what to call that. But a lot of open source companies are now ditching truly open source licenses if something not so open source of protective, protected turf, if you will, right. I mean, besides MongoDB, we have Elastic and Radius and a number of others do that, right? I mean, in, in my opinion, it is hard to predict how the market will split between that proprietary software, it's kind of source available and through open source, but I believe there is a lot of room and there's going to be a great market for through all open source database and that is what corner is really placing our bets on and what we want to do is to push the boundaries of open source databases. Would we make more money if he would instead do kind of commercial databases? I don't know but I cannot hold here right because there are many ways to make good money like people trafficking in the drug trade, right? Which I also do not want to go into.

**Matt Yonkovit:**  
Well, we'll leave it on not going into the drug trafficking or people trading because that is just Yes, yes. We are always happy to end on that note. Okay. But no thank you both for stopping by chatting with us and sharing some stories. We hope that you enjoyed letting people know about a little bit about the history of Percona here. 

Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.




