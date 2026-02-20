---
title: "PostgreSQL minor release postponed in Q1’ 2026"
date: "2026-02-18T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'pg_stat_monitor', 'monitoring']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2026/02/Jan-Cover-Feb17.png
---

In case you are awaiting the February PostgreSQL Community minor update [released on plan on February 12](https://www.postgresql.org/about/news/postgresql-182-178-1612-1516-and-1421-released-3235/) we want to make sure that our users and customers are up to date and aware of what to expect.

This scheduled PostgreSQL release was delivered by the PostgreSQL Community on time and came carrying 5 CVE fixes and over 65 bugs bug fixes.

Unfortunately shortly after, the [release team announced that an additional out of cycle release](https://www.postgresql.org/about/news/out-of-cycle-release-scheduled-for-february-26-2026-3241/) is planned for February 26. This follow up release addresses two regressions identified in the February 12 update.

Because of this, we have decided not to ship a [Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/18/) build based on the February 12 release. Instead, we will wait for the February 26 Community update and base our release on that version once it becomes available from PGDG. This means also a delay in the release of Percona Operator for PostgreSQL that uses images based on our PostgreSQL releases.

### Always look on the bright side

![](blog/2026/02/Jan-always-Feb17.png)

While this is a delay in release it comes with some benefits. For our users and customers, this means a cleaner upgrade path. Rather than releasing February 12 now and asking you to update again shortly after, we prefer to wait and deliver a single update that includes the fixes. Our goal is to make updates predictable and smooth for users of Percona Distribution for PostgreSQL, as well as extensions such as [pg_tde](https://github.com/percona/pg_tde) and [pg_stat_monitor](https://github.com/percona/pg_stat_monitor). It should also allow you to carry less operational burden with the added maintenance that an extra update would require.

We appreciate how quickly the PostgreSQL Community identified and addressed the regressions. Open collaboration across the ecosystem, including reports and testing from many contributors, helps ensure PostgreSQL continues to improve for everyone.

### Path forward

This is the third out of cycle release in the past year, following similar updates in [November 2024](https://www.postgresql.org/about/news/out-of-cycle-release-scheduled-for-november-21-2024-2958/) and [February 2025](https://www.postgresql.org/about/news/out-of-cycle-release-scheduled-for-february-20-2025-3016/). It highlights how responsive and diligent the PostgreSQL Community is when issues are identified. At the same time, it reminds us all how important continuous testing and collaboration are as PostgreSQL adoption continues to grow. Contributing to PostgreSQL, whether through testing, reporting, or development, is one of the best ways to help strengthen quality across the ecosystem.

### Elephants keep ears open

As soon as the February 26 release is available and our builds are ready, we will share the update.

If you need to move forward with the February 12 version in the meantime, please reach out. We are happy to talk through your situation and help you assess what makes the most sense for your environment.

Our customers can contact us through Percona Support Services to receive the high quality assistance we are known for. We also encourage community users to reach out via the [Percona Community Forums](https://forums.percona.com/), where we will do our best to provide guidance based on the information you share.

Thank you for your trust and for being part of the Percona community.
