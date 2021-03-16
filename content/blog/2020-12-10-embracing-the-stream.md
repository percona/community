---
title: 'Embracing the Stream'
date: Thu, 10 Dec 2020 10:33:29 +0000
draft: false
tags: ['author_kohntopp', 'centos', 'DevOps', 'GitHub', 'Gitlab', 'koehntopp', 'Linux', 'Open Source Databases', 'RedHat', 'Tools']
authors:
  - koehntopp
images:
  - blog/2020/12/stream-migrate-now.png
---

So this happened: [CentOS Project shifts focus to CentOS Stream](https://lists.centos.org/pipermail/centos-announce/2020-December/048208.html)

> The future of the CentOS Project is CentOS Stream, and over the next year we’ll be shifting focus from CentOS Linux, the rebuild of Red Hat Enterprise Linux (RHEL), to CentOS Stream, which tracks just ahead of a current RHEL release. CentOS Linux 8, as a rebuild of RHEL 8, will end at the end of 2021. CentOS Stream continues after that date, serving as the upstream (development) branch of Red Hat Enterprise Linux.

And a lot of people react like this: [![](https://isotopp.github.io/uploads/2020/12/stream-migrate-now.png)](https://twitter.com/nixcraft/status/1336348208184741888) _Oracle buys Sun: Solaris Unix, Sun servers/workstation, and MySQL went to /dev/null. IBM buys Red Hat: CentOS is going to >/dev/null. Note to self: If a big vendor such as Oracle, IBM, MS, and others buys your fav software, start the migration procedure ASAP. ([Tweet](https://twitter.com/nixcraft/status/1336348208184741888))_ So it seems my opinion is the unpopular one: CentOS switching to Stream is not bad at all. When you wanted to run Openstack on CentOS in 2015, you needed to enable [EPEL](https://fedoraproject.org/wiki/EPEL) to even begin an install. The first thing this did was literally replace every single package in the install. That was, because CentOS at that time was literally making Debian Stale look young. And we see similar problems with Ubuntu LTS, for what it’s worth. Ubuntu LTS comes out every 2 years, and that’s kind of ok-ish, but it lasts 5 years, which is nonsensical. It was not, in the past.

So what changed?
----------------

Software Development. We have been moving to a platform based development approach, leveraging the wins from DevOps. “Kris, that’s corporate bullshit.” It’s not, though. Let me spell it out in plain for you.

### Programming languages are platforms powered by tools

People these days do not program in an editor, with a compiler. They use Github or Gitlab, with many integrations, and a local IDE. They commit to a VCS (git, actually, the world converged on one single VCS), and trigger a bunch of things. Typechecks, Reformatters, Tests, but also Code Quality Metrics, and Security Scanners. Even starting a new programming language in 2020 is not as easy as it was in the past. Having a language is not enough, because you do not only need a language and maybe a standard library, but also a JetBrains Product supporting it, SonarQube support, XRay integration, gitlab-ci.yml examples and so on. Basically, there is a huge infrastructure system designed to support development and whatever you start needs to fit into it ,right from the start. That is, because we have come to rely on an entire ecosystem of tooling to make our developers faster, and to enforce uniform standards across the group. And that is a good thing, which can help us to become better programmers.

### Github and Gitlab are tools for conversations about code among developers

We also have come to rely on tooling to enable collaboration, and structured discussion about code, since we as programmers no longer work alone. A good part of the value of Gitlab, Github and similar is enabling useful cooperation between developers, in ways that Developers value. Another good part of the value is extracted at the production end of these platforms: We produce artifacts of builds, automatically and in reproducible ways. Which includes also knowing things about these artifacts - for example, what went into producing them and being able to report on these things:

*   Dependencies
*   Licenses
*   Versions
*   Vulnerabilities
*   Commit frequency and time to fix for each dependency, abandonware alert

and many more things. With these processes, and repositories, and with one other ingredient, we have made rollouts and rollbacks an automated and uniform procedure, provided we find a way to manage and evolve state properly. Compared to the hand crafted bespoke rollout and rollback procedures of the 2010s, this is tremendous progress.

### Immutable infrastructure, and reproducible builds

This other ingredient is immutable infrastructure. It is the basic idea that we do no longer manipulate the state of the base image we run our code on, ever, after it is deployed. It’s basically death to Puppet and its likes. Instead we change the build process, producing immutable images, and quickly rebuild and redeploy. We deploy the base image, and then supply secrets, runtime config and control config in other, more appropriate ways. Things like Vault, a consensus system such as Zookeeper, or similar mechanisms come to mind. It allows us to orchestrate change across a fleet of instances, all alike, in a way that guarantees consistency across our fleet, in an age where all computing has become distributed computing. The same thinking can be applied to the actual base operating system of the host, where we remove application installs completely from the base operating system. Instead we provide a mechanism to mount and unmount application installs, including their dependencies, in the form of virtual machine images, container images or serverless function deployments (also containers, but with fewer buttons). As a consequence, everything becomes single-user, single-tenant - one image contains only Postgres, another one only your static images webserver (images supplied from an external mountable volume), and a third one only your production Python application plus runtime environment. With only one thing in the container, Linux UIDs no longer have a useful separation function, and other isolation and separation mechanisms take their place:

*   virtualization,
*   CGroups,
*   Namespaces,
*   Seccomp,

and similar. They are arguably more powerful, anyway. This also forms a kind of argument in the great “Is curlbash or even sudo curlbash still a bad thing?” debate of our times, but I am unsure which (I’m not: in a single-user single-tenant environment curlbashing into that environment should not be a security problem, but you get problems proving the provenance of your code. Which you would not have, had you used another, less casual method of acquiring that dependency).

### Images as building blocks for applications

So now we can use entire applications, with configuration provided and injected at runtime, to construct services, and we can add relatively tiny bits of our own code to build our own services on top of existing services, provided by the environment. We get Helm Charts for Kubernetes, we get [The Serverless Sea Change](https://www.infoq.com/articles/serverless-sea-change/), and Step Functions. We also get Nocode, Codeless or similar attempts at building certain things only from services without actual coding. But it is more pervasive than this:

*   The Unifi Control Plane uses multiple Java processes and one Mongodb. It can be dockered into one container, or can be provided as helm chart or as a docker-compose with multiple containers, for better scalability and maintenance.
*   The gitlab Omnibus uses a single container, again, with Postgres, Redis and a lot of internal state plus Chef to deploy about a dozen components, but differentiated deploys for the individual components in a K8s context also exist.
*   Things like a Jitsi setup can be packaged into a single, relatively simple docker-compose.yml, and will assemble themselves from images mostly automatically. The result will run on almost any operating system substrate, as long as it provides a Linux kernel syscall interface.

### Fighting Conway’s law

At that is kind of the point: By packing all dependencies into the container or VM image itself, the base operating system hardly matters any more. It allows us to move on, each on their own speed, on a per-project basis. The project will bring its own database, cache, runtime and libraries with itself, without version conflicts, and without waiting for the distro to upgrade them, or to provide them at all. Conversely it allows the Distro to move to Stream: They are finally free from slow moving OSS projects preventing them from upgrading local components, because one of them is not yet ready to move. Even teams in the Enterprise are now free to move at their own speed, because they no longer have to wait for half a dozen stakeholders ot get to the Technical Debt Section of their backlog. The main point is, in my opinion, that it is okay and normal for the application to use a different “No longer a full OS” than what the host uses. In acknowledging that both can reduce scope and size, and optimize. This is a good thing, and will speed up development. So in a world where components and their dependencies are being packaged as single-user single-tenancy units of execution (virtual machines, containers and the like), CentOS moving to Streams is not only acknowledging that change, it also forced the slower half of the world to acknowledge this, and to embrace it. I say: This is a good thing. And if you rant “Stability goes out of the window!” - check your calendar and your processes. It’s 2020. Act like it. One of the major innovations in how we do computers in the last decade has been establishing the beginnings of a certifiable process for building the things we run. Or, as [Christoph Petrausch](https://isotopp.github.io/Christoph%20Petrausch) puts it in [this tweet](https://twitter.com/hikhvar/status/1336608880013488130): “If your compliance is based on certifying the running end product instead of the process that built it, your organisation will not be able to keep up with the development speed of others.”  

_First published on [https://blog.koehntopp.info/](https://blog.koehntopp.info/) and syndicated here with permission of the author._