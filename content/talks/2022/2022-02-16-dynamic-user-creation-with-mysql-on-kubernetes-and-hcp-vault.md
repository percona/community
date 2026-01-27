---
id: "b82c64f4-9e2b-4ebb-be61-97fc7fab5749"
title: "Dynamic User Creation with MySQL on Kubernetes and HCP Vault"
layout: single
speakers:
  - sergey_pronin
talk_url: "https://events.hashicorp.com/hashitalks2022"
presentation_date: "2022-02-16"
presentation_date_end: ""
presentation_time: "11:00 PM"
talk_year: "2022"
event: "Hashitalks 2022"
event_status: "Done"
event_date_start: "2022-02-17"
event_date_end: "2022-02-18"
event_url: ""
event_location: ""
talk_tags: ['MySQL', 'Kubernetes']
slides: ""
video: "https://www.youtube.com/watch?v=z-zWTxzhEc0"
---

## Abstract

Without dynamic credentials, organizations are susceptible to a breach due to secrets sprawl across different systems, files, and repositories. Dynamic credentials provide a secure way of connecting to the database by using a unique password for every login or service account. With Vault, these just-in-time credentials are stored securely and it is also possible to set a lifetime for them.

In this talk we are going to demonstrate the integration between Percona Kubernetes Operator and HCP Vault to provide dynamic user creation for a MySQL cluster.