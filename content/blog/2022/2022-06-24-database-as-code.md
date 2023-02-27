---
title: 'Database as Code. Not only migrations'
date: "2022-06-24T00:00:00+00:00"
draft: false
tags: ['SQL']
authors:
  - maksim_gramin
images:
  - blog/2022/6/code.jpg
slug: database-as-code
---


We are used to the Everything as Code things and we love it. But how about Database as Code? If you have just dropped your DB migrations scripts to your pipeline, then it’s great, but that’s where “Database as Code” is just getting started. In this post, I will share my view on “Database as Code” mantra.



## Everything as Code

And we will start with "Everything as Code" things. "Everything as Code" is a philosophy, 
where any IT area might be represented as a plain code. And we can work with it using standard tools and technologies (like code editors, control version systems, static analyzis etc.). And yes, indeed, there are many "Everything as Code" realizations for many areas. For example - Gitlab CI, Ansible, Markdown, etc.

And we can get all the benefits of working with Code:
- You have no more Monstrous GUI - Where you are afraid to click something wrong
- You can use Full Version Control For all your changes 
- You can put your Code to the CI/CD pipeline
- And everybody in your team is coding and using the same tools



## How about "Database as Code"?

It was a very exotic combination of words, but [Dan North](https://twitter.com/tastapod) in hist talk "[Aren't we forgetting someone?](https://speakerdeck.com/tastapod/arent-we-forgetting-someone)" proposed four simple rules for treating a database like Code:
- All database changes are scripted and automated
- All database changes are under version control
- Ability to release on demand at any time
- AND DBA should be integrated with Dev and Ops people

It's been six years, and nowadays, it's hard to find a project that doesn't follow these rules (at least the first three). There are a lot of different database migration tools and different ways to integrate it with your Version Control system and your CI/CD pipeline.
For example [Flyway](https://github.com/flyway/flyway), [Ghost](https://github.com/TryGhost/Ghost), [Sqitch](https://github.com/sqitchers/sqitch), [Skeema](https://github.com/skeema/skeema) and ofcourse [Liquibase](https://github.com/liquibase/liquibase).

And it's really great!



## DB isn't only Schema

First of all, DB is Data and Queries to Data (DML for data and metadata)

Also databases needs:
- Administration (like space managment and memory management)
- Monitoring (like metrics gathering and perfomance troubleshooting)
- Documentation
- and all this stuff
And there is a special Language for all these things.
And of course - it is SQL!

SQL is a universal language for data and metadata. And SQL first of all was made by humans for humans, not for machines.

![What is dbt](blog/2022/6/sql_everywhere.jpg)



## SQL Hell

But on the other hand we have some problems with SQL, I call it "SQL Hell" (like "JAR hell" or "DLL hell"). Our SQL-queries scattered everywhere:

- Our applicatons generate tonns of Dynamic Queries
- Many Static Queries are injected directly into the code of another program 
(like Java, Python or something else)
- or placed in configuration files (like YML, JSON or TOML)

And we can't control, test and trust these tons of SQL.



## Keep All SQL as Code

But how about dead simple idea - keep all your SQL-queries as normal code? Why not? And I have prepared some additional "Database as Code" rules:

- All changes and operations with the Database and all queries against the Database should be expressed as a plain Code. Not only DDL, DML and all other kinds of SQL - too
- Git (or anything else VCS) is a single source of truth for all your DB Code
- SQL actually is a main database language supported by almost all DBMS and storages
- Treat your SQL code (your SQL-queries) like a normal Code. SQL is a human-oriented computer language for your Data and your Database, is not a bytecode. It also needs static analysis, code review, tests and automation of it all in your CI/CD Pipeline

The full version of these rules is hosted on [GitHub](github.com/mgramin/database-as-code). Please check it out. And I will be very grateful for the stars, PR's, issues and any other feedback.



## Is There It in Wild Life?

But are there tools in real life that satisfy this rules? And our answer: "Yes, there are".



## Data Building Tool

First of all is Data Building Tool, or simply [dbt](https://github.com/dbt-labs/dbt-core). dbt is a tool for data transformation. And the main idea is very clear and very simple - you just drop sql-file with your select statements to yor repository, while dbt materializes these statements into tables and views. No boilerplate code, only SQL!

![What is dbt](blog/2022/6/what_is_dbt.jpg)

dbt provide also:
- Testing framework for you queries
- Templating with [Jinja](https://jinja.palletsprojects.com)
- Relationships management between queries
- Relationships visualization 



## Data Maping

Another example is Data Maping. Data Maping tools are usually very sophisticated tools for extracting and mapping our Data to our Data structures. It usually results in SQL code generation and performance issues.

But some tools provide to us a Query-first design. You just drop sql-file with your query to yor RepOsitory:

```sql
-- :name find_user :one
select *
  from users
 where user_id = :user_id
```

And use it from your application code:

```python
user = queries.find_user(user_id=42)
# -> { 'user_id': 42, 'username': 'mcfunley' }
```

it's very simple and predictable and no magic!

There are a lot of Query-first libraries and frameworks for different languages (e.g. [Yesql](https://github.com/krisajenkins/yesql), [HugSQL](https://github.com/layerware/hugsql), [PugSQL](https://github.com/mcfunley/pugsql), [SQLDelight](https://github.com/cashapp/sqldelight) etc).



## Project "Malewicz"

And finally, I would like to present my small experimental project based on the "Database as Code" ideas - [Malewicz](https://github.com/mgramin/malewicz).

Malewicz is Yet Another graphical SQL-client (or SQL-manager) 
for DB schema exploring and performance analysis but with some key features:
- This tool was originally designed for hacking and extending
- And you can use for that only your SQL skills (and a little bit HTML) without any boilerplate code.

Check it out on [GitHub](https://github.com/mgramin/malewicz) and try [online demo](http://malewicz.herokuapp.com)!



## Conclusion

In the database world, we already have a great universal language with marvelous history, and it's SQL. SQL allows you standardized declarative access not only to relational DB, but to non-relational DB, streaming platforms, files, clouds and so on. However, unfortunately, we often see that the SQL-code is often considered as a kind of [bytecode](https://gramin.pro/posts/sql-is-not-a-bytecode-for-data). But we say - SQL-code is a *normal* code and all SQL-code needs version control, review, testing, CI/CD and all this stuff.
