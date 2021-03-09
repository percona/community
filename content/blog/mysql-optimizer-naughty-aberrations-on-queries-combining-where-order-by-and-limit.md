---
title: 'MySQL Optimizer: Naughty Aberrations on Queries Combining WHERE, ORDER BY and LIMIT'
date: Mon, 29 Jul 2019 11:50:51 +0000
draft: false
tags: ['author_jfgagne', 'bugs', 'MySQL', 'optimizer', 'performance']
---

![](https://www.percona.com/community-blog/wp-content/uploads/2019/07/mysql-optimizer-choose-wrong-path-200x150.jpg)Sometimes, the MySQL Optimizer chooses a wrong plan, and a query that should execute in less than 0.1 second ends-up running for 12 minutes !  This is not a new problem: bugs about this can be traced back to 2014, and a blog post on this subject was published in 2015.  But even if this is old news, because this problem recently came yet again to my attention, and because this is still not fixed in MySQL 5.7 and 8.0, this is a subject worth writing about.

The MySQL Optimizer
-------------------

Before looking at the problematic query, we have to say a few words about the optimizer.  The [Query Optimizer](https://dev.mysql.com/doc/internals/en/optimizer.html) is the part of query execution that chooses the query plan.  A [Query Execution Plan](https://dev.mysql.com/doc/refman/5.7/en/execution-plan-information.html) is the way MySQL chooses to execute a specific query.  It includes index choices, join types, table query order, temporary table usage, sorting type ...  You can get the execution plan for a specific query using the [EXPLAIN command](https://dev.mysql.com/doc/refman/5.7/en/explain.html).

A Case in Question
------------------

Now that we know what are the Query Optimizer and a Query Execution Plan, I can introduce you to the table we are querying.  The SHOW CREATE TABLE for our table is below.```
mysql> SHOW CREATE TABLE \_test\_jfg\_201907\\G
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* 1. row \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
       Table: \_test\_jfg\_201907
Create Table: CREATE TABLE \`\_test\_jfg\_201907\` (
  \`id\` int(10) unsigned NOT NULL AUTO\_INCREMENT,
  \`str1\` varchar(150) DEFAULT NULL,
  \`id1\` int(10) unsigned NOT NULL,
  \`id2\` bigint(20) unsigned DEFAULT NULL,
  \`str2\` varchar(255) DEFAULT NULL,

\[...many more id and str fields...\]

  \`create\_datetime\` datetime NOT NULL,
  \`update\_datetime\` datetime DEFAULT NULL,
  PRIMARY KEY (\`id\`),
  KEY \`key1\` (\`id1\`,\`id2\`)
) ENGINE=InnoDB AUTO\_INCREMENT=\_a\_big\_number\_ DEFAULT CHARSET=utf8

1 row in set (0.00 sec)
```And this is not a small table (it is not very big either though...):```
\# ls -lh \_test\_jfg\_201907.ibd 
-rw-r----- 1 mysql mysql 11G Jul 23 13:21 \_test\_jfg\_201907.ibd
```Now we are ready for the problematic query (I ran PAGER cat > /dev/null before to skip printing the result):```
mysql> SELECT \* FROM \_test\_jfg\_201907
  WHERE id1 = @v AND id2 IS NOT NULL
  ORDER BY id DESC LIMIT 20;
20 rows in set (27.22 sec)
```Hum, this query takes a long time (27.22 sec) considering that the table has an index on id1 and id2.  Let's check the query execution plan:```
mysql> EXPLAIN SELECT \* FROM \_test\_jfg\_201907
  WHERE id1 = @v AND id2 IS NOT NULL
  ORDER BY id DESC LIMIT 20\\G
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* 1. row \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
           id: 1
  select\_type: SIMPLE
        table: \_test\_jfg\_201907
   partitions: NULL
         type: index
possible\_keys: key1
          key: PRIMARY
      key\_len: 4
          ref: NULL
         rows: 13000
     filtered: 0.15
        Extra: Using where
1 row in set, 1 warning (0.00 sec)
```What ? The query is not using the index key1, but is scanning the whole table (key: PRIMARY in above EXPLAIN) !  How can this be ?  The short explanation is that the optimizer thinks — or should I say hopes — that scanning the whole table (which is already sorted by the id field) will find the limited rows quick enough, and that this will avoid a sort operation.  So by trying to avoid a sort, the optimizer ends-up losing time scanning the table.

Some Solutions
--------------

How can we solve this ?  The first solution is to hint MySQL to use key1 as shown below. Now the query is almost instant, but this is not my favourite solution because if we drop the index, or if we change its name, the query will fail.```
mysql> SELECT \* FROM \_test\_jfg\_201907 USE INDEX (key1)
    WHERE id1 = @v AND id2 IS NOT NULL
    ORDER BY id DESC LIMIT 20;
20 rows in set (0.00 sec)
```A more elegant, but still very hack-ish, solution is to prevent the optimizer from using an index for the ORDER BY.  This can be achieved with the modified ORDER BY clause below (thanks to [Shlomi Noach](http://code.openark.org/blog/) for suggesting this solution on a MySQL Community Chat).  This is the solution I prefer so far, even if it is still somewhat a hack.```
mysql> SELECT \* FROM \_test\_jfg\_201907
    WHERE id1 = @v AND id2 IS NOT NULL
    ORDER BY (id+0) DESC LIMIT 20;
20 rows in set (0.00 sec)
```A third solution is to use the [Late Row Lookups](https://explainextended.com/2009/10/23/mysql-order-by-limit-performance-late-row-lookups/) trick.  Even if the post about this trick is 10 years old, it is still useful — thanks to my colleague Michal Skrzypecki for bringing it to my attention.  This trick basically forces the optimizer to choose the good plan because the query is modified with the intention of making the plan explicit. This is an elegant hack, but as it makes the query more complicated to understand, I prefer not to use it.```
mysql> SELECT y.\* FROM (
  SELECT id FROM \_test\_jfg\_201907
    WHERE id1 = @v AND id2 IS NOT NULL
    ORDER BY id DESC LIMIT 20) x
  JOIN \_test\_jfg\_201907 y ON x.id = y.id
  ORDER by y.id DESC;
20 rows in set (0.00 sec)
```

The ideal solution...
---------------------

Well, the best solution would be to fix the bugs below. I claim Bug#74602 is not fixed even if it is marked as such in the bug system, but I will not make too much noise about this as Bug#78612 also raises attention on this problem:

*   [Bug#74602: Optimizer prefers wrong index because of low\_limit](https://bugs.mysql.com/bug.php?id=74602)
*   [Bug#78612: Optimizer chooses wrong index for ORDER BY](https://bugs.mysql.com/bug.php?id=78612)
*   [PS-1653: Optimizer chooses wrong index for ORDER BY DESC](https://jira.percona.com/browse/PS-1653)
*   [PS-4935: Optimizer choosing full table scan (instead of index range scan) on query order by primary key with limit.](https://jira.percona.com/browse/PS-4935)

PS-4935 is a duplicate of PS-1653 that I opened a few months ago.  In that report, I mention a query that is taking 12 minutes because of a bad choice by the optimizer (when using the good plan, the query is taking less than 0.1 second). One last thing before ending this post: I wrote above that I would give a longer explanation about the reason for this bad choice by the optimizer.  Well, this longer explanation has already been written by Domas Mituzas in 2015, so I am referring you to his [on ORDER BY optimization](https://dom.as/2015/07/30/on-order-by-optimization/) post for more details. _\--_ _Photo by [Jamie Street](https://unsplash.com/@jamie452?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/wrong?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_ _The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors' own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._