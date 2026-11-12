#!/usr/bin/env python3
"""English URLs for every page, so search engines can index each language on its own.

The site is bilingual in one HTML file: Persian by default, English after the switch.
Search engines only ever see the Persian view of that URL. This script writes, next to
each page X.html, an English twin X.en.html that opens in English:

  - <html lang="en" dir="ltr" data-lang="en" data-lang-lock="en">
  - its own canonical and og:url, an English <title> and description
  - internal links point to the English twins
  - both pages carry hreflang links to each other (fa, en, x-default = Persian)

Persian pages whose <title> has no Persian at all get the Persian headline put in front.
Run before scripts/build_seo.py (which then writes structured data and the sitemap).
Running it twice changes nothing.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ditoman.com/"
SKIP = {"404.html"}
FA = re.compile(r"[؀-ۿ]")
HSTART, HEND = "<!-- hreflang:start -->", "<!-- hreflang:end -->"


def text(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s or "")).split())


def url_of(name):
    return BASE if name == "index.html" else BASE + name


def en_name(name):
    return name[:-5] + ".en.html"


def h1_texts(src):
    """(Persian headline, English headline) as written on the page, from any of its h1s."""
    fa = en = ""
    for attrs, body in re.findall(r"<h1([^>]*)>(.*?)</h1>", src, re.S):
        lang = re.search(r'lang="(fa|en)"', attrs)
        de = re.search(r'data-en="([^"]*)"', attrs)
        sfa = re.search(r'<span[^>]*lang="fa"[^>]*>(.*?)</span>', body, re.S)
        sen = re.search(r'<span[^>]*lang="en"[^>]*>(.*?)</span>', body, re.S)
        whole = text(body)
        if lang:
            if lang.group(1) == "fa" and not fa:
                fa = whole
            if lang.group(1) == "en" and not en:
                en = whole
            continue
        if sfa and not fa:
            fa = text(sfa.group(1))
        if sen and not en:
            en = text(sen.group(1))
        if de and not en:
            en = text(html.unescape(de.group(1)))
        if not sfa and not sen:
            if FA.search(whole) and not fa:
                fa = whole
            elif not FA.search(whole) and not en:
                en = whole
        if sfa and not sen and not en:
            rest = text(re.sub(r'<span[^>]*lang="fa"[^>]*>.*?</span>', "", body, flags=re.S))
            if rest and not FA.search(rest):
                en = rest
    return fa, en


def en_description(src):
    for pat in (r'class="subtitle"[^>]*lang="en"[^>]*>(.*?)</p>', r'<p class="subtitle" lang="en">(.*?)</p>',
                r'<p lang="en"[^>]*>(.*?)</p>', r'<p[^>]*data-en="([^"]*)"', r'class="hero-lede"[^>]*lang="en"[^>]*>(.*?)</p>'):
        m = re.search(pat, src, re.S)
        if m:
            t = text(html.unescape(m.group(1)))
            if len(t) > 40 and not FA.search(t):
                return t[:300].rsplit(" ", 1)[0] + ("…" if len(t) > 300 else "")
    return ""


def titles(src, name):
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    old = text(m.group(1)) if m else name
    segs = [s.strip() for s in old.split("|") if s.strip()]
    fa_h1, en_h1 = h1_texts(src)
    # drop a Persian name in brackets ("Kalleh (کاله)") first, then any Persian-only segment
    en_segs = [re.sub(r"\s*\([^)]*[؀-ۿ][^)]*\)", "", x).strip() for x in segs]
    en_segs = [x for x in en_segs if x and not FA.search(x)]
    en_title = " | ".join(en_segs) if en_segs else (en_h1 + " | Ditoman" if en_h1 else old)
    if not any("ditoman" in s.lower() for s in en_segs) and en_segs:
        en_title += " | Ditoman"
    fa_title = None
    if not FA.search(old) and fa_h1:
        fa_title = f"{fa_h1} | {old}"
    return old, fa_title, en_title


def hreflang_block(name):
    fa, en = url_of(name), BASE + en_name(name)
    return (f'{HSTART}\n  <link rel="alternate" hreflang="fa" href="{fa}" />\n'
            f'  <link rel="alternate" hreflang="en" href="{en}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{fa}" />\n  {HEND}')


def put_hreflang(src, name):
    block = hreflang_block(name)
    if HSTART in src:
        return re.sub(re.escape(HSTART) + r".*?" + re.escape(HEND), block, src, flags=re.S)
    return src.replace("</head>", "  " + block + "\n</head>", 1)


def make_en(src, name, names):
    old, _, en_title = titles(src, name)
    s = src
    # language of the document
    s = re.sub(r"<html[^>]*>", '<html lang="en" dir="ltr" data-lang="en" data-lang-lock="en">', s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(en_title, quote=False)}</title>", s, count=1, flags=re.S)
    desc = en_description(src)
    if desc:
        s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), s, count=1)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), s, count=1)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + html.escape(en_title) + m.group(2), s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + html.escape(en_title) + m.group(2), s, count=1)
    s = re.sub(r'<meta property="og:locale" content="[^"]*"', '<meta property="og:locale" content="en_US"', s, count=1)
    own = BASE + en_name(name)
    s = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{own}"', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{own}"', s, count=1)

    # internal links to the English twins
    def link(m):
        attr, target, rest = m.group(1), m.group(2), m.group(3)
        if target in ("./", "/", ""):
            return f'{attr}"index.en.html{rest}"'
        if target in names:
            return f'{attr}"{en_name(target)}{rest}"'
        if target.startswith(BASE):
            t = target[len(BASE):] or "index.html"
            if t in names:
                return f'{attr}"{BASE}{en_name(t)}{rest}"'
        return m.group(0)
    s = re.sub(r'(href=)"([^"#?]*?)((?:[?#][^"]*)?)"', link, s)
    return put_hreflang(s, name)


def main():
    pages = sorted(p for p in ROOT.glob("*.html") if not p.name.endswith(".en.html") and p.name not in SKIP)
    names = {p.name for p in pages}
    for p in pages:
        src = p.read_text(encoding="utf-8")
        old, fa_title, _ = titles(src, p.name)
        new = src
        if fa_title:
            new = re.sub(r"<title>.*?</title>", f"<title>{html.escape(fa_title, quote=False)}</title>", new, count=1, flags=re.S)
        new = put_hreflang(new, p.name)
        if new != src:
            p.write_text(new, encoding="utf-8")
        en = make_en(new, p.name, names)
        target = ROOT / en_name(p.name)
        if not target.exists() or target.read_text(encoding="utf-8") != en:
            target.write_text(en, encoding="utf-8")
    print(f"{len(pages)} pages, {len(pages)} English twins")


if __name__ == "__main__":
    main()
