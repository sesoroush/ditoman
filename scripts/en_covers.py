#!/usr/bin/env python3
"""English editions of the story and lesson cover images.

The original covers carry Persian text. In English mode the site shows these
instead, so no Persian appears in English. Each English cover is a typeset
card in the Ditoman palette: the English kicker, headline and summary taken
from the page itself, on the petrol ground with the eight-pointed-star motif.
Nothing is added that the page does not already say.

Stories:  social/<folder>/en.webp (1080 px square) plus en-card.webp (900) and en-thumb.webp (240)
Lessons:  <lesson image>-en.jpg at the original image's size, for lessons whose cover has Persian.

Run from the repo root: python3 scripts/en_covers.py [slug ...]
"""
import html
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "report" / "fonts"
GEO = ROOT / "assets" / "geo"
LOGO = ROOT / "tmn-logo-512.png"
# lesson covers that contain Persian text
LESSONS = ["lesson06", "lesson07", "lesson08", "lesson09", "lesson10"]


def clean(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s or "")).split())


def index_cards():
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    a = s.index('id="stories"')
    sec = s[a:s.index("</section>", a)]
    out = {}
    for m in re.finditer(r'<a class="co-card[^"]*"([^>]*)>(.*?)</a>', sec, re.S):
        attrs, body = m.group(1), m.group(2)
        href = re.search(r'href="([^"]+)"', attrs).group(1)
        special = "data-kicker" in attrs
        h3 = re.search(r"<h3>(.*?)<span lang=\"fa\">", body, re.S)
        cat = re.search(r'class="co-cat[^"]*"><span lang="fa">.*?</span><span lang="en">(.*?)</span>', body)
        out[href] = (clean(h3.group(1)) if h3 else "", "Special report" if special else (clean(cat.group(1)) if cat else ""))
    return out


def page_text(src):
    h1 = re.search(r'<h1 lang="en"[^>]*>(.*?)</h1>', src, re.S)
    sub = re.search(r'class="subtitle"[^>]*lang="en"[^>]*>(.*?)</p>', src, re.S) or \
        re.search(r'<p class="subtitle" lang="en">(.*?)</p>', src, re.S)
    badge = re.search(r'class="lesson-badge"[^>]*lang="en"[^>]*>(.*?)</', src, re.S)
    return (clean(h1.group(1)) if h1 else "", clean(sub.group(1)) if sub else "", clean(badge.group(1)) if badge else "")


def jobs(only):
    cards = index_cards()
    out = []
    for page in sorted(ROOT.glob("*.html")):
        src = page.read_text(encoding="utf-8")
        m = re.search(r'<img src="social/([^/"]+)/card\.webp"', src)
        if not m or page.name == "index.html":
            continue
        title, dek, _ = page_text(src)
        ctitle, cat = cards.get(page.name, ("", ""))
        lights = cat in ("Lights On", "Special report")
        out.append(dict(kind="story", page=page.name, folder=m.group(1), title=ctitle or title, dek=dek,
                        kicker=cat or "Report", accent="yellow" if lights else "mint",
                        size=(1080, 1080), out=ROOT / "social" / m.group(1) / "en.png"))
    for slug in LESSONS:
        page = ROOT / f"{slug}.html"
        src = page.read_text(encoding="utf-8")
        img = re.search(rf'<img src="({slug}-[^"]+\.(?:jpg|png))"', src)
        if not img:
            continue
        orig = ROOT / img.group(1)
        title, dek, badge = page_text(src)
        num = slug.replace("lesson", "")
        w, h = Image.open(orig).size
        out.append(dict(kind="lesson", page=page.name, image=img.group(1), title=title, dek=dek,
                        kicker=f"Lesson {num}" + (f" · {badge}" if badge and "Lesson" not in badge else ""),
                        accent="mint", size=(w, h), out=orig.with_name(orig.stem + "-en.png")))
    if only:
        out = [j for j in out if j.get("folder") in only or j["page"].replace(".html", "") in only]
    return out


CSS = """
@font-face { font-family: Bricolage; src: url('{fonts}/BricolageGrotesque.ttf'); font-weight: 200 800; }
@font-face { font-family: PlayfairI; src: url('{fonts}/PlayfairDisplay-Italic.ttf'); font-style: italic; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: {w}px; height: {h}px; }
body { background: #101f22; color: #f2f0e9; font-family: Inter, sans-serif; position: relative; overflow: hidden; }
.glow { position: absolute; inset: 0;
  background: radial-gradient(70% 60% at 100% 0%, rgba(87,217,199,.13), transparent 70%),
              radial-gradient(60% 50% at 0% 100%, rgba(242,160,31,.07), transparent 70%); }
.field { position: absolute; inset: 0; opacity: .07;
  background: linear-gradient(118deg, rgba(87,217,199,.6) 0%, rgba(87,217,199,.6) 38%, #f2a01f 50%, rgba(87,217,199,.6) 62%);
  -webkit-mask: url('{geo}/field.svg') 0 0 / {tile}px {tile}px repeat;
  -webkit-mask-image: url('{geo}/field.svg'), linear-gradient(to bottom, #000 0%, transparent 55%);
  -webkit-mask-size: {tile}px {tile}px, 100% 100%; -webkit-mask-repeat: repeat, no-repeat; -webkit-mask-composite: source-in; }
.rosette { position: absolute; width: {ros}px; height: {ros}px; right: -{rosoff}px; bottom: -{rosoff}px; opacity: .16;
  background: linear-gradient(118deg, rgba(87,217,199,.55) 0%, rgba(87,217,199,.55) 40%, #f2a01f 50%, rgba(87,217,199,.55) 60%);
  -webkit-mask: url('{geo}/rosette.svg') center / contain no-repeat; }
.wrap { position: absolute; inset: {pad}px; display: flex; flex-direction: column; }
.top { display: flex; align-items: center; justify-content: space-between; }
.brand { display: flex; align-items: center; gap: {g}px; font: 700 {brand}px/1 Inter, sans-serif; letter-spacing: .32em; }
.brand img { width: {logo}px; height: {logo}px; }
.kick { font: 800 {kick}px/1 Inter, sans-serif; letter-spacing: .04em; padding: {kp}px {kp2}px; border-radius: 999px; }
.kick.mint { background: rgba(87,217,199,.14); color: #57d9c7; border: 1px solid rgba(87,217,199,.45); }
.kick.yellow { background: #ffad00; color: #1a1300; }
.mid { flex: 1; display: flex; flex-direction: column; justify-content: center; max-width: {measure}px; }
.rule { width: {rule}px; height: {ruleh}px; background: #f2a01f; border-radius: 4px; margin-bottom: {gap}px; }
h1 { font-family: Bricolage, Inter, sans-serif; font-weight: 800; font-size: {title}px; line-height: 1.06; letter-spacing: -.02em; }
p { margin-top: {gap}px; font-size: {dek}px; line-height: 1.45; color: #b9c6c2; max-width: {measure}px; }
.foot { display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid rgba(242,240,233,.14); padding-top: {fp}px;
  font: 600 {small}px/1 Inter, sans-serif; letter-spacing: .14em; color: #a9b8b4; }
.foot i { font-family: PlayfairI, serif; font-style: italic; letter-spacing: .02em; font-size: {tag}px; color: #57d9c7; font-weight: 400; }
"""


def render(page, job):
    w, h = job["size"]
    u = min(w, h) / 1080  # unit scale
    if w > h * 1.2:
        u = w / 1080 * 0.78
    title = job["title"]
    n = len(title)
    tsize = 104 if n <= 22 else 92 if n <= 34 else 80 if n <= 48 else 68 if n <= 64 else 58
    if w > h * 1.2:  # landscape lessons: wider measure, smaller type
        tsize = int(tsize * 0.92)
    dek = job["dek"]
    if len(dek) > 170:
        cut = dek[:170].rsplit(" ", 1)[0].rstrip(",;:")
        dek = cut + "…"
    v = dict(fonts=FONTS.as_uri(), geo=GEO.as_uri(), w=w, h=h, tile=int(150 * u), ros=int(760 * u), rosoff=int(260 * u),
             pad=int(72 * u), g=int(16 * u), brand=int(26 * u), logo=int(54 * u), kick=int(24 * u), kp=int(11 * u),
             kp2=int(20 * u), measure=int((w - 144 * u) * (0.92 if w > h * 1.2 else 1)), rule=int(84 * u),
             ruleh=max(4, int(7 * u)), gap=int(28 * u), title=int(tsize * u), dek=int(33 * u), fp=int(26 * u),
             small=int(20 * u), tag=int(28 * u))
    css = CSS
    for k, val in v.items():
        css = css.replace("{" + k + "}", str(val))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="glow"></div><div class="field"></div><div class="rosette"></div>
<div class="wrap">
  <div class="top"><div class="brand"><img src="{LOGO.as_uri()}" alt="">DITOMAN</div>
    <div class="kick {job['accent']}">{html.escape(job['kicker'])}</div></div>
  <div class="mid"><div class="rule"></div><h1>{html.escape(title)}</h1>{f'<p>{html.escape(dek)}</p>' if dek else ''}</div>
  <div class="foot"><span>DITOMAN.COM/{html.escape(job['page'].upper().replace('.HTML', ''))}</span><i>Learn · Connect · Evolve</i></div>
</div></body></html>"""
    page.set_viewport_size({"width": w, "height": h})
    tmp = job["out"].with_suffix(".tmp.html")
    tmp.write_text(doc, encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="load")
    tmp.unlink()
    page.evaluate("document.fonts.ready")
    page.screenshot(path=str(job["out"]), clip={"x": 0, "y": 0, "width": w, "height": h})


def finish(job):
    src = job["out"]
    im = Image.open(src).convert("RGB")
    if job["kind"] == "story":
        d = src.parent
        im.save(d / "en.webp", "WEBP", quality=82, method=6)
        im.resize((900, 900), Image.LANCZOS).save(d / "en-card.webp", "WEBP", quality=80, method=6)
        im.resize((240, 240), Image.LANCZOS).save(d / "en-thumb.webp", "WEBP", quality=78, method=6)
    else:
        im.save(src.with_suffix(".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
    src.unlink()


def main():
    todo = jobs(set(sys.argv[1:]))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for j in todo:
            render(pg, j)
            finish(j)
            print("ok", j["page"], "|", j["title"])
        b.close()


if __name__ == "__main__":
    main()
