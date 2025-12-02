---
title: "What is New in Percona Toolkit 3.7.1"
date: "2025-12-10T00:00:00+00:00"
tags: ['Toolkit', 'MySQL', 'Percona', 'Opensource']
categories: ["MySQL", "Toolkit"]
authors:
  - sveta_smirnova
images:
  - blog/2025/12/toolkit-371.jpg
---

Percona Toolkit 3.7.1 has been released on **Dec 9, 2025**. The most important updates in this version are:

-   SSL/TLS support for MySQL
-   Support for Debian 13
-   Fixed MariaDB support broken in version 3.7.0
-   Added options to skip certain collections in `pt-k8s-debug-collector` and `pt-stalk`
-   Documentation improvements
-   Other performance improvements

SSL/TLS support for MySQL
-------------------------

Percona Toolkit historically did not have consistent SSL support. This was reported at <https://perconadev.atlassian.net/browse/PT-191>. In version 3.7.0, option `s` for `DSN` was introduced. This option instructs `DBD::mysql` to open a secure connection with the database. This version also adds command-line option `--mysql-ssl` and its short form `-s` to all tools. All other SSL/TLS-related options, such as `ssl-ca`, `ssl-cert`, `ssl-cipher`, and others, could be specified in the configuration file if necessary. This completes SSL/TLS support for MySQL. For more details and information check [this blog post](TBD).

Supported Platforms Update
--------------------------

Percona repositories now have Percona Toolkit packages for Debian 13. To install them enable repository `pt` with the `percona-release` utility. More information on Percona repositories is available in the [User Reference Manual](https://docs.percona.com/percona-software-repositories/index.html). There is no platform deprecation in this release.

Regression Bug Fixes
--------------------

Recent major changes introducing MySQL 8.4 support missed ignore case modificator for the regular expression that checks if MySQL flavor is MariaDB. As a result, tools executed replication statements not compatible with MariaDB. Version 3.7.1 fixes the regular expression and re-adds MariaDB support back. Future versions of Percona Toolkit will have better MariaDB support, including MariaDB-specific versions of non-offensive replication commands.

Utility `pt-sift` stopped working, because dependent library `alt_cmds.sh` was not included. This was not found during previous release testing, because regression test for the tool was not run. Now this miss is fixed and the utility works properly again. Additionally, regression test is updated.

Helper utility `version_cmp` was written in some compiled version and source code for it was not available. This broke version checking on platforms not compatible with the unknown platform where the binary was originally compiled. Now this utility rewritten as a Bourne-Again shell script.

Modern MySQL Support
--------------------

Percona Toolkit uses legacy MySQL syntax in many places to be compatible with older versions of MySQL. In other places, it misses modern MySQL diagnostic additions. This version makes first steps to improve this situation by adding such features as invisible index support in `pt-duplicate-key-checker` and `performance_schema.threads` collecton in `pt-stalk`. Currently, this data from `performance_schema.threads` is collected along with the deprecated `information_schema.processlist`. In the future, support for `information_schema.processlist` will be deprecated, then removed.

Future versions of Percona Toolkit will have more modern MySQL diagnostic support.

Performance Improvements
------------------------



Documentation Improvements
--------------------------

Community contributions
-----------------------

This release includes contributions from Community and Percona Engineers who do not actively work on the project. We want to thank:

- 