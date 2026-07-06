# Talks Image Generator

This tool generates consistent, branded social images for conference talks.  
It reads talk metadata from Markdown files, loads speaker information, renders a gradient background, places the event logo, title, metadata, and speaker photos, and saves the final PNG image into the project’s `assets/` directory.

The generator is designed for static‑site setups (Hugo, Jekyll, Astro, etc.) where talks are stored as Markdown files with YAML front matter.

---

## Features

- Automatic image generation for all talks (optional `min_year` filter in `load_all_talks`)
- Dynamic gradient backgrounds based on talk tags  
- Branded background photo with semi-transparent text panel  
- Automatic font scaling for long titles and long event names  
- Circular speaker photos with white borders  
- Support for one or two speakers  
- Automatic update of the talk’s Markdown front matter (`images:` field)  
- Clean, production‑ready codebase with minimal dependencies

---

## Project Structure

```
tools/
  talks_images/
    generator.py      # Image rendering logic
    data.py           # Talk loader + front matter updater
    main.py           # Entry point
    fonts/
      Inter-Bold.ttf
      Inter-Regular.ttf
    templates/
      logo-white.png
      logo.png
      percona-community-talk-bg.jpg
content/
  talks/
    <year>/<slug>.md  # Talk Markdown files
  contributors/
    <speaker>.md      # Speaker metadata
assets/
  talks/
    <year>/<slug>.png # Generated images
```

---

## Requirements

- Python 3.10+
- Pillow
- PyYAML
- python-frontmatter

Install dependencies:

```
pip install pillow pyyaml python-frontmatter
```

---

## How It Works

### 1. `data.py`
- Loads all talk Markdown files.
- Extracts metadata (title, speakers, event, tags, etc.).
- Loads speaker images from contributor files.
- Updates the talk’s front matter with the generated image path.

### 2. `generator.py`
- Creates a 1200×630 PNG image.
- Uses `percona-community-talk-bg.jpg` (cover-cropped) as the background.
- White community logo in the top-right corner (no panel behind it).
- Title and event metadata span the card width with side margins.
- Speaker(s) in rounded cards at the bottom — dark semi-transparent fill, circular photo, name/role, purple stripe on the right edge.
- Saves the final PNG into `assets/talks/<year>/`.

### 3. `main.py`
- Loads talks (with optional `--min-year` and `--only-new` filters).
- Generates images.
- Updates Markdown front matter.
- Prints progress.

---

## Usage

Run the generator manually after adding new talks:

```
python tools/talks_images/main.py --only-new
```

Only create cards for talks that do not yet have a PNG at `assets/talks/<year>/<slug>.png`. This is the usual command after adding one or more new talk files.

Process all talks from a given year (regenerates existing cards too):

```
python tools/talks_images/main.py
python tools/talks_images/main.py --min-year 2026
```

### CLI options

| Flag | Default | Description |
|------|---------|-------------|
| `--only-new` | off | Skip talks that already have `assets/talks/<year>/<slug>.png` |
| `--min-year` | `2025` | Only load talks with `talk_year >= min-year` |

To generate images for all years:

```
python tools/talks_images/main.py --min-year 2000
```

---

## Markdown Front Matter Update

After generating an image, the tool automatically updates the talk’s Markdown:

```
images:
  - talks/2025/my-talk.png
```

The path is stored **without** the `assets/` prefix, which is typical for static‑site generators.

---

## Speaker Images

Each speaker must have a contributor file:

```
content/contributors/<slug>.md
```

With at least:

```
fullname: John Doe
images:
  - contributors/john_doe.jpg
```

The generator loads the first image listed.

---

## Output Example

Generated images are saved to:

```
assets/talks/2025/my-talk.png
```

And referenced in Markdown as:

```
talks/2025/my-talk.png
```

---

## Development Notes

- The generator is deterministic: same input → same output.  
- Font scaling is based on pixel width, not character count.  
- The layout is optimized for readability and consistent branding.
