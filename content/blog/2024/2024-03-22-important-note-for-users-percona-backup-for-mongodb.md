---
title: "Important note for users and customers using the logical backup feature in Percona Backup for MongoDB (PBM)"
date: "2024-03-22T00:00:00+00:00"
tags: ['Percona', 'opensource', 'MongoDB']
description: "Percona Backup for MongoDB is an open-source, distributed and low-impact solution for consistent backups of MongoDB sharded clusters and replica sets."
authors:
  - santo_leto
images:
  - blog/2024/03/note-pbm-mongodb.jpg
---

## Introduction

[Percona Backup for MongoDB](https://www.percona.com/software/mongodb/percona-backup-for-mongodb) is an open-source, distributed and low-impact solution for consistent backups of MongoDB sharded clusters and replica sets.

A PBM issue has been recently discovered which, under certain and rare conditions, could cause the logical restore to fail ([PBM-1223](https://jira.percona.com/browse/PBM-1223)).

This article includes details about:

-   The conditions under which bug [PBM-1223](https://jira.percona.com/browse/PBM-1223) could be triggered.

-   How we resolved the issue.

-   Our recommendations to affected users and customers.

## Issue description

During the restore process, when using a PBM version minor than v2.4.0 and when some specific and rare conditions are met, PBM could see "commit" without any "writes" (as it would be in an "empty" transaction). As a result, during the restore process, PBM could return an "unknown transaction id" error, causing the restore to fail ([PBM-1223](https://jira.percona.com/browse/PBM-1223)).

This problem does not happen if you are restoring the backup with PBM v2.4.0 or higher.

## Am I affected?

You might be affected by [PBM-1223](https://jira.percona.com/browse/PBM-1223) if all the following conditions apply to you:

-   You are taking logical backups with PBM.

-   You run distributed transactions where "write" operations involve two or more shards.

-   Your PBM version is 2.3 or earlier.

## Issue resolution

The issue described in this article has been fixed in PBM v2.4.0. Starting with this version, if PBM sees an "empty" transaction, it now ignores it and continues (the restore will not abort).

## Recommendations

We recommend all PBM users and customers that might be affected by [PBM-1223](https://jira.percona.com/browse/PBM-1223) to upgrade to PBM v2.4.0 or higher and take a new backup as soon as possible. No other workarounds are currently available on earlier versions. Upgrading and taking a new backup will avoid possible problems related to this issue in the future.

## Additional questions

For any additional questions, Percona customers can open a new support ticket.

Community users can use the usual [community](https://percona.community/contribute/how-to-get-involved/) support channels to request help.