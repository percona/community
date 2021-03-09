---
title: 'SQL Clause is coming to town'
date: 
draft: true
tags: ['MySQL', 'Open Source Databases', 'Tools']
---

[Olya Kudriavtseva has an ugly christmas sweater](https://twitter.com/roliepoly/status/1342549035211661312):

[![](https://isotopp.github.io/uploads/2020/12/sql-clause.jpg)](https://twitter.com/roliepoly/status/1342549035211661312)

_“He’s making a table. He’s sorting it twice. SELECT \* FROM contacts WHERE behavior = “nice”; SQL Clause is coming town!_ ([buy here](https://www.xonot.com/product/sql-clause-sweatshirt/))

[Katie Bauer observes](https://twitter.com/imightbemary/status/1342676590145105921):

> I mean, except for the fact that sorting something twice is TERRIBLY optimized

So how bad is this? Let’s find out.

Some test data
--------------

We are defining a table `santa`, where we store peoples names (GDPR, [EU Regulation 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) applies!), their behavior (naughty or nice), their age, their location, and their wishlist items.

```
create table santa (
	id integer not null primary key auto_increment,
	name varchar(64) not null,
	loc point srid 0 not null,
	age integer not null,
	behavior enum('naughty', 'nice') not null,
	wish varchar(64) not null
)
```

We are also writing some code to generate data (to evade GDPR, we are using randomly generated test data):

```
for i in range(1, size):
	data = {
	    "id": i,
	    "name": "".join([chr(randint(97, 97 + 26)) for x in range(64)]),
	    "xloc": random()*360-180,
	    "yloc": random()*180-90,
	    "age": randint(1, 100),
	    "behavior": "naughty" if random() > nicelevel else "nice",
	    "wish": "".join([chr(randint(97, 97 + 26)) for x in range(64)]),
	}

	c.execute(sql, data)
	if i%1000 == 0:
	    print(f"{i=}")
	    db.commit()

db.commit()
```

The full data generator is available as [santa.py](https://github.com/isotopp/mysql-dev-examples/blob/master/mysql-santa/santa.py). Note that the data generator there defines more indexes - see below.

In our example we generate one million rows, and assume a general niceness of 0.9 (90% of the children are nice). Also, all of our children have 64 characters long names, a single 64 characters long wish, a random age, and are equidistributed on a perfect sphere.

Our real planet is not a perfect sphere, and also not many people live in the Pacific Ocean. Also, not many children have 64 character names.

Sorting it twice
----------------

How do you even sort the data twice? Now, assuming we sort by name, we can run an increasingly deeply nested subquery:

```
kris@localhost [kris]> select count(*) from santa where behavior = 'nice';
+----------+
| count(*) |
+----------+
|   900216 |
+----------+
1 row in set (0.25 sec)

kris@localhost [kris]> explain select count(*) from santa where behavior = 'nice'G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: santa
   partitions: NULL
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 987876
     filtered: 50.00
        Extra: Using where
1 row in set, 1 warning (0.00 sec)

Note (Code 1003): /* select#1 */ select count(0) AS `count(*)` from `kris`.`santa` where (`kris`.`santa`.`behavior` = 'nice')
```

Out of 1 million children, we have around 900k nice children. No indexes can be used to resolve the query.

Let’s order by name, using a subquery:

```
kris@localhost [kris]> explain 
  -> select t.name from (
  ->   select * from santa where behavior = 'nice'
  -> ) as t order by name;
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra                       |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
|  1 | SIMPLE      | santa | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 987876 |    50.00 | Using where; Using filesort |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)

Note (Code 1003): /* select#1 */ select `kris`.`santa`.`name` AS `name` from `kris`.`santa` where (`kris`.`santa`.`behavior` = 'nice') order by `kris`.`santa`.`name`
```

We can already see that the MySQL 8 optimizer recognizes that this subquery can be merged with the inner query, and does this.

This can be done multiple times, but the optimizer handles this just fine:

```
kris@localhost [kris]> explain 
  -> select s.name from (
  ->   select t.name from (
  ->     select * from santa where behavior = 'nice'
  ->   ) as t order by name
  -> ) as s order by name;
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra                       |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
|  1 | SIMPLE      | santa | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 987876 |    50.00 | Using where; Using filesort |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)

Note (Code 1003): /* select#1 */ select `kris`.`santa`.`name` AS `name` from `kris`.`santa` where (`kris`.`santa`.`behavior` = 'nice') order by `kris`.`santa`.`name`
```

We can see `using filesort`, so while we ask for the query result to be sorted by name twice, it is actually only sorted once.

No sorting at all
-----------------

We can improve on this, using a covering index in appropriate order:

```
kris@localhost [kris]> alter table santa add index behavior_name (behavior, name);
Query OK, 0 rows affected (21.82 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

Having done this, we now see that we lost the `using filesort` altogether:

```
kris@localhost [kris]> explain select s.name from ( select t.name from (select * from santa where behavior = 'nice') as t order by name ) as s order by name;
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+--------------------------+
| id | select_type | table | partitions | type | possible_keys | key           | key_len | ref   | rows   | filtered | Extra                    |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+--------------------------+
|  1 | SIMPLE      | santa | NULL       | ref  | behavior_name | behavior_name | 1       | const | 493938 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+--------------------------+
1 row in set, 1 warning (0.00 sec)

Note (Code 1003): /* select#1 */ select `kris`.`santa`.`name` AS `name` from `kris`.`santa` where (`kris`.`santa`.`behavior` = 'nice') order by `kris`.`santa`.`name`
```

The query is now annotated `using index`, which means that all data we ask for is present in the (covering) index `behavior_name`, and is stored in sort order. That means the data is physically stored and read in sort order and no actual sorting has to be done on read - despite us asking for sorting, twice.

Hidden ‘SELECT \*’ and Index Condition Pushdown
-----------------------------------------------

In the example above, we have been asking for `s.name` and `t.name` only, and because the name is part of the index, `using index` is shown to indicate use of a covering index. We do not actually go to the table to generate the result set, we are using the index only.

Now, if we were to ask for `t.*` in the middle subquery, what will happen?

```
kris@localhost [kris]> explain
  -> select s.name from (
  ->   select * from (
  ->     select * from santa where behavior = 'nice'
  ->   ) as t order by name
  -> ) as s order by name;
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+-----------------------+
| id | select_type | table | partitions | type | possible_keys | key           | key_len | ref   | rows   | filtered | Extra                 |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+-----------------------+
|  1 | SIMPLE      | santa | NULL       | ref  | behavior_name | behavior_name | 1       | const | 493938 |   100.00 | Using index condition |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+--------+----------+-----------------------+
1 row in set, 1 warning (0.00 sec)

Note (Code 1003): /* select#1 */ select `kris`.`santa`.`name` AS `name` from `kris`.`santa` where (`kris`.`santa`.`behavior` = 'nice') order by `kris`.`santa`.`name`
```

In the `Code 1003 Note` we still see the exact same reconstituted query, but as can be seen in the plan annotastions, the internal handling changes - so the optimizer has not been working on this query at all times, but on some intermediary representation.

The ‘using index condition’ annotation points to [Index Condition Pushdown Optimization](https://dev.mysql.com/doc/refman/8.0/en/index-condition-pushdown-optimization.html) being used. In our example, this is not good.

Worse than sorting: Selectivity
-------------------------------

The column we select on is a column with a cardinality of 2: `behavior` can be either `naughty` or `nice`. That means, in an equidistribution, around half of the values are `naughty`, the other half is `nice`.

Data from disk is read in pages of 16 KB. If one row in a page matches, the entire page has to be read from disk. In our example, we have a row length of around 200 Byte, so we end up with 75-80 records per page. Half of them will be `nice`, so with an average of around 40 `nice` records per page, we will very likely have to read all pages from disk anyway.

Using the index will not decrease the amount of data read from disk at all. In fact we will have to read the index pages on top of the data pages, so using an index on a low cardinality column has the potential of making the situation slightly worse than even a full table scan.

Generally speaking, defining an index on a low cardinality column is usually not helpful - if there are 10 or fewer values, benchmark carefully and decide, or just don’t define an index.

In our case, the index is not even equidistributed, but biased to 90% `nice`. We end up with mostly `nice` records, so we can guarantee that all data pages will be read for the SQL `SELECT * FROM santa WHERE behavior = "nice"`, and the index usage will not be contributing in any positive way.

We could try to improve the query by adding conditions to make it more selective. For example, we could ask for people close to our current position, using an RTREE index such as this:

```
kris@localhost [kris]> ALTER TABLE santa ADD SPATIAL INDEX (loc);
...
kris@localhost [kris]> set @rect = 'polygon((10 10, 10 20, 20 20, 20 10, 10 10 ))';
kris@localhost [kris]> select * from santa where mbrcovers(st_geomfromtext(@rect), loc);
...
1535 rows in set (3.53 sec)
```

The `ALTER` defines a spatial index (an RTREE), which can help to speed up coordinate queries.

The `SET` defines a coordinate rectangle around our current position (supposedly 15/15).

We then use the `mbrcovers()` function to find all points `loc` that are covered by the `@rect`. It seems to be somewhat complicated to get MySQL to actually use the index, but I have not been investigating deeply.

If we added an `ORDER BY name` here, we would see `using filesort` again, because data is retrieved in RTREE order, if the index `loc` is used, but we want output in `name` order.

Conclusion
----------

*   The Santa query is inefficient, but likely sorting twice is not the root cause for that.
    *   The optimizer will be able to merge the multiple sorts and be able to deliver the result with one or no sorting, depending on our index construction.
    *   The optimizer is not using the reconstituted query shown in the warning to plan the execution, and that is weird.
*   Selectivity matters, especially for indices on low cardinality columns.
    *   Asking for all `nice` behaviors on a `naughty`/`nice` column is usually not benefitting from index usage.
    *   Additional indexable conditions that improve selectivity can help, a lot.