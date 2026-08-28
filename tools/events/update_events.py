#!/usr/bin/env python3
"""
Updates event front matter (Jira-synced pages only):
1. events_year from date
2. events_tag from tags (tech keywords)
3. events_category based on speakers or content
4. normalize tags, events_year, events_tag, events_category to ["A","B"] format

Only touches pages with `source: jira`. Skips podcasts and hand-written events.
Only rewrites when taxonomy values actually change (avoids YAML reflow noise).
"""

from __future__ import annotations

import os
import re
import sys

import frontmatter
import yaml

EVENTS_DIR = "content/events"

# Hand-curated trees — do not rewrite front matter style here.
SKIP_DIR_NAMES = {"podcasts"}

TECH_TAGS_MAP = {
    "PostgreSQL": "PostgreSQL",
    "Postgres": "PostgreSQL",
    "PG": "PostgreSQL",
    "MySQL": "MySQL",
    "MariaDB": "MySQL",
    "ProxySQL": "MySQL",
    "Percona Server": "MySQL",
    "Percona Server for MySQL": "MySQL",
    "Percona XtraDB Cluster": "MySQL",
    "MongoDB": "MongoDB",
    "Mongo": "MongoDB",
    "Valkey": "Valkey",
    "Cloud": "Cloud Native",
    "CNCF": "Cloud Native",
    "Kubernetes": "Cloud Native",
    "K8s": "Cloud Native",
    "ArgoCD": "Cloud Native",
    "Docker": "Cloud Native",
    "Containers": "Cloud Native",
    "Percona Everest": "Cloud Native",
    "Minikube": "Cloud Native",
    "Podman": "Cloud Native",
    "Terraform": "Cloud Native",
    "Prometheus": "Cloud Native",
    "Operator": "Cloud Native",
    "Operators": "Cloud Native",
    "Opensource": "Opensource",
    "Open-Source": "Opensource",
    "Community": "Community",
    "Podcast": "Community",
    "Meetup": "Community",
}


def load_md(path):
    try:
        return frontmatter.load(path)
    except Exception as e:
        print(f"WARN: Failed to load {path}: {e}", file=sys.stderr)
        return None


def extract_year(val):
    if not val:
        return None
    s = str(val)
    m = re.search(r"\b(19|20)\d{2}\b", s)
    return m.group(0) if m else None


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v not in (None, "", [])]
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    return [value]


def format_list_field(name, values):
    """Return name: ["A", "B"]"""
    arr = ", ".join(f'"{v}"' for v in values)
    return f"{name}: [{arr}]"


def dump_event(doc, path):
    meta = dict(doc.metadata)

    meta_copy = {
        k: v
        for k, v in meta.items()
        if k not in ["tags", "events_year", "events_tag", "events_category"]
    }
    yaml_block = yaml.dump(
        meta_copy,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).strip()

    parts = ["---", yaml_block]
    for field in ["tags", "events_year", "events_tag", "events_category"]:
        if field in meta and isinstance(meta[field], list):
            parts.append(format_list_field(field, meta[field]))
    parts.append("---")
    text = "\n".join(parts) + "\n"
    if doc.content:
        text += doc.content.rstrip() + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def lists_equal(a, b) -> bool:
    return [str(x) for x in ensure_list(a)] == [str(x) for x in ensure_list(b)]


updated = 0
skipped_dirs = 0

for root, dirs, files in os.walk(EVENTS_DIR):
    # prune podcasts (and similar) so we never reflow their FM
    dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
    rel_root = os.path.relpath(root, EVENTS_DIR)
    if rel_root != "." and rel_root.split(os.sep)[0] in SKIP_DIR_NAMES:
        skipped_dirs += 1
        continue

    for fname in files:
        if not fname.endswith(".md"):
            continue

        path = os.path.join(root, fname)
        doc = load_md(path)
        if not doc:
            continue

        meta = doc.metadata
        # Never reflow hand-curated / legacy event pages (Percona Live rooms, etc.)
        if str(meta.get("source") or "").strip().lower() != "jira":
            continue

        before = {
            "tags": list(ensure_list(meta.get("tags"))),
            "events_year": list(ensure_list(meta.get("events_year"))),
            "events_tag": list(ensure_list(meta.get("events_tag"))),
            "events_category": list(ensure_list(meta.get("events_category"))),
        }

        # 1. events_year from date
        year = extract_year(meta.get("date"))
        if year:
            meta["events_year"] = [year]

        # 2. events_tag from tags
        tags = ensure_list(meta.get("tags"))
        events_tags = set(ensure_list(meta.get("events_tag")))
        for t in tags:
            if t in TECH_TAGS_MAP:
                events_tags.add(TECH_TAGS_MAP[t])
        if events_tags:
            meta["events_tag"] = sorted(events_tags)

        # 3. events_category rules
        speakers = ensure_list(meta.get("speakers"))
        category = list(ensure_list(meta.get("events_category")))
        if speakers and "Speaking" not in category:
            category.append("Speaking")
        content_lower = doc.content.lower() if doc.content else ""
        if ("sponsor" in content_lower or "booth" in content_lower) and "Sponsorship" not in category:
            category.append("Sponsorship")
        if category:
            meta["events_category"] = sorted(set(category))

        # 4. normalize tags (stable order only if present)
        if tags:
            meta["tags"] = sorted(set(str(t) for t in tags))

        after = {
            "tags": list(ensure_list(meta.get("tags"))),
            "events_year": list(ensure_list(meta.get("events_year"))),
            "events_tag": list(ensure_list(meta.get("events_tag"))),
            "events_category": list(ensure_list(meta.get("events_category"))),
        }

        if all(lists_equal(before[k], after[k]) for k in before):
            continue

        dump_event(doc, path)
        updated += 1
        print(f"Updated {path}")

print(f"Done. Updated {updated} event file(s).")
