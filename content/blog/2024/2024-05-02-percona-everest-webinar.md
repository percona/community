---
title: "How to Provision a MongoDB Cluster in Kubernetes with Percona Everest Summary"
date: "2024-05-02T00:00:00+00:00"
draft: false
tags: ["everest", "percona", "databases"]
categories: ['Cloud', 'Community']
authors:
  - edith_puclla
images:
  - blog/2024/05/percona-everest-mongodb.png
---

**Kubernetes** continues evolving, and the complexity of deploying and managing databases within the ecosystem is a topic of considerable discussion and importance these days. This article summarizes a detailed discussion between [Piotr Szczepaniak](https://www.linkedin.com/in/petersgd/) and [Diogo Recharte](https://www.linkedin.com/in/diogo-recharte/), who offer insights and live demonstrations to simplify database operations on Kubernetes with a new technology for cloud-native applications: Percona Everest. If you want to watch the full video, check out [How to Provision a MongoDB Cluster in Kubernetes Webinar](https://www.youtube.com/live/ITeM7Pdp4oc?si=XAeL_4myDdhyq38h).

![Percona Everest Webinar](blog/2024/05/peterdiogo.png)

Peter mentions that Initially, people were doubtful about using virtual machines for databases, just like they were skeptical about Kubernetes. However, the topic brings together many people who run databases on containers to share their use cases and new discussions at events like Data on [Kubernetes Day at Kubecon](https://www.youtube.com/playlist?list=PLHgdNuGxrJt1eqQeSHJ4J-RydHO6-LTeW).

The introduction of **StatefulSets** and **Persistent Volumes** has altered the perception of Kubernetes from being purely ephemeral to being capable of handling persistent data. This change is important for database applications that require data retention over time.

The Kubernetes ecosystem is rapidly expanding. This growth is thanks to its open-source nature and the continuous addition of new functionalities, such as support for specialized hardware like GPUs, which are crucial for AI and machine learning applications.

Peter also mentioned that its complexity is the main barrier to Kubernetes adoption for databases. Organizations often need help with the layer added by Kubernetes on top of database management. Also, failure in initial attempts to integrate Kubernetes can discourage organizations from further attempts, primarily due to a lack of internal expertise.

#### Benefits of Database as a Service (DBaaS)

DBaaS significantly reduces the time required for database provisioning, which is particularly useful in organizations needing rapid deployment. Public and private DBaaS solutions offer scalability, which is crucial for handling varying workloads and organizational growth without compromising performance.

#### Private vs. Public DBaaS

Private DBaaS offers more extensive customization options and control over databases, which is essential for companies with specific needs that public solutions cannot meet.

Data security and compliance with regulations are more manageable in a private DBaaS because it operate within the company's internal infrastructure.

#### Demo  to Deploying MongoDB on Kubernetes

Diogo presented a demo of deploying a MongoDB database using Percona's Everest platform on Kubernetes, where he showed how to handle daily operations and disaster recovery scenarios efficiently. Watch the [Percona Everest Demo on YouTube](https://youtu.be/ITeM7Pdp4oc?t=1039)

![Percona Everest Draw](blog/2024/05/percona-everest-mongodb.png)

The session explained how Kubernetes operators and custom resources help manage databases more easily. They do this by simplifying complex processes and automating regular tasks.

![Percona Everest GUI](blog/2024/05/everest-gui.png)

Some questions that users asked in this presentation are:

### How do we handle the PV when the Pods go down?

The PV will remain in place; this is a standard functionality of a stateful set. After the Pod goes down, the replacement Pod will attach to the PVC, which is standard behavior for a stateful set.

### What happens if the node in Kuberentes goes down?

It depends on the storage layer that you have configured in your cluster. If the storage class you are using is tied to that node, then placing it on a new node will provision a new one, and some reconciliation will occur within the database itself.

### What is the current state of Percona Everest?

Percona Everest is currently in a Beta stage, and Percona aims to release a GA version. The project is fully open source, and anyone can join our project on GitHub. We appreciate feedback from the community.

Do you want to send us feedback or contribute in this cool project? We are completely open-source, you can visit [Percona Everest on GitHub](https://github.com/percona/everest).
