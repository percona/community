---
title: "GitOps Journey: Part 4 – Observability and Monitoring with Coroot in Kubernetes"
date: "2025-07-23T00:00:00+00:00"
tags: ['PostgreSQL', 'Coroot', 'GitOps', 'ArgoCD']
categories: ['PostgreSQL']
authors:
  - daniil_bazhenov
images:
  - blog/2025/07/gitops-part-4.jpg
---

Our PostgreSQL cluster is running, and the demo app is generating traffic — but we have no visibility into the health of the Kubernetes cluster, services, or applications.

What happens when disk space runs out? What if the database is under heavy load and needs scaling? What if errors are buried in application logs? How busy are the network and storage layers? What’s the actual cost of the infrastructure?

This is where [Coroot](https://coroot.com/) comes in.

Coroot is an open-source observability platform that provides dashboards for profiling, logs, service maps, and resource usage — helping you track system health and diagnose issues quickly.

We’ll deploy it using **Helm via ArgoCD**, continuing with our GitOps workflow.

This is Part 4 in our series. Previously, we:

1. Set up ArgoCD and a GitHub repository for declarative manifests 

2. Installed a PostgreSQL cluster using Percona Operator  

3. Deployed a demo application to simulate traffic and interact with the database

All infrastructure is defined declaratively and deployed from the GitHub repository, following GitOps practices.

So far, we've explored cluster scaling, user management, and dynamic configuration — and now it's time for observability.

We’ll install Coroot by following the [official documentation](https://docs.coroot.com/installation/kubernetes/) for Kubernetes.

Steps ahead:

1. Install the Coroot Operator

2. Install the Coroot Community Edition

Let’s get started.

## Project Structure

We already have a `postgres/` directory for PostgreSQL manifests and an `apps/` directory for ArgoCD applications.

We'll preserve this layout and add a new `coroot/` folder for clarity. You can use a different structure if preferred.

## Create Manifest for Installing the Coroot Operator

The documentation recommends installing via Helm.  
Since we use ArgoCD, we’ll create a manifest that installs via Helm.

Create file: `coroot/operator.yaml`

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: coroot-operator
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://coroot.github.io/helm-charts
    chart: coroot-operator
    targetRevision: 0.4.2
  destination:
    server: https://kubernetes.default.svc
    namespace: coroot
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

Note: I’m using version `0.4.2`, which was current at the time of writing.  
To check available versions, use [this GitHub link](https://github.com/coroot/helm-charts/pkgs/container/charts%2Fcoroot-operator) or Helm CLI:

```
helm repo add coroot https://coroot.github.io/helm-charts
helm repo update
helm search repo coroot-operator --versions
```

## Create Manifest for Installing Coroot Community Edition

Create file: `coroot/coroot.yaml`

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: coroot
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://coroot.github.io/helm-charts
    chart: coroot-ce
    targetRevision: 0.3.1
    helm:
      parameters:
        - name: clickhouse.shards
          value: "2"
        - name: clickhouse.replicas
          value: "2"
        - name: service.type
          value: LoadBalancer
  destination:
    server: https://kubernetes.default.svc
    namespace: coroot
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

This chart creates a minimal Coroot Custom Resource.  
I've added `service.type: LoadBalancer` to expose a public IP.

If you don’t use LoadBalancer, you’ll need to forward the Coroot port after installation:

```
kubectl port-forward -n coroot service/coroot-coroot 8080:8080
```

## Create ArgoCD Application Manifest

Since we manage our infrastructure via a GitHub repository, we need an ArgoCD Application that tracks changes in the `coroot/` folder.

Create file: `apps/argocd-coroot.yaml`

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: coroot-sync-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/dbazhenov/percona-argocd-pg-coroot.git
    targetRevision: main
    path: coroot
  destination:
    server: https://kubernetes.default.svc
    namespace: coroot
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

This lightweight app will monitor the folder and apply updates automatically if a change is detected (e.g. chart version bump).

## Define Chart Installation Order

We have two charts: `operator.yaml` and `coroot.yaml`, and the operator must be installed first.

Create `coroot/kustomization.yaml` to specify resource order:

```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - operator.yaml
  - coroot.yaml
```

## Publish Manifests to GitHub

Check which files were changed:

```
git status
```

Add changes:

```
git add .
```

Verify staged files:

```
git status
```
Commit:

```
git commit -m "Installing Coroot Operator and Coroot with ArgoCD"
```

Push:

```
git push origin main
```

## Apply ArgoCD Application

Deploy the ArgoCD app that installs Coroot from our GitHub repository:

```
kubectl apply -f apps/argocd-coroot.yaml -n argocd
```

Validate installation and sync:

![GitOps - ArgoCD and Coroot](blog/2025/07/gitops-argocd-coroot-coroot-sync-app.png)

We now see `coroot`, `coroot-operator`, and `coroot-sync-app` deployed.

## Access Coroot UI

Since we deployed Coroot using LoadBalancer, retrieve its external IP:

```
kubectl get svc -n coroot
```

Open EXTERNAL-IP on port 8080.  
For example: `http://35.202.140.216:8080/`

If you didn’t use LoadBalancer, run port-forward:

```
kubectl port-forward -n coroot service/coroot-coroot 8080:8080
```

Then visit `http://localhost:8080`

You’ll be prompted to set an admin password on first login.

![GitOps - ArgoCD and Coroot](blog/2025/07/gitops-argocd-coroot-welcome.png)

## Exploring Coroot UI

On the home page, we see a list of applications running in the cluster and resource usage.

![GitOps - ArgoCD and Coroot - Home](blog/2025/07/gitops-argocd-coroot-home-dashboard.png)

I increased the load on the PostgreSQL cluster using the Demo App to test observability.

![GitOps - ArgoCD and Coroot - Demo App](blog/2025/07/gitops-argocd-coroot-demo-load.png)

The PostgreSQL cluster dashboard offers several tabs:

- CPU  
- Memory  
- Storage  
- Instances  
- Logs  
- Profiling  
- Tracing

![GitOps - ArgoCD and Coroot - PG Cluster](blog/2025/07/gitops-argocd-coroot-cluster.png)

Coroot displays a visual map of service interactions — showing which app connects to the PostgreSQL cluster.

![GitOps - ArgoCD and Coroot - PG Cluster](blog/2025/07/gitops-argocd-coroot-cluster-map.png)

The **Profiling** tab looks excellent and intuitive. Here’s the Demo App profiling view:

![GitOps - ArgoCD and Coroot - Demo App Profiling](blog/2025/07/gitops-argocd-coroot-demo-profiling.png)

I also triggered an intentional error in the demo app.  
Coroot correctly displayed it in both the home view and the app details page.

![GitOps - ArgoCD and Coroot - Demo App Logs](blog/2025/07/gitops-argocd-coroot-demo-profiling.png)

I especially liked the **Logs** and **Costs** sections in the sidebar — very well implemented.

![GitOps - ArgoCD and Coroot - Demo App Logs](blog/2025/07/gitops-argocd-coroot-cluster-logs.png)

![GitOps - ArgoCD and Coroot - Demo App Costs](blog/2025/07/gitops-argocd-coroot-cluster-costs.png)

## First Incident: Storage Usage in PostgreSQL Turns Yellow

While exploring Coroot and the cluster, I increased the load on the PostgreSQL cluster using the Demo App.

After a short while, I noticed that the Postgres disk was full.

![GitOps - ArgoCD and Coroot - PG Storage](blog/2025/07/gitops-argocd-coroot-cluster-storage.png)

I opened the cluster details and went to the **Storage** tab.

![GitOps - ArgoCD and Coroot - PG Storage Details](blog/2025/07/gitops-argocd-coroot-cluster-storage-details.png)

By default, the `cr.yaml` file allocates just 1Gi of disk space — which is fine for a test setup.

Let’s increase disk size the GitOps way.

## Increase Storage Size

Open the file `postgres/cr.yaml` and locate the section:

```
    dataVolumeClaimSpec:
#      storageClassName: standard
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
```

Change `storage` from `1Gi` to `5Gi`.

Note: Backup volumes (pgBackRest) are also enabled by default and set to `1Gi`.

```
      manual:
        repoName: repo1
        options:
         - --type=full
#        initialDelaySeconds: 120
      repos:
      - name: repo1
        schedules:
          full: "0 0 * * 6"
#          differential: "0 1 * * 1-6"
#          incremental: "0 1 * * 1-6"
        volume:
          volumeClaimSpec:
#            storageClassName: standard
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
```

Increase this storage to `5Gi` as well.

Save changes to `cr.yaml`, then commit and push to the GitHub repository.

ArgoCD will automatically apply the changes. Pure GitOps magic.

Check the result in Coroot — everything looks great. The disk is increased to `5Gi` and the issue is resolved.

![GitOps - ArgoCD and Coroot - PG Storage Details Results](blog/2025/07/gitops-argocd-coroot-cluster-storage-details-result.png)

![GitOps - ArgoCD and Coroot - PG Storage Results](blog/2025/07/gitops-argocd-coroot-cluster-storage-home-result.png)

## Conclusion

We’ve installed and tested a solid monitoring tool, and it really makes a difference.

Across this 4-part series, we walked through the GitOps journey step by step:

1. Created a Kubernetes cluster, installed ArgoCD, and set up a GitHub repository.

2. Deployed a PostgreSQL cluster using Percona Operator for PostgreSQL.

4. Deployed a demo app via ArgoCD using Helm.

5. Installed and tested **Coroot**, an excellent open-source observability tool.

Managed the cluster through GitHub and ArgoCD — scaled replicas, created users, resized volumes, configured access, and more.

Thank you for reading — I hope this series was helpful.

The project files are available in my repository https://github.com/dbazhenov/percona-argocd-pg-coroot

I’d love to hear your questions, feedback, and suggestions for improvement.

