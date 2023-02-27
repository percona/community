---
title: 'Percona Live ONLINE: MySQL on Google Cloud: War and Peace! by Akshay Suryawanshi & Jeremy Cole'
date: Tue, 02 Jun 2020 16:12:51 +0000
draft: false
tags: ['author_lawrence', 'DevOps', 'Google', 'Kubernetes', 'Kubernetes', 'MySQL', 'MySQL', 'mysql-and-variants', 'Open Source Databases', 'Shopify']
images:
  - blog/2020/06/SC-3-Matt-Percona.jpg
authors:
  - cate_lawrence
slug: percona-live-online-mysql-on-google-cloud-war-and-peace-by-akshay-suryawanshi-jeremy-cole
---

This session at [Percona Live ONLINE](https://www.percona.com/live/conferences) was presented by Akshay Suryawanshi, Senior Production Engineer at Shopify, and Jeremy Cole, Senior Staff Production Engineer - Datastores at Shopify. Shopify is an online and on-premise commerce platform, founded in 2006. 

Shopify is used by more than a million merchants, and hundreds of billions of dollars of sales have happened on the platform since its inception. The company is a large user of MySQL, and the Black Friday and Cyber Monday weekends are their peak dates during the year, handling hundreds of billions of queries with MySQL. This year’s presentation was an opportunity to talk about the company’s challenges and progress over the last twelve months.

Key Google Cloud concepts from the presentation
-----------------------------------------------

As part of the presentation, it’s important to understand the naming conventions that exist around Google Cloud:

*   Regions - a geographic region where cloud operates (these could include a building or adjoining buildings)
*   Zones - a subdivision inside particular regions. Typically there are three within each region, but it varies a bit by region.
*   GCE - Google Compute Engine platform, the system provides virtual machines to run as servers (most of Shopify’s microscale infrastructure is on GCP and runs in VMs).
*   Virtual machine instance - A GC virtual machine scheduled in a particular zone
*   Persistent disk - A network-attached log-structured block storage zone
*   GKE - Google's Kubernetes Engine, a managed Kubernetes solution that is managed on top of Google Cloud Platform (GPC) and managed within Google Cloud.

Peacetime stories
-----------------

Akshay spoke about Persistent disks, which are Network-Attached, distributed log-structure, block storage: “This is the place where you basically say most of your data is, especially when you're running MySQL data or any sort of databases.” Except for their performance, (which is usually affected by some degree of latency for network-attached storage) they provide incredible features, especially fast snapshotting of volumes. 

"We have utilized the snapshotting behavior to revamp our Backup and Restore infrastructure and brought down our recovery time to less than one hour for even a multi-terabyte disk. This is so incredibly fast that we actually restore each and every snapshot that we preserve or retain as a backup every single day. It's happening in both regions where we run most of our MySQL fleet,” detailed Akshay.

Configurable VMs
----------------

Virtual machines (VMs) expose an extensive API which is useful to do things programmatically with: “The API is very helpful. It is well documented, and we are using it in a bunch of places,” continued Akshay. 

Scaling VMs up and down are seamless operations (of course, most of them require a restart) and manageable. Provisioning new VMs in an appropriate region is very easy, according to Akshay: "Again because of the extensive API, which has provided something required to build resiliency against its own failures. So we spread our VMs across multiple zones. That helps us tremendously when a particular zone goes down. All of this has allowed us to build self-healing tooling to automatically replace failed VMs easily.”

GCP is truly multi-regional
---------------------------

Google Cloud’s multi-region availability means failover from one region to another is easy and Shopify can move all its traffic from one region to another in just a few minutes, multiple times in a day. They can also expand to a distant geographical region without a lot of work, yet maintain the same stability. 

Akshay noted: "Isolating PII data has been a big win for Shopify in the past year when we launched a certain product where PII data needed to be preserved in a particular region, and GCP provides excellent support for that."

Google Kubernetes Engine
------------------------

Kubernetes is an open-source project for container orchestration and Google Kubernetes Engine (GKE) is a feature-rich tool for using and running Kubernetes. According to Akshay: "Most of our future work is happening towards containers writing MySQL and running and scheduling them inside companies. The automatic storage and file system expansion are helpful in solving database problems.” 

Zone aware cluster node scheduling helps schedule the Kubernetes pods so that they are fault-tolerant towards zone failures. 

The GCP networking is simple to set up. Inter-regional latencies are pretty low, and Shopify can perform region failovers for databases quickly in the event of a disaster. "We can do a whole region, evac within a few minutes. This is because we can keep our databases in both regions up to date due to these low latencies," explained Akshay. 

Virtual private clouds (VPCs) are a great way to segment the workloads. Isolating the networking connection at VPC level has helped this achievement.

War: Some of the things that can go wrong
-----------------------------------------

Jeremy detailed some of the specific challenges that Shopify had faced over the last year, including stock outs which are when a resource requested (such as a VM or a disk) is not available at that time. 

Jeremy noted: “What that looks like is that you attempt to allocate it using some API, and it just takes a very long time to show up. In one particular instance, in one region, we had consistent PD and VM stockouts regularly occurring for several weeks.” 

It meant that the company had to adapt for when resources were not available at a moment’s notice, and to consider where time-critical components had to be resourced for availability.

Trouble in persistent disk land
-------------------------------

According to Jeremy: "One of the bigger problems that we've had in general is a persistent disk (PD).” An example was a recent outage caused by a change in persistent disks backend, which caused a regression “anywhere from minor latency impacts to full stalls for several seconds of the underlying PD volume, which of course, pretends to be a disk. So that means the disk is fully stalled for several seconds." 

It took several weeks to diagnose and pin the blame of the stalls on PD properly. Jeremy noted, “The fun part of the story is that the mitigation for this particular problem involves attaching a substantial PD volume to every one of our VMs to work around a problem that was happening in PD. In order to do that, since we had so many VMs in aggregate, we had to allocate petabytes of persistent disk, and leave them attached for a few months.” 

Crucial to solving the problem was working closely with their vendor partner. As Jeremy explained, “Sometimes you have to get pretty creative to make things work right now and get yourself back in action.

Troop replacements
------------------

Live migration (LM) was referred to in the previous year’s Shopify presentation at Percona Live, and the problem still persists according to Jeremy. “We continuously have machines being live migrated and their VMs being moved around between different physical machines.” 

The frequency of LM problems occurring and the number of times it causes this problem is directly related to the frequency of Linux kernel or Intel CDEs. “We're still getting hostError instance failures where migrations fail and this kills the host,” explained Jeremy. 

Some live migrations are still breaking in NTP time sync. “And we are still periodically getting multiple migrations per VM for the same maintenance - up to 11 within a day or so.”

A regional ally surrenders
--------------------------

In the last year, there was a regional outage: "Google had made a change to their traffic routing in one region, causing basically an overload of their networking stack. And we went down pretty hard because of that. There was nothing really that we could do about it," said Jeremy. This was despite being deployed across multiple zones and multiple regions. 

Jeremy concluded the talk with a simple statement: Running MySQL in the cloud is not magic. “There are some unique challenges to Google Cloud, unique challenges to running MySQL in cloud infrastructure and unique challenges with the cloud itself. Sometimes running databases in the cloud can feel like you are constantly at war.” 

Preparing in advance as much as possible around how you manage your database in the cloud can help, particularly when you run at the kind of scale that Shopify does. However there will always be unexpected events and incidents. Working with your cloud partner and support providers can help here too.

_You can [watch a video of the recording](https://www.percona.com/resources/videos/mysql-google-cloud-war-and-peace-akshay-suryawanshi-jeremy-cole-percona-live-online) which includes a Q&A at the end of the presentation._