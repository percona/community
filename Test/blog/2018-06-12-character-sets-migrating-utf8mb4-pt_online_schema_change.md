---
title: 'Character Sets: Migrating to utf8mb4 with pt_online_schema_change'
date: Tue, 12 Jun 2018 11:27:57 +0000
draft: false
tags: ['david-berube', 'character sets', 'collation', 'conversion', 'encoding', 'migration', 'MySQL']
authors:
  - david_berube
images:
  - blog/2018/04/problem.jpg
---

Modern applications often feature the use of data in many different languages. This is often true even of applications that only offer a user facing interface in a single language. Many users may, for example, need to enter names which, although using Latin characters, feature diacritics; in other cases, they may need to enter text which contains Chinese or Japanese characters. Even if a user is capable of using an application localized for only one language, it may be necessary to deal with data from a wide variety of languages. 

Additionally, increased use of mobile phones has lead to changes in communications behaviour; this includes a vastly increased use of standardized characters intended to convey emotions, often called "emojis" or "emoticons." Originally, such information was conveyed using ASCII text, such as ":-)" to indicate happiness - but, as noted, this has changed, with many devices automatically converting such sequences into single character "emojis." Such emojis are not typically presented as a a graphic; instead, such emojis are now a standard part of Unicode encoding. 

Since Unicode is a long established standard, and since MySQL has had support for Unicode for quite some time, one would imagine it would be seamless and easy to include them in your application. 

Unfortunately, there are several problems that may complicate that path for many users - first, though, let's discuss some background, so that we can fully understand the problem.

What is encoding?
-----------------

"Encoding," as you may already be aware, refers to the mapping of characters to binary values - or "code points". One of the oldest standard still in use is ASCII; in this encoding, the binary sequence "100 0001" is equivalent to the uppercase character "A". Many characters cannot be encoded into US-ASCII; in fact, since it uses only seven bytes per character, it can store only 128 different code points. Some of these code points are characters - like the "A" already mentioned, and others carry alternative meanings, such as for formatting. 

For example, "000 1001" represents a "tab" in US-ASCII. Later, ASCII coding was replaced with various 8-bit encodings, which could hold more different code points - but it was ultimately a standard called Unicode which dethroned ASCII. Unicode actually encompasses a number of different encodings - but it is UTF8 which is the most important, and that's what we will discuss in this post. 

"Collation" is a related concept; this refers to how characters are sorted. This may, at first, seem simple and logical. However, in practice, it can be more complicated. For example, some poorly programmed systems inadvertently sort in a "case sensitive manner" when "case insensitive" would be more appropriate. Such a system may sort "b,a,B,A,c" as "A,B,a,b,c" - whereas it may be more desirable to sort it as "A,a,B,b,c." This is an example of differing collations. In languages other than English, there may be more than one reasonable way to sort a list of strings; this is particularly true in languages that do not use an alphabet, such as Chinese or Japanese.

Why can encoding be a problem in MySQL?
---------------------------------------

Unicode adoption was by no means universal, and by no means quick. For a very long time, MySQL's default encoding was latin1; this supports basic English text and common punctuation reasonably well. However, it has limited support for other languages, and it does not support modern emoji characters. Eventually, MySQL very reasonably changed it's default to UTF8 - which, one would imagine, fixed the issue for many people... except that existing databases were not converted, and many databases still, to this day, have some, or even all, tables encoded as latin1 - not as a conscious choice, but simply as a relic of an older time. 

Additionally, "utf8" encoding in MySQL does not, in fact, mean standard UTF8. Standard UTF8 encoding involves a variable number of bytes per character, with a maximum of four bytes per character; most characters, however, use three or fewer. MySQL, for legacy technical reasons, supports a maximum of three bytes - which, regretably, means that MySQL's "utf8" encoding does not work with four byte characters, which include Emojis and some mathematical symbols. 

As a result, many databases are using MySQL's "utf8" encoding or it's older "latin1" default. In both cases, you may receive vexing "Incorrect string value: " errors when users attempt to enter non-support characters.

Changing encoding and collations
--------------------------------

Both encoding and collation can be set on a per-column level in MySQL. You can also set this value on a per-table level, which sets the default for new columns; further, you can set it on the database level, which sets the default for new tables. Finally, you can set it at the server level, which specifies a default for new databases. 

Let's walk through changing the encoding and collation for the MySQL sample database "sakila". You can download this database at the following URL: 

[https://dev.mysql.com/doc/index-other.html](https://dev.mysql.com/doc/index-other.html) 

First, let's start by examining the "actor" table:
```
mysql> SHOW CREATE TABLE actorG
*************************** 1. row ***************************
Table: actor
Create Table: CREATE TABLE `actor` (
`actor_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
`first_name` varchar(45) DEFAULT NULL,
`last_name` varchar(45) NOT NULL,
`last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`actor_id`),
KEY `idx_actor_last_name` (`last_name`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
```
As we can see here, the encoding on this table is set to UTF8; all of the VARCHAR columns listed are also encoded as UTF8. If one of them was encoded with a different encoding, it would be listed as part of it's column definition, e.g. "`first_name` varchar(45) CHARACTER SET latin1 DEFAULT NULL" instead of "`first_name` varchar(45) DEFAULT NULL". 

To change the encoding and collation for a particular column, we can use the CHANGE COLUMN command:
```
ALTER TABLE actor MODIFY COLUMN first_name VARCHAR(45) CHARACTER SET utf8mb4;
```
This, unsurprisingly enough, changes the character set to utf8mb4 - meaning this column can now support emojis and other 4 byte characters. Let's see what that does to our table defintion:
```
mysql> show create table actorG
*************************** 1. row ***************************
Table: actor
Create Table: CREATE TABLE `actor` (
`actor_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
`first_name` varchar(45) CHARACTER SET utf8mb4 DEFAULT NULL,
`last_name` varchar(45) NOT NULL,
`last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`actor_id`),
KEY `idx_actor_last_name` (`last_name`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
```
We can see that the "first_name" column has been changedto utf8mb4; however, the "last_name" column is still using the default character set, utf8. We can use the following command to set the default charset and convert all of the individual columns to our new character set:
```
ALTER TABLE actor CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
Note that the above command has a COLLATE clause; although we are focusing on changing encodings in this post, you can have either a CHARACTER SET cause, a COLLATE clause, or both in all of the commands we've mentioned - allowing you to change either the encoding or the collation or both at once. 

Let's see what this command does to our table definition:
```
show create table actorG
*************************** 1. row ***************************
Table: actor
Create Table: CREATE TABLE `actor` (
`actor_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
`first_name` varchar(45) DEFAULT NULL,
`last_name` varchar(45) NOT NULL,
`last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`actor_id`),
KEY `idx_actor_last_name` (`last_name`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4
1 row in set (0.00 sec)
```
As noted, MySQL only displays per-column encodings in table definitions if they are different from the default. We can see, therefore, that all of the columns are now in utf8mb4 encoding. Additionally, it only displays table level collations if they are different from the default - and since utf8mb4_general_ci is the default collation for utf8mb4, it won't display it either at the table level or the column level. (If we had changed it to a different collation - say, utf8mb4_bin or utf8mb4_unicode_ci - it would, in fact, show up.) 

At this point, we've successfully converted a single table to utf8mb4. However, this approach seems onerous for a large database - is there a better way?

Converting a database at a time with mysql_change_database_encoding
-------------------------------------------------------------------

For the purposes of this blog, I've encapsulated the logic to run the relevant commands for an entire database into a short Ruby script. You can download and install as follows:
```
git clone git@github.com:djberube/mysql_change_database_encoding.git
cd mysql_change_database_encoding
bundle
```
This command will use MySQL's INFORMATION_SCHEMA engine to get a list of all tables, and migrate them:
```
MYSQL_DATABASE=sakila MYSQL_USER=some_mysql_user MYSQL_PASSWORD=some_mysql_password ruby mysql_change_database_encoding.rb --collation utf8mb4_unicode_ci --encoding utf8mb4 --dir
ect --no-osc
Connecting to sakila
Processing database settings.
-- Setting database global settings.
Running SQL:
ALTER DATABASE `sakila` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0009s
-- Migrating without OSC
Running SQL:
ALTER TABLE `actor` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0036s
-- Migrating without OSC
Running SQL:
ALTER TABLE `address` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0670s
-- Migrating without OSC
Running SQL:
ALTER TABLE `category` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0293s
-- Migrating without OSC
Running SQL:
ALTER TABLE `city` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0400s
-- Migrating without OSC
Running SQL:
ALTER TABLE `country` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0239s
-- Migrating without OSC
Running SQL:
ALTER TABLE `customer` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0607s
.. snip...
```
I've cut the output down a bit for brevity. First, this script sets the default encoding and collation for the entire DB; then it sets it for each table using the ALTER TABLE .. CONVERT TO CHARACTER SET  command. 

You may have noticed the "migrating without OSC" lines in the output; OSC, or online schema change, is a technique for reducing the impact of database migrations on production installations. A typical technique for doing this is to create a duplicate of your table, set up triggers to keep that duplicate up to date, change the new table, and then swap them - this is sufficiently complicated that it's nontrivial to DIY, and so there's a few very nice tools available to do this. By using one of these tools, we can run schema changes in production environments while reducing the performance impact - having to lock a large table while converting it to UTF8MB4 may, indeed, take a large system down.

#### pt-online-schema-change

Percona Toolkit has a great tool for OSC, called pt-online-schema-change; the script mentioned above has builtin support for pt-online-schema-change. You can download it from here: 

[https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html](https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html) 

We can re-run our script using pt-online-schema-change by removing the "--no-osc" option and replacing it with, logically enough, a "--osc" option:
```
# MYSQL_DATABASE=sakila MYSQL_USER=some_mysql_user MYSQL_PASSWORD=some_mysql_password ruby mysql_change_database_encoding.rb --collation utf8mb4_unicode_ci --encoding utf8mb4 --direct --osc
Connecting to sakila
Processing database settings.
-- Setting database global settings.
Running SQL:
ALTER DATABASE `sakila` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-> 0.0007s
This SQL will be run using pt-online-schema-change:
CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
The following command will be run:
No slaves found. See --recursion-method if host spacepancake has slaves.
Not checking slave lag because no slaves were found and --check-slave-lag was not specified.
Operation, tries, wait:
analyze_table, 10, 1
copy_rows, 10, 0.25
create_triggers, 10, 1
drop_triggers, 10, 1
swap_tables, 10, 1
update_foreign_keys, 10, 1
Child tables:
`sakila`.`film_actor` (approx. 5462 rows)
.. snip...
```
Note that pt-online-schema-change can only be run against tables with a primary key; the mysql_change_database_encoding.rb  script will automatically fall back to directly running MySQL commands if the --direct flag is set. 

If you encounter any issues with the above script, please let me know via [http://berubeconsulting.com/](http://berubeconsulting.com/) or via Github. Pull requests are welcome.

Potential problems
------------------

Of course, there are several issues which may occur when changing your encoding or collation.

#### MySQL Version

Firstly, note that utf8mb4 support is only available in MySQL 5.5.2 or later; earlier than that, and you're limited to MySQL's nonstandard UTF8 implementation, with a maximum of three bytes per codepoint. In this case, it is generally advisable to upgrade to a recent version of MySQL - though you could, if desired, use the above approach to migrate your database to utf8 encoding.

#### Applications that need variable encoding

The second issue is that the approach detailed above - where a script automatically migrates all of the different tables - will result in every table having it's encoding and/or collation changed to the same destination encoding and collation. That's not necessarily a problem - but some applications do, indeed, make use of varying encodings for different tables and, in some cases, different columns in the same table. If so, you'd do well to use the above SQL examples as a guide, and manually create a SQL script - or a shell script that repeatedly calls pt-online-schema-change - which will do the migration for you. However, in many cases, a single encoding is both possible and desirable.

#### Key Length

Addditionally, note that maximum key lengths may be an issue for MySQL 5.6 and earlier installations. This is because earlier installations have a maximum key size limitation on indices; compared to utf8 columns, utf8mb4 columns have a higher maximum length on disk per character, and it's easy to bump into once you switch to utf8mb4. For example, many schemas have VARCHAR(255) columns - those are created by Ruby on Rails by default if one does not specify a column length - and VARCHAR(255) columns trigger this limitation. You could write a script that automatically resizes these indices or their associated columns, but I would recommend either upgrading to 5.7 or, if running 5.5 or later, enabling the innodb_large_prefix setting, which allows larger indices.

#### False positives

Finally, note that for some legacy installations, the mere fact of a column, table, or database being marked as "latin1" encoded or "utf8" encoded may not, in fact, mean that the data is actually encoded in that way; this may be because an application incorrectly marked the encoding of it's data. In that case, recovery may be complex or impossible, and will certainly be situation dependant - particularly since this issue may not effect all rows. 

Of course, to ensure that you particular application works without incident on a new encoding - and, to a lesser extent, collation - it's wise to thoroughly test any changes in a staging environment; if feasible, it's likely wise to test on a copy of the production environment as well.

Conclusion
----------

Unicode support is no longer an arcane, unapproachable topic; it's both possible and highly advisable to ensure that your application works well for international users and for more users using emojis. Such is quickly becoming not merely a value-add, but an expected part of an application's featureset, and implementing full support in your MySQL application is relatively straightforward. 

If you've found this post useful, feel free to let me know at [djberube@berubeconsulting.com](mailto:djberube@berubeconsulting.com), or via [http://berubeconsulting.com](http://berubeconsulting.com). 

Questions, comments, and reports of any inaccuracies are welcome.