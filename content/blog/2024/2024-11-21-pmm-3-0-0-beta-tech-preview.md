---
title: "Percona Monitoring and Management 3.0.0-Beta - Tech Preview"
date: "2024-11-21T00:00:00+00:00"
tags: ["PMM", "Technical Preview", "Monitoring", "Percona", "Databases", ]
authors:
  - ondrej_patocka
images:
  - images/pmm/pmm-blog-post-cover.png
slug: percona-monitoring-management-technical-preview
---

## Percona Monitoring and Management 3.0.0 Beta - Tech Preview

We're excited to announce the Tech Preview (Beta) release of **Percona Monitoring and Management (PMM) 3.0.0-Beta**.


> This release is intended for testing environments only, as it's not yet production-ready. The GA (General Availability) release will be available through standard channels in the upcoming months.

## Release notes

**To see the full list of changes, check out the [3.0.0-Beta - Tech Preview Release Notes](https://pmm-doc-3-0.onrender.com/release-notes/3.0.0_Beta.html)**

## Installation options


### PMM Server

#### Docker

- [Server](https://hubgw.docker.com/r/perconalab/pmm-server/tags?name=3.0.0-beta): `docker pull perconalab/pmm-server:3.0.0-beta`
- [Docker installation guide](https://pmm-doc-3-0.onrender.com/install-pmm/install-pmm-server/baremetal/docker/easy-install.html)

#### VM

- [Download OVA file](https://percona-vm.s3.amazonaws.com/PMM3-Server-2024-11-26-1307.ova)
- [VM Installation guide](https://pmm-doc-3-0.onrender.com/install-pmm/install-pmm-server/baremetal/virtual/index.html)


### PMM Client

#### Docker images
- [AMD 64 + ARM 64](https://hubgw.docker.com/r/perconalab/pmm-client/tags?name=3.0.0-beta): `docker pull perconalab/pmm-client:3.0.0-beta`


#### Binary packages
- [Download AMD 64 tarball](https://downloads.percona.com/downloads/TESTING/pmm-client-3.0.0beta/pmm-client-3.0.0beta.AMD64.tar.gz)
- [Download ARM 64 tarball](https://downloads.percona.com/downloads/TESTING/pmm-client-3.0.0beta/pmm-client-3.0.0beta.ARM64.tar.gz)

#### Package Manager installation
1. Enable testing repository via Percona-release: `percona-release enable pmm3-client testing`
1. Install relevant pmm-client package using your system's package manager



---
Contact us on the [Percona Community Forums](https://forums.percona.com/c/percona-monitoring-and-management-pmm).