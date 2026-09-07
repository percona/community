# Jira → Community Talks

Sync SPEAK Talks that are ready for the site into Hugo markdown under
`content/talks/`, then optionally generate social images.

## Prerequisites

Run from the **community** repo root. Credentials via env vars
(`tools/talks/.env` is gitignored) or CI secrets:

```
JIRA_URL=https://your-org.atlassian.net
JIRA_USER=you@example.com
JIRA_TOKEN=...
```

See `tools/talks/.env.example`. Never commit real tokens — this repo is public.

```bash
pip install -r tools/talks/requirements.txt
```

## Publication filter

Talks are included when **all** of:

- `issuetype = Talk`
- `status` ∈ `Accepted`, `Done`
- `Publication Status` = `Ready for publication` (after sync → `Published`)

## Usage

```bash
# Dry-run — list matching Talks, no files / no Jira writes
python tools/talks/main.py

# Write markdown + set Community Website URL / Published on Jira
# Then: event pages (gradient cards) + contributor recount
python tools/talks/main.py --create

# Single issue
# One Talk by key (bypasses Ready filter — re-publish / fix)
python tools/talks/main.py --create --jira-key SPEAK-2223

# Skip event pages / contributor recount
python tools/talks/main.py --create --skip-events --skip-contributors
```

## Pipeline after `--create`

1. Hugo talk markdown under `content/talks/`
2. Jira write-back (Community Website URL + Published)
3. **`tools/events_publish`** — Conference pages under `content/events/` when
   the Conference has ≥1 publishable Talk (`source: jira` + gradient card)
4. **`tools/contributors/update_contributors.py`** — recounts `talks_count` /
   `posts_count` / `events_count`, tags, contributor years
5. Optional talk images (manual):

```bash
pip install -r tools/talks_images/requirements.txt
python tools/talks_images/main.py --only-new
```

## Notes

- Event pages: see `tools/events_publish/README.md`. Hand-written events
  (no `source: jira`) are never overwritten.
- On the talk page, the event is title + URL (+ dates/location in front matter)
  from the linked Conference (**Conf & Talk**). **Conference Name** is used only
  when there are several Conf & Talk links (pick the matching one); with a single
  link that Conference is used as-is. Front matter also stores `event_jira`; the
  talk page links to / shows a card for the matching community event page when
  one exists.
- Speakers come from **Speaker & Talk** (fallback: Speakers multi-user field).
  When Speakers (user picker) is set, Jira avatars are downloaded into
  `assets/contributors/` for new cards (and replace `percona.jpeg` placeholders).
- Contributor cards are create-only under `content/contributors/`.
- Front matter `id` / `jira` use the Jira key (e.g. `SPEAK-2223`).

Notion loaders in `notion_utils.py` are unused by this CLI (kept for reference).
