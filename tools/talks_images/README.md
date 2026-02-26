# Talks Image Generator

This tool generates consistent, branded social images for conference talks.  
It reads talk metadata from Markdown files, loads speaker information, renders a gradient background, places the event logo, title, metadata, and speaker photos, and saves the final PNG image into the project’s `assets/` directory.

The generator is designed for static‑site setups (Hugo, Jekyll, Astro, etc.) where talks are stored as Markdown files with YAML front matter.

---

## Features

- Automatic image generation for all talks starting from a given year  
- Dynamic gradient backgrounds based on talk tags  
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
      logo.png
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
- Selects a gradient based on talk tags.
- Renders:
  - Logo  
  - “Talks” label  
  - Title (with dynamic font size)  
  - Event + date + location (with dynamic font size)  
  - Speaker photos and names  
- Saves the final PNG into `assets/talks/<year>/`.

### 3. `main.py`
- Loads all talks starting from a given year (default: 2025).
- Generates images.
- Updates Markdown front matter.
- Prints progress.

---

## Usage

Run the generator:

```
python tools/talks_images/main.py
```

By default, it processes all talks with:

```
load_all_talks(min_year=2025)
```

To generate images for all years, edit `main.py`:

```
talks = load_all_talks(min_year=None)
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
- Gradients are diagonal and computed pixel‑by‑pixel for smoothness.  
- Font scaling is based on pixel width, not character count.  
- The layout is optimized for readability and consistent branding.
