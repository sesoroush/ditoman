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

GLOBAL = {"btc": "BTC-USD", "gold": "GC=F", "brent": "BZ=F", "natgas": "NG=F",
          "wheat": "ZW=F", "corn": "ZC=F", "soybeans": "ZS=F"}  # grains quoted in US cents per bushel
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

# Iran daily change: compare the current price with the previous day's close from TGJU history.
FA2EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
def cell_num(c):
    c = re.sub(r"<[^>]+>", "", str(c)).translate(FA2EN)
    c = re.sub(r"[^\d.]", "", c)
    return float(c) if c else None
for k, code in TGJU.items():
    item = result["iran"].get(k)
    if not item: continue
    try:
        h = json.loads(get(f"https://api.tgju.org/v1/market/indicator/summary-table-data/{code}?lang=fa&order_dir=desc&draw=1&start=0&length=4"))
        rows = h.get("data") or []
        item["hist_raw"] = rows[:3]
        closes = [cell_num(r[3]) for r in rows if len(r) > 3]
        closes = [c for c in closes if c]
        cur = item["value_rial"]
        prev = None
        if closes:
            prev = closes[1] if (abs(closes[0] - cur) < 1e-6 and len(closes) > 1) else closes[0]
        if prev and cur:
            item["prev_rial"] = prev
            item["chg_hist"] = (cur - prev) / prev * 100
    except Exception as e:
        result["errors"][f"tgju_hist_{k}"] = repr(e)[:300]

# ---------- TMN: read the PancakeSwap V2 pool straight from BNB Smart Chain ----------
TMN = "0x86a56e59f22Eaf3867EEeB41fB9BfA81BacE790d"
WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
FACTORY = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"  # PancakeSwap V2
RPCS = ["https://bsc-dataseed.bnbchain.org", "https://bsc-rpc.publicnode.com", "https://bsc-dataseed1.defibit.io"]
def eth_call(to, data):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": to, "data": data}, "latest"]}).encode()
    last = None
    for rpc in RPCS:
        try:
            req = urllib.request.Request(rpc, data=body, headers={"Content-Type": "application/json", "User-Agent": UA["User-Agent"]})
            with urllib.request.urlopen(req, timeout=20) as r:
                j = json.loads(r.read())
            if "result" in j: return j["result"]
            last = j
        except Exception as e:
            last = e
    raise RuntimeError(f"rpc failed: {last!r}")
pad = lambda a: a.lower().replace("0x", "").rjust(64, "0")
tmn = {"contract": TMN}
try:
    pair = "0x" + eth_call(FACTORY, "0xe6a43905" + pad(TMN) + pad(WBNB))[-40:]
    tmn["pair"] = pair
    if int(pair, 16) == 0:
        tmn["note"] = "no PancakeSwap V2 TMN/WBNB pair"
    else:
        token0 = "0x" + eth_call(pair, "0x0dfe1681")[-40:]
        res = eth_call(pair, "0x0902f1ac")[2:]
        r0, r1 = int(res[0:64], 16), int(res[64:128], 16)
        tmn_raw, bnb_raw = (r0, r1) if token0.lower() == TMN.lower() else (r1, r0)
        tmn_amt, bnb_amt = tmn_raw / 1e9, bnb_raw / 1e18          # TMN has 9 decimals, WBNB 18
        bnb_usd = yahoo("BNB-USD")["value"]
        tmn.update({"reserve_tmn": tmn_amt, "reserve_bnb": bnb_amt, "bnb_usd": bnb_usd,
                    "price_bnb": bnb_amt / tmn_amt if tmn_amt else None,
                    "price_usd": (bnb_amt / tmn_amt) * bnb_usd if tmn_amt else None,
                    "liquidity_usd": 2 * bnb_amt * bnb_usd, "source": "PancakeSwap V2 pool reserves (on-chain)"})
except Exception as e:
    result["errors"]["tmn_onchain"] = repr(e)[:300]
for name, url in [("dexscreener", f"https://api.dexscreener.com/latest/dex/tokens/{TMN}"),
                  ("geckoterminal", f"https://api.geckoterminal.com/api/v2/networks/bsc/tokens/{TMN}/pools")]:
    try:
        j = json.loads(get(url))
        tmn[name] = len(j.get("pairs") or []) if name == "dexscreener" else len(j.get("data") or [])
        if name == "geckoterminal" and j.get("data"):
            at = j["data"][0].get("attributes", {})
            tmn["gt_pool"] = at.get("address")
            tmn["volume_24h_usd"] = float((at.get("volume_usd") or {}).get("h24") or 0)
            pc = (at.get("price_change_percentage") or {}).get("h24")
            tmn["change_24h_pct"] = float(pc) if pc not in (None, "") else None
    except Exception as e:
        tmn[name] = f"error {repr(e)[:120]}"
result["tmn"] = tmn

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
