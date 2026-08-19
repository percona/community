---
title: "Hackorum Update: What's New Since February"
date: "2026-08-20T10:00:00+00:00"
tags: ["Percona", "PostgreSQL", "Community", "Mailing Lists", "Open Source", "pg_kwagner"]
categories: ['PostgreSQL']
authors:
  - kai_wagner
images:
  - blog/2026/08/hackorum-update-banner.png
---

Back in February, I wrote about [Hackorum](https://hackorum.dev/), a forum style web view of the pg-hackers mailing list. If you missed that post, you can [read it here](https://percona.community/blog/2026/02/02/hackorum-a-forum-style-view-of-pg-hackers/) first. It turns the mailing list into something that reads and navigates a bit more like a modern forum, while the mailing list itself stays the source of truth.

![Hackorum topic index showing pg-hackers threads with commitfest, patch and CI status icons](blog/2026/08/hackorum-update-topic-index.png)

A lot has happened since then. We also talked about the project at the PostgreSQL meetup in Berlin in March, [at pgconf.de](https://www.postgresql.eu/events/pgconfde2026/schedule/session/7760-modernising-postgres-community-communication-with-hackorum/), and in a lightning talk at pgconf.dev, and a good chunk of what was still on the roadmap back then is live today. We also posted [a video introduction to Hackorum](https://www.youtube.com/watch?v=onQQJzQ8Qlw), if you prefer to see it in action rather than read about it. This post is a follow up to walk through what changed, what is new, and what we are looking at next.

## A quick recap

Hackorum is an Open Source project from the community to be used by the community and hosted on [hackorum.dev](https://hackorum.dev/). The code is on [GitHub](https://github.com/hackorum-dev/hackorum). If you are new here, the short version that it syncs postgres mailing lists in the background, keeps read status, stars, tags and notes for you, and adds commitfest context, commit and patch history, and contributor info directly next to the discussion.

Everything below is new for users since the last post. I am leaving out internal and admin only changes, since those do not affect how you use the site day to day.

## Commits linked back to their discussion

![Contributor profile showing commit credits and how many patch threads landed](blog/2026/08/hackorum-update-commit-profile.png)

Hackorum now links pushed commits back to the thread and patch discussion that produced them. Contributor profile pages have a new commit history tab, so you can see someone's message activity and their commits in one place. There is also a [community proposal on pgsql-www](https://www.postgresql.org/message-id/CAAKRu_Z42AAq7N%3DusSS3UPMtXqbVvsQzktNmH1X20oypyqA_Xg%40mail.gmail.com) for public contributor profile pages, with the PostgreSQL Contributors Committee looking to recognize specific contributions beyond code, for example volunteering at a conference. If that lands, it would be a natural fit to surface on this profile too.

## Patch CI results, now public

<img src="/blog/2026/08/hackorum-update-ci-status.png" alt="CI status card on a thread, showing apply, build and test results" style="display:block;margin:1rem auto;width:50%;border-radius:6px;">

Patches attached to a thread are automatically applied, rebased when master moves, and built and tested with the PostgreSQL test suite. Those results used to be an internal experiment, they are now public for everyone:

* CI status icons in the topic index, and full detail in tabs on the thread itself
* A CI dashboard at [hackorum.dev/ci](https://hackorum.dev/ci)
* A per topic CI history view
* A stats overview page

![Patch CI history for a thread, showing every tracked patchset version and its result](blog/2026/08/hackorum-update-ci-history.png)

We reapply the latest version of each patch once a day against current master. If it stops applying, we do not give up right away, we keep retrying for 30 more days, so one bad day does not retire a patch. Only after 30 days of failing do we mark it retired, meaning the base is too old, and stop trying until a new version is posted.

Once something actually gets committed, there is nothing left to test against. There are two ways this shows up. If the committer changed the patch before committing it, the old version no longer applies and Hackorum shows it as no longer matching. If the committer applied it exactly as submitted, the diff against the committed version on GitHub is empty, so we know it went in as-is. Either way, we stop running CI on that thread until a new patch shows up. Some threads get committed in stages, with fixups or follow up patches, so if a new patchset lands afterward, we pick CI back up and start testing it.

One more detail worth calling out is that Hackorum highlights patches that are already committed but still have an open commitfest entry, so those are easy to spot and clean up. That is currently a big issue and might really help to get this easier updated in the future. A future integration with the commitfest might be thinkable.

## Support for more mailing lists

<img src="/blog/2026/08/hackorum-update-mailinglist-badge.png" alt="Mailing list badges next to each thread, showing hackers, bugs and docs" style="display:block;margin:1rem auto;width:50%;border-radius:6px;">

Hackorum used to be pg-hackers only. It now also ingests pgsql-bugs, pgsql-docs, pgsql-general and pgsql-patches, with a badge next to each thread so you can see at a glance which list a message came from. We also tried pgsql-committers, it is imported up to around May/June, but we paused it for now. It is mostly terse commit notifications, and without a way to hide a list by default yet, it added more noise than value. We are planning to add more lists, so let us know if you are missing one.

## Saved searches

<img src="/blog/2026/08/hackorum-update-saved-searches.png" alt="Saved searches in the sidebar, grouped into global and personal searches" style="display:block;margin:1rem auto;width:30%;border-radius:6px;">

The advanced search from the last post is still there, but you no longer have to retype the same query every time. You can save a search, personally or shared with your team, and pin it to your sidebar. We also ship a few global saved searches out of the box.

## Ignore threads you do not care about

A small one, but a popular request was that you can now ignore a thread from the topic list with one click. Ignored threads disappear from your views and search results by default, and you can always list what you have ignored, or bring one back.

## Sending email from Hackorum

![Reply composer for sending a message to the mailing list from Hackorum](blog/2026/08/hackorum-update-reply-composer.png)

This was the top item on the "planned" list in February, and it is here now. You can reply to a thread directly from Hackorum, including reply all, with a Thunderbird style selective quote so you only quote the part you are actually replying to. There is a drafts sidebar so you can keep several replies in progress, and a "My emails" page that shows everything you have sent through the site.

This is currently limited to @gmail accounts and being under active testing. If you like early access, just reach out so we can activate it for your user.

## Everyday improvements

None of these are headline features on their own, but you will notice them:

* Long threads load in batches, so opening a huge discussion is noticeably faster
* A "jump to latest" button, and a setting to jump straight to your first unread message when you open a thread
* Read messages can collapse automatically if you prefer a shorter view
* Patch diffs now show inline line stats and highlighting
* Sessions now stay signed in for 30 days across devices
* The light/dark theme toggle is available everywhere, even before you sign in

## Mobile got a real pass

<img src="/blog/2026/08/hackorum-update-mobile-view.png" alt="Hackorum topic list on mobile" style="display:block;margin:1rem auto;width:60%;border-radius:6px;">

The mobile experience got a lot of attention: a proper burger menu, a quick shortcut to threads you starred, working swipe back and forward gestures, and layout fixes for tablets and foldables.

## What we are working on next

We are looking into AI generated summaries for longer threads, so you can get up to speed on a big discussion without reading every message.

## Try it and share feedback

If you want to take a look, just go to [https://hackorum.dev/](https://hackorum.dev/).

The repository, including a simple dev setup, is here: [https://github.com/hackorum-dev/hackorum](https://github.com/hackorum-dev/hackorum)

Want to chat with us, join the hackorum channel on the [PostgreSQL Hacking Discord](https://discordapp.com/channels/1258108670710124574/1471524461374083186).

Is this useful? What is missing? What would you change? Bug reports, feature requests, and contributions are all welcome: [https://github.com/hackorum-dev/hackorum/issues](https://github.com/hackorum-dev/hackorum/issues)

Thanks for taking a look, and we appreciate any feedback.
