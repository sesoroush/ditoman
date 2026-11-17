"""Apply reviewed logos from data/logos/ to company records: companies/<slug>/logo.webp, credit line, English-page rule."""
import json, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
res = json.load(open(R / "data/logos/results.json"))
REJECT = {"aryogen", "asiatech", "pars-online", "rubika", "x-vision"}   # wrong or blank image on review
FA_ONLY = {"cafebazaar", "divar", "fidibo", "mobinnet", "namava", "neshan", "nosa", "okala", "parsijoo", "zarinpal"}  # logo contains Persian script
n = 0
for slug, r in res.items():
    if not r["found"] or slug in REJECT:
        continue
    im = Image.open(R / "data/logos/files" / r["file"]).convert("RGBA")
    im.thumbnail((320, 320))
    d = R / "companies" / slug; d.mkdir(parents=True, exist_ok=True)
    im.save(d / "logo.webp", "WEBP", quality=88, method=6)
    p = R / "data/companies" / f"{slug}.json"
    c = json.load(open(p))
    c["logo"] = "logo.webp"
    c["logo_fa_only"] = slug in FA_ONLY
    lic = r["license"] or "see source"
    c["logo_credit"] = {"fa": f"لوگو: {r['source'] == 'commons' and 'ویکی‌مدیا کامنز' or 'منبع عمومی'} ({lic})؛ نشان تجاری صاحب آن است.",
                        "en": f"Logo: {'Wikimedia Commons' if r['source'] == 'commons' else 'public source'} ({lic}); a trademark of its owner."}
    c["logo_credit"]["url"] = r.get("page") or ""
    json.dump(c, open(p, "w"), ensure_ascii=False, indent=1)
    n += 1
print(n, "logos applied")
