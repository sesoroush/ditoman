"""One-off: TMN supply facts and security report. Writes market/tmn-onchain.json."""
import json, urllib.request, pathlib
UA = {"User-Agent": "Mozilla/5.0 Chrome/124", "Accept": "application/json", "Content-Type": "application/json"}
TMN = "0x86a56e59f22Eaf3867EEeB41fB9BfA81BacE790d"
RPCS = ["https://bsc-dataseed.bnbchain.org", "https://bsc-rpc.publicnode.com"]
def rpc(method, params):
    for u in RPCS:
        try:
            req = urllib.request.Request(u, data=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode(), headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                j = json.loads(r.read())
            if "result" in j: return j["result"]
        except Exception as e:
            last = e
    raise RuntimeError("rpc failed")
call = lambda data: rpc("eth_call", [{"to": TMN, "data": data}, "latest"])
pad = lambda a: a.lower().replace("0x","").rjust(64,"0")
out = {}
out["totalSupply"] = int(call("0x18160ddd"), 16) / 1e9
out["decimals"] = int(call("0x313ce567"), 16)
try: out["owner"] = "0x" + call("0x8da5cb5b")[-40:]
except Exception as e: out["owner"] = repr(e)
for name, a in {"dead": "0x000000000000000000000000000000000000dEaD", "zero": "0x0000000000000000000000000000000000000000",
                "founder_main": "0x521bf0254e2755abf8cd5afe8c7f9af35dccf50c", "former_owner": "0xAedA0cFe05FB79ce594E556f3001Ae88Dc8780e9",
                "deployer": "0x5c037043df41956cd0c9b639cffaf46feb9a7ff4", "pair": "0x6f1836b15de0c6294c16aaec67903515f532fa1c"}.items():
    out["bal_" + name] = int(call("0x70a08231" + pad(a)), 16) / 1e9
PAIR = "0x6f1836b15de0c6294c16aaec67903515f532fa1c"
pcall = lambda data: rpc("eth_call", [{"to": PAIR, "data": data}, "latest"])
out["lp_totalSupply"] = int(pcall("0x18160ddd"), 16) / 1e18
for name, a2 in {"deployer": "0x5c037043df41956cd0c9b639cffaf46feb9a7ff4", "founder_main": "0x521bf0254e2755abf8cd5afe8c7f9af35dccf50c",
                 "former_owner": "0xAedA0cFe05FB79ce594E556f3001Ae88Dc8780e9", "dead": "0x000000000000000000000000000000000000dEaD",
                 "zero": "0x0000000000000000000000000000000000000000"}.items():
    out["lp_bal_" + name] = int(pcall("0x70a08231" + pad(a2)), 16) / 1e18
out["block"] = int(rpc("eth_blockNumber", []), 16)
try:
    with urllib.request.urlopen(urllib.request.Request(f"https://api.gopluslabs.io/api/v1/token_security/56?contract_addresses={TMN.lower()}", headers=UA), timeout=30) as r:
        out["goplus"] = json.loads(r.read())
except Exception as e:
    out["goplus"] = {"error": repr(e)}
pathlib.Path(__file__).resolve().parents[2].joinpath("market", "tmn-onchain.json").write_text(json.dumps(out, indent=1))
