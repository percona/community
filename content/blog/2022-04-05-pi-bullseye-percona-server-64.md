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

I love the Raspberry Pi, and I love Percona server. The combination of the two can provide a nice home database. I have been running a Percona Server database since 2019 to hold all the weather information. That I collect from several of my Weather Stations.

I did a my first blog post on installing Percona Server 5.7 on the Raspberry Pi 3+.

You can read that blog post here:
[How to Build a Percona Server "Stack" on a Raspberry Pi 3+](https://percona.community/blog/2019/08/01/how-to-build-a-percona-server-stack-on-a-raspberry-pi-3/)

Fast forward to 2022 and we now have the resources to build Percona Server 8.0 on the Raspberry Pi 4. In this post I will cover building and installing Percona Server 8.0.27 and Percona XtraBackup 8.0.27.

**One Warning!** The builds will take sometime.

Prereqs:

1. Raspberry Pi 3B+, Pi 4 (any memory size will work).
3. 128GB or 256GB microSD card. Of course you can go bigger.

I won't cover installing Raspbian Bullseye, you can follow the steps here:
[Install Raspberry Pi OS Bullseye on Raspberry Pi](https://raspberrytips.com/install-raspbian-raspberry-pi/)

## The Builds

One step I have found which will help to increase the speed and success of your build is to add larger swap file.

In my build I have the source code sitting on a USB 3 SSD storage.

Create a new swap file. I found that a 4GB file worked just fine. I created the swap file on the / partition.

```
$ sudo dd if=/dev/zero of=/swapfile4GB bs=1M count=4096
$ sudo mkswap /swapfile4GB
$ sudo swapon /swapfile4GB
$ sudo chmod 0600 /swapfile4GB
```

You will need to install these additional packages listed below:
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install build-essential pkg-config cmake devscripts debconf debhelper automake bison ca-certificates libcurl4-gnutls-dev libaio-dev libncurses-dev libssl-dev libtool libgcrypt20-dev zlib1g-dev lsb-release python3-docutils build-essential rsync libdbd-mysql-perl libnuma1 socat librtmp-dev libtinfo5 liblz4-tool liblz4-1 liblz4-dev libldap2-dev libsasl2-dev libsasl2-modules-gssapi-mit libkrb5-dev apt-get libreadline-dev
libudev-dev libev-dev libev4

```
Let's download Percona Server and some additional tools.

```
$ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.28-19/source/tarball/percona-server-8.0.28-19.tar.gz
$ tar -zxvf percona-server-8.0.28-19.tar.gz
$ wget https://boostorg.jfrog.io/artifactory/main/release/1.73.0/source/boost_1_73_0.tar.gz
$ tar -zxvf boost_1_73_0.tar.gz
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.28-21/source/tarball/percona-xtrabackup-8.0.28-21.tar.gz
$ tar -zxvf percona-xtrabackup-8.0.28-21.tar.gz
```

## Build Percona Server
At the time of writing 8.0.28-21 is the current version. If you an USB 3 external drive, you might find the build will perform better from that device. In my build I used a 250GB SSD drive for the build.

```
$ cd percona-server-8.0.28-19
$ mkdir arm64-build
$ cd arm64-build
$ cmake .. -DCMAKE_BUILD_TYPE=Release -DWITH_BOOST=/home/pi/boost_1_73_0 -DCMAKE_INSTALL_PREFIX=/usr/local/mysql
$ sudo make -j2
$ sudo make install
```
With the 4GB swap file you created above you can use make -j2 for the compile. Depending on which Pi you are using build time should be around 3 hours.

 ## Build XtraBackup
 At the time of writing 8.0.28-21 is the current version.
 ```
 $ cd percona-xtrabackup-8.0.28-21
 $ mkdir arm64-build
 $ cd arm64-build
 $ cmake .. -DCMAKE_BUILD_TYPE=Release -DWITH_BOOST=$HOME/boost_1_73_0 -DCMAKE_INSTALL_PREFIX=/usr/local/xtrabackup
 $ sudo make -j2
 $ sudo make install
 ```
The builds are now complete. Since we created everything from source they are a
few last things that need to be done.

We need to create the mysql user and set its home directory. We need to update the /usr/local/mysql to be owned by mysql.
```
$ sudo useradd mysql -d /usr/local/mysql
$ sudo chown -R mysql:mysql /usr/local/mysql
$ sudo mkdir -p /var/log/mysql
$ sudo chown -R mysql:mysql /var/log/mysql
```
One last thing we need before to start MySQL for the 1st time is an /etc/my.cnf.

Here is a sample you can work with.
```
$ sudo vi /etc/my.cnf
```
Copy and paste the contents below into your my.cnf.
```
[mysqld]
character-set-server = utf8mb4
port = 3306
socket = /usr/local/mysql/mysql.sock
pid-file = /usr/local/mysql/mysqld.pid
basedir = /usr/local/mysql
datadir = /data0/mysql/data
tmpdir  = /data0/mysql/tmp
general_log_file = /var/log/mysql/mysql-general.log
log-error = /var/log/mysql/mysqld.log
slow_query_log_file =/var/log/mysql/slow_query.log
slow_query_log = 0 # Slow query log off
expire_logs_days = 5
log_error_verbosity = 1
lower_case_table_names = 1
max_allowed_packet = 32M
max_connections = 50
max_user_connections = 40
skip-external-locking
skip-name-resolve
table_open_cache=500
thread_cache_size=16
thread_pool_size=16

innodb_data_home_dir = /data0/mysql/data
innodb_log_group_home_dir = /data0/mysql/data
innodb_buffer_pool_size = 2048M
innodb_log_files_in_group = 2
innodb_log_file_size = 128M
innodb_log_buffer_size = 16M
innodb_flush_log_at_trx_commit = 2
innodb_lock_wait_timeout = 50
innodb_flush_method = O_DIRECT
innodb_file_per_table = 1

```
You will want to set the following setting to match your needs.

1. datadir =
2. innodb_data_home_dir = **this should match your datadir**
3. innodb_log_group_home_dir = **this should match your datadir**

Now you will want to create a mysqld.server service file in /lib/systemd/system
```
$ sudo vi /lib/systemd/system/mysqld.service
```
Add the below contents to your mysqld.service.
```
[Unit]
Description=Percona Server 8.0
After=syslog.target
After=network.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf
TimeoutSec=300
WorkingDirectory=/usr/local/mysql
Restart=on-failure
#RestartPreventExitStatus=1
PrivateTmp=true
```
Let's setup Percona Server to stop and start with the OS.
```
$ sudo systemctl enable mysqld.Service
```
## Finish your build.
Once you have completed all the above steps. You can follow this blog post
[The lost art of Database Server Initialization.](https://percona.community/blog/2021/09/06/lost-art-of-database-server-initialization/). Start at step 4.

Thats it. You have a new Percona Server 8.0 running on your Raspberry Pi 4.

This process does take some patience, but if you like the Raspberry Pi and

Percona Server this is well worth the time it takes.

## Now for some screen shots.

- Percona Server: ![Percona Status](blog/2022/4/percona-systemctl-status.png)
- Command Line Interface: ![CLI Example](blog/2022/4/percona-server-running.png)
- XtraBackup complete: ![Complete Backup](blog/2022/4/percona-xtrabackup.png)
