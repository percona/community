---
title: "Getting Started with Percona PXC Operator"
date: "2026-11-12T07:04:00+00:00"
tags: ['MySQL','PXC']
categories: ['MySQL']
authors:
  - neil_armitage
images:
  - blog/2026/10/getting-started-pg-cover.png
---

As part of many conversations I had during Percona Live I was asked why we didn't use the Percona Operator for MySQL based on Percona XtraDB Cluster. We are currently running hundreds of PXC clusters across many Kubernetes environments all deployed with our own in-house operator.  As part of the evaluation I needed to set up a repeatable environment with S3 compatible storage that could run locally so I've documented my setup in the hope it will help others.

I've tried not to dig too deeply into the operations of PXC cluster as I felt it would add too much complexity to the article and really needs more in-depth explanations than I could give here. There are lots of good articles around explaining the concepts introduced here so I would recommend further research if you are interested.

Parts of this article are the same as the getting started with [PostgreSQL](https://percona.community/blog/2026/10/29/getting-started-with-percona-postgresql-operator/), this isn't laziness it's my way of keeping things simple. I try and create the same development process for most environments, so the setup should be the same.

Full disclaimer: I've used this setup on an Arm-based MacBook. I'm assuming it will work on Linux pretty much the same but for Windows I have no idea. I've not touched Windows in a long time but it _should_ work the same.

Installing kind is pretty simple and will depend on your host O/S - full details are [here](https://kind.sigs.k8s.io/docs/user/quick-start/).

The scripts used below can be found on [GitHub](https://github.com/statefulops/mysql-scripts.git) in the directory ```Percona-Operator-PXC```

```shell
git clone https://github.com/statefulops/mysql-scripts.git
cd mysql-scripts/Percona-Operator-PXC
```

## Deploy a base cluster with an object store

The first step is to deploy a multi-node Kind cluster with a way of simulating an S3 compatible object store (in this example using [RustFS](https://rustfs.com/)). Using something like RustFS ensures we avoid any cloud costs when testing backups and restores.

The quick and dangerous way is to run a script from GitHub

```shell
curl -fsSL https://raw.githubusercontent.com/statefulops/kind-scripts/main/s3/create-cluster.sh | bash -s -- v1.37.0 percona-pxc
```

The safer way is to download the script, check it's not doing anything harmful and then execute it yourself

```shell
curl -fsSL https://raw.githubusercontent.com/statefulops/kind-scripts/main/s3/create-cluster.sh -o create-cluster.sh

less create-cluster.sh

chmod +x create-cluster.sh

./create-cluster.sh v1.37.0 percona-pxc
```

This will deploy a control-plane node and 3 workers with zone labels, and a container running RustFS, using Kubernetes 1.37. I tend to always use zone labels even locally as it simulates multiple zone deployments.

```shell
kubectl get nodes -L topology.kubernetes.io/zone
```

```text
NAME                        STATUS   ROLES           AGE     VERSION   ZONE
percona-pxc-control-plane   Ready    control-plane   3m39s   v1.37.0
percona-pxc-worker          Ready    <none>          3m25s   v1.37.0   AZ-A
percona-pxc-worker2         Ready    <none>          3m25s   v1.37.0   AZ-B
percona-pxc-worker3         Ready    <none>          3m25s   v1.37.0   AZ-C
```

```shell
kubectl get po -n rustfs
```

```text
NAME                      READY   STATUS    RESTARTS   AGE
rustfs-574c7b89d7-5dl4d   1/1     Running   0          4m1s
```

A nodeport is set automatically so the RustFS UI will be available on [http://localhost:9001](http://localhost:9001).  The user is set to *myadminuser* and the script sets a random value for the secret password in a Kubernetes secret. To get the password run

```shell
kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.secret-key}' | base64 -d
```

UI on [http://localhost:9001](http://localhost:9001)

![Rust FS Login](blog/2026/10/getting-started-pg-rustfs-logon.png)


![Rust FS UI](blog/2026/10/getting-started-pg-rustfs-ui.png)


Standard AWS CLI commands work as well - make sure you run the make_bucket command as it is needed later.

```shell
export AWS_ACCESS_KEY_ID=myadminuser
export AWS_SECRET_ACCESS_KEY=$(kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.secret-key}' | base64 -d)
export AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url http://localhost:9000 s3 mb s3://my-kind-bucket
```

```text
make_bucket: my-kind-bucket
```

```shell
aws --endpoint-url http://localhost:9000 s3 ls
```

```text
2026-10-12 12:14:49 my-kind-bucket
```

## Install the Percona PXC Operator 1.20.1

Add the Percona Helm repo:

```shell
helm repo add percona https://percona.github.io/percona-helm-charts/
helm repo update
```

Safety check — only ever run this against a local kind cluster: _I might have learnt this lesson the hard way_ :) 

```shell
CURRENT_CONTEXT=$(kubectl config current-context)
case "$CURRENT_CONTEXT" in
*kind*) echo "OK: using kind context '$CURRENT_CONTEXT'" ;;
*) echo "ABORT: context '$CURRENT_CONTEXT' is not a kind cluster"; exit 1 ;;
esac
```

```shell
kubectl create namespace pxc-operator
helm install pxc-operator percona/pxc-operator --version 1.20.1 --namespace pxc-operator

kubectl config set-context --current --namespace=pxc-operator
```

## Deploy the cluster


This is a simple deployment that will deploy a 3 node PXC cluster with 3 HAProxy nodes.

```shell
kubectl apply -f cr.yaml
```

Check status:

```shell
kubectl get perconaxtradbcluster
```

While initializing:

```text
NAME       ENDPOINT                        STATUS         PXC   PROXYSQL   HAPROXY   AGE
cluster1   cluster1-haproxy.pxc-operator   initializing   1                3         3m16s
```

Once ready:

```text
NAME       ENDPOINT                        STATUS   PXC   PROXYSQL   HAPROXY   AGE
cluster1   cluster1-haproxy.pxc-operator   ready    3                3         5m23s
```

_This will take some time to install based on internet speeds etc_

Eventually you should get a running cluster

```shell
kubectl get po
NAME                            READY   STATUS    RESTARTS   AGE
cluster1-haproxy-0              2/2     Running   0          12m
cluster1-haproxy-1              2/2     Running   0          10m
cluster1-haproxy-2              2/2     Running   0          10m
cluster1-pxc-0                  3/3     Running   0          12m
cluster1-pxc-1                  3/3     Running   0          10m
cluster1-pxc-2                  3/3     Running   0          9m14s
pxc-operator-64d6bd6f58-dn6mw   1/1     Running   0          14m
```

## Connect to the cluster via the CLI

Get the root password from the new Kubernetes secret:

```bash
kubectl get secret cluster1-secrets --template='{{.data.root | base64decode}}{{"\n"}}'
```

Launch a client pod and connect to the command line:

```bash
kubectl run -i --rm --tty percona-client --image=percona/percona-xtradb-cluster:8.4 --restart=Never -- bash -il
```

Inside the client pod:

```bash
mysql -u root -p -h cluster1-haproxy
```

```sql
mysql> select @@hostname;
+----------------+
| @@hostname     |
+----------------+
| cluster1-pxc-0 |
+----------------+
1 row in set (0.00 sec)

mysql>
```

The connection to the MySQL instance from ```cluster1-haproxy``` is via several hops.

* ```cluster1-haproxy``` is a Kubernetes service that points to the 3 HAProxy nodes.
* The HAProxy nodes route the connection to one of the active MySQL nodes in the cluster.

So as long as your client connection is well behaved and performs retries correctly your connection should remain connected to the cluster during a node failure.

From the client pod started above check what MySQL node you are connected to.

```sql
mysql> select @@hostname;
+----------------+
| @@hostname     |
+----------------+
| cluster1-pxc-0 |
+----------------+
1 row in set (0.00 sec)
```

In a separate terminal terminate the node you are connected to.

```shell
kubectl delete po cluster1-pxc-0 
```

While the pod is terminating in the original terminal re-try the select.

```sql
mysql> select @@hostname;
ERROR 2013 (HY000): Lost connection to MySQL server during query
No connection. Trying to reconnect...
Connection id:    3163
Current database: *** NONE ***

+----------------+
| @@hostname     |
+----------------+
| cluster1-pxc-2 |
+----------------+
1 row in set (0.01 sec)

mysql>
```

So the mysql client noticed the connection had broken, re-established it and this time HAProxy sent the connection to ```cluster1-pxc-2``` which was still active.

## Backup to RustFS

Before running the backup run a MySQL client again and create a table with some data

```sql
create schema test;
use test;
CREATE TABLE phonebook(phone VARCHAR(32) PRIMARY KEY, firstname VARCHAR(32), lastname VARCHAR(32), address VARCHAR(64));

INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7890', 'John', 'Doe', 'North America');

SELECT * FROM phonebook;
```

```sql
mysql> SELECT * FROM phonebook;
+-----------------+-----------+----------+---------------+
| phone           | firstname | lastname | address       |
+-----------------+-----------+----------+---------------+
| +1 123 456 7890 | John      | Doe      | North America |
+-----------------+-----------+----------+---------------+
1 row in set (0.00 sec)
```

Create the backup S3 secret from the RustFS admin credentials:

Either a quick one-liner:

```bash
kubectl create secret generic my-cluster-name-backup-s3 --from-literal=AWS_ACCESS_KEY_ID="$(kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.access-key}' | base64 -d)" --from-literal=AWS_SECRET_ACCESS_KEY="$(kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.secret-key}' | base64 -d)" --dry-run=client -o yaml | kubectl apply -f -
```

or get the base64-encoded values:

```bash
kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.access-key}'
kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.secret-key}'
```

Add the values above to the `data:` section of ```backup-secret-s3.yaml``` and apply it

```bash
kubectl apply -f backup-secret-s3.yaml
```

Run a backup:

```bash
kubectl apply -f backup.yaml
```

Find the backup pod and check its logs:

```bash
kubectl get po | grep xb-backup1
kubectl logs xb-backup1-bnrwj
```

```shell
2026-11-14 09:08:38.992  INFO: SST script finished with exit code: 0
2026-11-14 09:08:39.096  INFO: Exiting main loop with code OK
2026-11-14 09:08:39.096  INFO: Garbd returns 0
+ GARBD_EXIT_CODE=0
+ case ${GARBD_EXIT_CODE} in
+ log INFO 'Backup was finished successfully'
+ exit 0
2026-11-14 09:08:39 [INFO] Backup was finished successfully
```

Verify the backup landed in S3:

```bash
export AWS_ACCESS_KEY_ID=myadminuser
export AWS_SECRET_ACCESS_KEY=$(kubectl get secret rustfs-admin-credentials -n rustfs -o jsonpath='{.data.secret-key}' | base64 -d)
export AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url http://localhost:9000 s3 ls my-kind-bucket/
```

```shell
                           PRE cluster1-2026-11-14-09:07:52-full.sst_info/
                           PRE cluster1-2026-11-14-09:07:52-full/
2026-11-14 09:08:38      26667 cluster1-2026-11-14-09:07:52-full.md5
2026-11-14 09:08:23        128 cluster1-2026-11-14-09:07:52-full.sst_info.md5
```

## Restore


Before doing the restore remove the table created earlier to check the restore worked.

```sql
use test;
drop table phonebook;
```

Disable any binlog processing before running a restore.

```shell
kubectl patch pxc cluster1  \
  --type merge \
  -p '{"spec":{"backup":{"pitr":{"enabled":false}}}}'
```

In this case you should see the following message as it wasn't enabled

```shell
perconaxtradbcluster.pxc.percona.com/cluster1 patched (no change)
```

Trigger a restore and watch the pods get recreated

```shell
cat <<EOF | kubectl apply -f-
apiVersion: "pxc.percona.com/v1"
kind: "PerconaXtraDBClusterRestore"
metadata:
  name: "restore1"
spec:
  pxcCluster: "cluster1"
  backupName: "backup1"
EOF
```

Once the restore has been completed check the table is back.

```sql
mysql> SELECT * FROM phonebook;
ERROR 2013 (HY000): Lost connection to MySQL server during query
No connection. Trying to reconnect...
Connection id:    1117
Current database: test

+-----------------+-----------+----------+---------------+
| phone           | firstname | lastname | address       |
+-----------------+-----------+----------+---------------+
| +1 123 456 7890 | John      | Doe      | North America |
+-----------------+-----------+----------+---------------+
1 row in set (0.03 sec)

mysql>
```

## Enabling binlog syncing

Realistically you are going to want to back up the Binary Logs (binlogs) to minimise data loss.

Apply the updated cr which will enable the binlog syncing.

```bash
kubectl apply -f cr-binlogs.yaml
```

Verify pods:

```shell
kubectl get po
```

```shell
NAME                                  READY   STATUS      RESTARTS   AGE
cluster1-haproxy-0                    2/2     Running     0          17m
cluster1-haproxy-1                    2/2     Running     0          16m
cluster1-haproxy-2                    2/2     Running     0          16m
cluster1-pitr-7dc984dcd9-rs7xn        1/1     Running     0          47s
cluster1-pxc-0                        3/3     Running     0          17m
cluster1-pxc-1                        3/3     Running     0          16m
cluster1-pxc-2                        3/3     Running     0          15m
```

To get some binlogs being created start the sysbench container

```shell
kubectl apply -f sysbench.yaml
```

Once it has been running for a few minutes you should now be able to see binlogs being backed-up into the S3 bucket.

```shell
aws --endpoint-url http://localhost:9000 s3 ls my-kind-bucket/
```

```shell
                           PRE cluster1-2026-11-14-16:40:02-full.sst_info/
                           PRE cluster1-2026-11-14-16:40:02-full/
2026-11-14 17:05:50   19973933 binlog_1794675888_000025_40ab6621c720a080c20710905ef86632
2026-11-14 17:05:50         43 binlog_1794675888_000025_40ab6621c720a080c20710905ef86632-gtid-set
2026-11-14 16:40:29      26815 cluster1-2026-11-14-16:40:02-full.md5
2026-11-14 16:40:15        128 cluster1-2026-11-14-16:40:02-full.sst_info.md5
2026-11-14 17:05:50        346 gtid-binlog-cache.json
2026-11-14 17:05:50         43 last-binlog-set-d41f08dc-e04a-11f1-b333-4b79bd8eb077
```

## Cluster Operation Overview

This section was originally earlier on but I moved it later to avoid hitting some of the more complex bits early on. While this article is focused on Percona XtraDB Cluster (PXC) the basic principles are the same for Galera cluster, MariaDB Galera Cluster and PXC. They all go back to the same work done by Codership Oy back in the 2000s. I'm going to avoid commenting on the current state of the product and the purchase of Codership by MariaDB but focus on Percona's PXC as it's a stable supported version.

PXC adds the two following extra components to the running mysqld instance to form the cluster:

* The Group Communication System (GCS), this provides a private network between the nodes to manage cluster membership, order transactions globally and provide failure detection.
* The wsrep API provides write-set replication as a plugin to MySQL

These together allow the cluster to run a near full master-master replication allowing well behaved clients to write to any of the nodes simultaneously, in the right environment. Please note both caveats, a well-behaved client and the right environment.

* Dropping an existing poorly written application into PXC and expecting it to solve all of the problems you have isn't going to work. The application needs to understand that it might get deadlocked and to try again and if it reads from another node it may not see the data it has just written. The reason for this is briefly explained below.

* PXC nodes need to be able to talk to each other quickly to maintain state. In reality keeping the nodes in the same cloud region is probably a best practice. Nodes spread across availability zones in AWS seems to be a sweet spot. Spreading them around the globe will probably not work, yes I've seen it done but you start to stretch the laws of physics and end up with a very unstable environment. A more fault tolerant solution is needed for this use case.

The process of modifying data within the MySQL instance is now more complex than with a single node as it needs to be coordinated across all the nodes. The simplified steps are:

1. A transaction is completed on a local node and the client issues a commit, at this point the client has to wait before getting a response back
2. wsrep creates a write-set containing all the modifications in the commit. This is now broadcast to all the other nodes
3. Certification of the write-set is now carried out on all the nodes ensuring it can be applied everywhere. 
4. If there is no conflict the write-set is certified, the original transaction is allowed to commit successfully, and the other nodes add the write-set to their applier queues to be applied.
5. If there is a conflict and the write-set can't be applied to all nodes the transaction gets rolled back and it's not applied. This means the original client transaction fails and needs to be retried.

For the client a detail in step 4 is important, while the update is made on the original node it could still be on the applier queue on one of the other nodes meaning there is a small window when the data is different. The client needs to be aware of this and ensure if it needs to read its own writes it always connects to the same node (or uses `wsrep_sync_wait`). If the applier queue gets too large the cluster will pause updates until it is processed.

Updates can be performed as long as the cluster has _quorum_. More than 50% of the nodes have to be available and online to achieve quorum. This is why clusters are normally 3 nodes (or at least an odd number of nodes) as it allows for one node to be down and the cluster will continue to operate. 

## Recovery Modes IST vs SST

When nodes fail the cluster will recover the failed nodes using two different approaches.

* IST (Incremental State Transfer), this is used when the node has been down for a short period and the missing write-sets exist in a donor node's gcache. Once the failed (joiner) node is restarted it will connect to a donor node and apply the missing write-sets before joining the node into the cluster.

* SST (State Snapshot Transfer), if the missing write-sets are not available, or it's a new node, an SST will be triggered. This essentially takes a full backup from a donor node and rebuilds the node from this backup. This can obviously take some time to complete with a large dataset. The donor will stay available but will have the extra load of the backup running.

To see the two options first of all check the cluster is healthy and the sysbench load is running.

```sql
show status like 'wsrep_cluster%';
```

```sql
+----------------------------+--------------------------------------+
| Variable_name              | Value                                |
+----------------------------+--------------------------------------+
| wsrep_cluster_weight       | 30                                   |
| wsrep_cluster_capabilities |                                      |
| wsrep_cluster_conf_id      | 3                                    |
| wsrep_cluster_size         | 3                                    |
| wsrep_cluster_state_uuid   | ec51ce68-e0d6-11f1-808a-03de7cc64daa |
| wsrep_cluster_status       | Primary                              |
+----------------------------+--------------------------------------+
6 rows in set (0.00 sec)
```

Cluster status should be ```Primary``` and cluster size should be 3.

Sysbench should be pottering along generating load

```shell
kubectl logs sysbench-8dd57985c-hbcv7
```

```text
[ 570s ] thds: 4 tps: 20.90 qps: 418.00 (r/w/o: 292.60/45.60/79.80) lat (ms,95%): 7.43 err/s: 0.00 reconn/s: 0.00
[ 570s ] queue length: 0, concurrency: 0
[ 580s ] thds: 4 tps: 18.50 qps: 370.00 (r/w/o: 259.00/41.90/69.10) lat (ms,95%): 9.22 err/s: 0.00 reconn/s: 0.00
[ 580s ] queue length: 0, concurrency: 0
```

First to trigger an IST just delete one of the pods.

```shell
kubectl delete po cluster1-pxc-2
```

Once the pod has recovered review the MySQL logs to see what method was chosen.

```shell
kubectl logs cluster1-pxc-2 -c logs | cut -d "\"" -f4
```

```shell
2026-11-15T09:49:34.020065Z 2 [Note] [MY-000000] [Galera] Check if state gap can be serviced using IST\n
2026-11-15T09:49:34.020077Z 2 [Note] [MY-000000] [Galera] ####### IST uuid:ec51ce68-e0d6-11f1-808a-03de7cc64daa f: 14710, l: 14998, STRv: 3\n
2026-11-15T09:49:34.020121Z 2 [Note] [MY-000000] [Galera] IST receiver addr using ssl://10.244.1.7:4568\n
2026-11-15T09:49:34.020138Z 2 [Note] [MY-000000] [Galera] IST receiver using ssl\n
2026-11-15T09:49:34.020233Z 2 [Note] [MY-000000] [Galera] Prepared IST receiver for 14710-14998, listening at: ssl://10.244.1.7:4568\n
2026-11-15T09:49:34.021071Z 0 [Note] [MY-000000] [Galera] Member 1.0 (cluster1-pxc-2) requested state transfer from 'cluster1-pxc-1,'. Selected 0.0 (cluster1-pxc-1)(SYNCED) as donor.\n
2026-11-15T09:49:34.021089Z 0 [Note] [MY-000000] [Galera] Shifting PRIMARY -> JOINER (TO: 15027)\n
2026-11-15T09:49:34.021116Z 2 [Note] [MY-000000] [Galera] Requesting state transfer: success, donor: 0\n
2026-11-15T09:49:34.304854Z 0 [Note] [MY-000000] [WSREP-SST]    joiner: => Rate:[ 487 B/s] Avg:[ 487 B/s] Elapsed:0:00:00  Bytes:  244 B \n
2026-11-15T09:49:34.820780Z 0 [Note] [MY-000000] [WSREP-SST] xtrabackup_ist received from donor: Running IST\n
2026-11-15T09:49:34.820809Z 0 [Note] [MY-000000] [WSREP-SST] Running post-processing...........\n
2026-11-15T09:49:34.823184Z 0 [Note] [MY-000000] [WSREP-SST] Skipping mysql_upgrade (ist)\n
2026-11-15T09:49:34.823310Z 0 [Note] [MY-000000] [WSREP-SST] ...........post-processing done\n
2026-11-15T09:49:34.824151Z 0 [Note] [MY-000000] [WSREP-SST] Galera co-ords from recovery: ec51ce68-e0d6-11f1-808a-03de7cc64daa:14709\n
```

To ensure we trigger an SST this time we will first schedule the underlying PVC for deletion, as the PVC is in use the ```--wait=false``` ensures the command completes, the PVC is not deleted yet but will be when the pod releases it.

```shell
kubectl delete pvc datadir-cluster1-pxc-2 --wait=false
```

Then delete the pod again. 

```shell
kubectl delete po cluster1-pxc-2
```

This time the logs will show an IST wasn't possible and a full SST was triggered from another node.

```shell
2026-11-15T10:07:29.878548Z 2 [Note] [MY-000000] [WSREP] Prepared SST request: xtrabackup-v2|10.244.1.10:4444/xtrabackup_sst//1\n
2026-11-15T10:07:29.878586Z 2 [Note] [MY-000000] [Galera] Check if state gap can be serviced using IST\n
2026-11-15T10:07:29.878595Z 2 [Note] [MY-000000] [Galera] Local UUID: 00000000-0000-0000-0000-000000000000 != Group UUID: ec51ce68-e0d6-11f1-808a-03de7cc64daa\n
2026-11-15T10:07:29.878599Z 2 [Note] [MY-000000] [Galera] ####### IST uuid:00000000-0000-0000-0000-000000000000 f: 0, l: 35746, STRv: 3\n
2026-11-15T10:07:29.878672Z 2 [Note] [MY-000000] [Galera] IST receiver addr using ssl://10.244.1.10:4568\n
2026-11-15T10:07:29.878693Z 2 [Note] [MY-000000] [Galera] IST receiver using ssl\n
2026-11-15T10:07:29.878780Z 2 [Note] [MY-000000] [Galera] Prepared IST receiver for 0-35746, listening at: ssl://10.244.1.10:4568\n
2026-11-15T10:07:29.879207Z 0 [Note] [MY-000000] [Galera] Member 1.0 (cluster1-pxc-2) requested state transfer from 'cluster1-pxc-1,'. Selected 0.0 (cluster1-pxc-1)(SYNCED) as donor.\n
2026-11-15T10:07:29.879288Z 0 [Note] [MY-000000] [Galera] Shifting PRIMARY -> JOINER (TO: 35805)\n
2026-11-15T10:07:29.879332Z 2 [Note] [MY-000000] [Galera] Requesting state transfer: success, donor: 0\n
2026-11-15T10:07:29.879380Z 2 [Note] [MY-000000] [Galera] Resetting GCache seqno map due to different histories.\n
2026-11-15T10:07:29.879422Z 2 [Note] [MY-000000] [Galera] GCache history reset: 00000000-0000-0000-0000-000000000000:0 -> ec51ce68-e0d6-11f1-808a-03de7cc64daa:35746\n
2026-11-15T10:07:30.173225Z 0 [Note] [MY-000000] [WSREP-SST]    joiner: => Rate:[ 325 B/s] Avg:[ 325 B/s] Elapsed:0:00:00  Bytes:  166 B \n
2026-11-15T10:07:30.715773Z 0 [Note] [MY-000000] [WSREP-SST] Using PXB option --lock-ddl=REDUCED for SST\n
2026-11-15T10:07:30.734386Z 0 [Note] [MY-000000] [WSREP-SST] Proceeding with SST.........\n
2026-11-15T10:07:30.745528Z 0 [Note] [MY-000000] [WSREP-SST] ............Waiting for SST streaming to complete!\n
2026-11-15T10:07:45.945092Z 0 [Note] [MY-000000] [WSREP-SST]    joiner: => Rate:[0.00 B/s] Avg:[0.00 B/s] Elapsed:0:00:10  Bytes: 0.00 B \r   joiner: => Rate:[12.4MiB/s] Avg:[12.4MiB/s] Elapsed:0:00:15  Bytes:  188MiB \n
2026-11-15T10:07:45.949894Z 0 [Note] [MY-000000] [WSREP-SST] Decompressing the backup at /var/lib/mysql//sst-xb-tmpdir\n
2026-11-15T10:07:45.950708Z 0 [Note] [MY-000000] [Galera] 0.0 (cluster1-pxc-1): State transfer to 1.0 (cluster1-pxc-2) complete.\n
2026-11-15T10:07:45.951436Z 0 [Note] [MY-000000] [Galera] Member 0.0 (cluster1-pxc-1) synced with group.\n
2026-11-15T10:07:46.080311Z 0 [Note] [MY-000000] [WSREP-SST] Preparing the backup at /var/lib/mysql//sst-xb-tmpdir\n
2026-11-15T10:07:49.343928Z 0 [Note] [MY-000000] [WSREP-SST] Moving the backup to /var/lib/mysql/\n
2026-11-15T10:07:49.456464Z 0 [Note] [MY-000000] [WSREP-SST] Running post-processing...........\n
2026-11-15T10:07:49.458896Z 0 [Note] [MY-000000] [WSREP-SST] Skipping mysql_upgrade (sst): local version (8.4.8) == donor version (8.4.8)\n
2026-11-15T10:07:49.482932Z 0 [Note] [MY-000000] [WSREP-SST] Waiting for server instance to start.....  This may take some time\n
```

Once the pod is back, `wsrep_cluster_size` should return to 3.

## Tidy up

Drop the kind cluster

```shell
kind delete cluster --name percona-pxc
```
