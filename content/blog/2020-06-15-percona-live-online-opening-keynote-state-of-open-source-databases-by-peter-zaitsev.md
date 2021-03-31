---
title: 'Percona Live ONLINE Opening Keynote: State of Open Source Databases by Peter Zaitsev'
date: Mon, 15 Jun 2020 15:44:28 +0000
draft: false
tags: ['author_lawrence', 'AWS', 'DBaaS', 'Kubernetes', 'Kubernetes', 'MariaDB', 'MongoDB', 'MongoDB', 'MySQL', 'MySQL', 'mysql-and-variants', 'Open Source Databases', 'opensource', 'Percona', 'PostgreSQL', 'Tools']
images:
  - blog/2020/06/SC-3-Matt-Percona.jpg
authors:
  - cate_lawrence
slug: percona-live-online-opening-keynote-state-of-open-source-databases-by-peter-zaitsev
---

Peter Zaitsev is CEO and co-founder of Percona. He opened [Percona Live ONLINE](https://www.percona.com/live/conferences) with a keynote which took a look at the historical foundations of open source software and how they have shaped the field today.

The history of open source software
-----------------------------------

In the early days of computing, software and hardware were bundled together. While the term open source wasn't coined, software was open by default. According to Peter:  "One of the big reasons for that was copyrights on software was not a thing, because the software was not really a thing before that. Laws tend to move slower and only kind of catch up with technological development." 

The source code for software was shipped with early hardware. Early adopters - typically from universities - would modify the code to fix bugs and add needed functionality, akin to the advanced open source users of today. The changes back then were openly shared under academic principles.

Enter antitrust in the 1970s
----------------------------

In the late 1960s and the early 1970s, computing was growing into a significant industry, where IBM was controlling the vast majority of the mainframe market. This resulted in an antitrust lawsuit against IBM in the US, who as a response unbundled software from hardware. 

The Copyright Act was moved by Congress to make software copyrightable and created a separate software industry distinct from hardware. Software becomes the major class of intellectual property.

The 1980s and 1990s: The Era of Romantic Open source (and free) software
------------------------------------------------------------------------

After the development of copyright for software, new projects started that rejected applying copyright and restrictive licenses to their development. Peter asserted: "I would call that an era of romantic open source software. Right? Because a lot of software was started by hobbyists or as according to Linus Torvald 'just for fun.’”

The 2000s: A dramatic decade for OSS
------------------------------------

The 2000s was a dramatic decade for open source software, part in response to the .com crash. "A lot of companies needed ways to build their solutions very efficiently and Linux, Apache MySQL, a lot of other open source options allowed them to do just that," said Peter. 

Prior to 2000, big OSS companies were limited to Red Hat which went through an IPO in the late 1990s. Enter the 2000s and Sun acquired MySQL for $1 billion, which was hugely significant to the OSS market. It was during this period that Steve Ballmer famously asserted, "Linux is a cancer that attaches itself in an intellectual property sense to everything it touches." 

In the 2000s, many businesses started to recognize the value of open source software, and with an increasing number of large enterprises starting to adopt the open-source first mentality. This included adoption by governments "to help them avoid reliance on companies from other countries," according to Peter. 

The use of open source software had a range of benefits for both companies and for developers as individuals. For enterprise customers, moving to open source resulted in lower direct costs both short term and long term. As for developers, using open source became the preference for many of them, as it was easier to experiment and get familiar with tools. Over time, it became easier to find developers that were proficient in open source technologies compared to proprietary software. This led to better productivity and faster innovation. Customers were also able to avoid the historical barrier of vendor lock-in. 

The decade then led to a new generation of open source companies being created. However, the fact that many of these were venture capital funded lead to the need for fast, high returns on those investments. Thus, many of these companies found they had the need to build a monopoly based on the pervasive message as to the advantages of open source while also increasing “stickiness” for their own businesses.

Romantic vs business values lead to 'not quite open source'
-----------------------------------------------------------

For Peter, the time of new open source companies is a new challenge. "If you really look at those approaches to business values, many are in conflict with the early stage of romantic open-source software, and the values and ideas about sharing and letting other people innovate on your software, because hey, that actually can create competition for you," he explained. 

A lot of business models were evolving from open source to 'not quite open-source'. Some of those models would be open source eventually, such as shared source licenses and open-source compatible software, which is used by a lot of cloud vendors. Peter noted that vendors would spruik this by saying, "You can move from open source to our open-source compatible software. You probably would have a very hard time moving back, but we don't talk about that." 

On the positive side, the availability of funding meant there were a lot of investments and a high pace of innovation in the software around the open source community. On the negative side, the market became more complicated with the challenge to differentiate between open source software and ‘not quite open’ software that didn't provide the same value of truly open source software.

The 2010s: The rise of the cloud: unique challenges and opportunities for OSS
-----------------------------------------------------------------------------

While AWS was started in the previous decade, the 2010s were critical for open source databases - specifically, around the cloud and open source. Peter asserted, "Cloud really hijacked the GPL license. Before the Software as a Service deployment model, software vendors who did not want others to build commercial software on their solutions could just use the GPL. Not anymore. Now, AWS probably makes more money on MySQL than Oracle does. And they can just use the GPL software and don't have to pay Oracle anything." 

Unlike the 1970s, cloud services are now bundling hardware usage costs with software. This meant open source software could no longer benefit from a zero price effect. 

This was important psychology, as Peter noted: "Previously I would have to buy a server separately. And then I have a choice, either I could go and pay thousands of dollars to license Oracle to run on that server, or I could go ahead and download Postgres and use it for free.  That is not the case anymore. It just becomes a case of a difference in the price which may not be very well understood."

Market acceptance of Not fully open source software models
----------------------------------------------------------

Peter asserted that acceptance of not fully Open Source Software models is on the rise. "It's very important for us as an open source database community to really educate folks in the market about the difference of an open source software offering and one which is marketed using an open source term but not providing the true values of open source software."

2020s: Great Momentum for Commercial Open Source
------------------------------------------------

It's a fantastic time for Commercial Open Source, with many companies getting billion dollar valuations:

*   RedHat - $24B (acquired by IBM)
*   MongoDB - $11.2B (current valuation)
*   GitHub - $7.5B (acquired by Microsoft)
*   Databricks - $6.2B (current valuation)
*   Elastic - $5.8B (current valuation)
*   Hashicorp - $5B (current valuation)
*   Confluent - $4.5B (current valuation)
*   Cloudera - $2.5B  (current valuation)

Peter commented, "Because of the success of MongoDB, Elastic and some other open source companies, we see a lot of investment and a lot of innovation in the Open Source Database space." This includes new technologies like Planet-Scale, InfluxDB, yugabyteDB, and others. It's not limited to relational databases, it includes multimodal cloud, graph databases, and time series focused.

COVID-19 Pandemic
-----------------

The pandemic has led to an acceleration of digital transformation including service delivery online and digital education. This requires lower costs and/or cost-cutting due to the predicted economic slowdown. This can be another reason for open source success, as companies have to innovate and keep their costs down. These two desires will encourage companies to both consider open source, and to keep a close key on the cost for running those systems whether this is on existing hardware or in the cloud.

DBaaS
-----

Today database as a service (DBaaS) is a preferred way to consume open source database software. According to Peter, "This allows the development team to use multiple database technologies more easily, matching them to application needs because they don't really need to install and maintain them." 

However, Peter did point to one problem around DBaaS that can affect the success of implementation for companies and for developer teams. For many use cases, DBaaS is commonly marketed by cloud vendors as ‘fully managed.’ "Because of that, we don't have to get any DBAs or other database experts on the team. However this 'fully managed' approach still needs to be configured for security, somebody still needs to advise us on the schema, help us to design the queries, etc," explained Peter. 

The rise of DBaaS has meant that developers can choose and use databases directly without the supervision of database professionals. This can cause various bad outcomes ranging from security leaks to very inefficient delivery of database services over time. For developers that assume their DBaaS provider will deliver more insights or advice, this can lead to wasted time and budget.

DBaaS and Multiverse
--------------------

Peter then provided an overview of the future as he sees it: "From an open source prism, you can think of the cloud as a commodity with many compatible implementations. Or think about highly differentiated clouds, where you have proprietary solutions available from a single vendor. The latter can be a huge vendor lock-in.  However, many are trying to avoid lock-in." 

Thus, he said, we are increasingly seeing multiple database technologies: multiple environments, hybrid cloud, multi-cloud, Many proprietary solutions are available around cloud and hybrid environments, like Google Anthos, VMware and AWS Outposts.  Simultaneously Kubernetes also has emerged as the leading open source API for hybrid and public clouds. 

Kubernetes is ubiquitous. There are proprietary solutions to simplify Kubernetes management, and the Kubernetes interface is supported by Multi and Hybrid Cloud Platforms. The is relevant to open source databases and Peter believes we should be focusing on:

*   Adapting Cloud Native deployments in Multi and Hybrid Cloud
*   Kubernetes as the API of choice for Open Source database deployments
*   Making things simple and comparable to integrated DBaaS Solutions

An important question to ask is: "If I am choosing DBaaS as my software consumption model, how do I get the most value from what Open Source Software provides?" 

According to Peter, Percona is embracing the cloud-native and multi-cloud approach through Kubernetes. Percona has released [Kubernetes Operator for  XtraDB Cluster](https://www.percona.com/doc/kubernetes-operator-for-pxc/index.html) and [ Kubernetes Operator for Percona Server for MongoDB](https://www.percona.com/doc/kubernetes-operator-for-psmongodb/index.html). "We are also working through [Percona Monitor and Management](https://www.percona.com/software/database-tools/percona-monitoring-and-management) to really help you to reduce the friction and run the open source database successfully in those cloud environments and on-premises," he said. 

Peter also advised attendees to take the time to fill out the [Open Source Data Management Survey](https://www.percona.com/blog/2020/03/31/share-your-database-market-insight-by-completing-perconas-annual-survey/). Peter closed the keynote with: "Finally, I want to say Happy 25th Birthday to MySQL. Great job, MySQL team!" 

You can also watch Peter’s [keynote](https://www.percona.com/resources/videos/state-open-source-database-plo2020).