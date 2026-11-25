"""Render the public IMI-100 ranking (the Industrial Management Institute's list of Iran's largest companies by sales)
in a headless browser from a GitHub runner, pick each fiscal year, and save every data response the page receives."""
import json, pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
res = {"responses": [], "pages": {}}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(locale="fa-IR")

    def on_resp(r):
        if "BusinessEngine/API" in r.url:
            try:
                body = r.text()
            except Exception as e:  # noqa
                body = "ERR " + str(e)
            res["responses"].append({"url": r.url, "status": r.status, "req": r.request.post_data, "body": body[:400000]})
    pg.on("response", on_resp)
    for u in ["https://imi100.imi.ir/Ranking", "https://imi100.imi.ir/Ranking/p/500"]:
        pg.goto(u, wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(5000)
        sels = pg.query_selector_all("select")
        info = []
        for s in sels:
            opts = s.evaluate("e => [...e.options].map(o => [o.value, o.text])")
            info.append(opts)
        res["pages"][u] = {"selects": info, "html": pg.inner_html("body")[:150000]}
        # try picking the latest year in each select, then wait for data
        for s in sels:
            try:
                opts = s.evaluate("e => [...e.options].map(o => o.value)")
                if len(opts) > 1:
                    s.select_option(index=1)
                    pg.wait_for_timeout(6000)
            except Exception:  # noqa
                pass
        res["pages"][u]["text_after"] = pg.inner_text("body")[:200000]
    b.close()
(OUT / "imi_rank.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
print(len(res["responses"]), "responses")
