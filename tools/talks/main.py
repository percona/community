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
    speakers_fields, speakers_map = load_speakers()
    events_fields, events_map = load_events()
    talks = load_talks()

    # pprint.pprint(events_fields)
    
    print_count(speakers_map)
    print_count(events_map)
    print_count(talks)
    # print_all_fields(talks, limit=4, stop=True)
    process_talks(talks, extract_value, speakers_map, events_map)

if __name__ == "__main__":
    main()
