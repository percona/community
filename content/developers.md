---
title: "Percona Community Search API — developer docs"
description: "OpenAPI, quickstart, and public endpoints for the Percona Community semantic search API. No API key for POST /search."
url: /developers/
---

This page documents the **public search API** used by [percona.community](https://percona.community/) — semantic search over community blog posts, events, talks, contributors, and related pages.

It is **not** a product SDK portal for Percona Server, Operators, or PMM. For product documentation see [docs.percona.com](https://docs.percona.com/).

## Quick links

| Resource | URL |
|----------|-----|
| OpenAPI specification | [https://percona.community/openapi.json](https://percona.community/openapi.json) |
| AI Catalog | [https://percona.community/.well-known/ai-catalog.json](https://percona.community/.well-known/ai-catalog.json) |
| API base | [https://search.percona.community](https://search.percona.community) |
| Health | [https://search.percona.community/health](https://search.percona.community/health) |
| Site search UI | [https://percona.community/search/](https://percona.community/search/) |
| Agent site map (`llms.txt`) | [https://percona.community/llms.txt](https://percona.community/llms.txt) |

## Authentication

**None** for the public endpoints below. Do not send API keys.

Admin surfaces on `search.percona.community` (demo, OpenAPI UI on that host, indexing) may be protected with HTTP Basic Auth. Those are for operators, not for agents or site widgets.

## Endpoints

### `GET /health`

Liveness / readiness for the search service. Used by the site widget.

```bash
curl -sS https://search.percona.community/health
```

### `POST /search`

Semantic (and hybrid) search. Request body is JSON.

| Field | Type | Default | Notes |
|-------|------|---------|--------|
| `query` | string | required | Natural-language query |
| `limit` | int | `20` | Max results |
| `content_type` | string | omit = all | One type or comma-separated: `blog`, `percona_blog`, `event`, `talk`, `contributor` |
| `min_score` | float | server default | Cosine similarity floor |
| `per_type_limit` | bool | `false` | Legacy: up to `limit` per type |

Example:

```bash
curl -sS -X POST https://search.percona.community/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"zero downtime database migration","limit":8,"content_type":"blog,talk"}'
```

Each result includes `url`, `title`, `content_type`, `excerpt`, `score`, and optional `author`, `date`, `tags`, and image URLs. Full schemas live in the [OpenAPI file](https://percona.community/openapi.json).

## CORS

The API allows browser calls from `https://percona.community` (and related origins configured on the server). Server-to-server calls from agents do not need CORS.

## Rate limits

`POST /search` may be rate-limited at the reverse proxy. Prefer modest `limit` values and avoid tight polling loops.

## Widget

The same API powers the on-site widget:

```text
https://search.percona.community/community-search.js
```

See the [search page](https://percona.community/search/) for the interactive UI.

## OpenAPI for tools

Point OpenAPI-aware clients, codegen, or agents at:

```text
https://percona.community/openapi.json
```

The `servers` entry in that file targets `https://search.percona.community`.
