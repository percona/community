---
title: "Introduction"
description: "Architectural overview, Binary releases location, The relation between components"
weight: 1
---

Percona provides binary builds for Serverless PostgreSQL based on [the Neon: Serverless Postgres](https://github.com/neondatabase/neon).

This solution provides a serverless experience for PostgreSQL by separating the compute nodes and storage nodes. This allows scaling your storage as your data grows and makes the process transparent for end users.

At this point, the builds are **EXPERIMENTAL and for TESTING PURPOSES ONLY**. Percona does not provide official support for the builds at the moment.

Share your feedback and questions on [Percona Community Forum](https://forums.percona.com/c/percona-labs/serverless-postgresql/78).

## Binary Releases Location

Get binary releases on our [GitHub release page](https://github.com/Percona-Lab/neon/releases).

## Architecture

The build consists of the following main components:

- **Pageserver:** This is a storage server that stores data pages and WAL records.
- **Compute nodes:** They handle user queries and send requests for data pages to a page server.
- **Safekeeper(s):** They store WAL records durably before the page server can process them. Several safekeepers comprise a WAL service. To make sure that all WAL records are sent to the pageserver and avoid data loss, we recommend creating at least 3 safekeeper instances.
- **Storage broker:** It coordinates processing of WAL records between the WAL service and the page server.

![Percona - Serverless Postgres - WAL records](/images/labs/docs/serverless/introduction/architecture.png)

Compute nodes send requests to the page server. The pageserver responds with pages from the repository. WAL records that contain the changes to the data are sent to the WAL service, where the Paxos protocol distributes them between safekeepers thus reducing latency and ensuring data consistency. Safekeepers store the WAL records in memory until the storage broker sends them to the pageserver for further processing and storing in the repository.

![Percona - Serverless Postgres - Storage Broker](/images/labs/docs/serverless/introduction/listen-request.png)
