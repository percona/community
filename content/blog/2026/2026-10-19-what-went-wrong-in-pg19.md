---
title: "What went wrong in PG19: a case study of a revert"
date: "2026-10-19T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'Community']
categories: ['PostgreSQL']
authors:
  - zsolt_parragi
images:
  - blog/2026/10/pg19.png
---


In my previous blog post about the [PostgreSQL 19 delays](/blog/2026/10/15/apologies-for-delaying-postgres-19/), I mentioned reverts, or rather incomplete features, as one of the main causes behind it.
In this post, I'd like to present a specific feature as an example, and talk about what could have helped save the release, and the feature.
What could we do better next time, what do we have to change?

Previously I focused on what was different with this release, what made it worse than the many before it.
This time, I want to approach the question from a different angle, and look at the PostgreSQL development process overall, asking the question: what could we do differently?
But before we dive into details of that, let's start again with the most important part:

**YOU** could have helped.

# But PostgreSQL Hackers are scary!

PostgreSQL development seems complex, even by the standards of software projects:

1. First, you have to go to the mailing list -- what even is a mailing list in 2026?
2. Then you have to read through all those scary emails quoting source code fragments
3. Then you have to figure out which attachment is the latest patch
4. Download it
5. Apply it on top of the postgres sources, which you also have to figure out how to get
6. Build everything
7. And finally start the server up to begin testing

And what's even worse, people do throw those source code fragments around in the messages, so of course you assume you have to as well.
Even if you find a bug, how can you tell why it is happening?
That question can be difficult even for experienced developers freshly joining the project.

We could say that it's 2026, you can ask an AI agent, and it will confidently give you an answer you can copy-paste -- but let's assume we are trying to avoid being the human delivery mechanism for slop.

# The misconception: a review needs a developer

I'm not saying we don't need all the above -- developers discussing code quality and deducing bugs from the source code -- because we do.
But, especially with LLMs around, we need something even more important:
people actually trying features out, and saying that they work as expected, or the opposite, that they do something confusing.

You don't have to be a developer, anybody familiar with databases and PostgreSQL can help the project:
read the feature description, start up the server, try it out!

And sometimes it's even easier: if you start reading the documentation and find yourself scratching your head, thinking that something doesn't make sense there, then you found an issue without even sending a single SQL command to psql.

And before you can complain about the difficult steps above, I want to come back to the reverts I mentioned:
some of the reverted features should have raised many eyebrows at that step, simply when people read the documentation of the feature.

Other features should have raised questions when people tried slightly trickier scenarios with them, and then sent confused "Why is this happening?" questions to [bugs](https://www.postgresql.org/list/pgsql-bugs/) or [hackers](https://www.postgresql.org/list/pgsql-hackers/).

As [Alastair Turner recently mentioned on LinkedIn](https://lnkd.in/p/ergUiHPp), for PGQ all you had to do was create a schema and some data, dump it, restore it, and then write a disappointed email that you didn't get the same thing back.

All of the reverted features were committed, and after that they were easily available to anybody using the [development snapshots](https://www.postgresql.org/download/snapshots/).
Despite the scary name, those are essentially what most projects call "nightly builds", a release built from the master branch periodically.
These make it easy for anybody to try out already committed features.

# You CAN try out in-progress patches

And I also want to reiterate my point from the previous blog post:
the CI on [hackorum.dev](https://hackorum.dev) now automatically publishes a docker image for every patch submission.

If you find a thread with an interesting patch, all you have to do is execute:

```
docker run --rm -p 5432:5432 ghcr.io/hackorum-dev/postgres-patch:t<THREAD-ID>
```

Where `<THREAD-ID>` is the numeric identifier you can also see in the navbar; every thread also shows its own exact command.

This allows you to test features, or bugfixes to features, even before they become part of the main PostgreSQL development branch.

# SPLIT / MERGE PARTITION(S)

The rest of the post will mostly focus on a single example: the ALTER TABLE ... SPLIT / MERGE PARTITION(S) feature.
Not because this one was worse than the others -- I don't have anything against the feature or its authors -- I chose it simply because it checks all the boxes for the points I want to raise.

I could have chosen another reverted feature, or a combination of them, as any of them would be a good example for at least one of my points.

The idea of the feature itself is simple:
given a partitioned table, combine multiple partitions into one, or split one partition into multiple, preferably in a better way than what DBAs can achieve today by executing multiple commands.
While we could say that the simplicity of a single command is already better, the usual expectation is that it also does less locking, or is faster than the manual commands.

For a feature like this, I think there is one unspoken requirement: stability and safety.
Data integrity shouldn't change, nothing should get corrupted, and nothing surprising should happen that a user wouldn't expect from an `ALTER TABLE` command.

# Not enough post-commit feedback

I already mentioned this in a generic way earlier, but this is particularly bad in this case, so let's reiterate:

For some reverts we can clearly see a pattern: the feature was committed late, shortly before the feature freeze, in a rush to get it in.
Maybe hoping that even if there are some leftover bugs, there will be enough time to sort them out before the RC, and that no major issue gets discovered.

ALTER TABLE ... MERGE / SPLIT wasn't like that.
If we ignore the part that it was also committed and reverted in 2024, the original commit for PG 19 landed in [December 2025](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=1adf16b8fba45f77056d91573cd7138ed9da4ebf).

After that, it received only four fixes overall before the revert:

* in [April](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=713e553e3213d53f4ba25dcb7a8c41994b7cab9d) about missing extension dependencies
* in [June](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=ff8bec8c460a13bedbb416d8697f4675a0709ce8) about missing TOAST tables
* another minor doc change in [June](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=57f19774d6c88f501c835a7772a71ca5ba2bc163)
* in [July](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=881033ae8b55dbd22f7ee9c26991b6c4e67d6bd5) about it creating the new partitions as internal relations

The fifth discussion about the feature started when I read its documentation in the second half of July, and [asked a few questions](https://hackorum.dev/topics/253174).
A few hours later I also discovered that it breaks foreign keys, can insert NULL values into NOT NULL columns, and can cause other constraint failures.

While that second part sounds bad, it could have been easily fixed by itself. However, I think it raises a big warning sign for the development process:
a major feature that was committed 7 months before my discoveries had serious, easily discoverable bugs, and nobody noticed them.

Discovering those bugs didn't require a software engineering degree, the simple QA "let's try to break it" mentality is enough:
read the documentation, think about the corner cases, try them out.
The test cases for the above failures aren't that much more difficult than the PGQ example from earlier.
Even earlier LLMs were able to do such things: they could have been instructed to test this feature, and they would have raised these issues.

I was quite stunned when I discovered how bad some of the issues were, and I was even more surprised when I realized that this wasn't a last minute commit.
The fact that nobody checked before is bad for multiple reasons.

One: if somebody had written the email I wrote sooner, this feature could have been saved.

Two: one of my conclusions in the previous blog post was that I should pay more attention to master, even outside the features I review before they get committed.
And it seems like this should be a lesson for many other people.

# A mailing list thread isn't a pull request

Now that I've tackled the human part, what ordinary people could do to make things better, I want to look at another side we will have to improve: the process.

The mailing list is great.
Lots of conversations happen there, it doesn't lock the development process to a vendor, and it allows us to keep 30 years of history intact.

Except for the part that it isn't an issue tracker, it isn't a pull request.
And because of that, we lack proper tracking.

The original MERGE/SPLIT commit mentions 16 reviewers:

```
    Reviewed-by: Matthias van de Meent <boekewurm+postgres@gmail.com>
    Reviewed-by: Laurenz Albe <laurenz.albe@cybertec.at>
    Reviewed-by: Zhihong Yu <zyu@yugabyte.com>
    Reviewed-by: Justin Pryzby <pryzby@telsasoft.com>
    Reviewed-by: Alvaro Herrera <alvherre@alvh.no-ip.org>
    Reviewed-by: Robert Haas <rhaas@postgresql.org>
    Reviewed-by: Stephane Tachoires <stephane.tachoires@gmail.com>
    Reviewed-by: Jian He <jian.universality@gmail.com>
    Reviewed-by: Alexander Korotkov <aekorotkov@gmail.com>
    Reviewed-by: Pavel Borisov <pashkin.elfe@gmail.com>
    Reviewed-by: Masahiko Sawada <sawada.mshk@gmail.com>
    Reviewed-by: Alexander Lakhin <exclusion@gmail.com>
    Reviewed-by: Kyotaro Horiguchi <horikyota.ntt@gmail.com>
    Reviewed-by: Daniel Gustafsson <dgustafsson@postgresql.org>
    Reviewed-by: Tom Lane <tgl@sss.pgh.pa.us>
    Reviewed-by: Noah Misch <noah@leadboat.com>
```

That means it should be a well-tested, well-reviewed, solid feature, right?

On GitHub, we would see how many people pressed the "Approve" button for the latest patch version, and how many did so for an earlier one.
And if it was an earlier one, we would also see how long ago: whether they reviewed it a few weeks before, after which it only received cosmetic changes, or whether they approved a completely different approach 6 months earlier.

The PostgreSQL situation is not exactly the same.

For PostgreSQL commits, `Reviewed-by` doesn't necessarily mean that the mentioned person wrote a message saying "Approved" / "LGTM" for the final version of the patch.
It simply means that at some point, these people gave some feedback about the patch.

Please note that, similarly to the authors, I don't have anything against the reviewers, and I don't want to criticize their work.
This is an analysis of the `Reviewed-by` records, not of the people, or of their contributions to the PostgreSQL community.

Let's look at some statistics about how these people interacted [in the thread](https://www.postgresql.org/message-id/flat/c73a1746-0cd0-6bdd-6b23-3ae0b7c0c582%40postgrespro.ru), with a table based on both manual reading and LLM help:

| Reviewer | First | Last | Messages | Characters | Nature of feedback |
|---|---|---|---|---|---|
| Jian He | 2025-05, v38 | 2026-06, v68 | 37 | 74266 | Deep, full coverage of the rewrite, ~20 patches attached |
| Alexander Korotkov | 2024-03, v25 | 2026-06, v68 | 66 | 52270 | Committer and co-author |
| Robert Haas | 2022-09, v11 | 2024-08, v32 | 9 | 17780 | Deep, design level, found the privilege escalation |
| Alexander Lakhin | 2024-04, v31 | 2024-05, v31 | 16 | 17130 | Deep, adversarial testing, crashes and security |
| Justin Pryzby | 2022-09, v9 | 2026-06, v68 | 15 | 12340 | Solid, hands on, wrote patches |
| Stephane Tachoires | 2023-03, v14 | 2025-12, v66 | 10 | 5799 | Shallow, CF app build and apply checks only |
| Pavel Borisov | 2024-04, v31 | 2026-06, v68 | 11 | 5258 | Light, reads the diff, mostly cosmetic |
| Alvaro Herrera | 2022-07, v6 | 2026-01, v68 | 7 | 4932 | Light, 3 of 7 flagged "not a review" |
| Zhihong Yu | 2022-05, v2 | 2022-10, v12 | 7 | 2774 | Shallow, naming and typos |
| Noah Misch | 2024-08, v31 | 2024-08, v31 | 1 | 696 | One message, with a working exploit |
| Daniel Gustafsson | 2023-07, v17 | 2024-05, v31 | 2 | 591 | CF admin, rebase request and buildfarm report |
| Matthias van de Meent | 2022-05, v1 | 2022-05, v1 | 1 | 448 | One design question, no review |
| Tom Lane | 2024-05, v31 | 2024-05, v31 | 1 | 341 | One buildfarm report |
| Laurenz Albe | 2022-05, v1 | 2022-05, v1 | 1 | 300 | One question, says he did not read the patch |

Masahiko Sawada and Kyotaro Horiguchi sent no messages to the thread, so they are not included in the table.
Maybe they reviewed elsewhere, that's hard to tell at this point from an outside perspective.

We can't rule out that some of these people really reviewed recent versions outside the thread, but I want to point out that some of the people who responded to my thread and were surprised by the state of the feature are mentioned as reviewers.

And if we take this table as the source of truth, only 5 of the 16 reviewers looked at the patch between its first revert and the commit that brought it back: Alexander Korotkov, Alvaro Herrera, Jian He, Robert Haas, Stephane Tachoires.
Justin Pryzby and Pavel Borisov also posted messages in 2026, but only after the feature was committed again.

Two of them are co-authors of the patch, and Robert Haas's only message after the first revert is a revert postmortem, not a real review.
Alvaro Herrera clearly says in his only later email that

> Note: I didn't actually review the patch.

And Stephane's two messages in that period are basically

> Patches don't apply anymore.
> Could you rebase it please ?

So if this were GitHub or a similar platform, how many of the above 16 would you count as an "Approve!"?

# A mailing list thread isn't an issue tracker

Some of the issues I raised in my questions thread were design decisions.
It seemed strange to me that nobody had raised them before, that the feature got committed without anybody asking these questions.

Except that's not what happened: they were all raised, and then forgotten.

* [Robert Haas raised the problem with silently dropping properties, my point 5](https://www.postgresql.org/message-id/CA%2BTgmoY0%3DbT_xBP8csR%3DMFE%3DFxGE2n2-me2-31jBOgEcLvW7ug%40mail.gmail.com).
* [Jian He discovered the generator expression issue, my point 4](https://www.postgresql.org/message-id/CACJufxFGPLTDW55bgaBTH1uCf0%3DYUZUVKWFrTBvOZNYKc49MxA%40mail.gmail.com).
* [Pavel Borisov asked for coverage in the subscription tests](https://www.postgresql.org/message-id/CALT9ZEEwUkuhyxu2a1S7DYXZqfcy99q78q6BgvNRtpkY%3DVhfVQ%40mail.gmail.com), which would have found the logical replication issues, my first 3 points, but that never happened.

These long threads are not the most efficient way to organize things.
And the above isn't specific to MERGE / SPLIT, it can happen in any long thread, and I assume it happens in most of them.

Let's look at a different example too, so I do not only single out this feature:

A few weeks ago, when I started to test a new (PG20) feature, the [conflict log table for logical replication](https://hackorum.dev/topics/52043), I discovered a bug:
with the already merged patch, `DROP SUBSCRIPTION x RESTRICT;` started to `CASCADE`, while the documentation still said that the restrict/cascade argument doesn't matter, because there are no dependencies.

Before reporting the issue, I asked an LLM to check whether this was already mentioned in the thread.
[It was](TODO), the issue was discussed before the feature got committed, and forgotten shortly after.

That thread is also currently at 689 messages, with multiple parallel discussions going on in October 2026, and people working on multiple fixup patchsets at the same time.
That's not a well organized process, it's chaos, and it's a miracle that it works as well as it does.

And these two are just examples, we could find many more among the long-running threads.

# Where are the open items tracked?

Let's be positive! For now let's ignore the ongoing chaos, and focus on planning for the future instead.

Let's accept that MERGE / SPLIT was committed with these limitations, and let's pretend the revert didn't happen.

Where are we tracking the open items for this?
The "silently discarding properties" part was never meant as a final decision in a complete feature, it was meant as a gate against scope creep.
The expectation was that development would continue, and that the feature would get better.

People should be aware that we have an incomplete feature, and that it has many parts that need improvement, so that they can join the effort.
Where would they be able to find out about this?

And again, to look at other features too, here are a few more examples -- and there are many more:

In April I discovered that postgres [allows OAuth on plaintext connections](https://hackorum.dev/topics/248564), which is clearly insecure.
Apparently this was discussed during development, and for now accepted as-is, to allow for some specific use cases, and to stay in sync with other PG features that allow this.
But Jacob Champion also agrees that we could/should improve this in future versions, so why don't we have a clearly visible open item about this somewhere?

Or recently I started to work on support for [unlogged materialized views](https://hackorum.dev/topics/253126).
That feature has been missing since materialized views were added:
it was part of the original patch, but was quickly reverted after issues were discovered with it.
After that, people attempted to implement it multiple times, and it was discussed in several threads.
Shouldn't we have a single page where this, and other missing but nice to have features, would all be visible?

People, especially newcomers, who want to start contributing to PostgreSQL often ask where they can find good issues to work on.
The usual answer is that there are some wiki pages, and that multiple committers and contributors have their own TODO lists / wishlists somewhere on the internet, all you have to do is magically find them!

# The way forward

LLMs of course can help:
this became another item on my periodic checklist, asking LLMs to track "open items" on long-running threads, to help notice when something gets forgotten.

But that's not a long term, scalable solution, and it immediately breaks if I, or other people doing this, get tired of it or forget.

The proper solution would be a bug tracker.
We have [hackorum.dev](https://hackorum.dev), and we plan to add more features there that could improve this further: showcasing recent development, or maybe even trying to track open items using AI, similar to the AI summaries.
But that's all just a bandaid, not a proper solution, and it doesn't help that much if only some people use the tool, and it isn't enforced.

This is also what we see with the [commitfest](https://commitfest.postgresql.org/): even in 2026, only [40% of the submitted patches](https://hackorum.dev/stats) have a matching commitfest entry.

Think about the [conflict log table](https://hackorum.dev/topics/52043) I mentioned earlier:
it has a commitfest entry, and it is still open as I am writing this post.
However, the main feature was already merged, and people are now working on many bugfixes and improvements for it.
When somebody checks later, it will appear that all of those commits belong to the same commitfest entry. Is that the right way to use it?

I'm not saying that the commitfest doesn't improve things, and a tool for tracking bugs and open items would similarly help, even if only used by part of the community, even if it were imperfect.

In the end, it's up to the people: enforcement and advertising a tool only get you so far.
If a tool isn't helpful or user friendly (or enforced), people can and will always find ways around it.

And this brings us nicely to how this started:
We need more people.

More people to test patches, more people to tell us how to do things differently, more people to tell us what feature ideas they like, more people to say if something is good or bad.
More people to call out that something is wrong.

Open your e-mail client, write a message, join the herd!