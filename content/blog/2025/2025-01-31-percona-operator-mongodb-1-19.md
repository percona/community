---
title: "Percona Operator for MongoDB 1.19: Remote Backups, Auto-Generated Passwords, and More!"
date: "2025-01-31T00:00:00+00:00"
tags: ['Percona', 'opensource', 'Kubernetes', 'MongoDB']
categories: ["Cloud"]
authors:
  - sergey_pronin
  - daniil_bazhenov
images:
  - blog/2025/01/operator-1-19.jpg
---

The latest release of the [Percona Operator for MongoDB](https://docs.percona.com/percona-operator-for-mongodb/index.html), [version 1.19](https://docs.percona.com/percona-operator-for-mongodb/RN/Kubernetes-Operator-for-PSMONGODB-RN1.19.0.html), is here. It brings a suite of enhancements designed to streamline your MongoDB deployments on Kubernetes. This release introduces a technical preview of remote file server backups, simplifies user management with auto-generated passwords, supports Percona Server for MongoDB 8.0, and includes numerous other improvements and bug fixes. Let's dive into the details of what 1.19 has to offer.

## Remote Backups with Network File System (Technical Preview)

Backing up your MongoDB data is crucial, and Percona Operator for MongoDB 1.19 introduces a powerful new option for backup storage: the filesystem type. This feature, currently in technical preview, allows you to leverage a remote file server, mounted locally as a sidecar volume, for your backups. This is particularly useful in environments with network restrictions that prevent the use of S3-compatible storage or for organizations using non-standard storage solutions that support the Network File System (NFS) protocol.

### Setting Up Remote Backups

To use this new capability, you'll need to add your remote storage as a sidecar volume within the replsets section of your Custom Resource (and configsvrReplSet for sharded clusters). Here's how:

```
replsets:
  ...
  sidecarVolumes:
  - name: backup-nfs-vol
    nfs:
      server: "nfs-service.storage.svc.cluster.local"
      path: "/psmdb-my-cluster-name-rs0"
  ...
```

Then, configure the mount point and sidecar volume name in the `backup.volumeMounts` section:

YAML:
```
backup:
  ...
  volumeMounts:
  - mountPath: /mnt/nfs/
    name: backup-nfs-vol
  ...
```

Finally, set up a filesystem type storage in the backup.storages section, pointing it to the mount point:

YAML:
```
backup:
  enabled: true
  ...
  storages:
    backup-nfs:
      type: filesystem
      filesystem:
        path: /mnt/nfs/
```

See more in our [documentation about this storage type](https://docs.percona.com/percona-operator-for-mongodb/backups-storage.html#remote-file-server).

## Simplified User Management with Auto-Generated Passwords

Managing user credentials just got easier. Percona Operator for MongoDB 1.19 enhances declarative management of custom MongoDB users by adding the ability to generate passwords automatically. Now, when defining a new user in your deploy/cr.yaml file, you can omit the reference to an existing Secret containing the password, and the Operator will handle the generation for you:

YAML:
```
...
users:
  - name: my-user
    db: admin
    roles:
      - name: clusterAdmin
        db: admin
      - name: userAdminAnyDatabase
        db: admin
```

The Operator will create a Secret to store the generated password securely. It is important to note that the Secret will be created after the cluster is in the Ready state. 

Get the user credentials:
Find the Secret resource named <cluster-name>-custom-user-secret
Get the user password with this one-liner:

```
kubectl get secret my-cluster-name-custom-user-secret -o jsonpath='{.data.my-user}' | base64 -d
```

You can find more details on this automatically created Secret in our [documentation](https://docs.percona.com/percona-operator-for-mongodb/users.html#custom-mongodb-roles).

## Percona Server for MongoDB 8.0 Support

Staying up-to-date with the latest MongoDB versions is essential for performance and security. Percona Operator for MongoDB 1.19 now officially supports Percona Server for MongoDB 8.0, in addition to 6.0 and 7.0. This means you can leverage the latest features and improvements from MongoDB 8.0, combined with the enterprise-grade enhancements and open-source commitment of Percona Server for MongoDB.

![Percona Server for MongoDB 8.0 Support](blog/2025/01/operator-mongodb-8.png)

Check out [this blog post](https://www.percona.com/blog/percona-server-for-mongodb-8-0-most-performant-ever/) to learn more about the features in MongoDB 8.0.

## Streamlined AWS S3 Access with IAM Roles for Service Accounts (IRSA)

Percona Operator for MongoDB 1.19 adds support for [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html), simplifying secure access to AWS S3 for backups on Amazon EKS. IRSA lets you grant granular S3 permissions to specific Pods via their associated Kubernetes service accounts. This approach ensures that only the Pods that require S3 access receive it, adhering to the principle of least privilege. Furthermore, each Pod can only access credentials linked to its service account, providing strong credential isolation. For enhanced security, all S3 access is tracked through AWS CloudTrail, enabling comprehensive auditability. All of this happens without the need to manually manage and distribute AWS credentials.

Configuration Steps

1.  Create an IAM Role: Define an IAM role with S3 access permissions. See [AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).

2.  Identify Service Accounts: The Operator uses percona-server-mongodb-operator and your cluster uses default (customizable in deploy/cr.yaml).

3. Annotate Service Accounts: Link the IAM role to both service accounts:
    
    ```
    $ kubectl -n <cluster namespace> annotate serviceaccount default eks.amazonaws.com/role-arn: <YOUR_IAM_ROLE_ARN> --overwrite
    $ kubectl -n <operator namespace> annotate serviceaccount percona-server-mongodb-operator eks.amazonaws.com/role-arn: <YOUR_IAM_ROLE_ARN> --overwrite
    ```

4. Configure S3 Storage: Set up S3 storage in deploy/cr.yaml without s3.credentialsSecret. The Operator will use IRSA.


Important: IRSA credentials take precedence over IAM instance profiles, and S3 credentials in a Secret override both.

IRSA streamlines S3 access, enhancing security and manageability for your MongoDB backups on EKS. Learn more in our [documentation](https://docs.percona.com/percona-operator-for-mongodb/backups-storage.html#automating-access-to-amazon-s3-based-on-iam-roles).

## Conclusion

Percona Operator for MongoDB 1.19 delivers a significant step forward in simplifying and automating the management of your MongoDB clusters on Kubernetes. With features like remote backups, auto-generated passwords, and support for Percona Server for MongoDB 8.0, this release empowers you to deploy, manage, and scale your databases with greater ease and efficiency.

We encourage you to explore the [full release notes](https://docs.percona.com/percona-operator-for-mongodb/RN/Kubernetes-Operator-for-PSMONGODB-RN1.19.0.html) and try out the new features. As always, your feedback is invaluable to us. Please share your thoughts and contribute to the project on our [GitHub repository](https://github.com/percona/percona-server-mongodb-operator) or our [Community Forum](https://forums.percona.com/c/mongodb/percona-kubernetes-operator-for-mongodb/29).

