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

-   Finalized SSL/TLS support for MySQL
-   Added support for Debian 13 and Amazon Linux 2023
-   Fixed MariaDB support broken in version 3.7.0
-   Added options to skip certain collections in `pt-k8s-debug-collector` and `pt-stalk`
-   Documentation improvements
-   Other performance improvements

In this blog, I will outline the most significant changes. A full list of improvements and bug fixes can be found in the [release notes](https://docs.percona.com/percona-toolkit/release_notes.html).

# SSL/TLS support for MySQL

Percona Toolkit historically did not have consistent SSL support. This was reported at <https://perconadev.atlassian.net/browse/PT-191>. In version 3.7.0, option `s` for `DSN` was introduced. This option instructs `DBD::mysql` to open a secure connection with the database. This version also adds command-line option `--mysql-ssl` and its short form `-s` to all tools. All other SSL/TLS-related options, such as `ssl-ca`, `ssl-cert`, `ssl-cipher`, etc, could be specified in the configuration file if necessary. This completes SSL/TLS support for MySQL. For more details and information check [this blog post](TBD).

# Supported Platforms Update

Percona repositories now have Percona Toolkit packages for Debian 13 and Amazon Linux 2023. To install them enable repository `pt` with the `percona-release` utility. More information on Percona repositories is available in the [User Reference Manual](https://docs.percona.com/percona-software-repositories/index.html). There is no platform deprecation in this release.

# Regression Bug Fixes

Recent major changes introducing MySQL 8.4 support missed ignore case modificator for the regular expression that checks if MySQL flavor is MariaDB. As a result, tools executed replication statements not compatible with MariaDB. Version 3.7.1 fixes the regular expression and re-adds MariaDB support back ([PT-2451](https://perconadev.atlassian.net/browse/PT-2451)). Future versions of Percona Toolkit will have better MariaDB support, including MariaDB-specific versions of non-offensive replication commands.

Utility `pt-sift` stopped working, because dependent library `alt_cmds.sh` was not included ([PT-2498](https://perconadev.atlassian.net/browse/PT-2498)). This was not found during previous release testing, because regression test for the tool was not run. Now this miss is fixed and the utility works properly again. Additionally, regression test is updated.

Helper utility `version_cmp` was written in some compiled language and source code for it was not available ([PT-2469](https://perconadev.atlassian.net/browse/PT-2469)). This broke version checking on platforms not compatible with the unknown platform where the binary was originally compiled. Now this utility rewritten as a Bourne-Again shell script.

# Modern MySQL Support

Percona Toolkit uses legacy MySQL syntax in many places to be compatible with older versions of MySQL. In other places, it misses modern MySQL diagnostic additions. This version makes first steps to improve this situation by adding such features as invisible index support in `pt-duplicate-key-checker` ([PR-996](github.com/percona/percona-toolkit/pull/996)) and `performance_schema.threads` collecton in `pt-stalk` ([PT-1718](https://perconadev.atlassian.net/browse/PT-1718)). Currently, data from `performance_schema.threads` is collected along with the deprecated `information_schema.processlist`. In the future, support for `information_schema.processlist` will be deprecated, then removed.

Future versions of Percona Toolkit will have more modern MySQL diagnostic support.

# Performance Improvements

`pt-stalk` now has new option, `--skip-collection`, that allows to skip one or more collections. Supported values for this option are: `ps-locks-transactions`, `thread-variables`, `innodbstatus`, `lock-waits`, `mysqladmin`, `processlist`, `rocksdbstatus`, `transactions`. To skip two or more collections, separate them with a comma. E.g., `--skip-collection=processlist,innodbstatus`. You will find more information at [PT-2289](https://perconadev.atlassian.net/browse/PT-2289) and in the [User Reference Manual for `pt-stalk`](https://docs.percona.com/percona-toolkit/pt-stalk.html).

`pt-k8s-debug-collector` introduces option `-skip-pod-summary` allowing to skip pod summary collections, such as `pt-mysql-summary`, `pt-mongodb-summary`, or `pg_gather`. Check [PT-2453](https://perconadev.atlassian.net/browse/PT-2453) and the [User Reference Manual for `pt-k8s-debug-collector`](https://docs.percona.com/percona-toolkit/pt-k8s-debug-collector.html).

Originally, tools output was always buffered. This is usually good for performance but you may want to disable this feature when need to see output of the tools faster. For example, if you run `pt-archiver` or `pt-table-checksum` on large table in Kubernetes, you won't see progress ([PT-2052](https://perconadev.atlassian.net/browse/PT-2052)) until the tool finishes. New option, `--[no]buffer-stdout`, allows to disable buffering when needed.

## Incompatilbe change

Earlier, if `--chunk-size` was enabled for `pt-online-schema-change`, option `--chunk-time` was ignored. This caused situations when a user has to start with default automatic chunk size even if it was not effective for some tables, and wait when chunk size is adjusted in subsequent iterations. Alternatively, they had to guess fixed chunk size that implies time consuming [try and error](https://en.wikipedia.org/wiki/Trial_and_error) approach ([PT-1423](https://perconadev.atlassian.net/browse/PT-1423)).

Starting from version 3.7.1, if both options `--chunk-size` and `--chunk-time` are specified, initial chunk size will be as specified by the option `--chunk-size`, but later it will be adjusted, so that the next query takes specified amount of time (in seconds) to execute.

# Documentation Improvements

While working on this release we found undocumented featues such as `--recursion-method=dsn` support in `pt-table-sync` ([PT-2470](https://perconadev.atlassian.net/browse/PT-2470)), broken man page for `pt-secure-collect` and other tools written in Go language ([PT-1564](https://perconadev.atlassian.net/browse/PT-1564)), as well as minor documentation issues. Now all of them are fixed.

# Community contributions

This release includes contributions from Community and Percona Engineers who do not actively work on the project. We want to thank:

- Iwo Panowicz for option `-skip-pod-summary` in `pt-k8s-debug-collector` ([PT-2453](https://perconadev.atlassian.net/browse/PT-2453))
- Matthew Boehm for invisible indexes support in `pt-duplicate-key-checker` ([PR-996](https://github.com/percona/percona-toolkit/pull/996))
- Nilnandan Joshi for collecting `performance_schema.threads` along with `information_schema.processlist` in `pt-stalk` ([PT-1718](https://perconadev.atlassian.net/browse/PT-1718)) and fix for [PT-2014 - pt-config-diff does not honor case insensitivity flag](https://perconadev.atlassian.net/browse/PT-2014)
- Paweł Kudzia for the updated documentation of pt-query-digest ([PR-953](https://github.com/percona/percona-toolkit/pull/953))
- Maciej Dobrzanski for fixing [PR-890 - pt-config-diff: MySQL truncates run-time variable values longer than 1024 characters](https://github.com/percona/percona-toolkit/pull/890)
- Marek Knappe for fixing [PT-2418 - pt-online-schema-change 3.7.0 lost data when exe alter xxx rename column xxx](https://perconadev.atlassian.net/browse/PT-2418) and [PT-2458 - remove-data-dir defaults to True](https://perconadev.atlassian.net/browse/PT-2458)
- Yoann La Cancellera for his work on `pt-galera-log-explainer`
- Nyele for restoring MariaDB support ([PT-2465](https://perconadev.atlassian.net/browse/PT-2465))
- Taehyung Lim for fixing [PT-2401 - pt-online-schema-change 'table does not exist' on macos](https://perconadev.atlassian.net/browse/PT-2401)
- Viktoras Agejevas for fixing [PR-989 -  Fix script crashing with precedence error](https://github.com/percona/percona-toolkit/pull/989) in `pt-online-schema-change`
- Hartley McGuire for fixing [PT-2015 - pt-config-diff does not sort variable flags](https://perconadev.atlassian.net/browse/PT-2015)
