---
title: " Percona Community MeetUp - Installation and Configuration of PostgreSQL Operator - March, 2nd"
description: "Percona Community highlighted running your databases on Kubernetes with Nickolay Ihalainen. Specifically, how to install and use Postgres in a Kubernetes environment"
images:
  - events/percona-meetup/2022-03-02-postgresql-operator.jpg
date: "2022-03-02"
draft: false
aliases:
    - "/events/percona-meetups/percona-community-meetup-for-postgresql-operator-march-2nd" 
speakers:
  - nickolay_ihalainen
tags: ['Postgres', 'PostgreSQL', 'Operator' ]
---
Learn more about Installation and Configuration of PostgreSQL Operator in this video from our meetup of Wednesday, March, 2nd at 11 am EST. Nickolay Ihalainen show us how to work with PG replication cluster and internal components, access to your database, put data in it and use in your application, dealing with failover, backup, restore. This event is a part of our regular meetup series hosted by the Head of Open Source Strategy at Percona, Matt Yonkovit.

## Video

{{% youtube youtube_id="oDzc-Ej9hUc" %}}{{% /youtube %}}

## Transcript

**Matt Yonkovit:**  
Hello, everyone, welcome to another Percona live stream. I am here today with my special guest Nickolay. Nickolay, how are you today?

**Nickolay Ihalainen:**  
Hi Matt! I'm great, thank you.

**Matt Yonkovit:**  
And today we're going to make Nickolay Ihalainen famous by having him on the live stream here. So welcome to all of those out in the internet land. Hello, Jobin, thank you for giving us a wave there. We hope that everything is working in terms of sound and video. If it isn't, just let us know. And we'll make some adjustments on our side to try and fix it. So today Nickolay is going to join us and talk to us about a topic that is really, really exciting and hot in the IT space, especially in the database space. And that is running your databases on Kubernetes. Specifically, he's gonna show us how to install and use Postgres in a Kubernetes environment. But before we begin with that, I wanted to ask Nickolay, what attracted you to Kubernetes in the first place? Why did this seem like an interesting fit for you?

**Nickolay Ihalainen:**  
Well, I'd like the idea that something could be wrong in organizing its way, right. And if you have a single server, you can have just a few processes that will do some database job, for example. But if you want to run your application database, maybe some mail services, etc. You probably want to have many servers, because it's too costly to find the server that will solve all needs, especially big databases. That's why we need something that should control everything on many servers. And we need something that will assume application as a kind of process but in multi-server. Kubernetes, it's a way that provides this thing maybe not in a comfortable way for everyone, but at least we're able to do our job. Before I think last two years, it was hard to run databases inside Kubernetes because if you have something that can spawn, and after a few seconds, it can die. Well, you probably worry about your data in the database. And in such ephemeral environments. Well, it should be easy to lose your data, right. But if you have good orchestration, for the database for backups, for performance metrics, probably the database also could find its home in Kubernetes. So yeah, we have operators in Percona. We have been operators for the last several years. The operator is a kind of software that manages databases or manages applications inside coordinators. So and for Postgres, there is a Postgres operator, it's quite young, but Well, it's already useful if you want to run Postgres replication, with multiple servers used for high availability, because well, if your server will die, well, at some moment, hardware can die, or you can consider restarting the server, your database is always should be all there. 

**Matt Yonkovit:**  
Absolutely. Now, Nickolay, people are starting to use Kubernetes, for databases more often, and being in the support side, you get a lot of the people who do things maybe they shouldn't do, or maybe that they have problems with, is there something that you're seeing people use Kubernetes in the wrong way, or doing something that's a mistake from the database perspective that you see over and over again?

**Nickolay Ihalainen:**  
I think the most interesting thing, that people think that the same database that's running on similar hardware should run in the same way in Kubernetes. Like, if I have a 10 terabyte database, well, why can I put a 10 terabytes database in Kubernetes. In Kubernetes environments, frequently, it could be a better idea to not run multiple schemas, multiple unrelated databases on the same instance. Instead, you can run multiple containers around many servers, and you will get better. Better in many ways. You have better performance, you have better manageability because while backup for 10 terabytes, it's still a mess because we're limited by memory bandwidth. We're limited by flat storage needs, it's amazingly fast, but it's still limited. So if Backup and Restore require one day, well probably it's not a good idea for such Kubernetes systems because we want to start, we want to spawn another replica in maybe seconds, maybe hours, but not days.

**Matt Yonkovit:**  
Yeah. So that's good advice, right? So the shifting paradigm is, with Kubernetes, you can run lots of little things as opposed to one big monolithic, and you can run them more consistently and get a more efficient way of running things and multiple, so it negates some of the need to kind of combine everything and try and minimize the number of servers if everything's running consistently across the board.

**Nickolay Ihalainen:**  
Yeah, and this is cattle. And that's a problem because DBA is still considering the database as part. In many other companies, the database is required to do some too small job for some persistent data, but not something that would be the only and single thing. 

**Matt Yonkovit:**  
Okay, so let us walk through that. The reason you're here is to show us how to get started with the operator for Postgres, why don't we get started? Nickolay is going to share his screen, he's going to walk us through the setup. And we'll go from there. So let me go ahead and get Nickolay squared away here, we want to make sure he is visible and his screen is visible. Right. So there we go. And here we are.

**Nickolay Ihalainen:**  
Okay, so if we want to start with Kubernetes with any application, including database, we need a cluster, right? So if you have a job, we can ask for nodes. So what are nodes that we have? So in my case, the cube still components are still working. If on your site, it's not working, or if you're not understanding what's going on, please ask your Kubernetes administrator to fix this kubectl also can use some aliases for kubectl. Or the same could be executed this get nodes. Okay, also works in the same way because it's common. How to run our database in Kubernetes. Because we can run many, many different databases on the same server, while on the same cluster. We need a separation logic. So we can have multiple namespaces. Let's create a new one. create namespace pgo. So bye. For the talk, we have a default namespace, let's change the default to our new namespace.

**Matt Yonkovit:**  
And the namespace is a grouping of nodes or nodes of potential containers or objects, correct?

**Nickolay Ihalainen:**  
Yeah, basically Kubernetes is an object database as a DBA. That's using databases for my whole life. I say that while this is definitely a database with some triggers if you're creating something, some resource, it can trigger actual changes like it can allocate this space if you create persistent work. So configuration set-context, I need current context and I want namespace pgo. Oh, now I'm inside the pgo base, and it will be easy to run the course. So it's empty. For all containers running here, there is no container in this namespace. I want to install Percona operator software that will manage here. So it easily could be downloaded from github, it is an open source project. And actually, on top, we need files. For us on deployment examples, that could be found in the deploy directory. So in order to execute the operator, we need an operator. Operator Yaml is the definition of multiple resources, while the return counts the raw roles and well, this is optional, you don't need it for the time. Because you're going to accept the data. Let's apply this file with the simple comma. And what happens here, it creates such resources that were seen. And we can actually check if we have any new containers in our live space. So there's one that tries to download images that is already running. But while the name is quite interesting, it pgo deploys. So well, this does not look like that operator, what this thing is doing, we can check we have a log, it's some crypt. And if you know Ansible, well, you will see that his format of the output is definitely wrong. So it's installing things. It's quite old thing because there are many. That's here, right? We need to provide some security, which should create resources while operators work. Kubernetes is a database that works with specific objects with specific data. But we can create our own data. These are all data called Custom resources. And well for this data we need like table structure. So this custom resource definition or CRD is a template for creating an operator. And the operator will handle what happens if this resource is created. Unlike the disk allocation that we have for persistent volume, all these things will create orders required for our Postgres. Maybe it's okay, our deploy script finished at unready is zero, so it's not running anymore. But we have Postgres separator and Postgres separator as for containers, and all four containers are running right now in registers. So we are ready to continue on how we can continue? We need CR. Custom resource. Well, we've kind of the quality PG cluster. So this is a git version, main or blank version of the operator, of course, your production, you should use a specific release. So our release is 1.1 1.2 will be the next one now. And this Yaml file aims at many, many examples. Or we can specify a place where the operator will find users and passwords for some SSL encryption. We also have the ability to upgrade our database automatically. We can check for new versions. So well need a database for application because well, of course, Postgres will create an autonomous database for us, but it's a good practice to provide a database for the task so we can do our application tasks we can use pgdb. So well and most applications have users we will ask operators to read users, of course, we can take it by If we are changing it here, we also should change the secrets as to where we are storing both users and passwords. And et cetera, et cetera, needs a high available relation. So we will have a memory, and we will have a replica. So for the primary, it will be some specific version of this demonstration we will use Postgres14. So, of course, the database could consume terabytes of RAM or at least gigabytes nowadays, but for a small example, it will be enough to have 100 megabytes, and one gigabyte for storage.

Now, the database is to be used in many different ways after its installation. Of course, we can use a database globally, from any host on the internet, but most probably your application will use the database that will be hidden inside your environment. So for us, it will be enough to create a Cluster IP address. So their IP address or domain name will be used inside this Kubernetes cluster, but not outside and it will be automatically loaded. Yeah, we can all say they will want to read about it, skip it for it's and et cetera, et cetera.

**Matt Yonkovit:**  
So these are all the components right, Nickolay. So all of these are the different components that could be activated if we needed them, whether it's monitoring, I saw a PG bouncer there, there are different components that you can turn on and off as needed. And they'll be set up for you, saving you from having to install these and set these up yourself.

**Nickolay Ihalainen:**  
Yeah, you can even forget about existence, for example, pg_badger for your lock parser you can get how to manage it, etc. But you can install it, enable it once, and it will be available for you.

**Matt Yonkovit:**  
So there's a couple of questions. So the first one is from David Gonzalez, who asked specifically, I missed where the Kubernetes node is running, is it a minikube?

**Nickolay Ihalainen:**  
Okay, hopefully, you started a bit late. So let's check kubectl nodes. And you can see here, it's Google Kubernetes environment. So it's running on Google Cloud. But you can run it of course in about other Kubernetes clusters, including minikube, but for minikube, there is a fee. In order to do this, you need front servers, an affinity. Yeah, you need affinity. Or if you will run the replica on the same server as your main or as your main Postgres. To cause that is of a crash, you will lose both your replica and primary. So you want to run it inside minikube by default? Well, of course, you can try to modify it, but it runs just a single worker, not in kilometers. Now, you could disable affinity checks, allowing operators to run a replica. 

**Matt Yonkovit:**  
So the answer to there is we are running in GKE. And there is some work to get done in minikube. There's one other question here specific to the live stream. And then there's one that's more specific to Postgres. We'll address the general Postgres one in a bit. But the question from Jee "hey, what's the use case of a namespace? Why do we need to use a namespace?"

**Nickolay Ihalainen:**  
There are multiple benefits to using namespace. The first is simply that you can have different permissions like you can have permissions to see things but not delete or modify for database namespace for this specific user, but this user will be able to deploy the application. So well, that's a great idea because the user will not be able to destroy your data. Another thing is that You need some names. And if you have production and some pre-production environments, you can keep the namespace separated. And a weird thing is that someone will destroy everything, just because well, he forgot which environment he was using. But if he's specifying kubectl, tell, yes. pgo for if you're only specifying he will. But if you are not specifying like, if you're using full, you probably will not see this. Also, well, particularly, it's a kind of idea that allows multiple people to use the same cluster. Or it's at low multiple environments to be executed on the same server like you can have a development server. And each developer will have his own application and database copy. And they can share the same cluster, there is no need to create a separate cluster for each developer, especially for them.

**Matt Yonkovit:**  
So yeah, Charlie also brought up a good point that object names in the case are unique. But you can have multiple clusters or objects with the same name, but with different namespaces. So if you needed to name them the same.

**Nickolay Ihalainen:**  
yeah, you may need to have an A, like a new cluster. Well, every developer has an all-new cluster. So how you can install two applications that have a cluster name.

**Matt Yonkovit:**  
And so we were looking specifically at the different components that could be installed with the operator. And that fits into what Ninad is saying, He's asking, Is it possible to deploy Patrone using this operator?

**Nickolay Ihalainen:**  
Actually, if you want Postgres with manage its replication, you definitely need some good solutions. And Patroni is the best one, I think. Yeah. And actually, Patroni manages this cluster, and it's already installed.

**Matt Yonkovit:**  
So by default Patroni is installed. Yeah,

**Nickolay Ihalainen:**  
it's a key component of our operator of our Postgres cluster manager, right. For example, we can describe our operator Postgres. So, describe contains, of course, a description for the cursor in this format, so and here, I think. Here, yeah. Okay, Patroni didn't tell where the three are okay, let's ignore the fact now part three is a key component here. And this replica were managed by Patroni.

**Matt Yonkovit:**  
Yeah, and all the operators really require a cluster or a replicated setup to work properly because of the nature of how Kubernetes will remove and add clusters. They're designed to be stateless, right. So containers are supposed to be able to kind of move around so you need some sort of clustering software to ensure consistency.

**Nickolay Ihalainen:**  
Okay, let me explain this because this is actually not a requirement. If you have a Kubernetes cluster running it's like running a container. So, if you stop the container you will not lose your data. So, where the data is stored, we have persistent volume claims. So persistent volume claims are linked with volumes. So here there are some volumes, one gigabyte as I have mentioned before, so the data will be here, even if we delete the cluster. So the problem is if we have a node, if a node goes down, if you are going to put it on maintenance, the port the containers will be cute. So with our usual servers, while it's not happening frequently with our Kubernetes cluster, it also could be infrequent activity. Well, if something will die, we can recreate the board again, and the database will work. But increasingly, it's a small world, all this thing is automated. And if we have a clustering solution, we can be online, even if Kubernetes nodes are going down. So that's why we need clusters. That's why we need replication but not because, well, it's impossible to run Postgres without any replication cluster. Yeah, fair enough. Fair enough. 

**Matt Yonkovit:**  
So you ran this command to set up the cluster, the cluster is up and running. What about the other operations? You mentioned we got Patrone here. What about backups? What about if a failover has to happen automatically?

**Nickolay Ihalainen:**  
Yeah, I think we should start from simple things like, Okay, we started something, can we actually use it? Okay, because, okay, you saw PG user and PGDB. But how can I connect. So here, we can run and get secret. And see that I haven't been defined that all I need is a cluster of one users, right? But this object is created automatically. get secrets. So it's not only about the user, there are several other users like PG bouncer, PG user, Postgres, etc. So, we can log into the database using specific PG user details. So, how can we do it? we can create more applications like clients so I can base our application on the same image but you can create with Docker file your own image. So, this thing will spawn a container with bash commands running in a short loop, it will echo hello and sleep for every 10 seconds. So let's apply it!

So after that, the application itself can do things but in order to simplify, I think I will go inside this container. So I can try to connect to something, but wait, what is the temporal name, how I can use it? Okay. three is a resource called service or in short, etc, of course through work. So we have multiple versions. One is our primary Cluster One. Also, we have some backup PG bouncers as a connection pool. And the replica will represent all a secondary in Round Robin. So let's try to connect. It asks for passwords. And if you remember the passwords here, like okay, there is a password.

**Matt Yonkovit:**  
Nickolay, we had a question about that password. Is it possible to define the password upfront?

**Nickolay Ihalainen:**  
Yeah, one second. I will explain it in more detail. So while it's not working, right, I can paste the password. So it's not working. What happened here? So passwords are incorrect. Actually, secrets in Kubernetes usually contain base 64 passwords encoded to have basic 64. So we can use the echo command and run by 64 decodes and well, we will have our password. And it's, so let's copy this time the correct password. So we can go again, here. Okay, we're in the right place. So it says that all database users, of course, because our database is called pgdb. And now we are inside Postgres and we can run something. Well, let's create a table. And for example, c varchar. So we have something and we have can insert it

Hello. So definitely give it away. What else we can do is select the replica. And it works and we should be able to see our new table. Yes, there is.

**Matt Yonkovit:**  
We've got the replica set up. Now we've got everything configured, we've shown that we can connect up. There were a couple of other questions specific to the setup that I wanted to kind of get back to before we lose them. One of the questions came up, is there a minimum number of resources you need to have in order to use the operators? Like CPU memory?

**Nickolay Ihalainen:**  
Yeah, yeah. Well, it's a small program written in Go. I mean for the iterator itself to be cared for. If we check other stuff, we can see that the raw sum of four containers in it, we can check current user uses. And port or the operator itself, see pods? Yeah. Oh, currently, it uses a small amount of CPU. It's 212 divided by 1,000th and about 50 megabytes of RAM. But this is of course, not the database. But the database. The memory and CPU usage depends on your load pattern on the

**Matt Yonkovit:**  
database and the minimums would be the same as they would be for a normal Postgres.

**Nickolay Ihalainen:**  
Yeah, almost the same. Of course, there are some processes additional ones, but they're miserable compared to

**Matt Yonkovit:**  
Yes. We also had one specifically on authentication can different types of authentication methods like scram SHA, are they supported in the operator?

**Nickolay Ihalainen:**  
Well, by default it uses this method. Let's actually go inside postgrads as well as we have with clients we can go to cluster one and some random numbers. So stop it we go to the Postgres directory properly, it's mounted somewhere. so if you call pgdata. We are in the Postgres directory, the reads clutter one. This file is managed by Patroni, or by the operator itself. As you can see, it uses md5. So I'm not sure if you should change it. Well, probably not. But definitely, if it's not possible to modify it with our operator, it should be a good feature request. You can go open GitHub, and see what's there if you want. Okay, yeah.

**Matt Yonkovit:**  
And so there was a question: is cloud support available for the Postgres operator? If you're talking about support for running on, like either the Google or the Amazon Kubernetes services? The answer is yes.

**Nickolay Ihalainen:**  
Yeah. Right now it's running in the cloud. And of course, you can run it in exactly the same way in your on-premise version.

**Matt Yonkovit:**  
Yeah. Yeah. So it is portable that way and can go back and forth. Okay, continue on Nickolay, thank you for answering the questions as we've gone through this, this has been helping people interact and asking questions as we go through that those are good keep on bringing up the questions related to the, to the operators, or to Kubernetes has popped into your mind and we'll answer them as we get a chance.

**Nickolay Ihalainen:**  
Okay, so, able to connect and we have the secret in base 64 formats as we can see if we will provide a more format for the ticker. But we can actually if you want your own password, instead of randomly generated you can create the secrets first and after the last one or you can modify this secret and apply appropriate things to your data. So if you want a big how to ... anyway, so can convert it to a readable format

**Matt Yonkovit:**  
for those who are watching while Nickolay is getting that squared away and ready, curious if folks out there are already running some of their databases in a Kubernetes environment. You just want to answer in the comments as Nickolay gets some stuff ready here.

**Nickolay Ihalainen:**  
So we can think of the idea that sorting Kubernetes in a different way to sample the reason for the template method. And you can use some ports like Rangers for EA and values. And you can be surfing so and even called 64 Without this funky base 64 D So and couldn't net us can beat show passwords without base 64 encoding for you. Like wow, okay, there is a password for our pg user. So, yeah. Why this could be useful. Normally, it's not useful for your applications. But if you're investigating what you have in your cluster will be definitely useful. Because for applications, it's easier to set up passwords as a secret inside your containers. But of course, if you're running your applications outside of the Kubernetes cluster, you should be called such passwords and change your application configuration

**Matt Yonkovit:**  
Okay, so Nickolay, we got a couple of questions specifically on backups. Yeah. What about normal operations like backups? How are they handled? How are they scheduled? Where are they stored? And how do we ensure that you can get to the backups if the cluster goes away?

**Nickolay Ihalainen:**  
So for backup, we should have some of the course Docker images to handle it. And current implementation uses a PG backrest. It's a well-known method to create backups, and even for this, it can use local volumes inside your Kubernetes cluster. Or it can also use volume outside.

**Matt Yonkovit:**  
When you say outside ...

**Nickolay Ihalainen:**  
Yeah, exactly in some object stores, because backups are really huge and stored as SSDs. While it's costly to store your backups on SSDs, instead of storing it in certain, like Amazon glacier. So in order to do a backup, which should have things we should specify where to create a task, these tasks should create a backup for a specific purpose cluster. Well, could be incremental, it could be a full backup. So and we can store it, so let's try to run it. 

**Matt Yonkovit:**  
Nickolay with that backup script, or the backup yaml when backups are being deployed, is it automatically scheduled to run when the operator creates the database? Or do people have to schedule it? Or figure out how to set that up after the fact?

**Nickolay Ihalainen:**  
Well, pgbackrest has multiple ways to do backups. It allows us to do point-in-time recovery. And point in time recovery is when a writer fetlocks directly from Postgres. So that's why the backups are automatically configured. And if you remember, we had this pgbackrests Cluster One pods. So this container is used to store and always write backups. Yeah. See, and we also have this well, persistent disks.

**Matt Yonkovit:**  
there's a pod that's running the backups, and then there's a pod, or there's disks, persistent disk for those backups. If you're running local, if it's on s3, then obviously it's going to go out to the cloud or wherever you're storing it. And that's automatically when you start it up. It'll start running on the default settings, but you can change those default settings if you need to. That's what I'm here for.

**Nickolay Ihalainen:**  
Yes, as you can run your full backups to be able to restore things faster.

**Matt Yonkovit:**  
So from a backup perspective, is that going to run off of one of the replicas or is that going to run on your primary?

**Nickolay Ihalainen:**  
Well, let's go and check what's going on because we have executed a backup and it's created a container and this container is already finished. But the thing that you should love Kubernetes for is the ability to see logs for already finished tasks. As you can see, it runs PG backrest and there are crunchy data operators because the Percona operator was started as a fork of crunchy data operator. So it executes pgbackrest. So we can get a list of interruptions with my address, and this is not for you. It's actually related to our main Postgres so it is executed against the primary server.

**Matt Yonkovit:**  
Okay, is there a way to change that to the replica? Oftentimes you don't want to take your backups directly against the primary.

**Nickolay Ihalainen:**  
Well, I'm not sure how it's implemented currently. But definitely, this could change in the future as well. Yeah, it does not only depend on our operator, it also depends on how PG backrest works. Yeah, because in Percona, we are using open source components, we like open source. And even for backups, it's not some custom solution. It's a properly configured pgbackrest.

**Matt Yonkovit:**  
Okay. And I think Did anybody else have any questions specifically on backups? I think we covered all of them that were asked.

**Nickolay Ihalainen:**  
For restoration, we need to wait for a cluster or lead things. Oh, I don't want to do it right now. But we saw what you can do, you can restore one specific person, and you can restore it. So so it's a resource from cluster one. Storage type six means that we made the backup on disk, not in a cloud. And we can use point-in-time recovery. And the backup will not have two forwards after this point.

**Matt Yonkovit:**  
So Charlie wants to know about splitting load or H A proxy?

**Nickolay Ihalainen:**  
Yeah. For the load. First of all, in Postgres worlds, Postgres uses multiple processes because while it's a safe mode, it allows specific backend without problems. The whole database continues to work, but it's not a good solution for applications that connect and disconnect frequently. That's why we need some connection pool. And here for the operator port if we check get both again. You can fit this in there for several pgbouncer containers, and also for secrets. There is a bouncer user.pg bouncer is somehow integrated here. So we can go to our, so we know,  we can go to our clients and execute on select columns. So we can connect to this client. So instead of connecting to a replica, we can go to pgcluster. So Cluster One. So now we're connecting with PG bouncer. And from the application side, it's not making significant changes. We still can select from t right. What's our problem? Yeah, it's worse. So what is different is we can get the IP address for the server, it will show that it's a primary. So even if we are connecting several times this IP address will not change. So as you can remember from our backup investigation, it's our primer. So did you, bouncers, even if we have three of them, they're connected to the same primary. So why do we need such a strange setup? Because well, our k three tells us to do the same job right? This looks stupid, Kubernetes is all about running things in a cluster or running things highly available. So even if any of this pgbouncer thing will be dead, their service name get the right service name or one pgbouncer that the thing that I've used to connect with Pisco, it's will erode to alive PG bouncer port, and this allows PG bouncer will be able to connect to our primary. So yeah, this was in this way about splitting the loads while if we have multiple replicas, we can run some select queries on it as well.

okay, how it works. It's not using a PG bouncer. But we can specify a replica here, of course, it is asking for ...

Okay, of course, okay, let me come back. So pguser. so we are connected to replica, and we can repeat the query IP addresses changes. So it will repeat this query. It will always provide the same IP address. But if we connect several times you'll see it's a different IP address. Yeah. Oh, what this mean? If we return back, there are services where cluster a key type and class are a piece; it means that we can access the specified IP address. But instead, our requests instead of going to this IP address will go to specific ports of a different server and how it is described. There are things called endpoints. So each device is linked to a specific endpoint. For example, here pgbouncer is linked with this and pg replica with that.

**Matt Yonkovit:**  
Yeah. So Nickolay, we had one other question outside of pgbouncer here. It's about replication and how to replicate two nodes outside of Kubernetes.

**Nickolay Ihalainen:**  
So in order to replicate outside, we should export our IP address right, because if we get service here, you can see that there is no public IP address, there is no external IP address. But what we can do, we can go to the not here but I think here the reason example let's open read-only. So there is an example of how to do things, how to export your service instantly and why it's worth it. I load the button. And the meaning of this load balancer depends on your classical way. For public clouds, this will automatically allocate some public IP address or IP address from the network you have specified for your VPC if you will talk in Amazon terms. So you can specify a log bouncer and you will get an IP address that will be addressable over the internet or over your internal network but not on the inside. So you will be able to use it as a connection point for your streaming application.

**Matt Yonkovit:**  
Okay, so I don't see any other questions, there was one earlier that was specific to not the operator but for Postgres. And we can probably just see if we can quickly address that. And it was someone running an RDS. two instances in the same VPC, same region. They're setting, they're using logical replication. And one of the databases is 1.2 terabytes or the databases 1.2 terabytes, but the replication is going very slow, like one gig for five hours. That seems like it's a configuration issue if the replication stream is that slow. Nickolay, any thoughts on that?

**Nickolay Ihalainen:**  
Well, if it's the same location, the network should be fast, right? Yeah. So it could be something that prevents Postgres from processing at a reasonable speed. So while it's hard to say what's going on right now, just with those symptoms, definitely, you can try physical replication because it will need less decode power. And you can also check what's going on with your application because it's how you can run some short simple queries. And if those carriers modify billions of rows, well, this could create such delays easily. So instead of using such big transactions, you can consider changing your application to, for example, delete just 10,000 rows at once to reduce delay for the replication process.

**Matt Yonkovit:**  
So the short answer is there needs to be some investigation to figure that one out. That's not easy. Yeah, an easy one to just answer, definitely. So Nickolay, thank you for coming out and showing us you know how the operator works, giving us some insight walking us through some of the common commands. And definitely thank you for answering some of the questions here. If you like this, out there who are watching this, either live or in the future, go ahead and subscribe, hit the like button, let us know if there are topics you want us to cover. We would love to hear from you. We want to do things that are meaningful to the community. And so if there's another topic if you want to see this for MySQL, or for MongoDB. feel free to bring that up. In fact, in another week, we're gonna have Sergey Pronin going to be walking us through the MongoDB operator. So we're gonna have a similar discussion around that as well. so thank you all for coming. We appreciate your time here. And we'll see you next time.

**Nickolay Ihalainen:**  
Yeah, don't forget that Postgres and Kubernetes are just starting from such topics. And we are ready to provide significantly more interesting stuff to do, right?

**Matt Yonkovit:**  
Yes, absolutely.

**Nickolay Ihalainen:**  
All right. All right.
