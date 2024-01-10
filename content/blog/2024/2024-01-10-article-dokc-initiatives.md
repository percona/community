---
title: "Data on Kubernetes Community initiatives: Automated storage scaling"
date: "2024-01-10T00:00:00+00:00"
draft: false
tags:
  ["edith_puclla", "sergey_pronin", "kubernetes", "dok", "storage", "operators"]
authors:
  - sergey_pronin
  - edith_puclla
images:
  - blog/2024/01/dok-initiatives.png
slug: data-on-kubernetes-community-initiatives
---

In the world of Kubernetes, where everything evolves quickly. Automated storage scaling stands out as a critical challenge. Members of the [Data on Kubernetes Community](https://dok.community/) have proposed a solution to address this issue for Kubernetes operators.

If, like me, this is your first time hearing about Automated storage scaling, this will help you understand it better:

**Storage scaling in Kubernetes Operators** refers to the ability of an application running on Kubernetes to adjust its storage capacity automatically based on demand. In other words, it is about ensuring that an application has the right amount of storage available at any given time, optimizing for performance, cost, and operational efficiency, and doing this as automatically as possible.

![DoKC Initiatives](blog/2024/01/dok-initiatives.png)

As databases grow increasingly integral, the absence of unified solutions for storage scaling is becoming more evident. Let’s explore some existing solutions and their limitations:

## pvc-autoresizer

This project detects and scales **PersistentVolumeClaims** (PVCs) when the free amount of storage is below the threshold. [pvc-autoresizer](https://github.com/topolvm/pvc-autoresizer) It is and active open source project on GitHub.

There are certain downsides:

1. Works with PVCs only. It does not work with StatefulSet and does not have integration with Kubernetes Operator.
2. It requires Prometheus stack to be deployed.

Percona wrote a [blog post](https://www.percona.com/blog/storage-autoscaling-with-percona-operator-for-mongodb/) about pvc-autoresizer to automate storage scaling for MongoDB clusters on Kubernetes.

## EBS params controller

This controller provides a way to control IOPS and throughput parameters for EBS volumes provisioned by EBS CSI Driver with annotations on corresponding PersistentVolumeClaim objects in Kubernetes. It also sets some annotations on PVCs backed by EBS CSI Driver representing current parameters and last modification status and timestamps.

Find more about [EBS params controller on GitHub](https://github.com/Altinity/ebs-params-controller).

## Kubernetes Volume Autoscaler

This automatically increases the size of a Persistent Volume Claim (PVC) in Kubernetes when it is nearing full (either on space OR inode usage). It is a similar solution to pvc-autoresizer. Check out more about [Kubernetes Volume Autoscaler](https://github.com/DevOps-Nirvana/Kubernetes-Volume-Autoscaler)

## Kubernetes Event-driven Autoscaling(KEDA)

[KEDA](https://keda.sh/) performs horizontal scaling for various resources in k8s, including custom resources. The metric tracking component is already figured out, but unfortunately, it does not work with vertical scaling or storage scaling yet. We opened [an issue in GitHub](https://github.com/kedacore/keda/issues/5232) to start the discussion.

As you can see, there are some limitations to performing Automated storage scaling, and to address this gap, the **Data on Kubernetes community** wants to develop a solution that solves practical problems and contributes to the open source community.

We're tackling the significant challenge of unexpected disk usage alerts and potential system shutdowns due to insufficient volume space, a common issue in Kubernetes-based databases.

Our goal as a community is to develop a fully automated solution to prevent these inconveniences and failures.

We invite those interested, especially in this particular project, to join us. This is an opportunity to be at the forefront of shaping the automated scaling solutions in Kubernetes. You can join the [Data on Kubernetes community](https://join.slack.com/t/dokcommunity/shared_invite/zt-2a0ahuhsh-MdZ4OpF4nr_s4kyOwTurVw) on Slack, specifically on the #SIG-Operator.

**Once a new solution is validated and proven functional, it will benefit many communities, enabling them to integrate it with their operators. Additionally, it will present an excellent opportunity for Percona to incorporate it into our Operators, enhancing efficiency and facilitating automated storage scaling.**

Explore more about our open-source [Percona Kubernetes Operators for databases](https://www.percona.com/software/percona-kubernetes-operators).
