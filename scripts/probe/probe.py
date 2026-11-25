"""Render the public IMI-100 ranking pages in a headless browser (from a GitHub runner) and save their text.
IMI-100 (Industrial Management Institute) ranks Iran's 500 largest companies by sales; the list is drawn by script."""
import json, pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
URLS = ["https://imi100.imi.ir/Ranking", "https://imi100.imi.ir/Ranking/p/200", "https://imi100.imi.ir/Ranking/p/300",
        "https://imi100.imi.ir/Ranking/p/400", "https://imi100.imi.ir/Ranking/p/500"]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(locale="fa-IR")
    for u in URLS:
        try:
            pg.goto(u, wait_until="networkidle", timeout=90000)
            pg.wait_for_timeout(6000)
            res[u] = {"text": pg.inner_text("body")[:200000],
                      "tables": pg.evaluate("() => [...document.querySelectorAll('table')].map(t => [...t.rows].map(r => [...r.cells].map(c => c.innerText.trim())))")}
        except Exception as e:  # noqa
            res[u] = {"error": str(e)[:300]}
    b.close()
(OUT / "imi_rank.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
print({u: (len(v.get("text", "")), len(v.get("tables", []))) for u, v in res.items()})
