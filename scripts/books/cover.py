#!/usr/bin/env python3
"""Banner for a Ditoman book summary: the FIXED book-summary template.

The layout, sizes, colours and fonts below are the approved template (same as the covers of
«ابرقدرت غایب» and «نگذار هر چیزی روی تو اثر بگذارد»). Do not rearrange it. Only the texts,
the jacket and the faint background glow (the book's field colour) change from book to book.

Text comes from scripts/books/data/<slug>/meta.json -> "cover":
  gold    first title line (short, gold)          white   second title line (optional, white)
  teal    one-line subtitle                        author  e.g. «نویسنده: مورگان هاوزل»
  latin   e.g. "Morgan Housel · The Psychology of Money · 2020" (must fit one line)
  bullets two short sentences                      tags    three short topic words
The jacket is assets/books/<slug>.jpg and is never cropped: the book takes its proportions.

Run from the repo root:  python3 scripts/books/cover.py <slug>
Writes social/<slug>/post.png, post.webp, card.webp, thumb.webp and the English en*.webp set.
Exit code 2 means the text does not fit: shorten it and run again.
"""
import html, json, pathlib, sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
F = (ROOT / "fonts" / "iranyekanx").as_uri()
BR = (ROOT / "scripts" / "report" / "fonts" / "BricolageGrotesque.ttf").as_uri()
LOGO = (ROOT / "tmn-logo-512.png").as_uri()


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001  (no bundled browser in this workspace: use the installed Chrome)
        return p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])


def spine_colours(jacket):
    """Spine gradient taken from the jacket's own left edge."""
    im = Image.open(jacket).convert("RGB")
    strip = im.crop((0, 0, max(2, im.width // 30), im.height)).resize((1, 1), Image.BOX)
    r, g, b = strip.getpixel((0, 0))
    mix = lambda k: "#%02x%02x%02x" % tuple(max(0, min(255, int(c * k))) for c in (r, g, b))
    return mix(0.45), mix(1.0), mix(0.5)


def page_html(slug, c, glow):
    jacket = ROOT / "assets" / "books" / f"{slug}.jpg"
    jw, jh = Image.open(jacket).size
    bw = 440
    bh = round(bw * jh / jw)
    if bh > 720:
        bh = 720
        bw = round(bh * jw / jh)
    top = 800 - bh // 2
    left = 585 + (440 - bw) // 2
    s1, s2, s3 = spine_colours(jacket)
    e = lambda t: html.escape(t, quote=False)
    white = f'<span class="w">{e(c["white"])}</span>' if c.get("white") else ""
    bullets = "".join(f"<p>{e(b)}</p>" for b in c["bullets"])
    tags = "<span>•</span>".join(e(t) for t in c["tags"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Y;src:url({F}/IRANYekanXFaNum-Bold.woff2);font-weight:700}}
@font-face{{font-family:Y;src:url({F}/IRANYekanXFaNum-Black.woff2);font-weight:900}}
@font-face{{font-family:Y;src:url({F}/IRANYekanXFaNum-Medium.woff2);font-weight:500}}
@font-face{{font-family:B;src:url({BR})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;position:relative;overflow:hidden;background:#0a1b2b;font-family:Y;color:#F2F0E9}}
.bg{{position:absolute;inset:0;background:linear-gradient(180deg,#0a1b2b 0%,#0a1a2b 55%,#0a1a29 100%)}}
.ring{{position:absolute;left:440px;top:370px;width:860px;height:860px;border-radius:50%;border:24px solid rgba(54,186,162,.62);filter:blur(15px);
 -webkit-mask:conic-gradient(from 270deg,rgba(0,0,0,.30) 0deg,#000 55deg,#000 120deg,rgba(0,0,0,.30) 170deg,rgba(0,0,0,.12) 230deg,rgba(0,0,0,.75) 290deg,rgba(0,0,0,.30) 360deg)}}
.glow{{position:absolute;left:460px;top:390px;width:820px;height:820px;border-radius:50%;background:radial-gradient(circle,rgba(22,72,84,.36) 0%,rgba(16,54,68,.22) 50%,rgba(10,27,43,0) 72%)}}
.tint{{position:absolute;left:700px;top:980px;width:460px;height:330px;border-radius:50%;background:radial-gradient(ellipse,{glow}1c,{glow}00 70%)}}
.logo{{position:absolute;left:0;right:0;top:62px;display:flex;justify-content:center;align-items:center;gap:20px}}
.logo img{{width:84px;height:84px}}
.logo .bar{{width:1.5px;height:62px;background:rgba(242,240,233,.35)}}
.logo .nm{{text-align:right}}.logo .nm b{{display:block;font-weight:900;font-size:34px;line-height:1.1}}
.logo .nm i{{display:block;font-style:normal;font-family:B;font-weight:700;font-size:20px;letter-spacing:.32em;color:#57D9C7;direction:ltr;text-align:left}}
.L{{position:absolute;left:40px;top:280px;width:520px;direction:rtl;text-align:center}}
.pill{{display:inline-block;padding:8px 30px;border-radius:30px;border:2px solid #E9B94A;background:rgba(233,185,74,.12);color:#F4D27A;font-weight:900;font-size:28px}}
.t1{{margin-top:26px;font-weight:900;font-size:128px;line-height:1.08;white-space:nowrap;background:linear-gradient(180deg,#FFE7A3 0%,#E9B94A 55%,#B9842A 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))}}
.t1 .g{{display:block;padding:.06em 0}}
.t1 .w{{display:block;line-height:1.32;background:linear-gradient(180deg,#ffffff,#d8dde2);-webkit-background-clip:text;color:transparent}}
.t2{{margin-top:14px;font-weight:900;font-size:38px;color:#57D9C7;white-space:nowrap}}
.hr{{margin:30px auto 24px;width:400px;height:2px;background:linear-gradient(90deg,rgba(233,185,74,0),#E9B94A,rgba(233,185,74,0))}}
.au{{font-weight:900;font-size:33px;white-space:nowrap}}.au2{{margin-top:4px;font-family:B;font-size:19px;color:#9fb0bd;direction:ltr;white-space:nowrap}}
.box{{margin:44px auto 0;width:480px;border-radius:22px;background:rgba(18,36,52,.86);border:1.5px solid rgba(233,185,74,.35);padding:24px 28px;text-align:right}}
.box p{{position:relative;padding-right:26px;font-weight:700;font-size:25px;line-height:1.6}}
.box p+p{{margin-top:16px}}
.box p:before{{content:"";position:absolute;right:0;top:17px;width:11px;height:11px;border-radius:50%;background:#E9B94A}}
.bk{{position:absolute;left:{left}px;top:{top}px;width:{bw}px;height:{bh}px;perspective:1600px}}
.bk .f{{position:absolute;inset:0;background:url({jacket.as_uri()}) center/100% 100%;transform:rotateY(-14deg);transform-origin:left center;border-radius:3px 8px 8px 3px;box-shadow:30px 30px 60px rgba(0,0,0,.7),inset 6px 0 10px rgba(255,255,255,.18),inset -2px 0 3px rgba(0,0,0,.4)}}
.bk .s{{position:absolute;left:-26px;top:6px;width:28px;height:{bh - 12}px;background:linear-gradient(90deg,{s1},{s2} 60%,{s3});transform:skewY(-4deg);border-radius:3px 0 0 3px}}
.tags{{position:absolute;left:0;right:0;bottom:150px;text-align:center;direction:rtl;font-weight:700;font-size:25px;color:#cfd8de}}
.tags span{{color:#E9B94A;margin:0 10px}}
.web{{position:absolute;left:50%;bottom:62px;transform:translateX(-50%);display:flex;align-items:center;gap:12px;padding:12px 34px;border-radius:30px;background:rgba(18,36,52,.9);border:1.5px solid rgba(87,217,199,.45);font-family:B;font-weight:700;font-size:28px;letter-spacing:.06em}}
.web svg{{width:28px;height:28px}}
.cr{{position:absolute;left:585px;top:{top + bh + 25}px;width:440px;text-align:center;font-family:B;font-size:14px;color:#8a9aa8}}
</style></head><body>
<div class="bg"></div><div class="glow"></div><div class="tint"></div><div class="ring"></div>
<div class="logo"><div class="nm"><b>دیتومان</b><i>DITOMAN</i></div><div class="bar"></div><img src="{LOGO}"></div>
<div class="L">
<span class="pill">خلاصه کتاب</span>
<div class="t1"><span class="g">{e(c["gold"])}</span>{white}</div>
<div class="t2">{e(c["teal"])}</div>
<div class="hr"></div>
<div class="au">{e(c["author"])}</div>
<div class="au2">{e(c["latin"])}</div>
<div class="box">{bullets}</div>
</div>
<div class="bk"><div class="s"></div><div class="f"></div></div>
<div class="cr">Book cover © its publisher</div>
<div class="tags">{tags}</div>
<div class="web"><svg viewBox="0 0 24 24" fill="none" stroke="#57D9C7" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2c3 3.5 3 16.5 0 20M12 2c-3 3.5-3 16.5 0 20"/></svg>ditoman.com</div>
<script>
// Fit each one-line text to the column: shrink only, never wrap or grow past the template size.
function fit(el, max, cap) {{
  let size = cap; el.style.fontSize = size + 'px';
  const r = document.createRange(); r.selectNodeContents(el);
  while (r.getBoundingClientRect().width > max && size > 20) {{ size -= 1; el.style.fontSize = size + 'px'; }}
  return size;
}}
const g = document.querySelector('.t1 .g'), w = document.querySelector('.t1 .w');
const gs = fit(g, 484, 128);
if (w) fit(w, 470, gs >= 128 ? 128 : Math.round(gs * 0.8));
fit(document.querySelector('.t2'), 500, 38);
fit(document.querySelector('.au'), 500, 33);
fit(document.querySelector('.au2'), 500, 19);
</script>
</body></html>"""


def make(slug):
    data = ROOT / "scripts" / "books" / "data" / slug
    meta = json.loads((data / "meta.json").read_text(encoding="utf-8"))
    cat = json.loads((ROOT / "data" / "books" / "catalog.json").read_text(encoding="utf-8"))
    book = next((b for b in cat["books"] if b["slug"] == slug), None)
    glow = next((k["color"] for k in cat["categories"] if book and k["key"] == book["cat"]), "#E9B94A")
    out = ROOT / "social" / slug
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "cover.tmp.html"
    tmp.write_text(page_html(slug, meta["cover"], glow), encoding="utf-8")
    import en_covers
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1080, "height": 1440})
        pg.goto(tmp.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        box = pg.evaluate("document.querySelector('.box').getBoundingClientRect().bottom")
        sizes = pg.evaluate("[...document.querySelectorAll('.t1 .g,.t1 .w,.t2,.au,.au2')].map(e=>parseInt(getComputedStyle(e).fontSize))")
        pg.screenshot(path=str(out / "post.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
        job = dict(kind="story", page=slug + ".html", folder=slug, title=meta["card_en_title"], dek=meta["sub_en"],
                   kicker="Book summary", accent="yellow", size=(1080, 1080), out=out / "en.png")
        en_covers.render(pg, job)
        en_covers.finish(job)
        b.close()
    tmp.unlink()
    im = Image.open(out / "post.png").convert("RGB")
    im.save(out / "post.png", optimize=True)
    im.save(out / "post.webp", "WEBP", quality=90, method=6)
    im.resize((900, 1200), Image.LANCZOS).save(out / "card.webp", "WEBP", quality=80, method=6)
    im.crop((0, 250, 1080, 1330)).resize((240, 240), Image.LANCZOS).save(out / "thumb.webp", "WEBP", quality=78, method=6)
    print(f"cover {slug}: text box ends at {round(box)} px, font sizes {sizes}")
    problems = []
    if box > 1215:
        problems.append("the text column runs into the tags row: shorten the bullets")
    if sizes[0] < 60:
        problems.append("the gold title line is too long (font fell below 60 px): use fewer words")
    if sizes[-1] < 15:
        problems.append("the latin line is too long: shorten it")
    for line in problems:
        print("COVER TEXT DOES NOT FIT:", line)
    return 2 if problems else 0


if __name__ == "__main__":
    sys.exit(make(sys.argv[1]))
