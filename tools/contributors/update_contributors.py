#!/usr/bin/env python3
"""
Aggregates contributor activity from blog posts, events, podcasts, and talks.
Generates auto-fields in contributor cards: counts, tags, types, and activity years.
"""

import os
import sys
import frontmatter
import yaml
import re
from collections import defaultdict

# Paths to content directories
BLOG_DIR = "content/blog"
EVENTS_DIR = "content/events"
PODCASTS_DIR = "content/podcasts"
TALKS_DIR = "content/talks"
CONTRIB_DIR = "content/contributors"

# Fields that define the contributor's core profile (preserved at the top)
PRIMARY_FIELDS = [
    "title", "name", "name_pronunciation", "fullname", "fullname_pronounciation",
    "job", "country", "tagline", "social", "images"
]

# Global sets for aggregating data
all_categories = set()

# Activity counts
contributor_posts_count = defaultdict(int)   # blog posts authored
contributor_events_count = defaultdict(int)  # events + podcasts participated in
contributor_talks_count = defaultdict(int)   # talks given

# Tag collections
contributor_all_tags = defaultdict(set)      # tags matching known categories
contributor_blog_tags = defaultdict(set)     # unique tags from blog posts
contributor_events_tags = defaultdict(set)   # non-category tags from events/podcasts
contributor_talks_tags = defaultdict(set)    # non-category tags from talks

# Role types (author, speaker)
contributor_types = defaultdict(set)         # e.g., "author", "speaker"

# Activity years (e.g., "2025", "2024")
contributor_years = defaultdict(set)


def load_md(path):
    """
    Loads a Markdown file with YAML front matter.
    Returns: frontmatter.Post or None on failure.
    """
    try:
        return frontmatter.load(path)
    except Exception as e:
        print(f"WARN: Failed to load {path}: {e}", file=sys.stderr)
        return None


def extract_year(val) -> str | None:
    """
    Extracts a 4-digit year (19xx, 20xx) from a string.
    Supports formats:
      - ISO: "2025-03-31"
      - RFC 2822: "Thu, 14 Feb 2019 10:21:04 +0000"
      - ISO with timezone: "2024-10-15T14:30:00Z"
    Returns: Year as string (e.g., "2025") or None.
    """
    if not val:
        return None
    val_str = str(val).strip()
    if not val_str:
        return None
    match = re.search(r"\b(19|20)\d{2}\b", val_str)
    return match.group(0) if match else None


def extract_year_from_field(doc: frontmatter.Post, fields: list) -> str | None:
    """
    Extracts the first valid year from a list of fields in the document.
    Uses extract_year() for each field value.
    Returns: Year string or None.
    """
    for field in fields:
        val = doc.get(field)
        year = extract_year(val)
        if year:
            return year
    return None


def dump_contributor(contrib, path, auto_fields):
    """
    Saves the contributor file with:
      - Primary fields (as-is)
      - Auto-generated fields (sorted, with warning comment)
    Preserves content after front matter.
    """
    lines = ["---"]
    # Write primary fields in fixed order
    for key in PRIMARY_FIELDS:
        if key in contrib:
            val = contrib[key]
            snippet = yaml.dump({key: val}, allow_unicode=True, sort_keys=False).strip()
            lines.append(snippet)
    # Add comment for auto-generated fields
    lines.append("# Auto-generated fields. Do not edit manually.")
    # Write auto fields
    for key, val in auto_fields.items():
        snippet = yaml.dump({key: val}, allow_unicode=True, sort_keys=False).strip()
        lines.append(snippet)
    lines.append("---")
    # Preserve content
    if contrib.content:
        lines.append(contrib.content.strip())
    # Write file
    with open(path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))


# ———————————————————————
# 1. Process blog posts
# ———————————————————————
for root, _, files in os.walk(BLOG_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        path = os.path.join(root, fname)
        post = load_md(path)
        if not post:
            continue
        authors = post.get("authors", []) or []
        categories = post.get("categories", []) or []
        tags = post.get("tags", []) or []

        # Extract year: from 'date' field or directory name
        year = extract_year(post.get("date"))
        if not year:
            parts = root.split("/")
            for p in parts:
                if p.isdigit() and len(p) == 4:
                    year = p
                    break

        # Register categories
        for c in categories:
            if isinstance(c, str) and c.strip():
                all_categories.add(c.strip())

        # Aggregate per author
        for a in authors:
            if not isinstance(a, str) or not a.strip():
                continue
            contributor = a.strip()
            # Add category-matching tags
            for c in categories:
                if isinstance(c, str) and c.strip():
                    contributor_all_tags[contributor].add(c.strip())
            # Add blog-specific tags
            for t in tags:
                if isinstance(t, str) and t.strip():
                    contributor_blog_tags[contributor].add(t.strip())
            # Count and classify
            contributor_posts_count[contributor] += 1
            contributor_types[contributor].add("author")
            if year:
                contributor_years[contributor].add(year)


# ———————————————————————
# 2. Process events and podcasts
# ———————————————————————
for source, root_dir in [("events", EVENTS_DIR), ("podcasts", PODCASTS_DIR)]:
    for root, _, files in os.walk(root_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            path = os.path.join(root, fname)
            doc = load_md(path)
            if not doc:
                continue
            speakers = doc.get("speakers", []) or []
            doc_tags = doc.get("tags", []) or []

            # Extract year only from 'date' field
            year = extract_year(doc.get("date"))

            # Aggregate per speaker
            for s in speakers:
                if not isinstance(s, str) or not s.strip():
                    continue
                contributor = s.strip()
                for t in doc_tags:
                    if isinstance(t, str) and t.strip():
                        t_clean = t.strip()
                        if t_clean in all_categories:
                            contributor_all_tags[contributor].add(t_clean)
                        else:
                            contributor_events_tags[contributor].add(t_clean)
                contributor_events_count[contributor] += 1
                contributor_types[contributor].add("speaker")
                if year:
                    contributor_years[contributor].add(year)


# ———————————————————————
# 3. Process talks
# ———————————————————————
for root, _, files in os.walk(TALKS_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        path = os.path.join(root, fname)
        talk = load_md(path)
        if not talk:
            continue
        speakers = talk.get("speakers", []) or []
        talk_tags = talk.get("talk_tags", []) or []

        # Extract year from event_date_start or presentation_date
        year = extract_year_from_field(talk, ["event_date_start", "presentation_date"])

        # Aggregate per speaker
        for s in speakers:
            if not isinstance(s, str) or not s.strip():
                continue
            contributor = s.strip()
            for t in talk_tags:
                if isinstance(t, str) and t.strip():
                    t_clean = t.strip()
                    if t_clean in all_categories:
                        contributor_all_tags[contributor].add(t_clean)
                    else:
                        contributor_talks_tags[contributor].add(t_clean)
            contributor_talks_count[contributor] += 1
            contributor_types[contributor].add("speaker")
            if year:
                contributor_years[contributor].add(year)


# ———————————————————————
# 4. Update contributor cards
# ———————————————————————
updated = 0
for root, _, files in os.walk(CONTRIB_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        path = os.path.join(root, fname)
        contrib = load_md(path)
        if not contrib:
            continue
        name = contrib.get("name")
        if not isinstance(name, str) or not name.strip():
            print(f"WARN: Contributor file missing valid 'name': {path}", file=sys.stderr)
            continue
        key = name.strip()

        # Prepare auto-generated fields
        auto_fields = {
            "contributor_tag": sorted(contributor_all_tags[key]),
            "blog_tags": sorted(contributor_blog_tags[key]),
            "events_tags": sorted(contributor_events_tags[key]),
            "talks_tags": sorted(contributor_talks_tags[key]),
            "posts_count": int(contributor_posts_count[key]),
            "events_count": int(contributor_events_count[key]),
            "talks_count": int(contributor_talks_count[key]),
            "contributor_type": sorted(contributor_types[key]) if contributor_types[key] else [],
            "contributor_year": sorted(contributor_years[key], reverse=True)  # newest first
        }

        # Save updated file
        dump_contributor(contrib, path, auto_fields)
        updated += 1
        print(
            f"Updated {path}: "
            f"posts={auto_fields['posts_count']}, "
            f"events={auto_fields['events_count']}, "
            f"talks={auto_fields['talks_count']}, "
            f"contributor_year={auto_fields['contributor_year']}"
        )

print(f"Done. Updated {updated} contributor file(s).")
