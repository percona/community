---
title: "Setting Up Your Environment for Kubernetes Operators Using Docker, kubectl, and k3d"
date: "2024-03-04T00:00:00+00:00"
draft: false
tags: ["edith_puclla", "kubernetes", "operators", "k3d", "docker"]
categories: ['Cloud']
authors:
  - edith_puclla
images:
  - blog/2024/03/intro.png
slug: setting-up-your-environment-for-kubernetes-operators-using-docker-kubectl-and-k3d
---

If you are just starting out in the world of Kubernetes operators, like me, preparing the environment for their installation should be something we do with not much difficulty. This blog will quickly guide you in setting the minimal environment.

Kubernetes operators are invaluable for automating complex database operations, tasks that Kubernetes does not handle directly. Operators make it easy for us – they take care of essential tasks like **backups** and **restores**, which are crucial in database management.

If you want an introduction to Kubernetes Operators, I cover it in this 5-minute blog post, [Exploring the Kubernetes Application Lifecycle With Percona](https://www.percona.com/blog/exploring-the-kubernetes-application-lifecycle-with-percona/).

Now that we know why Kubernetes Operators are essential let’s prepare our environment to install some of them. We are going to base this installation on Linux for now.
Prerequisites:
For this, we will need a basic understanding of Kubernetes concepts and some Linux command line skills.
We also need [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) to be able to use K3d at all for containerization. To test, make sure this command runs appropriately:

```bash
docker run hello-world
```

## Installing kubectl

To manage and deploy applications on Kubernetes, we will need **kubectl** tool, which is included in most Kubernetes distributions. If it's not installed, let's do it following the [official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/):

To install the **kubectl** binary with curl on Linux, we need to download the latest release of kubectl using the command:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

The previous binary installs kubectl in /usr/local/bin/kubectl. We need root ownership and specific permissions for secure execution.

```bash
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

To test the installation, we use the following:

```bash
kubectl version --client
```

Or

```bash
kubectl version --client --output=yaml
```

If you receive a response like this, it indicates that you are ready to use `kubectl`.

```bash
Client Version: v1.29.2
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
```

## Installing K3d

k3d is a lightweight tool that simplifies running k3s (Rancher Lab's minimal Kubernetes distribution in Docker), enabling easy creation of single and multi-node k3s clusters for local development.

Install the current latest release of k3d with curl:

```bash
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

To test the installation, you can use the following:

```bash
k3d --help
```

If you see a message similar to this, you are ready to create your k3d Kubernetes clusters.

```bash
https://k3d.io/
k3d is a wrapper CLI that helps you to easily create k3s clusters inside docker.
Nodes of a k3d cluster are docker containers running a k3s image.
All Nodes of a k3d cluster are part of the same docker network.
Usage:
k3d [flags]
k3d [command]
Available Commands:
cluster Manage cluster(s)
completion Generate completion scripts for [bash, zsh, fish, powershell | psh]
config Work with config file(s)
```

## Starting the Kubernetes cluster

Let's use K3d and create a Kubernetes cluster with three nodes. Using the flag -a, you can specify the number of nodes you want to add to the k3d cluster.

```bash
k3d cluster create database-cluster -a 3
```

Now, list details for our k3d cluster.

```bash
k3d cluster list database-cluster

NAME SERVERS AGENTS LOADBALANCER
database-cluster 1/1 3/3 true
```

Now, our environment is ready to begin installing our Percona Kubernetes Operators.

## Conclusion

In this tutorial, we chose k3d over Minikube due to its efficiency and speed in setting up Kubernetes clusters with multiple nodes, which are essential for effectively testing Kubernetes operators in a local environment. Although it's possible to perform tests on a single node with both systems, k3d makes it easier to simulate a more realistic distributed environment, allowing us to utilize our resources more efficiently.

Take a look at our GitHub repository for our Percona Kubernetes Operators:

- [Percona Operator for MySQL](https://github.com/percona/percona-server-mysql-operator)
- [Percona Operator for MongoDB](https://github.com/percona/percona-server-mongodb-operator)
- [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator)

They are fully Open Source. And if you are looking for a version with a graphical interface, we have [Percona Everest](https://docs.percona.com/everest/index.html), our cloud-native database platform: docs.percona.com/everest

What's Next? Let's install our Kubernetes Operators!
