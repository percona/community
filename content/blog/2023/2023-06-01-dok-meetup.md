---
title: "Data on Kubernetes Meetup May 23"
date: "2023-06-01T00:00:00+00:00"
draft: false
tags: ["dok", "opensource", "cncf", "kuberentes", "percona", "operators"]
authors:
  - edith_puclla
images:
  - blog/2023/06/dok-intro.jpg
slug: percona-and-data-on-kubernetes-meetup
---

**Percona** has started to participate in **Data on Kubernetes** (DoK) meetings about **Kubernetes Operators**.
These meetings are an initiative of DoK meetups that spotlight DoK case studies. In this blog post series, I will summarize the topics covered in each meeting.

On May 23, very interesting topics were discussed on the agenda. Let's begin to summarize it.

We start with a new project proposal, which is called: [Distributed Systems Operator Interface (DSOI)](https://docs.google.com/document/d/1CJeFtNpDSyaPoPWvimwMFt5s1g2Zj2Ppg_DJX7nVurk/edit#). It is proposed by **Adheip Singh** from DataInfra, **Nitish Tiwari** from Parseable, and **Itamar Marom** from AppsFlyer.

This project is a set of best practices for building Kubernetes operators for distributed systems. The spec defines standard practices that can help define custom resources (CR). It consists of Kubernetes-native **CRDs** and specs and is not bound to any specific application. There are already two operators built using this set of practices:

- [Parseable Kubernetes Operator](https://github.com/parseablehq/operator)
- [Control Plane For Apache Pinot](https://github.com/datainfrahq/pinot-operator)

If you want to contribute, send proposals, join [datainfra-workspace](https://launchpass.com/datainfra-workspace) or raise bugs in the GitHub repository of [DSOI](https://github.com/datainfrahq/dsoi-spec/issues).

![Panel Discussion](blog/2023/06/dok-datainfra.jpeg)

As the second item on the agenda, we have an update about the [DoK Operator SIG Project Proposal - Security & Hardening Guide](https://docs.google.com/document/d/1tbm44jC1qf6kAf9qje5V-UhaXG-AlGud9nhMaoPN6mU/edit#heading=h.fjdgqyupbu03). This project is proposed by **Robert Hodges**, Altinity Inc.

This project is a guide to establishing a baseline for secure data management on Kubernetes by fortifying the database operators. The guide aims to identify the typical attack surfaces that exist for databases running on Kubernetes. **It will establish a collection of best practices for enhancing their security through the utilization of operators**.

Robert mentioned that he connected to TAG Security, which in turn led to a link to BadRobot, which is a scanner that checks operators for excessive privileges. Also, Robert presented to DoK Bay Area last week to introduce the problem of operator security.

![Panel Discussion](blog/2023/06/dok-security-hardering.jpeg)

For the Operator security & hardening guide, we can raise issues on [sig-operator](https://github.com/dokc/sig-operator). They are currently seeking volunteers and contributors for their project; Find [operator-security-hardening](https://github.com/dokc/sig-operator/tree/main/operator-security-hardening) project on GitHub, or feel free to write Robert Hodges **rhodges@altinity.com**.

Finally, we have an update of the Operator Feature Matrix (OFM)

The **Operator Feature Matrix (OFM)** is a project from the Data on Kubernetes Community to create a standardized and vendor-neutral feature matrix for various Kubernetes operators that manage stateful workloads. This project is proposed by **Alvaro Hernandez**, and it is definitely a good project to contribute if you are looking to improve the end-user experience with the use of workloads in Kubernetes.

**CloudNativePG** project sent feedback to improve OFM. CloudNativePG is the Kubernetes operator that covers the full lifecycle of a highly available PostgreSQL database cluster. Planning to create a website for end-user adoption

There are other (non-Postgres) technologies, like Apache Druid, jumping on OFM. This is a work in progress.

The end of June is being considered for a 1.0 freeze, before which it is required to get as much feedback as possible.
If you are interested, feedback can be as simple as opening an issue to discuss something; or sending a PR requesting improvements (or both). Feel free to do it on [OFM GitHub Repo](https://github.com/dokc/operator-feature-matrix).
