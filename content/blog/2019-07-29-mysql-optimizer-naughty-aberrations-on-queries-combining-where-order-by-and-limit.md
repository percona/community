---
title: 'MySQL Optimizer: Naughty Aberrations on Queries Combining WHERE, ORDER BY and LIMIT'
date: Mon, 29 Jul 2019 11:50:51 +0000
draft: false
tags: ['author_jfgagne', 'bugs', 'MySQL', 'optimizer', 'performance']
images:
  - blog/2019/07/mysql-optimizer-choose-wrong-path.jpg
authors:
  - jeff_gagne
slug: mysql-optimizer-naughty-aberrations-on-queries-combining-where-order-by-and-limit
---

Sometimes, the MySQL Optimizer chooses a wrong plan, and a query that should execute in less than 0.1 second ends-up running for 12 minutes!This is not a new problem: bugs about this can be traced back to 2014, and a blog post on this subject was published in 2015.But even if this is old news, because this problem recently came yet again to my attention, and because this is still not fixed in MySQL 5.7 and 8.0, this is a subject worth writing about.

![](blog/2019/07/mysql-optimizer-choose-wrong-path.jpg)

The MySQL Optimizer
-------------------

Before looking at the problematic query, we have to say a few words about the optimizer.The [Query Optimizer](https://dev.mysql.com/doc/internals/en/optimizer.html) is the part of query execution that chooses the query plan.A [Query Execution Plan](https://dev.mysql.com/doc/refman/5.7/en/execution-plan-information.html) is the way MySQL chooses to execute a specific query.It includes index choices, join types, table query order, temporary table usage, sorting type ... You can get the execution plan for a specific query using the [EXPLAIN command](https://dev.mysql.com/doc/refman/5.7/en/explain.html).

A Case in Question
------------------

Now that we know what are the Query Optimizer and a Query Execution Plan, I can introduce you to the table we are querying. The SHOW CREATE TABLE for our table is below.
```
mysql> SHOW CREATE TABLE _test_jfg_201907G
*************************** 1. row ***************************
Table: _test_jfg_201907
Create Table: CREATE TABLE `_test_jfg_201907` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`str1` varchar(150) DEFAULT NULL,
`id1` int(10) unsigned NOT NULL,
`id2` bigint(20) unsigned DEFAULT NULL,
`str2` varchar(255) DEFAULT NULL,

[...many more id and str fields...]

`create_datetime` datetime NOT NULL,
`update_datetime` datetime DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `key1` (`id1`,`id2`)
) ENGINE=InnoDB AUTO_INCREMENT=_a_big_number_ DEFAULT CHARSET=utf8

1 row in set (0.00 sec)
```
And this is not a small table (it is not very big either though...):
```
# ls -lh _test_jfg_201907.ibd
-rw-r----- 1 mysql mysql 11G Jul 23 13:21 _test_jfg_201907.ibd
```
Now we are ready for the problematic query (I ran PAGER cat > /dev/null before to skip printing the result):
```
mysql> SELECT * FROM _test_jfg_201907
WHERE id1 = @v AND id2 IS NOT NULL
ORDER BY id DESC LIMIT 20;
20 rows in set (27.22 sec)
```
Hum, this query takes a long time (27.22 sec) considering that the table has an index on id1 and id2. Let's check the query execution plan:
```
mysql> EXPLAIN SELECT * FROM _test_jfg_201907
WHERE id1 = @v AND id2 IS NOT NULL
ORDER BY id DESC LIMIT 20G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: _test_jfg_201907
partitions: NULL
type: index
possible_keys: key1
key: PRIMARY
key_len: 4
ref: NULL
rows: 13000
filtered: 0.15
Extra: Using where
1 row in set, 1 warning (0.00 sec)
```
What ? The query is not using the index key1, but is scanning the whole table (key: PRIMARY in above EXPLAIN) ! How can this be ? The short explanation is that the optimizer thinks — or should I say hopes — that scanning the whole table (which is already sorted by the id field) will find the limited rows quick enough, and that this will avoid a sort operation. So by trying to avoid a sort, the optimizer ends-up losing time scanning the table.

Some Solutions
--------------

How can we solve this ? The first solution is to hint MySQL to use key1 as shown below. Now the query is almost instant, but this is not my favourite solution because if we drop the index, or if we change its name, the query will fail.

```
mysql> SELECT * FROM _test_jfg_201907 USE INDEX (key1)
WHERE id1 = @v AND id2 IS NOT NULL
ORDER BY id DESC LIMIT 20;
20 rows in set (0.00 sec)
```

A more elegant, but still very hack-ish, solution is to prevent the optimizer from using an index for the ORDER BY. This can be achieved with the modified ORDER BY clause below (thanks to [Shlomi Noach](http://code.openark.org/blog/) for suggesting this solution on a MySQL Community Chat). This is the solution I prefer so far, even if it is still somewhat a hack.

```
mysql> SELECT * FROM _test_jfg_201907
WHERE id1 = @v AND id2 IS NOT NULL
ORDER BY (id+0) DESC LIMIT 20;
20 rows in set (0.00 sec)
```

A third solution is to use the [Late Row Lookups](https://explainextended.com/2009/10/23/mysql-order-by-limit-performance-late-row-lookups/) trick. Even if the post about this trick is 10 years old, it is still useful — thanks to my colleague Michal Skrzypecki for bringing it to my attention. This trick basically forces the optimizer to choose the good plan because the query is modified with the intention of making the plan explicit. This is an elegant hack, but as it makes the query more complicated to understand, I prefer not to use it.

```
mysql> SELECT y.* FROM (
SELECT id FROM _test_jfg_201907
WHERE id1 = @v AND id2 IS NOT NULL
ORDER BY id DESC LIMIT 20) x
JOIN _test_jfg_201907 y ON x.id = y.id
ORDER by y.id DESC;
20 rows in set (0.00 sec)
```

The ideal solution...
---------------------

Well, the best solution would be to fix the bugs below. I claim Bug#74602 is not fixed even if it is marked as such in the bug system, but I will not make too much noise about this as Bug#78612 also raises attention on this problem:

*   [Bug#74602: Optimizer prefers wrong index because of low_limit](https://bugs.mysql.com/bug.php?id=74602)
*   [Bug#78612: Optimizer chooses wrong index for ORDER BY](https://bugs.mysql.com/bug.php?id=78612)
*   [PS-1653: Optimizer chooses wrong index for ORDER BY DESC](https://jira.percona.com/browse/PS-1653)
*   [PS-4935: Optimizer choosing full table scan (instead of index range scan) on query order by primary key with limit.](https://jira.percona.com/browse/PS-4935)

PS-4935 is a duplicate of PS-1653 that I opened a few months ago. In that report, I mention a query that is taking 12 minutes because of a bad choice by the optimizer (when using the good plan, the query is taking less than 0.1 second). 

One last thing before ending this post: I wrote above that I would give a longer explanation about the reason for this bad choice by the optimizer. Well, this longer explanation has already been written by Domas Mituzas in 2015, so I am referring you to his [on ORDER BY optimization](https://dom.as/2015/07/30/on-order-by-optimization/) post for more details. 

_--_ 

_Photo by [Jamie Street](https://unsplash.com/@jamie452?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/wrong?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_ 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors' own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._

{{% comments %}}

## 6 Comments

{{% comment %}}
{{< commentheader author="Øystein Grøvlen" link="http://oysteing.blogspot.com/" date="July 29, 2019 at 9:43 am" >}}{{< /commentheader >}}
Hi JF,

I think this behavior may be expected if there is a correlation between the columns. For example, that id2 is more likely to be NULL for high (recent?) values of id. The MySQL optimizer does not have any statistics on how columns are correlated. Hence, it is not be able to effectively determine how many rows it needs to read to find the first 20 rows that satisfies the WHERE clause.

Bug#74602 describes a scenario where column values were not correlated. This particular problem was fixed in 5.7.
Bug#78612 seems to be caused by the use of a prefix index, which does not seem to be relevant here.

However, there are probably other bug reports that describes the problem you are facing. In order to address this problem, I think MySQL needs to add statistics on correlation between columns.

Unfortunately, as Domas decribes, the optimizer trace does not contain any information on the cost calculations made when it decides to switch to an index that provides sorting. Hence, it is not straight-forward to verify why this choice was made.
{{% /comment %}}
{{% comment %}}
{{< commentheader author="Jean-François Gagné" link="https://jfg-mysql.blogspot.com/" date="July 29, 2019 at 9:59 am" >}}{{< /commentheader >}}
Hi Øystein, thanks for the details about Bug#74602 and Bug#78612.

> In order to address this problem, I think MySQL needs to add statistics on correlation between columns.

This might be a solution, but I am sure there are others. Tracking correlations might be very complicated. A more simple solution might be to identify plans that are “probabilistic” (like the worse case I show in this post) and to not let queries using those plans run for too long before trying an alternative plan. Also, in the case of plans that might have a very worse case (like the one in this post), maybe running both queries in parallel and killing the other when one completes might be another way to avoid this problem.
{{% /comment %}}
{{% comment %}}
{{< commentheader author="Øystein Grøvlen" link="http://oysteing.blogspot.com/" date="July 30, 2019 at 5:13 am" >}}{{< /commentheader >}}
Hi,

I think it is an interesting idea to let the optimizer have a fallback plan, in case its original estimates is off. The challenge is how to detect in time that the estimates are off. Maybe it would be easier to just switch to the more safe plan if the execution takes longer than the estimate for the safe plan. (Unfortunately, it is not straight-forward to translate query cost to execution time in MySQL.) Another aspect is diagnostics. It must be a way for the user to determine which plan was actually used.

Maybe, the optimizer could be a bit more cautious, and choose a safe plan over a more risky, but potentially quicker plan. In your case, there will be a pretty accurate estimate for the number of rows that need to be read when using the secondary index, while how many rows needs to be read using the primary index depends on how the interesting rows are distributed.
{{% /comment %}}
{{% comment %}}
{{< commentheader author="Jeremy" link="" date="July 31, 2019 at 4:08 pm" >}}{{< /commentheader >}}
While in an ideal world I would like to see this fixed my solution is turn towards the application. It is easier to grow application servers than database servers. After all with solutions like Nginx and such one can easily have a farm of whatever application servers (PHP, Python, Java) and just keep adding more.

I generally keep queries super simple and let the application server(s) do the heavy lifting. For example sort. I almost never ask the database server(s) to sort in my own applications. That is wasting DB cycles on something the application layer can do quite easily and faster. So I am like just dump the raw data DB to app.

Thus keeping in mind: “The fastest query is the query you do NOT run”. I prefer to dump as much heavy lifting onto the application and let the database layer handle as little as possible. As stated I would rather spin up another app server than a DB server.

Of course I understand in some limited cases this isn’t always possible. Still in the vast majority of deployments there is an application layer. Also one could turn toward solutions like ProxySQL to cache bad queries although that doesn’t address the bug.

Finally, as stated, I would like to see this bug fixed. However I still wouldn’t ask the DB to sort in most cases.
{{% /comment %}}
{{% comment %}}
{{< commentheader author="s" link="" date="August 3, 2019 at 4:27 am" >}}{{< /commentheader >}}
also see <a href="https://bugs.mysql.com/bug.php?id=95543">https://bugs.mysql.com/bug.php?id=95543</a> (optimizer prefers index for order by rather than filtering – (70x slower))
{{% /comment %}}
{{% comment %}}
{{< commentheader author="Jean-François Gagné" link="https://jfg-mysql.blogspot.com/" date="July 28, 2021 at 5:48 pm" >}}{{< /commentheader >}}
Another blog post on the same subject (with a patch that was merged in 5.7 and 8.0):
<a href="https://blog.jcole.us/2019/09/30/reconsidering-access-paths-for-index-ordering-a-dangerous-optimization-and-a-fix/">https://blog.jcole.us/2019/09/30/reconsidering-access-paths-for-index-ordering-a-dangerous-optimization-and-a-fix/</a>
{{% /comment %}}
{{% /comments %}}