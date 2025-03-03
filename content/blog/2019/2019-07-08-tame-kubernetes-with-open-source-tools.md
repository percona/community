---
title: 'Tame Kubernetes with These Open-Source Tools'
date: Mon, 08 Jul 2019 13:03:15 +0000
draft: false
tags: ['DevOps', 'Kubernetes', 'Tools']
authors:
  - gaurav_belani
images:
  - blog/2019/07/kubernetes-management-tools.jpg
slug: tame-kubernetes-with-open-source-tools
---

[Kubernetes](https://kubernetes.io/)’ popularity as the most-preferred open-source container-orchestration system has skyrocketed in the recent past. The [overall container market](https://enterprisersproject.com/article/2017/11/kubernetes-numbers-10-compelling-stats) is expected to cross USD 2.7 billion by 2020 with a CAGR of 40 percent. Three orchestrators spearhead this upward trend, namely Kubernetes, [Mesos](http://mesos.apache.org/), and [Docker Swarm](https://docs.docker.com/engine/swarm/). However, referring to the graph below, Kubernetes clearly leads the pack. 

![](blog/2019/07/kubernetes-growth.jpg)

_source: [https://medium.com/@rdodev/saved-you-an-analyst-read-on-kubernetes-growth-2018-edition-810367876981 ](https://medium.com/@rdodev/saved-you-an-analyst-read-on-kubernetes-growth-2018-edition-810367876981)_

The automation and infrastructural capabilities of Kubernetes are transforming the DevOps space,  thereby enhancing the value of the business through software. With Kubernetes you can deploy, scale, and [manage cloud-native databases](https://www.percona.com/live/19/sites/default/files/digital_rack_aws.pdf) and applications from anywhere. No wonder, data scientists and [machine learning engineers](https://www.manipalprolearn.com/data-science/post-graduate-certificate-program-in-data-science-and-machine-learning-manipal-academy-higher-education) love Kubernetes and apply it to improve their productivity. As Kubernetes continues to evolve and grow in complexity, we need to be ready with solutions that simplify Kubernetes, thereby enhancing your development work. Here is a comprehensive list of Kubernetes tools that can help you tame this orchestrator, many of them open source. I have divided them into five functional categories.

1\. Tools for Automating Cluster Deployments
--------------------------------------------

Automated Kubernetes cluster services are a hot topic today because they eliminate much of the deployment and management hassles. An ideal application should consume declarative manifests, bootstrap fully-functioning clusters, and ensure that the K8 clusters are highly available.

*   [**KubeSpray**](https://github.com/kubernetes-sigs/kubespray) is a great choice for individuals who know Ansible. You can deploy this Ansible-driven cluster deployment tool on AWS, GCE, Azure, OpenStack, Baremetal, and Oracle Cloud Infrastructure.
*   [**Conjure-Up**](https://conjure-up.io/) can deploy the Canonical distribution of Kubernetes across several cloud providers using simple commands. The tool has native AWS integration, yet supports other cloud providers like GCE, Azure, Joyent, and OpenStack.
*   **[Kops](https://github.com/kubernetes/kops)** or **Kubernetes Operations** can automate the provisioning of K8 clusters in Amazon Web Services (officially supported) and GCE (beta support). The tool allows you to take full control of the cluster lifecycle, from infrastructure provisioning to cluster deletion.
*   [**Kube-AWS**](https://github.com/kubernetes-incubator/kube-aws) is a command-line tool that creates/updates/destroys fully-functional clusters using Amazon Web Services, namely CloudFormation, Auto Scaling, Spot Fleet, and KMS among others.
*   You might also like to check out the [**Percona Kubernetes operators**](https://www.percona.com/software/percona-kubernetes-operators) for Percona XtraDB Cluster and Percona Server for MongoDB.

2\. Cluster Monitoring Tools
----------------------------

Monitoring Kubernetes clusters is critical in a microservice architecture. The following graph shows the top cluster monitoring tools available today. ![](blog/2019/07/tools-services-to-monitor-kubernetes-clusters.jpg)

_Source: [https://thenewstack.io/5-tools-monitoring-kubernetes-scale-production/](https://thenewstack.io/5-tools-monitoring-kubernetes-scale-production/)_

Here are our recommendations.

*   [**Prometheus**](https://prometheus.io/) is an open-source Cloud Native Computing Foundation (CNCF) tool that offers enhanced querying, visualization, and alerting features.
*   [**CAdvisor**](https://github.com/google/cadvisor) or **Container Advisor** comes embedded into the kubelet, the primary node agent that runs on each node in the cluster. The tool focuses on container-level performance and provides an understanding of the resource usage and performance characteristics of the running containers.
*   [**Datadog**](https://www.datadoghq.com/) is a good monitoring tool for those who prefer working with a fully-managed SaaS solution. It has a simple user interface to monitor containers. Further, it hosts metrics, such as the CPU and RAM. Its open source projects can be accessed in [github](https://github.com/DataDog).
*   **[Heapster](https://github.com/kubernetes-retired/heapster)** was a native supporter of Kubernetes and is installed as a pod inside Kubernetes. Thus, it can effectively gather data from the containers and pods inside the cluster. Unfortunately developers have retired the project, but you can still access the open source code.

3\. Security Tools
------------------

Since Kubernetes effectively automates the provisioning and configuration of containers and provides IP-based security to each pod in the cluster, it has become the de facto container orchestrator. However, Kubernetes cannot offer advanced security monitoring and compliance enforcement, making it important for you to rely on the below-mentioned tools to secure your container stack and in turn [bolster DevOps security](https://www.manipalprolearn.com/blog/decoding-devops-security-three-best-practices).

*   [**Aporeto**](https://github.com/aporeto-inc) offers runtime protection to containers, microservices, and cloud and legacy applications, thereby securing Kubernetes workloads. It provides a cloud-network firewall system to secure apps running in distributed environments.
*   **[Twistlock](https://www.twistlock.com/)** is designed to monitor applications deployed on Kubernetes for vulnerability, compliance issues, whitelisting, firewalling, and offer runtime protection to containers. In fact, it had compliance controls for enforcing HIPAA and PCI regulations on the K8 containers. The latest version adds forensic analysis that can reduce runtime overhead.
*   [**NeuVector**](https://neuvector.com/) was designed to safeguard the entire K8 cluster. The container security product can protect applications at all stages of deployment.
*   [**Sysdig Secure**](https://sysdig.com/products/secure/) offers a set of tools for monitoring container runtime environments. Sysdig designed this tool for deep integrations with container orchestration tools and to run along with other tools, such as Sysdig Monitor.

4\. Development Tools
---------------------

Kubernetes applications consist of multiple services, each running in its own container. Developing and debugging them on a remote Kubernetes cluster can be a cumbersome undertaking. Here are a few development tools that can ease the process of developing and debugging the services locally.

*   **[Telepresence](https://www.telepresence.io/)** is a development tool that allows you to use custom tools, namely debugger and IDE to simplify the developing and [local debugging process](https://kubernetes.io/docs/tasks/debug-application-cluster/local-debugging/). It provides full access to ConfigMap and other services running on the remote cluster.
*   **[Keel](https://keel.sh/)** automates Kubernetes deployment updates as soon as the new version is available in the repository. It is stateless and robust and deploys Kubernetes services through labels, annotations, and charts.
*   [**Helm**](https://github.com/kubernetes/helm) is an application package manager for Kubernetes that allows the description of the application structure using helm-charts and simple commands.
*   [**Apollo**](https://github.com/logzio/apollo/wiki/Getting-Started-with-Apollo) is an open-source application that helps operators create and deploy their services to Kubernetes. It also allows the user to view logs and revert deployments at any time.

5\. Kubernetes-Based Serverless Frameworks
------------------------------------------

Due to Kubernetes’ ability to orchestrate containers across clusters of hosts, serverless FaaS frameworks rely on Kubernetes for orchestration and management. Here are a few Kubernetes-based serverless frameworks that can help build a serverless environment.

*   **[Kubeless](https://kubeless.io/)** is a Kubernetes-native open-source serverless framework that allows developers to deploy bits of code without worrying about the underlying infrastructure. It uses Kubernetes resources to offer auto-scaling, API routing, monitoring, and troubleshooting
*   [**Fission**](https://platform9.com/fission/) is an open-source serverless framework released by Platform9, a software company that manages hybrid cloud infrastructure with Kubernetes cloud solutions. The framework helps developers manage their applications without bothering about the plumbing related to containers.
*   [**KNative**](https://github.com/knative) is a platform used by operators to build serverless solutions on top of Kubernetes. It isn’t an outright serverless solution. KNative acts as a layer between Kubernetes and the serverless framework, enabling developers to run the application anywhere that Kubernetes runs.

Time for Action
---------------

Open-source container-orchestration systems like Kubernetes have helped users overcome several challenges in the DevOps space. However, as Kubernetes continues to evolve, your development, monitoring, and security strategies need to change. Use the Kubernetes tools and frameworks shared in this post to simplify cluster orchestration and deployment, making it easy to deploy this popular orchestrator. 

-- 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource, please **test** ideas before applying them to your production systems, and **always **secure a working back up._

_Featured image photograph [AnnaD on Pixabay](https://pixabay.com/photos/boat-wheel-ship-sea-nautical-2387790/)_