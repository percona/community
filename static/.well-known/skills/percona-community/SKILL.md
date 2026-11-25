---
name: percona-community
description: Use the Percona Community site and public Community Search API to find events, talks, blog posts, and contributors. Prefer search and llms.txt over scraping HTML.
---

# Percona Community

## When to use this skill

- Finding community blog posts, talks, events, or speakers on https://percona.community/
- Calling the public semantic search API at https://search.percona.community
- Editing the Hugo site in https://github.com/percona/community (read AGENTS.md first)

Do not use this skill for Percona product documentation, Operators, PMM, or Server APIs — use https://docs.percona.com/.

## Preferred discovery order

1. Read https://percona.community/llms.txt
2. Prefer markdown mirrors (`…/page.md` or `…/page/index.md`) over HTML
3. Search with `POST https://search.percona.community/search` (no API key)
4. Fall back to https://percona.community/sitemap.xml only when you need a full inventory

## Search API

```bash
curl -sS -X POST https://search.percona.community/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"postgresql backup restore","limit":8,"content_type":"blog,talk"}'
```

- OpenAPI: https://percona.community/openapi.json
- Human docs: https://percona.community/developers.md
- Health: https://search.percona.community/health

Do not send API keys. Do not use admin/indexing endpoints on that host.

## Site editing (repo agents)

- Content lives under `content/`
- Agent guide: https://github.com/percona/community/blob/main/AGENTS.md
- Do not invent MCP servers, OAuth, or product APIs in this repo unless explicitly asked
- Do not force-push `main`

## Constraints

- This site is community content, not a SaaS control plane
- `llms.txt` is curated on purpose; it will not list every sitemap URL
- GitHub Pages hosting does not negotiate `Accept: text/markdown`; use `.md` URLs instead
