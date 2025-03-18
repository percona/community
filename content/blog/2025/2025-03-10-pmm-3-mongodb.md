---
title: "Setting Up and Monitoring MongoDB 8 Replica Sets with PMM 3 Using Docker: A Beginner-Friendly Guide"
date: "2025-03-18T00:00:00+00:00"
tags: ['MongoDB', 'Docker', 'Opensource', 'PMM']
categories: ["PMM", 'MongoDB']
authors:
  - daniil_bazhenov
images:
  - blog/2025/03/pmm-mongodb-cover.jpg
---

This guide explains how to set up a MongoDB 8 Replica Set and monitor it using PMM 3, all within Docker. We'll guide you through the steps to create a local environment, configure the necessary components, and connect them for effective monitoring and management.

> The guide is written in detail for beginners. In [the conclusion](#conclusion) section there are ready configurations for the experienced. 

The recent [release](https://docs.percona.com/percona-monitoring-and-management/3/release-notes/3.0.0.html) of [Percona Monitoring and Management 3](https://docs.percona.com/percona-monitoring-and-management/3/index.html) introduces several new features:

* Upgraded Grafana version for an improved user experience.

* Rootless containers for enhanced security.

* ARM support for the pmm-client.

* Monitoring capabilities for MongoDB 8, along with [new dashboards](https://docs.percona.com/percona-monitoring-and-management/3/reference/dashboards/dashboard-mongodb-router-summary.html).

This article is intended for developers and DBAs who want to experiment with these tools locally using Docker. We will cover the following steps to set everything up and test the functionality:

* Launch the PMM 3 pmm-server for monitoring and open it in a browser.

* Install MongoDB, starting with a standalone server, and then convert it into a Replica Set with three nodes. [Percona Server for MongoDB](https://www.percona.com/mongodb/software/percona-server-for-mongodb) images are used in this article.

* Configure the pmm-client for MongoDB to send metrics to the pmm-server.

* Explore the PMM 3 [dashboards](https://docs.percona.com/percona-monitoring-and-management/3/reference/dashboards/dashboard-mongodb-router-summary.html).

![Percona Monitoring and Management (PMM) 3.0.0 - Dashboard - MongoDB Replica Set Overview](blog/2025/03/pmm-mongodb-rs.png)

We will use Docker Compose to define and run multiple containers efficiently through a single `docker-compose.yaml` file.

If you're ready to dive into the world of Dockerized database monitoring and management, let’s get started!


## Step Zero: Preparation

To get started, you need a terminal to run Docker commands and a text editor to modify the docker-compose.yaml file.

You also need Docker installed on your system. If Docker is not installed, follow these instructions to set it up:

1. Docker Desktop: This application includes both Docker and Docker Compose. It is available for multiple operating systems. This guide uses Docker Desktop on macOS with an Apple Silicon ARM processor. [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. Docker and Docker Compose (separately): If preferred, install Docker and Docker Compose individually. Use the following links for guidance:

    * [Download Docker for your OS](https://www.docker.com/get-started/)

    * [Download Docker Compose](https://docs.docker.com/compose/install/)


### Command to Verify Installation:

Verify Docker Compose Installation: If you're using Docker Desktop, Docker Compose is included. If you installed Docker Compose separately, you can verify the installation with:

```sh
docker-compose --version
```

This should return the version of Docker Compose installed.

```sh
➜  community git:(main) ✗ docker-compose --version
Docker Compose version v2.21.0-desktop.1
```

Once Docker and Docker Compose are installed and verified, you are ready to move on to the next steps of deploying PMM 3 and MongoDB in Docker.

### Project Directory

Create a directory where we’ll store the configuration and necessary files. For example, I created a directory named pmm-mongodb-setup and navigated into it.

```bash
mkdir pmm-mongodb-setup
cd pmm-mongodb-setup
```

## Step One: Starting PMM 3 Using Docker Compose

To start with, we will launch PMM 3, specifically the pmm-server, which we will later access via a browser.

### Create the Docker Compose Configuration File

First, create a file named `docker-compose.yaml` in your project directory. Then, copy and paste the following configuration into the file to set up PMM 3:

```yaml
version: '3'

services:
  pmm-server:
    image: percona/pmm-server:3
    platform: "linux/amd64" # Specifies that Docker should use the image for the amd64 architecture, which is necessary if the container doesn't support ARM and your host system is ARM (e.g., Mac with Apple Silicon).
    container_name: pmm-server
    ports:
      - 8080:80
      - 443:8443
    healthcheck: # Defines a command to check the container's health and sets the timing for executions and retries.
      test: ["CMD-SHELL", "curl -k -f -L https://pmm-server:8443 > /dev/null 2>&1 || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
```
> Explanation:
>
> We define the first `pmm-server` service to use the `percona/pmm-server:3` image
> 
> - `platform`: This parameter ensures compatibility with ARM-based processors, such as my Mac with Apple Silicon, by instructing Docker to use the image for the amd64 architecture.
>
> - `healthcheck`: This parameter performs a check to confirm that the container has started successfully.


### Start the PMM 3 Container

Save the `docker-compose.yaml` file, and then use the following command to start the PMM 3 container:

```shell
docker-compose up -d
```

This command will download the PMM 3 image if it is not already available locally and start the container in detached mode.

Expected result in the terminal:

```shell
➜  pmm-mongodb-setup docker-compose up -d
[+] Running 2/2
 ✔ Network pmm-mongodb-setup_default  Created   0.1s
 ✔ Container pmm-server               Started   0.9s
➜  pmm-mongodb-setup
```

Expected result in Docker Desktop:
![Percona Monitoring and Management (PMM) 3.0.0 - Docker Desktop Start](blog/2025/03/docker-pmm-start.png)

### Open PMM in a browser

Now you can open PMM in your browser at http://localhost. Use admin/admin as the username and password to log in. When prompted to change the password, skip this step by clicking the Skip button. Since this is a test setup, we need a simple password for other containers.


![Percona Monitoring and Management (PMM) 3.0.0 - Login](blog/2025/03/pmm-login.png)

![Percona Monitoring and Management (PMM) 3.0.0 - Home Page](blog/2025/03/pmm-home.png)

Now, PMM 3 is successfully running using Docker Compose.


Step Two: Starting MongoDB 

We start by launching a standalone MongoDB service. This simple configuration allows us to quickly understand how it operates before moving on to a more advanced setup with a Replica Set.

To keep the database data persistent, even after a restart, a `volume` is used for MongoDB data storage. Add the following configuration to the `docker-compose.yaml` file under the `pmm-server` service:

```yaml
  mongodb:
    image: "percona/percona-server-mongodb:8.0-multi"
    volumes:
      - mongodb-data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: databaseAdmin
      MONGO_INITDB_ROOT_PASSWORD: password
    ports:
      - "27017:27017"
    command: ["mongod", "--port", "27017", "--bind_ip_all", "--profile", "2", "--slowms", "200", "--rateLimit", "100"]
    healthcheck:
      test: ["CMD-SHELL", "mongosh --eval 'db.adminCommand(\"ping\")' --quiet"]
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  mongodb-data: # MongoDB data storage volume
```

> Explanation: 
> - `environment`: Configures the root user's credentials (username and password). 
> - `command`: Sets additional parameters for MongoDB: 
>   * `bind_ip_all`: Allows external access to the database, for instance, through MongoDB Compass. 
>   * `profile`: Enables profiling settings to support Query Analytics (QAN) in PMM. 
> - `healthcheck`: Ensures the container starts successfully by executing a health check command. 
> - `volumes:`: Creates the specified volume for MongoDB data storage. Defines a Docker volume to store MongoDB data persistently. 

### Launching the Configuration

Save the updated `docker-compose.yaml` file and launch the MongoDB service by running the following command:

```sh
docker-compose up -d
```

Docker Compose checks the configuration and starts the MongoDB container.

```sh
➜  pmm-mongodb-setup docker-compose up -d
[+] Running 3/3
 ✔ Volume "pmm-mongodb-setup_mongodb-data"  Created   0.0s
 ✔ Container pmm-mongodb-setup-mongodb-1    Started   0.1s
 ✔ Container pmm-server                     Running   0.0s
➜  pmm-mongodb-setup
```

Verifying MongoDB in Docker Desktop:

![Percona Monitoring and Management (PMM) 3.0.0 - Docker Desktop MongoDB](blog/2025/03/docker-pmm-mongodb.png)


## Step Three: PMM Client

At this point, we have both the PMM Server, which is accessible in the browser, and MongoDB running. To transfer metrics from MongoDB to the PMM Server, a container with `pmm-client` needs to be started.

Add another service `pmm-client` to the `docker-compose.yaml` file, right after `mongodb`. Note that `volumes:`` must remain at the bottom of the file.

```yaml
  pmm-client:
    image: percona/pmm-client:3
    container_name: pmm-client
    depends_on:
      pmm-server:
        condition: service_healthy
      mongodb:
        condition: service_healthy
    environment:
      PMM_AGENT_SERVER_ADDRESS: pmm-server:8443
      PMM_AGENT_SERVER_USERNAME: admin
      PMM_AGENT_SERVER_PASSWORD: admin
      PMM_AGENT_SERVER_INSECURE_TLS: 1
      PMM_AGENT_CONFIG_FILE: config/pmm-agent.yaml
      PMM_AGENT_SETUP: 1
      PMM_AGENT_SETUP_FORCE: 1
      PMM_AGENT_PRERUN_SCRIPT: >
        pmm-admin status --wait=10s &&
        pmm-admin add mongodb --username=databaseAdmin --password=password --host=mongodb --port=27017 --query-source=profiler
```

> Explanation: 
> - `depends_on`: Ensures that pmm-client starts only after pmm-server and mongodb have started successfully and passed the healthcheck. 
> - `PMM_AGENT_PRERUN_SCRIPT`: The pmm-admin add mongodb command adds the MongoDB service to PMM for monitoring. 
> - `PMM_AGENT_SERVER_ADDRESS`: Specifies the PMM Server address and uses port 8443. 
> - `PMM_AGENT_SERVER_USERNAME` and `PMM_AGENT_SERVER_PASSWORD`: Update these values if you have changed the PMM login credentials.

### Applying the Updated Configuration

Run the following command to apply the updated docker-compose.yaml configuration and start the pmm-client service:

```sh
docker-compose up -d
```

After running the command, you should see the pmm-client container start successfully:

```sh
➜  pmm-mongodb-setup docker-compose up -d
[+] Running 3/3
 ✔ Container pmm-mongodb-setup-mongodb-1  Healthy    0.0s
 ✔ Container pmm-server                   Healthy    0.0s
 ✔ Container pmm-client                   Started    0.1s
➜  pmm-mongodb-setup
```

Open PMM in your browser. On the homepage, you should now see MongoDB listed as a monitored service:

![Percona Monitoring and Management (PMM) 3.0.0 - PMM MongoDB](blog/2025/03/pmm-home-mongodb.png)


## Step Four: Convert a Standalone MongoDB to a Replica Set

A single MongoDB instance works well for development and testing. At this point, you can already connect to the database from your application or tools such as MongoDB Compass and run various NoSQL queries.

However, the goal is to deploy a Replica Set consisting of three replicas, which is recommended for production and operational setups. For now, we set up the Replica Set on a single machine with a single docker-compose, which is intended for testing and development purposes only.

Both the mongodb and pmm-client services need to be updated.

### Stopping All Services

First, stop all the currently running services:

```sh
docker-compose down 
```

Result:

```sh
➜  pmm-mongodb-setup docker-compose down
[+] Running 4/4
 ✔ Container pmm-client                   Removed    0.3s
 ✔ Container pmm-mongodb-setup-mongodb-1  Removed    0.4s
 ✔ Container pmm-server                   Removed    4.5s
 ✔ Network pmm-mongodb-setup_default      Removed
```

### Generating a Key File

To run three MongoDB replicas that can securely communicate with each other, a key file is required.

Create a `secrets` folder next to the `docker-compose.yaml` file and generate the `mongodb-keyfile`:

```sh
mkdir secrets
openssl rand -base64 128 > secrets/mongodb-keyfile
chmod 600 secrets/mongodb-keyfile
```

In this case, the mongodb-keyfile will be generated inside the secrets folder. If your operating system does not support these commands, manually create the secrets folder and add a mongodb-keyfile with the following content:

```
rVLhIK2PhZKGxysjwMR4t1OmNppqdAzEs408hrbzg95D146mn9YENixId6pvIGCA
Cy9hc1k6OKKabbv7Rm347NwSFxbdPPx0/jnaO80U/a6/mv0XqSmEl8wdR91b4jIm
d98LobplwRs4b7g9cnLMUAIULr0WG+J36NtKIA6q4eE=
```

### Add three mongodb services for Replica Set

Remove the existing mongodb service from the docker-compose.yaml file and replace it with three Replica Set services:

```yaml
  mongodb-rs101:
    image: percona/percona-server-mongodb:8.0-multi
    container_name: mongodb-rs101
    ports:
      - "27017:27017"  
    command: ["mongod", "--port", "27017", "--replSet", "rs", "--keyFile", "/etc/secrets/mongodb-keyfile", "--bind_ip_all", "--profile", "2", "--slowms", "200", "--rateLimit", "100"]
    environment:
      MONGO_INITDB_ROOT_USERNAME: databaseAdmin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb-data-101:/data/db
      - ./secrets:/etc/secrets:ro
    healthcheck:
      test: ["CMD-SHELL", "mongosh --host localhost --port 27017 --username databaseAdmin --password password --authenticationDatabase admin --eval 'rs.status().ok || 1'"]
      interval: 30s
      timeout: 10s
      retries: 5

  mongodb-rs102:
    image: percona/percona-server-mongodb:8.0-multi
    container_name: mongodb-rs102
    ports:
      - "28017:28017"  
    command: ["mongod", "--port", "28017", "--replSet", "rs", "--keyFile", "/etc/secrets/mongodb-keyfile", "--bind_ip_all", "--profile", "2", "--slowms", "200", "--rateLimit", "100"]
    environment:
      MONGO_INITDB_ROOT_USERNAME: databaseAdmin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb-data-102:/data/db
      - ./secrets:/etc/secrets:ro
    healthcheck:
      test: ["CMD-SHELL", "mongosh --host localhost --port 28017 --username databaseAdmin --password password --authenticationDatabase admin --eval 'rs.status().ok || 1'"]
      interval: 30s
      timeout: 10s
      retries: 5

  mongodb-rs103:
    image: percona/percona-server-mongodb:8.0-multi
    container_name: mongodb-rs103
    ports:
      - "29017:29017"  
    command: ["mongod", "--port", "29017", "--replSet", "rs", "--keyFile", "/etc/secrets/mongodb-keyfile", "--bind_ip_all", "--profile", "2", "--slowms", "200", "--rateLimit", "100"]
    environment:
      MONGO_INITDB_ROOT_USERNAME: databaseAdmin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb-data-103:/data/db
      - ./secrets:/etc/secrets:ro
    healthcheck:
      test: ["CMD-SHELL", "mongosh --host localhost --port 29017 --username databaseAdmin --password password --authenticationDatabase admin --eval 'rs.status().ok || 1'"]
      interval: 30s
      timeout: 10s
      retries: 5
```

> Key Points:
> 
> - `./secrets:/etc/secrets:ro:` Mounts the key file from your disk into the container.
> 
> - `ports:`: Each replica runs on a separate port since they are hosted on the same machine.
> 
> - `command:`: 
> 
>   * `--keyFile`: Enables replication and uses the key file for secure communication between replicas. 
> 
>   * `--replSet`: Defines a Replica set parameter named rs. 
> 
> - `healthcheck:`: Ensures that pmm-client starts only after the Replica Set is initialized.


### Adding Volumes

Define three separate volumes for data storage:

```yaml
volumes:
  mongodb-data-101:
  mongodb-data-102:
  mongodb-data-103:
```

### Initializing the Replica Set

Add another service to initialize the Replica Set (after `mongodb-rs103`):

```yaml
  mongodb-rs-init:
    image: percona/percona-server-mongodb:8.0-multi
    container_name: rs-init
    depends_on:
      - mongodb-rs101
      - mongodb-rs102
      - mongodb-rs103
    entrypoint: [
      "sh", "-c",
      "until mongosh --host mongodb-rs101 --port 27017 --username databaseAdmin --password password --authenticationDatabase admin --eval 'print(\"waited for connection\")'; do sleep 5; done && \
      mongosh --host mongodb-rs101 --port 27017 --username databaseAdmin --password password --authenticationDatabase admin --eval 'config={\"_id\":\"rs\",\"members\":[{\"_id\":0,\"host\":\"mongodb-rs101:27017\"},{\"_id\":1,\"host\":\"mongodb-rs102:28017\"},{\"_id\":2,\"host\":\"mongodb-rs103:29017\"}],\"settings\":{\"keyFile\":\"/etc/secrets/mongodb-keyfile\"}};rs.initiate(config);'"
    ]
    volumes:
      - ./secrets:/etc/secrets:ro
```

This service connects to one of the replicas and initializes the Replica Set configuration.

### Updating pmm-client

Finally, modify the pmm-client service to register all three Replica Set nodes:

```yaml
  pmm-client:
    image: percona/pmm-client:3
    container_name: pmm-client
    depends_on:
      pmm-server:
        condition: service_healthy
      mongodb-rs101:
        condition: service_healthy
      mongodb-rs102:
        condition: service_healthy
      mongodb-rs103:
        condition: service_healthy
    environment:
      PMM_AGENT_SERVER_ADDRESS: pmm-server:8443
      PMM_AGENT_SERVER_USERNAME: admin
      PMM_AGENT_SERVER_PASSWORD: admin
      PMM_AGENT_SERVER_INSECURE_TLS: 1
      PMM_AGENT_CONFIG_FILE: config/pmm-agent.yaml
      PMM_AGENT_SETUP: 1
      PMM_AGENT_SETUP_FORCE: 1
      PMM_AGENT_PRERUN_SCRIPT: >
        pmm-admin status --wait=10s &&
        pmm-admin add mongodb --service-name=mongodb-rs101 --username=databaseAdmin --password=password --host=mongodb-rs101 --port=27017 --query-source=profiler &&
        pmm-admin add mongodb --service-name=mongodb-rs102 --username=databaseAdmin --password=password --host=mongodb-rs102 --port=28017 --query-source=profiler &&
        pmm-admin add mongodb --service-name=mongodb-rs103 --username=databaseAdmin --password=password --host=mongodb-rs103 --port=29017 --query-source=profiler
```

> Explanation:
>
> `depends_on`: Ensures pmm-client waits until all replicas and pmm-server are initialized.
> 
> `PMM_AGENT_PRERUN_SCRIPT`: Adds all three replicas to PMM monitoring with the pmm-admin add mongodb command.

### Launching the Configuration

Start all services with:

```sh
docker-compose up -d 
```

Expected Output:

```sh
➜  pmm-mongodb-setup docker-compose up -d
[+] Running 10/10
 ✔ Network pmm-mongodb-setup_default            Created      0.0s
 ✔ Volume "pmm-mongodb-setup_mongodb-data-101"  Created      0.0s
 ✔ Volume "pmm-mongodb-setup_mongodb-data-102"  Created      0.0s
 ✔ Volume "pmm-mongodb-setup_mongodb-data-103"  Created      0.0s
 ✔ Container mongodb-rs103                      Healthy      0.1s
 ✔ Container pmm-server                         Healthy      1.1s
 ✔ Container mongodb-rs101                      Healthy      0.1s
 ✔ Container mongodb-rs102                      Healthy      0.1s
 ✔ Container rs-init                            Started      0.1s
 ✔ Container pmm-client                         Started      0.0s
➜  pmm-mongodb-setup
```

Expected Output in Docker Desktop:

![Percona Monitoring and Management (PMM) 3.0.0 - Docker Desktop MongoDB](blog/2025/03/docker-desktop-rs.png)

### Verifying in PMM

Open PMM and explore dashboards such as the MongoDB Replica Set Summary, which displays information about your replicas and various metrics:

![Percona Monitoring and Management (PMM) 3.0.0 - PMM MongoDB](blog/2025/03/pmm-rs-services.png)

For example, I experimented by restarting one of the MongoDB services in Docker Desktop. The Replica Set switched the Primary replica, and when I simulated a failure by stopping a service, the monitoring dashboard reflected this event:

![Percona Monitoring and Management (PMM) 3.0.0 - PMM MongoDB](blog/2025/03/pmm-rs-statuses.png)



## Connecting to MongoDB and Useful Commands

### Connecting to MongoDB

There are several ways to connect to MongoDB depending on your setup and tools:

1. Using Docker Desktop

    If you are using Docker Desktop, you can select a container and open the Exec tab. This opens a terminal within the container.

    From there, you can connect to MongoDB using the mongosh shell with the following command:

    ```sh
    mongosh --host localhost --port 27017 -u databaseAdmin -p password --authenticationDatabase admin
    ```

    ![Percona Monitoring and Management (PMM) 3.0.0 - Docker Desktop MongoDB Connect](blog/2025/03/mongodb-connect.png)

2. Using Docker CLI

    If you're running Docker without Docker Desktop, you can connect to the container using the following command:

    ```bash
    docker exec -it <container_name> bash
    ```
    when you connect to the container, connect to MongoDB 

    ```sh
    mongosh --host localhost --port 27017 -u databaseAdmin -p password --authenticationDatabase admin
    ```
    
3. Connecting from Applications or Tools


    If you are connecting through an application or a tool like MongoDB Compass, you can use connection strings tailored to your setup:

    Here are the MongoDB connection strings tailored for your use cases:

    1. Standalone MongoDB: Connects directly to a single MongoDB instance.

        ```sh
        mongodb://databaseAdmin:password@localhost:27017
        ```

    2. Primary Node: Forces a direct connection to the primary node in the Replica Set using the directConnection=true option.

        ```sh
        mongodb://databaseAdmin:password@localhost:27017/?directConnection=true
        ```

    3. Full Replica Set: Lists all Replica Set members and enables automatic failover using replicaSet=rs

        ```sh
        mongodb://databaseAdmin:password@localhost:27017,localhost:28017,localhost:29017/?replicaSet=rs
        ```

### Useful Commands

Here are some helpful commands for managing and troubleshooting your MongoDB setup:

1. Check the status of the Replica Set. After connecting to MongoDB, use the following command to retrieve the status of the Replica Set:

    ```sh
    rs.status()
    ```

2. Check MongoDB runtime configuration. Use this command to view the configuration options for the running MongoDB instance:

    ```sh
    db.adminCommand({ getCmdLineOpts: 1 })
    ```


## Conclusion

In this article, we explored deploying MongoDB using Docker and Docker Compose. We covered both a Single Instance MongoDB for simple setups and a MongoDB Replica Set for high availability, while integrating them with Percona Monitoring and Management (PMM) for monitoring.

Here are the final configurations you can download:

* Single Instance MongoDB + PMM 3: [Link](https://gist.github.com/dbazhenov/fc954c9bd7f21e2ad17dffb4acfd7142)

* Replica Set MongoDB + PMM 3: [Link](https://gist.github.com/dbazhenov/fd47167734230d294a4aa10da623d1f2)

Thank you for reading! I look forward to your comments and questions.







