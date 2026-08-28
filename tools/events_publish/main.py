"""
Sync Conference events from Jira SPEAK → Hugo content/events/.

Only Conferences that have ≥1 publishable Talk (Accepted/Done + Ready/Published).
Does not overwrite hand-written pages unless they have `source: jira`.

Usage (from community/ repo root):
  python tools/events_publish/main.py
  python tools/events_publish/main.py --create
  python tools/events_publish/main.py --create --jira-key SPEAK-2213
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from markdown_utils import process_events  # before jira_events path tweaks
from jira_events import load_events_with_talks, require_env


def run_events_images(repo_root: str, *, only_new: bool = True) -> None:
    script = os.path.join(repo_root, "tools", "events_images", "main.py")
    if not os.path.isfile(script):
        print(f"⚠️ events_images not found: {script}")
        return
    cmd = [sys.executable, script]
    if only_new:
        cmd.append("--only-new")
    print("\n🖼️ Generating event card images...")
    result = subprocess.run(cmd, cwd=repo_root, check=False)
    if result.returncode != 0:
        print(f"⚠️ events_images exited with code {result.returncode}")
    else:
        print("✅ Event images done.")


def run_update_events_filters(repo_root: str) -> None:
    script = os.path.join(repo_root, "tools", "events", "update_events.py")
    if not os.path.isfile(script):
        return
    print("\n🏷️ Normalizing event taxonomies...")
    subprocess.run([sys.executable, script], cwd=repo_root, check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create", action="store_true", help="Write event markdown")
    parser.add_argument("--jira-key", help="Conference or Talk SPEAK key to limit sync")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite even pages without source: jira (dangerous)",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Do not run events_images after create",
    )
    parser.add_argument(
        "--skip-filters",
        action="store_true",
        help="Do not run tools/events/update_events.py after create",
    )
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(_HERE, "..", ".."))
    os.chdir(repo_root)

    require_env()
    print("🔄 Starting Jira → Hugo sync for events...")
    print(f"📁 Working directory: {repo_root}")

    events = load_events_with_talks(jira_key=args.jira_key)
    print("-" * 50)
    print(f"Events to process: {len(events)}")
    for ev in events:
        print(
            f"  - {ev.get('key')}: {ev.get('title')!r} "
            f"talks={len(ev.get('talks') or [])} "
            f"sponsored={ev.get('sponsored')} {ev.get('attendance')}"
        )
    print("-" * 50)

    if not events:
        print("Nothing to sync.")
        return

    process_events(events, write=args.create, force=args.force)

    if not args.create:
        print("\nDry-run only. Re-run with --create to write event pages.")
        return

    if not args.skip_images:
        run_events_images(repo_root, only_new=True)
    if not args.skip_filters:
        run_update_events_filters(repo_root)

    print("\n🎉 Event sync completed.")


if __name__ == "__main__":
    main()
