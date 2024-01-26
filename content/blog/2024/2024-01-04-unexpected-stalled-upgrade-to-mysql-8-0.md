---
title: 'Unexpected Stalled Upgrade to MySQL 8.0'
date: "2024-01-03T00:00:00+00:00"
draft: true
tags: ['author_alexandre', 'Intermediate Level', 'MySQL', 'Percona Server for MySQL', 'upgrade']
authors:
  - alexandre_vaniachine
slug: unexpected-stalled-upgrade-to-mysql-8-0
---

A multi-tenant database is a database that serves multiple clients, or tenants, who share the same database schema but have separate data sets. One way to achieve data isolation for each client is to create a separate MySQL database for each tenant.

Some advantages of this approach are:

* It allows for easy backup and restore of individual tenant data.
* It simplifies the database administration and maintenance tasks, as each database can be managed independently.
* Scaling is easily achieved by adding more database servers and distributing tenant databases across them.

This approach requires a large number of tables on each server. Combined with the default value of `innodb_file_per_table=ON`, this results in a large number of files that affects [crash recovery time](https://percona.community/blog/2019/07/23/impact-of-innodb_file_per_table-option-on-crash-recovery-time) or [Percona XtraBackup](https://www.percona.com/blog/using-percona-xtrabackup-mysql-instance-large-number-tables) execution.

This blog post describes how to take care of a large number of files when upgrading to MySQL 8.0 in-place.

### Version Selection

A steady stream of MySQL 8.0 minor releases provides improvements and refactoring of new MySQL 8.0 features. However, some of these releases introduce incompatibilities that require corresponding changes on the application side. Limiting scope of the application-side changes, we chose MySQL 8.0.25 version. This was our first step towards the major version 8.0.

Upgrade In-Place
----------------

A new MySQL 8.0 option is the upgrade in-place procedure. According to the [upgrading guide](https://docs.percona.com/percona-server/8.0/upgrading-guide.html):

> An in-place upgrade is performed by using existing data on the server and involves the following actions:
> 
> * Stopping the MySQL 5.7 server
> * Replacing the old binaries with MySQL 8.0 binaries
> * Starting the MySQL 8.0 server with the same data files.
> 
> While an in-place upgrade may not be suitable for all environments, especially those environments with many variables to consider, the upgrade should work in most cases.

As an exception, in the case of an environment with a large number of tables, the upgrade in-place may get [stalled for weeks](https://forums.mysql.com/read.php?35,697581).

Below we describe how to debug and resolve such issue.

### Encountering the Issue

In our test environment, we encountered a similar issue. Despite steady CPU usage, the in-place upgrade looks stalled. We monitored the upgrade progress by counting files modified in the last 24 hours. Monitoring revealed low modification rates, like

        find /var/lib/mysql -name "*.ibd" -mtime -1 | wc -l
        14887

that were decreasing. Although the InnoDB files continued to be modified, the decreasing modification rate was too low to be practical.

### Investigating the Issue

To debug this problem we used the Linux [`perf`](https://percona.community/blog/2020/02/05/finding-mysql-scaling-problems-using-perf) tool. While the `mysqld` process was running during upgrade:

* we collected `perf` data

        perf record -F 10 -o mysqld.perf  -p $(pidof mysqld) -- sleep 20; 
        [ perf record: Woken up 1 times to write data ]
        [ perf record: Captured and wrote 0.256 MB mysqld.perf (1016 samples) ]

* and produced the `perf` report

        perf report --input mysqld.perf --stdio
        
        # To display the perf.data header info, please use --header/--header-only options.
        #
        #
        # Total Lost Samples: 0
        #
        # Samples: 1K of event 'cpu-clock'
        # Event count (approx.): 101600000000
        #
        # Overhead  Command  Shared Object       Symbol                                         
        # ........  .......  ..................  ................................
        #
            34.55%  mysqld   libc-2.17.so        [.] __sched_yield
            14.86%  mysqld   [kernel.kallsyms]   [k] __raw_spin_unlock_irq
            11.32%  mysqld   [kernel.kallsyms]   [k] system_call_after_swapgs
            11.32%  mysqld   mysqld              [.] Fil_shard::reserve_open_slot
            ...

To find out why `mysqld` process stuck in the `Fil_shard::reserve_open_slot` call, we checked the [Percona Server source code](https://github.com/percona/percona-server/blob/Percona-Server-8.0.25-15/storage/innobase/fil/fil0fil.cc#L2125) that shows:

* the function code

        /** Wait for an empty slot to reserve for opening a file.
        @return true on success. */
        bool Fil_shard::reserve_open_slot(size_t shard_id) {
          size_t expected = EMPTY_OPEN_SLOT;

          return s_open_slot.compare_exchange_weak(expected, shard_id);
        }

* and the corresponding comments

        The data structure (Fil_shard) that keeps track of the tablespace ID to
        fil_space_t* mapping are hashed on the tablespace ID. The tablespace name to
        fil_space_t* mapping is stored in the same shard. A shard tracks the flushing
        and open state of a file. When we run out open file handles, we use a ticketing
        system to serialize the file open, see Fil_shard::reserve_open_slot() and
        Fil_shard::release_open_slot().

Apparently, the stalled upgrade process hit the open files limit, given the large number of files in our environment.

### Resolving the Issue

To prevent the `mysqld` upgrade process from running out of open file handles, we followed [Percona guidance](https://www.percona.com/blog/using-percona-xtrabackup-mysql-instance-large-number-tables) for setting open files limit

1) Counted files as

        find /var/lib/mysql/ -name "*.ibd" | wc -l
        324780

and added another 1000 to this number for other miscellaneous open file needs.

2) Increased the `innodb_open_files` limit in two places:

* added a corresponding line to configuration file `/etc/my.cnf` like

        innodb_open_files = 325780

* added a corresponding line to the `systemd` configuration file such as `/etc/systemd/system/mysqld.service.d/override.conf` like

        [Service]
        LimitNOFILE = 325780

With these adjustments our upgrade completed processing of a terabyte of data in just a few hours. To provide more visibility into the upgrade process we also increased the default level of error log verbosity by adding another line to the `/etc/my.cnf` file:

    log_error_verbosity = 3

Increased verbosity enabled progress monitoring in the mysql error log during upgrade, like:

    2023-10-28T00:27:09.331924Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.25-15) starting as process 16034
    ...
    2023-10-28T00:27:09.353871Z 1 [System] [MY-011012] [Server] Starting upgrade of data directory.
    2023-10-28T00:27:09.353986Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
    ...
    2023-10-28T00:27:19.412572Z 1 [Note] [MY-012206] [InnoDB] Found 324780 '.ibd' and 0 undo files
    2023-10-28T00:27:19.412757Z 1 [Note] [MY-012207] [InnoDB] Using 17 threads to scan 324780 tablespace files
    2023-10-28T00:27:28.764032Z 0 [Note] [MY-012200] [InnoDB] Thread# 0 - Checked 15615/20298 files
    ...
    2023-10-28T00:27:31.718051Z 0 [Note] [MY-012201] [InnoDB] Checked 20298 files
    2023-10-28T00:27:31.718440Z 1 [Note] [MY-012208] [InnoDB] Completed space ID check of 324780 files.
    ...
    2023-10-28T00:27:48.821432Z 1 [Note] [MY-012922] [InnoDB] Waiting for purge to start
    2023-10-28T00:27:48.878058Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
    2023-10-28T00:27:48.885203Z 1 [Note] [MY-011088] [Server] Data dictionary initializing version '80023'.
    2023-10-28T00:27:49.187508Z 1 [Note] [MY-010337] [Server] Created Data Dictionary for upgrade
    ...
    2023-10-28T01:57:55.312683Z 2 [System] [MY-011003] [Server] Finished populating Data Dictionary tables with data.
    ...
    2023-10-28T01:59:15.187709Z 5 [System] [MY-013381] [Server] Server upgrade from '50700' to '80025' started.
    ...
    2023-10-28T03:01:09.880932Z 5 [System] [MY-013381] [Server] Server upgrade from '50700' to '80025' completed.
    ...
    2023-10-28T03:01:13.905459Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.25-15'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 15, Revision a558ec2.

### Discussion

While we were contemplating if this is a feature or a bug, MySQL release 8.0.28 refactored the related [`innodb_open_files`](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_open_files) code. Further details are provided in the corresponding open source commit [WL#14591 InnoDB: Make system variable `innodb_open_files` dynamic](https://github.com/percona/percona-server/commit/b184bd30f94df30a8bf178fc327590c5865d33bc):

    - The `innodb_open_files` system variable can now be set with a dynamic SQL procedure `innodb_set_open_files_limit(N)`. If the new value is too low, an error is returned to client with the minimum value presented. If the value is out of bounds or of incorrect type, it will be reported as error also.
    - `Fil_system::set_open_files_limit` was added to allow changes to the global opened files limit. The `Fil_system::m_max_n_open` is atomic now and extracted to a separate class `fil::detail::Open_files_limit`, instantiated as `Fil_system::m_open_files_limit`.
    ...
    - `Fil_shard::reserve_open_slot`, Fil_shard::release_open_slot and static Fil_shard::s_open_slot were removed. Now we have CAS-based system of assuring the opened files will not exceed the limit set.

Thus, the new MySQL 8.0.28 feature -- dynamic `innodb_open_files` variable -- eliminated the need for open files limit adjustments in preparation for MySQL 8.0 upgrade.

Conclusions
-----------

Lessons learned:

* Prepare for MySQL 8.0 upgrade in-place by taking a backup of the data directory.
* Take advantage of the Percona Server open source code.
* Follow guidance and advice posted in Percona blogs.

_The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._