"""Merge official TSETMC ranking (data/iran/tse/stocks.json) with hand metadata -> data/iran/top200.json"""
import json, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / "scripts"))
from top200_meta import M
t = json.load(open(R / "data/iran/top100.json"))
s = json.load(open(R / "data/iran/tse/stocks.json"))["companies"]
by = {c["isin"][4:8]: c for c in s}
mk = {300: "bourse", 303: "farabourse", 309: "farabourse"}
out = []
for c in t["companies"]:
    n = dict(c); k = c["isin"][4:8]
    if k in by:
        n["mcap"] = n["weight"] = by[k]["mcap"]; n["sym"] = by[k]["sym"]; n.pop("mcap_est", None); n["stale"] = False
    else:
        n["stale"] = True; n["mcap"] = c.get("mcap") or c["weight"]; n["weight"] = n["mcap"]
    out.append(n)
seen = {c["isin"][4:8] for c in out}; cnt = 0
for c in s:
    if c["isin"][4:8] in seen: continue
    cnt += 1
    if cnt > 100: break
    fa, en, br, sub = M[c["sym"]]
    out.append(dict(sym=c["sym"], fa=fa, en=en, branch=br, sub=sub, isin=c["isin"], market=mk.get(c["yVal"], "bourse"),
                    listed=True, mcap=c["mcap"], weight=c["mcap"], stale=False))
out.sort(key=lambda c: -c["mcap"])
for i, c in enumerate(out, 1): c["rank"] = i
t["companies"] = out
t["as_of"] = {"fa": "۲۶ آبان ۱۴۰۵", "en": "17 November 2026"}
t["source"] = {"fa": "داده‌های رسمی بازار از سامانه‌ی مدیریت فناوری بورس تهران (TSETMC)؛ ارزش بازار = قیمت پایانی آخرین روز معاملاتی × تعداد سهام، به میلیارد تومان.",
               "en": "Official market data from the Tehran Securities Exchange Technology Management Co. (TSETMC); market value = last closing price × shares outstanding, in billion toman."}
t["method"] = {"fa": "۲۰۰ شرکت با بیشترین ارزش بازار در بورس و فرابورس رتبه‌بندی شده‌اند؛ حق‌تقدم‌ها و صندوق‌ها کنار گذاشته شده‌اند. پنج شرکت (ایران‌خودرو، پتروشیمی پردیس، بانک پاسارگاد، بانک شهر، پارس آریان) در فهرست آن روز نبودند (بسته یا متوقف)؛ رقمشان از آخرین داده‌ی در دسترس (۱۴ آبان ۱۴۰۵) است و با «*» مشخص شده. شاخه و زیرشاخه‌ی هر شرکت را ما بر پایه‌ی فعالیت اصلی‌اش تعیین کرده‌ایم.",
               "en": "The 200 companies with the highest market value on the Bourse and Farabourse are ranked; rights issues and funds are excluded. Five companies (Iran Khodro, Pardis Petrochemical, Bank Pasargad, Bank Shahr, Pars Arian) were absent from that day's list (closed or halted); their figures come from the latest data available (5 Nov 2026) and are marked with an asterisk. We assigned each company's branch and sub-branch by its main activity."}
json.dump(t, open(R / "data/iran/top200.json", "w"), ensure_ascii=False, indent=1)
print(len(out), [(c["sym"], c["rank"]) for c in out if c["stale"]])
