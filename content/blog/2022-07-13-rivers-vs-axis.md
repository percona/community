---
title: 'Rivers vs Axis'
date: "2022-07-18T00:00:00+00:00"
draft: false
tags: ['SQL']
authors:
  - maksim_gramin
images:
  - blog/2022/7/axis.jpg
slug: rivers-vs-axis
---


It’s hard to find at least two people who would format the same SQL query in the same way. Everyone has their own style and their own arguments. And everyone is absolutely sure that this is the only right way.

That was to be expected, because of the declarative nature of SQL. In imperative program languages, we define and control the order of statements execution, and it affects how we format our code. But in SQL query we don't know at all the order of execution in advance and it deprives us of an important reference point. As a result, we have a lot of formatting options.

But almost all of these options have one common unpleasant detail. In typography, it is called a [river](https://en.wikipedia.org/wiki/River_(typography)) and it is considered to be bad typography. Let's look at a simple query. The river (marked red) tore our query into two jagged parts and makes the code more difficult to read.

![Rivers](blog/2022/7/rivers.png)

But legendary Joe Celko in his book ["Joe Celko's SQL Programming Style"](https://www.amazon.com/Celkos-Programming-Kaufmann-Management-Systems/dp/0120887975) sad: let's turn our rivers into axis. Same query but with the axis instead the river:

![Axis](blog/2022/7/axis.png)

Let's look at a more complicated query with subqueries:

![Axis](blog/2022/7/axis-2.png)

We immediately visually detect three axis and three corresponding queries. This allows us to quickly and easily find out what this query does.

In this post I use my way to build an axis (maybe not the best), surely you can find other methods for this.

PS

There are hot [Reddit discussion](https://www.reddit.com/r/SQL/comments/sp2jav/how_do_you_format_your_sql_queries) about rivers vs axis.

PPS

[sqlfluff](https://github.com/sqlfluff/sqlfluff) is amazing tool for linting and formatting your SQL queries. Unfortunately sqlfluff recognizes queries with axis like bad queries and it's very sad. Please vote to this issue https://t.co/YArKsaqUaM
