---
title: "Exploring Databases on Containers with Percona Server for MySQL"
date: "2023-02-23T00:00:00+00:00"
draft: false
tags: ["Docker", "MySQL", "Volume", "Percona"]
authors:
  - edith_puclla
images:
  - blog/2023/02/0-cover.png
slug: exploring-databases-on-containers-with-mysql
---

In this blog, we will explore databases on containers. We will use Docker as a container engine tool and [Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) as a database administration tool. Both are open source tools.

**MySQL** is a relational database management system that stores data on disk. Percona Server for **MySQL** is a fork of MYSQL, providing much more advanced features. To run it correctly, we need to know volumes because we want to “persist” the data, the most important thing in databases.

## Running a single Percona Server for MySQL container

First, let’s create a container without volumes:

![1-no-volume](/blog/2023/02/1-volume.png)

Figure 1: From Percona Server for MySQL image to a running container in Docker

The following command will create a container called percona-server-1, where we can create databases and add some data.

```bash
docker run -d --name percona-server-1 -e MYSQL_ROOT_PASSWORD=root percona/percona-server:8.0
```

Listing the image and the container:
![2-ls](/blog/2023/02/2-ls.png)

After the container is created:

- We have our base image, which is **percona/percona-server:8.0**
- The base image in Docker is read-only. We can’t modify it. It allows you to spin up multiple containers from the same image with the same immutable base.
- We can add data to our image. This new layer is readable and writable.
  If we create our database and populate it:

Accessing the detached container:

```bash
docker exec -it percona-server-1 /bin/bash
```

Connecting to the database

```bash
mysql -uroot -proot
```

Create a Database “cinema” and use it

```bash
CREATE DATABASE cinema;
USE cinema;
```

Create table movies in Database “cinema”

```bash
CREATE TABLE movies (
book_id BIGINT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(100) UNIQUE NOT NULL,
publisher VARCHAR(100) NOT NULL,
labels JSON NOT NULL
) ENGINE = InnoDB;
```

Insert data into Database “cinema”

```sql
INSERT INTO movies(title,publisher, labels)
VALUES(‘Green House’, ‘Joe Monter’, ’{“about” : {“gender”: “action”, “cool”: true, “notes”: “labeled”}}’);
```

Checking table

```sql
select \* from movies;
```

If you delete this container, everything will be deleted, too, your databases and your data because containers are temporary.
![3-image-no-volume](/blog/2023/02/3-image-no-volume.png)
Figure 2: View of the layers that are generated when we create the container. Source: Severalnines AB

## Running Multiple MySQL Containers

Now let’s see how the layers of two different containers work together.

```bash
docker run -d --name percona-server-1 -e MYSQL_ROOT_PASSWORD=root percona/percona-server:8.0
```

```bash
docker run -d --name percona-server-2 -e MYSQL_ROOT_PASSWORD=root percona/percona-server:8.0
```

Multiple containers can share the same base image, which is read-only. Each container can have its data state for reading and writing (Which is built on the top of the base image), but this state will be lost if we don’t create persistent volumes that can ve saved after the container is shut down.
![4-image-multiple-sql.png](/blog/2023/02/4-image-multiple-sql.png)
Figure 3: View the layers generated when we create two different containers. Source: Severalnines AB

As we said before, “Volumes open the door for stateful applications to run efficiently in Docker.”

## Running containers with Persistent Volumes

Now we will create a container with a persistent volume in Docker.
![5-image-volume](/blog/2023/02/5-no-volume.png)
Figure 4: From Percona Server for MySQL image to a running container in Docker with volumes

**percona-server** is the base of the image. On top of that, we have all the changes we will make in the database. When we create the volume, we link a directory in the container with a directory on your local machine or in the machine where you want to persist the data.
When you delete the container, you can attach another container to this volume to have the same data on a different container.

```bash
docker run -d --name percona-server -e MYSQL_ROOT_PASSWORD=root -v local-datadir:/var/lib/mysql percona/percona-server:8.0
```

![6-image-volume](/blog/2023/02/6-image-volume.png)
Figure 4: View of the layers that are generated when we create the container with volume.

## Backing up and restroring databases

There are two kinds of backups in databases, logical and physical backups.
We can use mysqldump to make logical backups and Percona XtraBackup, for physical backups. If we want to restore, we can use mysqldump and Percona XtraBackup, which offer much more advanced features.

## Back up

```bash
docker exec -it percona-server-backup mysqldump -uroot --password=root --single-transaction > /path/in/physical/host/dump.sql
```

## Restore

```bash
docker exec -it percona-server-restore mysql -u root --password=root < /path/in/physical/host/dump.sql
```

Now let’s share some tips to run databases on containers:

- Constantly monitor your database and host system
- Store data in a persistent volume outside the container
- Limit resource utilization, e.g., Memory, CPU
- Regularly back up the database and store the backup in a secure and separate location.
- Have a plan for database migrations and disaster recovery.

We explored how databases work on containers. Volumes are the important thing to persist the data.

What is next? Watch this fantastic talk by Peter Zaitsev [Open Source Databases on Kubernetes](https://www.youtube.com/watch?v=b_COgWA1lvk&t=145s)

Thanks for reading this! You can install Percona Server for MySQL from our [Docker Repository](https://hub.docker.com/r/percona/percona-server/tags?utm_source=percona-community&utm_medium=social&utm_campaign=edith) and if you have doubts write us in our [Percona community forum](https://forums.percona.com/?utm_source=percona-community&utm_medium=social&utm_campaign=edith).
