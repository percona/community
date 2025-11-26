---
title: "PGScorecard - PostgreSQL Compatibility Index"
date: "2025-11-13T00:00:00+00:00"
tags: ["Percona", "pg_tde", "pg_kwagner", "PostgreSQL", "Compliance", "Open Source"]
categories: ['PostgreSQL']
authors:
  - kai_wagner
images:
  - blog/2025/11/pci-pgscorecard.png
aliases:
  - /blog/2025/11/12/pgscorecard-postgresql-compatibility-index/
---

We’re excited to share that our recent test run using the [Postgres Compatibility Index (PCI)](https://github.com/secp256k1-sha256/postgres-compatibility-index/blob/main/readme.md) achieved 100% compatibility.

The PCI was created to bring clarity to the often used but loosely defined term "PostgreSQL compatible." As Mayur explains in his article [The Making of 'Postgres Is'](https://drunkdba.medium.com/the-making-of-postgres-is-5034c0dc4639), the goal is simple: to ensure that when a system claims to be compatible with PostgreSQL, it truly behaves like upstream PostgreSQL in practice. The PCI accomplishes this by running a comprehensive set of tests across features like data types, procedural functions, constraints, extensions, and more, and producing a measurable, transparent score. This gives users and vendors a reliable benchmark rather than relying on marketing claims.

Compatibility matters because many organizations rely on PostgreSQL variants, repackaged distributions, or vendor supported systems. They want the confidence that their schemas, tools, extensions, ORMs, client libraries, and workflows will continue to work as expected. A system that drifts from upstream PostgreSQL can introduce subtle risks such as, unsupported features, migration challenges, and vendor lock-in.

Achieving a perfect PCI score means our system supports the full baseline feature set as currently defined. It demonstrates that users can rely on the same behavior as community PostgreSQL, whether they are self-hosting, using a vendor-supported version, or integrating with existing tools. Importantly, it also shows that you can have a fully open-source system while still benefiting from vendor support, without compromising compatibility.

In a world where “PostgreSQL compatible” is often a vague claim, initiatives like the PCI provide the needed help with transparency and comparability. It helps to protect you from marketing claims in the PostgreSQL ecosystem, ensuring that tooling, and workflows continue to function reliably. 

Special thanks to Mayur, whose initiative is helping define a clear, standardized framework for PostgreSQL compatibility.

> The test run was done against [Percona Server for PostgreSQL 17.6.1](https://docs.percona.com/postgresql/17/index.html). [Click for test result](https://github.com/secp256k1-sha256/postgres-compatibility-index/blob/main/postgres-compatibility-index/outputs/Percona.json). Percona Server for PostgreSQL is a binary-compatible, open source drop-in replacement for PostgreSQL with the currently needed enhancements, to make [Transparent Data Encryption (TDE)](https://docs.percona.com/pg-tde/index.html) work.  

