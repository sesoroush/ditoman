"""Wikipedia helper run by wiki.yml.
Phase 1: members of a few categories (en + fa).  Phase 2: intro extracts for the titles listed in scripts/wiki/titles.json.
Output goes to data/iran/wiki/.
"""
import json, pathlib, urllib.request, urllib.parse, time
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent.parent / "data" / "iran" / "wiki"
OUT.mkdir(parents=True, exist_ok=True)
UA = "DitomanBot/1.0 (https://ditoman.com; fact checking for company profiles) python-urllib"


def api(lang, **p):
    p["format"] = "json"
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa
            time.sleep(3 * (i + 1))
    return {"error": "failed", "url": url}


CATS = {
    "en": ["Category:Technology companies of Iran", "Category:Pharmaceutical companies of Iran", "Category:Biotechnology companies of Iran",
           "Category:Software companies of Iran", "Category:Internet companies of Iran", "Category:Companies based in Tehran",
           "Category:Electronics companies of Iran", "Category:Aerospace companies of Iran", "Category:Medical technology companies of Iran",
           "Category:Telecommunications companies of Iran", "Category:Engineering companies of Iran", "Category:Iranian brands",
           "Category:Chemical companies of Iran", "Category:Iranian inventions", "Category:Online retailers of Iran", "Category:Financial technology companies of Iran"],
    "fa": ["رده:شرکت‌های دانش‌بنیان ایران", "رده:شرکت‌های فناوری اطلاعات ایران", "رده:شرکت‌های دارویی ایران", "رده:شرکت‌های زیست‌فناوری ایران",
           "رده:شرکت‌های نرم‌افزاری ایران", "رده:شرکت‌های اینترنتی ایران", "رده:شرکت‌های الکترونیک ایران", "رده:شرکت‌های فناوری ایران",
           "رده:شرکت‌های فناوری نانو ایران", "رده:شرکت‌های فین‌تک ایران", "رده:شرکت‌های تجهیزات پزشکی ایران"],
}
res = {}
for lang, cats in CATS.items():
    for c in cats:
        d = api(lang, action="query", list="categorymembers", cmtitle=c, cmlimit="500", cmtype="page")
        res[f"{lang}:{c}"] = [m["title"] for m in d.get("query", {}).get("categorymembers", [])] if "query" in d else d
(OUT / "categories.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

tf = ROOT / "titles.json"
if tf.exists():
    titles = json.loads(tf.read_text(encoding="utf-8"))   # {"slug": {"en": "...", "fa": "..."}}
    out = {}
    for slug, t in titles.items():
        out[slug] = {}
        for lang in ("en", "fa"):
            if not t.get(lang):
                continue
            d = api(lang, action="query", prop="extracts|pageprops|info", exintro="1", explaintext="1", redirects="1", titles=t[lang], inprop="url")
            pages = d.get("query", {}).get("pages", {})
            for pg in pages.values():
                out[slug][lang] = {"title": pg.get("title"), "url": pg.get("fullurl"), "extract": (pg.get("extract") or "")[:2500], "missing": "missing" in pg}
    (OUT / "extracts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()})
