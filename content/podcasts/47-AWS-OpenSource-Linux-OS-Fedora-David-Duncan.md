---
title: "Talking Open Source, Linux OS, Fedora With David Duncan (Solutions Architect, AWS) - Percona Podcast 47"
description: "David Duncan, Principal Solutions Architect, at AWS to talk about his experience, being a key contributor to the Fedora Project (Linux), and in general the open source community and more"
short_text: "Open source is key to the growth and success of cloud providers like  Amazon Web Services (AWS). The HOSS, Head of Open Source Strategy, at Percona sits down with David Duncan, Principal Solutions Architect, at AWS to talk about his experience working at AWS, being a key contributor to the Fedora Project (Linux), and in general the open source community and more.  David is focused on helping tech partners make it easier to deploy and use their products in the cloud."
date: "2021-11-22"
podbean_link: "https://percona.podbean.com/e/percona-podcast-47-talking-aws-open-source-linux-os-fedora-w-david-duncan/"
youtube_id: "sSZhZ_GV68U"
speakers:
  - david_duncan
---

## Transcript

**Matt Yonkovit:**  
Hi, everybody. Welcome to another HOSS talks FOSS. I'm HOSS, Head of Open Source Strategy at Percona. Matt Yonkovit. Today I'm here with David Duncan. Hi, David, how are you doing?

**David Duncan:**  
Hi, yeah, Hey Matt, how are you?

**Matt Yonkovit:**  
David, you work for AWS, as a partner architecture Solution Architect, our solution partner architect?

**David Duncan:**  
I am called a Partner Solutions Architect. I spend a lot of my time working with our operating system partners. So my job is specifically platform related. It's not, not the application layers, right? Most for the most part. 

**Matt Yonkovit:**  
Okay. And so tell us a little bit about what you do there. Like, like, like from a day to day perspective, what does what does that mean?

**David Duncan:**  
Well, it means that I'm looking at a lot of our Linux partners, for the most part, and how they fit into the structure of our strategy. And what we can do to create a better experience for customers who need to use something that is not provided by AWS directly, right? So that would be Red Hat working with Red Hat, Enterprise Linux, or supporting Oracle, Linux, or rocking Linux, or any of these guys that that have come along and then then, as it's not just limited to Linux, I also work with Unix partners, like the FreeBSD Foundation, and and really have a great time working with them, by the way is always, always a pleasure.

**Matt Yonkovit:**  
So you're helping them get their OS onto AWS.

**David Duncan:**  
Yeah, and to take advantage of things that you wouldn't that we want them, we want them to be able to take advantage of, like, the AMI public parameters, right, we provide a public parameter to allow you to, to find the latest machine image from from a project, and that's part of my job is to help them onboard with those programs, and make sure that the right accounts are there, and the structure is right, so that everyone can find what they're looking for. And they feel comfortable that it's official, not, it's not just some randomly published machine image, right. So making sure that everything gets in there in a way that is predictable and safe for use.

**Matt Yonkovit:**  
So, everybody who's using one of the official AMI's or the official packages out there, for one of these Linux distributions, it has your fingerprints on it,

**David Duncan:**  
if you launched it from the console, and it's not Amazon, Linux, I was the one who put it in the put the listing together for that.

**Matt Yonkovit:**  
as you're going through the issues, get things moving you're doing a bit of everything.

**David Duncan:**  
Yeah, they're having a great time do it right these are, these are my people, this is my tribe, right? So I'm excited every day that I get to go to work and, and to do the workaround in making sure that the right the right parts of the kernel or the right patches that have been in that have been introduced to mainline is, are getting into the right spot. So when the next generation of grab a time comes up, there'll be zero-day support for Red Hat and the zero-day support for Sousa and, and for Ubuntu, and all these other operating systems that are out there that we partner with. 

**Matt Yonkovit:**  
Very cool, very cool. And how did you get into this? Like how what, what are what is your career look like to get you to this point?

**David Duncan:**  
So it's funny because I mean, usually, I like to tell the shocking story, right versus, which is that I got my first job in computing. Basically, because I was working on a database, I was working on a back-end connection to an ICM database that was in a point of sale system at a fish store at a little aquarium store, where I was working as a minimum wage aquarium clerk. And, and I called I was just looking online trying to get the connection to our web store to work just noodling around and, and then called in the consulting company that because I couldn't get the ICM database, right buckets, and all working the way that I expected to in the inventory valuation. And I called them in and I said, Look, I need somebody to help me with how these buckets work in the accounting. And they said, great, they said an account now I explained for about a half an hour to her what I was trying to do, she said, Hold on a minute, I'll be right back. She stepped outside, came back inside and she said I talked to my boss and he said he has no idea what you just did. But do you want a job and that's how I got that's really how I got my start right. Before that, I was trying to do everything but computing. My dad was my dad who did computing work for NASA. My mom was a database administrator on PDP 11 and Vax and so I got to see a lot of that. My first computer was a Sinclair ZX 80, right, that I built from a kit and the first big computer program was random. Yeah, random character generator for Dungeons and Dragons, um, that kid right and, and so it's, uh, it just kind of ballooned from there, I got excited about it, then I got hired to do this point of sale stuff I had been to college for, which was great book school, but, but had been to a school where we did a lot of physics and a lot of math. And so when the, when the call came up, for someone to do work on Beowulf projects, I was ready to do some installations ready to talk about doing science. And I had already learned, I'd already been humbled enough to know that I wasn't a scientist, but I was a really good janitor for scientists. And this Linux thing was it was really firing up way with the, with the high-performance computing. And I just happened to be a Dell with the right time and, and have some great mentors, inside of this space people that you might not your viewers might not know, but Garima Kochar, who was a performance engineer at Dell, who really mentored me and what it was like to do community science together. And funny stories like that, those are kind of the, I guess that's how I got my start. And, and what, what made me love Linux so much is that I just got so directly connected into that world and in a quick and easy fashion.

**Matt Yonkovit:**  
Yeah, I think a lot of people, I think a lot of people started there, right? With, yeah hey, I'm trying to do this fun thing or this funny thing, and it just kind of evolves from one thing to the next, and you end up in the right place at the right time. I mean, my entire career started that way.  I worked at an Internet service provider back when there were dial-up modems. And they did websites, in the early days of websites. And after a year there, they like to take the kids who are in college and see what they want to do career-wise. And I remember the head of the engineering dude came over, and he's like, okay, so what do you want to do? And I didn't know. So I looked, I actually looked in the newspaper to find what jobs paid a lot of money in the IT space. And I found DBAs that I didn't like. I think I want to be a DBA because it pays the most money. And then he's like, we need one of those years. And that, like that was it right? And so then 25 years later, here I am. But it's always fun how these little things start, right? You just never know how things are going to evolve when you get started. And when you make some of these early decisions.

**David Duncan:**  
Right, exactly.  you just never know. And then my dad used to say luck is where preparation meets opportunity.  that the right answer here was that I was messing around until I had a fairly good idea of what it was that I wanted to do, but then convinced some other people that, that I could, I could commit and I could deliver, and then the rest is history. But there are some great moments to like, working on that point of sale system. It's funny, I remember a friend of mine and I won a bid to do an entire college stadium right to network and build out the devices for an entire college stadium. And we decided to use the Linux terminal services project Linux and Schools Project, right? Yeah, with it. And so we built out this entire configuration. And in the end, there was database corruption that kept happening. And we didn't understand what was going on. Well, we got to this Chris Dooley is a friend of mine, he was an administrator at our local museum Museum of Art and he was doing everything at the lowest cost and I was doing everything at this, I could on Linux with this Unix based system that we were working with. And so we just, we just beat our heads against the wall and I'll never forget this because we Got upon, we got up on actually IRC, we were on pound Linux. And we were talking about what was happening to us. And these people were using ZFS, as the basis, we were using Red Hat within with the ZFS overlay if you remember those days on an old power ad server, and we, we were told by the company or actually our customer was told by the customer by the company that handled the point of sale software that we were using an experimental file system. And, and we said, well, it says NFS, but it's not experimental, right. And so they weren't convinced, but we told somebody on pound Linux, what was what we were experiencing. And then they got David Love, who is one of the architects from SGI. And they said, Hey, there's what they're telling these kids, it's a, it's an experimental file system. And he said, experimental since 1968. He and Andrew Tribble helped us to debug the problem and gave us so I'm making the story much shorter. But, but we figured out that the people who had written this application, were not using proper file open and close on their, on their database files. And it worked fine with a single system. But once we had this distributed, NFS, NFS was cut, it was creating a dirty cache, and the right-back was happening on a timeout for XFS, right? So a combination of XFS, and NFS. And this program that wasn't properly closing its files, we were getting a deadline, right to the database. And it was awful. So, so there are our, but the experience we had with the community was that they rallied around us, and these were people who were famous for, for us. I mean, I knew they were but I never expect, you would never expect him to help you. Because you were just some guy and in Texas, who was working on an on a little, a little point of sale system, but no, they helped us to, to really keep ourselves clear of any blame-free of blame, and to really help our customer understand that we were really doing a great job for them. And it was right there that I was completely sold, my whole career has been around open source since very since that moment, but we knew that, that we were rallied around by a community of people that we could trust, and, and we try to be those people or you try to be that kind of citizen inside of this, this community. Right. So.

**Matt Yonkovit:**  
And I think that's, that speaks so much to the open-source community and how welcoming it is. I mean, that there are so many people out there who are willing to go to the degree to help one another, do more. And it's, it's so awesome when you start to see the empowerment that that's out there, especially in a lot of the older communities, like the Linux community, and some of the more established communities. And I think it's great that the new projects that come out try to learn from the old and try to make things a little better. And here we are all these years later, and everything is just exploding. Right? 

**David Duncan:**  
Yeah, it is. It is exploding. I mean, I feel like I think you always hear you hear from a lot of the people who have been in open source for a long time, they say we've won, right, like, now what now we're on top we've, we've come to a place where everyone has recognized the value of the open source. And I think that's true. But I think where we are now is continuing to tell that story in a way that, brings us, good citizens, right? It's so hard, I think to or it's easy to fall prey to the idea that you could provide a service model and somehow if you keep all this code to yourself, you can, you can make some money, the real thing is getting those people to recognize that their contribution back is a part of their as a part of their edification as a part of their reward. And, and to see that as something that is, that is a duty, right, a responsibility based on what they've done. And, and so I spend a lot of time I think preaching that message talking about it, but also living it you have to be a part of those communities or these communities to be to, to, to help people realize the deep connection the help that they can get.

**Matt Yonkovit:**  
No, I mean, absolutely. And I mean, I know, there's, there's quite a few out there to participate in and I would encourage everyone who's listening to choose one or two that interest you and get involved. Right, can you eat something back? It doesn't have to be code. Right? 

**David Duncan:**  
No, that thing? Oh, yeah. I can't remember who it was who said this. But in a beautiful way, there are many people out there in the world of open source who have said things similar. So I'll just say that, like, from the open source universe, documentation is engineering, right? Make sure that everybody can understand and read how to make software or how to install and, and use the software in a successful way. He has a real engineering talent and shouldn't be forgotten. 

**Matt Yonkovit:**  
Yeah. And so, David, as you've been working more with the Linux vendors, the OS vendors, I'm sure that there's now a very different ecosystem today than there was even five years ago, with not only the number of distributions but also the number of technologies and ways people deploy their apps. Right. So now we've got Kubernetes, we've got serverless systems, I've got so how has that changed your work?

**David Duncan:**  
significantly!  Of course, first off, part of what I did all of last year was to work on the architecture for the Red Hat,  OpenShift, AWS service, the Rosa service, so I spent a ton of time working with the Red Hat SRE. And, and the, in the engineering teams on at Red Hat, to build out OpenShift on AWS as a, as a service team, right, really in as a tier-one service. And so it's been that that changed everything for me to say, to see this, this model move from not just providing you with an open source software, but also those same people providing you with guidance and prescriptive management in ways that that is that helps everybody be successful together, right, in terms of support, and management, and opinion, a deployment. Every day, there is more of that experience around that continuous integration, continuous delivery, and all of those processes that go into that. But there's a unique kind of balance that goes into that as well, like, it's great that we can recompile. I can stand up a server and recompile on every change. But man, does that get expensive, right? I mean, that is true.  yeah, so there's a lot of fun, fun, and interesting ways of identifying give and take, right, I think we saw that with the Gnome Project project was where they got a fair amount of credit from Google, and Google gave them the ability to run your continuous integration, continuous deployment, and they in one quarter, consumed all that credit, right? Just finding a way to and so you want to make sure that you find those that balance in the opportunities to really say this is a critical component, and we don't just have to do the unit tests, we can go ahead and do that. Do the full compile, or we can build the whole project and do our behavioral tests or whatever. And, and kind of making that decision, I think, is a really interesting one that people have to bend.

**Matt Yonkovit:**  
Yeah. And I think that it's interesting to see the number of options and how this has evolved over the years. And I'm interested to see what you're seeing from your partners, vendors, what's new, what's what are they? What are they excited about? What are they looking forward to over the next few years? 

**David Duncan:**  
I think the first thing that we're all looking forward to is the evolution of this container space. Right? What does it look like? How do we make this work for the long haul? And then, what's the future of computing? Right? Like we don't, we don't. Is it serverless? Is it Kubernetes? Is it? Is it a  scalable system that has yet to be determined what what does it look like? Do we have the right kind of resource-sharing model for what storage looks like? I mean, I'm, I'm excited personally, I'm excited about the concepts around NVMe reservations and how that might, that might work. Another thing that I'm really excited about is power management. Right? So I don't know if you've looked at this, but in a general, generally like a, in a server world, there's no reason to think that you're going to put your server to sleep, right? I mean, who wants to put their server to sleep?

**Matt Yonkovit:**  
Yeah, I mean, it's gonna stay up.

**David Duncan:**  
Right? But, but in the cloud on the cloud, or we're in these opportunistic compute models, right. Lots of things don't necessarily have to stay awake, while you're using it, you can go with more advanced power management. And so we see that with customers who want to maintain your SEO at Amazon, and I work on it in the context of Fedora. But power management, where they, they suspend a system, to a swap file, on-off-on an instance, right, and then when they need it back, like I said, in an opportunity, opportunistic way, let's say, the cost we have on Amazon, we have Spot Instances, I'll use that as the example. In every spot, we look at utilization, just generally, and we determine a price and that price can fluctuate. And so if you're you could hibernate a system, and then just wake it back up to do whatever opportunistic work you have like transcoding or, or base compiling or whatever, the to-do that works only when there's a cheaper price to do it, right? But making that happen, means that you have to convince other people to come with you. Right?  So, so from the, from a general standpoint, the server doesn't require this right, you really need a, you need some sort of cloud management system that you're looking at that says, Okay, I, I will get it because I have this ability on, on KVM, I can use the ACPI controls to shut this down and bring it back up, when I'm when I think it's important, regardless of what the underlying model is, or the reasoning behind it, you still have this ability to make it happen. And I think that those are those finding that that model exists? Now finding the right workloads for that starts to be interesting. That's kind of the interesting thing right now. So what does that look like? It's I see, I've seen Monte Carlo, style, parallel computing, right, embarrassingly parallel computing that can benefit from this on a lot of occasions, reporting structures of that sort. And so now, it's kind of exciting to think about next-generation, are we as open source contributors going to make that model functional for people who want to use it at a, at a higher level at an application layer?

**Matt Yonkovit:**  
Okay. So I mean that those are some of the things you're looking forward to, is there a project that you're really involved in externally, maybe an open source thing that you're like, going, that is a cool project? Everybody should go check that out?

**David Duncan:**  
I'm biased in the sense that I've spent the last 15 years working on the Fedora project,

**Matt Yonkovit:**  
It's okay, you can be biased. Go ahead. And, and, and, and be biased.

**David Duncan:**  
Sure. So I mean, so I'll say two things there that, that I have very much enjoyed being part of Fedora from being just an ambassador to being an active contributor to now helping to run the Fedora Cloud SIG. And, and from that, from all of those generations, all those permutations, I've had an excellent experience, lots of guidance, great mentors, know if you're, if  Neil Gumpa, but Neil spends a lot of time working across multiple projects in the world on open source, works on the council there and, and then across Fedora, and on BTRFS, he's done a lot of work on BTRFS and then we just adopted that in Fedora cloud, by the way, Fedora 35 that's coming out here pretty soon and it'll have BTRFS in it. I'm so excited about that. That was an interesting decision, too. But yeah, I'm excited about Fedora in that sense the I love what Matthew Miller has done as the floor project lead and the way he's he's kind of been a lot of he's been the glue the creating the position was like a great thing right making coordinator for the project someone who could help us with, with the events and whatnot and flock whether it's virtual or in-person has been for many years now, a great experience for me and always an adventure and an opportunity to learn a lot more about packaging, and program management and, and just development general.

**Matt Yonkovit:**  
So where are you most active in that project?

**David Duncan:**  
I'm most active in Fedora Cloud, right? So

**Matt Yonkovit:**  
now what component of it

**David Duncan:**  
So I spend my time working on the project leadership, so rep coordinating meetings and getting people on the projects there and then have done a lot of the work is kind of spearheaded a lot of work that was done here. And in the short term with other people like Chris Murphy and Neal Gompa, on getting BTRFS into our working group. And we did that for a couple of reasons. So one is that on in cloud environments, usually, you have a single disc, right that that does things, and then if you have data, you put the data on some sort of a different kind of, or an additional device, right? So. So however you carve up that block storage, you tend to use a smaller, a smaller root device, and then to have these external devices. We found that in areas like cis hardening and things like that, we still have the same rules, right? So, removing, removing the executable bit from, from, from slash temp, all these things that make that are very difficult to do when you have a single partition. But BTRFS allows you to have the sub volumes and the subvolumes can be presented with a lot of these same traits. And so we thought this would be a great opportunity for us to experiment and see where we see just how far we can get working with what is effectively the more modern file systems. And this wasn't a good fit for the Fedora server at the same time. Because BTRFS doesn't have some of the lower level raids raid five, RAID six, those don't really work effectively on BTRFS today. But for the most part, there's no reason to have those in a hyper scalar environment. And so we decided that this was a great fit for cloud and, and started to put that together. So we put together a proposal, we found that there wasn't a whole lot of pushback in terms of the base or the cloud, the cloud image itself, on the front of, of the container, there is still generally a fair amount of work to be done to support the overlay model on BTRFS. So we're not there for the container containers don't have a BTRFS base, but for all of the component parts per file, that was something that we thought was pretty exciting and made it possible for us to do some things that we had not been able to do before in terms of splitter 

**Matt Yonkovit:**  
BTRFS has been in development since 2006-7.

**David Duncan:**  
That sounds right. Yeah. Yeah, I feel like it's mature enough and we're ready.  It's been in the workstation for a couple of releases now and I don't feel like we're in a steady-state in terms of Fedora. This was an opportunity for us to realign with the workstation components and to, to kind of pave the way I think for some of the other editions that are out there.

**Matt Yonkovit:**  
Why do you think it took so long to adopt?

**David Duncan:**  
There are, well, first of XFs come on we were using reason ext for the base images. But, but, but Red Hat really has a lot of as a, as a sponsor of the project, they have a lot of vested interest in ensuring that the work that they've done on XFS continues to be successful. And I'm not saying I'm not not going to afford it. I think that's, that's a, it's important to work. And, from the enterprise perspective, long-standing file systems and long-standing support are great things. But it is definitely long in the tooth.  I mean, as I said, I'm just experimental since 1968, right, so. But, but the BTRFS brings us a lot of things that I think are a more modern kind of functionality that is super helpful for us in the cloud today. And that was the exciting part for us. snapshotting volumes, being able to to take what's running on one server, and then snapshot that to the root volume of another server that or another server instance, right, that was a, that was a big deal for us, right, being able to make those changes very, very quickly and very dramatically. So I can share a root volume from one stopped instance, and then use the snap from another, to populate the same content to a different instance. And that allows me to do things like modify, like to have a fast model for modifying billing codes or things like that, where there's some sort of sticky metadata in the volume or the and the instance itself. And, and it doesn't seem like a, it doesn't seem like I mean, I'm speaking about it kind of abstractly, but it doesn't seem like a big deal until you run into this, and you have to do this on hundreds of volumes. And it becomes much easier with BTRFS than it is with anything else that you would possibly have than we would be using anything else we'd have to be doing this at a block-level replication layer much faster, right? You'd have to you'd end up with DRBD and between instances and have some sort of major failover it'd be a big deal.

**Matt Yonkovit:**  
So that I mean, it's an interesting change, right, because I mean, EXT4 has been around forever as well. So I mean, that is interesting now, and I'll bring up a point and you can say a few you want to talk about it or not like the change with CentOS did that. Did you see any movement for people starting to look at Fedora as more of a server workload? 

**David Duncan:**  
That's interesting, it's interesting that you bring that up. I like talking about CentOS and CentOS doing.

**Matt Yonkovit:**  
That was sarcasm or was that something you love talking about?

**David Duncan:**  
I really, I really liked talking about it. I think it's very interesting so I was not one of those people who had an instant negative reaction to it, because I'd spent so much time with the HPC community. And the HPC community says these they say these great, great things they say, well, we want to run on CentOS. Great. Why do you want to run CentOS? Well, because it's stable. Okay. That's great. It is stable. You're right. And from a cloud. Remember, I'm looking at it from a cloud perspective, right? I don't have any hardware today. I've been in the hardware world, but today, I don't have any except for what Amazon makes, right? So now. So now they'd say, okay, great. We want stability. I'm like, okay, great. So here's a kernel that's been tested. And then they'd say, Yeah, but it doesn't have the ENA driver. We want it to be great. So you're going to break that kernel so that you can have the ENA driver that you want. Now, whatever QA happened at Red Hat, whatever QA happened during the CI process for CentOS all that's gone because you just you made you just made this model modification to the kernel. Okay, now, that's great. But now what do you want? Oh, well, we need this additional version.  we need the latest version of lib fabrics. Okay, that's great. Now, now we definitely are into uncharted territory. And, and while we're pushing all those changes we know these things are coming right. The ENA team knows that they're pushing into mainline first right so we see this we see the changes in the kernel. They know that they're, but they're taking them for about a tree. And so here I am. am a guy who's spending most of my time talking to these high-performance computing customers about how they can get the Kernel broken. And nd really, we're pushing those same changes into Red Hat at the very same time, right? So six weeks later with CentOS stream, the concept is six weeks after we'll it'll take about six weeks for QA. So we push these changes into Red Hat because we have this relationship or AWS has this relationship with Red Hat. And we're constantly working with we have project owners at Red Hat, we have project owners on the AWS side, and then we're pushing them together so that they can talk about things and make real change. And six weeks later, it's going to land in the CentOS stream. This means that if we have stream these people who are asking me to make these modifications to CentOS because it's stable, I suddenly have a stable CentOS to use, right. So CenOS stream gives them those latest changes, roughly six weeks later, because they've been through the regression testing, and they've been through kernel testing. And they've been through QA, right? So we know they work. And Red Hat's not testing they're not just testing on their own hardware they're testing on the Amazon hardware as well. Right? Make sure they have every opportunity to do that. So we're having this constant conversation happening around Red Hat, that Red Hat conversation lands in the stream then it really is stable. It lands in the next point release of Red Hat. Now they've got this whole cycle where they know that they have stability for long for the long-term support on Red Hat the CentOS experience has been or the CentOS stream experience benefited from the QA process that we would normally have for Red Hat point release. And they can you know they can use that the whole time. So I think that the process in the progress has been better based on that right now. There's no reason for me to ask a customer to recompile a driver, there's no reason for them to have to go and find the latest version of the RDMA core because it's in the CentOS version based on our collaborative work with based on the collaborative work between Amazon and Red Hat right. So I see this as being incredibly beneficial. I understand that a lot of people saw this and they said oh, what's gonna go to Fedora to CentOS to Red Hat? 

That's okay.

Okay. So, the so So from the perspective of what, what are we working with today? Well, we're working with the latest tested kernel on the CentOS stuff, and then if we want something that's more stable, we've got Red Hat. Now. They started working on Rocky and us at Amazon, I had the great fortune of being able to support them pretty much immediately from their conception and work with the cloud Linux guys and worked on the Linux with the other Linux team and love working with them. They and all their products are perfectly functional on AWS?

**Matt Yonkovit:**  
Yeah, I mean, I'm not. I mean, from an AWS standpoint, I've said this. This is more of just a Yeah, CentOS, Not CentOS.

**David Duncan:**  
Yeah, it's hard to talk about out of context. Yeah.

**Matt Yonkovit:**  
Yeah. But it is an interesting thing because you mentioned a use case that many people don't think about, because they don't necessarily see that, like the vast majority of CentOS users that I've known. And that we work with. They're not compiling their own kernel extensions. They're not adding things. It's like the reason they're using CentOS. Let's be honest, they don't want to pay Red Hat for Red Hat Linux. Yeah. I mean, I mean, you don't even say that. I say that because that's the customers that I'm talking to.  like, that's what they're like. They're like, Oh, yeah, we don't want to pay for Red Hat Linux, but we want everything that redhead Linux offers,

**David Duncan:**  
Amazing people work on CentOS.

**Matt Yonkovit:**  
Yeah. Yeah. And, and that's great.  and I think that's, I mean, it gets back to the open source space. We've done some surveys over the years. And it's like, a minimum of two-thirds of those who are running open source are predisposed to never pay for something in the open source space that they get for free. I mean, right. And that's cool. Right, because that's part of the cool factor of being able to get things in the Linux space or in the open source space. And they can grab these things, they can make it work, and what more power to them if they can run production on their own.

**David Duncan:**  
I mean, that's not how I want to run my production database, sorry, oh, I'm sorry.

**Matt Yonkovit:**  
I get you, I get you. I'm, this is not, I'm not saying I condone it. But I'm saying that that's, that's a common thing. And I think that's why a lot of the push around, or the concern around that switch to stream came up is you've got a really large set of users using CentOS. That's basically just using it because it's Red Hat, Enterprise Linux without the Red Hat, Enterprise Linux name. And then all of a sudden, that changes, and then that disrupts what they expected. But it's interesting to hear from you like you've got things people are like they want sending to us because it's stable. But then they want this other stuff, which is, which is a little bit of a different space than I'm used to, because like I said, my customers, are a little different. Now, it's interesting that you mentioned that you don't want to run stuff in production, without having some sort of support or safety net, which is where most large enterprises are. But it's, it's super interesting, I found that most of the companies that choose self-support, choose self-support for one or two people who are at that company. And then when those people leave, like the people coming in, they're like, why did we do this? And then they change technologies, they change everything, they end up with support, right? And there's a cycle, right? It's a very independent choice. That really boils down to individual contributors on which technologies and a lot of cases and whether they're willing to pay and whether they want to support or not support

**David Duncan:**  
I mean, and you heard me saying that some of my earliest projects were at where my earliest large projects were built on things like the Linux and Schools Project. I mean, they weren't built on something that was built that was, but of course, when I bought those servers, those servers ran red hat, right.

**Matt Yonkovit:**  
At the time, was there even Red Hat Enterprise Linux? Or did you go with it on 30 floppy disks, as everyone else did? Or  the

**David Duncan:**  
CDs? Yeah. Yeah. Oh, yes. Yeah, well, no, it was it had, I mean, I had the XFS overlay that I'd created myself, right, because there wasn't such a thing at that point XFS was was, um, this is like, seven, two, right? Yesterday.

**Matt Yonkovit:**  
So I mean, like, yeah, I learned on Slackware by the way, so.

**David Duncan:**  
No, it's great. I that's, that's, uh, I think, I feel like there's, there's a lot of places there where we, we all learned, we all grew our abilities on Linux, I mean, Linux really was that was working on. I mean don't hold this against me, but most of my work was done on the scope. Scope. Before Yeah, I got a hang-up. But before I got into, into, into Red Hat and, and, and while you know Scope was a great experience for being able to work on multiple systems to support hundreds of terminals and things like that, for me long when the only other alternative for small business was windows. But, but every time I call in this is my experience, right? Is that proprietary software like that? Do you call in for support? Because you had some sort of a kernel bug, you pay somebody $700. So they talk to you about the facts. You had a kernel bug, and then the ultimate answer would be yes, there's a kernel bug.

**Matt Yonkovit:**  
Yeah, yeah.

**David Duncan:**  
And so I feel like that there in the olden days, it was a great thing. We, we were learning, but for that business, I mean, I had redhead support, right? There was no question about it. Like if something went wrong, I wasn't going to rely on myself and the one other guy who really had a day job right. To be there when they really needed they needed to know what had to go. What had to go right.  we wanted that. So Part One of the sense-certainty that we were going to be able to help them.

**Matt Yonkovit:**  
And I get it. I mean, Percona where I work, that's how we make our money is how the support does so. We were vested interests as well. But it is an interesting thing, because so many, I mean, you have the freedom and open source, that's the great thing is, it's about enabling those choices. 

**David Duncan:**  
Well, I mean, it's, it is and it's one of the things that I think is interesting is that we do have a choice, and we have the choice on where we get that support I mean, there's, there's great opportunity out there to be an open source supporter, and, and to make make a good living at it. Right. I mean, that's, that is the open source way is just to take advantage of the opportunities that are provided by people using the software and your expertise. So, but then it's interesting there, there are always places where there are lots of lessons to be learned about this. And I think that that knee-jerk reaction was one of the lessons that we really needed to learn, which is that the Zendo stream wasn't a direct descendant of Fedora, right? It was a collaborative effort around Enterprise Linux that then was provided in a way that was afoot forward for what would be released as a stable release a little bit later.

**Matt Yonkovit:**  
I mean, sometimes that's just marketing, right? I mean, it's how you position it, or market or like like, like, articulate the value of it. And I think in the open source space, especially, where passions run high, it's so important to be able to articulate, tell the story and convey what you're trying to do. And sometimes, as folks working on the back end, we sometimes overlook that or minimize that conversation or that

**David Duncan:**  
minimize is a really good way. Yeah, that's, that is a, something that we have to be very careful about, right in our world, because their opinions do run high, and there are many of them. And they don't necessarily converge. And right, one of them I see, I've seen this tactic from, from senior leadership, where someone has enough that has a really strong idea, but they don't know how to present it well. Right. They don't have enough detail on how to articulate it. And, and we need to be there for each other to help bootstrap those concepts. And, and to listen, I think, and this is I got from Plato, actually, but to listen to what I mean, not what I say.

**Matt Yonkovit:**  
There you go. Yeah, there you go. Well, David, thank you for stopping by and chatting with me about some of the things going on in your group, and also in the Fedora space was a pleasure to catch up and learn a little bit about your background and stuff. But I do appreciate you coming on.

**David Duncan:**  
Matt, this has been spectacular, right? I mean, I really enjoyed having the chat. We get to do it again.

**Matt Yonkovit:**  
Oh, yeah. Anytime if people want to chat with you, or reach out in the community and just you know say hi where's the best way for them to do that?

**David Duncan:**  
I'm davedunc everywhere. Hit me up on Twitter. Yeah, davedunc everywhere.

**Matt Yonkovit:**  
All right. Awesome. All right, David. Thanks so much.

**David Duncan:**  
Thank you.


