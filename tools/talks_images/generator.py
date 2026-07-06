import os
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


def text_height(draw, text, font, max_width, line_gap=6):
    if not text:
        return 0
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    if not lines:
        return 0
    return len(lines) * (font.size + line_gap) - line_gap


def text_width_wrapped(draw, text, font, max_width):
    if not text:
        return 0
    words = text.split()
    lines = []
    line = ""
    max_w = 0
    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    for ln in lines:
        max_w = max(max_w, draw.textlength(ln, font=font))
    return max_w


def draw_wrapped(draw, text, font, x, y, max_width, fill, line_gap=6):
    words = text.split()
    lines = []
    line = ""

    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)

    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += font.size + line_gap

    return y


def pick_title_font(title):
    title_len = len(title)
    if title_len <= 60:
        return ImageFont.truetype(FONT_BOLD, 52)
    if title_len <= 90:
        return ImageFont.truetype(FONT_BOLD, 44)
    if title_len <= 120:
        return ImageFont.truetype(FONT_BOLD, 38)
    return ImageFont.truetype(FONT_BOLD, 34)


def resize_logo(max_width=240):
    logo = Image.open(LOGO_WHITE_PNG).convert("RGBA")
    ratio = max_width / logo.width
    new_h = int(logo.height * ratio)
    return logo.resize((max_width, new_h), Image.LANCZOS)


def build_meta(post):
    event = (post.get("event") or "").strip()
    date = post.get("presentation_date") or post.get("event_date_start") or ""
    time_str = (post.get("presentation_time") or "").strip()
    location = (post.get("event_location") or "").strip()

    line1_parts = [p for p in (event, location) if p]
    line1 = " • ".join(line1_parts)

    line2 = date
    if time_str:
        line2 = f"{date}, {time_str}" if date else time_str

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


def draw_speaker_card(img, x1, y1, photo_path, name, job, font_name, font_job):
    probe = ImageDraw.Draw(img)
    pad = CARD_PAD
    text_gap = 10
    text_max_w = 380

    card_w, card_h, _text_w = measure_speaker_card(
        probe, name, job, font_name, font_job
    )

    layer = render_speaker_card_layer(card_w, card_h)
    img.paste(layer, (x1, y1), layer)
    draw = ImageDraw.Draw(img)

    photo_outer = PHOTO_SIZE + PHOTO_BORDER * 2
    photo_x = x1 + pad
    photo_y = y1 + (card_h - photo_outer) // 2

    if photo_path and os.path.exists(photo_path):
        p = Image.open(photo_path).convert("RGB")
        p = circle_with_border(p, PHOTO_SIZE)
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

    font_title = pick_title_font(talk.title)
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
    title_h = text_height(pdraw, talk.title, font_title, title_max_w, line_gap=8)
    meta_h, line1, line2, event, location = measure_meta_block(
        pdraw, post, font_event, font_loc, font_date
    )
    meta_y = title_y + title_h + meta_h
    content_bottom = meta_y

    card_gap = 20
    card_y2 = IMG_H - MARGIN_BOTTOM
    speaker_layout = []

    for i, sp in enumerate(talk.speakers[:2]):
        photo = talk.speaker_images[i] if i < len(talk.speaker_images) else None
        sp_post = frontmatter.load(f"content/contributors/{sp}.md")
        name = sp_post.get("fullname", sp)
        job = sp_post.get("job") or sp_post.get("tagline") or ""

        _, card_h, _ = measure_speaker_card(pdraw, name, job, font_speaker, font_job)
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
        content_bottom = max(content_bottom, card_y2)

    card_x = MARGIN_X
    for item in speaker_layout:
        item["x"] = card_x
        card_w, _, _ = measure_speaker_card(
            pdraw, item["name"], item["job"], font_speaker, font_job
        )
        card_x += card_w + card_gap

    panel_x1 = MARGIN_X - PANEL_PAD
    panel_x2 = IMG_W - MARGIN_X + PANEL_PAD
    panel_y1 = title_y - PANEL_PAD
    panel_y2 = content_bottom + PANEL_PAD
    img = draw_content_panel(img, panel_x1, panel_y1, panel_x2, panel_y2)

    draw = ImageDraw.Draw(img)
    y = draw_wrapped(
        draw, talk.title, font_title, MARGIN_X, title_y, title_max_w, TEXT_WHITE, line_gap=8
    )

    if line1 or line2:
        y += 20
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
        )
        item["w"] = card_w
        item["h"] = card_h

    img.paste(logo, (logo_x, logo_y), logo)

    out_dir = f"assets/talks/{talk.year}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{talk.slug}.png"
    img.convert("RGB").save(out_path, optimize=True)

    return f"talks/{talk.year}/{talk.slug}.png"
