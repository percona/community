---
title: "I Built an AI That Impersonates Me on Slack, and It Was Disturbingly Easy"
date: "2026-03-03T00:00:00+00:00"
tags: ["Percona", "Vibe Coding", "Community", "Security", "Open Source"]
categories: ['PostgreSQL']
authors:
  - kai_wagner
images:
  - blog/2026/03/vibe-coded-slack-impersonation.png
---

I spend a lot of time in Slack. Most people in tech do. It's where a lot of "work" happens suche like, quick questions, async decisions, the "hey can you look at this?" threads that never seem to end. It feels personal. You think you know who's on the other end.

So a few days back I just asked myself, what would it actually take to have an AI respond to my DMs, pretending to be me?

Turns out: a few hours, some TypeScript, and a token already sitting on my machine.

## What I Built

The bot polls your Slack DMs silently in the background using your real desktop token, no Slack admin approval, no OAuth app setup, no review process needed. It reads incoming messages and decides whether to reply, react with an emoji, or just stay quiet, the way a real person would. It replies in your voice, trained on a handful of past conversations you've had, matching your tone, vocabulary, and how casually you punctuate things.

If someone asks whether it's an AI, it responds with something like "lol what? why do you ask 😅", the kind of mild confusion a real person would show. Salary talks, politics, anything sensitive gets redirected with "let's talk about this in person". It handles images and files sensibly rather than just spitting back garbled metadata. And it only ever touches DMs; group channels are a hard no, with an explicit check baked in.

## How It Actually Works

**Getting a token:** Slack's desktop app stores your session in the browser's local storage. Open DevTools, one line of JavaScript in the console, done. Full API access, same as the Slack app itself. No developer portal, no approval, no waiting.

**The AI side:** Send the Anthropic API the recent thread plus a persona prompt built from your past conversations, get back a JSON response: text reply, emoji reaction, or silence. A rate limiter spaces things out to stay within free-tier limits.

**The persona:** Drop a few text files of your past conversations into a folder. Three or four examples are genuinely enough for the model to pick up a recognisable voice. That part surprised me more than anything else.

**The guardrails:** Prompt instructions. They work well enough for casual conversation. They're not magic.

Getting the first version working took maybe two hours. A few more to handle the rough edges: rate limits, image messages, a 200-DM pagination ceiling I ran into, emoji names Slack would reject. The usual stuff you'd expect from any real system.

## The Uncomfortable Part

Here's what stuck with me after building this.

Slack feels safe. It's behind your company SSO. It's where people share things they wouldn't put in an email. When a message comes from someone you work with every day, you apply almost zero scepticism to it. Of course it's them.

That assumption is now optional.

What I built here is, if you strip out the friendly framing: a system that reads every DM to a user, replies under their name in their tone, actively deflects if you try to verify whether it's human, and does all of this indefinitely and silently from a laptop running in the background.

Nobody on the receiving end would know. The messages look right. The timing is plausible. The style matches. It gives the one response that would usually expose it with the kind of confusion a real person would show.

We added ethical guardrails, no salary discussions, no politics, sensitive stuff gets redirected to "let's talk in person". But those are prompt instructions. They exist because I chose to write them. Someone building this without them simply wouldn't have them.

#### This conversation has happened, without me ever touching the keyboard....yes, Zsolt was aware!

![](blog/2026/03/impersonation-slack-conversation.png)


## "Easy" Is Relative, But Not By Much

Core functionality (polling DMs, calling the API, posting replies) was working in under two hours.

The tooling: **Bun**, a modern TypeScript runtime that made setup trivial. **Anthropic's SDK**, clean API, takes a system prompt and a conversation and returns structured JSON. **Slack's own API**, well-documented and permissive with desktop tokens.

No specialised knowledge needed. Anyone motivated enough could reproduce this easily. Someone who does this professionally could build something considerably more capable, and that's precisely where it gets more uncomfortable.

#### That's how the CLI output looks like

```
slack-bot$ bun run bot
$ bun run src/index.ts
[slack-bot] Running | mode: allowlist | backend: claude | review: off
[slack-bot] My user ID: U03A3PZHK5X
[slack-bot] Mode: allowlist | Allowlist: U03QTQQHZFX, U83651WSX
[slack-bot] Polling every 15s...
[slack-bot] D04BZ2BNABU: 1 new message(s) from [U83651WSX]
[slack-bot] New DM from U83651WSH — generating reply...
[slack-bot] Claude call — est. ~933 input tokens
[slack-bot] Claude tokens: 1049 in / 8 out
[slack-bot] Ignoring message from U83651WSX (AI chose no response)
[slack-bot] Handled message from U83651WSX
[slack-bot] D04BZ2BNABU: 1 new message(s) from [U83651WSX]
[slack-bot] New DM from U83651WSX — generating reply...
[slack-bot] Claude call — est. ~944 input tokens
[slack-bot] Claude tokens: 1059 in / 23 out
[slack-bot] Handled message from U83651WSX
[slack-bot] D04BZ2BNABU: 1 new message(s) from [U83651WSX]
[slack-bot] New DM from U83651WSX — generating reply...
[slack-bot] Claude call — est. ~976 input tokens
[slack-bot] Claude tokens: 1085 in / 36 out
[slack-bot] Handled message from U83651WSX
[slack-bot] D04BZ2BNABU: 1 new message(s) from [U83651WSX]
```

#### That's how the CLI helper and options look like

```
slack-bot$ bun run bot --help
$ bun run src/index.ts --help
Usage: slack-bot [options] [command]

Personal Slack bot that replies as you

Options:
  -V, --version                  output the version number
  --mode <mode>                  Response mode: auto | away | allowlist | manual
  --review                       Enable review mode (approve before sending)
  --no-review                    Disable review mode
  --allow <user>                 Add user to allowlist (Slack user ID)
  --interval <secs>              Poll interval in seconds
  --backend <name>               AI backend: claude | ollama
  --config <path>                Path to config file (default: "config.json")
  -h, --help                     display help for command

Commands:
  context                        Manage active context
  check-user [options] <userId>  Check whether a user's DM channel is found and reachable
```

## What It Looks Like Without the Constraints

What I built runs against Claude's API with free-tier rate limits, small context window, a handful of persona examples, a throttle on message volume. Those constraints are real, and also completely trivially removable.

Run the same thing with a local model, Llama 3, Mistral, take your pick from the open-weight models available on consumer hardware today, and it changes significantly.

**No rate limits.** Every message gets answered immediately, without the 12-second pause between API calls. Response timing becomes indistinguishable from a fast typist.

**No token budget.** Instead of a few hundred tokens of context, you can feed it your entire Slack history. Months, years of it. Every thread, every in-joke, every project reference. The model doesn't just match your writing style, it knows what you've been working on, what you said about the Q3 roadmap in October, what you think about your manager.

**No API calls leaving your machine.** Nothing logged externally. Invisible from a network perspective.

With a large enough context window (Llama 3.1 supports 128k tokens, roughly 100,000 words), the last few *months* fit. "Remember what we decided on Thursday?" doesn't expose it anymore, because it actually has that conversation in its context.

And fine-tuning: nothing stops someone from training an open-weight model on a complete message history. Not imitating a writing style, *being* that writing style. LoRA fine-tuning on a consumer GPU takes an afternoon.

What I built in a few hours is a proof of concept. The version someone builds with local inference, a full message history export, and a fine-tuned model is something qualitatively different. Not a research project, weekend work for someone who knows what they're doing. All the building blocks are public, free, and well-documented.

## A Few Things Worth Knowing

This isn't a call to panic. But it's probably worth recalibrating a bit.

For anything that actually matters, financial, personal, strategic, verify out-of-band. A quick voice note or phone call costs almost nothing and resolves almost everything.

Unusual patterns are worth noticing. Response timing that's too consistent. Answers that are slightly generic when you'd expect specific. Deflection where you'd expect directness. None of these are proof of anything individually, but they're worth filing away.

The safe-space feeling Slack gives you is a product of habit, not architecture. Slack's security model protects your data from outsiders. It doesn't protect you from someone who has authenticated as themselves and is quietly running a process in the background.

Specific questions still help, for now. "Remind me what we decided on Thursday?" trips up a system with limited context. But that window is closing as context windows grow.

## Why did I built it?

I built this to see if it was possible. It was, faster than I expected, with tools that are widely available. The version I built in an evening is convincing enough for routine exchanges. A version with local inference and full conversation history would be convincing for most exchanges, including ones where you're actively looking for tells.

That gap between "afternoon project" and "genuinely hard to detect" is smaller than people assume, and it's shrinking. Better models, larger context windows, cheaper hardware, each of these individually makes impersonation easier; together they compound.

The signals you rely on to establish trust in digital communication, name, avatar, writing style, shared history, plausible timing, are all reproducible now, with effort that ranges from an afternoon to a weekend depending on how convincing you want to be.

Be a little curious about who you're actually talking to. And every now and then, just call them...which reminds me, that this might be worth another evening project research ;-). 

---

*Built with [Claude](https://claude.ai), [Bun](https://bun.sh), and the [Slack Web API](https://docs.slack.dev/apis/web-api/). The full source is not in my repository, as I'm not sure this is a wise thing to share.*
