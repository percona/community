"""
Jira Conference → site event records (Conferences with publishable Talks).
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

_TALKS = Path(__file__).resolve().parent.parent / "talks"
# Append (not prepend) so sibling tools/*/markdown_utils.py is not shadowed
if str(_TALKS) not in sys.path:
    sys.path.append(str(_TALKS))

from jira_utils import (  # noqa: E402
    CITY,
    CONF_URL,
    FINISH_DATE,
    PUB_STATUS,
    START_DATE,
    TECHNOLOGY,
    adf_to_text,
    get_issue,
    labels_list,
    load_talks,
    require_env,
    select_value,
    slugify_name,
    time_to_date,
    url_field,
)

OFFLINE = "customfield_11936"
SPONSORSHIP = "customfield_11928"

CONF_FIELDS = [
    "summary",
    "status",
    "issuelinks",
    "labels",
    CONF_URL,
    START_DATE,
    FINISH_DATE,
    CITY,
    TECHNOLOGY,
    OFFLINE,
    SPONSORSHIP,
    PUB_STATUS,
]


def slugify_event(text: str) -> str:
    """ASCII slug: strip accents (México → mexico), collapse non-alnum."""
    norm = unicodedata.normalize("NFKD", text or "")
    ascii_text = "".join(c for c in norm if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def is_sponsored(sponsorship_field: Any) -> bool:
    text = adf_to_text(sponsorship_field).casefold()
    if not text:
        return False
    if re.search(r"\bno\b", text) and not re.search(r"\byes\b", text):
        return False
    if re.search(r"\byes\b", text):
        return True
    return len(text) > 2


def offline_online(field: Any, location: str) -> str:
    val = select_value(field).casefold()
    if "online" in val:
        return "Online"
    if "offline" in val:
        return "In-Person"
    loc = (location or "").casefold()
    if loc in {"online", "virtual", "remote"}:
        return "Online"
    return "In-Person"


def format_date_range(start: str, end: str) -> str:
    if start and end and start != end:
        return f"{start} – {end}"
    return start or end or ""


def index_local_talks(talks_dir: str = "content/talks") -> dict[str, dict[str, Any]]:
    """Map Jira talk key → local Hugo talk metadata."""
    import frontmatter

    out: dict[str, dict[str, Any]] = {}
    if not os.path.isdir(talks_dir):
        return out
    for root, _dirs, files in os.walk(talks_dir):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            try:
                post = frontmatter.load(path)
            except Exception:
                continue
            key = str(post.get("jira") or post.get("id") or "").strip()
            if not key.startswith("SPEAK-"):
                continue
            year = str(post.get("talk_year") or Path(root).name)
            slug = Path(name).stem
            speakers = post.get("speakers") or []
            if isinstance(speakers, str):
                speakers = [speakers]
            out[key] = {
                "path": path,
                "url": f"/talks/{year}/{slug}/",
                "title": post.get("title") or slug,
                "speakers": [str(s).strip() for s in speakers if str(s).strip()],
                "year": year,
                "slug": slug,
            }
    return out


def load_events_with_talks(
    *,
    jira_key: str | None = None,
) -> list[dict[str, Any]]:
    """
    Conferences linked to ≥1 publishable Talk (Accepted/Done + Ready/Published).
    """
    require_env()
    talks = load_talks()
    local = index_local_talks()

    by_conf: dict[str, list[dict[str, Any]]] = {}
    for talk in talks:
        conf_key = str((talk.get("event") or {}).get("key") or "").strip()
        if not conf_key:
            continue
        by_conf.setdefault(conf_key, []).append(talk)

    if jira_key:
        if jira_key in by_conf:
            by_conf = {jira_key: by_conf[jira_key]}
        else:
            # Talk key → its conference
            found = None
            for talk in talks:
                if talk.get("key") == jira_key:
                    found = str((talk.get("event") or {}).get("key") or "")
                    break
            if found and found in by_conf:
                by_conf = {found: by_conf[found]}
            elif jira_key.startswith("SPEAK-"):
                # Direct conference key with no publishable talks yet
                by_conf = {}
            else:
                by_conf = {}

    events: list[dict[str, Any]] = []
    for conf_key, conf_talks in sorted(by_conf.items()):
        try:
            issue = get_issue(conf_key, CONF_FIELDS)
        except Exception as exc:
            print(f"⚠️ Skip conference {conf_key}: {exc}")
            continue
        fields = issue.get("fields") or {}
        name = str(fields.get("summary") or "").strip()
        if not name:
            continue
        start = time_to_date(fields.get(START_DATE))
        end = time_to_date(fields.get(FINISH_DATE))
        city_raw = fields.get(CITY)
        location = (
            city_raw.strip()
            if isinstance(city_raw, str)
            else str(city_raw or "").strip()
        )
        tech = labels_list(fields.get(TECHNOLOGY))
        sponsored = is_sponsored(fields.get(SPONSORSHIP))
        attendance = offline_online(fields.get(OFFLINE), location)
        year = start[:4] if start and start[:4].isdigit() else "undated"
        base = slugify_event(name)
        if year.isdigit():
            base = re.sub(rf"^{year}-?", "", base)
            base = re.sub(rf"-?{year}$", "", base).strip("-")
        slug = f"{year}-{base}" if year != "undated" and base else (base or conf_key.lower())

        site_talks: list[dict[str, Any]] = []
        speaker_slugs: list[str] = []
        for t in conf_talks:
            tkey = str(t.get("key") or "")
            loc = local.get(tkey)
            entry: dict[str, Any] = {
                "key": tkey,
                "title": (loc or {}).get("title") or t.get("title") or tkey,
                "url": (loc or {}).get("url") or "",
                "speakers": [],
            }
            if loc:
                for s in loc.get("speakers") or []:
                    if s == "unknown":
                        continue
                    entry["speakers"].append(
                        {"slug": s, "name": s.replace("_", " ").title(), "url": f"/contributors/{s}/"}
                    )
                    if s not in speaker_slugs:
                        speaker_slugs.append(s)
            else:
                for sp in t.get("speakers") or []:
                    slug_sp = sp.get("slug") or slugify_name(sp.get("Name") or "")
                    if not slug_sp:
                        continue
                    entry["speakers"].append(
                        {
                            "slug": slug_sp,
                            "name": sp.get("Name") or slug_sp,
                            "url": f"/contributors/{slug_sp}/",
                        }
                    )
                    if slug_sp not in speaker_slugs:
                        speaker_slugs.append(slug_sp)
            site_talks.append(entry)

        events.append(
            {
                "key": conf_key,
                "title": name,
                "year": year,
                "slug": slug,
                "date_start": start,
                "date_end": end,
                "date_display": format_date_range(start, end),
                "location": location,
                "conf_url": url_field(fields.get(CONF_URL)),
                "technology": tech,
                "sponsored": sponsored,
                "attendance": attendance,
                "talks": site_talks,
                "speakers": speaker_slugs,
                "publication_status": select_value(fields.get(PUB_STATUS)),
            }
        )

    return events
