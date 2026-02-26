import os
import glob
import yaml
import frontmatter
from dataclasses import dataclass

TALKS_DIR = "content/talks"
CONTRIB_DIR = "content/contributors"
ASSETS_DIR = "assets"


@dataclass
class Talk:
    title: str
    speakers: list[str]
    year: str
    slug: str
    md_path: str
    speaker_images: list[str]
    event: str
    event_date: str
    location: str
    tags: list[str]


def load_contributor_image(slug: str) -> str | None:
    """
    Returns absolute path to contributor image from contributor markdown.
    """
    path = os.path.join(CONTRIB_DIR, f"{slug}.md")
    if not os.path.exists(path):
        return None

    post = frontmatter.load(path)
    imgs = post.get("images", [])
    if not imgs:
        return None

    # images: ["contributors/sonia_valeja.jpeg"]
    rel = imgs[0]
    return os.path.join(ASSETS_DIR, rel)

def load_all_talks(min_year: int | None = None) -> list[Talk]:
    """
    Loads talks from content/talks.
    If min_year is provided, only talks with talk_year >= min_year are returned.
    """

    files = glob.glob(f"{TALKS_DIR}/**/*.md", recursive=True)
    talks = []

    for md_path in files:
        post = frontmatter.load(md_path)

        year = post.get("talk_year")
        if not year:
            continue

        # filter early — skip unnecessary files
        if min_year and int(year) < min_year:
            continue

        title = post.get("title")
        speakers = post.get("speakers", [])
        slug = os.path.splitext(os.path.basename(md_path))[0]

        event = post.get("event", "")
        event_date = post.get("event_date_start", "")
        location = post.get("event_location", "")
        tags = post.get("talk_tags", [])

        speaker_images = [load_contributor_image(s) for s in speakers]

        talks.append(Talk(
            title=title,
            speakers=speakers,
            year=year,
            slug=slug,
            md_path=md_path,
            speaker_images=speaker_images,
            event=event,
            event_date=event_date,
            location=location,
            tags=tags
        ))

    return talks



def update_front_matter(md_path: str, image_path: str):
    """
    Adds generated image to front matter without reordering fields.
    image_path must be WITHOUT 'assets/' prefix.
    """

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # split front matter
    assert content.startswith("---")
    _, fm_text, body = content.split("---", 2)

    data = yaml.safe_load(fm_text)

    # append image path (no assets/)
    images = data.get("images", [])
    if image_path not in images:
        images.insert(0, image_path)
    data["images"] = images

    # dump YAML without sorting keys
    new_fm = yaml.dump(data, sort_keys=False, allow_unicode=True)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(new_fm)
        f.write("---")
        f.write(body)
