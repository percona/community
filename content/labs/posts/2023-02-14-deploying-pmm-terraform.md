---
title: 'Deploying Percona Monitoring and Management With Terraform'
date: "2023-02-14"
draft: false
tags: ['Labs','Terraform','PMM']
authors:
  - vadim_tkachenko
images:
  - images/labs/posts/Post-PMM-Terraform.jpg
---

Recently, we released [Percona Monitoring and Management 2.34 (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management) which includes upgrades for backup and Database as a Service (DBaaS) features, and we are seeking ways to simplify PMM deployment.

Previously I wrote about our Terraform provider to deploy Percona Server for MySQL — [Percona Server for MySQL: Automatic Cloud Deployment with Terraform](https://www.percona.com/blog/percona-server-for-mysql-automatic-cloud-deployment-with-terraform/) — and now we added capabilities to deploy PMM with Terraform.

You need the provider version 0.9.10 and PMM can be deployed as:

```
resource "percona_pmm" "pmm" {
  instance_type            = "t3.micro"                    
  key_pair_name            = "sshKey1"                     
  path_to_key_pair_storage = "/tmp/"                       
  volume_type              = "gp2"                         
}
```

Overall I like using Terraform as it offers the following benefits:

1. **Automation:** Terraform automates the process of creating, updating, and managing infrastructure, reducing the risk of errors and increasing efficiency.
2. **Versioning:** Terraform allows you to version control your infrastructure, making it easier to track changes and collaborate with others.
3. **Scalability:** Terraform makes it easy to scale infrastructure up or down, so you can quickly adapt to changing needs.
4. **Reusability:** Terraform provides reusable infrastructure components, so you don’t have to recreate the same infrastructure for different projects or environments.
5. **Portability:** Terraform’s infrastructure as code approach makes it easy to move infrastructure between different cloud providers or data centers.
6. **Improved Collaboration:** Terraform enables multiple team members to work together on infrastructure projects, improving collaboration and reducing the risk of configuration drift.

As another example, we also added PMM monitoring when deploying Percona Server for MySQL instances with Terraform:

```
resource "percona_ps" "ps" {
  count = 1
  instance_type            = "t3.micro" # for AWS
  key_pair_name            = "sshKey1"
  password                 = "password"
  replication_type         = "async"                          
  replication_password         = "replicaPassword"
  cluster_size             = 3
  path_to_key_pair_storage = "/tmp/"
  pmm_address              = "http://admin:XXXXXXX@18.191.19.40"    
}
```

The source code for our Terraform provider is here:

Percona-Lab/terraform-provider-percona: 

[Terraform modules to deploy Percona Server and Percona XtraDB Cluster (github.com)](https://github.com/Percona-Lab/terraform-provider-percona)

And you are welcome to use our prepackaged binaries from [Percona-Lab/percona | Terraform Registry](https://registry.terraform.io/providers/Percona-Lab/percona/latest).
