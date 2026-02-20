---
title: "Building and Running Percona Everest From Source Code"
date: "2023-10-30T00:00:00+00:00"
description: "Digging deeper into the architecture of an open source product"
draft: false
tags: ["Percona Everest", "Kubernetes", "Opensource", "DBaaS"]
categories: ['Cloud']
authors:
  - daniil_bazhenov
images:
  - blog/2023/10/everest-cover.jpg
---

_Digging deeper into the architecture of an open source product_

Recently, Percona team [announced](https://www.percona.com/blog/announcing-the-alpha-release-of-percona-everest-an-open-source-private-dbaas/) the public alpha version of a new open source product – Percona Everest. It allows you to create database clusters on Kubernetes cluster.

I have installed Percona Everest several times and tried its features. Standard installation is very simple and [takes a few minutes](https://docs.percona.com/everest/quickstart-guide/qs-overview.html).

But, to understand the product deeper, I came up with the idea to explore repositories, build and run Percona Everest from source.

In this post, I will explain what I did step by step and what components and frameworks are used in the development of Percona Everest.

## Architecture, components, and tools

At the top level, we have two components or tools on the user side: Percona Everest App and everestctl CLI tool.

The Percona Everest App is a basic application that provides a web interface for database creation and management functions. Percona Everest App can be installed on your computer or remote server. The App consists of two major components:

* Frontend is a browser-based application providing a web interface for managing clusters and interacting with backend APIs. It is developed with React and TypeScript.

* Backend API that process requests from frontend, interact with Kubernetes clusters and databases. It is developed on Golang and PostgreSQL as a database.

everestctl is a CLI tool for provisioning of Percona Everest on Kubernetes clusters. It is used to install Percona Everest components such as database operators on the Kubernetes cluster. It is developed in Golang and is provided as a ready-made executable, but, in this post, we will also build it from source code.

Remember that normally, when you install Percona Everest following the instructions in the documentation, the frontend and backend are built and integrated into a single container and run as a single unit.

Let's get started with our experiments.

## Frontend installation and launch

Percona Everest Frontend is developed using the Bit framework.

[Bit](https://bit.dev/) is an open source toolchain for the development of composable software using React library and TypeScript.

Bit is used by about 100K developers, 250+ community plugins and has 16K+ stars on [GitHub](https://github.com/teambit/bit).

### Clone the Frontend repository

You need to clone a repository with the Percona Everest frontend:
[https://github.com/percona/percona-everest-frontend](https://github.com/percona/percona-everest-frontend)

`git clone git@github.com:percona/percona-everest-frontend.git`

### Install Bit

Bit requires the npm package manager to install. [npm](https://www.npmjs.com/) is a popular registry of JavaScript packages and libraries. The npm registry contains over 800,000 code packages. Open source developers use npm to share software. Installing npm on your operating system is straightforward. I'm sure you can handle it. It installs along with Node.js.

Open the Percona Everest Frontend source directory and run the following commands.

```
npm i -g @teambit/bvm
```
```
bvm install 1.0.0
```
```
bit install --recurring-install
```

![Percona Everest Frontend](blog/2023/10/everest-frontend.png)

### Launching the frontend application

Moving forward, we have two options:

* Run the frontend application using Bit.

* Build a ready application and copy it to the backend.

The Percona Everest frontend repository contains versioning branches `release-[version]` and the current version in development in the main branch. We will run the latest dev version from main.

Let's run the command:

```
bit run everest --skip-watch
```

As a result, we can open `localhost:3000` in the browser.

The Frontend is now built, and we can move on to the Backend.

![Percona Everest Frontend Run](blog/2023/10/everest-front-run.png)

![Percona Everest Frontend Result](blog/2023/10/everest-front-run-result.png)


### Additional information

There is the other way to build a frontend to work with backend. You will need two commands:

```
bit snap --build
```
```
bit artifacts percona.apps/everest --out-dir build
```

In this case, the build will be done to the folder:

`build/percona.apps_everest/artifacts/apps/react-common-js/everest/public/`

You need to copy all the files to the `public/dist` folder of the backend repository. We will talk about backend in the next section.

The installation process may change over time, so I recommend to keep track of the up-to-date commands in the files:

* README.md

* Makefile

* CI/CD of GitHub configuration, file `.github/workflows/ci.yml` in the repository.

## Backend

So we've launched Frontend, and now it shows an error because it sends requests to the Backend API, and we don't have it yet.

We will need to clone the repository with Percona Everest Backend

[https://github.com/percona/percona-everest-backend](https://github.com/percona/percona-everest-backend)

Percona Everest Backend is developed in Golang using [the Echo framework](https://echo.labstack.com/). [The Echo repository](https://github.com/labstack/echo) has over 26k stars on GitHub.

Generally, it is an API that interacts with the frontend, processing requests and sending them to the Kubernetes cluster.

Let's get it up and running.

### Run PostgreSQL locally

You need Docker to run it. I hope you have [Docker](https://www.docker.com/) installed.

Let's run one of the two commands in the repository directory:

```
make local-env-up
```
or
```
docker-compose up --detach --remove-orphans
```

![Percona Everest Backend](blog/2023/10/backend-docker-pg.png)

![Percona Everest Backend](blog/2023/10/backend-docker-pg-desktop.png)

Using Docker for this process will be replaced by Kubernetes. You can see the YAML manifest in the file:

`/deploy/quickstart-k8s.yaml`

### Launch the Go app

We have two options, I use:

```
go run cmd/main.go
```

But you can also use:

```
make run-debug
```

Starting with version 0.4.0, you will need to add the SECRETS_ROOT_KEY environment variable before starting the application. The secret key must be used on restarts if you do not start from the scratch.
`export SECRETS_ROOT_KEY=$(openssl rand -base64 32)`

![Percona Everest Backend Go Run](blog/2023/10/backend-go-run.png)

Now we can open the localhost:3000 in the browser again and check that the backend is running. But we see that we have no Kubernetes clusters connected and configured.

![Percona Everest Backend Go Result](blog/2023/10/backend-go-run-result.png)

## Everestctl and Kubernetes cluster

Another important component of Percona Everest is everestctl. [everestctl](https://github.com/percona/percona-everest-cli/) is a CLI tool responsible for provisioning Percona Everest on Kubernetes clusters.

We will need:

* Kubernetes cluster

* Build and run everestctl

### Preparation of the Kubernetes Cluster

You can use Kubernetes Cluster on AWS, Google Cloud, or minikube.

The Percona Everest documentation says:

_You must have a publicly accessible Kubernetes cluster to use Percona Everest. EKS or GKE is recommended, as it may be difficult to make it work with local installations of Kubernetes such as minikube, kind, k3d, or similar products._

The documentation provides instructions on how to run the test cluster

* [Create Kubernetes cluster on Amazon Elastic Kubernetes Service (EKS)](https://docs.percona.com/everest/quickstart-guide/eks.html)

* [Create Kubernetes cluster on Google Kubernetes Engine (GKE)](https://docs.percona.com/everest/quickstart-guide/gke.html)

In this post, we use [minikube](https://minikube.sigs.k8s.io/docs/start/) which is preliminarily installed.

[The Makefile](https://github.com/percona/percona-everest-backend/blob/main/Makefile) of [the Percona Everest Backend repository](https://github.com/percona/percona-everest-backend) contains the `make k8s` command to start the cluster in minikube.

Let's open the directory of the backend repository and launch minikube:

```
make k8s-macos
```

or
```
make k8s
```

![Percona Everest Backend Minikube](blog/2023/10/everest-minikube.png)

As a result, I see in the console this message:

```
🏄 Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

I also see that I have a minikube cluster with three nodes. It is time to install Percona Everest components using everestctl.

```
➜  percona-everest-backend git:(main) ✗ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   3m44s   v1.26.3
minikube-m02   Ready    <none>          3m22s   v1.26.3
minikube-m03   Ready    <none>          3m3s    v1.26.3
```

### Build everestctl

Let's clone the repository: [https://github.com/percona/percona-everest-cli/](https://github.com/percona/percona-everest-cli/)

Open the repository folder and run build:

```
make build
```

everestctl is built in the binary file `/bin/everest`

Grant execution privileges

```
chmod +x ./bin/everest
```

Let's run the Percona Everest installation:

```
./bin/everest install operators
```

That command will start the installation wizard.

I will leave all default values, just pressing Enter. Otherwise, you can experiment with the settings, it is your choice.

![Percona Everest Wizard](blog/2023/10/everest-wizards.png)

As a result, the following processes will run on the cluster:

Creating namespace percona-everest.

* Installing Operator Lifecycle Manager (OLM).

* Installing [Percona OLM Catalog](https://github.com/percona/everest-catalog).

* Installing Percona Operators for the databases selected in the wizard.

* Installing [everest-operator](https://github.com/percona/everest-operator) operator.

* Creating services and roles.

That's it! We've installed Percona Everest completely. You can open it in a browser and create a database.

![Percona Everest Start](blog/2023/10/everest-finish-start.png)

![Percona Everest Create DB](blog/2023/10/everest-create-db.png)

## What's next?

Try creating databases with different configurations.

![Percona Everest Create DB](blog/2023/10/everest-dbs.png)

Repeat the installation with a different cluster or settings.

If you face any problems or have ideas on how to improve components, create Issues on GitHub in the appropriate repositories.

### Stop and remove Percona Everest

Once you finished your experiments, you can:

* Stop Frontend - stop Bit running by pressing CTRL+C in the console.

* Stop Backend API - stop Golang script by pressing CTRL+C in the console.

* Stop and remove PostgreSQL in Docker - run `make local-env-down` in the backend repository, or use Docker Desktop to stop.

* Remove Kubernetes cluster.

### Updates

Every day, developers make changes to the code and publish to repositories on GitHub.

You can stop the component, pull the changes with `git pull`, and start a new version. It's just for experimentation and development. Some versions of components will not be compatible; uninstall all components and start over using the appropriate versions. Detailed instructions on how to upgrade will appear later.

You can see changes to the build process or parameters in the repositories.

### Couple of useful commands

List of databases
```
kubectl -n percona-everest get db
```
List of pods
```
kubectl -n percona-everest get pods
```
### Conclusion

I hope you were able to make it this far, and it was interesting for you.

I'd love if you leave your feedback in the comments.
