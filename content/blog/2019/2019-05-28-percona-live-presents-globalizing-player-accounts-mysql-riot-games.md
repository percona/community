---
title: 'Percona Live Presents: Globalizing Player Accounts with MySQL at Riot Games'
date: Tue, 28 May 2019 16:48:15 +0000
draft: false
tags: ['author_tyler', 'Events', 'MySQL', 'Open Source Databases', 'Percona Live 2019']
images:
  - blog/2019/05/riot-games.jpg
authors:
  - tyler_turk
slug: percona-live-presents-globalizing-player-accounts-mysql-riot-games
---

![](blog/2019/05/riot-games.jpg)

During my presentation at [Percona Live 2019](https://www.percona.com/live/19/sessions/globalizing-player-accounts-with-mysql-at-riot-games), I’ll be talking about how [Riot Games](https://www.riotgames.com/en), the company behind League of Legends, migrated hundreds of millions of player accounts to unlock opportunities for us to delight players. This meant moving ten geographically distributed databases into a single global database replicated into four AWS regions. I’ll talk about some of the technical decisions we made, the expected vs actual outcomes, and lessons we learned along the way. 

Migrating hundreds of millions of player records without impacting a player's ability to manage their account and log in was a daunting task. I'll shed some light on how we managed to handle this data migration while modifying the database schema. I’ll also go into detail on the backend architecture of our accounts service, such as how we use Continuent Tungsten, which we’re leveraging to manage our globally replicated database. 

I gave a [similar version of this talk](https://www.youtube.com/watch?v=MJpZZm62ZKw) at AWS re:Invent last year, and wrote the article “[Globalizing Player Accounts](https://technology.riotgames.com/news/globalizing-player-accounts)” on the [Riot Games Tech Blog](http://technology.riotgames.com)—check out these resources for more deep tech details and context on our accounts solution.

Who’d get the most from this presentation?
------------------------------------------

The presentation will be most helpful for folks who want to learn about strategies for deploying globally replicated databases, especially developers and DBA/DBEs who are building global services. I’ll also discuss how we think about deploying applications that will talk to these types of databases.

Whose presentations are you most looking forward to?
----------------------------------------------------

In particular, I'm really looking forward to VividCortex's talk on [optimizing performance and efficiency](https://www.percona.com/live/19/sessions/optimizing-database-performance-and-efficiency) because I’d like to see their perspectives on performance issues. I’m excited to learn more by comparing their solutions to the ones I’ve seen at my own company. 

I'm also looking forward to the Facebook talks ([Part 1](https://www.percona.com/live/19/sessions/mysql-replication-and-ha-at-facebook-part-1) & [Part 2](https://www.percona.com/live/19/sessions/mysql-replication-and-ha-at-facebook-part-2)) on HA MySQL because I’m interested in this problem space and I’m curious about their solutions for managing data at scale.