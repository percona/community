---
title: "Percona Monitoring and Management 2.43.0 Preview Release"
date: "2024-09-12T00:00:00+00:00"
tags: ['PMM_prev']
authors:
  - ondrej_patocka
images:
  - superhero.png
slug: preview-release
---

## Percona Monitoring and Management 2.43.0 Tech Preview Release

Hello everyone! Percona Monitoring and Management (PMM) 2.43.0 is now available as a Tech Preview Release.

We encourage you to try this PMM preview release in **testing environments only**, as these packages and images are not fully production-ready. The final version is expected to be released through the standard channels in the coming week.

To see the full list of changes, check out the [PMM 2.43.0 Tech Preview Release Notes](https://pmm-doc-pr-1271.onrender.com/release-notes/2.43.0.html)

### PMM server Docker installation

[Run PMM Server with Docker instructions](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/docker.html)

docker tag:

`perconalab/pmm-server:2.43.0-rc`

### PMM client package installation

1. [Download AMD64](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm2-client/pmm2-client-latest-29.tar.gz) or [Download ARM64](https://s3.us-east-2.amazonaws.com/pmm-build-cache/PR-BUILDS/pmm2-client-arm/pmm2-client-latest-49.tar.gz) pmm2-client tarball for 2.43.0.

2. To install pmm2-client package, enable testing repository via Percona-release: 

`percona-release enable percona testing`

3. Install pmm2-client package for your OS via Package Manager.

### OVA

[Run PMM Server as a VM instructions](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/virtual-appliance.html)

[PMM2-Server-2.43.0.ova file](https://percona-vm.s3.amazonaws.com/PMM2-Server-2.43.0.ova)

### AMI

[Run PMM Server hosted at AWS Marketplace instructions](https://docs.percona.com/percona-monitoring-and-management/setting-up/server/aws.html)

`ami-0db618c7da6e202f4`


---

Contact us on the [Percona Community Forums](https://forums.percona.com/].