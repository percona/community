import os
from PIL import Image, ImageDraw, ImageFont, ImageColor

IMG_W = 1200
IMG_H = 630

FONT_BOLD = "tools/talks_images/fonts/Inter-Bold.ttf"
FONT_REG = "tools/talks_images/fonts/Inter-Regular.ttf"
LOGO_PNG = "tools/talks_images/templates/logo.png"


# -------------------------------
# Gradient selection
# -------------------------------

def pick_gradient(tags):
    if not tags:
        return ("#1c3754", "#026dcf")

    t = tags[0].lower()

    if "mongo" in t:
        return ("#14584B", "#59DAC1")
    if "postgres" in t or "postgresql" in t:
        return ("#4B5468", "#439EFF")
    if "kubernetes" in t or "cloudnative" in t or "operators" in t:
        return ("#127AE8", "#0E1A53")
    if "mysql" in t:
        return ("#0E5FB5", "#30D1B2")
    if "pmm" in t:
        return ("#8C2F05", "#EA4D0F")
    if "valkey" in t:
        return ("#0E5FB5", "#62AEFF")

    return ("#1c3754", "#026dcf")


def diagonal_gradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    r1, g1, b1 = ImageColor.getrgb(c1)
    r2, g2, b2 = ImageColor.getrgb(c2)

    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            draw.point((x, y), (r, g, b))

    return img


# -------------------------------
# Helpers
# -------------------------------

def crop_to_square(img):
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def circle_with_border(img, size, border=6):
    img = crop_to_square(img)
    img = img.resize((size, size))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    circle = Image.new("RGBA", (size, size))
    circle.paste(img, (0, 0), mask)

    border_size = size + border * 2
    border_img = Image.new("RGBA", (border_size, border_size), (255, 255, 255, 0))
    border_mask = Image.new("L", (border_size, border_size), 0)
    draw2 = ImageDraw.Draw(border_mask)
    draw2.ellipse((0, 0, border_size, border_size), fill=255)

    border_img.paste((255, 255, 255), (0, 0), border_mask)
    border_img.paste(circle, (border, border), circle)

    return border_img


def draw_wrapped(draw, text, font, x, y, max_width, fill):
    words = text.split()
    lines = []
    line = ""

    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)

    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + 6

    return y


def pick_meta_font(draw, text, max_width):
    for size in [32, 30, 28, 26, 24]:
        font = ImageFont.truetype(FONT_REG, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
    return ImageFont.truetype(FONT_REG, 22)


# -------------------------------
# Main generator
# -------------------------------

def generate_talk_image(talk):
    import frontmatter
    post = frontmatter.load(talk.md_path)

    event = post.get("event", "")
    date = post.get("event_date_start", "")
    location = post.get("event_location", "")
    tags = post.get("talk_tags", [])

    c1, c2 = pick_gradient(tags)
    img = diagonal_gradient(IMG_W, IMG_H, c1, c2)
    draw = ImageDraw.Draw(img)

    font_speaker = ImageFont.truetype(FONT_BOLD, 32)
    font_job = ImageFont.truetype(FONT_REG, 26)
    font_talk = ImageFont.truetype(FONT_BOLD, 40)

    # Logo
    logo = Image.open(LOGO_PNG).convert("RGBA")
    logo = logo.resize((343, 73))
    logo_x = 80
    logo_y = 64
    img.paste(logo, (logo_x, logo_y), logo)

    # "Talks" label
    draw.text((IMG_W - 180, 64), "Talks", font=font_talk, fill="white")

    # Title
    title_len = len(talk.title)
    if title_len <= 60:
        font_title = ImageFont.truetype(FONT_BOLD, 52)
    elif title_len <= 90:
        font_title = ImageFont.truetype(FONT_BOLD, 44)
    elif title_len <= 120:
        font_title = ImageFont.truetype(FONT_BOLD, 38)
    else:
        font_title = ImageFont.truetype(FONT_BOLD, 36)

    title_y = logo_y + 73 + 60
    y = draw_wrapped(draw, talk.title, font_title, 80, title_y, 1000, "white")

    # Event line
    meta_parts = []
    if event:
        meta_parts.append(event)
    if date:
        meta_parts.append(date)
    if location:
        meta_parts.append(location)

    meta_line = " • ".join(meta_parts)
    max_meta_width = 1040
    font_meta_dynamic = pick_meta_font(draw, meta_line, max_meta_width)

    draw.text((80, y + 10), meta_line, font=font_meta_dynamic, fill="white")
    y += 80

    # Speakers
    count = len(talk.speaker_images)
    if count == 0:
        return

    # One speaker
    if count == 1:
        size = 160
        photo = talk.speaker_images[0]
        if photo and os.path.exists(photo):
            p = Image.open(photo).convert("RGB")
            p = circle_with_border(p, size)
            img.paste(p, (80, IMG_H - size - 64), p)

        sp = talk.speakers[0]
        sp_post = frontmatter.load(f"content/contributors/{sp}.md")
        name = sp_post.get("fullname", sp)
        job = sp_post.get("job") or sp_post.get("tagline") or ""

        tx = 80 + size + 40
        ty = IMG_H - size - 20

        draw.text((tx, ty), name, font=font_speaker, fill="white")
        draw.text((tx, ty + 40), job, font=font_job, fill="white")

    # Two speakers
    elif count == 2:
        size = 100
        speakers_y = y + 40

        left_x = 80
        right_x = 600

        positions = [
            (left_x, speakers_y),
            (right_x, speakers_y)
        ]

        text_max_width = 360

        for i, sp in enumerate(talk.speakers[:2]):
            photo = talk.speaker_images[i]
            if photo and os.path.exists(photo):
                p = Image.open(photo).convert("RGB")
                p = circle_with_border(p, size)
                img.paste(p, positions[i], p)

            sp_post = frontmatter.load(f"content/contributors/{sp}.md")
            name = sp_post.get("fullname", sp)
            job = sp_post.get("job") or sp_post.get("tagline") or ""

            px, py = positions[i]
            tx = px + size + 20
            ty = py + 20

            draw_wrapped(draw, name, font_speaker, tx, ty, text_max_width, "white")
            draw_wrapped(draw, job, font_job, tx, ty + 36, text_max_width, "white")

    # Save
    out_dir = f"assets/talks/{talk.year}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{talk.slug}.png"
    img.save(out_path)

    return f"talks/{talk.year}/{talk.slug}.png"
