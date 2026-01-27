---
id: "2ee674d0-91f3-80c4-87f4-ced74b919b1b"
title: "Running your databases on Kubernetes in the cloud: what is the overhead?"
layout: single
speakers:
  - fernando_laudares_camargos
talk_url: "https://www.mysqlandfriends.eu/post/prefosdem-mysql-belgian-days-2026-agenda/"
presentation_date: "2026-01-29"
presentation_date_end: ""
presentation_time: "1:50 pm"
talk_year: "2026"
event: "MySQL Belgian Days (preFOSDEM) 2026"
event_status: "Accepted"
event_date_start: "2026-01-29"
event_date_end: ""
event_url: "https://sessionize.com/prefosdem-mysql-belgian-days"
event_location: "Belgian, Brussels"
talk_tags: ['MySQL']
slides: ""
video: ""
---
## Abstract

One way of looking at Kubernetes is that it is all about convenience. Considering you are using an operator, you can easily and quickly deploy a new database environment in the cloud that is highly available and comes pre-configured with backups. But do we get the same performance from our database compared to running it in the same cloud but without Kubernetes? After all, the latter implies using containers on top of an already virtualized environment, over which we have less control.

To gain a better understanding of the level of overhead imposed by the Kubernetes layer, I experimented with running Sysbench's OLTP and TPC-C read-write workloads on a MySQL environment deployed directly on cloud instances. I then repeated the same tests on a Kubernetes-based environment using the same cloud instances and persistent storage. This talk presents the results of these tests conducted on two different cloud providers in two distinct scenarios: one in which the dataset fits in the database cache and another in which it does not.

Although the primary goal of these experiments was to address the overhead question for these controlled environments and workloads, this talk also provides insight into what it looks like to run databases on Kubernetes.