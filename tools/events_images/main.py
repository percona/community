"""Generate card images for Jira-sourced event pages."""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from data import process_event_images


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only-new",
        action="store_true",
        help="Skip events that already have assets/events/<slug>/card.png",
    )
    parser.add_argument("--min-year", type=int, default=None)
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(_HERE, "..", ".."))
    os.chdir(repo_root)
    process_event_images(only_new=args.only_new, min_year=args.min_year)


if __name__ == "__main__":
    main()
