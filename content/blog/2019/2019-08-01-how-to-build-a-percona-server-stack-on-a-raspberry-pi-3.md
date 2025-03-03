---
title: 'How to Build a Percona Server "Stack" on a Raspberry Pi 3+'
date: Thu, 01 Aug 2019 12:50:36 +0000
draft: false
tags: ['MySQL', 'Percona Server for MySQL', 'Raspberry Pi', 'Toolkit']
categories: ['MySQL', 'Toolkit']
authors:
  - wayne
images:
  - blog/2019/07/Percona-installation-on-Raspberry-Pi-3.jpg
slug: how-to-build-a-percona-server-stack-on-a-raspberry-pi-3
---

The blog post [_How to Compile Percona Server for MySQL 5.7 in Raspberry Pi 3_](https://www.percona.com/blog/2018/08/22/how-to-compile-percona-server-for-mysql-5-7-in-raspberry-pi-3/) by Walter Garcia, inspired me to create an updated install of Percona Server for the [Raspberry Pi 3+](https://www.raspberrypi.org/products/). 

![Percona installation on Raspberry Pi 3+](blog/2019/07/Percona-installation-on-Raspberry-Pi-3.jpg)

This how-to post covers installing from source and being able to use [Percona Server for MySQL](https://www.percona.com/software/mysql-database) in any of your maker projects. I have included everything you need to have a complete Percona Server, ready to store data collection for your weather station, your GPS data, or any other project you can think of that would require data collection in a database. 

My years of hands-on support of Percona Server enable me to customize the install a bit. I wanted to build a full Percona "Stack" including XtraBackup, and Percona Toolkit.

Hardware and Software
---------------------

*   Tested on a Raspberry PI 3B and 3B+
*   OS is Raspbian Buster. You can download it here: [https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/)
*   I choose the option: Raspbian Buster with Desktop.
*   64GB SD Card, not required, but would not suggest less than 32GB. For best performance use and SD card that is between 90 - 100MB per sec.

The Step-by-Step Guide
----------------------

Let's get on and build!

### 1. Prep Your Raspberry PI

You will notice I use sudo rather often, even during the make and cmake. I found that running as the default pi user for the install gave me issues. Using sudo for root based commands is the best practice that I always try to follow.
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install screen cmake debhelper autotools-dev libaio-dev 
automake libtool bison bzr libgcrypt20-dev flex autoconf libtool libncurses5-dev 
mariadb-client-10.0 libboost-dev libreadline-dev libcurl4-openssl-dev libtirpc-dev
```
Create a swapfile. Very much needed for these two compiles.
```
sudo dd if=/dev/zero of=/swapfile2GB bs=1M count=2048
sudo mkswap /swapfile2GB
sudo swapon /swapfile2GB
sudo chmod 0600 /swapfile2GB
```

### 2. Build Percona Server for MySQL

This will take about 3.5 to 4 hours to run. Download percona-server 5.7.26 source tar ball
```
wget https://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.26-29/source/tarball/percona-server-5.7.26-29.tar.gz
```
Extract to /home/pi
```
cd percona-server-5.7.26-29
sudo cmake -DDOWNLOAD_BOOST=ON -DWITH_BOOST=$HOME/boost .
sudo make -j3
sudo make install
```

### 3. Build Percona XtraBackup

This will take about 3 hours.
```
sudo apt-get install libcurl4-gnutls-dev libev-dev libev4
```
Note: installing the package libcurl4-gnutls-dev  will remove the package libcurl4-openssl-dev . I had compile failures for XtraBackup when libcurl4-openssl-dev  was installed. Download XtraBackup 2.4.14
```
wget https://www.percona.com/downloads/Percona-XtraBackup-2.4/Percona-XtraBackup-2.4.14/source/tarball/percona-xtrabackup-2.4.14.tar.gz
```
Extract to /home/pi
```
cd percona-xtrabackup-2.4.14

sudo cmake -DWITH_BOOST=$HOME/boost -DBUILD_CONFIG=xtrabackup_release -DWITH_MAN_PAGES=OFF
sudo make -j3
sudo make install
```

### 4. Build Percona Toolkit

Done in a few minutes.
```
wget https://www.percona.com/downloads/percona-toolkit/3.0.13/source/tarball/percona-toolkit-3.0.13.tar.gz
```
extract to /home/pi
```
cd percona-toolkit-3.0.13

perl Makefile.PL
make
make test
sudo make install
```

### 5. Create the mysqsl user

```
sudo useradd mysql -d /var/lib/mysql
```
Create directories for mysql to use.
```
sudo mkdir -p /var/lib/mysql/data
sudo mkdir /var/lib/mysql/binlog
sudo mkdir /var/lib/mysql/tmp
sudo mkdir /var/log/mysql
```
Change ownership of directories to mysql user.
```
sudo chown -R mysql:mysql /var/lib/mysql
sudo chown mysql:mysql /var/log/mysql
sudo chown -R mysql:mysql /usr/local/mysql
```

### 6. Prep my.cnf

```
sudo rm -fR /etc/mysql
```
I like to remove any leftover mysql directories or files in /etc before I create my file in the next step.
```
sudo vi /etc/my.cnf
```
Add these lines, below, to your new my.cnf file.
```
[mysqld]
port = 3306
socket = /var/lib/mysql/mysql.sock
pid-file = /var/lib/mysql/mysqld.pid
basedir = /usr/local/mysql
datadir = /var/lib/mysql/data
general_log_file = /var/log/mysql/mysql-general.log
log-error = /var/log/mysql/mysqld.log
slow_query_log_file = /var/log/mysql/log/slow_query.log
slow_query_log = 0 # Slow query log off
lc-messages-dir = /usr/local/mysql/share
plugin_dir = /usr/local/mysql/lib/mysql/plugin
skip-external-locking
log-bin = /var/lib/mysql/binlog/mysql-bin
sync_binlog = 1
expire_logs_days = 5
server-id = 1
binlog_format = mixed
innodb_data_home_dir = /var/lib/mysql/data
innodb_log_group_home_dir = /var/lib/mysql/data
innodb_log_files_in_group = 2
innodb_buffer_pool_size = 128M
innodb_log_file_size = 16M
innodb_log_buffer_size = 8M
innodb_flush_log_at_trx_commit = 1
innodb_lock_wait_timeout = 50
innodb_flush_method = O_DIRECT
innodb_file_per_table = 1
innodb_buffer_pool_instances = 1
```
Save the my.cnf file.
```
sudo chown mysql:mysql /etc/my.cnf
```

### 7. Initialize the database files

At this point, you can initialize the database files
```
sudo /usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/var/lib/mysql/data
```

### 8. Start Percona Server

This is the exciting part coming up. We are going to start Percona Server
```
sudo /usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf --user=mysql &
```
If everything went well you should see the following lines in your /var/log/mysql/mysqld.log .```
2019-06-24T19:56:52.071765Z 0 [Note] Server hostname (bind-address): '*'; port: 3306
2019-06-24T19:56:52.072251Z 0 [Note] IPv6 is available.
2019-06-24T19:56:52.072385Z 0 [Note]   - '::' resolves to '::';
2019-06-24T19:56:52.072770Z 0 [Note] Server socket created on IP: '::'.
2019-06-24T19:56:52.132587Z 0 [Note] InnoDB: Buffer pool(s) load completed at 190624 15:56:52
2019-06-24T19:56:52.136886Z 0 [Note] Failed to start slave threads for channel ''
2019-06-24T19:56:52.178087Z 0 [Note] Event Scheduler: Loaded 0 events
2019-06-24T19:56:52.179153Z 0 [Note] /usr/local/mysql/bin/mysqld: ready for connections.
Version: '5.7.26-29-log'  socket: '/var/lib/mysql/mysql.sock'  port: 3306 Source distribution
```

### 9. Test login to Percona Server

```
mysql -u root --socket=/var/lib/mysql/mysql.sock
```
If you plan on keeping this as an active Percona Server I **strongly advise** you to remove the root user and create your own privileged user. 

First, stop Percona Server
```
/usr/local/mysql/bin/mysqladmin -u root --socket=/var/lib/mysql/mysql.sock shutdown
```
Create the mysqld.server and enable it.
```
sudo vi /etc/systemd/system/mysqld.service
[Unit]
Description=Percona Server Version 5.7.x
After=syslog.target
After=network.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf
TimeoutSec=300
WorkingDirectory=/usr/local/mysql/bin
#Restart=on-failure
#RestartPreventExitStatus=1
PrivateTmp=true
sudo systemctl enable mysqld.service
```
Now if everything was done correctly you should be able to reboot your Pi and Percona Server will auto start on OS Boot. 

This is it, you now have an entire Percona Server for MySQL up and running, with XtraBackup for your daily backups and Percona Toolkit to assist you with daily and complicated tasks. If you try this out, I'd love to hear about the uses you make of your Percona Server on a Raspberry Pi. 

_—_ 

_Image based on Photo by [Hector Bermudez](https://unsplash.com/@hectorbermudez?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/raspberry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_ 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up._