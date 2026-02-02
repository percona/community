---
title: "The Ins and Outs of PostgreSQL Default Configuration Tuning"
date: "2022-03-31T00:00:00+00:00"
draft: false
tags: ['Postgres', 'PostgreSQL', 'MySQL']
categories: ["PostgreSQL"]
images:
    - blog/2022/3/Meetups-PG-1.jpg
authors:
  - aleks_abramova
---

If you're wondering what the optimal settings for a newly installed Postgres database are, here are some simple steps to take to tune it right from the start. Matt Yonkovit discussed them with Charly Batista, Postgres Tech Lead at Percona during the live-streamed meetup. Watch the [recording](https://percona.community/events/percona-meetups/2022-01-27-percona-meetup-for-postgresql/) to see how Charly tunes a default installation of Percona Distribution for PostgreSQL 13.

Most of the default settings have been defined long, long time ago, where one gigabyte of RAM was very expensive. So, they are not optimal. There are lots of things that we can change, but let’s have a look at the basic things to make your box more reliable and raise both in speed and performance. They can be divided into 2 groups: OS settings (Linux kernel) and database settings.

## OS (Linux) Settings

No matter that is your workload, these things you want to make sure you have set from the operating system perspective out of the gate to make your box healthier.

### Swap and Swappiness

Allocate swap to prevent the kernel from killing the database. But keep in mind that swappines should not be too high. What is this swappiness? The swappiness tells the kernel how likely it should use the swap. Change it to 1 to allow the kernel to use the swap only when it is really necessary. 
For swap, we need to create a file and then allocate it. For the swappiness, we can tell the systemctl to change the swappiness of our box. 

### Transparent Huge Pages

Transparent huge pages are enabled by default on the Linux kernel.  And it’s not a good thing for databases like Postgres. They can cause a lot of memory fragmentation. It can slow down your database and also cause memory problems. For example, you need one gigabyte of memory for one activity, and even though you have one gigabyte available, they are split into small pieces. You cannot allocate that one gigabyte of memory. The first thing that the kernel will try to do is swap. It will just kill the database. So the transparent huge page can lead to performance issues, because we just don’t have memory, even though the memory is there, but the memory is not able to allocate.

### CPU Speed

Make sure the CPU runs at its max speed. Find the CPU Governor file and disable the on-demand utility. For the database, we don’t want to adjust on-demand, we always want it as fast as we can.

## Postgres Settings

Here are some database settings that you can change to optimize your database regardless of the workload you have.

### Shared Buffers Value

Change the value for shared buffers to 8 GB. You can ask - why? When we talk about MySQL, a good value for the shared buffer is 50% to 70% of your memory because that will give you the ability to grow. Typically, you want your hot data all in shared memory, all data that is access at a high frequency. But unlike MySQL, Postgres relies a lot on OS buffers. In case of Postgres, if you write intensive workload, it might want to get your shared buffer much smaller, like around 5% of memory that you have, because most of the things are going to go for the kernel buffer.

### Random Page Cost

Make sure you get the random page cost right. The random page cost is one that we think could be a big win for us, just because the default is so high compared to sequential. Lowering that by default is probably a good thing. Random page cost is the cost optimizer change. So, it’s going to push random pages to be a bit more costly and favor some sequential. 

We need to understand how Postgres stores data, and how Postgres stores the indexes. MySQL uses cluster storage here. The data that is stored on Postgres is not a cluster, it doesn’t organize the data. So it just keeps it. Random page cost is going to improve the index usage because it will prefer indexes. It changes the cost optimizer to prefer random pages or index scans over sequential. And it can improve or decrease performance a lot.

Note that to be able to get the random page cost right, you need to understand what kind of disks you have. If you are using AWS, we suppose you have SSDs and NVMe. They are really fast. And the cost for the random page is almost the cost of the sequential page, which is why the change is not so high. 

### Synchronous Commit

So one thing that we can change on Postgres is the synchronous commit. The synchronous commit will force the database to commit every time to the cache, to the kernel, every time that you do a commit or transaction. It is a trade off that can improve performance. But you lose a little on reliability. 

But here is one setting on Postgres that you should never change even trying to improve performance - **fsync**. Just never change it. By default, it is on, and it is on the top of the synchronous commit. The fsync instructs the kernel to write flash data to the disk for crash safety. If you disable the fsync, you might have some performance benefits, but your writes to the disk become not safe enough. You can have disk corruption. It’s really based on the disk having its own cache and its own systems going on, and you’re basically relying on it to do everything for you, instead of forcing that right to be consistent. It’s fine to work and tune and play around the synchronous commit, but not with the fsync.

## Conclusion

Everything above are things that are independent of your workload. But there are no strict rules that you should, for example, use eight gigabytes of shared buffer if you have 32 gigabytes of memory. After you do all of those things, come back again, run the load test to check your performance. You can’t get worse performance instead of better performance. 

