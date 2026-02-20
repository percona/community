---
id: "306674d0-91f3-8074-92c2-c9b7088308bb"
title: "Automated, Consistent, and Safe: Database Backups with Kubernetes Operators"
layout: single
speakers:
  - george_kechagias
talk_url: "https://buildevcon.com/cloud-native-databases/"
presentation_date: "2026-02-20"
presentation_date_end: ""
presentation_time: ""
talk_year: "2026"
event: "Cloud Native Databases"
event_status: "Accepted"
event_date_start: "2026-02-20"
event_date_end: "2026-02-21"
event_url: "https://buildevcon.com/cloud-native-databases/"
event_location: "Virtual "
talk_tags: ['Kubernetes', 'Cloud Native', 'database', 'Open Source']
slides: ""
video: ""
---
## Abstract

Running databases on Kubernetes is no longer experimental, and backups remain a non-negotiable part of any production deployment. As stateful workloads grow in Kubernetes, the need for automated, consistent, and database-aware backup strategies becomes critical.

This talk explores the challenges of backing up databases in containerized environments and demonstrates how Kubernetes Operators can handle backup and restore for MySQL, MongoDB, and PostgreSQL using a declarative, Custom Resource–based workflow. Inspired by the Percona Operators, we'll see how complex backup procedures can be turned into simple, repeatable Kubernetes resources—keeping data protection fully Kubernetes-native.