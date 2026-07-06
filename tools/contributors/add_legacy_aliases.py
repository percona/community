#!/usr/bin/env python3
"""
Add Hugo aliases so old /authors/{slug}/ and /speakers/{slug}/ URLs redirect to
/content/contributors/ pages after the authors+speakers merge (PR #1059).
"""

import os
import subprocess
import sys

import frontmatter

CONTRIB_DIR = "content/contributors"
MERGE_PARENT = "cfb2c63e9^"

# Old git slug -> contributor filename when slug/filename no longer match
SLUG_TO_FILE = {
    "vicențiu_ciorbaru": "vicentiu_ciorbaru.md",
    "aleksandra_abramova": "aleks_abramova.md",
    "dmitry_kostiuk": "dmitriy_kostiuk.md",
    "fernando_laudares": "fernando_laudares_camargos.md",
    "takis_stathopoulos": "takis_panagiotis_stathopoulos.md",
}


def old_slugs(section: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "ls-tree", "-z", "--name-only", f"{MERGE_PARENT}:content/{section}"],
        text=True,
    )
    return [
        entry.replace("/index.md", "").replace(".md", "")
        for entry in out.split("\0")
        if entry and entry != "_index.md"
    ]


def resolve_contributor_file(slug: str, contrib_files: set[str], contrib_by_name: dict[str, str]) -> str | None:
    if slug in SLUG_TO_FILE:
        return SLUG_TO_FILE[slug]
    candidate = f"{slug}.md"
    if candidate in contrib_files:
        return candidate
    if slug in contrib_by_name:
        return contrib_by_name[slug]
    return None


def alias_paths(section: str, slug: str) -> list[str]:
    base = f"/{section}/{slug}"
    return [base, f"{base}/"]


def merge_aliases(existing, new_paths: list[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for path in list(existing or []) + new_paths:
        if path not in seen:
            seen.add(path)
            merged.append(path)
    return merged


def main() -> int:
    contrib_files = {
        f for f in os.listdir(CONTRIB_DIR) if f.endswith(".md") and f != "_index.md"
    }
    contrib_by_name: dict[str, str] = {}
    for fname in contrib_files:
        with open(os.path.join(CONTRIB_DIR, fname), encoding="utf-8") as fh:
            post = frontmatter.load(fh)
        name = post.get("name")
        if isinstance(name, str) and name.strip():
            contrib_by_name[name.strip()] = fname

    updates: dict[str, list[str]] = {}
    missing: list[tuple[str, str]] = []

    for section in ("authors", "speakers"):
        for slug in old_slugs(section):
            fname = resolve_contributor_file(slug, contrib_files, contrib_by_name)
            if not fname:
                missing.append((section, slug))
                continue
            updates.setdefault(fname, []).extend(alias_paths(section, slug))

    if missing:
        for section, slug in missing:
            print(f"ERROR: no contributor for /{section}/{slug}/", file=sys.stderr)
        return 1

    changed = 0
    for fname, new_paths in sorted(updates.items()):
        path = os.path.join(CONTRIB_DIR, fname)
        with open(path, encoding="utf-8") as fh:
            post = frontmatter.load(fh)
        merged = merge_aliases(post.get("aliases"), new_paths)
        if merged == (post.get("aliases") or []):
            continue
        post["aliases"] = merged
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(frontmatter.dumps(post))
        changed += 1

    index_path = os.path.join(CONTRIB_DIR, "_index.md")
    with open(index_path, encoding="utf-8") as fh:
        index_post = frontmatter.load(fh)
    index_aliases = merge_aliases(
        index_post.get("aliases"),
        ["/authors", "/authors/", "/speakers", "/speakers/"],
    )
    if index_aliases != (index_post.get("aliases") or []):
        index_post["aliases"] = index_aliases
        with open(index_path, "w", encoding="utf-8") as fh:
            fh.write(frontmatter.dumps(index_post))
        changed += 1

    print(f"Updated aliases on {changed} file(s) ({len(updates)} contributor profiles).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
