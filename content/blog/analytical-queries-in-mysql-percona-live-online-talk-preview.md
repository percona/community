---
title: 'Analytical Queries in MySQL – Percona Live ONLINE Talk Preview'
date: Fri, 09 Oct 2020 17:05:14 +0000
draft: false
tags: ['oystein.grovlen', 'Events', 'MariaDB', 'MySQL', 'PLO-2020-10', 'PostgreSQL']
---

_[Percona Live Online Agenda](https://www.percona.com/live/agenda) Slot: Tue 20 Oct • New York 6:00 p.m. • London 11:00 p.m. • New Delhi 3:30 a.m. • Singapore 6:00 a.m._

### Abstract

MySQL's sweet spot is known to be online transaction processing (OLTP), and it can support a very high load of short transactions. Many users will also want to run analytical queries (OLAP) on their MySQL data. Often they achieve this by exporting their data to another database system that is tailored for analytical queries. However, this introduces overhead and delay that can be avoided by running your analytical queries directly in your MySQL database. This presentation will discuss how you can tune your complex analytical queries to achieve better performance with MySQL. We will look at some of the queries from the well-known TPC-H/DBT-3 benchmark, and show how we can improve the performance of these queries through query rewrites, optimizer hints, and improved configuration settings. We will also compare the performance of these queries to other database systems like MariaDB and PostgreSQL, and discuss how MySQL could be improved to better support these queries. While this presentation will mainly focus on MySQL, we will also compare with MariaDB and Postgres and discuss what causes the difference in performance between the systems.

### Why is your talk exciting?

This talk is exciting because we will show several ways you can improve the performance of complex queries in MySQL. We will also compare the performance of MySQL to other database systems, and discuss what MySQL could learn from those systems.

### Who would benefit the most from your talk?

Developers who use MySQL will learn how to write more efficient queries, and DBAs will learn how to tune their systems for better performance of complex queries. People that are interested in implementation aspects of database systems, should find the discussion of what.can be learned from other database systems interesting.

### What other presentations are you most looking forward to?

I look forward to the other presentations on analytical queries: "[SQL Row Store vs Data Warehouse: Which Is Right for Your Application?](https://sched.co/ePo2)" by Robert Hodges, and "[Building Data Lake with MariaDB ColumnStore](https://sched.co/ePr2)" by Sasha Vaniachine. (However, I will probably not get up at 5:30am to watch the latter live :-)). I also look forward to the presentations on "[How Can Databases Capitalize on Computational Storage?](https://sched.co/eN9q)" by Tong Zhang and JB Baker, and "[How to Protect the SQL Engine From Running Out of Memory](https://sched.co/ePo7)" by Huaiyu Xu and Song Gao.