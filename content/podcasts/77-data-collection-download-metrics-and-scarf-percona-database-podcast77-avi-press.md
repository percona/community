---
title: "Data Collection, Download Metrics, and Scarf - Percona Database Podcast 77 /w Avi Press"
description: "Matt Yonkovit, Head of Open Source Strategy at Percona sits down with Avi Press, Founder & CEO at Scarf. Listen out for an overview of Avi’s background, projects that he worked for, and the ideas that took him to Scarf. Dive into Scarf backend and learn how it works. They tackle the pros and cons of collecting data, catch up with some trends in the open-source space, and answer rapid-fire questions."
date: "2022-06-30"
podbean_link: "https://percona.podbean.com/e/data-collection-download-metrics-and-scarf-percona-database-podcast-77-w-avi-press/"
youtube_id: "sVrFW-c_P8I"
speakers:
  - matt_yonkovit
  - avi_press
---

## Transcript

**Matt Yonkovit**  
Hello, everybody. Welcome to another HOSS Talks FOSS. I'm the HOSS, Matt Yonkovit, Head of Open Source Strategy, here at Percona. And today, I'm joined by Avi Press, the CEO of Scarf. Avi, how're you doing today?

**Avi Press**  
I'm doing great. Excited to be here.

**Matt Yonkovit**  
Great, great to hear. Now, Avi, I'm passionate about open source. And I have had lots of conversations around measuring open source. And I know scurf is designed to help measure the impact of your projects and what's happening in the open source space. But before we get there, I wanted to talk to you and ask you about you. Where did you start your career? And how did you get involved in open source?

**Avi Press**  
Yeah, so, my career background is in software engineering. And I would say I got into open source kind of from two different sides. So one of them is just being a developer, all the tools that I was using just up and down, the stack is open source, and just get very involved with it that way. In my first programming job, I worked at Pandora right out of school and was using a lot of open sources there and got to deal with a lot more of an open source community just by way of depending on these tools, an industrial setting, needing to work through bugs as they pop up in our dependencies. But down the road, I think I got more of the experience from the maintainer side of things, when I was just building tools for myself for fun, or work or whatever, and just putting them out there. If they're useful to me, they'd be useful to other people and just kind of put stuff online. And as some of the projects picked up steam and people came for contributions or questions or whatever, it might have just continued to kind of walk down the path of an open source maintainer. And that's  what got me so hooked on the experience of being an open source and just wow, someone from Brazil or Finland or Nigeria contributing to the project, that's such a, it's, it's an incredible thing to see a project take off like that.

**Matt Yonkovit**  
And you didn't start off as a maintainer, then. So you started off as that user, that end user who is appreciating using and you're like, hey, I want to develop something to work on might as well throw it out, there's open source, and people just started using

**Avi Press**  
Pretty much, I think I got lucky a couple of times with Hacker News just like it was there. And then sometimes you get that little shotgun blast off of PR for the project. And often, that just goes away and dissipates in 24 hours, but some people stick around. And that's, that's when you got kind of a semblance of whatever early kind of community you're gonna build.

**Matt Yonkovit**  
Yeah, if you can go viral on Hacker News, people love it, right, like, so you get a big bump like, I've gotten, like 30 40,000 views just from one Hacker News on the front page, right? And it can, it can boost things. Now, as you were this maintainer, you were starting to look at these projects, and people started to contribute and started to work with you and started to download sort of yours. From what I understand, you found that there was a deficiency in understanding your users. Absolutely. Tell us a little bit about that.

**Avi Press**  
Yeah. So my projects were distributed. So code is on GitHub, and the artifacts I was distributed either on the package registry is that the language I was using, which was largely Haskell, so Hackage being the main Registry, or via Docker containers, on Docker Hub, all I knew about the impact of my project was, well, here's how many downloads I have. And here's how many pissed-off people are opening issues on them. And all the lovely people that were contributing, and, like, that's all I had to work with. But anytime, people would come in with some issue or complaint. And that person complaining wasn't a big company; that's a pretty stressful situation to be in as a maintainer. You want your project to look good, you want to look good and space. And so over time, that increased maintenance burden was kind of the thing that was someone says, Hey, this doesn't work on this, this breaks on Windows, and I. And I wonder, well, how many people actually use this on Windows? Like, should I prioritize this or not? Or should I just say, I hope someone comes in and fixes it because I don't have a way I'm not on a Windows machine, or I wasn't at the time, and I'm still not? And so, metrics were kind of failing me both from a like just doing my work as a maintainer perspective, but also the perspective of, well, if I'm providing value to people at big businesses, should I start a company around these tools, maybe I should, maybe I shouldn't. But I didn't have any data to help answer that question.

**Matt Yonkovit**  
And that's how Scarf was born is a way to measure the impact of your project because, lets be honest, necessity is the father of all innovation, as they say. And so you have the pain of understanding how you could maintain these projects better, you started to look at ways to collect additional metrics and find out more data on who's using and how it's being used in the wild.

**Avi Press**  
That's exactly right. It at the time, a lot of the tools I was putting out there was like, command line utilities in one form or another. And it didn't seem, it seemed kind of weird too, for instance, stand up like a back end, just so I could collect metrics from those CLI tools, for instance, but the distribution channels I was using to get the stuff out there just wasn't helping at all. And when I thought about, okay, well, like if I did connect with, say, a commercial user, like, what would I even do? Like? How would I, what would I sell to them? If I was trying to build a business? I could try to broker a support contract. Maybe I could try to change the license structure and sell them access to additional features. But if I did, how would I give them those new features? Like I would have just to do all of the gatings inside the CLI application? Like, do I want to start putting stripe integrations into a command line app? Like, that's crazy. And so it became, it became a front of mind problem of like, how do I get better data out of distribution channels? And how do I? How do I have a distribution of my software that is amenable to the kinds of things that I would like to do? And so those ideas are what got Scarf started, I put out a blog post with these two pieces of mine, like the analytics, and then the like, commercialization of the distribution channels. And that blog post is what kind of took off more than other things I put online. And that's what told me that, oh, yeah, there's a lot of other developers that are struggling with these things as well. And there might be something that I can do to address it.

**Matt Yonkovit**  
What exactly is Scarf? Maybe you haven't experienced it? So we've been talking a little bit about the metrics and your journey, and it's an interesting story. because I think it's, it's a very common story, right? you start off using open source, you build some tools to help you out, people start to use them, they start to get popular, and you have no idea who's using them or how they're using them. They're asking you for help. Right? And you're like, I don't know if I should do this or not, I don't know how to handle this. And then that leads you to create Scarf. which most people don't create Scarf, you're the only one so proprietary. Do. so? So that's where the story deviates. But it's a very common story. So you built Scarf to solve these problems? What is it tell us what it is?

**Avi Press**  
Yeah, Scarf has evolved since I first started working on it, but what it has turned into is a set of tools to aid with open source distribution, analytics, and then downstream for that commercialization. So we build tools that help you understand how are people doubt? Like, how are people downloading the software, where in the world are our users, and what companies do they work at? What versions are in use for all these kinds of things that are commonplace kind of metrics and other domains of software but not in open source? And so we're trying to make it so that if you are an open source project, company maintainer, you can understand the impact over your work and what companies rely on it, you can connect with those companies, and you can build a business around your tools, or you just understand what, what is the impact of what you are doing in the open source space, and better understand that. And so, whatever your goals are, they will probably be aided by being informed and being able to make data-driven decisions. And that's kind of a that is the foundation of what we're building. Yeah, so a suite of tools that all fit together will give you different pieces of the story. So you can kind of understand the journey that your users are going through when it comes to your open source, like how did they discover it? How do they use it? Where are they getting stuck? How are they engaging?

**Matt Yonkovit**  
Okay, and that suite of tools, the two that are out there now, one is geared towards measuring who's accessing and using your documentation, the others on the Scarf gateway, which I understand is just it's a, it's a proxy server that collects data. It's a gateway that allows you to see who's coming, meaning and asking for right now downloads or packages, but it could be anything. It's whatever you want to measure, right?

**Avi Press**  
That's exactly right. It is very similar to how Bitly works for URL shortening; we've kind of taken that idea and applied it more for the open source space. So you can put packages behind the containers behind it, arbitrary URLs and files behind it, and people put their whole websites behind it. And it is just kind of a way to put up some eat very, very easily put up some analytics in front of whatever it is you distribute. But then also making them available all from one place. So you can be distributing files from GitHub releases executables, on s3, and Docker Hub containers, all from the same endpoint, and it just kind of just works for all but whatever package managers, you might be pulling that down.

**Matt Yonkovit**  
Yeah, and I think that what's, what's interesting is that you aren't just relying on Download stats, and in my experience, a lot of projects start early on focused on downloads; that's how they get their funding. That's how they prove their growth, their adoption, right? I got a million downloads. But oftentimes, when you talk about download numbers, those are often skewed or unreliable.

**Avi Press**  
That is exactly right. I think this is more common than we would like to admit; in the open source space, you may have a million downloads a month, but realize that 95% of them come from two people that just have a CI pipeline that is pulling all the time. And we see this like that is not a made up, that is not a made up scenario at all, it is very real. And yeah, I think from building a business and raising money from institutional investors, or whatever that might look like, it's very different from saying, Yeah, we have 1000 downloads from one person, or 1000, downloads from 100 people or 150, businesses, these are all very different contexts, and they have very different implications for what opportunity you have in front of you. And making that more available in open source more generally just means that we can have maintainers that are making better decisions, in general, and maintaining their software more effectively and more proactively, I think, would be another very underrated aspect of this because my personal experience as a maintainer would just, it often just felt like you're just drowning, under the issues and bugs and these kinds of things, and never getting out from under it because you only know something when someone comes and tells you, which by then in a lot of circumstances is already too late.

**Matt Yonkovit**  
Yeah, and I think that as we start to invest more in the open source space, as a society, and as we see more of these projects come along, the need for more analytics on what's happening is just growing in this space. Now, now, I'm curious if you have users who are using Scarf to collect metrics and collect data on their packages. Are you seeing any trends or seeing anything in that, like it used to be like I said, People distributed through yaml repos, or like that your classic Linux repos. And I, it's, it's evolved, right. So now you've got Python has their own repos. And you can get repos for Ruby, and you can get like repos for everything else. And we're seeing Docker containers. So from a packaging perspective, how are people releasing their software nowadays? Is it changing?

**Avi Press**  
Yeah, it's a good question in terms of how things are getting released. I mean, I think, in a lot of, in some ways, these things are getting a little bit more decentralized. And in some sense that you do want to start pushing artifacts to different places, depending on use cases. The Linux world is a great example because you have to manage am I going to be Yeah, am I going to be in kind of the main line apt and yaml, or do I want to self host these repositories? Or what do we want to do, and in practice, you might want to do multiple things. And in the container world, there's been a lot of similar discussions here where everyone was pushing a docker hub for a long time, and Then suddenly, they say we're gonna start rate limiting anonymous accounts from how much they can pull from us effectively gaining access to other people's work, putting a paywall in front of other people's work and cutting the creators of that work out of the equation entirely. And so you have a lot of people that they want to switch to GitHub or switch to Google or these other things, but there's that block in effect as well. So yeah, I think, I think the overall trend with publishing that I would say is changing over time, what we see changing is just a desire for more control over the distribution channel. So it should be something that you serve from your own domain, not from someone else's domain because they can use your app laterally to make these changes to your distribution that you have no control over, which is an increasingly problematic situation. I think.

**Matt Yonkovit**  
That's an interesting shift, right? Because if you are coming kind of full circle, because I mean, like, early days before we had repositories, everything was self-hosted. So you're seeing kind of that reversal, where now we're saying like, Okay, we were hosting on x, but now we're going to host on our own, you think that's driven? Because there are so many places you could go get the software, and it's difficult to deploy to all of them?

**Avi Press**  
That's a good question. I mean, I think that's certainly part of it, I know that I see a lot of, we see a lot of companies that are specifically with Linux packaging of like, there are so many places we need to push this too, that it's easier, just push it here, and then we can let the repository maintainer is that Debian or wherever do their own thing with this? And I think that there's yeah, there's, there's, there's pros and cons to that model, I think. But ultimately, yeah, ultimately, I think it's kind of it's it's on you to distribute, if you want to have any say in how these things are distributed, distributed, you will ultimately need to do some of it yourself, or have some kind of policy on what you do here. And I think over time, we are also seeing improvements in the observability of these things over time. So like, the Python is a lot better, like the lot of data that you can get out of the PR And these kinds of registries, same with like rust with crates.io. And these, these other sources that are giving a little bit better insight here, as there's more choice for what you can do. Yeah, honestly, honestly, I think the choice aspect of this is big, that just we don't get locked into the single platform of the day, we can, we can go to multiple places, which is also important for service continuity, what happens when one of these registries goes down? What do you do, like people are just offline for a while, development flows stopped while CI is crashing, and these kinds of things, so yeah, rambling to get towards an answer to this, I think that's one of the big shifts that we are seeing is kind of more ownership being taken over distribution.

**Matt Yonkovit**  
And I think that how Scarf works from what I understand is, it provides a gateway, almost like a Bitly, right, like, so you have a URL, and it basically passes through that channel, and then it can ultimately go to any of the repositories behind the scenes. But because you have that gateway, you control some of the data that's being collected and how often it's being referenced. So, if you're going to go and hole out of Docker Hub, for instance, you would then put a gateway in front, which would then allow you to collect more data that you might have to pay Docker to get access to on their side, but it's only going to show you a portion of what that those downloads are because odds are you might have multiple places where you're hosted. So how do you aggregate them into one? And I think that that's another interesting thing. I've been a big proponent of figuring out how to measure the effectiveness of open sources for a while. And I view this as you mentioned the pipeline earlier, I view this as you start out, you're looking at those like, who's curious about your product, and I know, you have a documentation product as well to say like, oh, well, well, we'll check who's accessing the documentation, but then it's like, Okay, once you've checked that, then it's trying it out. And then that's the download phase, right? And so if you look at who's accessing the website, who's accessing my documentation, who is downloading, and then Moving down to who's downloading and using it again in a month or two months or three months. That's an interesting way to view the data. But I'm curious. There's also this kind of negative connotation around collecting data now, especially with GDPR in Europe and PII. So what are you doing to prevent collecting too much data? Or keeping people's data safe?

**Avi Press**  
It is a very good question. Because it's not easy to do all of this stuff and still be compliant with things like GDPR. And so one of the things that our system does, so our users don't have to do it, is that once we process, once we process metadata for an IP address, like what country did this come from, or what company was associated with the different download or view or whatever, we then delete that information from our system. So we're not holding on to these raw IP addresses or PII in the event that Scarf was to get hacked or something. And so we're not, we're not sending those IPS out to our users, because we don't have them to give them which I think solves a lot of these solves a lot of these problems, ultimately, that's on us to make sure that we're very rigidly doing that. And there are no bugs that can potentially leak that information anywhere. But by doing that work and making that available to people, that ends up kind of securing a lot of these things. And one of the aspects of this conversation that I feel like it's not often talked about enough is that we're always having to, oh, well, what about the PII that's associated with Scarf's collecting, but like, all the existing registries also collect this stuff today, they just don't use it, and they just don't give the maintainers access to it. That doesn't mean it's not being collected. It doesn't mean that if someone were to hack one of these registries tomorrow that a bunch of PII wouldn't be leaking about exactly who was using what, we just don't confront the fact that this data is being collected or making use of it. And so I think this is something that applies to a lot about open source and privacy and economics is that like, these incentives are there, we're just kind of like keeping a blind eye to it. And we would benefit from being much more explicit about what's in play here.

**Matt Yonkovit**  
Yeah, So what you're saying is, you're just taking the data that is not being used but is available and using it.

**Avi Press**  
Depending on what you mean by available here. But yeah, like it's available to Docker, it's available to NPM. And yeah, so yes.

**Matt Yonkovit**  
So it's about freeing the data that other people are already collecting on your users?

**Avi Press**  
That's exactly right. Yeah. And so I think,

**Matt Yonkovit**  
that's an interesting angle, right? Because from yeah, I've got users using my product, all around the world. And all these other companies, all these other projects know about them, they might not do anything with it, but they can get access, they can do all the stuff that I can't.

**Avi Press**  
Right, right. And like, if anyone is going to have that data, the maintainers, I think most people would agree, would be the one group of people that should have it. And so one of the things that we learned early on, though, is that it's not just about what data is being collected that people are sensitive to; it's also how it is collected. And so one of the things that we tried early was, we made a JavaScript library that would just send the post-installation hook that would send these statistics up to Scarf, the exact same stuff that NPM would collect from there, as the way that their terms of service defined, will keep people had a people didn't like it because we were inserting analytics and phone home mechanisms in a place where it didn't exist before. And so we got a lot of pushback on that from the end users of the maintainers that were using Scarf. And so, the way that we've approached this with Scarf gateway has proved to be a lot better because it doesn't involve any code instrumentation, that's kind of just part of the normal path, and no additional books are being added, which seems to, which seems to be very important to people, although I think ultimately, we shouldn't probably care more about the data being collected, but nevertheless, here we are, so we got just to do what people we got just to do a typical one.

**Matt Yonkovit**  
Telemetry is often a challenge, right? And unfortunately, you can't build a solid product and continue to grow without understanding who and how your stuff is being used. And I'm not talking about who from an individual right, so and this is where there's a fine line. knowing that 30 people from this kind of basic demographic use a product in a certain way is different than knowing Avi uses it this way. Right. And I think that there's a fine line between those two. But the pushback often gets pushed back on both when it's more about the individual, right, like preventing the individual's data in it is an interesting thing, because we've seen this in the past several years where people have tried to move more towards the telemetry and gotten just slapped down because of it. Because people don't want to be tracked potentially, even though they're already being tracked.

**Avi Press**  
Right? Yeah, it's a real tough thing. I think we just haven't accepted how much this has already had, like, these wheels have been in motion for a long time. And now that there's, like, explicit discussion of it there's more hesitation around it. But ultimately, because it's there, it's a question of, it's not a question of, should we collect it? It's a question of who should have access to it. And that's, that's, I think, the crux, the crux of the issue here.

**Matt Yonkovit**  
So, I like to go through a rapid-fire round of questions. These are completely random. I have no idea what I'm gonna ask. So it might be scary, but it's okay. We'll get through it. All right. So, so Avi, what was the first programming language you used?

**Avi Press**  
Scheme! In college. I loved it. scheme. Absolutely. Loved it. Yeah. scheme.

**Matt Yonkovit**  
I don't even know if I've heard of the scheme. What is a scheme?

**Avi Press**  
Oh, it's a flavor of Lisp? Oh, yeah. So I was in college? Yeah.

**Matt Yonkovit**  
What? I hadn't heard of that. I mean, I guess it dates me a little bit. Maybe. I just missed that one. So, okay, so if you're going to sit down today and hack out some code, what are you gonna write it in?

**Avi Press**  
I will, depending on what I'm building. But my tool of choice these days is typically Haskell. I  love coding, and Haskell and Scarf are largely built into it.

**Matt Yonkovit**  
And why Haskell?

**Avi Press**  
That's a great question. I mean, there are a lot of objective benefits that I would point to, but ultimately, just because it's what I enjoy coding the most, why I enjoy it the most is because I  enjoy languages that have a huge emphasis on the type system. And on static verification that the program does what I think it does when I write the code. And so Haskell, I think, is a joy to code in because it's the only language where you can sit down, write something very complex, try it with the compiler for an hour, and then once it compiles, it might just work. Like, without ever having, like the first time you actually can execute the program, a very good chance that it does what you think it does. It's not to say it's like a perfect system or anything, but I think that that experience of like wrestling with the compiler to explicitly code what I have in my brain and have it just run is a very particular kind of joy that I liked.

**Matt Yonkovit**  
Okay, well, fair enough. Most used application on your desktop.

**Avi Press**  
I mean, I assume we do not include browsers here.

**Matt Yonkovit**  
browser,

**Avi Press**  
Chrome them, but I think, an interesting one, I do live in Emacs all day, even as a nonvalue even when I'm not writing code anymore, because all of my notes and to-do's and I use org-mode very extensively.

**Matt Yonkovit**  
I don't like Emacs. That's fair.

**Avi Press**  
If it matters, I use space Max. I'm using vim bindings within the maximum if that changes things.

**Matt Yonkovit**  
Things right. It's okay. I won't hold it against you. and so if you are going to go to a conference, meet up with someone, and you're all gonna go out to dinner. What are you going to order? Nine times out of 10?

**Avi Press**  
Oh, just generic any kind of restaurant.

**Matt Yonkovit**  
Anything like you just goes, What's your favorite food? What are you gonna look for first?

**Avi Press**  
Any kind of noodle dish I  enjoy, like pasta noodles, anything like that. I'm a big fan.

**Matt Yonkovit**  
Not doing the keto diet, then.

**Avi Press**  
No, I'm not. But not for now. Anyway.

**Matt Yonkovit**  
And the last book you read

**Avi Press**  
the last book I read. I'm not  I don't read nearly as many books as I ought to these days. But the last book I read was Norwegian Would I read recently, which I  enjoyed? Okay. Yeah, I think I don't read stiction all that often. But it did happen recently, but recommended. And so I read it; if you wouldn't highly recommend it,

**Matt Yonkovit**  
if you weren't doing Scarf, what would you be doing?

**Avi Press**  
Well, that's a great question. I would, I mean, I'd probably still just be, I'd probably be an engineer at a startup around in the Bay Area. I don't know exactly what, but that's what I was doing before. But I wasn't doing technology. Take the tech out. Okay, fair enough. I mean, perhaps I almost became I was on track to the to in college, I was on a pre-med route. And before, I kind of fell in love with programming, like just went off the deep end with coding, so I probably would have been a doctor.

**Matt Yonkovit**  
Wow. But yeah,

**Avi Press**  
these days, I also I got very, I  love baking as well. And so maybe some version of me would have been a baker.

**Matt Yonkovit**  
There you go. What do you bake in lately? Like, is it cookies? Bread what do you make and bake

**Avi Press**  
a lot of bread? Yeah, or not, not so much these days with Scarf; it kind of put a wrench into a lot of that. But I  love baking bread and bagels and just any kind of like, anything related to that.


**Matt Yonkovit**  
But hey, everybody who's listening in, if you do have a project, you're looking to get some additional metrics on who's using how the project is being used out in the wild, check out Scarf. It's free. You can sign up, you can start using it today. Get some additional metrics. And let Avi know if you have some feedback, I'm sure he and the team would appreciate the help.

**Avi Press**  
Feedback is always extremely welcome. And we will send you a Scarf Scarf if you do.

**Matt Yonkovit**  
Wait a minute, that's what you send out as Scarf scarves.

**Avi Press**  
We sometimes send out Scarf scarves they are they are our favorite company swag that we have.

**Matt Yonkovit**  
Okay. But I have to ask, is it like one of those Doctor Who scarves with like, the 12-foot-like rainbow, these are awesome.

**Avi Press**  
It's not, but we are going to be making some new ones soon. So I will take that as some feedback.

**Matt Yonkovit**  
If you want to be geeky, like go to the doctor.

**Avi Press**  
noted. Yes. Absolutely.

**Matt Yonkovit**  
Bobby, thanks for coming out today and chatting with me for a little bit, sharing with us about Scarf about download metrics. And you know a few other things. So I do appreciate the time. Yeah.

**Avi Press**  
Thanks so much for having us. That's fun.

**Matt Yonkovit**  
All right. And people who are watching, Go ahead, feel free to like, subscribe, and tell us what you'd like to hear from or from next. And if you have questions for Robbie, just leave them in the comments. And we'll make sure he gets them. Until next time, everyone. Thanks so much.
