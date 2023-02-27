---
title: 'Finding MySQL Scaling Problems Using perf'
date: Wed, 05 Feb 2020 16:18:14 +0000
draft: false
tags: ['author.daniel', 'cacheline', 'MariaDB', 'MySQL', 'perf', 'performance', 'POWER']
authors:
  - daniel_black
images:
  - blog/2020/01/ricardo-gomez-angel-87vUJY3ntyI-unsplash.jpg
slug: finding-mysql-scaling-problems-using-perf
---


The thing I wish I'd learned while still a DBA is how to use [perf](https://perf.wiki.kernel.org/index.php/Main_Page). Conversely after moving to a developer role, getting access to real external client workloads to get a perf recording directly is rare. To bridge this gap, I hope to encourage a bit of perf usage to help DBAs report bugs/feature requests in more detail to MySQL developers, who can then serve your needs better. 

![](blog/2020/01/ricardo-gomez-angel-87vUJY3ntyI-unsplash.jpg)

A recent client request showed how useful perf is in exposing the areas of MySQL that are otherwise well tuned, but can still be in need of coding improvements that increase throughput. The client had a [TPCCRunner](https://sourceforge.net/projects/tpccruner/) (variant) workload that they wanted to run on a [Power 9](https://www.ibm.com/it-infrastructure/power/power9) CPU, in [READ-COMMITTED](https://dev.mysql.com/doc/refman/5.7/en/innodb-transaction-isolation-levels.html#isolevel_read-committed) mode, and they received less performance than they hoped. Being a 2 socket, 20 cpus/socket 4 threads per core, and 256G RAM total it has enough resources. 

With such abundance of resources, the perf profile exposed code bottlenecks not normally seen. 

The principles driving MySQL development for a considerable time have been to a) maintain correctness, and b) deliver performance, usually meaning the CPU should be the bottleneck. The whole reason for large innodb buffer pools, innodb MVCC / LSN, group commit, table caches, thread caches, indexes, query planner etc, is to ensure that all hot data is in memory, ready to be processed optimally in the most efficient way by the CPU. 

Based on this principle, without a requirement to sync to persistent storage for durability, a SQL read mostly load should be able to add scale linearly up to the CPU capacity. Ideally after the CPU capacity has been reached the throughput should stay at the capacity limit and not degrade. Practical overheads of thread measurement mean this is never perfectly achieved. However, it is the goal.

Steps to using perf
-------------------

To install and use perf, use the following steps:

#### 1. Install perf

This is a standard package and is closely tied to the Linux kernel version. The package name varies per distro:

*   Ubuntu: [linux-tools-common](https://packages.ubuntu.com/bionic/linux-tools-common)
*   Debian: [linux-base](https://packages.debian.org/buster/linux-base)
*   RHEL / Centos / Fedora: perf

Distributions normally set the [sysctl](http://man7.org/linux/man-pages/man8/sysctl.8.html) [_kernel.perf_event_paranoid_](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html#perf-event-paranoid) to a level which is hard to use (or [exploit](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html)) and this may need to be adjusted to obtain our recording. Large perf recordings due to hardware threads can require file descriptors and memory, and their limits may need to be increased with care (see [kernel manual](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html#perf-events-perf-resource-control)).

#### 2. Install debug symbols (a.k.a. debug info) for MySQL

Debug symbols mapping memory addresses to real server code can assist greatly in understanding the recorded results. The debug info needs to map to the exact build of MySQL (both version number and its origin). 

Distros provide debug information in separate package repositories (distribution instructions: [Ubuntu](https://wiki.ubuntu.com/Debug%20Symbol%20Packages), [Debian](https://wiki.debian.org/AutomaticDebugPackages), [RHEL](https://access.redhat.com/solutions/9907), [Fedora](https://fedoraproject.org/wiki/StackTraces#What_are_debuginfo_rpms.2C_and_how_do_I_get_them.3F)) and MySQL, [MariaDB](https://mariadb.com/kb/en/library/how-to-produce-a-full-stack-trace-for-mysqld/#installing-debug-info-packages-on-linux) and Percona provide debug info packages in their repositories without additional configuration. 

If compiling from source, the default cmake option -DCMAKE_BUILD_TYPE=RelWithDebugInfo  has debug info as the name suggests.

#### 3. Ensure that your table structures and queries are sane.

MySQL works well when the database table structures, indexes, and queries are in a `natural` simple form. Asking MySQL developers to make poor table structures/queries to achieve greater performance will attract a low priority as making these changes can add to the overhead of simple queries.

#### 4. Ensure that you have tuned the database for the workload.

MySQL has a lot of system variables, and using the performance schema and status variables assists in creating an optimally tuned MySQL instance before beginning perf measurements.

#### 5. Ensure that the active data is off disk

To ensure you measurement is at its maximum, having the hot part of the data loaded into memory enables perf to focus on recording CPU related areas under stress, not just waiting to load from disk. 

For example, the TPCCRunner example described earlier took about an hour before it reached a point where it achieved its maximum transaction throughput. TPCRunner displays this, but generally watch for a leveling out of the queries per second over several minutes. 

When starting/stopping mysqld for testing, [innodb_buffer_pool_dump_at_shutdown](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_buffer_pool_dump_at_shutdown)=1 / innodb_buffer_pool_dump_at_start=1 / innodb_buffer_pool_dump_pct=100 will help restore the innodb buffer pool significantly quicker.

#### 6. Know what workload is being measured

A batch job may not have the same throughput requirements. It also may impact the concurrent workload that you are perf recording by creating longer history length, innodb buffer pool pressure etc. 

The application that generates the workload should be on a different server, different VM or in some way constrained in CPU to avoid resource contention with mysqld. Check the client side to ensure that it isn't overloaded (CPU, network) as this could be indirectly constraining the server side workload.

Measuring
---------

With a hot workload running let's start some measurement. 

Perf uses hardware (PMU) to assist its recording work, but there are limits to hardware support so there's a point where it will affect your workload, so start slow. Perf works by looking at a frequency distribution of where the mysqld process is spending its time. To examine a function that is taking 0.1% of the time means that 1000 samples will likely show it once. As such a few thousand samples is sufficient. The number of samples is the multiplication of [perf record's](http://man7.org/linux/man-pages/man1/perf-record.1.html) _-F / --freq_ – which may by default be several thousand / second – the recording duration, and the number of CPUs. 

If your SQL queries are all running in much less than a second and occurring frequently, then a high frequency recording for a short duration is sufficient. If some query occurs less often, with a high CPU usage spike, a helper program [FlameScope](https://github.com/Netflix/flamescope) will be able to narrow down a perf recording to a usable sample interval. 

Analysis involves looking through a number of sets of data. Below I show a pattern of using _name _as a shell variable, and a large one line command to conduct a number of recordings in sequence. In my case, I cycled through _RC _ (read-committed) vs _RR _(repeatable read), different compile options _-O0_ , kernel versions, final stages of _warmup _(compared to test run) and even local changes to mysqld (thread_local_ut_rnd_ulint_counter ). Keeping track of these alongside the same measurement of the test run output helps to correlate results more easily.
```
name=5.7.28-thread_local_ut_rnd_ulint_counterO0-RC_warmup2 ; 
pid=$(pidof mysqld); 
perf record -F 10 -o mysql-${name}.perf  -p $pid  -- sleep 20; 
perf record -g -F 10 -o mysql-${name}.g.perf  -p $pid  -- sleep 5; 
perf stat -B -e cache-references,cache-misses,cycles,instructions,branches,faults,migrations -p $pid sleep 20 
2>&1  | tee perf-stats-${name}.txt

```
With the above command, the recording is constrained the recording to mysqld (_-p $pid_), at _-F 10_ samples/per second for (_sleep_) _20_ seconds. A longer recording without the stack trace (-g) is taken as reference point to see if the shorter recording with _-g_ stack trace is a fair sample. 10 hz x 20 seconds may not seem like many samples, however this occurred on each of the 160 threads. A record with _-g_ is needed as a perf profile that shows all time in the kernel or pthread mutex (lock) code, but it doesn't mean much without knowing which lock it is and where it was accessed from. 

Perf record with _-g_ call-graph (also known as stack chain or backtrace) adds to the size of the recording and the overhead of measurements. To ensure that there isn't too much perf data (resulting in workload stalls), get the right frequency and duration before enabling _-g_. 

Perf stats were measured to identify (cpu) cache efficiency, instructions/cycle efficiency, instructions throughput (watch out for frequency scaling), faults (connecting real memory to the virtual address - should be low after warmup), and migrations between numa nodes. 

During measurement look at _htop_/_top_ to ensure that the CPUs are indeed loaded. Also check the client side isn't flooded with connection errors that could impact the validity of the recorded results.

Analysis
--------

### Viewing a perf recording

[perf report](http://man7.org/linux/man-pages/man1/perf-report.1.html) is used to textually view a perf recording. It is during the report stage that the debug info is read, since the linux kernel image resolves symbols. Run the report under `nice -n 19 perf report` to ensure it has the lowest CPU priority if you are at all concerned about production impacts. It's quite possible to do this on a different server provided the same kernel and MySQL packages are installed. `perf report --input mysql-5.7.28-event_run2_warmup_run1.perf --stdio`

```
# Total Lost Samples: 0
#
# Samples: 91K of event 'cycles:ppp'
# Event count (approx.): 1261395960159641
#
# Overhead  Command  Shared Object        Symbol                                                                         
# ........  .......  ...................  ...............................................................................
#
     5.84%  mysqld   mysqld               [.] rec_get_offsets_func
     3.62%  mysqld   mysqld               [.] MYSQLparse
     2.70%  mysqld   mysqld               [.] page_cur_search_with_match
     2.70%  mysqld   mysqld               [.] buf_page_get_gen
     2.22%  mysqld   mysqld               [.] cmp_dtuple_rec_with_match_low
     1.93%  mysqld   mysqld               [.] buf_page_hash_get_low
     1.49%  mysqld   mysqld               [.] btr_cur_search_to_nth_level
     1.35%  mysqld   [kernel.kallsyms]    [k] do_syscall_64
     1.14%  mysqld   mysqld               [.] row_search_mvcc
     0.93%  mysqld   mysqld               [.] alloc_root
     0.92%  mysqld   mysqld               [.] lex_one_token
     0.67%  mysqld   libc-2.27.so         [.] malloc
     0.64%  mysqld   libc-2.27.so         [.] _int_malloc
     0.61%  mysqld   libpthread-2.27.so   [.] __pthread_getspecific
     0.59%  mysqld   mysqld               [.] pfs_rw_lock_s_lock_func
     0.59%  mysqld   mysqld               [.] dispatch_command
     0.50%  mysqld   mysqld               [.] check_stack_overrun
     0.50%  mysqld   [tg3]                [k] tg3_poll_work
```
This shows a %CPU time measured when the CPU instruction pointer was at a particular time, grouped by the function name. To find out why malloc or the kernel do_syscall_64 appears so often the stack recording is needed.

### Viewing a perf recording with a stack

When the _perf record_ used _-g_, then _-g_ can be used in perf report to show the breakdown. By default it groups the functions, including the functions it calls, as below. 
`perf report -i mysql-5.7.28-event_run2_warmup_run1.g.perf`
```
Samples: 85K of event 'cycles:ppp', Event count (approx.): 261413311777846
  Children      Self  Command  Shared Object        Symbol
+   80.08%     0.00%  mysqld   libpthread-2.27.so   [.] start_thread
+   80.08%     0.00%  mysqld   mysqld               [.] pfs_spawn_thread
+   80.05%     0.07%  mysqld   mysqld               [.] handle_connection
+   79.75%     0.14%  mysqld   mysqld               [.] do_command
+   77.98%     0.70%  mysqld   mysqld               [.] dispatch_command
+   75.32%     0.18%  mysqld   mysqld               [.] mysql_parse
+   62.63%     0.38%  mysqld   mysqld               [.] mysql_execute_command
+   58.65%     0.13%  mysqld   mysqld               [.] execute_sqlcom_select
+   55.63%     0.05%  mysqld   mysqld               [.] handle_query
+   25.31%     0.41%  mysqld   mysqld               [.] st_select_lex::optimize
+   24.67%     0.12%  mysqld   mysqld               [.] JOIN::exec
+   24.45%     0.59%  mysqld   mysqld               [.] JOIN::optimize
+   22.62%     0.29%  mysqld   mysqld               [.] sub_select
+   20.15%     1.56%  mysqld   mysqld               [.] btr_cur_search_to_nth_level
```
In MySQL, as expected, most significant CPU load is in the threads. Most of the time this is a user connection, under the _handle_connection_ function, which parses and executes the SQL. In different situations you might see innodb background threads, or replication threads: understanding which thread is causing the load is important at a top level. Then, to continue analysis, use the perf report _--no-children_ option. This will show approximately the same as the non_-g_ recording, however it will provide the mechanism of being able to hit Enter on a function to show all the call stacks that go to that particular function. 
`perf report -g --no-children --input mysql-5.7.28-event_run2_warmup_run1.g.perf`
```
  Overhead  Command  Shared Object        Symbol                                                                                                ◆
-    6.24%  mysqld   mysqld               [.] rec_get_offsets_func                                                                              ▒
     start_thread                                                                                                                               ▒
     pfs_spawn_thread                                                                                                                           ▒
     handle_connection                                                                                                                          ▒
     do_command                                                                                                                                 ▒
     dispatch_command                                                                                                                           ▒
     mysql_parse                                                                                                                                ▒
     mysql_execute_command                                                                                                                      ▒
     execute_sqlcom_select                                                                                                                      ▒
   - handle_query                                                                                                                               ▒
      - 4.57% JOIN::exec                                                                                                                        ▒
         - sub_select                                                                                                                           ▒
            + 3.77% evaluate_join_record                                                                                                        ▒
            + 0.60% join_read_always_key                                                                                                        ▒
      + 1.67% st_select_lex::optimize
```
This shows a common call stack into _handle_query_, where the _JOIN::exec_ and _st_select_lex::optimize_ is the diverging point. If the _evaluate_join_record_ and other sub-functions were to be expanded, the bottom level of the call graph would show _rec_get_offsets_func._

### Disassembly (annotation)

In the ncurses interfaces. Selecting 'a' (annotate) on a particular function calls out to the [objdump](https://linux.die.net/man/1/objdump) (binutils) disassembler to show where in this function the highest frequency occurred and maps this to a commented C++ code above it. 

As compilers have significant understanding of the architecture, and given that the C/C++ language provides significant freedom in generating code, it's sometimes quite difficult to parse from assembly back to the C/C++ source. In complex operations, C++ variables don't have an easy translation to CPU registers. Inlined functions are also particularly hard as each inlining can further be optimized to a unique assembly depending on its location. To understand the assembly, I recommend focusing on the loads, stores, maths/conditions with constants and branches to see which register maps to which part of the MySQL server code in the context of the surrounding code. 

E.g annotation on _rec_get_offsets_func_:
```
       │     dict_table_is_comp():
       │
       │     #if DICT_TF_COMPACT != 1
       │     #error "DICT_TF_COMPACT must be 1"
       │     #endif
       │
       │             return(table->flags & DICT_TF_COMPACT);
  0.44 │       mov    0x20(%rsi),%rsi
 39.30 │       movzbl -0x3(%rdi),%eax
       │     _Z20rec_get_offsets_funcPKhPK12dict_index_tPmmPP16mem_block_info_t():
       │
       │             ut_ad(rec);
       │             ut_ad(index);
       │             ut_ad(heap);
       │
       │             if (dict_table_is_comp(index->table)) {
  0.44 │       testb  $0x1,0x34(%rsi)
  0.15 │     ↓ je     e611d8 <rec_get_offsets_func(unsigned char const*, dict_index_t const*, 128
       │                     switch (UNIV_EXPECT(rec_get_status(rec),
```
Here we see that _dict_table_is_comp_ is an expanded inline function at the top of _rec_get_offsets_, the _movzlb .. %eax._ The dominate CPU use in the function however isn't part of this. The _testb 0x1 (DICT_TF_COMPACT) ... %rsi_ is the testing of the flag with _je_ afterwards to return from the function.

Example - mutex contention
--------------------------

Compared to the performance profile on x86 above under 'Viewing a perf recording', this is what the performance profile looked like on POWER. perf report --input mysql-5.7.28-read_mostly_EVENT_RC-run2.perf --stdio
```
# Total Lost Samples: 0
#
# Samples: 414K of event 'cycles:ppp'
# Event count (approx.): 3884039315643070
#
# Overhead  Command  Shared Object        Symbol                                                                         
# ........  .......  ...................  ...............................................................................
    13.05%  mysqld   mysqld               [.] MVCC::view_open
    10.99%  mysqld   mysqld               [.] PolicyMutex<TTASEventMutex<GenericPolicy> >::enter
     4.11%  mysqld   mysqld               [.] rec_get_offsets_func
     3.78%  mysqld   mysqld               [.] buf_page_get_gen
     2.34%  mysqld   mysqld               [.] MYSQLparse
     2.27%  mysqld   mysqld               [.] cmp_dtuple_rec_with_match_low
     2.15%  mysqld   mysqld               [.] btr_cur_search_to_nth_level
     2.05%  mysqld   mysqld               [.] page_cur_search_with_match
     1.99%  mysqld   mysqld               [.] ut_delay
     1.83%  mysqld   mysqld               [.] mtr_t::release_block_at_savepoint
     1.35%  mysqld   mysqld               [.] rw_lock_s_lock_func
     0.96%  mysqld   mysqld               [.] buf_page_hash_get_low
     0.88%  mysqld   mysqld               [.] row_search_mvcc
     0.84%  mysqld   mysqld               [.] lex_one_token
     0.80%  mysqld   mysqld               [.] pfs_rw_lock_s_unlock_func
     0.80%  mysqld   mysqld               [.] mtr_t::commit
     0.62%  mysqld   mysqld               [.] pfs_rw_lock_s_lock_func
     0.59%  mysqld   [kernel.kallsyms]    [k] power_pmu_enable
     0.59%  mysqld   [kernel.kallsyms]    [k] _raw_spin_lock
     0.55%  mysqld   libpthread-2.28.so   [.] __pthread_mutex_lock
     0.54%  mysqld   mysqld               [.] alloc_root
     0.43%  mysqld   mysqld               [.] PolicyMutex<TTASEventMutex<GenericPolicy> >::exit
```
What stands out clearly is the top two entries that didn't appear on x86. Looking closer at _MVCC::view_open_: 
`perf report -g --no-children --input mysql-5.7.28-read_mostly_EVENT_RC-run2.g.perf`

```
-   13.47%  mysqld   mysqld               [.] MVCC::view_open                                                                                                                                                          ▒
     __clone                                                                                                                                                                                                           ▒
     0x8b10                                                                                                                                                                                                            ▒
     pfs_spawn_thread                                                                                                                                                                                                  ▒
     handle_connection                                                                                                                                                                                                 ▒
     do_command                                                                                                                                                                                                        ▒
     dispatch_command                                                                                                                                                                                                  ▒
     mysql_parse                                                                                                                                                                                                       ▒
     mysql_execute_command                                                                                                                                                                                             ▒
     execute_sqlcom_select                                                                                                                                                                                             ▒
   - handle_query                                                                                                                                                                                                      ▒
      - 11.22% JOIN::exec                                                                                                                                                                                              ▒
         - sub_select                                                                                                                                                                                                  ▒
            - 10.99% join_read_always_key                                                                                                                                                                              ▒
                 handler::ha_index_read_map                                                                                                                                                                            ▒
                 ha_innobase::index_read                                                                                                                                                                               ▒
               - row_search_mvcc                                                                                                                                                                                       ▒
                  - 10.99% trx_assign_read_view                                                                                                                                                                        ▒
                       MVCC::view_open
```
Annotation of MVCC::view_open
```
       │     _ZNK14TTASEventMutexI13GenericPolicyE7is_freeEjjRj():                                                                                                                                                     ▒
       │             bool is_free(                                                                                                                                                                                     ▒
  0.02 │a08: ↓ bne    cr4,10db7a30 <MVCC::view_open(ReadView*&, a90                                                                                                                                                    ▒
       │     ↓ b      10db7ad0 <MVCC::view_open(ReadView*&, trx_t*)+0xb30>                                                                                                                                             ▒
       │     ut_rnd_gen_ulint():                                                                                                                                                                                       ▒
       │             ut_rnd_ulint_counter = UT_RND1 * ut_rnd_ulint_counter + UT_RND2;                                                                                                                                  ▒
       │a10:   addis  r7,r2,2                                                                                                                                                                                          ▒
  0.02 │       addi   r7,r7,26904                                                                                                                                                                                      ▒
 81.15 │       ld     r8,0(r7)                                                                                                                                                                                         ▒
  0.02 │       mulld  r8,r27,r8                                                                                                                                                                                        ▒
  0.02 │       addis  r8,r8,1828                                                                                                                                                                                       ▒
  0.02 │       addi   r8,r8,-14435                                                                                                                                                                                     ▒
       │     ut_rnd_gen_next_ulint():                                                                                                                                                                                  ▒
       │             rnd = UT_RND2 * rnd + UT_SUM_RND3;                                                                                                                                                                ▒
  0.02 │       mulld  r9,r8,r19                                                                                                                                                                                        ▒
       │     ut_rnd_gen_ulint():                                                                                                                                                                                       ▒
       │             ut_rnd_ulint_counter = UT_RND1 * ut_rnd_ulint_counter + UT_RND2;                                                                                                                                  ▒
  0.04 │       std    r8,0(r7)
```
Due to the inline of code, within [MVCC::view_open](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/read/read0read.cc#L554..L611) one of the mutexs got expanded out and the random number is used to spinlock wait for the lock again. [PolicyMutex<TTASEventMutex<GenericPolicy> >::enter](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/include/ib0mutex.h#L707..L717) expanded to exactly the same code. 

We see here that the load (_ld_) into _r8_, is the slowest part of this. In mysql-5.7.28, [ut_rnd_ulint_counter](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/ut/ut0rnd.cc#L48) is an ordinary global variable, meaning its shared between threads. The simple line of code _ut_rnd_ulint_counter = UT_RND1 * ut_rnd_ulint_counter + UT_RND2_,  shows the result stored back in the same variable. To understand why this didn't scale, we need to understand cache lines. 

note: _MVCC::view_open_ did show up in the x86 profile, at 0.23% and had the lock release as the highest cpu point. For x86 _PolicyMutex<TTASEventMutex<GenericPolicy> >::enter_ was at 0.32%.

### Cache Lines

All modern CPUs that are likely to support MySQL will have some from of [cache hierarchy](https://en.wikipedia.org/wiki/Cache_hierarchy). The principles are that a largely accessed memory location, like _ut_rnd_ulint_counter_, can be copied into cache and at some point the CPU will push it back to memory. To ensure behavior is consistent, cache lines represent a MMU (memory management unit) concept of a memory allocation to a particular CPU. Cache lines can be read only, or exclusive, and a protocol between CPU cores exists to ensure that exclusive access is to one CPU only. When one CPU modifies a memory location it gains an exclusive cache line, and the cached value in other CPU caches are flushed. At which cache level this flushing occurs at, and to what extent are caches shared between CPUs, is quite architecture specific. However, citing rough [metrics](http://brenocon.com/dean_perf.html), cache access is orders of magnitude faster than RAM. 

In the perf recording above, storing back of _ut_rnd_ulint_counter_ clears the cache for the other CPUs, and this is why the load instruction is slow. MySQL did have this fixed in [5.7.14](https://github.com/mysql/mysql-server/commit/dedc8b3d567fbb92ce912f1559fe6a08b2857045) but reverted this fix in [5.7.20](https://github.com/mysql/mysql-server/commit/dedc8b3d567fbb92ce912f1559fe6a08b2857045) (assuming some performance degradation in thread local storage). In MySQL [8.0+](https://github.com/mysql/mysql-server/commit/ea4913b403db72f26565520f68686b385872e7d2#diff-5f582f65ca6be1efafb5e278e4bffc44R35), _ut_rnd_ulint_counter_ is a C++11 [thread_local](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2008/n2659.htm) variable which has a faster implementation. [MariaDB-10.3.5](https://github.com/MariaDB/server/commit/ce04790) avoided this by removing the random delay in InnoDB mutexes. Thread local variables reduce contention because each thread has its independent memory location. Because this is only a random number seed, there's no need for synchronization of results.

### Cache collisions

The impacts of _ut_rnd_ulint_counter_ however aren't limited to itself. Cache lines reserve blocks of memory according to the cache line size of the architecture (x86 - 64 bytes, arm64 and POWER - 128 bytes, s390 - 256 bytes). High in the CPU profile is the _btr_cur_search_to_nth_level_ function. This is part of innodb's scanning of an index and it would be easy to discount its high CPU usage. Looking at the disassembly however shows:
```
  0.01 │        ld     r8,3464(r31)
       │                      cursor->low_match = low_match;
  0.05 │        std    r10,96(r25)
       │                      cursor->up_bytes = up_bytes;
  0.00 │        ld     r10,3456(r31)
       │                      if (btr_search_enabled && !index->disable_ahi) {
 24.08 │        lbz    r9,0(r9)
       │                      cursor->low_bytes = low_bytes;
  0.01 │        std    r7,104(r25)
       │                      cursor->up_match = up_match;
  0.00 │        std    r8,80(r25)
       │                      cursor->up_bytes = up_bytes;
  0.01 │        std    r10,88(r25)
       │                      if (UNIV_LIKELY(btr_search_enabled) && !index->disable_ahi) {
  0.00 │        cmpwi  cr7,r9,0
  0.00 │        ld     r9,48(r29)
  0.01 │      ↓ beq    cr7,10eb88a8 <btr_cur_search_to_nth_level(dict_index_t*, 2348
```
The _lbz_ is a load byte instruction referring to _btr_search_enabled_. _btr_search_enabled_ and is the MySQL server variable associated with the SQL global [innodb_adaptive_hash_index](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_adaptive_hash_index) . As a global system variable, this isn't changed frequently, probably only once at startup. As such it should be able to rest comfortably in the cache of all CPUs in a read only cache line.

To find out why the relative address is examined in the mysql executable:
```
$ readelf -a bin/mysqld | grep btr_search_enabled
  8522: 0000000011aa1b40     1 OBJECT  GLOBAL DEFAULT   24 btr_search_enabled
 17719: 0000000011aa1b40     1 OBJECT  GLOBAL DEFAULT   24 btr_search_enabled
```
Taking the last two characters off the hexadecimal address _0000000011aa1b40_ and the other variables in the same 256 (0x100) byte address range can be examined.
```
$ readelf -a bin/mysqld | grep 0000000011aa1b
  1312: 0000000011aa1be0   296 OBJECT  GLOBAL DEFAULT   24 fts_default_stopword
  8522: 0000000011aa1b40     1 OBJECT  GLOBAL DEFAULT   24 btr_search_enabled
  9580: 0000000011aa1b98    16 OBJECT  GLOBAL DEFAULT   24 fil_addr_null
 11434: 0000000011aa1b60     8 OBJECT  GLOBAL DEFAULT   24 zip_failure_threshold_pct
 12665: 0000000011aa1b70    40 OBJECT  GLOBAL DEFAULT   24 dot_ext
 13042: 0000000011aa1b30     8 OBJECT  GLOBAL DEFAULT   24 ut_rnd_ulint_counter
 13810: 0000000011aa1b48     8 OBJECT  GLOBAL DEFAULT   24 srv_checksum_algorithm
 18831: 0000000011aa1bb0    48 OBJECT  GLOBAL DEFAULT   24 fts_common_tables
 27713: 0000000011aa1b38     8 OBJECT  GLOBAL DEFAULT   24 btr_ahi_parts
 33183: 0000000011aa1b50     8 OBJECT  GLOBAL DEFAULT   24 zip_pad_max
  2386: 0000000011aa1b58     7 OBJECT  LOCAL  DEFAULT   24 _ZL9dict_ibfk
  5961: 0000000011aa1b68     8 OBJECT  LOCAL  DEFAULT   24 _ZL8eval_rnd
 10509: 0000000011aa1be0   296 OBJECT  GLOBAL DEFAULT   24 fts_default_stopword
 17719: 0000000011aa1b40     1 OBJECT  GLOBAL DEFAULT   24 btr_search_enabled
 18777: 0000000011aa1b98    16 OBJECT  GLOBAL DEFAULT   24 fil_addr_null
 20631: 0000000011aa1b60     8 OBJECT  GLOBAL DEFAULT   24 zip_failure_threshold_pct
 21862: 0000000011aa1b70    40 OBJECT  GLOBAL DEFAULT   24 dot_ext
 22239: 0000000011aa1b30     8 OBJECT  GLOBAL DEFAULT   24 ut_rnd_ulint_counter
 23007: 0000000011aa1b48     8 OBJECT  GLOBAL DEFAULT   24 srv_checksum_algorithm
 28028: 0000000011aa1bb0    48 OBJECT  GLOBAL DEFAULT   24 fts_common_tables
 36910: 0000000011aa1b38     8 OBJECT  GLOBAL DEFAULT   24 btr_ahi_parts
 42380: 0000000011aa1b50     8 OBJECT  GLOBAL DEFAULT   24 zip_pad_max
```
The _ut_rnd_ulint_counter_ is stored 16 bytes away from the _btr_search_enabled_. Because of this, every invalidation of _ut_rnd_ulint_counter_ cache line results in a cache invalidation of _btr_search_enabled_ on POWER, and every other variable in the _0000000011aa1b00 to 0000000011aa1b40_ address range for x86_64 (or to _0000000011aa1b80_ for POWER and ARM64, or to _0000000011aa1c00_ for s390). There are no rules governing the layout of these variables so it was only luck that caused x86_64 to not be affected here. 

While the contended management of _ut_rnd_ulint_counter_ remains an unsolved problem on MySQL-5.7, putting all the global variables into the same memory block as a way to keep them out of the same cache as other potentially frequently changed variables is a way to prevent unintended contention. Global variables are an ideal candidate for this as they are changed infrequently and are usually hot in code paths. By pulling all the global variables in the same location, this maximized the cache by using less cache lines that remain in a read only mode. 

To achieve this co-location, MySQL uses the Linux kernel mechanism of using [section attributes on variables](https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#index-section-variable-attribute) and a linker script to bind their location. This was is described in MySQL [bug 97777](https://bugs.mysql.com/bug.php?id=97777) and the MariaDB task [MDEV-21145](https://jira.mariadb.org/browse/MDEV-21145). The segmenting of the system global variables using this mechanism resulted in a 5.29% increase in the transactions per minute of the TPCCRunner benchmark (using MUTEXTYPE=sys).

Mutex Implementations
---------------------

Having discovered what I thought to be a smoking gun with the _ut_rnd_ulint_counter_ contention being the source of throughput problems for the benchmark, the _thread_local_ implementation of MySQL-8.0 was back-ported to MySQL-5.7.28. Disappointingly it was discovered that the throughput was approximately the same. From a perf profile perspective, the CPU usage was no longer in the inlined _ut_rnd_gen_ulint_ function, it was in the [sync_array_wait_event](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/sync/sync0arr.cc#L451..L488) and [sync_array_reserve_cell](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/sync/sync0arr.cc#L333..L400) functions.
```
Samples: 394K of event 'cycles:ppp', Event count (approx.): 2348024370370315
  Overhead  Command  Shared Object               Symbol                                                                                                                               ◆
-   45.48%  mysqld   [kernel.vmlinux]            [k] _raw_spin_lock                                                                                                                   ▒
     __clone                                                                                                                                                                          ▒
   - 0x8b10                                                                                                                                                                           ▒
      - 45.48% pfs_spawn_thread                                                                                                                                                       ▒
           handle_connection                                                                                                                                                          ▒
         - do_command                                                                                                                                                                 ▒
            - 45.44% dispatch_command                                                                                                                                                 ▒
               - 45.38% mysql_parse                                                                                                                                                   ▒
                  - 45.38% mysql_execute_command                                                                                                                                      ▒
                     - 44.75% execute_sqlcom_select                                                                                                                                   ▒
                        - handle_query                                                                                                                                                ▒
                           - 38.28% JOIN::exec                                                                                                                                        ▒
                              - 25.34% sub_select                                                                                                                                     ▒
                                 - 24.85% join_read_always_key                                                                                                                        ▒
                                      handler::ha_index_read_map                                                                                                                      ▒
                                    - ha_innobase::index_read                                                                                                                         ▒
                                       - 24.85% row_search_mvcc                                                                                                                       ▒
                                          - 24.85% trx_assign_read_view                                                                                                               ▒
                                             - MVCC::view_open                                                                                                                        ▒
                                                - 12.00% sync_array_wait_event                                                                                                        ▒
                                                   - 5.44% os_event::wait_low                                                                                                         ▒
                                                      - 2.21% os_event::wait_low                                                                                                      ▒
                                                           __pthread_mutex_unlock                                                                                                     ▒
                                                           system_call                                                                                                                ▒
                                                           sys_futex                                                                                                                  ▒
                                                         + do_futex                                                                                                                   ▒
                                                      + 2.04% __pthread_mutex_lock                                                                                                    ▒
                                                      + 0.94% pthread_cond_wait                                                                                                       ▒
                                                   + 2.34% __pthread_mutex_lock                                                                                                       ▒
                                                   + 2.28% sync_array_free_cell                                                                                                       ▒
                                                   + 1.60% sync_array_wait_event                                                                                                      ▒
                                                + 10.69% sync_array_reserve_cell                                                                                                      ▒
                                                + 1.32% os_event_set
```
These functions are largely wrappers around a pthread locking implementation. From the version history these were imported from MySQL-5.0 with minor modification in 2013 compared to the pthread implementation that receives significant maintenance from the glibc community represented by major CPU architecture manufacturers. 

Thankfully, MySQL has a compile option _-DMUTEXTYPE=sys_ that results in [pthreads being used directly](https://github.com/mysql/mysql-server/blob/mysql-5.7.28/storage/innobase/include/ib0mutex.h#L110..L123) and that increased x86 performance marginally, but much more significantly on POWER (understandable as since the sync_array elements have multiple instances on the same cache line size of 128 bytes compared to x86_64 which is 64 bytes). I'll soon get to benchmarking these changes in more detail and generate some bug report to get this default changed in distro packages at least.

Encode - Another example
------------------------

Even while carrying out this investigation a [MariaDB zulip chat](https://jira.mariadb.org/browse/MDEV-21285) exposed a benchmark of [ENCODE](https://mariadb.com/kb/en/library/encode/) (notably deprecated in MySQL-5.7) having scaling problems. Using the exact techniques here it was quick to generate and extracted a perf profile ([MDEV-21285](https://jira.mariadb.org/browse/MDEV-21285)) and stack that showed every initial guess at the source of the problem – including mine – was incorrect. With the perf profile, however, the nature of the problem is quite clear – unlike the solution. That requires more thought.

Report/Show your perf recordings
--------------------------------

Alongside its low overhead during recording, the useful aspect of perf from a DBA perspective is that perf stack traces show only the MySQL code being executed, and the frequency of its execution. There is no exposed database data, SQL queries, or table names in the output. However, the [Perf Events and tool security (item 4)](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html#overview) indicates that registers can be captured in a perf recording so be careful about sharing raw perf data. 

Once the raw perf data is processed by _perf report_, with correct debug info and kernel, there are no addresses and only mysqld and kernel function names in its output. The most that is being exposing by sharing a perf report is the frequency of use of the MySQL code that was obtained externally. This should be enough to convince strict and competent managers and security people to sharing the perf recordings. 

With some realistic expectations (code can't execute in 0 time, all of the database can't be in CPU cache) you should now be able to show the parts of MySQL that are limiting your queries.

### Resulting bug reports

MySQL:
* [bug 97777](https://bugs.mysql.com/bug.php?id=97777)
* [bug 97822](https://bugs.mysql.com/bug.php?id=97822)

MariaDB: 
* [MDEV-21145 ](https://jira.mariadb.org/browse/MDEV-21145)
* [MDEV-21452](https://jira.mariadb.org/browse/MDEV-21452)
* [MDEV-21212](https://jira.mariadb.org/browse/MDEV-21212)

-- 

_Disclaimer: The postings on this site are the authors own and don't necessarily represent IBM's positions, strategies or opinions._ 

_The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._ 

Photo by [Ricardo Gomez Angel](https://unsplash.com/@ripato?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/perforations?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)