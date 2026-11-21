#!/usr/bin/env python3
"""Arabic editions of the pages listed in AR_PAGES: X.html (Persian) -> X.ar.html.

The Persian page is the source, because its layout is already right-to-left. Every Persian text
node and translatable attribute is replaced from the translation files in data/i18n/src/ar-*.json
(exact strings) and the rules in scripts/i18n/ar_rules.py (dates, reading times, steps, digits).
Strings that have no translation yet keep their Persian text and are listed in data/i18n/ar-missing.json.

Each Arabic page: <html lang="ar" dir="rtl" data-site-lang="ar">, its own canonical and og:url,
links to other Arabic pages, the Arabic font, and ar.js (translates text that scripts write later).
The Persian and English pages of the same set get an hreflang="ar" link.
Run after build_en_pages.py and before build_seo.py. Running it twice changes nothing.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "i18n"))
import ar_rules  # noqa: E402

BASE = "https://ditoman.com/"
# posts, calendar and press are filled every day from Persian feeds; they get Arabic when the feeds do
AR_PAGES = ["index.html", "learn.html", "prices.html", "tmn.html", "learn-earn.html"]
FA = re.compile(r"[؀-ۿ]")
HSTART, HEND = "<!-- hreflang:start -->", "<!-- hreflang:end -->"
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-fa", "data-fa-label", "data-kicker")
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n  '
        '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'" />\n  '
        '<link rel="stylesheet" href="ar.css?v=20261121a" />')

D = {}
for f in sorted((ROOT / "data" / "i18n" / "src").glob("ar-*.json")):
    D.update(json.loads(f.read_text(encoding="utf-8")))
missing = {}


def norm(s):
    return " ".join(html.unescape(s).split())


def tr(raw, where):
    t = norm(raw)
    if not t or not FA.search(t):
        return None
    out = D.get(t) or ar_rules.apply(t)
    if out is None:
        missing.setdefault(t, where)
        return None
    return out


def tr_text(m, where):
    raw = m.group(0)
    out = tr(raw, where)
    if out is None:
        return raw.translate(ar_rules.FA_DIG) if FA.search(raw) else raw
    lead = raw[: len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    return lead + html.escape(out, quote=False) + trail


def translate_body(s, name):
    # split off script/style blocks, translate text between tags elsewhere
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", s, flags=re.S | re.I)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        seg = re.sub(r"(?<=>)[^<>]+(?=<)", lambda m: tr_text(m, name), seg)

        def attr(m):
            out = tr(m.group(3), name)
            if out is None:
                return m.group(0).translate(ar_rules.FA_DIG) if FA.search(m.group(3)) else m.group(0)
            return f'{m.group(1)}={m.group(2)}{html.escape(out)}{m.group(2)}'
        seg = re.sub(r'\b(' + "|".join(ATTRS) + r')=(["\'])(.*?)\2', attr, seg)
        # meta descriptions and titles
        seg = re.sub(r'(<meta (?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description|og:image:alt)" content=")([^"]*)(")',
                     lambda m: m.group(1) + html.escape(tr(m.group(2), name) or m.group(2)) + m.group(3), seg)
        parts[i] = seg
    return "".join(parts)


def ar_name(name):
    return name[:-5] + ".ar.html"


def url_of(name):
    return BASE if name == "index.html" else BASE + name


def hreflang_block(name):
    fa, en, ar = url_of(name), BASE + name[:-5] + ".en.html", BASE + ar_name(name)
    return (f'{HSTART}\n  <link rel="alternate" hreflang="fa" href="{fa}" />\n'
            f'  <link rel="alternate" hreflang="en" href="{en}" />\n'
            f'  <link rel="alternate" hreflang="ar" href="{ar}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{fa}" />\n  {HEND}')


def put_hreflang(src, name):
    block = hreflang_block(name)
    if HSTART in src:
        return re.sub(re.escape(HSTART) + r".*?" + re.escape(HEND), lambda m: block, src, flags=re.S)
    return src.replace("</head>", "  " + block + "\n</head>", 1)


def make_ar(src, name):
    s = src
    s = re.sub(r"<html[^>]*>", '<html lang="ar" dir="rtl" data-lang="fa" data-lang-lock="fa" data-site-lang="ar">', s, count=1)
    # the Persian page's early script switches to English from a saved choice; not wanted here
    s = re.sub(r"<script>try\{if\(localStorage\.getItem\(\"ditoman-lang\"\)===\"en\"\).*?</script>\s*", "", s, count=1, flags=re.S)
    own = BASE + ar_name(name)
    s = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{own}"', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{own}"', s, count=1)
    s = re.sub(r'<meta property="og:locale" content="[^"]*"', '<meta property="og:locale" content="ar_AR"', s, count=1)
    s = put_hreflang(s, name)
    s = translate_body(s, name)

    def link(m):
        target, rest = m.group(2), m.group(3) or ""
        if target in AR_PAGES:
            return f'{m.group(1)}"{ar_name(target)}{rest}"'
        return m.group(0)
    s = re.sub(r'(href=)"([a-z0-9\-]+\.html)(#[^"]*)?"', link, s)
    s = re.sub(r'(href=)"(\./?)"', lambda m: 'href="index.ar.html"', s)
    if "ar.css" not in s:
        s = s.replace("</head>", "  " + FONT + "\n</head>", 1)
    if 'src="ar.js' not in s:
        s = s.replace("</body>", '<script src="ar.js?v=20261121a"></script>\n</body>', 1)
    return s


def main():
    for name in AR_PAGES:
        p = ROOT / name
        src = p.read_text(encoding="utf-8")
        (ROOT / ar_name(name)).write_text(make_ar(src, name), encoding="utf-8")
        for twin in (p, ROOT / (name[:-5] + ".en.html")):
            if twin.exists():
                t = twin.read_text(encoding="utf-8")
                t2 = put_hreflang(t, name)
                if t2 != t:
                    twin.write_text(t2, encoding="utf-8")
    (ROOT / "data" / "i18n" / "ar-missing.json").write_text(json.dumps(missing, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(AR_PAGES)} Arabic pages; {len(missing)} strings still in Persian")


if __name__ == "__main__":
    main()
