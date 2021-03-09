---
title: 'Minimalist Tooling for MySQL/MariaDB DBAs'
date: Wed, 14 Aug 2019 14:21:10 +0000
draft: false
tags: ['author_geoff', 'DBA Tools', 'MariaDB', 'MySQL', 'Tools']
---

![](https://www.percona.com/community-blog/wp-content/uploads/2019/08/dba-tools-minimalist-mysql-tooling-200x150.jpg)In my roles as a DBA at various companies, I generally found the tooling to be quite lacking. Everything from metrics collection, alerting, backup management; they were either missing, incomplete or implemented poorly. [DBA-Tools](http://gitlab.com/gwinans/dba-tools) was born from a desire to build backup tools that supported my needs in smaller/non-cloud environments. As BASH is easily the most common shell available out there on systems running MySQL® or MariaDB®, it was an easy choice.

How DBA-Tools came to be
------------------------

While rebuilding my home-lab two years ago, I decided I wanted some simple tools for my database environment. Being a fan of NOT re-inventing the wheel, I thought I would peruse GitHub and Gitlab to see what others have put together. Nothing I saw looked quite like what I wanted. They all hit one or more of the checkboxes I wanted, but never all of them. My checklist when searching for tools included the following features:

*   Extendable
*   Configurable
*   User Friendly
*   Easy-to-Read

The majority of scripts I found were contained within a single file and not easy to extend. They were universally easy-to-use. My subjective requirement for code quality simply was not met. When I considered what kits were already available to me against the goal I had in mind, I came to the only reasonable conclusion I could muster: I would build my own tools!

A trip down release lane and publicity
--------------------------------------

DBA-Tools was designed to be simple, extendible and configurable. I wanted my kit to have very few external dependencies. BASH was the shell I chose for implementation and I grew my vision from there. At the most fundamental level, I enjoy simplicity. I consider procedural programming to be just that – simple. This, thus far, remains my guiding philosophy with these tools. My first public release was on July 7th, 2019. The scripts only did single full backups and most of the secondary scripts only worked with MariaDB. I posted about it in one of the MySQL Slack groups. The tools were written for my lab use and, while I hoped others would find my offering useful, the lack of noticeable response did not bother me. The second release, 22 days later, marked full incremental support and ensured all the secondary scripts supported MySQL and MariaDB. I decided to call this one 2.0.0 and posted it again. I received my first “support” email that day, which spurred me to create better documentation. Later, I found out that Peter Zaitsev posted about the tools I wrote on his Twitter and LinkedIn pages on August 11th 2019. I can’t say thank you enough – I didn’t expect these tools to be used much beyond a small niche of home-lab engineers that might stumble across them.

What’s next?
------------

As of this writing, I’m working on adding extensible, easy-to-use alerting facilities to these tools. I’m always ready to accept PRs and help from anyone that would like to add their own features. Now, I just need to get significantly better with git. In any case, check them out at [http://gitlab.com/gwinans/dba-tools](http://gitlab.com/gwinans/dba-tools) or read the Wiki at [https://gitlab.com/gwinans/dba-tools/wikis/home](https://gitlab.com/gwinans/dba-tools/wikis/home)

\-- _Photo by [Iker Urteaga](https://unsplash.com/@iurte?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/tools?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_

_The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._