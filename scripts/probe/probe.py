"""Fetch the public IMI-100 ranking (the Industrial Management Institute's list of Iran's largest companies by sales)
through the page's own data service, from a headless browser on a GitHub runner. Saves data/probe/imi500_<year>.json."""
import json, pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
JS = """async ([year, n]) => {
  const r = await fetch('/DesktopModules/BusinessEngine/API/Service/RunService', {method: 'POST',
    headers: {'Content-Type': 'application/json', 'TabId': '186', 'ModuleId': '1027', 'ModuleGuid': 'b9bd02e5-5375-48b9-8a1c-016157192857'},
    body: JSON.stringify({ServiceID: '8d7d32e0-2183-4012-a0d3-7cb400c89f21',
      Params: {'@PageIndex': '1', '@PageSize': String(n), '@FiscalYear': String(year), '@ListCount': String(n)}})});
  return [r.status, await r.text()];
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(locale="fa-IR")
    pg.goto("https://imi100.imi.ir/Ranking/p/500", wait_until="networkidle", timeout=90000)
    for year in (1403, 1402):
        rows = []
        for n in (100, 200, 300, 400, 500):
            st, body = pg.evaluate(JS, [year, n])
            rows += json.loads(body).get("Data", [])
            print(year, n, st, len(body))
        (OUT / f"imi500_{year}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    b.close()
