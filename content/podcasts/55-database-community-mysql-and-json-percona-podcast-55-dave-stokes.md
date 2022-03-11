---
title: "All About Database Community, MySQL, and JSON - Percona Podcast 55 /w Dave Stokes, Technology Evangelist at Percona"
description: "Dave Stokes joined Percona as Technology Evangelist last February and he sat down with the HOSS Matt Yonkovit to talk more about his background, his interaction with open source database communities, his early days, and his choice of MySQL Community"
short_text: "This episode is a passionate talk about database technologies between The Head Of Open Source Strategy at Percona, Matt Yonkovit, and the Technology Evangelist at Percona Dave Stokes. Dave joined Percona last February and he is welcome to the podcast as well. Listen about Dave’s background, his interaction with open source database communities, his early days, and his choice of MySQL Community. They tackle also the difference between MySQL Community and Postgres Community, the recent change and evolution in the database space with more and more explosive data, before plunging into the future of the technology space, particularly the JSON datatype"
date: "2022-03-11"
podbean_link: "https://percona.podbean.com/e/database-community-mysql-and-json-percona-podcast-55-w-dave-stokes-technology-evangelist-at-percona/"
youtube_id: "saIfiuv0C9k"
speakers:
  - dave_stokes

---

## Transcript

**Matt Yonkovit:**  
Hello, everybody, welcome to another HOSS Talks FOSS. I am the HOSS Matt Yonkovit, Head of Open Source Strategy at Percona. And today we are joined with one of Percona's newest employees, Dave Stokes. Dave, welcome to Percona.

**Dave Stokes:**  
Well, thank you. I enjoyed being here.

**Matt Yonkovit:**  
Yes. So if you are in the MySQL community, you probably know, Dave, from the many years, that he has spent giving us all kinds of interesting, cool conference talks, blog posts. He's been a super active member of the community for years and years. In fact, many of us at Percona has worked with Dave previously when he worked at MySQL, or at Oracle. And when I hired Dave, I got a lot of pings and said, Oh, my God, Dave's joining us. Now, I don't know, maybe that was a good thing or a bad thing I tried to clarify, and most people thought it was positive. So you're in the clear there, but what somebody has, oh, my god, Dave's joining us. Right?

**Dave Stokes:**  
Hopefully, it's all for the positive. 

**Matt Yonkovit:**  
Yes, it was all positive. So Dave is joining us, to help us in the community team to help us on the Dev Rel side, and the evangelism side, continuing the work that he's been doing in the MySQL space for all these years, and I figured it would be good to do an introduction, and let people out in the community who watched the podcast who follow us on YouTube, or on Twitch or wherever we're streaming to get an introduction to Dave, learn a little about him and hear about some of his experiences. So Dave, why don't you introduce yourself to our vast audience. And by the way, I don't know if you knew this. But we actually achieve number one status in Tunisia for this podcast, for our demographic. So open-source database, technical content in Tunisia. We're like the top podcast

**Dave Stokes:**  
 Glad to hear that will drive my Q rating, which will make me even more. 

**Matt Yonkovit:**  
Yes, yes. Thank you, to those in Tunisia tuning in. 

**Dave Stokes:**  
Yes. Let's see the background. Many years ago, I was working at a university on the West Coast, the University of San Diego. And the vendor that we chose for our hardware kept killing off the operating systems that we use, Russ just he tops 10, tops 20. And I got the ability to load up one of our machines where they version of Unix. And from then on I am really thinking this is really neat. People are contributed, contributing all over the world, to this operating system to add features. And a little while later, you hear about this crazy guy from Finland. Somehow the opposite such world was always a crazy guy in Finland, to create this operating system that he was giving away. Many years ago, you used to have to buy your operating system from the vendor that made your hardware, and you couldn't take that software to someone else's hardware. 

**Matt Yonkovit:**  
Yeah, it was expensive too! Like any like when you were talking Unix. It was like $100,000. 

**Dave Stokes:**  
Well, it's like a university. We only had to pay $300 to Berkeley to get the 1600 VPI. Magnetic reel tape. Oh, and oh, yeah, we yeah, we were hot stuff. Anyway, many years later, I'm at the American Heart Association, I was putting them on the internet. And we had a need for a database. And at the time, in the open-source world, there was one called MSQL. And it's sort of word really wasn't free. And yet another crazy guy from Finland says we have this thing called MySQL, it's got to be a better product that has an extra letter in the name. And ever since then, I've been using MySQL. About the same time, I discovered PHP, so thanks to Rasmus Lerdorf, as pretty much been the core of my career ever since. And in 2007, I was expanding my horizons by taking the MySQL server certification for DBA 5.0. And back then it was two tests to get the certification. And I failed the second test by one question, and a lot of the questions were kind of poorly worded. And at the same time, I saw a notice on forums for MySQL that they were looking for a PHP developer. If you're well, let me see what's going on. So I wrote a letter that was half complain about, hey, some of your questions really need to be tightened up a little bit. And the half, hey, this is why you need to hire me. And surprise, surprise, I had been hired by MySQL AB. And that that was a little bit of a shock. I mean, this was a very small company, global reach people all over the place. And a very exciting customer base. That's the thing that really gets me going about MySQL. And the same thing I've seen in the Postgres and Mongo communities out there. And what I see growing with, like proxy SQL and some other tools out there is that the community is always doing something different. Used to be you go to a conference, you hear something in the hallway track that would instantly make you go down the rabbit hole with some other new approach to doing stuff. And there's always innovation, there's always creativity. And there's always something new happening. It's not static, a lot of the software bases out there, I won't name them for various reasons. You go back after six months, and see Oh, what have they done? Have they changed anything? Nope, still arguing the same things. No one's really done anything. But the Glasgow community and the open-source database community are generally very vibrant. What's really interesting is, especially in the open-source database world, when I talk to the folks from Postgres, a few folks have gone through Mongo, we're a lot more alike than we are different. And the approaches change a little bit. But they're all kind of how do we make things better? How do we make the product better? How do we make it more accessible? How do we make it more redundant? How do we make it safer? And it's a very interesting niche to be in. 

**Matt Yonkovit:**  
Yeah. And Dave, so we joined MySQL AB the same year? I don't know if you knew that. In 2007, which was, what two years before the Oracle purchase? 

**Dave Stokes:**  
Yes, right. And for those of you who were not there, we were told by Mårten Mickos, you have to be in the room in conference room at 7:55 precisely. And everyone's going, cheap Martin's ever been a stickler for a time before, what's going on. And they handed out shots of vodka, which, for me, was a little bit of a shock.

**Matt Yonkovit:**  
Yeah! At 8:00 AM in the morning. For everyone, at MySQL AB, to announce that Sun had acquired MySQL. 

**Dave Stokes:**  
And then a year and a quarter later, I'm at the MySQL users, group meeting, or user show. And I turn on channel two news in Boston, in San Francisco, known as the Silicon Valley, Oracle has bought Sun Microsystems. And I started texting some of my co-workers who are saying you really were drinking that much last night where you're getting disrupted turn on the news, turn on the news. So. So that was kind of exciting. 

**Matt Yonkovit:**  
I was actually in. We had shared rooms as part of the professional service team, right. So we had a double room, and I was with each ago. And I remember getting up at like five, or six or whatever. And, like, I saw that and I'm like, Oh, my God and he was kind of half-awake what are you complaining about? Like, ah, we just got bought? Like, by who? It's like Oracle. And he's like, What?

**Dave Stokes:**  
The whole MySQL Professional Services Group was quite an impressive group. Yeah, I got to know Brian. I got to know Brian fairly well. Is it this is one of those guys. You'd ask him any of your questions about MySQL, it not only gives you an A-plus answer but tells you how to work around any issues. And Josh Chalmers used to run the group was very formidable. If you ever were in a discussion with him, you always I would say felt intimidated, but you could tell that he was always negotiating from a point of strength. And you guys would work four days a week and then spend the fifth day writing up the customer review Action List of what was going on? 

**Matt Yonkovit:**  
Oh, not as much as you would think, that might not have been the goal. But a lot of times, it was five days, and then you just kind of wrote it on your own. So it was kind of a back and forth that depended on who you were working with, and like what they wanted, but back then, it was Road Warrior time, right. So I spent 46 weeks out of the year on the road. Being dropped into a new customer every week, or sometimes two customers a week. And you would go in and get MySQL, you would tune some Linux stuff, you do and some Apache stuff you kind of do everything to get whatever that particular customer wanted. I mean, you're talking about a who's who of Silicon Valley at the time? It was quite, an intense position, because you just, you were doing so much so quickly. Right? It was, it was amazing how much you turn things over and how quickly you did. And it's great to see so many people move on from that team, and from the early days of MySQL into greater things, right. You've got Yoshinori, for instance, over at Facebook spent a ton of time building out there, Rocks dB, you've got Monte Taylor, who was very active in the OpenStack community and Drizzle, and is now at Oracle. Right. And he's kind of going through the paces. But he was one of the top contributors for OpenStack for years. Brian Akerobviouslyfrom an overall perspective has moved on and done a ton of other things with HP and other companies. So there are a lot of really awesome technical people who went on to achieve a lot of great things post MySQL AB, which is, is often cool to see. And I know there are hundreds of others. And I didn't mention you snap, because I didn't like there's so many, right, I mean, that there just is. And you see that kind of tree, if you will, right, where people have come out and accomplished so much. So, I think those early days always have a special place in my heart, at least. And kind of introduced me to that open-source philosophy and lifestyle. So I always had that special place. 

**Dave Stokes:**  
The other thing that impressed me when I first joined as I was taking one of the MySQL classes, I think, was the DBA class just to kind of get a feel for it. And Sarah Brunel was teaching it. And what was interesting is she had her notes up, she had a chat line going, she had three other ways of communication. So she was talking to the software engineers who were writing the code when she had questions, to talk to other instructors. Should you talk to the various program managers? And if someone had a really out of the ballpark question, she could very quick answer, which I thought, wow, these folks really, really support each other.

**Matt Yonkovit:**  
Yeah. Well as you mentioned, Sarah, and she's gone on to have a heck of a career leading organizations around support and customer success and worked at a plethora of companies that have gone to unicorn status. And I remember she was one of the trainers who are in Tobias when I started in the first week, you always had to go through training. And it was even I in training the same week before we actually officially started. And that was my first introduction to a few of the MySQL folks. But no, I mean, it was great. Great times back then. And like I said, so many great people. Now, Dave, you continued your MySQL journey with Oracle for many, many years. And what I'm really curious about is being part of this community, why has the MySQL community for you just been your home and a place that you just you love, like, what has led to that kind of like, you haven't wanted to leave the MySQL community, you wanted to just continue to thrive and excel in that space? What attracts you to that? 

**Dave Stokes:**  
Well, as I mentioned earlier, it's innovation. You see new stuff going on all the time. Also, it's very interesting. You see a small business that claws its way into existence, and they start running MySQL backing up for WordPress or something like that. And you see them start to grow and evolve and develop. And it's a very nice incubation tool to see someone go from zero to a trillion fairly quickly. And also, the people in the community are just fantastic. Used to be when I went to trade shows, even when I ran to someone who was upset with MySQL. They're still using MySQL And it's one of those things where it's just a great starting point for so many businesses, and there's so much you can do with it. Now, I've heard you talk about you need to make sure you architect things, right. And even when people don't do that, you still get fairly decent performance out of it. Now, in the Postgres world, which I love, there's, I would say, there's a lot more rigor to developing things, but they, the community there is as dynamic, probably. Looking for a good term, it's a similar field, vein, and I need to get into that better. I used to go to computer shows when you're at a computer show, they close down this thing, you go out to dinner, you go out to dinner with the other computer geeks, so you end up talking with them. And the passion you see there is the same as you see in MySQL, just I think MySQL is a little more in my focus, because I, I'm dealing with it every day. 

**Matt Yonkovit:**  
Yeah. And, from my experience, from a Postgres perspective, the community is outstanding, they're very welcoming. They are deeply technical. And I think part of the difference between MySQL and the Postgres community is a lot of the folks in the Postgres community are core contributors. In a sense, it is a community-driven project that has many companies that, that contribute whether its crunchy, or EDB, or Percona, or others that provide engineering talent, it's still a collective that is developing the core of Postgres, whereas MySQL, it's, it's an Oracle own company, it was a MySQL owned company. So the majority of the engineering resources were in one company. So that's where I see a big difference, is, it's more of technical collaboration, whereas, in the MySQL community, you have a wide swath of user community, right? So people who are extending, as opposed to really building the core, in my opinion. 

**Dave Stokes:**  
But I also wonder you see, so many open-source projects, we have the benevolent dictator for life. And exactly, the exact opposite of the spectrum is Postgres where everything's very distributed, very non-directive. And it's kind of interesting to see how the two approaches work. And the great thing is both approaches work.

**Matt Yonkovit:**  
Right. Yeah. So and I mean in this is where it's just, it's, it's a slightly different use case, a slightly different area. And there's room for both, and that people always ask, like, MySQL or Postgres. And the answer isn't one or the other. It's both right. And I think that both have their place. And both can do awesome things. And I think it's counterproductive to argue specifically about like, which database is better? It's not like there's going to be a street fight between the two. 

**Dave Stokes:**  
They were it'd be very short-lived.

**Matt Yonkovit:**  
So. But Dave, in like, the last few years we've seen an immense evolution in the database space, both in MySQL, Postgres, and elsewhere. So I'm curious, like, what have you seen in your travels in your community engagement what are some of the things that are kind of popping up over and over again, as you have talked to people out in that user space? What's on the top of their minds? 

**Dave Stokes:**  
Well, 11 and a half years ago, when I started being a community manager, by the way, I was half years, Dave. Yeah. The old promise, we're, I'm a Linux admin, and I got this database, how do I keep it right? And that's kind of shifted to being Hi, I'm a reliability engineer. I've never actually seen my hardware. It's all up in the cloud. How do I keep it running? Right! So the focus has changed from how do I keep this box so I can literally go and progressively hit when it's not behaving what I want to this virtual thing that somewhere somehow and actually has multiple instances, other some house in some places. It's a big shift. The other great thing is that in the old days, your database started running out of disk space. Okay, well, I got to put in a capital request to have my business go out and purchase a disk drive, which means purchasing has got to get involved. The tax compliance people might be involved in all this other stuff, and then you got to schedule your downtime to plug in this disk, reformat it spread things around. Now you want more disk space you call up and hopefully, your credit card has more money on it. The days of having to sweat overdo I do a write-through or write-back cache on my disk drives? No one's arguing that anymore, except for very small groups. The focus has changed away from how to mechanically do things to how do I logically do things? 

**Matt Yonkovit:**  
Hmm. Yeah, no, and I mean, it's a good point and you mentioned SRE, who now it's an SRE who has to deal with the database once in a while, I think it's also the developers who have to write so it's more and more, I trusted that hey, this, the cloud service is going to take care of the database. For me, they're my quote, unquote, DBA, without realizing that there's a lot more activity that has to happen. So there's definitely a need for smarter tooling smarter AI, maybe, or even like, just that knowledge on how to fix those things quickly, when they do come up in position.

**Dave Stokes:**  
Both are going to be a need for the traditional DBA functions, of tuning queries, making sure the data types match the use, and planning for the growth of the tables. A lot of the old stuff backup, that that's much more easily done. Now, you actually don't have someone running and changing tapes anymore, or, or, or that sort of work. So what's interesting is there used to, 

**Matt Yonkovit:**  
There used to be just a person who would walk through take tapes out and put them in, like containers, and ship them off-site. Right? 

**Dave Stokes:**  
Yeah, no, it's not like the old days when you'd see an old engineer with a pocket protector little punch cards for money, or for food. But it's interesting to see how the focus has changed. Yeah. And the size of the databases has gotten absolutely amazing. I was talking to someone who's got a 15 terabyte test set from their four-petabyte data lake. And that's their test set. 

**Matt Yonkovit:**  
And, yeah, it's a pretty big test, like so. Yeah. But you want to test in realistic scenarios. So I guess.

**Dave Stokes:**  
And not that long ago, we're talking about what we have to run Hadoop to do MapReduce all this to get things down to a small, cooler size, so we can actually process it. That's out the window. 

**Matt Yonkovit:**  
Yeah, it's, it's interesting, because when you talk about the explosive data sizes that have happened we do have more and more data, and you talk about what you mentioned, like data like, and the funny thing is, there are so many disparate sources of data. Now, that's where this data lake concept, we used to call it a data warehouse, right or data Mart's, or operational data store, I mean, there's a bazillion term for something that's been around for, basically forever. But the idea that there's all of this different data and all of these different places, and you want to kind of pull it together, or put it in someplace that you can easily access it, and combine it and do some activities. It's not a new concept, but I think that two things have really changed it. Right. And so I think the first is, we don't want to get rid of anything. Right? like, there is so much out there collecting so much data on all of us. and everyone is scared to death that they might lose some competitive advantage if they get rid of some data or don't store it if it's available. They want to every forever and ever and ever. Right. And I think that that has led to an additional burden on a lot of the systems. When you look at the different database technologies, there's really now a database for almost every potential use case, I saw that there are DB engines lists over 350 different databases that they're tracking. And several of them I have seen in use at one particular customer. You might have customers now for users who have eight to 10 different databases that they're storing data in and they have some need to combine that data or access it in a unified way. 

**Dave Stokes:**  
Well, what's an acquaintance online is a database to expert. There's you've never heard of it. This is back in the early days of PCs. Now, this person's new claim to fame is that they have it running on a PC and there are lawyers involved in a court case where someone had some frozen data from a business deal gone bad, and they're in the middle of litigation now, and they have data that's 20, some odd years old that they have to store and maintain and keep pristine. Considering how quickly we evolve various storage engines and various storage methods, would we be able to actually be able to come back and say, Okay, five years from now, can we come back to March 3, 2022? And have an exact representation of the data because someone's trying to prove something in a court of law? Scary? 

**Matt Yonkovit:**  
That is, right. I mean, I think that the pace of technology makes that increasingly difficult, especially if you're only relying on backups, which means that a lot of people have resorted to just leaving the data live in whatever active system they have currently, even if it does not access that off. 

**Dave Stokes:**  
And by the way, if you've never tried, if you haven't recently tried to buy a five and a quarter inch floppy disk. It's an exercise in futility. 

**Matt Yonkovit:**  
Do they actually sell them? Like I don't? I don't even know. I'm sure that 

**Dave Stokes:**  
I'm sure everything's available on Amazon these days? Sure, yeah. 

**Matt Yonkovit:**  
Well, you're not gonna buy, right, like you're not gonna It's like buying a new VHS player, the last VHS, the company that made VHS players went out of business. So you're gonna buy it in the second-hand market. 

**Dave Stokes:**  
But ironically, somebody's still making Betamax I've been told. So there you go. It's for industrial uses in podcast networks. 

**Matt Yonkovit:**  
But Dave, you're dating us with this technology on the five-and-a-half-hour show. So let's look at the future. 

**Dave Stokes:**  
Future, I think it's kind of interesting, especially when you see things like the JSON data type. It's funny how all the database relational databases were written on the NoSQL databases that were mainly JSON based that hey, you guys are transactional. So is it okay to become transactional? Meanwhile, all relational databases, Oracle, Postgres, MySQL, SQL Server, added a JSON data type. And it's kind of like, well, are they just trying to do a checkbox out there? Because hey, if we have this out there, you kind of weave that over the fish's head. Now, actually, the JSON data type is turned out to be very valuable, because there's so much data being sent out in JSON, it's nice to be able to capture it and store it in that native data type. And the uses of that are really exciting to me because you have the ability to have highly immutable data on top of a fairly rigid relational structure. And that works very well for a lot of folks. And also, a couple of years ago, the JSON schema.org folks came out. And by the way, they'd like to be called brilliant, I did that in a blog post one time, we get a lot of positive feedback for that came up with a way to get rid of the one thing that always made me cringe about JSON was that there was no way to have rigor on your data. If I was storing a JSON document, and I had an email tag, and I was spelling an E, M, Al, all lowercase, and you were doing it with a camel case and someone else was typing electronic mail, there was no way to actually force the data to be what you wanted in the format you wanted, there was this folk worked out a way to by setting up an exemplar that you check the document against before it checks into your data, so you don't get the bad data into the database. And it's easier to keep bad data out than trying to go back and fix bad data. So all these little innovations like that I see are a big step forward for us. 

**Matt Yonkovit:**  
Yeah. And that's interesting because that brings to my two points. Right. So one is one of the benefits that people extol about JSON is flexibility, which is difficult if you're doing schema or JSON validation. Because if it's not validatable, then it is rejected. And therefore, some people's minds are not flexible. So there is some weirdness that goes on with people like, right, because yeah, if you're looking for certain validation within that document. That kind of negates some of that flexibility in some people's minds. 

**Dave Stokes:**  
How many times have you opened up someone's data table, and you've seen Oh, everything's a varchar 255 All 25 columns, and they're storing string data in there, and then somehow he kept it together. 

**Matt Yonkovit:**  
I get it. Right. I'm saying that this is where a lot of people extol the virtues of schemaless or this flexible design without realizing what the implications necessarily are. Now, the other thing that kind of comes to mind is the cyclical nature of technology. Right? We live in we've been around long enough, Dave, where we have seen things kind of repeat. Right? So let's be honest whether it's virtualized versus containers versus or it's sharing resources, like the cloudlike, these things are not concepts that are new, necessarily, it's just that you see the cyclical nature of technology. And what we see is there are patterns. And I can tell you, one of the patterns that come and go is consolidation versus distribution or central control versus distributed control. And what I mean by this and how this relates to databases in general and technology is you will see phases where everything is, we need more, right, we need to expand and choose the best thing for the job, followed by a phase where it's like, things have become too unruly. And we want flexibility. But we want one thing to control the flexibility, followed by something that says one monolithic control plane is stupid, we want the benefits of all these other things. Instead, you have the explosion, and then you have the consolidation. And so this, there's this back and forth between consolidation versus explosive growth of technology sprawl. It's a cyclical thing that happens every few years. But you mentioned back in the Unix days, big iron, right? We want massive boxes, and we want less of them. We want more horsepower in the one, we're going to consolidate as much as possible, nope, we want commodity. we want blade servers, we want multiple technologies that allow us to scale out. And then we go back to, well, yeah, the scale-out was so hard to manage, we're going to come back to a single thing. And then we go back. So I mean, like this, this technology cycle is cyclical. And it's interesting when you mentioned things like the JSON data type because a lot of databases start out. And you can see this pattern where it's, I'm here to solve a specific use case, right MongoDB, document database we're here to store documents in the BSON or JSON like format. This is what we do. Right? We're not worried about transactional workload, we're not worried about this, we're not worried about that. And then at a certain point, they're like, Oh, now we're gonna add two additional. Now we're gonna add this. Now we're gonna add that, and they start to take what was a very specific use case, which means that you would have technology that sprawls right, for every use case you know, you've got a transactional database, you have a document, and as you're documenting it, you have a need for Hadoop type workload, you have that and so you have, like, each type of technology, whereas, now you start to see some of the bigger vendors say, we need to take the features in these other databases and consolidate them into ours. So then they'll just use ours as the single-use case, and everyone can kind of standardize and consolidate. 

**Dave Stokes:**  
80% of folks running databases have more than one type of database in their environment. Yeah, more than that. Yeah. I remember. 

**Matt Yonkovit:**  
Yeah, yeah. And so it, but I think that the vendors in the projects themselves, get a lot of pressure. Because people want to have fewer things that they're responsible for because a lot of them are difficult to manage, right? Like, how do you manage that? Yeah. All these different disparate technologies, how do you get expertise in it? And so there's that pressure of Ooh, we can help them and but there's also pressure in, we can capture more market share. Because when you cornered the market in one particular niche use case, to expand sometimes you need to jump to the adjacent land, right? Generate a bit more revenues if you can have a relational database that all of a sudden does document database type stuff for analytics, it's a jump that you can make these it's one kind of lean over. But expand your use case. So it's an interesting dynamic in the market because I do see that from a Database perspective, more and more databases try to adopt features just to catch up, or just to try and say, Look, you can consolidate and use us for everything.

**Dave Stokes:**  
Now, the consolidation of the cloud, I've heard people argue that we're just kind of going back to kind of a theoretical mainframe environment where there's going to be one box that has all our data, and everyone uses that one box to get all the data out of. And I know mechanically behind the scenes, that's the way it is. But I know a lot of businesses are thinking, Well, I don't have to have a PC on everyone's desk, I just have to have them have a way to access the cloud. And the cloud will act as the equivalent of a mainframe for my data.

**Matt Yonkovit:**  
Yeah, well, I mean, yeah, well, let's, let's, that's a whole another discussion. We talked about like desktops and whatnot, cloud. 

**Dave Stokes:**  
When you're talking to businesses, everyone has one of these. So let's, let's make that our Universal Interface to our data, which was Hertz?

**Matt Yonkovit:**  
Well, it's possible. But I think that this is where you could see decentralized computing, as something that eventually takes over from some of these centralized resources. Right. So right now, you mentioned putting everything in the cloud, and whether that's monolithic or a single point is debatable. But there's a lot of work on decentralized services, especially with Blockchaintype technology. And like when you look at the finance and crypto space, where you're looking at decentralized identity and decentralized services, and decentralized this and that, there's, there's a point where someone will look to figure out how they can utilize that technology to instill or bring kind of a crowdsourcing approach to a lot of the bigger data problems that we have, whereas you might have, instead of having one centralized controlled server, and this is kind of this idea of serverless, right, you have the idea of serverless. Right now in a lot of cloud providers and things where it's like you don't really have a server. But there is really a server behind the scenes, you don't know about it, where but ultimately, what you'd want is to find out the work. And then wherever it is, it handles the work and gives you a result. And right now, the technology that we have is very specific to that particular data center or that particular provider. But it is possible to cross all the rounds and make it truly distributed in the future. Now probably sound like a heretic or something, and people will be like what I'm talking about. But that's what we've gotten to a really weird space here, which I didn't expect. You never know where these conversations will have. But Dave, what, in your opinion, is the most interesting new thing around the MySQL ecosystem that you've seen in the last year or two?

**Dave Stokes:**  
The two things that really made me stop and take a look at them. I'm always reading things like slash.org, the various forums for the various databases, the Reddit forums for the various databases. When you see something like a proxy SQL or Vitess, pop up, and it's not run by the main vendor for the database. And you see the swarm of people who go to it because it's solving a need that they have. And as an industry matures, you tend to have consolidation. And things kind of become gelatinous, and they slow down and become messy. But we see something like proxy SQL that suddenly is on the scene and doing a whole lot of really neat stuff for a whole lot of people. That's one of the things that yeah, there's fresh blood in the environment. That's doing really neat stuff. The other thing that's interesting to me is I'm going out on these forums and looking at all these novices who are coming into the database world. And they haven't had formal schooling and relational theory sets, Boolean logic of that, but they're going out there and they're using databases to do what they need. And the changes from when I started or, or even a couple of years ago to the ability to have these folks be able to go from zero to 60 miles an hour. It's got a lot better. Still not where I think it should be. But these people are able to get in their use of technology and do pretty amazing stuff fairly quickly. 

**Matt Yonkovit:**  
Yeah, definitely. Well, Dave, welcome to Percona. We appreciate you coming and hanging out with us. you're going to be seeing Dave over the next few months here, start popping up on live stream, start doing some videos, you're gonna see his name on the Percona blog. We're gonna put Dave's name in lights. Dave's gonna become Percona famous. That's the goal. Percona famous Dave. So, thanks for hanging out this morning. And if you want to reach out to Dave feel free to drop him a line at david.stokes@percona.com Or follow him on his own personal blog or on the Twitterverse. Wherever Dave is, you will see him!

**Dave Stokes:**  
I hope to see you on Percona Live. 

**Matt Yonkovit:**  
Yes. See, look, he's already making you know, good on his promise to help us out by plugging Percona Live!

**Dave Stokes:**  
The call for paper is open. It's in Austin. And if you have any questions about Austin, I live a couple of hours north of there, but I can tell you all the good places to eat, and some other amazing adventures you have in the nearby area. So submit that paper today.

**Matt Yonkovit:**  
Okay. Soso Dave's gonna be your host down in Austin. So come on down. All right. Bye, everybody.

**Dave Stokes**
Adios amigos
