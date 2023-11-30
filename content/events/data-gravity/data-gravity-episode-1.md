---
title: "Data Gravity Episode 1 - Charles Thompson - Dolphie, a Real-Time MySQL Monitoring Assistant"
description: "Joe Brockmeier talks to Charles Thompson, creator of Dolphie - a real-time MySQL monitoring assistant that's open source and available for multiple platforms."
images:
  - events/data-gravity/Data-Gravity-Episode-1.jpg
draft: false
date: "2023-11-14"
speakers:
  - charles_thompson
  - joe_brockmeier
tags: ['Data Gravity', 'Podcast']
---

In this [episode](https://datagravity.podbean.com/e/data-gravity-episode-1/), Joe Brockmeier talks to Charles Thompson, creator of Dolphie - a real-time MySQL monitoring assistant that's open source and available for multiple platforms. He talks about creating Dolphie, how it fits into the MySQL monitoring space, and more.

[Episode 1 Link](https://datagravity.podbean.com/e/data-gravity-episode-1/)

<iframe title="Data Gravity Episode 1" allowtransparency="true" height="300" width="100%" style="border: none; min-width: min(100%, 430px);height:300px;" scrolling="no" data-name="pb-iframe-player" src="https://www.podbean.com/player-v2/?i=jhft7-14ba058-pb&from=pb6admin&pbad=0&square=1&share=1&download=1&rtl=0&fonts=Arial&skin=1&font-color=auto&logo_link=episode_page&btn-skin=7&size=300" loading="lazy" allowfullscreen=""></iframe>


[All Data Gravity Podcast Episodes](/events/data-gravity/)

**Joe Brockmeier:**  
Good afternoon. Good evening. Good morning, whatever time it happens to be for you. My name is Joe Brockmeier, the head of community at Percona. And this is the inaugural episode of our podcast, data gravity. Today, I'm going to have the pleasure of talking to Charles Thompson. He is a senior database engineer at Digital Ocean. And he is the author of a fairly new application called Dolphie is a real time MySQL monitoring assistant looks fantastic. He was kind enough to write a blog about this for our community blog. And I wanted to bring him into the virtual studio here and have a conversation with him about why he wrote Dolphie, and what he plans to do with it, and generally his experience with open source databases, Charles, thanks, and welcome, and thank you for being the first guest on this podcast. I really appreciate it.

**Charles Thompson:**  
Hey, Joe, you're very welcome, man. I'm glad to be a part of this.

**Joe Brockmeier:**  
Thank you for writing Dolphie, let's dive in a little Python, there seems to be a little bit what inspired you to write this? I mean, there are some other things, there's PMM, what made you think of writing this application.

**Charles Thompson:**  
So what inspired me to create Dolphie is the fact that I looked around at what was currently available, right, there isn't really anything except as you already mentioned. And, and that's a good tool, but it's not currently maintained well, and just not really a modern app. So I thought about it, and I saw the opportunity, that could be able to build a tool, where that it would sharpen my skills in Python, by also at the same time to be able to give back to the MySQL community, right? Because I have used a lot of open source tools from the AI community myself, and, you know, it would just feel extremely good to me to be able to be a part of that, and to be able to have people use the tools that I intend to be able to help them right. So, so far are everything I have heard from a user base of Dolphie, it has, has helped them out tremendously, you know, I have received very positive feedback that, you know, eBay can do things that they used to not be able to see and that you know, they just had that transparency into their database servers that fat didn't have. So it feels very rewarding. And just a good feeling to be able to give back. And something else that inspired me actually, it was that whenever I found out about the Python package textual, I'm not sure if you have ever heard of that, but it is a T Y, that allows people to be able to easily create a UI in a terminal, right. And that just provides a lot of possibilities for how that can be able to present the data that Dolphie actually does write, like, I mean, with all of the various graphs that has to how the tables are presented and various things of that nature. Right? That's all possible because of the use with textual and I mean, it's extremely easy to use, right? So it just goes to open up a world of possibilities for me, and allows me to be able to share that with everybody else.

**Joe Brockmeier:**  
How would you know, like the differences between Dolphie and something like PMM? Like, where would you use one or the other? Would you or would you just use one or the other? Or do you think they work together pretty well?

**Charles Thompson:**  
Yeah. So I see Dolphie operating with a symbiotic relationship with PMM and, and various other historical monitoring systems rather than competing with them. It complements AI capabilities. It provides a real time perspective of a database server with a level of granularity that sets it apart, particularly in its ability to manipulate a process list. It is also the reality that many people reside within their terminals, right? Which, in my opinion, makes it a very practical solution that stops people from having to context switch to a web browser or some other tool.

**Joe Brockmeier:**  
All right, I have to ask right now while we're while we're taking a slight pauses, so what is your favorite terminal? Like what's your what's your workstation? 

**Charles Thompson:**  
What should be my favorite terminal right now and is the term two? Okay, that is what I currently use right now. Yep.

**Joe Brockmeier:**  
Okay, so your Mac filler?

**Charles Thompson:**  
Oh yeah. I am well, I mean, I use Mac for work. And then I switched back to Windows, you know, for my personal life.

**Joe Brockmeier:**  
Alright, I'm a Linux guy most of the time myself. But that's cool.

**Charles Thompson:**  
I use a Mac, but then I SSH to Linux servers all day long, is just kind of like a group of various systems, right?

**Joe Brockmeier:**  
It's basically a candy shell to lay out kind of Yeah, exactly. So how long have you been working on Dolphie? You mentioned it took a while to get where you wanted it to be for a release? How long have you been working on this?

**Charles Thompson:**  
Right. So I think I started on it a year and a half ago. But the first version of it was just kind of a bare bones thing. At that point, it did not use a textual package. And it didn't have a lot of the features it currently has right now. And so the first version of it was just pretty much like a personal tool. And then, probably up until recently, in the last, like, three months is when I chose to, like really let in gay del work to make it, but it is right now,

**Joe Brockmeier:**  
I think it's gonna catch on. It's one of those tools I've been covering open source and Linux now for some, almost a quarter of a century going on that. And this looks like one of those tools. I remember the first time for example, I saw H top. And it looks like something like one of those things where it's gonna catch on, people are gonna love this, when they get their hands on it. Is this the first kind of full-featured application you've written? I'm taking, I'm gonna guess that you've got some chops at Shell scripting and have written lots of things. But is this your first kind of major app?

**Charles Thompson:**  
Yeah, so this is probably my largest project I have ever worked on. There have been some smaller projects I have worked on in the past, but they haven't gained popularity. 

**Joe Brockmeier:**  
A dolphe has told me a little bit about your licensing choice here. So it looks like you've chosen the GPLv3 for this one. Why, why that is that just because GPL kind of aligns with MySQL or any particular?

**Charles Thompson:**  
I suppose choice isn't really one, I put a whole lot of thought and two, just because of the fact that I don't really care what someone does with the code, you know, it is publicly available if someone wants to use some of my code. Absolutely can you know, download theme you start to copy paste it and slap some other name on it.

**Joe Brockmeier:**  
So tell me a little bit about what led you to this, like, was there a particular you know, this is your day job monitoring and troubleshooting databases, making sure that digital oceans customers are happy and everything is running? Was there any particular instance or you know, incident that inspired this was there like a horror story that you're like I need, I've got to have Delphi to or something like Dolphie to troubleshoot.

**Charles Thompson:**  
There wasn't a specific event or anything of that sort that happened. That prompted me to want to create a tool like Delphi, it was more along the lines of creating something that helped me do my job while simplifying my life at the same time. But what led me to creating Delphi was creating a tool that was up to my standards, I am a bit OCD on the way that data is presented, and what thief on factor is a color scheme, you know, so on and so forth. So creating my own enables me to, to make it in my own image that satisfies all the requirements, I have, wow, providing that full control to change it. 

**Joe Brockmeier:**  
However, I see fit, by the way. So for folks who are listening to the podcast, if you do a search for Dolphie, you should be able to find it on GitHub under Charles dash 001 that repo. And also I wish that this is one of the few times you definitely don't need to see my face. But I wish I could show you some screenshots because it's actually for a DUI really, actually a beautiful application. I'm looking at the screenshots and have played with it just a little bit. So it is for terminal app, it is quite attractive. 

**Charles Thompson:**  
How much of that is thanks to textual GAE color scheme that you see there is all me. I played around a lot with colors to find the right balance and what looks good. What you see with all the tables, graphs, the positioning of objects, no flickering between screens, etc is all thanks to textual and allows me to easily create renderable to display them all into a terminal, which absolutely love.

**Joe Brockmeier:**  
This works with MySQL, MySQL 5.7 and 8 are just 8.

**Charles Thompson:**  
Currently, it is not that six out that seven, eight and eight that one. 

**Joe Brockmeier:**  
The first question you will probably get if you go to like any trade shows or anything is like, Well, what about Postgres?

**Charles Thompson:**  
Yeah, the thing with a tool like Dolphie is it requires extensive knowledge and experience of a database to know what data to present, how to present it, etc, right, because it runs a lot of queries that I already knew about because of my experience as a DBA. Whereas with Postgres or Tamil, their database, I would have to take a lot of time to research, what should be presented, what queries are run, and things of that nature, which I just don't have the time for right now. I do think the biggest advantage of Delphi actually is the fact that it is a tool built by a DBA. For DBAs, I personally have over 10 years experience with MySQL. So everything I've learned that is important to see at a glance is included. So as time goes on, it'll get better and better. I am also taking contribution. So if anyone wants to pitch in, you are more than welcome to.

**Joe Brockmeier:**  
So it sounds like you could use Dolphie if somebody was a heavy duty Postgres enthusiast could maybe use it as a jumping off point or or maybe you would even accept pull requests if somebody wanted to work with you on it. 

**Charles Thompson:**  
Yeah, I mean, if someone really wanted to have a tool like Dolphie, for another database server, it should probably be attending.

**Joe Brockmeier:**  
So I mean, you mentioned that this took a lot of know how with MySQL. Maybe tell me a little bit about your journey with MySQL, when do you get started with MySQL, how long you've been supporting it and using it. 

**Charles Thompson:**  
I started off with MySQL as an intern, which transformed into a full time position. But when I was an intern, it felt like that everything I was doing just clicked, you know, I loved everything I was learning and just the field in general, there were a lot of avenues at the time for me, buy databases in general just felt right at this point now, and I've been in the field for around 10 years, and I'm very glad I stuck with it.

**Joe Brockmeier:**  
Now we're getting close to the end of our time, nor respect everybody's time, I do want to recommend that people check this out. If you're using MySQL, I strongly recommend we've got a blog on percona.community about it. And also you could just, you know, pip install and try it out. Go look on GitHub, is there anything about in particular about Dolphie, though, that you wanted to highlight or mention that we haven't covered? You know, anything? I always like to ask people when I do endorse, like, you know, what happened, I asked that I should. 

**Charles Thompson:**    
So some good things to note is that it supports Mac, Linux, and Windows also works for MySQL. I really wanted to support the older verses just because I know a lot of people that are still on 5.7, and even some people that are on 5.6, though, you know, it's important to me back and be able to share it with people that are on the older versions of me, it is kind of crazy to think that companies and people still use pod plastics, I'm not really sure why. But you know, at that point, it is what it is. Yeah, and I forgot to mention that it also supports group replication. So as you can see, I am trying to support as much as I can, that's feasible for me, but there's obviously going to be some things I currently don't support, but I am improving upon Dolphie, you know, through time, and eventually it will support even more things. So yeah, to close things out. I just want to thank you, Joe, for inviting me on and for letting me be the first person on your podcast here. I really appreciate that man. And I would like to encourage all of our listeners of the podcast to check out Dolphie to see how they can be able to help them with their database needs.

**Joe Brockmeier:**  
All right, and those of you who are still on MySQL five, six, you need to reconsider your life choices and get upgraded soon. If you need help with MySQL 5.7 Percona is going to help you support that that is commercialism going to make the podcast right there. But we are supporting folks pass it upstream into life. But really upgrade if you're on 5.6 for whatever, for goodness sakes. Please do check it out. I want to thank Charles again for being on the podcast. I really appreciate it. He's. This has been really great and thank you for making the first episode so easy. Please check back for more episodes and share and enjoy. 
