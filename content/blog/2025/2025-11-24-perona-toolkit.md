---
title: "The Right Tool for the Job"
date: "2025-11-24T00:00:00+00:00"
tags: ["Opensource", "Percona", "toolkit", "MySQL", "Community", "Percona Server", "PXC"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2025/11/vintage-toolbox-open.jpg
---
When I first got into woodworking, my mentor shared a piece of advice that has stuck with me ever since: “Use the right tool for the job.” You wouldn’t reach for a belt sander to flatten a board when a planer can accomplish the task faster, cleaner, and with far better results.

The same principle applies in the world of database engineering. When working with MySQL or Percona Server, choosing the correct tool can be the difference between efficient diagnostics and unnecessary downtime.

In this post, I’ll highlight several of the most practical and commonly used utilities from the Percona Toolkit. While the toolkit includes many powerful commands, I’ll focus on the ones that provide the most value in day-to-day operations, troubleshooting, and gathering actionable details for support cases.

## PT Summary
A Percona Toolkit utility that provides a concise, high-level overview of a system’s hardware, OS configuration and performance-related metrics. It’s designed to quickly capture the essential details needed for diagnostics or support cases—CPU, memory, disk layout, kernel parameters and more all in a single, easy-to-read report.

### Examples
Run pt-summary with no arguments to print a full system summary:
```
> pt-summary
# Percona Toolkit System Summary Report ######################
        Date | 2025-11-24 17:15:19 UTC (local TZ: EST -0500)
    Hostname | pi16gb
      Uptime | 41 days,  2:27,  4 users,  load average: 0.00, 0.00, 0.00
    Platform | Linux
     Release | Debian GNU/Linux 12 (bookworm) (bookworm)
      Kernel | 6.12.47+rpt-rpi-2712
Architecture | CPU = 32-bit, OS = 64-bit
   Threading | NPTL 2.36
     SELinux | No SELinux detected
 Virtualized | No virtualization detected
# Processor ##################################################
  Processors | physical = 4, cores = 0, virtual = 4, hyperthreading = no
      Speeds | 
      Models | 
      Caches | 
  Designation               Configuration                  Size     Associativity
  ========================= ============================== ======== ======================
# Memory #####################################################
         Total | 15.8G
          Free | 675.0M
          Used | physical = 5.3G, swap allocated = 512.0M, swap used = 0.0, virtual = 5.3G
        Shared | 44.7M
       Buffers | 10.6G
        Caches | 10.5G
         Dirty | 128 kB
       UsedRSS | 5.1G
    Swappiness | 60
   DirtyPolicy | 20, 10
   DirtyStatus | 0, 0
  Locator   Size     Speed             Form Factor   Type          Type Detail
  ========= ======== ================= ============= ============= ===========
# Mounted Filesystems ########################################
  Filesystem      Size Used Type   Opts                                                                                             Mountpoint
  /dev/nvme0n1p1  510M  14% 
  /dev/nvme0n1p2  458G   5% 
  /dev/sda1       117G  16% 
# Disk Schedulers And Queue Size #############################
     nvme0n1 | [none] 255
         sda | [mq-deadline] 60
# Disk Partitioning ##########################################
# Kernel Inode State #########################################
dentry-state | 107782	98346	45	0	32304	0
     file-nr | 3680	0	9223372036854775807
    inode-nr | 99614	20818
# LVM Volumes ################################################
Unable to collect information
# LVM Volume Groups ##########################################
Unable to collect information
# RAID Controller ############################################
  Controller | No RAID controller detected
# Network Config #############################################
  Controller | 00.0 Ethernet controller
 FIN Timeout | 60
  Port Range | 60999
# Interface Statistics #######################################
  interface  rx_bytes rx_packets  rx_errors   tx_bytes tx_packets  tx_errors
  ========= ========= ========== ========== ========== ========== ==========
  lo       6000000000     175000          0 6000000000     175000          0
  eth0              0          0          0          0          0          0
  wlan0    5000000000   30000000          0 15000000000   22500000          0
# Network Devices ############################################
  Device    Speed     Duplex
  ========= ========= =========
  eth0       Unknown!   Unknown!  
# Network Connections ########################################
  Connections from remote IP addresses
    192.168.1.91        1
    192.168.1.251       1
    2603                2
  Connections to local IP addresses
    192.168.1.145       2
    2603                2
  Connections to top 10 local ports
    3306                2
    6011:ef0:7260:::22     2
  States of connections
    ESTABLISHED         3
    LISTEN              6
    TIME_WAIT           1
# Top Processes ##############################################
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
  95842 root      20   0       0      0      0 I   6.7   0.0   0:00.08 kworker+
      1 root      20   0  169520  13088   8672 S   0.0   0.1   0:18.56 systemd
      2 root      20   0       0      0      0 S   0.0   0.0   0:01.70 kthreadd
      3 root      20   0       0      0      0 S   0.0   0.0   0:00.00 pool_wo+
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+
      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+
      7 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+
      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+
# Notable Processes ##########################################
  PID    OOM    COMMAND
    ?      ?    sshd doesn't appear to be running
# Simplified and fuzzy rounded vmstat (wait please) ##########
  procs  ---swap-- -----io---- ---system---- --------cpu--------
   r  b    si   so    bi    bo     ir     cs  us  sy  il  wa  st
   2  0     0    0     1     6    100    150   0   0 100   0   0
   1  0     0    0     0     0   1750   3000   1   3  97   0   0
   1  0     0    0     0     0    250    400   0   0 100   0   0
   1  0     0    0     0     0    300    450   0   0 100   0   0
   1  0     0    0     0     0    300    450   0   0 100   0   0
# Memory management ##########################################
# The End ####################################################
```
Redirect output to a file.
```
> pt-summary > server-summary.txt
```


## PT MySQL Summary
A Percona Toolkit utility that collects and displays a concise overview of a MySQL or Percona Server instance, including key configuration settings, performance metrics, storage engine details, replication status, buffer pool usage, and important global variables. It provides a fast, structured snapshot of the database environment, making it ideal for troubleshooting, tuning, and preparing information for support teams.

### Example
```
> ./pt-mysql-summary
# Percona Toolkit MySQL Summary Report #######################
              System time | 2025-11-24 17:45:54 UTC (local TZ: EST -0500)
# Instances ##################################################
  Port  Data Directory             Nice OOM Socket
  ===== ========================== ==== === ======
   3306 /data0/mysql/data/         0    0   /usr/local/mysql/mysql.sock
# MySQL Executable ###########################################
       Path to executable | /usr/local/mysql/bin/mysqld
              Has symbols | Yes
# Report On Port 3306 ########################################
                     User | wayne@localhost
                     Time | 2025-11-24 12:45:54 (EST)
                 Hostname | pi16gb
                  Version | 8.4.6-6 Source distribution
                 Built On | Linux aarch64
                  Started | 2025-10-14 09:48 (up 41+02:57:35)
                Databases | 10
                  Datadir | /data0/mysql/data/
                Processes | 2 connected, 2 running
              Replication | Is not a replica, has 1 replicas connected
                  Pidfile | /usr/local/mysql/mysqld.pid (exists)
# Processlist ################################################

  Command                        COUNT(*) Working SUM(Time) MAX(Time)
  ------------------------------ -------- ------- --------- ---------
  Binlog Dump GTID                      1       1   3000000   3000000
  Query                                 1       1         0         0

  User                           COUNT(*) Working SUM(Time) MAX(Time)
  ------------------------------ -------- ------- --------- ---------
  replication                           1       1   3000000   3000000
  wayne                                 1       1         0         0

  Host                           COUNT(*) Working SUM(Time) MAX(Time)
  ------------------------------ -------- ------- --------- ---------
  192.168.1.251                         1       1   3000000   3000000
  localhost                             1       1         0         0

  db                             COUNT(*) Working SUM(Time) MAX(Time)
  ------------------------------ -------- ------- --------- ---------
  NULL                                  2       2   3000000   3000000

  State                          COUNT(*) Working SUM(Time) MAX(Time)
  ------------------------------ -------- ------- --------- ---------
  init                                  1       1         0         0
  Source has sent all binlog to         1       1   3000000   3000000

# Status Counters (Wait 10 Seconds) ##########################
Variable                                Per day  Per second     11 secs
Aborted_clients                               1                        
Binlog_snapshot_position                 350000           4            
Binlog_cache_use                           6000                        
Bytes_received                         20000000         225         600
Bytes_sent                           2250000000       25000        4000
[...]
Table_open_cache_misses                     400                        
Table_open_cache_overflows                  225                        
Threads_created                               9                        
Uptime                                    90000           1           1
# Table cache ################################################
                     Size | 1000
                    Usage | 100%
# Key Percona Server features ################################
      Table & Index Stats | Disabled
     Multiple I/O Threads | Enabled
     Corruption Resilient | Enabled
      Durable Replication | Not Supported
     Import InnoDB Tables | Not Supported
     Fast Server Restarts | Not Supported
         Enhanced Logging | Disabled
     Replica Perf Logging | Disabled
      Response Time Hist. | Not Supported
          Smooth Flushing | Not Supported
      HandlerSocket NoSQL | Not Supported
           Fast Hash UDFs | Unknown
# Percona XtraDB Cluster #####################################
# Plugins ####################################################
       InnoDB compression | ACTIVE
# Schema #####################################################
Specify --databases or --all-databases to dump and summarize schemas
# Noteworthy Technologies ####################################
                      SSL | Yes
     Explicit LOCK TABLES | No
           Delayed Insert | No
          XA Transactions | No
              NDB Cluster | No
      Prepared Statements | Yes
 Prepared statement count | 0
# InnoDB #####################################################
                  Version | 8.4.6-6
         Buffer Pool Size | 8.0G
         Buffer Pool Fill | 30%
        Buffer Pool Dirty | 0%
           File Per Table | ON
                Page Size | 16k
            Log File Size | 2 * 48.0M = 96.0M
          Log Buffer Size | 64M
             Flush Method | O_DIRECT
      Flush Log At Commit | 2
               XA Support | 
                Checksums | 
              Doublewrite | ON
          R/W I/O Threads | 4 4
             I/O Capacity | 200
       Thread Concurrency | 4
      Concurrency Tickets | 5000
       Commit Concurrency | 0
      Txn Isolation Level | REPEATABLE-READ
        Adaptive Flushing | ON
      Adaptive Checkpoint | 
           Checkpoint Age | 0
             InnoDB Queue | 0 queries inside InnoDB, 0 queries in queue
       Oldest Transaction | 0 Seconds
         History List Len | 1
               Read Views | 0
         Undo Log Entries | 0 transactions, 0 total undo, 0 max undo
        Pending I/O Reads | 0 buf pool reads, 0 normal AIO, 0 ibuf AIO, 0 preads
       Pending I/O Writes | 0 buf pool (0 LRU, 0 flush list, 0 page); 0 AIO, 0 sync, 0 log IO (0 log, 0 chkp); 1 pwrites
      Pending I/O Flushes | 0 buf pool, 0 log
       Transaction States | 3xnot started
# MyISAM #####################################################
                Key Cache | 8.0M
                 Pct Used | 20%
                Unflushed | 0%
# Security ###################################################
                    Users | 8 users, 0 anon, 0 w/o pw, 7 old pw
            Old Passwords | 
# Encryption #################################################
No keyring plugins found
# Binary Logging #############################################
                  Binlogs | 3
               Zero-Sized | 0
               Total Size | 437.9M
            binlog_format | ROW
         expire_logs_days | 
              sync_binlog | 0
                server_id | 10
             binlog_do_db | 
         binlog_ignore_db | 
# Noteworthy Variables #######################################
     Auto-Inc Incr/Offset | 1/1
   default_storage_engine | InnoDB
               flush_time | 0
             init_connect | 
                init_file | 
                 sql_mode | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
         join_buffer_size | 256k
         sort_buffer_size | 256k
         read_buffer_size | 128k
     read_rnd_buffer_size | 256k
       bulk_insert_buffer | 0.00
      max_heap_table_size | 16M
           tmp_table_size | 16M
       max_allowed_packet | 64M
             thread_stack | 1M
                      log | 
                log_error | /var/log/mysql/mysqld.log
             log_warnings | 
         log_slow_queries | 
log_queries_not_using_indexes | OFF
      log_replica_updates | ON
# Configuration File #########################################
              Config File | /etc/my.cnf

[mysqld]
character-set-server                = utf8mb4
authentication_policy               = '*'
port                                = 3306
socket                              = /usr/local/mysql/mysql.sock
pid-file                            = /usr/local/mysql/mysqld.pid
basedir                             = /usr/local/mysql/ 
datadir                             = /data0/mysql/data/
tmpdir                              = /data0/mysql/tmp/
general_log_file                    = /var/log/mysql/mysql-general.log
log-error                           = /var/log/mysql/mysqld.log
slow_query_log_file                 = /var/log/mysql/slow_query.log
[...]
innodb_data_home_dir                = /data0/mysql/data/
innodb_log_group_home_dir           = /data0/mysql/data/
innodb_temp_data_file_path          = ../tmp/ibtmp1:12M:autoextend:max:8G
innodb_buffer_pool_size             = 8G 
innodb-redo-log-capacity            = 2G 
innodb_flush_log_at_trx_commit      = 2 
innodb_lock_wait_timeout            = 50
innodb_flush_method                 = O_DIRECT 
innodb_file_per_table               = 1
innodb_io_capacity                  = 200
innodb_buffer_pool_instances        = 8
innodb_thread_concurrency           = 4

# Memory management library ##################################
jemalloc is not enabled in mysql config for process with id 788
# The End ####################################################
```
Redirect output to file.

```
pt-mysql-summary > percona-server.txt
```

Capture both pt-summary and pt-mysql-summary into a single file.
```
pt-summary > percona-server-summary.txt
pt-mysql-summary >> percona-server-summary.txt
```

## PT Online Schema Change
A Percona Toolkit utility that performs non-blocking, online ALTER TABLE operations by creating a shadow copy of the table, applying the schema changes there, and incrementally syncing data using triggers before swapping it with the original table. This approach minimizes locking and downtime, making it safe to modify large tables in production without disrupting application workloads.

### Examples

#### Adding a New Column
```
pt-online-schema-change \
  --alter "ADD COLUMN status TINYINT NOT NULL DEFAULT 0" \
  D=mydb,t=orders \
  --execute
```
This safely introduces a new column to a busy table without blocking reads or writes. The tool handles the copy, synchronization, and final table swap automatically.

#### Modifying a Column Type
```
pt-online-schema-change \
  --alter "MODIFY COLUMN price DECIMAL(10,2)" \
  D=shop,t=products \
  --execute
```
Changing column definitions—especially on large datasets—can be disruptive using standard SQL. With pt-osc, the migration happens online, keeping applications responsive throughout the operation.

#### Dropping an Unused Column
```
pt-online-schema-change \
  --alter "DROP COLUMN old_flag" \
  D=analytics,t=events \
  --execute
```
Column drops can require a full table rebuild, making them great candidates for pt-osc. This example removes a legacy column while avoiding table locks.

#### Adding an Index
```
pt-online-schema-change \
  --alter "ADD INDEX idx_user_id (user_id)" \
  D=app,t=logins \
  --execute
```
Index creation is another expensive operation for large tables. Here, pt-osc allows the index to be added online, improving performance without interrupting the application.

#### Changing a Primary Key
```
pt-online-schema-change \
  --alter "DROP PRIMARY KEY, ADD PRIMARY KEY(id, created_at)" \
  D=orders,t=order_items \
  --execute
```
Primary key modifications usually require a full table rewrite. pt-osc makes this process safer and easier on production systems by performing the change on a temporary shadow table.

#### Performing a Dry Run
```
pt-online-schema-change \
  --alter "ADD COLUMN test INT" \
  D=mydb,t=mytable \
  --dry-run
```
A dry run allows you to validate the plan and review the process without making any actual changes—a critical safeguard when preparing for production schema work.

#### Printing SQL Changes Before Execution
```
pt-online-schema-change \
  --alter "ADD COLUMN updated_at TIMESTAMP NULL" \
  D=crm,t=customers \
  --print \
  --execute
```
Using --print provides transparency into the SQL operations the tool will perform. This is particularly useful during code reviews or change-control processes.

## PT Show Grants
A Percona Toolkit utility that extracts MySQL user accounts and privileges and outputs them as clean, executable CREATE USER and GRANT statements. It normalizes and orders the privileges for readability, making it valuable for auditing security, documenting access, migrating users between servers, or preparing accurate privilege information for support and compliance purposes.
