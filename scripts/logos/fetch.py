"""Logo finder run by logos.yml. For each company in targets.json:
Wikipedia page -> Wikidata logo image (P154) -> Wikimedia Commons file; fallbacks: page image whose name says logo,
Commons file search, and the og:image of the official website (P856). Saves a <=512px file in data/logos/files/<slug>.<ext>
and the source, licence and credit in data/logos/results.json. Nothing is published from here; a human reviews the result."""
import json, pathlib, re, time, urllib.request, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent.parent / "data" / "logos"
FILES = OUT / "files"; FILES.mkdir(parents=True, exist_ok=True)
UA = "DitomanBot/1.0 (https://ditoman.com; company profile logos) python-urllib"


def get(url, raw=False, timeout=40):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
                d = r.read()
                return d if raw else json.loads(d)
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def wp(lang, **p):
    p["format"] = "json"
    return get(f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)) or {}


def commons_info(fname):
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": "File:" + fname, "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime|size", "iiurlwidth": 512})) or {}
    for pg in d.get("query", {}).get("pages", {}).values():
        ii = (pg.get("imageinfo") or [None])[0]
        if ii:
            m = ii.get("extmetadata", {})
            return {"url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl"), "mime": ii.get("mime"),
                    "license": m.get("LicenseShortName", {}).get("value", ""), "artist": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")),
                    "source": "commons"}
    return None


def enwiki_file(lang, fname):
    d = wp(lang, action="query", titles="File:" + fname, prop="imageinfo", iiprop="url|extmetadata|mime", iiurlwidth=512)
    for pg in d.get("query", {}).get("pages", {}).values():
        ii = (pg.get("imageinfo") or [None])[0]
        if ii:
            m = ii.get("extmetadata", {})
            return {"url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl"), "mime": ii.get("mime"),
                    "license": m.get("LicenseShortName", {}).get("value", "non-free / unknown"), "artist": "", "source": lang + "wiki"}
    return None


def wikidata(qid):
    d = get("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": qid, "props": "claims", "format": "json"})) or {}
    cl = d.get("entities", {}).get(qid, {}).get("claims", {})
    def first(p):
        for s in cl.get(p, []):
            v = s.get("mainsnak", {}).get("datavalue", {}).get("value")
            if v:
                return v
    return first("P154"), first("P856")


def og_image(site):
    h = get(site, raw=True, timeout=25)
    if not h:
        return None
    h = h.decode("utf-8", "ignore")
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', h, re.I) or \
        re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', h, re.I)
    return urllib.parse.urljoin(site, m.group(1)) if m else None


def search_commons(name):
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "list": "search", "srnamespace": 6, "srsearch": name + " logo", "srlimit": 5})) or {}
    toks = [t.lower() for t in re.findall(r"[A-Za-z]{3,}", name)][:2]
    for r in d.get("query", {}).get("search", []):
        t = r["title"][5:]
        if "logo" in t.lower() and toks and all(x in t.lower() for x in toks[:1]):
            return t
    return None


T = json.load(open(ROOT / "targets.json"))
R = {}
for slug, t in T.items():
    res = {"slug": slug, "found": False, "tried": []}
    info = None; site = None
    for lang, title in t["cand"] or []:
        d = wp(lang, action="query", titles=title, redirects=1, prop="pageprops|pageimages", ppprop="wikibase_item", piprop="name")
        for pg in d.get("query", {}).get("pages", {}).values():
            q = pg.get("pageprops", {}).get("wikibase_item")
            if q:
                logo, site2 = wikidata(q)
                site = site or site2
                res["tried"].append(f"{lang}:{title}:{q}:{logo}")
                if logo and not info:
                    info = commons_info(logo)
            pi = pg.get("pageimage")
            if pi and re.search("logo|لوگو|نشان", pi, re.I) and not info:
                info = commons_info(pi) or enwiki_file(lang, pi)
    if not info:
        n = search_commons(t["en"])
        res["tried"].append("commons-search:" + str(n))
        if n:
            info = commons_info(n)
    if not info and site:
        u = og_image(site)
        res["tried"].append("og:" + str(u))
        if u:
            info = {"url": u, "page": site, "mime": "", "license": "website image, trademark of its owner", "artist": "", "source": "website"}
    if info:
        data = get(info["url"], raw=True)
        if data and len(data) > 300:
            ext = {"image/png": "png", "image/jpeg": "jpg", "image/svg+xml": "png", "image/webp": "webp", "image/gif": "gif"}.get(info.get("mime"), None)
            if not ext:
                ext = "png" if data[:4] == b"\x89PNG" else "jpg" if data[:2] == b"\xff\xd8" else "webp" if data[8:12] == b"WEBP" else "bin"
            fn = f"{slug}.{ext}"
            (FILES / fn).write_bytes(data)
            res.update(found=True, file=fn, bytes=len(data), **{k: info[k] for k in ("page", "license", "artist", "source")}, site=site)
    R[slug] = res
    print(slug, res["found"], res.get("source"), res.get("license"))
(OUT / "results.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(1 for r in R.values() if r["found"]), "of", len(R), "found")
