---
title: 'Deploying MySQL Group Replication With Terraform'
date: "2023-02-14"
draft: false
tags: ['Labs','Terraform','MySQL']
authors:
  - vadim_tkachenko
images:
  - images/labs/posts/Group-Replication.jpg
---

Previously, I wrote about our Terraform provider to deploy Percona Server for MySQL ([Percona Server for MySQL: Automatic Cloud Deployment With Terraform](/labs/posts/2022-10-20-terraform-percona-server-for-mysql/)) and Percona Monitoring and Management ([Deploying Percona Monitoring and Management (PMM) With Terraform](/labs/posts/2023-02-14-deploying-pmm-terraform/)). Now we also added the capability to deploy Group Replication configuration with Percona Server for MySQL, and assuming we have PMM installed (see previous post), we also can automatically add Group Replication nodes to PMM monitoring.

```
resource "percona_ps" "psgr" {
  count = 1
  instance_type            = "t3.micro" # for AWS
  key_pair_name            = "sshKey1"
  password                 = "password"
  replication_type         = "group-replication"                            
  replication_password         = "replicaPassword"
  cluster_size             = 3
  path_to_key_pair_storage = "/tmp/"
  pmm_address              = "http://admin:XXXXXX@18.191.19.40"      
  pmm_password             = "password"
}
```

After deployment we have a 3-node Group Replication cluster with monitoring in PMM:

![3-node Group Replication cluster with monitoring in PMM](images/labs/posts/terraform-group-pmm-1.png)

The source code for our Terraform provider is here: [Percona-Lab/terraform-provider-percona: Terraform modules to deploy Percona Server and Percona XtraDB Cluster (github.com)](https://github.com/Percona-Lab/terraform-provider-percona).

And you are welcome to use our prepackaged binaries from [Percona-Lab/percona | Terraform Registry](https://registry.terraform.io/providers/Percona-Lab/percona/latest).