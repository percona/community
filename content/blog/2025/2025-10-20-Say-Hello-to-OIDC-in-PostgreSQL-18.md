---
title: "Say Hello to OIDC in PostgreSQL 18!"
date: "2025-10-22T11:00:00+00:00"
tags: ['PostgreSQL', 'Opensource', 'pg_jan', 'OIDC', 'Security']
categories: ['PostgreSQL']
authors:
  - jan_wieremjewicz
images:
  - blog/2025/10/Slonik-passport.png
aliases:
  - /blog/2025/10/20/say-hello-to-oidc-in-postgresql-18/
  - /blog/2025/10/20/say-hello-to-oidc-in-postgresql-18
---

If you’ve ever wondered how to set up OpenID Connect (OIDC) authentication in PostgreSQL, the wait is almost over.

We’ve spent some time exploring what it would take to make OIDC easier and more reliable to use with PostgreSQL. And now, we’re happy to share the first results of that work.

### Why OIDC, and why now?

We’ve spoken to some of our customers and noticed a trend of moving away from LDAP to OIDC. Our MongoDB product is already providing OIDC integration and the team working on PostgreSQL products saw an opportunity coming with PostgreSQL 18.

As some of you may have noticed **PostgreSQL 18** has introduced improvements to authentication that include OAuth 2.0 support. It’s a small step from OAuth 2.0 to OIDC, which builds directly on top of it. So we set out to test PostgreSQL 18’s integration with one of the most common OIDC providers: Okta.

That’s when we discovered a missing piece. While PostgreSQL 18 includes the underlying support for OAuth 2.0, it still lacks a validator library required to successfully complete an OIDC configuration.
So… we built it.

### Closing the gap for enterprise needs

Percona is known for our Support, Managed, and Consulting services for open source databases. But while our services are commercial, our mission remains deeply open source.

We don’t differentiate users by the size of their wallets. We want everyone using open source databases to succeed, grow, and benefit from the same quality foundations that enterprises rely on. Services is what finances our open source investments, what we believe is truly honest and sustainable open source development.

OIDC is a great example of how real-world enterprise needs and community innovation come together. PostgreSQL 18 introduced OAuth thanks to community efforts, but OIDC that helps organizations handle compliance and scale was still not supported. With the work on OIDC validator we want to close the gap between these two while keeping the solution open source.

### The power is in testing

It would be great if integrating with one OIDC provider meant it works with all of them. Unfortunately, real world implementations differ, sometimes significantly.
That’s why compatibility testing matters. That’s also why often particular providers we find require independent approach and some custom handling in the code.

So far, we’ve done some preliminary tests of the library. It’s not production-ready yet. It’s a first release that’s shared with users and Community to get feedback while in the meantime our engineers will put it through rigorous testing regimen.
We’ve so far tested the validator library compatibility with:

&nbsp;&nbsp;&nbsp;&nbsp;✅ **Okta**

&nbsp;&nbsp;&nbsp;&nbsp;✅ **Ping Identity**

&nbsp;&nbsp;&nbsp;&nbsp;✅ **Keycloak**

&nbsp;&nbsp;&nbsp;&nbsp;✅ **Microsoft Entra ID (Azure AD)**

We’re aware it’s not yet compatible with Google’s OIDC implementation, which has a few unique quirks, but that’s on our roadmap for future work.
The broader the testing, the stronger the solution. This is where we hope the Community can join us.

### Try the OIDC validator library now!

We’re excited to share that the first release of the OIDC [validator library is now available](https://github.com/Percona-Lab/pg_oidc_validator/releases/tag/latest) for your feedback.
[The repository includes](https://github.com/Percona-Lab/pg_oidc_validator/tree/main):

* Basic setup instructions in the README,
* Introductory documentation for getting started, and
* Links to examples and test configurations.

More detailed guides, including how OIDC works under the hood and how to use it in real PostgreSQL deployments, as well as direct integration guides are coming soon in follow up blog posts and documentation articles.

### We’d love your feedback

If you’re experimenting with PostgreSQL 18 or exploring modern authentication options, give the [OIDC validator library](https://github.com/Percona-Lab/pg_oidc_validator/releases/tag/latest) a try and [let us know what you think](https://github.com/Percona-Lab/pg_oidc_validator/discussions)!
Your input will help us make this capability more robust, portable, and enterprise-ready while keeping it open source and accessible to everyone.
