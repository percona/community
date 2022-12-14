---
title: "How To Generate Data With Pagila in Percona Distribution for PostgreSQL"
date: "2022-12-13T00:00:00+00:00"
draft: false
tags: ["Docker", "PostgreSQL", "Pagila", "Database"]
authors:
  - edith_puclla
images:
  - blog/2022/12/percona-pagila.png
slug: how-to-generate-data-with-pagila-in-percona-distribution-for-postgresql
---

Have you ever faced the need to generate test data for your Postgres database? I am sure you have! This blog post will guide you step-by-step through one of the many ways to get it fast and easy. That will leave you plenty of time to focus on queries. No need to spend time creating your data generation scripts!

For this guide, we will use [Pagila](https://github.com/devrimgunduz/pagila), a tool that provides a standard schema that we can use for examples in books, tutorials, articles, samples, etc. The project is open source; you can clone it and start to run the queries. With Pagila, we will create all schema objects and insert the data into our tables.

We will use [Percona Distribution for PostgreSQL](https://www.percona.com/software/postgresql-distribution) 12.13 or higher as a database. It is an easy but powerful way to implement an enterprise-grade, fully open source PostgreSQL environment.

Let's start it!

## Requirements

- Docker
  - You can install Docker by following this [guide](https://docs.docker.com/engine/install/ubuntu/).
  - Manage Docker as a non-root user: **_sudo usermod -aG docker $USER_**

## Installing Percona Distribution for PostgreSQL

1. On your terminal, pull the Percona Distribution for PostgreSQL image. I am using the 12.13 version.

```bash
docker pull perconalab/percona-distribution-postgresql:12.13
```

2. Run Percona Distribution PostgreSQL container. You must specify POSTGRES_PASSWORD as a non-empty value for the superuser.

```bash
docker run --name percona-postgres -e POSTGRES_PASSWORD=secret -d perconalab/percona-distribution-postgresql:12.13
```

## Using Pagila to Generate Data

1. Clone the Pagila GitHub repository.

```bash
git clone https://github.com/devrimgunduz/pagila
```

2. Enter in the Percona Distribution Postgresql container.

```bash
docker exec -it  percona-postgres psql -U postgres
```

3. Create a database called perconadb

```bash
CREATE DATABASE perconadb;
\q
```

4. Create all schema objects (tables, etc.):

```bash
cd pagila
```

We will execute the script pagila-schema.sql inside percona-postgres container. The script will create the schemas objects like tables, views, functions, and constraints

```bash
cat pagila-schema.sql | docker exec -i percona-postgres psql -U postgres -d perconadb
```

![Output](blog/2022/12/pagila-schema-output.png)

5. Insert all data.
   We will execute pagila-data.sql script inside the container to insert data in all the tables we created before.

```bash
cat pagila-data.sql | docker exec -i percona-postgres psql -U postgres -d perconadb
```

![Output](blog/2022/12/pagila-data-output.png)

6. Validate the data; let’s check if the tables were created and if it is populated with data.

```bash
docker exec -it percona-postgres psql -U postgres
\c perconadb
\dt

```

![Output](blog/2022/12/dt-output.png)

```postgresql
SELECT * FROM inventory;
```

![Output](blog/2022/12/inventory-output.png)

You are ready! The data is there and ready to be used.
You can refer to the official documentation of [Percona Distribution for PostgreSQL](https://www.percona.com/software/postgresql-distribution) if you want to know the entire collection of tools to help you manage your PostgreSQL database system.
You can check [Pagila](https://github.com/devrimgunduz/pagila) open source project to generate data for Postgres.
