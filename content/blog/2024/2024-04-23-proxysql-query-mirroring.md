---
title: "Using ProxySQL Query Mirroring to test query performance on a new cluster"
date: "2024-04-23T00:00:00+00:00"
draft: false
tags: ["ProxySQL", "Upgrades"]
authors:
  - isobel_smith
slug: using-proxysql-query-mirroring-to-test-query-peromance-on-a-new-cluster
images:
  - blog/2024/04/proxysql-query-mirroring.png
---

ProxySQL is an SQL aware proxy, which gives DBA's fine grained control over clients’ access to the MySQL cluster. A key part of our DBA team’s process in testing and preparing for major MySQL version upgrades is comparing query plans using [ProxySQL query mirroring](https://proxysql.com/documentation/mirroring/). This feature allows us to mirror queries to another cluster / host, by configuring query rules. What makes mirroring particularly useful is the ability to selectively mirror queries based on the query digest, or client user. Results from the queries that are mirrored are not returned to the client, and are sent to /dev/null.

Before configuring ProxySQL for Query Mirroring, ensure that the clients that you want to mirror the queries for, are able to connect to both the current, and the new cluster. You should also ensure that the ProxySQL monitor can connect to the new cluster, otherwise ProxySQL will mark the new hosts as offline, and the queries will not be mirrored there.

## To set up query mirroring in ProxySQL:

In order to set up query mirroring, you need to add the new hosts into the `mysql_server` table in ProxySQL. This is how the current `mysql_servers` table looks, before we add the new host that we want to mirror the queries to:

```
MySQL> SELECT hostgroup_id, hostname FROM mysql_servers;
+--------------+--------------+
| hostgroup_id | hostname     |
+--------------+--------------+
| 10           | 10.12.0.123  |
| 20           | 10.12.0.123  |
| 20           | 10.16.0.456  |
| 20           | 10.16.0.789  |
+--------------+--------------+
4 rows in set (0.01 sec)
```

It is important to choose a `hostgroup_id` that is not yet in use. You can double check the currently configured host groups in the mysql hostgroups table, as you do not want to inadvertently add the mirror hosts into the production traffic! 

```
MySQL> select * from mysql_replication_hostgroups;
+------------------+------------------+------------+----------------------+
| writer_hostgroup | reader_hostgroup | check_type | comment              |
+------------------+------------------+------------+----------------------+
| 10               | 20               | read_only  | Async Cluster        |
+------------------+------------------+------------+----------------------+
1 row in set (0.00 sec)
```

Please note, in our example, we are using async replication, so we check the `mysql_replication_hostgroups` table, but the hostgroups table you need to check, depends on the cluster architecture you are using: 

 - async replica clusters check the `mysql_replications_hostgroups` table.
 - galera clusters check the `mysql_galera_hostgroups` table
 - group replication check the `mysql_group_replication_hostgroups` table.

We are using hostgroup 10 for the writer hostgroup, and hostgroup 20 for the reader. For this example, we will choose 100 for the mirror `hostgroup_id`. Once you have decided on an unused hostgroup ID, add the new clusters’ nodes to the `mysql_servers` table in ProxySQL.

```
MySQL>  INSERT INTO mysql_servers(host, hostgroup, comment) VALUES ("10.12.0.987", 100, "mirror_cluster");
LOAD MYSQL SERVERS TO RUN;
SAVE MYSQL SERVERS TO DISK;
```

The `mysql_servers` table will now include the new host:

```
MySQL> SELECT hostgroup_id, hostname FROM mysql_servers;
+--------------+--------------+
| hostgroup_id | hostname     |
+--------------+--------------+
| 10           | 10.12.0.123  |
| 20           | 10.12.0.123  |
| 20           | 10.16.0.456  |
| 20           | 10.16.0.789  |
| 100          | 10.12.0.987  |
+--------------+--------------+
4 rows in set (0.01 sec)
```

In order to enable query mirroring, you need to update the `mirror_hostgroup` column in the `mysql_query_rules` table. When mirroring is not enabled, the value of the `mirror_hostgroup` column is `NULL`. 
Our query rules before enabling query mirroring are defined as:

```
MySQL> select rule_id, username, match_digest, destination_hostgroup, mirror_hostgroup from mysql_query_rules;
+---------+------------------------+---------------------+-----------------------+------------------+
| rule_id | username               | match_digest        | destination_hostgroup | mirror_hostgroup |
+---------+------------------------+---------------------+-----------------------+------------------+
| 1       | myApplicationUser      | ^SELECT.*FOR UPDATE | 10                    | NULL             |
| 2       | myApplicationUser      | ^SELECT             | 20                    | NULL             |
+---------+------------------------+---------------------+-----------------------+------------------+
2 rows in set (0.00 sec)

```

To enable mirroring, we just need to update the `mirror_hostgroup`. For this example, we will mirror all the `SELECT` queries made by `myApplicationUser`:


```
UPDATE mysql_query_rules SET mirror_hostgroup = 100 where rule_id=2;
LOAD mysql query rules TO RUN;
SAVE mysql query rules TO DISK;
```

The rules should now be updated:

```
MySQL> select rule_id, username, match_digest, destination_hostgroup, mirror_hostgroup from mysql_query_rules;
+---------+-----------------------+---------------------+-----------------------+------------------+
| rule_id | username              | match_digest        | destination_hostgroup | mirror_hostgroup |
+---------+-----------------------+---------------------+-----------------------+------------------+
| 1       | myApplicationUser     | ^SELECT.*FOR UPDATE | 10                    | NULL             |
| 2       | myApplicationUser     | ^SELECT             | 20                    | 100              |
+---------+-----------------------+---------------------+-----------------------+------------------+
2 rows in set (0.00 sec)

```

The incoming queries that match the query rule, (in our example above, this is all queries as matching the regular expression '^SELECT', for myApplicationUser, excluding queries matching '^SELECT.*FOR UPDATE'), will now be mirrored to the new cluster. You can verify this by checking the MySQL processlist on the new cluster. 

The `stats_mysql_query_digest` table on ProxySQL holds statistics for the queries that are being processed by ProxySQL. To use the `stats_mysql_query_digest` table, the global variables `mysql-commands_stats` and `mysql-query_digests` must be set to true, which is the default.

Comparing query performance between two clusters

Query the `stats_mysql_query_digest` table to compare the performance per query between the current and the new cluster:

```
MySQL> select
  (b.count_star+a.count_star)/2 as count,
  cast(round(((b.sum_time + 0.0)/(b.count_star + 0.0))/((a.sum_time + 0.0)/(a.count_star + 0.0)),2)*100 as int) as percent,
  cast(round(((b.sum_time + 0.0)/(b.count_star + 0.0))/((a.sum_time + 0.0)/(a.count_star + 0.0)),2)*100 as int)*(b.count_star+a.count_star)/2 as load ,
  substr(a.digest_text,1,150)
from
  stats_mysql_query_digest a
inner join
  stats_mysql_query_digest b on
  a.digest = b.digest
where
  a.hostgroup = 10
  and b.hostgroup = 100
order by
  percent ASC;
```

In this example, the current production cluster has hostgroup 10, and the new mirror cluster was assigned hostgroup 100. The queries with a percentage above 100 are the queries that perform slower on the new cluster, and may be worth investigating, while the queries with a percentage below 100 are more performant on the new cluster. To investigate queries, you can compare the EXPLAIN plan of the query on the current and the new cluster. We use PMM Query Analytics to compare query analytics and the explain plan of the queries on the two separate clusters.

It is worth noting, that you should allow enough time for the MySQL buffer pool to get filled, before checking the `stats_mysql_query_digest` table. Otherwise, the query times on the new cluster can be skewed, as the active dataset may not yet be in memory (whereas on the current cluster it might be). Also, keep in mind that if you are mirroring only a subset of queries, the load on the new cluster will be different to the current cluster, and could affect the query performance on the new cluster, so that they appear significantly faster. Checking the execution plan of the query to see whether it has changed, is therefore more important than looking at overall load.

To conclude, using query mirroring to test queries on a new system, before making the migration, allows you to compare latency and query plans per normalised query, and proactively detect any necessary alterations before switching live traffic to the new cluster.
