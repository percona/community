---
title: "Installation"
description: "Packages, Resource planning, Deployment steps"
weight: 2
---

Right now we have tar.gz packages 

* [neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.31.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.31.tar.gz)
* [neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.35.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG14-1.0.0-Linux-x86_64.glibc2.35.tar.gz)
* [neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.31.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.31.tar.gz)
* [neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.35.tar.gz](https://github.com/Percona-Lab/neon/releases/download/v1.0.0/neondatabase-neon-PG15-1.0.0-Linux-x86_64.glibc2.35.tar.gz)

We ship packages either with PostgreSQL 14 or PostgreSQL 15 and for systems with glibc2.31 (Ubuntu 20.04) or glibc2.35

The packages contain all binaries to start and evaluate the deployment.

## Resource planning

Given the distributed nature of the deployment, we need separate systems (either bare metal, virtual images, or cloud instances) for the following components:

1. Storage broker
2. Page server
3. Safekeeper (3 instances)
4. Compute nodes

Some components can be hosted together, and for testing purposes, you can use only a single safekeeper, so all components can be hosted on the same single server. However, this is not recommended for the production environment.

For reference, we provide ansible scripts that you can use to see the sequence of operations and exact commands to deploy the system.

[Percona-Lab/serverless-postgresql-ansible: Ansible playbook to deploy serverless PostgreSQL (github.com)](https://github.com/Percona-Lab/serverless-postgresql-ansible)

## Deployment steps

Let’s assume we have  hosts with names `storagebroker`, `safekeeper1`, `safekeeper2`, `safekeeper3`, `pageserver` and they all can communicate with each over network

### 1. Start storage broker

On the server storagebroker execute:

```
storage_broker -l 0.0.0.0:50051
```

### 2. Start safekeepers

Create datadir for safekeepers in `/data/skdata`

And for each safekeeper execute (vary N from 1 to amount you have)

```
safekeeper --id=N -D /data/skdata  --broker-endpoint=http://storagebroker:50051 -l safekeeperN:5454 --listen-http=0.0.0.0:7676
```

### 3. Start pageserver

Create datadir for pageserver in `/data/neondata`

Execute

```
pageserver -D /data/neondata -c "id=1" -c "broker_endpoint='http://storagebroker:50051'" -c "listen_pg_addr='0.0.0.0:6400'" -c "listen_http_addr='0.0.0.0:9898'"
```

### 4. Initialize compute nodes

This is the most involving step as we need to do some preparation

The Neon instance supports multiple tenants and each tenant can have multiple branches (timelines) 

The first step is to create tenant, this is done by REST API call to pageserver:

```
echo "Create a tenant"
PARAMS=(
     -sb 
     -X POST
     -H "Content-Type: application/json"
     -d "{}"
     http://pageserver:9898/v1/tenant/
)
tenant_id=$(curl "${PARAMS[@]}" | sed 's/"//g')
echo "Tenant id: $tenant_id"
```

Now, having `tenant_id`, we create a timeline (branch) for this tenant:

```
tenant_id=$1

PARAMS=(
     -sb 
     -X POST
     -H "Content-Type: application/json"
     -d "{\"tenant_id\":\"${tenant_id}\", \"pg_version\": 14}"
     "http://pageserver:9898/v1/tenant/${tenant_id}/timeline/"
)

result=$(curl "${PARAMS[@]}")
echo $result | jq .

tenant_id=$(echo ${result} | jq -r .tenant_id)
timeline_id=$(echo ${result} | jq -r .timeline_id)

echo "Tenant id: $tenant_id"
echo "Timeline id: $timeline_id"
```

The next step is to prepare a specification json file for the compute node. The easiest way it to take template

[serverless-postgresql-ansible/spec.prep.json.j2 at main · Percona-Lab/serverless-postgresql-ansible (github.com)](https://github.com/Percona-Lab/serverless-postgresql-ansible/blob/main/templates/spec.prep.json.j2)

And set the proper values in the following sections:

```
{
   "name": "neon.safekeepers",
   "value": "{{ groups['safekeeper'] | map('extract', hostvars, ['ansible_'+networkinterface, 'ipv4', 'address']) | join(':5454,')  }}:5454",
   "vartype": "string"
},
{
   "name": "neon.timeline_id",
   "value": "TIMELINE_ID",
   "vartype": "string"
},
{
   "name": "neon.tenant_id",
   "value": "TENANT_ID",
   "vartype": "string"
},
{
   "name": "neon.pageserver_connstring",
   "value": "host={{hostvars[groups['pageserver'][0]]['ansible_facts'][networkinterface]['ipv4']['address']}} port=6400",
   "vartype": "string"
},
```
Create datadir for computenode in `/data/compute-pgdata`

And then start a compute node as

```
echo "Start compute node"
compute_ctl --pgdata /data/compute-pgdata \
     -C "postgresql://cloud_admin@localhost:55433/postgres"  \
     -b <PATH_TO_PG_FROM_TARGZ>/postgres         \
     -S spec.json
```

Where postgres should be taken from our tar.gz packages

If all steps were execute successfully at this stage we should have running a compute node,
which can act as a normal postgresql server.

So we can connect it to with psql client:

`psql -p55433 -h 127.0.0.1 -U cloud_admin postgres`



