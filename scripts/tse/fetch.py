"""Rank listed companies by market value from the official TSETMC market watch (run by tse.yml).

Writes data/iran/tse/stocks.json: every listed company (Tehran Stock Exchange, Farabourse, Farabourse
base market) with last closing price, shares, market value, sector, ISIN; and for the top 260 the
instrument card (sector name, English short name) fetched one by one.
Market value in billion toman = last closing price (rial) / 10 * shares / 1e9.
"""
import json, pathlib, urllib.request, time, concurrent.futures as cf
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "iran" / "tse"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
MW = ("https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&paperTypes[0]=1&paperTypes[1]=2&paperTypes[2]=3&paperTypes[3]=4"
      "&paperTypes[4]=5&paperTypes[5]=6&paperTypes[6]=7&paperTypes[7]=8&paperTypes[8]=9&showTraded=false&withBestLimits=true")
INFO = "https://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/"


def get(url, tries=3, timeout=25):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json", "Referer": "https://main.tsetmc.com/"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (i + 1))
    raise last


def fix(s):
    return (s or "").replace("ي", "ی").replace("ك", "ک").replace("‌", " ").strip()


rows = json.loads(get(MW, timeout=90))["marketwatch"]
(OUT / "marketwatch.json").write_bytes(json.dumps({"marketwatch": rows}, ensure_ascii=False).encode())
best = {}
for r in rows:
    if r["yVal"] not in (300, 303, 309) or not r["insID"] or not r["ztd"] or not r["pcl"]:
        continue
    sym = fix(r["lva"])
    if sym.endswith("ح") or any(ch.isdigit() for ch in sym[-1:]):
        continue
    code = r["insID"][4:8]
    mc = r["pcl"] / 10 * r["ztd"] / 1e9
    if code not in best or mc > best[code]["mcap"]:
        best[code] = dict(sym=sym, name=fix(r["lvc"]), isin=r["insID"], insCode=r["insCode"], price_rial=r["pcl"], shares=r["ztd"],
                          mcap=round(mc), yVal=r["yVal"], flow=r["flow"], csv=fix(r.get("csv")))
ranked = sorted(best.values(), key=lambda x: -x["mcap"])
for i, x in enumerate(ranked, 1):
    x["rank"] = i


def card(x):
    try:
        j = json.loads(get(INFO + x["insCode"]))["instrumentInfo"]
        x["sector"] = fix(j["sector"]["lSecVal"]); x["sector_code"] = j["sector"]["cSecVal"].strip()
        x["en"] = j.get("lVal18"); x["shares_card"] = j.get("zTitad"); x["market_title"] = j.get("flowTitle"); x["group"] = j.get("cgrValCotTitle")
    except Exception as e:  # noqa
        x["card_error"] = str(e)[:80]
    return x


with cf.ThreadPoolExecutor(8) as ex:
    list(ex.map(card, ranked[:260]))
(OUT / "stocks.json").write_text(json.dumps({"date_hint": "see marketwatch", "count": len(ranked), "companies": ranked}, ensure_ascii=False, indent=0), encoding="utf-8")
print("companies", len(ranked), "cards ok", sum(1 for x in ranked[:260] if "sector" in x))
