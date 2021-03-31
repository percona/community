---
title: 'Enabling KMS encryption for a running Amazon RDS instance'
date: Fri, 08 Jun 2018 11:40:02 +0000
draft: false
tags: ['renato-losio', 'Amazon RDS', 'AWS', 'encryption', 'KMS encryption', 'MySQL']
authors:
  - renato_losio
images:
  - blog/2018/04/safety-2890768_640.jpg
slug: enabling-kms-encryption-running-amazon-rds-instance
---

Since summer 2017, Amazon RDS supports [encryption](https://aws.amazon.com/about-aws/whats-new/2017/06/amazon-rds-enables-encryption-at-rest-for-additional-t2-instance-types/) at rest using AWS Key Management Service (KMS) for db.t2.small and db.t2.medium database instances, making the feature now available to virtually every instance class and type. 

Unless you are running [Previous Generation DB Instances](https://aws.amazon.com/rds/previous-generation/) or you can only afford to run a db.t2.micro, every other instance class now supports native encryption at rest using KMS. As for the Amazon documentation:

> _Encryption on smaller [T2 database instances](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html) is useful for development and test use cases, where you want the environment to have identical security characteristics as the planned production environment. You can also run small production workloads on T2 database instances, to save money without compromising on security._

How to encrypt a new instance
-----------------------------

Enabling encryption at rest for a new RDS instance is simply a matter of setting one extra parameter in the create instance request. For example using the [CLI create-db-instance](http://docs.aws.amazon.com/cli/latest/reference/rds/create-db-instance.html)
```
[--storage-encrypted | --no-storage-encrypted]
```
or a check-box in the console. But what about existing instances? **There is no direct way to modify the encryption of a running RDS instance.**

### **Snapshot approach**

The simplest way to have an encrypted MySQL instance is to terminate the existing instance with a final snapshot or take a snapshot in a read only scenario. 

With the encryption option of [RDS snapshot copy](http://docs.aws.amazon.com/cli/latest/reference/rds/copy-db-snapshot.html), it is possible to convert an unencrypted RDS instance into encrypted simply by starting a new instance from the encrypted snapshot copy, for example:
```
aws rds copy-db-snapshot --source-db-snapshot-identifier --target-db-snapshot-identifier --kms-key-id arn:aws:kms:us-east-1:******:key/016de233-693e-4e9c-87e8-**********
```
where the kms-key-id  is the KMS encryption key. 

Unfortunately this is simple but requires a significant downtime as you will not be able to write to your RDS instance from the moment that you take the first snapshot until the time the new encrypted instance is available. A matter of minutes or hours, according to the size of your database.

### What about limited downtime?

There are at least two more options on how to encrypt the storage for an existing RDS instance:

1.  Use [AWS Database Migration Service](https://aws.amazon.com/dms/): the source and target will have the same engine and the same schema but the target will be encrypted. However, this is usually not suggested for homogeneous engines as in our scenario.
2.  Use a native MySQL read replica with a similar approach to the one documented by AWS to [move RDS MySQL Databases from EC2 classic to VPC](https://d0.awsstatic.com/whitepapers/RDS/Moving_RDS_MySQL_DB_to_VPC.pdf).

### Encrypting and promoting a read replica

Let's see how we can leverage MySQL native replication to convert an unencrypted RDS instance to an encrypted RDS instance with reduced down time. All the tests below have been performed on a MySQL 5.7.19 (the latest available RDS MySQL) but should work on any MySQL 5.6+ deployment. 

Let's assume the existing instance is called test-rds01 and a master user rdsmaster

1.  We create a RDS read replica _test-rds01-not-encrypted_ of the existing instance _test-rds01_.
    ```
    aws rds create-db-instance-read-replica --db-instance-identifier test-rds01-not-encrypted --source-db-instance-identifier test-rds01
    ```
2.  Once the read replica is _available_, we stop the replication using the RDS procedure "CALL mysql.rds_stop_replication;"  Note that not having a super user on the instance, the procedure is the only available approach to stop the replication.
    ```
    $ mysql -h test-rds01-not-encrypted.cqztvd8wmlnh.us-east-1.rds.amazonaws.com -P 3306 -u rdsmaster -pMyDummyPwd --default-character-set=utf8 -e "CALL mysql.rds_stop_replication;"
    
    +---------------------------+
    
    | Message |
    
    +---------------------------+
    
    | Slave is down or disabled |
    
    +---------------------------+
    
    
    ```
3.  We can now save the the binary log name and position from the RDS replica that we will need later on calling:
    ```
    Relay_Master_Log_File: mysql-bin-changelog.275872
    
    Exec_Master_Log_Pos: 3110315
    ```
4.  And create a snapshot _test-rds01-not-encrypted_ of the RDS replica _test-rds01-not-encrypted_ as the replication is stopped.
    ```
    $ aws rds create-db-snapshot --db-snapshot-identifier test-rds01-not-encrypted --db-instance-identifier test-rds01-not-encrypted
    ```
5.  And once the snapshot _test-rds01-not-encrypted_ is available, copy the content to a new encrypted one _test-rds01-encrypted_ using a new KMS key or the region and account specific default one:
    ```
    $ aws rds copy-db-snapshot --source-db-snapshot-identifier test-rds01-not-encrypted --target-db-snapshot-identifier test-rds01-encrypted --kms-key-id arn:aws:kms:us-east-1:03257******:key/016de233-693e-4e9c-87e8-******
    ```
6.  Note that our original RDS instance _test-rds01_ is still running and available to end users, we are simply building up a large Seconds_Behind_Master. Once the copy is completed, we can start a new RDS instance _test-rds01-encrypted_ in the same subnet of the original RDS instance _test-rds01_
    ```
    $ aws rds restore-db-instance-from-db-snapshot --db-instance-identifier test-rds01-encrypted --db-snapshot-identifier test-rds01-encrypted --db-subnet-group-name test-rds
    ```
7.  After waiting for the new instance to be available, let us make sure that the new and original instances share the same security group and that that TCP traffic for MySQL is enabled inside the security group itself. Almost there.
8.  We can now connect to the new encrypted standalone instance _test-rds01-encrypted_ reset the external master to make it a MySQL replica of the original one.
    ```
    mysql> CALL mysql.rds_set_external_master (
    -> ' test-rds01.cqztvd8wmlnh.us-east-1.rds.amazonaws.com'
    -> , 3306
    -> ,'rdsmaster'
    -> ,'MyDummyPwd'
    -> ,'mysql-bin-changelog.275872'
    -> ,3110315
    -> ,0
    -> );
    
    Query OK, 0 rows affected (0.03 sec)
    ```
9.  And we can finally start the encrypted MySQL replication on _test-rds01-encrypted_
    ```
    mysql> CALL mysql.rds_start_replication;
    +-------------------------+
    | Message |
    +-------------------------+
    | Slave running normally. |
    +-------------------------+
    
    1 row in set (1.01 sec)
    ```
10.  We can now check the Slave_IO_State calling show slave status. Once the database catches up —Seconds_Behind_Master is down to zero — we have finally a new encrypted _test-rds01-encrypted_ instance in sync with the original unencrypted _test-rds01_ RDS instance.
11.  We can now restart the replica on the unencrypted RDS read replica _test-rds01-not-encrypted_ that is still in a stopped status in the very same way to make sure that the binary logs on the master get finally purged and do not keep accumulating.
    ```
    mysql> CALL mysql.rds_start_replication;
    +-------------------------+
    | Message |
    +-------------------------+
    | Slave running normally. |
    +-------------------------+
    
    1 row in set (1.01 sec)
    ```
12.  It is is time to promote the read replica and have our application switching to the new encrypted _test-rds01-encrypted_ instance. Our downtime starts here and as a very first step we want to make _test-rds01-encrypted_ a standalone instance calling the RDS procedure:
    ```
    CALL mysql.rds_reset_external_master
    ```
13.  We can now point our application to the new encrypted _test-rds01-encrypted_ or we can alternatively rename our RDS instances to minimize the changes. Let's go with the swapping cname approach:
    ```
    aws rds modify-db-instance --db-instance-identifier test-rds01 --new-db-instance-identifier test-rds01-old --apply-immediately
    ```
14.  and once the instance is in available state (usually 1-2 minutes) again:
    ```
    $aws rds modify-db-instance --db-instance-identifier test-rds01-encrypted --new-db-instance-identifier test-rds01 --apply-immediately
    ```
    We are now ready for the final cleanup, starting with the now useless _test-rds01-not-encrypted_ read replica.
15.  Before deleting the old not encrypted _test-rds01-old_, make sure you don't need to keep the backups anymore: on switching the instance your N days retention policy on automatic backups is now gone. It is usually better to stop (not delete) the old unencrypted _test-rds01-old_ instance until the N days are passed and the new encrypted _test-rds01_ instance has the same number of automatic snapshots.
16.  Done! You can now enjoy your new encrypted RDS instance _test-rds01_

To recap
--------

Downtime is not important? Create an encrypted snapshot and create a new RDS instance. Otherwise you can use MySQL replication to create the encrypted RDS while your instance in running and swap them when you are ready.