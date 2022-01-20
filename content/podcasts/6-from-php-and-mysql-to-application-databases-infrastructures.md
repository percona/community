---
title: "From PHP and MySQL to Application, Databases, Infrastructures - Percona Podcast 06"
description: "The HOSS sits down with Gabi to talk about her journey from Brazil to the US, how she broke into the tech space, and how she ended up at Google."
short_text: "Gabi’s role at Google is to help developers get the most out of their applications, their databases, and their infrastructures. She has been a long time community member helping people in the PHP and MySQL community for years. The HOSS sits down with Gabi to talk about her journey from Brazil to the US, how she broke into the tech space, and how she ended up at Google."
date: "2021-02-22"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep06-featuring-gabi-ferrara-dev-advocate-at-google-and-talk-about-open-source-databases-php-and-more/"
youtube_id: "cD_w7kUcWKc"
speakers:
  - gabi_ferrara
aliases:
    - "/podcasts/6/"
url: "/podcasts/6-from-php-and-mysql-to-application-databases-infrastructures"
---

## Transcript

**Matt Yonkovit:**  
We're here with Gabby from Google. We're here to talk about all the cool things that she's been doing. And maybe goose catches up a little because it's been an age and a half since we've seen each other at a conference because we can't travel anywhere. We're all just stuck at home. So Gabby, how has home been treating you? And maybe tell us a little bit about what you've been working up?

**Gabriela Ferrara:**  
 So I think the last time I saw you were on Percona Live 2019.

**Matt Yonkovit:**  
2019hHas it been that long? 

**Gabriela Ferrara:**  
Yeah, 2019 and that was the first one that you've made outside of California, right? 

**Matt Yonkovit:**  
Yes. That was the first one outside of California. 

**Gabriela Ferrara:**  
Yeah. So yeah. I met a lot of some people there. I did talk to many people that on all my talks. There are other more interesting talks. But like I'm, so I don't have people, for people to know me. I'm a developer advocate at Google. So what means is, I am not sales. I'm not marketing, what I like to describe, I am a software engineer that teaches other software engineers, how to use our products, but not on like, you have to use it like places I talk about MySQL, which doesn't belong to Google. It's kind of like Percona in that regard. Like we don't own MySQL yet we talked a lot about it. Right.

And you contribute to the source code, sometimes with bug reports, I have seen? 

**Matt Yonkovit:**  
Oh, yes, we do a lot of contributions. We also have our own versions. But yes, yeah. 

**Gabriela Ferrara:**  
Yeah, I know. I do open some bugs. And I think there's wants to open down that. But whatever it was,

**Matt Yonkovit:**  
 There's one open with us. There's a bug open at Percona or with MySQL?

**Gabriela Ferrara:**  
 MySQL. 

**Matt Yonkovit:**  
So, Gabby, you do a lot of connecting folks to the right technology, helping them.  guide, I think I know, you have office hours. Yeah, people can show up and just ask you questions. They can schedule something, right?

**Gabriela Ferrara:**  
Yeah, it's free. So you don't need to worry. Oh, well, credit card information. 

**Matt Yonkovit:**  
So you don't charge them anything? Just they're talking?

**Gabriela Ferrara:**  
Yeah, it's actually a Google Pay for it. 

**Matt Yonkovit:**  
Oh, it's Google-sponsored free advice from them. 

**Gabriela Ferrara:**  
It doesn't need to be about Google products at all. Like some people come to me and like, oh, I'm using RDS for this, this is fine. And for me, it's also cool because like, I don't have as much time as I want to do research on others. I don't see competing products, but other platforms because I like, as I said, as I do talk about myself. And they've stopped in love with those guys to a law that we can't log with me, although there are some other things going on. But not they are the subject here. But particularly between us the demo community, we're very, very friendly. So I actually love hearing about other people's problems on the platform. So I can not like a spy but mostly say how can I avoid to happen?

**Matt Yonkovit:**  
You're not a spy?

**Gabriela Ferrara:**  
I'm not. I'm not. 

**Matt Yonkovit:**  
Okay. Okay. I wanted to clarify because you said,

**Gabriela Ferrara:**  
Yeah, lawyer cats. I'm not a spy. Now actually. There are some agreements that we can use. So like, if you notice a blog post on Google launching a product, and there is a product from somewhere else. Have you noticed that the access never has numbers? 

**Matt Yonkovit:**  
Oh, yeah. That's okay. Interesting. So, Gabby you've been in the MySQL space for a while you've been helping people, maybe tell us like are there some really interesting things that you've been seeing lately, some, some trends, and what people are using, how they're using it?  I know you've been working a lot with Spanner, for instance maybe what sort of things are you seeing now is the hot topic. 

**Gabriela Ferrara:**  
So, um, so just a puppy. That was because the other day for our person from called would say when I would say this way, he would always correct me. It's called Spanner. Spanner. It is there is a spanner. The Spanner Spanner is the eternal version of Google. Cloud Spanner is the external version that customers can use. 

**Matt Yonkovit:**  
So, thank you for clarifying.

**Gabriela Ferrara:**  
Yeah, I see the same thing. But it's not the same thing. I'm been helping them because it's nice specifically because I usually prefer open-source technology. I have a lot of enterprise customers. And one thing depending It doesn't depend on the size of the customers, I think Percona has the same. People asked me, How do I manage my schema migrations? I'm not talking about moving from RDS to cloud SQL, or from Azure to AWS. I'm talking like, how do I apply? I don't know when I add a new column. How do I do that on my pipeline, because, what a lot of people have is like they have a monolith? Remember, they say the DOM. But even though it's a microservice architecture, you still have to have a main application somewhere. And usually the main applications, we have the database migrations, and that can be in Java using hibernate could be in Django, use another form a job with enough SQL alchemy or whatever. There is a PHP you can use doctoring alarm. So rails, you use active record. So like, every language, MyFramework has its own migration tool. Yeah. And that's fine if you're only working with that one. But we're just having microservices that technically shouldn't, but they are connected to the same database. And that happens a lot. So I'm not here to tell them how they should run their business. Because if it, they'll give me their money. I have no position to give them advice. They know it better than me. Yeah. So if they're doing that, which most people are doing, I'm like, so you're gonna deploy your microservice code, and I need to change a database. So you're gonna have to deploy in two different places because the migration is on the application. And the thing is, on the other. And, if you don't do that, how like points is clean checks before, if the database schema is the same, and rails are the same. So yeah, you need to keep that on the main applications. It's gonna flop whenever now. And anyway, just say like, what? So what I've been telling clients is like, if you do microservice, for any scale, you should treat your either migration as a microservices zone, or whatever CI CD pipeline to deploy, not tie to your main application or your microservice code. And one of the main tools that I like coding is one is Liquibase, which is there's an open-source and paid version, and Flyway, which I don't know how it works much but also there, as far as I know, both Java tools, that it doesn't matter, because like if you're using GitHub actions, you can connect another container, and I have a container running Liquibase, which I like, you don't have to install Java or whatever, whatever to run, it's Azure. And then have a specifically a repo, let's say, more your migrations, and then your relations. So it's kind of like, I don't, I know, for case changes according to the company, but it's just an example like a simple example on how to do that. And you notice, as I GitHub actions, which is obviously the executive, I don't try to push that that's why I like being an advocate, I don't have to push,

**Matt Yonkovit:**  
right, you can, you can let them choose. And you can kind of guide them to different the best solution for them. Right. So the best solution for the job. And  it's interesting because this is a problem that has plagued developers,

**Gabriela Ferrara:**  
I hope to have that. Yeah. 

**Matt Yonkovit:**  
Oh, yeah. In the new version of MySQL, 8023 actually has invisible columns, which is very interesting, because it can help this a little bit because you can actually add the columns to make them visible. So applications that decide to do a select star or frameworks that decide to do a select star will often break with some of those new columns unless things are fixed in the application.

**Gabriela Ferrara:**  
I Didn't work on the new version yet! Yeah, didn't have time. 

**Matt Yonkovit:**  
You haven't looked at the new version. Oh, fall behind. Hmm.

**Gabriela Ferrara:**  
I am. I told you, I have too many to do. 

**Matt Yonkovit:**  
Oh, that's okay. That's okay. Oh, by the way, many people might be wondering why we're wearing propeller hats today. And so the reason for the propeller hats is because I love attention. And I always strive to get more attention at conferences, years and years ago, I wore this hat. This is actually a prize for an internal Percona thing at a conference. And I wear this hat at the conference. So people would find me, right. And so it'd be like hey, just my guy with the propeller hat. And then when I stopped wearing it, everybody complain. And so then it became a thing where everybody wanted me to wear the hat at conferences, and there'd be like, I don't recognize you that your hat. Where's your hat? And then I wore it and I never got to take selfies with me. And so now it's just kind of like got a life goes on. And so now Gabby knows me for the hat because we've 

**Gabriela Ferrara:**  
And it's funny because even with onboarding remote people still getting their Propeller hats

**Matt Yonkovit:**  
Oh, yeah. Well, because everybody wants the hat. it's gonna cool. Yeah, yeah. Well, you got a new girl I got her. So I don't know,

**Gabriela Ferrara:**  
Well, if I go to a visibility tool at the conferences if you notice, I always have ties. If you look at talks that I have on YouTube, all most of my talks, I'm using a tie. I'm British and I wear a tie.

**Matt Yonkovit:**  
And it is one of those ties though, that you could put like the beer and they have beer ties? I don't know if you said 

**Gabriela Ferrara:**  
No, it's a real tie male tie. 

**Matt Yonkovit:**  
Well, I'm just saying though, but you can have a tie that will hold your beer while you talk. 

**Gabriela Ferrara:**  
No, I don't drink beer, though. 

**Matt Yonkovit:**  
your soda, or your water bottle, or your anything. There are bottle holder ties. I'm telling you like it's worth trying to explore. 

**Gabriela Ferrara:**  
Well, I live in the US so you could put a flask on

**Matt Yonkovit:**  
there are all kinds of, I'm just saying it's a universe. It's not only a time. It's also a beverage holder, which is fine. 

**Gabriela Ferrara:**  
Oh, gosh. No, but it became like because fortunately, my brains work weird ways. And I would still makeup and stuff like that. But it was a fitted shirt. not different. Like this ones like lumberjack show. Oh, um, I use a tie because he would actually make me people will think I would know more what it's the bias and cushions by though like she's dressing more masculine. So she probably knows more. And that works. 

**Matt Yonkovit:**  
Wow, that's crazy. 

**Gabriela Ferrara:**  
So this is where I didn't wear the tie. I got a lot. Well, actually, and even people interrupting me that need to talk. Yes. People want to ask me this. And when I was to talk, the tie people I was with come in I was at the sunrise site, I thought I was able to match the color scheme with my presentation just to make it a bit of fun. But people never will actually know when I was with it, they would ask questions, but it was more respectful. So it may be how causation or correlation thing but like it's too much of a coincidence to ignore. 

**Matt Yonkovit:**  
No, that's, that's, that's horrible that you'd have to wear a tie to get like some sort of respect. 

**Gabriela Ferrara:**  
I mean, that's just that it's the unconscious bias.  I know. 

**Matt Yonkovit:**  
Well, just realize that I will question you whether you have a tie on or not because that's the way that I am. I am an equal opportunity complainer so just an FYI. 

**Gabriela Ferrara:**  
Oh, yeah. I remember I remember when I went to PHP UK once I live in the UK and never thought that would be we never or anything and Morgan Tucker or co-working article and he'll always developer who knows that at that time five-seven was still the main version and it this me off that the Oracle documentation at a time for the Senate columns. They didn't exist five-seven. So like I had a problem with her it was a big database at the time has 12 million rows, and we needed to order by to the Senate. And even though the syntax allowed to be the sending, it took me days to realize it wasn't doing the same wasn't working, right. No. And then I rented accommodation. And I was like, oh, and I a lot of my talk was saying this. Sorry, my dog is barking. That's okay. It would say although that risk is acceptable, same tax. It's not implemented yet. Okay. Seriously? Seriously. I just saw I asked Morgan was like, dude when you're gonna implement it.

**Matt Yonkovit:**  
That was implemented for you specifically?

**Gabriela Ferrara:**  
I don't think so. I think it was already coming and he couldn't say anything, but like, I put all my ducks I finally had the sun enough and people don't get it. How do you know that thing was for me? 

**Matt Yonkovit:**  
Well, it's those little things though. Right? Like it's the little things that matter and when they don't work, right. They're just annoying, right? They just like, Ah, I'm so annoyed.

**Gabriela Ferrara:**  
I'm like, why is it like if it doesn't work? Why don't I get a winning

**Matt Yonkovit:**  
So Morgan that tie DB now again?  Yeah, he is I actually just did a recording with him a week ago. And so that'll be coming out shortly as well. So I, but I didn't know to give him grief on that. And so next time I talked to him, I'll make sure that I'll bring it up.

**Gabriela Ferrara:**  
He doesn't remember that I did, because he bought me or asked for a lot of people. Oh, okay. I talked to him about after when I joined Google, I was like, I'm still sorry, they're off doing a conference. He's like, I don't recall. He was like, fine. 

**Matt Yonkovit:**  
Well, so Peter used to harass me during my session, just Oh, no, like, Oh, yes. Like, like, like, yeah, he was very bad like he was, I would be up there. And I'll be like, so if you look at this benchmark here, and he's like, your benchmarks wrong.

**Gabriela Ferrara:**  
It's like, no, like that. I like it, wasn't it when he finished his talk? after he finished everything, I'm not like, I don't like it? Well, as I said, a lot of people love doing well, actually, and I don't like when people do that to me. So I've done did that to people. So this question that I visit with the person I actually take them aside is like,

**Matt Yonkovit:**  
So are you coming into the Dev role? You spoke a lot before joining Google. But how did you get into the dev rel role specifically? 

**Gabriela Ferrara:**  
Well, I would like to say it was organic, it wasn't. So it wasn't like I wasn't in Brazil at the time, my English was way worse. And you'll see that I have a lot of grammar errors, pronunciation errors because I learned English on my own.

**Matt Yonkovit:**  
Hold on. I was born in the US and have spoken English all my life. And I have more grammar errors than probably anyone else. I know. So don't feel bad. Like I'm just saying, like, like, like, I'm horrible at spelling and grammar. That's not my thing. But anyway. 

**Gabriela Ferrara:**  
So I learned English on my own. And I want to as being the talker, woman in most companies, like I was, like, I noticed how the Brazilian societies and I were like, I don't want to work here anymore. I want to get. So then I started thinking how people can like actually hire me, like, actually wants to hire me. And they thought they don't know why they would hire me. They don't know me. So I started applying to conferences to speak at that about software engineering databases, which was doing I wasn't a data engineer, that mostly works with databases. So whether you use PHP, where people are mostly using MySQL, I used to, I even have a blog come out, like I used to hate MySQL. So like, I was like, okay, that's okay. Like, it's for the greater good, I can talk about it. But my objective was, how to help developers do better with the database because people have a lot of assumptions. And most of the time they're well because I think SQL and the ORM are going to do all the jobs they need, and they don't need DBA your data engineer to help them at all. That's how I come from the developer side. And when I applied to Percona, I didn't get the job by the way, because I didn't know the operation much. 

**Matt Yonkovit:**  
I remember we talked I was very nice to you. 

**Gabriela Ferrara:**  
No! I am not complaining but that's usually why was biting me back was the fact that I didn't have much operations experience or much more developer experience. 

**Matt Yonkovit:**  
Yeah, and were painful. 

**Gabriela Ferrara:**  
Your background is a bit different from what I was doing. So like it says, Yeah, I just wanted to make fun of you. So anyway, so my it was a thought process so I decided people need to know me I need five so I said a blog posting more and applying to conferences. And so someone decided, hey, let's say there's a topic that there is a problem though. I live in Brazil, the conversion of dollar Brazil to the dollar it's so like whatever you think a lot of money is easy like a low paying job is in the US. I was making the last

**Gabriela Ferrara:**  
Even though for Brazil, it sends a good salary, but it's still I had to buy the plane ticket the hotel Oh, yeah, I could only the conferences that that could pay for my travel. I don't mean pay me as a speaker but pay for my travel. 

**Matt Yonkovit:**  
Yeah, I mean, that could get expensive with all a lot of travel. 

**Gabriela Ferrara:**  
Well, before joining Google, every talk I gave was, when they cover the I couldn't do it that I couldn't attend a conference at all, honestly, because conferences are not cheap, you know. And that was my way to network. And that's how I said it. So it was a conscious decision. So my first step was to get near. But I wasn't thinking about that, specifically, I just wanted to be hired as a software engineer. So I could get out of my country and have a better life. Because I helped my family and stuff like that. So it actually work, I got my first job a year after that, and I set it up with, and honestly, it wasn't good company. But let's say they took advantage of the fact that was an expat, like, offer me less money than I could have been making. But also I was in a bad situation personally, in Brazil, I wanted to get out. So I was like, Whatever I'll figure that that's probable future me. So let's take this opportunity. And after that, like I started doing more talks because it's much more do people might know you and like, then I started diving into MySQL 8, and one was like, now I have blog posts for like, an 801. Like one was also previewed or whatever. And that was the problem. 15,16 when they started talking about it, right, and also be following it because I wanted to be inside and be a reference about it. That's why I say oh, they already have a new version. So as you're getting behind, they're like, Yeah, that's true. But that's how I joined Dev's role in the end. Then it was to do ask for personal reasons. And couldn't work because of these reasons. And I do I could still do speaking engagements. But I couldn't have any compensation for it. Because  But they didn't want to in Washington, DC, Php role. To me there, he paid for the hotel. And I, the only thing I didn't pay for was the ticket. And like, as a speaker, I don't think that counts as a paid engagement.  like, I'm gonna pay for my own ticket. Yeah. I mean, there are conferences that do that, but there isn't, it's completely different. The ticket is usually way cheaper when that happens.

**Matt Yonkovit:**  
 So, let me ask you this, right. So there are probably many other people who are in a similar boat to what you were early on, right?  maybe they feel like they're there. They're in that male-dominated world, they're in a country that they don't necessarily think that they can thrive in, you have advice, like going through what you've done, like, what would you do the same or different? That might help.

**Gabriela Ferrara:**  
So, like, I get sometimes a bit of criticism, because like, I write articles of videos all in English, I don't do in Portuguese. And although people say they are learned by this house didn't have a lot to learn, because community help if someone were to dock someone made the job of translation, I like the PHP docs in Portuguese, or, like, actually, on the fewest languages that I went to was didn't know English yet, was the only language that I could actually learn because they had a Portuguese translation. So just to peddle it back, I get a lot of criticism, because I don't give much to my own language the Brazilian community itself. But I'm going to be honest, mostly because I forgot Portuguese.

**Matt Yonkovit:**  
Oh, okay. Okay,

**Gabriela Ferrara:**  
The terms like sometimes there is no translation like, and sometimes new concepts. And like, I don't, I don't want some pedantic mixing Portuguese of English and a lot of natives Zealand, I don't like. So they're very protective of the language. So first of all, learning a second language, like, English is going to be the easiest, because even if I move to Germany, whatever, like, if a Google is something technical, the chances are that you're going to find something. If it is a Google and English.

**Matt Yonkovit:**  
Yeah, yeah.

**Gabriela Ferrara:**  
That might be English, usually too. So but being able to show like, people say, Oh, I hate those of us and do GitHub should be your resume. Don't fall for that a lot of people work for private companies where, especially if the price, you don't publish your code, as it talks about projects, but you have NDA signed so you need to show that you're good. Yes, Github for like, that favors, mostly males. Because I was joking women, we have our own job, or house job, no stuff for the house, and also need to look pretty too. So we have three jobs. Male, they just have one job, which is doing their job, they don't shave, they don't do dishes. I'm not saying all males, but so expect them to be someone that has three jobs who also do open source, it's a fear, in my opinion. So so like, it's, unfortunately, you're gonna have to get on the burden to study on the weekend. Because you don't have this same privilege as other people, like I did all my talk. So my spare time, I would do traveling on my vacation time, even though it was for conference. So, unfortunately, if you're an underrepresented group, that is women, you will have to work double because we don't have the same starting point as other people. And that's something, unfortunately, depends a lot on the personal spirit. So that does have a rule, you're gonna have to figure out what is your best cadence to reach a goal? So I would say, put up a long go and then say, How do I get there? And so let's say like, my goal was, I want to get out of this country because they don't value my work. And so how did I get there? Oh, people need to hire me for what they need to hire me. So like all the thought processes ago, even the problem solving, so how do you get there? And not say, speaking at conferences is gonna make you maybe just going on with your halftime, go to the GitHub documentation? And people say, are just going to be jobless? Yeah, a lot of this stuff is very, very, very close. Like it's a club, it's hard to get it. So you can just Stack Overflow questions. You can do like documentation people spot like saying, Oh, that's not good. Yeah, I guess, started the documentation, get to understand a lot of the project. And in the future, you get to do actually meaning coding, contributions. So I think Doc's people dismiss it, but like, I think it's good to learn a bit about the project. And then you get a reputation of the maintainers. And then you can actually do something because as I said, it is a club, it is not as open as people think it is.

**Matt Yonkovit:**  
Well, so what can we do as an open-source community to be more inclusive? Like, what do you think would be the good first step for maintainers, or projects, or for the open-source teams that do have more responsibility? How do we open those clubs up?

**Gabriela Ferrara:**  
So it's a bit of a double sore because I know a lot of open source maintainers and that will are all people that would like to come to, to contribute. But like, let's talk about a good analogy. As we walk in tech, how many recruiters emails do you get per week,

**Matt Yonkovit:**  
the whole email, just email just

**Gabriela Ferrara:**  
faster was just a message, hey, let's connect I work or like, I work for this meeting. You start up I have this project that has blockchain every time someone says blockchain has sent this path. Okay, like, as something new? I'm sorry, my mom's calling me!

**Matt Yonkovit:**  
We're on if you want.

**Gabriela Ferrara:**  
So, as an open-source as something new we get, we complain about recruiters, right? Yeah, it's one of those it's a good problem to have. So I think that's the same thing that happens to open source maintainer is, they get a lot of pull requests. And honestly, sometimes they're not good to pull requests. I understand that. But sometimes someone is just being honest and trying to reach you. So that's to say that the whole sort of question because like, you're almost any having someone that's some type of inexperience of project, it's all No, no, I have this site person that does a lot of other projects and gets like, hundreds of dollars per week. So they're jaded, and you're trying to, it's up to the wall to overcome so I see both sides and understand both sides. But like both of us, both sides need to have empathy. And that's what I like about that file. It's like we are, we think about empathy at first. So even though you may be ravine it's hard. And it is energy-consuming. And like putting yourself in someone else's sues, even though their code may be wrong. And honestly, nitpicking, because I just have no Like, if it's just some lip balm one yourself the length of fix the PR, I don't diminish someone else's work just because Oh, you use two spaces settle for but like seriously like that to my issue with the whole thing? Like, do you have a late on your project because if you don't have set up on your open source project only know that that's why you're doing this in the first place.

**Matt Yonkovit:**  
So this is where Yeah, I think that one of the things I've been thinking a lot about around trying to get more people more diversity in the open-source space is really about mentorship. I mean, there are so many people who know how things work. But you're right, like a lot of them are busy. I think that there needs to be a real concerted effort to dedicate time to help people and that doesn't necessarily just mean that quote, it could be  you mentioned speaking and getting speaking spot like helping people polish their presentations, or,

**Gabriela Ferrara:**  
yeah, that's the question there is some I know the PHP community has a website, I don't know, it's like, helped me CFP helped me abstract, I think that is the name of the the website. So it's a media talk. And there are, well, people volunteered to help you create an abstract for your thing. And also, actually, you can, if you know the conference organizers, it's hard to know, but like, usually when you're doing most good conference and being has like this thing for the abstract and an extra box, we say that this is for the people analyzing the CFP, say hey, like me, English is not my first language. So if there is any grammar, I can fix it later. But that's what I meant and that's the goal of the stock. So like, sometimes it's not as clear, and talking doesn't mean it is bad talk. So maybe adding the extra food so people can explain a bit about more of the talk that you want to give because it abstract has to be like, let's say clickbait so one just shows an abstract, it shouldn't be the only thing I think conferences organizers should be looking at. But also contention. And that's why the extra box, it's good and also says, Hey, I know you have a lot of talks to look for. But this is my third show of this talk and gives a bit of background, though, right? And I say they're just saying like, this is my goal. And if it is not grammar perfectly, or if there's something wrong there, it's out of like, lack of knowledge for the language or that kind of thing. So people can actually put themselves in your shoes because as a woman just think like, oh, they don't know what they're talking about. Yeah. And the problem is that we are so dismissive. If someone gets some part of the lingo wrong, you know?

**Matt Yonkovit:**  
Yeah, we have to be mindful that we have to assume really good intentions, we have to treat everyone with the same respect we would want to be treated with. Right, and it's very important.

**Gabriela Ferrara:**  
One analogy, just to finish, not about that, we are gonna do another Percona tools is one for migrations actually, like any look. Yeah, so I never use that. I'm gonna be honest, but like, I was talking to a friend that started using GCP at their job. And they're like, Oh, how do I do? I'm klutzy, which is a part of what I do, how do I like to change something without having downtime, like a big change That's gonna take hours. I lock tables, with rows, whatever, whatever. So how can I run this on a replica? And then like, promote that replica? And then I was like, I was like, Look, I'll console specifically I don't even RDS you can do that because once it is a replica, it is read-only you cannot change it.  like, that's the purpose of a replica. It's it is not to be changeable. So you're gonna have to compromise it, though them like, and then I started giving some examples that could, I don't know, create a new column. You mentioned the new invisible columns. That's a good example of how to do that kind of thing. But like, I didn't know about that. stuck to that was new. It's brand new. It's very new. But this advice I also thought about relational database-agnostic also was on my on MySQL would be the same person. So like, if you're planning a column, and it usually is an online operation, you won't have any problem with locking rows. Of course, there are some specifics like if it has a default value, so things change, but roll it out. If you're just an opinion column like five But I feel like I want to change the type of a column that's a bit more tricky because like, you're, let's say you find great brigands. And then like, impulsiveness. For instance, if you have a foreign key that's integrated with only kings, how big it actually accepts MySQL compliance. So like, depends on the database. So let's say you want to increase rates to begin, it's gonna be a locking row operation because it's gonna have to change copy the whole table, you know? So like, well, if it's not the primary key, let's say it's another column, you can create a new column, create a trigger, an adult triggers all the triggers. And I went through a whole algorithm on how to do that. And then like, oh, that's PT. It's all about the tool. And then I look at about oh, that's the whole idea. I'm good.

**Matt Yonkovit:**  
You, you reinvented pt online schema change.

**Gabriela Ferrara:**  
I mean, I didn't implement it. But that was the whole algorithm that I talked about, I mean, one tweak thing, I didn't test it. But like, it was, that my point is, like, I want to talk about the lingo. That's where I don't want to get, I didn't know the right thing to look for. There is already a tool that does that. But they didn't know so it doesn't mean I'm a bad engineer for not knowing it, but I knew they were worried. And my algorithm was basically the same. So am I a bad engineer for not knowing that?

**Matt Yonkovit:**  
oh, no, let's be honest. There, there are hundreds of 1000s Millions of tools and projects. There's no way you can know them all. I mean, just MySQL, if you got to get a hold of MySQL, there are over 140,000 projects. And how many ha projects there are? Over 1000 High Availability projects? So Wow. Yeah, yeah. So, so figuring out, like, what's out there? Could somebody have done something that you have an idea? Sure. I mean, I guess they could look for that. Oh, you care? Like, honestly, like like, I mean, go out and type in MySQL, and use MySQL ha. But even that, like, if you get 2000 results, you're not gonna go through all 3000? You're gonna be like, alright, yeah, maybe you'll look at the top-rated ones. And if it doesn't do what you want, then you're just gonna say like, oh, I need to write it. But yeah, it's an interesting dilemma there, because there is quite a bit of stuff out there. But I mean in terms of like, understanding like the toolsets the change how it's referenced. It's one of the benefits and drawbacks in the open-source space is you can create anything rapidly, you can start to prototype, you can start to fork you can start to modify. But then you have kind of this Hydra and all these tentacles that you might not be able to know what's actually out there and what state it's in. So it's a challenge.

**Gabriela Ferrara:**  
Yeah. And then I mentioned my friend who works at Gilad is like, Oh, I think, I think, ghosts, the one for GitHub. Okay. Yeah. It is like, it does the same thing. I was like, didn't know. Like, but then it's, like, I have my job to do I want to do at home and super phases like I cannot possibly be open source projects out there. 

**Matt Yonkovit:**  
It's challenging. It really is. I mean, like, as I said, there's so much it's crazy but Gabby, I know that I know, you told me that you had a meeting in a few minutes, so I don't want to make you late for talking to your boss. Yeah. Yes, yes. I don't want to make you late for that. That is That would be horrible. But I do appreciate you coming on and chatting with me for a little while. Thank you very much. I appreciate you being open candid with us and also for talking at Percona lives in the past and appreciate that.

**Gabriela Ferrara:**  
Yeah, I love working out I love every time someone asked me. So the Percona people they're good about.

**Matt Yonkovit:**  
We appreciate.

**Gabriela Ferrara:**  
Oh, no, I always I'm referring people to you as soon as I don't know if they say oh, Gabby send me here. Well, I'm always referring them to you.

**Matt Yonkovit:**  
Here is Gabby's scorecard. It's like maybe we should provide your coupon code. Like yes, yeah. We'll give you a Gabby coupon

