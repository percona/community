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

## Content workflows (agents)

### Jira → talks / events

- Rule: `.cursor/rules/jira-talks-events-sync.mdc` — checklist + **fast path**.
- Done means: talk MD, linked **event** page + event card, contributor recount, then **talk** cards (`talks_images --only-new`).
- Preferred: Ready for publication → **one** `python tools/talks/main.py --create` (talks + events + contributor recount) → `python tools/talks_images/main.py --only-new`.
- Few keys: talk sync with `--skip-events --skip-contributors`, then `events_publish` / `update_contributors` **once** each, then talk images.
- Do **not** loop full `--create` per talk.

### Talks / events (manual, no Jira)

Use when there is no SPEAK issue, or the user asks to add content by hand. Example shape: `content/events/prosvita-2026/`, `content/talks/2026/2026-06-22-shift-left-…`.

1. **Speaker** — `content/contributors/<slug>.md` + `assets/contributors/<slug>.*` if missing.
2. **Event** — `content/events/<slug>/index.md` with `speakers`, dates, location/URL. **Do not** set `source: jira` (that marks pages owned by `events_publish`; hand-written pages must stay without it so sync will not overwrite them).
3. **Event images** — promo/photos in `assets/` (often `assets/blog/<YYYY>/<MM>/` or `assets/events/<slug>/`); wire via front matter `images:` and/or body markdown. Optional gradient card: `python tools/events_images/main.py --only-new` when using that pipeline.
4. **Talk** — `content/talks/<YYYY>/<YYYY-MM-DD>-<slug>.md` with `speakers`, `presentation_date`, event fields, abstract in the body. Match nearby talk front matter.
5. **Talk cover card** — always generate with the template script (never paste “I’m speaking” / event promo into `images:` as the cover):

```bash
python tools/talks_images/main.py --only-new
```

   Rule: `.cursor/rules/talks-cards.mdc`. Output: `assets/talks/<YYYY>/<slug>.png` + front matter `images:`.
6. **Inline images** (speaker graphics, photos) — store under `assets/`, embed in the talk/event **body** (`![…](talks/…)` or `blog/…`), not as the generated cover.
7. **Recount** — `python tools/contributors/update_contributors.py` (commit only touched speaker cards if the run dirties everyone).
8. On event pages that list sessions with cards, prefer `grid` / `griditem` shortcodes (see talks-cards rule / ProsvITa event).

### Blog post

- Rule: `.cursor/rules/blog-posts.mdc`.
- Done means: author profile + photo in `assets/contributors/` (if new), **all** post images (cover + inline) in `assets/blog/<YYYY>/<MM>/`, post MD under `content/blog/<YYYY>/`, then **`update_contributors.py`** so `posts_count` / `blog_tags` refresh (commit only that author’s card if the script touches everyone).
- Long human guide: `content/blog/2022/2022-2-15-how-to-publish-blog-post.md`.

### Verify (talks, events, blog)

- Confirm `hugo` / `hugo --minify` builds. Do **not** browser-check the live/local page unless asked.

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
