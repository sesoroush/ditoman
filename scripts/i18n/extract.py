"""List the Persian strings of the given pages (text nodes and translatable attributes), in page order, unique.
Usage: python3 scripts/i18n/extract.py page.html ... > out.json"""
import html, json, re, sys
from html.parser import HTMLParser

FA = re.compile(r"[؀-ۿ]")
ATTRS = {"alt", "title", "aria-label", "placeholder", "data-fa", "data-fa-label", "data-kicker", "data-cat", "content", "data-en-label"}


def norm(s):
    return " ".join(html.unescape(s).split())


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        for k, v in attrs:
            if v and k in ATTRS and FA.search(v):
                if k == "content" and dict(attrs).get("name") not in ("description", "twitter:title", "twitter:description") and dict(attrs).get("property") not in ("og:title", "og:description", "og:image:alt"):
                    continue
                self.out.append(norm(v))
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
    def handle_data(self, d):
        if self.skip:
            return
        t = norm(d)
        if t and FA.search(t):
            self.out.append(t)


def strings(path):
    p = P(); p.feed(re.sub(r'<a class="xl" href="[^"]*">(.*?)</a>', r"\1", open(path, encoding="utf-8").read(), flags=re.S)); return p.out


if __name__ == "__main__":
    seen, res = set(), []
    for f in sys.argv[1:]:
        for s in strings(f):
            if s not in seen:
                seen.add(s); res.append(s)
    json.dump(res, sys.stdout, ensure_ascii=False, indent=0)
