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

* [Percona XtraDB Cluster](https://github.com/percona/percona-xtradb-cluster)

* [Percona Server for MySQL](https://github.com/percona/percona-server)

* [Percona Distribution for PostgreSQL](https://github.com/percona/postgres)

* [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator)

* [Percona Server for MongoDB](https://www.percona.com/mongodb/software/percona-server-for-mongodb)

* [Percona Backup for MongoDB](https://www.percona.com/mongodb/software/percona-backup-for-mongodb)

* [Percona Operator for MongoDB](https://github.com/percona/percona-server-mongodb-operator)

* [Percona Everest](https://github.com/percona/everest) 

* [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management)

* [pg_tde: Transparent Database Encryption for PostgreSQL](https://github.com/percona/pg_tde)

* As well as CI/CD related projects with the Percona Build Engineering.


# Project Ideas for GSoC 2025

Below are some suggested project ideas categorized by Percona software:


## Percona Distribution for PostgreSQL

### Snapshot-based PostgreSQL backups

Database users are often very familiar with their storage provider's storage snapshot capabilities. These snapshots are very handy and performant to use, hence their popularity among users. Backups for other databases (e.g., MongoDB) are often configured via this capability as it provides many performance benefits for large-scale data, especially on Cloud deployments. Having such technology supported across the backup solutions for multiple databases makes it possible to leverage this effectively for Percona Everest via the Percona Operators.

[Comments from Crunchy](https://www.crunchydata.com/blog/postgresql-snapshots-and-backups-with-pgbackrest-in-kubernetes) on what needs to be glued together to get snapshots and pgBackRest working together better. Additionally, [Timescale on how they use snapshots and pgBackRest together in their hosted managed service](https://www.timescale.com/blog/making-postgresql-backups-100x-faster-via-ebs-snapshots-and-pgbackrest).

**Deliverables**:
Have an API available to Percona Distribution for PostgreSQL to effectively use storage snapshots to create backups and restore from storage snapshot-based backups. Preferably, have it added to/complementary to the currently recommended solution of pgBackRest.

Have Percona Operator for PostgreSQL expose the storage snapshot-based backup/restore so that Percona Everest can leverage it.

**Required/preferred skills:** C++, PostgreSQL, Kubernetes
**Duration:** 350 hours
**Difficulty level: **Hard
**Mentors:** @Andrew_Pogrebnoi, @Jan_Wieremjewicz
**Relevant repository and resources:**

* [GitHub - percona/percona-postgresql-operator: Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator)
* [GitHub - percona/postgres: Percona Server for PostgreSQL](https://github.com/percona/postgres)

### pgBackRest to Barman close gap improvements

PostgreSQL has two main backup tools: Barman and pgBackRest. Both are powerful backup and restore tools, each with its own strengths. pgBackRest is generally considered more advanced in terms of parallelism, performance, and flexibility. Barman does offer some advantages in certain areas. While pgBackRest is maintained by Community, Barman is a tool mainly maintained by one company and is less popular. Barman does have UX improvements over pgBackRest, especially for non-expert users:

* direct WAL archiving with PostgreSQL’s built-in archive_command,
* simpler backup and recovery process, especially for standby creation,
* clearer logging and monitoring for backup integrity,
* simpler configuration in small to medium deployments,
* better native tools for cloud backups

It would be beneficial for Percona, which uses pgBackRest in the Percona Distribution for PostgreSQL, to have the backup tool close any functionality gaps in Barman. Percona customers sometimes use Barman and expect Percona to support it. Having a way to migrate off Barman to pgBackRest, reducing any potential friction for the users, would be beneficial.

**Deliverables:**
Provide a close-gap set of improvements based on the list available in the description

**Required/preferred skills:** C++, PostgreSQL
**Duration:** 350 hours
**Difficulty level:** Hard
**Mentors:** @Andrew_Pogrebnoi, @Jan_Wieremjewicz
**Relevant repository and resources:**
* [GitHub - percona/postgres: Percona Server for PostgreSQL](https://github.com/percona/postgres)


### Tool to investigate PostgreSQL locks for dummies

Currently, there is no tool that allows users with low experience to detect and understand all types of locks on their PG database, which may lead to many issues in deployments not managed by expert PostgreSQL users. As described in the blog posts below, understanding how locks work is difficult:

* [Anatomy of Table-Level Locks in PostgreSQL](https://xata.io/blog/anatomy-of-locks)
* [Anatomy of table-level locks: Reducing locking impact](https://xata.io/blog/anatomy-of-locks-reduce)

**Deliverables:**

1. Detect ddl with mixed strong locks and others. i.e. allow to review locked PIDs as pg_locks will not work
2. Present all locks in a GUI
3. (Streched) have the GUI integrated in PMM

**Required/preferred skills:** C++, PostgreSQL
**Duration:** 350 hours
**Difficulty level:** Medium
**Mentors: **Kai Wagner, @Jan_Wieremjewicz
**Relevant repository and resources:**

* [GitHub - percona/postgres: Percona Server for PostgreSQL](https://github.com/percona/postgres)

### Session continuity for PgBouncer for the zero downtime upgrades

Percona is looking to introduce zero downtime upgrades capability to the Percona Operator and later on to Percona Everest. The assumption is to base on pgBouncer and our HA solution utilizing the replica with the new database and a switch from the previous version to the new version.

Such a solution provides a zero downtime upgrade capability and a Rollback capability. To provide true zero downtime major upgrades for the current Percona Distribution for PostgreSQL, there needs to be an improvement that takes over the switching of sessions between the databases: the previous version and the new version

In the future, this tool should also make it possible to zero downtime and migrate to Everest.

**Deliverables:**
Extend pgBouncer to ensure that the sessions can be switched between the databases without downtime for the users but only a potential performance drop

**Required/preferred skills:** C++, Kubernetes
**Duration:** 175 hours
**Difficulty leve**l: Hard
**Mentors: **Kai Wagner, @Jan_Wieremjewicz
**Relevant repository and resources:**
* [GitHub - percona/postgres: Percona Server for PostgreSQL](https://github.com/percona/postgres)

## Percona Software for MongoDB

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


### Percona Backup for MongoDB backup speed throttling

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


### Percona Backup for MongoDB Golang SDK

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


### CEPH Storage support in Percona Backup for MongoDB

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

### BoostFS storage support in Percona Backup for MongoDB

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

### OpenStack Swift storage support in Percona Backup for MongoDB

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

## Percona Server for MySQL and Percona XtraDB Cluster

### Automating Code Merges with AI

The regular and manual merge from Oracle’s GitHub repository process is time-consuming, complex, and prone to errors, particularly due to merge conflicts. Careful attention is required to avoid introducing regressions into Percona’s open-source products. While this project is specific to Percona’s needs, it addresses a common challenge in open-source software development, as many projects rely on upstream repositories for their code. Therefore, the solution can be generalized and could benefit other open-source projects with similar code integration needs.

This GSoC project aims to develop an intelligent system using Artificial Intelligence to automate the MySQL fork merge process. Percona has been performing these merges for 18 years, accumulating a wealth of historical data (code changes, merge resolutions, conflict histories, test results) that can be leveraged to train an AI model.

The core objective is to create a tool that can:

* Analyze upstream changes: Process and understand the changes introduced by Oracle in their MySQL repository.
* Identify merge conflicts: Identify conflicts between upstream changes and Percona’s modifications.
* Suggest merge resolutions: Propose solutions for resolving identified conflicts, drawing on patterns from historical merge data.
* Automate merges: Automatically apply upstream changes with the suggested merge resolutions.
* Learn and adapt: Continuously improve its performance and accuracy by learning from new merge data and feedback.

**Deliverables:**

* Reduced merge time and effort: Automating the merge process will free up developer time for other critical tasks.
* Improved merge accuracy: AI can potentially identify subtle conflicts that might be missed by manual review.
* Faster release cycles: Streamlining the merge process will enable quicker releases of updated Percona products.
* Open-source contribution: The resulting tool will be open-sourced, benefiting other projects that maintain forks of MySQL or similar databases. This problem is not unique to Percona; other open-source projects facing similar merging challenges can utilize this solution.

As a result of this project, you’re expected to deliver:

* A working prototype of the AI-powered merge tool.
* Well-documented code and training data.
* Comprehensive test suite and evaluation results.
* A report detailing the project’s methodology, findings, and future directions.

**Required/preferred skills:** Python, Machine Learning libraries and frameworks (e.g., TensorFlow, PyTorch, scikit-learn), C++, Git, database systems
**Duration:** 350 hours
**Difficulty level:** Hard
**Mentors:** Julia Vural, Oleksiy Lukin
**Relevant repositories and resources:**
* [GitHub - percona/percona-server: Percona Server](https://github.com/percona/percona-server)
* [GitHub - percona/percona-xtradb-cluster: A High Scalability Solution for MySQL Clustering and High Availability](https://github.com/percona/percona-xtradb-cluster)
* [https://github.com/mysql/mysql-servermetal/docs/installing/openstack](https://github.com/mysql/mysql-servermetal/docs/installing/openstack)

## Percona Everest

### Easier Troubleshooting on database clusters in Percona Everest
The main goal is to provide tools to Percona Everest users to troubleshoot database clusters. This project will require the implementation of log collection, rotation, UI, and possibly an AI helper to analyze those logs. If users have a centralized log collection implemented, this tool needs to be able to integrate with it.

**Deliverables:**

Full user flow to support database cluster troubleshooting process (UI, backend, API, integrations).

* Log Collection & Rotation System:
  * Implement a mechanism to collect logs from Percona Everest-managed database clusters.
  * Ensure efficient log rotation to manage storage and performance impact.
  * Enable compatibility with external log aggregation tools (e.g., Elasticsearch, Grafana Loki, or OpenTelemetry)
* User Interface for Log Access:
  * Develop a UI within Percona Everest to allow users to view and analyze logs.
  * Include search, filtering, and visualization options for better troubleshooting.
* AI-Powered Log Analysis (Stretched scope)
  * Explore AI-driven log analysis to provide users with insights, anomaly detection, and recommendations.
  * Implement basic AI-assisted troubleshooting if feasible within the project timeline.
* Documentation & Testing:
  * Deliver user and developer documentation covering installation, usage, and troubleshooting.
  * Include test cases and automation scripts to ensure system reliability.

**Required/preferred skills:** Kubernetes, Go, CI/CD
**Duration:** 350 hours
**Difficulty level: **Medium
**Mentors:** @Diogo_Recharte, @Mayank_Shah
**Relevant repository and resources:** [https://github.com/percona/everest](https://github.com/percona/everest)

### Percona Everest RBAC policies management UI

Create a user interface to create and manage role-based access control policies

**Deliverables:**

* Role-Based Access Control (RBAC) UI:
  * Develop a user-friendly interface in Percona Everest to create, update, and manage RBAC policies.
  * Implement role assignment and permission configuration for database clusters.
* Documentation & Testing:
  * Deliver comprehensive user and developer documentation.
  * Include test cases and automation scripts to ensure reliability.

**Required/preferred skills:** Front-end, CI/CD tools
**Duration:** 90 hours
**Difficulty level:** Medium
**Mentors:** @Diogo_Recharte, Peter Szczepaniak
**Relevant repository and resources:** [https://github.com/percona/everest](https://github.com/percona/everest)

### Context sensitive help
The Percona Everest documentation contains valuable information, hints, and tips, but we lack a way to present relevant information to our users. This project aims to work with the UX and Docs teams to solve this problem.

**Deliverables:**

* Implement a mechanism to display relevant documentation, hints, and tips based on the user’s current action or screen within Percona Everest.
* Ensure seamless integration with the existing UI for a non-intrusive experience.
* Enable contextual tooltips, pop-ups, or side panels that present relevant documentation without requiring users to leave the interface.
* Support links to full documentation pages when needed.
* Optionally, explore AI-driven suggestions based on user behavior and past queries.
* Allow users to control the level of help they receive (e.g., enable/disable tips, adjust verbosity).
* Provide user and developer documentation on how the system works and how to extend it.
* Ensure thorough testing to validate the accuracy and relevance of displayed help content.

**Required/preferred skills:** Front-end, CI/CD tools
**Duration:** 175 hours
**Difficulty level:** Medium
**Mentors:** @Diogo_Recharte, Peter Szczepaniak
**Relevant repository and resources:** [https://github.com/percona/everest](https://github.com/percona/everest)

### Backups and restore timeline visualization

Databases are usually long-living services, and investigating issues with them is easier when you can see events like backups and restores of this service on a timeline.

**Deliverables:**

* Develop a visual timeline within Percona Everest to display backup and restore events for database clusters.
* Ensure the timeline is intuitive, zoomable, and supports different time ranges (e.g., last 24 hours, 7 days, custom range).
* Retrieve and display backup and restore events from Percona Everest’s database and logs.
* Include metadata such as timestamps, duration, status (success, failure), and associated users or processes.
* Allow users to filter events by type (full backup, incremental backup, restore, etc.).
* Enable color-coding or icons to differentiate event types at a glance.
* Deliver comprehensive user and developer documentation.
* Ensure automated tests for data accuracy, UI performance, and usability.

**Required/preferred skills:** Front-end, CI/CD tools
**Duration:** 175 hours
**Difficulty level:** Medium
**Mentors:** @Diogo_Recharte, Peter Szczepaniak
**Relevant repository and resources:** [https://github.com/percona/everest](https://github.com/percona/everest)

### Refactor test automation using page object model

Our project currently has a functional end-to-end (E2E) UI test suite that ensures the stability and correctness of our application. However, the test suite does not follow the Page Object Model (POM) design pattern, making it harder to maintain, scale, and debug.

**Deliverables:**

* Restructure existing test automation to follow the Page Object Model (POM) design pattern.
* Ensure better separation of test logic and UI elements for improved maintainability.
* Implement modular and reusable page object classes for different UI components and workflows.
* Standardize naming conventions and best practices for test scripts.
* Improve error handling and logging to make test failures easier to diagnose.
* Ensure the refactored test suite runs efficiently in CI/CD pipelines.
* Validate test performance improvements and maintain test coverage.

Required/preferred skills: Playwright, Typescript, Kubernetes
Duration: 175 hours
Difficulty level: Medium
Mentors: @Diogo_Recharte, Tomislav_Plavcic, Edith Puclla
**Relevant repository and resources:** [https://github.com/percona/everest](https://github.com/percona/everest)

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

### PMM UI for PostgreSQL backups - create, restore, check, monitor
Backup management without UI is not an easy task for the users. Having a tool that could be a tool of choice for backup and restore management could provide a unification layer for multiple backup/restore tools as well as provide a very important value that’s often overlooked: backup monitoring.

As it turns out, many DBAs are often worried about the state of their backups and make it a daily routine task to check how the backups they have configured are. As the environments scale, this task becomes increasingly tiresome. Also, having to check whether the backups they create are effective makes it another routine task that needs either extra automation scripting to run a restore or a manual task.

**Deliverables:**

* Extend PMM UI to add existing backups so that they can be monitored
* Extend PMM UI to create backups
* Create a tool to automate the backup testing (check whether the backups created are usable)
* Extend PMM to monitor and alert on backup irregularities
* Integrate the backup management with external schedulers like cron.

**Required/preferred skills:** C++, Go, PostgreSQL
**Duration:** 350 hours
**Difficulty level:** Hard
**Mentors:** Kai Wagner, @Jan_Wieremjewicz
**Relevant repository and resources:**
* [GitHub - percona/postgres: Percona Server for PostgreSQL](https://github.com/percona/postgres)
* [GitHub - percona/pmm: Percona Monitoring and Management: an open source database monitoring, observability and management tool](https://github.com/percona/pmm)

### LLM-Powered Test Scenario Generation for Open Source Contributions

Open-source projects thrive on community contributions, but ensuring that each pull request (PR) has adequate test coverage is a major challenge. Many PRs introduce changes without proper regression tests, leading to bugs and unstable releases.

This project aims to build an LLM-powered tool that analyzes code changes in GitHub PRs and automatically generates relevant test scenarios. Using an Open Source LLM (e.g., DeepSeek, Mistral, LLaMA), the system will identify impact areas, suggest missing test cases, and recommend regression tests based on past commits. The goal is to integrate this into GitHub workflows, enabling maintainers to quickly assess PR test coverage and guide contributors in writing better tests.

**Deliverables:**

1. The student will work on developing a system with the following features:
  * PR Analysis & Impact Assessment
  * Extract and analyze code diffs in pull requests.
  * Identify affected functions, dependencies, and modules.
  * Predict impact areas using a dependency graph.

2. Test Scenario Generation using LLMs
  * Use an Open Source LLM (DeepSeek, Mistral, etc.) to generate test cases.
  * Recommend unit tests, integration tests, and regression scenarios.
  * Compare new tests with existing ones to detect gaps in coverage.

3. GitHub Bot for Automated Suggestions
  * Implement a bot that comments on PRs with test recommendations.
  * Provide interactive feedback to contributors and maintainers.
  * Integrate with GitHub Actions for CI/CD automation.

5. Regression Test Identification
  * Identify existing test cases that need to be re-run.
  * Suggest additional tests based on historical PRs and past bug reports.

6. Evaluation Metrics & Benchmarking
  * Measure effectiveness by tracking missed bugs before/after integration.
  * Collect feedback from maintainers and contributors.

**Future Scope:**

* Extend beyond GitHub to GitLab, Bitbucket, and other version control systems.
* Support additional test types, such as security and performance tests.
* Implement self-learning mechanisms to improve accuracy over time.

**Required/preferred skills:** Strong programming skills in Python or JavaScript, Experience with GitHub APIs & Pull Request Workflows, Understanding of Machine Learning / LLMs (DeepSeek, Mistral, LLaMA, etc.), Familiarity with Software Testing & QA Automation, Experience with CI/CD Pipelines & GitHub Actions (Bonus).
**Duration:** 350 hours
**Difficulty level:** Hard
**Mentor:** Peter Sirotnak, @vasyl.yurkovych

## Percona Build Engineering

### SBOMs for Percona database software - MySQL, PostgreSQL, and MongoDB

A “software bill of materials” (SBOM) has emerged as a key building block in software security and software supply chain risk management. An SBOM is a nested inventory, a list of ingredients that comprise software components. The project aims to adapt Percona’s build pipelines to generate SBOMs for Percona Software for MySQL, PostgreSQL, and MongoDB. This will enable organizations using Percona software to be more secure and avoid software supply chain vulnerabilities that were very harmful in late 2020 with the discovery of the [Solar Winds](https://www.csoonline.com/article/3601508/solarwinds-supply-chain-attack-explained-why-organizations-were-not-prepared.html) cyberattack or later with the [Log4j](https://en.wikipedia.org/wiki/Log4Shell) security flaw.


**Deliverables:**
At the end of the project, a running staging pipeline in Jenkins and Trivy should produce complete SBOMs for Percona Server for MySQL, PostgreSQL, and MongoDB, Percona Backup for MongoDB, Percona Xtra Backup for MySQL. SBOMs are uploaded automatically to the Percona repository and are downloadable publicly. Additionally, technical documentation on how the process works is expected to be created.

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
