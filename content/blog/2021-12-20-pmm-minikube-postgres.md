---
title: "PMM development and testing with help of minikube"
date: "2021-12-20T00:00:00+00:00"
tags: ['PMM', 'PostgreSQL', 'PG', 'pg_stat_monitor', 'minikube', 'podman']
authors:
  - denys_kondratenko
images:
  - superhero.png
slug: pmm-minikube-postgres
---

## Why
Some time ago I needed to test PG14 with the new `pg_stat_monitor` version that wasn't released. I decided to log my journey so I would spend less effort next time to replicate it.

I do use podman and run PMM with its help but I also like to hack PMM DBaaS features and think that k8s and minikube are perfect and better scalable solutions for the different development environments and especially for the number of clusters and DBs.
If I need just PMM I would run it with podman, but while I am already hacking around DBaaS, I would like to use the same tool for my other development activities.

So my goal is to deploy PMM on minikube, deploy PG14 there with new `pg_stat_monitor` and check that PMM has support of new fields and features in [QAN](https://www.percona.com/doc/percona-monitoring-and-management/2.x/using/query-analytics.html).

## `minikube`

I use Linux and in the examples bellow I run Fedora 35.

First of all you would need minikube - [install it](https://minikube.sigs.k8s.io/docs/start/).

I had a clean system and `podman` and `buildah` installed. When you first start a minikube with `minikube start` it searches for available drivers and tries to deploy kubernetes on top of it. In my case it found podman and provided me with instruction that I needed to follow to get minikube correctly use podman driver.

After setting everything up I was ready to go:
```sh
$ minikube start
😄  minikube v1.24.0 on Fedora 35
✨  Using the podman driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing podman container for "minikube" ...
🐳  Preparing Kubernetes v1.22.3 on Docker 20.10.8 ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

OK, that was easy.

```sh
$ minikube kubectl -- get nodes
    > kubectl.sha256: 64 B / 64 B [--------------------------] 100.00% ? p/s 0s
    > kubectl: 44.73 MiB / 44.73 MiB [-------------] 100.00% 36.08 MiB p/s 1.4s
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   28d   v1.22.3
```

Minikube has it's own kubectl in case you don't have one installed. If you do it would configure it to use the correct kubernetes config to access k8s it has deployed.

I had some [issue](https://github.com/kubernetes/minikube/issues/12569#issuecomment-932732865) while deploying on my btrfs root file system, and I could workaround it starting it with:
```sh
$ minikube start --feature-gates="LocalStorageCapacityIsolation=false"
```

## PMM in k8s

PMM currently doesn't have native k8s support as the container has root privileges and is tightly integrated with different components.

But it is fine for running in staging and testing environments.

To deploy PMM there are 2 ways:
1. hard one with persistent storage
2. easy one with ephemeral storage

The hard one is longer and could break anytime. The option #1 is used in [this blog](https://www.percona.com/blog/2021/05/19/percona-monitoring-and-management-dbaas-overview-and-technical-details/) post and you could use [this yaml](https://github.com/percona-platform/dbaas-controller/blob/main/deploy/pmm-server-minikube.yaml) file to see how to do it.

I need to quickly run testa and don't care if data disappears (ephemeral storage) neither for PMM nor for DB. So I wrote this quick deployment `pmm-k8s-ephemeral.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: pmm
spec:
  selector:
    app: pmm
  type: NodePort
  ports:
  - port: 80
    name: web
    targetPort: 80
    nodePort: 30080
  - port: 443
    name: api
    targetPort: 443
    nodePort: 30443

---

apiVersion: v1
kind: Service
metadata:
    name: pmm-net
spec:
  selector:
     app.kubernetes.io/part-of: pmm
  ports:
    - name: pmm-server
      port: 443
    - name: vm-agent
      port: 8428

---

apiVersion: v1
kind: ConfigMap
metadata:
  name: pmm-conf
  labels:
    app: pmm
    app.kubernetes.io/part-of: pmm
data:
  PMM_AGENT_SERVER_PASSWORD: admin
  PMM_AGENT_SERVER_USERNAME: admin
  PMM_AGENT_SERVER_ADDRESS: pmm-net:443
  PMM_AGENT_SETUP: 'true'
  PMM_AGENT_DEBUG: 'true'
  PMM_AGENT_TRACE: 'true'
  PMM_AGENT_CONFIG_FILE: "/usr/local/percona/pmm2/config/pmm-agent.yaml"
  PMM_AGENT_SETUP_METRICS_MODE: "push"
  PMM_AGENT_SERVER_INSECURE_TLS: "true"

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: pmm-deployment
  labels:
    app: pmm
    app.kubernetes.io/part-of: pmm
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: pmm
  template:
    metadata:
      labels:
        app: pmm
        app.kubernetes.io/part-of: pmm
    spec:
      containers:
      - name: pmm-server
        image: docker.io/perconalab/pmm-server:2
        ports:
        - containerPort: 80
          name: web
        - containerPort: 443
          name: api
        - containerPort: 8428
          name: vm
```

What I have done there:
* Service (pmm) that will expose PMM to the local machine so I can reach PMM in the browser
* Service (pmm-net) for tools and PMM client to contact PMM server and send monitoring and analytics
* ConfigMap (pmm-conf) with parameters for the PMM client
* Deployment that runs PMM container and exposes couple of ports for the Services

Let's deploy it:

```sh
$ minikube kubectl -- apply -f pmm-k8s-ephemeral.yaml
service/pmm created
service/pmm-net created
configmap/pmm-conf created
deployment.apps/pmm-deployment created
```

Nice, is it running?

```sh
$ minikube kubectl -- get pods
NAME                             READY   STATUS    RESTARTS   AGE
pmm-deployment-d785ff89f-rz8zp   1/1     Running   0          61s
```

Lets open PMM in the browser:
```ssh
$ minikube kubectl -- get pods
NAME                             READY   STATUS    RESTARTS   AGE
pmm-deployment-d785ff89f-rz8zp   1/1     Running   0          61s

$ minikube service pmm
|-----------|------|-------------|---------------------------|
| NAMESPACE | NAME | TARGET PORT |            URL            |
|-----------|------|-------------|---------------------------|
| default   | pmm  | web/80      | http://192.168.49.2:30080 |
|           |      | api/443     | http://192.168.49.2:30443 |
|-----------|------|-------------|---------------------------|
🎉  Opening service default/pmm in default browser...
Opening in existing browser session.
```

And it will open a couple of links, if you would like to use one on `30443` port - add `https://` before the IP. The user/pass is `admin/admin`.

OK, now I see the PMM and it is working.

Lets connect some clients to it.

## PG14 with pg_stat_monitor

For my task I need to take vanila PG14 and add `pg_stat_monitor` to it, as it doesn't come as a part of standard container distribution. Percona has [Percona Distribution for PostgreSQL](https://www.percona.com/software/postgresql-distribution) which comes with `pg_stat_monitor` installed, but it wouldn't work for me as I need unreleased version and it also wasn't available with PG14.

First I need to build [pg_stat_monitor](https://github.com/percona/pg_stat_monitor). There are [instructions](https://github.com/percona/pg_stat_monitor#building-from-source) so lets do it but I would use `toolbox` to not pollute my host system:
```sh
$ git clone https://github.com/percona/pg_stat_monitor.git
$ cd pg_stat_monitor
$ toolbox create pg_mon
Creating container pg_mon: | Created container: pg_mon
Enter with: toolbox enter pg_mon
[pg_stat_monitor]$ toolbox enter pg_mon
⬢[pg_stat_monitor]$ sudo dnf module reset postgresql -y
⬢[pg_stat_monitor]$ sudo dnf module enable postgresql:14
⬢[pg_stat_monitor]$ sudo dnf install make gcc redhat-rpm-config postgresql-server-devel
⬢[pg_stat_monitor]$ make USE_PGXS=1
...
⬢[pg_stat_monitor]$ ls -la ?(*.sql|*.so)
-rw-rw-r--. 1 user user   6904 Dec 17 22:23 pg_stat_monitor--1.0.sql
-rwxr-xr-x. 1 user user 253328 Dec 17 22:23 pg_stat_monitor.so
⬢[pg_stat_monitor]$ exit
```

OK, so I have a new `pg_stat_monitor` that I built from the `main` branch.

Now I need to embed it into the standard PG14 container:

```sh
$ container=$(buildah from postgres)
$ buildah copy $container ./pg_stat_monitor.so /usr/lib/postgresql/14/lib/
cea14ac2e80f79232619557c6e2a7fb2f2379dc5216a67b775905819f5f5c730
$ buildah copy $container ./pg_stat_monitor.bc /usr/lib/postgresql/14/lib/bitcode/
4d24aedb673a86a09883336657f6abaf20327ff21ec7a1885e2018a32a548f57
$ buildah copy $container ./pg_stat_monitor.bc /usr/lib/postgresql/14/lib/bitcode/pg_stat_monitor/
4d24aedb673a86a09883336657f6abaf20327ff21ec7a1885e2018a32a548f57
$ buildah copy $container ./pg_stat_monitor--1.0.sql usr/share/postgresql/14/extension/
ff06a0a8c94bcfe92b8b3616c5791a8e54180a1d9730c6c26c42400741a793dd
$ buildah copy $container ./pg_stat_monitor.control usr/share/postgresql/14/extension/
ec90a547ee46e628ad853c7e4a0afc6aa6ba39677e9adcf04c22bd820dc9aa4b
$ buildah run $container -- sh -c "echo shared_preload_libraries = \'pg_stat_monitor\' >> /usr/share/postgresql/postgresql.conf.sample"
$ buildah commit $container postgresql-pg-stat-monitor-test
Getting image source signatures
Copying blob 9321ff862abb skipped: already exists
Copying blob 1fd9b284a3ce skipped: already exists
Copying blob e408a39a0b68 skipped: already exists
Copying blob 8083ac6c7a07 skipped: already exists
Copying blob 16bdcb6f65a3 skipped: already exists
Copying blob 470529a805d0 skipped: already exists
Copying blob 51e951dc5705 skipped: already exists
Copying blob 27051a077cdc skipped: already exists
Copying blob dd44883ded8b skipped: already exists
Copying blob 1b8d5d101e2a skipped: already exists
Copying blob 806c98b52cc8 skipped: already exists
Copying blob 1fb1b8252a25 skipped: already exists
Copying blob 20371ceade59 skipped: already exists
Copying blob 94a669b6abd4 done
Copying config 381f3d202a done
Writing manifest to image destination
Storing signatures
381f3d202aca494c2caa663dfa1f95934c3a0bb64e0efceb0388ff6f3854be08
$ podman save --format docker-archive -o postgresql-pg-stat-monitor-test.tar localhost/postgresql-pg-stat-monitor-test
Copying blob 9321ff862abb done
Copying blob 1fd9b284a3ce done
Copying blob e408a39a0b68 done
Copying blob 8083ac6c7a07 done
Copying blob 16bdcb6f65a3 done
Copying blob 470529a805d0 done
Copying blob 51e951dc5705 done
Copying blob 27051a077cdc done
Copying blob dd44883ded8b done
Copying blob 1b8d5d101e2a done
Copying blob 806c98b52cc8 done
Copying blob 1fb1b8252a25 done
Copying blob 20371ceade59 done
Copying blob 94a669b6abd4 done
Copying config 381f3d202a done
Writing manifest to image destination
Storing signatures
$ minikube image load ./postgresql-pg-stat-monitor-test.tar
$ minikube image ls
...
docker.io/localhost/postgresql-pg-stat-monitor-test:latest
...
```

What I have done there:
* created new image from `docker.io/library/postgres`
* copied all needed files from locally built `pg_stat_monitor` to the new image
* enabled `pg_stat_monitor` in the config
* commited changes to the image
* saved image to the archive
* loaded image from the archive to the minikube cache (if anyone know how to load local image directly - please let me know)

So now I have a PG14 image with the new `pg_stat+monitor` that I would like to test as the image in my k8s cluster.

Lets create a PG14 deployment, shall we? Here is `postgresql_eph.yaml` file:


```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-configuration
  labels:
    app: postgres
data:
  POSTGRES_DB: admin
  POSTGRES_USER: admin
  POSTGRES_PASSWORD: admin

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
  labels:
    app: postgres
spec:
  serviceName: "postgres"
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: docker.io/localhost/postgresql-pg-stat-monitor-test:latest
        imagePullPolicy: Never
        envFrom:
        - configMapRef:
            name: postgres-configuration
      - name: pmm-agent
        image: docker.io/perconalab/pmm-client:2
        envFrom:
        - configMapRef:
            name: pmm-conf
        ports:
        - containerPort: 8428
          name: vm
```

Notice here `imagePullPolicy: Never` and `image: docker.io/localhost/postgresql-pg-stat-monitor-test:latest`, I am instructing k8s to not pull the image but only use one in cache and it is the image name that I have uploaded earlier.

I also added a PMM client sidecar container to monitor and query PG14. Also notice that PG14 is not exposed outside of the pod, I just don't need it. The load I need I could produce just from inside of the pod. So if you use this example for something else - expose the port for PG14.

Lets deploy it:
```sh
$ minikube kubectl -- apply -f ./postgresql_eph.yml
$ minikube kubectl -- get pods
NAME                             READY   STATUS    RESTARTS      AGE
pmm-deployment-d785ff89f-sgr6s   1/1     Running   0             11m
postgres-statefulset-0           2/2     Running   0             11m
```

Now I have PMM and PG14 running, let's connect them.

## PMM QAN with `pg_stat_monitor`

First of all I need to enable `pg_stat_monitor` extension for PG14:
```sh
$ minikube kubectl -- exec --stdin --tty postgres-statefulset-0 --container postgres -- /bin/bash
root@postgres-statefulset-0:/# psql -U admin
psql (14.1 (Debian 14.1-1.pgdg110+1))
Type "help" for help.

admin=# CREATE EXTENSION pg_stat_monitor;
CREATE EXTENSION
admin=# SELECT pg_stat_monitor_version();
 pg_stat_monitor_version
-------------------------
 1.0.0-rc.1
(1 row)
admin-# \q
root@postgres-statefulset-0:/# exit
```

Now I need connect PG14 to the PMM client so it would start monitor it and scrape query analytics:
```sh
$ minikube kubectl -- exec --stdin --tty postgres-statefulset-0 --container pmm-agent -- /bin/bash
bash-4.2$ pmm-admin list
Service type        Service name        Address and port        Service ID

Agent type           Status           Metrics Mode        Agent ID                                              Service ID
pmm_agent            Connected                            /agent_id/318838db-bd57-44d4-b7a7-3786ec2492f0
node_exporter        Running          push                /agent_id/58ef7f93-cf83-4d5b-bd2b-be34b7fc5ecf
vmagent              Running          push                /agent_id/d29685ba-61e0-429f-84f5-4f85505242dc

bash-4.2$ pmm-admin add postgresql --username=admin --password=admin --query-source=pgstatmonitor
PostgreSQL Service added.
Service ID  : /service_id/736b6453-23d2-45f1-b30e-2bacccca3644
Service name: postgres-statefulset-0-postgresql
```

Now if I go to the PMM UI, I could see the QAN data for the postgres, or debug why I don't see it :)

## Conclusion

minikube is a very nice tool for developers and testers to bring up complex deployments, play, debug and test.

k8s yaml [manifests](https://kubernetes.io/docs/reference/glossary/?fundamental=true#term-manifest) are really good standardized and have tons of configurable options as ConfigMaps, Secrets and etc. Which you could have different in testing, staging and production but sharing same operators, deployments and pods. It also has a clear, documented, open source API and code.

Also podman has `play kube` feature that allows the reuse of the same manifest files to create pods with podman. It is not fully featured, but potential and ideas are very powerful.

Check out [Kubernetes Podcast](https://kubernetespodcast.com/episode/164-podman/) to learn more about podman.
