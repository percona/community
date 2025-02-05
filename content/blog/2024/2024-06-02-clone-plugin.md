---
title: "Take a Clone it will last longer"
date: "2024-06-02T00:00:00+00:00"
tags: ['Percona', 'opensource', 'clone', 'replication','MySQL',]
categories: ['MySQL']
description: "Want to learn more about MySQL and Cloning?"
authors:
  - wayne
images:
  - blog/2024/06/dna-microscopic-view.jpg
---
So cloning is a great subject. I mean we clone sheep, we can clone human organs in time we might be able to clone humans,
but thats a topic for scientist and philosophers.

**What is MySQL Replicaion:**

The MySQL clone plugin can be used to replicate data from a MySQL server to another MySQL server, and it supports replication. The cloning process creates a physical snapshot of the data, including tables, schemas, tablespaces, and data dictionary metadata. It tracks replication coordinates from the source server and transfers them to the replica, which allows replication to begin at a consistent position in the replication stream. This data includes the binary log position (filename, offset) and the gtid_executed GTID set. The replication metadata repositories are also copied during the cloning operation.

The clone plugin that was released with MySQL Version 8.0.17. Its quick and very easy to setup. You can use it for so many different solutions. I've listed some common ones below, but I know that there are many more use cases.

1. Create a new replica.
2. Recover a replica which is out of sync with the primary.
3. Quickly deploy MySQL servers with data set already in place.

In this article I will cover the basics of setting up and running a clone from and existing MySQL server. I will be using MySQL version 8.0.36.

## Prepare the Source Server

1. Install the clone plugin.
2. Create a clone user.

**Install Clone plugin**

```
source > INSTALL PLUGIN clone SONAME 'mysql_clone.so';
```

Verify the clone plugin was installed.

```
source > show plugins;
```

![clone image 1](blog/2024/06/clone-plugin-img1.png)

**Create Clone User**

Now we need to create a user to run the clone process. I highly suggest you create a user for the cloning. Please don't use an ID with full admin rights. Create a user with the least amount of privileges needed.

```
source > CREATE USER 'clone_user'@'%' IDENTIFIED BY 'S3k3rtPassWd';
source > GRANT BACKUP_ADMIN ON *.* TO 'clone_user'@'%';
```

Verify your new clone user.

```
source > show grants for clone_user;
```

![clone image 2](blog/2024/06/clone-plugin-img2.png)

Preparation on the source server is complete. Lets move on to the clone.

## Prepare the Clone Server

1. We need to start by installing the clone plugin.
2. Then we need to define the source that clone will be based on.

**Install plugin**

```
clone > INSTALL PLUGIN clone SONAME 'mysql_clone.so';
```

Verify the clone plugin was installed.

```
clone > show plugins;
```

![clone image 1](blog/2024/06/clone-plugin-img1.png)

**Define Source Server**

You can use the source host name or host IP address.

```
clone > SET GLOBAL clone_valid_donor_list='SOURCE_HOSTNAME:3306';
```

## Start and monitor the cloning process

We are now ready to kick off the cloning.

```
clone > CLONE INSTANCE FROM clone_user@SOURCE_HOSTNAME:3306 IDENTIFIED BY 'S3k3rtPassWd';
```

Cloning should start now. If you have any issues, check your log files and very the steps above. Now that the cloning is running we can monitor the cloning process using this command.

```
clone > SELECT * FROM performance_schema.clone_progress\G
```

As you can see in the output below, that the cloning has completed DROP DATA and is now working on FILE COPY.

![clone image 3](blog/2024/06/clone-plugin-img3.png)

## Observations

Just recently I worked with a customer who moved a 5.6TB database from a Galera Cluster to standard MySQL replication. The data was moved from the source to replicas in two different locations. Timings are detailed below.

1. Source to Replica in same location: 5.6TB in approxmently 50 mins.
    - 112GB per minute.
2. Source to Replica in different geographic locations: 5.6TB in approxmently 1 hour and 45 mins.
    - 53.33GB per minute.

MySQL Clone Plugin's robust performance and efficiency in managing large data transfers, making it an excellent tool for environments requiring quick and reliable data replication.

## Summary

The MySQL Clone Plugin offers several benefits, including:

1. Fast Data Copying:
    - Enables rapid cloning of MySQL instances, facilitating quick data replication and environment setup.
2. Consistent Data State:
    - Ensures data consistency during cloning, avoiding issues that can arise from manual copying or inconsistent states.
3. Reduced Downtime:
    - Minimizes downtime during cloning operations, crucial for maintaining service availability.
4. Ease of Use:
    - Simplifies the cloning process through straightforward commands, reducing the complexity for database administrators.
5. Automated Cloning Process:
    - Automates many steps involved in the cloning process, reducing the potential for human error and increasing efficiency.

## Reference

[The Clone Plugin](https://dev.mysql.com/doc/refman/8.0/en/clone-plugin.html)

[Image by kjpargeter on Freepik](https://www.freepik.com/free-photo/dna-microscopic-view_854596.htm#fromView=search&page=1&position=1&uuid=b58a4350-e1ba-44f8-9c0a-0c4498e84ac5)
