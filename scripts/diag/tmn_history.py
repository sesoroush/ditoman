"""One-off: when did key TMN balances change? Binary-searches historical state on an archive RPC,
then reads the Transfer logs of the found block. Writes market/tmn-transfers.json."""
import json, time, urllib.request, pathlib
UA = {"User-Agent": "Mozilla/5.0 Chrome/124", "Accept": "application/json", "Content-Type": "application/json"}
TMN = "0x86a56e59f22eaf3867eeeb41fb9bfa81bace790d"
PAIR = "0x6f1836b15de0c6294c16aaec67903515f532fa1c"
DEAD = "0x000000000000000000000000000000000000dead"
DEPLOYER = "0x5c037043df41956cd0c9b639cffaf46feb9a7ff4"
FOUNDER = "0x521bf0254e2755abf8cd5afe8c7f9af35dccf50c"
FORMER = "0xaeda0cfe05fb79ce594e556f3001ae88dc8780e9"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
CANDIDATES = ["https://bsc.drpc.org", "https://bsc-mainnet.public.blastapi.io", "https://binance.llamarpc.com",
              "https://bsc.meowrpc.com", "https://bsc-pokt.nodies.app", "https://bsc.blockpi.network/v1/rpc/public",
              "https://endpoints.omniatech.io/v1/bsc/mainnet/public", "https://rpc.ankr.com/bsc", "https://bsc-rpc.publicnode.com",
              "https://1rpc.io/bnb", "https://bsc.publicnode.com", "https://bscrpc.com"]
LOGRPC = ["https://bsc-rpc.publicnode.com", "https://bsc.drpc.org", "https://bsc-dataseed.bnbchain.org"] + CANDIDATES
log = []
pad = lambda a: a.lower().replace("0x", "").rjust(64, "0")

def rpc(url, method, params):
    req = urllib.request.Request(url, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(), headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read())
    if "error" in j:
        raise RuntimeError(str(j["error"])[:200])
    return j["result"]

def first(urls, method, params):
    for u in urls:
        try:
            return rpc(u, method, params)
        except Exception as e:
            log.append(f"{u} {method}: {e!r}"[:250])
    raise RuntimeError(method + " failed everywhere")

latest = int(first(LOGRPC, "eth_blockNumber", []), 16)
OLD = 12_000_000  # ~Nov 2021
archive = []
for u in CANDIDATES:
    try:
        r = rpc(u, "eth_call", [{"to": TMN, "data": "0x18160ddd"}, hex(OLD)])
        archive.append(u)
        log.append(f"archive ok: {u} -> {r[:20]}")
    except Exception as e:
        log.append(f"archive no: {u}: {e!r}"[:250])

def call_at(to, data, block):
    for u in archive:
        for _ in range(2):
            try:
                return int(rpc(u, "eth_call", [{"to": to, "data": data}, hex(block)]) or "0x0", 16)
            except Exception as e:
                err = e
                time.sleep(0.5)
    raise RuntimeError(f"call failed at {block}: {err!r}")

def safe_call(to, data, block):
    try:
        return call_at(to, data, block)
    except Exception:
        return None  # e.g. contract not deployed yet

def first_block(pred, lo, hi):
    """Smallest block in (lo, hi] where pred(block) is True, assuming False at lo and True at hi."""
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi

def describe(block, address, label):
    item = {"label": label, "block": block}
    try:
        item["time"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(int(first(LOGRPC, "eth_getBlockByNumber", [hex(block), False])["timestamp"], 16)))
    except Exception as e:
        item["time_err"] = repr(e)[:200]
    try:
        logs = first(LOGRPC, "eth_getLogs", [{"address": address, "fromBlock": hex(block), "toBlock": hex(block)}])
        item["transfers"] = []
        for l in logs:
            t = l["topics"]
            if t and t[0] == TRANSFER and len(t) >= 3:
                item["transfers"].append({"tx": l["transactionHash"], "from": "0x" + t[1][-40:], "to": "0x" + t[2][-40:],
                                          "raw": int(l["data"], 16) if l["data"] not in ("0x", "") else 0})
        for tx in {x["tx"] for x in item["transfers"]}:
            t = first(LOGRPC, "eth_getTransactionByHash", [tx])
            item.setdefault("txs", []).append({"tx": tx, "sender": t["from"], "nonce": int(t["nonce"], 16), "to": t["to"], "input": t["input"][:10]})
    except Exception as e:
        item["logs_err"] = repr(e)[:200]
    return item

out = {"latest": latest, "archive": archive, "events": []}
if archive:
    # the contract's first block with state
    created = first_block(lambda b: safe_call(TMN, "0x18160ddd", b) not in (None, 0), 1, latest)
    out["events"].append(describe(created, TMN, "token created"))
    S = lambda b: safe_call(TMN, "0x18160ddd", b) or 0
    start_supply = S(created)
    out["start_supply_raw"] = start_supply
    # dead address: first block with any balance, and first block with today's balance
    bal = lambda a, b: safe_call(TMN, "0x70a08231" + pad(a), b) or 0
    now_dead = bal(DEAD, latest)
    if now_dead:
        b1 = first_block(lambda b: bal(DEAD, b) > 0, created - 1, latest)
        out["events"].append(describe(b1, TMN, "dead address first receives TMN"))
        if bal(DEAD, b1) != now_dead:
            b2 = first_block(lambda b: bal(DEAD, b) >= now_dead, b1, latest)
            out["events"].append(describe(b2, TMN, "dead address reaches today's balance"))
    # total supply drop (burn to zero address)
    if S(latest) < start_supply:
        b3 = first_block(lambda b: S(b) < start_supply, created, latest)
        out["events"].append(describe(b3, TMN, "total supply first drops"))
    # LP pair: creation / first LP tokens to deployer and founder
    lpbal = lambda a, b: safe_call(PAIR, "0x70a08231" + pad(a), b) or 0
    for a, name in [(DEPLOYER, "deployer"), (FOUNDER, "founder main wallet")]:
        if lpbal(a, latest):
            b4 = first_block(lambda b: lpbal(a, b) > 0, created - 1, latest)
            out["events"].append(describe(b4, PAIR, f"LP tokens first reach {name}"))
    # the former owner's ~2.1T: when did it leave?
    if bal(FORMER, latest) == 0:
        peak_b = None
        b5 = first_block(lambda b: bal(FORMER, b) > 0, created - 1, latest)
        out["events"].append(describe(b5, TMN, "former owner wallet first receives TMN"))
        b6 = first_block(lambda b: b > b5 and bal(FORMER, b) == 0, b5, latest)
        out["events"].append(describe(b6, TMN, "former owner wallet emptied"))
for a, name in [(DEPLOYER, "deployer"), (FOUNDER, "founder"), (FORMER, "former_owner")]:
    try:
        out[f"nonce_{name}"] = int(first(LOGRPC, "eth_getTransactionCount", [a, "latest"]), 16)
    except Exception:
        pass
out["log"] = log[-40:]
pathlib.Path(__file__).resolve().parents[2].joinpath("market", "tmn-transfers.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["events"], indent=1)[:3000])
