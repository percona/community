#!/usr/bin/env python3
"""Copy Hugo index.md outputs to sibling .md URLs for agent fetchers.

Hugo writes public/path/to/page/index.md. Mintlify/AFDocs-style checks often
request public/path/to/page.md (append .md after stripping a trailing slash).
This script mirrors each index.md to that sibling path.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def flatten(public: Path) -> int:
    copied = 0
    for index_md in public.rglob("index.md"):
        if not index_md.is_file():
            continue
        page_dir = index_md.parent
        if page_dir == public:
            # Root index.md already satisfies /index.md
            continue
        sibling = page_dir.parent / f"{page_dir.name}.md"
        if sibling.resolve() == index_md.resolve():
            continue
        sibling.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(index_md, sibling)
        copied += 1
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--public",
        default="public",
        type=Path,
        help="Hugo public output directory (default: public)",
    )
    args = parser.parse_args()
    public = args.public
    if not public.is_dir():
        print(f"ERROR: {public} is not a directory", file=sys.stderr)
        return 1
    copied = flatten(public)
    print(f"Mirrored {copied} index.md file(s) to sibling .md URLs under {public}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
