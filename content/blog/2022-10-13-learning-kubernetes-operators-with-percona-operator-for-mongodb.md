---
title: "Learning Kubernetes Operators with Percona Operator for MongoDB"
date: "2022-10-13T00:00:00+00:00"
draft: false
tags: ["kubernetes", "operators", "databases", "mongodb", "docker"]
authors:
  - edith_puclla
images:
  - blog/2022/13/with-operators.png
slug: learning-kubernetes-operators-with-percona-operator-for-mongodb
---

One of the topics that have resonated a lot for me since the first KubeCon I attended in 2018 is **Kubernetes Operators**.

The concept of Operators was introduced much earlier in 2016 by the CoreOS Linux development team. They were looking for a way to improve automated container management in Kubernetes.

## What do we mean by a Kubernetes Operator?

We use the [definition of CNCF](<https://www.cncf.io/blog/2022/06/15/kubernetes-operators-what-are-they-some-examples/#:~:text=K8s%20Operators%20are%20controllers%20for,Custom%20Resource%20Definitions%20(CRD).>). The Kubernetes project defines **“Operator”** simply: **“Operators are software extensions that use custom resources to manage applications and their components“**.

This means that among the applications that can be run on Kubernetes, there are applications that still require manual operations to manage them and complete the Kubernetes deployment cycle because Kubernetes itself can’t manage all these manual operations. It is what the Operators take care of, to automate those manual processes of the applications deployed in Kubernetes.

**How can this be possible?**

The Operators use/extend the **Kubernetes API** (this API has the basics needed for a user to interact with the Kubernetes cluster) and create [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#:~:text=A%20custom%20resource%20is%20an,resources%2C%20making%20Kubernetes%20more%20modular.) to add new functionality according to the needs of an application to be flexible and scalable.

Once the creation of the **custom resource** is finished, it creates objects that can be managed using kubectl, as other default Kubernetes resources are managed, such as Deployments, Pods, etc.

Here we see the difference between the workflows with and without operators.

**With Operators**

![With Operators](blog/2022/13/with-operators.png)

**Without Operators**

![Without Operators](blog/2022/13/without-operators.png)

The above illustration is based on a presentation by [Sai Vennam](https://youtu.be/i9V4oCa5f9I?t=403).

It is time for an example!
We will see how Percona Operator for MongoDB works.

Percona Operator for MongoDB contains everything we need to quickly and consistently deploy and scale [Percona Server for MongoDB instances](https://www.percona.com/software/mongodb/percona-server-for-mongodb) into a Kubernetes cluster on-premises or in the cloud.

You can find Percona Operator for MongoDB officially in:

- [Artifact Hub](https://artifacthub.io/packages/olm/community-operators/percona-server-mongodb-operator)
- [Operator Hub](https://operatorhub.io/operator/percona-server-mongodb-operator)

**Why does Percona Server for MongoDB (a database) need a Kubernetes Operator?**

Kubernetes has been designed for stateless applications. Kubernetes in many cases doesn't require operators for stateless applications because Kubernetes doesn't need more automation logic. But stateful applications like databases do need operators because they cannot automate the entire process natively.

One of the main benefits of operators is the automation of repetitive tasks that are often handled by human operators, eliminating errors in application lifecycle management.

## Installing MongoDB Percona Operator using GKE

This guide shows you how to deploy **Percona Operator for MongoDB** on **Google Kubernetes Engine (GKE)**. We use GKE which takes less time to set up Kubernetes in Google Cloud just for the purpose of this demo. This demonstration assumes you have some experience with the platform. For more information on the GKE, see [Kubernetes Engine Quickstart](https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster.)

As prerequisites, we need [Google Cloud shell and Kubectl](https://docs.percona.com/percona-operator-for-mongodb/gke.html#prerequisites). You can find the installation guides for AWS and AZURE in the [Percona documentation](https://docs.percona.com/percona-operator-for-mongodb/#advanced-installation-guides). Let´s start!

- Creating a GKE cluster with three nodes.

```bash
gcloud container clusters create my-cluster-name --project percona-product --zone us-central1-a --cluster-version 1.23 --machine-type n1-standard-4 --num-nodes=3
```

![Overview](blog/2022/13/1-operators-gcloud.png)

- Now you should configure the command-line access to your newly created cluster to make kubectl able to use it.

```bash
gcloud container clusters get-credentials my-cluster-name --zone us-central1-a --project percona-product
```

![Overview](blog/2022/13/2-operators-get-credentials.png)

- Finally, use your [Cloud Identity and Access Management [Cloud IAM]](https://cloud.google.com/iam) to control access to the cluster. The following command will give you the ability to create Roles and RoleBindings:

```bash
kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value core/account)
```

![Overview](blog/2022/13/3-kubectl-create-cluisterrolebinding.png)

### Install the Operator and deploy your MongoDB cluster

- Create a new namespace called **percona-demo-namespace**

```bash
kubectl create namespace percona-demo-namespace
```

![Overview](blog/2022/13/4-kubectl-create-namespace.png)

- Set the context for the namespace

```bash
kubectl config set-context $(kubectl config current-context) --namespace=percona-demo-namespace
```

![Overview](blog/2022/13/5-kubectl-config-set-contex.png)

- Deploy the Operator

```bash
kubectl apply -f https://raw.githubusercontent.com/percona/percona-server-mongodb-operator/v1.13.0/deploy/bundle.yaml
```

![Overview](blog/2022/13/6-kubectl-apply-f-bundle.png)

- The operator has been started, and you can deploy your MongoDB cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/percona/percona-server-mongodb-operator/v1.13.0/deploy/cr.yaml
```

![Overview](blog/2022/13/7-kubectl-apply-f-cr.png)

- When the process is over, your cluster will obtain the ready status. Check with:

```bash
  kubectl get psmdb.
```

![Overview](blog/2022/13/8-kubectl-get-psmdb.png)

**Note:** “psmdb” stands for [Percona Server for MongoDB](https://www.percona.com/software/mongodb/percona-server-for-mongodb)

### Verifying the cluster operation

- You will need the login and password for the admin user to access the cluster. Use kubectl get secrets command to see the list of Secrets objects

```bash
kubectl get secret my-cluster-name-secrets -o yaml
```

![Overview](blog/2022/13/9-kubectl-get-secret.png)

- Bring it back to a human-readable form to **MONGODB_DATABASE_ADMIN_PASSWORD** and **MONGODB_DATABASE_ADMIN_USER**

![Overview](blog/2022/13/10-decode.png)

- We check the details of the Services, before testing the connection to the cluster

![Overview](blog/2022/13/11-get-services.png)

- Run a Docker container with a MongoDB client and connect its console output to your terminal. The following command will do this, naming the new Pod percona-client:

```bash
kubectl run -i --rm --tty percona-client --image=percona/percona-server-mongodb:4.4.16-16 --restart=Never -- bash -il
```

![Overview](blog/2022/13/12-run-docker-container.png)

- Now run mongo tool in the percona-client command shell using the login (which is normally clusterAdmin)

```bash
mongo "mongodb://clusterAdmin:Dgqjc1HElUvvGnH9@my-cluster-name-mongos.percona-demo-namespace.svc.cluster.local/admin?ssl=false"
```

![Overview](blog/2022/13/13-mongo.png)

**Woolaaa!** We have deployed MongoDB in Kubernetes using Operator, It works! **:)**

Now that you have the MongoDB cluster, you have full control to configure and manage MongoDB deployment from a single Kubernetes control plane, which means that you can manage MongoDB instances in the same way you manage default objects in Kubernetes like Deployments, Pods, or Services. For advanced configuration, topics see our guide [Percona Operator for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/users.html).

### Conclusion

Kubernetes Operators extend the Kubernetes API to automate processes that cannot be achieved natively with Kubernetes. This is the case for stateful applications like MongoDB.
Percona develops [Percona Operator for MongoDB](https://github.com/percona/percona-server-mongodb-operator) that contains everything you need to quickly and consistently deploy and scale Percona Server for MongoDB instances into a Kubernetes cluster on-premises or in the cloud. You can try it on different cloud providers and [tutorials](https://docs.percona.com/percona-operator-for-mongodb/#advanced-installation-guides) for more advanced configurations.

You can find **Percona Operator for MongoDB** in Hacktoberfest! If you're looking to improve your Kubernetes skills, this is a [great project to start contributing](https://www.percona.com/blog/contribute-to-open-source-with-percona-and-hacktoberfest/) to.

We also have a **[public roadmap](https://github.com/percona/roadmap/projects/1)** of Percona Kubernetes Operators. If you have any feedback or want to draw our attention to a particular feature, feel free to be part of it and vote for issues! :)

**Resources:**

- [Installation of MongoDB via Kubernetes Operator by Sergey Pronin - MongoDB Kubernetes operator](https://www.youtube.com/watch?v=HZ9yaS-ZS48&t=2809s)
- [Install Percona Server for MongoDB on Google Kubernetes Engine (GKE)](https://docs.percona.com/percona-operator-for-mongodb/gke.html)
- [Percona Server Mongodb Operator GitHub Repository](https://github.com/percona/percona-server-mongodb-operator)
- [Kubernetes Operators: what are they? Some examples CNCF.IO](<https://www.cncf.io/blog/2022/06/15/kubernetes-operators-what-are-they-some-examples/#:~:text=K8s%20Operators%20are%20controllers%20for,Custom%20Resource%20Definitions%20(CRD).>)
- [Kubernetes Operators Explained by Sai Vennam](https://www.youtube.com/watch?v=i9V4oCa5f9I)
- [Working with Kubernetes API Ivan Velichko](https://iximiuz.com/en/series/working-with-kubernetes-api/)
