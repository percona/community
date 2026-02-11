---
title: ' Comunity MeetUp - Installation of the main part of Percona products - February
  9th, 2022 at 10:00 am EST'
description: Learn different installation methods for getting started with Percona
  distributions and tooling in this Community MeetUp with Evgeniy Patlan. Follow us!
images:
- events/percona-meetup/2022-02-09-meetup-products.jpg
date: '2022-02-09'
draft: false
aliases:
- /events/percona-meetups/percona-meetup-for-percona-products-february-9th-2022/
speakers:
- evgeniy_patlan
- matt_yonkovit
tags: ["Meetup", "MongoDB", "MySQL", "PMM", "Percona products", "PostgreSQL"]
events_year: ["2022"]
events_tag: ["Community", "MongoDB", "MySQL", "PostgreSQL"]
events_category: ["Speaking"]
---
This video and its transcript are from the Percona Commmunity Meetup that we had with Evgeniy Patlan last February 9th, 2022. We have talked how to install Percona's various components, the different software that we have, specifically looking at our server software in Postgres, MySQL, and MongoDB. We tackle how to install from a repository and what are the different install options that we have?

## Video

{{% youtube youtube_id="LkmbEql9Mj8" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Hey, welcome everyone; welcome to the live stream. Yes, we are here once again with another Percona live stream. I am here with Evgeniy this week. You might have heard him on the latest HOSS talks FOSS podcast. Welcome, how are you doing today?

**Evgeniy Patlan:** 
Hi, I'm okay, as usual. Just build it and build it. Yeah,

**Matt Yonkovit:**  
Yes, you have so many things to build. There are so many things being built right now. It's crazy.. So today, we're going to be specifically covering: how to install Percona's various components, the different software that we have, specifically looking at our server software. So Postgres, MySQL, and Mongo, and this is going to cover some of the basics around how to install from a repository, what are the different install options that we have? Look at some of the special scripts we have to help you choose the right software and things like that. And if we have time, we might even get to look at how you could build your own from the source. Oh, won't that be fun? But before we begin, I want to point out something. Evgeniy has a special shirt on today because he is one of Percona Unsung Heroes. He is one of the unsung heroes of the forum. He had over 100 Answers to Questions last year. In fact, yesterday, he was just talking to someone he said about some sort of installation problem or questions. What was the question? By the way? Was it an interesting question?

**Evgeniy Patlan:** 
So there was an issue during installation on Debian 10.

**Matt Yonkovit:**  
Oh, okay. All right. Yeah, it's, it's funny because as the different releases come out, you run into different issues. And as you try to jump potentially to different distros that aren't officially supported, you run into all kinds of weird things. Like I tried to install on Amazon, Linux and ran into all kinds of weird stuff. Because Amazon Linux is a little different, right? It's not an officially supported build.

**Evgeniy Patlan:** 
Well, it's supported in general is supported, but it depends. What Amazon Linux did you use? Was it Amazon? Linux One? Amazon Linux two?

**Matt Yonkovit:**  
I don't remember. It was probably because

**Evgeniy Patlan:** 
probably Amazon Linux is based on CentOS six, and Amazon Linux Two is based on CentOS seven. Ah, that might be some issues.

**Matt Yonkovit:**  
Okay. And so we support two or what do we support one?

**Evgeniy Patlan:** 
We support both of them.

**Matt Yonkovit:**  
Both of them. Okay.

**Evgeniy Patlan:** 
Some products are not available for Amazon Linux One because centOs six is already at the end of life. That's why we might not prepare packages for it.

**Matt Yonkovit:**  
Hmm. Okay. Fair enough. Fair enough. I don't remember that. But the number of builds out there is pretty significant. So why don't we just jump right into it? And let's talk about how we can install the various Percona products and what sort of methods are out there. And I'll let you share your screen and we can go from there.

**Evgeniy Patlan:** 
I will suggest starting from our Percona repo because in general, you might download packages from our website or from our repo. The suggested way is to use packages and our packaging repos. But still, all packages are available on a website and you can download them even you might see this there is a bundle in tarballs, which contains all needed packages for this operation system on Oracle Linux seven. Yeah. Yes, this thought about it does contain all packages compressed, and you don't need to copy all links to these packages, just one tarball. And that's it. But once you download it, there would be some more interesting things you should do. Because there might be some dependency issues. And you might need to create your local repo for example. This is why it's better to use our repo. One more way to install everything is to use our generic tarball is a bit outdated way of installation, I would say because, well, it's not contained all needed dependencies it is just precompiled binaries. I don't think it's valuable to use it in production for this I assume is okay but not in prod. But still, we have some difference is that some sometimes we provide glibc to the valve sometimes the glibc to the 17 It depends on which platform we use for built because if we provide support of CentOs six, we use the oldest operation system and it's supported operation system and it would be CentOs six it would be a glibc 2.12. Now, so, all newer version would be compatible and this binary tarball would work on any operation systems with glibc older than 2.12. And the best installation way is of course our repo previously we have only one repo it was called Percona and here we have apt and yum repos what is the inside of this repo. First of all is Percona release package and a lot as a packages, for example, you can see Percona server Percona Server for MongoDB, XtraBackup, XtraDB Cluster and what is Percona repo in general now it can be called also original this repo contains all our products that we ever built and for all operations systems, but you see it's hard to maintain such repos as there are lot of versions already unsupported versions, for example, Percona server 5.1 and we decided to create a separate repo or reach standalone product and now you can see there are a lot of them

**Matt Yonkovit:**  
Yeah. So let's proceed.

**Evgeniy Patlan:** 
okay. So we created separate repos. For every our product, for example, you can see the PMM client and PMM 2 client. There are also repos for example, pxb2.4, pxb8.0 so we created this repo to separate products. For example, if you want to install Percona Server, why do you need the Percona server from MySQL? Why do you need to have enabled repo for PostgreSQL for example, or for MongoDB you selected only one repo and visit. So any dependency issues which could appear with any other repo are not does not affect your system. For example, if you're wanting to install Percona Server for MySQL, it wouldn't try to install Percona XtraDB cluster for you because both of these packages provides MySQL. And we decided that this setup would work better. Additionally, inoriginal Percona Repo, we started only one Deb package version for each product so you weren’t able to install all the versions for these standalone repos we decided that it's not good behavior and now you can install any of five latest versions just said what version do you need for example let's check pxb repo and we will see in main all versions 8.0 to 27 - 26 - 25 - 23 - 22 you can install any of this version and you don't need to download it from website create local repo and installed packages because for example why you might need to create local repo you download packages for example, Percona XtraDB cluster and might be some dependencies. But if you're going to install packages use then dpkg comment it wouldn't resolve dependencies you would get error and you will need to install dependencies manually and try installation again. It is great starting from Ubuntu 18 to Debian nine you already can install a lot of packages that you downloaded on your system using apt command apt results dependencies but previously for example in Debian 8 and Ubuntu 14 - 16 it wasn't possible. so how we can configure this on your system because all this repo remember everything isn't really easy because we have a big bunch of products for this we created Percona release script and sure there standalone repo for it. so first of all you need some somehow get it on your system. It is five latest versions. Let's use the latest one and I will start vagrant. I destroyed okay well VM is studying I would tell what is inside this package. In this package, you can find configuration script and GPG keys in order to verify that all packages are provided by Percona because all our bigger packages are signed with GPG key and you can verify that it's our packages and not someone else trying to break your system

**Matt Yonkovit:**  
Evgeniy, can you still hear me? Yeah, you can still hear me so I'm going to ask the audience then if they can still hear me because I just made a quick adjustment so maybe they can they can't let's see.

**Evgeniy Patlan:** 
So finally started

**Matt Yonkovit:**  
Nice. Mr. David Stokes says he can hear me now so thank you, everyone, for coming I'm sorry. audio problems. I was telling Evgeniy this morning that I woke up to this machine being rebooted after an update and everything went wonky. So I'm glad you can hear me now continue on.

**Evgeniy Patlan:** 
Okay, let's download this Package and install it. So, first of all once this is a fresh machine, we need to update apt repo because there will be some dependencies that we need to install. And what we need to do, first of all we need to install package gnupg2 install. For future versions of Percona release package, we are going to fix this. And this package will be installed automatically as dependencies. But as I already told, for example, on Debian 8 systems, it's not possible to resolve this dependence. That's why we need to install the package manually. But is Debian 8 is already EOL, we are going to improve this again. So apt install Percona release. Yeah, we already got a help message, how to configure it. And you can see there is setup common. What more comments can we get in Percona release?

**Matt Yonkovit:**  
That's a lot. That's a lot of stuff.

**Evgeniy Patlan:** 
Yeah, it's not packages. It is repos? Yeah, it's so available repos for installation. But then, we decided that, Hey, why do we need to put them now what caused them into scripts and so on, we made this script my intelligent. And now it automatically checks if the repo available or not, for example, if I would say, a Percona release, enable, for example, Percona2 repo release, it will say, hey, there is no such repo. But for example, we don't have incidences least smdb 5.0. What we'll see, enable psmdb50 release. Hey, hey, this. So it checks our repo availability.

**Matt Yonkovit:**  
So if you updated this package, you won't get the list in the help, but you can still get the releases that are out there potentially.

**Evgeniy Patlan:** 
Yeah. We are going to add additional comments that will currently Percona shows all enabled repos. But we will add, maybe at least comments that will check all available repo and provide you this big output. But for now, the best way to verify if the report is available or not, is to go to repo-percona.com. And you'll see this big list of repo. So I even don't know should we put it into console because it will take maybe two or three screens? Hmm.

**Matt Yonkovit:**  
I mean, one of the things you could do is make it so if you did the help, you could pass it. Like the type of database you're looking at, like if you want MySQL or Mongo to be able to put the Percona release, help Mongo and just list the MongoDB. Yeah, yeah, yeah, that could reduce it quite a bit as well. And make it easier for people to find what they're looking for. Now, these are the official GA, but we can also do experimental right and beta releases.

**Evgeniy Patlan:** 
Yeah, yeah, we have three types of repo release, testing and experimental. In a release, we put all version which is G or G ready. Sometimes, we put some better versions, but we put them into testing repo or experimental. What does testing repo mean? Testing repo means that any of these packages at any time can begin to become G. So we are testing them. And experimental is just our testing build and alpha, better versions? So never, never, never use experimental or testing repo in production? Because at anytime packages can be changed there. And there might be some issues. They're still in testing, huh?

**Matt Yonkovit:**  
Okay. Yeah. And so if you want to test out some of the new features beta builds, just be mindful that you would have to change that from release to testing or experimental.

**Evgeniy Patlan:** 
In general, it's easy visit script because, for example, let's check which repo are available now are enabled now. Percona release shows and say, Hey, we have enabled originals. This is all huge repo URL, it's gonna release script. So at any time you can get update for the Percona release package, and we already have enabled psmdb50 repo. If you want to enable, for example, this repo, you just want to see testing and it will, Hey, we have to enable through this. So in this case, for example, you're using psmdb50 in production, you installed the latest packages any and finally you enable testing repo run up upgrade, it will update

**Matt Yonkovit:**  
to the to the testing. So whatever the latest one is it will overwrite Yeah. So that is something that you should be careful of. How would you remove the testing if you did that by accident?

**Evgeniy Patlan:** 
I will disable

**Matt Yonkovit:**  
ah see, look at that, see how easy it is. There we go.

**Evgeniy Patlan:** 
And here it is. Sometimes also, there are some tricks. For example, you want to add some products have dependencies, for example, you want to use XtraBackup together with PXC, PBM together is PSMDB. So you don't need to type to enable repo by repo. You can, for example, say Percona release setup ps80. Let's check. What is going on now. It disables all enabled repositories. And enable Percona server 80 repository and Percona tools repository. Okay. Why is needed? because in PS 80 repo we have Percona server. But in tools, we have Xtra Backup Percona tool kit and some other stuff, for example, you want to test your setup, and you want to run sysbench. It's also in tools repo. But if you want, for example, only the XtraBackup, on any repo on any your system, you can say, hey, enable only pxb. And it will disable also all repos and enable only the XtraBackup repo.

**Matt Yonkovit:**  
Yeah, and the reason that those who are watching would want to do this is that a lot of these packages, especially older versions, if you have incompatibilities could impact one another or not work as expected. So if you've got a version of XtraBackup, which is really old, it might not work with the latest version of Percona Server for MySQL, or vice versa. If you have one that's really new, there might be some compatibility issues. And so the idea is the repositories get disabled to prevent sort of those issues from occurring.

**Evgeniy Patlan:** 
Yeah. And also while talking about repos, I cannot say anything about our distributions, because our distributions are currently our flavors. And what is distribution in general, distribution is just a set of components, which we confirm that they are tested and correctly work together. For example, we have such distribution for PXC Percona XtraDB Cluster for Percona server, Percona Server for MongoDB, Percona PostgreSQL setup, and how it works, what is inside distribution and how to work with them. Now, if you want to install Percona server 80 for example, you need to enable Percona Server repo then you need to enable PXB repo to have it inside. But also we have distribution repositories, which contains a bigger amount of packages. Let's just check what is inside them. For example, let's use pdps repo 80 26. So Percona release set up

**Evgeniy Patlan:** 
pdp-8.0.26 release. Tipo! Yeah, thanks. So we enabled it. And currently, you will get only one version of Percona Server Xtra backup. Additionally, we put here Orchestrator let's check the web, it will be faster. So what we have MySQL shell, Orchestrator,  Percona toolkit, XtraBackup, proxysql.

**Matt Yonkovit:**  
Yeah. And so the reason, like for those who are watching, just to explain a little bit behind the scenes here, one of the things that we found quite early on was, there's a lot of really great software and packages out there people use with MySQL or Mongo on a fairly frequent basis. And so the idea is these distributions repositories put all of the versions we know to work together, have all of those common tools out in the ecosystem into one package. So that the version of the orchestrator will work with the version of MySQL, we're shipping. So all of those kinds of bundled together and give you a full list of things that are kind of version locked to upgrade, lock and step and in work together.

**Evgeniy Patlan:** 
Yeah, and an additional tricky thing about our distributions is that we create a separate repo for each distribution. So you can stick only for one version of any product. So if you don't want to make any updates, and you want to use Percona Server for MySQL, 8.0.25, use the tabs on this repo, as I said, You will never get any updates, in order to update to 8.0.26, you need to enables this repo and only after that you will get update. But if you still want to have this rolling updates, you need to enable another repo, it will be pdps-8.0. And only in this repo, you will get updates.

**Matt Yonkovit:**  
So you have the capability to either use the full 8.0 branch and follow along and update as updates occur. Or you can pick a specific version. So so really, I think most people will probably end up using the 8.0, the more general with the updates included and then update as they want. But if you do have that need to lock into a version and you want to prevent it or prevent an accidental upgrade, when you're not ready, you can lock in and then upgrade as you go. And,  quick question for you Evgeniy, you tell me so if you're going to go from 8.0.25 to 8.0.26. Is the upgrade path still the same then? So is it just you change the repository, and then you run the apt? yeah, update. Okay. There you go.

**Evgeniy Patlan:** 
Just the same as usual, which is easy as possible. Yeah. So yeah. I also think it's really useful, for example, for PostgreSQL setups, because still, there are a lot of nine bushings installed everywhere. It's a rolled. Yeah,

**Matt Yonkovit:**  
yeah, yeah. Yeah, there's a lot of older versions of Postgres for sure.

**Evgeniy Patlan:** 
Yeah, that's why just enable one repo. And you're there, the packages will never been updated, before you decided that it's high time to update them.

**Matt Yonkovit:**  
 Well, but that's not 100% True. Is it like so if there is a What about a point release or a sub release? If there's a fixed 8026 And it's a hotfix or something that needs to get fixed because of a CVE? And it doesn't increment it to 27? Because we've seen that sometimes.

**Evgeniy Patlan:** 
They will update packages in exactly this repo. Yeah.

**Matt Yonkovit:**  
Okay. So so there is a caveat to that. So it's not going to upgrade to 8027. But if there was a fix or something that needed to upgrade to 8026 Yes, typically then it would get included in that and so that fix would then show up.

**Evgeniy Patlan:** 
Yeah, additionally what I want to show is how it works on CentOS 8 and Red Hat 8 systems because there are some differences between Ubuntu and Debian. So, let me just copy/paste

**Matt Yonkovit:**  
and just while you're doing that, just so everybody knows once you have those repo set up, it's just like adding any other package. So just apt get, Percona server things like that.

**Evgeniy Patlan:** 
Oh, interesting. Oh, it's because it's CentOS 7.8 and it's already the end of life. And wait, do I have any other got Rocky? Oh eight, you have rel eight.

Let's try Rocky. But it might be a bit old image. Rail, it's not very useful, because it's nice to have a subscription for it.

**Matt Yonkovit:**  
You have a nice Slackware one there. I see. Ooh. Slackware. Haven't you? Slackware and yours?

**Evgeniy Patlan:** 
It was a question on the forum about the install compiling XtraBackup on Slackware. Wow, I decided that hey, there's any way I could change this.

**Matt Yonkovit:**  
Oh, wait. So if anybody's watching and if you're running Slackware? Like, tell us I'm curious. Like, is anyone out there running? Slackware? I mean, seriously, I haven't seen someone run it in years. I mean, I guess. Possible, but wow.

**Evgeniy Patlan:** 
And the results of this built is here. So it was possible to compile, compile XtraDB on Slackware like Wow. Okay, let's try Rocky Linux seems works well.

**Matt Yonkovit:**  
Now I don't know. it's interesting. So as we talked about the CentOS thing. Now with CentOS gone, people have started to move around to different things. I don't know how many people are going to stream versus looking at these alternatives yet. But I think a lot more are really, really considering the alternatives.

**Evgeniy Patlan:** 
Yeah, because there are already  syncs with CentOS eight before it's gone EOL. For examples, there was some cases. So once they removed packages from repo, they added new version, but removed old one. And all packages said tests, brushing dependencies were broken. It wasn't possible to install them. For example, we had such an issue with our PostgreSQL packages, as they depend on LLVM. Okay, and CentOS say just decided, hey, let's remove these packages from repo. And what should we do we compile the LLVM and put it into our repo.

**Matt Yonkovit:**  
Yeah, so we got to fix those things, right?

**Evgeniy Patlan:** 
Yeah, if operation system doesn't work, then we should fix it. Yeah. And in order to add any package in module, you can just do it as a patch release for it. And it's not so easy. So sometimes you need to disable modules. But how we can make our users life easier. Our script detects if it needed to disable module or not. For example, let's setup ppg-14.1. And it's ask. Hey, I need to disable modules. Do we want to disable it or not? Literally we want, but it's not very good idea to do this automation, because nobody runs a setups many away. Everyone has Ansible, puppet, run in AWS and so on. So it's not very convenient I will say.  What we can say, we have an automatic way. And we installed our repo. And modules were disabled. So in any case, you can make this work automatically and for manual setup. To check what's going on, you can disable it. Oh, yes, for what we can say. It is finish about, repo set up and so on. And we can move forward. So build

**Matt Yonkovit:**  
so I'm gonna ask the thing that's on everyone's tongue. So so, you're gonna, you're gonna build for VM one right now, right?

**Evgeniy Patlan:** 
No, not yet.

**Matt Yonkovit:**  
No. Why not? Why not? So I did get this question over the weekend. So so before we move to builds let me ask this question here. And you know that this, this will be an interesting one for me. So what extra work has to go in when you're going to build for something like an ARM processor?

**Evgeniy Patlan:** 
In general, I would say is it just check build flex? What would be different? Yeah. Yeah. And so because we just need to start doing it, I can't say, hey, we need to get these dependencies, these dependencies, let's start doing it. And while doing it, we will see what's going on how I made our builds, I just started, well, when I see an error, I investigate it, and move forward.

**Matt Yonkovit:**  
So it's just a process of starting the work. But as you get into something like that, because that's a whole new architecture. So the risk is always without the right build flags, it could still build, but it's going to slow down, or there's going to be some error later on when you're running that you might not know. So you really rely on a lot more QA testing for those, right?

**Evgeniy Patlan:** 
Yeah. And his main part of the work would be on QA, because I can build even sometimes miss wrong build flex, but it will work differently and incorrectly. And it will be QA tasks to verify if it builds correctly, and if it works correctly, because what I can check, I can build it, I can install package, I can install package, I can update package and run some parameters. That's it. Because I don't know what should be inside of it. Some stress testing some performance testing, some QA.

**Matt Yonkovit:**  
So it's interesting because one of the other questions that came up over the weekend because I was doing a QA for Peter. On his, he did a CPU architecture, talk and foster. So of course, arm comes up, right because it was one of the things on there was arm, but also power PC or the open risk came up and it's like, well, that's even yet a nother architecture that might have idiosyncrasies.

**Evgeniy Patlan:** 
Oh, well, I met a few bills for power eight architecture. And I wouldn't say it was much different from our standard 64 bit architecture and the architecture.

**Matt Yonkovit:**  
Okay. Okay. And so, so from a power perspective, the builds you've done, it was not a terrible change to switch architectures there.

**Evgeniy Patlan:** 
Yeah. I spent maybe two or three days and the product was built correctly and worked correctly. And also I included in this time, automation, I prepared build script, I prepared the pipeline. So everything was done. And it worked.

**Matt Yonkovit:**  
Okay, great. Okay. So let's assume that we're going to build and if you want, I'll just plug in my Raspberry Pi back here. And you can just build on that right now. AWS? Oh, yes, you can, you can use the Graviton. But anyways, go move forward telling show us how someone might want to build in honestly, there's not that the very few people still build from source some do. In normally, it's it's more of a, let's say, a relatively small percentage of the population. 

**Evgeniy Patlan:** 
you're gonna be surprised, but a lot of questions on forum about builds?

**Matt Yonkovit:**  
Well, of course there might be a lot of questions, but I still think that the vast majority of people are going to stick with a repository or a tarball. If they unless there's a need. I don't know, what do people who are watching think? Is there any love for building these? from source? Of course, you build from source? Yeah, of course you do. Yes. But I don't know. Is there anybody out there? Who is doing that for their own production systems? And if so, why? I'm curious. Because I think from a repo perspective, you kind of get that QA tested verified with all the correct build flex, but go ahead and show us the correct way to build from source.

**Evgeniy Patlan:** 
Yeah, because our way to build from source is just common for all Percona products. We have done a build scripts for them, for example. Which products do you want us to build?

**Matt Yonkovit:**  
Which product? Yeah, let's do Percona server for Mongo.

**Evgeniy Patlan:** 
Okay. Let's use Mongo

**Matt Yonkovit:**  
I hope he doesn't say anyone but that one? No, right. Like let's say

**Evgeniy Patlan:** 
Let's use version five zero. So we have here Percona packaging repo directory. And inside it we have directory scripts. And here is psmdb builder. sh script. For example. I would open in a separate tab recorder so server for MySQL just to show that we have it. And we have you might sees it in most cases in just the same. A bit less flex, but is the same. So we prepared this build script. A bit small. Yeah. Relatively small

**Matt Yonkovit:**  
1200 lines.

**Evgeniy Patlan:** 
Yeah. What's this script can do for us? It can install dependencies. Because at anytime the main question would be Hey, what packages I need to install to build it correctly. And once you run build hey I forgot to install GCC I forgot to install some leaves for example, open SSL and correct version and forgot about additional modules and so on. This script will do everything for you. Additionally, it will get sources so it will prepare source tarball for you. The next stage would be prepare source package because we want repeatable builds and how we can ensure this is built as repeatable, just create source package and everyone can build as their own package just the same as ours from this source package. Also the script can prepare packages and binary tarballs. I will say one more time we have this scripts for any our product. So just download the script and try on it to see how to run it. So we wouldn't have enough time to build it to build from scratch, for example, Mongo, but I will show how it works and then stop. For example, download build script, it requires some build directory. I will do it this way, because it's easy. What will be the next step sudo? I like to see a huge output, because it helps me to find any errors. When it's minus build..., do it needs absolute pass to the bill, Director that's why I use this way and minus minus install depths. The main question and you see it detected, what operation system it is. And say, hey, this appeal and started installing all needed packages. The same way

**Matt Yonkovit:**  
So my question here is with this build script, is that going to then just grab all the dependencies or will it run the build itself? Will it actually start compile?

**Evgeniy Patlan:** 
No, because we pass on only installed apps. Okay. If you want to run build, for example, what we need to do for build we need source tarball. We need some sources to compile. So minus minus sources. Also, we can pass branch stack. Even we can pass a repo, because sometimes, for example, the developer want to build it from its own fork.

**Matt Yonkovit:**  
Yes. And so that's probably going to be a very common thing if you are going to build from source where I see it as your you've built something as an enhancement. And so how would you do that? How would you include your own source with this build script?

**Evgeniy Patlan:** 
Repo minus minus repo, and

**Matt Yonkovit:**  
then he just put it where it is

**Evgeniy Patlan:** 
GitHub, blah, blah, blah,

**Matt Yonkovit:**  
Ah, okay. So you can pass in the repo, then it will go get it and build it from that with the right flags. Yeah. But it needs to be a fork of our Percona server for Mongo for that to work.

**Evgeniy Patlan:** 
Yo, let's just open the script. And I will show you. We have a prom repo. And it's on GitHub

**Matt Yonkovit:**  
So then you would replace that or like

**Evgeniy Patlan:** 
Yeah, so so you can pass here anything you want. Or if you're doing a lot of builds, then you just can update this line in script and it will always use your own fork. So if we want to make build stuff get sources and it will just download sources, but sometimes well we don't know the sources we know that it builds we want to build tarball we can just say hey tarball ... build tarball. I don't remember exactly where's my help?

**Matt Yonkovit:**  
where's your help? Yeah.

**Evgeniy Patlan:** 
build tarball param. So we can pass them together. If we want to build RPM we can pass all three prams get services build source rpm and build rpm and it will go stage by stage first of all it will get sources and prepare source tarball and then prepare rpm and on each stage it will store artifacts. Each artifact will be stored in a separate directory for example, if it sources it will be called directory will be called source tarball Eva's RPM it will be called rpmc. If a tarball it will be called tarball and you use ye'll be able to use any of these artifacts. It's really useful because in build pipeline we use Jenkins and we need to store this artifacts and pass somehow. So it's easy for us we have artifact we just need to save it and pass the next stage Oh for example, you just need to have source tarball and just checks it ever since search character so just get sources as I said. So I want just to show that everything starts if I pass several params. And what did I say? Command not found Yeah, because we didn't finish this install because we don't have Git installed on the system, we don't have some dependencies this why doesn't work. Fair enough. That was the scene and the scene just shows it is a bit intelligence. It's again, detected that it's Debian and installed packages for Debian. Fair enough. And shows a script can be used everywhere in Jenkins locally in Docker, everywhere. It will install dependencies and built what you want. And again, the script is available for all our products. A bit another story for PostgreSQL because we still don't make a lot of changes for PostgreSQL. That's why we have separate repo service with build scripts. But still, we have same flex for all build scripts. So you don't need to say Hey, I yesterday I built Mongo today built Percona Server for MySQL what flex I should use? They are the same. And in my mind is on the correct way for writing build scripts, use the same flex, and it will make your life and everyone's life easier.

**Matt Yonkovit:**  
Make sense? Alright, so I don't see any questions out there. We've got about five minutes left here. So yeah, Evegeniy, is there anything else you wanted to show us? And I'm going to assume so I'm going to switch over to the other screen. And hopefully people can still hear me. I hope we shall see. But hopefully everyone out there is still hearing me no problems at all. Although it looks like I might have duplicated myself. We'll see. Hopefully, that helps with everything there. So, Evgeniy, thank you for coming today. Appreciate it. For those who are watching this live or after the fact, please like this, subscribe to our channel. Sorry about the sound issues we had earlier. Hopefully this will all get resolved as we go forward. We're trying out some new ways to stream and make this a little more interactive, make the screen a little prettier. So I do appreciate you all hanging out though. All right. Well, thanks a bunch.

**Evgeniy Patlan:** 
Thank you, Matt. Thanks.