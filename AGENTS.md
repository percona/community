# AGENTS.md — Percona Community site

Guidance for AI coding agents working in [percona/community](https://github.com/percona/community) (Hugo site for https://percona.community/).

## What this repo is

- Static **Hugo** community site: events, talks, speakers, blog, knowledge base, contributors.
- **Not** product documentation for Percona Server / Operators / PMM — that lives at https://docs.percona.com/.
- Public **semantic search API** is separate (`https://search.percona.community`). This repo documents it and hosts OpenAPI; it does not run the API.

## When to use this repo

- Add or edit community content (markdown under `content/`).
- Fix layouts, SCSS, hub pages, or agent-facing static files (`llms.txt`, `openapi.json`, `robots.txt`).
- Do **not** invent product APIs, OAuth, or MCP servers here unless explicitly asked.

## High-value paths

| Path | Purpose |
|------|---------|
| `content/` | Site content (blog, talks, events, …) |
| `layouts/` | Hugo templates |
| `assets/scss/` | Styles (brand tokens in `common/_variables.scss`) |
| `static/llms.txt` | Agent site map |
| `static/openapi.json` | OpenAPI for Community Search |
| `static/.well-known/ai-catalog.json` | ARD / AI Catalog entries |
| `content/developers.md` | Search API human docs (`/developers/`) |
| `.cursor/rules/` | Project conventions (tone, brand, hubs) |

## Conventions

- Prefer minimal diffs; match existing partials and SCSS.
- Community tone: engineer-to-engineer, not marketing. See `.cursor/rules/` and `.cursor/skills/` when present.
- Brand colors via SCSS tokens — primary purple `#653DF4`.
- Do not commit secrets. Do not force-push `main`.
- Talk card images are generated separately (`python tools/talks_images/main.py --only-new`) after talk markdown is added.

## Search API (read-only from this repo)

- Spec: https://percona.community/openapi.json
- Docs: https://percona.community/developers/
- Runtime: `POST https://search.percona.community/search` (no API key)
- Keep OpenAPI and `/developers/` in sync when documenting public endpoints.

## Local build

```bash
hugo server
# or
hugo --minify
```

Production deploys from `main` via GitHub Pages.
