import os
from datetime import date, datetime

from PIL import Image, ImageDraw, ImageFont

IMG_W = 1200
IMG_H = 630

FONT_BOLD = "tools/talks_images/fonts/Inter-Bold.ttf"
FONT_REG = "tools/talks_images/fonts/Inter-Regular.ttf"
LOGO_WHITE_PNG = "tools/talks_images/templates/logo-white.png"
BG_JPG = "tools/talks_images/templates/percona-community-talk-bg.jpg"

MARGIN_X = 80
MARGIN_TOP = 56
MARGIN_BOTTOM = 56
CONTENT_W = IMG_W - MARGIN_X * 2

BRAND_PURPLE = (101, 61, 244, 255)
PANEL_FILL = (28, 27, 30, 130)
PANEL_RADIUS = 20
PANEL_PAD = 28
CARD_PAD = 16
CARD_STRIPE_GAP = 28
CARD_FILL = (48, 47, 47, 230)
CARD_RADIUS = 14
STRIPE_WIDTH = 14
TEXT_WHITE = (255, 255, 255, 255)
TEXT_MUTED = (210, 210, 210, 255)

PHOTO_SIZE = 80
PHOTO_BORDER = 4
PHOTO_SUPER = 3
TITLE_BELOW_LOGO_GAP = 64


# -------------------------------
# Background
# -------------------------------

def load_background():
    """Cover-crop background to 1200×630."""
    bg = Image.open(BG_JPG).convert("RGB")
    src_w, src_h = bg.size
    scale = max(IMG_W / src_w, IMG_H / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - IMG_W) // 2
    top = (new_h - IMG_H) // 2
    return bg.crop((left, top, left + IMG_W, top + IMG_H)).convert("RGBA")


# -------------------------------
# Helpers
# -------------------------------

def crop_to_square(img):
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def circle_with_border(img, size, border=PHOTO_BORDER, supersample=PHOTO_SUPER):
    """High-quality circular avatar with white ring (supersampled)."""
    img = crop_to_square(img)
    s = supersample
    inner = size * s
    b = border * s

    if min(img.size) < inner:
        scale = inner / min(img.size)
        img = img.resize(
            (int(img.width * scale), int(img.height * scale)),
            Image.LANCZOS,
        )
        img = crop_to_square(img)

    img = img.resize((inner, inner), Image.LANCZOS)

    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, inner - 1, inner - 1), fill=255)

    photo = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    photo.paste(img.convert("RGBA"), (0, 0), mask)

    outer = inner + b * 2
    result = Image.new("RGBA", (outer, outer), (0, 0, 0, 0))
    ImageDraw.Draw(result).ellipse((0, 0, outer - 1, outer - 1), fill=(255, 255, 255, 255))
    result.paste(photo, (b, b), photo)

    final = size + border * 2
    return result.resize((final, final), Image.LANCZOS)


def draw_left_rounded_rect(draw, box, radius, fill):
    """Rectangle with rounded top-left and bottom-left corners only."""
    x1, y1, x2, y2 = box
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    if r <= 0:
        draw.rectangle(box, fill=fill)
        return
    draw.rectangle([x1 + r, y1, x2, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x1 + r, y2 - r], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill)
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill)


def draw_right_rounded_rect(draw, box, radius, fill):
    """Rectangle with rounded top-right and bottom-right corners only."""
    x1, y1, x2, y2 = box
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    if r <= 0:
        draw.rectangle(box, fill=fill)
        return
    draw.rectangle([x1, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x2 - r, y1 + r, x2, y2 - r], fill=fill)
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill)
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill)


_SMALL_LINE_STARTS = frozenset(
    {"a", "an", "the", "of", "or", "and", "to", "in", "on", "at", "for", "by", "with"}
)


def _greedy_wrap(draw, words, font, max_width):
    lines, line = [], ""
    for w in words:
        test = f"{line} {w}" if line else w
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def _score_title_lines(draw, lines, font, max_width):
    """Higher is better. Favors balance, breaks after ':', avoids weak line starts."""
    widths = [draw.textlength(ln, font=font) for ln in lines]
    if not widths or any(w > max_width + 0.5 for w in widths):
        return float("-inf")
    avg = sum(widths) / len(widths)
    variance = sum((w - avg) ** 2 for w in widths) / len(widths)
    score = -variance

    for ln in lines[:-1]:
        if ln.rstrip().endswith((":", "—", "–")):
            score += avg * avg * 0.45

    longest = max(widths)
    if widths[-1] < 0.5 * longest:
        score -= (longest - widths[-1]) ** 2 * 0.25

    for ln in lines[1:]:
        first = ln.split()[0].lower().strip("\"'“”")
        if first in _SMALL_LINE_STARTS:
            score -= avg * avg * 0.2

    return score


def wrap_lines(draw, text, font, max_width, *, balance=False):
    """Word-wrap. With balance=True (titles), pick a typographically better break."""
    if not text:
        return []
    words = text.split()
    greedy = _greedy_wrap(draw, words, font, max_width)
    if not balance or len(greedy) <= 1 or len(words) < 3:
        return greedy

    n_lines = len(greedy)
    # For 2-line titles, score every valid break. For longer titles, binary-search
    # a target width (CSS text-wrap: balance), then refine among nearby breaks.
    if n_lines == 2:
        best, best_score = greedy, _score_title_lines(draw, greedy, font, max_width)
        for i in range(1, len(words)):
            lines = [" ".join(words[:i]), " ".join(words[i:])]
            score = _score_title_lines(draw, lines, font, max_width)
            if score > best_score:
                best, best_score = lines, score
        return best

    lo, hi = 1, int(max_width)
    balanced = greedy
    while lo < hi:
        mid = (lo + hi) // 2
        trial = _greedy_wrap(draw, words, font, mid)
        if len(trial) <= n_lines:
            balanced = trial
            hi = mid
        else:
            lo = mid + 1

    # Prefer a punctuation break if it still fits in n_lines and scores better.
    best, best_score = balanced, _score_title_lines(draw, balanced, font, max_width)
    for i, w in enumerate(words[:-1]):
        if not w.endswith((":", "—", "–")):
            continue
        left, right = " ".join(words[: i + 1]), " ".join(words[i + 1 :])
        # Re-wrap each side greedily within max_width; accept if total lines == n.
        left_lines = _greedy_wrap(draw, left.split(), font, max_width)
        right_lines = _greedy_wrap(draw, right.split(), font, max_width)
        lines = left_lines + right_lines
        if len(lines) != n_lines:
            continue
        score = _score_title_lines(draw, lines, font, max_width)
        if score > best_score:
            best, best_score = lines, score
    return best


def text_height(draw, text, font, max_width, line_gap=6, *, balance=False):
    if not text:
        return 0
    lines = wrap_lines(draw, text, font, max_width, balance=balance)
    if not lines:
        return 0
    return len(lines) * (font.size + line_gap) - line_gap


def text_width_wrapped(draw, text, font, max_width, *, balance=False):
    if not text:
        return 0
    lines = wrap_lines(draw, text, font, max_width, balance=balance)
    return max((draw.textlength(ln, font=font) for ln in lines), default=0)


def draw_wrapped(draw, text, font, x, y, max_width, fill, line_gap=6, *, balance=False):
    lines = wrap_lines(draw, text, font, max_width, balance=balance)

    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += font.size + line_gap

    return y


def pick_title_font(title, *, large: bool = False):
    title_len = len(title)
    if large:
        if title_len <= 60:
            return ImageFont.truetype(FONT_BOLD, 58)
        if title_len <= 90:
            return ImageFont.truetype(FONT_BOLD, 50)
        if title_len <= 120:
            return ImageFont.truetype(FONT_BOLD, 44)
        return ImageFont.truetype(FONT_BOLD, 40)
    if title_len <= 60:
        return ImageFont.truetype(FONT_BOLD, 52)
    if title_len <= 90:
        return ImageFont.truetype(FONT_BOLD, 44)
    if title_len <= 120:
        return ImageFont.truetype(FONT_BOLD, 38)
    return ImageFont.truetype(FONT_BOLD, 34)


# Logo-bottom layout for talks on/after this date (larger type, balanced title wrap).
LAYOUT_LOGO_BOTTOM_FROM = date(2026, 9, 24)


def parse_iso_date(value) -> date | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        try:
            return datetime.strptime(text[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def talk_card_date(talk, post) -> date | None:
    """Best-effort talk date for layout selection."""
    for key in ("presentation_date", "event_date_start"):
        d = parse_iso_date(post.get(key))
        if d:
            return d
    d = parse_iso_date(getattr(talk, "event_date", None))
    if d:
        return d
    # Slug prefix: 2026-10-07-...
    return parse_iso_date(getattr(talk, "slug", ""))


def use_logo_bottom_layout(talk, post) -> bool:
    # Two speakers fill the footer; logo stays top-right (legacy layout).
    if len(talk.speakers) != 1:
        return False
    d = talk_card_date(talk, post)
    return d is not None and d >= LAYOUT_LOGO_BOTTOM_FROM


def resize_logo(max_width=240):
    logo = Image.open(LOGO_WHITE_PNG).convert("RGBA")
    ratio = max_width / logo.width
    new_h = int(logo.height * ratio)
    return logo.resize((max_width, new_h), Image.LANCZOS)


def format_presentation_date(date_str: str) -> str:
    """YYYY-MM-DD → October 7, 2026 (keep non-ISO as-is)."""
    text = (date_str or "").strip()
    if not text:
        return ""
    try:
        dt = datetime.strptime(text[:10], "%Y-%m-%d")
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}"
    except ValueError:
        return text


def build_meta(post):
    event = (post.get("event") or "").strip()
    date_raw = post.get("presentation_date") or post.get("event_date_start") or ""
    date = format_presentation_date(str(date_raw))
    time_str = (post.get("presentation_time") or "").strip()
    location = (post.get("event_location") or "").strip()
    room = (post.get("room") or "").strip()

    line1_parts = [p for p in (event, location) if p]
    line1 = " • ".join(line1_parts)

    line2_parts = [p for p in (date, time_str, room) if p]
    line2 = " · ".join(line2_parts)

    return line1, line2


def draw_meta_line1(draw, x, y, event, location, font_event, font_loc):
    """Event slightly larger; event and location on one line, all white."""
    if event:
        draw.text((x, y), event, font=font_event, fill=TEXT_WHITE)
        x += draw.textlength(event, font=font_event)
    if location:
        sep = " • " if event else ""
        draw.text((x, y + 2), sep + location, font=font_loc, fill=TEXT_WHITE)


def measure_speaker_card(draw, name, job, font_name, font_job, photo_size=PHOTO_SIZE, pad=CARD_PAD):
    text_gap = 10
    text_max_w = 380
    name_w = draw.textlength(name, font=font_name)
    job_w = text_width_wrapped(draw, job, font_job, text_max_w) if job else 0
    text_w = min(text_max_w, max(name_w, job_w))

    name_h = font_name.size
    job_h = text_height(draw, job, font_job, text_max_w, line_gap=4) if job else 0
    text_h = name_h + (6 + job_h if job else 0)

    photo_outer = photo_size + PHOTO_BORDER * 2
    inner_h = max(photo_outer, text_h)
    card_h = int(inner_h + pad * 2)
    card_w = int(pad + photo_outer + text_gap + text_w + CARD_STRIPE_GAP + STRIPE_WIDTH)
    return card_w, card_h, text_w


def render_speaker_card_layer(card_w, card_h):
    layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    body_w = card_w - STRIPE_WIDTH
    draw_left_rounded_rect(draw, (0, 0, body_w, card_h), CARD_RADIUS, CARD_FILL)
    draw_right_rounded_rect(
        draw, (body_w, 0, card_w, card_h), CARD_RADIUS, BRAND_PURPLE
    )
    return layer


def draw_speaker_card(img, x1, y1, photo_path, name, job, font_name, font_job, photo_size=PHOTO_SIZE):
    probe = ImageDraw.Draw(img)
    pad = CARD_PAD
    text_gap = 10
    text_max_w = 380

    card_w, card_h, _text_w = measure_speaker_card(
        probe, name, job, font_name, font_job, photo_size=photo_size
    )

    layer = render_speaker_card_layer(card_w, card_h)
    img.paste(layer, (x1, y1), layer)
    draw = ImageDraw.Draw(img)

    photo_outer = photo_size + PHOTO_BORDER * 2
    photo_x = x1 + pad
    photo_y = y1 + (card_h - photo_outer) // 2

    if photo_path and os.path.exists(photo_path):
        p = Image.open(photo_path).convert("RGB")
        p = circle_with_border(p, photo_size)
        img.paste(p, (photo_x, photo_y), p)

    text_x = photo_x + photo_outer + text_gap
    text_y = photo_y + 6

    draw.text((text_x, text_y), name, font=font_name, fill=TEXT_WHITE)
    if job:
        draw_wrapped(
            draw,
            job,
            font_job,
            text_x,
            text_y + font_name.size + 6,
            text_max_w,
            TEXT_MUTED,
            line_gap=4,
        )

    return img, card_w, card_h


def measure_meta_block(draw, post, font_event, font_loc, font_date):
    event = (post.get("event") or "").strip()
    location = (post.get("event_location") or "").strip()
    line1, line2 = build_meta(post)
    height = 0

    if not line1 and not line2:
        return 0, line1, line2, event, location

    height += 20
    if line1:
        if len(line1) > 70 or draw.textlength(line1, font=font_event) > CONTENT_W:
            height += text_height(draw, line1, font_event, CONTENT_W, line_gap=6) + 8
        else:
            height += font_event.size + 10
    if line2:
        height += font_date.size

    return height, line1, line2, event, location


def draw_content_panel(img, x1, y1, x2, y2):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (x1, y1, x2, y2), radius=PANEL_RADIUS, fill=PANEL_FILL
    )
    return Image.alpha_composite(img, layer)


# -------------------------------
# Main generator
# -------------------------------

def generate_talk_image(talk):
    import frontmatter

    post = frontmatter.load(talk.md_path)
    img = load_background()

    logo_bottom = use_logo_bottom_layout(talk, post)
    font_title = pick_title_font(talk.title, large=logo_bottom)
    speaker_photo = PHOTO_SIZE
    if logo_bottom:
        font_event = ImageFont.truetype(FONT_BOLD, 36)
        font_loc = ImageFont.truetype(FONT_REG, 32)
        font_date = ImageFont.truetype(FONT_REG, 30)
        font_speaker = ImageFont.truetype(FONT_BOLD, 30)
        font_job = ImageFont.truetype(FONT_REG, 23)
        speaker_photo = 92
        logo = resize_logo(220)
        title_y = MARGIN_TOP  # replaced below after measuring speaker band
    else:
        font_event = ImageFont.truetype(FONT_BOLD, 32)
        font_loc = ImageFont.truetype(FONT_REG, 28)
        font_date = ImageFont.truetype(FONT_REG, 26)
        font_speaker = ImageFont.truetype(FONT_BOLD, 26)
        font_job = ImageFont.truetype(FONT_REG, 20)
        logo = resize_logo(240)
        logo_w, logo_h = logo.size
        logo_x = IMG_W - MARGIN_X - logo_w
        logo_y = MARGIN_TOP
        title_y = logo_y + logo_h + TITLE_BELOW_LOGO_GAP

    title_max_w = CONTENT_W

    probe = Image.new("RGBA", (IMG_W, IMG_H))
    pdraw = ImageDraw.Draw(probe)
    title_h = text_height(pdraw, talk.title, font_title, title_max_w, line_gap=8, balance=True)
    meta_h, line1, line2, event, location = measure_meta_block(
        pdraw, post, font_event, font_loc, font_date
    )

    card_gap = 20
    card_y2 = IMG_H - MARGIN_BOTTOM
    speaker_layout = []

    for i, sp in enumerate(talk.speakers[:2]):
        photo = talk.speaker_images[i] if i < len(talk.speaker_images) else None
        sp_post = frontmatter.load(f"content/contributors/{sp}.md")
        name = sp_post.get("fullname", sp)
        job = sp_post.get("job") or sp_post.get("tagline") or ""

        _, card_h, _ = measure_speaker_card(
            pdraw, name, job, font_speaker, font_job, photo_size=speaker_photo
        )
        card_y1 = int(card_y2 - card_h)
        speaker_layout.append(
            {
                "x": MARGIN_X if i == 0 else None,
                "y1": card_y1,
                "photo": photo,
                "name": name,
                "job": job,
            }
        )

    if logo_bottom:
        # Bottom-align title/meta just above the speaker row so the block
        # sits near the vertical center of the card.
        # measure_meta_block() already includes a 20px leading gap — replace it.
        title_meta_gap = 24
        meta_content_h = max(meta_h - 20, 0) if (line1 or line2) else 0
        text_block_h = title_h + title_meta_gap + meta_content_h
        # Breathing room above the larger speaker card (~logo_bottom photo 92).
        gap_above_speakers = 64
        band_bottom = (
            speaker_layout[0]["y1"] - gap_above_speakers
            if speaker_layout
            else IMG_H - MARGIN_BOTTOM
        )
        title_y = band_bottom - text_block_h
        title_y = max(title_y, MARGIN_TOP)

    meta_y = title_y + title_h + meta_h
    content_bottom = meta_y
    for item in speaker_layout:
        content_bottom = max(content_bottom, card_y2)

    card_x = MARGIN_X
    for item in speaker_layout:
        item["x"] = card_x
        card_w, _, _ = measure_speaker_card(
            pdraw,
            item["name"],
            item["job"],
            font_speaker,
            font_job,
            photo_size=speaker_photo,
        )
        card_x += card_w + card_gap

    if logo_bottom:
        logo_w, logo_h = logo.size
        logo_x = IMG_W - MARGIN_X - logo_w
        # Align logo vertically with the speaker card row.
        if speaker_layout:
            sp_y1 = speaker_layout[0]["y1"]
            _, sp_h, _ = measure_speaker_card(
                pdraw,
                speaker_layout[0]["name"],
                speaker_layout[0]["job"],
                font_speaker,
                font_job,
                photo_size=speaker_photo,
            )
            logo_y = int(sp_y1 + (sp_h - logo_h) / 2)
        else:
            logo_y = IMG_H - MARGIN_BOTTOM - logo_h

    panel_x1 = MARGIN_X - PANEL_PAD
    panel_x2 = IMG_W - MARGIN_X + PANEL_PAD
    if logo_bottom:
        # Panel hugs the text block so empty dark space above the title doesn't
        # make the copy read as top-aligned; text itself is mid-band.
        panel_y1 = title_y - PANEL_PAD
        panel_y2 = content_bottom + PANEL_PAD
    else:
        panel_y1 = title_y - PANEL_PAD
        panel_y2 = content_bottom + PANEL_PAD
    img = draw_content_panel(img, panel_x1, panel_y1, panel_x2, panel_y2)

    draw = ImageDraw.Draw(img)
    y = draw_wrapped(
        draw,
        talk.title,
        font_title,
        MARGIN_X,
        title_y,
        title_max_w,
        TEXT_WHITE,
        line_gap=8,
        balance=True,
    )

    if line1 or line2:
        y += 24 if logo_bottom else 20
        if line1:
            if len(line1) > 70 or draw.textlength(line1, font=font_event) > CONTENT_W:
                y = draw_wrapped(
                    draw, line1, font_event, MARGIN_X, y, CONTENT_W, TEXT_WHITE, line_gap=6
                )
                y += 8
            else:
                draw_meta_line1(draw, MARGIN_X, y, event, location, font_event, font_loc)
                y += font_event.size + 10
        if line2:
            draw.text((MARGIN_X, y), line2, font=font_date, fill=TEXT_WHITE)

    for item in speaker_layout:
        img, card_w, card_h = draw_speaker_card(
            img,
            item["x"],
            item["y1"],
            item["photo"],
            item["name"],
            item["job"],
            font_speaker,
            font_job,
            photo_size=speaker_photo,
        )
        item["w"] = card_w
        item["h"] = card_h

    img.paste(logo, (logo_x, logo_y), logo)

    out_dir = f"assets/talks/{talk.year}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{talk.slug}.png"
    img.convert("RGB").save(out_path, optimize=True)

    return f"talks/{talk.year}/{talk.slug}.png"
