---
title: "Using the JSON data type with MySQL 8"
date: "2023-03-13T00:00:00+00:00"
draft: false
tags: ["json", "mysql", "Databases", "Percona", "Open Source"]
authors:
  - edith_puclla
images:
  - blog/2023/03/13-cover-change.jpg
slug: using-the-json-data-type-with-mysql-8
---

If you are a mobile app, frontend, backend, or game developer, you use data types such as string, numeric, or DateTime. You also know that since the advent of non-relational databases (NoSQL) such as **MongoDB**, which, by not being tied to a traditional **SQL schema**, do reading and writing on databases much faster. But **MySQL** showed that storing the JSON (JavaScript Object Notation) data type could also improve the speed of reading and writing relational databases.

This post will explore the JSON Data type in [Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server).

One of the key features of **Percona Server** is support for **JSON** data type, which allows for the storage of JSON documents within MySQL. It allows for more flexible and efficient storage of semi-structured data (​​which is more human-readable ) within a relational database.

We will install **Percona Server for MySQL** in a Docker container to make basic operations for inserting, modifying, and removing JSON data types.

To start, we will bring version 8.0 of Percona Server for MySQL; the name of this image in Docker Hub is percona-server. You will need Docker; if you don't have it installed, follow the official [Docker documentation](https://docs.docker.com/engine/install/).

```bash
docker pull  percona/percona-server:8.0
```

We will run the container for **Percona Server for MySQL**, call our container percona-server and pass in an environment variable called **MYSQL_ROOT_PASSWORD**; This variable specifies a password that is set for the MySQL root account.

```bash
docker run -d \
  --name percona-server \
  -e MYSQL_ROOT_PASSWORD=root \
  percona/percona-server:8.0
```

After confirming that our container is running with "docker ps," we can enter our Percona Server for MySQL container to start executing commands.

```bash
docker exec -it percona-server /bin/bash
```

The Percona Server for MySQL database is already running, and we will proceed to connect to it:

```bash
mysql -uroot -p
```

Use **root** as a password.

Create the database called **cinema**

```bash
CREATE DATABASE library;
USE library;
```

Create a table called **books**

```bash
CREATE TABLE books (
  book_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(100) UNIQUE NOT NULL,
  publisher VARCHAR(100) NOT NULL,
  labels JSON NOT NULL
) ENGINE = InnoDB;
```

## Insert JSON type into books table

```bash
INSERT INTO books(title,publisher, labels)
VALUES('Green House', 'Joe Monter', '{"about" : {"gender": "action", "cool": true, "notes": "labeled"}}');

INSERT INTO books(title,publisher, labels)
VALUES('El camino', 'Daniil Zotl', '{"about" : {"gender": "documental", "cool": true, "notes": "labeled"}}');
```

```bash
select * from books;
```

As you can see, JSON is a more flexible data type than what you might be used to when working with data in **MySQL**.

## Select with JSON_EXTRACT

```bash
SELECT title, JSON_EXTRACT(labels, '$.about.notes') AS Notes FROM books;
A shortcut of JSON_EXTRACT is “->”
SELECT title, labels->'$.about.notes' AS Notes FROM books;
```

The short operator -> provides the same functionality as JSON_EXTRACT

```bash
SELECT titulo, etiquetas->'$.acerca.genero' AS Genero FROM books;
```

## Updating JSON type records

```bash
UPDATE books SET labels = JSON_REPLACE(labels, '$.about.gender', 'romance') WHERE title = 'the roses';

UPDATE books SET labels = JSON_REPLACE(labels, '$.about.notes', 'not labeled') WHERE title = 'the roses';
```

```bash
select * from books;
```

## Deleting a JSON record

```bash
DELETE FROM books WHERE book_id = 1 AND JSON_EXTRACT(labels, '$.about.gender') = "documental";
```

## Deleting a value inside a JSON structure

```bash
UPDATE books SET labels = JSON_REMOVE(labels, '$.about.notes') WHERE book_id = 2;
```

You can use these fundamental operations to manage JSON data types in Percona Server MySQL. This allows for more flexible and efficient data modeling and querying for applications that work with JSON data. How will that work in an application? Keep an eye out, I’ll be following this up with a blog about an application using JSON data in MySQL very soon.

Get more about Percona Server for MySQL documentation in our [official documentation](https://www.percona.com/software/mysql-database/percona-server). And if you want to know why JSON is the preferred format for many developers and why it's so popular, check out [David Stokes' blog: JSON and Relational Databases – Part One](https://www.percona.com/blog/json-and-relational-databases-part-one)
