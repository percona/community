---
title: 'The Errant GTID'
date: "2021-11-08T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', 'Recovery', 'Replication', 'GTID']
authors:
  - wayne
images:
  - blog/2021/11/errant-gtid-1.png
slug: The-Errant-GTID-PT1
---

# Part 1

<p>What is a GTID? Oracle/MySQL define a GTID as "A global transaction identifier (GTID) is a unique identifier created and associated with each transaction committed on the server of origin (the source). This identifier is unique not only to the server on which it originated, but is unique across all servers in a given replication topology."

An errant transaction can make
promotion of a replica to primary very difficult.

An errant transaction is BAD. Why is it bad? The errant transaction could still be in the replicas binlog so when it becomes the new primary these event will get sent to other replicas causing data corruption or breaking replication.

#### Its easy to prevent errant transaction.

1. `read_only = ON` in the replicas my.cnf
2. Disable binlogs when you need to perform work on a replica.  `set session sql_log_bin = 'off';` before your work on replica. `set session sql_log_bin = 'on';` when your work is complete.</p>

#### Find and correct errant transaction

How do you correct an errant transaction? Compare the `gtid_executed` on the primary and replica. Identify the errant transaction on the replica and then apply that transaction to the primary.

I will show you one method in the steps below.

1. On the replica run `show variables like 'gtid_executed'`

You will receive output similar to this:
```
mysql_replica> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)
```
Make note of the gtid_executed value. You will need this to check if you have an errant transaction.

2. On the primary run `show variables like 'gtid_executed'`

You will receive output similar to this:
```
mysql_primary> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)
```
Make note of the gtid_executed value. You will need this to check if you have an errant transaction.

3. We need to determine if the replica has any errant transaction's. We will use the function: 'gtid_subset' to compare the executed GTID set from **replica** and **primary**.
```
mysql_replica> select gtid_subset('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as subset;
+--------+
| subset |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)
```
Subset = 1 tells us we have **no** errant transactions.

Now we need to introduce an errant transaction in to the replica. Let's do something simple by creating a new database.
```
mysql_replica> create database community;
Query OK, 1 row affected (0.01 sec)
```
Lets repeat step 1 from above.
```
mysql_replica> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)
```
We will repeat step 3 using the **new gtid_executed** from the replica and the **original gtid_executed** from the primary.

```
mysql_replica> select gtid_subset('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as subset;
+--------+
| subset |
+--------+
|      0 |
+--------+
1 row in set (0.00 sec)
```
Subset = 0 tells us that this replica has errant transactions.

Now we need to determine the errant transaction. We will need to subtract the `replica executed GTID` from the `primary executed GTID`. To do this we will use the `gtid_subtract` function.
```
`mysql_replica> select gtid_subtract('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as errant;
+----------------------------------------+
| errant                                 |
+----------------------------------------+
| 858d4d54-3fe1-11ec-a7e8-080027ae8b99:2 |
+----------------------------------------+
1 row in set (0.00 sec)
```
Now we have our errant transaction from the replica `858d4d54-3fe1-11ec-a7e8-080027ae8b99:2`

#### Repair the issue

Now let's move to the **primary**.

Once on the **primary** we want to insert a pseudo transaction to resolve the errant transaction from the replica.
```
mysql_primary> set gtid_next='858d4d54-3fe1-11ec-a7e8-080027ae8b99:2';
Query OK, 0 rows affected (0.00 sec)

mysql_primary> begin;
Query OK, 0 rows affected (0.00 sec)

`mysql_primary> commit;
Query OK, 0 rows affected (0.00 sec)

`mysql_primary> set gtid_next='automatic';
Query OK, 0 rows affected (0.00 sec)
```
We can compare the GTID executed again from the replica and primary.

#### Primary:
```
mysql_primary> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)
```
#### Replica:
```
mysql_replica> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)`
```
Note that both values match. We have repaired the errant transaction from the replica to the primary.

Now we need to take care of the replica that had the errant transaction. We need to flush and purge the binary logs. Use the commands below to find the current binary file, and then flush and purge. **Remember to be on the replica**.

```
show binary logs;
FLUSH LOGS;
PURGE BINARY LOGS TO 'binlog.00000x';
```

<p>Thats it. You have fixed the errant transaction. This was a rather simple example of an errant GTID. I will be doing part 2 that will look at more complexed examples.

If you want to validate your data is consistent between the primary and replica. You could use a tool like [pt-table-checksum](https://percona.community/blog/2021/07/22/lets-be-insync/), or any other method you prefer. </p>
