---
title: "Backups for MySQL With mysqldump"
date: "2023-03-10T00:00:00+00:00"
draft: false
tags: ["MySQL", "Backup"]
authors:
  - mario_garcia
images:
  - blog/2023/03/backup.jpg
slug: backups-for-mysql-with-mysqldump
---

![Backup](/blog/2023/03/backup.jpg "Backup by Nick Youngson CC BY-SA 3.0 Pix4free")

## Basic Usage
[mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) is a client utility that can be used for doing logical backups. It will generate the necessary SQL statements to reproduce the original database.

The following statements are some common uses of mysqldump:

1. `mysqldump -u username -p database_name [table_name] > dump.sql`
2. `mysqldump -u username -p --databases db1_name db2_name > dump.sql`
3. `mysqldump -u username -p --all-databases > dump.sql`

The first example is for backing up a single database. If you need to back up some specific tables instead of the whole database, write their names, space-separated.

With the `--databases` option, you can back up two or more databases, their names must be space separated.

To back up all the databases in your MySQL server, just append the `--all-databases` option.

The `dump.sql` file doesn’t contain the create database SQL statement. If you need it, add it with the `-B` option. This is unnecessary if you’re running `mysqldump` with the `--databases` and `--all-databases` options.

Ignoring tables when backing up a database is also possible with the `--ignore-tables` option.

```
$ mysqldump -u username -p database_name --ignore-tables=database_name.table1 > database_name.sql
```

If you need to ignore more than one database, just use the option as many times as needed.

```
$ mysqldump -u root -p database_name --ignore-table=database_name.table1 --ignore-table=database_name.table2 > database_name.sql
```

## Schema Backup
In case you need to backup only the schema of your database with no data, run mysqldump with the `--no-data` option:

```
$ mysqldump -u username -p database_name --no-data > dump.sql
```

You can also backup the schema while running `mysqldump` with the `--databases` and `--all-databases` options. 

```
$ mysqldump -u username -p --all-databases --no-data > dump.sql
```

```
$ mysqldump -u username -p --databases db1_name db2_name --no-data > dump.sql
```

## Data Restore
To restore the databases in your `dump.sql` file, run the following command:

```
$ mysqldump -u root -p < dump.sql
```

If you need to restore a single database from the complete backup, you can do it by running any of the following statements:

```
$ mysqldump -u root -p -o database_name < dump.sql
```

```
$ mysqldump -u root -p --one-database database_name < dump.sql
```

In both cases, the database must exist in your MySQL server, as it only will restore the schema and the data.

## Conditional Backup
If you need to create a backup that contains data that matches a condition, you can use  a `WHERE` clause with mysqldump.

You can use a single where condition:

```
$ mysqldump database_name table_name --where="id > 500" > dump.sql
```

Or multiple conditions:

```
$ mysqldump database_name users --where="id > 500 and disabled = 0" > dump.sql
```

As explained [here](https://mysqldump.guru/how-to-use-a-where-clause-with-mysqldump.html) in the [mysqldump.guru](https://mysqldump.guru/) website.

For example, in a database with the following schema, built from the [Movienet](https://movienet.github.io/) dataset:

![Movienet Database](/blog/2023/03/movienet-model.png "Movienet Database")

If you want to back up the movies produced in a specific country, like Mexico, a way to do it is by running mysqldump with a `WHERE` clause.

```
$ mysqldump -u root -p movienet movies --where=”country = 22” > dump.sql
```

`22` is the `country_id` of Mexico in this particular database, created using [this Python script](https://github.com/mattdark/json-mysql-importer).

You can also get those values by executing the following SQL statement:

```
select movies.movie_id, movies.title, countries.name as country from movies inner join countries on movies.country = countrie
s.country_id and movies.country = '22';
```

```
+-----------+-----------------------------------------------------------+---------+
| movie_id  | title                                                     | country |
+-----------+-----------------------------------------------------------+---------+
| tt0047501 | Sitting Bull (1954)                                       | Mexico  |
| tt0049046 | Canasta de cuentos mexicanos (1956)                       | Mexico  |
| tt0076336 | Hell Without Limits (1978)                                | Mexico  |
| tt0082048 | El barrendero (1982)                                      | Mexico  |
| tt0082080 | Blanca Nieves y sus 7 amantes (1980)                      | Mexico  |
| tt0083057 | El sexo de los pobres (1983)                              | Mexico  |
| tt0110185 | El jardín del Edén (1994)                                 | Mexico  |
| tt0116043 | De jazmín en flor (1996)                                  | Mexico  |
| tt0121322 | El giro, el pinto, y el Colorado (1979)                   | Mexico  |
| tt0133354 | Algunas nubes (1995)                                      | Mexico  |
| tt0207055 | La risa en vacaciones 4 (TV Movie 1994)                   | Mexico  |
| tt0208889 | To and Fro (2000)                                         | Mexico  |
| tt0211878 | La usurpadora (TV Series 1998– )                          | Mexico  |
| tt0220306 | El amarrador 3 (1995)                                     | Mexico  |
| tt0229008 | El vampiro teporocho (1989)                               | Mexico  |
```

## Skipping Databases
There’s no option for `mysqldump` to skip databases when generating the backup, but here’s a solution that could work for you:

```
DATABASES_TO_EXCLUDE="db1 db2 db3"
EXCLUSION_LIST="'information_schema','mysql'"
for DB in `echo "${DATABASES_TO_EXCLUDE}"`
do
    EXCLUSION_LIST="${EXCLUSION_LIST},'${DB}'"
done
SQLSTMT="SELECT schema_name FROM information_schema.schemata"
SQLSTMT="${SQLSTMT} WHERE schema_name NOT IN (${EXCLUSION_LIST})"
MYSQLDUMP_DATABASES="--databases"
for DB in `mysql -u username -p -ANe"${SQLSTMT}"`
do
    MYSQLDUMP_DATABASES="${MYSQLDUMP_DATABASES} ${DB}"
done
MYSQLDUMP_OPTIONS="--routines --triggers"
mysqldump -u username -p ${MYSQLDUMP_OPTIONS} ${MYSQLDUMP_DATABASES} > MySQLDatabases.sql
```

The above BASH script will generate the backup of your MySQL server excluding the `information_schema` and `mysql` databases, listed in the `EXCLUSION_LIST` variable, as well as the databases of your choice in the `DATABASES_TO_EXCLUDE` variable. 

Don’t forget to add the databases you want to exclude to the `DATABASES_TO_EXCLUDE` variable, replace the `username`, in both `mysql` and `mysqldump` commands, and add the required options to the `MYSQLDUMP_OPTIONS` variable.

## Security Considerations
Some of the common questions in [our forum](https://forums.percona.com) are about how to do a partial restoration from a complete backup. For example, when you back up a database with `mysqldump`, you will get the statements for creating the schema of the database and inserting the data from your backup. 

If you only need the schema, you can run mysqldump with the --no-data option. But if you need to restore the schema of a specific database from a complete backup, I found an interesting solution:

```
cat dump.sql | grep -v ^INSERT | mysql -u username -p
```

The above command will restore the schema of your database, skipping the SQL statements for inserting the data. It works well when you backup a single database, but there’s no reason to use it as you can get the schema with the --no-data option, instead of removing the inserts.

What happens if you try to run this command with a backup that includes all the databases in your server? You must be careful as this will try to overwrite the system schema in the `mysql` database which is dangerous. This database store authentication details and overriding the data will make you lose access to your server.

If you don’t need to backup the `mysql` database, run `mysqldump` with the `--databases` option to specify which databases you require or use the script shared in the [Skipping Databases](#skipping-databases) section.

## Conclusion
Through this blog post you learned how to use mysqldump for backing up the databases in your MySQL server as well as some recommendations while using this tool. For advanced usage of mysqldump you can check [this article](https://www.percona.com/blog/the-mysqlpump-utility/) in our blog.