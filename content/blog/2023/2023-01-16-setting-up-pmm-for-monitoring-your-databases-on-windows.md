---
title: 'Setting Up PMM For Monitoring Your Databases on Windows'
date: "2023-01-16T00:00:00+00:00"
draft: false
tags: ['PMM', 'MySQL', 'PostgreSQL', 'MongoDB', 'Monitoring']
authors:
  - mario_garcia
images:
  - blog/2023/01/pmm-login-screen.png
slug: setting-up-pmm-for-monitoring-your-databases-on-windows
---

Before deploying Percona Monitoring and Management (PMM) in production, you might want to test it or set up a development instance locally. Since many developers and DBAs have Windows desktops, I wanted to demonstrate how to set up PMM on Windows for an easy test environment. In this post, I’ll walk you through setting up PMM with Docker and WSL. 

If you’re a Linux user, check the blog post I wrote on [Setting up PMM for monitoring MySQL in a local environment](https://percona.community/blog/2022/08/05/setting-up-pmm-for-monitoring-mysql-on-a-local-environment/). There you can find instructions for installing Percona Monitoring and Management (PMM) on Linux and how to set it up for monitoring a MySQL instance. Otherwise, continue reading to get PMM up and running on Windows.

## Getting Started With PMM on Windows
If you’re a Windows user and want to try PMM, the recommended way for installing both the server and client would be to use the official Docker images and follow these guides:
* [Server](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/docker.html)
* [Client](https://docs.percona.com/percona-monitoring-and-management/setting-up/client/index.html#docker)

Before running the commands in those guides, you should install Docker Desktop and Windows Subsystem for Linux (WSL). These instructions should work for users who are on current versions of Windows 10 and Windows 11. For installing WSL, follow the [instructions](https://learn.microsoft.com/en-us/windows/wsl/install) on the Microsoft Learn website. Then, get the [Docker Desktop](https://docs.docker.com/get-docker/) installer. Now you’re ready to install and configure PMM.

## PMM Server
As stated in the [documentation](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/docker.html), you can store data from your PMM in:
* Docker volume (Preferred method)
* Data container
* Host directory

The preferred method is also recommended for Windows. Open PowerShell and execute the instructions in the [Run Docker with volume](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/docker.html#run-docker-with-volume) section. I’ve reproduced the steps here to save you time:

1. Get the Docker image:

```bash
$ docker pull percona/pmm-server:2
```

2. Create a volume:

```bash
$ docker volume create pmm-data
```

3. Run the image:

```
$ docker run --detach --restart always \
--publish 443:443 \
-v pmm-data:/srv \
--name pmm-server \
percona/pmm-server:2
```

4. Change the password for the default `admin` user:

```bash
$ docker exec -t pmm-server change-admin-password <new_password>
```

Once PMM Server is installed, open the browser and visit https://localhost. You will see the PMM login screen.

![PMM Login Screen](/blog/2023/01/pmm-login-screen.png "PMM Login Screen")

Now that the server is up and running, you need to get its IP address before connecting the client to the server. To get the IP address, you need the name or container ID. You can get it by running:

```bash
$ docker ps
```

The `docker ps` command will give you a list of the containers running on your system, as follows:

```
CONTAINER ID   IMAGE                                COMMAND                  CREATED        STATUS                    PORTS                          NAMES
fd988ad761aa   percona/pmm-server:2                 "/opt/entrypoint.sh"     2 months ago   Up 11 minutes (healthy)   80/tcp, 0.0.0.0:443->443/tcp   pmm-server
```

Take note of the container ID or name of the PMM Server container. Then, execute this command:

```
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' your_container
```

Replacing `your_container` with the container ID or name copied previously.

## PMM Client
Go to the [Set Up PMM Client](https://docs.percona.com/percona-monitoring-and-management/setting-up/client/index.html#docker) section in the documentation and follow the first two steps. All of these commands are executed from PowerShell.

In Step 3, you need to specify the IP address of the PMM Server by setting up the `PMM_SERVER` environment variable:

```bash
$ $env:PMM_SERVER=’X.X.X.X:443’
```

Replacing `X.X.X.X` with the server’s IP address. Then, initialize the container:

```
$ docker run \
--rm \
--name pmm-client \
-e PMM_AGENT_SERVER_ADDRESS=$env:PMM_SERVER \
-e PMM_AGENT_SERVER_USERNAME=admin \
-e PMM_AGENT_SERVER_PASSWORD=admin \
-e PMM_AGENT_SERVER_INSECURE_TLS=1 \
-e PMM_AGENT_SETUP=1 \
-e PMM_AGENT_CONFIG_FILE=config/pmm-agent.yaml \
--volumes-from pmm-client-data \
percona/pmm-client:2
```

`PMM_AGENT_SERVER_PASSWORD` default value is `admin`. Replace this value with the password assigned when the server was configured.

## Configure Your Database
Now that the client is connected to the server, you must configure PMM for monitoring your database. Follow the instructions below.

* MySQL
  * [Installation](#mysql-installation)
  * [Configuration](#mysql-configuration)
* PostgreSQL
  * [Installation](#postgresql-installation)
  * [Configuration](#postgresql-configuration)
* MongoDB
  * [Installation](#mongodb-installation)
  * [Configuration](#mongodb-configuration)

Once PMM is configured, the Home Dashboard will show the databases that are being monitored. For more information and advanced configuration, check the [documentation](https://docs.percona.com/percona-monitoring-and-management/index.html).

  ![PMM Home Dashboard](/blog/2023/01/pmm-home-dashboard.png "PMM Home Dashboard")

### MySQL Installation

If you already have a MySQL instance running, skip the installation process and continue with the [configuration](#mysql-configuration).

On Windows, you can install Percona Server for MySQL on Ubuntu running under WSL, but it’s better to use the official [Docker image](https://hub.docker.com/r/percona/percona-server/), as the MySQL server would be running on the same network as PMM.

For installing MySQL using Docker, follow the instructions in the [Percona Server for MySQL](https://docs.percona.com/percona-server/8.0/installation/docker.html) documentation.

You need to start the container with the latest version of Percona Server for MySQL 8.0:

```
$ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  percona/percona-server:8.0
```

Where `ps` is the name of the container, and the default password for the `root` user is `root`. You can change these values according to your needs.

### MySQL Configuration
Once Percona Server for MySQL is running, you need to get its IP address by running:

```bash
$ docker ps
```

```bash
CONTAINER ID   IMAGE                                COMMAND                  CREATED         STATUS                   PORTS                          NAMES
1fb4ddb35e48   percona/pmm-client:2                 "/usr/local/percona/…"   2 minutes ago   Up 2 minutes                                            pmm-client
```

Copy the container ID or name of the Percona Server for MySQL container. Then, execute this command:

```bash
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' your_container
```

Replacing `your_container` with the value you copied previously.

The IP address of the PMM Client container is also needed.

For configuring PMM for monitoring MySQL, we need to create a PMM user. First, log into MySQL:

```bash
$ docker run -it --rm percona mysql -h MYSQL_SERVER -uroot -p
```

Where `MYSQL_SERVER` is the IP address of the Percona Server for MySQL container

Then, execute the following SQL statements

```sql
CREATE USER 'pmm'@'localhost' IDENTIFIED BY 'pass' WITH MAX_USER_CONNECTIONS 10;
```

```sql
GRANT SELECT, PROCESS, SUPER, REPLICATION CLIENT, RELOAD, BACKUP_ADMIN ON *.* TO 'pmm'@'localhost';
```

Replacing `pass` with your desired password, and `localhost` with the IP address of the PMM Client container.

And finally, register the MySQL server for monitoring:

```bash
$ docker exec pmm-client pmm-admin add mysql --username=pmm --password=pass --host MYSQL_SERVER --query-source=perfschema
```

Where `MYSQL_SERVER` is the IP address of the Percona Server for MySQL container. Replace this value with the IP address and replace `pass` with the password of your `pmm` user.

### PostgreSQL Installation
If you already have a PostgreSQL instance running, skip the installation process and continue with the [configuration](#postgresql-configuration).

On Windows, you can install PostgreSQL using the Windows installer or install it on Ubuntu running under WSL, but it’s better to install it using the official image provided by the PostgreSQL project.

You need to start the container with the latest version of PostgreSQL:

```bash
$ docker run --name postgres -e POSTGRES_PASSWORD=password -d postgres
```

Where `password` is the password for the default `postgres` user. Replace this value according to your needs.

### PostgreSQL Configuration
Once PostgreSQL is running, you need to get its IP address by running:

```bash
$ docker ps
```

```bash
CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS                    PORTS                          NAMES
0460c671db12   postgres                             "docker-entrypoint.s…"   6 days ago       Up 48 seconds             5432/tcp                       postgres
```

Copy the container ID or name of the PostgreSQL container. Then, execute this command:

```bash
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' your_container
```

Replacing `your_container` with the value you copied previously.

The IP address of the PMM Client container is also needed.

For configuring PMM for monitoring PostgreSQL, we need to create a PMM user. First, log into PostgreSQL:

```bash
$ docker exec -it postgres psql --user postgres
```

Then, execute the following SQL statement:

```sql
CREATE USER pmm WITH SUPERUSER ENCRYPTED PASSWORD '<password>';
```

Replacing `<password>` with your desired password.

And finally, register the PostgreSQL server for monitoring:

```bash
$ docker exec pmm-client pmm-admin add postgresql --username=pmm --password=pass --host POSTGRESQL_SERVER --query-source=perfschema
```

Where `POSTGRESQL_SERVER` is the IP address of the PostgreSQL container. Replace this value with the IP address and replace `pass` with the password of your `pmm` user.

### MongoDB Installation
If you already have a MongoDB instance running, skip the installation process and continue with the [configuration](#mongodb-configuration).

On Windows, you can install Percona Server for MongoDB on Ubuntu running under WSL, but it’s better to use the official [Docker image](https://hub.docker.com/r/percona/percona-server/), as the MongoDB server would be running on the same network as PMM.

For installing MongoDB using Docker, follow the instructions in the [Percona Server for MongoDB](https://docs.percona.com/percona-server-for-mongodb/6.0/install/docker.html) documentation.

You need to start the container with the latest version of Percona Server for MongoDB 6.0:

```bash
$ docker run --name psmdb -d percona/percona-server-mongodb:6.0
```

### MongoDB Configuration
Once Percona Server for MongoDB is running, you need to get its IP address by running.

```bash
$ docker ps
```

```bash
CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS                    PORTS                          NAMES
2c3d291535b3   percona/percona-server-mongodb:6.0   "/entrypoint.sh mong…"   6 days ago       Up 27 minutes             27017/tcp                      psmdb
```

Copy the container ID or name of the Percona Server for MongoDB container. Then, execute this command:

```bash
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' your_container
```

Replacing `your_container` with the value you copied previously.

The IP address of the PMM Client container is also needed.

For configuring PMM for monitoring MongoDB, we need to create a PMM user. First, connect to the `admin` database in MongoDB using the MongoDB Shell (mongosh):

```bash
$ docker run -it --link psmdb --rm percona/percona-server-mongodb:6.0 mongosh mongodb://MONGODB_SERVER:27017/admin
```

Where `MONGODB_SERVER` is the IP address of your MongoDB server.

Then, create the user for PMM, executing the following instructions:

```
db.createRole({
   "role":"explainRole",
   "privileges":[
      {
         "resource":{
            "db":"",
            "collection":""
         },
         "actions":[
            "collStats",
            "dbHash",
            "dbStats",
            "find",
            "listIndexes",
            "listCollections"
         ]
      }
   ],
   "roles":[]
})
```

```
db.getSiblingDB("admin").createUser({
   "user":"pmm",
   "pwd":"<password>",
   "roles":[
      {
         "role":"explainRole",
         "db":"admin"
      },
      {
         "role":"clusterMonitor",
         "db":"admin"
      },
      {
         "role":"read",
         "db":"local"
      }
   ]
})
```

Replacing `<password>` with the password you want to assign to the `pmm` user.

And finally, register the MongoDB server for monitoring:

```bash
$ docker exec pmm-client pmm-admin add mongodb --username=pmm --password=pass --host MONGODB_SERVER
```

Where `MONGODB_SERVER` is the IP address of the MongoDB container. Replace this value with the IP address and replace `pass` with the password of your `pmm` user.