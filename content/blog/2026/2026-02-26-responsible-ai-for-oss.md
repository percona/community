---
title: "A reponsible role for AI in Open Source projects?"
date: "2026-02-26T14:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_alastair', 'Community', 'AI']
categories: ['PostgreSQL', 'AI']
images:
  - blog/2026/02/OutOfCycleRelease_GeminiNanoBananaProImage.png
authors:
  - alastair_turner
slug: responsible-ai-for-oss
---
AI-driven pressure on open source maintainers, reviewers and, even, contributors, has been very much in the news lately. Nobody needs another set of edited highlights on the theme from me. For a Postgres-specific view, and insight on how low quality AI outputs affect contributors, Tomas Vondra published a great post on his blog recently [https://vondra.me/posts/the-ai-inversion/], which referenced an interesting talk by Robert Haas [https://www.pgevents.ca/events/pgconfdev2025/schedule/session/254-committer-review-an-exercise-in-paranoia/] at PGConf.dev in Montreal last year. I won’t rehash the content here, they’re both quite quick reads and well worth the time.

The key points which got me thinking about the rest of this piece are:
 - Low quality AI reviews are also a time sink, not just AI slop patches
 - AI is best at code review, so that happens soonest, but conceptual review should happen first

Today also marks the release of an out-of-cycle of Postgres. The release is happening because a number of security fixes which were introduced in the releases two weeks ago were found to cause functional and performance regressions. On the upside, this shows that the longer, public patch review process does find issues which otherwise go unnoticed. On the whole, fewer out-of-cycle releases, with the friction they create for the maintainers and users would, however, be better.

The link between these two tracks of thought is review. Reviewing the security patches included in any Postgres release cycle is clearly different. What if it’s different in a way which suited AI assistance?

We know that AI coding agents can contribute to this process, because one just has. Unfortunately, a little bit late. Some of the issues fixed in today’s out-of-cycle release were identified when a contributor opened up his agentic AI coding assistant one morning and asked it to tell him about the new patches. Some of those patches were newly visible to most contributors, after being pushed to the Git source control system for Postgres, because they were security patches which had not been discussed on the public mailing lists. You may hear the issues which drove these fixes referred to by the initialism for the Common Vulnerabilities and Exposures program which records these security reports (CVEs). 

It should go without saying that this is not just a case of: download Claude Code or Gemini Code Assist, install, add value and attain glory. There is definitely work involved in getting value out of these tools:
Setting up a project specific context is important, particularly for a long standing project like Postgres, which has some long standing coding styles
Asking the right question, known in the AI-assisted paradigm as prompting, will also require quite some understanding of the problem domain
Human judgement on the quality of the output. At its most basic, this is a decision about whether to turn the coding assistant’s output into a review, bin the output, or investigate further.

The first two of those, the purely technical ones, are very unlikely to happen on the first attempt to use agentic AI as a coding assistant. This is a new class of tool everyone needs to learn. Perversely, people who have more of that third quality, that judgement, are more likely to walk away from their early experiments because those experiments are not delivering value. People skipping the third area of work is how we have ended up with AI being regarded as a burden on open source projects. This isn’t new, long before we got Large Language Models involved in code analysis, there were deterministic static analysis tools, and their false positives have been heaping noise on the signal in patch review processes for years.

In his presentation which I linked above, Robert lists four key, high level principles for patch review:
 - Start With The Big Picture
 - Consistency Is Critical
 - Be a Pessimist
 - Apply a Spirit of Maintainership

The middle two of those principles, consistency and pessimism, are the two most amenable to AI interventions, and the two most important for reviewing security patches.

When a piece of code has been committed, the big picture decisions and the decisions in the spirit of maintainership have already been made. If the code is later found to expose Postgres users to security issues, reviewing the solution comes down to all the possible angles of pessimism about the new code’s possible impact. It is in this area where Claude Code not just identified a regression in the case above, but also created a small reproducer to trigger the regression.

Crafting and reviewing security patches is a beast of a task. The leading experts on all matters Postgres are writing and reviewing these patches, but the group is small, because any information about potential exploits needs to be kept under tight control. Timelines for a fix might also be quite tight. Both factors limit opportunities for collaboration and multi-stage review. In these conditions, an extra pair of AI eyes (A-Eyes?) on the patches may just be very useful.

Set up, prompted, and reviewed by those who really know the problem domain, AI coding agents could provide valuable pointers on issues and regressions to consider when reviewing security patches. In that small bubble, this would not be a source of empty workload, but a source of extra review without having to coordinate more people in a small  team. AI assistance will probably not provide time savings or quality gains on the first security patch it’s used to review, maybe not even on the seventh. After some setup effort, and a human learning a bit about improving its setup, an Agentic AI assistant (or two, with different configuration on different providers) may well be able to avoid another out-of-cycle release. That would be a major win. 
