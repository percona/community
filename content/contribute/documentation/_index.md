---
title: "Percona Product Documentation"
description: "How to contribute to the Percona Product Documentation"
---

{{% hero background="purplegalaxy.jpg" %}}
{{% herotext %}}
## Contributing to Percona Product Documentation

Our product documentation is constantly evolving and improving. Did you spot
some outdated information, or a typo? Is the documentation incomplete or confusing?

Help us making it better!

If you would like to leave feedback or make a suggestion about enhancing our
product documentation, you have multiple options of doing so.
{{% /herotext %}}
{{% /hero %}}

{{% hero %}}
{{% typography %}}
## Submitting Actual Changes to the Documentation

As we say in the open source world, "patches are always welcome!" - So instead of
submitting a request to get the documentation changed, how about submitting the
concrete changes yourself? It's really easy but can be intimidating the first
time. This guide should take the edge off and you'll see your changes live in a
matter of hours!

* Similar to our software, our documentation is open source and is managed using
  the same tools and processes that we use to incorporate changes to our code
  base.
* Several of our manuals already provide an "Edit this page" link that you can
  use to perform the actual documentation changes that you would like to see in
  your web browser. Note that this process requires having an account on GitHub
  and some basic understanding of the [code submission and review
  process](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
  on this platform.
* The location of where the documentation for a specific product is maintained
  differs from product to product. For some products/project, we maintain the
  documentation files in the same git repository that is also used for the
  project's source code. For other products, the documentation is maintained in
  a dedicated git repository. See [Location of Documentation and
  Sources](./locations) for details about the location of the documentation for
  each product.
* Most of these locations contain a file called `CONTRIBUTING.md` that outlines
  the steps required to submit a change for the documentation. This process may
  be different from product to product, so make sure to follow these
  instructions.

## Submitting a Jira ticket

If your suggestion is bigger than what you can personally handle or you would
like to solicit some feedback on your proposal before submitting it, no problem!
Similar to the software engineers working on our various products, we use our
[public instance of Atlassian Jira](https://jira.percona.com/) for tracking our
Documentation work as well.

* If you have a **product-specific** suggestion, please submit your request in
  the corresponding product's Jira project (e.g.
  [PS](https://jira.percona.com/projects/PS/) for Percona Server for MySQL,
  [PMM](https://jira.percona.com/projects/PMM/) for PMM,
  [PSMDB](https://jira.percona.com/projects/PSMDB/) for Percona Server for
  MongoDB).
* Make sure to **select "Documentation" as the Component** when submitting your
  request and please **include a link to the public location** of the
  documentation page that you would like to get changed.
* If you would like to suggest an improvement or change that affects all of
  Percona's documentation (e.g. a structural or stylistic change), there's a
  [dedicated DOCS Jira project](https://jira.percona.com/projects/DOCS/) that
  tracks overarching documentation issues.
{{% /typography %}}
{{% /hero %}}
