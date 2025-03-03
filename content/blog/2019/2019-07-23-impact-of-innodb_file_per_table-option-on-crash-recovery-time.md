---
title: 'Impact of innodb_file_per_table Option On Crash Recovery Time'
date: Tue, 23 Jul 2019 13:34:14 +0000
draft: false
tags: [ 'MySQL', 'MySQL', 'MySQL Crash Recovery', 'Open Source Databases']
authors:
  - timur_solodovnikov
images:
  - blog/2019/07/logo-mysql-170x115.png
slug: impact-of-innodb_file_per_table-option-on-crash-recovery-time
---

Starting at version MySQL5.6+ by default innodb_file_per_table is enabled and all data is stored in separate tablespaces. It provides some [advantages](https://dev.mysql.com/doc/refman/5.7/en/innodb-multiple-tablespaces.html). 

![MySQL Logo](blog/2019/07/logo-mysql-170x115.png) 

I will highlight some of them:

*   You can reclaim disk space when truncating or dropping a table stored in a file-per-table tablespace. Truncating or dropping tables stored in the shared [system tablespace](https://dev.mysql.com/doc/refman/5.7/en/glossary.html#glos_system_tablespace "system tablespace") creates free space internally in the system tablespace data files ([ibdata files](https://dev.mysql.com/doc/refman/5.7/en/glossary.html#glos_ibdata_file "ibdata file")) which can only be used for new InnoDB data.
*   You can store specific tables on separate storage devices, for I/O optimization, space management, or backup purposes.
*   You can monitor table size at a file system level without accessing MySQL.
*   Backups taken with [Percona XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) takes less space (compared with the physical backup of ibdata files)

### Problem

There are disadvantages [described](https://dev.mysql.com/doc/refman/5.7/en/innodb-multiple-tablespaces.html) on MySQL man page but I found another one that is not mentioned: if you have a huge number of tables, the crash recovery process may take a lot of time. During crash recovery the MySQL daemon scans .ibd files:
```
2019-07-16 21:00:04 6766 [Note] InnoDB: Starting crash recovery.
2019-07-16 21:00:04 6766 [Note] InnoDB: Reading tablespace information from the .ibd files...
# Started at Jul 16 23:46:52:
Version: '5.6.39-83.1-log' socket: ......
```
During startup time I checked MySQL behavior and found that MySQL opens files one by one. In my test case it was 1400000+ tables and it took 02:46:48 just to scan ibd files. 

To prevent such a long downtime we decided to move all the tables to shared tablespaces.

### Solution – moving tables to shared tablespaces

1.  Make sure that you have enough space on disk.
2.  Modify my.cnf and add the files.
3.  Restart MySQL and wait until it creates the data files.
4.  Move your InnoDB tables to shared tablespaces.

You can use this script:
```
# Get table list that stored in own tablespace (SPACE>0)
mysql -NB information_schema -e "select NAME from INNODB_SYS_TABLES WHERE name not like 'SYS_%' AND name not like 'mysql/%' AND SPACE > 0" | split -l 30000 - tables;

# Generate SQL script
for file in `ls tables*`;
do
perl -e '$curdb=""; while(<STDIN>) {chomp; ($db,$table) = split(///); if ($curdb ne $db ) { print "USE $db;n"; $curdb=$db; } print "ALTER TABLE $table engine=innodb;n"; }' < $file > $file.SQL;
done

# Apply files $file.SQL ( you can use parallel execution ) :
cat<<EOF>convert.sh
file=$1
mysql < ${file}
EOF

# Do not forget to fix my.cnf
mysql -e "set global innodb_file_per_table = 0"
chmod +x convert.sh
# run 10 parallel threads
ls tables*.SQL | xargs -n1 -P10 ./convert.sh
```
What the script does:

1.  Retrieves all tables that are occupying their own tablespace
2.  Generates SQL code in this pattern USE DB_X; ALTER TABLE TBL_Y engine=innodb;
3.  Applies the SQL scripts in parallel.

After changing file_per_table to 0 and moving the InnoDB tables:
```
2019-07-17 22:16:47 976 [Note] InnoDB: Reading tablespace information from the .ibd files...
2019-07-17 22:25:45 976 [Note] mysqld: ready for connections.
```

### Conclusion

Using the default value of innodb_file_per_table (ON) is not always a good choice. In my test case: 4000+ databases, 1400000+ tables. I reduced recovery time from 02:46:48 to 00:08:58 seconds. That's 18 times less! Remember, there is no "golden my.cnf config", and each case is special. Optimize MySQL configuration according to your needs. 

_--_ 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource, please **test** ideas before applying them to your production systems, and **always **secure a working back up._ 

_Cartoon source [https://imgur.com/](https://imgur.com/)_