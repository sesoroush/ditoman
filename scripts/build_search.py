#!/usr/bin/env python3
"""Build search-index.json for the site search (search.js).

One entry per public page: url, Persian and English titles, category,
description, cover image and a plain-text excerpt of the page body.
Story categories come from the homepage cards (index.html is the source
of truth for stories); other pages are grouped by type.

Run from the repo root: python3 scripts/build_search.py
"""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"404.html"}
TEXT_LIMIT = 2400  # characters of body text kept per page
FA = re.compile(r"[؀-ۿ]")


class Text(HTMLParser):
    """Collects visible body text, skipping scripts, styles, header, nav and footer."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "header", "nav", "footer", "template", "aside"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.in_body = False
        self.parts = []
        self.h1 = []
        self._h1 = None

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        if tag in self.SKIP_TAGS:
            self.depth += 1
        if tag == "h1" and not self.depth:
            self._h1 = []
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "br", "div", "td"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.depth:
            self.depth -= 1
        if tag == "h1" and self._h1 is not None:
            self.h1.append(" ".join("".join(self._h1).split()))
            self._h1 = None

    def handle_data(self, data):
        if not self.in_body or self.depth:
            return
        self.parts.append(data)
        if self._h1 is not None:
            self._h1.append(data)


def meta(src, name):
    m = re.search(r'<meta (?:name|property)="%s" content="([^"]*)"' % re.escape(name), src)
    return html.unescape(m.group(1)).strip() if m else ""


def clean(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def story_cards(index_src):
    """slug -> (en title, fa title, fa category, en category) from homepage cards."""
    out = {}
    for m in re.finditer(r'<a class="co-card[^"]*"[^>]*href="([^"]+)"(.*?)</a>', index_src, re.S):
        href, body = m.group(1), m.group(2)
        cat = re.search(r'class="co-cat[^"]*"><span lang="fa">(.*?)</span><span lang="en">(.*?)</span>', body)
        h3 = re.search(r"<h3>(.*?)<span lang=\"fa\">(.*?)</span></h3>", body, re.S)
        if not h3:
            continue
        out[href] = (
            clean(h3.group(1)),
            clean(h3.group(2)),
            clean(cat.group(1)) if cat else "مطلب",
            clean(cat.group(2)) if cat else "Story",
        )
    return out


def linked_from(page):
    p = ROOT / page
    if not p.exists():
        return set()
    return set(re.findall(r'href="([a-z0-9-]+\.html)"', p.read_text(encoding="utf-8")))


def main():
    index_src = (ROOT / "index.html").read_text(encoding="utf-8")
    sec = index_src[index_src.index('id="stories"'):]
    sec = sec[:sec.index("</section>")]
    stories = story_cards(sec)
    iran_pages = {p.name for p in ROOT.glob("iran-*.html")}

    entries = []
    for path in sorted(ROOT.glob("*.html")):
        name = path.name
        if name in SKIP or name.endswith(".en.html"):
            continue
        src = path.read_text(encoding="utf-8")
        if 'name="robots" content="noindex' in src:
            continue
        parser = Text()
        parser.feed(src)
        body = " ".join("".join(parser.parts).split())

        title_tag = clean(re.search(r"<title>(.*?)</title>", src, re.S).group(1)) if "<title>" in src else name
        segs = [s.strip() for s in title_tag.split("|") if s.strip()]
        brand = {"ditoman", "ditoman learn", "iranian companies", "what iran has"}
        core = [x for x in segs if x.lower() not in brand] or segs or [name]
        fa_title = ""
        m = re.match(r"^(.*?)\s*\(([^)]*[\u0600-\u06FF][^)]*)\)\s*$", core[0])
        if m:  # company pages: "Kalleh (کاله)"
            core[0], fa_title = m.group(1).strip(), m.group(2).strip()
        en_parts = [x for x in core if not FA.search(x)]
        en_title = ": ".join(en_parts[:2]) if en_parts else core[0]
        fa_title = fa_title or next((x for x in core if FA.search(x)), "")
        if not fa_title:
            fa_title = next((h for h in parser.h1 if FA.search(h)), "")
        desc = meta(src, "description") or meta(src, "og:description")
        image = meta(src, "og:image").replace("https://ditoman.com/", "")

        if name in stories:
            en_title, fa_title, cat_fa, cat_en = stories[name]
            kind = "story"
        elif re.match(r"lesson\d+\.html$", name) or name == "learn.html":
            cat_fa, cat_en, kind = "آموزش", "Learn", "lesson"
        elif "| Iranian Companies |" in src[:src.find("</title>")]:
            cat_fa, cat_en, kind = "شرکت‌ها", "Companies", "company"
        elif name in iran_pages or name == "iran.html":
            cat_fa, cat_en, kind = "ایران چه دارد", "What Iran has", "iran"
        else:
            cat_fa, cat_en, kind = "بخش سایت", "Section", "page"

        m_img = re.search(r'<img lang="en" src="([^"]+)"', src)
        image_en = m_img.group(1) if m_img else ""
        entries.append({
            "u": name if name != "index.html" else "./",
            "t": en_title,
            "f": fa_title,
            "c": cat_fa,
            "ce": cat_en,
            "k": kind,
            "d": desc[:400],
            "i": image,
            "ie": image_en,
            "x": body[:TEXT_LIMIT],
        })

    order = {"story": 0, "lesson": 1, "iran": 2, "company": 3, "page": 4}
    story_order = list(stories)
    entries.sort(key=lambda e: (order[e["k"]], story_order.index(e["u"]) if e["u"] in stories else 0, e["u"]))
    out = ROOT / "search-index.json"
    out.write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(entries)} pages, {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
