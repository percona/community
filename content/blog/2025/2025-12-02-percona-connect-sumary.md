---
title: "Community Recap: Percona.Connect London 2025, Building the Future of Open Source Together"
date: "2025-12-02T00:00:00+00:00"
tags: ['Community', 'Event Recap', 'Open Source', 'MySQL', 'PostgreSQL', 'Valkey']
categories: ['Community']
authors:
  - edith_puclla
images:
  - blog/2025/12/intro.jpeg
---

Percona.Connect London 2025 brought the open-source database community together for a half-day of learning and collaboration. The event focused on providing practical, technical insights for DBAs, DevOps engineers, and developers. The main takeaway was clear: Stability, Openness, and Automation are essential for modern, large-scale data infrastructure.

## Top Discussions & Key Takeaways

## 1. The Rise of Valkey: A Truly Open Caching Alternative

Following changes to the Redis license, the community needs a trusted, open-source replacement. Valkey was highlighted as the leading solution.

- Valkey was started by former Redis contributors quickly after Redis removed its open source license in 2024.
- It is a true open-source project governed under the Linux Foundation.
- It offers enhancements like better memory efficiency, performance, and scalability.
- In a recent Percona survey of 200 DBAs, Valkey was the most preferred alternative to Redis.

![Percona Connect London 2025](/blog/2025/12/img1.png)


## 2. Running PostgreSQL in a Cloud Native context

Takis Stathopoulos presented on running PostgreSQL in a Cloud Native context, explaining how Kubernetes Operators simplify complex deployments.

- Cloud Native vs. Cloud First: Cloud Native (Kubernetes) offers Portability and No vendor lock-in, allowing you to run the database consistently across different clouds and on-premise infrastructure.
- Percona Operator for PostgreSQL: This tool automates crucial operations like setting up high availability (using Patroni), backups (using pgBackrest), and scaling.
- When to use Cloud Native: It's ideal for large, microservice-based applications and teams prioritizing portability and avoiding vendor lock-in.

![Percona Connect London 2025](/blog/2025/12/img2.png)

![Percona Connect London 2025](/blog/2025/12/img3.png)



## 3. Native PostgreSQL TDE is Here: Securing Data Simply

Alastair Turner introduced the new Native Transparent Data Encryption (TDE) for PostgreSQL.

- Need for TDE: Encryption is necessary for data security, privacy protection, breach prevention, and meeting compliance requirements.
- The pg_tde Extension: This open-source TDE solution for PostgreSQL is designed to meet strict compliance rules (like PCI DSS 4.0.1) by ensuring the encryption key is controlled by the database, not just the operating system.
- Community Development: Percona is building this feature as an extension and plans to submit parts of the work to the upstream PostgreSQL community.

![Percona Connect London 2025](/blog/2025/12/img4.png)

## 4. The Future of MySQL: Vector Search & Binlog Server

Dennis Kittrell discussed two key features planned for MySQL that address major operational and feature challenges.

- MySQL Binlog Server MVP: This component aims to solve the problem of quick disaster recovery by acting as a stable, reliable replication source. It enables Precise Point-in-Time Recovery (PITR) using simple time or GTID coordinates.
- Native Vector Support MVP: This feature allows users to eliminate the complexity of using a separate vector database. You can store, index, and search vector embeddings directly in MySQL, allowing you to combine vector searches with standard business logic in a single, transactional query

### Our Community Focus

A common theme from the use cases was that while open source adoption is high, operational teams often lack the proper support and visibility.

Percona's goal is to support the community by providing:

- Stability when under heavy load or during maintenance.
- Faster Troubleshooting with better monitoring and observability.
- Safer Deployments through expert configuration and security support.

![Percona Connect London 2025](/blog/2025/12/img5.jpeg)

Thank you to everyone who joined us in London for a dynamic event. We hope the insights gained will help you with your open source database deployments.

The conversations continue in the Percona Community! You can reach out directly to the speakers:

- Martin Visser (Valkey Technical Lead)
- Dennis Kittrell (MySQL Product Manager)
- Alastair Turner (Postgres Community Advocate)
- Takis Stathopoulos (Enterprise Architect)

![Percona Connect London 2025](/blog/2025/12/img6.jpeg)

Join the Percona Community Conversation!

- [Percona Forum](https://forum.percona.com/)
- [Percona on LinkedIn](https://www.linkedin.com/company/percona/)

