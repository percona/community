---
title: "ZettaDB and Kunlun Database Takes the Best of PostgreSQL and MySQL - Percona Podcast 26"
description: "David sits down with Matt Yonkovit (The HOSS) to talk about the Kunlun project, distribution, implementation, scalability, and more."
short_text: "David Zhao (ZettaDB) has been working on database kernels for years, developing code and enhancements for Berkeley DB, MySQL, and TDSQL. David is back with a new Hybrid database called Kunlun which aims to take the best of what's in the PostgreSQL and MySQL space both and output a better database. David sits down with Matt Yonkovit (The HOSS) to talk about the Kunlun project, distribution, implementation, scalability, and more. If you are interested in learning more David also delivered a talk at Percona Live 2021 entitled “Performance Comparison of MySQL and PostgreSQL based on Kernel Level Analysis” which is also available now."
date: "2021-06-30"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep26-david-zhao-database-systems-expert-zettadb/"
youtube_id: "fIK2ZnSDa2s"
speakers:
  - david_zhao
  - matt_yonkovit
aliases:
    - "/podcasts/26/"
url: "/podcasts/26-zettadb-kunlun-database-the-best-of-postgresql-and-mysql"
---

## Transcript

**Matt Yonkovit:**
Hi, everybody! Matt Yonkovit, Head of Open Source Strategy at Percona, or the HOSS for short. I'm here with another podcast “The HOSS Talks FOSS” and today I'm here with David Zhao from ZettaDB. Hello, David. 

**David Zhao:**
Hi, Matt. Hi, everyone. Glad to meet you. 

**Matt Yonkovit:**
I am very glad to have you here. Now, David, can you tell us a little bit about your background? You actually worked for Oracle and for Tencent?

**David Zhao:**
Yeah, I worked in Oracle for six years or so and in Tencent for another three years. So in Oracle, I worked on Berkeley DB and MySQL database systems. And in Tencent, I wrote down TD SQL, it is a distributed DBMS. That's basically what I did. In my entire career, I worked on database systems.

**Matt Yonkovit:**
The internals, though, not just the databases, you were into the very low levels.

**David Zhao:**
Yes. Starting from the Berkeley DB, it is an embeddable database engine, storage engine, and it supports all the transactional semantics. And as always, the key value is simple query interface. In my MySQL I worked in an optimizer team, working on several functionalities of the optimizer of MySQL. 

**Matt Yonkovit:** 
And you like performance? Because in your talk, you compared quite a bit of different performance benchmarks. So, I can see the optimizer team was a good fit for you early on in your career. 

**David Zhao:**
Yeah. It's a great team, and the engineers in MySQL optimizer team.

**Matt Yonkovit:** 
Yes. And everybody always wants faster, they always do. So you decided to leave Tencent and start at ZettaDB. 

**David Zhao:**
Yeah. 

**Matt Yonkovit:** 
And so now you have a project called Kunlun which you talked about at Percona Live. Now, one of the cool things about the talk is that you do compare Postgres and MySQL at a kernel level, so you walk through the different features. And it sounds like you really approach your project by trying to take the best that was in Postgres, and the best that was in MySQL and combine the two.

**David Zhao:**
Yeah, exactly. Because I also worked on Postgres for several years in Teradata. And I know how it works, and those strengths and weaknesses. So basically, in Kunlun projects, what I want to do is to combine the best of both Postgres and MySQL. And I believe the essence is that the best part of Postgres is the query processing, for MySQL is the inner DB storage engine and it's binlog application. As always, it has also a very good optimizer. Yes, for sure. But any, I believe, if I combine the two, I can build something new. That's in the kernel and distributed DBMS. Now, we are very close to making it a commercial database system, it has all the basic functionality including the transaction processing, the query processing, common DDL and DML statements are all supported now. And it shows very good performance, and also other aspects, for example, stability, crash safety, and so on.

**Matt Yonkovit:** 
Okay, if you built this as a sharded system, correct. So the data is “share nothing”, as opposed to “share everything”.

**David Zhao:**
Exactly. The reason is that in the future, especially in bigger countries, like China and the USA,  there are a lot of internet users. There are many companies which have a huge amount of data. That's hundreds of terabytes of data. For example, I worked in Tencent before that, the DBMS we built was called TD SQL, that is really the distributed DBMS, which uses MySQL as the storage nodes. It supports a lot of internet businesses and games of Tencent. And in each of the games there is a lot of data. So I see that there will be many other companies which will have more data. Similar amount of data is Tencent or Alibaba, because these are very leading world companies, Internet companies of the world, but there will be more companies, which will also meet all these challenges. That's why I left Tencent and do this project. I believe it will help a lot of smaller companies, which don't have the resources to build a special database kernel team to get you to do all these kernel developments. 

**Matt Yonkovit:** 
Yes, in a lot of the work that you're doing, it is similar to other problems that other database or other companies have had. YouTube, for instance, created Vitess to do their specific sharding solution. I know that at the Percona Live, there was also a talk from the people at Uber, who built their own database engine on MySQL. You've taken the unique approach of combining the best of both worlds with Postgres and MySQL, whereas those two are very focused solely on MySQL. So this is a very common problem. And it's a very unique solution that you've taken to it. Now, I'm curious, one of the challenges with any of these systems is always like I mentioned the sharding. When you set up your tables and your structures, are you picking the shard key? Or is the shard key automatic? Tell us a little bit about the sharding implementation?

**David Zhao:**
Okay, the sharding part, okay. In Kunlun, we need the DBA to choose the sharding key for each table. So that means a little bit of extra work for DBAs. But for a good DBA he needs to know his business, what kind of tables is he building so, so that makes sense for him to know which table should be sharded or not. For example, a huge table like Orders table, it should be sharded because there can be millions or opinions of orders. For another table, for example, a department table, it is small, so it should not be sharded at all, it should be a standalone table. So for different types of table, it needs to specify how the table should be sharded. For example, it should be hashed by some columns that he choose or another table maybe should be sharded by range, for example, by dates. For a number of other tables there may be a shortage every week or even day for big websites like Taobao. So that it makes sense for DBA to know all these details. So our approach, our philosophy is that DBA should know this and should all get involved in all this work. It should not be something that's just like a simple camera… I don’t know how to say that in English anyway. So, with all this extra work DBA does makes our system more able to do more optimization. For example, we know each table is sharded and we can do more optimization for cost performance optimization. So it's a balance, we choose the professional end and it's not a lot of work. It's only a little bit of extra work. And we can make a DBA life easier by providing a GI interface. So in the end, they don't actually have much work to do.

**Matt Yonkovit:** 
Okay, great. And I mean with Kunlun, you have a system that is distributed. And performance on big data is always important. But sometimes systems struggle with smaller queries or maybe aggregates or maybe there's certain query patterns that don't work well with the particular implementations. Are there some implementations or some query patterns that work really, really well, in Kunlun right now and other ones that still need some work?

**David Zhao:**
I think queries generally work very well in Kunlun. Things like aggregates are what we are working on now. The guideline is to push down extra work, as much work as we can to storage and storage shards. So that we can do parallel and distributed work. They can work together at the same time. So another way we can minimize the amount of data transferred. So that's the philosophy. So maybe for a distributed system, the network latency is something that you just come to totally avoid. But the good thing is that the computer nodes are always supposed to stay in the same, at least, data center with the storage shards. Usually, in real deployments, seldom separate them across multiple data centers. They can separate some part of each storage shard, some nodes (several, one or two nodes), to another data center for crash safety, for high availability. But they always put computing notes together with the majority of storage shards.

**Matt Yonkovit:** 


Yeah, it's always hard to have that geo distributed cluster, because you don't know the network connectivity and the volatility between two separate geo located data centers. I know like going from, let's say, China to a data center in Europe might have latency issues that introduce all kinds of complexities and issues that you just might not normally have to deal with. So it is a complex problem. Definitely. And now Kunlun is 100% open source, right? So it's available on GitHub.

**David Zhao:**
It's open source in GitHub. And we actually also have an Enterprise Edition, the enterprise has exactly the same set of functionality as the open source edition. The only difference is the performance. Actually, Enterprise Edition has some particular performance enhancements.

**Matt Yonkovit:** 
Okay. And so you're following the model “Hey, get started with the free version. And when you need more performance, call us up. And then we'll talk about buying the license or the support for the enterprise version”.

**David Zhao:** 
Yes. And also the open source edition has all the crash safety fixes to MySQL. I mean,
I wrote an article, maybe you already know, MySQL has quite some crash safety issues regarding the XA transactions. Those parts are all open source. So the open source edition is actually crash safe.

**Matt Yonkovit:** 
Well, that's good. I actually know that way, way, way... back when, because I worked for MySQL, AB, right? Back then XA transactions were added on as almost an afterthought. So there wasn't a lot of work. And we always would tell people from a consulting perspective “We don't know if you really want to use those because they haven't been as tested and ready for production as people might like”. So back then we used to tell people that so it's great that you fixed some of those issues, because I knew that some of them existed since 2007. Probably.

**David Zhao:** 
Well, actually, I think maybe the TD SQL of Tencent, the project I was working on, my responsibility was to make TD SQL a real distributed database in Tencent. The TD SQL  is probably the first distributed DBMS that uses MySQL as storage nodes, that totally fix all the MySQL XA issues. That's why I am proud that I make a lot of contribution to the MySQL team, we contributed all the bug fixes, reported all the bugs we found regarding the XA transaction to the MySQL team. And some of them have been fixed, some not yet. So that's why we still need to fix several XA issues, XA transaction crash safety issues, including storage. 

**Matt Yonkovit:**  
So what I could do here is while we're on here, I'll call out Lenz Grimmer who is in charge of our server engineering: “Lenz, you should talk to David and get those patches and put them in Percona Server”.

**David Zhao:**
Yeah, sure. I am glad to contribute the patches to Percona and MySQL teams.

**Matt Yonkovit:** 
It's great. And that's the power of open source. Right? People have different use cases, they find issues, they can fix them. And that's really a great thing.Well, David, thank you for coming. Thank you for talking to Percona Live. If you haven't seen David's talk at Percona Live, it is available now. Either on our website or through YouTube. It is 100% free. I would definitely encourage you if you want to know the differences between Postgres and MySQL at a kernel level. To check it out. It is a very interesting talk from that perspective. And good luck with the project. And hopefully this helps get people interested in. We’ll try it out and give you feedback. 

**David Zhao:**
Yes, thank you very much. 

**Matt Yonkovit:** 
Wow, what a great episode that was. We really appreciate you coming and checking it out. We hope that you love open source as much as we do. If you liked this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open source with us.

