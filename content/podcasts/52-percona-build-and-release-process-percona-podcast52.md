---
title: "Percona Build and Release Process - Percona Podcast 52 with Evgeniy Patlan"
description: "Listen to Evgeniy Patlan as he is talking about his background, build engineering, the local community,  and go deep into the build process"
short_text: "This week’s episode of Percona Podcast, The HOSS Talks FOSS is with Evgeniy Patlan, Manager, Build & Release Engineering Team at Percona. We are talking about Evgeniy’s background, build engineering, how work in the local community,  and go deep into the build process: including monitoring, debuging, automated package testing. Matt Yonkovit, the HOSS at Percona, Talks to Evgeniy’s recent work in the open source space with the Chernihiv IT cluster where he has been teaching DevOps courses."
date: "2022-02-04"
podbean_link: "https://percona.podbean.com/e/percona-build-and-release-process-percona-podcast-52-with-evgeniy-patlan/"
youtube_id: "A7oEkTMNrr0"
speakers:
  - evgeniy_patlan
  - matt_yonkovit
---

## Transcript

**Matt Yonkovit:**  
Hi everybody, welcome to another episode of The HOSS talks FOSS. This week's episode, I'm here with Evgeniy Patlan. Hi, Evgeniy, how are you?

**Evgeniy Patlan:**  
Hi Matt. I am OK, Thank you!

**Matt Yonkovit:**  
So Evgeniy works for Percona. And he is the manager of the build and release team. So he's out there, making sure that all of our builds and releases are done properly. And I figured it would be really good to talk to him a little bit about what he does in that group, maybe talk a little bit about his background, and also talk a little bit about the work he's doing in his local community around open source. So we'll get to that in a second. So Evgeniy, why don't you tell us a little bit about your background?

**Evgeniy Patlan:**  
Okay, my background, originally from Chernihiv and started here in Chernihiv, Technological University. Then I joined Percona, almost six years ago, as build engineer, building RPM steps, compiling all our services, making ci cd pipeline and automating these builds. So, all our products are connected with me.

**Matt Yonkovit:**  
Yeah, that's a lot of builds, because we support quite a few platforms. How many platforms do we have? We have a lot, right.

**Evgeniy Patlan:**  
Yeah, currently we support it. Three Centos Red Hat systems are 678. And we support three Debian systems: Debian 910, and 11. And Ubuntu LTS. 1804, and 2004.

**Matt Yonkovit:**  
Yeah, so and that's for each one of the products needs each one of those as well. Yeah. So you. So right there, you've got eight different operating system versions, and then you have to test every product that we have, and all the versions of those products. So for those who don't know, if we are supporting multiple versions, let's say MySQL, like MySQL five, seven, MySQL eight all of those need to be tested as well.

**Evgeniy Patlan:**  
Well, but first of all, it should be built, and it's my work

**Matt Yonkovit:**  
Right, build and then test. There are a lot of buildings. Right. And you mentioned setting up a lot of automation for that. Maybe talk to us a little bit about the automation that's set up, what are we using what's what's our stack that we use to do our automation for built,

**Evgeniy Patlan:**  
We use Jenkins, for our build, to recreate the different CI/CD pipelines, because it's built. And what's interesting, we have a few Jenkins, as I remember, sitting Jenkins server master servers, and the main part of them using AWS Spot Instances. So we don't know when the small master server can go down. We just got a notification in two minutes before the server will go down and we need to run the server for it. And we succeeded with this. Because we unmount the partition starting your server and mount the partition to your servers all Jenkins information and it takes less than two minutes.

**Matt Yonkovit:**  
So wait. So what you're saying is we're since we're using Spot Instances, Spot Instances can go up and down. If the spot instance goes away, do we get a regular instance or do we try to build for another spot?

**Evgeniy Patlan:**  
Another spot.

**Matt Yonkovit:**  
Okay, so we're right now running everything through the Jenkins process with spot instance, running the spot instance notifies us, Hey, you're going to go down in two minutes or whatever. And then we quickly go build on another spot instance, and then mount the EBS volumes for all of that onto the other box and start rebuilding.

**Evgeniy Patlan:**  
Yeah, exactly. Wow. Everything is automated.

**Matt Yonkovit:**  
That's awesome. That's great. Yeah. And so is the automation for building on the new spot instance, in moving everything out. What's that built-in?

**Evgeniy Patlan:**  
What do I mean?

**Matt Yonkovit:**  
So is that part of the Jenkins pipeline there? Or did we write something custom?

**Evgeniy Patlan:**  
It is done in cloud formation AWS

**Matt Yonkovit:**  
CloudFormation. Okay, okay. Yeah. Okay. And so when we're talking about like, like, builds like this, and going through the build process. Every like, like, we talked a little bit about these different platforms we have. There's also different hardware that can be built against as well. Now, right now, we're doing things for Intel and x86. But there's a lot of discussion around ARM based processors as well.

**Evgeniy Patlan:**  
Yeah, this is a really tough question, because currently we are doing any ARM build, and it is a pity, because all of us are struggling doing this. And I hope that soon, very soon, we'll have at least test builds for it. Because just making a build is not a difficult task. But the software which we build should be optimized for ARM. There's a main question, are we ready to optimize it?

**Matt Yonkovit:**  
Well, I mean, it's not only being ready, it's also adding a new architecture like that. doubles the work, right? So if everything is built for x86, and we're doing eight different operating systems, and we've got five different products we're building, right, so we've already got 40 builds that we're doing then, if we're going to do that now, not only for x86, but also for ARM, then all of a sudden you jumped at.

**Evgeniy Patlan:**  
Yeah, but you're also told that we have five build products. But it's not true. Because, for example, for PostgreSQL, we have, as I remember, eight components? And yeah,

**Matt Yonkovit:**  
Yeah, each of the components needs to be built separately as well. So I mean, literally, there's, there's hundreds, and so doubling that is quite it's not necessarily easy. So, as these build processes are running, and as we are increasing, it becomes more difficult to keep visualizing all of them. So what sort of monitoring do you do for the build processes? And when something goes wrong with the build process, what do you do? How do you get in and fix it?

**Evgeniy Patlan:**  
Well, in general, there is such a term in the DevOps world called Chat ops. So once the build has failed, it sends us just a message that, hey, the build has failed and we are going to chat log for it. So for each build, it might even take more than a day to figure out what's going on, and fix an issue.

**Matt Yonkovit:**  
Right? So it tells you, hey so you get a Slack message. It's integrated into Slack. And it will say, my build is broken, whatever 1432, you should go look at this. And you go out, and then you'll debug that particular issue. And it could take you a day or two to figure out what was going on with it. 

**Evgeniy Patlan:**  
Yeah. Sometimes it is just, oh, we forgot to add in some, maybe a coma, in called, oh, just forgot to set a tag. So set it builds as in progress. For example, Percona Server for MySQL build takes three hours and a half for this platform. So.

**Matt Yonkovit:**  
Yeah. And so those builds happen just for the one. If something happens in the middle, then you've got to go back and debug it, obviously fix it. But it's not just about the build process failing, there's also the automated testing that has to occur after the fact. Right?

**Evgeniy Patlan:**  
Yeah, we have automated package testing, which is done by our QA team. And still we, we need to add improvements. Because it is, it would be great to create a really big container, delivery pipeline, which will test everything automatically once built is done. But currently, we can just say, hey, package our key, we can proceed with the release, we need to check functionality, and we need steel to integrate this.

**Matt Yonkovit:**  
Yep. And I mean, like, so that process. I mean, it's pretty big and complicated. And there's a lot of different automations that we have built into the entire process there. And you mentioned that you attended the Technical University in Chernihiv right? And you are actually active in that open source community. Tell us a little bit about the Chernihiv cluster?

**Evgeniy Patlan:**  
Well, maybe four or five years ago, I don't remember exactly in Chernihiv a few years IT companies decided to build local communities because we have quite a small city, just 300,000 people. But we are not far from our capital Kiev, just 150 kilometers. So you can sense that everyone goes to Kiev to work. And these companies decided to keep IT specialists in our native city, and they created the Chernihiv IT cluster. The purpose of this class is to build community and to help students in the university to learn something because the programming in the university is quite, let's say outdated, because they're learning how to work with maybe Pascal. And while I was starting, I wrote some code in Assembly. So it's really outdated. And in university, it's tough to update the program. The main question is to have good lectures, good professors. That's why the IT cluster decided to help them. And it's awesome that this year Percona became a participant of this cluster. And we already performed DevOps crash course for students, and not only for students, people from Kiev. And it was awesome, because we talked about DevOps, previously, in Chernihiv two talks about DevOps, maybe in the last four years. And one of these two talks was mine. Yeah. Yeah, yeah,

**Matt Yonkovit:**  
I think it's important that like, I think you're right, a lot of folks who come out of university now, they have a good foundation from an academic perspective, but a lot of times it doesn't translate to real world work. Yeah. And it's good to try and bridge that gap, and bring more practical experience, and help update some of the curriculum that they have. Now, you just gave a series of talks last week, correct?

**Evgeniy Patlan:**  
Yes, six stall talks during this DevOps Crash Course. And four of them were done by Percona staff. And two models were done by Chernihiv Company Agile Vision. And it was really great because all of us just added something new to the previous speaker. It was interesting. Our students got certificates that confirm they participated in it. And you see, I saw it as a real interest in students' eyes, and his main idea of this course.

**Matt Yonkovit:**  
And so what specifically was your section on like, can you give us maybe like a little bit of a background into that?

**Evgeniy Patlan:**  
Well, I'm talking about creating CI/CD pipelines in Jenkins? And because is the main part of DevOps work? And I found out while interviewing people, not all of them know how it worked previously. What is the difference between scripted and declarative pipelines? How to build them correctly, as it's why I decided to talk about this. And it does not provide a lot of knowledge for students because everyone can build it. And I just showed how to make a declarative pipeline with some bash code.

**Matt Yonkovit:**  
Okay, all right. There you go. There you go. I mean, that's, that's, that's interesting. You're giving that foundation to people who don't necessarily get it, which is good. And helping those students maybe come up and get some skills that they wouldn't otherwise see. So that's always very good, positive. Now, I wanted to go back to the builds for a second, because one of the things that I have seen is, while a lot of people use the packages that we provide, or other providers provide, there's still a fair number of people who want to build from source themselves. Right? So maybe give us a couple of pointers for those who are interested in building from the source? Are there any? Is there any advice you could give them?

**Evgeniy Patlan:**  
Well, if we will speak about Percona products, each of our products in GitHub has a build script, which can be used for a build process, and everyone can use a script. They are done in the same way. So they have just exactly the same flex. So using these build scripts, you can install dependencies, get source code, great source packages, great binary tarballs, great binary packages for any platform we support. And it's easy. Maybe a year ago, I created a blog post about how to build a Percona server for MySQL, using this build script. And last maybe two or three months, I got a lot of requests about how to build the Percona XtraDB Cluster. And my answer was, hey, just take this link to build a script, and use this blog post. But I see that I still need to explain how to use it. And maybe this month, I would create one more blog post about how to build a Percona XtraDB cluster. And it will really help because I got maybe five or seven questions about it.

**Matt Yonkovit:**  
Yeah, so there is a build script out there. For those who are interested in building from source. If you use that, it will give you all of the commands and you can modify as you need or adjust from that it gives a pretty good starting point if you're interested. And I think that that's good advice to start with something that's there. And we'll put a link to your blog in this video. And in the descriptions, so people can get to it if they're interested in learning how to build from source themselves. So, Evgeniy, I wanted to thank you for coming on and chatting with us today. I appreciate you taking a few minutes out of your time talking to us a little bit about the build and release process here. Also a little bit about the local community that you are building in your local city. But I appreciate the time.

**Evgeniy Patlan:**  
Thank you, Matt. And I'm really happy to participate in this session.

**Matt Yonkovit:**  
I appreciate it. Thank you very much.
