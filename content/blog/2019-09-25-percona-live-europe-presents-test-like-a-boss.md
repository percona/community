---
title: 'Percona Live Europe Presents: Test Like a Boss'
date: Wed, 25 Sep 2019 06:31:58 +0000
draft: false
tags: ['author-giuseppe', 'conferences', 'dbdeployer', 'Events', 'MySQL', 'testing', 'Tools']
images:
  - blog/2019/09/dbdeployer.jpg
authors:
  - giuseppe
---

![](blog/2019/09/dbdeployer.jpg)

My first talk is a tutorial _Testing like a boss: Deploy and Test Complex Topologies With a Single Command_, scheduled at [Percona Live Europe in Amsterdam](https://www.percona.com/live-agenda) on September 30th at 13:30. 

My second talk is _Amazing sandboxes with dbdeployer_ scheduled on October 1st at 11:00. It is the same topic as the tutorial, but covers a narrow set of features, all in the \*amazing\* category. 

The tutorial introduces a challenging topic, because when people hear _testing_, they imagine a troop of monkeys fiddling with a keyboard and a mouse, endlessly repeating a boring task. What I want to show is that testing is a creative activity and, with the right tools and mindset, it could be exciting and rewarding. During my work as a quality assurance engineer, I have always seen a boring task as an opportunity to automate. [dbdeployer](https://github.com/datacharmer/dbdeployer), the tool at the heart of my talk, was born from one such challenge. While working as a MySQL consultant, I realized that every customer was using a different version of MySQL. When they had a problem, I couldn't just use the latest and greatest version and recommend they upgrade: almost nobody wanted to even consider that, and I can see the point. Sometimes, upgrading is a huge task that should be planned appropriately, and not done as a troubleshooting measure. If I wanted to assist my customers, I had to install their version, reproduce the problem, and propose a solution. After installing and reinstalling several versions of MySQL manually, and juggling dozens of options to use the right version for the right task, I decided to make a tool for that purpose. That was in 2006, and since then the tool has evolved to handle the newest features of MySQL, was rewritten almost two years ago, and now is been adopted by several categories of database professionals: developers, DBAs, support engineers, and quality assurance engineers. 

Looking at the user base of dbdeployer, it's easy to reconsider the concept of _testing_: it could be exploring the latest MySQL or Percona Server release, or a building a sample Group Replication or Percona XtraDB Cluster, or comparing a given setup across different versions of MySQL. Still unconvinced? Read on!

### What's the catch? What do attendees get from attending?

In addition to opening their eyes to the beauty of testing, this tutorial will show several activities that a normal user would consider difficult to perform, time consuming, and error prone. 


The key message of this presentation is that users should focus on **what** to do, and leave the details of **how** to perform the task to the tools at their disposal. The examples will show that you can deploy complicated scenarios with just a few commands, usually in less than one minute, sometimes in less than ten seconds, and then spend your time with the real task, which is exploring, trying a particular feature, proving a point, and not doing manually and with errors what the tool can do for you quickly and precisely.

Some examples to water your mouth: you can deploy group replication in less than 30 seconds. And what about deploying two groups and running asynchronous replication between them? Even if you have done this before, this is a task that takes you quite a while. dbdeployer can run the whole setup (two clusters in group replication + asynchronous replication on top of it) in less than one minute. How about testing the new [clone plugin?](https://dev.mysql.com/doc/refman/8.0/en/clone-plugin.html) You can do it in a snap using dbdeployer as [demonstrated recently by Simon Mudd](http://blog.wl0.org/2019/09/mysql-8-0-17-cloning-is-now-much-easier/) , which proves the point that having the right tools makes your experiments easier. 

Another example? MySQL upgrade: dbdeployer can run a server upgrade for you faster than you can say "blueberry muffin" or maybe not that fast, but surely faster than reading the manual and following the instructions.

### What else is in store at PerconaLive? What will I do apart from charming the attendees?

Percona Live Amsterdam is chock-full of good talks. I know because I was part of the review committee that has examined hundreds of proposals, and painfully approved only a portion of them. Things that I look forward to:

*   The _InnoDB Cluster tutorial_ on Monday. Although I have seen this talk several times, the cluster has been improved continuously, and it is useful to see it in action. Besides, [Lefred's](https://lefred.be/) style of presentation is so engaging that I enjoy it every time.
*   Jeremy Cole's take on Google Cloud, on Tuesday afternoon. Jeremy has been at the top of the database game for long time, and his views are always stimulating.
*   _Backing up Wikipedia_, with Jaime Crespo and Manuel Arostegui. Seeing how big deployments are dealt with is a sobering experience, which I highly recommend to newcomers and experts alike.
*   _ClickHouse materialized views_, with Robert Hodges of Altinity. You may not be thrilled about the topic, but the speaker is a guarantee. Robert has been working with databases for several decades, and he knows his way around big data and difficult problems to solve. Looking forward to learning something new here.

There are many more talks that I encourage you to peruse in [the agenda](https://www.percona.com/live-agenda). 

As usual, the best part of the conference is networking in the intervals and around the venue before and after the event. This is where the best morsels of knowledge land with serendipity in my plate. See you soon! 

If you haven’t yet [registered](https://www.percona.com/live-registration), then you are invited to use the code **CMESPEAK-GIUSEPPE** for a 20% discount. ![](https://www.percona.com/community-blog/wp-content/uploads/2019/09/giuseppe-maxia-two-talks-1024x536.jpg) _The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._