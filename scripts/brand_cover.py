"""Build the cover image for a company record: real products and the brand's logos.

Standing rule for every company added to Ditoman: the card and record open with a photo
of a few of the company's own products (or its plant/output for industrial firms), with
its Persian and English logos on the image. Sources go in data/companies/<slug>.json.

Run:  python3 scripts/brand_cover.py            (all brands in BRANDS)
      python3 scripts/brand_cover.py kalleh     (one brand)
Output: companies/<slug>/cover.webp (1600x1000) and companies/<slug>/logo.png
"""
import pathlib, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "brand-src"
FONT_FA = ROOT / "fonts" / "iranyekanx"
W, H = 1600, 1000

# layout "shelf": packshots on white, set on a light stage
# layout "photo": one real photo, full bleed
BRANDS = {
    "kalleh": {
        "layout": "shelf", "bg": ("#fff7f3", "#e8f3e6"), "glow": "#e53935",
        "products": ["kalleh/e2.4.jpg", "kalleh/e6.0.jpg", "kalleh/e7.7.jpg", "kalleh/e4.7.jpg", "kalleh/e5.0.jpg"],
        "crop": {"kalleh/e7.7.jpg": (40, 150, 680, 570)},
        "logos": ["kalleh/logo.png", ("kalleh/e7.7.jpg", (300, 226, 440, 296), "ellipse")],
    },
    "golrang": {
        "layout": "shelf", "bg": ("#f6f7fb", "#fde9ea"), "glow": "#c62828",
        "products": ["golrang/e1.17.jpg", "golrang/e2.0.jpg"],
        "logos": ["golrang/logo.png", "golrang/c.1.jpg"],
    },
    "aryasasol": {
        "layout": "photo", "photo": "aryasasol/pe.2.jpg", "photo_crop": (0, 0, 1920, 1000),
        "logos": ["aryasasol/logo.jpg"],
    },
    "fateh-sanat": {
        "layout": "photo", "photo": "fateh/c.2.jpg", "photo_crop": (0, 0, 1157, 652),
        "logos": ["fateh/logo.jpg"], "logo_text_en": "Fateh Sanat Kimia",
    },
}


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def stage(bg, glow):
    a, b = hexrgb(bg[0]), hexrgb(bg[1])
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((W * 0.15, -H * 0.5, W * 0.85, H * 0.55), fill=60)
    g = g.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new("RGB", (W, H), hexrgb(glow)), im, g)
    # floor line
    ImageDraw.Draw(im).rectangle((0, int(H * 0.86), W, H), fill=tuple(max(c - 14, 0) for c in hexrgb(bg[1])))
    return im


def trim_white(im):
    """Cut the white margin around a packshot."""
    rgb = im.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255))).convert("L")
    box = diff.point(lambda v: 255 if v > 18 else 0).getbbox()
    return im.crop(box) if box else im


def shelf(cfg):
    im = stage(cfg["bg"], cfg["glow"])
    shots = []
    for p in cfg["products"]:
        s = Image.open(SRC / p).convert("RGB")
        if p in cfg.get("crop", {}):
            s = s.crop(cfg["crop"][p])
        shots.append(trim_white(s))
    floor = int(H * 0.86)
    n = len(shots)
    slot = (W - 160) / n
    maxh = H * (0.5 if W == H else 0.62)
    x = 80
    for s in shots:
        scale = min(maxh / s.height, (slot - 30) / s.width)
        s = s.resize((int(s.width * scale), int(s.height * scale)), Image.LANCZOS)
        px = int(x + (slot - s.width) / 2)
        py = floor - s.height + 6
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).ellipse((px + s.width * 0.08, floor - 10, px + s.width * 0.92, floor + 22), fill=120)
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        im = Image.composite(Image.new("RGB", (W, H), (60, 60, 60)), im, sh)
        # white packshot background disappears on the light stage (multiply)
        region = im.crop((px, py, px + s.width, py + s.height))
        im.paste(ImageChops.multiply(region, s), (px, py))
        x += slot
    return im


def photo(cfg):
    p = Image.open(SRC / cfg["photo"]).convert("RGB").crop(cfg["photo_crop"])
    scale = max(W / p.width, H / p.height)
    p = p.resize((int(p.width * scale) + 1, int(p.height * scale) + 1), Image.LANCZOS)
    left, top = (p.width - W) // 2, (p.height - H) // 2
    return p.crop((left, top, left + W, top + H))


def logo_img(spec):
    if isinstance(spec, tuple):
        path, box, shape = spec
        im = Image.open(SRC / path).convert("RGBA").crop(box)
        im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
        if shape == "ellipse":
            m = Image.new("L", im.size, 0)
            ImageDraw.Draw(m).ellipse((4, 4, im.width - 4, im.height - 4), fill=255)
            im.putalpha(m)
        return im
    return trim_white(Image.open(SRC / spec).convert("RGBA"))


def logo_chip(im, cfg):
    logos = [logo_img(s) for s in cfg["logos"]]
    hh = 120
    logos = [l.resize((int(l.width * hh / l.height), hh), Image.LANCZOS) for l in logos]
    text = cfg.get("logo_text_en")
    font = ImageFont.truetype(str(ROOT / "scripts" / "report" / "fonts" / "BricolageGrotesque.ttf"), 40) if text else None
    tw = int(ImageDraw.Draw(im).textlength(text, font=font)) + 20 if text else 0
    pad, gap = 26, 30
    cw = pad * 2 + sum(l.width for l in logos) + gap * (len(logos) - 1) + (gap + tw if text else 0)
    ch = hh + pad * 2
    chip = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(chip).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=34, fill=(255, 255, 255, 240))
    x = pad
    for l in logos:
        chip.alpha_composite(l, (x, pad))
        x += l.width + gap
    if text:
        ImageDraw.Draw(chip).text((x, ch / 2), text, font=font, fill=(20, 40, 60), anchor="lm")
    shadow = Image.new("RGBA", (cw + 60, ch + 60), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((30, 38, cw + 30, ch + 38), radius=34, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    base = im.convert("RGBA")
    ox, oy = (W - cw) // 2 if W == H else W - cw - 130, 110
    base.alpha_composite(shadow, (ox - 30, oy - 30))
    base.alpha_composite(chip, (ox, oy))
    return base.convert("RGB"), logos[0]


def build(slug):
    global W, H
    cfg = BRANDS[slug]
    out = ROOT / "companies" / slug
    out.mkdir(parents=True, exist_ok=True)
    # wide cover for the record page, square version for cards
    for name, size in (("cover.webp", (1600, 1000)), ("card.webp", (1000, 1000))):
        W, H = size
        im = shelf(cfg) if cfg["layout"] == "shelf" else photo(cfg)
        im, main_logo = logo_chip(im, cfg)
        im.save(out / name, "WEBP", quality=84, method=6)
    lg = logo_img(cfg["logos"][0])
    bg = Image.new("RGBA", lg.size, (255, 255, 255, 255))
    bg.alpha_composite(lg)
    bg.convert("RGB").save(out / "logo.png")
    print(slug, "ok")


if __name__ == "__main__":
    for s in (sys.argv[1:] or BRANDS):
        build(s)
