---
title: 'Fixing Common PostgreSQL Performance Bottlenecks'
date: Fri, 04 Dec 2020 20:26:50 +0000
draft: false
tags: ['Michael.Aboagye', 'PostgreSQL']
categories: ["PostgreSQL"]
authors:
  - michael_aboagye
images:
  - blog/2020/08/social-forums-postgresql-general-discussion.jpg
slug: fixing-common-postgresql-performance-bottlenecks
aliases:
    - /blog/fixing-common-postgresql-performance-bottlenecks/
---

Overview
--------

In this article, I look at how poorly designed sharding systems and replication systems in PostgreSQL affect query performance in high volume situations, and how to ensure data consistency across many servers.  I also discuss how excessive vacuuming generates I/O traffic, and how connection pooling is used to improve transaction throughput by caching connections from clients.  I also cover how insufficient memory could affect PostgreSQL performance.  These are key problems I have encountered as a database consultant, and how I've overcome them.

Sharding Bottlenecks
--------------------

Sharding is one of the ways to scale a database server to store terabytes of data. Sharding distributes data evenly via a partitioning function or algorithm to different tables or to a different server instance. 

The following are common sharding approaches for production systems:

*   Sharding by geography
*   Sharding by username
*   Sharding by user-id
*   Sharding by a range

Although sharding is one of the most common strategies to handle a large number of queries from clients, a poorly designed sharding system can affect database performance and become a performance bottleneck. 

Let's assume we have a database made up of two tables such as the users' table and followers table. The users' table contains registered users of a social site service while the followers' table is made up of users being followed by users in the users' table. 

Since we have approximately 10,000 users subscribing to our social site service and most of the subscribed users do not have many followers, we decided to shard the users' table by username (indexing the username as the query key). Each sharded table is assigned to 2,000 users. Thus all 10,000 users are assigned to five (5) tables. 

It is advisable to shard large tables instead of smaller tables. 

Now let's look at why the sharding approach we selected can affect query performance and become a bottleneck in database infrastructure. 

In a situation where a follower sends a query or request for a particular user's details (let's say username, Frank Brown). Assuming there are more than five users with the first name Frank. The query engine needs to go through multiple names with the first name 'Frank' before arriving at the user with the last name 'Brown'. 

Also because a username is updateable or a mutable value, we need to perform an update operation to make sure every old username in the users' table is replaced with a new username. 

Performing an update operation for many users in a relational database is really expensive as we need to do so across many tables. In this case, even though we decided to introduce scalability by sharding the users' table, we failed to design effective sharding. 

Instead of sharding user tables by usernames in a heavy data-intensive environment, it is advisable to shard by geographical area. Users from a specific region or continent are assigned to a specific table. For instance, we can assign subscribed users from the EMEA region to a specific table and other groups of subscribed users to the LATAM region. 

Although the geographical area is a mutable value likewise username, it does not introduce redundancy. It is not mandatory to update a user's location. We can still maintain the same geographical value for a user even if the user migrates from one location to another. 

In addition, we can also improve query optimization by storing each value in a single column. In this case, the first name and the last name of a user is stored in different or separate columns. There is no need for the query engine to go through multiple users with username 'Frank'. 

Storing two values in a single column makes it difficult or almost impossible to run an efficient query.

Replication Bottlenecks
-----------------------

Building a high data-intensive service requires a well-designed replication system too. The best way to set up a replication system is to align it with the design of a web service. In other words, the structure of the web service should determine which replication concept to use. 

Most relational database systems follow the concept of asynchronous and synchronous replication. 

With Asynchronous replication, data is replicated or copied to the slave server once the transaction has been committed on the master server. Synchronous replication ensures that data written by the transaction will be on both the master server and the slave server at the time the transaction commits. 

Let assume we decided to use a synchronous replication system for a write-intensive web service. This requires the same set of data to exist on both the master and the slave server at the time the transaction commits. But this can lead to latency issues. 

Synchronous replication is far more expensive than asynchronous replication because of the overhead involved. Data usually is replicated on more than two servers at the time the transaction commits. 

How do we ensure data consistency and yet prevent latency issues? 

In setting up a replication system for a write-intensive service, the best solution is to implement asynchronous replication. It is less expensive since since no overhead involved. The master server does not need to connect to two or three remote replica servers to replicate data at the time the transaction commits. Instead, data is replicated on the slave servers after the transaction has been committed on the master. 

We can sometimes rely on XLOG to replay all transaction in case the master server experiences partition failure. Partition failure or 'split-brain' separates the master server from the slave servers so there is no longer communication between them.  However, it is advisable to also provide external backups for the master server instead of relying solely on XLOG. 

In PostgreSQL, it possible to backup data on a master server to an external archive using the archive command. There is also a restore command to restore the master server to its previous state. Although this procedure (asynchronous replication + continuous archiving) is complex to administer, it guarantees efficient performance than synchronous replication. Also continuous archiving does not consume excess I/O capacity. 

Choosing whether to use synchronous replication or asynchronous replication should be determined by the design of the service communicating with the database.

Checkpointing Bottlenecks
-------------------------

In PostgreSQL, data protection and consistency are assured through the XLOG. Any data written to postgres is sent to the XLOG before it is written to the data files. It is impossible to write data to the XLOG forever without taking up or filing up disk space, checkpointing needs to be done. 

Thus checkpointing is the process of deleting or truncating XLOG after a specified period. However, if the `checkpoint_segment` and `checkpoint_time` parameters in the `postgres.conf` file is not tuned well, we have a problem at hand. 

For instance, if the distance between two checkpoints is very large and in the event of a system crash, postgres has to replay the last checkpoint, the failed database instance might take a long time to start again. 

When it comes to checkpointing, the following parameters inside the postgres.conf file are very important. Balanced configuration of these two parameters is a must.

*   **checkpoint_segment**: In addition to the `checkpoint_timeout`, this parameter defines the distance between two checkpoints. In Postgres, a segment is 16MB by default. In production systems, it is safe to set checkpoint_segment to 256MB.
*   **checkpoint_timeout**: It defines the upper limit of time allowed between two checkpoints. You can increase it to about 30min.

Bloat Bottlenecks
-----------------

In PostgreSQL, autovacuum is used for dealing with dead rows and frozen rows. Dead rows are rows that have been deleted or become obsolete but they have not been physically removed from tables. Frozen rows occur when a row version is old enough to become a candidate for being frozen. 

In PostgreSQL, we make use of the VACCUM command to deal with dead rows and frozen rows. Although vacuuming is the best way to deal with dead and frozen rows, it creates a lot of I/O traffic. In order to prevent high disk I/O, it is often necessary to turn off vacuuming by modifying the autovacuum parameter in the postgres.conf file.  But bloated tables and indexes can occur when you turn off autovaccum for a longer time than usual. Bloated tables and indexes tend to affect database performance because they occupy more storage space. 

Postgresql provides extension such as pgstattuple to deal with bloated tables and indexes. The function pgstattuple can be used to examine row-level statistics to determine or find out if there are dead rows available. If dead rows are present, the dead tuples percent column value is greater than zero. If there are no dead rows, the value is less than 1. 

The following steps show how to discover and remove dead rows:
```sql
CREATE EXTENSION pgstattuple;
CREATE TABLE m_data AS SELECT * FROM generate_series(1, 1000)
SELECT * FROM stats.pgstattuple('m_data')
DELETE FROM m_data WHERE generate_series % 3 = 0
SELECT * FROM stats.pgstattuple('m_data')
VACCUM m_data
SELECT * FROM stats.pgstattuple('m_data')

```
You can run the following query to check if there are any bloating indexes for a particular table.
```sql
SELECT relname, pg_table_size(oid) as index_size,
100-(stats.pgstatindex(relname)).avg_leaf_density AS bloat_ratio
FROM pg_class WHERE relname ~ 'casedemo' AND relkind = 'i';
```

Vacuuming Bottlenecks
---------------------

Although autovaccum or vacuum is used to remove dead rows, it is also used for the following:

*   To keep statistics collection up to date which is used by the PostgreSQL query planner.
*   To prevent the loss of old transaction data due to transaction ID wraparound issues.

Although autovacuum or vacuum can be used to physically remove dead rows to prevent bloated tables, excessive vacuuming can cause a database to perform below par because it generates high I/O traffic. 

There are two situations where there might be high I/O traffic during vacuuming: 
1. When a table is made up of a large number of rows that need freezing. 
2. When there are many rows with the same transaction ID during freezing time. 

In order to avoid excessive vaccuming, you need to focus on the following parameters in the `postgresql.conf` file.

*   **autovaccum_vaccum_threshold**: This parameter determines the number of updated and deleted rows to initiate VACCUM in the associated table. You can set the value to 100. Thus 100 rows of updated and deleted rows will be vaccumed.
*   **autovaccum_analyze_threshold**: This parameter determines the number of updated and deleted rows to initiate ANALYZE in the associated table.
*   **autovaccum_analyze_threshold**: This parameter specifies the number of updated and deleted rows you need to initiate ANALYZE in the associated table. You can set this value to 100.
*   **autovaccum_max_workers**: This parameter specifies the number of workers that might be executed during vaccuming. A maximum of 5 workers is is enough to avoid excessive use of OS resources.
*   **autovaccum_vaccum_scale_factor**: This parameter specifies the fraction of the table size that needs to be added to autovaccum_vaccum_threshold when deciding whether to trigger VACCUM. You can set it value to 0.4.
*   **autovaccum_analyze_scale_factor**: This parameter specifies the fraction of the table size that needs to be added to autovaccum_vaccum_threshold when deciding whether to trigger ANALYZE. You can set it value to 0.3.

Apart from modifying the above parameters to suit your database behavior, you need to select tables with a large number of updated and deleted rows to vacuum frequently. In addition, it is advisable to vacuum after working hours or on weekends. You can schedule vacuuming using the [pg_cron](https://github.com/citusdata/pg_cron) extension. For instance, the code below executes the VACCUM command at 10:00 pm every Sunday.
```sql
SELECT cron.schedule('0 10 * * 7', 'VACCUM')
```

Connection Bottleneck
---------------------

If your application is designed around 'short-lived' connections and you expect many queries from different client sessions, then you need to implement connection pooling using the likes of pgbouncer, pgpool2, and so on. 

Why is connection pooling important? 

Connection pooling creates a pool of connections and caches or reserves those connections so that it can be used again. In PostgreSQL, there is a process known as postmaster which handles or manages communication between frontend and backend processes. The postmaster process starts another separate server process known as Postgres to handle connections from clients. 

Each time a client connects to the Postgres database, the postmaster process spawns or creates a new process for each connection to the database. This process takes up to 2 or 3 MB memory for every connection to the database. 

So imagine a database infrastructure without any connection pooling? More memory is consumed for creating these connections.