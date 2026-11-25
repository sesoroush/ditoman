"""One-off reachability probe for Iranian official company-data sources (run by probe.yml from a GitHub runner).
Writes data/probe/result.json: status code, final URL and the first 3,000 characters of each page."""
import json, pathlib, urllib.request, urllib.parse
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
q = urllib.parse.quote("شیرین عسل")
URLS = [
    "https://www.rrk.ir/",
    "https://newspaper.rrk.ir/",
    f"https://newspaper.rrk.ir/Search?keyword={q}",
    "https://ilenc.ir/",
    "https://www.ilenc.ir/",
    "https://www.codal.ir/",
    "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false",
    "https://imi100.imi.ir/",
    "https://imi.ir/",
    "https://www.tsetmc.com/",
]
res = []
for u in URLS:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(200000).decode("utf-8", "replace")
            res.append({"url": u, "status": r.status, "final": r.geturl(), "head": body[:3000]})
    except Exception as e:  # noqa
        res.append({"url": u, "error": str(e)[:200]})
(OUT / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps([{k: v for k, v in r.items() if k != "head"} for r in res], ensure_ascii=False, indent=1))
