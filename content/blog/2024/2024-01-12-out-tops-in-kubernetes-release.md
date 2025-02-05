---
title: "Our Top Picks from the Kubernetes 1.29 Release"
date: "2024-01-12T00:00:00+00:00"
draft: false
tags: ["edith_puclla", "sergey_pronin", "kubernetes", "release"]
categories: ['Cloud']
authors:
  - sergey_pronin
  - edith_puclla
images:
  - blog/2024/01/k8s-mandala-medium.png
slug: our-top-picks-from-the-kubernetes-release
---

The latest **Kubernetes** version, **1.29**, was released on December 13th 2023. Inspired by the Mandala and symbolizing universal perfection, it concludes the 2023 release calendar. This version comes with various exciting improvements, many of which will be helpful for users who run databases on Kubernetes.

![Mandala](blog/2024/01/k8s-mandala-medium.png)

**Figure 1** - Mandala created in Excalidraw, not perfectly symmetrical.

Here, we highlight this latest release's four key features and improvements. Let's take a look at them together.

## In-Place Update of Pod Resources

This alpha feature allows users to change requests and limits for containers without restarting. It simplifies scaling by a lot and opens new opportunities for auto scaling tools like HPA, VP, and Kubernetes Event-driven Autoscaling (KEDA). It removes the barriers of scaling the applications that were not easy to restart.

When resource resizing is not possible in-place, there are clear strategies for users and controllers (like StatefulSets, JobController, etc.) to handle the situation effectively.

It was first introduced in 1.27 but moved back to alpha as it requires additional architectural changes. It also has [performance improvements](https://github.com/kubernetes/kubernetes/pull/119665) and comes with [Windows containers support](https://github.com/kubernetes/kubernetes/pull/112599).
Read more about this in its Kubernetes Enhancement Proposals ([KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1287-in-place-update-pod-resources)) and the [issue #1287](https://github.com/kubernetes/enhancements/issues/1287) created to add this feature.

## Kubernetes VolumeAttributesClass ModifyVolume

The Kubernetes v1.29 release introduces an alpha feature enabling modification of volume attributes, like IOPS and throughput, by altering the volumeAttributesClassName in a PersistentVolumeClaim (PVC). This simplifies volume management by allowing direct updates within Kubernetes, avoiding the need for external provider API management. Previously, users had to create a new StorageClass resource and migrate to a new PVC; now, changes can be made directly in the existing PVC.

Discover further details in the [KEP](https://github.com/kubernetes/enhancements/pull/3780) and issue [#1287](https://github.com/kubernetes/enhancements/issues/3751), which was established for the inclusion of this feature.

## ReadWriteOncePod PersistentVolume Access Mode

Kubernetes offers access modes for Persistent Volumes (PVs) and Persistent Volume Claims (PVCs), including ReadWriteOnce, ReadOnlyMany, and ReadWriteMany. In particular, ReadWriteOnce restricts volume access to a single node, enabling multiple pods on that node to read from and write to the same volume concurrently. This setup ensures exclusive volume access on a per-node basis while allowing shared volume usage within the node. However, this introduces a potential issue, especially for applications that require exclusive access by a single pod.
In this release, the ReadWriteOncePod access mode for PersistentVolumeClaims has become stable. Now that it is stable, a PVC can be configured to be mounted by a single Pod exclusively.

Here are the Kubernetes Enhancement Proposal ([KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/2485-read-write-once-pod-pv-access-mode)) and issue [#2485](https://github.com/kubernetes/enhancements/issues/2485) that led to the development of this feature.

## Make Kubernetes aware of the LoadBalancer behavior

**kube-proxy's** handling of LoadBalancer Service External IPs is set to change. Traditional methods, such as IPVS and iptables, bind these IPs to nodes, optimizing traffic but causing issues with certain cloud providers and bypassing key Load Balancer features.

There are numerous problems with existing behavior:

- Some cloud providers (Scaleway, Tencent Cloud, ...) are using the LB's external IP (or a private IP) as source IP when sending packets to the cluster. This is a problem in the ipvs mode of kube-proxy since the IP is bounded to an interface, and healthchecks from the LB is never coming back.
- Some cloud providers (DigitalOcean, Scaleway, ...) have features at the LB level (TLS termination, PROXY protocol, ...). Bypassing the LB means missing these features when the packet arrives at the service (leading to protocol errors).

The solution would be to add a new field in the loadBalancer field of a Service's status, like ipMode. This new field will be used by kube-proxy in order to not bind the Load Balancer's External IP to the node (in both IPVS and iptables mode). The value VIP would be the default one (if not set, for instance), keeping the current behavior. The value Proxy would be used to disable the shortcut. This change allows more flexible handling of External IPs, maintaining current behavior as the default and offering an alternative to avoid these issues.

Read more about this in its Kubernetes Enhancement Proposals ([KEP](https://github.com/kubernetes/enhancements/tree/b103a6b0992439f996be4314caf3bf7b75652366/keps/sig-network/1860-kube-proxy-IP-node-binding#kep-1860-make-kubernetes-aware-of-the-loadbalancer-behaviour))

If you are interested in learning about databases on Kubernetes, you can start by [running MySQL in Kubernetes](https://www.percona.com/blog/run-mysql-in-kubernetes-solutions-pros-and-cons/). Explore the solutions, and weigh the pros and cons.
Also, discover our [predictions for Cloud Native](https://www.percona.com/blog/cloud-native-predictions-for-2024/) technologies for this year.
