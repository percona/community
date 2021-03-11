---
title: 'Percona Live Presents: Gonymizer, A Tool to Anonymize Sensitive PostgreSQL Data Tables for Use in QA and Testing'
date: Fri, 17 May 2019 11:11:58 +0000
draft: false
tags: ['author_junkert', 'Events', 'Kubernetes', 'PostgreSQL']
images:
  - blog/2019/05/gonymizer-postgres-data-anonymizer.jpg
authors:
  - levi_junkert
---

[SmithRX](https://smithrx.com/)[![gonymizer postgres data anonymizer](blog/2019/05/gonymizer-postgres-data-anonymizer.jpg)](https://smithrx.com/) is a next generation pharmacy benefit platform that is using the latest technology to radically reshape the prescription benefit management industry. To move quickly, we require the ability to iterate and test new versions of our software using production like data without violating Health Information Portability and Accountability Act (HIPAA) regulations. 

At Percona Live 2019, we are introducing a project we open sourced to anonymize our sensitive production data for use in rapid QA and testing of our software. The talk will cover:

*   An introduction to HIPAA and Protected Health Information (PHI)
*   Deciding which parts of your data need to be anonymized
*   Column mapping and how to represent relations that need to be anonymized
*   An introduction to the design of the software and how it works
*   Dumping data from a sensitive source
*   Processing the sensitive data to create an anonymized data set
*   Loading of the anonymized data set to a QA environment
*   How SmithRx is using multiple Kubernetes CronJob to reload our Q/A and development environments daily
*   Other examples on how Gonymizer can be used in other scheduling systems such as AWS Lambda
*   What this means for you and how you can contribute

### Who’d get the most from the presentation?

This presentation is intended for software engineers that need a quick and easy way to anonymize their data. Intended for middle level database infrastructure (devops), and continuous integration systems. This presentation is also appropriate for Go developers looking to contribute to  an open source project that is database related. Currently Gonymizer only supports PostgreSQL, but the software has been designed to handle multiple RDBMS in the future so anyone with HIPAA, DISA (Defense Information Systems Agency), or PCI () experience in other RDBMS may find this presentation useful for getting you started on porting Gonymizer to your RDBMS.

### Whose presentations are you most looking forward to?

At SmithRx we are currently growing our infrastructure size, automation management, and monitoring systems for our PostgreSQL database tier. There are many presentations we look forward to attending, but the following four talks will be a focus for SmithRx:

*   [HA PostgreSQL on Kubernetes](https://www.percona.com/live/19/sessions/ha-postgresql-on-kubernetes-by-demo) by Josh Berkus
*   [Automated Database Monitoring at Uber With M3 and Prometheus](https://www.percona.com/live/19/sessions/automated-database-monitoring-at-uber-with-m3-and-prometheus) by Richard Artoul
*   [Monitoring PostgreSQL with Percona Monitoring and Management (PMM)](https://www.percona.com/live/19/sessions/monitoring-postgresql-with-percona-monitoring-and-management-pmm) by Avinash Vallarapu
*   [Future of Postgres](https://www.percona.com/live/19/sessions/future-of-postgres) by Ken Rugg

__

Photo by [Viktor Talashuk](https://unsplash.com/photos/bhoj9tHlsiY?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/mannequin?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)