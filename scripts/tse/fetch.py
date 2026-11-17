"""Try the official TSETMC endpoints from the GitHub runner and save what comes back (run by tse.yml)."""
import json, pathlib, urllib.request, urllib.error, time
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "iran" / "tse"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
URLS = {
    "marketwatch.json": "https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&paperTypes[0]=1&paperTypes[1]=2&paperTypes[2]=3&paperTypes[3]=4&paperTypes[4]=5&paperTypes[5]=6&paperTypes[6]=7&paperTypes[7]=8&paperTypes[8]=9&showTraded=false&withBestLimits=true",
    "marketwatch-old.txt": "http://old.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0",
    "instrument-sample.json": "https://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/35425587644337450",
}
log = []
for name, url in URLS.items():
    for host_try in (url,):
        try:
            req = urllib.request.Request(host_try, headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*", "Referer": "https://main.tsetmc.com/"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            (OUT / name).write_bytes(data)
            log.append(f"OK {name} {len(data)}")
        except Exception as e:
            log.append(f"FAIL {name} {type(e).__name__} {e}")
(OUT / "log.txt").write_text("\n".join(log) + "\n")
print("\n".join(log))
