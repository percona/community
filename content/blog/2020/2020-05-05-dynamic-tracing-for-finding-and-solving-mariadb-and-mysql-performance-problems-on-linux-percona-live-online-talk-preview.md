---
title: 'Dynamic Tracing for Finding and Solving MariaDB (and MySQL) Performance Problems on Linux - Percona Live ONLINE Talk Preview'
date: Tue, 05 May 2020 21:13:57 +0000
draft: false
tags: ['valeriy.kravchuk', 'Events', 'MariaDB', 'MySQL']
authors:
  - valeriy_kravchuk
images:
  - blog/2020/05/Social-PL-Online-2020-1.jpg
slug: dynamic-tracing-for-finding-and-solving-mariadb-and-mysql-performance-problems-on-linux-percona-live-online-talk-preview
---

_[Percona Live Online](https://www.percona.com/live/conferences) Agenda Slot (CORRECTED): Wed 20 May • New York 6:00 a.m. • London 11:00 a.m. • New Delhi 3:30 p.m._ _Level: Advanced_

### Abstract

While troubleshooting MariaDB server performance problems it is important to find out where the time is spent in the mysqld process, on-CPU and off-CPU. The process of investigation should have as small influence as possible on the server we try to troubleshoot.  Performance\_schema introduced in MySQL 5.5 (and inherited from MySQL 5.6 by MariaDB) is supposed to provide detailed enough instrumentation for most cases. But it comes with a cost, requires careful sizing of performance counters, and the process of instrumenting the code is not yet complete even for MySQL 8, to say nothing about MariaDB with its 3rd party storage engines, plugins and libraries like Galera. 

This is when perf profiler and, on recent Linux kernels (4.9+) eBPF and bpftrace tools come handy.  Specifically, perf profiler and ftrace interface can be easily used while studying MariaDB performance problems. Basic usage steps are presented and several typical real life use cases (including adding dynamic probes to almost any line of MariaDB code) are discussed.  On Linux 4.9+ eBPF is probably the most powerful and least intrusive way to study performance problems. Basic usage of , bcc tools and bpftrace, as well as main bpftrace features and commands are demonstrated.  One of the ways to present and study stack samples collected by perf or bpftrace, Flame Graphs, is also presented with examples coming from my experince as a support engineer.

### Why is your talk exciting?

It summarizes the experience from my recent years of practical non-trivial performance problems solving for MariaDB and MySQL systems in production. It turned out that application level instrumentation of database servers in MySQL ecosystem is not detailed and dynamic enough for some complex cases. We do not see Performance Schema instrumentation as every other line of MySQL code, yet, and even less so it applied to 3rd party plugins and technologies, like Galera. 

We can not expect developers to promptly add instrumentation where we need it and release custom binaries for every specific case, even in such a dynamic company like MariaDB Corporation, where we in services work closely with Engineering every day. That is why I personally got so excited when I found out that Linux starting for kernels 2.6.x (RHEL6) provides tools and approaches to add instrumentation almost anywhere, from kernel code to applications, dynamically, at run time, without any change needed in kernel or application code (something I've seen in action with DTrace on Solaris and OS X since 2008 or so). 

I started with perf profiler as a way to find out why some threads hanged for minutes when Performance Schema had not provided the answer, back in 2016, and this is when I first hit Brendan Gregg's site ([http://www.brendangregg.com/)](http://www.brendangregg.com/)). Since that first real success with perf I follow him and dynamic tracing topic closely, and try to apply new tools added in the meantime while working on complex performance issues in MariaDB Support. I've shared my experience both in public and internally in MariaDB Corporation, and got several key MariaDB developers excited and happy about the details they can get from perf and dynamic tracing in general, comparing to any other approach. I'd like to convert more engineers to this faith with my presentation. 

I know about companies like Facebook having the entire teams working on custom dynamic tracing tools, and other MySQL Community members sharing their positive experience recently. Linux kernel developers work hard on making dynamic tracing even more safe, non-intrusive and easy to use. So, dynamic tracing (finally) becomes a hot topic that every database expert should follow!

### Who would benefit the most from your talk?

I think experienced DBAs, as well as everyone working in professional services who cares about performance tuning on Linux would benefit a lot. But Linux sysadmins and application developers may get entirely new, different perspective on how to deal with performance problems when their application level instrumentation does not help to pinpoint the root cause. I consider dynamic tracing and profiling on modern Linux systems (starting from kernels 2.6.x, and especially 4.9+ with eBPF fully functional) a practice worth to be mastered by any IT professional these days.

### What other presentations are you most looking forward to?

I am really interested in "Diagnosing Memory Utilization, Leaks and Stalls in Production" by Marcos Albe. I expect they my dear friend, former colleague and manager in Percona Support is exploring the same way of approaching performance problems (with Linux dynamic tracing tools) that I do. He probably started exploring this way earlier than me (my first attempts to use perf profiler while working on support issues date back only to 2016). He is also of the smartest people I ever worked with, and is working for a company that deals with complex performance problems on all kinds of forks of open source databases, not only MySQL, in all kinds of environments including containers. So I'll surely benefit from his views and experience shared in this presentation. I hope to study more about eBPF-based dynamic tracing of memory allocations, cache and registers usage, memory flame graphs and similar tools applied in production to MySQL and other DBMSes. 

I am also looking forward to "Profiling MySQL and MariaDB Hash Join Implementations" by Jim Tommaney. MySQL Optimizer and query optimization in general are my area of interests since 2005 and I'd really want to find more details about the way hash joins are finally implemented, and comparison to various BKA-based optimizations we have for that in MariaDB. MySQL 8.0.x is a moving target now, with every minor release introducing new features, and I do not have enough time to keep my knowledge current on this topic. That's why i expect both a useful review and summary, and details about changes introduced by recent MySQL 8.0.20 in this area. 

Overall [the conference agenda](https://www.percona.com/live/percona-live-online-full-agenda) looks really great, and i am considering taking a full day (if not two) off to spend most of these 24 hours online listening to talks.