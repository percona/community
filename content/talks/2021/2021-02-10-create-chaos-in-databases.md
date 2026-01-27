---
id: "eef0d065-de2e-494a-9f87-56e0604e10ef"
title: "Create Chaos in Databases"
layout: single
speakers:
  - vadim_tkachenko
talk_url: ""
presentation_date: "2021-02-10"
presentation_date_end: ""
presentation_time: "10/Feb/21 10:00 PM"
talk_year: "2021"
event: ""
event_status: "Done"
event_date_start: ""
event_date_end: ""
event_url: ""
event_location: ""
talk_tags: ['Kubernetes']
slides: ""
video: "https://www.youtube.com/watch?v=fSgtUflRqCU"
youtube_id: "fSgtUflRqCU"
---
## Abstract

Database is a critical piece of the infrastructure. With applying some chaos we can improve resiliency and reliability of a system that handles our data. In this talk I will discuss how we evaluate resiliency and reliability of our Percona XtraDB Cluster Operator (MySQL) and Percona Server for MongoDB Operator. We run MySQL and MongoDB in Kubernetes and we are looking to proving automatic deployment and management of database nodes and we need to make sure our data and management layer is able to sustain different kind of failures. For this I will discuss what kind of failures we are looking for, how we apply them and how database handle them.