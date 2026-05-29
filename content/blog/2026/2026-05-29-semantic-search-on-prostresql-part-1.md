---
title: "Building Smart Semantic Search using PostgreSQL and pgvector - Case Study, Part 1: Introduction"
date: "2026-05-29T11:00:00+00:00"
tags: ["PostgreSQL", "pgvector", "search", "embeddings", "ai"]
categories: ['PostgreSQL']
authors:
  - daniil_bazhenov
images:
  - blog/2026/05/search-part-1-cover.png
slug: semantic-search-on-postgresql-part-1
---

Type "zero downtime database migration" into the site's search bar and you'll get articles and talks about database migration with minimal downtime, even if those words aren't in the titles or content. This is **semantic search** on **PostgreSQL** and **[pgvector](https://github.com/pgvector/pgvector)**, without paid embedding APIs or a separate vector database. In this series I'll cover how it works and why I chose this stack.

I'll walk through how and why I built the search for our community site: blog, events, talks, and profiles. The post should help if you want to repeat the approach or need a practical case study on simple components. If you've done something similar, I'd like to hear your feedback.

![Smart Semantic Search using PostgreSQL and pgvector - Introduction](blog/2026/05/search-part-1-intro-kubernetes.png)


## Context: Website, Search, and Task

The Community team has a website on **Hugo**, an open-source static site generator, hosted for free on **GitHub Pages**. The site has articles, events, talks, videos, and more.

> If you're thinking of starting your own, I recommend checking out these examples: [blog.koehntopp.info](https://blog.koehntopp.info/), [openeverest.io](https://openeverest.io/), [perconalive.com](https://perconalive.com/), [oursqlfoundation.org](https://oursqlfoundation.org/)

But a Hugo site is a collection of HTML files without a backend. Search or filters only work via frontend JS or an external service. For a long time our site had no search at all. Then **Kai Wagner** contributed a JS search for the blog that matched exact words ([percona.community/blog](https://percona.community/blog)).

Recently our community lead **Laura Czajkowski** asked for smart AI search on the site. We tried several off-the-shelf products; they were either too expensive or a poor fit. We also want search to cover more than the site itself eventually: videos from other platforms, the forum, our GitHub repos, and maybe documentation later.

I suggested building it ourselves. Modern AI assistants are good enough for a prototype like this. Below I'll explain the stack.

## What We'll Do

The site stays on Hugo and GitHub Pages. The search service runs **separately**; for this architecture that's the sensible option. The goal is simple: the user types a query in plain language and gets a list of semantically relevant links.

Kai's keyword search was a step forward, but it doesn't catch **meaning**. Type "postgresql" and you get pages where the word appears. An article about slow queries or replication may be missing if the wording is different. **Semantic search** works differently: the query and documents become **vectors**, numeric representations of meaning (**embedding**). Similar meaning lands nearby in vector space even when the words differ. A query like "how to speed up slow queries in MySQL" can surface tuning and optimization content without those words in the title.

Why not another engine? **[OpenSearch](https://opensearch.org/)** is a solid open-source option: full-text and vector search, mature ecosystem. I also looked at **[Manticore Search](https://manticoresearch.com/)**. Both work, but **semantics** still need an embedding pipeline (model at index time and on each query). That's another service to run beside the model.

I wanted my own stack on **Postgres** with pgvector: a practical experiment, not a hunt for the perfect search product. **PostgreSQL with [pgvector](https://github.com/pgvector/pgvector)** keeps page metadata, chunks, vectors, and query history in one database. **[Percona Distribution for PostgreSQL 18](https://docs.percona.com/postgresql/18/index.html)** ships pgvector in the distribution; run `CREATE EXTENSION vector` and you're set.

The plan has four parts:

1. **Widget** on the site: search field and results (plain JS; Hugo unchanged).
2. **API**: takes the query, embeds it with the same model as indexing, searches the DB, returns JSON links.
3. **Indexer**: background worker that reads RSS/HTML, chunks text, embeds, writes to the DB.
4. **PostgreSQL + pgvector**: one database for metadata, chunks, vectors, and search history.

Hugo stays static; the smart parts live in a separate service. No separate vector DB, no paid embedding API, no RAG chat, only links.

The diagram shows two flows: **search** (user query) and **indexing** (refresh the DB on demand or on a schedule). Top to bottom, from the user:

```mermaid
flowchart TB
    User(["👤 User"])

    Widget["🔍 JS widget<br/>percona.community · GitHub Pages"]

    API["⚡ FastAPI<br/>search.percona.community"]

    Model["🧠 Embedding model<br/>shared · API & indexer"]

    DB[("🗄️ PostgreSQL + pgvector")]

    Content["📰 Content<br/>blog · events · talks"]

    Indexer["📥 Indexer worker"]

    User -->|"① query"| Widget
    Widget -->|"② POST /search"| API
    API <-->|embed query| Model
    API <-->|"③ vector search"| DB
    API -->|"④ results"| Widget
    Widget --> User

    Content -->|"A. RSS + HTML"| Indexer
    Indexer <-->|embed chunks| Model
    Indexer -->|"B. chunks + vectors"| DB

    style User fill:#e1f5ff
    style Widget fill:#fff4e6
    style Content fill:#fff9e6
    style API fill:#ffe6e6
    style Model fill:#fff0f5
    style Indexer fill:#f0e6ff
    style DB fill:#e6ffe6
```

The diagram shows the shared **embedding model**; worth stating explicitly anyway. **The indexer and the API must use the same model.** Query vectors and stored vectors must share one space or search is meaningless. Don't mix Nomic at index time with OpenAI at query time, for example. The widget only sends text; it doesn't know which model runs behind the API.

On paper it looked simple. In practice I changed the database schema **three times** and tuned ranking so blog posts didn't crowd out events and talks. The **similarity threshold** mattered more than I expected: one parameter, large swing in results. Still, within a few days we had a working beta on the live site. Here's what shipped.

## The Result (Spoiler)

It took about **three unhurried days** and roughly **$20 in Cursor tokens** to build, debug, and deploy. Try it on **[percona.community](https://percona.community)** (search icon in the header) or **[percona.community/search/](https://percona.community/search/)**.

The index currently covers the site: blog, events, talks, member profiles. Video from other platforms, the forum, and GitHub are planned; the design should allow new sources without replacing the stack.

This is **beta**: the content is public and search isn't business-critical, but I watch stability and security.

### Website Widget

The header has a search icon. Click it to get an input field and a popup with results, **similarity score** (0 to 1, how close the hit is in meaning), and API latency. The site stays static; the widget calls `search.percona.community` and renders JSON. "All results" opens `/search/`.

Try it on [percona.community](https://percona.community), e.g. `slow queries mysql tuning` or `kubernetes operator database`. Comments welcome if something feels off.

![Smart Semantic Search using PostgreSQL and pgvector - Widget](blog/2026/05/search-part-1-intro-pz-talks.png)


### Full Results Page

A separate `/search/` page with filters by content type, cards, and links.


![Smart Semantic Search using PostgreSQL and pgvector - Search Page](blog/2026/05/search-part-1-intro-page.png)

[Example](https://percona.community/search/?q=Postgres+backup+solutions&type=blog)

### API

**FastAPI** at `https://search.percona.community`: embed the query, search Postgres, return JSON with links, scores, and timings (model vs database).

The service runs on **AWS EC2** in Docker Compose: API, indexer, Postgres.

### Demo Dashboard

The Cursor AI agent handled a lot of the boilerplate, so I also built a **dev dashboard** (`/demo`) to test search, run indexing, inspect history, and browse indexed chunks. Not for production, but it saved debugging time.

Demo Dashboard
![Smart Semantic Search using PostgreSQL and pgvector - Demo Dashboard Search](blog/2026/05/search-part-1-intro-demo-search.png)

Search history: making search better

![Smart Semantic Search using PostgreSQL and pgvector - Demo Dashboard Search history](blog/2026/05/search-part-1-intro-demo-history.png)

Indexing status, to see when search data was last updated

![Smart Semantic Search using PostgreSQL and pgvector - Demo Dashboard Indexing status](blog/2026/05/search-part-1-intro-demo-status.png)

Indexed documents with the ability to view data and chunks.

![Smart Semantic Search using PostgreSQL and pgvector - Demo Dashboard Indexed documents](blog/2026/05/search-part-1-intro-demo-pages.png)

### What I Used

Briefly, **why** this stack (deeper comparison in **part two**):

- **[PostgreSQL](https://www.postgresql.org/)** + **[pgvector](https://github.com/pgvector/pgvector)**: vectors and metadata in one DB. Cosine similarity plus an HNSW index is enough at community scale. ([pgvector in Percona docs](https://docs.percona.com/postgresql/18/enable-extensions.html#pgvector))

- **[Percona Distribution for PostgreSQL 18](https://docs.percona.com/postgresql/18/index.html)**: Postgres with pgvector and a Docker image. Vanilla Postgres works too if you install the extension; I used Percona to try "their" Postgres + pgvector in a real deploy.

- **[Python](https://www.python.org/)** + **[FastAPI](https://fastapi.tiangolo.com/)**: fast API setup, OpenAPI included, good libraries for crawl/embed/Postgres.

- **[nomic-embed-text-v1](https://huggingface.co/nomic-ai/nomic-embed-text-v1)** + **[sentence-transformers](https://www.sbert.net/)**: open model, 768 dims, CPU-friendly, no per-chunk API bill. Index and query must use the **same** model; Nomic fits. I'll compare others later.

- **[Hugo](https://gohugo.io/)** + **JavaScript**: thin widget on existing static site.

- **[Docker](https://www.docker.com/)** / **Docker Compose**: same layout locally and on EC2.

- **[AWS EC2](https://aws.amazon.com/ec2/)** + **nginx**: HTTPS on `search.percona.community`, CORS for GitHub Pages.

- **[Cursor](https://cursor.com/)**: main dev tool; its AI agent helped with boilerplate, wiring API to the demo, and Docker fixes. I still reviewed everything. Without it, the same work would have taken weeks.


### How long did it take?

- **~6 hours** with Cursor to a first prototype: crawl, API, Docker, basic demo;
- **~2 more days** for schema changes, per-type ranking, embed/page widget, search history, dashboard, indexer fixes, EC2 deploy;
- **~$20** in Cursor tokens total.

Without AI I'd have stretched the same work over weeks. With the agent I mostly wrote tasks, checked output, and fixed edges.

### About the code and repository

I'm not publishing the repo yet. The code is tied to **percona.community**: our RSS feeds, content types, Hugo widget, EC2 layout. It's an internal prototype, not a reusable library.

If you wanted a drop-in repo: porting someone else's monolith often takes longer than rebuilding from a clear sketch. Part two will have architecture, schema, and stack notes enough for a Cursor agent (or similar) to rebuild for **your** feeds and UI.

Interested in a **generic open-source** or **search-as-a-service** version? Say so in the comments; I'm weighing whether it's worth a separate project.

### What's Next

Try search on [percona.community](https://percona.community) and comment what you find, especially where semantics beat the old substring search.

Part **two** will go inside: schema (including those three rewrites), chunking, HNSW, per-type result caps, and a local Docker Compose walkthrough.
