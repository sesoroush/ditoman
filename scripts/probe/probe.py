"""Probe IMI-100 ranking pages: save raw HTML (scripts included) so the data endpoint can be found."""
import json, pathlib, urllib.request, urllib.parse
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
URLS = ["https://imi100.imi.ir/Ranking", "https://imi100.imi.ir/Ranking/p/500",
        "https://imi100.imi.ir/blog/ID/2707/معرفی-شرکتهای-برتر-از-نظر-شاخص-فروش",
        "https://imi100.imi.ir/blog/ID/2785/معرفی-شرکت-های-برتر-صادرات-گرا-در-سال-1404"]
for i, u in enumerate(URLS):
    s = urllib.parse.urlsplit(u)
    u2 = urllib.parse.urlunsplit((s.scheme, s.netloc, urllib.parse.quote(s.path), s.query, ""))
    try:
        req = urllib.request.Request(u2, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=40) as r:
            (OUT / f"raw{i}.html").write_bytes(r.read())
    except Exception as e:  # noqa
        (OUT / f"raw{i}.html").write_text("ERROR " + str(e), encoding="utf-8")
print("ok")
