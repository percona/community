---
title: "Reviewing large projects with AI: contributing in a meaningful way"
date: "2026-07-25T00:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'AI']
categories: ['PostgreSQL']
authors:
  - zsolt_parragi
images:
  - blog/2026/07/ai-review.png
---

When you read about how LLMs help developers start on a project, it's usually about how quickly they can create their first meaningful PRs.
But is it really them creating those patches?

This happens in the corporate world, where managers and owners write AI-praising posts on LinkedIn about how coding agents made their junior developers so much more productive and onboarding so much smoother.

It also happens with opensource projects, where we can see that drive-by contributors storm projects with AI created PRs.
Maintainers often also rely on AI, so we can observe conversations where humans are just copy-pasting, essentially reducing themselves to carrier pigeons.
Maybe it's time for an update to [RFC 1149](https://datatracker.ietf.org/doc/html/rfc1149)?

![RFC 1149.42: AI over Human Carriers](blog/2026/07/rfc1149-42.png)

In this blog post, I'd like to showcase an AI-assisted review infrastructure that runs completely on a subscription-based Claude Code workflow, [autoreviewer](https://github.com/dutow/autoreviewer).
I originally created it to help me get started on the PostgreSQL hackers list, the main mailing list overseeing PostgreSQL development.
Since then, I made it more generic and we are using it for most of our PostgreSQL-related projects.

I'll approach it from far away, with a long detour:
explaining why you should start your AI-adventure on large projects with understanding and reviewing instead of making changes.
And if you'll take my advice, maintainers will love your contributions, and you can become a better software engineer instead of drowning in the AI noise.

As the saying goes, we can do it fast or cheap or good -- you can choose two.
The issue in the above examples is that people tend to choose fast and cheap:
the minimal effort, most comfortable combination, and that results in a local maximum, not global.

## Don't outsource your brain!

Let's say you are onboarding to a new large project.
It doesn't matter if you just started a new job, or you want to start contributing to a large project like PostgreSQL, the pain is the same:
you don't even know where to start, everything seems overwhelming.

But let's try to resist the clear fast path of simply asking AI to generate something (PR/patch, review comments, feature suggestions) and copy-pasting it upstream.
While that might result in a short excitement burst that you contributed something, it is unlikely to result in anything actually useful.

AI is here, it is part of our everyday life, and it is improving quickly, ignoring it wouldn't be useful.
We have to adapt our workflow to become better programmers.
The only question is, how do we properly integrate it?

I don't doubt that AI will be smarter than us one day in every aspect.
We are not there yet, but this also doesn't mean that it is inferior to human engineers in everything.
We are at the point in time where humans still have the advantage in some tasks, while AI is already winning in others.

Can we come up with an "onboarding" strategy where we rely on the strength of AI, while still remaining the engineers in control?

![Many opinions about today's AI were formed based on yesterday's models](blog/2026/07/ai-woodcutter.png)

## What can AI do for us?

It can navigate a large codebase and build an overview of the parts that matter:
spot differences, misuses of an API, notice patterns, summarize what the software does.
It still makes mistakes sometimes, but it's getting less and less likely with the newer models, in this area it is most likely better than us.

People still often say that AI is bad at planning and designing an overall architecture, but I think that's also wrong:
it is quite good both at understanding the architecture of existing codebases and suggesting improvements or different approaches, or designing new things from scratch.
Yes, it's still a hit-and-miss, but isn't it the same for humans, when we start new research prototypes?
We just have to keep this in mind, think about the ideas we get, ask challenging questions, instead of blindly saying OK to the first one.

It also has vastly better generic knowledge than most of us:
writing or understanding software often requires domain knowledge about some other field we lack and would normally require weeks of research before we can start.
AI can answer our questions about the subject immediately, and start suggesting approaches.
That's all good -- if instead of asking it to prototype something for us that we don't even look at, we actually spend some time to also learn something.

## What about reviewing with AI?

Normally, when you join a new large project you don't start by submitting huge pull requests making changes to multiple distinct parts of the code because you lack the understanding to do so.
Now you can, but should you do so?

Without AI, the traditional process is that you either start submitting small low-hanging "Good first issue" PRs, or instead start by reviewing changes, reading the documentation, understanding the code (or both at the same time).
In the second case, you often don't even write a single line of code for weeks.

When I decided to join the PostgreSQL community, I knew that there is mainly a shortage of reviewers, not a lack of patch contributors.
I wanted to help out there instead of making the issue even worse by submitting more and more patches.

But I also had a problem:
the project is huge, even after working on extensions for it for a few years, I knew little about it.
I was also aware that other people tried to submit AI-reviews already and generally that wasn't welcome there.
Not that I would have wanted to do so anyway, downloading a patch and pointing an AI at it with "Review it!", and then copy-pasting the result doesn't feel like productive work to me.

I wanted to learn, but I also wanted to leverage the modern tools we have.
So how can we have the best of both?

Since the codebase is huge, I decided to study it by patches:
I selected a few interesting looking threads, downloaded the patches, looked at them a bit, and tried to figure out how to proceed.

I quickly ended up with a simple workflow:

1. Asking an LLM to summarize the patch itself, how it fits into the overall project, what it changes.
   This is useful especially for large patches, and gives an interesting comparison point immediately:
   what the patch author advertises in the thread, and what the agent thinks about it.
2. Asking it to look at the "big idea", the design, the overall architecture -- does it follow the postgres way, are there similar examples in the codebase, what different ways would it try to approach the same goal, would any of those be a better fit?
   This immediately gives so much context to explore, suddenly I didn't only have to review the patch, I also had to explore what those suggestions are, how those could work?
3. Asking it to review the actual code, and find issues with it.
   Crashes, security problems, small bugs, typos, nitpicks, everything, including a classification about the seriousness of the issue.
4. And then requiring another verification step for all findings:
   what from the above list is actually exploitable?
   If it is supposed to be a user facing issue, can it create a testcase for it using the test frameworks available in PostgreSQL?
   If it can cause problems for extensions, can it showcase the problem with a mini dummy extension?
   If it can't do any of the above, is the issue even real, do we really have to consider it, what's its reasoning about it?
5. After all this already happened, I asked it to read the actual conversation, and verify what's already reported and under discussion, what's new, and if there's anything else it wants to try now based on the discussion, let's do another iteration.
6. And finally, a summary, an overview from the interesting points of all above, so that I can quickly decide what to expect:
   is this already a ready-to-commit patch I should only read to see what a good patch looks like, or I am reviewing something completely broken?

This is of course highly automateable, and that is where my [autoreviewer](https://github.com/dutow/autoreviewer) comes in:
the point of AI and vibe-coding is that we automate boring tasks so we can focus on the important ones.
Repeating the above process manually each time would be as bad as reducing myself to a carrier pigeon, so of course after realizing the pattern I asked my ~~best friend~~ Claude to prototype it for me, and then I kept improving it for half a year, before sharing it now.

The situation is similar to when I shared my [ai-workflow related dotfiles](https://percona.community/blog/2026/05/05/how-i-stopped-babysitting-my-coding-agent-with-dotfiles/) previously:
this is my personal project, take it with a grain of salt, adapt it to your needs, use as inspiration.
Compared to the dotfiles repo, this is actually usable as-is for others, but far from perfect.

## Subscription-automation approach

Let's talk a bit about the architecture of the automation, as it can be interesting, and possibly useful for other projects too.

I designed it with the following design constraints initially, and these still hold:

1. I want it to run on a normal, fixed price subscription, not token based usage.
   As I already have subscriptions, and I'm not using them all the time to their limits, this is basically free.
2. Since I have a good desktop PC, I want things to run in parallel:
   if I enqueue two postgres patch reviews at the same time, I would prefer them completing sooner in parallel than later in sequence.
3. All this parallelization has to be easily user visible, for example I want to be able to see and access the claude sessions.
4. AI only reviews, most of the automation steps above happen in a fixed script.
   This both reduces token usage and makes things more predictable.
   Of course, the reviewer can still decide that it needs a different build and execute it, but it starts with a good generic baseline already available.
5. Because it's an automated AI workflow, it has to run in a completely sandboxed container, separated from everything else.

This is all nice, but is 1 actually possible?
Back when I started it, programmatic use of `claude` was still allowed with subscription pricing, but there were already talks about it being restricted to token based usage for 3rd party tools.

Do we have to go there to accomplish our goal?
Can't we simply ask claude to create a specific empty file on completion, and then `kill` the process when we detect it? Or add a stop hook that accomplishes the same in an even more reliable way?

The entire workflow runs with `tmux`, starting a new pane for each new `claude` session.
If something gets stuck a bit because of an LLM decision, or because I hit the session limit and it needs a manual nudge to continue, that's fine.
It runs in one of my terminal windows, and I can take a quick look at it once a day.
If one session gets stuck, nothing gets lost, and all other tasks will continue without issues.

This could be improved further, as there are ways to auto-restart after a session limit hit.
But so far it wasn't a big enough issue for me to actually do anything.

## Practical use

As I said in the beginning, at this point we are using this tool in most of our PostgreSQL-related projects, and that evolved into two different patterns:

For our github repos, with less traffic, it automatically watches the open pull requests:
if anything gets updated, it automatically downloads it, builds it, runs tests locally, checks CI status, conversations, everything it can access.
After this initial preparation is completed, it reviews the changes and writes the results in markdown files.
The review process is also aware of its previous reviews/findings, so it can track that properly, e.g. verify what was fixed, what's a new regression, and so on.

In this setup, I don't have to do anything except look at the results when I review PRs -- unless I look at something a few minutes after it was opened/updated, the AI analysis is automatically there.

Note that **it writes markdown files**. Those files and reproduction scripts are automatically published on a separate simple HTML site generated from the review report, but it intentionally does not automatically post anything.

![Autoreviewer screenshot](blog/2026/07/pg-autoreviewer.png)

I am following the same principle many others adopted:
it doesn't matter if a contribution is self-written or AI generated, you own it.
The AI doesn't post reviews to a PR, I do.

If I automate myself out of this process, then:

1. I won't learn anything from it.
2. It becomes too easy for me to completely ignore the PR myself.
   By looking at the AI review, I am also forced to look at the PR itself myself.
3. I possibly spam my colleagues with slop, even if at this point my autoreviewer rarely makes bad change requests.

For high throughput projects, such as the PostgreSQL mailing list, I don't want to review everything:
that takes CPU time (build and test execution on my PC), I would also quickly hit my session limits, and even if I would process everything, I do not have the time to personally look through all that.

Instead I am still actively looking at the hackers list on [hackorum.dev](https://hackorum.dev):
see what new threads get posted, which threads I am actively reviewing get updated, and so on.
When something interesting receives a new patch version, I manually type a simple command to queue it using the hackorum thread id, but that's all I have to specify.
After that, the automation automatically downloads the patch and the entire mailing list conversation, applies the patch, builds, tests, and of course reviews.

Actually publishing the review is similar to the github workflow:
I decide what and how to mention in an email, not the LLM.

## Verify, don't trust!

The LLM is already required to verify findings with written-down scripts, but how do we ensure that it didn't hallucinate both the finding and the repro script?
It's simple, we have to execute the verification manually.

I can't emphasize this enough, don't forget, we are part of the process too, we have to learn and adapt too.

And the more difficult that is to do, the more likely it becomes that we'll blindly accept it instead of properly checking the issue ourselves, so we have to make it easy!

I strongly rely on [go-task](https://github.com/go-task/task) in my projects, and that includes the autoreviewer.
Many of these automations are project specific, so staying with the postgres example, I have a task that starts/stops/restarts/etc a server with a specific patch, or gives me a psql or bash console.
Since I have all the builds and verification scripts already part of the review infrastructure, these tasks are part of this too.

I kept a somewhat simplified but still fully functional example postgres review infrastructure in the autoreviewer repo.

## Disclaimer on LLM automation and security

Running LLMs unsupervised has its own dangers, I wrote more about this [previously](https://percona.community/blog/2026/05/05/how-i-stopped-babysitting-my-coding-agent-with-dotfiles/).
Autoreviewer runs claude code with `--dangerously-skip-permissions` in a docker/podman sandbox.
As long as the separation holds, it shouldn't have access to anything outside the review directory on your PC, but it does have full network access, and it holds a github token and possibly a deploy key, so keep that in mind, and keep those as restrictive as possible.

What to do with that problem, and how, I leave as an open question to everyone.
Personally, I am simply using a MITM proxy to log the requests it sends, but you might want to add more restrictions to it.

## Closing thoughts

LLM based reviews are a complex, controversial topic:
on one hand I am strongly against the mindless communication happening everywhere on the internet, on the other hand I have to agree that we have some awesome review and teaching tools, we just have to put the effort into learning and using them properly.

As with everything else, nothing is free:
you can't expect an AI agent to make your life magically better.
Easier, for sure, but that's not the same.

If you are interested in using it for reviewing and learning in a meaningful way, please check out the [autoreviewer](https://github.com/dutow/autoreviewer) repository, and share your thoughts!

I have been personally using this project for more than half a year now, and it has been an awesome help to me:
learning is much easier while actively doing something, and with this help, I was able to orient myself and actually do something productive instead of just annoying the postgresql community.

If you check out [my activity](https://hackorum.dev/person/zsolt.parragi@percona.com) on the PostgreSQL mailing lists, most of my reviews were done with the help of the infrastructure described in this blog post.

Are you doing something even marginally similar?
Then share it in some way, let's advertise the smart use of AI!

![Shooting with human carriers](blog/2026/07/human-carriers.png)