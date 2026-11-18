---
title: "When did I start contributing to pgBackRest, exactly?"
date: "2026-11-19T14:00:00+01:00"
tags: ['PostgreSQL', 'pgBackRest', 'Community', 'Contributions', 'pgstef']
categories: ['PostgreSQL']
authors:
  - stefan_fercot
images:
  - blog/2026/11/pgbackrest-contribution-journey-preview.png
slug: when-did-i-start-contributing-to-pgbackrest-exactly
---

In October, I was in the audience at PGConf.EU for ["The Monday We Learned Who Maintains Our Backups"](https://www.postgresql.eu/events/pgconfeu2026/schedule/session/7963-the-monday-we-learned-who-maintains-our-backups/), by David Steele and Jan Wieremjewicz. I was happy to hear how pgBackRest was born, straight from the person who wrote it.

![David Steele and Jan Wieremjewicz on stage](blog/2026/11/the-monday-we-learned-who-maintains-our-backups.jpg)

One slide listed the project's founding major contributors: David, Cynthia Shang, Stephen Frost, and Reid Thompson. The next slide added "Next:" above my own name.

I knew I had been around for a while. But I didn't realize how long it had been. So I sat there wondering: when did I start contributing, exactly? I decided to go back through the GitHub history to find out.

## When did I start, exactly?

February 2019. My first pull request, [#675](https://github.com/pgbackrest/pgbackrest/pull/675), is dated 12 February 2019. It proposed adding a check to the `info` command to verify that the WAL segments needed by the backups were actually present in the repository. David answered the next day.

That pull request was never merged. David was concerned about adding that much I/O to a command that has to stay fast, and I ended up implementing the check in [check_pgbackrest](https://github.com/pgstef/check_pgbackrest), the monitoring plugin I had started back then.

But one line in the patch fixed a real bug: `info` was not showing the minimum and maximum archived WAL segments when a stanza was specified. David committed that line on 21 February 2019 with the words "Fixed by Stefan Fercot", and it shipped in v2.11 on 11 March. So my first [contribution to land](https://github.com/pgbackrest/pgbackrest/commit/80df1114bdc9) in pgBackRest was a one-line fix, nine days after I showed up.

Over the following months, I gradually got more involved:

- **July 2019:** my first issue, [#781](https://github.com/pgbackrest/pgbackrest/issues/781), a question about S3 configuration with MinIO.
- **April 2020:** my second contribution to the code, showing in `info` when a backup or expiration operation is running.
- **June 2020:** my first comment on one of David's pull requests, [#1068](https://github.com/pgbackrest/pgbackrest/pull/1068), about `repo-ls`.
- **July 2020:** my first answer to a user's issue, [#1096](https://github.com/pgbackrest/pgbackrest/issues/1096), and my first two pull requests merged through GitHub: the [expire-auto](https://github.com/pgbackrest/pgbackrest/pull/1098) option and automatic cipher passphrase detection in [repo-get](https://github.com/pgbackrest/pgbackrest/pull/1095).

Then it became a habit. Between July 2020 and September 2023, I opened 27 pull requests, and 23 were merged: `archive-mode-check`, `db-exclude`, `repo-retention-history`, `restore --type=lsn`, and more.

## Reviewing a patch back then

Reviewing a patch was time-consuming. I read the diff, then the code around it, until I understood what the change was supposed to do.

Then I had to see it work. That meant building pgBackRest from the branch, installing it in a local test environment by hand, and checking that it behaved the way the patch said it should.

The check_pgbackrest test suite helped me with that. It uses Ansible to deploy typical setups with either a shared repository or a dedicated repository host. It can build pgBackRest from source and run an activity script against POSIX, S3, or Azure repositories. I had written it to test the monitoring plugin, but it also became my test environment for reviewing patches.

## The numbers back then

"Back then", for me, is July 2020 to September 2023: the thirty-nine months when I contributed code and reviews regularly. Here is what the GitHub history shows for that period.

- **Issues:** 740 issues were opened (excluding bots), about 19 a month. Among the 730 that received an answer, the median time to first answer was 8.3 hours. Two thirds of all issues got an answer within a day. I gave the first answer to 37% of all issues, and David on 52%.
- **Pull requests:** 366 were opened, about 9 a month. David opened 222 of them, and everyone else opened 144.
- **First review:** among the pull requests that received a formal GitHub review, the median time to first review was about 20 hours.
- **Merge:** among merged pull requests, the median time to merge was 47 hours. Of all pull requests opened during that period, 72% were merged within a week.
- **My reviews:** I reviewed 74 pull requests, about two a month, and 67 of them were David's. My first formal review came a median of 17.5 hours after the pull request was opened.

Then came a period when I no longer had time at work to contribute code. I still tried to help by answering GitHub issues and advocating for the project.

## Back at it, at a different speed

Thanks to Percona, I have work time for pgBackRest again, and the first thing I noticed was the speed.

Let's compare three periods: July 2020 to September 2023 ("Back then"), October 2023 to August 2026 ("In between"), and 1 September to 18 November 2026 ("Now").

| Measure | Back then | In between | Now |
| --- | --- | --- | --- |
| Issues opened per month | 19.0 | 12.7 | 10.4 |
| Median issue body length | 1,782 characters | 1,883 characters | 2,693 characters |
| Median time to first answer on an issue | 8.3 hours | 7.4 hours | 14.5 hours |
| Pull requests opened per month | 9.4 | 5.8 | 21.3 |
| Pull requests opened by David per month | 5.7 | 3.5 | 13.2 |
| Median time to first formal review | 19.6 hours | 29.7 hours | 17.4 hours |
| Median time to merge (merged pull requests only) | 46.6 hours | 99.4 hours | 39.3 hours |
| Pull requests merged within a week (at least a week old) | 72.4% | 51.7% | 57.1% |
| Distinct pull requests I formally reviewed per month | 1.9 | 1.3 | 8.1 |

**Issue reports are longer.** There are fewer of them per month, but the median issue body is now about 2,700 characters long, compared with 1,800 back then. Markdown headings appear in 44% of reports (12 of 27), compared with 8%. Longer reports are not necessarily easier to resolve, of course.

**We receive a lot of pull requests.** There have been 55 since 1 September, more than twice the monthly rate back then. David alone opened 34, including 20 in November by the time I collected the data. And 12 people opened their first pgBackRest pull request, compared with 23 over the full thirty-nine months back then.

**Reviews are still moving quickly.** Among pull requests that received a formal review, the median time to first review is about 17 hours, compared with 20 back then. Among merged pull requests, the median time to merge is 39 hours, compared with 47. Six of the 55 recent pull requests had not received a formal review when I collected the data, so those medians do not describe every submission.

**My own activity has really picked up in November.** Between July 2020 and September 2023, I reviewed 74 pull requests, about two a month. Since September 2026, I've reviewed 21, including 19 in November alone. Of the pull requests opened since September, 17 were merged after I reviewed them. For those, the median time from my first formal review to merge was 3.9 hours, compared with 24 hours back then.

**Many pull requests from other contributors are still open.** Of the 21 opened since September by people other than David, 13 are still open. Twenty were at least a week old when I collected the data; seven of those had been merged within their first week. That is 35%, compared with 62% back then. These pull requests also add more code: a median of 161 lines, compared with 93.

*Numbers were extracted from the GitHub API on 18 November 2026.*

## Reviewing a pull request today

Today, I no longer build a test environment by hand for each pull request. Thanks to the wizardry of my colleague [Zsolt](https://github.com/dutow), the process is partly automated.

The automation picks up every pull request David opens, and I queue the others manually when needed. A new commit on a pull request I follow triggers another review.

The review process runs in Docker. A container fetches the pull request and its discussion, then builds both the proposed changes and the base branch.

An LLM reviews the change in six phases: overview, design, code review, validation, cross-checking against the discussion, and summary. The prompt includes pgBackRest's own practices: the coding standards, the 100% coverage rule, and a reminder that this is not PostgreSQL code.

Every finding has to be backed up. Depending on the finding, that means tracing the code path, writing a test and running it through pgBackRest's test harness, or running an actual backup and restore with the latest version of PostgreSQL. Findings that do not hold up are discarded.

For me, one of the hardest parts of both development and review is still getting the regression test right. It needs to catch the bug and prevent it from coming back, while staying focused and easy to understand. Finding that balance remains a challenge.

Then comes my own review. I read the summary, then I read the pull request itself. If I do not understand something, I ask questions until I can explain the change in my own words.

I do not want to approve a pull request without a comment. So I write down what I tested and how I understand the change. Ten of my November reviews led David to make a change: a fix, a regression test, a release note, some help text, or even a new pull request.

The tools help me work through more pull requests, but I still want to understand and explain what I'm approving.

## Releases follow a new rhythm

![Timeline of every pgBackRest release since v2.00, one dot per release: patch releases appear in June 2024 and make up 9 of the 17 releases since then](blog/2026/11/pgbackrest-release-timeline.svg)

*Source: pgBackRest release notes, from v2.00 (23 February 2018) to v2.60.1 (16 November 2026).*

The release rhythm has changed too. For years, every release was a full release, roughly every four to six weeks while the code was being migrated to C, then roughly every nine weeks from 2021 to mid-2024. An urgent fix either waited for the next one or forced a full release early, as happened with v2.43, six days after v2.42 in November 2022.

Patch releases changed that. The schedule is now written down in the [release documentation](https://pgbackrest.org/release.html): "Feature releases are scheduled for the third Monday of January, April, July, and October. Patch releases are scheduled for the third Monday of any other month as required."

Feature releases are now scheduled once a quarter, and an important bug or security fix can go out between them. An urgent patch release can also come ahead of the scheduled Monday: v2.59.3 fixed a weak encryption subkey bug one week after v2.59.2.

That means fixes can reach users sooner. In 2026, 15 of the 21 bug fixes that came through a pull request went out in a patch release. The median time from merge to release was 11 days, compared with 18 days from 2021 to 2023.

## New contributors and the reviews we are missing

Since September, 12 people have opened their first pgBackRest pull request.

That is good news, and it raises two questions. Do they come back? And do they review?

| First pull request | People | Opened a second one | Reviewed someone else's |
| --- | --- | --- | --- |
| Jul 2020 – Sep 2023 | 23 | 10 (43%) | 7 (30%) |
| Oct 2023 – Aug 2026 | 40 | 14 (35%) | 3 (8%) |
| Since Sep 2026 | 12 | 2 so far | 1 so far |

**Many come back.** Across the project's GitHub pull request history, 94 people other than David have opened a pull request, and 40 have opened at least two. Of the 12 newcomers since September, 2 already have. The older groups have had much longer to contribute again, so we cannot compare those return rates directly.

**Fewer take part in reviews.** Only 14 of those 94 people have submitted a formal GitHub review on someone else's pull request. By the time I collected the data, 7 of the 23 newcomers from July 2020 to September 2023 had done so, compared with 3 of the 40 who arrived between October 2023 and August 2026.

The gap is visible in the last few months too. Since September, 18 people have opened 55 pull requests. Only three people have submitted formal reviews on those pull requests: Douglas J Hunley, David, and me.

David put it plainly on 17 November, when a new contributor asked what else was needed to get a pull request reviewed: "[Just a bit of patience. Right now we have a lot of patches and few reviewers.](https://github.com/pgbackrest/pgbackrest/issues/2888#issuecomment-6950141671)"

So if you are new here, please be patient, and consider offering reviews too. You do not need commit rights or years of experience with the project to read someone else's pull request, build it, test it, and share what you tried and what you understood.

## One thing has not changed

Almost eight years after that one-line fix, pgBackRest is receiving more than twice as many pull requests per month as it did during my earlier period of regular contributions. For the pull requests that get reviewed and merged, the median review and merge times remain comparable.

As of 18 November, every one of the 574 pull requests merged through GitHub was merged by David.

So if your first pull request waits a little, please be patient. Every merge still goes through one person. And while you wait, review someone else's.
