---
title: "MySQL 8.4 Support in Percona Toolkit 3.7.0"
date: "2025-01-06T00:00:00+00:00"
tags: ['Percona', 'opensource', 'Toolkit', 'MySQL', "Featured"]
categories: ["MySQL", "Toolkit"]
authors:
  - sveta_smirnova
images:
  - blog/2025/01/toolkit-370.jpg
---

*Percona Toolkit 3.7.0 has been released on **Dec 23, 2024**. The main feature of this release is MySQL 8.4 support.*

*In this blog, I will explain what has been changed. A full list of improvements and bug fixes can be found in the *[*release notes*](https://docs.percona.com/percona-toolkit/release_notes.html)*.*

TLDR;

-   Replication statements in 8.4 are fully supported by the Percona Toolkit
-   `pt-slave-delay` has been deprecated.
-   `pt-slave-find` has been renamed to `pt-replica-find`. The old name has been deprecated but exists in the repository as an alias of the `pt-replica-find`.
-   `pt-slave-restart` has been renamed to `pt-replica-restart`. Old name has been deprecated but exists in the repository as an alias of the `pt-replica-restart`.
-   Basic SSL support has been added to the tools where it was not working before (see <https://perconadev.atlassian.net/browse/PT-191> ), and Percona Toolkit now supports `caching_sha2_password`  and `sha256_password`authentication plugins. Full implementation of <https://perconadev.atlassian.net/browse/PT-191> is planned for the next version.

Replication Statements
----------------------

MySQL 8.4 removed earlier deprecated offensive language, such as `SLAVE` or `MASTER`. This made tools written for earlier versions not compatible with the new version. Percona Toolkit was also affected, and I had to rewrite it.

However, Percona Toolkit should be able to run not only with MySQL 8.4 but also with older versions. So, the change was not a simple grep and replace of offensive words. It is not even possible for version MySQL 8.0 because new syntax was first introduced in 8.0.23 for the `CHANGE REPLICATION SOURCE` and `START/STOP REPLICA` commands. Earlier versions weren't aware of this change.

Another challenge was the fact that I could replace all occurrences of the word `SLAVE` with `REPLICA`. Still, I could not do the same for the `MASTER` and `SOURCE`  pairs because replication source-related commands are mapped differently:

| **Legacy syntax** | **Syntax without offensive words** |
|----------|----------|
| `CHANGE MASTER` | `CHANGE REPLICATION SOURCE` (since 8.0.23) |
| `SHOW MASTER STATUS` | `SHOW BINARY LOG STATUS` (since 8.4.0) |
| `RESET MASTER` | `RESET BINARY LOGS[ AND GTIDS]` ( since 8.4.0) |
| `MASTER`  in other commands | `SOURCE` (partially since 8.0.23, fully since 8.4) |

So, I added selectors that use the correct command depending on the MySQL server version.

I intentionally implemented new syntax for version 8.4 only, so I do not have to check every single minor version of 8.0. I also did not implement new syntax for MariaDB. This may happen in the future.

***However, all messages displayed to the user use the new syntax. If you rely on old syntax somewhere in your scripts, adjust them.***

Internally, most of the functions were renamed to use the new syntax, but the important module `lib/MasterSlave.pm` kept its name.

Deprecated and Outdated Tools
-----------------------------

As a result of this change, `pt-slave-delay` has been deprecated. The tool stays in the repository and works as before when connected to MySQL 8.0 or an earlier version. However, it refuses to work with MySQL 8.4. The tool will be removed in one of the future versions.

Tools `pt-slave-find` and `pt-slave-restart` were renamed to `pt-replica-find` and `pt-replica-restart`. Aliases with old names still exist, so you have time to change your scripts. However, expect that these aliases will be removed in one of the future versions as well.

Tool `pt-variable-advisor` has been updated to reflect current default values.

Basic SSL Support
-----------------

Percona Toolkit did not have consistent SSL support: some of the tools were able to connect using SSL, and others did not. This was reported at <https://perconadev.atlassian.net/browse/PT-191>. In this version, I added option "`s`" for `DSN` that instructs `DBD::mysql` to open a secure connection with the database. As a result, Percona Toolkit now supports `caching_sha2_password` and `sha256_password` authentication plugins. But other SSL options are still missed. Full SSL support will be added in the next version.

Conclusion
----------

Percona Toolkit fully supports MySQL 8.4. If you use `pt-slave-find` and `pt-slave-restart`, consider calling them by their new names `pt-replica-find` and `pt-replica-restart`. Tool `pt-slave-delay`  has been deprecated and will be removed in future versions. Use built-in feature [delayed replication](https://dev.mysql.com/doc/refman/8.4/en/replication-delayed.html) instead.