---
title: "Running PMM with Docker on Ubuntu 20.04"
date: "2022-08-05T00:00:00+00:00"
draft: false
tags: ["PMM", "DevOps", "MySQL", "Docker"]
authors:
  - edith_puclla
images:
  - blog/2022/8/pmm-ubuntu-overview.png
slug: installing-pmm-with-docker-on-ubuntu-20
---

I started at Percona a few weeks ago and was looking for a quick way to learn about PMM (Percona Monitoring and Management), which is one of my favorite technologies within Percona to monitor the health of our database infrastructure, explore new patterns in the database behavior, manage and improve the performance of our databases, all with customizable dashboards and real-time alerts using [Grafana](https://grafana.com/) and [VictoriaMetrics](https://victoriametrics.com/).

The best of all is that PMM is Open Source, you can check the [PMM repository](https://github.com/percona/pmm) in case you want to contribute.

There are many flavors for PMM installation, here I will describe the steps to install PMM on Ubuntu 20.04, using Docker for PMM Server on an Amazon EC2 instance.

This image summarizes our goal.

![Overview](blog/2022/8/pmm-ubuntu-overview.png)

## Requirements

- An Amazon EC2 instance with Ubuntu 20.04
  - This instance is configured with a Security Group with TCP port 443 open.
- Docker
  - You can install Docker by following this [guide](https://docs.docker.com/engine/install/ubuntu/).
  - Manage Docker as a non-root user: **_sudo usermod -aG docker $USER_**
- MySQL
  - I am using Percona Server for MySQL from [Percona apt repository](https://docs.percona.com/percona-server/8.0/installation/apt_repo.html)

## Installing PMM Server with Docker

1. Download PMM server Docker image

```bash
docker pull percona/pmm-server:2
```

2. Create the data volume container

```bash
docker create --volume /srv --name pmm-data percona/pmm-server:2 /bin/true
```

3. Run PMM server container

```bash
docker run --detach --restart always --publish 443:443 --volumes-from pmm-data --name pmm-server percona/pmm-server:2
```

4. Verify the creation of the container.

```bash
docker ps
```

![docker ps](blog/2022/8/pmm-ubuntu-docker-ps.png)

Start a web browser and in the address bar enter the IP address of the **PMM server** host: https://<PUBLIC_IP>:443/. For example, https://172.31.53.46. If you are running on your local machine use https://localhost:443/.
Woohoo! We have a PMM Server running and we can see our dashboard!

![pmm-ubuntu-pmm-dashboard](blog/2022/8/pmm-ubuntu-pmm-dashboard.png)

**Note:** Some browsers may not trust the self-signed SSL certificate when you first open the URL. If this is the case, Chrome users may want to type **thisisunsafe** to bypass the warning.

The user and password are **“admin”** and **“admin”**, It will ask you to change the password after login in for the first time, for this demo I will use **admin2020** as a password. We will use these credentials to register the node in PMM Server later.

Until now we have only PMM Server. To monitor a database, we need a PMM client.

## Installing PMM client

**PMM Client** is a collection of agents and exporters that run on the host being monitored. Let´s install it using the repository package.

1. Download Percona Repo Package

```bash
wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
```

2. Install Percona Repo Package

```bash
sudo apt install ./percona-release_latest.$(lsb_release -sc)_all.deb
```

3. Update apt cache

```bash
sudo apt update
```

4. Install Percona Monitoring and Management Client

```bash
sudo apt install pmm2-client
```

5. Checking the installation. We will use pmm-admin in the next steps.

```bash
sudo pmm-admin -v
```

![pmm-ubuntu-pmm-dashboard](blog/2022/8/pmm-ubuntu-pmm-admin-v.png)

## Creating a user for monitoring

Let’s create a user in MySQL.

1. Login in MySQL for use the command-line: **_mysql -uroot -p_**

2. Create a “pmm” user with “welcOme1!” As a password

```bash
CREATE USER 'pmm'@'localhost' IDENTIFIED BY 'welcOme1!' WITH MAX_USER_CONNECTIONS 10;
```

3. Give “pmm” user with specific permission to monitor the database

```bash
GRANT SELECT, PROCESS, REPLICATION CLIENT, RELOAD, BACKUP_ADMIN ON *.* TO 'pmm'@'localhost';
```

Checking if the user was created correctly with the respective permissions, use

```bash
 show grants for 'pmm'@'localhost';
```

![pmm-ubuntu-show-grants](blog/2022/8/pmm-ubuntu-show-grants.png)

## Connect Client to Server

1. Register Percona Monitoring and Management client with server, use the default admin/admin username and password.

```bash
sudo pmm-admin config --server-insecure-tls --server-url=https://admin:admin2020@172.17.0.1:443
```

**Note:** I am using **172.17.0.1** because this is the private IP where the PMM Server is running. You can get this IP by entering the docker container and typing **“hostname -I”**

![pmm-ubuntu-hostname-i](blog/2022/8/pmm-ubuntu-hostname-i.png)

After registering your client with the server you will see this information:

![pmm-ubuntu-pmm-admin-config](blog/2022/8/pmm-ubuntu-pmm-admin-config.png)

2. Check if the node was registered

```bash
pmm-admin  inventory list nodes
```

A new node should appear in the list which is **pmm-server**

![pmm-ubuntu-hostname-i](blog/2022/8/pmm-ubuntu-pmm-admin-inventory.png)

## Adding a MySQL Database to monitoring

1. Use pmm-admin to register the database with the user we created in MySQL

```bash
sudo pmm-admin add mysql --username=pmm --password=welcOme1! --query-source=perfschema
```

![pmm-ubuntu-pmm-admin-add-sql](blog/2022/8/pmm-ubuntu-pmm-admin-add-sql.png)

2. In the dashboard, we will see that our node and database are registered and ready to be monitored by PMM.

![pmm-ubuntu-last-dashboard](blog/2022/8/pmm-ubuntu-last-dashboard.png)

That's it! :) We learned how to monitor our databases for free with Percona Monitoring Database (PMM). Additionally, you can go to the next level by registering a PMM instance with [Percona Platform](https://docs.percona.com/percona-platform/) and receive more information.

I hope you've enjoyed this tutorial, and if you need help following it, feel free to contact the [Percona team support](https://percona.community/blog/2022/02/10/how-to-publish-blog-post/#assistance-and-support). We will be happy to help.
