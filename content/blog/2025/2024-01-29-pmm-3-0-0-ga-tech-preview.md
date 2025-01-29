---
title: "Percona Monitoring and Management 3.0.0-GA - Tech Preview"
date: "2025-29-01T00:00:00+00:00"
tags: ["PMM", "Technical Preview", "Monitoring", "Percona", "Databases", ]
authors:
  - ondrej_patocka
images:
  - images/pmm/pmm-blog-post-cover.png
slug: percona-monitoring-management-technical-preview
---

## Percona Monitoring and Management 3.0.0 GA - Tech Preview

We're excited to announce the Tech Preview release of **Percona Monitoring and Management (PMM) 3.0.0 (GA)**.


*This release is intended for testing environments only, as it's not yet production-ready. The public release will be available through standard channels in upcoming days.*

## Release notes

**To see the full list of changes, check out the [3.0.0-GA - Tech Preview Release Notes](https://pmm-release-3-0-pr-3431.onrender.com/release-notes/3.0.0.html)**

## Installation options


### PMM Server

#### Docker

- [Server image](https://hubgw.docker.com/r/perconalab/pmm-server/tags?name=3.0.0-rc): `docker pull perconalab/pmm-server:3.0.0-rc`
- [Docker installation guide](https://pmm-release-3-0-pr-3431.onrender.com/quickstart.html)

#### VM

- [Download OVA file](https://percona-vm.s3.amazonaws.com/PMM3-Server-3.0.0.ova)
- [VM Installation guide](https://pmm-release-3-0-pr-3431.onrender.com/install-pmm/install-pmm-server/baremetal/virtual/index.html)


### PMM Client

#### Docker
- [AMD 64 + ARM 64 images](https://hubgw.docker.com/r/perconalab/pmm-client/tags?name=3.0.0-rc): `docker pull perconalab/pmm-client:3.0.0-rc`


#### Binary packages
- [Download AMD 64 tarball](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm-client/pmm-client-latest-250.tar.gz)
- [Download ARM 64 tarball](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm-client-arm/pmm-client-latest-255.tar.gz)

#### Package Manager installation
1. Enable testing repository via [percona-release](https://docs.percona.com/percona-software-repositories/percona-release.html): `percona-release enable pmm3-client testing`
1. Install relevant `pmm-client` package using your system's package manager



---
Contact us on the [Percona Community Forums](https://forums.percona.com/c/percona-monitoring-and-management-pmm).