"""
Generate branded OG/card images for community event pages.

Uses procedural gradients (until photo backgrounds are provided) + Percona
Community white logo. Badges: Speaking / Sponsoring.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from datetime import date, datetime

from PIL import Image, ImageDraw, ImageFont

IMG_W = 1200
IMG_H = 630

FONT_BOLD = "tools/talks_images/fonts/Inter-Bold.ttf"
FONT_REG = "tools/talks_images/fonts/Inter-Regular.ttf"
LOGO_WHITE = "tools/talks_images/templates/logo-white.png"

MARGIN_X = 80
MARGIN_TOP = 48
LOGO_MAX_WIDTH = 340
TEXT_WHITE = (255, 255, 255, 255)
TEXT_SOFT = (235, 235, 242, 255)
TEXT_MUTED = (186, 190, 205, 255)
TEXT_FOOT = (170, 174, 188, 210)

# Modern dark gradients (RGB stops). Avoid flat purple-on-white.
GRADIENTS: list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]] = [
    ((15, 23, 42), (30, 58, 95), (15, 118, 110)),       # slate → teal
    ((17, 24, 39), (55, 48, 80), (190, 75, 90)),        # ink → rose
    ((12, 35, 40), (20, 80, 70), (40, 120, 100)),       # deep forest
    ((28, 25, 23), (70, 50, 40), (180, 120, 60)),       # warm charcoal/gold
    ((10, 20, 40), (40, 60, 120), (20, 40, 80)),        # navy night
    ((25, 25, 35), (60, 60, 70), (100, 100, 110)),      # cool grey
]


@dataclass
class EventCard:
    title: str
    date_display: str
    location: str
    year: str
    slug: str
    md_path: str
    sponsored: bool
    speaking: bool


def _font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def pick_gradient(slug: str) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    return GRADIENTS[h % len(GRADIENTS)]


def make_gradient(
    c1: tuple[int, int, int],
    c2: tuple[int, int, int],
    c3: tuple[int, int, int],
) -> Image.Image:
    """Fast diagonal-ish 3-stop gradient via tiny strip + LANCZOS upscale."""
    strip_w, strip_h = 64, 32
    strip = Image.new("RGB", (strip_w, strip_h))
    px = strip.load()
    for y in range(strip_h):
        for x in range(strip_w):
            t = (x / (strip_w - 1) * 0.65) + (y / (strip_h - 1) * 0.35)
            if t < 0.5:
                u = t * 2
                r = int(c1[0] + (c2[0] - c1[0]) * u)
                g = int(c1[1] + (c2[1] - c1[1]) * u)
                b = int(c1[2] + (c2[2] - c1[2]) * u)
            else:
                u = (t - 0.5) * 2
                r = int(c2[0] + (c3[0] - c2[0]) * u)
                g = int(c2[1] + (c3[1] - c2[1]) * u)
                b = int(c2[2] + (c3[2] - c2[2]) * u)
            px[x, y] = (r, g, b)
    return strip.resize((IMG_W, IMG_H), Image.LANCZOS).convert("RGBA")


def parse_iso_day(raw: str) -> date | None:
    text = (raw or "").strip()[:10]
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _fmt_day(d: date) -> str:
    return f"{d.strftime('%B')} {d.day}"


def humanize_date_display(raw: str) -> str:
    """
    Turn ISO fragments into readable copy:
      2026-09-23              → September 23, 2026
      2026-09-22 – 2026-09-26 → September 22–26, 2026
      2026-09-28 – 2026-10-02 → September 28 – October 2, 2026
    """
    text = (raw or "").strip()
    if not text:
        return ""

    start: date | None = None
    end: date | None = None

    m = re.match(
        r"^(\d{4}-\d{2}-\d{2})(?:\s+[–—−-]+\s+|\s*[–—−]\s*)(\d{4}-\d{2}-\d{2})$",
        text,
    )
    if m:
        start = parse_iso_day(m.group(1))
        end = parse_iso_day(m.group(2))
    else:
        start = parse_iso_day(text)
        end = start

    if not start:
        return text
    if not end or start == end:
        return f"{_fmt_day(start)}, {start.year}"
    if start.year == end.year and start.month == end.month:
        return f"{start.strftime('%B')} {start.day}–{end.day}, {start.year}"
    if start.year == end.year:
        return f"{_fmt_day(start)} – {_fmt_day(end)}, {start.year}"
    return f"{_fmt_day(start)}, {start.year} – {_fmt_day(end)}, {end.year}"


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = (text or "").split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def fit_title(
    draw, text: str, max_width: int, max_lines: int = 3
) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, list[str]]:
    for size in range(70, 38, -2):
        font = _font(FONT_BOLD, size)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
    font = _font(FONT_BOLD, 38)
    return font, wrap_text(draw, text, font, max_width)[:max_lines]


def text_width(draw: ImageDraw.ImageDraw, text: str, font) -> float:
    return float(draw.textlength(text, font=font))


def draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font,
    fill,
) -> int:
    tw = text_width(draw, text, font)
    x = int((IMG_W - tw) / 2)
    draw.text((x, y), text, font=font, fill=fill)
    return int(getattr(font, "size", 28))


def draw_centered_tracked(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font,
    fill,
    tracking: float = 5.5,
) -> int:
    """Uppercase + letter-spacing for a poster-style location line."""
    chars = list((text or "").upper())
    if not chars:
        return 0
    widths = [text_width(draw, c if c != " " else " ", font) for c in chars]
    total = sum(widths) + tracking * max(0, len(chars) - 1)
    # Don't track spaces as hard — keep readable
    x = (IMG_W - total) / 2
    for c, w in zip(chars, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + tracking
    return int(getattr(font, "size", 24))


def draw_badge(base: Image.Image, text: str, x: int, y: int) -> int:
    """Draw a crisp rounded badge; returns width used."""
    font = _font(FONT_BOLD, 21)
    # Measure with textbbox so vertical centering is even across glyphs
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = probe.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 20, 12
    w, h = int(tw + pad_x * 2), int(th + pad_y * 2)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 240))
    tx = (w - tw) / 2 - bbox[0]
    ty = (h - th) / 2 - bbox[1]
    od.text((tx, ty), text, font=font, fill=(18, 18, 28, 255))
    base.alpha_composite(overlay, (x, y))
    return w


def generate_event_image(event: EventCard) -> str | None:
    c1, c2, c3 = pick_gradient(event.slug)
    canvas = make_gradient(c1, c2, c3)

    # Soft vignette + center glow for depth
    overlay = Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(100):
        alpha = int(100 * (i / 100))
        od.rectangle((0, IMG_H - 100 + i, IMG_W, IMG_H - 99 + i), fill=(0, 0, 0, alpha))
    canvas = Image.alpha_composite(canvas, overlay)

    draw = ImageDraw.Draw(canvas)

    # Logo top-right
    if os.path.isfile(LOGO_WHITE):
        logo = Image.open(LOGO_WHITE).convert("RGBA")
        ratio = LOGO_MAX_WIDTH / logo.width
        logo = logo.resize(
            (LOGO_MAX_WIDTH, max(1, int(logo.height * ratio))),
            Image.LANCZOS,
        )
        canvas.alpha_composite(logo, (IMG_W - MARGIN_X - logo.width, MARGIN_TOP))

    content_w = IMG_W - MARGIN_X * 2

    # Badges top-left
    badge_y = MARGIN_TOP + 4
    bx = MARGIN_X
    if event.speaking:
        bx += draw_badge(canvas, "Speaking", bx, badge_y) + 12
    if event.sponsored:
        draw_badge(canvas, "Sponsoring", bx, badge_y)

    draw = ImageDraw.Draw(canvas)
    title_font, title_lines = fit_title(draw, event.title, content_w)
    location = (event.location or "").strip()
    date_human = humanize_date_display(event.date_display)

    loc_font = _font(FONT_BOLD, 22)
    date_font = _font(FONT_REG, 30)

    title_line_h = int(getattr(title_font, "size", 56) * 1.12)
    loc_h = 34 if location else 0
    date_h = 40 if date_human else 0
    rule_h = 24 if (location or date_human) else 0
    loc_date_gap = 36 if (location and date_human) else 0
    block_h = (
        len(title_lines) * title_line_h
        + rule_h
        + loc_h
        + loc_date_gap
        + date_h
    )

    # Sit the stack lower than true center
    y = int(IMG_H * 0.58 - block_h / 2)
    y = max(badge_y + 100, min(y, IMG_H - 88 - block_h))

    for line in title_lines:
        draw_centered(draw, line, y, title_font, TEXT_WHITE)
        y += title_line_h

    if location or date_human:
        y += 20
        rule_w = 56
        rx = (IMG_W - rule_w) // 2
        draw.rectangle((rx, y, rx + rule_w, y + 2), fill=(255, 255, 255, 160))
        y += rule_h

        if location:
            draw_centered_tracked(draw, location, y, loc_font, TEXT_SOFT, tracking=6)
            y += loc_h + loc_date_gap

        if date_human:
            draw_centered(draw, date_human, y, date_font, TEXT_MUTED)

    # Footer
    foot = _font(FONT_REG, 18)
    draw_centered(draw, "percona.community/events", IMG_H - 46, foot, TEXT_FOOT)

    out_dir = os.path.join("assets", "events", event.slug)
    os.makedirs(out_dir, exist_ok=True)
    out_rel = f"events/{event.slug}/card.png"
    out_abs = os.path.join("assets", out_rel)
    canvas.convert("RGB").save(out_abs, "PNG", optimize=True)
    return out_rel
