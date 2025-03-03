---
title: 'Matt Yonkovit: It''s a crazy world, and these trends are disrupting and breaking your database infrastructure'
date: Fri, 12 Jun 2020 15:30:28 +0000
draft: false
tags: ['Cloud', 'DBA Tools', 'DBaaS', 'Kubernetes', 'Kubernetes', 'MongoDB', 'MongoDB', 'MySQL', 'MySQL', 'mysql-and-variants', 'Open Source Databases', 'Percona Monitoring and Management', 'PMM', 'Postgres', 'PostgreSQL', 'Tools']
authors: 
  - cate_lawrence
images:
  - blog/2020/06/PLO-Card-Matt.jpg
slug: matt-yonkovit-its-a-crazy-world-and-these-trends-are-disrupting-and-breaking-your-database-infrastructure
---

Matt Yonkovit, Chief Experience Officer at Percona, presented a session at this year's Percona Live ONLINE, sharing initial insights from the [Open Source Data Management Survey 2020.](https://www.percona.com/open-source-data-management-software-survey) The survey provides a critical insight first-hand into how enterprises of all sizes are using, developing, and troubleshooting open source database software. The full data will be released later this year with a detailed analysis.

He who controls the application controls the stack
--------------------------------------------------

Matt started with discussing the challenge that developers face: "Those building it are not the ones managing it. And those who are building it are the ones deciding what to put in it." 

Last year a survey asked Who gets to choose the database technology at companies? Most people choosing database technology are outside the database or the infrastructure side. More architects (32%) and developers (26%) are choosing the tech than management (17%) or DBAs (23%). 

However, the challenge is that the DBAs are inheriting technology from the development stack, and all of a sudden they have to support it. Matt said he likes to call this, "The technology inheritance problem: So now you've got a team of people who are not necessarily skilled at managing those technologies all of a sudden being responsible for new technologies."

The multiverse of technology
----------------------------

Enter the multiverse of technology: multi-database, multi-cloud, multi-location, multi-skilled. Matt explained this as follows: 

 "Instead of saying we're going to run on AWS and we're going to consolidate on a single database or a set of databases, you're running on multiple databases, you're running in multiple locations, you're running multi skilled people, because you're no longer, you know, an expert Oracle DBA on its own. You're a DBA of everything. And it's leading to these multi-database environments.”

The database footprint is growing
---------------------------------

In last year's survey, more than 92% of companies were running more than one database, and 89% have more than one open source database in place. This year the number of companies that reported having between 100 and 1000 database instances in place grew by 40%. Those reporting over 1000 database instances grew by more than 50%. Matt noted: 

 "Now we've got environments that have thousands of databases that have to be managed and supported, and that means that the care and feeding of each database is very difficult." 

This is partly attributable to new technologies like machine learning and an insatiable need for more data to make better decisions. The footprints of databases continue to grow. Only 3.5% shrunk, whereas 14% stayed the same. And the vast majority, 80% saw growth, and almost 39% saw larger massive growth in the size of their environment.

Enter the multiverse
--------------------

The deluge of data and more databases leads to a multi-cloud space. In 2019, 30% reported that they were running a multi-cloud environment. In 2020 it's 39%. Matt noted this by saying, "Some of the cloud providers are now taking notice. They're investing in tools to let you run their platform across other competitors’ platforms. The growth also exists, albeit slower in the hybrid space: In 2019, 41% were hybrid, and in 2020 it's 44%. 

So we're seeing more databases, more data, more providers, more locations, more hybrid installations. And so, what are the consequences? "It means for a lot of us who have to work on these systems, we have less expertise in any one of them, because we don't have the time to not only enhance our skills but to enhance the systems that we're supporting and ensure that they're properly managed and set up. We've less time per application, and we just have less time available," continued Matt. 

This means more mistakes are happening, more automated cascading issues, more outages, more security issues, more complexity, more cost, and more help is needed.

How does the industry respond?
------------------------------

Matt asserted: "There's a pervasive debate between, ‘Do we need to automate? Or how much do we need to automate? How much do we not need people? How much do we need to focus on, the automation of things, and the AI versus bringing in experts?’ We are looking at DBaaS versus the need for DBAs, and we still need experts and people who know what they are doing." 

“We need to ensure that we still have the tools and the skill set to address these problems as they occur correctly. Otherwise, we just make more problems.”

DBaaS
-----

According to Matt: "Database as a service (DBaaS) is probably one of the best inventions that have happened in the last ten years to databases." It enables developers to move quicker; it overcomes all kinds of skill gaps. However, it doesn't eliminate the need for understanding and the tools to help. It helps, but it does not eliminate the need for DBAs and expertise.

What keeps you up at night?
---------------------------

According to the respondents of this year's survey, particular challenges keep developers up at night: 

The biggest is downtime (31%) followed by fixing some unforeseen issues (17%), security issues 15%). Bad performance and query issues are insomnia inducing for 13%, while staffing issues/a lack of resources challenge 9% of respondents.

Problems happen everywhere
--------------------------

The survey further found that problems happen everywhere, whether you're in the cloud or not: 

62% in the cloud had performance issues, 54% non-cloud. Overworked staff increase by 10% when DBaaS is factored in, from 19% to 29%. According to Matt: "My speculation is when we move to a database service, we move those resources to do other things. And when database problems occur, they've got 17 other jobs to work on."

Configuration errors a significant cause of data breaches
---------------------------------------------------------

Outages and slowdowns persist in being a headline-grabbing problem. [News this week](https://www.cisomag.com/db8151dd-an-untraceable-data-breach-22-mn-emails-compromised/) reported the hacking of an open Elasticsearch database containing around 22 million of email records. [Research](https://enterprise.verizon.com/resources/reports/dbir/) by Verizon reveals that the fastest growing data breach cause is configuration errors.

How many people choose to scale their database via credit card?
---------------------------------------------------------------

From a spend perspective, survey respondents were asked: are you spending at plan, below plan, or above plan? About 24% were above plan. 33% of those using DBaaS and Cloud were above plan. 

Upon being asked, how often have you had to upgrade your database instances to something bigger the results are significant:

*   0 times - 11%
*   1-3 times 40.4%
*   4-9 times 28.6%
*   10+ times 19.5%

Matt stated that he believes the following situation is more common than it should be: "Most of these can be avoided by fixing performance problems. If we don't look for those performance issues, then we're going to fix them by paying more. And that's what a lot of people end up doing."

Unexpected costs
----------------

Several survey respondents have experienced unexpected costs, which have increased as the software complexity increases:

*   Non-public cloud users - 8% reported unexpected costs.
*   Public cloud users - 10% reported unexpected costs
*   Public cloud DBaaS - 19% said that their costs were unexpectedly higher

"We need better automation, and we need smarter tools, we need better education, better security, better performance, we need to make us all more efficient and be able to solve these problems that come up. It's very, very important," commented Matt.

Percona Monitoring and Management
---------------------------------

[Percona Monitoring and Management](https://www.percona.com/software/database-tools/percona-monitoring-and-management) is the company’s free and open source tool to simplify this with a single interface to reduce complexity. Matt shared this as background: "We want a simplified management system, where we can take that complexity and give you the ability to reduce the complexity with it."

Matt's selfish security goal and a simple solution
--------------------------------------------------

When discussing databases and security, Matt provided a very personal goal for improving the current situation. He lamented, "I don't need more credit monitoring in response to database breaching, I am good until the year 2082!" 

Matt has a simple solution: "I can solve more than 50% of the data breaches that exist now. And I can do it in one line of code: Set your password! db.changeUserPassword (username, password). It is the Change Password command for MongoDB. Mongo and Elastic are currently the two most breached databases. Most of those breaches are because nobody set a password!" 

Percona Monitoring and Management 2.6 includes the first version of Percona's security threat tool:

*   This provides checks for basic security problems and the most common issues, like missing passwords or not being at the latest version
*   More checks will be added over the next several months

### The first Release of [Percona Distribution for MongoDB:](https://www.percona.com/software/mongodb)

On the first Distribution that Percona has released for MongoDB, Matt shared: "We take all the best of the open-source components and bundle it into one there. And we're also now offering [managed services for MongoDB](https://www.percona.com/services/managed-services/percona-managed-database-services)." 

Percona also has a Distribution for PostgreSQL currently, with a Distribution for MySQL coming up. Matt also mentioned the world's highest, most trusted high availability solution for MySQL in [PerconaXtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster). 

Matt described Percona’s approach as looking to remove the problems for companies running multiple databases: "We take out all of those features and fixes and bundle it on top of MySQL Community to make it truly an enterprise-ready system.”

Helping you to scale and simplify:
----------------------------------

*   [XtraDB Cluster 8](https://www.percona.com/software/mysql-database/percona-xtradb-cluster) is faster and more scalable. There are new Kubernetes operators with easier management.
*   [Percona Distribution for PostgreSQL](https://www.percona.com/software/postgresql-distribution) has launched with more performance enhancements to come.

Percona and Linode Partnership
------------------------------

At the end of the session Matt went through how Percona is partnering with Linode to help bring Linode's customers an enhanced DBaaS. The community benefits from better operations, better tools, and enhancements that will show up in our distributions. 

Blair Lyon, VP of Marketing at Linode joined the session to share how he sees this developing: 

"Since 2003, Linode has been helping our clients accelerate innovation by making cloud computing simple, affordable, and accessible for all. We're leading a growing category of alternative cloud providers with nearly a million worldwide customers and 11 global data centers. And the key to being a true alternative to the big guys is providing the best of breed enterprise solutions and DBaaS is no exception." 

Finally, Matt encouraged all attendees to the Percona Live event to provide their insight as part of 2020’s Open Source Data Management research report. If you have not filled out the [Open Source Data Management Survey](https://www.percona.com/blog/2020/03/31/share-your-database-market-insight-by-completing-perconas-annual-survey/) then you can do so. Watch Matt's [keynote](https://www.percona.com/resources/videos/trends-are-disrupting-and-breaking-your-db-infrastructure-matt-yonkovit-percona).