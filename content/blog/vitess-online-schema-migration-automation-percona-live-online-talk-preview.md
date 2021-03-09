---
title: 'Vitess Online Schema Migration Automation – Percona Live ONLINE Talk Preview'
date: Sat, 10 Oct 2020 00:28:19 +0000
draft: false
tags: ['shlomi.noach', 'MySQL', 'PLO-2020-10']
---

_[Percona Live Online Agenda](https://www.percona.com/live/agenda) Slot: Wed 21 Oct • New York 2:30 a.m. • London 7:30 a.m. • New Delhi 12:00 noon • Singapore 2:30 p.m._

### Abstract

For many, running an online schema migration operation is still a manual job: from building the correct command, through identifying where the migration should run and which servers are to be affected, to auditing progress and completing the migration. Sharded environment poses an additional burden, as any logical migration must be applied multiple times, once for each shard. What if you could just issue an ALTER TABLE ... statement, and have all that complexity automated away? Vitess, an open source sharding framework for MySQL, is in a unique position to do just that. This session shows how Vitess's proxy/agent/topology architecture, together with gh-ost, are used to hide schema change complexity, and carefully schedule and apply schema migrations.

### Why is your talk exciting?

My work unifies multiple open source solutions (gh-ost, freno, and others) in a single, managed place. Vitess becomes an infrastructure solution, which can automate away the complexities of schema migrations: running, tracking, handling errors, cleaning up. It offers a completely automated cycle for most users, yet still gives them the controls. Whether with gh-ost or pt-online-schema-change, vitess is able to abstract away the migration process such that the user will normally just run and forget. Having worked as an operational engineer, and having developed schema migration automation in my past experience, I’m just excited to think about the users who will save hours of manual labor a week with this new offering.

### Who would benefit the most from your talk?

Operational DBAs and engineers who perform manual schema migrations, or are looking to automate their database infrastructure.

### What other talks are you most looking forward to?

I’m in particular curious to hear about what’s new in distributed databases and geo replication. Otherwise, as always, I’m keen to hear about open source tools in the MySQL ecosystem.

### Is there any other question you would like to answer?

Q: Is this work public? A: Yes, it is. This work is expected to be released as an experimental feature as part of Vitess 8.0, end of October 2020. It is public, free and open source.