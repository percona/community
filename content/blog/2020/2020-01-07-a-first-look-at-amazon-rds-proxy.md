---
title: 'A First Look at Amazon RDS Proxy'
date: Tue, 07 Jan 2020 11:45:40 +0000
draft: false
tags: ['renato-losio', 'Amazon RDS', 'AWS', 'aws', 'DevOps', 'MySQL', 'proxy', 'RDS', 'RDS Proxy']
authors:
  - renato_losio
images:
  - blog/2019/12/allie-smith-zp-0uEqBwpU-unsplash-50.jpg
slug: a-first-look-at-amazon-rds-proxy
---

At [re:Invent](https://reinvent.awsevents.com/) in Las Vegas in December 2019, **AWS announced the public preview of [RDS Proxy](https://aws.amazon.com/rds/proxy/)**, a fully managed database proxy that sits between your application and RDS. The new service offers to "_share established database connections, improving database efficiency and application scalability"_. 

But one of the benefits that caught my eye is the ability to reduce the downtime in case of an instance failure and a failover. As for the announcement:

![Photo by Allie Smith on Unsplash](blog/2019/12/allie-smith-zp-0uEqBwpU-unsplash-50.jpg)

> In case of a failure, RDS Proxy automatically connects to a standby database instance while preserving connections from your application and reduces failover times for RDS and Aurora multi-AZ databases by up to 66%"

You can read more about the announcement and the new service on the AWS [blog](https://aws.amazon.com/about-aws/whats-new/2019/12/amazon-rds-proxy-available-in-preview/) but as the service is already available in public preview, it is time to give it a try.

What does "reduces failover times by 66%" mean and how can we test it?
----------------------------------------------------------------------

According to the documentation:

> "Failovers, as defined by the interval between the detection of the failure on the primary and the resumption of transactions on the standby, typically complete within one to two minutes. Failover time can also be affected by whether large uncommitted transactions must be recovered; the use of adequately large instance types is recommended with Multi-AZ for best results. "

So I decided to perform a simple test, using only two terminals, a MySQL client and a while loop in Bash: I wanted to check what happens when I trigger **a forced failover (reboot with failover)** on a Multi AZ RDS instance running MySQL 5.7.26 behind a RDS Proxy.

### The simplest test

I created a new proxy _"test-proxy"_ that pointed to a m5.large Multi AZ _"test-rds"_ instance. And I set the idle client connection timeout to 3 minutes, a value that should allow us to avoid dropping connections given the expected failover time on the RDS instance. 

![Creating RDS Proxy](blog/2019/12/Screenshot_2019-12-19-RDS-·-AWS-Console.png) 

And after a few minutes I was ready to go. I started two while loops against the proxy and against the instance, each retrieving current time from MySQL:
```
$ while true; do mysql -s -N -h test-proxy.proxy-cqz****wmlnh.us-east-1.rds.amazonaws.com -u testuser -e "select now()"; sleep 2; done

$ while true; do mysql -s -N -h test-rds.cqz****wmlnh.us-east-1.rds.amazonaws.com -u testuser -e "select now()"; sleep 2; done
```
Acknowledged, this is a pretty basic and limited approach, but one that can quickly provide a feeling of how the RDS proxy performs during a forced failover. **test-rds instance**
```
2019-12-16 18:45:48
2019-12-16 18:45:50
2019-12-16 18:45:52
2019-12-16 18:45:54
(...)
```
**test-proxy proxy**
```
2019-12-16 18:45:48
2019-12-16 18:45:50
2019-12-16 18:45:52
2019-12-16 18:45:54
(...)
```
Which terminal was going to be the winner and have the smallest gap in the time **once I triggered the reboot with failover?**
```
aws rds reboot-db-instance --db-instance-identifier test-rds --force-failover
```Let's see the results. **test-rds instance**```
(...)
2019-12-16 18:47:31
2019-12-16 18:47:33 
2019-12-16 18:49:44
2019-12-16 18:49:46
(...)
```
**test-proxy proxy**
```
(...)
2019-12-16 18:47:31
2019-12-16 18:47:33
2019-12-16 18:47:56
2019-12-16 18:47:58
(...)
```
**From a delay of 129 seconds for the "test-rds" instance to 21 seconds for the proxy**, it is quite a significant difference. Even better than the advertised 66%. I performed the test a couple of more times to make sure the result was not a one off, but the numbers are pretty consistent and **the gap was always significant**.

### Main limitations and caveats

As of today, RDS Proxy is in public preview and available for RDS MySQL (MySQL 5.6 and MySQL 5.7) and Aurora MySQL . There is currently no support for RDS PostgreSQL or Aurora PostgreSQL. And it's important to note: **there is as yet no opportunity to change the instance size or class once the proxy has been created. That means it cannot be used to reduce downtime during a vertical scaling of the instance, which would be one of the main scenarios for the product.** 

You can still trigger a modifying instance on the Multi AZ RDS but the proxy will then not be able to recover after a scaling operation. It will still be there but will only provide a "MySQL server has gone away" message.
```
ERROR 2006 (HY000) at line 1: MySQL server has gone away
ERROR 1105 (HY000) at line 1: Unknown error
ERROR 2006 (HY000) at line 1: MySQL server has gone away
ERROR 2006 (HY000) at line 1: MySQL server has gone away
ERROR 2006 (HY000) at line 1: MySQL server has gone away
```
That is actually expected. As per the documentation:

> "Currently, proxies don't track any changes to the set of DB instances within an Aurora DB cluster. Those changes include operations such as host replacements, instance renames, port changes, scaling instances up or down, or adding or removing DB instances."

You can find all the current limitations [here](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html#rds-proxy.limitations).

What about costs?
-----------------

Compared to other more convoluted AWS models, **the pricing structure of RDS Proxy is actually [simple](https://aws.amazon.com/rds/proxy/pricing/)**: you pay a fixed hourly amount ($0.015 in us-east-1) per vCPU of the underlying database instance, regardless of instance class or other configurations. The larger the instance running behind the Proxy, the higher the price.

### How is that going to affect your overall RDS costs?

Let's take two popular instances t3.small (1vCPU) and m5.large (2 vCPU): the cost of the Proxy is about 12 USD and 24 USD per month. That is about 8% on top of cost of the Multi AZ instance for the m5.large, and over 20% for the t3.small. 

Of course, as you are likely preserving connections, you might be able to absorb the cost of the proxy itself by running a smaller instance, but that might not be always the case. 

Note that as per the current documentation, the Amazon RDS Proxy preview was free until the end of 2019 only. 

To recap, **RDS Proxy is a new service by Amazon and still in preview but the results in term of reduced failover times are really promising.** On top of providing a simpler layer to handle database connections for serverless architectures. 

_The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content. Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._ 

_--_ 
_Photo Allie Smith on [Unsplash](https://unsplash.com/)_