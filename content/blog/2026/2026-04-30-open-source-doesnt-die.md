---
title: "Open source doesn’t die. It gets unfunded."
date: "2026-04-30T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'pgBackRest']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2026/04/opensourcedoesntdie-blog-hero-fundit.png
---

If you are using PostgreSQL in any capacity very likely this week has started for you with a bang. pgBackRest, one of the most known tools for PostgreSQL, praised for the scalable and reliable way to do backups has announced that the project is currently archived.

## Archived, [you mean EOL](https://www.reddit.com/r/PostgreSQL/comments/1sx2ttg/comment/oilzdag/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)?

![blog/2026/04/opensourcedoesntdie-reddit.png](blog/2026/04/opensourcedoesntdie-reddit.png)

No! Open source software rarely has a hard “end of life.” What it does have are maintainership gaps and those can be just as serious.

It’s different when PostgreSQL community announces a major version EOL. This happens because Community chooses to not to support it and move on to focus on newer versions.

![blog/2026/04/opensourcedoesntdie-thisisopensource.png](blog/2026/04/opensourcedoesntdie-thisisopensource.png)

Reading the message from David Steele, the long-time primary maintainer of pgBackRest you will not find “end of life” term. The project is marked read-only and no longer actively maintained, but that is not the same as being permanently dead.

![blog/2026/04/opensourcedoesntdie-maintenance.png](blog/2026/04/opensourcedoesntdie-maintenance.png)

pgBackRest is not “end of life.” There is no governing body declaring support ended. What happened is simpler and more common in open source: the maintainer can no longer afford to continue.

## So what happened then?

This requires some story telling and I don’t think that I can do it better than [Lætitia Avrot](https://mydbanotebook.org/about/) already did in her [blogpost](https://mydbanotebook.org/posts/pgbackrest-is-dead.-now-what/#what-happened) (though I do not like the title): 

> Crunchy Data, which had sponsored `pgBackRest` for most of its life and employed David, was sold. After that, David spent months looking for a position that would let him keep working on the project. He also tried to secure independent sponsorship. Neither worked out. He needs to make a living. The project requires sustained effort which he can no longer provide without being paid for it.

This is the issue. An experienced developer, who wants to work on the project (that a big chunk of enterprises use) finds himself to be the “Nebraska guy” from [XKCD comic](https://xkcd.com/2347/). 

When you look at the situation we’re in this is the classic “Nebraska guy problem”: critical infrastructure maintained by a single person. pgBackRest is widely used in production, yet its sustainability dependson one individual being able to justify working on it. That does not seem fair and David did right to point this out with his move. 

Of course, if anyone in the community chose to, they can still maintain the project by forking it. But why, since the problem is elsewhere?

Most people understand that engineers need to be paid for their work. What not everyone realizes is that the free for all software that the open source license provides does not mean free as in beer. Someone still needs to fund it! 

Unfortunately “someone” almost certainly is going to be “no-one” unless “anyone” realizes they are going to miss the software if nobody maintains it anymore. 

While there’s a claim to be made that:

> Companies are as good as they have to and as bad as they are allowed to

And often we see that an entity uses software they do not have to pay license fees for, treating this as cost optimization. There is also a large chunk of organizations that realize this is not a good long term strategy. Actively lowering the operational risk is important.

This is where foundations typically kick in: providing an easy way for organizations to contribute and ensure the longevity and healthiness of the projects. But PostgreSQL does not (yet) have one.

## Where are we now?

There’s a lot of backchannel talks happening. 

Join the ones on:

- Telegram
- Discord
- Slack
- [Reddit](https://www.reddit.com/r/PostgreSQL/comments/1sx2ttg/pgbackrest_is_no_longer_being_maintained/) (I don’t have enough karma to engage there :/)

or let us know what is your stance [(Percona Community Forum thread available)](https://forums.percona.com/t/pgbackrest-is-eol/40720) so that we can represent you in the discussions we are having.

A lot of blog posts have been written on this subject, check out [Planet PostgreSQL](https://planet.postgresql.org/) to find some of them! I particularly enjoyed some of them, the [one](https://proopensource.it/blog/postgresql-ecosystem-problems-2026) from [Stefanie Janine Stölting](https://proopensource.it/stefanie-janine-stoelting.html), I feel I am mostly aligned with. PostgreSQL needs an Ecosystem Umbrella Foundation

## The future of open source is on us

Reading that a project is EOL is triggering to me. When long-time maintainer announced plans to step away after more than a decade of work, instead of focusing on what the problem is that caused him to do so and how to solve the issue.Naming it “dead” complicate things even further. Labeling the project as “dead” doesn’t solve the problem. Rather, it accelerates the wrong response. Users start looking for replacements instead of asking how to sustain the project.

This is not the way, young Padawan!

![blog/2026/04/opensourcedoesntdie-youngpadawan.png](blog/2026/04/opensourcedoesntdie-youngpadawan.png)

We need a body that helps both users and authors by:

1. Providing governance and a helping hand to the ecosystem. Yes, this is also funding
2. Providing guarantees of healthiness. This means users will have it easier to know the tools are in good shape.

## So what’s with pgBackRest

While we talk here in the public, a lot of decisions are being made and Percona among other companies is working towards resolving this situation. 

![blog/2026/04/opensourcedoesntdie-allyouneed.png](blog/2026/04/opensourcedoesntdie-allyouneed.png)

Have patience. Work is already underway behind the scenes, and the situation is evolving. There will be positive news resolving the situation coming soon, as Open Source doesn't die!
