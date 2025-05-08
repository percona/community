---
title: "Progress report on pg_tde - GA extension is nearer every day!"
date: "2025-05-08T00:00:00+00:00"
tags: ['PG_TDE', 'Postgres', 'Opensource', 'pg_jan']
categories: ["PostgreSQL"]
authors:
  - jan_wieremjewicz
images:
  - blog/2025/05/jan-tde.jpg
---

Another week, another blogpost about the state of open source Transparent Data Encryption (TDE) for PostgreSQL. 

First off, thank you for all the feedback shared so far!

Whether it's reports about deployment issues with `pg_tde`, integration with KMS, missing features or gaps in our documentation, we truly appreciate it! Your input helps us build a better, more complete solution and to properly prioritize what's next. 

## What’s the word?

![Progress report on pg_tde - Bird](blog/2025/05/big-bird-sesame-street.gif)

We know many of you are eagerly waiting for a production-ready release of `pg_tde`, and today we’ve got some good news! You may remember the last release was a Release Candidate (RC), now we're gearing up to launch RC2.

If you're not familiar with the terminology, this simply means we’re one step closer to General Availability (GA).

Our nightly builds are always there if you want to keep up with the latest updates, but this new milestone release highlights the fixes to some pain points that our tests and your feedback helped uncover. 

## When to expect RC2?

This post is just a heads-up. The actual release is planned for early next week (after May 12, 2025). Keep an eye out.

In the meantime, feel free to check what’s coming in RC2. And if you'd like to benefit from these improvements right away, nightly builds are the way to go.

## What’s new in RC2 compared to RC1?

Some recent documentation updates are already live, and we’d love to hear your thoughts on them. Don’t be a stranger, let us know how do you find them!

As for the code, here are the key changes:

- KMS configuration improvements including:
    - New parameter for passing a client certificate when configuring a KMIP provider
    - Compatibility updates for key management systems (KMS)
        - Thales CypherTrust
        - Fortanix Data Security Manager
    - Validation enforcement when adding key provider configurations
- WAL improvements, hardening encryption in our beta WAL support
- Security enhancements for multi-tenancy scenarios
- Other updates like:
    - Added `pg_tde_verify_default_key()` and `pg_tde_default_key_info()` functions
    - Fixed support for logical replication

## How to use nightly builds

In case you’re wondering what nightly builds are: think of them as automatically generated versions of the software with the latest changes, usually built overnight 😎. They're useful for testing (especially for integration testing) and for those, like our developers, who want to work with the freshest code.

![Progress report on pg_tde - nightly builds](blog/2025/05/nightly_builds.jpg)

No elephants have been hurt to create our nightly builds! We rely solely on CI/CD automation!

You can find them in our [experimental repo](https://repo.percona.com/ppg-17.0/).  Do note, they're currently only available for x86_64 and a limited set of operating systems:

- [Ubuntu Jammy/Noble](https://repo.percona.com/ppg-17.0/apt/pool/experimental/)
- [OL/Rocky 8/9](https://repo.percona.com/ppg-17.0/yum/experimental)