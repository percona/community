"""
Write Hugo event pages under content/events/<slug>/index.md from Jira records.
"""

from __future__ import annotations

import os
import re
from typing import Any

import yaml

EVENTS_DIR = "content/events"
PERCONA_EVENTS_PREFIX = "https://percona.community/events/"


def slugify_event(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def event_dir(slug: str) -> str:
    return os.path.join(EVENTS_DIR, slug)


def event_index_path(slug: str) -> str:
    return os.path.join(event_dir(slug), "index.md")


def public_url(slug: str) -> str:
    return f"{PERCONA_EVENTS_PREFIX}{slug}/"


def read_existing_marker(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[4:end]) or {}
    except Exception:
        return {}


def can_write_event(path: str, *, force: bool = False) -> bool:
    """Only create new pages, or update pages marked source: jira."""
    if force:
        return True
    if not os.path.exists(path):
        return True
    fm = read_existing_marker(path)
    return str(fm.get("source") or "").strip().casefold() == "jira"


def build_description(event: dict[str, Any]) -> str:
    bits = [event.get("title") or "Event"]
    if event.get("date_display"):
        bits.append(event["date_display"])
    if event.get("location"):
        bits.append(event["location"])
    n = len(event.get("talks") or [])
    if n:
        bits.append(f"{n} talk{'s' if n != 1 else ''} from Percona")
    return " · ".join(bits)


def build_tags(event: dict[str, Any]) -> list[str]:
    tags = ["Event", "opensource"]
    if event.get("sponsored"):
        tags.append("sponsorship")
    if event.get("talks"):
        tags.append("speaking")
    for t in event.get("technology") or []:
        if t and t not in tags:
            tags.append(t)
    return tags


def build_categories(event: dict[str, Any]) -> list[str]:
    cats: list[str] = []
    if event.get("talks"):
        cats.append("Speaking")
    if event.get("sponsored"):
        cats.append("Sponsorship")
    return cats or ["Speaking"]


def build_event_tags(event: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    att = event.get("attendance") or ""
    if att:
        tags.append(att)
    # Map common tech into filter tags (same spirit as update_events.py)
    tech_map = {
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mysql": "MySQL",
        "mariadb": "MySQL",
        "mongodb": "MongoDB",
        "valkey": "Valkey",
        "kubernetes": "Cloud Native",
        "k8s": "Cloud Native",
        "cloud native": "Cloud Native",
    }
    for t in event.get("technology") or []:
        mapped = tech_map.get(str(t).casefold())
        if mapped and mapped not in tags:
            tags.append(mapped)
    return tags


def build_body(event: dict[str, Any]) -> str:
    title = event.get("title") or "Event"
    lines: list[str] = []

    when = event.get("date_display") or ""
    where = event.get("location") or ""
    conf_url = event.get("conf_url") or ""

    intro_bits = [f"**{title}**"]
    if when:
        intro_bits.append(f"takes place **{when}**")
    if where:
        intro_bits.append(f"in **{where}**")
    lines.append(" ".join(intro_bits) + ".")
    lines.append("")

    if conf_url:
        lines.append(f"Conference site: [{conf_url}]({conf_url})")
        lines.append("")

    badges: list[str] = []
    if event.get("sponsored"):
        badges.append("**Sponsoring**")
    if event.get("talks"):
        badges.append("**Speaking**")
    if badges:
        lines.append("Percona presence: " + " · ".join(badges) + ".")
        lines.append("")

    # Talks list is rendered by layouts/events/single.html (related-talks partial).

    lines.append(
        "Follow [Percona Community](https://percona.community/) for more open source "
        "database talks and events."
    )
    lines.append("")
    return "\n".join(lines)


def build_markdown(event: dict[str, Any], *, image_rel: str | None = None) -> str:
    year = event.get("year") or ""
    tags = build_tags(event)
    categories = build_categories(event)
    event_tags = build_event_tags(event)
    speakers = event.get("speakers") or []

    fm: dict[str, Any] = {
        "title": event.get("title"),
        "description": build_description(event),
        "layout": "single",
        "source": "jira",
        "jira": event.get("key"),
        "date": event.get("date_start") or "",
        "event_date_end": event.get("date_end") or "",
        "event_url": event.get("conf_url") or "",
        "event_location": event.get("location") or "",
        "speakers": speakers,
        "tags": tags,
        "events_year": [year] if year and year.isdigit() else [],
        "events_category": categories,
        "events_tag": event_tags,
    }
    if image_rel:
        fm["images"] = [image_rel]
    else:
        # Preserve later by caller; empty list omitted
        pass

    # Keep field order readable
    ordered_keys = [
        "title",
        "description",
        "images",
        "layout",
        "source",
        "jira",
        "speakers",
        "date",
        "event_date_end",
        "event_url",
        "event_location",
        "tags",
        "events_year",
        "events_category",
        "events_tag",
    ]
    ordered = {k: fm[k] for k in ordered_keys if k in fm and fm[k] not in (None, [], "")}
    # always keep empty speakers as list
    if "speakers" not in ordered:
        ordered["speakers"] = speakers

    fm_str = yaml.dump(ordered, sort_keys=False, allow_unicode=True, width=1000).strip()
    body = build_body(event)
    return f"---\n{fm_str}\n---\n\n{body}"


def preserve_images(markdown: str, existing_path: str) -> str:
    if not os.path.exists(existing_path):
        return markdown
    old = read_existing_marker(existing_path)
    images = old.get("images")
    if not images:
        return markdown
    if not markdown.startswith("---"):
        return markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return markdown
    fm = yaml.safe_load(markdown[4:end]) or {}
    if fm.get("images"):
        return markdown
    fm["images"] = images
    body = markdown[end + 5 :]
    fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True, width=1000).strip()
    return f"---\n{fm_str}\n---\n{body}"


def process_events(
    events: list[dict[str, Any]],
    *,
    write: bool = True,
    force: bool = False,
) -> dict[str, Any]:
    created = 0
    updated = 0
    skipped = 0
    planned: list[dict[str, Any]] = []

    for event in events:
        slug = event.get("slug") or slugify_event(event.get("title") or "event")
        path = event_index_path(slug)
        url = public_url(slug)
        md = build_markdown(event)
        exists = os.path.exists(path)
        writable = can_write_event(path, force=force)

        planned.append(
            {
                "key": event.get("key"),
                "title": event.get("title"),
                "path": path,
                "url": url,
                "talks": len(event.get("talks") or []),
                "exists": exists,
                "writable": writable,
            }
        )

        print(f"✅ {event.get('title')} [{event.get('key')}]")
        print(f"   → {path}")
        print(f"   → {url}  talks={len(event.get('talks') or [])}")

        if not write:
            continue

        if not writable:
            print(f"⏭️ Skip (manual page, no source: jira): {path}")
            skipped += 1
            continue

        md = preserve_images(md, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Saved: {path}")
        if exists:
            updated += 1
        else:
            created += 1

    print("\n" + "=" * 60)
    print("📊 EVENTS SUMMARY" + (" (dry-run)" if not write else ""))
    print("=" * 60)
    print(f"Events:   {len(events)}")
    print(f"Created:  {created}")
    print(f"Updated:  {updated}")
    print(f"Skipped:  {skipped}")
    print("=" * 60)

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "planned": planned,
    }
