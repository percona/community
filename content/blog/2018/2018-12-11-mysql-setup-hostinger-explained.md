---
title: 'MySQL Setup at Hostinger Explained'
date: Tue, 11 Dec 2018 15:27:45 +0000
draft: false
tags: ['hosting', 'MySQL', 'ProxySQL', 'Tools', 'Zookeeper Cluster']
authors:
  - donatas_abraitis
images:
  - blog/2018/12/mysql-setup-hostinger.jpg
slug: mysql-setup-hostinger-explained
canonical: https://www.hostinger.com/blog/mysql-setup-at-hostinger-explained
---

Ever wondered how hosting companies manage their MySQL database architecture? At [Hostinger,](https://www.hostinger.com/) we have various MySQL setups starting from the standalone replica-less instances to [Percona XtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster) (later just PXC), [ProxySQL](http://www.proxysql.com/) routing-based and even absolutely custom and unique solutions which I’m going to describe in this blog post. 

We do not have elephant-sized databases for internal services like API, billing, and clients. Thus almost every decision ends up with high availability as a top priority instead of scalability. 

Still, scaling vertically is good enough for our case, as the database size does not exceed 500GB. One and the top requirements is the ability to access the master node, as we have fairly equal-distanced workloads for reading and writing. 

Our current setup for storing all the data about the clients, servers and so forth is using PXC formed of three nodes without any geo-replication. All nodes are running in the same datacenter. 

We have plans to migrate this cluster to geo-replicated cluster across three locations: the United States, Netherlands, and Singapore. This would allow us to warrant high availability if one of the locations became unreachable. 

Since PXC uses fully synchronous replication, there will be higher latencies for writes. But the reads will be much quicker because of the local replica in every location. 

We did some research on [MySQL Group Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication.html), but it requires instances to be closer to each other and is more sensitive to latencies.

> Group Replication is designed to be deployed in a cluster environment where server instances are very close to each other, and is impacted by both network latency as well as network bandwidth.

PXC was used previously, thus we to know how to deal with it in critical circumstances and make it more highly available. 

In [000webhost.com](https://www.000webhost.com/) project and hAPI (Hostinger API) we use our aforementioned unique solution which selects the master node using Layer3 protocol. 

One of our best friends is BGP and BGP protocol, which is aged enough to buy its own beer, hence we use it a lot. This implementation also uses BGP as the underlying protocol and helps to point to the real master node. To run BGP protocol we use the ExaBGP service and announce VIP address as anycast from both master nodes. 

You should be asking: but how are you sure MySQL queries go to the one and the same instance instead of hitting both? We use [Zookeeper’s ephemeral nodes](https://zookeeper.apache.org/doc/current/zookeeperOver.html) to acquire the lock as mutually exclusive. 

Zookeeper acts like a circuit breaker between BGP speakers and the MySQL clients. If the lock is acquired we announce the VIP from the master node and applications send the queries toward this path. If the lock is released, another node can take it over and announce the VIP, so the application will send the queries without any efforts. 

![mysql setup at hostinger](blog/2018/12/mysql-setup-hostinger.jpg) 
_MySQL Setup at Hostinger_ 

The second question comes: what conditions should be met to stop announcing VIP? This can be implemented differently depending on use case, but we release the lock if MySQL process is down using systemd’s `Requires` in the unit file of ExaBGP:

> Besides, with or without specifying After=, this unit will be stopped if one of the other units is explicitly stopped.

With [systemd](https://www.freedesktop.org/wiki/Software/systemd/) we can create a nice dependency tree which ensures all of them are met. Stopping, killing, or even rebooting the MySQL will make systemd stop the ExaBGP process and withdraw the VIP announcement. The final result is a new master selected. 

We battle tested those master failovers during our [Gaming days](https://www.hostinger.com/blog/new-network-infrastructure) and nothing critical was noticed _yet_. 

If you think good architecture is expensive, try bad architecture 😉 

-- _This post was originally published at [https://www.hostinger.com/blog/mysql-setup-at-hostinger-explained/](https://www.hostinger.com/blog/mysql-setup-at-hostinger-explained/) in June 2018. The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource **test** ideas before applying them to your production systems, and **always **secure a working back up._