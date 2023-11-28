---
title: "Data Gravity Episode 3 - benny Vasquez - AlmaLinux Project and the Future of Databases"
description: "Joe Brockmeier interviews benny Vasquez of the AlmaLinux Project to discuss open source data, the future of databases, and how databases and Linux distros go together."
images:
  - events/data-gravity/Data-Gravity-Episode-3.jpg
draft: false
date: "2023-11-16"
speakers:
  - benny_vasquez
  - joe_brockmeier
tags: ['Data Gravity', 'Podcast']
---

In this [episode](https://datagravity.podbean.com/e/data-gravity-episode-3-benny-vasquez-of-almalinux/), Joe Brockmeier interviews benny Vasquez of the AlmaLinux Project to discuss open source data, the future of databases, and how databases and Linux distros go together.

[Episode 3 Link](https://datagravity.podbean.com/e/data-gravity-episode-3-benny-vasquez-of-almalinux/)

<iframe title="Data Gravity Episode 3: benny Vasquez of AlmaLinux" allowtransparency="true" height="150" width="100%" style="border: none; min-width: min(100%, 430px);height:150px;" scrolling="no" data-name="pb-iframe-player" src="https://www.podbean.com/player-v2/?i=4zdi4-14f0fae-pb&from=pb6admin&pbad=0&share=1&download=1&rtl=0&fonts=Arial&skin=1&font-color=auto&logo_link=episode_page&btn-skin=7" loading="lazy"></iframe>


[All Data Gravity Podcast Episodes](/events/data-gravity/)

## Transcript

**Joe Brockmeier:**

Good morning, good afternoon. Good evening. Whatever timezone it happens to be for you. This is Joe Brockmeier, the Head of Community at Percona. And you are listening to Data Gravity, our podcast about open source databases, control of your data and all things similar to that all kinds of open source. Today we have with us a guest. I'm really excited to talk to benny from AlmaLinux project. Benny, would you like to do a little more formal intro?

**benny Vasquez:**  

Yeah, so I am the chair of AlmaLinux OS Foundation. We manage control and release an Enterprise Linux operating system based on the Red Hat Enterprise Linux versions that get released. We have been around just over two and a half years. Historically, we have been attempting to replace CentOS Linux that was discontinued in 2021. And recently, we've kind of started forging our own path as CentOS has the source rpms are no longer being released for RHEL. So now we get to do our own fun things. 

**Joe Brockmeier:**

And these days, you're pulling from the stream repo plus some bonus fixes and things like those kinds of diversions. 

**benny Vasquez:**   

The goal is to remain as tightly coupled with Red Hat as we can, because that's what serves our community the best they want Enterprise Linux and Red Hat is a stable operating system. So the closer we can stay, the better. And we're just pulling the updates from CentOS stream, but aren't following CentOS stream. We're not doing the regular releases.

**Joe Brockmeier:**   

Right. And so on of the reasons I wanted to talk to you today is, you know, obviously, the operating system underlies the database and is deeply important. And wanted to talk to you a little bit about, you know, how you see this whole ecosystem, what's important to you, in terms of databases on top of and control of data on top of all about, for example. So maybe start with a softball. So tell me a little bit about almost creating space for, you know, Red Hat, Enterprise Linux ships with a couple of standard databases you can install if you want. But tell me a little bit about maybe creating space for other databases where people might want something that doesn't ship with RHEL?

**benny Vasquez:**   

Sure, yeah. But one of the common things that we get from our users is that they're coming to us because they don't want to interact with the Red Hat Enterprise licensing system. Right. And there are a lot of reasons for that. Some of that is just we don't, you know,it's another layer of obfuscation and a layer of work that they have to do. But a lot of it is, I don't want to have to give my data to Red Hat If I don't need to. And so they go for other solutions that allow them to pass on that same concern for privacy to their other to their users or to themselves, right. I think one of the most exciting things that we're doing now that we are kind of more intentionally doing our own thing is opening up, like you said, opening up the door for other shall we say, just other pieces of software that Red Hat hasn't historically felt the need to add significant support for? That's one of the things we get to do. Like with Percona, right? We get to support in that way, the users that want to use Percona or anything else, and don't have to wait for the Red Hat approval.

**Joe Brockmeier:**  

They take a very, you know, narrow view of what they want to support, which is reasonable, no. But that does constrain people a little bit. So having that opportunity to say something like Percona Server moves more or less in lockstep with Alma, if that's your choice, kind of dovetails real nicely, or if there's maybe a database that they wouldn't historically shipped some sort of open source thing like FerretDB, for example. You know, that maybe someday Red Hat will see business opportunity, but for now people shouldn't be constrained by that, right? Yep, for sure. So folders closure for people listening is I actually used to work for Red Hat. And, you know, have worked with the subscription stuff myself. Two things really one is the friction of if you're just wanting so you know, I use all my at home, for example, for a couple of things. And if you want to not have to do, it's not a huge amount of friction, but it's still friction of like, I want to whip this onto a server. And I just, I just want to put it on a server, I don't want to have to create an account, I don't want to have to do any of that stuff. Don't have to worry about am I subscribe to things. And the other thing that you mentioned is interesting is people who are concerned about privacy. Do you see that as more of an individual concern? Or do you see that as an institutional thing where people avoid engaging, because they just don't want to have that relationship layer? Do you really see a lot of institutions that are like we just don't want anyone knowing what we're installing?

**benny Vasquez:**  

So I think that the stronger an individual feels, the more they will have an impact on the institution, right? Sure. The, what we're seeing right now has a large number of users that so individuals that that feel that way, but I'm seeing more and more organizations that don't require the amount of support or interaction that they would get from a Red Hat business agreement coming to us because they don't want to have to give up anything to Red Hat at all, they don't want to deal with getting the cold calls, they don't want to have to deal with, like, all the stuff that comes with, I have started this small amount of relationship, and I only need three servers, and I know how to support them myself. So I'm just gonna go with something else.

**Joe Brockmeier:**  

Gotcha. Okay. I do think, you know, that is one of the really important things in open source is the ability to use the software. So anybody, for example, can download Percona Server, and they don't actually have to have any relationship with us at all, you can go to GitHub, and, you know, we only packaged Percona Server and our stuff for a couple of operating systems, if you want to use it on Alpine, for example, we don't package that, but you could do it, and you don't have to have any relationship with us to use it or support it. So I think that that is an important thing is like if you have a vendor that is a that you have to have a relationship with, like you're seeing with some of these non-open source licenses not like what Red Hat did, where they're not distributing the sources freely, but more of the SSPL or be BSL where it's like, you must deal with us if you want to use this. Yep, those are real bad, in my opinion, kind of constrains people's control. Getting back to the theme of the podcast, their control their data, right. Yeah. When you're talking to people who are using Alma, are you seeing any trends for types of workloads? You know, like so, obviously, my vision is focused on databases these days, but I'm wondering like, do you have any, any insight into like specific industries like since it used to be real big with supercomputing, for example?

**benny Vasquez:**   

Yeah, yeah, we're definitely seeing a ramp up of supercomputing for Alma, where I think we're on the top, there are on six of the top 500, high, high performance computing servers that are used all over the world. There's a couple in Germany, a couple in there, I don't know they're all over the place. And those are just the ones that are reported, right? So for sure, we're seeing high performance computing, we're seeing web hosting, we're seeing I'm hesitant to name names, because I don't have any official relationship with these people. But I can tell who's using them by who's coming in to ask questions and that kind of stuff. So we've got we've got Telecom, we've got, like internet providers, we've got, like, all kinds of big, like names, you would know doing video, and then like video production and big. How do I say this, like movie producing studios.

**Joe Brockmeier:**   

We've got in the old days, we would say things like, North American company with a mouse mascot, or something. 

**benny Vasquez:**   

It's that kind of stuff. Like we're, every day I'm finding somebody new today there was a big audio company that has nothing to do with like it in general. They produce, um, um, like, like stuff that you would wear in your ears to listen to music sort of stuff. And they're, they're in our chat asking questions today. And that's the kind of stuff that we're seeing is we are being picked up because we're available and usable and stable and trusted.

**Joe Brockmeier:**  

Okay. Do you see, you know, what do you think about the trends of more and more things going into the cloud is, is a common thing, like any thoughts on the trend of maybe they're running on Linux, but they're doing it with a cloud provider? Where, you know, by the way, the podcast name comes from a guy named Dave McCrory, who coined the term data gravity a few years ago, many years ago. Now, back in the remember, when big data was a thing for like, five minutes basically, the more data you have in a service, the harder it is like a black hole, the harder it is to get out. Yep. Any thoughts on that? Like, just around I, there's a big, you know, kind of hairball of a question. But yeah, any thoughts on the data that's hosted in the cloud? And how organizations can control their destiny there?

**benny Vasquez:**   

For sure. Yeah, I think we are certainly seeing and have been over the last, you know, at least five years, more like 10, a move toward the cloud native approach to basically everything like when, when AWS East goes down, you see who's using it, right? Because a number of applications just stop working. And like, oh, that's why Spotify is being dumb. That's why this is happening. All of that kind of stuff. I think that one of the things you don't really think about when you're choosing the applications that you're using, is that all of your data is stored somewhere that you're not at all in control of. And will these applications using the cloud native approach or any kind of cloud development, it's, it's certainly a concern, especially, I don't want to I don't want to rag on Microsoft too much.

**Joe Brockmeier:**   

But, but a little, you want to do it a little bit.

**benny Vasquez:**   

They had that that big compromise this year, where a bunch of data was very open and very public and not in the way that you want it to be. And you might not get the notification because they will sell their customers. Right. Right. But their customers are still, you're still relying on them to tell you. And it's its a much bigger problem.

**Joe Brockmeier:**   

I always call that an internet snow day when a major service goes down. You know, it's basically one of the one of the sad things completely unrelated. But one of the sad things about being an adult is no more snow days, you know, especially as a remote worker, right, exactly.

**benny Vasquez:**

I won't get to my desk is not an option.

**Joe Brockmeier:**  

Exactly. It's like do you still have internet and power, Brockmeier, then get to work. I always avoid though knocking too hard at anybody else having a security or whatever, because everybody gets a turn in the barrel. Yeah. If you're making fun of your competitors, or something, don't wait. It'll be your turn one of these days. Yep. Okay. Any thoughts on databases and that kind of thing in general, like anything, any trends that you're seeing you're, you're in a great spot, for example, to see, you know, adoption of different things, for example, any thoughts on the perpetual foot race between MySQL and Postgres?

**benny Vasquez:**   

Interestingly, because of our approach to data in general, we don't get to look at those kinds of trends, because I'm not tracking what anybody is using. I can tell how many servers are getting updates, but I'm not looking at individual packages, that kind of stuff. But I can definitely say it's been as somebody who's who spent a number of years as part of the web hosting industry. It has been interesting to watch the shift between MySQL, MariaDB, Percona. Like everybody shifts around. And it's, it's almost always this feature that I want, isn't here, I have to go over here now. And it's, I think, really indicative of software in general. That if you meet the needs of your users with features and security. 

**Joe Brockmeier:**  

That's who's gonna win who like the Debian Popcorn type thing? Or anything where you're tracking to see these packages are most installed or anything like that?

**benny Vasquez:**   

Nope, nope, not yet. It is one of those things that we really struggle with philosophically. Because I think that it's if if we say, on one hand, come use us, because we don't require a license agreement, and we're not going to nefariously use your data. On the other hand, if we start tracking that data, how do we ensure that that data stays safe, doesn't get compromised like personal information, there's all the PII worries, I don't want any of that. So that means that we have to get very specific and very granular, and that's not Anytime somebody's asking for data about what's being used. That's my counter is okay, we can start doing that. But you have to do all of this other work first.

**Joe Brockmeier:**   

And if you don't have it, you can't use it or abuse it. Right.

**benny Vasquez:**   

Exactly. It can't get compromised, because I don't have it. I can't use it, because I don't have it. Fair enough. Fair enough.

**Joe Brockmeier:**   

All right. One thing, we're kind of coming towards the end of the time here, but one thing I always want to ask people is so what haven't I asked that you would want to talk about on this or similar topics?

**benny Vasquez:**   

That's an open question.

**Joe Brockmeier:**   

It is I like to open the door wide, because usually, I like to think I'm okay at coming up with questions. But you know, I know that. I don't, I don't know everything to ask all the time.

**benny Vasquez:**  

I think one of the most interesting discussions happening right now in open source, especially, is around what AI looks like, as an open source anything, because you've got this wide world of both the engines and the data that they're trained on? And how do you define what is or is not open source? And so I think that I mean, I'll put it, I'll put it back on you, where do you think we're gonna go with that? How does that going to kind of play out with all of your, like corporate open source knowledge?

**Joe Brockmeier:**  

That's, well, that's a probably billion-dollar question. That's not $1,000 question. I'm really hoping that we're going to see a strong push towards actual open licenses, I'm not sure how to treat the data, especially given that the datasets, I'd like to see more datasets that are trained on things where people have, either it's public domain, you know, look at all the stuff that's in like Project Gutenberg, you can train anything you want on that, because it's all public domain, or where people have consented to say, yes, you may train your AI on this. You know, as somebody who has done a little bit of writing over my career, I feel some kind of way about people training things on my data. And the other interesting thing you got me on a soapbox now is that people have this. Depending on, they have different ideas about it, depending on who's doing it. And I want to have a very, you know, it should be the same rules for meta and Microsoft and AWS, as it is for, say, the Internet Archive. And if I don't think it's okay for meta to do it, IA shouldn't be doing it and vice versa. Like if the holders of copyright don't want to give the permissions to Internet Archive, then why should Microsoft have those permissions for my data?

**benny Vasquez:**   

Yeah, I think that consent thing is going to be the biggest concern in the next, you know, five to 10 years. I think that's where most of the litigation in AI is going to be. Well, I never said you could use it, I realized I didn't say you couldn't use my data. 

**Joe Brockmeier:** 

My official position by the way, my official position is I wish I had gone to law school because I know where there's a lot of money to be made in the very near future. Unfortunately, I'm not poised to make any of it. So yep. On that note. Cool. Any last thoughts?

**benny Vasquez:**    

No. Thank you for having me. Well,

**Joe Brockmeier:**    

I really appreciate you being on, and it's always fun to talk to you. Once again. You've been listening to data gravity. I'm Joe Brockmeier, the host of Talking to Benny from AlmaLinux. And we'll be back with another episode soon. Thanks very much for listening.
