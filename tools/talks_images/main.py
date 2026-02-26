from data import load_all_talks, update_front_matter
from generator import generate_talk_image


def main():
    # Only generate images for talks from 2025 and newer.
    # This avoids regenerating thousands of old talks.
    talks = load_all_talks(min_year=2025)

    print(f"Found {len(talks)} talks from 2025 and newer")

    for talk in talks:
        img_path = generate_talk_image(talk)   # returns talks/<year>/<slug>.png
        update_front_matter(talk.md_path, img_path)
        print(f"Generated: {img_path} for {talk.md_path}")


if __name__ == "__main__":
    main()
