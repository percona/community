---
title: "Recap Monthly Percona Developer Meetup Hacktoberfest"
date: "2022-10-05T00:00:00+00:00"
draft: false
tags: ["hacktoberfest", "percona", "databases"]
authors:
  - edith_puclla
images:
  - blog/2022/10/recap-mpdm-hacktoberfest-intro.png
slug: recap-monthly-percona-developer-meetup-hacktoberfest
---

The [Monthly Percona Developer Meetup](https://percona.community/blog/2022/09/26/monthly-percona-developer-meetup/) is an opportunity to get a behind-the-scenes view of different projects in Percona and directly interact with the experts to exchange ideas, ask questions, etc.

From now on, Monthly Percona Developer Meetups will take place monthly to have open discussions and in-person (online) communication. You can join our Developer Meetup via Restream, the [Percona YouTube](https://www.youtube.com/channel/UCLJ0Ok4HeUBrRYF4irturVA) channel, and [LinkedIn](https://www.linkedin.com/company/percona/) events.

![Overview](blog/2022/10/recap-mpdm-hacktoberfest-intro.png)

The topic of the first Monthly Percona Developer Meetup was [Hacktoberfest](https://hacktoberfest.com/).

**What is Hacktoberfest?** Hacktoberfest is an annual event hosted by DigitalOcean that encourages people to contribute to Open Source throughout October. It is inclusive, everyone can join to work on Open Source projects, and you can participate by choosing your favorite project.

You need two essential things to participate. First, register on the Hacktoberfest website anytime between September 26 and October 31, 2022. Second, look through the participating projects, choose your favorites, and consult the documentation guiding you to send your first contribution.

Forty thousand participants who complete Hacktoberfest and have at least four pull/merge requests accepted between October 1 and October 31 can have a tree planted in their name or the Hacktoberfest T-shirt. In that case, you can pick a tree planted in your name or the Hacktoberfest 2022 T-shirt.

Let's ask the Percona experts!

## Which Percona projects joined Hacktoberfest?

All the [Percona GitHub Projects](https://github.com/search?q=org%3Apercona+hacktoberfest) with the label: “hacktoberfest” are ready to contribute.

![Overview](blog/2022/10/recap-mpdm-hacktoberfest-youtube.png)

## How do I find issues?

- On **GitHub**, the issues are tagged with the **good-first-issue** tag.
- On Jira, tagged with **newbie**, **hacktoberfest** and **onboarding**
- You can also pick any other issue you like or create new ones.

## What types of contributions count?

You can contribute in several ways: coding, documentation, testing, design, discussions, Content Creator (Blog posts, videos), etc.; they all count.

## How can you reach the Percona team?

The best way to do it is directly in the Percona projects, or you can join our community slack, [Discord](https://discord.com/channels/808660945513611334/1019608914683244635), or write us in our [Community Forum](https://forums.percona.com/).

![Overview](blog/2022/10/recap-mdpdm-hacktoberfest-repositories.png)

Look at some of the Percona projects added to Hacktoberfest this year.

Starting for [percona/percona-docker](https://github.com/percona/percona-docker). Supported by **Evgeniy Patlan**, Manager, Build & Release Engineering. There are images for basic scenarios. The idea is to create more images and improve the existing ones or extend them to Docker Compose. Also, contributions to improve the Docker setup are welcome. You can find issues in Jira or GitHub, where you can also participate in discussions about Percona Docker images.

![Overview](blog/2022/10/recap-percona-docker.png)

Our next project is [Percona Monitoring and Management (PMM)](https://github.com/percona/pmm). This project is supported by **Artem Gavrilov**, Backend Software Engineer, and **Nurlan Moldomurov**, Full-Stack Engineer. PMM is a great project to contribute to during Hacktoberfest. There are minor and easy-to-do issues in [Github](https://github.com/percona/pmm/issues); it is not necessary to register them in Jira. These contributions are welcome if you have any good ideas, want to improve something or simplify some process. Send your PR; the maintainers will review it as soon as possible. We also have advanced issues if you want to go for more advanced tasks.

![Overview](blog/2022/10/recap-pmm.png)

For our third project, we have [percona/mongodb_exporter](https://github.com/percona/mongodb_exporter). **Carlos Salguero** is the maintainer for this project. He says it is a project easy to get started, and there is not much-complicated logic behind this.
It is about running some MongoDB internal commands to get statistics like diagnostic data or replica status, passing JSON to produce metrics from these commands. You use a complete Makefile to start sandbox instances to test almost everything; you don’t have a virtual machine or different MongoDB instances. The issues are in **GitHub** and **Jira**. The primary programming language is Go.

It's the turn of [percona/percona-server-mongodb-operator](https://github.com/percona/percona-server-mongodb-operator); **Denys Kondratenko** is the maintainer of this project. It is an excellent opportunity to learn about Kubernetes and how to extend it and maintain stateful databases inside Kubernetes. Most of the things are tracked in GitHub and Jira.

![Overview](blog/2022/10/recap-operator.png)

Our next project is [percona/pg_stat_monitor](https://github.com/percona/pg_stat_monitor), a Query Performance Monitoring tool for PostgreSQL. The maintainer is **Ibrar Ahmed**, Sr. Software Engineer (PostgreSQL). The primary area to contribute is the releases. If there are contributions with ideas on improving the information provided for **pg_stat_monitor**, they are welcome. The issues are defined in Jira.

**In summary**, those are some of our projects that are in Hacktoberfest.
This month is Open Source month; it's Hacktoberfest month party!

Remember that you can interact with the maintainers of each project through [GitHub](https://github.com/search?q=org%3Apercona+hacktoberfest)/[Jira](https://jira.percona.com/browse/DISTMYSQL-228?filter=-4)/[Discord](https://discord.com/channels/808660945513611334/1019608914683244635) or our [Community Forum](https://forums.percona.com/).

If you haven't sent a PR, this is the time to do it. Write us at community-team@percona.com if you have any questions.

Happy Hacktoberfest with Percona!
