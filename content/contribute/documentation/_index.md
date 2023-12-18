---
title: "Percona Product Documentation"
description: "How to contribute to the Percona Product Documentation"
---

{{% hero-gradient class="aqua" %}}

# Contributing to Percona Product Documentation

Our product documentation is constantly evolving and improving. Did you spot
some outdated information, or a typo? Is the documentation incomplete or confusing?

Help us making it better!

If you would like to leave feedback or make a suggestion about enhancing our
product documentation, you have multiple options of doing so.

{{% /hero-gradient %}}

{{% hero %}}
{{% typography %}}
## Submitting Actual Changes to the Documentation

As we say in the open source world, "patches are always welcome!" - So instead of
submitting a request to get the documentation changed, how about submitting the
concrete changes yourself? It's really easy but can be intimidating the first
time. This guide should take the edge off and you'll see your changes live in a
matter of hours!

* Similar to our software, our documentation is open source and is managed using
  the same tools that we use to manage changes to our code base.
* All of our manuals provide an "Edit this page" option that you can
  use to perform the actual documentation changes that you would like to see in
  your web browser. Note that this process requires having an account on GitHub
  and some basic understanding of the [code submission and review
  process](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
  on this platform.
* The documentation for each product is maintained in dedicated git repositories
  per product. See [Location of Documentation and Sources](./locations) for
  details about the location of the documentation for each product.
* Most of these locations contain a file called `CONTRIBUTING.md` that outlines
  the steps required to submit a change for the documentation.
* We try to maintain a consistent style across our documentation. If you're
  making changes to the documentation, please follow the guidelines outlined in
  the [Percona Documentation Style Guide](https://docs.percona.com/style-guide/).

<iframe width="560" height="315" src="https://www.youtube.com/embed/3bNBzgd1qxI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Submitting a Jira ticket

If your suggestion is bigger than what you can personally handle or you would
like to solicit some feedback on your proposal before submitting it, no problem!
Similar to the software engineers working on our various products, we use our
[public instance of Atlassian Jira](https://perconadev.atlassian.net/) for tracking our
Documentation work as well.

* If you have a **product-specific** suggestion, please submit your request in
  the corresponding product's Jira project (e.g.
  [PS](https://perconadev.atlassian.net/projects/PS/) for Percona Server for MySQL,
  [PMM](https://perconadev.atlassian.net/projects/PMM/) for PMM,
  [PSMDB](https://perconadev.atlassian.net/projects/PSMDB/) for Percona Server for
  MongoDB).
* Make sure to **select "Documentation" as the Component** when submitting your
  request and please **include a link to the public location** of the
  documentation page that you would like to get changed.
* If you would like to suggest an improvement or change that affects all of
  Percona's documentation (e.g. a structural or stylistic change), there's a
  [dedicated DOCS Jira project](https://perconadev.atlassian.net/projects/DOCS/) that
  tracks overarching documentation issues.
{{% /typography %}}
{{% /hero %}}
