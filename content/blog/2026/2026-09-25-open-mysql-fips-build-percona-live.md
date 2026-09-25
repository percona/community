---
title: "Open FIPS Build, Vectors, and Binlog Server: Marco Tusa at Percona Live"
date: "2026-09-25T11:00:00+00:00"
tags: ['MySQL', 'Percona Live', 'Open Source', 'Percona Server', 'PXC']
categories: ['MySQL', 'Community']
authors:
  - daniil_bazhenov
images:
  - blog/2026/09/marco-tusa-percona-live-amsterdam-cover.jpg
slug: open-mysql-fips-build-percona-live
---

This post collects the main things Marco Tusa covered in his keynote at Percona Live 2026 in Amsterdam: where Percona stands on MySQL, which features landed in the server, and what holds the MySQL community together.

Watch it here: ["I Was Going to Show You a Roadmap"](https://www.youtube.com/watch?v=cB6iDhdWW8o), about 18 minutes.

Start with the community, because the rest of it follows from there. In 2011, after the Sun and Oracle acquisitions, O'Reilly stopped the MySQL Conference, and Percona kept a conference going when nobody knew what came next. The community scattered again more recently, and Peter Zaitsev and others regrouped it in the [OurSQL Foundation](https://oursqlfoundation.org/). MySQL, MariaDB, and Percona ship competing solutions. The people running and building them are one community, with one shared interest: this environment stays usable and open.

## Oppose the decision, not the people

MariaDB moved later Galera development inside an enterprise circle. The MariaDB Foundation pushed back. MariaDB keeps its own version, and others can still improve it. Percona keeps shipping Percona XtraDB Cluster (PXC). PXC has been in production since about 2012, and it was not built as a reply to that dispute. The argument is with the decision, not with the people who made it.

The same rule applies inside Percona. A FIPS implementation in the Pro Build program was available to customers and not to everyone else. That broke the mandate to stay open. The code is open now: it is the default, and everyone can get it.

## What is already there

This is work in progress, not a list of future dates.

- A binlog server, shown in Yura Sorokin's talk "Beyond the Dumb Pipe." It is early: a bicycle that should become a full server.
- Vector search inside Percona Server for MySQL, with no separate system beside it.
- Monitoring and observability an agent can use to see a query more clearly.
- MyRocks and PXC, still in active development. They are first-class parts of the server, not items added to fill a list.
- MySQL Enterprise features carried from version to version. Each version needs merges and adjustments. That work stays in the freely available server.

The written vision is at [percona.com/mysqlvision](https://www.percona.com/mysqlvision). The roadmap follows it, in public.

Answer the MariaDB questionnaire from Percona Live, and share the answer. MySQL Calculator is an open source project you can try through the operator. If something is wrong, open an issue.

More sessions from the event are in the [Percona Live 2026 Amsterdam playlist](https://www.youtube.com/playlist?list=PLOgsvlaOXz2c). The same recordings are on the conference site, in [Videos](https://perconalive.com/2026-amsterdam/videos/).
