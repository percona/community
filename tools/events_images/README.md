# Event card images (Jira-sourced pages)

Generates `assets/events/<slug>/card.png` for Hugo event pages with
`source: jira` in front matter.

Until photo backgrounds are provided, cards use procedural dark gradients
plus the Percona Community white logo (`tools/talks_images/templates/logo-white.png`)
and Speaking / Sponsoring badges.

```bash
pip install -r tools/events_images/requirements.txt

# Only missing cards
python tools/events_images/main.py --only-new

# Regenerate all jira-sourced cards
python tools/events_images/main.py
```

Usually invoked automatically by `tools/events_publish/main.py --create`.
