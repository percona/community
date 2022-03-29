---
title: "Oracle, MySQL, PostgreSQL, and MongoDB DBA's to DBRE's - Percona Podcast 05"
description: "Covering multiple databases (Oracle, MySQL, PostgreSQL, and MongoDB) and multiple clouds is never easy, we talk about why keeping control of your data is so important, and how companies can enable developers to move faster by removing the database basics as a bottleneck."
short_text: "Join Percona’s HOSS (Head of Open Source Strategy) Matt Yonkovit as he sits down with David Murphy to talk about his journey and how he is seeing the DBA position evolve into DBRE’s and SRE’s. David has recently been working on helping a major airline modernize its internal database management systems and infrastructure, bringing more of a DevOps and SRE mentality to the company. He will discuss some of the issues and trends he has seen in his role.  Covering multiple databases (Oracle, MySQL, PostgreSQL, and MongoDB) and multiple clouds is never easy, we talk about why keeping control of your data is so important, and how companies can enable developers to move faster by removing the database basics as a bottleneck."
date: "2021-02-19"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep05-featuring-david-murphy-talking-devops-dbre-sre-mongodb-and-modernizing-it/"
youtube_id: "do3LX8xMOIs"
speakers:
  - david_murphy
  - matt_yonkovit
aliases:
    - "/podcasts/5/"
url: "/podcasts/5-oracle-mysql-postgresql-and-mongodb-dba-to-dbre"
---

## Transcript

**Matt Yonkovit:**  
Hi everybody. **Matt Yonkovit**, The HOSS, Head of Open Source Strategy here at Percona, I welcome you to another Percona Tech Talk, where we're gonna bring you the best in the open-source space and give you the most interesting fun speakers ever. We hope you enjoy the show. So David, how have you been? What have you been up to? I know you've been busy since the last time I saw you, which was actually in person in Percona Live Amsterdam, like, a year in a few months ago. 

**David Murphy:**  
Yeah, so! Obviously, that when I was at Percona, I moved to Europe. So my last year has been kind of interesting because COVID didn't want me to travel. But I'm working towards my citizenship in Ireland anyway. So haven't gone to Percona Live this year. Like, even if you had him, I wasn't gonna be able to do it. So why didn't talk this time? Because that's just like, yeah, all that was gonna play out. But broadly speaking, after I left Percona, I went to Huawei. And I was working with them on their cloud. And so it's Postgres, MySQL, helping them kind of start looking at SRE fundamentals in general DBA Fundamentals. Obviously, through the course of American politics, and the China versus US thing, I decided it was probably better if I didn't work for that specific Chinese company. While I didn't have European citizenship.

**Matt Yonkovit:**  
It totally makes sense.

**David Murphy:**  
And so I ended up kind of forming my own. Oh, I'm under an umbrella contact company that I did. And I work with Aer Lingus a lot like one of my main customers. So what I do with them is I kind of came in as you would expect, they brought me in because they had a lot of problems with Mongo, they were looking at modernizing, and automating, and all of these types of things. And so that was great. And then they kind of came in, I kind of did that I did a whole cybersecurity review with them. And I was like, Okay, this is how we fix Mongo, and how we secure Mongo for you. That's great. But then they turn around, and they're like, Okay, well, how can you make our builds of Oracle faster, because it takes us three weeks to build an environment. And so because of that, I kind of brought started bringing them on an SRE mindset to shift out of their database administrator mindset into sharing more with the dev teams as far as knowledge and accessibility, but also maintaining the right frameworks so that the database experts are so leading the charge on how to do it. They're just enabling those other people to do the thing.

**Matt Yonkovit:**  
Well, and we started talking just recently exchanging some threads when I posted my question of the week, which was, do you still need a DBA anymore? And I said, you really need more of an SRE. You said a DBRE. Sorry. And so hey, let's talk about that. And I'm curious, from your perspective where do you see that line between DBA and DBRE And then DBRE and SRE, right? So database reliability engineer versus site reliability engineer versus DBA? Database administrator?

**David Murphy:**  
Yeah, so a lot of it comes down to where the company is in their DevOps lifecycle model. So some companies that they're still gonna have a central database thing, they get the choice here do are we going to going to have it to where the DBAs just manage the application sitting on the physical server or the hypervisor, whatever you're using, and they're just managing that, but only that app, they don't have root access, etc, etc, very classic, it kind of scenario. And so that's where the DVDs kind of fall in the spectrum of the thread that we talk, when it's more interesting is the DevOps versus SRE versus DBR. And that all comes down to where you want ownership because in some companies are like, Oh, just more like Google model. They're like, Okay, well, I want every developer to also be a DBA, to also be a network admin, and they just trade their specific product stack. Yeah. And then there are other places that are like, No, we don't want to do that well, we want to do is create specialty groups inside of our DevOps SRE model, that are the database experts. And what happens is kind of base things are done in general-purpose, like having immutable servers and stuff like that are done in my main SRE group. But my DBRE group is all about how do I take a lot of those principles and apply them to a stateful system that I can't just blow away and recreate? I need to think about it differently. I need to think about how am I going to do patching of this system rather than destroy and create blue versus green kinds of scenarios? And I think that's where the big split between the DBRE and SRE comes from, is that specialty knowledge and one of the things I did after I left working for Percona is I was also working with ServiceNow. And in their model, they have an SRE team, typical DevOps, the SRE team, but in that, they have something they called SWAT. And SWAT was specifically database expert tech people, Java memory debugging type things. So very much your escalation firefighter group that can come in and explain weird problems that your person really about TerraForm and using important and

**Matt Yonkovit:**  
 There was a real expert, it was like you had a, you had a vertical expert for topics. 

**David Murphy:**  
And so so in traditional like, in your, in your four-chair model support approach that everybody needs familiar with, you would say that your DevOps group or your SRE group, in that case, was your ones and twos, but your threes and fours more in this specialty group. And, and I had done the same thing, working with Aer Lingus, in that I am trying to get the more DevOps group to work with us. And they're doing a lot of the TerraForm stuff, and we're providing guidance and recommendations to them. But my team is building the AMI, for example. And we're building those flows. And I'm setting requirements like, it's great, you're using AWS session manager, and you're logging in with the SSM user on your app peers with immutable servers. But for my databases, I want you to drop them in as their LDAP or ad user, and then they have to pass through privileges to get to the database data access.

**Matt Yonkovit:**  
So are you still getting the escalations on the performance issues and the troubleshooting, are you still, I mean, as your environment grows and you're doing the needle in the haystack searching is that kind of like still that role in the DBRE?

**David Murphy:**  
Yeah, absolutely. The way we have it structured is there's like digital production support, which is buying mostly from our DevOps stuff. And it's a mix of legacy kit and new AWS DevOps kind of design. And what we're doing there is, if there's a call out to the DBA, team, they're calling out to us to support the performance or support. We're having this issue where the database slowed down, or we're getting this alert that the database ran out of disk space, or a tablespace, with full different things like that, that you would typically have. But what we're being tasked with, because, again, I'm only a year into the transition, what I'm doing more and more is automating more and more of that getting ready to ship all my database audit logs into Cloud watch, for example, doing stuff like how do I start putting in agents or cron jobs that will auto grow the database, slash whatever support ticket system, you're using message to you to actually tell DBA Hey, last night, you would have been woken up the DBRE. In this case, you would have been woken up but I went ahead and added an extra 10 gigs of space to the system and added a new data file to the Oracle so that you could sleep please look at this before it gets out of control and does it again.

**Matt Yonkovit:**  
So yeah, so you're doing a lot more of I mean, almost like a very basic type functionality around the automation. That's, looking for those events and trying to autocorrect and fix them.

**David Murphy:**  
Yeah, so we're starting with that. But also, like I mentioned earlier, I took the Oracle to build process is now completely automated, where to use you tell TerraForm set these tags on the system, it'll build the right version of Oracle with the right said, and all this type of stuff. But then if it's this type of scenario will also fire off installing the app and loading data from the staging environment into it, where you have a completely working database ready for an app to connect to it.

**Matt Yonkovit:**  
It's about making the developers more efficient and making the move faster.

**David Murphy:**  
So it's a couple of things, it's, it's making them more efficient, but also making it easier for them to request it environment has something or do something to where you get more into a dev environment should just build it and throw it away when you're done with Project X or test X, instead of the classic approach where I had dev environment one through 10, and you're currently assigned to the one you're currently assigned in and then you all that, assign somebody else on to it, which as and everybody watching this probably knows can be an utter nightmare to manage. And from compatibility are finding weird snowflake, the edge cases of things that weren't cleaned up, becomes unmanageable, well

**Matt Yonkovit:**  
you guys are using a lot of microservices and so that's just going to make it so people can spin those up much quicker but it's the potential to just have like a massive number of databases that are out there and a lot of them are just kind of like forgotten about

**David Murphy:**  
to some degree. What we do a lot with what we're doing is you have these environments that you build those but there's tags in it as well to word text environment and does it create ha does not create HA And then also there's reporting on how much usage was the system getting? Do we think that this dev environment is no longer used should we stop using them. So it's all about being able to reclaim that. Now, remember that as it has been in an airline, and in this transitionary step, we still have a lot of waterfall II type processes in someplace for staying stuff up. But all of what we're building now is enabling people to move to a place that when they want to do product-centric development, they want to do more microservices, they can do so. And as more of that happens, I'll be looking at well, do I create kind of, in Oracle terms, a central CDB that has different DBAs in it? Or do I flip that around and have a cloud or a DBaaS of some sort in place? Now, I have a different viewpoint than I think Percona has on this because I don't believe that you should have stuff in Kubernetes if it's your database, that's the application layer. There's a big fight, I think, right now inside the database community, on those lines, and where were those ships? I was talking to charity about that reasonably.

**Matt Yonkovit:**  
And I think I think everybody has a little bit of a different mindset around like the Kubernetes side so many applications have adopted containerization and Kubernetes. For the microservices. There are a lot of companies that want to use their databases the same way they use the application layer doesn't always work. Sometimes it does. I mean, my philosophy, and I had actually posted a video on this as well, is it depends, right? There's no way I'm going to run a multi-terabyte database in Kubernetes. I'm sorry. It's just that's just not, that's not there. But, hey, if I've got 100, WordPress databases, and like, they're all these little small databases yeah, sure, or even some of the medium size. But I have seen a lot of people really successful in a reasonable size. I'm not gonna say massive, but reasonable size Kubernetes. deployments and,

**David Murphy:**  
Okay yeah, it's not that I'm against using it, it's that you're kind of shoehorning in the database there. And if your database, as we said, is small enough, it makes a lot of sense. And it fits Kubernetes does make things fit much better in your microservices and SRE strikes, in general, it just does. But the flip side is you're still running some risk with databases because Kubernetes would never envision truly stateful systems. Like that, 's wasn't what it was designed to solve.

**Matt Yonkovit:**  
And there's a lot of work on that's been going on. I mean, I know we've talked to a lot of the folks in the data on Kubernetes community, for instance, DoK, I don't know if you're familiar with him. that the folks that Datastax I know are looking at Kubernetes. I know Maria dB, folks are looking at Kubernetes. That's what SkySQL is built on. planet-scale, guys. Right, like, so I think there's a lot of emphasis, I don't know how long it will take to get fully there. But I do see a lot of production workload there so far. It's not everything. Now. It's far from everything. But you can guess that's like any technology, right?

**David Murphy:**  
Yeah. Yeah. That's what I was. That's what I've been debating more recently is, How far along is that going to go? And is it going to be kind of the approach Docker has had in general taken for a while, which was, it's fine in dev, but when you go to critical, platinum, prod systems, you draw a line and says, say this need to be actual instances as opposed to containers? But it could be that in four years, we're talking about how were we ever not on containers

**Matt Yonkovit:**  
And I think that's the thing, right? It's like, there's a lot of work there. It'll still evolve. Is it ready for everything? No. But it can handle a lot of the smaller things and a lot of the medium-sized things

**David Murphy:**  
We will see it in Mongo, much more verbosely than we see it in MySQL or Postgres, I think. Because Mongo HA is built on things that would make it continue to work in a Kubernetes environment.

**Matt Yonkovit:**  
Yep. That's it. Different levels, different databases, different ease of use. So yeah, I mean, it's an interesting topic and interesting debate for sure. Because it is something that as you get the larger systems and the more volume, it's harder to manage. And, yeah, it just makes it so much easier, right.

**David Murphy:**  
I would say that's where a lot of my automation comes in is I have a relatively small team of people, and we're managing one Lot of systems and more systems are being piled into this team being brought into AWS as we're doing more of our digital transformation into the clouds in general with the airlines. But what I am noticing is a lot of people are very surprised once you start down this kind of standards approach and automated builds of TerraForm. And stuff, just how much your team actually gets to focus on making sure your design is right, as opposed to just filling the infrastructure,

**Matt Yonkovit:**  
So it really does flip that where it's more, hey, let's design the architecture. Correct. And let's let the infrastructure kind of handle itself.

**David Murphy:**  
Yeah. Because yeah, I met the point that when we build a new environment, for the website side of the airline, I can get handed to the normal infrastructure team that builds all of the infrastructures, and that builds a database that triggers all the stuff with the database, and then I just get one of my DBRE team to do a quick QC of it. So I spend an hour Up, whereas before we had three weeks assigned to somebody doing that, those two and a half other weeks, I get to spend on improving that, or looking at the next version, or testing patches or all the things that we should have been doing. But teams never had time for it because they were too busy in the firefighting.

**Matt Yonkovit:**  
So a lot of as you do your modernization, it sounds like you guys are kind of standardizing on AWS. Oh,

**David Murphy:**  
I think that's the first day that first cloud of choice, but there is definitely a very strong hybrid cloud view.

**Matt Yonkovit:**  
Okay, so you're looking at the multi-cloud. To get in any reason why? 

**David Murphy:**  
Well, it's just in case we needed to pivot for different things we are in Ireland. And so AWS has a big presence here. So that makes a lot of sense. But also, like, as different times of all we need to look at that we need to make sure that AWS can't come down and say, they don't get any discounts. This is your new rate, tough look with it. At the same time, 

**Matt Yonkovit:**  
it's more of a price protection thing for you.

**David Murphy:**  
 There's a price protection aspect of it. But there's also the other side of it, which is how do we make sure that if AWS has a critical failure, we have a plan on how to get off of that. We could talk about like, recently, there was a platform that got platformed, from AWS. And they were like, Oh, we're already we can just shift, and then they sued because they found out they couldn't shift. 

**Matt Yonkovit:**  
Oh, so they tried to do to the like a lift and shift and didn't work? 

**David Murphy:**  
Well. Yeah, well, yeah. And they always said they could do it until AWS pulled their plug for different things that happened in America recently. And then they couldn't do it. And so they resorted to the legal system because it basically shut down their company. We don't want to be in that position that for, for whatever reason, whether it's AWS, resourcing pricing, or some sort of environmental thing that just takes a data center offline, that we couldn't just shift somewhere else, we want to make sure that we have that flexibility. But from my perspective, it's also it's making sure that you're trying to use generic tools, for example, we could be using a different AWS container, Image Builder, it's stuff like that. But we're still using things like Git, Bitbucket, TerraForm, stuff like that. So that we're staying at that agnostic level,

**Matt Yonkovit:**  
and you're trying to stay at arm's length. So you have the portability.

**David Murphy:**  
If you're trying to adopt it, especially when you're early in your duty level, especially with DBRE and stuff, there gonna be times where you're like, I should use Aurora, or I should use RDS for these different things. And you have to take a measured approach, and not be always arm's distance, but always not tied too closely to a cloud to go, okay. I don't want to invest in trying to rebuild what they've already built for now. So let's just use that thing with a backlog item of how can we do this in a more nonvendor-specific way, because like RDS and Aurora, they saw some good problems. But they do have some other ones like, you have way more control over failovers. If you have EC2 instances. Like if you're using a database as a service from a cloud provider, you kind of just stuck going out the failover is happening. There's nothing I can do as a DBRE. which is a very unsettling thing for me personally, because I don't like the fact that I can't tell people when I expect the database to be back up. Because I'm waiting on AWS, Azure Google scheduler,

**Matt Yonkovit:**  
so it's a trust thing as well, right, like so. So you've got like this trust aspect?

**David Murphy:**  
Yeah, I think there's also there's a trust aspect. But there's also a control aspect to a large degree. Because you lose a lot of control when you hand these things off. And similarly, I have conversations all the time about should we move something to a databases service provider, whether it's Mongo Atlas, whether it's RDS Aurora, different things like that, or Snowflakes, or stuff like that, or should we maintain control? Because how often are we going to be able to update that given app? Are we going to run into a problem when that vendor says hey, we're decommissioning version X, upgrade your app? And we're like, whoa, we don't have that team anymore. Or the third party we paid to build that app no longer exists. How do we update this to a new driver?

**Matt Yonkovit:**  
Like, well, and most of these databases are services though they have features that are only exclusive for that and that really wrecks that portability.

**David Murphy:**  
You as it does, but also just broadly speaking, for example, like if, if I wanted to adopt Postgres quickly, I might use RDS Postgres, but then put a time gate on it to say, okay, by this time, we need to have a non-AWS native approach to the same thing.

**Matt Yonkovit:**  
So it's rapid prototyping. Yeah, we're,

**David Murphy:**  
I think what's important in your DevOps model is you don't black block rapid prototyping. But you keep your mind on how do I keep myself in a position where I can pivot these things to new technology? And versus how tightly do I tie into this one cloud provider, which has benefits don't get me wrong, there are very strong benefits to having tight coupling. It's just a matter of where you want to spend the money. Do I want to spend the money on features and prototyping? Or do I want to spend the money on resiliency and scalability? Because those are different buckets that, unfortunately, too many people try to merge into one.

**Matt Yonkovit:**  
So let me ask you this. Do you need a DBRE or a DBA in that cloud model, if you're running a database as a service?

**David Murphy:**  
 Yes. Think about it this way. I'm, I'm running. I'm running RDS, Oracle, for example. It doesn't matter that I'm running an RDS Oracle, I still need a DBA to help plan out partitions, and tablespaces and data file applications, and stuff like that. Because while it manages the operating system for you, and you can scale storage and stuff like that if you just set a database to auto-extend, you will have fragmentation problems. If you have not planned your data structure out, you will have shared segment problems and neighbor segment problems, all these other things that still exist, you will have wasted memory, you will have missing indexes, or just bad design because somebody put a blog where they should put varchar. And you can't expect your DevOps devs, to know how to fine-tune it to that level, what you expect them to do is come up with a plan. And then you need an expert to kind of cross-check that what we do in our stuff is we have both internal and external developers in the airline. And the DBRE team is part of the inning of their dev face of stuff when they try to go in to sit and test and prod and all of that when they kind of are ready to say Oh, I think we're dev feature complete, we want to merge this into the upstream, the DBRE Team looks over the schema and advises them over different pitfalls they'll have, it doesn't matter that they're on rds, or some other date database as a service platform that reviewed so needs to happen. So that what works in dev doesn't fall apart at scale.

**Matt Yonkovit:**  
Yeah, so So yeah, you do. It sounds like the DBA isn't necessarily doing the classic DBA of install, and the orchestration, they don't need to, it's more on that development cycle. So they need to have that good relationship, that good integration with the developers, the architects, and the DevOps folks.

**David Murphy:**  
Yeah, ideally, in your DBRE team, what you'll want to have is kind of a principal DBRE  for Oracle, Mongo, MySQL, whatever your tests are that you're using. And then another one that is your principal tooling, DBRE, and that way, you get the benefits of those people working closely together, but not as spread out as a full. Every SRE is also a DBA mindset that some people have. But what you do with that team is relatively small, can then teach and provide tooling to the rest of the SRE organization to enable them so that this team is only doing that last mile slash architecture design. And everybody else is utilizing the pattern that's been provided to them.

**Matt Yonkovit:**  
Cool. Well, let me leave you with this question. And I like to ask this question because I'm just curious. So is there anything that you can continue to see plugs, your developers, the DBA staff, or your internal folks are the folks that you work with? is there a consistent issue that if they would just stop doing that your life would be like 10 times easier?

**David Murphy:**  
So there are a couple of things. And I actually have projects on our duty backlog for one of these. Okay, the first one is config management. Okay, the number of people that try to copy Dev, config files, and then script the database because they're using the wrong sequence values or different things that blow everything up, or just simple things like they're copying from A to B and they are like an Oracle. There's a difference between a sIt and a service. Sit is kind of the instance identifier where services are you want to expose a different friendlier view of it.  Well, the difference in the JDBC driver on that is whether you use a colon or slash. And so one of my projects that I've been pushing for is for us to store stuff in secrets, whether that's a TerraForm, a guide to free up your company makes her formidable

**Matt Yonkovit:**  
HashiCorp

**David Murphy:**  
Whether it's HashiCorp, or AWS,  Azure, or Google, everybody has a secret story, getting, it's getting the developers, especially the DevOps teams, to start thinking about using those toolings, to provide their parameters to then get those configs to where they're just-auto built. And all the DBRE team needs to provide to the other teams is this is your config template use that will automatically populate your passwords and dislocation and it'll fetch them and whether it's solid or Ansible, it'll fetch them and it'll pull them, your life will be better, you won't have these problems. But then there are other things where the number of times I see developers think they can just write a SQL statement, and they're like, Oh, well select star from blah, blah, blah, join on blah, blah, blah, join on blah, blah, blah, it's fine. And then I'm like, Are you sure you're going to have the indexes that you're using there? Because if not, your database is going to tank? Also, selecting stars are very dangerous. If you add a column, you just potentially broke your application

**Matt Yonkovit:**  
Indeed, yeah, yeah. I mean, it's, it's they're all small things. It's just small things that matter so much.

**David Murphy:**  
But these things keep happening. And this is what been one of my arguments with, the different leadership teams on why a DBRE Team is needed. Because you needed that knowledge, you needed that ability for somebody to quickly look at something and go, Yeah, you really shouldn't do that. Because you're gonna hurt yourself in six months when you forget why you did it. And you wouldn't expect any general developer to do it, and you see a repeat problem of them doing it over and over. 

**Matt Yonkovit:**  
Right! It's just the continual thing that

**David Murphy:**  
Yeah, cuz you're just you're playing Whack a Mole with different Developer Groups or different developers. And then let's face it, sometimes you run into technical people that like to do it their way and just don't really listen.

**Matt Yonkovit:**  
No technical people are totally willing to listen to everything that DBRE says, right?

**David Murphy:**  
I said, technical people, because I include DBRE, and DBAs, in that, that they're some of the worst offenders of a DBA. Trying to transition to DBRE, he has a really hard time taking the hands off of the black box and letting people peer into that world. They, and that's one of the things that I focused on since I was with, with optic rocket, I've been focusing, as you saw trying to get people to shift more into the trust others they mean, well, kind of mindset.

**Matt Yonkovit:**  
Yep. Yep. Try like, you can have good intentions, right. Assume good attention! Yeah. People are trying to be mean, they're not trying to make your life hard.

**David Murphy:**  
Yeah. And just to help people understand that, the DBAs can shift a DBRE, it's a change in roles. But just because you're getting people access to do these things, doesn't mean that the business doesn't need you to do these other things that you've just never had the time for. They're excited that they get to give you these things that are actually more interesting to you. But you just didn't know it, because you were so used to the existing mindset that you were afraid of that change.

**Matt Yonkovit:**  
Well, David, thanks for chatting with me for a few minutes today. I really appreciate it. I think this was very good to talk about the DBRE journey and a few of the things that you guys got going on over there. Sounds like you got a lot of work and it's exciting. 

**David Murphy:**  
Yeah, definitely. And I'm sure I'll see you at one of the conferences soon.

**Matt Yonkovit:**  
 Hopefully, hopefully, we'll all get our vaccinations and we'll be at conferences in person.

**David Murphy:**  
Yeah, I am hoping for that. I very much am I'm missing FOSDEM I'm, I really don't like that. I have missed two years of it now.

**Matt Yonkovit:**  
It's virtual. It's the virtual FOSDEM. I'll have a beer. It's gonna be like five o'clock in the morning for my session. I'll drink a beer while the sessions going on just just just make it a little more normal.

**David Murphy:**  
Yeah, it's true. But anyway, it's good to have it tell you.

**Matt Yonkovit:**  
Alright, great chat with you as well.

