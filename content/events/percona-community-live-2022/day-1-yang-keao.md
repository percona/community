---
title: "Emulate Block Device Incidents With IO Scheduler"
description: "Block device incidents are frequent and frightening in production. To achieve high availability, distributed databases usually have fault tolerant strategies to handle these incidents."
images:
  -  events/percona-community-live/cards/Community-Live-Day-1-Yang-Keao.jpg
PublishedDate: "2022-06-21"
draft: false
day: "June 21"
speakers:
  - yang_keao
tags: ['Percona Community Live']
---

![Emulate Block Device Incidents With IO Scheduler](events/percona-community-live/cards/Community-Live-Day-1-Yang-Keao.jpg)

This session was presented on [Percona Community Live](/events/percona-community-live-2022/) Online June 21-23, 2022. Check out the full schedule [here](/events/percona-community-live-2022/).

Block device incidents are frequent and frightening in production. To achieve high availability, distributed databases usually have fault tolerant strategies to handle these incidents. As the system gets more complicated, it's even hard to prove whether these strategies are working. For example, if the execution and distribution of scheduling commands also depend on the hanging storage, it will have no effect.

In order to help developers verify the performance of their databases under storage disasters, we designed a Linux IO scheduler called IOEM to emulate the properties of block devices.

IOEM allows developers to specify latency and IOPS per block device and process, making it possible to emulate a complex cluster with limited resources. Developers can emulate a wide range of properties of storage devices with little overhead. Besides the incidents, IOEM can also be used to measure the performance of databases under low-end storage devices.

In this talk, Yang Keao will show a real-world example where the fault-tolerant strategies failed, and how they reproduced them in the development environment with the help of IOEM. He will also introduce the structure and implementation of IOEM, compare it with other implementation of block device latency injection, and describe the convenience it will bring to the development of databases.

## Watch Video Here

{{% youtube youtube_id="LQHxt3DtQxk" %}}{{% /youtube %}}

## Transcript

