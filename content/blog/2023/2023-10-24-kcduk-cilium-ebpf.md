---
title: "Kubernetes Community Days UK: Keynote Cilium and eBPF"
date: "2023-10-24T00:00:00+00:00"
draft: false
tags: ["ckd", "kubernetes", "cilium", "ebpf"]
authors:
  - edith_puclla
images:
  - blog/2023/10/kcduk-01.png
slug: kcduk-cilium-ebpf
---

This week, at [Kubernetes Community Days UK](https://community.cncf.io/events/details/cncf-kcd-uk-presents-kubernetes-community-days-uk-2023/) in London. **Liz Rice**, Chief Open Source Officer at Isovalent, delivered a keynote on Cilium, eBPF, and the new feature of Cilium: Mutual Authentication.

![lizrice-keynote-01](blog/2023/10/kcduk-01.png)

_Figure 1. Liz Rice Keynote KCD UK, London. Tuesday 17, 2023_

[Cilium](https://cilium.io/) is an eBPF-powered open source, cloud native solution for delivering, securing, and observing network connectivity between workloads.

eBPF is a technology that allows us to create modules to modify the behavior of the Linux kernel, but why would we want to change the Linux kernel?

Some use cases for observability, security, and networking require tracking and monitoring our application, but we don't want to constantly modify our application with these changes. It's better to add a program that can observe the behavior of our application from the kernel.

But changing the Linux kernel can be, well, hard.

![addfea-to-the-kernel](blog/2023/10/kcduk-02.png)

_Figure 2. Adding features to the kernel (cartoon by Vadim Shchekoldin, Isovalent)_

However, eBPF enables you to modify the kernel's behavior without directly altering the kernel itself. It might sound unconventional, but eBPF makes this possible through the creation of programs for the Linux kernel. The Linux kernel accepts eBPF programs that can be loaded and unloaded as needed.
![addingfeatures-to-the-kernel-with-ebpf](blog/2023/10/kcduk-03.png)

_Figure 3. Adding kernel features with eBPF (cartoon by Vadim Shchekoldin, Isovalent)_

To ensure that these eBPF programs written by us are secure, there is a mechanism in place that allows these programs to be verified safe for execution. This can be seen in [eBPF verification and security](https://ebpf.io/what-is-ebpf/#ebpf-safety). You don't have to restart the kernel to deploy or remove eBPF applications, which makes eBPF one of the technology tools of the moment.

Liz also announced that Cilium recently graduated from CNCF. This means Cilium is considered stable and has been successfully used in production environments.
![cncf-project-maturity-levels](blog/2023/10/kcduk-04.png)

_Figure 4. CNCF Project Maturity Levels, https://www.cncf.io/project-metrics/_

After understanding what eBPF is, let's move on to the actual topic of Liz's keynote. She spoke about "Mutual Authentication” with Cilium.

Mutual Authentication with Cilium was the last significant feature missing from Cilium Service Mesh. It's a somewhat more complex topic related to mTLS (Mutual transport layer security).

mTLS is a mechanism that ensures the authenticity, integrity, and confidentiality of data exchanged between two entities in the network.

In Cilium 1.14, one of the most significant releases, Cilium introduces support for a feature that many developers have requested: mutual authentication. This feature simplifies the process of achieving mutual authentication between two workloads. It now only requires adding two lines of code to the YAML in the Cilium Network Policy to authenticate communication between two workloads.

Slightly more complex, isn't it? Let's explore Mutual Authentication with Cilium in a second blog post very soon. We'll also examine how this is related to Kubernetes and why it matters when running databases on Kubernetes.

Check what the other Graduated and Incubating Projects are at CNCF, and don´t forget to subscribe to our Percona Community Blog to read more about Open Source, CNCF Projects, and Database.
