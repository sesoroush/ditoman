"""Probe IMI-100 (Industrial Management Institute ranking of Iran's top companies) from a GitHub runner.
Saves every link on the IMI-100 site's main pages and the text of pages that look like ranking tables."""
import json, pathlib, re, urllib.request, urllib.parse, html
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
BASE = "https://imi100.imi.ir/"


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace"), r.geturl()


def text(h):
    h = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


res = {"pages": {}, "links": {}}
seen, queue = set(), [BASE]
while queue and len(seen) < 40:
    u = queue.pop(0)
    if u in seen:
        continue
    seen.add(u)
    try:
        h, final = get(u)
    except Exception as e:  # noqa
        res["pages"][u] = {"error": str(e)[:200]}; continue
    links = {}
    for href, label in re.findall(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', h, re.S):
        full = urllib.parse.urljoin(final, html.unescape(href))
        links[full] = text(label)[:80]
    res["links"][u] = links
    res["pages"][u] = {"final": final, "text": text(h)[:20000], "tables": h.count("<table")}
    for l, lab in links.items():
        if l.startswith(BASE) and not re.search(r"\.(jpg|png|pdf|xlsx?|zip)$", l, re.I) and \
                re.search(r"رتبه|۵۰۰|500|100|۱۰۰|IMI|شرکت|فهرست|جدول|ranking|rank", lab + l, re.I):
            queue.append(l)
(OUT / "imi.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(seen), "pages")
