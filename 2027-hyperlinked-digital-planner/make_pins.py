"""Pinterest pins for the 2027 Hyperlinked Digital Planner (1000x1500, Pillow)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[1] / "products" / "2027-hyperlinked-digital-planner"
PREV = PROD / "preview"
EXTRA = PREV / "extra"

W, H = 1000, 1500
NAVY = (36, 71, 107)
ORANGE = (217, 115, 58)
INK = (43, 43, 43)
GREY = (110, 110, 110)
BG = (242, 242, 242)
WHITE = (255, 255, 255)

FONT_DIR = Path("C:/Windows/Fonts")
BOLD = str(FONT_DIR / "segoeuib.ttf")
REG = str(FONT_DIR / "segoeui.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def page(name):
    p = EXTRA / name if not name.startswith("2027_") else PREV / name
    return Image.open(p).convert("RGB")


def framed(img, width, border=3):
    """Resize a page to width and give it a thin grey border."""
    h = round(img.height * width / img.width)
    img = img.resize((width, h), Image.LANCZOS)
    out = Image.new("RGB", (width + 2 * border, h + 2 * border), (200, 200, 200))
    out.paste(img, (border, border))
    return out


def paste_shadow(canvas, img, xy, radius=14, offset=(0, 10), alpha=90):
    x, y = xy
    pad = radius * 3
    sh = Image.new("L", (img.width + 2 * pad, img.height + 2 * pad), 0)
    ImageDraw.Draw(sh).rectangle([pad, pad, pad + img.width, pad + img.height], fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    black = Image.new("RGB", sh.size, (0, 0, 0))
    canvas.paste(black, (x - pad + offset[0], y - pad + offset[1]), sh)
    canvas.paste(img, (x, y))


def center_text(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def brand(d, dark=False):
    f = font(REG, 30)
    center_text(d, H - 62, "Neat Sheets Studio", f, WHITE if dark else GREY)


# ---------------------------------------------------------------- pin 1
def pin1():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 560], fill=NAVY)
    center_text(d, 40, "2027", font(BOLD, 190), WHITE)
    center_text(d, 285, "Hyperlinked", font(BOLD, 92), WHITE)
    center_text(d, 395, "Digital Planner", font(BOLD, 92), WHITE)
    d.rectangle([W / 2 - 60, 520, W / 2 + 60, 528], fill=ORANGE)

    # three real pages, cascaded
    pages = [("2027_Hyperlinked_Digital_Planner_Monday_Start_p1.png", (70, 605)),
             ("mon_m2.png", (230, 830)),
             ("mon_d73.png", (130, 1040))]
    for name, xy in pages:
        paste_shadow(im, framed(page(name), 640), xy)

    d.rectangle([0, H - 160, W, H], fill=NAVY)
    center_text(d, H - 140, "493 linked pages  \u00b7  GoodNotes & Notability", font(BOLD, 36), WHITE)
    brand(d, dark=True)
    im.save(HERE / "pin1.png")


# ---------------------------------------------------------------- pin 2
def pin2():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    center_text(d, 60, "2027 Digital", font(BOLD, 112), NAVY)
    center_text(d, 195, "Planner", font(BOLD, 112), NAVY)
    center_text(d, 350, "Yearly \u00b7 Monthly \u00b7 Weekly \u00b7 Daily", font(REG, 44), INK)

    pg = framed(page("mon_m2.png"), 900)
    paste_shadow(im, pg, ((W - pg.width) // 2, 450))

    y = 450 + pg.height + 60
    d.rounded_rectangle([60, y, W - 60, y + 210], radius=28, fill=ORANGE)
    center_text(d, y + 28, "Tap any date to open", font(BOLD, 64), WHITE)
    center_text(d, y + 110, "its daily page", font(BOLD, 64), WHITE)
    brand(d)
    im.save(HERE / "pin2.png")


# ---------------------------------------------------------------- pin 3
def pin3():
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 330], fill=NAVY)
    center_text(d, 45, "What's Inside the", font(BOLD, 80), WHITE)
    center_text(d, 150, "2027 Digital Planner", font(BOLD, 80), WHITE)
    d.rectangle([W / 2 - 60, 280, W / 2 + 60, 288], fill=ORANGE)

    items = [("1", "year-at-a-glance calendar"),
             ("12", "month calendars"),
             ("12", "monthly plan pages"),
             ("53", "weekly pages"),
             ("365", "daily pages"),
             ("12", "habit trackers"),
             ("12", "budget trackers"),
             ("12", "meal & grocery pages"),
             ("10", "notes pages")]
    fn, ft = font(BOLD, 50), font(REG, 46)
    y = 370
    for n, t in items:
        nw = d.textlength(n, font=fn)
        d.text((230 - nw, y), n, font=fn, fill=ORANGE)
        d.text((260, y + 3), t, font=ft, fill=INK)
        y += 72

    # strip of real pages
    names = ["mon_h3.png", "mon_b9.png", "mon_w10.png"]
    tw, gap = 290, 25
    x = (W - (3 * (tw + 6) + 2 * gap)) // 2
    for name in names:
        th = framed(page(name), tw)
        paste_shadow(im, th, (x, 1050), radius=8, offset=(0, 6), alpha=70)
        x += th.width + gap

    d.rectangle([0, H - 200, W, H], fill=NAVY)
    center_text(d, H - 182, "Monday + Sunday start editions", font(BOLD, 44), WHITE)
    center_text(d, H - 122, "Tabs on every page", font(REG, 38), WHITE)
    brand(d, dark=True)
    im.save(HERE / "pin3.png")


if __name__ == "__main__":
    pin1()
    pin2()
    pin3()
