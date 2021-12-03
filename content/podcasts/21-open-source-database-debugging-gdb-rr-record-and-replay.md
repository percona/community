---
title: "Open source database, debugging, GDB & RR - Record and Replay - Percona Podcast 21"
description: "In this episode we cover his career, finding and debugging hard to find bugs, GDB & RR - Record and Replay - and talk about ideas for a potential special in-person barbecue & open source event"
short_text: "The HOSS sit down with the Software Engineer at Percona Marcelo Altmann to talk about all things open source, database, and debugging big projects. In this episode we cover his career, finding and debugging hard to find bugs, GDB & RR - Record and Replay - and talk about ideas for a potential special in-person barbecue & open source event"
date: "2021-05-20"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-21-with-marcelo-altmann-software-engineer-percona/"
youtube_id: "wUqxEqBIJlQ"
speakers:
  - marcelo_altmann
aliases:
    - "/podcasts/21/"
url: "/podcasts/21-open-source-database-debugging-gdb-rr-record-and-replay"
---

## Transcript

**Matt Yonkovit:**
Hey everybody. Welcome to another HOSS Talks Foss. I'm here with Marcelo Altmann, our Percona’s own super engineer. Marcelo, you've been at Percona for a few years now, I remember we met in person a couple times at a conference here in there. And also, you came to our headquarters, and, Marcelo, you're down in Brazil. And so what does the American do to the guy who comes from Brazil? He brings them to the Brazilian restaurant, just to see how close the Brazilian food is in America to Brazilian food in Brazil. Right. And so, and we found out it was not, it was kind of okay, right? It was okay. 

**Marcelo Altmann:**
It was okay. They had good barbecues and good picanha.

**Matt Yonkovit:**
Yeah, but it wasn't, it wasn't up to the Brazilian standards.

**Marcelo Altmann:**
Not quite. Like, especially here in South Brazil. We are close to Uruguay like asada and barbecue. It's a big thing. 

**Matt Yonkovit:**
So it is a big thing. It is a big thing. I have only found one year ago in barbecue in all of the US. I actually found it once. Like I was driving around. And I'm like, whoa. And so I had to pull in and I had to go get some because we do know that we have some excellent barbecue skills down in the South American region. Yeah, so Marco’s barbecues are the thing of legend.

**Marcelo Altmann:**
Indeed, if you had a chance to go to some Uruguayan team meeting at the end of the year meeting like he is, we call him the day designated by the barbecue master. 

**Matt Yonkovit:**
So here is actually planning a barbecue and open source event where we're all going to get and we're going to grill and we're going to barbecue individually and talk open source. And other people, I think it's going to be an outstanding event.

**Marcelo Altmann:**
I don't know about the others. And I don't think I could do that, like, talk, technical thing and barbecue. But I'm sure that Marco's will be able to do that.

**Matt Yonkovit:**
So now there's a challenge out there. So those who are interested in barbecue and open source a new event for the community, let me know. Because we're really excited about that. That's gonna be awesome.  Yeah. So Marcello you've been at Percona, like I said, for a few years, you started off in the support team, now you're in the engineering team. And so tell me a little bit about your background here. So you know what, what kind of brought you into the open source space, and brought you to Percona. And tell me about that journey to eventually doing some engineering work. 

**Marcelo Altmann:**
Right. So I started with MySQL, I know around 2006-2007 as like, lamp, learned Linux, PHP and MySQL. And like, if you are in the MySQL ecosystem, like you know about Percona, like you read the Performance blog and everything. So I moved to Ireland. I was a database administrator for the top level country domain like the company responsible for the.ie domains like the dot coms in US. I think in 2014, I got the chance to go to London and speak on a Percona Live. I met a few of the guys there but it was in 2006 when I went to Santa Clara in another Percona Live where again, where Marcus and Wagner Bianchi  introduced me to a lot of folks in Percona. And they said, Well, come to work here. Well, I don't know if I'm capable off but let's try and remember I had some projects to finish for the Irish company. And I did that and then I applied for a position and here I am.

**Matt Yonkovit:**
And here you are and then you and Charlie came out and visited me a Brazilian barbecue. Yeah. And you started off your career. So you got you started in the support space. And then you move from support to engineering. Why the switch?

**Marcelo Altmann:**
I don't know. It's like in MySQL, it's like a big thing like he can like replication, you can like I don't know optimising queries, you can like design schemas, things like that. And in support, I was always attracted to crashes. I when I first started again Marcus was my buddy. And before joining Percona, I have never opened MySQL source code. It was like something unbelievable. And in my case, and I remembered working with Marcus in some cases, he said, Well, it's open source, dude, let's open the source. And once I started to get familiar with things, I was always attracted for crashing, every new being regarding Slack, and it was crash signal six signal 11, no one wanted to touch those type of cases. And I was like, leave to me, leave to me. So it was like an opportunity to get a real case scenario and like, explore a bit more of the source code. And then I remember I tried to apply to an engineering position, but it was like some senior position and I was not accepted. And basically talking with Karina, my manager at the time, I said, well, that's actually what I want. And he spoke with George, which is my actual manager at the moment. And we did some sort of arrangement. I worked four days a week on support in one day, a week as as a engineer, C++ engineering. So that's how it started, I think I spent like a year doing that. 

**Matt Yonkovit:**
You got more familiar with the source code, you were able to, you started to learn C. So you actually got the opportunity to not only, like, kind of scratch your itch with the chaos and the crashes, you're able to actually learn a lot of those engineering things. 

**Marcelo Altmann:**
And, and it's kind of some sort of a big step. Because one thing, it's okay, I want to be an engineer. The other thing is to understand what is the day to day on an engineering side, and like that actually gave me the opportunity to taste these and understand well, that's actually what I want, or no, like, let's stay at the support. 

**Matt Yonkovit:**
What is the day and life of an engineer like what like, what does that look like? 

**Marcelo Altmann:**
Well, if I had to work with crashes before, like, right now, it's even more. That's basically what we do like when we try to solve crashes or design new features. But basically a day in life of an engineer, it's, I don't know, five minutes coding and the rest of the day running tests, because it's like, my sequel has this gigantic test suite. So every time we do something, either a new feature or a bug fix, we need to make sure we write a proper test case. So someone else doesn't introduce this same bug or issue again, and like MySQL has for all those years now. Like it has a gigantic list of test cases. So every time you do something, you have to make sure you're not introducing a regression on something that was supposed to work before so right. 

**Matt Yonkovit:**
Yeah, I mean, then QA is always a critical component especially with data, you don't want to mess with people's data. Yeah, right. That's one of the things you need to keep it as safe as possible. Now, your love for bug crashes led you to really become kind of more intimately involved with GDB. Yes, because GDB is the tool of choice to look at your traces and try and find some of those problems. For those who don't know what GDB is, because we've got kind of all over the board audience, number one in Tunisia. Number two in Madagascar, in terms of podcasts on Apple, so very proud of that. So for all of those folks who are out there who don't know what GDB is, maybe give a little bit of background on GDB for folks. 

**Marcelo Altmann:**
So GDB it's basically a debugger that works in various languages, including C and C++, which is the language that MySQL it's written with. And basically, it allows you to go inside the process and like trace whatever it's it's going on, like you can do some crazy things like you can change your MySQL variable from the from the GDB source like you can, what we most do, like we do set set points before like a crash happened so you can understand what was like the value of a variable and who changed that variable, like you can add a harder watch points on memory address to see who changed that that memory value or something. So those are the most useful things that you do with with GDB. Basically, it's meant for debugging. 

**Matt Yonkovit:**
And you just wrote this blog post. And this was a really cool tool that I didn't even know about. And in fact, when I was talking to people at Percona, like half of them are like, I've never heard that tool called RR, for replaying GDB traces. So you can kind of walk through. So how does that work? 

**Marcelo Altmann:**
I was like, fascinated when I heard about this. And I was kind of scratching myself, like, I have to test this, I have to find a case where this will be useful when I'm sure like, this will be a game changer. And we actually had one one case that it's the one that I wrote a blog post, which was the first one we use it, but basically RR, was designed by the Mozilla guys to find some bugs on Firefox. And like, when you are dealing with bugs, like the most, your chances to find, fix for a bug is if you have a test case, finding a deterministic test case, it's like not always the case, it's very difficult to be able to write a deterministic test case and like with this type of software that we do nowadays, like MySQL, it's it's multi process, you have tonnes of components inside the softer things have to happen in certain in a certain order. So you can explore that edge case that you are seeing. Sometimes it takes weeks for you to be able to reproduce once and you are in the middle of reproducing that the whole day, the whole week. And when you reproduce use, you kind of lost track Okay, what I changed this now that made it reproducible, so RR came into to help these like, it's not that I think in the MySQL ecosystem, like everyone that does softer, has issues with finding deterministic test cases. And the Mozilla guys, they created this tool that basically, it keeps track of all the system calls that the process does in the return eight receivers and the signals it record those,  and they can be replayed using the GDB, our favourite tool.
And like it's the it's, it's really cool, because it's 100%, deterministic, like even like the memory addresses and everything, like if you can replay that over and over again. And you will always get the same result. And, and the most amazing thing about this tool, it's like it also allows you to play the execution backwards like with GDB. Like you have to port breakpoints for example, like, I want breakpoint on step two, and then you go to step two with I don't know, one example, like sometimes it takes time to replace all the execution. So let's say take 15 minutes to repeat this execution, and you hit the breakpoint on step two, for example. And then you realise like the issue, it's not the issue here, it's in step 111, you are doing that with gdb itself on a running process, what will have to happen, like you have to start everything over again. But we've recorded replay, like, you can just put a breakpoint on step one and replayed execution backwards. And like this is that's very amazing. That's really cool that you can go back where you were before and kind of step backwards and forwards. Yeah. So you can go back and forth as much as you want. And like, as I mentioned this, it's been a game changing in terms of finding books and reducing shortening, like the time to on the resolution of those.

**Matt Yonkovit:**
Very cool, very cool, and the blogs out there now. So I would encourage people if they want to know more details to check it out. Because this isn't a tool that had a lot of documentation either. So you got to figure out some of this as well. 

**Marcelo Altmann:**
Yes. And one thing that I really like it, it's the guys here at Mozilla, they are really open. I was also doing some work with these and with a project with Vadim regarding Percona XtraDB Cluster, and I actually found a bug on the tool that there were some deadlock when you were using like outputting strings on our pipe. And I just wrote our deterministic test case, a programme that could reproduce that I opened an issue with the RR guys and I think in one day or two, they fix it. Yeah, and but it's true, like there is not much documentation.The tool is not like the most user friendly as you can imagine, like it touches like some low level things, you have to do some depending on your processor, you will have to do some some changes, like in my case I have on a AMD ryzen. So you have to do some work around in order to be able to trace everything before it goes to get to the CPU. But it's, it's amazing. Like it's new, it's kind of a new tool. It's getting some traction right now. So more people were using it and more people were contributing to this. So I believe it will be very popular and perhaps even deliver on its standard like Linux distro in the future. 

**Matt Yonkovit:**
Great. That's awesome. Well, Marcel, thanks for taking a few minutes to chat with us about RR, a little bit about what you've been working on your career. Appreciate the time today, and hope to see you in the future at an actual in person barbecue. You know, that would be nice. Yes, yes. But thanks. Thanks a lot, Marcello. Appreciate it. 

**Marcelo Altmann:**
Thank you, Matt.

**Matt Yonkovit:**
Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course tune into next week's episode. We really appreciate you coming and talking open source with us.

