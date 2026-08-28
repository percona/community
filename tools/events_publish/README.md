# Jira → Community Events

Create Hugo event pages for SPEAK Conferences that have ≥1 **publishable** Talk
(Accepted/Done + Publication Status Ready/Published).

## Usage

From `community/` root. Uses the same Jira env as `tools/talks`
(`JIRA_URL` / `JIRA_USER` / `JIRA_TOKEN` — see `tools/talks/.env.example`):

```bash
pip install -r tools/events_publish/requirements.txt

# Dry-run
python tools/events_publish/main.py

# Write content/events/<slug>/index.md + card images
python tools/events_publish/main.py --create

# One conference (or a talk under it)
python tools/events_publish/main.py --create --jira-key SPEAK-2213
```

Also runs after `python tools/talks/main.py --create` unless `--skip-events`.

## Page rules

- Front matter includes `source: jira` and `jira: SPEAK-…`
- **Never overwrites** hand-written pages without `source: jira` (use `--force` only if intentional)
- Body: dates, location, conf URL, Speaking/Sponsoring, linked talks + speakers
- Then `tools/events_images` draws a gradient card + Percona Community logo
- Then `tools/events/update_events.py` normalizes taxonomies

## Images

Photo backgrounds can replace gradients later — drop files into
`tools/events_images/templates/` and wire them in `generator.py`.
For now: procedural gradients + `tools/talks_images/templates/logo-white.png`.
