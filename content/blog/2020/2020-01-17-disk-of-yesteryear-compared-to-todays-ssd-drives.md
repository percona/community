---
title: 'Disk of Yesteryear Compared to Today’s SSD Drives'
date: Fri, 17 Jan 2020 16:48:46 +0000
draft: false
tags: ['MySQL', 'Open Source Databases', 'Percona Server for MySQL']
authors:
  - wayne
images:
  - blog/2020/01/enrico-sottocorna-HOhR-t0yZIU-unsplash.jpg
slug: disk-of-yesteryear-compared-to-todays-ssd-drives
---

![](blog/2020/01/enrico-sottocorna-HOhR-t0yZIU-unsplash.jpg)

In my [last blog post](https://www.percona.com/
community-blog/2019/08/01/how-to-build-a-percona-server-stack-on-a-raspberry-pi-3/) I showed you how to get the entire Percona “Stack" up and running on a Raspberry Pi. This time around, I would like to show the impact on performance between using an SSD hard disk and a standard hard disk. 

Disk performance is a key factor in [Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) (or any RDB platform) performance on a Raspberry Pi 4.

Test set up
-----------

Each test below was run three times per Hard Disk and I took the best of the three for comparison. Hardware

*   Raspberry Pi 4+ with 4GB ram.
*   Disk 1: USB3 Western Digital My Passport Ultra, 1TB
*   Disk 2: USB3 KEXIN 240GB Portable External SSD Drive

Hardware stayed consistent during test, except for the hard disk that were switched from KEXIN to Western Digital drive. Software

*   Raspbian Buster
*   Persona Server Version: 5.7.27-30 built from source. See the above BLOG for install instructions.
*   Sysbench 1.0.17

Sample my.cnf
```
[mysqld]
port = 3306
socket = /var/lib/mysql/mysql.sock
pid-file = /var/lib/mysql/mysqld.pid
basedir = /usr/local/mysql
datadir = /data0/mysql/data
tmpdir = /data0/mysql/tmp
general_log_file = /var/log/mysql/mysql-general.log
log-error = /var/log/mysql/mysqld.log
slow_query_log_file = /var/log/mysql/log/slow_query.log
slow_query_log = 0 # Slow query log off
lc-messages-dir = /usr/local/mysql/share
plugin_dir = /usr/local/mysql/lib/mysql/plugin
log-bin = /data0/mysql/binlog/mysql-bin
sync_binlog = 1
expire_logs_days = 5
server-id = 1
binlog_format = mixed
max_allowed_packet = 64M
max_connections = 50
max_user_connections = 40
query_cache_size=0
query_cache_type=0

innodb_data_home_dir = /data0/mysql/data
innodb_log_group_home_dir = /data0/mysql/data
innodb_log_files_in_group = 2
innodb_buffer_pool_size = 1536M
innodb_log_file_size = 64M
innodb_log_buffer_size = 8M
innodb_flush_log_at_trx_commit = 2
#innodb_flush_log_at_trx_commit = 0
innodb_lock_wait_timeout = 50
innodb_flush_method = O_DIRECT
innodb_file_per_table = 1
innodb_buffer_pool_instances = 1
skip-name-resolve=0
thread_pool_size=20
innodb_temp_data_file_path = ../tmp/ibtmp1:12M:autoextend:max:8G
```
Sysbench MySQL test prep step:
```
sysbench --db-driver=mysql —mysql-db=sbtest --oltp-table-size=500000 --oltp-tables-count=10 --threads=8 --mysql-host= --mysql-port=3306 --mysql-user= --mysql-password=
/usr/share/sysbench/tests/include/oltp_legacy/parallel_prepare.lua run
```

Test 1
------

This was done using the: KEXIN 240GB Portable External SSD Drive. Sysbench command:
```
sysbench --db-driver=mysql --mysql-db=sbtest --report-interval=2 --mysql-table-engine=innodb --oltp-table-size=500000 --oltp-tables-count=10 --oltp-test-mode=complex --threads=10 --time=150 —mysql-host= --mysql-port=3306 —mysql-user= —mysql-password= /usr/share/sysbench/tests/include/oltp_legacy/oltp.lua run
```
Output:
```
SQL statistics:
    queries performed:
        read:                            486542
        write:                           139012
        other:                           69506
        total:                           695060
    transactions:                        34753  (231.62 per sec.)
    queries:                             695060 (4632.45 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)
General statistics:
    total time:                          150.0362s
    total number of events:              34753

Latency (ms):
         min:                                   20.28
         avg:                                   43.16
         max:                                   94.32
         95th percentile:                       57.87
         sum:                              1500044.61

Threads fairness:
    events (avg/stddev):           3475.3000/368.77
    execution time (avg/stddev):   150.0045/0.01

```
As you can see the performance with the KEXIN (SSD) Drive was pretty good:
```
transactions:                        34753  (231.62 per sec.)
queries:                             695060 (4632.45 per sec.)

```

Test 2
------

This was done using the: Western Digital My Passport Ultra 1TB drive.
```
SQL statistics:
    queries performed:
        read:                            60984
        write:                           17424
        other:                           8712
        total:                           87120
    transactions:                        4356   (29.00 per sec.)
    queries:                             87120  (579.94 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          150.2160s
    total number of events:              4356

Latency (ms):
         min:                                   23.26
         avg:                                  344.75
         max:                                 1932.12
         95th percentile:                      733.00
         sum:                              1501739.03

Threads fairness:
    events (avg/stddev):           435.6000/5.71
    execution time (avg/stddev):   150.1739/0.05

```
As you can see the performance on the Western Digital Drive was really bad:
```
transactions:                        4356   (29.00 per sec.)
queries:                             87120  (579.94 per sec.)

```

### Disk IO Tests

KEXIN:
```
Operations performed:  208123 Read, 138748 Write, 443904 Other = 790775 Total
Read 3.1757Gb  Written 2.1171Gb  Total transferred 5.2928Gb  (18.066Mb/sec)
 1156.24 Requests/sec executed

Test execution summary:
    total time:                          300.0004s
    total number of events:              346871
    total time taken by event execution: 113.1569
    per-request statistics:
         min:                                  0.02ms
         avg:                                  0.33ms
         max:                                 31.07ms
         approx.  95 percentile:               0.60ms

Threads fairness:
    events (avg/stddev):           346871.0000/0.00
    execution time (avg/stddev):   113.1569/0.00

```
Western Digital:
```
Operations performed:  24570 Read, 16380 Write, 52352 Other = 93302 Total
Read 383.91Mb  Written 255.94Mb  Total transferred 639.84Mb  (2.1327Mb/sec)
  136.50 Requests/sec executed

Test execution summary:
    total time:                          300.0103s
    total number of events:              40950
    total time taken by event execution: 230.0220
    per-request statistics:
         min:                                  0.03ms
         avg:                                  5.62ms
         max:                                692.52ms
         approx.  95 percentile:              13.96ms

Threads fairness:
    events (avg/stddev):           40950.0000/0.00
    execution time (avg/stddev):   230.0220/0.00

```

Conclusion
----------

As you can see the transactions per second between the Western Digital Drive and the KEXIN Drive was more than 12.5% slower. The queries per second between the Western Digital Drive and KEXIN drive were more than 12.5% slower. Even the sysbench showed an extreme difference between the two drives. There is a 13.36ms difference in the 95% percentile. KEXIN:
```
transactions:                        34753  (231.62 per sec.)
queries:                             695060 (4632.45 per sec.)

```
Western Digital:
```
transactions:                        4356   (29.00 per sec.)
queries:                             87120  (579.94 per sec.)

```
With the cost of SSD drives dropping, we can see that the Raspberry Pi 4, 4GB with an SSD drive is a good choice for a small business (or anyone) that needs a good robust database at an affordable price range. 

_The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._ 

_Photo by [Enrico Sottocorna](https://unsplash.com/@enricosottocorna?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/berries-spoons?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_