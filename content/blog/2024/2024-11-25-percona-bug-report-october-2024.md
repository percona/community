---
title: "Percona Bug Report: October 2024"
date: "2024-11-25T00:00:00+00:00"
tags: ['Percona', 'opensource', 'PMM', 'Kubernetes', 'MySQL', 'PostgreSQL']
authors:
  - aaditya_dubey
images:
  - blog/2024/11/BugReportOctober2024.jpg
---

At Percona, we operate on the premise that full transparency makes a product better. We strive to build the best open-source database products, but also to help you manage any issues that arise in any of the databases that we support. And, in true open-source form, report back on any issues or bugs you might encounter along the way.

We constantly update our [bug reports](https://jira.percona.com/) and monitor [other boards](https://bugs.mysql.com/) to ensure we have the latest information, but we wanted to make it a little easier for you to keep track of the most critical ones. This post is a central place to get information on the most noteworthy open and recently resolved bugs.

In this edition of our bug report, we have the following list of bugs,

## Percona Server/MySQL Bugs


[PS-8057](https://perconadev.atlassian.net/browse/PS-8057): When max_slowlog_size is set to above 4096, then it  gets reset to 1073741824. This overwrites the slow log file path with a different file name, which becomes like node_name.log.000001. Due to this issue, your path defined at slow_query_log_file won`t be useful. This issue has started happening since MySQL Version 8.0.32.

E.g.:

MySQL 8.0.36 is running with the following set of configurations:

```
slow_query_log = ON
slow_query_log_file = /home/user/sandboxes/msb_ps8_0_36/data/slow
long_query_time = 10
max_slowlog_files = 2
max_slowlog_size = 510000000
```

Check the log_file path:
```
mysql [localhost:8036] {msandbox} ((none)) > show global variables like "%slow_query_log_file%";
+---------------------+------------------------------------------------------------+
| Variable_name       | Value                                                      |
+---------------------+------------------------------------------------------------+
| slow_query_log_file | /home/adi/sandboxes/msb_ps8_0_36/data/localhost.log.000001 |
+---------------------+------------------------------------------------------------+
1 row in set (0.00 sec)
```
Interestingly, you will see that this file,/home/user/sandboxes/msb_ps8_0_36/data/localhost.log, 000001, was not even created.

```
user@localhost:~/sandboxes/msb_ps8_0_36/data$ ll | grep slow
-rw-r----- 1 adi adi  355518891 Aug 13 16:45 localhost-slow.log
-rw-r----- 1 adi adi 1079653421 Jul 30 18:13 localhost-slow.log.old
-rw-r----- 1 adi adi        255 Aug 13 16:48 slow
-rw-r----- 1 adi adi        255 Aug 13 16:45 slow.000001
```

After removing max_slowlog_size = 510000000

```
mysql [localhost:8036] {msandbox} ((none)) >  show global variables like "%slow_query_log_file%";
+---------------------+--------------------------------------------+
| Variable_name       | Value                                      |
+---------------------+--------------------------------------------+
| slow_query_log_file | /home/adi/sandboxes/msb_ps8_0_36/data/slow |
+---------------------+--------------------------------------------+
1 row in set (0.01 sec)
```

**Reported Affected Version/s:** 5.7.36-39, 8.0.35-27, 8.0.36-28

**Fixed Version:** PS 8.0.39-30, 8.4.2-2

**Workaround/Fix:** Use "set global slow_query_log_file ='<correct slow query log file>';"


[PS-9214](https://perconadev.atlassian.net/browse/PS-9214): INPLACE ALTER TABLE might fail with a duplicate key error if concurrent insertions occur; there have been many bugs reported here and in MySQL bugs regarding duplicate key errors while doing an online alter table operation on tables with primary and unique keys indexes. The bug is not as easy to reproduce but involves ONLY the primary key and includes an atomic sequence that cannot create a duplicate.  It seems to be related to page splits/merges.

**Reported Affected Version/s:** 8.0.35-27, 8.0.36-28

**Fixed Version:** PS 8.0.39-30, 8.4.2-2

**Upstream Bug:**  [115511](https://bugs.mysql.com/bug.php?id=115511)

**Workaround/Fix:** Use ALTER TABLE ... ALGORITHM=COPY instead.


[PS-9275](https://perconadev.atlassian.net/browse/PS-9275): When querying based on a function, MySQL does not use the available functional index when using the LIKE operator, which results inconsistent query plans when functional Indexes are used.

E.g.:
```
CREATE TABLE `test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `a` varchar(200) DEFAULT NULL,
  `test02` varchar(9) GENERATED ALWAYS AS (monthname(from_unixtime(`a`))) VIRTUAL,
  `!hidden!test01!0!0` varchar(9) GENERATED ALWAYS AS (monthname(from_unixtime(`a`))) VIRTUAL,
  PRIMARY KEY (`id`),
  KEY `test01` ((monthname(from_unixtime(`a`)))),
  KEY `test02` (`test02`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
```
mysql> explain select MONTHNAME(FROM_UNIXTIME(a)) from test  WHERE MONTHNAME(FROM_UNIXTIME(a)) Like 'April%';
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | test  | NULL       | ALL  | NULL          | NULL | NULL    | NULL |   13 |   100.00 | Using where |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0,00 sec)

mysql> explain select MONTHNAME(FROM_UNIXTIME(a)) from test  WHERE `!hidden!test01!0!0` Like 'April%';
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | test  | NULL       | range | test01        | test01 | 39      | NULL |    2 |   100.00 | Using where |
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0,00 sec)
```

**Reported Affected Version/s:** 8.0.36-28, 8.4.X

**Upstream Bug:**  [104713](https://bugs.mysql.com/bug.php?id=104713)

**Workaround/Fix:** Use the indexes created on virtual fields explicitly.


[PS-9286:](https://perconadev.atlassian.net/browse/PS-9286) [KMIP](https://docs.oasis-open.org/kmip/spec/v1.4/kmip-spec-v1.4.html#:~:text=Limits%20Attribute%20Rules-,3.22%20State,-This%20attribute%20is) Component leaves keys in a pre-active state.

**Reported Affected Version/s:** 8.0.X, 8.3.0-1, 8.4.0-1

**Fixed Version:** PS 8.0.39-30, 8.4.2-2


[PS-9314:](https://perconadev.atlassian.net/browse/PS-9314) The database crashed due to the SELECT statement. Since the JSON is invalid, the command should return ERROR 3146, an Invalid data type for JSON, but unfortunately, it crashed the instance with Signal 11 using JSON_TABLE.

**Reported Affected Version/s:** 8.0.36-28, 8.0.37-29, 8.0.39-30

**Fixed Version:** PS 8.0.39-30, 8.4.2-2

E.g.:

```
mysql> show global variables like 'version%';
+-------------------------+-----------------------------------------------------+
| Variable_name           | Value                                               |
+-------------------------+-----------------------------------------------------+
| version                 | 8.0.36-28                                           |
| version_comment         | Percona Server (GPL), Release 28, Revision 47601f19 |
| version_compile_machine | x86_64                                              |
| version_compile_os      | Linux                                               |
| version_compile_zlib    | 1.2.13                                              |
| version_suffix          |                                                     |
+-------------------------+-----------------------------------------------------+
6 rows in set (0.01 sec)

mysql> SELECT ele AS domain FROM JSON_TABLE('["TEST'+(select load_file('test'))+'"]', "$[*]" COLUMNS (ele VARCHAR(70) PATH "$" )) AS json_elements ;
ERROR 2013 (HY000): Lost connection to MySQL server during query
No connection. Trying to reconnect...
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (111)
ERROR:
Can't connect to the server
```


[PS-9369:](https://perconadev.atlassian.net/browse/PS-9369) The audit plugin causes memory exhaustion after a few days; disconnecting threads and disabling the audit plugin is undesirable. This workaround can not be used since it requires scheduling an application outage. Even when small, it's a recurrent event.

**Reported Affected Version/s:** 8.0.37-29

**Fixed Version:** PS 8.0.40-31 [Yet to Release]

## Percona Xtradb Cluster


[PXC-4453:](https://perconadev.atlassian.net/browse/PXC-4453) In 3 Node PXC cluster, node01 has active flow control(FC). Active FC blocks user sessions to insert a message into the channel queue (session waits on send monitor (conn->sm)); send monitor is blocked because FC is active. The idea behind the logic is that applier threads, when consuming messages from the queue conn->recv_q, should check if FC is active, and if the queue level is below conn->lower_limit, FC should be disabled, and the user connection thread waiting on the sending monitor should be woken up. In other words, disabling the FC signal is driven by the consumption of events from recv_q by applier threads.

In this case, it seems that recv_q is empty, but FC is active, so nothing can be added to recv_q. We have a vicious circle of some kind of deadlock, and due to this race condition, we are seeing cluster hangs.

**Reported Affected Version/s:** 5.7.25, 5.7.44,  8.0.36-28

**Fixed Version:** PXC 8.0.37-29, 8.4.0


[PXC-4404:](https://perconadev.atlassian.net/browse/PXC-4404) wsrep_preordered=ON causes protocol violations, which cause a node to crash when the group view changes on a cluster with a node acting as an async replica.

**Reported Affected Version/s:** 5.7.44-31

**Workaround/Fix:** Set wsrep_preordered=OFF; however, you may experience a delay in async replication.

Note: Option [wsrep_preordered](https://galeracluster.com/library/documentation/mysql-wsrep-options.html#wsrep-preordered) is deprecated in MySQL-wsrep: 8.0.19-26.3, MariaDB: 10.1.1


[PXC-4362:](https://perconadev.atlassian.net/browse/PXC-4362) The PXC node evicted when creating a function by the user doesn`t have the super privilege, and binary logging is enabled.

**Reported Affected Version/s:** 8.0.34-26

**Fixed Version:** PXC 8.0.36-28, 8.4.0

**Workaround/Fix:** Setting log_bin_trust_function_creators is the workaround. Note that log_bin_trust_function_creators is deprecated by MySQL 8.0.34 and will be removed in the future.


[PXC-4365](https://perconadev.atlassian.net/browse/PXC-4365): PXC nodes leave clusters when the row size is too large and have more than 3 nvarchar columns.

**Reported Affected Version/s:** 8.0.35-27

**Fixed Version:** PXC 8.0.36-28, 8.3.0

## Percona Toolkit

[PT-2325](https://perconadev.atlassian.net/browse/PT-2325):  pt-table-sync does not produce the correct SQL statements to sync tables containing JSON columns properly.

E.g.:

pt-table-sync emits the following SQL:

```
DELETE FROM `test`.`test_to` WHERE `id`='2' AND `data`='{"baz": "quux"}' LIMIT 1;

INSERT INTO `test`.`test_to`(`id`, `data`) VALUES ('1', '{"foo": "bar"}');
```

The INSERT statement works fine, but the DELETE fails to delete the row with `id`='2', because the AND `data`='{"baz": "quux"}' portion of the WHERE clause will result in the query matching zero rows.

Verify the incorrect contents of the test_to table with the following:

```
# Examine the state of our test tables.
$ docker exec -it mysql_5_7_12_test mysql -utest -ptest -e "
    use test;
    select * from test_to;"
```
That should return the following output:
```
+------+-----------------+
| id   | data            |
+------+-----------------+
|    2 | {"baz": "quux"} |
|    1 | {"foo": "bar"}  |
+------+-----------------+
```

Witness that the row with id=2 still exists in the table and was not deleted as it should have been. With JSON columns, the DELETE statement would need to look like this:

```
DELETE FROM `test`.`test_to`
WHERE `id`='2'
AND `data`=CAST('{"baz": "quux"}' AS JSON)
LIMIT 1;
```

**Reported Affected Version/s:** 3.5.7


[PT-2329](https://perconadev.atlassian.net/browse/PT-2329): During the run, pt-archiver will ignore columns that are camelCase during the insert, but it will get all the columns during select.

It could be confirmed by using a dry-run:

```
pt-archiver --source [...] --dest [...] --where "1=1" --statistics --progress=10000 --limit=1000 --no-delete --no-safe-auto-increment --no-check-columns --columns=addressLine1,addressLine2,city,state,postalCode,country,customerNumber --why-quit --skip-foreign-key-checks --dry-run
```

Here are the results:

```
SELECT /*!40001 SQL_NO_CACHE */ `addressLine1`,`addressLine2`,`city`,`state`,`postalCode`,`country`,`customerNumber`,`customernumber` FROM `classicmodels`.`customers` FORCE INDEX(`PRIMARY`) WHERE (1=1) ORDER BY `customernumber` LIMIT 1000

SELECT /*!40001 SQL_NO_CACHE */ `addressLine1`,`addressLine2`,`city`,`state`,`postalCode`,`country`,`customerNumber`,`customernumber` FROM `classicmodels`.`customers` FORCE INDEX(`PRIMARY`) WHERE (1=1) AND ((`customernumber` > ?)) ORDER BY `customernumber` LIMIT 1000

INSERT INTO `classicmodels`.`addresses`(`city`,`state`,`country`) VALUES (?,?,?)
```

**Reported Affected Version/s:** 3.5.7

**Workaround/Fix:** The solution is to include all columns in lowercase in the param --columns until the bug is fixed.


[PT-2344](https://perconadev.atlassian.net/browse/PT-2344): pt-config-diff compares mysqld options, but it fails if the [mysqld] section is in uppercase, even though that is a valid way of setting mysqld variables. Since [MYSQLD] is acceptable for MySQL, pt-config-diff should compare the options under that section.

**Reported Affected Version/s:** 3.5.7

**Workaround/Fix:** Use [mysqld] as lowercase until the bug is fixed.


[PT-2355](https://perconadev.atlassian.net/browse/PT-2355): Table data is lost if we accidentally resume a previously failed job that has null boundaries. pt-online-schema-change should not resume a job with empty boundaries.

**Reported Affected Version/s:** 3.6.0

**Fixed Version:** PT 3.7.1

**Workaround/Fix:** Do not run pt-online-schema-change with job id having null boundaries.


[PT-2356](https://perconadev.atlassian.net/browse/PT-2356): If you run pt-online-schema-change, which results in an error, then subsequent runs will create new tables that won`t be cleaned up.

**Reported Affected Version/s:** 3.6.0


[PT-2349](https://perconadev.atlassian.net/browse/PT-2349): pt-table-sync is failing to sync data from PXC to the async environment, and trigger errors include "WSREP detected deadlock/conflict and aborted the transaction."

**Reported Affected Version/s:** 3.3.1, 3.5.2, 3.6.0


[PT-1726](https://perconadev.atlassian.net/browse/PT-1726): pt-query-digest is not distinguishing queries when an alias is used

**Reported Affected Version/s:** 3.6.0

E.g.:

Queries from slow query log:

```
Time: 2019-01-31T11:00:00.728957Z
# User@Host: sageone_ext_uk[sageone_ext_uk] @ [10.181.130.22] Id: 18714290
# Query_time: 2.709699 Lock_time: 0.000402 Rows_sent: 19 Rows_examined: 51011
use sageone_ext_uk;
SET timestamp=1548932400;
SELECT a,b,c from table1 as t1 where t1.a=3 and t1.b=5;

# Time: 2019-01-31T11:00:00.728957Z
# User@Host: sageone_ext_uk[sageone_ext_uk] @ [10.181.130.22] Id: 18714290
# Query_time: 2.709699 Lock_time: 0.000402 Rows_sent: 19 Rows_examined: 51011
use sageone_ext_uk;
SET timestamp=1548932400;
SELECT a,b,c from table1 as t1 where t1.a=3 and t1.c=5;
```

The fingerprints for the above queries are the same, which is incorrect behaviour:

```
select a,b,c from table? as t? where t?=? and t?=?
```


[PT-2374](https://perconadev.atlassian.net/browse/PT-2374): If we say --ignore=bob, every combination of the bob user will be ignored. This includes bob@localhost, bob@::1, bob@foobar, etc. But this is not the case. Only bob@% is ignored; pt-show-grants --ignore does not ignore all accounts.

**Reported Affected Version/s:** 3.6.0


[PT-2375](https://perconadev.atlassian.net/browse/PT-2375): When pt-table-sync is used on a table with a GENERATED AS column, it fails because we cannot REPLACE/INSERT values into a GENERATED column.

E.g.:
```
`requestStatus` tinyint(1) GENERATED ALWAYS AS (if((`provRequired` = 0),(`httpSyncStatus` not between 200 and 299),(`httpAsyncStatus` not between 200 and 299))) VIRTUAL,

ERROR 3105 (HY000): The value specified for generated column 'requestStatus' in table 'qqq' is not allowed.
```

The ----ignore-columns parameter specifically states that if a REPLACE/INSERT is needed, all columns will be used. Due to this, the pt-table-sync does not work with the generated columns.

**Reported Affected Version/s:** 3.6.0

## PMM [Percona Monitoring and Management]


[PMM-12013:](https://perconadev.atlassian.net/browse/PMM-12013) If we add many RDS instances to the PMM server, say 200+, and Change the prom scrape.maxScrapeSize to the value that allows the VM to parse the reply from the exporter, then the metrics are gathered unreliably, there are gaps, and the exporter`s RSS feed goes to like 5GB for instance. This concludes that rds_exporter is unreliable for large deployments.

**Reported Affected Version/s:** 2.35.0

**Fixed Version:** PMM 3.0.0-Beta available as Tech Preview]


[PMM-12161:](https://perconadev.atlassian.net/browse/PMM-12161) In the Mongodb cluster summary page, Under QPS of Config Services dashboard, it is being clubbed configRS, mongoS and mongod servers. This results in too many configuration services under the QPS of the Config Services dashboard.

**Reported Affected Version/s:** 2.42.0

**Fixed Version:** PMM 3.1 [Yet to Release]


[PMM-12993:](https://perconadev.atlassian.net/browse/PMM-12993) In PMM, CPU metrics have a label "mode" to identify between CPU info: sys, iowait, nice, user, idle, etc. With 1 rds instance, the metric is perfectly fine. However, after adding more instances, the CPU metric is still collected, but the "mode" label is empty, which breaks the graphs in the Advanced Data Exploration dashboard.

**Reported Affected Version/s:** 2.41.1, 2.41.2


[PMM-13148](https://perconadev.atlassian.net/browse/PMM-13148): If we run the queries without using the schema name, then we don`t see such queries in the QAN.

E.g.:
```
mysql [localhost:8036] {msandbox} ((none)) > update test.joinit set g=100,t="06:44:50" where i=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

Here, we can see we did not explicitly select the database name using the USE <database> command and executed the query directly. This results in QAN not being able to capture such queries for analytics.

**Reported Affected Version/s:** 2.41.2

**Workaround/Fix:** Run queries with USE <dbname>; <Query>;


[PMM-13252:](https://perconadev.atlassian.net/browse/PMM-13252) A 500 error message is returned while creating the role with the existing name.

E.g.:

  1. Enable Access roles in PMM Settings

  2. Open the Access role page and create a role with the name “Test. “

  3. Try to create a new role with the name “Test. “

  It returns with Internal server error 500:

  ```
  in logs: msg="RPC /accesscontrol.v1beta1.AccessControlService/CreateRole done in 1.409839ms with unexpected error: pq: duplicate key value violates unique constraint "roles_title_key""
  ```

**Reported Affected Version/s:** 2.42.0

**Workaround/Fix:** It is expected to be fixed in PMM 3


[PMM-13277](https://perconadev.atlassian.net/browse/PMM-13277): When we try to launch PMM using AWS AMI as mentioned in our docs. However, the AWS webpage works fine, and it logins, but every graph and details are blank with "Server error 502" The same can be seen in the log for Victoria metrics:

The following error will be seen:

```
2024-07-27T06:40:22.848Z        panic   /home/builder/rpm/BUILD/VictoriaMetrics-pmm-6401-v1.93.4/lib/mergeset/part_header.go:88 FATAL: cannot read "/srv/victoriametrics/data/indexdb/17D6772949F4A234/17D6772B9FDF298D/metadata.json": open /srv/victoriametrics/data/indexdb/17D6772949F4A234/17D6772B9FDF298D/metadata.json: no such file or directory
panic: FATAL: cannot read "/srv/victoriametrics/data/indexdb/17D6772949F4A234/17D6772B9FDF298D/metadata.json": open /srv/victoriametrics/data/indexdb/17D6772949F4A234/17D6772B9FDF298D/metadata.json: no such file or directory
```

**Reported Affected Version/s:** 2.42.0

**Fixed Version:** PMM 2.43.0

## Percona XtraBackup


[PXB-3302](https://perconadev.atlassian.net/browse/PXB-3302): If the number of GTID sets is absolutely large on a MySQL instance, the output "GTID of the last change" in the Xtrabackup log is truncated compared to the full output in xtrabackup_binlog_info and xtrabackup_info. This can be an issue for external tools obtaining the GTID coordinates from the log as it would be impractical to get the coordinates from  xtrabackup_binlog_info or xtrabackup_info on a large, compressed xbstream file.

Here is a snippet of a backup log:

```
2024-06-03T10:18:59.678581+08:00 0 [Note] [MY-011825] [Xtrabackup] MySQL binlog position: filename 'mysql-bin.000002', position '10197', GTID of the last change ** REDACTED **,9f18624b-214f-11ef-871f-b445068273a0:1,9f1bf5ae-214f-11ef-871f-b445068273a0:1,9f1f6fac-214f-11ef-871f-b445068273a0:1,9f231076-214f-11ef-871f-b445068273a0:1,9f26d153-214f-11ef-871f-b445068273a0:1,9f2a5fdd-214f-11ef-871f-b445068273a0:1,9f2df6e8-214f-11ef-871f-b445068273a0:1,9f318143-214f-11ef-871f-b445068273a0:1,9f353351-214f-11ef-871f-b445068273a0:1,9f38f96c-214f-11ef-871f-b445068273a0:1,9f3cdc53-214f-11ef-871f-b445068273a0:1,9f40fcc0-214f-11ef-871f-b445068273a0:1,9f44955a-214f-11ef-871f-b445068273a0:1,9f481188-214f-11ef-871f-b445068
```

Snippet of xtrabackup_binlog_info:

```
mysql-bin.000002        10197   ** REDACTED **,9fdd9048-214f-11ef-871f-b445068273a0:1,9fe138a3-214f-11ef-871f-b445068273a0:1,9fe4c3d8-214f-11ef-871f-b445068273a0:1,9fe82e39-214f-11ef-871f-b445068273a0:1
```

**Reported Affected Version/s:** 8.0.35-30

**Fixed Version:** PXB 8.4.0-1, 8.0.35-32


[PXB-3283](https://perconadev.atlassian.net/browse/PXB-3283): When xtrabackup takes a backup and exports a tablespace,  xtrabackup gets the wrong table definition from the ibd for tables that have changed the charset-collation in MySQL before backup.

Eg:

```
CREATE TABLE test.a (
  a datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;
```

the collation_id is 8 (latin1_swedish_ci)

```
shell> ibd2sdi /var/lib/mysql/test/a.ibd | jq '.[1].object.dd_object.columns[0]' | grep collation_id
  "collation_id": 8
```

When MySQL converts the charset on a table, it converts the date and time data types columns in the ibd file but not the data dictionary cache. The collation in the ibd does not match that of the data dictionary.

```
ALTER TABLE test.a CONVERT TO CHARACTER SET utf8mb4 collate utf8mb4_unicode_ci;
```

The collation_id becomes 224 (utf8mb4_unicode_ci)

```
shell> ibd2sdi /var/lib/mysql/test/a.ibd | jq '.[1].object.dd_object.columns[0]' | grep collation_id
  "collation_id": 224
```

The collation_id of the copied table is 8 (latin1_swedish_ci)

```
create table xb.a like test.a;

shell> ibd2sdi /var/lib/mysql/xb/a.ibd | jq '.[1].object.dd_object.columns[0]' | grep collation_id
  "collation_id": 8
```

When xtrabackup exports the tablespace, the collation_id is 224 in ibd. Xtrabackup will write it to cfg metadata file.

When MySQL imports a tablespace, MySQL gets an error Column %s precise type mismatch because the collation_id of MySQL does not match that of xtrabackup.

**Reported Affected Version/s:** 8.0.35-30

**Fixed Version:** PXB 8.4.0-1, 8.0.35-31


[PXB-2797](https://perconadev.atlassian.net/browse/PXB-2797): When importing a single table (IMPORT TABLESPACE) from a backup made using xtrabackup and the table contains a full-text index, the import process will error out with:

```
ERROR 1808 (HY000) at line 132: Schema mismatch (Index xxxxxx field xxxxxx is ascending which does not match metadata file which is descending)
```

**Reported Affected Version/s:** 8.0.28-20

**Fixed Version:** PXB 8.0.35-31


[PXB-3210](https://perconadev.atlassian.net/browse/PXB-3210): PXB fails to build on macOS since 8.0.33-28 due to FIND_PROCPS()

```
CMake Error at cmake/procps.cmake:29 (MESSAGE):
  Cannot find proc/sysinfo.h or libproc2/meminfo.h in .  You can pass it to
  CMake with -DPROCPS_INCLUDE_PATH=<path> or install
  procps-devel/procps-ng-devel/libproc2-dev package
Call Stack (most recent call first):
  storage/innobase/xtrabackup/src/CMakeLists.txt:24 (FIND_PROCPS)
```

**Reported Affected Version/s:** 8.0.33-28, 8.0.34-29, 8.0.35-30

**Fixed Version:** PXB 8.0.35-31


[PXB-3130](https://perconadev.atlassian.net/browse/PXB-3130): Performing upgrade from PS 8.0.30 -> PS 8.0.33 using PXB

1. Use PXB 8.0.30 on PS 8.0.30

2. Copy to new host

3. Prepare using PXB 8.0.33

4. Start PS 8.0.33

Which results in the Assertion:

```
I0825 22:33:01.738917 05155 ???:1] xtrabackup80-apply-log(stderr) - InnoDB: Assertion failure: log0recv.cc:4353:log.m_files.find(recovered_lsn) != log.m_files.end()
```

**Reported Affected Version/s:** 8.0.30

**Fixed Version:** PXB 8.0.35-31

## Percona Kubernetes Operator


[K8SPXC-1398:](https://perconadev.atlassian.net/browse/K8SPXC-1398) Scheduled PXC backup job pod fails to complete the process successfully in a random/sporadic fashion.

Error Returns As:

```
+ EXID_CODE=4
+ '[' -f /tmp/backup-is-completed ']'
+ log ERROR 'Backup was finished unsuccessfull'
Terminating processProcess completed with error: /usr/bin/run_backup.sh: 4 (Interrupted system call)2024-05-03 09:39:08 [ERROR] Backup was finished unsuccessfull
+ exit 4
```

**Reported Affected Version/s:** 1.13.0

**Fixed Version:** PXCO 1.16.0 [Yet to Release]

Note: Since we don`t have steps to reproduce the issue, it is hard to confirm whether the fix is working as expected. Please feel free to provide feedback or create a Jira if required.


[K8SPXC-1397:](https://perconadev.atlassian.net/browse/K8SPXC-1397) The operator`s default configuration makes the cluster unusable if TDE (Transparent data encryption) is used; the entry point of the PXC container configures the parameter binlog_rotate_encryption_master_key_at_startup. As a workaround, binlog_rotate_encryption_master_key_at_startup should be disabled. However, it has security implications.

**Reported Affected Version/s:** 1.12.0

**Fixed Version:** PXCO 1.16.0 [Yet to Release]
 

[K8SPXC-1222:](https://perconadev.atlassian.net/browse/K8SPXC-1222) Upgrading Cluster Fails When Dataset Has Large Number Of Tables. When the operator replaces the first pod with one with the new version, it fails to start up and gets stuck in a loop that restarts every 120 seconds.

The problem looks like from pxc-entrypoint.sh:

```
for i in {120..0}; do
            if echo 'SELECT 1' | "${mysql[@]}" &>/dev/null; then
                break
            fi
            echo 'MySQL init process in progress...'
            sleep 1
        done
```

**Reported Affected Version/s:** 1.11.0, 1.12.0

**Fixed Version:** PXCO 1.16.0 [Yet to Release]

## Orchestrator


[DISTMYSQL-406](https://perconadev.atlassian.net/browse/DISTMYSQL-406): Orchestrator 3.2.6-11 shows the MySQLOrchestratorPassword variable value in the error log and when accessing the web interface.

E.g.:

Create a MySQL and Orchestrator node
```
mysql -e "CREATE USER 'orchestrator_srv'@'%' IDENTIFIED BY 'orc_server_password'; GRANT ALL ON orchestrator.* TO 'orchestrator_srv'@'%';"
```
Configure Orchestrator to use node0 as MySQL backend database

```
vi /usr/local/orchestrator/orchestrator.conf.json 
```
Add the following lines and remove sqlite options:
```
  "MySQLOrchestratorHost": "node_0_IP",
  "MySQLOrchestratorPort": 3306,
  "MySQLOrchestratorDatabase": "orchestrator",
  "MySQLOrchestratorUser": "orchestrator_srv",
  "MySQLOrchestratorPassword": "orc_server_password",
```
On node1, there are several messages showing the backend password:
```
Feb 28 23:26:03 XX-XX-node1 orchestrator[4262]: 2024-02-28 23:26:03 ERROR 2024-02-28 23:26:03 ERROR QueryRowsMap(orchestrator_srv:orc_server_password@tcp(10.124.33.138:3306)/orchestrator?timeout=1s&readTimeout=30s&rejectReadOnly=false&interpolateParams=true) select hostname, token, first_seen_active, last_seen_Active from active_node where anchor = 1: dial tcp 10.124.33.138:3306: connect: connection refused
```

**Reported Affected Version/s:** 8.0.36(PS)

**Fixed Version:** 8.4.0(PS)

## Summary

We welcome community input and feedback on all our products. If you find a bug or would like to suggest an improvement or a feature, learn how in our post, [How to Report Bugs, Improvements, New Feature Requests for Percona Products](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/).

For the most up-to-date information, be sure to follow us on [Twitter](https://twitter.com/percona), [LinkedIn](https://www.linkedin.com/company/percona), and [Facebook](https://www.facebook.com/Percona?fref=ts).

Quick References:

[Percona JIRA](https://jira.percona.com)

[MySQL Bug Report](https://bugs.mysql.com/)

[Report a Bug in a Percona Product](https://www.percona.com/blog/2019/06/12/report-bugs-improvements-new-feature-requests-for-percona-products/)

___

About Percona:

As the only provider of distributions for all three of the most popular open source databases---PostgreSQL, MySQL, and MongoDB---Percona provides [expertise](https://www.percona.com/services/consulting), [software](https://www.percona.com/software), [support](https://www.percona.com/services/support/mysql-support), and [services](https://www.percona.com/services/managed-services) no matter the technology.

Whether its enabling developers or DBAs to realize value faster with tools, advice, and guidance, or making sure applications can scale and handle peak loads, Percona is here to help.

Percona is committed to being open source and preventing vendor lock-in. Percona contributes all changes to the upstream community for possible inclusion in future product releases.
