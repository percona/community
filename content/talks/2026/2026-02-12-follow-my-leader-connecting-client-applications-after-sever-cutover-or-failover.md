---
id: "2f5674d0-91f3-80a9-bde7-eaa64953e059"
title: "Follow my Leader - connecting client applications after sever cutover or failover"
layout: single
speakers:
  - alastair_turner
talk_url: ""
presentation_date: ""
presentation_date_end: ""
presentation_time: ""
talk_year: "2026"
event: "Postgres Edinburgh Feb 2026"
event_status: "Accepted"
event_date_start: "2026-02-12"
event_date_end: ""
event_url: "https://luma.com/user/vyruss?e=evt-7qhEzVfw0eiEYK8"
event_location: ""
talk_tags: ['PostgreSQL']
slides: ""
video: ""
---
## Abstract

During a planned changeover, or after the failure of a primary, smoothly promoting a Postgres replica is not the end of the problem. It’s the start of a new phase of the problem - getting the clients connected to the right Postgres instance.

It’s quite clear where the promotion and demotion of instances should take place, even if there are a few options for how to manage it. Making sure that client applications only try to write to the primary can be done in many places, from the client library in the application to the network configuration of the servers. Picking the best option is not just about technical correctness or elegance. Decisions also affect the ease of change, consistency across the environment, complexity of each deployment and costs.

Join me for an overview of where DBAs, application teams and network teams can take control of how applications connect after a changeover, and how to pick an option.