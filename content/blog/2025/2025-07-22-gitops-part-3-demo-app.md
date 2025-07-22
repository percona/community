---
title: "GitOps Journey: Part 3 – Deploying a Load Generator and Connecting to PostgreSQL"
date: "2025-07-21T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'GitOps', 'ArgoCD']
categories: ['PostgreSQL']
authors:
  - daniil_bazhenov
images:
  - blog/2025/07/gitops-part-3.jpg
---

We’ll deploy a demo application into the Kubernetes cluster using ArgoCD to simulate load on the PostgreSQL cluster.

This is a series of articles, in previous parts we:
1. [Part 1]() - Prepared the environment and installed ArgoCD and GitHub repository.
2. [Part 2]() - Installed Percona Operator for Postgres and created a Postgres cluster.

The application is a custom Go-based service that generates traffic for PostgreSQL, MongoDB, or MySQL.  

It uses a dataset of GitHub repositories and pull requests, and mimics real-world operations like fetching, creating, updating, and deleting records.  
Load intensity is configurable through a browser-based control panel.

We’ll install it using Helm, tracked and deployed via ArgoCD.

Reference repository: [github-stat](https://github.com/dbazhenov/github-stat)

## Create the ArgoCD Application Manifest

Create a file named `argocd-demo-app.yaml` in the `apps/` directory.

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/dbazhenov/github-stat
    targetRevision: main
    path: k8s/helm
  destination:
    server: https://kubernetes.default.svc
    namespace: demo-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

This will install the Helm chart from  
`https://github.com/dbazhenov/github-stat/tree/main/k8s/helm`

By default, the service is configured as `LoadBalancer`, making it accessible from the internet.

To switch to `NodePort` (if needed), override the Helm value:

```
source:
  helm:
    parameters:
      - name: controlPanelService.type
        value: NodePort
```

We’ll keep default settings in this example.

## Push the Application Manifest to GitHub

Track and commit your changes:

```
git status
```
```
git add .
```
```
git commit -m "Installing Demo Application in ArgoCD by HELM"
``` 
```
git push origin main 
```
Expected Git output:

```
➜  percona-argocd-pg-coroot git:(main) git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    apps/argocd-demo-app.yaml

nothing added to commit but untracked files present (use "git add" to track)
➜  percona-argocd-pg-coroot git:(main) ✗ git add .
➜  percona-argocd-pg-coroot git:(main) ✗ git commit -m "Installing Demo Application in ArgoCD by HELM"
[main 03ce175] Installing Demo Application in ArgoCD by HELM
 1 file changed, 20 insertions(+)
 create mode 100644 apps/argocd-demo-app.yaml
➜  percona-argocd-pg-coroot git:(main) git push origin main
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 10 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 686 bytes | 686.00 KiB/s, done.
Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:dbazhenov/percona-argocd-pg-coroot.git
   6b2dc98..03ce175  main -> main
➜  percona-argocd-pg-coroot git:(main)
```


## Apply the ArgoCD Application

Deploy the app via:

```
kubectl apply -f apps/argocd-demo-app.yaml -n argocd
```

ArgoCD will install the app and has started tracking the app's HELM chart


## Validate the Deployment

Confirm the app status in ArgoCD UI:

![GitOps - Percona Operator for Postgres and PG Cluster](blog/2025/07/gitops-github-argo-demo-app.png)

Check running pods:

```
kubectl get pods -n demo-app
```

Expected pods:
```
➜  percona-argocd-pg-coroot git:(main) kubectl get pods -n demo-app
NAME                               READY   STATUS    RESTARTS   AGE
demo-app-dataset-6d886f67-j648w    1/1     Running   0          2m52s
demo-app-load-577cff97c9-d8j99     1/1     Running   0          2m52s
demo-app-valkey-74989c9bf7-gjp4x   1/1     Running   0          2m52s
demo-app-web-5b98d4c65c-xmkq9      1/1     Running   0          2m52s
```

* demo-app-dataset - loads dataset  
* demo-app-load - generates traffic  
* demo-app-valkey - Redis-compatible DB backend  
* demo-app-web - UI dashboard


## Open the Application Dashboard

Retrieve the external IP:
```
kubectl get svc -n demo-app
```

Find the `EXTERNAL-IP` of `demo-app-web-service`.

Sample output:

```
➜  percona-argocd-pg-coroot git:(main) kubectl get svc -n demo-app
NAME                      TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
demo-app-valkey-service   ClusterIP      34.118.235.203   <none>          6379/TCP       4m59s
demo-app-web-service      LoadBalancer   34.118.232.144   34.28.221.107   80:31308/TCP   4m59s
```

Access the app in your browser:

![GitOps - ArgoCD Demo App UI](blog/2025/07/gitops-demo-app-ui.png)

Navigate to the **Settings** tab to configure a PostgreSQL connection.


## PostgreSQL Credentials Setup

Percona Operator has already ([Application and system users](https://docs.percona.com/percona-operator-for-postgresql/2.0/users.html)):

- Created schema and database `cluster1`
- Created user `cluster1`
- Stored credentials in `cluster1-pguser-cluster1` secret

Extract the password:

```
kubectl get secret cluster1-pguser-cluster1 -n postgres-operator --template='{{.data.password | base64decode}}{{"\n"}}'
```

Let's connect to the database from the Demo application using the given user and cluster1-pgbouncer.postgres-operator.svc host 

In the Connection String field enter

```
user=cluster1 password='[PASSWORD]' dbname=cluster1 host=cluster1-pgbouncer.postgres-operator.svc port=5432
```

![GitOps - ArgoCD Demo App UI - Connect](blog/2025/07/gitops-demo-app-ui-connect.png)

The connection has been successfully created, this is good. 

To start generating the load, we need to import the Dataset using the Import Dataset button.

## Dataset Import Error: Create Schema Denied

During import, the app tries to create a schema.  
By default, pgBouncer limits user privileges, preventing this action.

Percona [documentation](https://docs.percona.com/percona-operator-for-postgresql/2.0/users.html#superuser-and-pgbouncer) suggests enabling `proxy.pgBouncer.exposeSuperusers` and creating a privileged user.

We’ll handle this via GitOps. It seems cool that we'll be doing this with tracking in Git, as these are important settings and we shouldn't forget about them and turn them off in the future.

## Define a New PostgreSQL User

We will make changes to postgres/cr.yaml that will add a new user and also enable the proxy.pgBouncer.exposeSuperusers option.

In the postgres/cr.yaml file I found the users section, uncommented and added my user data.

In `postgres/cr.yaml`, add:

```
  users:
    - name: daniil
      databases:
        - demo
      options: "SUPERUSER"
      password:
        type: ASCII
      secretName: "daniil-credentials"
```

Note: In production, use scoped permissions like `"LOGIN CREATE CREATEDB"` rather than `SUPERUSER`.

I also found the proxy.pgBouncer.exposeSuperusers setting and set it to true

Update pgBouncer config:

```
  proxy:
    pgBouncer:
      replicas: 3
      image: docker.io/percona/percona-pgbouncer:1.24.1
      exposeSuperusers: true
```

Commit and push:

```
git status
```
```
git add .
```
```
git commit -m "Postgres cluster: Creating a new user and pgBouncer.exposeSuperusers"
```
```
git push origin main
```

After a couple of minutes, ArgoCD will synchronize the changes and Percona Operator will create the user and change the configuration.

![GitOps - ArgoCD Demo App UI](blog/2025/07/gitops-argocd-pg-new-user.png)

## Connect With the New User

Get the password:

```
kubectl get secret daniil-credentials -n postgres-operator --template='{{.data.password | base64decode}}{{"\n"}}'
```

Let's replace Connection String in Demo application, I got the following string

```
user=daniil password='iKj:e[wT3*g]OF5+f' dbname=dataset host=cluster1-pgbouncer.postgres-operator.svc port=5432
```

![GitOps - ArgoCD Demo App UI - Connection](blog/2025/07/gitops-argocs-demo-app-new-user.png)

Click the “Import Dataset” button and wait a few minutes until the import is in Done status in the Dataset tab.

![GitOps - ArgoCD Demo App UI - Connection](blog/2025/07/gitops-argocs-demo-app-dataset.png)

## Enable Load Generation

Activate the load generator:

- Toggle **Enable Load** in the connection settings
- Click **Update Connection**

![GitOps - ArgoCD Demo App UI - Enable Load](blog/2025/07/gitops-argocd-demo-app-enable-load.png)

Open the **Load Generator Control Panel** and adjust sliders and toggles as needed:

![GitOps - ArgoCD Demo App UI - Load Generator](blog/2025/07/gitops-argocd-demo-app-panel.png)

## Conclusion

In this part, we:

- Deployed a demo application via Helm in ArgoCD
- Connected it to our PostgreSQL cluster
- Managed PostgreSQL users and access via GitHub and GitOps
- Imported a dataset and activated the traffic generator through the web UI

In Part 4, we’ll deploy **Coroot** for observability and profiling.  
It’s an impressive tool for diagnosing behavior across services in the Kubernetes cluster.
