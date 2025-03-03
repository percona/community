---
title: "Some Notable Bugfixes in MySQL 8.0.32"
date: "2023-03-15T00:00:00+00:00"
draft: false
tags: ["MySQL", "Databases", "Open Source", "Release"]
categories: ["MySQL"]
authors:
  - aleksandra_abramova
images:
  - blog/2023/03/mysql-bugfixes.jpg
---

MySQL 8.0.32 came out recently and had some important bugfixes contributed by Perconians. Here is a brief overview of the work done.

## Inconsistent data and GTIDs with mysqldump

Marcelo Altmann (Senior Software Engineer) fixed the bug when data and GTIDs backed up by mysqldump were inconsistent. It happened when the options --single-transaction and --set-gtid-purged=ON were both used because GTIDs on the server could have already increased between the start of the transaction by mysqldump and the fetching of GTID_EXECUTED. Marcelo developed a patch, and it was partially included in the release. Now, in MySQL 8.0.32, a FLUSH TABLES WITH READ LOCK is performed before fetching GTID_EXECUTED, to ensure its value is consistent with the snapshot taken by mysqldump. However, Percona Server for MySQL includes the entire patch, which does not require FLUSH TABLE WITH READ LOCK to work.

Marcelo also corrected the issue when the MySQL server [exits on ALTER TABLE created an assertion failure: dict0mem.h:2498:pos < n_def](https://perconadev.atlassian.net/browse/PS-8303).

## Fixing garbled UTF characters

Kamil Holubicki (Senior Software Engineer) proposed a patch to fix garbled UTF characters in SHOW ENGINE INNODB STATUS. It happened because the string was truncated, and UTF characters (which are multibyte) were cut in the middle which caused garbage at the end of the string.

## Duplicate table space objects in 5.6 to 8.0 upgrade

Rahul Malik (Software Engineer) investigated and fixed an issue when an 8.0 upgrade from MySQL 5.6 crashed with Assertion failure. It happened due to a duplicate table space object. All SYS_* tables are loaded, and then their table IDs are changed. Some SYS tables like SYS_ZIP_DICT, VIRTUAL can have ids > 1024 (say, 1028). 

Changing table_ids of SYS_FIELDS from 4 to 1028 will conflict with the table_ids of those existing SYS_ZIP_DICT/VIRTUAL which haven't been shifted by 1024 yet and are currently loaded with 1028. Hence, we need to change the IDs of that SYS tables in reverse order to fix it. So in the example above, SYS_FIELD is the first shift to 1028+1024, and then SYS_FIELD changes to 1028 to avoid conflicts.

## Why open source databases matter

Great work by Marcelo, Kamil, Rahul, and everybody else who contributed to the MySQL 8.0.32 release. 

This is why open source databases are so important. We can all help improve MySQL, and those improvements benefit all users of MySQL. 

Percona is proud to be part of the MySQL community, and we hope you’ll join us in improving MySQL and its surrounding software. Check out our [contributing page](https://percona.community/contribute/) to find ways to contribute! 


