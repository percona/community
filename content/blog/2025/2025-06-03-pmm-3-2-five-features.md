---
title: "What's new in PMM 3.2.0: Five major improvements you need to know"
date: "2025-06-03T00:00:00+00:00"
tags: ["PMM", "Monitoring", "Percona", "Databases"]
categories: ["PMM"]
authors:
  - catalina_adam
images:
  - blog/2025/06/PMM-32-five.jpg
slug: percona-monitoring-management-3-2-five-improvements
---


PMM 3.2.0 brings some long-awaited fixes and new capabilities. You can now install PMM Client on Amazon Linux 2023 with proper RPM packages, get complete MySQL 8.4 replication monitoring, and track MongoDB backups directly in PMM.

Here's what's most important in this release:

## 1. Native Amazon Linux 2023 support - no more workarounds

What's new: If you've been running PMM Client on AL2023 and dealing with complex manual installations, those days are over. You can now install PMM Client through [native RPM packages](https://repo.percona.com) just like any other supported platform.

What this means for you: Streamlined setup means you can get your Amazon Linux 2023 environments monitored faster.

## 2. Complete MySQL 8.4 replication monitoring

What's new: PMM now fully supports replication monitoring for MySQL 8.4, including key metrics like IO Thread status, SQL Thread status, and Replication Lag. MySQL 8.4 changed how these metrics are exposed, and earlier PMM versions couldn't track them accurately.

What this means for you: With the upgraded MySQL Exporter (v0.17.2), you now get complete replication monitoring across all supported MySQL versions (5.7, 8.0, and 8.4) without any visibility gaps.

## 3. MongoDB backup monitoring dashboard

What's new: The new [PBM Details dashboard ](https://docs.percona.com/percona-monitoring-and-management/3/reference/dashboards/dashboard-mongodb-PBM-details.html)lets you monitor MongoDB backups directly in PMM using the PBM collector. Instead of switching between PMM and separate backup tools, you now get a real-time, unified view of backup activity across replica sets and sharded clusters.

What this means for you: Easily track backup status, configuration, size, duration, PITR status, and recent successful backups---all in one place. No more tool-hopping to stay on top of your backup operations.

## 4. Grafana 11.6 upgrade with enhanced capabilities

What's new: PMM now ships with Grafana 11.6, delivering enhanced visualization capabilities and improved alerting workflows.

Key features include:

-   Alert state history for reviewing historical changes in alert statuses

-   Improved panel features and visualization actions

-   Simplified alert creation with better UI workflows

-   Recording rules for creating pre-computed metrics

-   Navigation bookmarks for quick dashboard access

What this means for you: These enhancements make your monitoring dashboards more interactive, your alerting more sophisticated, and your overall monitoring workflow more efficient.

## 5. Dramatically improved Query Analytics performance

What's new: We've optimized QAN filter loading performance to reduce the number of processed rows by up to 95% in large environments.

What this means for you: Filters on the [PMM Query Analytics page](https://docs.percona.com/percona-monitoring-and-management/3/use/qan/index.html?h=query+ana) now load much faster, making the interface more responsive to improve your troubleshooting efficiency.

## Additional improvements worth noting

Beyond these five major enhancements, PMM 3.2.0 also introduces:

-   Secure ClickHouse connections with authenticated credential support

-   MongoDB Feature Compatibility Version (FCV) panels for better cluster version visibility

-   Nomad integration laying groundwork for future extensibility

-   Numerous bug fixes improving stability across ProxySQL, PostgreSQL, and MySQL monitoring

## Getting started with PMM 3.2.0

Ready to experience these improvements? Set up your PMM 3.2.0 instance using our [quickstart guide](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) or upgrade your existing installation following our [migration documentation](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html).

For existing users with external PostgreSQL databases, make sure to review the [external PostgreSQL configuration migration guide](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/external_postgres_pmm_upgrade.html) before upgrading.

Questions or feedback? We'd love to hear from you! Connect with the Percona community through our [forums](https://forums.percona.com/c/percona-monitoring-and-management-pmm/30/none) or join the conversation on our community channels.