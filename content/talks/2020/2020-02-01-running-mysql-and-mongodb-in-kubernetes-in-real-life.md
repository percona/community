---
id: "c3e166e3-b3dd-4b5d-95a0-fe5d4d511377"
title: "Running MySQL and MongoDB in Kubernetes in real life"
layout: single
speakers:
  - sami_ahlroos
talk_url: "https://fosdem.org/2020/schedule/event/mysql_k8s/"
presentation_date: "2020-02-01"
presentation_date_end: ""
presentation_time: "2:10 PM"
talk_year: "2020"
event: "FOSDEM 2020"
event_status: "Done"
event_date_start: "2020-02-01"
event_date_end: "2020-02-02"
event_url: "https://fosdem.org/2020/"
event_location: "Belgium"
talk_tags: ['Kubernetes', 'MySQL', 'Open Source', 'Video']
slides: ""
video: "https://fosdem.org/2020/schedule/event/mysql_k8s/"
---
## Abstract

Running databases in Kubernetes has come a long way. In this talk we will
discuss challenges and issues as well as opportunities and benefits of
doing so as seen in real production use, concentrating on MySQL and MongoDB.
Rolling out a database is easy enough, but things can and will get interesting when
scaling up and down, or taking and restoring backups. How to find out the
last backup is in fact going to restore without issues? We will also look into
monitoring the deployment.

Outline:
- Introduction
- Installing
  - MySQL in Kubernetes
  - MongoDB in Kubernetes
- Scaling up, scaling down
- Backup, restore, verification
- Monitoring (PMM)
- What could possibly go wrong?

Takeaways:
This presentation should encourage the audience to embrace possibilities of
running databases on Kubernetes, and provide attendees with the "do's and
dont's" of such a deployment.