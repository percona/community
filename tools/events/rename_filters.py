import os

TARGET_DIR = "content/events"

REPLACEMENTS = {
    "event_category": "events_category",
    "event_tag": "events_tag",
    "event_year": "events_year",
}

for root, dirs, files in os.walk(TARGET_DIR):
    for filename in files:
        if not filename.endswith(".md"):
            continue

        path = os.path.join(root, filename)
        print(f"Fixing {path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        for old, new in REPLACEMENTS.items():
            new_content = new_content.replace(old, new)

        # # backup
        # with open(path + ".bak", "w", encoding="utf-8") as f:
        #     f.write(content)

        # write updated file
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

print("Done!")
