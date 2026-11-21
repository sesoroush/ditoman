#!/usr/bin/env python3
"""Arabic editions of the story cover images, for the Arabic pages.

Same card as the English editions (scripts/en_covers.py): the Ditoman petrol ground, the star motif,
the kicker, the headline and the summary; here right-to-left in IBM Plex Sans Arabic, with the
Arabic text taken from the translation files (data/i18n/src/ar-*.json) for the homepage card.
Nothing is added that the card does not already say.

Writes social/<folder>/ar.webp (1080), ar-card.webp (900) and ar-thumb.webp (240).
Run from the repo root: python3 scripts/ar_covers.py [folder ...]
"""
import html
import json
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "brand-src" / "fonts"
GEO = ROOT / "assets" / "geo"
LOGO = ROOT / "tmn-logo-512.png"
D = {}
for f in sorted((ROOT / "data" / "i18n" / "src").glob("ar-*.json")):
    D.update(json.loads(f.read_text(encoding="utf-8")))


def clean(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s or "")).split())


def jobs(only):
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    a = s.index('id="stories"')
    sec = s[a:s.index("</section>", a)]
    out = []
    for m in re.finditer(r'<a class="co-card[^"]*"([^>]*)>(.*?)</a>', sec, re.S):
        attrs, body = m.group(1), m.group(2)
        href = re.search(r'href="([^"]+)"', attrs).group(1)
        img = re.search(r'src="social/([^/"]+)/(?:thumb|card)\.webp"', body)
        h3 = re.search(r'<h3>.*?<span lang="fa">(.*?)</span>', body, re.S)
        cat = re.search(r'class="co-cat[^"]*"><span lang="fa">(.*?)</span>', body)
        dek = re.search(r'class="co-fa" lang="fa">(.*?)</p>', body, re.S)
        if not (img and h3):
            continue
        t, c, d = clean(h3.group(1)), clean(cat.group(1)) if cat else "", clean(dek.group(1)) if dek else ""
        if t not in D:
            print("no Arabic title yet:", href, t); continue
        special = "data-kicker" in attrs
        kick = D.get(c, c) if c else ""
        out.append(dict(page=href, folder=img.group(1), title=D[t], dek=D.get(d, ""), kicker=kick or "تقرير",
                        accent="yellow" if (special or c == "چراغ روشن") else "mint"))
    if only:
        out = [j for j in out if j["folder"] in only]
    return out


CSS = """
@font-face { font-family: PlexAr; src: url('{fonts}/IBMPlexSansArabic-Regular.ttf'); font-weight: 400; }
@font-face { font-family: PlexAr; src: url('{fonts}/IBMPlexSansArabic-SemiBold.ttf'); font-weight: 600; }
@font-face { font-family: PlexAr; src: url('{fonts}/IBMPlexSansArabic-Bold.ttf'); font-weight: 700 900; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1080px; overflow: hidden; }
body { background: #101f22; color: #f2f0e9; font-family: PlexAr, sans-serif; position: relative; overflow: hidden; }
.glow { position: absolute; inset: 0;
  background: radial-gradient(70% 60% at 0% 0%, rgba(87,217,199,.13), transparent 70%),
              radial-gradient(60% 50% at 100% 100%, rgba(242,160,31,.07), transparent 70%); }
.field { position: absolute; inset: 0; opacity: .07;
  background: linear-gradient(118deg, rgba(87,217,199,.6) 0%, rgba(87,217,199,.6) 38%, #f2a01f 50%, rgba(87,217,199,.6) 62%);
  -webkit-mask-image: url('{geo}/field.svg'), linear-gradient(to bottom, #000 0%, transparent 55%);
  -webkit-mask-size: 150px 150px, 100% 100%; -webkit-mask-repeat: repeat, no-repeat; -webkit-mask-composite: source-in; }
.rosette { position: absolute; width: 760px; height: 760px; left: -260px; bottom: -260px; opacity: .16;
  background: linear-gradient(118deg, rgba(87,217,199,.55) 0%, rgba(87,217,199,.55) 40%, #f2a01f 50%, rgba(87,217,199,.55) 60%);
  -webkit-mask: url('{geo}/rosette.svg') center / contain no-repeat; }
.wrap { position: absolute; inset: 72px; display: flex; flex-direction: column; direction: rtl; }
.top { display: flex; align-items: center; justify-content: space-between; }
.brand { display: flex; align-items: center; gap: 16px; font: 700 26px/1 Inter, Arial, sans-serif; letter-spacing: .32em; direction: ltr; }
.brand img { width: 54px; height: 54px; }
.kick { font: 700 26px/1.2 PlexAr, sans-serif; padding: 10px 22px 12px; border-radius: 999px; }
.kick.mint { background: rgba(87,217,199,.14); color: #57d9c7; border: 1px solid rgba(87,217,199,.45); }
.kick.yellow { background: #ffad00; color: #1a1300; }
.mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.rule { width: 84px; height: 7px; background: #f2a01f; border-radius: 4px; margin-bottom: 30px; }
h1 { font-weight: 700; font-size: {title}px; line-height: 1.32; }
p { margin-top: 28px; font-size: 32px; line-height: 1.65; color: #b9c6c2; }
.foot { display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid rgba(242,240,233,.14); padding-top: 26px;
  font: 600 20px/1 Inter, Arial, sans-serif; letter-spacing: .14em; color: #a9b8b4; direction: ltr; }
.foot i { font-family: Georgia, serif; font-style: italic; letter-spacing: .02em; font-size: 28px; color: #57d9c7; font-weight: 400; }
"""


def render(page, job):
    t = job["title"]; n = len(t)
    size = 92 if n <= 26 else 80 if n <= 40 else 70 if n <= 56 else 60 if n <= 76 else 52
    dek = job["dek"]
    if len(dek) > 190:
        dek = dek[:190].rsplit(" ", 1)[0].rstrip("،؛,:") + "…"
    css = CSS.replace("{fonts}", FONTS.as_uri()).replace("{geo}", GEO.as_uri()).replace("{title}", str(size))
    doc = f"""<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="glow"></div><div class="field"></div><div class="rosette"></div>
<div class="wrap">
  <div class="top"><div class="kick {job['accent']}">{html.escape(job['kicker'])}</div>
    <div class="brand"><img src="{LOGO.as_uri()}" alt="">DITOMAN</div></div>
  <div class="mid"><div class="rule"></div><h1>{html.escape(t)}</h1>{f'<p>{html.escape(dek)}</p>' if dek else ''}</div>
  <div class="foot"><i>Learn · Connect · Evolve</i><span>DITOMAN.COM</span></div>
</div></body></html>"""
    page.set_viewport_size({"width": 1080, "height": 1080})
    out = ROOT / "social" / job["folder"] / "ar.png"
    tmp = out.with_suffix(".tmp.html")
    tmp.write_text(doc, encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="load")
    tmp.unlink()
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(150)
    page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1080})
    im = Image.open(out).convert("RGB")
    d = out.parent
    im.save(d / "ar.webp", "WEBP", quality=82, method=6)
    im.resize((900, 900), Image.LANCZOS).save(d / "ar-card.webp", "WEBP", quality=80, method=6)
    im.resize((240, 240), Image.LANCZOS).save(d / "ar-thumb.webp", "WEBP", quality=78, method=6)
    out.unlink()


def main():
    todo = jobs(set(sys.argv[1:]))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for j in todo:
            render(pg, j)
            print("ok", j["folder"], "|", j["title"])
        b.close()


if __name__ == "__main__":
    main()
