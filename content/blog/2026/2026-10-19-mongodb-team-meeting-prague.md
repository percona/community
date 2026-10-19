---
title: "Three Days in Prague with the Percona MongoDB Team"
date: "2026-10-19T08:00:00+00:00"
tags: ["Percona", "MongoDB", "Community", "Open Source", "Team"]
categories: ['Community', 'MongoDB']
authors:
  - puneet_kala
images:
  - blog/2026/10/prague-team-meeting-group.jpg
---

Our MongoDB team at Percona works remotely, spread across many countries and time zones. Most days that works well, but once in a while it helps to be in the same room. In October we met in Prague for three days to plan next year, look at how we work, and spend some time together away from our laptops.

Here is a short look at what we did and what we learned.

![The Percona MongoDB team in Prague](blog/2026/10/prague-team-meeting-group.jpg)

## Who was there

Engineers, QA, documentation, product management and our Scrum Master, all working on [Percona Server for MongoDB](https://docs.percona.com/percona-server-for-mongodb/), [Percona Backup for MongoDB](https://docs.percona.com/percona-backup-mongodb/) and Percona ClusterSync for MongoDB. One teammate could not travel and joined part of the sessions over Zoom.

## Planning 2027 with customer and community feedback

We spent most of the first day on the roadmap. We started with the product vision, then went through feedback from customers and the community, and the requests we see most often in support. After that we ran a roadmap workshop with Now, Next and Later columns on the wall and moved cards around until we agreed where to focus for each product.

A good part of the feedback we reviewed was already in our plans. The rest went into the roadmap for the product it belongs to. If you use any of our MongoDB products and have a feature request or a pain point, the [Percona Community Forum](https://forums.percona.com) is a good place to tell us. That feedback ends up in exactly these discussions.

![Roadmap workshop with Now, Next and Later columns](blog/2026/10/prague-roadmap-workshop.jpg)

![Going through the roadmap cards](blog/2026/10/prague-roadmap-board.jpg)

We also looked back at the engineering goals we set for this year: which ones helped our users and the team, and which ones we should not continue. That review will shape our goals for next year.

## Using AI agents for documentation

With regular releases across several products, documentation can easily become the slowest step. Rasika from our documentation team showed the agents she built to help with this:

- **Release notes agent:** takes the exact versions, the Jira release report and the product template, and opens a pull request with draft release notes.
- **Feature agent:** takes a Jira ticket or other source and drafts the feature docs, references and navigation updates in a pull request.

The agents draft and check. The writer still resolves gaps with engineering, reviews the diff, approves and publishes. We agreed to make this part of our normal workflow and to keep docs changes for a release in a release branch, so they are ready when the release goes out.

![Rasika presenting documentation pull requests with project agents](blog/2026/10/prague-docs-agents.jpg)

## Getting releases out faster

We release Percona Server for MongoDB every month, and a common question from users is how quickly we follow upstream MongoDB releases. We spent an afternoon going through every step of a release, from building and testing to documentation, to see where the time goes.

The main ideas were more build and test capacity so more jobs can run in parallel, and more automation to pick up new upstream tags as soon as they are published. We also talked about balance. Faster releases are good for users, but not at the cost of burning out the team.

## Performance testing

Our QA team walked us through how we run performance tests today and what we focus on. One thing we want to add is regular performance regression checks for Percona ClusterSync for MongoDB builds, so we catch slowdowns before a release, not after.

## Retro and a quick safety check

Our Scrum Master ran a retro using Start, Stop, Continue. Before that we did a safety check: everyone put a sticky note on a scale from 1 ("I won't say anything meaningful, I'll smile and agree") to 5 ("I'll talk about anything"). Most of the team voted 4. It takes five minutes and tells you a lot about how open the following discussion will be, so it is worth trying with your own team.

One theme that came up clearly: there are still small, repetitive tasks in our daily work where we could use AI more.

![Start, Stop, Continue retro board](blog/2026/10/prague-retro-board.jpg)

![Safety check before the retro](blog/2026/10/prague-safety-check.jpg)

## Prison Island and Prague evenings

On the second day we left the meeting room for Prison Island Praha, a set of small challenge rooms you solve in teams. Some rooms need logic, some need speed, and most need a bit of both. It was a good way to see how people work together when the problem is not a database.

The evenings were for good food and Czech beer, at Vinohradský Parlament on the first night and Cà Phê Cổ on the second. Thanks to Jakub for organizing all of it.

![The team at Prison Island Praha](blog/2026/10/prague-prison-island-team.jpg)

![Lining up at Prison Island](blog/2026/10/prague-prison-island-lineup.jpg)

![Team dinner in Prague](blog/2026/10/prague-team-dinner.jpg)

![An evening out in Prague](blog/2026/10/prague-evening-out.jpg)

## Wrapping up

Three days was not enough for every topic on our list, and the rest will go into our regular team calls. But meeting in person makes the remote work that follows easier. We know each other better, and we left with a clear picture of what we want to build next.

If you run MongoDB with Percona Server for MongoDB, Percona Backup for MongoDB or Percona ClusterSync for MongoDB, we would like to hear from you. Share your feedback, questions and ideas on the [Percona Community Forum](https://forums.percona.com).
