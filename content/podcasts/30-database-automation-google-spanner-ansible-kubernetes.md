---
title: "Database automation, Google Spanner, Ansible, Kubernetes - Percona Podcast 30"
description: "Derek Downey who recently joined the Google cloud team to talk about his career in the database space, learning Google Spanner, Ansible, database automation, Kubernetes, and more."
short_text: "Matt Yonkovit, The HOSS, talks with Google Dev Rel Engineer Derek Downey who recently joined the Google cloud team to talk about his career in the database space, learning Google Spanner, Ansible, database automation, Kubernetes, and more. Derek recently gave a talk at Percona Live entitled \"Practical DB Automation Ansible\", and has been active in the open source community for over 10 years."
date: "2021-07-15"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-30-with-derek-downey-developer-relations-engineer-google/"
youtube_id: "x1OKIxzI6kA"
speakers:
  - derek_downey
aliases:
    - "/podcasts/30/"
url: "/podcasts/30-database-automation-google-spanner-ansible-kubernetes"
---


## Transcript

**Matt Yonkovit:** 
Everybody, welcome to another HOSS Talks FOSS. I'm here with Derek Downey. Hi, Derek, how are you doing? 

**Derek Downey:**
Hi, Matt. Doing great. How are you? 

**Matt Yonkovit:** 
Good. So Derek we're wanting to talk a little bit about what you talked about at Percona Live. But before that there was some exciting news that I saw on the Twitter slash LinkedIn verse. You've just joined Google. Congratulations on the new role. If many of you don't know Derek, Derek has been around the MySQL space, and the open source database space for Oh, gosh, 10 years. I think we think I originally interviewed you for Percona, like 10 years ago.

**Derek Downey:**
Close to about eight years ago, but I was in the MySQL world. Well, before I even dared to apply to Percona. But yeah, it's been a while.

**Matt Yonkovit:** 
Yeah. And you worked at Pythian for a while, you worked at solar winds. And now you're at Google. So what are you gonna be doing at Google?

**Derek Downey:**
Yeah, so I'm working as a developer advocate at Google Cloud, focusing on Google Clouds, database offerings and services. Cloud SQL will be part of it. My initial focus will be on Cloud Spanner, actually. The big product at Google Cloud has around relational databases, distributed databases. So we're very excited about that, actually.

**Matt Yonkovit:** 
Well, yeah, and Spanner is one of those technologies that has just generated so much innovation in the space when you talk to like, gigabyte, they're like, Oh, this is Postgres and other things with Google Spanner you talk with Cockroach, they say a very similar story. I mean, Spanner is really kind of the granddaddy of all of these technologies.

**Derek Downey:**
Yeah. And so I'm really excited about that. I mean, they're solving a thing that has really been hard to solve in a MySQL database. So there's this distributed data store yet still retain a lot of the SQL layer relational aspects, that I guess noSQL database has tried to do away with it for a while. 

**Matt Yonkovit:** 
Oh, yeah. Right. I mean, it's the trade offs, right? It's the CAP theorem. You've got to trade something off in order to get the other two.

**Derek Downey:**
So there's an interesting debate about Spanner. Does it destroy the CAP theorem? And there's a couple of talks that I was watching recently about. I can't remember his name, but the person who created the CAP theorem developed it, wrote about it, basically saying Spanner does not destroy the CAP theorem. And it's basically agreement that Spanner trades off partitioning, right, like, it's just a very low chance that that partition is going to happen. So that's how it kind of avoids that.

**Matt Yonkovit:** 
Well, and I think it's similar with a lot of these other technologies, they're willing to trade off some of the either the partitioning or like, availability, even because they figure that the underlying hardware now or the cloud infrastructure is going to be highly redundant anyways. So there's always these things to mitigate one of those areas, which is always an interesting thing to dig into, and to look at. So where do you fall? So do you think that CAP theorem has been invalidated now by Spanner?

**Derek Downey:**
No, I think a lot of it is like, we still trade off partitioning. But like you said, we've mitigated the risk of that by being redundant. 

**Matt Yonkovit:** 
Yeah. And so if you're listening, and you don't know CAP theorem, it is the idea that you can get two out of the three big areas, which is consistency, partition tolerance, or availability. And so in any clustered system, you basically pick two out of the three, and then the other. The third one kind of like, gets minimised or even eliminated in many cases. And most databases will pick two of the three, and you know that there hasn't been any that has crossed all three. 

**Derek Downey:**
But anyway, that's what I'm doing around that. So developer advocate, if you're not familiar with the term, what I'm the way I phrase that is, I'm helping users use Spanner, like if you don't know what Spanner is, and you're just getting started. Like I will be helping put content out there to train you on the concepts around it. But also, it's kind of a bridge between the users and the product team where I'm taking that feedback and going back to the product team and saying, hey, this could be improved or are we missing this feature or things like that? So it's kind of like that bridge between customers and the products.

**Matt Yonkovit:** 
So your role is not only to help educate people and get people to understand what they can do with it, but also make the product better. 

**Derek Downey:**
Right, exactly. 

**Matt Yonkovit:** 
And so for those who are using Google Spanner, like, what are some of the use cases that you've seen early on? I know, it's only been like, a few weeks now but Spanner has been around for a while. So what are you seeing in some of those use cases that people are deploying it for?

**Derek Downey:**
You know, I'm not gonna be able to speak with any authority on use cases here. Basically, one of the beauties of me becoming a developer advocate for Spanner is I really am net zero, other than a high understanding of how they're solving distributed SQL. But there's all like, there was a big demo that they did at Google Next, back in 2019, back when things could be in person and things like that. But anyway, the demo was all around like a ticketing system. Okay, so distributed, like you're buying and selling tickets to events all around the world, you only want to sell one ticket. So, I mean, that's a classic use case of it. I imagine financing would be a good use case, because you have potentially Bitcoin, like all these things around the world, and it's like I'm just kind of spitballing some ideas. You know, the idea is that you need that consistency, that durability, acid compliance for a distributed database, a globally distributed database. And so anything? If you're not in that space, then you probably don't need Spanner, you know?

**Matt Yonkovit:** 
Well, we look forward to seeing what you learn with you, we and seeing, it's always fun when you learn technologies together. And if you've got someone who's walking through that journey, it's an awesome thing to kind of walk with them. And experience what other people would do, if you've been in the space for years, it's very easy for someone in the MySQL space, for instance, like myself or you to probably overlook some of those things you just inherently know. And so oh, what do you mean, you didn't do this? Oh, you should have done that coming out.

**Derek Downey:**
And I find the questions that come out of sessions like that to be very enlightening, because, like, we're all coming in from our different perspectives and our experiences. And it's like, Oh, I didn't think of it that way. So how do I solve that? 

**Matt Yonkovit:** 
Yeah. So we mentioned like, you talk to Percona Live. And so one of the things we wanted to get you on to talk about was your topic, which was talking about using Ansible to do automation around the databases. And here's the thing. I mean, I know, in your new role, you'll probably see this quite a bit. And you probably saw this in your older roles as well. Everybody has a bazillion databases now. It's not just like, when I started, there was like, the database, right? Like and I'm dating myself, but you know oh, the database is down, everybody knew what the database was, and the database is down. Now, there isn't the database. It's which one of 10,000 databases?

**Derek Downey:**
And yeah, so that's, that's an interesting, like, observability problem, too. It's not just automation. Sure. Yeah. But God was your question. 

**Matt Yonkovit:** 
Yeah, yeah, no, no, I mean, and this is, this is where it puts it to the forefront. How do you manage? How do you deploy? How do you ensure that everything is consistent across this massive realm of databases, everybody wants their own database. And so you talk about Ansible, other people use Kubernetes, other people use Chef, Puppet for orchestration, any tool you want. But maybe talk to us a little bit about, like what kind of brought you to Ansible. And what you see in this space, where he's everything is just kind of exploding and in terms of the size and amount of databases.

**Derek Downey:**
Yeah, it's a great question. Like you said, automation means a lot of different things to a lot of different people. There's a lot of different tools out there to solve a problem. My talk on Ansible was as an example of solving some problems around the databases with this particular tool. I really got into Ansible. You know, when I first started at Pythian a couple months ago, there was a project that I was working on that really had this customer with about 20 databases distributed like in a three tier replication architecture across three different data centres. And we pointed out, hey, there's some issues with your architecture, you might want to kind of reduce that a little bit for dr reasons. And so they said, Sure, let's do that. So it was my job to write the run book, basically, to squash this tear of 20 databases into a two tier system. So I did that, I wrote the runbook, it was along the lines of login to the node, stop replication, let it catch up repoint to the primary, whatever, the new primary at that time, it was binary log positions. So you have, you have to figure out the right positioning, right, so have a completely different parent. So anyway, it was gonna take, let's, let's say about almost two hours to do this entire maintenance. And that is with being cautious, and hopefully not making any mistakes along the way, and pointing it to the wrong server and having to rebuild and all that fun stuff. My manager came in, this was when I first started pythian, this was 2013 time period. He's like, Okay, I'm gonna write this, and Ansible. And Ansible had been out for about a year, maybe at the time. So this is Ansible 1.2, or whatnot. So really fresh technology. I'm like, Oh, sure, whatever. He writes this thing, completes the maintenance in five minutes. I'm like, Oh, that's awesome. That's what I really had, like the light bulb go off that there is a better way to deal with some of these tasks than manually and runbooks, even runbooks get you somewhere there. And they're all trying to solve a specific need of mitigating risk during maintenance, right. But you're still typing and cutting and pasting and all this stuff. Whereas if you can write some automation around it, that and have a good script, then you cut out the need for copy, or the potential for even those copy and paste errors. So that's when I really started developing a love for automation. And yeah, Ansible was my if you skip the whole bash scripting custom scripts, and get into a framework Ansible was my first exposure.

**Matt Yonkovit:**  
And this is really, for this use case, you're talking about here. This isn't necessarily about the herd mentality. It's about saving time and efficiency, and reducing errors.

**Derek Downey:**
And safety. Yes, yes, absolutely. And that's what I think automation on the data layer is all about is like saving time, providing a little bit of ROI for your time, so that you can get back to the real critical tasks. And then reducing errors, because the data environment is probably your most critical environment that you don't want mistakes on. So, anyway, I started with Ansible. I, since have expanded into, like you said, containers and somewhat Kubernetes more recently, but Terraform for sure. So my presentation was really like, if you're not automating, then why not? And here are some practical tips to get started in the database management realm, if that's where you're coming from. And then I ended with some cautions on Hey, just because you are now starting with Ansible, there are so many other tools out there and you need to be evaluating. Do I really need to be automating this isn't worth the investment? And also how to avoid..

**Matt Yonkovit:**  
So really, there isn't this magic automation button that just makes everything better? You know, so you have to think about it, because there is the cost of building the automation. And so is the cost worth? Is it justifiable? Exactly the important aspect of that, I think that that's an often overlooked one, because I think it's so easy to get caught up in the swing of, I'm just gonna make this automatically happen without me. So I don't even need to worry about this angle, spend my time on board interesting things. And then a year later, you still haven't completely finished your automation as you're trying to perfect it or something. You know, and I think that as a tool, it's an important step in the right direction. But I think people often use it as that silver magic bullet to fix it.

**Derek Downey:**
So I'm going to propose a way to address this podcast, but like I have this kind of the way I think about how I prioritise what task I do is I kind of look at three different components. The first one is frequency, how often is the task run. If you're running it all the time, then you're probably going to want to get more of a return on your investment for automating it. Which ties into the second one, which is complexity, is it really hard to automate? Because if it's really hard to automate, then you're going to be spending a lot more time developing the edge cases and things like that. So you need to kind of read it on those two spectrums. And then the third one is criticality, which is, is this a super critical component of managing a database? If I don't do this task, will it come back to bite me later. And so if you can rate those are kind of on a matrix, so it takes a little bit of forethought and evaluation on your part to say, am I really going to get my bang for buck out of automating this particular task? Is it going to be too much, and then you can look at it and say what, I'm not going to, but I'm gonna do partially automation. Like, there are pieces of this that I can automate with something like Ansible, that can reduce errors. But the rest of it is still something that a human has to do.

**Matt Yonkovit:**  
And I think that that's important to be able to evaluate. And to build that out, I think the other dark seedy underbelly of automation, if you will, is, once you've automated at once doesn't mean it's going to continue to work. And I think that's one of the things that is a fallacy some people get into, I'm just going to automate this, I'm going to just stick it out there. And then I don't have to ever worry about it again. And the fact of the matter is, upgrades happen, as changes happen to the environment, underlying software, the stacks of new security patches, all of that has the potential to cause other issues. And this is especially true when you look at like a CI/CD pipeline, because CI/CD pipeline is really just automation of that release and deploy. And you see that so many major outages happen, because somebody introduces some underlying code, it gets automated and propagated to 10,000 machines, now all of a sudden, you have to roll back 10,000 machines. And that is a problem that I see continually crop up and continually persist. And it doesn't matter how many, like layers of redundancy or availability you have, if you're going to automatically deploy bad code or misconfigurations, across all of your nodes. 

**Derek Downey:**
Absolutely, I touched on this a little bit in my presentation, in the cautions aspect, because I think you're absolutely right, the idea of complacency, like once it's automated, it's good. And I don't have to worry about maintaining it. And then you go to run your quarterly dr script that the whole thing has changed in the last quarter, and then that doesn't work. Right. So I really like the idea is, is like continual testing in production, chaos engineering these concepts, like, it's really hard to do, to get your mind around it in your critical data environment, because it's like, I can't test this in production, because I might bring down an outage, right? Well, you have to because otherwise, you won't know what happens in production when you run it.

**Matt Yonkovit:**  
Well, so this is where it's, it's interesting, because I think the theory outpaces the ability to implement those technologies, right? So are those ideas like, so you talk about chaos engineering, you talk about testing in production? This is great. If you can get away with it so let's bring down a random node today. Yay, let's see, let's make sure that everything still works or what have you. The problem is, most applications aren't designed for that. Right. They're not designed for that level of fault tolerance. And oh, well you know, you mentioned earlier that sometimes fail overs take time, right and and I think that during the automation process, as you start to automate things, certain automations like, it could take 10 minutes for a new node to be built up and created and move things over. That's an unacceptable amount of time for most applications. And so that means that like, unless your application is built, to say, Oh, this resource is out, now I'm gonna go do this or you're using something that will automatically spin up additional nodes or has that elastic capacity to survive that it becomes problematic and a lot of times people end up with a lot of redundancy in the application side and very limited on the database side. They rely on a replica or group replication or something like that.

**Derek Downey:**
Yep. Yep. I think you're absolutely right. Like, if you're, if you're listening to these theories and concepts of how some of the big companies have solved, like chaos engineering, like Netflix, or, or all these different aspects of managing databases, they're solving for really big problems that you're probably not going to. But what comes out of these discussions as Netflix engineers, and Facebook engineers, and all these big companies start sharing their knowledge is new applications spin up with a foundation that's a little bit better than what the old applications have been spun up with. Right? And so overall, over time, you start to get a better foundation for architectures and data layers and stuff like that.

**Matt Yonkovit:**  
Yeah, I mean, you think you continually want to level up, and levelling up those applications is important. It's just that there's so much legacy out there. A lot of times people will hear like, Oh, yeah, we should totally do some chaos engineer, we should totally, you know, run a continuous deployment, continuous test environment, but then they try to apply it to a inherently fragile or legacy pipeline, and it just destroys it.

**Derek Downey:**
Don't start with it in production, until you've tested it somewhere. And I touched on that with the Ansible automation courses, or the presentation, which was, hey, if this is your first venture into automating with Ansible, you're not going to be running it against production, until you vetted it in, in a development environment, a staging environment, and you built some confidence in what you've developed, that it's going to work, you don't want to just push button deploy in production, if you've never done it before,

**Matt Yonkovit:** 
Yeah, I mean, testing is so critical, and all of this and making sure that it does work in the right environment in the right context. And even with testing, you're still gonna run into those issues. And unfortunately, for sure, you have to realise that and that's where it requires you to think about how this is deployed, how this is built. And it's similar, looping all the way back to Spanner, as you build an application with Spanner, or any of these distributed databases that are out there, it does change how you develop your application, how you think about it. It's not always just that lift and shift like, oh, we're, we're just running a single node of everything. And now all of a sudden, we're gonna go to this multi layered database, multi layered application stack. We're gonna add the Kubernetes fairy or whatever, to this and it's just gonna magically like, just scale. It just works. Yeah. There is no magic Kubernetes fairy, at least none that I've met yet. Maybe there is. That would be a cool. He's here to say it, solve all your problems. Whoo, pixie dust. Whoo.

**Derek Downey:**
Then we're all out of a job. And we can go sit my ties on a beach. So,

**Matt Yonkovit:** 
Right, there you go. There you go. It's the automation, or some replacement humans, right. So, so Derek, where do you see things you know, kind of evolving you you were able to attend percona live, you were able to you've been in the ecosystem in the database ecosystem for a while. What do you think's next? What do you think is this, the next thing that's kind of cropping up that you're looking at going like, that looks interesting. So that's where I think the next really interesting discussions or technology is going to come from.

**Derek Downey:**
I mean, the thing that stood out to me from Percona Live this year was the amount of Kubernetes sessions that there were. So you've mentioned it a few times, data on Kubernetes. There's a really good community around it. I think that you've done a podcast with or a talk with Bart, on Data on Kubernetes and how do you solve that problem. The trend to me is like, hey, Kubernetes may be the standard de facto way to manage infrastructure. Should soon and it has been for a little bit for applications, perhaps data is just state is starting to creep up on that. Or it's actually feasible to do that. I think that's if you're talking about in the next two, three years, we're going to get some really interesting stuff out of running databases on Kubernetes. I felt that way for a while, I first started playing with Docker, when, like the 2015-14 timeframe, I was like, Oh, this is really great for dev testing, right? But there's no way this is good enough to run a database in production. But as technology does, you solve the use case, and then that you're going for and then you start tackling the next one. And the next one. And so I think Kubernetes is doing that with databases. If you're not thinking of running something cloud vendors, Database as a Service for your underlying data layer. 

**Matt Yonkovit:** 
I mean, I look at this as almost like the drive to not have to even think about databases or the infrastructure. I mean, from an application perspective, it's the push button desire, that I don't really care what database technology I'm using, as long as I have an interface, and I know it's going to be up and secure. I think it's becoming less and less that developers… But I mean, let's, let's be honest from a development perspective, if you've got the ability to access and store data, retrieve it quickly get what you need, you don't want to worry about the HA, the backups, the the security side of things you just want it handled behind the scenes. And in a lot of those cases, you don't even care about whether it's Mongo or MySQL, or Postgres or Cassandra, as long as you're able to access the data easily and quickly, it becomes less important for you to understand that underlying infrastructure. Now, for those who have to maintain the infrastructure, that's a whole different question. But you know, when we talk about, from a developer perspective, that desire to have like, almost like a, like a 00 database, it is a real thing, I think. And that's where I think from a Kubernetes perspective, everyone wants their own database, and you never know which database it's going to be. And so having some technology to allow you to easily add, remove the right databases makes sense from an infrastructure standpoint, because you just don't know if the same things you need today will be the same things you need tomorrow.

**Derek Downey:**
Yeah, my caution on that whole concept of developers wanting something push button easy to deploy, is that usually when you try to get something generic enough, that can be all needs, complexity creeps in, and you start to get really inefficient, like, operations. My example of this is when I first started off as a PHP developer, all of the developers or all the designers were using an app Dreamweaver, that what you see is what you get, like a website developer type thing. If you looked at the code that was developed by Dreamweaver, it was the most ugly, inefficient use of tables within tables within tables. And so like my first project, there was to say, Hey, here's your design in Dreamweaver. Here's what I did with divs, and CSS and all this stuff. The files are about oh, I don't know, I think I cut it down by 30% of the file size, by the way, that translates into load time for your websites. So all that to say is like you can get complexity, that starts to look inefficient with your infrastructure, and either it's going to go start performing slower. Or you got to get really good infrastructure people to understand how to mitigate that or improve that. That complexity.

**Matt Yonkovit:** 
That whole complexity versus speed has been around forever. I mean, think about overheads. You know, so like largely, or EMS are there to hide the complexity of the database for you. And they generally make some pretty weird decisions around like joins and like what data is retrieved and other things, which has often been the bane of most DBAs existence, because they're looking at these performance problems. But who would write that query? Like, what were you thinking? And either developers, I wasn't the..

**Derek Downey:**
And the developers still go towards the OROMS. Like, they're still a thing. They're still highly popular.

**Matt Yonkovit:** 
Because I think it's that, like, it's that abstraction layer. I really do. Because databases are a pain in the rear and they're not cool. Yeah, let's be honest, databases are really that not cool.

**Derek Downey:**
And so it's probably alarms do a really good job. For the generic use case that like, let's say, 80% use case, just to use some famous numbers. There's 20% of that. You may not be in, so you may not have to think about it until you are and then you're in this mess of infrastructure and how do you solve that? So I think that's how like middle layers, middleware crops up like ProxySQL to kind of bridge between translating what the ORM is doing to something that's more useful for and better for the database. 

**Matt Yonkovit:** 
So that's actually interesting. So I have not, I have not seen anyone do that. So have you seen people actually use ProxySQL or like you know, a proxy server to translate the crappy ORM code into something that actually is performance. Like, I mean, I know, I've seen like, query rewrites, but I have not seen it specific to an ORM.

**Derek Downey:**
It's not so much specific to an ORM, like, I consulted with the proxy, I contacted with them for a period of time, and it was more, every one was different. But you started to get a sense of which ORMs a client was using and saying, Oh, you need to make sure that you handle this case. So it's not ORM specific, you need to do an evaluation or your queries to do the rewriting. But if you've worked with it, across a wide spectrum, you can start to publish, which has not happened, like I agree with you, hat there's no like common use cases of these rewrites. If you're using Ruby on Rails, or these rewrites if you're using Django or whatever. I came at SQL alchemy is what I'm thinking of. But yet, but that's why it exists is because the application is not going to rewrite the queries, whether the application is custom, or the application is an ORM. So something has to translate that. And sometimes it works, and sometimes it doesn't.

**Matt Yonkovit:** 
Yeah. Well, Derek, thanks for sitting down with me today. I appreciate it. And if you haven't checked out Derek's talk at Percona Live, it should be up on YouTube or on our website. Derek also has his own blog, you want to plug your blog and your channels there, Derek?

**Derek Downey:**
Yeah, absolutely. So my blog is Distributed DBA, where I basically publish a weekly blog post, sometimes all the time in video, and then a transcript of that, so that you can learn differently on database topics, but also remote work, because I've worked remotely for my whole career. So I like to plug in every now and then like tips on how to work remotely because we're doing that. So that's my blog https://distributeddba.com/. And yeah, I'm a Google Cloud, you can best finally on Twitter. My handle is Derrick underscore, underscore Downey. And that's where I can most readily be reached.

**Matt Yonkovit:** 
Alright, great. So Derek, thanks for joining us today. We appreciate it. And we look forward to learning all about Spanner with you over the next you know, few months. 

Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.
