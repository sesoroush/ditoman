"""One-off: where is TMN listed / indexed? Writes market/tmn-status.json."""
import json, urllib.request, pathlib
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124", "Accept": "application/json"}
TMN = "0x86a56e59f22Eaf3867EEeB41fB9BfA81BacE790d"; PAIR = "0x6f1836b15de0c6294c16aaec67903515f532fa1c"
out = {}
def get(name, url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            out[name] = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        out[name] = {"error": repr(e)[:300]}
get("dexscreener_token", f"https://api.dexscreener.com/latest/dex/tokens/{TMN}")
get("dexscreener_pair", f"https://api.dexscreener.com/latest/dex/pairs/bsc/{PAIR}")
get("dexscreener_profile", f"https://api.dexscreener.com/orders/v1/bsc/{TMN}")
get("gecko_token", f"https://api.geckoterminal.com/api/v2/networks/bsc/tokens/{TMN}")
get("gecko_token_info", f"https://api.geckoterminal.com/api/v2/networks/bsc/tokens/{TMN}/info")
get("gecko_pool", f"https://api.geckoterminal.com/api/v2/networks/bsc/pools/{PAIR}")
get("gecko_trades", f"https://api.geckoterminal.com/api/v2/networks/bsc/pools/{PAIR}/trades")
get("coingecko_contract", f"https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/{TMN.lower()}")
get("trustwallet_info", f"https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/smartchain/assets/{TMN}/info.json")
p = pathlib.Path(__file__).resolve().parents[2] / "market" / "tmn-status.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1)[:200000])
