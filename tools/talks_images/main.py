import argparse

from data import load_all_talks, talk_image_exists, update_front_matter
from generator import generate_talk_image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate branded card images for Percona Community talks."
    )
    parser.add_argument(
        "--only-new",
        action="store_true",
        help="Generate cards only for talks missing assets/talks/<year>/<slug>.png",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=2025,
        help="Only process talks with talk_year >= this value (default: 2025)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    talks = load_all_talks(min_year=args.min_year)

    if args.only_new:
        talks = [t for t in talks if not talk_image_exists(t)]

    label = "new talks" if args.only_new else "talks"
    print(f"Found {len(talks)} {label} from {args.min_year} and newer")

    for talk in talks:
        img_path = generate_talk_image(talk)
        if not img_path:
            print(f"Skipped (no speaker image): {talk.md_path}")
            continue
        update_front_matter(talk.md_path, img_path)
        print(f"Generated: {img_path} for {talk.md_path}")


if __name__ == "__main__":
    main()
