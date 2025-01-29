---
title: "Percona Monitoring and Management 3.0.0-GA - Tech Preview"
date: "2025-01-29T00:00:00+00:00"
tags: ["PMM", "Technical Preview", "Monitoring", "Percona", "Databases", ]
authors:
  - ondrej_patocka
images:
  - blog/2025/01/pmm-blog-post-cover.jpg
slug: percona-monitoring-management-technical-preview
---


We're excited to announce the Tech Preview release of **Percona Monitoring and Management (PMM) 3.0.0 (GA)**.

*This release is intended for testing environments only, as it's not yet production-ready. The public release will be available through standard channels in upcoming days.*

The Percona Monitoring and Management (PMM) 3.0.0 release delivers major security and stability enhancements. Notable security improvements include rootless deployments and encryption of sensitive data, along with improved API authentication using Grafana service accounts. Deployment options have expanded with official ARM support and the ability to use Podman for rootless deployments, providing flexibility and better security. Additionally, the introduction of containerized architecture has increased stability, and a streamlined upgrade process ensures reliability and ease of maintenance.

User experience has been significantly improved with more flexible monitoring configurations and UI-based upgrades for Podman installations. This release also includes new features such as monitoring for MongoDB 8.0 and integration with Watchtower for automated container updates. These enhancements aim to provide users with a more secure, stable, and user-friendly monitoring and management experience.

## Release notes

**To see the full list of changes, check out the [3.0.0-GA - Tech Preview Release Notes](https://pmm-release-3-0-pr-3431.onrender.com/release-notes/3.0.0.html)**


Percona Monitoring and Management (PMM) 3.0.0 Release Notes:

-   **Security Enhancements**:

    -   Implementation of rootless deployments to enhance security.

    -   Encryption of sensitive data to ensure information confidentiality.

    -   Improved API authentication with Grafana service accounts, increasing access security.

-   **Deployment Options**:

    -   Official PMM Client ARM support, allowing the use of PMM on ARM architecture devices.

    -   Rootless deployments using Podman, providing flexibility and security.

    -   Support for deployments using Helm, Docker, Virtual Appliance, and Amazon AWS for various use cases.

-   **Stability Improvements**:

    -   Increased stability through containerized architecture, providing isolation and manageability.

    -   Streamlined upgrade process, reducing the risk of failures during updates and enhancing reliability.

-   **User Experience**:

    -   Flexible monitoring configurations, allowing users to tailor the system to their needs.

    -   UI-based upgrades for Podman installations, making the update process more convenient and intuitive.

-   **New Features**:

    -   Monitoring for MongoDB 8.0, ensuring support for the latest database versions.

    -   Integration with Watchtower for automated container updates, simplifying management and keeping the system up-to-date.

We invite you to install and try the new PMM 3.0

## Installation options

### PMM Server

**Docker**

- [Server image](https://hubgw.docker.com/r/perconalab/pmm-server/tags?name=3.0.0-rc): `docker pull perconalab/pmm-server:3.0.0-rc`
- [Docker installation guide](https://pmm-release-3-0-pr-3431.onrender.com/quickstart.html)

**VM**

- [Download OVA file](https://percona-vm.s3.amazonaws.com/PMM3-Server-3.0.0.ova)
- [VM Installation guide](https://pmm-release-3-0-pr-3431.onrender.com/install-pmm/install-pmm-server/baremetal/virtual/index.html)


### PMM Client

**Docker**

- [AMD 64 + ARM 64 images](https://hubgw.docker.com/r/perconalab/pmm-client/tags?name=3.0.0-rc): `docker pull perconalab/pmm-client:3.0.0-rc`


**Binary packages**

- [Download AMD 64 tarball](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm-client/pmm-client-latest-250.tar.gz)
- [Download ARM 64 tarball](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm-client-arm/pmm-client-latest-255.tar.gz)

**Package Manager installation**
1. Enable testing repository via [percona-release](https://docs.percona.com/percona-software-repositories/percona-release.html): `percona-release enable pmm3-client testing`
1. Install relevant `pmm-client` package using your system's package manager


---
Contact us on the [Percona Community Forums](https://forums.percona.com/c/percona-monitoring-and-management-pmm).