---
title: "Join Percona for Google Summer of Code 2025 – Explore, Innovate, and Contribute!"
date: "2025-02-05T00:00:00+00:00"
tags: ["PMM", "Percona", "Opensource", "MongoDB", "GSoC"]
authors:
  - radoslaw_szulgo
images:
  - blog/2025/02/gsoc-blog-post-cover.jpg
slug: google-summer-of-code-2025
---

Are you passionate about open-source databases, AI/ML, and security? Do you want to work on real-world projects that impact thousands of developers and enterprises worldwide? Percona is excited to invite students to participate in [**Google Summer of Code 2025 (GSoC)**](https://summerofcode.withgoogle.com/) and help advance our cutting-edge open-source database solutions! 

# Why Contribute to Percona?

At Percona, we believe that **open world is a better world**! GSoC is an excellent opportunity to work with seasoned developers, gain hands-on experience, and contribute to powerful database tools used by businesses globally.

For 2025, we’re especially interested in projects that focus on **AI/ML** and **security**—two critical areas shaping the future of databases. Whether you're passionate about **automating database performance insights** with AI or **hardening security for mission-critical data**, we have exciting challenges for you!

Percona mentors are going to help you realize your ideas or one of the ideas below. We invite you to contribute to products and projects such as:

* [Percona Server for MongoDB](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

* [Percona Backup for MongoDB](https://www.percona.com/mongodb/software/percona-backup-for-mongodb)

* [Percona Operator for MongoDB](https://github.com/percona/percona-server-mongodb-operator)

* [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management)

* [pg_tde: Transparent Database Encryption for PostgreSQL](https://github.com/percona/pg_tde)

* As well as CI/CD related projects with the Percona Build Engineering.


# Project Ideas for GSoC 2025

Below are some suggested project ideas categorized by Percona software:

## Percona Server for MongoDB

### Interactive Shell Installer for Percona Software for MongoDB

This project aims to develop an interactive shell-based installer for [Percona Server for MongoDB](https://www.percona.com/mongodb/software/percona-server-for-mongodb) and [Percona Backup for MongoDB](https://www.percona.com/mongodb/software/percona-backup-for-mongodb). The installer will simplify the installation, configuration, and initial setup process, making it easy for users to deploy these open-source enterprise solutions efficiently. The primary goal is to enhance the user experience by reducing manual setup steps and ensuring proper configuration through guided prompts and automation.

**Deliverables:**

- A command-line-based interactive installer script.
- Automated dependency checks and installation.
- Interactive prompts for configuration choices (e.g., authentication, replication, sharding).
- Seamless installation of both Percona Server for MongoDB and Percona Backup for MongoDB.
- Integration with package managers for major Linux distributions (Debian, Ubuntu, RHEL, CentOS).
- Logging and validation mechanisms to ensure correct setup.
- Documentation and user guide for the installer.

**Required/preferred skills:** C++ or Go

**Duration:** 350 hours

**Difficulty level:** Medium

**Mentors**: @radoslaw.szulgo 

**Relevant repository and resources:** https://github.com/percona/percona-backup-mongodb


## Percona Backup for MongoDB

### PBM backup speed throttling

On large scale deployments, backups may significantly impact network performance - speficially network bandwidth may be heavily utilized, if the backup storage is fast, causing performance degradation of the database itself. Database reliability engineers would like to reduce the network load by slowing down physical backups with Percona Backup for MongoDB (PBM) configuration. The scope of the project is to implement a network bandwidth rate limiter and perform load testing showing the impact or rate limiting on backup time.

**Deliverables:**
The expected outcome of this project is insurance that backup will not degrade network bandwidth impacting the database. As a result a participant needs to provide proposed code changes in a form of fork of PBM and a create a report with load test results. 

- **Required/preferred skills:** Go

- **Duration:** 175 hours

- **Difficulty level:** Easy

- **Mentors**: @radoslaw.szulgo 

- **Relevant repository and resources:** 

    * https://github.com/percona/percona-backup-mongodb
    * https://github.com/percona/percona-server-mongodb


### PBM golang SDK

The project’s purpose is to extend capabilities and reduce maintenance in monitoring, managing, and automating backup and restores of MongoDB from [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management) tool. In the scope of the project there’s a migration from [Percona Backup for MongoDB](https://www.percona.com/mongodb/software/percona-backup-for-mongodb) CLI  to a dedicated PBM golang client library in PMM. The client library (aka SDK) has to be implemented and map all current CLI operations to Go API functions. As a stretch goal, the project can be extended into implementing a backup progress reporting using the created SDK.  

**Deliverables:**
The expected outcome of the project is the reduced maintenance of backup integration in PMM project and enabling extensibility of backup management. As a result of the project a new open-source SDK should be create

- **Required/preferred skills:** Go
- **Duration:** 350 hours
- **Difficulty level:** Easy
- **Mentors**: @radoslaw.szulgo 
- **Relevant repository and resources:** 
    * https://github.com/percona/percona-backup-mongodb
    * https://github.com/percona/pmm


### CEPH Storage support for PBM

Ceph is an open source Software Defined Storage(SDS) software that is massively scalable and reliable. It’s one of the most popular storage technologies in Kubernetes and Openshift. The project aims to enable users to store their Percona Backups for MongoDB data on a Ceph storage which would be very convenient as they wouldn’t need to manage other additional storages. The scope of the project includes building a workspace setup on Kubernetes and [Percona Operator for MongoDB](https://github.com/percona/percona-server-mongodb-operator), research on current challanges using Ceph storage, and implement necessary changes to make it work in a performant way. At the end document the solution. 

**Deliverables:**
The project's deliverables are technical documentation, Percona Operator for MongoDB changes, and instructions on setting up an environment with Ceph storage. 

- **Required/preferred skills:** Go, Kubernetes
- **Duration:** 175 hours
- **Difficulty level:** Easy
- **Mentors**: @radoslaw.szulgo 
- **Relevant repository and resources:** 
    * https://github.com/percona/percona-backup-mongodb
    * https://github.com/percona/percona-server-mongodb

### BoostFS storage support for PBM

Dell Data Domain Boost File System (BoostFS) provides a general file system interface to the DD Boost library, allowing standard backup applications to take advantage of DD Boost features. In this project we’d like to extend our open-source Percona Backup for MongoDB to leverage that storage technology to reduce backup and restore time - and the same time help users to reduce their Recovery Time Objective (RTO) and Recovery Point Objective (RPO).  In the scope of the project there’s a preparation of the workspace setup with Percona Server for MongoDB, Percona Backup for MongoDB and mounted BoostFS disk volumes on Google Cloud Platform and documenting the architecture of the environment. Additionally, the project includes a research on how PBM works with that storage and implementing necessary changes to PBM to make it work. Finally, a simple benchmark should be performed that proves the performance boost. 

**Deliverables:**
It is expected that project delivers an architecture diagram of the testing environment in Google Cloud Platform, implementation of required changes to support BoostFS in PBM, and report incl. performance benchmark results and comparison to other storage systems.

- **Required/preferred skills:** Go, GCP
- **Duration:** 350 hours
- **Difficulty level:** Hard
- **Mentors**: @radoslaw.szulgo 
- **Relevant repository and resources:** 
    * https://github.com/percona/percona-backup-mongodb
    * https://infohub.delltechnologies.com/en-us/l/dell-apex-block-storage-for-aws-backup-and-recovery-using-ddve-and-dd-boost-oracle-rman-agent/backup-procedure/
    * https://www.dell.com/support/manuals/pl-pl/dd-virtual-edition/dd_p_ddve-gcp_ig/purpose-of-this-guide?guid=guid-015a004c-0518-4a23-a043-39c97ed165f0&lang=en-us

### OpenStack Swift storage support for PBM

The OpenStack Object Store project, known as Swift, offers cloud storage software so that you can store and retrieve lots of data with a simple API. It's built for scale and optimized for durability, availability, and concurrency across the entire data set. Swift is ideal for storing unstructured data that can grow without bound. Swift is very convenient to use as a backup storage for MongoDB workloads running on OpenStack platform. The scope of the project includes building a workspace environment on Google Cloud Platform with OpenStack clusters and running there Percona Server for MongoDB. Then implementing required changes in Percona Backup for MongoDB to support Swift storage. Finally, performing benchmark tests and comparison to GCP native storages. 

**Deliverables:**
It is expected that project delivers an architecture diagram of the testing environment in Google Cloud Platform, implementation of required changes to support OpenStack Swift in PBM, and report incl. performance benchmark results and comparison to other storage systems. 

- **Required/preferred skills:** Go, GCP, OpenStack
- **Duration:** 175 hours
- **Difficulty level:** Medium
- **Mentors**: @radoslaw.szulgo 
- **Relevant repositories and resources:** 
    * https://github.com/percona/percona-backup-mongodb
    * https://github.com/openstack/swift
    * https://github.com/ncw/swift
    * https://cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/installing/openstack


## Percona Monitoring and Management (PMM)

### Queryable backup and restore of Percona Server for MongoDB

The project aims to equip MongoDB Database Administrators with [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management) extension that allows to query data directly from a backup. It solves their pain when they want to inspect just a single document in a collection from a few Terabytes size backup. The time associated with downloading the snapshot, decompressing it, getting it running in a local MongoDB node, and finally running the query would be significant. Not only that, but there are obvious nontrivial costs — both monetary and operational — associated with having to quickly spin up new environments. In scope of the project there is a backend Go application server implementation to run on-demand ephemeral mongodb instance, load data from backup, and enable user to run a DB query from a UI interface. 

**Deliverables:**
It’s expected to deliver source code changes to PMM in form of PMM fork that extends PMM functionality for queryable MongoDB backup.  Specifically, it is expected to prepare a solution design, implementation, unit and/or integration tests based on a Docker environment, and documentation. 

- **Required/preferred skills:** Go, MongoDB
- **Duration:** 350 hours
- **Difficulty level:** Medium
- **Mentors**: @radoslaw.szulgo 
- **Relevant repository:** 
    * https://github.com/percona/pmm
    * https://github.com/percona/percona-backup-mongodb

### Design Engineering for PMM

[Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management) is a long-standing open-source software, but its age also comes with some UX and UI debt. Facing new goals to help innovate PMM, the team is excited to look forward to starting "renovating the house" and swapping the GUI with a more modern one built in-house. We are looking for experts in design engineering to help with:
- Making/refining/cataloging UI components that we will need for QA and production;
- Creating functional prototypes ad hoc from written ideas or designs;
- Convert old PMM pages like for like into new PMM pages (with new UI).

**Deliverables:**
- Contributing with ideas to help make the code library more easy to contribute to;
- Contributing to the code library with at least one new component;
- Create at least one code prototype for one of the team's ongoing ideas;
- Convert at least one existing PMM functionality page UI into the new UI.

**Required/preferred skills:** CI/CD, Git, Storybook, React, MUI, Figma

**Duration:** 350 hours

**Difficulty level:** Medium

**Mentor**: @pedro.fernandes 

## Percona Build Engineering

### SBOMs for Percona Software for MongoDB

A “software bill of materials” (SBOM) has emerged as a key building block in software security and software supply chain risk management. An SBOM is a nested inventory, a list of ingredients that make up software components. The project aims to adapt Percona’s build pipelines to generate SBOMs for Percona Software for MongoDB. This will enable organizations using PSMDB and PBM to be more secure and avoid software supply chain vulnerabilities that were very harmful in late 2020 with the discovery of the [Solar Winds](https://www.csoonline.com/article/3601508/solarwinds-supply-chain-attack-explained-why-organizations-were-not-prepared.html) cyberattack or later with the [Log4j](https://en.wikipedia.org/wiki/Log4Shell) security flaw.

**Deliverables:**
At the end of the project, a running staging pipeline in Jenkins and Trivy should produce complete SBOMs for Percona Server for MongoDB and Percona Backup for MongoDB. SBOMs are uploaded automatically to the Percona repository and are downloadable publicly. Additionally, technical documentation on how the process works is expected to be created.

- **Required/preferred skills:** Jenkins, Trivy
- **Duration:** 175 hours
- **Difficulty level:** Easy
- **Mentors**: @radoslaw.szulgo 
- **Relevant repository and resources:** 
    * https://github.com/percona/percona-backup-mongodb
    * https://github.com/percona/percona-server-mongodb
    * https://trivy.dev/v0.33/docs/sbom/

### Evolving CI/CD: Automating Build, Test, and Release for Robust Software Delivery

Continuous Integration and Continuous Deployment (CI/CD) pipelines are the backbone of modern software development, ensuring rapid, reliable, and repeatable delivery. However, many pipelines still operate in fragmented stages, where builds and tests are automated, but releases remain a manual or semi-automated process.

This project aims to transform our CI/CD pipelines into a true end-to-end automated system, seamlessly integrating build, test, and release stages. By implementing best practices in CI/CD automation, we will ensure that only thoroughly tested software progresses to release, minimizing human intervention and reducing the risk of deployment failures.

**Deliverables:**
The successful completion of this project will result in a fully automated and robust CI/CD pipeline that seamlessly integrates build, test, and release processes. The key outcomes will include:

**Fully Automated CI/CD Pipeline**

A redesigned pipeline where builds, testing, and releases are interconnected and automated.
Code changes will automatically trigger builds, run tests, and, if successful, deploy releases without manual intervention.
Comprehensive Test Integration

The pipeline will incorporate unit tests, integration tests, security scans, and other quality assurance mechanisms.
Ensuring that faulty builds do not reach production by enforcing test-driven deployment.
Automated Release Process

A mechanism that automatically releases software only if all tests pass.
Versioning, tagging, and artifact management will be streamlined.
The release process will be documented and configurable for different environments (e.g., staging, production).
Infrastructure as Code (IaC) & Deployment Automation

**Documentation & Guides**

Clear technical documentation detailing the new pipeline’s workflow and configuration.
A step-by-step guide for developers and DevOps engineers on how to use and extend the pipeline.

- **Required/preferred skills:** CI/CDl like Jenkins, GitHub Actions, GitLab CI, or similar; Docker; Testing frameworks and automated deployment strategies; infrastructure as code (IaC) and cloud environments is a plus.
- **Duration:** 350 hours
- **Difficulty level:** Medium
- **Mentors**: @Evgeniy_Patlan , @Vadim_Yalovets 
- **Relevant repository:** https://github.com/Percona-Lab/jenkins-pipelines

### Build Automation for Open-Source Databases

Building and maintaining multiple database forks—such as MySQL, MongoDB, and PostgreSQL—often involves redundant build scripts, leading to inefficiencies, inconsistencies, and maintenance overhead. Currently, each database has its own set of build scripts despite sharing many common steps.

This project aims to develop a modular, extensible build system that allows for streamlined compilation and packaging of different database forks. The system will provide a flexible framework where users can select required modules, specify target OS distributions, and automate the build process with minimal configuration.

By implementing a plugin-based architecture, this modular builder will simplify cross-database maintenance, reduce duplication, and improve consistency across different builds.

**Deliverables:** 

- Modular Build Framework – A reusable, pluggable system that dynamically selects required modules for MySQL, MongoDB, and PostgreSQL builds.

- Multi-OS Support – Automated builds for multiple Linux distributions (Debian, Ubuntu, CentOS, RHEL) with configurable OS selection.

- Automated Package Creation – DEB and RPM package generation with standardized versioning and tagging.

- Configurable & Scalable Builds – Easy customization of build parameters, allowing extension to new database forks or patches.

- CI/CD Integration – Optional support for Jenkins, GitHub Actions, or GitLab CI to enable fully automated builds.

- Comprehensive Documentation – User and developer guides with example configurations for quick adoption and extension.


**Required/preferred skills:** Bash/Python, CMake, Makefiles, Autotools, Linux and packaging (DEB/RPM), dependency management, CD/CD tools are a plus

**Duration:** 175 hours

**Difficulty level:** Medium

**Mentors**: @Evgeniy_Patlan , @Vadim_Yalovets 

**Relevant repositories**:

* https://github.com/percona/percona-server-mongodb 
* https://github.com/percona/percona-xtradb-cluster
* https://github.com/percona/percona-server

----

*More ideas are coming soon!*

Suggest your ideas in the comments of the post or on [the forum]((https://forums.percona.com/t/google-summer-of-code-2025-project-ideas/36461)).

----

GSoC isn’t just about working on predefined ideas—it’s about innovation! If you have a project idea that aligns with **Percona software, AI/ML, security, or database performance**, submit your proposal, and our mentors will be happy to discuss it with you.

**Do you have questions?** Visit our [Community Forum](https://forums.percona.com/t/google-summer-of-code-2025-project-ideas/36461) or join our chat channels to connect with potential mentors.

**Ready to get started?** See our [Google Summer of Code 2025: Contribution guide](https://forums.percona.com/t/google-summer-of-code-2025-contribution-guide/36420).

See you in GSoC 2025!