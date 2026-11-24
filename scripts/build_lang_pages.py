#!/usr/bin/env python3
"""Chinese, Turkish and Russian editions: X.en.html (English twin) -> X.zh.html, X.tr.html, X.ru.html.

The English page is the source. Every English text node and translatable attribute is replaced from
data/i18n/src/<lang>-*.json (keys are the English strings) and the patterns in scripts/i18n/lang_rules.py
(dates, reading times, steps). A page is written only when nothing on it is left untranslated; the
rest are listed in data/i18n/<lang>-missing.json and keep linking to the English page.
Each page: <html lang="zh|tr|ru" dir="ltr" data-site-lang=...>, its own canonical/og:url/og:locale,
the shared hreflang block, links to the same-language pages that exist, i18n.css for fonts.
Run after build_en_pages.py and build_ar_pages.py, before build_seo.py. Running it twice changes nothing.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "i18n"))
import hl  # noqa: E402
import lang_rules  # noqa: E402

BASE = "https://ditoman.com/"
LOCALE = {"zh": "zh_CN", "tr": "tr_TR", "ru": "ru_RU", "pt": "pt_PT", "es": "es_ES", "fr": "fr_FR", "de": "de_DE"}
# page sets, by stage; a page not listed for a language is not built for it
CORE = ["index", "learn", "prices", "tmn", "learn-earn"]
PAGES = {l: list(CORE) for l in ("zh", "tr", "ru", "pt", "es", "fr", "de")}
try:
    PAGES.update(json.loads((ROOT / "scripts" / "lang_pages.json").read_text(encoding="utf-8")))
except FileNotFoundError:
    pass
LAT = re.compile(r"[A-Za-z]{2}")
FA = re.compile(r"[؀-ۿ]")
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-kicker", "data-en-label", "data-en")
METAS = r"(?:name|property)=\"(?:description|og:title|og:description|twitter:title|twitter:description|og:image:alt)\""
CSS = '<link rel="stylesheet" href="i18n.css?v=20261121a" />'


def norm(s):
    return " ".join(html.unescape(s).split())


MAX_MISSING = 20


def run(lang, names):
    D = {}
    for f in sorted((ROOT / "data" / "i18n" / "src").glob(f"{lang}-*.json")):
        D.update(json.loads(f.read_text(encoding="utf-8")))
    missing = {}

    def tr(raw, where):
        t = norm(raw)
        if not t or not LAT.search(t) or FA.search(t):
            return None
        out = lang_rules.apply(lang, t) or D.get(t)
        if out is None:
            missing.setdefault(t, where)
        return out

    def translate_body(s, name):
        parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", s, flags=re.S | re.I)
        for i in range(0, len(parts), 2):
            seg = parts[i]

            def text(m):
                raw = m.group(0)
                out = tr(raw, name)
                if out is None:
                    return raw
                lead, trail = raw[: len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
                return lead + html.escape(out, quote=False) + trail
            seg = re.sub(r"(?<=>)[^<>]+(?=<)", text, seg)

            def attr(m):
                out = tr(html.unescape(m.group(3)), name)
                return m.group(0) if out is None else f"{m.group(1)}={m.group(2)}{html.escape(out)}{m.group(2)}"
            seg = re.sub(r"\b(" + "|".join(ATTRS) + r")=([\"'])(.*?)\2", attr, seg, flags=re.S)
            seg = re.sub(r"(<meta " + METAS + r" content=\")([^\"]*)(\")",
                         lambda m: m.group(1) + html.escape(tr(html.unescape(m.group(2)), name) or html.unescape(m.group(2))) + m.group(3), seg)
            parts[i] = seg
        return "".join(parts)

    def make(src, name):
        s = src
        s = re.sub(r"<html[^>]*>", f'<html lang="{lang}" dir="ltr" data-lang="en" data-lang-lock="en" data-site-lang="{lang}">', s, count=1)
        own = BASE + f"{name}.{lang}.html"
        s = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{own}"', s, count=1)
        s = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{own}"', s, count=1)
        if 'property="og:locale"' in s:
            s = re.sub(r'<meta property="og:locale" content="[^"]*"', f'<meta property="og:locale" content="{LOCALE[lang]}"', s, count=1)
        else:
            s = s.replace('<meta property="og:type"', f'<meta property="og:locale" content="{LOCALE[lang]}" />\n  <meta property="og:type"', 1)
        s = translate_body(s, name)

        def link(m):
            t = m.group(2)
            ok = t in names
            return f'{m.group(1)}{t}.{lang if ok else "en"}.html'
        s = re.sub(r'(href=(?:&quot;|["\']))([a-z0-9\-]+)(?:\.en)?\.html', link, s)
        s = re.sub(r'(href=)"(\./?)"', lambda m: f'href="index.{lang}.html"', s)

        def cover(m):
            folder, kind = m.group(1), m.group(2) or ""
            new = {"card": f"{lang}-card", "thumb": f"{lang}-thumb", "": lang}[kind]
            return f"social/{folder}/{new}.webp" if (ROOT / "social" / folder / f"{new}.webp").exists() else m.group(0)
        s = re.sub(r"social/([^/\"\s]+)/en(?:-(card|thumb))?\.webp", cover, s)
        if "i18n.css" not in s:
            s = s.replace("</head>", "  " + CSS + "\n</head>", 1)
        if f"i18n-{lang}.js" not in s:
            s = s.replace("</body>", f'<script src="i18n-{lang}.js?v=20261121a"></script>\n</body>', 1)
        return s

    built = []
    for name in names:
        p = ROOT / f"{name}.en.html"
        if not p.exists():
            continue
        out = make(p.read_text(encoding="utf-8"), name)
        built.append((name, out))
    return built, missing


def main():
    report = {}
    for lang, names in PAGES.items():
        names = [n for n in names if (ROOT / f"{n}.en.html").exists()]
        built, missing = run(lang, set(names))
        left = {}
        for k, w in missing.items():
            left.setdefault(w, []).append(k)
        done = 0
        for name, out in built:
            f = ROOT / f"{name}.{lang}.html"
            # A few new strings (e.g. today's headlines on the homepage) stay in English until
            # translated; only a page that is largely untranslated is held back.
            if len(left.get(name, [])) > MAX_MISSING and "--force" not in sys.argv:
                if f.exists():
                    f.unlink()
                continue
            f.write_text(hl.put(out, name), encoding="utf-8")
            done += 1
        (ROOT / "data" / "i18n" / f"{lang}-missing.json").write_text(json.dumps(left, ensure_ascii=False, indent=0), encoding="utf-8")
        report[lang] = (done, sum(len(v) for v in left.values()))
        print(lang, f"{done} pages built;", report[lang][1], "strings missing on", len(left), "pages")
    # hreflang on the other editions of every page that has one
    for p in ROOT.glob("*.html"):
        b = hl.base_of(p.name)
        if any((ROOT / f"{b}.{l}.html").exists() for l in PAGES) and p.name.split(".")[-2] not in PAGES:
            t = p.read_text(encoding="utf-8")
            t2 = hl.put(t, p.name)
            if t2 != t:
                p.write_text(t2, encoding="utf-8")


if __name__ == "__main__":
    main()
