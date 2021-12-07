---
title: "Recap From Percona Live and Percona Postgres Operator - Percona Podcast 32"
description: "Sergey Pronin, Kubernetes Operator Product Owner at Percona stops by again to chat with the HOSS about the current state of operators at Percona."
short_text: "Sergey Pronin, Kubernetes Operator Product Owner at Percona stops by again to chat with the HOSS about the current state of operators at Percona. We also get a recap of Sergey’s talks he shared at Percona Live, and about the latest entry into Percona’s Operator lineup, the Percona Postgres Operator. Check out Sergey’s talks from Percona Live including “Percona XtraDB Cluster Operator - Architecture Decisions”. Full recording of this session is now available for in-depth tech talk for free."
date: "2021-07-22"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-32-sergey-pronin/"
youtube_id: "Mj9c14cYYNs"
speakers:
  - sergey_pronin
aliases:
    - "/podcasts/32/"
url: "/podcasts/32-recap-from-percona-live-and-percona-postgres-operator"
---


## Transcript

**Matt Yonkovit:** 
Everybody, welcome to another HOSS Talks FOSS. I'm Matt Yonkovit, the HOSS here at Percona, Head of Open Source Strategy. I'm back with Sergey Pronin. Hey, Sergey, how are you doing today? 

**Sergey Pronin:**
Hello, Matt. Fantastic. Thank you. 

**Matt Yonkovit:** 
You know, you will be happy to know that today in this podcast I've recorded another one earlier with a different Sergey. So this is a dual Sergey for me. 

**Sergey Pronin:**
Lucky day for you, right. 

**Matt Yonkovit:** 
Yes. So I'm going to end with you, Sergey. And I started with Sergey. So it's like a double dose of Sergeys today, which is awesome. But for those of you who have listened to Sergey talk before, this is his third appearance on the podcast, because Sergey is doing all kinds of awesome work on what is one of the hottest topics in the tech space, which is Kubernetes and Kubernetes operators. And Sergey always has something interesting to say. And the big interesting thing that came out of Percona Live was the talk about our Postgres operator. And so I wanted to touch off with that. So if you haven't seen Percona has already released operators for Mongo and PXC or MySQL, if you will. And now we are working on Postgres. And I heard that we're looking at eta in August for that. Is that correct? Sergey? 

**Sergey Pronin:**
Yeah, yeah, Correct. Correct. 

**Matt Yonkovit:**
So, yeah, tell us about.

**Sergey Pronin:**
Yeah. So for Postres, as you mentioned, it was one of the missing pieces in our puzzle, right. So we have MySQL, we have Mongo, and we have Postgres as Percona company, we have distributions for MySQL, Mongo, and Postgres, right. And we also have operators for MySQL and Mongo, but we never had anything for Postgres, so we definitely wanted to add one. And the story was that we were thinking, Okay, shall we start from scratch and write everything from scratch? Or shall we fork some existing operator or work with some other guys on upstream? And we decided not to go with development from scratch, because it will take an enormous amount of time. And we chose a CrunchyData operator as the base for our recording operator. So now we forked it. And we are also committing our changes to the upstream to Crunchy as they also open source folks. And I'm pretty excited about that. During Percona Live, we released it as a technical preview. And it's going to be GA somewhere in August. And for us, what means ga is going to have the same look and feel as other operators that will have for MySQL on Mongo. So it will be a seamless experience.

**Matt Yonkovit:**
So Sergey, with Postgres, what are the unique challenges when developing that operator versus an operator for, let's say, PXC or Mongo

**Sergey Pronin:**  
I would not say there are some unique challenges, but Postres as well as MySQL. These are pre all technologies, which are not cloud native, really, which were never intended to run on Kubernetes. No one ever thought that. So there is all obviously challenged to make it work on Kubernetes. The challenge is always the data on Kubernetes, right? Because you need to keep it, you need to make sure that you don't lose any transactions in the process. And yada yada, yada, this is the biggest challenge on Kubernetes. It's not the database specifically, I will tell it like that. But for us, the big challenge would be the, for distributions, for Percona distribution for Postgres, we support multiple Postgres versions. And we need to do the same, or operator because we want to keep the theory. And this is the challenge for our team, because some of the baggage is outdated, we need to keep them updated. So it is the work of our building police team, operators team, and our engineering team. So a lot of hands are involved. And it's a great effort. But yeah, more or less, it's, it is still the database, and you need to run it on Kubernetes.

**Matt Yonkovit:**
So when we talk from a Postgres feature perspective, are we approaching what the parity with what we've already got in the PXC and Mongo operator?

**Sergey Pronin:**  
Yeah, it's a good question. Yeah, exactly. So the CrunchyData operator, which we're basing our operate on, is quite feature rich, and it is production ready. So all the features that they have, we can already use in our operator. And on top of that we are getting something from us like PMM integration, some customizations that we used to have, but more or less the barrier is there. And we're gonna get closer to it and make all our operators aligned. The biggest challenge it's, well, not the biggest. But one of the challenges that we have is the UI. In operators world UI is yml manifest, which was specified to run the database on Kubernetes. And we have certain standards in Mongo operator, in MySQL operator, and the way how the Crunchy operator was structured is not how we envisioned it. And we need to change it. This is the number one challenge for us. Because if we don't do this now, then later on, this would be the breaking changes for our users and customers. And we don't want to do that. And so we're doing all this cosmetic changes in UI beyond the stages.

**Matt Yonkovit:**
Okay. Okay. And when we talk about, like the CrunchyData operator, what features have we already added? Like, what are the gaps that we're trying to fill there?

**Sergey Pronin:**  
Number one gap was in CrunchyData. And we had some users who complained that the container images that CrunchyData uses in their operator are not free, they have their own development licence. And this licence allows you to run it only in a non production environment. If you want to run on production, you need to purchase something from Crunchy like support subscription, and then you can run it, then this is number one change. We're an open source company. And we changed it right away, we added our reporting distribution for Postres container images there instead. Another thing is, the container images that Crunchy was using were based on some I believe on, I believe, consent OS version, which is kind of dying now. And we are basing all our images on the UBI Red Hat universal base image. And this also allows you to run the operator on OpenShift, which is important for enterprise costs. 

**Matt Yonkovit:**
So there is OpenShift support as well. 

**Sergey Pronin:** 
Yes. Also, we are adding Percona Monitoring and Management. And also the interesting part with Crunchy when we first started using it was the part with end to end tests. And we kind of saw it recently CrunchyData released the 4.7.0 version. And when we started the mergers and started the tests, we saw that the recovery process is not working, point in time recovery broke completely and without look at what's going on. So what we're doing and what we already have for MySQL and Mongo, we have feature-rich, I don't know how to say, a wide scope of end to end tests, which will automatically run for every pull request. And that is a lot of work for our quality assurance team for our engineering team. And we want to make it right from the very beginning. So that we have, we have some standards of quality, and we want to give them at that level for all operators that we have.

**Matt Yonkovit:**
Okay, now let's go a little bit off of our specific operators for a second. Now, you mentioned one of the challenges with MySQL and Postgres is they were never designed for that kind of cloud native architecture. So we've seen this kind of rise of the new SQL databases, whether it's Cockroach,Yudabite, TAIDB, so there are, quote Postgres and MySQL compatible new SQL options out there. You know, they're not always compatible from a 100%, which is typically one of the challenges that companies have moving to them because it's a very different mindset when you shift over. What do you see those going, what's the growth of those new SQL versus some of the the operator thing? So it's more of a thought question than it is a technical one, but I'm interested to hear your take on that.

**Sergey Pronin:**  
Well, first of all, I think all this projects appeared for some reason, right either they this company was not happy with existing technology, or some big customer told the founder, hey, I need this feature in MySQL or some other database. So they are solving some problem that someone else has, right. But I believe that slowly, and I already saw in some other MongoDB forks and some other databases, or kind of all the other technologies that have huge traction from the community, they're going to catch up on these features. Like, if Postgres has enormous community. And if someone is interested in delivering the same feature as Yugabite has, for example, they will do it. And it's easier for companies to move to Postgres than us to go by it because it's easier to find people who knows Postres instead of finding people who work with Yugabyte, right, so I believe that more or less, the big companies or big databases that are now top five, they will slowly kill the ones that are appearing now, because they solve someone's problem, but it's not that big of a problem. And this can be solved in Postgres or other database, that's my way of thinking. 

**Matt Yonkovit:**
I mean, this is an open discussion. So just, I'm thinking as we talk here, I mean, but some of those those architectural decisions on like, how MySQL was architected, or how Postgres was architected, those are not easy changes, grab to catch up with some of that distributed system, it's a completely different back end. And I mean, I think that's where there's some compelling work being done, contrast and compare? I don't know, can you think that it is feasible for the Postgres community to re-architect Postgres in a way that makes it a distributed database?

**Sergey Pronin:**  
I think it is. I think it's feasible. It is hard, but with Postgres, Postgres is not a good example, I think Postgres is super modular, they have a lot of packages, and you just plug in some new package, and it just works. With MySQL, it's much harder. But it's still possible. And I don't know if MySQL or Oracle is going to be doing that, if they are interested in that, or if they have the sheriff's customers already.

**Matt Yonkovit:**
Yeah, I mean, and you see other projects that are coming up trying to solve the clustering and the distributed systems as well. Yeah, Vitess, for instance, is a good example. You know, you've got quite a movement to try and solve this, the scalability issue. So it's definitely an interesting space. Now, when we talk about scalability and availability one of the critical things in a lot of these systems is the ability to run geographically dispersed clusters or failover, between multiple data centres. Now, I know, on the roadmap for our operators is that capability. So, in other words you're running in a data centre in the US, and the data centre in US goes down, and then all of a sudden, automatically, you failover to a data centre in Europe. Tell us about that feature and that functionality, and when we can expect to see some of that.

**Sergey Pronin:**   
Yeah. Okay. This is a good one. The goal for operators is to run performance software on Kubernetes performance distributions on Kubernetes. Right. And our users, they can do a lot of stuff, VMs on bare metal servers with our databases. And when they go into the operator's space, they say, Okay, how can I do it? In the Kuban age? How can I do it with operators? And a feature like replicating the data between different data centres is not the operators and we're working on that. The idea is simple. You have 2 distance data centres, one in the East Coast, one in the West Coast. And you want to set up the replication between them so that you have disaster recovery in place and you can execute your disaster recovery protocol. And to do that with operators, we need to ensure that we can configure it through the operator on both outs on master or on Main and replica, right. That is what we want to do for our MySQL operator for PXC and for Mongo. It's easier for Mongo, it is just adding load into the replica set. But it's more complex on the code level. So in the operator, it's coming in the next release for PXC, and then the next-next release for MongoDB. But in reality, what excites me more in this feature is not the disaster recovery capabilities which enterprises want so badly. But for me, what is more important is that it allows the users to migrate from the bare metal databases where they run in their data centres to Kubernetes seamlessly, they can just set up the replication and the data just flows into the database on Kubernetes. And it's awesome, because there is a lot of pushback from DBAs to run the data on Kubernetes, because they say okay, it does not provide the same performance levels and does not have the same isolation, I don't like it. But we can make it work. Right. And that is why this feature, this disaster recovery, or multi cluster database deployment with operators, allows you to seamlessly migrate to Kubernetes, and then you can try it out. You can point some applications to read from the database on Kubernetes. And you will see that it's performance. It's great. Everything is awesome. So that is why I'm excited about it more than a disaster recovery.

**Matt Yonkovit:**
Okay, that makes sense. I mean, I think that it is a problem that many people are trying to solve. And so I think it helps, especially the enterprises who are looking to have that portability. It's almost like the failover between availability zones that you get in most cloud providers. R I mean, I think that's really the key critical thing

**Sergey Pronin:**   
is when the availability zones, it kind of already works. But between the regions. This is what he's missing right now. 

**Matt Yonkovit:**
You're right. Yeah. The regions versus availability zones? Yeah, sadly. And so, I know you were at Percona Live. And you did do a couple of these talks. So you had a couple talks, where you talked extensively about our operators, and kind of the benefits and for each of the ones that we have available. Those are all available online now. So if anybody is interested to learn more about those operators, you can head over to YouTube, or Percona’s website, and we have links to those. So you can hear Sergey go in depth on either of the topics.

**Sergey Pronin:**   
You can hear me talking more. 

**Matt Yonkovit:**
Yes, yes, we can hear all kinds of more Sergeyisms. But, Sergey, I appreciate you sitting down with me for a few minutes today to chat with me about what's going on in that operator space. Appreciate your insights into both the Postgres operator and the HA across regions. Both are very welcome news. And so thank you very much, and we hope to chat with you in the future.

**Sergey Pronin:**     
If you invite. I'm always eager to join you. 

**Matt Yonkovit:**
All right. Thanks, Sergey.

Wow, what a great episode that was! We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.

