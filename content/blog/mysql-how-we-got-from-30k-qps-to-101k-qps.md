---
title: 'MySQL 5.6/Maria 10.1 : How we got from 30k qps to 101k qps.....'
date: Wed, 07 Aug 2019 07:52:45 +0000
draft: false
tags: ['author_gurnish', 'MariaDB', 'MySQL', 'performance']
---

![](https://www.percona.com/community-blog/wp-content/uploads/2019/08/tuning-mysql-for-throughput-300x200.jpg)Late one evening, I was staring at one of our large MySQL installations and noticed the database was hovering around 7-10 run queue length (48 cores, ~500 gigs memory, fusionIO cards). I had been scratching my head on how to get more throughput from the database. This blog records the changes I made to tune performance in order to achieve a 300% better throughput in MySQL. I tested my theories on MySQL 5.6/Maria 10.1. While with 5.7 DBAs would turn to _performance\_schema_ for the supporting metrics, I hope that you find the process interesting nevertheless.

View from an Oracle RDBMS DBA...
--------------------------------

For context, I came to MySQL from a background as an Oracle RDBMS DBA, and this informs my expectations. For this exercise, unlike with Oracle RDBMS, I had no access to view _wait events_ so that I could see where my database was struggling. At least, no access in MySQL 5.6/Maria 10.1 without taking a performance hit by using _performance\_schema_, which was less efficient in these earlier versions. In fact, overall, I find that MySQL has far fewer bells and whistles than Oracle at the database level. I constantly whine to my team mates how MySQL provides less knobs compared to Oracle. Even for just creating an index. Without counting, I can confidently say there are over 50 permutations combinations I could use. For example initrans, pctfree, pct\*\*, reverse, function, w/o gathering statistics... Admittedly some may be obsolete and discarded in recent versions, but you get my point. :) Oracle allows the DBA’s to tune blocks in an index or a table, their physical characteristics….all the way to pinning tables in buffer, tuning specific latches used for buffer cache so one can get rid of cache buffer chains waits with help of a hidden parameter  :) Anyway, I digress. Back to the challenges of MySQL!

Tuning MySQL... a process
-------------------------

Given the version of MySQL that provided this challenge, one of the few tools you have access to is the output from show engine innodb status. While that has a wealth of information, I haven't yet found a single source of good documentation for each of the metrics shown in the report. I repeatedly saw these _waits_ in the SEMAPHOREs section:```
buf0buf.c
row0rel.cc
btr0btr.c
```Very naturally I started with reference books available on MySQL’s website, traversing through countless blogs, and sniffing through the code. Only after I had looked at multiple sources did I begin to get a gist of the metrics available in the status report. My research over the next few nights led me to a few different parameters. These ultimately helped me to find the answers I needed.

Making the changes that mattered
--------------------------------

Here is a quick snippet that I changed from the default – or lower – values set by a previous DBA.```
innodb\_buffer\_pool\_instances=32
table\_open\_cache\_instances=12
table\_open\_cache=8000
table\_definition\_cache=12000
innodb\_change\_buffer\_size=5
```Some other parameters that I changed are shown next. Although these are very scenario specific, they all helped in tuning one or other of the performance problems I was encountering:```
innodb\_purge\_batch\_size=5000 
optimizer\_search\_depth=0
innodb\_log\_file\_size=32g
innodb\_log\_buffer\_size=1G

```Plus, I set innodb\_adaptive\_hash\_index\_parts to 32. _Note:_ this parameter may be called innodb\_adaptive\_hash\_partitions  in some db versions I will try and explain them to the best of my knowledge and understanding. innodb\_buffer\_pool\_instances  had to be increased to allow a greater number of latches to access the buffer pool. Ideally we want to keep this parameter either equal to or a little lower than the number of cores. In this case we set this at half of the number of cores. We have other boxes in the farm with fewer cores and prefer to keep to standard configs and not have snowflakes! table\_open\_cache\_instance also provided similar performance improvement for all queries accessing table metadata. If you are a heavy user of adaptive hash indexes, splitting innodb\_adaptive\_hash\_parts/innodb\_adaptive\_hash\_partitions (depending on your db version) to a higher number of partitions helps a lot with concurrency. It allows you to split hash indexes into  different partitions and to remove contention with hot tables access. We reduced innodb\_change\_buffer\_size  to 5% from its default 25% because change buffer was never used more than 400mb. With the default value the change buffer had ~90gb allocated. This provided for a lot more data and indices to fit into the buffer pool.

Conclusion
----------

Overall this set of parameters tuning worked for us and for our workload. We saw a great performance benefit from these changes. It was the first time we ever surpassed 100k qps without changing the code or hardware. Please make sure to understand what each parameter does, and to test your workload against them. _—_ _[Photo by ](https://unsplash.com/search/photos/raspberry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)[João Silas](https://unsplash.com/@joaosilas?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)[ on ](https://unsplash.com/search/photos/raspberry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)[Unsplash](https://unsplash.com/search/photos/mystery?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_ _The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._