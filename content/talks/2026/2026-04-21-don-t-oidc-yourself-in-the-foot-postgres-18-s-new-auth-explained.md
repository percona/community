---
id: "310674d0-91f3-80ea-8fe9-fad9aae63063"
title: "Don’t OIDC Yourself in the Foot: Postgres 18’s New Auth Explained"
layout: single
speakers:
  - zsolt_parragi
talk_url: "https://www.postgresql.eu/events/pgconfde2026/sessions/session/7555-dont-oidc-yourself-in-the-foot-postgres-18s-new-auth-explained/"
presentation_date: "2026-04-21"
presentation_date_end: "2026-04-22"
presentation_time: ""
talk_year: "2026"
event: "PGConf Germany 2026"
event_status: "Accepted"
event_date_start: "2026-04-21"
event_date_end: "2026-04-22"
event_url: "https://2026.pgconf.de/"
event_location: "Essen, German"
talk_tags: ['PostgreSQL', 'OIDC']
slides: ""
video: ""
---
## Abstract

Postgres 18 adds native support for OAuth and OpenID Connect (OIDC) authentication, one of the most significant security-related changes in years. While widespread adoption will take time, since the feature requires client-side support and external validators, it is already possible to experiment with command-line clients like psql together with validators such as pg_oidc_validator.

This talk includes a demo of a minimal setup using Keycloak and pg_oidc_validator, showing how developers and DBAs can start experimenting immediately. We’ll then dive into how PostgreSQL integrates with OIDC under the hood, demystifying the flow from token issuance to database login.

OIDC promises convenience and streamlined “single sign-on,” yet it’s surprisingly easy to deploy insecurely, and sometimes less secure than traditional password-based authentication. This session highlights the most common pitfalls, misconceptions, and misconfigurations seen in OIDC deployments and provides clear guidance on how to avoid them. Attendees will leave with a practical understanding of both the power and the sharp edges of OIDC in Postgres 18.