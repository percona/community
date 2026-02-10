#!/usr/bin/env python3
"""
Updates event front matter:
1. event_year from date
2. event_tag from tags (tech keywords)
3. event_category based on speakers or content
"""

import os
import sys
import frontmatter
import yaml
import re

EVENTS_DIR = "content/events"

# Словарь соответствия тегов → event_tag
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
    "Meetup": "Community"
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

def dump_event(doc, path):
    lines = ["---"]
    yaml_block = yaml.dump(doc.metadata, allow_unicode=True, sort_keys=False).strip()
    lines.append(yaml_block)
    lines.append("---")
    if doc.content:
        lines.append(doc.content.strip())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

updated = 0

for root, _, files in os.walk(EVENTS_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue

        path = os.path.join(root, fname)
        doc = load_md(path)
        if not doc:
            continue

        meta = doc.metadata
        changed = False

        # 1. event_year from date
        year = extract_year(meta.get("date"))
        if year:
            meta["event_year"] = [year]
            changed = True

        # 2. event_tag from tags
        tags = ensure_list(meta.get("tags"))
        event_tags = set(ensure_list(meta.get("event_tag")))
        for t in tags:
            if t in TECH_TAGS_MAP:
                event_tags.add(TECH_TAGS_MAP[t])
        if event_tags:
            meta["event_tag"] = sorted(event_tags)
            changed = True

        # 3. event_category rules
        speakers = ensure_list(meta.get("speakers"))
        category = []
        if speakers:
            category.append("Speaking")
        content_lower = doc.content.lower() if doc.content else ""
        if "sponsor" in content_lower or "booth" in content_lower:
            category.append("Sponsorship")
        if category:
            meta["event_category"] = sorted(set(category))
            changed = True

        if changed:
            dump_event(doc, path)
            updated += 1
            print(f"Updated {path}")

print(f"Done. Updated {updated} event file(s).")
