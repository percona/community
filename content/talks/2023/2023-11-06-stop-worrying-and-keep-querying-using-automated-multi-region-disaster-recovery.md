---
id: "54e893d9-733c-4193-9d43-faf6e0b305aa"
title: "Stop Worrying and Keep Querying, Using Automated Multi-Region Disaster Recovery"
layout: single
speakers:
  - sergey_pronin
talk_url: "https://colocatedeventsna2023.sched.com/event/1Rj5I/stop-worrying-and-keep-querying-using-automated-multi-region-disaster-recovery-shivani-gupta-elotl-sergey-pronin-percona"
presentation_date: "2023-11-06"
presentation_date_end: ""
presentation_time: ""
talk_year: "2023"
event: "KubeCon NA 2023"
event_status: "Done"
event_date_start: "2023-11-06"
event_date_end: "2023-11-09"
event_url: "https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/"
event_location: "Chicago, IL"
talk_tags: ['PostgreSQL', 'Cloud', 'Kubernetes', 'Cloud Native']
slides: ""
video: ""
---
## Abstract

Disaster Recovery(DR) is critical for business continuity in the face of widespread outages taking down entire data centers or cloud provider regions. DR relies on deployment to multiple locations, data replication, monitoring for failure and failover. The process is typically manual involving several moving parts, and, even in the best case, involves some downtime for end-users. A multi-cluster K8s control plane presents the opportunity to automate the DR setup as well as the failure detection and failover. Such automation can dramatically reduce RTO and improve availability for end-users. This talk (and demo) describes one such setup using the open source Percona Operator for PostgreSQL and a multi-cluster K8s orchestrator. The orchestrator will use policy driven placement to replicate the entire workload on multiple clusters (in different regions), detect failure using pluggable logic, and do failover processing by promoting the standby as well as redirecting application traffic