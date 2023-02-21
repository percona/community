---
title: 'Percona Server for MySQL – Automatic Cloud Deployment with Terraform'
date: "2022-10-20"
draft: false
tags: ['Labs','Terraform','MySQL']
authors:
  - vadim_tkachenko
images:
- images/labs/posts/MySQL-Terraform.jpg
---

We are looking to provide simplified ways to deploy Percona software in cloud environments, especially for more advanced scenarios like replication and multi-node cluster (in the case of [Percona XtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster)).

For this I propose trying out our new Terraform provider, with the capabilities:

* Deploy in AWS or GCP Cloud. The provider will automatically create instances and deploy [Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server)
* Deploy either Percona Server for MySQL or Percona XtraDB Cluster
* Choose instance size
* Choose storage volume size, type, and IOPs
* Multi-node async replication or multi-node Percona XtraDB Cluster
* Customize MySQL configuration file
* Capability to deploy MyRocks Engine

To get more understanding let’s review some examples, but before that, where you can obtain modules:

The provider is available from Terraform registry:

[https://registry.terraform.io/providers/Percona-Lab/percona/0.9.0](https://registry.terraform.io/providers/Percona-Lab/percona/0.9.0)

And source code at GitHub:

[Percona-Lab/terraform-provider-percona: Terraform modules to deploy Percona Server and Percona XtraDB Cluster (github.com)](https://github.com/Percona-Lab/terraform-provider-percona)

Keep in mind that this is an EXPERIMENTAL software yet and is not covered by Percona Support.

###Examples:

As a single server is quite trivial, let’s jump to more complex scenarios: Asynchronous replication between two nodes.

Here is our main.tf file:

```
# AWS provider configuration
provider "percona" {
  region  = "us-east-2"
  profile = "default"
  cloud   = "aws"
}
 
 
resource "percona_ps" "psrepl2" {
  instance_type            = "t3.micro" # for AWS
  key_pair_name            = "sshKey2"
  password                 = "password"
  replica_password         = "replicaPassword"
  cluster_size             = 2
  volume_size              = 30
}
```

And we apply with:

```
terraform apply
…
percona_ps.psrepl2: Still creating... [4m20s elapsed]
percona_ps.psrepl2: Still creating... [4m30s elapsed]
percona_ps.psrepl2: Still creating... [4m40s elapsed]
percona_ps.psrepl2: Creation complete after 4m47s [id=JZnEGllTfJIOqjgMyyRl]
```

So five minutes later we have the following:

* We created and initialized two t3.micro AWS instances in us-east-2 region
* Each instance uses 30GB volume sizes
* We can log in to instances with an ssh key (which will be created if it didn’t exist before)
* Each instance will have installed Percona Server for MySQL with the latest 8.0 version
* Instances will be connected by SOURCE->Replica MySQL replication

Similarly, for deploying a 3 node Percona XtraDB Cluster, we use:

```
# AWS provider configuration
provider "percona" {
  region  = "us-east-2"
  profile = "default"
  cloud   = "aws"
}
 
 
resource "percona_pxc" "pxc3" {
  instance_type            = "t3.micro" # for AWS
  key_pair_name            = "sshKey2"
  password                 = "password"
  cluster_size             = 3
  volume_size              = 30
}
```

Now we also can show an example for Google Cloud:

```
# AWS provider configuration
provider "percona" {
  region  = "us-east-2"
  profile = "default"
  cloud   = "aws"
}
 
 
resource "percona_pxc" "pxc3" {
  instance_type            = "t3.micro" # for AWS
  key_pair_name            = "sshKey2"
  password                 = "password"
  cluster_size             = 3
  volume_size              = 30
}
```

In this case, we will use more powerful instances with dedicated SSD volumes of 40GB each.

The script will deploy instances and install three Percona Server for MySQL servers connected in replication (one source and two replicas).

### In conclusion:

We offer a Terraform provider that simplifies the deployment of Percona Server for MySQL and Percona XtraDB Cluster in cloud environments and offers various customizations for instances and replication configurations.