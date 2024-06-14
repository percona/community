---
title: "Let's take a look at Percona Everest 1.0.0 RC"
date: "2024-06-14T00:00:00+00:00"
tags: ['Percona Everest', 'opensource', 'Kubernetes', 'MySQL', 'PostgreSQL', 'MongoDB']
description: "Percona Everest is the first open source cloud-native platform for provisioning and managing PostgreSQL, MongoDB and MySQL database clusters."
authors:
  - daniil_bazhenov
images:
  - blog/2024/06/percona-everest-1-rc-cover.png
---

Hi, the Percona Everest 1.0.0-rc1 release was published on [GitHub](https://github.com/percona/everest/releases).

[Percona Everest](/projects/everest/) is the first open source cloud-native platform for provisioning and managing PostgreSQL, MongoDB and MySQL database clusters.

I want to tell you how to install it so you can try it out. 

**RC builds aren't meant for the general public; we don't support upgrading from RC to stable versions. This means that this is only for testing and familiarizing yourself with the features. RC builds are not stable and are often buggy. There will be no upgrade. :)**

To get started, you will need a Kubernetes cluster. Right now, [Percona Everest](https://docs.percona.com/everest/index.html) is in Beta. Don't use production clusters; use test clusters in the cloud like GKE or local in Minikube, k3d, or Kind. 

I created a test cluster in GKE with the command:

`gcloud container clusters create test-everest-rc --project percona-product --zone us-central1-a --cluster-version 1.27 --machine-type n1-standard-4 --num-nodes=3`

Delete it after the test with the command:

`gcloud container clusters delete test-everest-rc --zone us-central1-a`

Now, we need [Everest CLI](https://docs.percona.com/everest/install/installEverestCLI.html) for the RC version; [download](https://github.com/percona/everest/releases) it from GitHub for your operating system.

![Percona Everest 1.0.0-RC1 GitHub](blog/2024/06/percona-everest-1-rc-github.png)

I downloaded it, renamed it to `everestctl`, and copied it to a folder for experimentation. 

Now, we need to make it executable 

`chmod +x ./everestctl`

Let's check that everestctl works and that we have the correct version.

`./everestctl version`

We can now install Percona Everest.

`./everestctl install --version-metadata-url https://check-dev.percona.com`

Note that I use the `--version-metadata-url parameter https://check-dev.percona.com`; this is required for RC builds.

During the installation process, you must set one or more namespaces and databases.

![Percona Everest 1.0.0-RC1 Install](blog/2024/06/percona-everest-1-rc-install.png)

Once the installation is complete, the new user authentication feature is the first significant change. You will be offered two commands.

Command to retrieve the admin user password that was generated automatically during installation:

`./everestctl accounts initial-admin-password`

Command to set a new password:

`./everestctl accounts set-password --username admin`

![Percona Everest 1.0.0-RC1 Admin Password](blog/2024/06/percona-everest-1-rc-admin-pass.png)

Now that we know the admin user password, we can open Percona Everest in a browser. Run the following command to use kubectl port forwarding to connect to Percona Everest without exposing the service:

`kubectl port-forward svc/everest 8080:8080 -n everest-system`

More information in [the documentation](https://docs.percona.com/everest/install/installEverest.html)

![Percona Everest 1.0.0-RC1 Port Forward](blog/2024/06/percona-everest-1-rc-port.png)

Now you can open localhost:8080 in your browser and use admin and password to log in.

![Percona Everest 1.0.0-RC1 User Authentication](blog/2024/06/percona-everest-1-rc-login.png)

Create a PostgreSQL cluster to test how it works. 

![Percona Everest 1.0.0-RC1 Create PostgreSQL](blog/2024/06/percona-everest-1-rc-db.png)

![Percona Everest 1.0.0-RC1 PostgreSQL](blog/2024/06/percona-everest-1-rc-postgres.png)

You can also create other databases, set up backups, and monitoring with [PMM](https://www.percona.com/open-source-database-monitoring-tools-for-mysql-mongodb-postgresql-more-percona). By the way, PMM has some cool [new dashboards](https://www.percona.com/blog/postgresql-monitoring-with-percona-monitoring-and-management-a-redefined-summary/) in the Experimental section.

Your feedback would be greatly appreciated. Create a new topic on [the forum](https://forums.percona.com/c/percona-everest/81) or issue on [GitHub](https://github.com/percona/everest/issues).

*Don't forget to delete the test cluster to save your budget.*

Thank you very much.
