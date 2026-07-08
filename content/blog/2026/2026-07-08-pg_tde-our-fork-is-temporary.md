---
title: "pg_tde: our fork is temporary, our commitment to open TDE is not"
date: "2026-07-08T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_zsolt', 'TDE', 'Security']
categories: ['PostgreSQL']
authors:
  - zsolt_parragi
images:
  - blog/2026/07/pg_tde_upstreaming.png
---

Recently we noticed a LinkedIn post promoting [open_pg_tde](https://github.com/commandprompt/open_pg_tde), a fork of our [pg_tde](https://github.com/percona/pg_tde), claiming to be more open.
I looked at the repository, and have to disagree with their claim.
In this blog post, I'll explain why.

The short version: open_pg_tde needs the exact same modified PostgreSQL that pg_tde does -- TDE isn't possible without those upstream changes.
The only difference is delivery: they ship those changes as a patch file users have to apply by hand, while we provide a ready-made branch.


## Upstreaming TDE!

The main point of open_pg_tde is that it is more open, as it is not gated behind a vendor fork.
A bit later I'll go into details why I think that's incorrect from a technical point of view, but before that, I want to make something clear:
we do not want to keep TDE in our fork, we are actively working on upstreaming it!

The LinkedIn post also linked to a pgedge blog post written at the end of May, [Why Postgres Lacks Transparent Data Encryption](https://www.pgedge.com/blog/why-postgres-lacks-transparent-data-encryption).

While it seems to be optimistic about the future of encryption in the community version, it also missed that we had not [one](https://2026.pgconf.dev/session/559), but [two](https://2026.pgconf.dev/session/738) sessions about it at pgconf.dev, the first one organized by Kai Wagner from Percona, and the second one by Ants Aasma from Cybertec.

We had some really good discussions during those sessions, and ended up with lots of "homework":
things we wanted to explore and benchmark before continuing the discussion on pgsql-hackers, where the discussion will soon continue.

With this I want to emphasize that Percona is 100% behind making PostgreSQL transparent data encryption open, as part of the community.

![](blog/2026/07/pg_tde_upstreaming.png)

Our fork was born out of necessity, not because we wanted to have our own version.
In fact, if you look back into the [git history of pg_tde](https://github.com/percona/pg_tde/commits/main/), or at our [earlier blog posts](https://www.percona.com/blog/protect-your-postgresql-database-with-pg_tde-safe-and-secure/), we first tried to make it work without any upstream patch. Unfortunately, that didn't work out.

## Why do we have our fork?

The open_pg_tde documentation publishes the following comparison table:

![](blog/2026/07/open_pg_tde_comparison.png)

The table is clearly AI generated, and has some misleading and/or inconsistent elements.
Here is what we think a more honest comparison looks like:

| Aspect | pg_tde | open_pg_tde |
| --- | --- | --- |
| Requires a patched PostgreSQL | Yes | Yes |
| How the patches are delivered | Ready-made fork/branch | Patch file, applied by hand |
| Source available, patches cherry-pickable | Yes | Yes |
| Actually vendor locked | No | No |
| API-version safety check | Yes (`PERCONA_API_VERSION`) | No, it was removed |
| Guards against mismatched-package corruption | Yes | No |
| Supports PostgreSQL 16, 17, 18 | Yes | Yes |
| Encrypts temporary files at rest | No | Yes |
| Supports all KMIP- and Vault-compatible key providers | Yes | Yes |

I'll leave out the discussion about temporary files in this blog post.
That's a complex topic by itself, it raises many questions, and we have good reasons why we are still thinking about it instead of shipping a quick version prototyped with Claude.
It is something I plan to talk about later, on its own.

Back to the comparison: it claims that pg_tde is vendor locked because it only works with our fork.
I don't think that's the case:
Our fork is completely open source, anybody can go to our [GitHub](https://github.com/percona/postgres/) and cherry-pick our patches manually.

open_pg_tde doesn't remove the need for these patches: it can't, TDE requires them.
It just ships them as a patch file users apply manually, rather than as a branch.
Both approaches modify PostgreSQL identically.

The fork exists for one sole reason:
convenience, we want to make the life of our users easier.
Checking out a fork is easier than manually applying patch files.

So the difference between pg_tde and open_pg_tde is not *whether* you patch PostgreSQL, you do, either way.
It's *how* those patches reach you.

## PERCONA_API_VERSION

The open_pg_tde commit that [removes "vendor lock-in"](https://github.com/commandprompt/open_pg_tde/commit/55ed7f1c4ad5bb31ab085e378699377c04158d09#diff-2b9df17a765260aa1b6bc32fedb30dee1d5f80f975252c2bf6308e5097591aac) is mainly a documentation change:
it adds the patch file, and asks users to apply it manually.

It has one single code change other than that:
in our upstream fork we define `PERCONA_API_VERSION` and check against it, and open_pg_tde removes both.

While it has PERCONA in its name, and because of that it has been misinterpreted as vendor lock-in, that isn't why we added it:
it's to prevent accidents.

And with encryption, which modifies the storage of data, **accidents might mean data corruption**.

PostgreSQL normally is very stable:
minor versions contain only bugfixes, the API/ABI is very stable, a minor upgrade is considered easy and safe.

However, when you start applying patches manually, you break this promise:
is your patch as stable as PostgreSQL itself?

The reality is that it's not.
pg_tde is backported to earlier major versions. Both pg_tde and open_pg_tde support PostgreSQL 16, and we could backport it to even earlier versions.

This means that the patch has to apply to multiple major versions, and if we have to make a breaking change in it?
Then we have to make that change in all major versions!

Our API version isn't about locking users to our fork, it's a safety net.
It is there to make sure that upgrades happen correctly, and our users don't accidentally mix pg_tde and PostgreSQL packages that aren't 100% compatible, but seem to work.

Imagine this:

1. You have a working PostgreSQL + pg_tde installation
2. There's an update, you upgrade PostgreSQL
3. What you didn't notice is that we also updated pg_tde.
   You forgot to update that package, or for some reason intentionally didn't update it yet, and because we didn't break the API boundary, everything seems to work.
   Except, we did change some internal details of how our patch works.
   It doesn't cause any visible issues at first, but slowly some pages of your database are becoming unreadable, or you start getting segmentation faults when accessing a table...

The above of course is a hypothetical scenario, we didn't release any dangerous update like that.

But the point is, even if we have to, in pg_tde, we have safeguards.
In our solution the API version check catches this: at the 3rd step, instead of a slow data corruption, we present you with an early error stating that you should fix your system.

In the above scenario, let's say that in the first step you have a working installation where both the server and pg_tde have `PERCONA_API_VERSION=1`.
After that, you only update the server, and the new version now has `PERCONA_API_VERSION=2`.
Since the extension is still at the previous version 1, the server will fail immediately at startup, reminding you that these two packages are not compatible.

Maybe we could have called it something different, `TDE_PATCH_VERSION`, or something like that.
But the goal is still the same, it is an important safeguard, please do not remove it!
Currently open_pg_tde doesn't protect against this type of mismatch.

In fact, in our latest release, not yet included in open_pg_tde, we did increment PERCONA_API_VERSION because of a slightly incompatible change.
We don't expect any data corruption possibilities from it, it was a very minor API change, but we want to play things safe, as keeping the data of our users secure is our first priority.

## Patches welcome!

If we look into the git history of open_pg_tde, it's mostly (AI written) documentation changes.
Other than the removal of the API check I explained above, there are two actual code changes:

* One is the addition of the AES-XTS algorithm for encrypting relation pages
* Another is the support for temporary file encryption

We would be happy to start a discussion of any of these features, or even others.
If you want to contribute, please do not hesitate, and contact us.

This is the strength of open source: it allows contributions and open discussions.
While the team behind open_pg_tde, or anybody else, can of course fork pg_tde this way (because we are open and do not gatekeep features), the energy spent on that could be used to make pg_tde better in a shared community effort.

You can open a [Pull Request](https://github.com/percona/pg_tde/pulls), or a [GitHub Issue](https://github.com/percona/pg_tde/issues), or even use our [Jira](https://perconadev.atlassian.net/projects/PG/issues/), all options are equally good!

Even an issue/PR stating "please call PERCONA_API_VERSION differently", we are not against changing that if the consensus is that it should be something different.

But please don't create forks without even reaching out to your "upstream".
That only increases fragmentation, and makes the life of our common audience harder.

What we ask for is simple: let's make PostgreSQL better with our work, not harder to use.

![](blog/2026/07/open_pg_tde_do_not_fork.png)
