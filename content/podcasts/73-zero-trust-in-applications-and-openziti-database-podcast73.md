---
title: "Zero Trust in Applications and OpenZiti - Percona Database Podcast 73 with Clint Dovholuk"
description: "Clint Dovholuk stops by to talk about Zero Trust in Applications, and how it can extend to the database.  He gives us an overview of OpenZiti and explains some of the bigger security-related issues in the tech space"
date: "2022-06-09"
podbean_link: "https://percona.podbean.com/e/zero-trust-in-applications-and-openziti-percona-database-podcast-73-w-clint-dovholuk/"
youtube_id: "Lw7h48RkDmI"
speakers:
  - matt_yonkovit
  - clint_dovholuk
---

## Transcript

**Matt Yonkovit**  
Hello, everyone. Welcome to another HOSS Talks HOSS. I'm the HOSS Matt Yonkovit, Head of Open Source Strategy here at Percona. And today I am with Clint Dovholuk.

**Clint Dovholuk**  
Nailed it.

**Matt Yonkovit**  
Oh, I practice all day long. And so Clint is from NetFoundry. And a couple of folks from NetFoundry are going to be at Percona Live, they're going to be talking and they have a product that kind of piqued my interest here. Now, Clint, I've been talking about security and databases for a while, specifically, because I have had my data breached so many times, and my daughter has an inheritance of free credit monitoring. And I'm pretty sure my grandchildren will eventually have that as well.

**Clint Dovholuk**  
You might consider using a firewall

**Matt Yonkovit**  
It's my data breach, right? Like, someone else's. Someone else has my data out there. I wish they would protect it better than they are. Right. Very true. But oh, my gosh, yes. you can't turn around without seeing data being leaked all over the place database, database breaches. This that the other thing, and it's kind of a weird space we're in. Because we want more data, we have more applications than ever before, but then we're doing a really crappy job and keeping it secure. So I think we're in that weird space. And I know, there are all the buzzwords around Zero Trust.

**Clint Dovholuk**  
it's the buzziest of buzzwords right now

**Matt Yonkovit**  
Maybe you could tell us, what does that mean? Like, what is Zero Trust, and how is it related to the database side of things?

**Clint Dovholuk**  
 Yeah, sure. It's a great way to start off. So the first thing we're gonna say is, while NetFoundry sponsors the OpenZD project, it's not necessarily the product. So Vos, right free and open-source, openZD is free and open-source, you can go get that right now it's out on GitHub. That's right, free and open source is where it's at. So NetFoundry is just the main sponsor of that project. I am a developer on that project, we have quite a few. And where it comes in is OpenZD is actually doing something a little bit different. It's trying to bring Zero Trust into your applications. And so databases, not quite your application may be but very important to your application. And so Zero Trust what is Zero Trust. Zero Trust in a nutshell is really about having, having no trust or distrust of own networks everywhere. It does not matter if it is a private network and your Amazon data center, Whedon VPC does not matter. No matter if it's your home network, like the network I am on, doesn't matter if it's the coffee shop down the street, every single network is considered hostile. And that's what Zero Trust really is all about. There are a few main components of Zero Trust, the most important is probably a strong identity. So you think x 509 certificates are very strong, cryptographically secure identities. And that's what ZD actually uses. We'll also call ZD, the open ZD. So if you hear me say both, you don't think of the pasta, I will although we can absolutely get into the pasta jokes because I like pasta, I promise you, I promise you, they're not all been made yet. But we're getting there we're getting. So strong identity is very important. And then another fundamental pillar of Zero Trust is authorized before connecting. So when you try to connect to something, if you aren't authorized to connect to that thing, you cannot connect to that thing. And this is actually ahead of even authentication of whatever you're connecting to. So in terms of databases, you would have a secure Zero Trust connection from your application, whatever that is over to your database. And then on top of that secure Zero Trust connection, you would also have your database authentication. So you could choose to use no password and rely on Open ZD if you want, but you absolutely can layer on the second layer of protection, which is your own username, password, or whatever. maybe if you're going to present a certificate, whatever, whatever authentication mechanism your database requires. So that's the Open ZD and that's Zero Trust in a real nutshell. There's a bunch more stuff, but I think those are the key salient points.

**Matt Yonkovit**  
Okay. Yeah. And I mean I think that we have long strived for that, that Zero Trust type of setup. I remember back in the day when I was playing around with different distributions. I wanted to secure distribution, so I used open SSH or open BSD. which shuts everything off. And you can't do anything with the server. And it was like, Oh, my God, I can't do a single thing. And it was jarring because there were very limited things you could do. But it was super secure. I think the most secure application is one with no user access, right? So no users accessing, it's super secure. But unfortunately,

**Clint Dovholuk**  
I do get hacked when nobody can use it.

**Matt Yonkovit**  
yes. But I think that obviously, we want to use it. And so I'm curious we always talk about defense in depth. So layers mentioned layers of different defense. So obviously, application logins, that's critical. So, from a database perspective, how does, how does Open ZD work in doing that Zero Trust connection, if I understand correctly, it's, it's JDBC. Or it's like the client connection?

**Clint Dovholuk**  
Yeah, we're gonna, we're gonna put on our swim. And we're gonna dive right in here, because it's gonna, it's gonna get deep real fast. Okay, so let me just start out, because you mentioned the security posture of OpenBSD. Having default, secure by default, right, that's a term you'll hear OpenZD toss around secure by default, what does that mean? It means there are no listening ports on your network. That is ZD, these end all be all, if you can if you can take an open source as Ed SDK and put it in your application. And if you can put it into your database, then what you can do is you can actually live in a world where there are no open ports. And so your database is only addressable on the overlay and not on the underlay, the underlay being layer three, layer four of the OSI model, TCP IP, that type stuff, the overlay being some ethereal layer that Open ZD provides for you the overlay on top of IP or TCP, which is somewhere between layers four and seven. I will just say that seven is still up there, right? And you can even say maybe ZD might be layer eight, but we're not gonna go there yet. We're like, I like to make the joke that our security goes to 11. Right? Yeah. Right. So our OSI model goes to 8, more than seven, right? So, how does that work with a database, a database is a little bit different, because generally speaking, you're not, you're probably not going to be permitted to take an Open ZD SDK and cram it into MySQL, right. If you want to go and build it, you certainly could, but out of the box, probably not going to do that. So right out of the gate, we have to take one of those core tenants of no ports open, we know we're going to have to have one port open somewhere. But let's put that port just as close as possible to something else. So we have these things we call tunnelers. And what they'll do is they'll provide the offload from as close as you can get it to the database, ideally, right on localhost, if you can put it all the way onto your database server itself, then you can, you can only trust. And this is where trust comes back in, you can only trust your host's network. And presumably, that's pretty good, right? Pretty good right there. You can also move that trust zone a bit bigger and trust your private network space if you need to. And so that's the server-side of things. Now, when we talk about Zero Trust and overlay networks, it's very easy to forget that there's a client and a server, I started with the server this time you started with the client because I'm gonna bring it back to the client. Now, with the client, you have a bunch of options. We do these things when you take a ZD SDK, and you smush it into an application, we call that a ZD. Vacation, you have z to find it, you've added ZD into it. And so we have z defied JDBC. So we have a JDBC wrapper, and we'll I'll talk about that in a second. And then we also just have the straight-up ability to create a socket connection. Or it's effectively a socket connection from your existing infrastructure. So inside of your code itself. So if you are a developer, and you're actually writing that app, you can take that Java SDK and just smush it right into your application itself. And then just use regular quote-unquote, regular JDBC. And you'll be fine. That will work perfectly well. I have a great video out on YouTube, you can go watch it, I use PostgreSQL, and MySQL, but you can go see how I did that with Docker. Now, if you don't have that capability, you're not a Java developer. Maybe you're using like, what I use locally you use. What's the I'm trying to I'm blanking on the name of the database tool I use from IntelliJ, not IntelliJ from JetBrains. What is the name of that thing anyway? So you've got your database client locally. I'm going to come up with it.

**Clint Dovholuk**  
That's okay. I'm totally blanking on it right now. But if you've got that client that is capable of having a JDBC driver added to it, you can take our ZDBC driver, which is what we do, if there's a, if there's a letter that can be replaced with Z for ZD will do it. Instead of JDBC, we got ZDBC, right? That's Z defied JDBC. And what that is, is it's so SQL, yeah, perfect, I love it. So that's, it's a jar that you can include into your client like a DB verb is another good example, you can add it to your client, and the client will bootstrap that jar. And that jar is smart enough to know how to poke the actual driver that you actually want. And so what it will do, it's not its own driver, that's really important. If it was his own driver, it's a maintenance nightmare. On our side, we'd have to build drivers for everybody. That's not how JDBC works. That's how JDBC works, I mean, so what we'll do is we'll just poke JDBC in all the right places, on your behalf, you provide a slightly different JDBC looking URL, and then suddenly, you have a Zero Trust connection that knows how to ride on the overlay and knows how to offload from that tunnel or at the other side as closest to the database as you can get it. And so you can have that MySQL server with no open ports to your local network, one local port to your local host and not your local network, not your wide area network. And that would be how you would do it. Okay. So different kinds of modifications there, then I can build it into my app, and then I have an app, and I'm going to take your driver and put it into it.

**Matt Yonkovit**  
Okay, so I'm going to oversimplify this just to make sure I got it right. And because commonly when we're using either Postgres, or we're using MySQL or Mongo or other databases in the space there's often a proxy server or HA proxy or something to do load balancing, or somebody do redirects, basically your tunnel or is something like that, but it's not exposing any ports externally. It's just there for the ZD connection, correct?

**Clint Dovholuk**  
That's exactly right. And can do, it can do load balancing, that also, it also serves that purpose, if you need to have three machines, you can have a precedent set on that connection that says, This is my main one, only use this if I have to failover or you can round-robin it. you can do that sort of stuff, too.

**Matt Yonkovit**  
Okay. And so as we talked about that connection most of us are used to set up an SSL connection between the app and the database, right. So you'll do that, and then you'll have your normal encryption, you can't see that connection, because of the layer it's in, right. And that's, that's kind of the secret sauce there is it's kind of hidden, it's, it's poked in the multiverse if you will, it's the dimensional gateway,

**Clint Dovholuk**  
it is kind of a bit of black magic, there's no question about that. Yeah. And so you're right, I would still encourage you to use TLS connection when you set up your driver, your driver, because even though you have that one local port, and that one local host, if somebody gets on that local host if you're not using a secure protocol, it is technically able to be

**Matt Yonkovit**  
well, let's be honest, if they're on the local host, you got way more problems to write like me, usually is very true. Yeah, true. No, no. And I mean, I think that that's where it's again, it's defense-in-depth, right like, so make it as difficult as possible once you get there. so that's pretty cool. So so in this space, you probably come across a lot of different use cases or a lot of different problems that people are trying to solve what are those common things that people are seeing in the space while they're looking to Open ZD to solve it? Like, are there specific things that have happened or occurrences or things that they're really trying to protect against?

**Clint Dovholuk**  
Yeah, it's really varied. Because OpenZD is that magic tunnel that gets you from point A to point B securely, using strong identities using all that Zero Trust, networking principle, goodness, you can literally run anything that you want over it, but there are quite a few common very, very common use cases. The DevOps space is one that lots gets lots and lots of attraction because I went to a B-sides event, I don't know if you're familiar with it besides but it's a security-focused conference. At the besides event, there was a great presentation and in that presentation, it was given by a fella from the company snowflake, and he was talking about how he runs Red Team Blue team exercises. And he has said he has never seen a red team fail an exercise and the red team or the attacker is blue as defenders. They've, he's never seen a red team fail an exercise if they were given access to Jenkins. So Jenkins CI CD pipeline, incredibly important, right, we've all heard about supply chain attacks, Jenkins is right in the middle of your supply chain, he's never seen at Red Team fail if it gave any access to Jenkins, which is pretty astonishing. We've had, we had our Jenkins on the open internet because as a DevOps fellow that we have here, a site reliability engineer, he calls himself that his job is basically to open holes and firewalls because that's what has to happen to make the business run with open ZD, we're able to take all those and hide them totally. So we have a little agent that we run locally if you don't have the capability of running it in the application like we were talking about before those tunnelers. So I have a ton of that running on my local machine right now. And that's how I get to Jenkins. That's how I'll get to Grafana. That's how I will SSH from my machine to a production machine. We don't have a bastion in the cloud anymore. We have a hidden Bastion, we have a great blog post about what a dark Bastion even means. How can you have a dark Bastion? Do you have to have your Bastion listening on port 22? Somewhere? Well, you don't when you have an OpenZD connection. So those are some of the big ones. I also did a video about SSH and in general, we Zita FIDE, and we made an SSH client, which is capable of SSH into machines that don't have SSH open at all, just kind of its kind of neat. So those are the two those are the big ones. But we have lots of we have a customer who likes to provide access to other engineers. So the access is provided to their engineers through OpenZD as opposed to a VPN, okay, when you're on a VPN, which is the classic way of doing things. And then so what happened was COVID came around, everybody left the office, go home, and worked from home became a nightmare, right? VPN was over there overloaded everywhere, because all of a sudden, there were all these connections that didn't expect before. And people didn't like their VPN anymore. So we have some big customers who use open ZD as a way of replacing their VPN. But in a more controlled, fit fashion. With open ZD, you can control access to the service. So if I told you, you had access to Port 80, you can only access port 80, you can't access any other ports whatsoever. So it's much more, it's a much more secure way over the standard VPN where you generally have access to every port that is available and every IP on your VPN. So we have lots of lots of people use that. But that's not our target, right? Our big target is actually app embedded. It's that's really, like if I were to tell you what the future is maybe this is me having some of that kool-aid that is so popular. But it's really application-embedded technology. That's really where open ZD shines. Now, it's a journey to get there, right? Like I can't just go and OpenZD to Jenkins, because I'm not Jenkins. But sure, most people will still have our tunnelers because there'll be programs that aren't certified yet. And I'll make my easy-to-find apps. And I'll provide my private connectivity over commodity internet, wherever I do no matter where I am, because I treat everything as hostile, including my local computer's network as hostile. And so that's what really that's what Open ZD really shines. And those are the kinds of use cases I think, probably the most prominent ones.

**Matt Yonkovit**  
Okay. Well, I like to kind of move away from some of the technical talk and do a rapid-fire question. So Ooh, who doesn't like rapid-fire questions, to get to know you a little bit more and to let our audience know who you are? in case they're interested. So they are completely random questions that just pop into my head. So there is no prep work for that you can do like unless you can read my brain, which would be really scary. Maybe, maybe, maybe. So what do you think is the biggest potential security threat in the coming years? Like, what do you see on the horizon that could cause some issues?

**Clint Dovholuk**  
I mean, it's not even on the horizon. It's right in front of us, right? Like, this is why Zero Trust is everywhere. It is literally the land and expansion of networks. This of something a fella says that I liked, which is networks were meant to share information, not secure information, right? This is absolute, it's absolutely true. you make a network so you can connect somewhere else. And inherently, you are opening yourself up to attacks. Like I love the log for Shell. I mean, I don't love it, but I mean like it's, it's just like there was this vulnerability in Java. I'm a longtime Java developer. And logged for J is a library that you just bake into your application. And if you poked log for J straight, then you could gain access to that machine and run whatever command you want to it. And so, NetFoundry opens ZD has a mascot called Open Ziggy. And open. Ziggy loves to tweet about CBSs scores and CBSS. Are you saying not technical? I'm going technical, technical.

**Matt Yonkovit**  
This is just a random popcorn question.

**Clint Dovholuk**  
So CBS is cool because it's, it's a way of gauging a vulnerability how troublesome of vulnerabilities, you see something over nine, you better act. So Ziggy, loves to find vulnerabilities that our attack vector network permissions required none. If you have an attack vector network permissions require none. That means you can be attacked from anywhere on the internet. Log for Shell was a 10. Like you can gain root command access to that machine from anywhere in the world that had logged for shut that lump shell vulnerability on it. So like, it's right here, it's right in front of us. This is why I really believe Zero Trust and the application embedded in Zero Trust is the future. So I think that's the biggest. We're seeing it with Ukraine.

**Matt Yonkovit**  
Well, well, yeah. I mean, so this is an interesting one, because, as you talked about, like Zero Trust, and you talk about like supply chain type issues, or you talk about CDs, like the log for J stuff, that was something that was whether it was malicious or not. I think it was just a mistake, right? Yeah. Totally

**Clint Dovholuk**  
easy to make that mistake, right. Like, it's, I've probably made that mistake, right. 

**Matt Yonkovit**  
It's bug-like, it's nothing it's missed. But you start to see that there are people who we have put our trust in, especially in the open-source space, because right now we are in CICD world where it grabs your code, the latest version off of GitHub, and deploys.

**Clint Dovholuk**  
Just go. Yeah, right. Would you? Why would you not get the latest? Don't you always want the latest?

**Matt Yonkovit**  
well, and I mean hey, we're just gonna deploy and we're gonna see what happens. Right and you saw with the famous nuked JavaScript apps, right, like, so we had colors. And a couple of others. And then there was, so you mentioned Ukraine, there was some other open-source software that if if you happen to be in certain regions of the world that is like, totally screwed up your website. So you could call it the rise in one case of protest where, or you could call it the rise of nuking we put a lot of trust into different components or different locations that probably haven't earned or can keep that trust, which is a different thing than talking about, like a malicious hacker who is specifically targeting your network. And that's an interesting place, right? Like, it's, it's, it's something that, I think, is industry, we're going to have to pivot and figure out how to resolve.

**Clint Dovholuk**  
But hackers don't have to target your network at all. That's the worst part about it. They target all networks everywhere. It's they just scan open ports and say, vulnerable it's like this. There's this great movie from the 90s called The Lawnmower Man. I don't know. Yeah, remember,

**Matt Yonkovit**  
I remembered a lot more of it. 

**Clint Dovholuk**  
But, but spoiler alert, all right. So anybody who doesn't want to hear how the Lawnmower Man ends, spoiler alert, in the end, they're in virtual reality, do you remember this scene, and Job is trying to escape because the protagonist had cut the landline back in landline days, right. And so now job, the the antagonist is stuck in virtual reality. And he's sitting there, and he's, he's doing all this little that X and you hear access, denied, access, denied, Access denied. And what he's doing is he's dialing all the ports outbound from his virtual reality space, looking for a port so that he can escape, right. And that's what these people are doing. They're just dialing every single port, it's everywhere until they find one, and they get that access granted. And when they get that access, granted, they just start hammering at it. That's why I have to go back to the Bastion point I made earlier like if you leave your SSH server on the open Internet, and just watch what happens like you're gonna see attack after attack after attack after attack, it's going to just test for strong ciphers. I use good ciphers are using a used reused password, here's a rainbow table attack all the other passwords there might be right like, it just happens. So supply chain is a whole different one, like supply chain and the building aspect of things. The inclusion of the software is definitely very different. In fact, that was what the B sides talk I watched was about was securing the supply chain. And how just shocked me how shockingly easy it was to compromise vault from within Kubernetes. Well, I had never seen

**Matt Yonkovit**  
but I mean, yeah, I mean, like, I mean, so you've got that it's the cascading impact, right. So I have been in the open-source space for 20 years. I love open source is awesome. A lot of The folks in the open-source space are overwhelmed. And we saw that recently the University of Minnesota had a whole class who just tried to introduce our abilities into the kernel. Right? Which, which, which is like, let's see what we can get away with. And then you had like these other examples that and

**Clint Dovholuk**  
that was just and that was just college students, like not being particularly nefarious about it

**Matt Yonkovit**  
Well, right. And I think that like, we've seen this kind of evolution there. But when you put that into a, whether it's a Jenkin space, or Kubernetes, or a TerraForm space, if you're able to get to one of those nodes, the controller of the configuration that controller of what is setting configuration setting like orchestrating or building out the servers. Oh, my gosh, like, you take a problem that is potentially like one server hacked. And now like malicious code can be deployed to 10,000. It's kind of scary.

**Clint Dovholuk**  
It's terrifying can happen in a heartbeat? No question. Yeah, the supply of the securing the supply chain is shockingly complicated. And so I actually, Ziggy tweeted this one day, because that same fellow, Ziggy follows him. And there was some problem with some CVE with NPM. And NPM reminded me of the DNS Haiku, if you recall, right. It's not DNS. There's no way it was DNS. It was DNS. Yeah. When I saw the CVE came out, I was like, it's not NPM. There's no way it's, it was NPM. Right? Like, I'm not dissing MPM, because it's, it's great. But the number of vulnerabilities that are coming specifically from that space lately has been significant.

**Matt Yonkovit**  
Yes, yeah. Yeah. So that was a little more than rapid-fire there. But that's okay. So we'll move on to the next thing, which is, what is your favorite tool that you use on a daily basis?

**Clint Dovholuk**  
My favorite tool that's really exciting for me is the Windows subsystem for Linux. I'm one of the people who enjoy using Windows, generally, because I like my software to just work. So it's nice when it does just work. And Windows subsystem for Linux is a breath of fresh air for some fellow like me, who has been running virtual machines forever. I also love my virtual I also love my virtual box. So Windows subsystem for Linux and Windows terminal. Some of the things that lately I've been really excited for

**Matt Yonkovit**  
okay, and do you hack away at code very often?

**Clint Dovholuk**  
Every day? I was doing it earlier, 

**Matt Yonkovit**  
 favorite programming language?

**Clint Dovholuk**  
Go

**Matt Yonkovit**  
Go.

**Clint Dovholuk**  
If you'd asked me before would have been C sharp and before that would have been Java? Oh, okay. Okay. Least favorite. My least favorite was probably JavaScript. It's maybe Python. It's gonna be any dynamically typed language. I have a strong disdain for anything really dynamically. Yeah, strong. I'm a typical guy through and through. So TypeScript is a big improvement for JavaScript. But Python gets a special place in my heart from the whole concept that you are encouraged to monkey patch things. Like that's just totally normal. Like go ahead and change the functionality any way you see fit. Go for it. That's, that's encouraging. But it's hard to argue with something that works, right, like working software trumps everything. And so if you can get it to work, and that was what you had to do. They get the job done.

**Matt Yonkovit**  
There you go. You're wearing a Star Wars t-shirt. Favorite movie favorite one of

**Clint Dovholuk**  
I like the Rogue one the best really? That was Yeah, I think that was it was an assassin. We're gonna read it recently about how there need to be more wars in Star Wars and Rogue One was a war movie largely and a relatively sad ending if anybody hasn't seen I'm not gonna spoil that one because that's kind of recent, but relatively sad ending on that one

**Matt Yonkovit**  
worst Star Wars movie.

**Clint Dovholuk**  
Oh, worst. It's gonna be I don't even remember episode one whatever. A New Hope. Is that what it is? I can't even remember the original 77 version. No, no, no, that's episode three or 406

**Matt Yonkovit**  
A New Hope was

**Clint Dovholuk**  
trying to come up with

**Matt Yonkovit**  
the one with the kid. The kid with a mannequin? Yeah, The Phantom Menace.

**Clint Dovholuk**  
Phantom Menace. There we go. Thank you. Yeah, no, no, no, no.

**Matt Yonkovit**  
Jar Binks episode. Yeah, it was rough. A lot of hope for that movie and it all else

**Clint Dovholuk**  
is terrible. And plus Natalie Portman great actress, but somehow the director made her come off just horrible.

**Matt Yonkovit**  
Just so bad. Well, she is the new Thor.

**Clint Dovholuk**  
I saw that. That's pretty neat.

**Matt Yonkovit**  
She's done for so the hammer. There you go. There you go. Well, Clint, thank you for swinging on by chatting with us a little bit about Zero Trust and sharing some of the rapid-fire questions there at the end. I appreciate you hanging out. And you've got a colleague who is going to be speaking at Percona Live. And by the time this podcast is released, it's probably going to be done. But you can check out the recording, which will be online, which will be cool. And people will love it. Yeah, I'm sure they will, especially if you're into securing databases and for the love of God, please do that.

**Clint Dovholuk**  
If you could, can I say, OpenZD, free open-source software go to Open go to github.com/OpenZD/ZD. And give it a star? Because it helps us get that word out there. Right. We are trying to let people know that's actually application security and just security, in general, is probably really important. Absolutely. Database especially for your apps.

**Matt Yonkovit**  
Absolutely. And so Clint, where can they find you on Twitter, LinkedIn, all of the socials.

**Clint Dovholuk**  
Oh, sure. Yeah, you can find me on Twitter. It's my last name Dovholuk I have no followers, but well don't bother Follow me. Follow OpenZD which is out there and open Ziggy Zig gy. Okay, both of which are totally out there. We have a YouTube channel. I usually do something very similar to this live stream. It's more of a coffee-style chat. We just talk tech you're welcome to come if you're interested. Anytime. We're Yeah, we just talking about dude talking about random stuff. We got the Twitter's we also have a discourse forum. If you're interested in OpenZD and you want to ask questions. And don't forget that star and that star you need to start to like and subscribe to. 

**Matt Yonkovit**  
Yeah, speaking of liking and subscribing. If you're watching this, like, subscribe, and leave comments. tell us what you'd like to see in the future. We would like that and appreciate it. Well, until next time, thank you for hanging out with us today and we'll catch you later.

