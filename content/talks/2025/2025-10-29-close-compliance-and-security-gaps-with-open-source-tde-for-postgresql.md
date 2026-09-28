---
id: SPEAK-2827
jira: SPEAK-2827
title: Close compliance and security gaps with open source TDE for PostgreSQL
layout: single
speakers:
- valeria_bogatyreva
talk_url: https://datastackconf.com/pages/data-stack-conf-2025
presentation_date: '2025-10-29'
presentation_date_end: ''
presentation_time: ''
room: ''
talk_year: '2025'
event: Data Stack Conf 2025
event_jira: ''
event_status: Done
event_date_start: '2025-10-29'
event_date_end: ''
event_url: https://datastackconf.com/pages/data-stack-conf-2025
event_location: Sofia, Bulgaria
talk_tags:
- PostgreSQL
- Video
- Security
slides: ''
video: https://www.youtube.com/watch?v=Gv2z-wVLuvo
youtube_id: Gv2z-wVLuvo
images:
- talks/2025/2025-10-29-close-compliance-and-security-gaps-with-open-source-tde-for-postgresql.png
---
Compliance frameworks keep getting stricter — HIPAA, PCI DSS, SOX, GDPR and friends all push harder on encryption at rest, key management, and proving you can actually encrypt data. Budgets to deal with that usually do not grow with the rules.

This talk walks through where PostgreSQL data lands on disk (WAL, heap, TOAST), what Transparent Data Encryption (TDE) covers versus storage-level encryption, and why table-level granularity plus KMS-backed keys matter for auditors. Valeria covers Percona’s open source `pg_tde` extension for Percona Server for PostgreSQL: no gated features, KMS integrations (HashiCorp Vault, Thales, Fortanix, OpenBao), and the performance picture including WAL encryption moving to GA.

Takeaway: you can meet enterprise compliance expectations for data-at-rest encryption without giving up open source Postgres — and without rewriting the application.
