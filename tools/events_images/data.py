"""Load auto-generated (source: jira) event pages for card image generation."""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass

import frontmatter
import yaml

from generator import EventCard, generate_event_image

EVENTS_DIR = "content/events"
ASSETS_DIR = "assets"


@dataclass
class EventPage:
    card: EventCard


def load_auto_events(min_year: int | None = None) -> list[EventCard]:
    files = glob.glob(f"{EVENTS_DIR}/**/index.md", recursive=True)
    out: list[EventCard] = []
    for md_path in files:
        try:
            post = frontmatter.load(md_path)
        except Exception:
            continue
        if str(post.get("source") or "").casefold() != "jira":
            continue
        slug = os.path.basename(os.path.dirname(md_path))
        years = post.get("events_year") or []
        year = str(years[0]) if years else (post.get("date") or "")[:4]
        if min_year and year.isdigit() and int(year) < min_year:
            continue
        cats = post.get("events_category") or []
        cats_l = [str(c).casefold() for c in cats]
        date = str(post.get("date") or "")
        end = str(post.get("event_date_end") or "")
        if date and end and date != end:
            date_display = f"{date} – {end}"
        else:
            date_display = date
        out.append(
            EventCard(
                title=str(post.get("title") or slug),
                date_display=date_display,
                location=str(post.get("event_location") or ""),
                year=year or "undated",
                slug=slug,
                md_path=md_path,
                sponsored="sponsorship" in cats_l,
                speaking="speaking" in cats_l or bool(post.get("speakers")),
            )
        )
    return out


def event_image_exists(event: EventCard) -> bool:
    return os.path.isfile(os.path.join(ASSETS_DIR, "events", event.slug, "card.png"))


def update_front_matter(md_path: str, image_path: str) -> None:
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    assert content.startswith("---")
    _, fm_text, body = content.split("---", 2)
    data = yaml.safe_load(fm_text) or {}
    images = data.get("images") or []
    if isinstance(images, str):
        images = [images]
    if image_path not in images:
        images.insert(0, image_path)
    data["images"] = images
    new_fm = yaml.dump(data, sort_keys=False, allow_unicode=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"---\n{new_fm}---\n{body.lstrip(chr(10))}")


def process_event_images(*, only_new: bool = True, min_year: int | None = None) -> int:
    events = load_auto_events(min_year=min_year)
    if only_new:
        events = [e for e in events if not event_image_exists(e)]
    print(f"Found {len(events)} event(s) for image generation")
    n = 0
    for event in events:
        rel = generate_event_image(event)
        if not rel:
            continue
        update_front_matter(event.md_path, rel)
        print(f"Generated: {rel} for {event.md_path}")
        n += 1
    return n
