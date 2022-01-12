---
title: "Kubernetes Operators and the Latest Trends in the Database Space - Percona Podcast 03"
description: "Sergey Pronin Percona's Product Owner for Percona's Kubernetes operators sat down to talk to us about using Kubernetes to manage databases, running Kubernetes on the edge, and where he sees the technology space headed."
short_text: "Sergey Pronin Percona's Product Owner for Percona's Kubernetes operators sat down to talk to us about using Kubernetes to manage databases, running Kubernetes on the edge, and where he sees the technology space headed. We talk to Sergey about his latest blogs covering:

* [Building A DBaaS with Kubernetes](https://www.percona.com/blog/2021/02/08/dbaas-on-kubernetes-under-the-hood/)

* [Running Kubernetes on the Edge](https://www.percona.com/blog/2021/01/13/running-kubernetes-on-the-edge/)

* [Draining Kubernetes nodes wisely](https://www.percona.com/blog/2021/01/20/drain-kubernetes-nodes-wisely/)


Don't miss the latest episode of the HOSS talks Foss.  "
date: "2021-02-17"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep03-talking-databases-on-kubernetes-k8-on-the-edge-operators-and-more/"
youtube_id: "Qx-tKmucomc"
speakers:
  - sergey_pronin
aliases:
    - "/podcasts/3/"
url: "/podcasts/3-kubernetes-operators-latest-trends-in the-database-space"
---

## Transcript

**Matt Yonkovit:**  
Hi everybody. Matt Yonkovit, The HOSS, Head of Open Source Strategy here at Percona, I welcome you to another Percona Tech Talk, where we're gonna bring you the best in the open source space and give you the most interesting and fun speakers ever. We hope you enjoy the show. Hi, Sergey, thanks for joining me for a quick chat here. Sergey, you've been with Percona for a few months now. Right? So you're fairly new?

**Sergey Pronin:**  
 Yeah, it's like months?

**Matt Yonkovit:**  
Yeah. So maybe, maybe tell us a little bit about you, and what you're working on. And then we could talk a little bit about these, these awesome blogs that you've been putting out there and some of the work we're doing around our Kubernetes operators?

**Sergey Pronin:**  
Sure, sure. Gladly. So as we mentioned, I joined Percona, like three or four months ago, I'm fairly new to Percona and into the open source community. I'm a product owner here, and I worked on our Kubernetes, cloud and operators stuff. And before that, I was working in merger and acquisition business. And we were acquiring lots of companies. And we're putting them all on our sample platforms. Of course, Kubernetes as a service, database as a service, VMware as a service. It was quite an interesting time back then. And they're also started looking at switching my job from engineering management, product management. I ended up here, and also I got interested in open source in general, how it works, how it makes money. What about the community, helping the whole community to build new awesome things. I was very curious about that and decided to join Percona as an open source, I think open source leader nowadays.

**Matt Yonkovit:**  
Yeah, yeah. So you mentioned that you were you were in this company that was that was acquiring companies and kind of moving them to their platform. And Kubernetes was one of those, the those basic building blocks, why is Kubernetes getting so popular? You know like you've seen this growth, you've been part of it?

**Sergey Pronin:**  
Yeah. So it's kind of an emerging technology. If we look back how it started, it was first bare metal and servers, right? Then, VM virtual machines were introduced, and they were produced to pack things more tightly on a single server and make it possible to move them from one thing to another. And then Docker. And Docker appeared to answer the challenge of the market. So the people and businesses wanted to deliver faster, and to have smooth pipelines of software development, and Docker. And containers jumped in just nicely, right. And then after some time, once Docker appeared, people started thinking, okay, now I have 1000s of Docker containers, what to do with them? How can I move one container from one place to another, and then Kubernetes kinda jumped in and said, Hey, you can do everything here, right? You have a single control plane, a single entry point, you can just give me some Yaml files, and I will do everything for you. Right? And now Kubernetes is kinda emerging. And sometimes it's seen as a silver bullet for most of the companies, and they see companies can solve all their problems. And it's not obviously

**Matt Yonkovit:**  
Wait, wait, wait, you can't just solve the world hunger war, famine, like everything with Kubernetes. I've been misled. I'm just talking.

**Sergey Pronin:**  
Now make your camp right. You need to apply some other skills as well. But given that it is a good tool it is just an automation tool that helps to orchestrate your containers, right? For one small startup, which is just running an MVP. Is that okay? I will use Kubernetes. It's a mistake. Right. And in this merger acquisition business where I was at, yeah, we were moving some parts to Kubernetes. But it was not like a lift and shift in prices. So when we acquired a company, it was right in some data center. Obviously, you should not move all this stuff to Kubernetes. Because not everything can feed into Kubernetes. Some stateless workloads. Sure, databases with coordinates are possible as well with operators. Sure. But some other workloads, like super complex one for banking, you cannot cram them in. It's not feasible like huge Oracle VMs. You cannot pack them into Kubernetes right away. You need to smash them into microservices. And then we've probably moved on, right? So yeah, it's a complex process. And more and more businesses understand that they need Kubernetes to deliver code faster to production, and with the help of containers, and that is why this is an emergent technology nowadays.

**Matt Yonkovit:**  
And it's interesting, you mentioned databases because honestly these containers and Kubernetes were never designed for databases originally, I mean, it's, it's the add on kind of effect. And similar as you, as you mentioned you start to get 1000s of containers, and you, you start to break out your microservices, and you get just I know of companies that have 10s, if not hundreds of 1000s of containers that they're running and, and just 1000s of microservices all over the place, each one of them wants a database, right. And as you start to build that developer development enablement or the development pipeline ecosystem for your teams, the database needs to be part of it. And that's where databases are being pulled along, kind of kicking and screaming into that Kubernetes space and into that DevOps automation pipeline. And we've, we've seen things like outside of Kubernetes, as well, like, TerraForm, for instance. and certainly VMware has their solutions. We've seen the Tanzu marketplace around there, and Pivotal is now kind of pivoting more towards Kubernetes. But there's been a lot of solutions that have been focused on trying to solve managing the herd of not only applications but databases. And that's why it's really important, from a database perspective to ensure that your databases are properly set up, to use Kubernetes. And that's why the work that you are doing on operators is critical to make sure that people can get stable, consistent performance and setups, because it's kind of complicated.

**Sergey Pronin:**  
Yes, definitely. But it's also very challenging and interesting, but you mentioned it correctly. So Kubernetes started as a tool to run your stateless workloads. And developers and operations teams, they were running on stateless workloads and Kubernetes, and they had the data somewhere, right? If they run in the cloud, it's something like Amazon RDS, or whatever it is, some of the tools. And running a database in a container, even nowadays, is not the norm, right? People don't believe in it. But we see in the corner that already 80% of developers report that the runway and databases dock already, right? So it's a lot. And it's, it seems like not a problem. And then you come to another challenge, where you have your data somewhere on Amazon, or Google Cloud and some managed service. And you quickly need to move from one cloud to another. What to do, right? And Kubernetes, again, jumps in just nicely. It's a hybrid cloud-ready tool, which can move your workload from one cloud to another with a few clicks, right? And that is where operators jump just nicely. You have your database as a set of Kubernetes Yaml standardized, which you can move from one Kubernetes cluster to another easily and it does not depend on the cloud specifics, right, it can just move it along. So yeah, running databases in Kubernetes is, I would not say it's failing a new concept. There are some other companies that are running the best platforms and Kubernetes. And we want to do the same because we see that it is requested by the community by the customers.

**Matt Yonkovit:**  
Okay. And so what kind of challenges have you been running into? I mean, you've only been here for four months, but as you've gone out and started to work on the operators. it's not always easy. you mentioned it's a challenge. So what are some of the common challenges that you're running into?

**Sergey Pronin:**  
Well, I think if we talk about operators in general, without touching the databases, I believe the biggest challenge here is quality assurance, QA when he writes the code for Kubernetes, whether you for operators specifically, you need to test a lot of different variations, like you need to test various Kubernetes versions. You need to test various database designs, you need to test various flags and Kubernetes like service type load balancer, whatever we have there. And there are like hundreds and maybe 1000s of permutations that QA needs to think about. and test. This is the general operators problem in Kubernetes's problem, I would say. And the challenge with the database in Kubernetes is that initially, when I just joined, we thought, okay, what what is it about, it's just running the database in the middle, just run it, like setting the image, and you're set, but it's not right. And I saw some products outside there, which do exactly the same, they just think that, okay, if I put my Docker image in, in Kubernetes, and run it there, it will work and my database will work. It's not right. So you need to build a lot of code around there to support the database itself. Because if you just think that Kubernetes can manage the data very well, right now, it cannot, because you will lose data if you just think you can run your databases.

**Matt Yonkovit:**  
It's the stateful application of databases, right, I mean, that's really the driver. So you've written this blog, and I know, a lot of companies are buzzing around the buzzword, edge computing. Right. it's, it's, it's something that is it's a legitimate thing, and for those who are watching who don't know, what edge computing is, it's running machines as close to the source as possible. So, if you've got multiple locations, you have machines in each location. So you wrote an article on running Kubernetes on the edge, and maybe you could tell us a little bit about that and your thoughts on running multiple Kubernetes clusters in different locations and running them as close to that source as possible.

**Sergey Pronin:**  
Sure, sure. So Kubernetes is an orchestration platform, right? And when I first heard about the edge, I never thought about Kubernetes, being able to without, and then I read some articles and ran some experiments, and I saw that it was spring grade one. And the reason for that is the edge is, as you said, it's just bringing your computation power closer to the source or your end devices, I know you have a camera, doorbell, whatever it is connected as an IoT device to the internet. And you need computation power to support that. I don't know, maybe for Dobell, you have video encoding or something like that, you need to do that there, right. And Kubernetes just helps you to bring this computation power closer to your devices, without changing your development pipelines or whatever, you don't need to invent anything, you don't need to think, Okay, how do I ship an update to my doorbell? How do I ship an update to my video server? You just have Kubernetes. And it's a standard YAML file thing? You just shoot your Yaml file, and you're done. Right? So this standardization of Kubernetes kinda works super great. If you want to build your own micro cloud, or you want to manage hundreds and 1000s of devices right away.

**Matt Yonkovit:**  
I mean, like, yeah, sorry to interrupt. But I mean, I think where it's interesting is it's that portability, right? It's the, drop it into the different locations, and you can expand and shrink as needed. I think that that's really

**Sergey Pronin:**  
Yeah, yeah, exactly. Portability is great with Kubernetes as well. Correct. And, in general, sometimes people ask, okay, why do you want to run Kubernetes not just simple containers? And the answer is, if your system is complex enough like you have only one container, you have 10 containers to support the system. You need Kubernetes, because, again, you need some orchestration to move these containers around. So this is why.

**Matt Yonkovit:**  
So Sergey, let me finish with this question for you. Are there technologies or trends that you're either excited about or concerned about that are happening? right now, we're trying to look forward? I like to ask this question because that way people can understand what the experts are seeing. So are there certain trends or technologies that you're extra excited about or are really concerned about?

**Sergey Pronin:**  
Okay, okay. One of the technologies that I'm really, really excited about is I will say Kubernetes, again, about Kubernetes as the control plane to manage not only containers but VMs, as well. So I saw it, there was a project called Project Pacific from VMware. And they renamed it to tanzu later on, and now it's called Tanzu grid, I think. And it's super cool because it allows you to manage all your current infrastructure and the new one where you want to migrate to containers to a single Kubernetes control plane. And you don't need to change anything at all. You just move your workloads from VM to Container seamlessly. It's super great. And I believe this will be a game-changer for huge enterprises, which are currently stuck with legacy, data centers and some mainframes and they want to move forward to some new emerging technologies. And this whole thing will help them a lot.

**Matt Yonkovit:**  
yeah, yeah, that's really cool. Like if you can manage VMs, and containers flip between them seamlessly that that has benefits because there's a lot of times VMs are better than containers, containers are better than VMs. And so you've got to be able to pick the right tool for the right job.

**Sergey Pronin:**  
Correct! That's right. As I said, I don't believe in Kubernetes as a silver bullet. So VMs will stay there for some time, for sure.

**Matt Yonkovit:**  
Right? Yeah. Well, alright, Sergey, thank you for sitting down with me and chatting with me today. I really appreciate it. And let us know if anything new and exciting comes out. We'd love to chat with you again. And we'll be looking forward to checking out your blogs.

**Sergey Pronin:**  
Thank you. Thank you, Matt. Thank you for having me. Have a good day.

