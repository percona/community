---
title: "How to Use IAM Roles for Service Accounts (IRSA) with Percona Operator for MongoDB on AWS"
date: "2025-02-17T00:00:00+00:00"
tags: ['Kubernetes', 'MongoDB']
authors:
  - natalia_marukovich
images:
  - blog/2025/02/mongo-aws-iam.jpg
---

Introduction
=====

[Percona Operator for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/index.html) is an open-source solution designed to streamline and automate database operations within Kubernetes. It allows users to effortlessly deploy and manage highly available, enterprise-grade MongoDB clusters.  The operator simplifies both initial deployment and setup, as well as ongoing management tasks like backups, restores, scaling, and upgrades, ensuring seamless database lifecycle management.

When running database workloads on Amazon EKS (Elastic Kubernetes Service), backup and restore processes often require access to AWS services like S3 for storage. A key challenge is ensuring these operations have secure, least-privileged access to AWS resources without relying on static credentials. Properly managing these permissions is crucial to maintaining data integrity, security, and compliance in automated backup and restore workflows.

[IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) is the recommended approach to solve this problem. IRSA allows Kubernetes pods to securely assume IAM roles, eliminating the need for hardcoded credentials, long-lived AWS keys, or excessive permissions. Instead, it leverages OpenID Connect (OIDC) authentication, ensuring that only the right workloads get access to AWS services.\
By implementing IRSA, you enhance the security posture of your Kubernetes workloads while simplifying IAM management. In this article, we'll walk through how IRSA works, why it's beneficial, and how to configure it properly for the Percona Operator for MongoDB in EKS clusters.

IRSA Installation and Configuration for Percona Operator for MongoDB
====================================================================

1.  IRSA requires an OpenID Connect (OIDC) provider associated with your EKS cluster.\
    So, you should [create an OIDC provider for your EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html#:~:text=To%20create%20a%20provider%2C%20choose,com%20and%20choose%20Add%20provider.). 

Creating an OIDC provider for your EKS cluster involves several steps. This setup allows your EKS cluster to use IAM roles for service accounts, which makes it possible to grant fine-grained IAM permissions to pods.

```shell
# Check if OIDC is already set up:

aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text

https://oidc.eks.eu-west-3.amazonaws.com/id/7AA1C67941083331A80382E464EB2F1F

# If it is not already set up, create an OIDC provider:

eksctl utils associate-iam-oidc-provider --region <region> --cluster <cluster-name> --approve
```

Here oidc-id is 7AA1C67941083331A80382E464EB2F1F. We will use it under role creation.

2. Create an IAM Policy to access s3 buckets.  Substitute <s3_bucket> with your correct bucket name:
```shell
# Define the required permissions in an IAM policy JSON file: 


cat s3-bucket-policy.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::<s3_bucket>",
        "arn:aws:s3:::<s3_bucket>/*"
      ]
    }
  ]
}

# Create the IAM policy:

aws iam create-policy --policy-name <policy name> --policy-document file://s3-bucket-policy.json
```

3. Create an IAM Role and Attach the Policy:

```shell
# Role example. Replace <account-id> with account id and <oidc-id> with cluster’s OIDC ID


cat role-trust-policy.json



{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account-id>:oidc-provider/oidc.eks.<region>.amazonaws.com/id/<oidc-id>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.<region>.amazonaws.com/id/<oidc-id>:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}

# Create role:

aws iam create-role --role-name <role_name> --assume-role-policy-document file://role-trust-policy.json --description "Allow access to s3 bucket"



```
4. Attach the policy to the role.

```shell
# Please update <role-name>, <account-id> and <policy-name> with the corresponding values.

aws iam attach-role-policy --role-name <role-name> --policy-arn arn:aws:iam::<account-id>:policy/<policy-name>
```

5. [Install the operator and deploy Percona Server for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/eks.html#install-the-operator-and-deploy-your-mongodb-cluster) in your EKS cluster (skip this step if you already have the operator and the database cluster installed).

6. To ensure proper functionality, we need to annotate both the operator service account (default: percona-server-mongodb-operator) and the cluster service account (default: default).

🔴 Warning: The cluster and operator  won't restart automatically; therefore, a manual restart is necessary to apply the changes.

```shell
# Get service accounts:

$ kubectl get sa -n <namespace>
NAME                              SECRETS   AGE
default                           0         25m
percona-server-mongodb-operator   0         25m


# Get role_arn:

aws iam get-role --role-name <role-name> --query "Role.Arn" --output text

# Annotate service account. Please update role_arn with appropriate value.

kubectl annotate serviceaccount default  \
	eks.amazonaws.com/role-arn="<role_arn>" 

kubectl annotate serviceaccount percona-server-mongodb-operator \
	eks.amazonaws.com/role-arn="<role_arn>"
```

7. To verify that the settings have been applied, inspect service accounts and the environment variables in both the operator and replica set (RS/Config) pods. The variable AWS_ROLE_ARN should be properly set.
```shell
# Check annotation in service account

$ kubectl get sa -n <namespace> percona-server-mongodb-operator -o yaml

$ kubectl get sa -n <namespace> default -o yaml


# Check the variable inside container

$ kubectl exec -ti <percona-server-mongodb-operator-container> -n <operator_namespace>  bash

bash-5.1$ printenv | grep 'AWS_ROLE_ARN'
AWS_ROLE_ARN=arn:aws:iam::1111111111111:role/some-name-psmdb-access-s3-bucket


$ kubectl exec -ti <rs0-0_pod> -n <namespace> bash

[mongodb@some-name-rs0-0 db]$ printenv | grep 'AWS_ROLE_ARN'
AWS_ROLE_ARN=arn:aws:iam::1111111111111:role/some-name-psmdb-access-s3-bucket
```

8. Configure the backup/restore settings as usual, but do not provide s3.credentialsSecret for the storage in deploy/cr.yaml. For detailed instructions  please refer to [Configure storage for backups](https://docs.percona.com/percona-operator-for-mongodb/backups-storage.html).

```shell
# backup section in cr.yaml example 
   storages:
      aws-s3:
        type: s3
        s3:
          region: <region>
          bucket: <bucket>

```

---
Conclusion
==============

Using IAM Roles for Service Accounts (IRSA) in an  Amazon EKS cluster is a best practice when running [database operators](https://docs.percona.com/percona-operators/) in Kubernetes. By integrating IRSA, database operators---such as the[ Percona Server for MongoDB Operator](https://docs.percona.com/percona-operator-for-mongodb/index.html)---can securely access AWS services like S3 for backups without relying on static credentials.

IRSA enhances security by enforcing the principle of least privilege, ensuring that database operators in EKS have access only to the specific AWS resources they require. This approach reduces the risk of unauthorized access while also improving manageability by eliminating the need to store and rotate AWS credentials within Kubernetes secrets. By adopting IRSA in [Percona Server for MongoDB Operator](https://docs.percona.com/percona-operator-for-mongodb/index.html) , organizations can create a more secure, scalable, and automated environment for managing MongoDB databases.