"""Fetch market prices for the Ditoman daily report and write market/latest.json.

Runs on GitHub Actions (open internet). Every value records its source and
fetch time; anything that fails is recorded under "errors" instead of guessed.
"""
import json, re, sys, time, datetime, pathlib, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept": "application/json,text/html;q=0.9,*/*;q=0.8"}
OUT = pathlib.Path(__file__).resolve().parent.parent / "market" / "latest.json"
now = datetime.datetime.now(datetime.timezone.utc)
result = {"fetched_utc": now.isoformat(timespec="seconds"), "global": {}, "forex": {}, "iran": {}, "errors": {}}

def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def yahoo(symbol):
    j = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d"))
    m = j["chart"]["result"][0]["meta"]
    price = m["regularMarketPrice"]
    prev = m.get("chartPreviousClose") or m.get("previousClose")
    closes = [c for c in j["chart"]["result"][0]["indicators"]["quote"][0]["close"] if c is not None]
    # previous trading day's close: second to last daily close when the last bar is today
    if len(closes) >= 2:
        prev = closes[-2]
    chg = (price - prev) / prev * 100 if prev else None
    return {"value": price, "prev": prev, "chg": chg, "source": f"Yahoo Finance {symbol}",
            "market_time_utc": datetime.datetime.fromtimestamp(m.get("regularMarketTime", 0), datetime.timezone.utc).isoformat(timespec="minutes")}

GLOBAL = {"btc": "BTC-USD", "gold": "GC=F", "brent": "BZ=F", "natgas": "NG=F"}
FOREX = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X", "USD/CHF": "CHF=X", "USD/CNY": "CNY=X", "USD/TRY": "TRY=X"}

for key, sym in GLOBAL.items():
    try: result["global"][key] = yahoo(sym)
    except Exception as e: result["errors"][key] = repr(e)[:300]
for key, sym in FOREX.items():
    try: result["forex"][key] = yahoo(sym)
    except Exception as e: result["errors"][key] = repr(e)[:300]

# BTC cross-check from CoinGecko (24h change)
try:
    j = json.loads(get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"))
    result["global"]["btc_coingecko"] = {"value": j["bitcoin"]["usd"], "chg": j["bitcoin"]["usd_24h_change"], "source": "CoinGecko (24h change)"}
except Exception as e:
    result["errors"]["btc_coingecko"] = repr(e)[:300]

# Iran open-market rates from TGJU (values in rial)
TGJU = {"usd": "price_dollar_rl", "eur": "price_eur", "aed": "price_aed", "gold18_gram": "geram18", "coin_emami": "sekee"}
try:
    raw = get("https://call1.tgju.org/ajax.json")
    j = json.loads(raw)
    cur = j.get("current", {})
    for k, code in TGJU.items():
        item = cur.get(code)
        if not item:
            result["errors"][f"iran_{k}"] = f"code {code} missing"; continue
        num = lambda s: float(re.sub(r"[^\d.]", "", str(s))) if s not in (None, "") else None
        rial = num(item.get("p"))
        dp = item.get("dp"); dt = item.get("dt")
        chg = None
        if dp not in (None, ""):
            chg = float(dp) * (-1 if dt == "low" else 1)
        result["iran"][k] = {"value_rial": rial, "value_toman": rial / 10 if rial else None, "chg": chg,
                             "updated": item.get("t") or item.get("ts"), "source": f"TGJU {code}"}
except Exception as e:
    result["errors"]["tgju"] = repr(e)[:300]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
