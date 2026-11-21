"""List the English strings of English twin pages (text nodes + translatable attributes), unique, in order.
Usage: python3 scripts/i18n/extract_en.py a.en.html b.en.html ... > out.json"""
import html, json, re, sys
from html.parser import HTMLParser

FA = re.compile(r"[؀-ۿ]")
LAT = re.compile(r"[A-Za-z]{2}")
ATTRS = {"alt", "title", "aria-label", "placeholder", "data-kicker", "data-en-label", "data-en"}
METAS = {"description", "twitter:title", "twitter:description", "og:title", "og:description", "og:image:alt"}


def norm(s):
    return " ".join(html.unescape(s).split())


def ok(t):
    return t and LAT.search(t) and not FA.search(t)


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.title = [], 0, False
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        a = dict(attrs)
        for k, v in attrs:
            if v and k in ATTRS and ok(norm(v)):
                self.out.append(norm(v))
        if tag == "meta" and (a.get("name") in METAS or a.get("property") in METAS) and a.get("content") and ok(norm(a["content"])):
            self.out.append(norm(a["content"]))
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
    def handle_data(self, d):
        if self.skip:
            return
        t = norm(d)
        if ok(t):
            self.out.append(t)


def strings(path):
    p = P(); p.feed(open(path, encoding="utf-8").read()); return p.out


if __name__ == "__main__":
    seen, res = set(), []
    for f in sys.argv[1:]:
        for s in strings(f):
            if s not in seen:
                seen.add(s); res.append(s)
    json.dump(res, sys.stdout, ensure_ascii=False, indent=0)
