"""All companies listed on the Tehran Stock Exchange, Farabourse and the Farabourse base market, ranked by market value.

Starts from data/iran/top200.json (hand-checked names, branches and families for the first 200), adds every other
listed company from the official TSETMC market watch (data/iran/tse/marketwatch.json), with English names from
scripts/listed_names.tsv and a branch/sub-branch from the official TSETMC industry code. Writes data/iran/listed.json.
"""
import json, re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
T = json.load(open(R / "data/iran/top200.json", encoding="utf-8"))
MW = json.load(open(R / "data/iran/tse/marketwatch.json", encoding="utf-8"))["marketwatch"]
NAMES = {}
for line in open(R / "scripts/listed_names.tsv", encoding="utf-8"):
    if line.strip() and not line.startswith("#"):
        p = line.rstrip("\n").split("\t")
        NAMES[p[0]] = p[1:]

# TSETMC industry code -> (branch, sub-branch)
CSV = {"01": ("industry", "food"), "10": ("resources", "minerals"), "11": ("energy", "upstream"), "13": ("resources", "metals"),
       "14": ("resources", "minerals"), "17": ("industry", "textile"), "19": ("industry", "textile"), "20": ("industry", "wood"),
       "21": ("industry", "wood"), "22": ("industry", "wood"), "23": ("energy", "refining"), "25": ("industry", "chem"),
       "26": ("industry", "consumer"), "27": ("industry", "steel"), "28": ("industry", "machinery"), "29": ("industry", "machinery"),
       "31": ("industry", "machinery"), "32": ("industry", "consumer"), "34": ("industry", "auto"), "38": ("industry", "food"),
       "39": ("technology", "finance"), "40": ("energy", "power"), "42": ("industry", "food"), "43": ("industry", "pharma"),
       "44": ("energy", "petrochem"), "45": ("industry", "construction"), "46": ("industry", "consumer"), "47": ("industry", "consumer"),
       "49": ("industry", "construction"), "53": ("industry", "construction"), "54": ("industry", "construction"),
       "55": ("tourism", "hotels"), "56": ("technology", "finance"), "57": ("technology", "finance"), "58": ("technology", "finance"),
       "60": ("transport", "logistics"), "61": ("transport", "sea"), "64": ("technology", "telecom"), "66": ("technology", "finance"),
       "67": ("technology", "finance"), "70": ("industry", "construction"), "71": ("industry", "machinery"), "72": ("technology", "platforms"),
       "73": ("technology", "telecom"), "74": ("industry", "machinery"), "84": ("technology", "finance"), "90": ("tourism", "arts"), "93": ("tourism", "arts")}
MK = {300: "bourse", 303: "farabourse", 309: "base", 313: "base"}


def fix(s):
    s = (s or "").replace("ي", "ی").replace("ك", "ک").replace("‌", " ")
    return re.sub(r"\s+", " ", s).strip()


best = {}
for r in MW:
    if r["yVal"] not in MK or not r["insID"] or not r["ztd"] or not r["pcl"]:
        continue
    sym = fix(r["lva"])
    if sym.endswith("ح") or sym[-1:].isdigit():
        continue
    code = r["insID"][4:8]
    mc = round(r["pcl"] / 10 * r["ztd"] / 1e9)
    if code not in best or mc > best[code]["mcap"]:
        best[code] = dict(sym=sym, name=fix(r["lvc"]), isin=r["insID"], mcap=mc, yVal=r["yVal"], csv=fix(r.get("csv")))

out = list(T["companies"])
for c in out:
    k = c["isin"][4:8]
    if k in best:
        c["market"] = MK[best[k]["yVal"]]
have = {c["isin"][4:8] for c in out}
missing = []
for code, c in best.items():
    if code in have:
        continue
    if c["sym"] not in NAMES:
        missing.append(c["sym"]); continue
    en, *rest = NAMES[c["sym"]]
    fa = rest[0] if rest and rest[0] else c["name"]
    if fa.count("(") > fa.count(")"):
        fa = fa.split("(")[0].strip()
    br, sub = (rest[1], rest[2]) if len(rest) > 2 and rest[1] else CSV[c["csv"]]
    if br == "energy" and sub == "petrochem" and "پتروشیمی" not in fa and "پترو" not in fa:
        br, sub = "industry", "chem"
    out.append(dict(sym=c["sym"], fa=fa, en=en, branch=br, sub=sub, isin=c["isin"], market=MK[c["yVal"]],
                    listed=True, mcap=c["mcap"], weight=c["mcap"], stale=False))
# --- Sales from IMI-100 (Industrial Management Institute ranking of Iran's 500 largest companies, fiscal 1403) ---
IMI = json.load(open(R / "data/iran/imi/imi500_1403.json", encoding="utf-8"))
SKIP = {199, 203, 267, 300, 426, 458, 477, 489, 491, 493}  # fuzzy matches that are a different company
FORCE = {147: "خوساز"}


def imi_norm(s):
    s = s.replace("ي", "ی").replace("ك", "ک").replace("\u200c", "")
    for w in ["(هولدینگ)", "هولدینگ", "(هلدینگ)", "هلدینگ", "شرکت", "سهامی عام", "سهامی خاص", "(", ")", "-", ".", "«", "»", " "]:
        s = s.replace(w, "")
    return s


idx = {imi_norm(c["fa"]): c for c in out}
bysym = {c["sym"]: c for c in out}
for x in sorted(IMI, key=lambda x: x["RankingSalesThisYear"]):
    r = x["RankingSalesThisYear"]
    if r in SKIP:
        continue
    n = imi_norm(x["CompanyNameFa"])
    c = bysym.get(FORCE.get(r)) or idx.get(n)
    if not c:
        hits = [k for k in idx if len(n) > 6 and len(k) > 6 and (n in k or k in n)]
        c = idx[hits[0]] if len(hits) == 1 else None
    if c and "sales" not in c:
        c["sales"] = round(x["Sales"] / 10)  # billion rial -> billion toman
        c["figures_year"] = 1403
        c["imi_rank"] = r
if missing:
    raise SystemExit(f"no English name for {len(missing)}: {missing[:20]}")
out.sort(key=lambda c: -c["mcap"])
for i, c in enumerate(out, 1):
    c["rank"] = i
n = len(out)
T["companies"] = out
fa_n = str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
T["method"] = {"fa": f"همه‌ی {fa_n} شرکت سهامی بورس تهران، فرابورس و بازار پایه‌ی فرابورس به ترتیب ارزش بازار آمده‌اند؛ حق‌تقدم‌ها، صندوق‌ها و اوراق کنار گذاشته شده‌اند. پنج شرکت (ایران‌خودرو، پتروشیمی پردیس، بانک پاسارگاد، بانک شهر، پارس آریان) در فهرست آن روز نبودند (بسته یا متوقف)؛ رقمشان از آخرین داده‌ی در دسترس (۱۴ آبان ۱۴۰۵) است و با «*» مشخص شده. شاخه‌ی ۲۰۰ شرکت اول را ما بر پایه‌ی فعالیت اصلی‌شان تعیین کرده‌ایم و بقیه را بر پایه‌ی گروه صنعت رسمی‌شان در سامانه‌ی بورس.",
               "en": f"All {n} listed companies on the Tehran Stock Exchange, the Farabourse and the Farabourse base market, ranked by market value; rights issues, funds and bonds are excluded. Five companies (Iran Khodro, Pardis Petrochemical, Bank Pasargad, Bank Shahr, Pars Arian) were absent from that day's list (closed or halted); their figures come from the latest data available (5 Nov 2026) and are marked with an asterisk. We assigned the branch of the first 200 by their main activity, and the rest by their official industry group on the exchange system."}
json.dump(T, open(R / "data/iran/listed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(n, "companies")
