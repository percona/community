---
title: 'A Nice Feature in MariaDB 10.3: no InnoDB Buffer Pool in Core Dumps'
date: Thu, 28 Jun 2018 12:28:58 +0000
draft: false
tags: ['author_jfgagne', 'core dump', 'InnoDB', 'InnoDB Buffer Pool', 'MariaDB', 'MariaDB 10.3', 'MariaDB Server', 'MySQL', 'MySQL', 'operations', 'Percona Server for MySQL']
images:
  - blog/2018/06/InnoDB-buffer-pool-size.jpg
authors:
  - jeff_gagne
slug: nice-feature-in-mariadb-103-no-innodb-buffer-pool-in-coredumps
---

MariaDB 10.3 is now generally available (10.3.7 was released GA on 2018-05-25). The article [What's New in MariaDB Server 10.3](https://mariadb.com/resources/blog/whats-new-mariadb-server-103) by the MariaDB Corporation lists three key improvements in 10.3: temporal data processing, Oracle compatibility features, and purpose-built storage engines. Even if I am excited about [MyRocks](https://mariadb.com/kb/en/library/myrocks/) and curious on [Spider](https://mariadb.com/kb/en/library/spider-storage-engine-overview/), I am also very interested in less flashy but still very important changes that make running the database in production easier. This post describes such improvement: **no** [**InnoDB Buffer Pool**](https://dev.mysql.com/doc/refman/5.7/en/innodb-buffer-pool.html) **in core dumps**. 

Hidden in the _Compression_ section of the page [Changes & Improvements in MariaDB 10.3](https://mariadb.com/kb/en/library/changes-improvements-in-mariadb-103/) from the [Knowledge Base](https://mariadb.com/kb/), we can read:

> On Linux, shrink the core dumps by omitting the InnoDB buffer pool

This is it, no more details, only a link to [MDEV-10814 (Feature request: Optionally exclude large buffers from core dumps)](https://jira.mariadb.org/browse/MDEV-10814). This Jira ticket was open in 2016-09-15 by a well-known MariaDB Support Engineer: Hartmut Holzgraefe. I know Booking.com was asking for this feature for a long time, this is even mentioned by Hartmut in a [GitHub comment](https://github.com/MariaDB/server/pull/333#issuecomment-296206130). 

The ways this feature eases operations with MariaDB are well documented by Hartmut in the description of the Jira ticket:

*   it needs less available disk space to store core dumps,
*   it reduces the time required to write core dumps (and hence restart MySQL after a crash),
*   it improves security by omitting substantial amount of user data from core dumps.

In addition to that, I would add that smaller core dumps are easier to share in tickets. I am often asked by support engineers to provide a core dump in relation to a crash, and my reply is "_How do you want me to give you with a 192 GB file ?_" (or even bigger files as I saw MySQL/MariaDB being used on servers with 384 GB of RAM). This often leads to a "_Let me think about this and I will come back to you_" answer. Avoiding the InnoDB Buffer Pool in core dumps makes this less of an issue for both DBAs and support providers. 

Before continuing the discussion on this improvement, I need to give more details about what a core dump is.

#### **What is a Core Dump and Why is it Useful ?**

By looking at the [Linux manual page for core (and core dump file)](http://man7.org/linux/man-pages/man5/core.5.html), we can read:

> [A core dump is] a disk file containing an image of the process's memory at the time of termination. This image can be used in a debugger to inspect the state of the program at the time that it terminated.

The [Wikipedia article for core dump](https://en.wikipedia.org/wiki/Core_dump) also tells us that:

*   the core dump includes key pieces of program state as processor registers, memory management details, and other processor and operating system flags and information,
*   the name comes from [magnetic core memory](https://en.wikipedia.org/wiki/Magnetic_core_memory), the principal form of random access memory from the 1950s to the 1970s, and the name has remained even if magnetic core technology is obsolete.

So a core dump is a file that can be very useful to understand the context of a crash. The exact details of how to use a core dump have been already discussed in many places and is beyond the subject of this post. The interested reader can learn more by following those links:

*   [Getting MySQL Core file on Linux](https://www.percona.com/blog/2011/08/26/getting-mysql-core-file-on-linux/)
*   [How to Produce a Full Stack Trace for mysqld](https://mariadb.com/kb/en/library/how-to-produce-a-full-stack-trace-for-mysqld/)
*   [MySQL is crashing: a support engineer’s point of view](https://www.percona.com/blog/2015/08/17/mysql-is-crashing-a-support-engineers-point-of-view/)
*   [Database issue cheat sheet (including gdb commands for using core dumps)](https://www.dropbox.com/s/j4salsgphyrsnjw/Cheat%20Sheet.pdf)
*   [What to Do If MySQL Keeps Crashing](https://dev.mysql.com/doc/refman/5.7/en/crashing.html)
*   [Debugging mysqld under gdb](https://dev.mysql.com/doc/refman/5.7/en/using-gdb-on-mysqld.html)

**Update 2018-07-31**: more links about how to use core dumps:

*   [How to Find Values of Session Variables With gdb](https://mysqlentomologist.blogspot.com/2017/08/how-to-find-values-of-session-variables.html)
*   [How to Find Processlist Thread id in gdb](http://mysqlentomologist.blogspot.com/2017/07/how-to-find-processlist-thread-id-in-gdb.html)
*   [gdb tips and tricks for MySQL DBAs](https://archive.fosdem.org/2015/schedule/event/mysql_gdb/attachments/slides/595/export/events/attachments/mysql_gdb/slides/595/FOSDEM2015_gdb_tips_and_tricks_for_MySQL_DBAs.pdf)

Now that we know more about core dumps, we can get back to the discussion of the new feature.

#### **The** **_no InnoDB Buffer Pool in Core Dump_** **Feature from MariaDB 10.3**

As already pointed out above, there are very few details in the release notes about how this feature works. By digging in [MDEV-10814](https://jira.mariadb.org/browse/MDEV-10814), following pointers to pull requests (#[333](https://github.com/MariaDB/server/pull/333), #[364](https://github.com/MariaDB/server/pull/364), [365](https://github.com/MariaDB/server/pull/365), ...), and reading the [commit message](https://github.com/MariaDB/server/pull/364/commits/b600f30786816e33c1706dd36cdabf21034dc781), I was able to gather this:

*   An initial patch was written by Hartmut in 2015.
*   It uses the MADV_DONTDUMP flag to the [madvise](http://man7.org/linux/man-pages/man2/madvise.2.html) system call (available in Linux kernel 3.4 and higher).
*   Hartmut's patch was rebased by Daniel Black, a well-known MariaDB Community Contributor (pull request #[333](https://github.com/MariaDB/server/pull/333)).
*   The first work by Daniel had a configuration parameter to allow including/excluding the InnoDB Buffer Pool in/from core dumps, but after a [discussion](https://github.com/MariaDB/server/pull/333#issuecomment-295460913) in pull request #333, it was decided that the RELEASE builds would not put the InnoDB Buffer Pool in core dumps and that [DEBUG builds](https://mariadb.com/kb/en/library/compiling-mariadb-for-debugging/) would include it (more about this below).
*   The function buf_madvise_do_dump is added but never invoked by the server; it is there to be called from a debugger to re-enable full core dumping if needed (from this [commit message](https://github.com/MariaDB/server/pull/364/commits/b600f30786816e33c1706dd36cdabf21034dc781)).
*   The [InnoDB Redo Log buffer](https://dev.mysql.com/doc/refman/5.7/en/innodb-redo-log-buffer.html) is also excluded from core dumps (from this [comment](https://github.com/MariaDB/server/pull/364#issuecomment-345655419)).

I have doubts about the absence of a configuration parameter for controlling the feature. Even if the InnoDB Buffer Pool (as written above, the feature also concerns the InnoDB Redo Log buffer, but I will only mention InnoDB Buffer Pool in the rest of this post for brevity) is not often required in core dumps, Marko Mäkelä, InnoDB Engineer at MariaDB.com, [mentioned sometimes needing it](https://github.com/MariaDB/server/pull/364#issuecomment-325307968) to investigate deadlocks, corruption or race conditions. Moreover, I was recently asked, in a support ticket, to provide a core dump to understand a crash in MariaDB 10.2 (public bug report in [MDEV-15608](https://jira.mariadb.org/browse/MDEV-15608)): it looks to me that the InnoDB Buffer Pool be useful here. Bottom line: having the InnoDB Buffer Pool (and Redo log buffer) in core dumps might not be regularly useful, but it is sometimes needed. 

To include the InnoDB Buffer Pool in core dumps, DBAs can install DEBUG binaries or they can use a debugger to call the buf_madvise_do_dump function (well thought Daniel for compensating the absence of a configuration parameter, but there are caveats described below). Both solutions are suboptimal in my humble opinion. For #2, there are risks and drawbacks of using a debugger on a live production database (when it works ... see below for a war story). For #1 and unless I am mistaken, DEBUG binaries are not available from the [MariaDB download site](https://downloads.mariadb.org/). This means that they will have to be built by engineers of your favorite support provider, or that DBAs will have to [manually compile](https://mariadb.com/kb/en/library/compiling-mariadb-for-debugging/) them: this is a lot of work to expect from either party. I also think that the usage of DEBUG binaries in production should be minimized, not encouraged (DEBUG binaries are for developers, not DBAs); so I feel we are heading in the wrong direction. Bottom line: I would not be surprised ([and I am not alone](https://github.com/MariaDB/server/pull/333#issuecomment-295644884)) that a parameter might be added in a next release to ease investigations of InnoDB bugs. 

Out of curiosity, I checked the core dump sizes for some versions of MySQL and MariaDB with [dbdeployer](https://github.com/datacharmer/dbdeployer) (if you have not tried it yet, you should probably spend time [learning how to use dbdeployer](https://www.percona.com/blog/2018/05/24/using-dbdeployer-to-manage-mysql-percona-server-and-mariadb-sandboxes/): it is very useful). Here are my naive first results with default configurations and freshly started mysqld:

*   487 MB and 666 MB core dumps with MySQL 5.7.22 and 8.0.11 respectively,
*   673 MB and 671 MB core dumps with MariaDB 10.2.15 and MariaDB 10.3.7 respectively.

I tried understanding where the inflation is coming from in MySQL 8.0.11 but I tripped on [Bug#90561](https://bugs.mysql.com/bug.php?id=90561) which prevents my investigations. We will have to wait for 8.0.12 to know more... 

Back to the feature, I was surprised to see no shrinking between MariaDB 10.2 and 10.3. To make sure something was not wrong, I tried to have the InnoDB Buffer Pool in the core dump by calling the buf_madvise_do_dump function. I used the [slides](https://archive.fosdem.org/2015/schedule/event/mysql_gdb/attachments/slides/595/export/events/attachments/mysql_gdb/slides/595/FOSDEM2015_gdb_tips_and_tricks_for_MySQL_DBAs.pdf) from the [gdb tips and tricks for MySQL DBAs](https://archive.fosdem.org/2015/schedule/event/mysql_gdb/) talk by [Valerii Kravchuk](https://mysqlentomologist.blogspot.com/) presented at FOSDEM 2015 (I hope a similar talk will be given soon at Percona Live as my gdb skills need a lot of improvements), but I got the following result:
```
$ gdb -p $(pidof mysqld) -ex "call buf_madvise_do_dump()" -batch
[...]
No symbol "buf_madvise_do_dump" in current context.
```
After investigations, I understood that the generic MariaDB Linux packages that I used with dbdeployer are compiled without the feature. A reason could be that there is no way to know that those packages will be used on a Linux 3.4+ kernel (without a recent enough kernel, the MADV_DONTDUMP argument does not exist for the madvise system call). To be able to test the feature, I would either have to build my own binaries or try packages for a specific distribution. I chose to avoid compilation but this was more tedious than I thought… 

By the way, maybe the buf_madvise_do_dump function should always be present in binaries and return a non-zero value when failing with a detailed message in the error logs. This would have spared me spending time understanding why it did not work in my case. I opened [MDEV-16605: Always include buf_madvise_do_dump in binaries](https://jira.mariadb.org/browse/MDEV-16605) for that. 

Back to my tests and to see the feature in action, I started a [Ubuntu 16.04.4 LTS](http://releases.ubuntu.com/16.04/) in AWS (it comes with a 4.4 kernel). But again, I could not call buf_madvise_do_dump. After more investigation, I understood that the Ubuntu and Debian packages are [not compiled with symbols](https://sysadmin.compxtreme.ro/how-to-add-debug-symbols-for-mariadb-debianubuntu-packages/), so calling buf_madvise_do_dump cannot be easily done on those (I later learned that there are _mariadb-server-10.3-dbgsym_ packages, but I did not test them). I ended-up falling back to Centos 7.5, which comes with a 3.10 kernel, and it worked ! Below are the core dump sizes with and without calling buf_madvise_do_dump:

*   527 MB core dump on MariaDB 10.3.7 (without calling buf_madvise_do_dump),
*   674 MB core dump on MariaDB 10.3.7 (with calling buf_madvise_do_dump).

I was surprised by bigger core dumps in MariaDB 10.3 than in MySQL 5.7, so I spent some time looking into that. It would have been much easier with the [Memory Instrumentation](https://dev.mysql.com/doc/mysql-perfschema-excerpt/5.7/en/memory-summary-tables.html) from [Performance Schema](https://dev.mysql.com/doc/refman/5.5/en/performance-schema.html), but this is not yet available in MariaDB. There is a Jira ticket opened for that ([MDEV-16431](https://jira.mariadb.org/browse/MDEV-16431)); if you are also interested in this feature, I suggest you vote for it. 

I guessed that the additional RAM used by MariaDB 10.3 (compared to MySQL 5.7) comes from the caches for the [MyISAM](https://mariadb.com/kb/en/library/myisam-storage-engine/) and [Aria](https://mariadb.com/kb/en/library/aria-storage-engine/) storage engines. Those caches, whose sizes are controlled by the [key_buffer_size](https://mariadb.com/kb/en/library/myisam-system-variables/#key_buffer_size) and [aria_pagecache_buffer_size](https://mariadb.com/kb/en/library/aria-system-variables/#aria_pagecache_buffer_size) parameters, are 128 MB by default in MariaDB 10.3 (more discussion about these sizes below). I tried shrinking both caches to 8 MB ([the default value in MySQL since at least 5.5](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_key_buffer_size)), but I got another surprise:

```
> SET GLOBAL key_buffer_size = 8388608;
Query OK, 0 rows affected (0.001 sec)

> SET GLOBAL aria_pagecache_buffer_size = 8388608;
ERROR 1238 (HY000): Variable 'aria_pagecache_buffer_size' is a read only variable
```
The [aria_pagecache_buffer_size](https://mariadb.com/kb/en/library/aria-system-variables/#aria_pagecache_buffer_size) parameter is not dynamic ! This is annoying as I like tuning parameters to be dynamic, so I opened [MDEV-16606: Make aria_pagecache_buffer_size dynamic](https://jira.mariadb.org/browse/MDEV-16606) for that. I tested with only shrinking the MyISAM cache and by modifying the startup configuration for Aria. The results for the core dump sizes are the following:

*   527 MB core dump for the default behavior,
*   400 MB core dump by shrinking the MyISAM cache from 128 MB to 8 MB,
*   268 MB core dump by also shrinking the Aria cache from 128 MB to 8 MB.

We are now at a core dump size smaller than MySQL 5.7.22: this is the result I was expecting. 

I did some more tests with a larger InnoDB Buffer Pool and with a larger InnoDB Redo Log buffer while keeping MyISAM and Aria cache sizes to 8 MB. Here are the results of the sizes of the compact core dump (default behavior) vs the full core dump (using gdb):

*   340 MB vs 1.4 GB core dumps when growing the InnoDB Buffer Pool from 128 MB to 1 GB,
*   357 MB vs 1.7 GB core dumps when also growing the InnoDB Redo Log buffer from 16 MB to 128 MB.

I think the results above show the usefulness of the no InnoDB Buffer Pool in core dump feature.

#### **Potential Improvements of the** **_Shrinking_** **Core Dump Feature**

The end goal of excluding the InnoDB Buffer Pool from core dumps is to make generating and working with those files easier. As already mentioned above, the space and time taken to save core dumps are the main obstacles, and sharing them is also an issue (including leaking a lot of user data). 

Ideally, I would like to always run MySQL/MariaDB with core dump enabled on crashes (I see one exception when using [database-level encryption](https://www.percona.com/blog/2016/04/08/mysql-data-at-rest-encryption/) for not leaking data). I even think this should be the default behavior, but this is another discussion that I will not start here. My main motivation is that if/when MySQL crashes, I want all information needed to understand the crash (and eventually report a bug) without having to change parameters, restart the database, and generate the same crash again. Obviously, this configuration is unsuitable for servers with a lot of RAM and with a large InnoDB Buffer Pool. MariaDB 10.3 makes a big step forward by excluding the InnoDB Buffer Pool (and Redo Log buffer) from core dumps, but what else could be done to achieve the goal of always running MySQL with core dump enabled ? 

There is a [pull request to exclude the query cache from core dumps](https://github.com/MariaDB/server/pull/366) (also by Daniel Black, thanks for this work). When MariaDB is run with a large [query cache](https://mariadb.com/kb/en/library/query-cache/) (and I know this is unusual, but if you know of a valid real world use case, please add a comment below), excluding it from core dumps is good. But I am not sure this is a generally needed improvement:

*   [MySQL 8.0 has retired the query cache](https://mysqlserverteam.com/mysql-8-0-retiring-support-for-the-query-cache/),
*   the [query cache is disabled by default from MariaDB 10.1.7](https://mariadb.com/kb/en/library/server-system-variables/#query_cache_type),
*   and the default value for the [query cache size was zero before MariaDB 10.1.7](https://mariadb.com/kb/en/library/server-system-variables/#query_cache_size).

It looks like there is a consensus that the query cache is a very niche feature and otherwise should be disabled, so this work might not be the one that will profit most people. Still good to be done though. 

I would like similar work to be done on MyISAM, Aria, [TokuDB](https://mariadb.com/kb/en/library/tokudb/) and MyRocks. As we saw above, there is an opportunity, for default deployments, to remove 256 MB from core dumps by excluding MyISAM and Aria caches. I think this work is particularly important for those two storage engines as they are loaded by default in MariaDB. By the way, and considering the relatively low usage of the MyISAM and Aria storage engine, maybe the default value for their caches should be lower: I opened [MDEV-16607: Consider smaller defaults for MyISAM and Aria cache sizes](https://jira.mariadb.org/browse/MDEV-16607) for that. 

I cannot think of any other large memory buffers that I would like to exclude from core dumps. If you think about one, please add a comment below. 

Finally, I would like the shrinking core dump feature to also appear in Oracle MySQL and Percona Server, so I opened [Bug#91455: Implement core dump size reduction](http://bugs.mysql.com/bug.php?id=91455) for that. For the anecdote, I was recently working on a Percona Server crash in production, and we were reluctant to enable core dumps because of the additional minutes of downtime needed to write the file to disk. In this case, the no InnoDB Buffer Pool in core dump would have been very useful !