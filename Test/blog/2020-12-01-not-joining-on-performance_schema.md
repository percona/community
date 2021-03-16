---
title: 'Not JOINing on PERFORMANCE_SCHEMA'
date: Tue, 01 Dec 2020 19:22:46 +0000
draft: false
tags: ['author_kohntopp', 'MySQL', 'Open Source Databases', 'Tools']
authors:
  - koehntopp
images:
  - blog/2020/12/Screenshot-2020-12-01-at-23.21.51.png
---

The tables in `PERFORMANCE_SCHEMA` (`P_S`) are not actually tables. You should not think of them as tables, even if your SQL works on them. You should not JOIN them, and you should not GROUP or ORDER BY them.

Unlocked memory buffers without indexes
---------------------------------------

The stuff in `P_S` has been created with “keep the impact on production small” in mind. That is, from a users point of view, you can think of them as unlocked memory buffers - the values in there change as you look at them, and there are precisely zero stability guarantees. There are also no indexes.

### Unstable comparisons

When sorting a table for a GROUP BY or ORDER BY, it may be necessary to compare the value of one row to other rows multiple times in order to determine where the row goes. The value compared to other rows can change while this happens, and will change more often the more load the server has. The end result is unstable. Also, as the table you sort may be larger on a server under load, the row may need more comparisons, making this even more likely to happen. The table you look at may produce correct results on your stable, underutilized test systems, but the monitoring you base on this will fail on a loaded test system. Do not use GROUP BY or ORDER BY on `P_S` tables.

### No indexes, meaning slow joins on loaded systems

When JOINing a `P_S` table against other tables, the join is done without indexes. There are no indexes defined in `P_S`, and if there were they would make updates to values in `P_S` more expensive, which is against the initial design tenet - “keep the impact on production small”. In practice that means your join against the processlist or session variables tables in `P_S` do little harm in test, but will fail in production environments with many connections. You will be losing monitoring the moment you need it most - under load, in critital situations. Do not JOIN `P_S` tables to anything.

How to monitor
--------------

About the only type of query you can successfully run on `P_S` is a single table `SELECT * FROM P_S.table`, maybe with a simple `WHERE` clause. That is, you can download and materialize data from a single `P_S` table at a time, unsorted, unaggregated. Connection to other tables, aggregation and sorting have to be done on tables that are not `P_S` tables. There are multiple ways to do this.

### Subqueries, without optimization

It used to be that the MySQL optimizer did not resolve simple subqueries properly. So
```
mysql> select <complicated stuff> from
    -> ( select * from performance_schema.sometable ) as t
    -> order by <something>
```
used to work. The subquery `t` would materialize the `P_S` table as whatever your version of MYSQL used for implicit temporary tables, and the rest of the query resolution would happen on the materialized temptable. This is a snapshot, and would be stable. It still would not have indexes. And it still would not add up to 100%, of course. That is, queries like Dennis Kaarsemakers “How loaded is the SQL_THREAD” Replication Load analysis never came out at 100%, because the various values changed while the temporary table would be materialized, so you do not get a consistent snapshot (and by construction, this kind of consistency is impossible in `P_S`). Anyway, with older versions of MySQL, this results in the query plan we want. Since MySQL 5.7, this does no longer work:
```
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.22    |
+-----------+
1 row in set (0.00 sec)

mysql> explain select * from ( select * from processlist ) as t;
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table       | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+
|  1 | SIMPLE      | processlist | NULL       | ALL  | NULL          | NULL | NULL    | NULL |  256 |   100.00 | NULL  |
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)
```
Newer MySQL (5.7 and above) will apply the `derived_merge` optimization and fold the subquery into the outer query, resulting in a rewritten single query that again is executed on `P_S` directly. You either need to `SET SESSION optimizer_switch = "derived_merge=off";` or provide an advanced [MySQL 8 optimizer hint](https://dev.mysql.com/doc/refman/8.0/en/optimizer-hints.html#optimizer-hints-table-level) to prevent the optimizer from ruining your cunning plan:
```
mysql> explain select /*+ NO_MERGE(t) */ * from ( select * from processlist ) as t;
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table       | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+
|  1 | PRIMARY     | <derived2>  | NULL       | ALL  | NULL          | NULL | NULL    | NULL |  256 |   100.00 | NULL  |
|  2 | DERIVED     | processlist | NULL       | ALL  | NULL          | NULL | NULL    | NULL |  256 |   100.00 | NULL  |
+----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------+

```
Here we get the `DERIVED` table as a non-`P_S` temptable, and then run our “advanced” SQL on that as `PRIMARY` on it.

### In the client

The alternative is, of course, to completely download the tables in question into client side hashes, and then perform the required operations on them on the client side, in memory. The important thing here is to limit the amount of memory spent - do not download unconstrained result sets into your client monitoring program. Then use a linearly scaling join method to construct the connections between the tables. Effectively, load data into hashes, and then program a client side hash join. This is additive (n + m) instead of quadratic (n * m), so you can survive this. This is the recommended method.

Who is doing it wrong?
----------------------

Getting monitoring queries that use `P_S` wrongly is common - it understands SQL, it handles `SHOW CREATE TABLE`, so it is treated as a table and exposed to full SQL all the time. And on idle test boxen, it even looks like it works. At work, see this in our own code (still using a deprecated Diamond collector) and in SolarWinds nee Vividcortex. SolarWinds kindly highlights itself:
```sql
-- Most time consuming query - Coming from solar winds monitoring itself ¯_(ツ)_/¯
select `ifnull` (`s`.`sql_text` , ?) , `ifnull` (`t`.`processlist_user` , ?) , `ifnull` (`t`.`processlist_host` , ?) 
  from `performance_schema`.`events_statements_history` `s` 
  left join `performance_schema`.`threads` `t` 
    using (`thread_id`) 
  where `s`.`thread_id`=? and `s`.`event_id`=?
 
-- Coming from the "table ownership write identifier".
select count (*) as `cnt` , `digest_text` , `current_schema` , `processlist_user` as system_user 
  from `performance_schema`.`events_statements_history` `esh` 
  inner join `performance_schema`.`threads` `t` 
    on `t`.`thread_id`=`esh`.`thread_id` 
  where `event_name` in (...) 
    and `current_schema` in (...) 
  group by `digest_text` , `current_schema` , `processlist_user`
 
-- Coming from diamond collector
select `t`.`processlist_user` , `sbt`.`variable_value` , count (*)
  from `performance_schema`.`status_by_thread` `sbt` 
  join `performance_schema`.`threads` `t`
    using (`thread_id`) 
  where `sbt`.`variable_name`=? 
    and `t`.`processlist_user` is not null
group by `t`.`processlist_user` , `variable_value`
```
Many of the above examples fail in multiple ways: Using JOIN for bad scalability (this is how we spotted them), by also using unstable sorting. We also see ORDER BY statements in the [Telegraf MySQL plugin](https://github.com/influxdata/telegraf/blob/master/plugins/inputs/mysql/mysql.go#L376) in one place. It uses LIMIT, but if the ORDER BY does not work (ie does not actually sort), you cut off randomly.

Is PERFORMANCE_SCHEMA broken?
------------------------------

Clearly, it is not. Just badly misunderstood. The alternative is `INFORMATION_SCHEMA`, which often locks, and that can be actually deadly: Just `select * from INFORMATION_SCHEMA.INNODB_BUFFER_PAGE` on a server with a few hundreds of GB of buffer pool, humming at 10k QPS. The query will freeze the server completely for the runtime of the query – which with a large buffer pool size can be substantial. I’d rather have this in `P_S` and then deal with the vagaries of the data changing while I read it than lose an important production server. 

_First published on [https://blog.koehntopp.info/](https://blog.koehntopp.info/) and syndicated here with permission of the author._