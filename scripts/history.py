"""Build daily price-history series for the site's Prices page.

Pulls daily closes from TGJU's public history tables and merges them into
market/series/<key>.json as [["YYYY-MM-DD", value_in_toman], ...] (oldest first).

  python scripts/history.py --full     # backfill as far back as the source allows
  python scripts/history.py            # nightly: only the most recent rows
"""
import json, re, sys, time, pathlib, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "market" / "series"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept": "application/json"}

# key -> (TGJU indicator code, description). Values are stored in toman (rial / 10).
SERIES = {
    "usd_free":     ("price_dollar_rl", "US dollar, open (free) market"),
    "usd_sana":     ("sana_sell_usd",   "US dollar, SANA (bank exchange-house) sell rate"),
    "usd_nima":     ("nima_sell_usd",   "US dollar, NIMA (exporters' system) sell rate"),
    "usd_mex":      ("mex_usd_sell",    "US dollar, Iran Center of Exchange (markaz-e mobadele) rate"),
    "gold18_gram":  ("geram18",         "18k gold, per gram"),
    "coin_emami":   ("sekee",           "Emami gold coin"),
    "coin_half":    ("nim",             "Half Bahar Azadi gold coin"),
    "coin_quarter": ("rob",             "Quarter Bahar Azadi gold coin"),
    "eur":          ("price_eur",       "Euro, open market"),
    "gbp":          ("price_gbp",       "British pound, open market"),
    "aed":          ("price_aed",       "UAE dirham, open market"),
    "try":          ("price_try",       "Turkish lira, open market"),
    "cny":          ("price_cny",       "Chinese yuan, open market"),
    "usdt":         ("crypto-tether-irr", "Tether (USDT) in toman"),
    # World prices in US dollars (no rial -> toman conversion)
    "gold_oz":      ("ons",             "Gold, troy ounce", "usd"),
    "silver_oz":    ("silver",          "Silver, troy ounce", "usd"),
    "brent":        ("oil_brent",       "Brent crude oil, barrel", "usd"),
    "btc":          ("crypto-bitcoin",  "Bitcoin", "usd"),
}
FA2EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def num(c):
    c = re.sub(r"<[^>]+>", "", str(c)).translate(FA2EN)
    c = re.sub(r"[^\d.]", "", c)
    return float(c) if c else None

def fetch(code, full, div=10):
    rows, start, page = [], 0, 500 if full else 15
    while True:
        j = get(f"https://api.tgju.org/v1/market/indicator/summary-table-data/{code}?lang=fa&order_dir=desc&draw=1&start={start}&length={page}")
        data = j.get("data") or []
        for r in data:
            try:
                d = datetime.datetime.strptime(re.sub(r"<[^>]+>", "", str(r[6])).strip(), "%Y/%m/%d").date()
            except Exception:
                continue
            close = num(r[3])
            if close:
                rows.append([d.isoformat(), round(close / div, 4 if close / div < 10 else 2)])
        if not full or len(data) < page or start > 20000:
            break
        start += page
        time.sleep(0.8)
    return rows

def main():
    full = "--full" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for key, spec in SERIES.items():
        if only and key not in only:
            continue
        code, desc = spec[0], spec[1]
        unit = spec[2] if len(spec) > 2 else "toman"
        path = OUT / f"{key}.json"
        # A new series has no history yet, so backfill it fully even on a nightly run.
        old = json.loads(path.read_text()) if path.exists() else {"key": key, "code": code, "desc": desc, "unit": unit, "data": []}
        try:
            new = fetch(code, full or not old["data"], 10 if unit == "toman" else 1)
        except Exception as e:
            report[key] = f"error: {e!r}"[:200]
            continue
        merged = {d: v for d, v in old["data"]}
        merged.update({d: v for d, v in new})
        old["data"] = sorted([[d, v] for d, v in merged.items()])
        old["updated_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        old["source"] = f"TGJU {code}"
        if old["data"]:
            path.write_text(json.dumps(old, ensure_ascii=False, separators=(",", ":")))
        report[key] = {"rows": len(old["data"]), "first": old["data"][0] if old["data"] else None, "last": old["data"][-1] if old["data"] else None}
    (OUT / "_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps(report, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
