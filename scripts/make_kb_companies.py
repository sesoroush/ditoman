"""Write data/companies/<slug>.json for the knowledge-based & technology list from scripts/kb_data.py."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / "scripts"))
from kb_data import K, LAB
ex = json.load(open(R / "data/iran/wiki/extracts.json"))
CHECKED = {"fa": "۲۶ آبان ۱۴۰۵", "en": "17 November 2026"}
SECTOR = {"id": "knowledge", "fa": "شرکت‌های دانش‌بنیان و فناور", "en": "Knowledge-based and technology companies"}
for c in K:
    v = ex[c["key"]]
    lang = "en" if (v.get("en") and not v["en"]["missing"] and v["en"]["extract"]) else "fa"
    x = v[lang]
    if lang == "en":
        src = {"id": 1, "title": "ویکی‌پدیا (انگلیسی): " + x["title"], "title_en": "Wikipedia: " + x["title"], "url": x["url"]}
    else:
        src = {"id": 1, "title": "ویکی‌پدیا (فارسی): " + x["title"], "title_en": "Wikipedia (Persian edition): " + c["en"], "url": x["url"]}
    facts = [{"label": {"fa": LAB[k][0], "en": LAB[k][1]}, "value": {"fa": fa, "en": en}, "src": [1]} for k, fa, en in c["facts"]]
    if c["official"]:
        facts.insert(0, {"label": {"fa": "وضعیت", "en": "Status"}, "value": {"fa": "ویکی‌پدیا آن را «دانش‌بنیان» می‌نامد", "en": "Wikipedia calls it a knowledge-based company"}, "src": [1]})
    rec = {
        "slug": c["slug"], "status": "published", "last_checked": CHECKED, "sector": SECTOR,
        "branch": c["branch"], "sub": c["sub"], "name": {"fa": c["fa"], "en": c["en"]}, "logo": None,
        "tagline": {"fa": c["tfa"], "en": c["ten"]}, "facts": facts,
        "summary": {"fa": c["sfa"], "en": c["sen"]}, "summary_src": [1],
        "photos": {"main": {"file": None, "art": "office", "alt": {"fa": "تصویرسازی", "en": "Illustration"}}},
        "unconfirmed": {
            "fa": ["ثبت رسمی به‌عنوان شرکت «دانش‌بنیان» در فهرست معاونت علمی و فناوری ریاست‌جمهوری؛ هنوز با منبع رسمی تطبیق نداده‌ایم", "ارقام مالی (فروش، دارایی) و فهرست مدیران"],
            "en": ["Official registration as a knowledge-based company by the Vice-Presidency for Science and Technology; we have not yet matched it against the official register", "Financial figures (sales, assets) and leadership"]},
        "disclosure": {"fa": "این پرونده بر پایه‌ی منبع عمومی (ویکی‌پدیا) نوشته شده و شرکت پیش از انتشار آن را بازبینی نکرده است. «دانش‌بنیان» بودن رسمی را جداگانه و از فهرست رسمی تأیید می‌کنیم.",
                       "en": "This record is based on a public source (Wikipedia) and was not reviewed by the company before publication. Official knowledge-based status is something we confirm separately against the official register."},
        "sources": [src],
    }
    (R / "data/companies" / f'{c["slug"]}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(K), "records")
