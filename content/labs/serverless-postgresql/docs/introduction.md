---
title: "Introduction"
description: "Architectural overview, Binary releases location, The relation between components"
weight: 1
---

Percona provides binary builds for Serverless PostgreSQL based on [the Neon: Serverless Postgres](https://github.com/neondatabase/neon).

This solution provides a serverless experience for PostgreSQL by dividing the compute nodes and storage nodes, allowing the storage to be scaled as your data grows and making the process transparent for end-users.

At this point the binaries are **EXPERIMENTAL and ONLY for TESTING** purposes. Percona does not provide official support for the build at this moment.

For the feedback and questions please use our Forums: (LINK)

## Binary releases location

The binaries for releases are hosted on github release page

[Releases · Percona-Lab/neon (github.com)](https://github.com/Percona-Lab/neon/releases)

## Architectural overview

The build provides multiple components necessary to start Serverless PostgreSQL. The primary components are:

1. Storage Broker
2. Page Server
3. Safe Keeper
4. Compute Nodes

## The relation between components

### WAL records

Compute nodes write WAL records to the WAL Service, which consists of safekeepers. To provide low-latency operations, safekeepers keep records only in memory. However, there are three of them combined in a consistent group.

For permanent storage, WAL records are shipped later to Pageserver.

![Percona - Serverless Postgres - WAL records](/images/labs/docs/serverless/introduction/image1.png)

### Data pages

The Pageserver listens for GetPage@LSN requests from the Compute Nodes, and responds with pages from the repository. 

![Percona - Serverless Postgres - Data pages](/images/labs/docs/serverless/introduction/image2.png)

### Storage Broker

Storage Broker is a coordination component between WAL Service and Pageserver

![Percona - Serverless Postgres - Storage Broker](/images/labs/docs/serverless/introduction/image3.png)

