---
title: "Percona DBaaS Infrastructure Creator"
description: "Percona DbaaS Infrastructure Creator creates the infrastructure for you to try a PMM DBaaS. It will help you to choose the right types of instances based on the number of vCPU and the amount of memory and create clusters."
layout: product
images:
    - images/labs/dbaas-infrastructure-creator.jpg
tags: ['Labs','Creator', 'DBaaS']
---


If you would like to try a PMM DBaaS, but don’t want to deal with Kubernetes, [Percona DbaaS Infrastructure Creator](https://mydbaas.labs.percona.com/) is the right tool for you. It creates the infrastructure in an AWS account. 

It will help you to choose the right types of instances based on the number of vCPU and the amount of memory and create clusters. It can even deploy the clusters and Kubernetes operators for MySQL, PXC, and MongoDB.

## Interested?

Try this tool out and share your thoughts with us! If you would like to talk with Percona Labs creators or stay in touch for a future update - leave your contact details in the [Contact form](/labs/contacts).

## Forum

Join our [Percona Community Forum](https://forums.percona.com/c/percona-labs/percona-dbaas-infrastructure-creator/79) for discussion.

## Introduction

Percona DbaaS Infrastructure Creator is very easy to use. You have 2 features:

* **An instance selector**: In case you don’t know what instance type to use, but you DO know how many CPUs and how much memory your databases require.

* **A Cluster Creator**: This is where you decide on some minimal and basic properties of the cluster and deploy it.

### Instance Selector

Currently, AWS has 270 different instance types available. Which one to use? The instance selector will help you with that. Just pass the number of vCPUs and the amount of memory and it will show a list of EKS suitable EC2 instances.

![Percona DBaaS Infrastructure Creator - Instance Selector](images/labs/docs/dbaas-creator/image1.jpg)

### Cluster Creator

You only need to pass the name of the cluster, the amount of desired nodes, the instance type and on which region you would like to run the cluster.

![Percona DBaaS Infrastructure Creator - Cluster Creator - Step 1](images/labs/docs/dbaas-creator/image2.jpg)

If you pass your AWS key/secret, the tool will take care of deploy the cluster and once is done, it will return the contents of the Kubeconfig file for you to use in the DBaaS of PMM

For security reasons, you may choose NOT to pass the AWS credentials.

Under the hood, the cluster is created using the tool [eksctl](https://github.com/weaveworks/eksctl) which is a “CloudFormation stack creator”. 

If you are proficient enough with ekstcl, you can just copy/paste the created YAML and run the eksctl command on your own server, without sharing your credentials. 

![Percona DBaaS Infrastructure Creator - Cluster Creator - Step 2](images/labs/docs/dbaas-creator/image3.jpg)

Give it a try! And start using the Percona DBaaS without writing a single command.
