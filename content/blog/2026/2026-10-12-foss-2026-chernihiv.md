---
title: "FOSS 2026 conference in Chernihiv: how it went"
date: "2026-10-12T10:00:00+00:00"
tags: ["Percona", "Community", "Events", "Conferences", "Open Source", "Education", "MySQL", "MongoDB", "PMM"]
categories: ['Community']
authors:
  - evgeniy_patlan
images:
  - blog/2026/10/foss-2026-chernihiv-cover.png
---

On October 1-2, Chernihiv Polytechnic National University held the II International scientific and practical conference [“Free/Open Source Software in Education, Science & Business”](/events/2026-feit-stu-foss/). The conference was online and free for everyone. The idea is to bring together people from universities, from industry and from open source communities and talk about how free software is used in education, science and business.

This year Percona was well represented. There were six speakers from Percona, and two more keynote speakers also worked at Percona in the past.

## Day 1: keynotes

The first day started with welcome words from Volodymyr Bazylevych, Chair of the Organizing Committee, and Anatolii Prystupa, Vice-Rector for Research. After that there were five keynote talks.

**Yevhen Patlan (Percona)** spoke about embedding DuckDB into MySQL. MySQL works very well for transactions, but analytical queries over hundreds of millions of rows can take a long time on InnoDB. Usually people solve this by copying data to a separate column store, so they need to support two systems and a pipeline between them. Yevhen showed another way: run DuckDB inside MySQL. He talked about Percona’s experimental DuckDB engine for MySQL 9.7: how query pushdown works, how results stay the same as in InnoDB, and the TPC-H results on 500 GB. He also told about a two-phase commit bug that made a replica lose data without any error.

**Frédéric Descamps (MariaDB Foundation)**, known in the community as “lefred”, worked many years at Percona and then in the MySQL Community Team. This year he joined the MariaDB Foundation. In his talk he showed MariaDB Server features that people often don’t know about: system-versioned tables, flashback, sequences, invisible columns and others. For every feature he explained which real problem it solves.

**Sergii Shchaslyvyi (AWS)** talked about virtualization. After the licensing changes, many companies started to look for alternatives to their current virtualization platform. Sergii explained what migration options exist and where open source technologies make sense.

**Oleksiy Lukin (Percona)** is not a new person for this conference. He worked at Chernihiv Polytechnic for more than 20 years and has been one of the organizers since 2009. Oleksiy presented kmipclient and kmipcore, an open source C++ library for KMIP (Key Management Interoperability Protocol). It supports KMIP 1.4 and 2.0, it is tested with five different KMIP servers, and Percona Server for MySQL already uses it.

**Vinicius Grippa (Readyset, Oracle ACE Director)** finished the first day. Before Readyset he worked at Percona for eight years. He presented myflames, an open source tool that builds flame graphs, treemaps and Visual Explain style diagrams from MySQL execution plans. With these pictures it is much easier to understand where a query spends time.

## Day 2: track talks

On the second day there were 13 talks from researchers, teachers and students. A team from Chernihiv Polytechnic presented a browser-based simulator for STM32 firmware and electrical circuits. Other talks were about microgrid optimization with CVXPY, local AI on x86 NPUs, digital education in crisis conditions, cyber hygiene for students and teaching steganography with free software.

Four more Percona engineers spoke on this day:

- **Adnan Šupić** - zero-downtime migration with Percona ClusterSync for MongoDB
- **Puneet Kala** - a practical open source stack for running MongoDB
- **Fabio Silva** - how PMM hosts another application inside an iframe
- **Briana Swift** - how to manage public messaging for seven database technologies without a PMO, using a public GitHub repository and treating text like code

## Some numbers

- 82 registered participants
- 51 submitted theses
- 18 talks
- more than 90 people online
- participants from Ukraine, Belgium, Brazil, The Gambia, India and other countries

Big thanks to the computer engineering students of Chernihiv Polytechnic. They were active during both days and asked speakers a lot of good questions.

## Thanks to our partners

The conference would not be possible without our partners:

- **Chernihiv Polytechnic National University** - for hosting and organizing the conference.
- **WIN-WIN EDIH** - the conference was held as part of this project, co-funded by the European Union.
- **Percona** - for the support and for six speakers.
- **MariaDB Foundation** - for the support and the keynote about MariaDB Server.
- **Amazon Web Services (AWS)** - for the support and the keynote about migration from proprietary virtualization.
- **Readyset** - for the support and the keynote about myflames.
- **OurSQL Foundation** - for the support of the conference.
- **PortaOne** - for the support of the conference.
- **Chernihiv IT Cluster (Chernihiv.IT)** - for helping to connect the university with the local IT community.

Thanks to you, the conference stays free, and Ukrainian students and researchers can listen to and talk with people from the international open source community.

## Recordings and materials

- Keynote recordings on YouTube: [https://www.youtube.com/@foss-che](https://www.youtube.com/@foss-che)
- Program and slides: [https://feit.stu.cn.ua/foss/](https://feit.stu.cn.ua/foss/)
- Conference proceedings will be published at the end of October.

Thanks to all speakers, authors and participants. See you at FOSS 2027!

*The conference was held as part of the WIN-WIN EDIH project, co-funded by the European Union (Grant Agreement No. 101191647). Views and opinions expressed are those of the authors only and do not necessarily reflect those of the European Union or the granting authority.*
