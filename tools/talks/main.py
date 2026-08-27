"""
Sync Talks from Jira SPEAK → Hugo site (percona.community).

Usage (from community/ repo root):
  python tools/talks/main.py                     # dry-run
  python tools/talks/main.py --create            # write MD + Jira URL + contributors
  python tools/talks/main.py --create --jira-key SPEAK-2223

Then (optional images):
  python tools/talks_images/main.py --only-new
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

# Allow imports when run as `python tools/talks/main.py` from repo root
_TOOLS_TALKS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_TALKS not in sys.path:
    sys.path.insert(0, _TOOLS_TALKS)

from jira_utils import load_talks, require_env
from markdown_utils import process_talks


def run_update_contributors(repo_root: str) -> None:
    """Recount posts/events/talks on contributor cards after talks sync."""
    script = os.path.join(repo_root, "tools", "contributors", "update_contributors.py")
    if not os.path.isfile(script):
        print(f"⚠️ Contributors updater not found: {script}")
        return
    print("\n👥 Updating contributor counts (talks / events / posts)...")
    result = subprocess.run(
        [sys.executable, script],
        cwd=repo_root,
        check=False,
    )
    if result.returncode != 0:
        print(f"⚠️ update_contributors.py exited with code {result.returncode}")
    else:
        print("✅ Contributor cards updated.")


def run_events_publish(repo_root: str, *, jira_key: str | None = None) -> None:
    """Create/update event pages for Conferences linked to synced talks."""
    script = os.path.join(repo_root, "tools", "events_publish", "main.py")
    if not os.path.isfile(script):
        print(f"⚠️ events_publish not found: {script}")
        return
    cmd = [sys.executable, script, "--create"]
    if jira_key:
        cmd.extend(["--jira-key", jira_key])
    print("\n📅 Syncing event pages from Jira...")
    result = subprocess.run(cmd, cwd=repo_root, check=False)
    if result.returncode != 0:
        print(f"⚠️ events_publish exited with code {result.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--create",
        action="store_true",
        help="Write Markdown files and update Jira Community Website URL",
    )
    parser.add_argument(
        "--jira-key",
        help="Sync a single Talk issue key (e.g. SPEAK-2223)",
    )
    parser.add_argument(
        "--skip-contributors",
        action="store_true",
        help="With --create: do not run tools/contributors/update_contributors.py",
    )
    parser.add_argument(
        "--skip-events",
        action="store_true",
        help="With --create: do not run tools/events_publish (event pages + images)",
    )
    args = parser.parse_args()

    # Hugo paths are relative to community/ repo root
    repo_root = os.path.abspath(os.path.join(_TOOLS_TALKS, "..", ".."))
    os.chdir(repo_root)

    require_env()
    print("🔄 Starting Jira → Hugo sync for talks...")
    print(f"📁 Working directory: {repo_root}")

    talks = load_talks(jira_key=args.jira_key)
    print("-" * 50)
    print(f"Talks to process: {len(talks)}")
    for t in talks:
        print(
            f"  - {t.get('key')}: {t.get('title')[:60]!r} "
            f"status={t.get('status')} pub={t.get('publication_status')} "
            f"event={(t.get('event') or {}).get('name')!r}"
        )
    print("-" * 50)

    if not talks:
        print("Nothing to sync.")
        return

    print("📝 Processing talks..." + ("" if args.create else " (dry-run)"))
    process_talks(talks, write=args.create)

    if not args.create:
        print("\nDry-run only. Re-run with --create to write files and update Jira.")
        print("After --create: events pages, contributors, then optional talk images:")
        print("  python tools/talks_images/main.py --only-new")
        return

    if not args.skip_events:
        # Prefer conference key from first talk when limiting scope
        conf_key = None
        if args.jira_key and talks:
            conf_key = (talks[0].get("event") or {}).get("key") or args.jira_key
        run_events_publish(repo_root, jira_key=conf_key)

    if not args.skip_contributors:
        run_update_contributors(repo_root)

    print("\n🎉 Sync completed.")
    print("Next: python tools/talks_images/main.py --only-new")


if __name__ == "__main__":
    main()
