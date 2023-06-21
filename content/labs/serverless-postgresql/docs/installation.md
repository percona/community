---
title: "Installation"
description: "Packages, Resource planning, Deployment steps"
weight: 2
---
## Installation Packages
Packages are shipped with PostgreSQL 14 or PostgreSQL 15 and for systems with glibc2.31 (Ubuntu 20.04) or glibc2.35:

* [neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.31.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.31.tar.gz)
* [neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.35.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.35.tar.gz)
* [neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.31.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.31.tar.gz)
* [neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.35.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.35.tar.gz)

The packages contain all binaries to start and evaluate the deployment.

## Resource Planning

Given the distributed nature of the deployment and depending on the type of use, separate systems—bare metal, virtual images, or cloud instances—are required. In the table below, you can see how many instances of each are required for using Percona Builds for Neon for testing and production.

| Component | Testing Environment | Production Environment |
| ---- | ----| ---- | 
| Storage broker | 1 instance | 1 instance |
| Pageserver | 1 instance | 1 instance |
| Safe keeper | 1 instance | 3 instances |
| Compute nodes | 1 instance per tenant | Dynamic, depends on your scaling needs |

Some components can be hosted together, and for testing purposes, you can use only a single safekeeper, so all components can be hosted on the same single server. However, this is not recommended for the production environment.

For your convenience, we provide Ansible scripts that you can use to see the sequence of operations and exact commands to deploy the system.

[Percona-Lab/serverless-postgresql-ansible: Ansible playbook to deploy serverless PostgreSQL (github.com)](https://github.com/Percona-Lab/serverless-postgresql-ansible)

## Percona Builds for Neon using Docker
### Prerequisites
- Docker image with all components in Docker Hub
- Hostnames for each instance of storage broker, pageserver, and safekeepers that can communicate with each other through the network.

Deployment of Percona Builds for Neon using Docker consists of two parts:
1. Deploying core components: pageserver, storage broker, and safekeepers.
2. Deploying compute nodes using one of the following combinations:
	- Compute node with new tenant and timeline
	- Compute node with existing tenant and timeline
	- Compute node with branching from existing tenant and timeline
### 1. Deploying core components
**To deploy storage broker, safekeepers, and pageserver:**
1. Start the storage broker by running the following command:
	```
	docker run -d -t --name storagebroker --net=host
	--entrypoint "storage_broker"
	perconalab/neon:latest -l 0.0.0.0:50051
	```
2. Start safekeepers by doing the following:
	1. In /data/skdata, create **datadir**.
	2. For each safekeeper instance, run the following command:
	```
		docker run -d -t --name safekeeper<N> --net=host
		--entrypoint "safekeeper"
		perconalab/neon:latest
		--id=N -D /data --broker-endpoint=http://<0.0.0.0>:50051
		-l <0.0.0.0>:5454 --listen-http=<0.0.0.0>:7676
		```
	Where 
	*safekeeper<N>* is the name of a safekeeper. Depending on the number of safekeepers you want to configure, it can be *safekeeper1*, *safekeeper2*, or *safekeeper3*.
	*N* is the ID of a safekeeper. Depending on the number of safekeepers you want to configure, it can be *1*, *2*, or *3*.
	*<0.0.0.0>* is the IP address of the machine on which the configuration is being set up.
3. Start the pageserver by doing the following:
	1. In /data/neondata, create **datadir**.
	2. Run the following command:
		```
		docker run -d -t --name pageserver --net=host
		--entrypoint "pageserver"
		perconalab/neon:latest
		-D /data -c "id=1" -c "broker_endpoint='http://<0.0.0.0>:50051'"
		-c "listen_pg_addr='0.0.0.0:6400'" -c "listen_http_addr='0.0.0.0:9898'"
		-c "pg_distrib_dir='/opt/neondatabase-neon/pg_install'"
	```
The core components are running. You can proceed to deploying compute nodes.

### 2. Deploying compute nodes
There are several ways of deploying compute nodes based on a tenant-timeline combination that you need:
- Deploying a compute node with a new tenant and timeline.
- Deploying a compute node with the existing tenant and timeline.
- Deploying a compute node with branching from the existing tenant and timeline.

#### Deploying a compute node with a new tenant and timeline
**To deploy a compute node with a new tenant and timeline:**
Run the following command:
```
docker run -d -t --name compute<N>
--entrypoint "/compute.sh"
-p55432:55432 -e PAGESERVER=<0.0.0.0>
-e SAFEKEEPERS=<0.0.0.0>:5454 perconalab/neon:latest
```
Where 
*compute<N>* is the name of the new compute node. For example, *compute1*.
*<0.0.0.0>* is the IP address of the machine where the pageserver and safekeepers are located.
The compute node is running. It can act as a normal PostgreSQL server.
You can connect it to with PostgreSQL client via the 55432 port by running the following command:
psql -p55433 -h 127.0.0.1 -U cloud_admin postgres

#### Deploying a compute node with the existing tenant and timeline
To deploy a compute node with the existing tenant and timeline
1. In docker logs compute, locate the tenant and timeline values. For example:
```
{
"name": "neon.timeline_id",
"value": "4b4541ad75370114cd7956e457cc875f",
"vartype": "string"
},
{
"name": "neon.tenant_id",
"value": "6c92c037a54c0e3a005cdd4a69d6e997",
"vartype": "string"
},
```
Where the timeline value is *4b4541ad75370114cd7956e457cc875f* and the tenant value is *6c92c037a54c0e3a005cdd4a69d6e997*.
2. Run the following command:
```
docker run -d -t --name compute<N>
--entrypoint "/compute.sh" -p55433:55432
-e PAGESERVER=<0.0.0.0> -e SAFEKEEPERS=<0.0.0.0>:5454
-e TENANT=<value> -e TIMELINE=<value>
perconalab/neon:latest
```
Where
*compute<N>* is the name of the compute node. For example, *compute2*.
*<0.0.0.0>* is the IP address of the machine where the page server and safekeepers are located.
*<value>* is the corresponding tenant or timeline value from `docker logs`.

#### Deploying a compute node with branching from the existing tenant and timeline
**To deploy a compute node with branching from the existing tenant and timeline:**
Run the following command:
```
docker run -d -t --name compute<N>
--entrypoint "/compute.sh" -p55435:55432
-e PAGESERVER=<0.0.0.0>
-e SAFEKEEPERS=<0.0.0.0>:5454
-e TENANT=<value> -e TIMELINE=<value>
-e "CREATE_BRANCH=1" perconalab/neon:latest
```
Where
*compute<N>* is the name of the new compute node. For example, *compute3*.
*<0.0.0.0>* is the IP address of the machine where the page server and safekeepers are located.
*<value>* is the corresponding tenant or timeline value from `docker logs`.