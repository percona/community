---
title: "The Importance of Anti-Affinity in Kubernetes"
date: "2023-11-30T00:00:00+00:00"
draft: false
tags: ["kubernetes", "anti-affinity", "mongodb", "percona"]
authors:
  - edith_puclla
images:
  - blog/2023/11/intro.png
slug: anti-affinity-in-kubernetes
---

Last week, I embarked on the task of deploying our [Percona Operator for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/index.html) in Kubernetes. After completing the deployment process, I noticed that the status of the Custom Resource Definition for Percona Server for MongoDB was still displaying as 'initializing' and two of our Pods remained in a **Pending** state.

```bash
edithpuclla@Ediths-MBP % kubectl get perconaservermongodbs.psmdb.percona.com -n mongodb
NAME             ENDPOINT                                          STATUS         AGE
my-db-psmdb-db   my-db-psmdb-db-mongos.mongodb.svc.cluster.local   initializing   4m58s
```

```bash
edithpuclla@Ediths-MBP % kubectl get pods -n mongodb
NAME                                    READY   STATUS    RESTARTS   AGE
my-db-psmdb-db-cfg-0                    2/2     Running   0          109m
my-db-psmdb-db-cfg-1                    2/2     Running   0          108m
my-db-psmdb-db-cfg-2                    0/2     Pending   0          107m
my-db-psmdb-db-mongos-0                 1/1     Running   0          106m
my-db-psmdb-db-mongos-1                 1/1     Running   0          106m
my-db-psmdb-db-rs0-0                    2/2     Running   0          109m
my-db-psmdb-db-rs0-1                    2/2     Running   0          108m
my-db-psmdb-db-rs0-2                    0/2     Pending   0          107m
my-op-psmdb-operator-77b75bbc7c-qd9ls   1/1     Running   0          118m
```

Upon further inspection of the pod in **pending** status, I discovered a clear indicator of the error:

```bash
kubectl describe pod my-db-psmdb-db-cfg-2 -n mongodb
Events:
  Type     Reason             Age                   From                Message
  ----     ------             ----                  ----                -------
  Normal   NotTriggerScaleUp  3m53s (x62 over 13m)  cluster-autoscaler  pod didn't trigger scale-up:
  Warning  FailedScheduling   3m27s (x4 over 13m)   default-scheduler   0/2 nodes are available: 2 node(s) didn't match pod anti-affinity rules. preemption: 0/2 nodes are available: 2 No preemption victims found for incoming pod..

```

I took a closer look at the YAML configuration of our CRD in the **Replsets** section, particularly drawn to the **Affinity** subsection.

```bash
kubectl describe perconaservermongodbs.psmdb.percona.com my-db-psmdb-db -n mongodb
```

Here's what I discovered:

![Affinity](blog/2023/11/affinity-01.png)

**Affinity** and **Anti-Affinity** are key parts of the scheduling process in Kubernetes, and both focus on ensuring that Pods are correctly assigned to Nodes in the cluster. You can configure a Pod to run on a specific node or group of nodes. There are several ways to achieve this, [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) is the simplest way to constrain Pods to nodes with specific labels. Affinity and anti-affinity expand the types of constraints you can define and give you more flexibility.

Let’s explore what it means to specify anti-affinity rules for the ReplicaSets.

The key **kubernetes.io/hostname** is a well-known label in Kubernetes that is automatically assigned to each node in the cluster. It usually holds the value of the node's hostname.
When used as a topology key in anti-affinity rules, it implies that the rule should consider the hostname of the nodes. In simpler terms, it's telling Kubernetes to not to schedule the pods of this ReplicaSet on the same physical or virtual host (node).

If we review our cluster, it has two nodes for installing the Percona Operator for MongoDB.

```bash
edithpuclla@Ediths-MBP ~ % kubectl get nodes
NAME                                                 STATUS   ROLES    AGE   VERSION
gke-mongo-operator-test-default-pool-7c118de9-b9vc   Ready    <none>   68m   v1.27.4-gke.900
gke-mongo-operator-test-default-pool-7c118de9-ts16   Ready    <none>   68m   v1.27.4-gke.900
```

In the context of databases like MongoDB, High availability is often achieved through replication, ensuring that the database can continue to operate even if one or more nodes fail. Within a MongoDB Replica Set, there are multiple copies of the data, and these copies are hosted on different Replica Set members. The default HA MongoDB topology is a 3-member Replica Set. **Percona Operator for MongoDB** deploys MongoDB in the same topology by default. With anti-affinity set to kubernetes.io/hostname, that means at least 3 Kubernetes worker nodes are needed to deploy MongoDB.

![Affinity](blog/2023/11/affinity-02.png)

We created the minimum three nodes that the **Percona Operator for MongoDB** needs. We see that we don’t have the error with Antiaffinity in the Pods because each Pod was located appropriately in different nodes. Now our operator and our database were deployed correctly.

```bash
edithpuclla@Ediths-MBP ~ % kubectl get nodes
NAME                                                 STATUS   ROLES    AGE   VERSION
gke-mongo-operator-test-default-pool-e4e024a8-1dj3   Ready    <none>   76s   v1.27.4-gke.900
gke-mongo-operator-test-default-pool-e4e024a8-d6j2   Ready    <none>   74s   v1.27.4-gke.900
gke-mongo-operator-test-default-pool-e4e024a8-jkkr   Ready    <none>   76s   v1.27.4-gke.900
```

If we list all the resources in our namespace, we can see that all pods are running properly and all the resources have been created.

```bash
edithpuclla@Ediths-MBP ~ % kubectl get all -n mongodb
NAME                                        READY   STATUS    RESTARTS   AGE
pod/my-db-psmdb-db-cfg-0                    2/2     Running   0          4m40s
pod/my-db-psmdb-db-cfg-1                    2/2     Running   0          4m2s
pod/my-db-psmdb-db-cfg-2                    2/2     Running   0          3m20s
pod/my-db-psmdb-db-mongos-0                 1/1     Running   0          2m56s
pod/my-db-psmdb-db-mongos-1                 1/1     Running   0          2m39s
pod/my-db-psmdb-db-rs0-0                    2/2     Running   0          4m39s
pod/my-db-psmdb-db-rs0-1                    2/2     Running   0          3m59s
pod/my-db-psmdb-db-rs0-2                    2/2     Running   0          3m28s
pod/my-op-psmdb-operator-77b75bbc7c-q2rqh   1/1     Running   0          6m47s

NAME                            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)     AGE
service/my-db-psmdb-db-cfg      ClusterIP   None           <none>        27017/TCP   4m40s
service/my-db-psmdb-db-mongos   ClusterIP   10.72.17.115   <none>        27017/TCP   2m56s
service/my-db-psmdb-db-rs0      ClusterIP   None           <none>        27017/TCP   4m39s

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-op-psmdb-operator   1/1     1            1           6m47s

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/my-op-psmdb-operator-77b75bbc7c   1         1         1       6m47s

NAME                                     READY   AGE
statefulset.apps/my-db-psmdb-db-cfg      3/3     4m41s
statefulset.apps/my-db-psmdb-db-mongos   2/2     2m58s
statefulset.apps/my-db-psmdb-db-rs0      3/3     4m40s
```

In conclusion, affinity and anti-affinity in Kubernetes are tools for strategically placing pods in a cluster to optimize factors such as performance, availability, and compliance, which are critical for the smooth and efficient operation of containerized applications, also setting up anti-affinity rules like [failure-domain.beta.kubernetes.io/zone](https://docs.percona.com/percona-operator-for-mongodb/constraints.html#affinity-and-anti-affinity) in Kubernetes is a key strategy for keeping clusters running, especially in production environments. This approach spreads pods across different availability zones, which means if one zone has an issue, the others can keep the system running. It's a smart way to ensure your cluster can handle unexpected outages, making it a popular choice for those who need their Kubernetes setups to be reliable and available at all times.

Learn more about our [Percona Operator for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/index.html), and if you have questions or comments, you can write to us on our [Percona Community Forum](https://forums.percona.com/).
