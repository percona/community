"""
🔄 Sync Talks from Notion to Hugo Site

This script:
1. Loads data from Notion (speakers, events, talks)
2. Processes each talk:
   - Generates a Markdown file in content/talks/
   - Updates aliases if the URL changed
   - Creates contributor cards for new speakers
3. Updates Notion with the new public URL.

Used by: CI/CD, manual sync.
"""

from notion_utils import (
    load_speakers,
    load_events,
    load_talks,
    extract_value
)
from markdown_utils import process_talks
from debug_utils import print_count, print_all_fields
import pprint


def main():
    """
    Main execution flow:
    - Load speakers, events, and talks from Notion
    - Print counts for visibility
    - Process all talks (generate files, update aliases, create contributors)
    """
    print("🔄 Starting Notion to Hugo sync for talks...")

    # Load data from Notion
    speakers_fields, speakers_map = load_speakers()
    print("✅ Speakers database loaded")

    events_fields, events_map = load_events()
    print("✅ Events database loaded")

    talks = load_talks()
    print("✅ Talks list loaded")

    # Debug: print number of entries
    print("-" * 50)
    print_count(speakers_map, label="Speakers")
    print_count(events_map, label="Events")
    print_count(talks, label="Talks")
    print("-" * 50)

    # Debug: inspect raw fields (uncomment if needed)
    # print_all_fields(speakers_map, limit=4, stop=True)
    # pprint.pprint(events_fields)

    # Process all talks: generate Markdown, manage aliases, create contributors
    print("📝 Processing talks...")
    process_talks(talks, extract_value, speakers_map, events_map)

    print("🎉 Sync completed successfully!")


if __name__ == "__main__":
    main()
