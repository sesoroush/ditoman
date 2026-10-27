"""One-off: full Transfer history of TMN (and of its PancakeSwap LP token) from on-chain logs.
Writes market/tmn-transfers.json. Uses adaptive block ranges because public RPCs cap eth_getLogs."""
import json, time, urllib.request, pathlib
UA = {"User-Agent": "Mozilla/5.0 Chrome/124", "Accept": "application/json", "Content-Type": "application/json"}
TMN = "0x86a56e59f22eaf3867eeeb41fb9bfa81bace790d"
PAIR = "0x6f1836b15de0c6294c16aaec67903515f532fa1c"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
RPCS = ["https://bsc-rpc.publicnode.com", "https://bsc.drpc.org", "https://1rpc.io/bnb", "https://bsc-dataseed.bnbchain.org"]
log = []

def rpc(method, params, url):
    req = urllib.request.Request(url, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(), headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        j = json.loads(r.read())
    if "error" in j:
        raise RuntimeError(str(j["error"])[:200])
    return j["result"]

def any_rpc(method, params):
    for u in RPCS:
        try:
            return rpc(method, params, u)
        except Exception as e:
            log.append(f"{u} {method}: {e!r}"[:300])
    raise RuntimeError("all rpcs failed")

def logs_for(address, start, end):
    """Collect every log of `address` between start and end, shrinking the window when an RPC refuses."""
    out, url_i, step, b = [], 0, 5_000_000, start
    while b <= end:
        e = min(end, b + step - 1)
        try:
            res = rpc("eth_getLogs", [{"address": address, "fromBlock": hex(b), "toBlock": hex(e)}], RPCS[url_i])
            out += res
            b = e + 1
            if step < 5_000_000:
                step *= 2
        except Exception as ex:
            if step > 2000:
                step //= 4
            else:
                url_i += 1
                log.append(f"switch rpc at {b}: {ex!r}"[:300])
                if url_i >= len(RPCS):
                    log.append(f"gave up at block {b}")
                    break
                step = 50_000
            time.sleep(0.3)
    return out

def dec(l, scale):
    t = l["topics"]
    if not t or t[0] != TRANSFER or len(t) < 3:
        return None
    return {"block": int(l["blockNumber"], 16), "tx": l["transactionHash"], "from": "0x" + t[1][-40:], "to": "0x" + t[2][-40:],
            "amount": int(l["data"], 16) / scale if l["data"] not in ("0x", "") else 0}

latest = int(any_rpc("eth_blockNumber", []), 16)
out = {"latest": latest}
tmn = [x for x in (dec(l, 1e9) for l in logs_for(TMN, 0, latest)) if x]
lp = [x for x in (dec(l, 1e18) for l in logs_for(PAIR, 0, latest)) if x]
blocks = sorted({x["block"] for x in tmn + lp})
ts = {}
for b in blocks[:400]:
    try:
        ts[b] = int(any_rpc("eth_getBlockByNumber", [hex(b), False])["timestamp"], 16)
    except Exception:
        pass
for x in tmn + lp:
    if x["block"] in ts:
        x["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts[x["block"]]))
out["tmn_transfers"] = tmn
out["lp_transfers"] = lp
# nonce of the wallets involved, to match a wallet app's "nonce" with an address
nonces = {}
for a in sorted({x["from"] for x in tmn + lp} | {x["to"] for x in tmn + lp}):
    try:
        nonces[a] = int(any_rpc("eth_getTransactionCount", [a, "latest"]), 16)
    except Exception:
        pass
out["nonces"] = nonces
out["log"] = log[-40:]
pathlib.Path(__file__).resolve().parents[2].joinpath("market", "tmn-transfers.json").write_text(json.dumps(out, indent=1))
print(len(tmn), "tmn transfers;", len(lp), "lp transfers")
