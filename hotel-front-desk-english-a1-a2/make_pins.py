"""Generate 3 Pinterest pins (1000x1500) for Hotel Front Desk English A1-A2."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PRODUCT = os.path.join(HERE, "..", "..", "products", "hotel-front-desk-english-a1-a2")
PREVIEW = os.path.join(PRODUCT, "preview")

W, H = 1000, 1500
NAVY = (35, 70, 106)
NAVY_DARK = (24, 50, 78)
ORANGE = (224, 129, 44)
LIGHT = (238, 240, 244)
WHITE = (255, 255, 255)
INK = (33, 37, 41)
MUTED = (160, 178, 200)

FONT_DIR = r"C:\Windows\Fonts"
REG = os.path.join(FONT_DIR, "arial.ttf")
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def page(n):
    return Image.open(os.path.join(PREVIEW, f"hotel-front-desk-english-a1-a2_A4_p{n}.png")).convert("RGB")


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, f, x, y, fill, gap=1.12, center=False):
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * gap)
    for ln in lines:
        lx = (W - text_w(d, ln, f)) // 2 if center else x
        d.text((lx, y), ln, font=f, fill=fill)
        y += lh
    return y


def pill(d, text, f, x, y, bg, fg, pad_x=26, pad_y=12, center=False):
    tw = text_w(d, text, f)
    asc, desc = f.getmetrics()
    h = asc + desc + pad_y * 2
    w = tw + pad_x * 2
    if center:
        x = (W - w) // 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=f, fill=fg)
    return y + h


def paste_page(canvas, img, w, xy, angle=0, shadow=True):
    h = int(img.height * w / img.width)
    pg = img.resize((w, h), Image.LANCZOS)
    pg_rgba = pg.convert("RGBA")
    if angle:
        pg_rgba = pg_rgba.rotate(angle, expand=True, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new("RGBA", pg_rgba.size, (0, 0, 0, 0))
        mask = pg_rgba.split()[3].point(lambda a: 90 if a > 0 else 0)
        sh.putalpha(mask)
        big = Image.new("RGBA", (pg_rgba.width + 60, pg_rgba.height + 60), (0, 0, 0, 0))
        big.paste(sh, (30, 30), sh)
        big = big.filter(ImageFilter.GaussianBlur(14))
        canvas.alpha_composite(big, (xy[0] - 30 + 10, xy[1] - 30 + 14))
    canvas.alpha_composite(pg_rgba, xy)
    return pg_rgba.size


def brand(d, color, line_color):
    f = font(BOLD, 30)
    s = "Neat Sheets Studio"
    y = H - 70
    d.line([(W // 2 - 220, y - 22), (W // 2 + 220, y - 22)], fill=line_color, width=2)
    d.text(((W - text_w(d, s, f)) // 2, y - 6), s, font=f, fill=color)


# ---------- Pin 1: overview + overlapping pages ----------
def pin1():
    c = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(c)
    y = pill(d, "ENGLISH FOR WORK  ·  A1–A2", font(BOLD, 32), 0, 70, ORANGE, WHITE, center=True)
    y = draw_lines(d, ["Hotel Front Desk", "English"], font(BOLD, 104), 0, y + 30, WHITE, gap=1.05, center=True)
    y = draw_lines(d, ["Printable Workbook for", "Hotel & Guesthouse Staff"], font(REG, 46), 0, y + 14, WHITE, gap=1.15, center=True)
    top = y + 40
    # three real pages fanned out
    paste_page(c, page(5), 430, (520, top + 40), angle=-6)
    paste_page(c, page(3), 430, (60, top + 40), angle=6)
    paste_page(c, page(1), 470, (265, top))
    d = ImageDraw.Draw(c)
    # bottom band
    d.rectangle([0, H - 250, W, H], fill=NAVY_DARK)
    f = font(BOLD, 40)
    s = "6 units  ·  35 pages  ·  Answer key"
    d.text(((W - text_w(d, s, f)) // 2, H - 215), s, font=f, fill=WHITE)
    f2 = font(REG, 32)
    s2 = "Role-play cards  ·  A4 + US Letter PDF"
    d.text(((W - text_w(d, s2, f2)) // 2, H - 160), s2, font=f2, fill=MUTED)
    brand(d, WHITE, ORANGE)
    return c


# ---------- Pin 2: one page big + key benefit ----------
def pin2():
    c = Image.new("RGBA", (W, H), LIGHT + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 430], fill=NAVY)
    y = pill(d, "HOTEL ENGLISH  ·  A1–A2", font(BOLD, 30), 0, 55, ORANGE, WHITE, center=True)
    y = draw_lines(d, ["Front Desk", "Role-Play Cards"], font(BOLD, 96), 0, y + 26, WHITE, gap=1.05, center=True)
    # big page
    pw = 740
    paste_page(c, page(5), pw, ((W - pw) // 2, 380))
    d = ImageDraw.Draw(c)
    # benefit band
    band_top = H - 330
    d.rectangle([0, band_top, W, H], fill=NAVY)
    f = font(BOLD, 48)
    lines = ["Staff + guest cards in every unit", "to practice what you say to guests"]
    draw_lines(d, lines, f, 0, band_top + 55, WHITE, gap=1.18, center=True)
    brand(d, WHITE, ORANGE)
    return c


# ---------- Pin 3: what's inside list ----------
def pin3():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 360], fill=NAVY)
    y = pill(d, "WHAT'S INSIDE", font(BOLD, 32), 0, 55, ORANGE, WHITE, center=True)
    y = draw_lines(d, ["Hotel Front Desk", "English Workbook"], font(BOLD, 88), 0, y + 24, WHITE, gap=1.05, center=True)

    items = [
        ("6 units, 24 worksheets", "Greetings to check-out"),
        ("Picture match + gap-fill", "8 words and a dialogue per unit"),
        ("Cut-out role-play cards", "Staff card + guest card"),
        ("Respond & Write", "Multiple choice + 'I can' check"),
        ("Vocabulary + phone English", "Polite requests, spelling alphabet"),
        ("Answer key + teacher notes", "6 pages, plus a progress check"),
    ]
    # page thumbnails on the right
    paste_page(c, page(3), 290, (672, 430), angle=-4)
    paste_page(c, page(6), 290, (662, 880), angle=3)
    d = ImageDraw.Draw(c)
    fb, fr = font(BOLD, 36), font(REG, 29)
    y = 420
    for head, sub in items:
        d.ellipse([56, y + 7, 82, y + 33], fill=ORANGE)
        hl = wrap(d, head, fb, 520)
        yy = draw_lines(d, hl, fb, 100, y, NAVY, gap=1.08)
        sl = wrap(d, sub, fr, 520)
        yy = draw_lines(d, sl, fr, 100, yy + 2, INK, gap=1.12)
        y = yy + 30
    # footer band
    d.rectangle([0, H - 170, W, H], fill=NAVY)
    f = font(BOLD, 36)
    s = "35-page PDF  ·  A4 + US Letter"
    d.text(((W - text_w(d, s, f)) // 2, H - 150), s, font=f, fill=WHITE)
    brand(d, MUTED, ORANGE)
    return c


if __name__ == "__main__":
    for name, fn in [("pin1.png", pin1), ("pin2.png", pin2), ("pin3.png", pin3)]:
        img = fn().convert("RGB")
        assert img.size == (W, H)
        img.save(os.path.join(HERE, name))
        print("saved", name)
