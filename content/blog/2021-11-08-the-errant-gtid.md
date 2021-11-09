---
title: 'The Errant GTID, PT1'
date: "2021-11-08T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', 'Recovery', 'Replication', 'GTID']
authors:
  - wayne
images:
  - blog/2021/11/lostart-01.png
slug: The Errant GTID PT1
---

# Part 1

No one likes to see an errant GTID on a replica. An errant GTID can make
promotion of the replica to the primary difficult.

An errant GTID is BAD. Why is it bad? The errant GTID could still be in the replicas binlog so when it becomes the new primary these event will get sent to other replicas causing data corruption or breaking replication.

### Its easy to prevent errant GTID's.

1. `read_only = ON` in the replicas my.cnf
2. Disable binlogs when you need to perform work on a replica that he primary does need to to know about. `set sql_log_bin = 'off';` before your work on replica. `set sql_log_bin = 'on';` when your work is complete.

### Find and correct errant GTID

How do you correct an errant GTID? Compare the `gtid_executed` on the primary and replica. Identify the errant GTID on the replica and then apply that GTID to the primary. Pretty simple? well yes and no.

Let me walk you through how I look for and then correct errant GTID's.

1. On the replica I run `show variable like 'gtid_executed'`

You will get output similar to this:

`mysql_replica> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)`

Take note of the `Value:` copy this and hold on to it for later in the steps.

2. On the primary I run `show variable like 'gtid_executed'`

You will get output similar to this:

`mysql_primary> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)`

Again take note of the `Value:` copy this and hold on to it for later in the steps.

3. Now lets determine if the replica has any errant GTID's. We will compare the gtid_subset of the replica. So in below example it will be replica GTID and then primary GTID

`mysql_replica> select gtid_subset('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as subset;
+--------+
| subset |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)`

Subset = 1 meaning we have no errant GTID's.

Now lets introduce an errant transaction on the replica. Let's do something simple by creating a new database.

`mysql_replica> create database community;
Query OK, 1 row affected (0.01 sec)`

Lets do step 1 from above.

`mysql_replica> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)`

Lets repeat step 3 using the new gtid_executed from the replica and the original gtid_executed from the primary.

`mysql_replica> select gtid_subset('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as subset;
+--------+
| subset |
+--------+
|      0 |
+--------+
1 row in set (0.00 sec)`

Subset = 0 meaning we do have an errant GTID on our replica.

Now we need to determine what that is. We will need to subtract the `replica executed GTID` from the `primary executed GTID`. To do this we will using the `gtid_subtract` function.

`mysql_replica> select gtid_subtract('858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2','858d4d54-3fe1-11ec-a7e8-080027ae8b99:1,
    '> a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2') as errant;
+----------------------------------------+
| errant                                 |
+----------------------------------------+
| 858d4d54-3fe1-11ec-a7e8-080027ae8b99:2 |
+----------------------------------------+
1 row in set (0.00 sec)`

Now we have our errant GTID from the replica `858d4d54-3fe1-11ec-a7e8-080027ae8b99:2`

### Repair the issue

Now let's move to the primary.

Once on the primary we want to insert a pseudo GTID to resolve the errant on the replica.

`mysql_primary> set gtid_next='858d4d54-3fe1-11ec-a7e8-080027ae8b99:2';
Query OK, 0 rows affected (0.00 sec)`

`mysql_primary> begin;
Query OK, 0 rows affected (0.00 sec)`

`mysql_primary> commit;
Query OK, 0 rows affected (0.00 sec)`

`mysql_primary> set gtid_next='automatic';
Query OK, 0 rows affected (0.00 sec)`

Now lets compare the GTID executed again from the replica and primary.

### Primary:
`mysql_primary> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)
`
### Replica:
`mysql> show variables like 'gtid_executed'\G
*************************** 1. row ***************************
Variable_name: gtid_executed
        Value: 858d4d54-3fe1-11ec-a7e8-080027ae8b99:1-2,
a6b3751e-3fd3-11ec-a4f5-080027ae8b99:1-2
1 row in set (0.00 sec)`

Note that both Values match. We have repaired the errant GTID from the replica to the primary.

I would suggest you now run pt-table-checksum from the primary to verify your data is consistent.

In my example I created a database called community on the replica to create the errant GTID.

I suggest you remove that database community from the replica. Let's just step through the quick steps to drop the community database.

1. Connect to replica
2. show databases; (verify that community still exists)
3. set sql_log_bin = 'off';
4. drop database community;
5. show databases; (verify that community is dropped)
6. set sql_log_bin = 'on';

Thats it. You have fixed and cleaned up the mess you made. This was a rather simple example of an errant GTID. I will be doing part 2 that will look at more complexed examples.
