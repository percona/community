---
title: "Why PostgreSQL needs an AI usage policy"
date: "2026-06-26T10:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'ai']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2026/06/Jan-cover-ai.png
---

We often hear that open source is about people.

People who contribute their time and, in a way, parts of their lives to work on software that is available for everyone without limitations and without licensing costs.

The more popular a project becomes, the more often we also hear about the need for sustainable open source. Nothing surprising here. Often projects start off as "scratching ones itch" and it's very appreciated when others notice the work done. The more time passes and the more the work becomes appreciated, the higher the chances that there will be a need to spend more time on the project.

When projects graduate from a hobby project to software used by thousands of users, or even a foundational building block in production, things get interesting.

At that point, we may hope to see new contributors joining the project. This would normally be a good thing. But is it still the same in the AI hype era, where anyone can generate almost any content and claim it as their own?

AI was supposed to be a killer of open source. After all, a lot of publicly available code from open source communities was part of what AI systems trained on. The fear was that as it would become so easy to create our own software, there would not be as much need for the existing open source projects. While this was the hype speaking, we can notice another trend. It became much easier to propose patches, detect and report security threats, or submit code reviews. Even without any developer experience or coding capabilities.

### How sustainable is that for the human maintainers?

It is easy to imagine that there is a very fine line between positively helpful and overwhelming. As with anything unwanted, AI-generated code or text can be harmful to many open source projects. Especially those with a single maintainer treating their project as a spare time hobby and suddenly experiencing a waterfall of [AI-slop](https://en.wikipedia.org/wiki/AI_slop).

![RPCS3 plead to vibe coders social media post](blog/2026/06/Jan-ps3.png)

 [Playstation 3 emulator project](https://github.com/RPCS3/rpcs3) recently [RPCS3 posted a plea](https://x.com/rpcs3/status/2053248922974605431?lang=en) to the vibe coders to stop the AI-generated abuse already and they are not alone in this problem.

![FOSDEM 2026 Daniel Stenberg presentation](blog/2026/06/Jan-fosdem-curl.png)

Daniel Stenberg from the [curl project](https://curl.se/) captured this well in [his FOSDEM 2026 talk](https://fosdem.org/2026/schedule/event/B7YKQ7-oss-in-spite-of-ai/) summarizing that: “AI gives us the worst and the best, simultaneously.”

In the same talk, he discussed how curl had to stop its bug bounty program. Curl has also posted on the [rules of AI use](https://curl.se/dev/contribute.html#on-ai-use-in-curl). Even that was not enough, which led to the “[curl summer of bliss](https://daniel.haxx.se/blog/2026/06/15/curl-summer-of-bliss/)”, where they will:

> 
> not accept or otherwise handle any vulnerability reports during the month of July 2026.
> 

Security reports are an especially sensitive case. An AI-generated vulnerability report is not harmless. Someone has to read it, reproduce it, evaluate it and decide whether it is real. Even when the issue is not there, the work is still very real. Like it or not but when it’s unfounded work that proves a ai-generated false it is abusive.

Knowing that some projects adopt AI-focused policies, I searched for examples of such policies, using AI obviously 🙂, and stumbled upon [a very useful (open source!) list that already gathers this kind of information](https://github.com/melissawm/open-source-ai-contribution-policies).

Further analysis of the resources linked in the list, as of June 2026, shows that most policies allow assisted use, but not “AI as the contributor.”

Commonly allowed uses include:

- drafting code,
- generating tests,
- improving docs,
- debugging,
- summarizing, or asking an LLM for help.

All of that is usually acceptable as long as the human reviews and owns the result.

Typically banned practices include:

- fully AI-generated PRs with little human engagement
- AI-generated “good first issue” work
- AI as co-author
- automated AI code reviews
- unreviewed agentic output

It is completely understandable that experienced developers and communities say “no” to submissions of low quality. That would not be sustainable. Maintainers already carry a lot of invisible work, and AI can easily multiply that work if contributors treat it as a shortcut instead of a tool.

What is very positive for the future of AI-enhanced work is that the general direction seems to be acceptance, as long as there is a human-in-the-loop.

AI-enhanced work, as long as a human was involved, is possible across a range of open source products: [Apache Airflow](https://github.com/apache/airflow/blob/main/contributing-docs/05_pull_requests.rst#gen-ai-assisted-contributions), [Apache DataFusion](https://datafusion.apache.org/contributor-guide/index.html#ai-assisted-contributions), [Arrow](https://arrow.apache.org/docs/dev/developers/overview.html#ai-generated-code), [CloudNativePG (CNPG)](https://github.com/cloudnative-pg/governance/blob/main/AI_POLICY.md), [CPython](https://devguide.python.org/getting-started/ai-tools/index.html), [Django](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/#ai-assisted-contributions), [Firefox](https://firefox-source-docs.mozilla.org/contributing/ai-coding.html), [Flutter](https://github.com/flutter/flutter/blob/master/docs/contributing/Tree-hygiene.md#ai-contribution-guidelines), [Ghostty](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md), [Gitea](https://github.com/go-gitea/gitea/blob/main/CONTRIBUTING.md#ai-contribution-policy), [Homebrew](https://github.com/Homebrew/brew/blob/main/CONTRIBUTING.md#artificial-intelligencelarge-language-model-aillm-usage), [Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/#ai-guidance), [Linux Kernel](https://kernel.org/doc/html/next/process/coding-assistants.html), [LLVM](https://llvm.org/docs//AIToolPolicy.html), [Matplotlib](https://matplotlib.org/devdocs/devel/contribute.html#generative-ai), [NumPy](https://numpy.org/devdocs/dev/ai_policy.html), [Pandas](https://pandas.pydata.org/docs/dev/development/contributing.html#automated-contributions-policy), [PyTorch](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md#ai-assisted-development), [SciPy](https://scipy.github.io/devdocs/dev/conduct/ai_policy.html), [SymPy](https://docs.sympy.org/dev/contributing/ai-generated-code-policy.html), [Wagtail](https://docs.wagtail.org/en/latest/contributing/general_guidelines.html#general-coding-guidelines), [Zulip](https://github.com/zulip/zulip/blob/main/CONTRIBUTING.md#ai-use-policy-and-guidelines), and [others](https://github.com/zulip/zulip/blob/main/CONTRIBUTING.md#ai-use-policy-and-guidelines).

What is interesting is that, at this moment, PostgreSQL does not have any official policy of this sort available.

### Slonik says "I haven't noticed..."

While this may be a problem that does not directly touch PostgreSQL as a database server, it already has an impact on the PostgreSQL ecosystem, which consists of many other extensions and tools.

The reason may be quite trivial. Even with AI, the entry threshold for PostgreSQL core hacking is still higher than for many other tools. Hackers communicate through mailing lists, and even with the adoption of modern tools like Hackorum.dev, it is still not that easy to work with PostgreSQL compared with many other, more tempting projects.

![Beware of elephants drowning in AI slop](blog/2026/06/Jan-waterfall.png)

The issue, as I often see it for PostgreSQL, is that there is not much leadership for the wider ecosystem from the core project. Availability of responsible AI usage policies for the ecosystem could make maintainers’ lives easier. And let’s be honest, for many smaller projects, creating such policies from scratch is a burden they could be spared.

Seems like any help would be appreciated.

### What now? Is this over? Was this a rant?

I like to say, and repeat myself, that “AI usage in open source is all about respect.” To me, this is enough to say all that is needed. People need to communicate. This was meant as a start of the discussion.

[PGConf.EU](https://2026.pgconf.eu/) is coming in October, as well as many smaller meetups this year. There will be lots of space for hallway track discussions and hopefully some outcomes. Not to mention async communication channels. What I hope is that we can leverage all these channels to propose some solutions, experiment, and get better.

Let this be a call to action to help us all be more reasonable and more respectful of other people’s time.

With this in mind, 

<details>

<summary>check out my original text before I refined it with AI if you want to see how it changed.</summary>

Often we hear how open source is the people. The people who contribute their time, in a way their lives, to produce software available for everyone without limitations. Without licensing cost on the users.

The more a project becomes popular the higher chances we also hear about the need for sustainable open source from it. Nothing surprising here. At first we want others to notice the work we’ve done. The more times pass and the work becomes appreciated, the higher chances that there will be a need to spend more time on the project. 

When it graduates from a hobby project to software used by thousands of users or even a production founding block things become really interesting. Now we may hope to see new contributors joining the project. This would normally be a good thing but is it the same in the AI hype era where anyone can generate any content and claim it their own?

AI was supposed to be open source killer because it will become so easy to create our own software and not use open source. While this was the hype speaking, we notice another trend. It became way easier to propose patches, detect and report security threats or submit code reviews. Even without any developer experience or any coding capabilities. 

#### How sustainable for the human maintainers is that? 

It’s easy to imagine that there is a very fine line between positively helpful and overwhelming. As with anything unwanted, the AI generated unwanted code or texts can be harmful to the many ope source projects. Especially those with a single maintainer treating their project as a spare time hobby and experiencing a waterfall of [AI-slop](https://en.wikipedia.org/wiki/AI_slop).

![RPCS3 plead to vibe coders social media post](blog/2026/06/Jan-ps3.png)

Playstation 3 emulator RPCS3 posted a plead to the vibe coders to stop the AI-generated abuse already and they are not alone in this problem.

![FOSDEM 2026 Daniel Stenberg presentation](blog/2026/06/Jan-fosdem-curl.png)

As Daniel Stenberg from curl says (check out his talk during FOSDEM 2026) “AI gives us the worst and the best - simultaneously”

Seeing that [curl](https://curl.se/) had to stop their bug bounty program (as discussed in the talk above) and even this was not enough and ended up in the “[curl summer of bliss](https://daniel.haxx.se/blog/2026/06/15/curl-summer-of-bliss/)” where they will:

> 
> not accept or otherwise handle any vulnerability reports during the month of July 2026.
> 

Security reports are an especially sensitive case. A wrong AI-generated vulnerability report is not harmless. Someone has to read it, reproduce it, evaluate it and decide whether it is real. Even when the issue is not there, the work is still very real. Like it or not but when it’s unfounded work that proves a ai-generated false it is abusive.

Knowing that some projects adopt policies, I searched (using AI obviously 🙂) for examples of such policies and stumbled upon [a very useful list that gathers such information already](https://github.com/melissawm/open-source-ai-contribution-policies). 

Further analysis of the resources linked in the list (state in June 2026) shows that:

- Most policies allow assisted use, not “AI as the contributor.”
- Commonly allowed uses include drafting code, generating tests, improving docs, debugging, summarizing, or asking an LLM for help, as long as the human reviews and owns the result.
- Typically banned practices include:
    - Fully AI-generated PRs with little human engagement
    - AI-generated “good first issue” work
    - AI as co-author
    - Automated AI code reviews
    - Unreviewed agentic output

It’s only understandable that experienced developers and Communities say “no” to low quality submissions. That would not be sustainable. What is very positive for the future of AI enhanced work is that the repo shows general acceptance as long as there is a “human in the loop”. AI enhanced work as long as human was involved is possible across a range of open source products: [Apache Airflow](https://github.com/apache/airflow/blob/main/contributing-docs/05_pull_requests.rst#gen-ai-assisted-contributions), [Apache DataFusion](https://datafusion.apache.org/contributor-guide/index.html#ai-assisted-contributions), [Arrow](https://arrow.apache.org/docs/dev/developers/overview.html#ai-generated-code), [CloudNativePG (CNPG)](https://github.com/cloudnative-pg/governance/blob/main/AI_POLICY.md), [CPython](https://devguide.python.org/getting-started/ai-tools/index.html), [Django](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/#ai-assisted-contributions), [Firefox](https://firefox-source-docs.mozilla.org/contributing/ai-coding.html), [Flutter](https://github.com/flutter/flutter/blob/master/docs/contributing/Tree-hygiene.md#ai-contribution-guidelines), [Ghostty](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md), [Gitea](https://github.com/go-gitea/gitea/blob/main/CONTRIBUTING.md#ai-contribution-policy), [Homebrew](https://github.com/Homebrew/brew/blob/main/CONTRIBUTING.md#artificial-intelligencelarge-language-model-aillm-usage), [Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/#ai-guidance), [Linux Kernel](https://kernel.org/doc/html/next/process/coding-assistants.html), [LLVM](https://llvm.org/docs//AIToolPolicy.html), [Matplotlib](https://matplotlib.org/devdocs/devel/contribute.html#generative-ai), [NumPy](https://numpy.org/devdocs/dev/ai_policy.html), [Pandas](https://pandas.pydata.org/docs/dev/development/contributing.html#automated-contributions-policy), [PyTorch](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md#ai-assisted-development), [SciPy](https://scipy.github.io/devdocs/dev/conduct/ai_policy.html), [SymPy](https://docs.sympy.org/dev/contributing/ai-generated-code-policy.html), [Wagtail](https://docs.wagtail.org/en/latest/contributing/general_guidelines.html#general-coding-guidelines), [Zulip](https://github.com/zulip/zulip/blob/main/CONTRIBUTING.md#ai-use-policy-and-guidelines), and [others](https://github.com/zulip/zulip/blob/main/CONTRIBUTING.md#ai-use-policy-and-guidelines).

### Slonik says "I haven't noticed..."

![Beware of elephants drowning in AI slop](blog/2026/06/Jan-waterfall.png)

What is interesting that at this moment PostgreSQL does not have any official policy of this sort available. While this may be a problem that does not touch PostgreSQL as a database server it already has an impact on the PostgreSQL ecosystem consisting of many other extensions and tools. The reason may be quite trivial - even with AI the entry threshold for PostgreSQL core hacking is still higher than any other tool. Hackers communicate via mailing lists and even with adoption of modern tools like Hackorum.dev it’s still not that easy to work with PostgreSQL comparing to a lot of other more tempting tools.

The issue as I often see it for PostgreSQL is that there is not much leadership for the ecosystem from the core. Availability of responsible AI usage policies for the Ecosystem could make the life of maintainers easier and let’s be honest, for a lot of smaller projects that’s a burden they could be spared. Seems like any help would be appreciated.

#### What now? Is this over? Was this a rant?

I like to say, and repeat myself that “AI usage in open source is all about the respect”. To me this is enough to say all that’s needed. People need to communicate. This was meant as a start of the discussion. 

PGConf.EU is coming in October, as well as many smaller meetups this year. Lots of space for hallway track discussion and hopefully some outcomes. Not to mention async communication channels. What I hope is we can leverage all these channels to propose some solutions, experiment and get better. 

Let it be a call to action to help us all be more reasonable and respectful to others time.

With this in mind check out my original text I refined with AI if you want to see how it changed. Because of course I polished it to some extent to ensure that the grammar and phrasing is cleaner and crispier 🙂


</details>

Because of course I polished it a little to make sure the grammar and phrasing are cleaner and crispier 🙂

