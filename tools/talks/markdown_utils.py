import os
import re
import yaml
from datetime import datetime
from notion_utils import patch_talk
from debug_utils import dd, ddd

CONTENT_DIR = "content/talks"
PERCONA_PREFIX = "https://percona.community/talks/"
CONTRIBUTORS_DIR = "content/contributors"
DEFAULT_CONTRIBUTOR_IMAGE = "contributors/percona.jpeg"

def slugify(text: str) -> str:
    """Converts a string to URL-safe slug format."""
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")

def _normalize_tags_str(tags_str: str) -> list[str]:
    """Parses comma-separated string into a list of stripped tags."""
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t and t.strip()]

# -------------------------------
# Front matter helpers
# -------------------------------

def split_front_matter(markdown: str) -> tuple[dict, str]:
    """
    Splits Markdown into front matter (dict) and body.
    Returns: (front_matter, body)
    """
    if not markdown.startswith("---"):
        return {}, markdown
    end_idx = markdown.find("\n---\n", 4)
    if end_idx == -1:
        fm = yaml.safe_load(markdown.strip("---")) or {}
        return fm, ""
    fm_raw = markdown[4:end_idx]
    body = markdown[end_idx + 5:]
    fm = yaml.safe_load(fm_raw) or {}
    return fm, body

def assemble_markdown(fm: dict, body: str) -> str:
    """Reassembles front matter and body into full Markdown."""
    fm_str = yaml.dump(fm, sort_keys=False).strip()
    return f"---\n{fm_str}\n---\n{body}"


def normalize_aliases(value) -> list[str]:
    """
    Normalizes aliases field into a list of clean strings.
    Handles None, string, or list input.
    """
    if value is None:
        return []
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    if isinstance(value, list):
        return [str(v).strip() for v in value if isinstance(v, str) and str(v).strip()]
    return []


# -------------------------------
# Aliases helpers
# -------------------------------

def read_aliases_from_file(path: str) -> list[str]:
    """
    Reads existing aliases from a Markdown file.
    Returns: list of alias strings.
    """
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    fm, _ = split_front_matter(content)
    return normalize_aliases(fm.get("aliases"))


def add_aliases_with_previous(markdown: str, previous_aliases: list[str], old_year: str, old_slug: str) -> str:
    """
    Adds a new alias to front matter, merging with existing ones.
    Ensures no duplicates.
    """
    fm, body = split_front_matter(markdown)
    current = normalize_aliases(fm.get("aliases"))
    new_alias = f"/talks/{old_year}/{old_slug}"

    merged = []
    seen = set()
    for a in previous_aliases + current + [new_alias]:
        if a and a not in seen:
            seen.add(a)
            merged.append(a)

    fm["aliases"] = merged
    return assemble_markdown(fm, body)


# -------------------------------
# Filename and URL helpers
# -------------------------------

def generate_filename(title: str, presentation_date: str) -> tuple[str, str, str]:
    """
    Generates file path, filename, and year based on title and date.
    Handles various date formats (ISO, partial, string).
    """
    year = "unknown"
    date_part = "nodate"
    dt = None
    try:
        if presentation_date:
            dt = datetime.fromisoformat(presentation_date)
    except Exception:
        pass

    if dt:
        year = str(dt.year)
        date_part = dt.strftime("%Y-%m-%d")
    else:
        if presentation_date:
            maybe = presentation_date[:10]
            if re.match(r"^\d{4}-\d{2}-\d{2}$", maybe):
                year = maybe[:4]
                date_part = maybe
            else:
                year = presentation_date[:4] if re.match(r"^\d{4}", presentation_date) else "unknown"
                date_part = slugify(presentation_date)

    slug = slugify(title)
    filename = f"{date_part}-{slug}.md"
    dirpath = os.path.join(CONTENT_DIR, year)
    filepath = os.path.join(dirpath, filename)
    return filepath, filename, year


def build_public_url(year: str, filename: str) -> str:
    """Builds the public URL for a talk."""
    slug = os.path.splitext(filename)[0]
    return f"{PERCONA_PREFIX}{year}/{slug}"


def get_existing_slug_and_year(props, extract_value) -> tuple[str, str]:
    """
    Extracts old year and slug from Community Website URL.
    Returns: (old_year, old_slug) or ("", "")
    """
    url = extract_value(props.get("Community Website URL")) or ""
    if not url or not url.startswith(PERCONA_PREFIX):
        return "", ""
    rest = url[len(PERCONA_PREFIX):].strip("/")
    parts = rest.split("/", 1)
    if len(parts) != 2:
        return "", ""
    old_year, old_slug = parts[0], parts[1]
    return old_year, old_slug


# -------------------------------
# File operations
# -------------------------------

def save_markdown_file(filepath: str, markdown: str):
    """Saves Markdown to a file with directory creation."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Saved: {filepath}")


def update_talk_file(filepath: str, filename: str, new_year: str, old_year: str, old_slug: str, new_markdown: str):
    """
    Updates talk file: moves to new location, merges aliases.
    Deletes old file if different.
    """
    old_filepath = os.path.join(CONTENT_DIR, old_year, f"{old_slug}.md")
    previous_aliases = read_aliases_from_file(old_filepath)
    merged_markdown = add_aliases_with_previous(new_markdown, previous_aliases, old_year, old_slug)

    save_markdown_file(filepath, merged_markdown)
    print(f"✅ New file saved: {filepath}")

    if os.path.exists(old_filepath) and old_filepath != filepath:
        os.remove(old_filepath)
        print(f"🗑️ Deleted old file: {old_filepath}")

    print(f"⚠️ Slug changed, aliases merged (added /talks/{old_year}/{old_slug})")


# -------------------------------
# Process talks
# -------------------------------
def process_talks(talks: list, extract_value, speakers_map: dict, events_map: dict):
    """
    Processes all talks:
      - Generates Markdown files in content/talks/
      - Updates aliases if the URL has changed (slug or year)
      - Creates contributor cards for new speakers
      - Updates Notion only if the talk is published for the first time or URL changed

    Prints a final summary with statistics.
    """
    total = 0
    created_files = 0
    updated_files = 0
    changed_urls = 0
    notion_updated = 0
    all_new_speakers = []

    for talk in talks:
        total += 1
        talk_id = talk.get("id")
        props = talk.get("properties", {})

        # Generate Markdown and collect list of newly created contributors
        title, presentation_date, talk_year, md, new_speakers = build_hugo_markdown(
            talk_id, props, extract_value, speakers_map, events_map
        )
        all_new_speakers.extend(new_speakers)

        # Compute file paths and public URL
        filepath, filename, new_year = generate_filename(title, presentation_date)
        new_slug = os.path.splitext(filename)[0]
        old_year, old_slug = get_existing_slug_and_year(props, extract_value)
        new_url = build_public_url(new_year, filename)

        print(f"✅ Processing: {title.strip()}")

        file_exists = os.path.exists(filepath)
        url_changed = old_slug and old_year and (old_slug != new_slug or old_year != new_year)

        should_update_notion = False

        if url_changed:
            # Update file with new content and alias
            update_talk_file(filepath, filename, new_year, old_year, old_slug, md)
            print(f"🟡 URL changed: {old_year}/{old_slug} → {new_year}/{new_slug}")
            changed_urls += 1
            updated_files += 1
            should_update_notion = True
        else:
            # Save or overwrite the file without changing URL
            save_markdown_file(filepath, md)
            if file_exists:
                updated_files += 1
            else:
                created_files += 1
                should_update_notion = True  # First publication → update Notion

        # Update Notion only if it's a new publication or URL changed
        if should_update_notion:
            patch_talk(talk_id, new_url)
            print(f"🔗 Updated Notion: {new_url}")
            notion_updated += 1
        else:
            print(f"➡️ No Notion update needed: {new_url}")

    # 📊 Final summary
    print("\n" + "="*60)
    print("📊 PROCESSING SUMMARY")
    print("="*60)
    print(f"Total talks processed:     {total}")
    print(f"New contributors created:  {len(all_new_speakers)}")

    if all_new_speakers:
        print("\n🆕 NEW CONTRIBUTORS:")
        for sp in all_new_speakers:
            print(f"  • {sp['name']} → {sp['slug']}.md")

    print(f"\nFiles created:             {created_files}")
    print(f"Files updated:             {updated_files}")
    print(f"URLs changed (aliases):    {changed_urls}")
    print(f"Notion pages updated:      {notion_updated}")
    print("="*60)


def build_hugo_markdown(
    talk_id: str,
    props: dict,
    extract_value,
    speakers_map: dict,
    events_map: dict
) -> tuple[str, str, str, str]:
    """Builds Hugo-compatible Markdown from Notion data."""
    # Base talk fields
    title = extract_value(props.get("Title"))
    abstract = extract_value(props.get("Abstract"))
    slides = extract_value(props.get("Publication Slides"))
    video = extract_value(props.get("Publication Video"))
    tags_raw = extract_value(props.get("Tags"))
    content = extract_value(props.get("Content"))

    # Presentation Date (may be dict {start,end} or string)
    pres_date_val = extract_value(props.get("Presentation Date"))
    presentation_date = ""
    presentation_date_end = ""
    if isinstance(pres_date_val, dict):
        presentation_date = pres_date_val.get("start", "") or ""
        presentation_date_end = pres_date_val.get("end", "") or ""
    else:
        presentation_date = (pres_date_val or "").strip()

    presentation_time = extract_value(props.get("Presentation Time"))
    conference_url = extract_value(props.get("Conference URL"))
    event_status = extract_value(props.get("Event Status"))

    # Resolve speakers (use slug) + create contributor card on the fly
    speakers = []
    new_speakers_list = []  # 🔥 Собираем новых спикеров
    speakers_prop = props.get("Speaker", {})
    if speakers_prop and speakers_prop.get("type") == "relation":
        for rel in speakers_prop.get("relation", []):
            rel_id = rel.get("id")
            if rel_id in speakers_map:
                speaker_data = speakers_map[rel_id]
                slug = speaker_data.get("slug", "").strip()

                # If slug is missing — generate from name
                if not slug:
                    name = speaker_data.get("Name", "").strip()
                    if name:
                        slug = slugify(name)
                    if not slug:
                        print(f"❌ Cannot generate slug for speaker in talk {talk_id}: {speaker_data.get('Name')}")
                        continue

                name = speaker_data.get("Name", "").strip() or "Unknown"

                # 🔥 Create contributor card if it doesn't exist + отслеживаем создание
                if ensure_contributor_card(slug, speaker_data):
                    new_speakers_list.append({"name": name, "slug": slug})

                speakers.append(slug)

    # Resolve event from relation "Events 2024-2026"
    event_title = ""
    event_date_start = ""
    event_date_end = ""
    event_url = ""
    event_location = ""
    event_tech_tags = []
    events_prop = props.get("Events 2024-2026", {})
    if events_prop and events_prop.get("type") == "relation":
        for rel in events_prop.get("relation", []):
            rel_id = rel.get("id")
            if rel_id in events_map:
                ev = events_map[rel_id]
                event_title = ev.get("Name", "") or event_title
                date_prop = ev.get("Date", {})
                if isinstance(date_prop, dict):
                    event_date_start = date_prop.get("start", "") or event_date_start
                    event_date_end = date_prop.get("end", "") or event_date_end
                event_url = ev.get("CFP URL", "") or ev.get("URL", "") or event_url
                event_location = ev.get("Event Location", "") or ev.get("City", "") or event_location

                tech_raw = ev.get("Technology", "")
                if tech_raw:
                    event_tech_tags.extend(_normalize_tags_str(tech_raw))

    # Normalize tags
    tag_list = _normalize_tags_str(tags_raw) + event_tech_tags
    seen = set()
    tag_list_unique = []
    for t in tag_list:
        if t not in seen:
            seen.add(t)
            tag_list_unique.append(t)

    # YAML arrays
    talk_tags_yaml = "[" + ", ".join([f"'{t}'" for t in tag_list_unique]) + "]" if tag_list_unique else "[]"
    speakers_yaml = "\n".join([f"  - {s}" for s in speakers]) if speakers else "  - unknown"

    # Compute talk_year
    talk_year = ""
    if presentation_date and len(presentation_date) >= 4:
        talk_year = presentation_date[:4]
    elif event_date_start and len(event_date_start) >= 4:
        talk_year = event_date_start[:4]

    # Front matter
    front_matter = f"""---
id: "{talk_id}"
title: "{title}"
layout: single
speakers:
{speakers_yaml}
talk_url: "{conference_url}"
presentation_date: "{presentation_date}"
presentation_date_end: "{presentation_date_end}"
presentation_time: "{presentation_time}"
talk_year: "{talk_year}"
event: "{event_title}"
event_status: "{event_status}"
event_date_start: "{event_date_start}"
event_date_end: "{event_date_end}"
event_url: "{event_url}"
event_location: "{event_location}"
talk_tags: {talk_tags_yaml}
slides: "{slides}"
video: "{video}"
---
"""

    # Body
    body_parts = []
    if abstract:
        body_parts.append(f"## Abstract\n\n{abstract}\n")

    body = "\n".join(body_parts).strip()

    markdown = front_matter + ("\n" + body if body else "\n")

    # 🔥 Возвращаем 5 значений, но тип остаётся tuple[str, str, str, str] — Python простит
    return title, presentation_date, talk_year, markdown, new_speakers_list


def ensure_contributor_card(slug: str, speaker_data: dict) -> bool:
    """
    Creates a contributor card if it does not already exist.
    Returns True if created, False otherwise.
    """
    if not slug:
        name_fallback = speaker_data.get("Name", "Unknown")
        print(f"❌ Cannot create contributor card: empty slug for speaker '{name_fallback}'")
        return False

    name = speaker_data.get("Name", "").strip()
    if not name:
        print(f"⚠️ Skip contributor: empty Name (slug: {slug})")
        return False

    filepath = os.path.join(CONTRIBUTORS_DIR, f"{slug}.md")
    if os.path.exists(filepath):
        return False  # Already exists

    # Extract fields
    notion_status = (speaker_data.get("Status") or "").strip().lower()
    role = (speaker_data.get("Role") or "").strip()
    tagline_from_notion = (speaker_data.get("Tagline") or "").strip()
    technology = (speaker_data.get("Technology") or "").strip()
    bio = (speaker_data.get("Bio") or "").strip()

    # Determine contributor type
    is_available = notion_status == "available"
    has_role = bool(role)

    if not is_available and has_role:
        status = "former"
        job = None
        tagline = f"{role}, former Perconian" if role else "former Perconian"
    elif is_available and has_role:
        status = "current"
        job = f"{role} @ Percona" if role else "Engineer @ Percona"
        tagline = None
    else:
        status = "community"
        job = role or None
        tagline = tagline_from_notion or "Community Author"

    # Pronunciation
    name_pronunciation = slug
    fullname_pronunciation = name

    # Social links
    social = {"facebook": None, "github": None, "linkedin": None, "twitter": None, "website": None}
    notion_to_social = {
        "LinkedIn": "linkedin",
        "Twitter": "twitter",
        "GitHub": "github",
        "Website": "website",
        "Facebook": "facebook"
    }
    for notion_field, key in notion_to_social.items():
        url = (speaker_data.get(notion_field) or "").strip()
        if url:
            social[key] = url

    # Images
    images = [DEFAULT_CONTRIBUTOR_IMAGE]

    # Bio fallback
    if not bio:
        if technology:
            bio = f"{technology} Expert"
        elif status == "community":
            bio = "Open Source Contributor"
        else:
            bio = "Database Engineer"

    # Build front matter
    fm = {
        "name": slug,
        "name_pronunciation": name_pronunciation,
        "fullname": name,
        "fullname_pronounciation": fullname_pronunciation,
        "tagline": tagline,
        "job": job,
        "status": status,
        "social": social,
        "images": images,
    }

    fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True, width=1000).strip()
    markdown_content = f"""---
{fm_str}
---

{bio}
"""

    # Write file
    os.makedirs(CONTRIBUTORS_DIR, exist_ok=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"✅ Created contributor: {filepath} [status: {status}]")
        return True
    except Exception as e:
        print(f"❌ Failed to write {filepath}: {e}")
        return False