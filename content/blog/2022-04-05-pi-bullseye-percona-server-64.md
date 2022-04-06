---
title: 'Raspberry Pi Bullseye Percona Server 64bit'
date: "2022-04-05T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', '64bit', 'Raspberry Pi', 'Bullseye']
authors:
  - wayne
images:
  - blog/2022/4/bullseye.jpg
slug: Percona-Server-Raspberry-Pi
---

So if you know me, you know I love the Raspberry Pi and Percona Server.
I did a my first blog post on installing Percona Server 5.7 on the Raspberry
Pi 3+.

Please check out my previous post: [How to Build a Percona Server "Stack" on a Raspberry Pi 3+](https://percona.community/blog/2019/08/01/how-to-build-a-percona-server-stack-on-a-raspberry-pi-3/)

Fast forward to 2022 and we now have the resources to build Percona Server 8.0
on the Raspberry Pi 4.

In this post I will cover Percona Server 8.0.27 and Percona XtraBackup 8.0.27.

One Warning! The build is a bit long, but worth it. Well in my twisted mind it is.

I wont cover installing Raspbian Bullseye, you can follow the steps here: [Install Raspberry Pi OS Bullseye on Raspberry Pi](https://raspberrytips.com/install-raspbian-raspberry-pi/)

Prereqs:

1. Raspberry Pi 4, 4GB or 4GB model.
2. Raspbian Bullseye 64bit.

```
sudo apt install bison pkg-config cmake devscripts debconf debhelper \
automake bison ca-certificates libcurl4-gnutls-dev cmake libaio-dev \
libncurses-devlibssl-dev libtool libz-dev libgcrypt-dev \
libev-dev lsb-release python-docutils build-essential rsync libdbd-mysql-perl \
libnuma1 socat librtmp-dev libtinfo5 qpress liblz4-tool liblz4-1 liblz4-dev
```
