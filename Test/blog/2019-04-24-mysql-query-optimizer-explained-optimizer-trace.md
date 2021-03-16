---
title: 'Percona Live Presents: The MySQL Query Optimizer Explained Through Optimizer Trace'
date: Wed, 24 Apr 2019 16:16:09 +0000
draft: false
tags: ['author_oystein', 'Events', 'MySQL', 'Percona Live 2019']
images:
  - blog/2019/04/oysteing3.jpg
authors:
  - oystein_grovlen
---

During my presentation at [Percona Live 2019](https://www.percona.com/live/19/sessions/the-mysql-query-optimizer-explained-through-optimizer-trace) I will show how using Optimizer Trace can give insight into the inner workings of the MySQL Query Optimizer. Through the presentation, the audience will both be introduced to optimizer trace, learn more about the decisions the query optimizer makes, and learn about the query execution strategies the query optimizer has at its disposal. I'll be covering the main phases of the MySQL optimizer and its optimization strategies, including query transformations, data access strategies, the range optimizer, the join optimizer, and subquery optimization.

![Øystein Grøvlen](blog/2019/04/oysteing3.jpg)

Who’d benefit most from the presentation?
-----------------------------------------

DBAs, developers, support engineers and other people who are concerned about MySQL query performance will benefit from this presentation. Knowing the optimizer trace will enable them to understand why the query optimizer selected a particular query plan. This will be very helpful in order to understand how tune their queries for better performance.

Whose presentations are you most looking forward to?
----------------------------------------------------

I'm definitely looking forward to [A Proactive Approach to Monitoring Slow Queries](https://www.percona.com/live/19/sessions/a-proactive-approach-to-monitoring-slow-queries) by Shashank Sahni of [ThousandEyes Inc](https://www.thousandeyes.com/). It is always interesting to learn how users of MySQL monitor their systems to detect and improve slow queries.