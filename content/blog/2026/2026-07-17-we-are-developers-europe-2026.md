---
title: "Perconians at WeAreDevelopers World Congress 2026: Agents Everywhere, Security Wake-Up Calls, and Buzzword Bingo"
date: "2026-07-17T11:00:00+00:00"
tags: ['Events', 'Community', 'Open Source', 'AI', 'Community Ascent', 'Security']
categories: ['Community']
authors:
  - radoslaw_szulgo
  - sandra_romanchenko
images:
  - blog/2026/07/wearedevelopers.jpeg
slug: wearedevelopers-2026
---

On July 9–10, the two of us — **Sandra** (Engineering, Percona for MongoDB) and **Radek** (Product, Percona for MongoDB) — packed our backpacks and headed to Berlin for the [WeAreDevelopers World Congress Europe 2026](https://www.wearedevelopers.com/world-congress) (WAD). The 11th edition of the congress gathered **15,000 developers and 500+ speakers** for two intense days, and we came back with full notebooks, fresh ideas, and one very clear message from the industry.

At Percona, we genuinely love getting out of our daily routine to learn what's new. Stepping away from the roadmap for two days is a fantastic reset: you zoom out, see where the whole industry is heading, and build what Sandra calls a *mental index* — concepts that might not solve today's ticket, but will absolutely pay off six months from now. This post is our attempt to share that index with you, with links so you can dig deeper into whatever catches your eye.

Spoiler: if you played buzzword bingo with "agentic AI," you'd have won in the first hour. 

## The one big theme: Agentic AI (surprise!)

Every conference right now has an AI theme, but WAD went deep: adoption stories, best practices, building and optimizing RAG pipelines, and — importantly — what happens to security when agents write and ship code.

Our personal top takeaways:

- **Security matters more than ever in the age of AI.** More on that below — this one deserves its own section.
- **Agents are only as good as their context.** Intent, mission, purpose, style, goals, success metrics — the teams winning with AI are the ones writing this down for their agents.
- **Understand *why* you do what you do.** Agents won't think about that for us. The engineering judgment moves up the stack; it doesn't disappear.

## "The SDLC is dead" — the Agentic Assembly Line keynote

Thomas Dohmke (CEO of Entire, previously CEO of GitHub) opened with a demo-filled keynote about where developers and agents are headed. A few numbers that made the whole room sit up:

- Teams using coding agents ship **5× more code** (measured by PRs), and PRs are **3× bigger** than 18 months ago.
- **20%+ of AI-generated changes are accepted without human review.** (Brave? Terrifying? Discuss.)
- Some products — Codex, notably — are now written *only* by AI.

![GitHub Stats](/assets/blog/2026/07/githubstats.png "GitHub statistics")
![Claude Code Stats](/assets/blog/2026/07/claudecodestats.png "Claude Code statistics")

His conclusion: **the Software Development Lifecycle as we know it is dead.** The DevOps loop is evolving into what he called ["The Ralph Loop"](https://medium.com/@tentenco/what-is-ralph-loop-a-new-era-of-autonomous-coding-96a4bb3e2ac8) — a much faster path from code to production, with developers acting as verifiers, because agents still fail often. The winning team, in his view, is the one whose agents understand the company's mission, values, and purpose.

One practical problem he highlighted: when you code with agents, context fragments across chats, prompts, sessions, and branches. Tools like [entire.io](https://entire.io/) now store the chat sessions behind each PR right in the GitHub repository — so the *intent* behind a change doesn't evaporate. You may want to check this tool out! Let's see how the GitHub, we know today, evolves over the next decade.

## Retrieval is the weakest link in your RAG

One of our favorite technical talks, by Tomek Porozynski (deepsense.ai), tackled the "R" in RAG (Retrieval Augmented Generation). General embedding models are trained on public data — they know general language, **not your business**. The fix: fine-tune the embedding model on examples from your own domain, so the vector space itself shifts to reflect your terminology and the real relationships between your terms.

The mechanics are surprisingly approachable: reshape the vector space through relative distances (pull matching pairs closer, push mismatched pairs apart), using either **triplet loss** or **MultipleNegativesRankingLoss** — and with the [Sentence Transformers](https://sbert.net/) toolkit, the latter is literally one import away.

![RAG Cheat sheet](/assets/blog/2026/07/rag.jpeg "Your RAG cheat sheet")

If you want to try it yourself, the speaker shared [hands-on Colab notebooks](https://github.com/ontaptom/workshops/tree/main/notebooks).

## The security wake-up call: surviving the "Vulnpocalypse"

Adrian Mouat (Chainguard) delivered the talk that stuck with us the most. Advanced AI models can now autonomously discover and weaponize zero-day vulnerabilities at machine speed — effectively **erasing the traditional patch window**. Especially with the rise of [Anthropic Mythos](https://www.anthropic.com/claude/mythos) model, this might lead to Vulnpocalypse!

This is very serious for open source: attackers can point LLMs at public codebases, while underfunded maintainers face an overwhelming volume of newly discovered bugs. As people who live and breathe open source databases, this hits close to home.

The defenses he proposed:

- **Fight AI with AI** — proactively scan your own infrastructure and find vulnerabilities before attackers do.
- **Minimize your attack surface** — fewer dependencies, and consider AI-written snippets over pulling in vulnerable third-party libraries.
- **Strict hygiene** — immediate patching and eliminating long-lived access tokens are non-negotiable.
- **Industry coalitions** — rapid-response groups like [Athena](https://www.chainguard.dev/athena) share mitigations at machine speed, while "Akrites" safely funnels fixes back into upstream open source projects.

At Percona, we're already evaluating joining these coalitions - stay tuned! 

Related: Isha Salania (Microsoft) showed how **confidential computing** extends encryption to data *in use* — your prompts, retrieved chunks, and keys living in encrypted memory. For anyone building sovereign RAG systems on top of databases, this end-to-end view of data protection is worth understanding — and it's going to raise expectations for queryable encryption across the whole database ecosystem.

## "MCP doesn't suck — your agent does"

Best talk title of the conference, courtesy of Jan Curn (Apify). The problem: most agents load *all* available tool schemas into the context window upfront, causing context rot, slow performance, and rapidly burning tokens. Their answer is **mcpc** — a lightweight CLI that enables *progressive tool discovery*: the agent fetches only the tool schemas it needs, on demand, and chains workflows through native code execution. Add OAuth 2.1 and sandboxed proxy connections, and you get a much saner MCP setup.

## More gems worth your time

- **From SDLC to ADLC.** Marcin Wawryszczuk (Andersen) argued that AI speeds up *coding* but not the *release cycle* — the industry needs an Agentic Delivery Lifecycle where agents help with requirements, architecture, docs, and pipelines, while engineers keep authority over architecture, governance, and validation. 
- **Don't lock in your AI tooling too early.** Angie Jones shared how Block bought access to many tools and let engineers run with them — what works for a web developer doesn't work for a mobile or JVM developer, and that diversity of feedback is gold. Standardize when you see workflows succeeding repeatedly, not because a vendor made a good pitch.
- **LLMs in the wild.** GetYourGuide's data scientist and MLOps engineer walked through keeping an AI-driven recommendation system alive in production. Real numbers, real trade-offs. 
- **Platform-as-a-Product.** Dominik Schmidle (Giant Swarm) on why internal platforms fail: happy users won't save your platform if the C-level sees it as pure cost. Know your user *and* your decision-maker — and do internal marketing.
- **Werner Vogels (CTO, Amazon) fireside chat.** Invisible work is important and worth sharing. Stay curious, never stop learning — and he recommended the book [*Ask Your Developer*](https://www.amazon.de/Ask-Your-Developer-Software-Developers/dp/0063018292) by Jeff Lawson.

## The expo floor

Between the talks, we've also hung out at the Percona booth - yes, we've been there the entire two days and chatting with 100+ visitors about what we love the most - databases!
 
![Percona booth](/assets/blog/2026/07/perconabooth.jpeg "Percona Booth at WeAreDevelopers 2026")

We've also visited our neighbours at the expo hall and had great conversations with them, too — but there was one that stood out:

[**Qodo**](https://www.qodo.ai/) (formerly CodiumAI): AI code review that indexes your entire repository, so reviews understand the architectural "why" behind a change — and it's [free for open source projects](https://github.com/marketplace/qodo-merge-pro-for-open-source). We're excited to try it on our own projects.

## Parting words

Two quotes from the WeAreDevelopers founders stayed with us. From CPO Thomas Pamminger:

> AI didn't make me worse at my job — it made it easier to be worse without noticing. Charles Eames, asked what he'd delegate, said: **never the understanding.**

And from CEO Sead Ahmetović:

> Someone, somewhere, will depend on what you ship next. That's not a burden — that's the whole point, because your work matters. Let's do it well.

That's a pretty good summary of why we go to these events: to keep understanding, not just shipping.

If any of the topics above sparked something — RAG fine-tuning, supply chain security, vector search in databases — chat with us on the [Percona Community Forum](https://forums.percona.com/) or just drop a comment here. We'd love to hear what *you* took away from WAD if you were there.

See you at the next event!
