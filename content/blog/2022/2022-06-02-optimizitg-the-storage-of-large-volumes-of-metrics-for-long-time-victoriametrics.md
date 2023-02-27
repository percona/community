---
title: "Optimizing the Storage of Large Volumes of Metrics for a Long Time in VictoriaMetrics"
date: "2022-06-02T00:00:00+00:00"
draft: false
tags: ['blog', 'metrics', 'VictoriaMetrics']
images:
  - blog/2022/6/VictoriaMetrics.jpg
authors:
  - anton_bystrov
slug: 'long-time-keeping-metrics-victoriametrics'
---

## Introduction

Nowadays, the main tools for monitoring the operation of any application are metrics and logs. An important role is played by the time of their storage. Often, in order to understand certain processes and predict their development in the future, we need to analyze metrics over a fairly long period of time. In the case, when the project is just starting, their volume is relatively small, but over time it becomes larger and larger and there is a need for optimization. In this article, I will touch upon the mechanisms for processing, storing and optimizing metrics during their long-term storage.  

## VictoriaMetrics at a Glance

The monitoring solution and the base for storing time series VictoriaMetrics was released relatively recently - in 2018, but has already gained popularity.

Initially, VictoriaMetrics was designed as a time series database, but over time it has grown into a full-fledged alternative to Prometheus with its own ecosystem.

VictoriaMetrics is currently a fast, cost-effective and scalable monitoring solution. You can deploy the application either from a binary file, a docker image or a snap package, or build it yourself from the source code. Single-node and cluster versions are available.

## Why Choose VictoriaMetrics?

The main reasons for switching from Prometheus to VictoriaMetrics for us were significant savings in system requirements and the ability to work in Push mode.

Despite many external tests, we wanted to get our own data. Test bench configuration had 8 CPU, 32 GB RAM, SSD drive. The test lasted 24 hours. 25 virtual machines were the source, each of which emulated 10 MySQL instances. In terms of the volume of metrics, there were to 96100 metrics per second, the total volume was about 8.5 billion metrics per day.

The result of testing was about three times less disk space usage with VictoriaMetrics (8.44 GB against 23.11 with Prometheus), approximately twice less the amount of RAM. The CPU requirements were about the same.

As for the push mode, it works as follows: exporters work on the target host and collect metrics, then in the classical scheme of work, Prometheus polls the exporters and collects metrics at specified intervals. This scheme of operation has a significant disadvantage as we need to maintain several ports open. The new scheme uses the VMAgent component, which is installed on the client side and collects metrics from exporters, after which it pushes to the VictoriaMetrics server.

Also, important factors in favor of VictoriaMetrics were: ease of installation and subsequent support, the possibility of more flexible performance settings and the availability of features that are not available in other applications. For example, Prometheus lacks downsampling.

## VictoriaMetrics Single-Node and Cluster Versions

VictoriaMetrics can work in two versions: single-node and cluster.

The single-node version is used for relatively small amounts of data (less than a million metrics per second) and does not provide scalability and fault tolerance, since all application components are connected into a monolith.

VictoriaMetrics consists of the following components:

1. **vmstorage** - the storage itself;
2. **vminsert** - endpoint for receiving metrics based on the Prometheus remote_write API;
3. **vmselect** - a component that allows you to make queries using the Prometheus querying API.

In the official documentation, developers recommend using the single-node version and use clustered version only if there is a real need, and you understand the consequences of such a decision.

## General Principles of TSDB Work

TSDB (a time series database) is used as a database for storing metrics. TSDB has many differences compared to relational databases - write operations prevail over read operations, there are no relationships between data. Since the metric has one value at a certain point in time, there is no need for nested structures. Typically, an amount of data is large.

The unit of data in such a database is a time point. The data structure of such a point consists of:

1. timestamp - time in Unix format
2. The __name__ field, from which the name of the metric is taken. This field can be missing, but this is an antipattern, because in any case we need to know the name of the metric we are tracking.
3. Additional Label fields that are needed for any actions with metrics (aggregation by some attribute, filtering, etc.)
4. Field with metric value.

When data is recorded, time series are formed. A time series is a sequence of strictly monotonically increasing data points over time that can be accessed using a metric.

Thus, we can say that the database is relatively "static", because it contains a certain amount of data (metrics) that do not change over time. That means that, the data in these time series increases  over time, but their number remains the same. This is the basis for optimization examples that will be discussed later.

## Optimization of Large Queries

If the number of metrics and their storage time increases, the amount of required resources for the application inevitably increases too. VictoriaMetrics has mechanisms for adjusting consumed resources.

The `memory.allowedPercent` and `memory.allowedBytes` keys allow you to limit the amount of memory for external buffers and query caching data.

The `search.maxUniqueTimeseries` key prevents excessive resource consumption when executing large queries, and in some cases can prevent the application from crashing with an out of memory error when executing large queries. This parameter is set to 300000 by default and reflects the number of unique series returned in response to the request to `/api/v1/query` and `/api/v1/query_range` endpoints.

Also, the `search.maxSamplesPerQuery` key can be very useful, which limits the number of returned metrics in one query.

The `search.maxQueueDuration` key is responsible for the time to wait for a response to a request.

In general, there are a fairly large number of keys that affect performance. In this post, I mention only whose that we use in our practice.

## What Downsampling Is and How It Works

An important feature of VictoriaMetrics is downsampling - the ability to delete data as it becomes obsolete. This functionality is available only in the Enterprise version. But it is also built into PMM - Percona Monitoring and Management.

As I mentioned above (in the paragraph describing the features of the TSDB work), time series must have a large amount of data and be unchanged in order to obtain maximum sampling efficiency.

The -downsampling.period key is responsible for the work. Example: the frequency of collecting metrics in our case is once every 5 seconds, but in this case, the volume of the database will grow very quickly if we have a large amount of metrics. So we define a policy for storing metrics - after one hour we store metrics with an interval of 10 seconds, every other day with an interval of 30 seconds, after a week - with an interval of 1 minute, after a month - with 5 minutes, after a year - 1 hour. So it will look like this:
`-downsampling.period=1h:10s,1d:30s,1w:1m,30d:5m,360d:1h`

## What Deduplication Is and How It Works

Deduplication is a technology that allows you to analyze duplicate data and replace it with an appropriate reference. The use of deduplication can significantly reduce the amount of data. It is used when Prometheus or vmagent are working in HA mode and write to one VictoriaMetrics instance.

In this case, we definitely need deduplication, since the database stores overlapping data, which significantly increases its volume and, in case of large volumes, the data request time. The `dedup.minScrapeInterval` key is responsible for the operation of deduplication.

For example, `-dedup.minScrapeInterval=60s` means that within the same time series, all data will be collapsed and only the first point within 60 seconds will be saved. Since version 1.77 leave the last raw sample per each -dedup.minScrapeInterval discrete interval.

It is recommended to set this parameter to scrape_interval for metrics. According to best practice, scrape_interval should be the same for all metrics, but this is a topic is for a separate post.

## Example of Deduplication

As an example, let’s consider the case where scrape_interval=10s and minScrapeInterval=15s.

**Before deduplication:** 05, 10, 15, 25, 35, 45, 55

**interval:** [00...15] [15...30] [30...45] [45...60]
**timestamp:** [05 10] [15 25] [35 ] [45 55]

Thus, after deduplication, only those points will remain: 05, 15, 35, 45.

## Rotation of Metrics

Rotation of metrics is their removal when they become obsolete. The retentionPeriod key is responsible for rotation in the VM. By default, this period is 30 days. Therefore, you should immediately set the required storage period when launching VictoriaMetrics. Let's dive a little deeper into the features of data storage. Example: we set the metrics rotation time to 1 year, 4 months, 2 weeks, 3 days and 5 hours `-retentionPeriod=1.3y2w3d5h`. The year is a fractional number here to avoid the confusion with "m" which can mean both the month and the minute.

When writing, data is stored in directories like ../data/{small,big}. This directory contains data like rowsCount_blocksCount_minTimestamp_maxTimestamp. The directories are rotated as follows: in the first unit of time of the selected period (day, week, month, year), metrics for the period preceding the previous one are deleted. Example: metric rotation is set to 1 month by default. On March 1, the directory containing the data for January is deleted. An important feature is that it is possible to increase the rotation time without any data loss of the running instance. If the rotation time is reduced accordingly, the data that goes beyond this time will be deleted.

Based on personal experience, a sufficient data retention period for metrics will be one and a half years.

It is also worth emphasizing that if you plan to store data indefinitely, then you still need to set the data retention period, in this case it is set to a very large number, for example, 900 years.

## Conclusion

In this post, we looked into the possibilities that VictoriaMetrics can offer to optimize the storage of metrics and reduce the usage of disk space and RAM. It can help you to reduce your costs significantly, especially if you need to store a lot of metrics. But be mindful regarding the parameters to be set, with clear understanding of your goals.
