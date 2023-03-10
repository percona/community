---
title: "Binding your application to the database in the Kubernetes cluster"
date: "2023-01-24T00:00:00+00:00"
tags: ["Labs","kubernetes", "operators", "databases", "PMM", "DBaaS", "minikube"]
authors:
  - denys_kondratenko
images:
  - blog/2023/02/petclinic.png
slug: k8s-app-db-binding
---

[dbaas-operator](https://github.com/percona/dbaas-operator) is Yet Another DBaaS Kubernetes Operator (need to suggest yadbko as a name) that tries to simplify and unify Database Cluster deployments by building a higher abstraction layer on top of [Percona Kubernetes Operators](https://www.percona.com/software/percona-kubernetes-operators).

So it becomes much easier to deploy the DB cluster with `dbaas-operator` and [PMM DBaaS](https://docs.percona.com/percona-monitoring-and-management/get-started/dbaas.html) on top of it.

But another part of the picture is applications and their workloads to connect to the deployed DB Clusters.

## Services and Applications

On Kubernetes, application deployment could be done in many ways, either manually or as part of automatic deployments.

PMM DBaaS offers both - UI to create DB Clusters and get credentials and API to automate those actions.

`dbaas-operator` adds Kubernetes native API to that batch as well.

But both require additional automation to join the application and the database in one deployment and provide a service to the end user.

And that operation is a challenging task, as every application could expect credentials in some specific format: secrets with hardcoded structures, environment variables with custom names, mount point secrets in particular locations, etc.

Database services add their complexity to that picture by exposing their connections and secrets in a format that is convenient or makes sense for them.

Usually, some Continues Delivery system or deployment package (helm, etc.) ensures all components' correct deployment sequence and health. So many custom pipelines and packages exist to connect a specific application to a database service.

But for simplicity and scalability, it would be nice to have some standard for connection or software that automates such a connection. 

## Service Binding

Connecting services is a known pattern: Service Discovery (broker, registry, repository) for the [Service-Oriented Architecture](https://en.wikipedia.org/wiki/Service-oriented_architecture).

[servicebinding.io](https://servicebinding.io/) is another pattern to bind applications and workloads to the services (REST APIs, databases, event buses, etc.). This specification aims to create a Kubernetes-wide specification for communicating service secrets to workloads in a consistent way.

[Service Binding Operator](https://redhat-developer.github.io/service-binding-operator/userguide/intro.html) glues services and Kubernetes workflows together. It does so for the services and applications that support ServiceBinding specifications and those that don't. 

Out of the box Service Binding Operator supports [Percona Operator for MySQL based on Percona XtraDB Cluster](https://docs.percona.com/percona-operator-for-mysql/pxc/index.html) (PXC), so we will deploy Database Cluster with `dbaas-operator` and connect it to the simple Java application. We will use Spring PetClinic application that supports [Spring Cloud Bindings](https://github.com/spring-cloud/spring-cloud-bindings).

## Create an environment

We need to have Kubernetes cluster, [Operator Lifecycle Manager](https://olm.operatorframework.io/) (OLM) to install operators, and all required operators installed. In this blog, I would use minikube and assume that `operator-sdk` is installed on the system

Here is a [link to the script](https://github.com/denisok/k8s-connect-app-to-db/blob/main/assets/bin/service_binding.sh) that:

- setups multi-node Kubernetes cluster
- installs OLM
- installs needed operators with the help of OLM

As a result we get cluster with all needed operators:

```sh
$ kubectl get sub -A
NAMESPACE   NAME                              PACKAGE                           SOURCE                  CHANNEL
default     dbaas-operator                    dbaas-operator                    dbaas-catalog           stable-v0
default     percona-server-mongodb-operator   percona-server-mongodb-operator   dbaas-catalog           stable-v1
default     percona-xtradb-cluster-operator   percona-xtradb-cluster-operator   dbaas-catalog           stable-v1
operators   my-service-binding-operator       service-binding-operator          operatorhubio-catalog   stable
```

## Create Database Cluster

We will use `dbaas-operator` to demonstrate how easy it is to create DB Cluster with it:

```sh
$ cat <<EOF | kubectl apply -f -
apiVersion: dbaas.percona.com/v1
kind: DatabaseCluster
metadata:
  name: test-pxc-cluster
spec:
  databaseType: pxc
  databaseImage: percona/percona-xtradb-cluster:8.0.27-18.1
  databaseConfig: |
    [mysqld]
    wsrep_provider_options="debug=1;gcache.size=1G"
    wsrep_debug=1
    wsrep_trx_fragment_unit='bytes'
    wsrep_trx_fragment_size=3670016
  secretsName: pxc-sample-secrets
  clusterSize: 1
  loadBalancer:
    type: haproxy
    exposeType: ClusterIP
    size: 1
    image: percona/percona-xtradb-cluster-operator:1.11.0-haproxy
  dbInstance:
    cpu: "1"
    memory: 1G
    diskSize: 15G
EOF

$ kubectl get db
NAME                 SIZE   READY   STATUS   ENDPOINT                                              AGE
test-pxc-cluster     2      2       ready    test-pxc-cluster-haproxy.default                      5m
```

## Create Spring PetClinic app and bind it to the database

```sh
$ kubectl apply -f https://raw.githubusercontent.com/redhat-developer/service-binding-operator/master/samples/apps/spring-petclinic/petclinic-mysql-deployment.yaml
deployment.apps/spring-petclinic created
service/spring-petclinic created

$ kubectl get pods
NAME                                                 READY   STATUS    RESTARTS      AGE
spring-petclinic-f7f587c5c-rvq2v                     0/1     CrashLoopBackOff   2 (17s ago)   67s
```

As we didn't create a binding yet, the application can't connect to the database and thus fails.

Let us bind application to the database and verify it is working:

```sh
$ cat <<EOF | kubectl apply -f -
apiVersion: binding.operators.coreos.com/v1alpha1
kind: ServiceBinding
metadata:
  name: spring-petclinic
  namespace: default
spec:
  services:
    - group: pxc.percona.com
      version: v1
      kind: PerconaXtraDBCluster
      name: test-pxc-cluster
  application:
    name: spring-petclinic
    group: apps
    version: v1
    resource: deployments
EOF

$ kubectl get servicebindings
NAME               READY   REASON              AGE
spring-petclinic   True    ApplicationsBound   4m47s

$ kubectl get deployments
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
spring-petclinic                    1/1     1            1           17m

$ minikube service spring-petclinic --url
http://192.168.39.215:31181
```

What we have done above:

1. Created `kind: ServiceBinding`, which takes PXC secrets and maps them to the application as mount points. 
2. As PetClinic supports ServiceBinding spec with Spring framework, it understands those mount points and connects to the database.

Here is what mount point by ServiceBinding specification that Spring Cloud Bindings library parsed and connected to the database:
```sh
$ kubectl exec deployment/spring-petclinic  -- ls -la /bindings/spring-petclinic/..2023_01_20_21_33_47.4121788695

total 56
drwxr-xr-x 2 root root 320 Jan 20 21:33 .
drwxrwxrwt 3 root root 360 Jan 20 21:33 ..
-rw-r--r-- 1 root root  18 Jan 20 21:33 clustercheck
-rw-r--r-- 1 root root   5 Jan 20 21:33 database
-rw-r--r-- 1 root root  32 Jan 20 21:33 host
-rw-r--r-- 1 root root  17 Jan 20 21:33 monitor
-rw-r--r-- 1 root root  17 Jan 20 21:33 operator
-rw-r--r-- 1 root root  18 Jan 20 21:33 password
-rw-r--r-- 1 root root   4 Jan 20 21:33 port
-rw-r--r-- 1 root root   7 Jan 20 21:33 provider
-rw-r--r-- 1 root root  17 Jan 20 21:33 proxyadmin
-rw-r--r-- 1 root root  18 Jan 20 21:33 replication
-rw-r--r-- 1 root root  18 Jan 20 21:33 root
-rw-r--r-- 1 root root   5 Jan 20 21:33 type
-rw-r--r-- 1 root root   4 Jan 20 21:33 username
-rw-r--r-- 1 root root  17 Jan 20 21:33 xtrabackup
$ kubectl exec deployment/spring-petclinic  -- cat /bindings/spring-petclinic/..2023_01_20_21_33_47.4121788695/database
mysql
$ kubectl exec deployment/spring-petclinic  -- cat /bindings/spring-petclinic/..2023_01_20_21_33_47.4121788695/host
test-pxc-cluster-haproxy.default
```

Check the url that was exposed by minikube:

![Pet Clinic](/blog/2023/02/petclinic.png)

## Summary

There are many ways to deploy applications and services and connect them.

I am trying to collect some of them under my [personal repo](https://github.com/denisok/k8s-connect-app-to-db) to understand the problem deeper. Please suggest other ways by commenting under this blog or in repo.

ServiceBinding specification is a standardized way that scales easily and allows you to connect Kubernetes workloads to the database services.

I will propose to `dbaas-operator` to implement that specification so that it could expose different Database engines (mysql, mongo, pg) in a standard way.
