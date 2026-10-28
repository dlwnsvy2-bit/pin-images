"""Pinterest pins for the Homeschool Hours & Attendance Record Workbook (1000x1500, Pillow)."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PRODUCT = os.path.join(HERE, "..", "..", "products", "homeschool-hours-attendance-workbook")
PREVIEW = os.path.join(PRODUCT, "preview")

W, H = 1000, 1500
TEAL = (30, 90, 110)
TEAL_DARK = (22, 68, 84)
ORANGE = (217, 130, 43)
CREAM = (246, 230, 204)
LIGHT = (244, 244, 244)
INK = (34, 40, 46)
WHITE = (255, 255, 255)

FONT_REG = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def page(n):
    return Image.open(os.path.join(PREVIEW, f"Homeschool_Hours_Attendance_Printable_A4_p{n}.png")).convert("RGB")


def fit_width(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


def paste_with_shadow(canvas, img, xy, angle=0, border=True):
    """Paste a page with a thin border and soft drop shadow; optional rotation."""
    if border:
        framed = Image.new("RGB", (img.width + 2, img.height + 2), (200, 200, 200))
        framed.paste(img, (1, 1))
        img = framed
    img = img.convert("RGBA")
    if angle:
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True)
    pad = 40
    shadow = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    alpha = img.split()[3].point(lambda a: 90 if a else 0)
    shadow.paste((0, 0, 0, 255), (pad, pad), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    x, y = xy
    canvas.alpha_composite(shadow, (x - pad + 8, y - pad + 14))
    canvas.alpha_composite(img, (x, y))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, gap, center=False):
    for line in lines:
        lx = (W - draw.textlength(line, font=fnt)) / 2 if center else x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += gap
    return y


def brand(draw, color):
    f = font(30, True)
    t = "Neat Sheets Studio"
    draw.text(((W - draw.textlength(t, font=f)) / 2, H - 70), t, font=f, fill=color)


# ---------- Pin 1: product overview + overlapping page previews ----------
def pin1():
    c = Image.new("RGBA", (W, H), LIGHT + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 560], fill=TEAL)

    d.text((70, 70), "EXCEL / GOOGLE SHEETS + PRINTABLE PDF", font=font(30, True), fill=CREAM)
    y = draw_lines(d, ["Homeschool Hours", "& Attendance", "Record Workbook"], font(86, True), 70, 125, WHITE, 100)
    d.text((70, y + 22), "Auto-totals for up to 5 kids", font=font(42), fill=CREAM)

    # three real pages fanned out
    p_cover = fit_width(page(1), 440)
    p_goals = fit_width(page(4), 440)
    p_example = fit_width(page(3), 460)
    paste_with_shadow(c, p_cover, (25, 625), angle=5)
    paste_with_shadow(c, p_goals, (500, 625), angle=-5)
    paste_with_shadow(c, p_example, (370, 720), angle=0)

    d = ImageDraw.Draw(c)
    d.rectangle([0, H - 110, W, H], fill=TEAL_DARK)
    brand(d, CREAM)
    return c.convert("RGB")


# ---------- Pin 2: one page large + one key benefit ----------
def pin2():
    c = Image.new("RGBA", (W, H), TEAL + (255,))
    d = ImageDraw.Draw(c)

    y = draw_lines(d, ["Track Homeschool", "Hours by Month"], font(84, True), 0, 60, WHITE, 98, center=True)
    benefit = "Core & non-core subtotals + year-to-date total"
    for line in wrap(d, benefit, font(38), 880):
        d.text(((W - d.textlength(line, font=font(38))) / 2, y + 14), line, font=font(38), fill=CREAM)
        y += 50

    big = fit_width(page(3), 700)
    top = y + 55
    paste_with_shadow(c, big, ((W - big.width) // 2, top))

    d = ImageDraw.Draw(c)
    tag = "Filled-in example page"
    tf = font(28, True)
    tw = d.textlength(tag, font=tf)
    d.rounded_rectangle([(W - tw) / 2 - 22, top - 26, (W + tw) / 2 + 22, top + 24], 24, fill=ORANGE)
    d.text(((W - tw) / 2, top - 16), tag, font=tf, fill=WHITE)

    d.rectangle([0, H - 110, W, H], fill=TEAL_DARK)
    brand(d, CREAM)
    return c.convert("RGB")


# ---------- Pin 3: "What's inside" list ----------
def pin3():
    c = Image.new("RGBA", (W, H), LIGHT + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 300], fill=TEAL)
    d.text((70, 60), "What's Inside", font=font(96, True), fill=WHITE)
    d.text((70, 185), "Homeschool Hours & Attendance Workbook", font=font(40), fill=CREAM)

    items = [
        ("Spreadsheet", "Auto-totals for up to 5 kids (Excel / Google Sheets)"),
        ("Daily Log", "Drop-down lists for child, subject & attendance code"),
        ("Dashboard", "Compare all kids with a 'Behind pace' flag"),
        ("Calendar", "12-month attendance calendar, coloured by code"),
        ("Printable PDF", "23 pages in A4 and US Letter"),
        ("Monthly logs", "12 hour logs, August to July"),
        ("Records", "Reading log, field trips, portfolio, year-end summary"),
    ]
    y = 335
    hf, bf = font(38, True), font(30)
    for head, body in items:
        d.ellipse([70, y + 9, 92, y + 31], fill=ORANGE)
        d.text((115, y), head, font=hf, fill=TEAL)
        lines = wrap(d, body, bf, 820)
        yy = y + 46
        for line in lines:
            d.text((115, yy), line, font=bf, fill=INK)
            yy += 36
        y = yy + 14

    # strip of real pages
    tw = 200
    thumbs = [fit_width(page(n), tw) for n in (2, 5, 4)]
    th = thumbs[0].height
    gap = (W - 3 * tw) // 4
    ty = H - 140 - th
    for i, t in enumerate(thumbs):
        paste_with_shadow(c, t, (gap + i * (tw + gap), ty))

    d = ImageDraw.Draw(c)
    d.rectangle([0, H - 110, W, H], fill=TEAL_DARK)
    brand(d, CREAM)
    return c.convert("RGB"), y, ty


if __name__ == "__main__":
    pin1().save(os.path.join(HERE, "pin1.png"))
    pin2().save(os.path.join(HERE, "pin2.png"))
    img, list_end, thumbs_top = pin3()
    if list_end > thumbs_top - 20:
        print(f"WARNING pin3: list ends at {list_end}, thumbnails start at {thumbs_top}")
    img.save(os.path.join(HERE, "pin3.png"))
    print("done")
