---
title: "Percona Terraform Provider"
description: "Percona Terraform Provider"
images:
 - images/labs/percona-terraform-provider.jpg
---

[← Labs Home](/labs/)


Percona offers Terraform provider for easy installation of Percona Server for MySQL and PMM in AWS and Google Cloud.

Terraform offers the following benefits:

1. Automation: Terraform automates the process of creating, updating, and managing infrastructure, reducing the risk of errors and increasing efficiency.
2. Versioning: Terraform allows you to version control your infrastructure, making it easier to track changes and collaborate with others.
3. Scalability: Terraform makes it easy to scale infrastructure up or down, so you can quickly adapt to changing needs.
4. Reusability: Terraform provides reusable infrastructure components, so you don't have to recreate the same infrastructure for different projects or environments.
5. Portability: Terraform's infrastructure as code approach makes it easy to move infrastructure between different cloud providers or data centers.
6. Improved Collaboration: Terraform enables multiple team members to work together on infrastructure projects, improving collaboration and reducing the risk of configuration drift.

With Percona Terraform Provider you can:

* Install single Percona Server for MySQL instance
* Install Percona XtraDB Cluster with multiple nodes
* Install Percona Server for MySQL in async replication mode with 2 or more instances with primary node and replica nodes
* Install Percona Server for MySQL in Group Replication mode 
* Install PMM to monitor deployed MySQL instances

We support both AWS and Google Cloud.
Source code and examples are:
[Percona-Lab/terraform-provider-percona](https://github.com/Percona-Lab/terraform-provider-percona)
