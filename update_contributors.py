#!/usr/bin/env python3
import os
import sys
import frontmatter
import yaml
from collections import defaultdict

BLOG_DIR = "content/blog"
EVENTS_DIR = "content/events"
PODCASTS_DIR = "content/podcasts"
CONTRIB_DIR = "content/contributors"

PRIMARY_FIELDS = [
    "title", "name", "name_pronunciation", "fullname", "fullname_pronounciation",
    "job", "country", "tagline", "social", "images"
]

# Aggregates
all_categories = set()
author_contributor_tags = defaultdict(set)   # categories + matching event/podcast tags
author_events_tags = defaultdict(set)        # unique event/podcast tags not in categories
author_blog_tags = defaultdict(set)          # all tags from posts
author_posts_count = defaultdict(int)
author_talks_count = defaultdict(int)        
author_contributor_types = defaultdict(set)

def load_md(path):
    try:
        return frontmatter.load(path)
    except Exception as e:
        print(f"WARN: Failed to load {path}: {e}", file=sys.stderr)
        return None

def dump_contributor(contrib, path, auto_fields):
    """Save YAML with preserved order and comment for auto-generated fields"""
    lines = ["---"]
    # primary fields first
    for key in PRIMARY_FIELDS:
        if key in contrib:
            val = contrib[key]
            snippet = yaml.dump({key: val}, allow_unicode=True, sort_keys=False).strip()
            lines.append(snippet)
    # comment in English
    lines.append("# Auto-generated fields below. Do not edit manually.")
    # auto fields
    for key, val in auto_fields.items():
        snippet = yaml.dump({key: val}, allow_unicode=True, sort_keys=False).strip()
        lines.append(snippet)
    lines.append("---")
    if contrib.content:
        lines.append(contrib.content.strip())
    with open(path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))

# Step 1: blog posts → author
for root, _, files in os.walk(BLOG_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        post = load_md(os.path.join(root, fname))
        if not post:
            continue
        categories = post.get("categories", []) or []
        tags = post.get("tags", []) or []
        authors = post.get("authors", []) or []
        for c in categories:
            if isinstance(c, str) and c.strip():
                all_categories.add(c.strip())
        for a in authors:
            if not isinstance(a, str) or not a.strip():
                continue
            author = a.strip()
            for c in categories:
                if isinstance(c, str) and c.strip():
                    author_contributor_tags[author].add(c.strip())
            for t in tags:
                if isinstance(t, str) and t.strip():
                    author_blog_tags[author].add(t.strip())
            author_posts_count[author] += 1
            author_contributor_types[author].add("author")

# Step 2: events → speaker
for root, _, files in os.walk(EVENTS_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        event = load_md(os.path.join(root, fname))
        if not event:
            continue
        speakers = event.get("speakers", []) or []
        event_tags = event.get("tags", []) or []
        ev_tags = [t.strip() for t in event_tags if isinstance(t, str) and t.strip()]
        for s in speakers:
            if not isinstance(s, str) or not s.strip():
                continue
            speaker = s.strip()
            author_talks_count[speaker] += 1
            author_contributor_types[speaker].add("speaker")
            for tag in ev_tags:
                if tag in all_categories:
                    author_contributor_tags[speaker].add(tag)
                else:
                    author_events_tags[speaker].add(tag)

# Step 3: podcasts → считаем как speaker (talks)
for fname in os.listdir(PODCASTS_DIR):
    if not fname.endswith(".md"):
        continue
    podcast = load_md(os.path.join(PODCASTS_DIR, fname))
    if not podcast:
        continue
    speakers = podcast.get("speakers", []) or []
    podcast_tags = podcast.get("tags", []) or []
    p_tags = [t.strip() for t in podcast_tags if isinstance(t, str) and t.strip()]
    for s in speakers:
        if not isinstance(s, str) or not s.strip():
            continue
        speaker = s.strip()
        # подкасты считаем как мероприятия
        author_talks_count[speaker] += 1
        author_contributor_types[speaker].add("speaker")
        for tag in p_tags:
            if tag in all_categories:
                author_contributor_tags[speaker].add(tag)
            else:
                author_events_tags[speaker].add(tag)

# Step 4: overwrite contributors
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

        auto_fields = {
            "contributor_tag": sorted(author_contributor_tags[key]),
            "events_tags": sorted(author_events_tags[key]),
            "blog_tags": sorted(author_blog_tags[key]),
            "posts_count": int(author_posts_count[key]),
            "talks_count": int(author_talks_count[key]),  
            "contributor_type": sorted(author_contributor_types[key]) if author_contributor_types[key] else []
        }

        dump_contributor(contrib, path, auto_fields)
        updated += 1
        print(
            f"Updated {path}: contributor_tag={auto_fields['contributor_tag']}, "
            f"events_tags={auto_fields['events_tags']}, "
            f"blog_tags={auto_fields['blog_tags']}, "
            f"posts={auto_fields['posts_count']}, talks={auto_fields['talks_count']}, "
            f"contributor_type={auto_fields['contributor_type']}"
        )

print(f"Done. Updated {updated} contributor file(s).")
