---
title: "GitOps Journey: Part 2 – Deploying PostgreSQL with GitOps and ArgoCD"
date: "2025-07-21T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'GitOps', 'ArgoCD']
categories: ['PostgreSQL']
authors:
  - daniil_bazhenov
images:
  - blog/2025/07/gitops-part-2.jpg
---

We’re now ready to deploy **PostgreSQL 17** using GitOps — with ArgoCD, GitHub, and the Percona Operator for PostgreSQL.

If you're a DBA, developer, DevOps engineer, or engineering manager, this part focuses on GitOps in action: deploying and managing a real database cluster using declarative infrastructure.

In [Part 1](/blog/2025-07-21-gitops-part-1-argocd-github), we set up the Kubernetes environment and installed ArgoCD.  
Now it’s time to define and launch the PostgreSQL cluster — fully versioned and synced through Git.

We’ll follow the official [Percona Operator documentation](https://docs.percona.com/percona-operator-for-postgresql/2.0/gke.html) and reference the [GitHub repository](https://github.com/percona/percona-postgresql-operator) to build out a production-grade setup.


## Preparing the Environment

There are multiple ways to install the Percona Operator and create a PostgreSQL cluster.  
We’ll use the simplest and most GitOps-friendly approach:

1. Deploy the operator using `deploy/bundle.yaml`

2. Deploy the cluster using `deploy/cr.yaml`

Source files:
- `https://github.com/percona/percona-postgresql-operator/blob/main/deploy/bundle.yaml`
- `https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml`

## Project Structure

Repository structure can vary depending on your services and infrastructure scale.  
For this series, we'll use:

- `postgres/` → Contains all manifests related to PostgreSQL: the operator, clusters, backups
- `apps/` → Contains ArgoCD application manifests that track changes in the repository

You’re free to choose a different structure. Just ensure all paths are correctly referenced in ArgoCD.

## Creating the Postgres Directory and Saving Manifests

You can manually download the files from GitHub or automate it via CLI:

```
mkdir postgres
```
```
curl -o postgres/bundle.yaml https://raw.githubusercontent.com/percona/percona-postgresql-operator/v2.7.0/deploy/bundle.yaml
```
```
curl -o postgres/cr.yaml https://raw.githubusercontent.com/percona/percona-postgresql-operator/v2.7.0/deploy/cr.yaml
```

You can also separately clone [the operator repository](https://github.com/percona/percona-postgresql-operator) and grab the necessary files from there.


## Creating the ArgoCD Application Manifest

This ArgoCD application will track the `postgres/` directory and automatically sync changes from GitHub.

Create the file: `apps/argocd-postgres.yaml`

Content:

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: postgres
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/dbazhenov/percona-argocd-pg-coroot.git
    targetRevision: main
    path: postgres 
  destination:
    server: https://kubernetes.default.svc
    namespace: postgres-operator
  syncPolicy:
    automated:
      prune: true 
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true 
```

You can also create this app manually via the ArgoCD UI or CLI, but using a manifest aligns better with GitOps principles.

Double-check your:
- `repoURL` → matches your GitHub repository
- `path` → corresponds to your PostgreSQL manifest directory
- `namespace` → targets the correct namespace for operator and cluster


## Managing ArgoCD Sync Order with Waves

ArgoCD applies manifests based on `sync-wave` annotations.

- The operator (`bundle.yaml`) should be applied first
- The cluster (`cr.yaml`) comes second

Add these annotations:

**In `bundle.yaml`:**

```
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

**In `cr.yaml`:**

```
metadata:
  name: cluster1
  annotations:
    argocd.argoproj.io/sync-wave: "5"
```
This ensures a stable deployment sequence. 

Later in the series (e.g. when installing Coroot), we’ll use a more advanced method: defining sync order via `kustomization.yaml`.


## Reviewing Cluster Configuration

Before applying the manifests, review and adjust your cluster settings in `cr.yaml`.

Key defaults:
- `name: cluster1` → Cluster name
- `postgresVersion: 17` → PostgreSQL version

To keep the cluster lightweight and test horizontal scaling later, reduce replicas to 1:

```
instances:  
  - name: instance1  
    replicas: 1
```
```
proxy:  
  pgBouncer:  
    replicas: 1
```

You can also configure resource limits, disk sizes, backups, and users in this file.

## Publishing the Configuration to GitHub

Verify your repo status:

```
git status
```

Add files:

```
git add .
```

Review staged files:

```
git status
```

Expected result:
```
➜  percona-argocd-pg-coroot git:(main) ✗ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    apps/
    postgres/

nothing added to commit but untracked files present (use "git add" to track)
➜  percona-argocd-pg-coroot git:(main) ✗ git add .
➜  percona-argocd-pg-coroot git:(main) ✗ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    new file:   apps/argocd-postgres.yaml
    new file:   postgres/bundle.yaml
    new file:   postgres/cr.yaml
```

Commit:

```
git commit -m "Initial configuration of a Postgres cluster using Percona Operator for Postgres and ArgoCD"
```

Push to GitHub:

```
git push origin main
```

Verify files are published correctly in the repository.

![GitOps - Percona Operator for Postgres and PG Cluster](blog/2025/07/gitops-github-pg-init.png)


## Applying the ArgoCD App Manifest

To initiate the deployment, apply the previously created manifest:

```
kubectl apply -f apps/argocd-postgres.yaml -n argocd
```

After a minute or two, the ArgoCD dashboard should display the synced PostgreSQL application and the deployed cluster.

![GitOps - ArgoCD app - Postgres](blog/2025/07/gitops-argocd-pg-app-sync.png)

![GitOps - ArgoCD app - Postgres - map](blog/2025/07/gitops-argocd-pg-app-map.png)

## Verifying Cluster Status

Check the running pods:

```
kubectl get pods -n postgres-operator
```

Expected results:
- One PostgreSQL instance pod
- One pgBouncer pod

```
➜  percona-argocd-pg-coroot git:(main) kubectl get pods -n postgres-operator
NAME                                           READY   STATUS      RESTARTS   AGE
cluster1-backup-5g98-5b29w                     0/1     Completed   0          27m
cluster1-instance1-22vd-0                      4/4     Running     0          28m
cluster1-pgbouncer-649b7cf845-fgs9l            2/2     Running     0          28m
cluster1-repo-host-0                           2/2     Running     0          28m
percona-postgresql-operator-79f75d5f76-xjndr   1/1     Running     0          29m
```

## Scaling the Cluster via GitOps

Let’s test the GitOps model by updating the cluster configuration to increase replicas to 3.

Edit `postgres/cr.yaml`:

```
  instances:  
  - name: instance1  
    replicas: 3
```
```
  proxy:  
    pgBouncer:  
      replicas: 3
```
Save the changes and push them:

```
git status
```
```
git add .  
```
```
git commit -m "Postgres cluster: Horizontal scaling from 1 replica to 3" 
```
``` 
git push origin main
```

ArgoCD will automatically detect and apply this update.

Expected results:
```
➜  percona-argocd-pg-coroot git:(main) git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
    modified:   postgres/cr.yaml

no changes added to commit (use "git add" and/or "git commit -a")
➜  percona-argocd-pg-coroot git:(main) ✗ git add .
➜  percona-argocd-pg-coroot git:(main) ✗ git commit -m "Postgres cluster: Horizontal scaling from 1 replica to 3"
[main 6b2dc98] Postgres cluster: Horizontal scaling from 1 replica to 3
 1 file changed, 2 insertions(+), 2 deletions(-)
➜  percona-argocd-pg-coroot git:(main) git push origin main
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 10 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 435 bytes | 435.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To github.com:dbazhenov/percona-argocd-pg-coroot.git
   81ae9e8..6b2dc98  main -> main
➜  percona-argocd-pg-coroot git:(main)
```

Expected results on GitHub Repo:

![GitOps - ArgoCD app - Postgres scale - GitHub](blog/2025/07/gitops-github-scale.png)

## Confirming the Update in ArgoCD

In the ArgoCD UI, you should now see the application synced to the latest commit with the updated replica count.

![GitOps - ArgoCD apps - Postgres scale - Argo](blog/2025/07/gitops-github-scale-argo.png)

Verify pods:

```
kubectl get pods -n postgres-operator
```

Expected result — 3 PostgreSQL pods and 3 pgBouncer pods.

```
➜  percona-argocd-pg-coroot git:(main) kubectl get pods -n postgres-operator
NAME                                           READY   STATUS      RESTARTS   AGE
cluster1-backup-5g98-5b29w                     0/1     Completed   0          38m
cluster1-instance1-22vd-0                      4/4     Running     0          39m
cluster1-instance1-q2r4-0                      4/4     Running     0          3m38s
cluster1-instance1-r4s2-0                      4/4     Running     0          3m39s
cluster1-pgbouncer-649b7cf845-9cppx            2/2     Running     0          3m37s
cluster1-pgbouncer-649b7cf845-fgs9l            2/2     Running     0          39m
cluster1-pgbouncer-649b7cf845-tkf9z            2/2     Running     0          3m36s
cluster1-repo-host-0                           2/2     Running     0          39m
percona-postgresql-operator-79f75d5f76-xjndr   1/1     Running     0          40m
```

## What’s Next

We’ve successfully installed the Percona Operator for PostgreSQL and deployed a cluster using GitHub and ArgoCD.

We also verified GitOps functionality by scaling the cluster through Git-controlled configuration.  
All changes are tracked, versioned, and declarative — a solid foundation for modern infrastructure management.

To continue experimenting:

1. [Connect to the Cluster](https://docs.percona.com/percona-operator-for-postgresql/2.0/connect.html)  
2. [Manage Users](https://docs.percona.com/percona-operator-for-postgresql/2.0/users.html). Note: the default user does not have SUPERUSER privileges. If your app requires creating databases, you’ll need to configure appropriate roles.
3. [Expose the Cluster](https://docs.percona.com/percona-operator-for-postgresql/2.0/expose.html). So you can connect from external clients or apps.

We'll do exactly that in the next part — by deploying a demo application and connecting it to the database using GitOps.

