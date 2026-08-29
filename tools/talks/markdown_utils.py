"""
Hugo markdown generation for Community Talks (Jira source).

Writes content/talks/<year>/<date>-<slug>.md and create-only contributor cards.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any

import yaml

from jira_utils import patch_talk
from debug_utils import dd, ddd  # noqa: F401 — kept for local debugging

CONTENT_DIR = "content/talks"
PERCONA_PREFIX = "https://percona.community/talks/"
CONTRIBUTORS_DIR = "content/contributors"
ASSETS_CONTRIBUTORS_DIR = "assets/contributors"
DEFAULT_CONTRIBUTOR_IMAGE = "contributors/percona.jpeg"


def slugify(text: str) -> str:
    """Converts a string to URL-safe slug format (hyphens for filenames)."""
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def _normalize_tags_str(tags_str: str) -> list[str]:
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t and t.strip()]


def split_front_matter(markdown: str) -> tuple[dict, str]:
    if not markdown.startswith("---"):
        return {}, markdown
    end_idx = markdown.find("\n---\n", 4)
    if end_idx == -1:
        fm = yaml.safe_load(markdown.strip("---")) or {}
        return fm, ""
    fm_raw = markdown[4:end_idx]
    body = markdown[end_idx + 5 :]
    fm = yaml.safe_load(fm_raw) or {}
    return fm, body


def assemble_markdown(fm: dict, body: str) -> str:
    fm_str = yaml.dump(
        fm,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
        default_flow_style=False,
    ).strip()
    return f"---\n{fm_str}\n---\n{body}"


def normalize_aliases(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    if isinstance(value, list):
        return [str(v).strip() for v in value if isinstance(v, str) and str(v).strip()]
    return []


def read_aliases_from_file(path: str) -> list[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    fm, _ = split_front_matter(content)
    return normalize_aliases(fm.get("aliases"))


def add_aliases_with_previous(
    markdown: str, previous_aliases: list[str], old_year: str, old_slug: str
) -> str:
    fm, body = split_front_matter(markdown)
    current = normalize_aliases(fm.get("aliases"))
    new_alias = f"/talks/{old_year}/{old_slug}"

    merged: list[str] = []
    seen: set[str] = set()
    for a in previous_aliases + current + [new_alias]:
        if a and a not in seen:
            seen.add(a)
            merged.append(a)

    fm["aliases"] = merged
    return assemble_markdown(fm, body)


def generate_filename(title: str, presentation_date: str) -> tuple[str, str, str]:
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
                year = (
                    presentation_date[:4]
                    if re.match(r"^\d{4}", presentation_date)
                    else "unknown"
                )
                date_part = slugify(presentation_date)

    slug = slugify(title)
    filename = f"{date_part}-{slug}.md"
    dirpath = os.path.join(CONTENT_DIR, year)
    filepath = os.path.join(dirpath, filename)
    return filepath, filename, year


def build_public_url(year: str, filename: str) -> str:
    slug = os.path.splitext(filename)[0]
    return f"{PERCONA_PREFIX}{year}/{slug}"


def get_existing_slug_and_year(community_url: str) -> tuple[str, str]:
    url = (community_url or "").strip()
    if not url or not url.startswith(PERCONA_PREFIX):
        return "", ""
    rest = url[len(PERCONA_PREFIX) :].strip("/")
    parts = rest.split("/", 1)
    if len(parts) != 2:
        return "", ""
    return parts[0], parts[1]


def find_existing_talk_path(jira_key: str, community_url: str) -> str | None:
    """Locate an existing MD by Community URL path or jira/id front matter."""
    old_year, old_slug = get_existing_slug_and_year(community_url)
    if old_year and old_slug:
        path = os.path.join(CONTENT_DIR, old_year, f"{old_slug}.md")
        if os.path.exists(path):
            return path

    if not os.path.isdir(CONTENT_DIR):
        return None
    needle = jira_key.strip()
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as f:
                    head = f.read(4000)
            except OSError:
                continue
            fm, _ = split_front_matter(head)
            if str(fm.get("jira") or "").strip() == needle:
                return path
            if str(fm.get("id") or "").strip() == needle:
                return path
    return None


def read_front_matter_from_file(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return {}
    fm, _ = split_front_matter(content)
    return fm if isinstance(fm, dict) else {}


def preserve_site_fields(markdown: str, existing_path: str | None) -> str:
    """
    Keep Hugo-only / previously curated fields that talks sync does not own
    (images, aliases, presentation_date_end) when overwriting a talk page.
    """
    if not existing_path or not os.path.exists(existing_path):
        return markdown
    old_fm = read_front_matter_from_file(existing_path)
    if not old_fm:
        return markdown
    fm, body = split_front_matter(markdown)
    changed = False
    old_images = old_fm.get("images")
    if old_images and not fm.get("images"):
        fm["images"] = old_images
        changed = True
    old_aliases = normalize_aliases(old_fm.get("aliases"))
    if old_aliases:
        merged = normalize_aliases(fm.get("aliases"))
        seen = set(merged)
        for a in old_aliases:
            if a not in seen:
                merged.append(a)
                seen.add(a)
        if merged != normalize_aliases(fm.get("aliases")):
            fm["aliases"] = merged
            changed = True
    # Sync always emits empty presentation_date_end; keep curated value if present.
    new_end = str(fm.get("presentation_date_end") or "").strip()
    old_end = str(old_fm.get("presentation_date_end") or "").strip()
    if not new_end and old_end:
        fm["presentation_date_end"] = old_end
        changed = True
    if not changed:
        return markdown
    return assemble_markdown(fm, body)


def save_markdown_file(filepath: str, markdown: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Saved: {filepath}")


def update_talk_file(
    filepath: str,
    new_year: str,
    old_year: str,
    old_slug: str,
    new_markdown: str,
    old_filepath: str | None = None,
):
    old_path = old_filepath or os.path.join(CONTENT_DIR, old_year, f"{old_slug}.md")
    previous_aliases = read_aliases_from_file(old_path)
    merged_markdown = add_aliases_with_previous(
        new_markdown, previous_aliases, old_year, old_slug
    )
    merged_markdown = preserve_site_fields(merged_markdown, old_path)

    save_markdown_file(filepath, merged_markdown)
    print(f"✅ New file saved: {filepath}")

    if os.path.exists(old_path) and old_path != filepath:
        os.remove(old_path)
        print(f"🗑️ Deleted old file: {old_path}")

    print(f"⚠️ Slug changed, aliases merged (added /talks/{old_year}/{old_slug})")


def process_talks(
    talks: list[dict[str, Any]],
    *,
    write: bool = True,
    only_new: bool = False,
) -> dict[str, Any]:
    """
    Process enriched Jira talks into Hugo markdown.

    write=False → dry-run (print plan only, no files / no Jira write-back).
    only_new=True → do not overwrite talks that already exist on disk.
    """
    total = 0
    created_files = 0
    updated_files = 0
    skipped_existing = 0
    changed_urls = 0
    jira_updated = 0
    all_new_speakers: list[dict[str, str]] = []
    planned: list[dict[str, Any]] = []

    for talk in talks:
        total += 1
        title, public_date, talk_year, md, new_speakers = build_hugo_markdown(
            talk, create_contributors=write
        )
        all_new_speakers.extend(new_speakers)

        filepath, filename, new_year = generate_filename(title, public_date)
        new_slug = os.path.splitext(filename)[0]
        community_url = talk.get("community_url") or ""
        old_year, old_slug = get_existing_slug_and_year(community_url)
        existing_path = find_existing_talk_path(talk.get("key") or "", community_url)
        if existing_path and not (old_year and old_slug):
            # Derive year/slug from discovered path for alias handling
            rel = os.path.relpath(existing_path, CONTENT_DIR)
            parts = rel.split(os.sep)
            if len(parts) >= 2:
                old_year = parts[0]
                old_slug = os.path.splitext(parts[-1])[0]

        new_url = build_public_url(new_year, filename)
        file_exists = os.path.exists(filepath) or bool(
            existing_path and os.path.exists(existing_path)
        )
        url_changed = bool(
            old_slug and old_year and (old_slug != new_slug or old_year != new_year)
        )

        planned.append(
            {
                "key": talk.get("key"),
                "title": title,
                "path": filepath,
                "url": new_url,
                "status": talk.get("status"),
                "pub": talk.get("publication_status"),
                "url_changed": url_changed,
                "exists": file_exists,
            }
        )

        print(f"✅ Processing: {title.strip()} [{talk.get('key')}]")
        print(f"   → {filepath}")
        print(f"   → {new_url}")

        if only_new and file_exists and not url_changed:
            print(f"⏭️ Skip existing talk (only-new)")
            skipped_existing += 1
            continue

        if not write:
            continue

        should_update_jira = False
        pub = (talk.get("publication_status") or "").strip()
        # Always write back when still in the Ready queue → flip to Published.
        ready_for_pub = pub.casefold() == "ready for publication"

        if url_changed:
            update_talk_file(
                filepath,
                new_year,
                old_year,
                old_slug,
                md,
                old_filepath=existing_path,
            )
            print(f"🟡 URL changed: {old_year}/{old_slug} → {new_year}/{new_slug}")
            changed_urls += 1
            updated_files += 1
            should_update_jira = True
        else:
            was_existing = os.path.exists(filepath) or bool(
                existing_path and os.path.exists(existing_path)
            )
            source_for_preserve = existing_path if existing_path else (
                filepath if os.path.exists(filepath) else None
            )
            md = preserve_site_fields(md, source_for_preserve)
            save_markdown_file(filepath, md)
            if was_existing:
                updated_files += 1
            else:
                created_files += 1
                should_update_jira = True

        if ready_for_pub:
            should_update_jira = True

        if should_update_jira:
            try:
                patch_talk(str(talk.get("key")), new_url)
                print(f"🔗 Updated Jira: {new_url}")
                jira_updated += 1
            except Exception as exc:
                print(f"❌ Jira write-back failed for {talk.get('key')}: {exc}")
        else:
            print(f"➡️ No Jira update needed: {new_url}")

    print("\n" + "=" * 60)
    print("📊 PROCESSING SUMMARY" + (" (dry-run)" if not write else ""))
    print("=" * 60)
    print(f"Total talks processed:     {total}")
    print(f"New contributors created:  {len(all_new_speakers)}")

    if all_new_speakers:
        print("\n🆕 NEW CONTRIBUTORS:")
        for sp in all_new_speakers:
            print(f"  • {sp['name']} → {sp['slug']}.md")

    print(f"\nFiles created:             {created_files}")
    print(f"Files updated:             {updated_files}")
    print(f"Skipped existing:          {skipped_existing}")
    print(f"URLs changed (aliases):    {changed_urls}")
    print(f"Jira issues updated:       {jira_updated}")
    print("=" * 60)

    return {
        "total": total,
        "created": created_files,
        "updated": updated_files,
        "skipped_existing": skipped_existing,
        "changed_urls": changed_urls,
        "jira_updated": jira_updated,
        "planned": planned,
        "new_speakers": all_new_speakers,
    }


def build_hugo_markdown(
    talk: dict[str, Any],
    *,
    create_contributors: bool = True,
) -> tuple[str, str, str, str, list[dict[str, str]]]:
    """Build Hugo markdown from an enriched Jira talk record."""
    talk_id = talk.get("key") or talk.get("id") or ""
    title = talk.get("title") or ""
    abstract = talk.get("abstract") or ""
    slides = talk.get("slides") or ""
    video_url = talk.get("video") or ""
    tags_raw = talk.get("labels") or []

    presentation_date = (talk.get("presentation_date") or "").strip()
    presentation_date_end = ""
    presentation_time = (talk.get("presentation_time") or "").strip()
    conference_url = talk.get("talk_url") or ""
    event_status = talk.get("status") or ""

    event = talk.get("event") or {}
    event_title = event.get("name") or ""
    event_date_start = event.get("date_start") or ""
    event_date_end = event.get("date_end") or ""
    event_url = event.get("url") or ""
    event_location = event.get("location") or ""
    event_tech_tags = list(event.get("technology") or [])

    public_date = presentation_date.strip()
    if not public_date and event_date_start:
        public_date = event_date_start

    talk_year = public_date[:4] if public_date and len(public_date) >= 4 else ""

    speakers: list[str] = []
    new_speakers_list: list[dict[str, str]] = []
    for speaker_data in talk.get("speakers") or []:
        slug = (speaker_data.get("slug") or "").strip()
        name = (speaker_data.get("Name") or "").strip() or "Unknown"
        if not slug and name:
            slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        if not slug:
            print(f"❌ Cannot generate slug for speaker in talk {talk_id}: {name}")
            continue
        if create_contributors and ensure_contributor_card(slug, speaker_data):
            new_speakers_list.append({"name": name, "slug": slug})
        elif create_contributors:
            # Existing card: still try to replace Percona placeholder with Jira avatar
            backfill_contributor_avatar(slug, speaker_data)
        speakers.append(slug)

    if isinstance(tags_raw, str):
        tag_list = _normalize_tags_str(tags_raw) + event_tech_tags
    else:
        tag_list = [str(t).strip() for t in tags_raw if str(t).strip()] + event_tech_tags

    if video_url:
        tag_list.append("Video")
    if slides:
        tag_list.append("Slides")

    seen: set[str] = set()
    tag_list_unique = [t for t in tag_list if not (t in seen or seen.add(t))]
    talk_tags_yaml = (
        "[" + ", ".join([f"'{t}'" for t in tag_list_unique]) + "]"
        if tag_list_unique
        else "[]"
    )

    escaped_title = title.replace("\\", "\\\\").replace('"', '\\"')

    youtube_id = None
    if video_url:
        match = re.search(
            r"(?:v=|/embed/|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url
        )
        youtube_id = match.group(1) if match else None

    final_presentation_date = presentation_date or event_date_start

    front_matter_lines = [
        "---",
        f'id: "{talk_id}"',
        f'jira: "{talk_id}"',
        f'title: "{escaped_title}"',
        "layout: single",
        "speakers:",
    ]
    front_matter_lines.extend(
        [f"  - {s}" for s in speakers] if speakers else ["  - unknown"]
    )
    front_matter_lines.extend(
        [
            f'talk_url: "{conference_url}"',
            f'presentation_date: "{final_presentation_date}"',
            f'presentation_date_end: "{presentation_date_end}"',
            f'presentation_time: "{presentation_time}"',
            f'talk_year: "{talk_year}"',
            f'event: "{event_title}"',
            f'event_jira: "{event.get("key") or ""}"',
            f'event_status: "{event_status}"',
            f'event_date_start: "{event_date_start}"',
            f'event_date_end: "{event_date_end}"',
            f'event_url: "{event_url}"',
            f'event_location: "{event_location}"',
            f"talk_tags: {talk_tags_yaml}",
            f'slides: "{slides}"',
            f'video: "{video_url}"',
        ]
    )
    if youtube_id:
        front_matter_lines.append(f'youtube_id: "{youtube_id}"')
    front_matter_lines.append("---")

    front_matter = "\n".join(front_matter_lines)
    body = abstract.strip() if abstract else ""
    markdown = front_matter + ("\n" + body if body else "\n")

    return title, public_date, talk_year, markdown, new_speakers_list


def download_contributor_avatar(avatar_url: str, slug: str) -> str | None:
    """
    Download a Jira/Atlassian avatar into assets/contributors/<slug>.<ext>.
    Returns Hugo-relative path (contributors/<slug>.ext) or None.
    """
    url = (avatar_url or "").strip()
    if not url or not slug:
        return None
    # Skip obvious initials-only placeholders from Atlassian
    if "/initials/" in url:
        return None

    import requests

    try:
        response = requests.get(url, timeout=45)
    except requests.RequestException as exc:
        print(f"⚠️ Avatar download failed for {slug}: {exc}")
        return None
    if not response.ok or not response.content:
        print(f"⚠️ Avatar HTTP {response.status_code} for {slug}")
        return None

    ctype = (response.headers.get("content-type") or "").split(";")[0].strip().lower()
    ext = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
        "image/gif": "gif",
    }.get(ctype)
    if not ext:
        # sniff
        head = response.content[:8]
        if head.startswith(b"\xff\xd8"):
            ext = "jpg"
        elif head.startswith(b"\x89PNG"):
            ext = "png"
        elif head.startswith(b"RIFF"):
            ext = "webp"
        else:
            print(f"⚠️ Unknown avatar type {ctype!r} for {slug}")
            return None

    os.makedirs(ASSETS_CONTRIBUTORS_DIR, exist_ok=True)
    filename = f"{slug}.{ext}"
    abs_path = os.path.join(ASSETS_CONTRIBUTORS_DIR, filename)
    try:
        with open(abs_path, "wb") as f:
            f.write(response.content)
    except OSError as exc:
        print(f"⚠️ Cannot write avatar {abs_path}: {exc}")
        return None
    return f"contributors/{filename}"


def _contributor_uses_placeholder(images: Any) -> bool:
    if not images:
        return True
    if isinstance(images, str):
        images = [images]
    if not isinstance(images, list) or not images:
        return True
    only = str(images[0] or "").strip()
    return only == DEFAULT_CONTRIBUTOR_IMAGE or only.endswith("/percona.jpeg")


def backfill_contributor_avatar(slug: str, speaker_data: dict) -> bool:
    """If contributor exists with percona.jpeg placeholder, replace with Jira avatar."""
    filepath = os.path.join(CONTRIBUTORS_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        return False
    avatar_url = (speaker_data.get("avatar_url") or "").strip()
    if not avatar_url:
        return False
    try:
        with open(filepath, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return False
    if not text.startswith("---"):
        return False
    end = text.find("\n---\n", 4)
    if end == -1:
        return False
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except Exception:
        return False
    if not _contributor_uses_placeholder(fm.get("images")):
        return False
    rel = download_contributor_avatar(avatar_url, slug)
    if not rel:
        return False
    fm["images"] = [rel]
    body = text[end + 5 :]
    fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True, width=1000).strip()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}\n---\n{body}")
    except OSError as exc:
        print(f"⚠️ Cannot update avatar in {filepath}: {exc}")
        return False
    print(f"🖼️ Updated contributor avatar: {filepath} → {rel}")
    return True


def ensure_contributor_card(slug: str, speaker_data: dict) -> bool:
    """Create contributor card if missing. Returns True if created."""
    if not slug:
        name_fallback = speaker_data.get("Name", "Unknown")
        print(f"❌ Cannot create contributor card: empty slug for speaker '{name_fallback}'")
        return False

    name = (speaker_data.get("Name") or "").strip()
    if not name:
        print(f"⚠️ Skip contributor: empty Name (slug: {slug})")
        return False

    filepath = os.path.join(CONTRIBUTORS_DIR, f"{slug}.md")
    if os.path.exists(filepath):
        return False

    notion_status = (speaker_data.get("Status") or "").strip().lower()
    role = (speaker_data.get("Role") or "").strip()
    tagline_from_notion = (speaker_data.get("Tagline") or "").strip()
    technology = (speaker_data.get("Technology") or "").strip()
    bio = (speaker_data.get("Bio") or "").strip()

    is_available = notion_status in {"available", ""}
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

    social = {
        "facebook": None,
        "github": None,
        "linkedin": None,
        "twitter": None,
        "website": None,
    }
    notion_to_social = {
        "LinkedIn": "linkedin",
        "Twitter": "twitter",
        "GitHub": "github",
        "Website": "website",
        "Facebook": "facebook",
    }
    for notion_field, key in notion_to_social.items():
        url = (speaker_data.get(notion_field) or "").strip()
        if url:
            social[key] = url

    images = [DEFAULT_CONTRIBUTOR_IMAGE]
    avatar_rel = download_contributor_avatar(
        str(speaker_data.get("avatar_url") or ""), slug
    )
    if avatar_rel:
        images = [avatar_rel]

    if not bio:
        if technology:
            bio = f"{technology} Expert"
        elif status == "community":
            bio = "Open Source Contributor"
        else:
            bio = "Database Engineer"

    fm = {
        "name": slug,
        "name_pronunciation": slug,
        "fullname": name,
        "fullname_pronounciation": name,
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

    os.makedirs(CONTRIBUTORS_DIR, exist_ok=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"✅ Created contributor: {filepath} [status: {status}]")
        return True
    except Exception as e:
        print(f"❌ Failed to write {filepath}: {e}")
        return False
