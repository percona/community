---
title: 'MySQL: Tracing a single query with PERFORMANCE_SCHEMA'
description: "My task is to collect performance data about a single query, using `PERFORMANCE_SCHEMA` (P_S for short) in MySQL, to ship it elsewhere for integration with other data."
date: "2022-10-18"
draft: false
tags: ['MySQL']
authors:
  - koehntopp
images:
  - blog/2022/10/mysql-tracing-a-single-query.jpg
---

My task is to collect performance data about a single query, using `PERFORMANCE_SCHEMA` (P_S for short) in MySQL, to ship it elsewhere for integration with other data.

In a grander scheme of things, I will need to define what performance data from a query I am actually interested in.
I will also need to find a way to attribute the query (as seen on the server) to a point in the codebase of the client, which is not always easy when an ORM or other SQL generator is being used.
And finally I will need to find a way to view the query execution in the context of the client code execution, because the data access is only a part of the system performance.

But this is about query execution in the server, and the instrumentation available to me in MySQL 8, at least to get things started.
So we take the tour of performance schema, and then run one example query (a simple join) and see what we can find out about this query.

_First published on [https://blog.koehntopp.info/](https://blog.koehntopp.info/2021/09/15/mysql-tracing-a-single-query-with-performanceschema.html) and syndicated here with permission of the [author](/authors/koehntopp/)._

# Performance Schema, the 10.000 m view

[The Manual](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html) has a major chapter that covers P_S in details.
The original idea of P_S is to have a bunch of preallocated memory areas without locks, presented to the database itself as tables.

P_S is unusual in the way that P_S "tables" are never locked while you work with them.
That means the values in a "table" can change while you read them.
That is important - if you for example calculate percentages, they may not add up to 100%.
If you `ORDER BY`, the sort may or may not be stable.

These are good properties: P_S will not freeze the server, and you won't kill the server by working with P_S tables.

It is a good idea to make a copy of P_S tables while you work with them, by turning off subquery merging with `select /*+ NO_MERGE(t) */ `, and then materializing P_S tables in subqueries.

Originally, P_S also had no secondary indexes, so joining P_S tables against other P_S tables did not work efficiently.
That was probably a good idea, because joining against a table that is changing while you execute the join is probably generating random results anyway.
But because it is so common, and because MySQL itself does this now internally in `sys.*`, secondary indexes to join efficiently now exist.
That does not make the joins more correct, but at least you get the result faster.

I wrote about all this [in an earlier article](https://blog.koehntopp.info/2020/12/01/not-joining-on-performance-schema.html).

## Instruments, Objects, Actors, Threads and Consumers

The data P_S collects is centered around three major things:

- Time consumed. In database servers, that is mostly wait time - waiting on I/O or locks.
- Data transferred. In database servers, that is mostly pages read or written. In a way, this related to I/O wait.
- Memory used. In database servers, that is buffers allocated - how large, and how often, and peak usage.

P_S collects this in the form of "events" (and takes care to note that P_S events are not binlog events or other any events).
The collection points are in the database server code, which is instrumented, so the collectors are *instruments*.

The thing that the server code works on may be of a certain kind, for example a table or another *object* in the server, but have a variable identity (that would be different tables, with different names).
Instruments can be filtered by using object names.

The activity done in the server is done on behalf of a database user, in the form of *user@host* or, new in MySQL 8, using roles.
The entity on which behalf the server is working on is called the *actor*.

The activity done in the server is also done in the context of a *thread*, some of which are background threads, while the majority in a busy server are usually connection threads.

And finally, the data collected is put into the in-memory tables of P_S.
These come in various groups, and are called *consumers*.


<img src="https://blog.koehntopp.info/uploads/2021/09/performance_schema_filtering.png" />

*Data is collected from objects using instruments. Instruments can be turned on and off. Their collected data is then filtered by Objects, Actors and Threads, and finally dropped into consumers. Many consumers are aggregates, some collect information specific to one query execution.*

For each of these things there is a `setup_...` table that controls how event data is collected by the instrumentation, filtered and the consumed in result tables.
In parallel, object identities are collected in `..._instances` tables, which are needed to resolve object identities.

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > show tables like "setup_%";
+----------------------------------------+
| Tables_in_performance_schema (setup_%) |
+----------------------------------------+
| setup_actors                           |
| setup_consumers                        |
| setup_instruments                      |
| setup_objects                          |
| setup_threads                          |
+----------------------------------------+
5 rows in set (0.00 sec)

mysql [localhost:8025] {msandbox} (performance_schema) > show tables like "%_instances";
+--------------------------------------------+
| Tables_in_performance_schema (%_instances) |
+--------------------------------------------+
| cond_instances                             |
| file_instances                             |
| mutex_instances                            |
| prepared_statements_instances              |
| rwlock_instances                           |
| socket_instances                           |
+--------------------------------------------+
6 rows in set (0.00 sec)

mysql [localhost:8025] {msandbox} (performance_schema) > select * from socket_instances;
+----------------------------------------+-----------------------+-----------+-----------+-----------+-------+--------+
| EVENT_NAME                             | OBJECT_INSTANCE_BEGIN | THREAD_ID | SOCKET_ID | IP        | PORT  | STATE  |
+----------------------------------------+-----------------------+-----------+-----------+-----------+-------+--------+
| wait/io/socket/mysqlx/tcpip_socket     |             106328376 |        44 |        21 | ::        | 18025 | ACTIVE |
| wait/io/socket/mysqlx/unix_socket      |             106328688 |        44 |        22 |           |     0 | ACTIVE |
| wait/io/socket/sql/server_tcpip_socket |             106329000 |         1 |        26 | 127.0.0.1 |  8025 | ACTIVE |
| wait/io/socket/sql/server_unix_socket  |             106329312 |         1 |        28 |           |     0 | ACTIVE |
| wait/io/socket/sql/client_connection   |             106330560 |        50 |        41 |           |     0 | ACTIVE |
+----------------------------------------+-----------------------+-----------+-----------+-----------+-------+--------+
5 rows in set (0.00 sec)
```

## Current, History and History Long Tables vs. Summaries

P_S collects data in a lot of summary table, which should not interest us that much here.
Our task is to look at the performance data of a single, individual query to better understand what happened when it ran.

These unaggregated tables are `events_transactions`, `events_statements`, `events_stages` and `events_waits`. 
For each of them, we have  `_current`, `_history` or `_history_long` tables.

The `_current` tables contain one entry for the currently running thread.
The `_history` tables contain a configurable number of entries for each thread, for example 10 per thread.
And the `_history_long` tables contain a configurable number of entries, shared across all threads, for example 10.000 in total.
As the server continues to execute statements and produce events, old entries are discarded and new entries are added, automatically.
Additionally, each query execution is aggregated along several dimensions in summary tables.
Summary tables state these dimension(s) using `by_<dimensionname>`, for example `_by_user_by_eventname` or similar.

In current MySQL, P_S is enabled by default.
But not all instruments and consumers are enabled, because some instrumentation slows query execution down, and some consumers can use a lot of memory.
To be fast and safe, all memory is statically allocated at config change so the memory resource usage of P_S is constant and no allocations are made during execution.

We can enable all instrumentation completely with this SQL:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > UPDATE 
 -> performance_schema.setup_instruments SET ENABLED = 'YES', TIMED = 'YES';
Query OK, 494 rows affected (0.00 sec)
Rows matched: 1216  Changed: 494  Warnings: 0

mysql [localhost:8025] {msandbox} (performance_schema) > UPDATE 
 -> performance_schema.setup_consumers SET ENABLED = 'YES';
Query OK, 0 rows affected (0.00 sec)
Rows matched: 15  Changed: 0  Warnings: 0
```

When we look at one of these tables, for example `events_statements_current`, we see a structure like this:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > show create table events_statements_current\G
*************************** 1. row ***************************
       Table: events_statements_current
Create Table: CREATE TABLE `events_statements_current` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
...
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `NESTING_EVENT_LEVEL` int DEFAULT NULL,
  `STATEMENT_ID` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

That is, events are tagged with a `THREAD_ID` (which is not a CONNECTION_ID() as seen in processlist), an `EVENT_ID/END_EVENT_ID` bracket, various source and timer values and for further dissection, a `NESTING_EVENT_ID` and `_TYPE`.

We can translate processlist ids into thread ids using the `P_S.THREADS` table, and then use this to limit our view on the `events_statements_current` table:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select thread_id from threads 
 -> where processlist_id = connection_id();
+-----------+
| thread_id |
+-----------+
|        50 |
+-----------+
1 row in set (0.00 sec)

mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> thread_id, 
 -> event_id, 
 -> event_name, 
 -> source, 
 -> sys.format_time(timer_wait), 
 -> sql_text 
 -> from events_statements_current 
 -> where thread_id = 50\G
*************************** 1. row ***************************
                  thread_id: 50
                   event_id: 88463
                 event_name: statement/sql/select
                     source: init_net_server_extension.cc:94
sys.format_time(timer_wait): 341.04 us
                   sql_text: select thread_id, event_id, event_name, source, sys.format_time(timer_wait), sql_text from events_statements_current where thread_id = 50
1 row in set (0.00 sec)
```

So running this query took 341 Microseconds, or 0.341 ms.
And sources are named after their location in the server sourcecode, [filename and line number](https://github.com/mysql/mysql-server/blob/8.0/sql/conn_handler/init_net_server_extension.cc#L94-L96).

Events exist in a hierarchy: wait events nest within stage events, which nest within statement events, which nest within transaction events.
Some nested events refer to their own type, for example, statement events can point to other statement events they are nested in.
Other events refer to their enclosing context in the hierarchy.
Nesting Event ID, Type and Level make this clear.

## Instrument names

The manual explains [Instrument Names](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-instrument-naming.html).

They have path-like names that group instruments hierarchically, for example `wait/io/file/innodb/innodb_data_file`. 
This is a `wait` event, `io` related, specifically `file` I/O, more specific `innodb` and even more specific `innodb_data_file`.
Looking at other fields in the `events_waits_history` table, we would see the file name as part of the `OBJECT_SCHEMA.OBJECT_NAME` designator for this event.
That means, we can see how long we waited for I/O coming from this specific file or going to the file.

Further up in the nesting we would see, at the statement level, the actual `SQL_TEXT`, and also the number of rows scanned.
That means we can get a rough estimate why this particular statement instance was slow - for example, the plan was good, the number of rows was low, but we see a lot of actual file IO waits, so probably the buffer pool was cold.

The manual page above discusses the instrument names at length, and it is important to get an overview of what exists and what is measured.
Specifically, for statement level entries the instruments vary during query execution and become more detailed, as they reflect the progress in understanding of the server about the nature of the statement as it is executed.

# An example run

In a freshly restarted idle server, we log in to a shell and `use world` for the world sample database.
This is a tiny database, but because the server has been just restarted, nothing of it is cached.
We run a simple query:

```sql
mysql [localhost:8025] {msandbox} (world) > select 
 -> co.continent, 
 -> co.name as country, 
 -> co.population as copop, 
 -> ci.name as capital, 
 -> ci.population as cipop 
 -> from country as co join city as ci
  ->   on co.capital = ci.id 
  -> where continent = 'Europe';
+-----------+-------------------------------+-----------+------------------------------------+---------+
| continent | country                       | copop     | capital                            | cipop   |
+-----------+-------------------------------+-----------+------------------------------------+---------+
| Europe    | Albania                       |   3401200 | Tirana                             |  270000 |
...
| Europe    | Yugoslavia                    |  10640000 | Beograd                            | 1204000 |
+-----------+-------------------------------+-----------+------------------------------------+---------+
46 rows in set (0.00 sec)
```

Now let's check what we can find out, using a second session:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select * from threads 
 -> where processlist_db = 'world'\G
*************************** 1. row ***************************
          THREAD_ID: 48
               NAME: thread/sql/one_connection
               TYPE: FOREGROUND
     PROCESSLIST_ID: 9
   PROCESSLIST_USER: msandbox
   PROCESSLIST_HOST: localhost
     PROCESSLIST_DB: world
PROCESSLIST_COMMAND: Sleep
   PROCESSLIST_TIME: 4
  PROCESSLIST_STATE: NULL
   PROCESSLIST_INFO: NULL
   PARENT_THREAD_ID: 1
               ROLE: NULL
       INSTRUMENTED: YES
            HISTORY: YES
    CONNECTION_TYPE: Socket
       THREAD_OS_ID: 346752
     RESOURCE_GROUP: USR_default
1 row in set (0.00 sec)
```

In our case we are only interested in the fact that our `thread/sql/one_connection` in the processlist is shown as connection `9`, but internally has a thread_id of `48`.
The Linux Operating System PID is `346752`.

We can use this to check `events_transactions_wait`, and find

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> thread_id, 
 -> event_id, 
 -> state, 
 -> source, 
 -> sys.format_time(timer_wait) as timer, 
 -> nesting_event_id, 
 -> nesting_event_type 
 - from events_transactions_history 
 -> where thread_id = 48;
+-----------+----------+-----------+-----------------+-----------+------------------+--------------------+
| thread_id | event_id | state     | source          | timer     | nesting_event_id | nesting_event_type |
+-----------+----------+-----------+-----------------+-----------+------------------+--------------------+
|        48 |      179 | COMMITTED | handler.cc:1328 | 496.05 us |               85 | STATEMENT          |
|        48 |      401 | COMMITTED | handler.cc:1328 | 559.99 us |              278 | STATEMENT          |
|        48 |     5606 | COMMITTED | handler.cc:1328 | 3.03 ms   |             5574 | STATEMENT          |
+-----------+----------+-----------+-----------------+-----------+------------------+--------------------+
3 rows in set (0.00 sec)
```

Why are there three statement events? We can check:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> thread_id, 
 -> event_id, 
 -> sql_text 
 -> from events_statements_history 
 -> where thread_id = 48 and event_id in (85, 278, 5574);
+-----------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| thread_id | event_id | sql_text                                                                                                                                                                                        |
+-----------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        48 |       85 | show databases                                                                                                                                                                                  |
|        48 |      278 | show tables                                                                                                                                                                                     |
|        48 |     5574 | select co.continent, co.name as country, co.population as copop, ci.name as capital, ci.population as cipop from country as co join city as ci on co.capital = ci.id where continent = 'Europe' |
+-----------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

The mysql command line client is running from the sandbox with `/home/kris/opt/mysql/8.0.25/bin/mysql --defaults-file=/home/kris/sandboxes/msb_8_0_25/my.sandbox.cnf world`.
Autocompletion for names is not disabled.
So on client startup, the client invisibly runs `show databases` to learn the names of all databases for autocompletion.
It then enters the `world` database as requested and runs `show tables` to learn the names of all tables in the `world` database.

Only then we come to the prompt and can paste our query.

We are only interested in `thread_id = 48 AND event_id = 5574`, our query.

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select * 
 -> from events_statements_history 
 -> where thread_id = 48 AND event_id = 5574\G
*************************** 1. row ***************************
              THREAD_ID: 48
               EVENT_ID: 5574
           END_EVENT_ID: 6624
             EVENT_NAME: statement/sql/select
                 SOURCE: init_net_server_extension.cc:94
            TIMER_START: 61628458852000
              TIMER_END: 61631769329000
             TIMER_WAIT: 3310477000
              LOCK_TIME: 224000000
               SQL_TEXT: select co.continent, co.name as country, co.population as copop, ci.name as capital, ci.population as cipop from country as co join city as ci on co.capital = ci.id where continent = 'Europe'
                 DIGEST: 409c336982f0d3d45c4b29da77fe83aed12c6043e8ce9771c11ec82ff347e647
            DIGEST_TEXT: SELECT `co` . `continent` , `co` . `name` AS `country` , `co` . `population` AS `copop` , `ci` . `name` AS `capital` , `ci` . `population` AS `cipop` FROM `country` AS `co` JOIN `city` AS `ci` ON `co` . `capital` = `ci` . `id` WHERE `continent` = ?
         CURRENT_SCHEMA: world
            OBJECT_TYPE: NULL
          OBJECT_SCHEMA: NULL
            OBJECT_NAME: NULL
  OBJECT_INSTANCE_BEGIN: NULL
            MYSQL_ERRNO: 0
      RETURNED_SQLSTATE: NULL
           MESSAGE_TEXT: NULL
                 ERRORS: 0
               WARNINGS: 0
          ROWS_AFFECTED: 0
              ROWS_SENT: 46
          ROWS_EXAMINED: 92
CREATED_TMP_DISK_TABLES: 0
     CREATED_TMP_TABLES: 0
       SELECT_FULL_JOIN: 0
 SELECT_FULL_RANGE_JOIN: 0
           SELECT_RANGE: 0
     SELECT_RANGE_CHECK: 0
            SELECT_SCAN: 0
      SORT_MERGE_PASSES: 0
             SORT_RANGE: 0
              SORT_ROWS: 0
              SORT_SCAN: 0
          NO_INDEX_USED: 0
     NO_GOOD_INDEX_USED: 0
       NESTING_EVENT_ID: NULL
     NESTING_EVENT_TYPE: NULL
    NESTING_EVENT_LEVEL: 0
           STATEMENT_ID: 125
1 row in set (0.00 sec)
```
The statement is `statement/sql/select`.
It took 3310477000 picoseconds (3.31ms) to run.
The `sql_text` is the full text of the statement (up to a cutoff point, in order to manage memory consumption).
The parsed statement is called `digest_text` - identifiers are quoted, whitespace is normalized, actual constants are replaced with placeholders, and (not shown here) variable length `WHERE ... IN (...)` clauses are shortened with ellipses.
This normalized digest is then hashed and produces an identifier for this group of identically formed statements, the `digest`.
We learn about the number of rows looked at, `92` and sent, `46`.
No special flags indicating specific execution modes were set.

We can use the `event_id` to look even deeper:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> thread_id, 
 -> event_id, 
 -> event_name, 
 -> source, 
 -> sys.format_time(timer_wait) as timer 
 -> from events_stages_history 
 -> where thread_id = 48 
 ->   and nesting_event_id = 5574 
 -> order by event_id;
+-----------+----------+--------------------------------------+----------------------+-----------+
| thread_id | event_id | event_name                           | source               | timer     |
+-----------+----------+--------------------------------------+----------------------+-----------+
|        48 |     5610 | stage/sql/optimizing                 | sql_optimizer.cc:270 | 15.88 us  |
|        48 |     5611 | stage/sql/statistics                 | sql_optimizer.cc:534 | 703.58 us | <- !!
|        48 |     5710 | stage/sql/preparing                  | sql_optimizer.cc:618 | 31.93 us  |
|        48 |     5712 | stage/sql/executing                  | sql_union.cc:1126    | 2.26 ms   | <- !!
|        48 |     6593 | stage/sql/end                        | sql_select.cc:586    | 1.86 us   |
|        48 |     6594 | stage/sql/query end                  | sql_parse.cc:4542    | 1.93 us   |
|        48 |     6596 | stage/sql/waiting for handler commit | handler.cc:1594      | 9.05 us   |
|        48 |     6600 | stage/sql/closing tables             | sql_parse.cc:4593    | 14.02 us  |
|        48 |     6621 | stage/sql/freeing items              | sql_parse.cc:5042    | 29.4 us   |
|        48 |     6623 | stage/sql/cleaning up                | sql_parse.cc:2252    | 1.17 us   |
+-----------+----------+--------------------------------------+----------------------+-----------+
10 rows in set (0.00 sec)
```

These are the various execution stages of our statement - we select by `thread_id` and with the `event_id` of the statement, `5574` as a `nesting_id`, ordered by `event_id`.
Time was consumed by the `stage/sql/statistics` phase, looking up table stats for a good execution plan, and then by the actual query execution in `stage/sql/executing`.
The former took 0.7ms (703.58us), the latter 2.26ms.

We are interested in what took so long, specifically, so we look into waits for event_ids 5611 and 5712 - finding nothing, and also nothing particularly time-consuming:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select
 -> thread_id, 
 -> event_id, 
 -> event_name, 
 -> sys.format_time(timer_wait) as timer, 
 -> nesting_event_type, 
 -> nesting_event_id, 
 -> operation 
 -> from events_waits_history 
 -> where thread_id = 48
  -> order by event_id;
+-----------+----------+------------------------------------------+-----------+--------------------+------------------+-----------+
| thread_id | event_id | event_name                               | timer     | nesting_event_type | nesting_event_id | operation |
+-----------+----------+------------------------------------------+-----------+--------------------+------------------+-----------+
|        48 |     6614 | wait/synch/mutex/innodb/trx_mutex        | 56.26 ns  | STAGE              |             6600 | lock      |
|        48 |     6615 | wait/synch/mutex/innodb/trx_mutex        | 48.64 ns  | STAGE              |             6600 | lock      |
|        48 |     6616 | wait/synch/mutex/innodb/trx_mutex        | 50.4 ns   | STAGE              |             6600 | lock      |
|        48 |     6617 | wait/synch/mutex/innodb/trx_mutex        | 46.88 ns  | STAGE              |             6600 | lock      |
|        48 |     6618 | wait/synch/mutex/innodb/trx_mutex        | 43.36 ns  | STAGE              |             6600 | lock      |
|        48 |     6619 | wait/synch/mutex/innodb/trx_mutex        | 45.12 ns  | STAGE              |             6600 | lock      |
|        48 |     6620 | wait/synch/mutex/sql/LOCK_table_cache    | 66.8 ns   | STAGE              |             6600 | lock      |
|        48 |     6622 | wait/io/socket/sql/client_connection     | 18.91 us  | STAGE              |             6621 | send      |
|        48 |     6624 | wait/synch/mutex/sql/THD::LOCK_thd_query | 124.23 ns | STAGE              |             6623 | lock      |
|        48 |     6626 | wait/io/socket/sql/client_connection     | NULL      | WAIT               |             6625 | recv      |
+-----------+----------+------------------------------------------+-----------+--------------------+------------------+-----------+
10 rows in set (0.00 sec)
```

We can see I/O in a global summary, and the timings make sense in the context of the experiment:

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select
 -> object_type, 
 -> object_schema, 
 -> object_name, 
 -> count_star, 
 -> sys.format_time(max_timer_read) as `read`, 
 -> sys.format_time(max_timer_write) as `write`, 
 -> sys.format_time(max_timer_fetch) as `fetch`
  -> from table_io_waits_summary_by_table 
  -> where object_schema = 'world'\G
*************************** 1. row ***************************
  object_type: TABLE
object_schema: world
  object_name: city
   count_star: 46
         read: 569.17 us
        write: 0 ps
        fetch: 569.17 us
*************************** 2. row ***************************
  object_type: TABLE
object_schema: world
  object_name: country
   count_star: 47
         read: 703.4 us
        write: 0 ps
        fetch: 703.4 us
...
```

But why are the I/O times not visible to us?
That's a bit unclear.
My theory was that the reads happen asynchronously by some background thread.
But a quick query shows no time spend on reader threads.

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> t.thread_id, 
 -> t.name, 
 -> t.type 
 -> from threads as t join events_waits_summary_by_thread_by_event_name as e 
 ->    on t.thread_id = e.thread_id  
 -> where e.max_timer_wait > 0 
 ->    and e.event_name = 'wait/io/file/innodb/innodb_data_file';
+-----------+---------------------------------------------+------------+
| thread_id | name                                        | type       |
+-----------+---------------------------------------------+------------+
|         1 | thread/sql/main                             | BACKGROUND |
|         9 | thread/innodb/io_write_thread               | BACKGROUND |
|        10 | thread/innodb/io_write_thread               | BACKGROUND |
|        11 | thread/innodb/io_write_thread               | BACKGROUND |
|        12 | thread/innodb/io_write_thread               | BACKGROUND |
|        13 | thread/innodb/page_flush_coordinator_thread | BACKGROUND |
|        33 | thread/innodb/clone_gtid_thread             | BACKGROUND |
|        47 | thread/sql/one_connection                   | FOREGROUND |
|        48 | thread/sql/one_connection                   | FOREGROUND |
+-----------+---------------------------------------------+------------+
9 rows in set (0.00 sec)
```

We seem to be unable to attribute time spent loading data from disk to a specific thread, and we seem to be unable to account for the runtime of certain stages by looking at waits.
That's unexpected.

# Memory only as summary

Diverse `memory_%` tables exist to track memory usage in the server.
All of these tables are summary tables, there are no memory events tables that could trace memory usage per query.
That might be okay.

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > show tables like '%memory%';
+-----------------------------------------+
| Tables_in_performance_schema (%memory%) |
+-----------------------------------------+
| memory_summary_by_account_by_event_name |
| memory_summary_by_host_by_event_name    |
| memory_summary_by_thread_by_event_name  |
| memory_summary_by_user_by_event_name    |
| memory_summary_global_by_event_name     |
+-----------------------------------------+
5 rows in set (0.00 sec)
```

We can do interesting things with stuff such as `memory_summary_by_thread_by_event_name`, at least on our mostly idle server.

```sql
mysql [localhost:8025] {msandbox} (performance_schema) > select 
 -> thread_id, 
 -> event_name, 
 -> count_alloc, 
 -> sum_number_of_bytes_alloc, 
 -> high_number_of_bytes_used 
 -> from memory_summary_by_thread_by_event_name 
 -> where thread_id = 48 
 ->   and HIGH_NUMBER_OF_BYTES_USED > 0 
 -> order by HIGH_NUMBER_OF_BYTES_USED desc limit 5;
+-----------+-------------------------------+-------------+---------------------------+---------------------------+
| thread_id | event_name                    | count_alloc | sum_number_of_bytes_alloc | high_number_of_bytes_used |
+-----------+-------------------------------+-------------+---------------------------+---------------------------+
|        48 | memory/sql/THD::main_mem_root |          22 |                   1181008 |                    613544 |
|        48 | memory/innodb/memory          |         226 |                   1059368 |                    250032 |
|        48 | memory/sql/dd::objects        |         205 |                     47432 |                     44648 |
|        48 | memory/innodb/ha_innodb       |          26 |                     35784 |                     35784 |
|        48 | memory/innodb/fil0fil         |           2 |                     65600 |                     32800 |
+-----------+-------------------------------+-------------+---------------------------+---------------------------+
5 rows in set (0.00 sec)
```

# No EXPLAIN

Another thing that would be useful to collect from P_S is the actual execution plan of a query.
But while we can explain a lot of statements by running `EXPLAIN <stmt>`, and while we can `EXPLAIN FOR CONNECT ...`, the former is not the recorded execution plan, and the latter only works while the query is running.
It's the actual execution plan while the query executes, but it is not recorded.

# Summary

A lot of information about query execution can be gathered from P_S.
The query execution can be broken down in statements, stages and waits.
Specifically, statements collect a lot of interesting quality flags.
Stages can collect percentages of completion for long-running queries and give a general feel about where in the query execution time is spent.
Waits should be able to attribute time to individual operations in the database server, but specifically for file I/O this seems to be more complicated, and I have not been able to solve it.

We can see waits for I/O summary tables, and we can see a lot of other statistical information in other summary tables.
We can also use additional tables not covered here for debugging (for example `DATA_LOCKS` for locking behavior).

Memory instrumentation is interesting, but at this stage it is unclear to me if it is sufficient.

It seems to be really hard to record execution plans together with statements.

More experimentation with more complicated queries is necessary to see if it is possible to see things like sorting, temp files and similar operations, and attribute time to these operations.

The number of queries on P_S necessary to extract information about a single query is staggering, a 10:1 ratio.
At least filters exist and are on by default, so that I do not have to hear my monitoring noise in my monitoring.
That is good.

I could really use a single large JSON blob containing the entire package with performance data for a query, at once - one query to trace one query.
That is, the information from transaction, statement, stages, waits, the execution plan and the memory consumption for a given transaction or statement, in one go.

_First published on [https://blog.koehntopp.info/](https://blog.koehntopp.info/2021/09/15/mysql-tracing-a-single-query-with-performanceschema.html) and syndicated here with permission of the [author](/authors/koehntopp/)._
