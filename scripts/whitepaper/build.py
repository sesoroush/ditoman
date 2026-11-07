"""Build whitepaper-v5-fa.pdf (Persian whitepaper) from whitepaper-v5-fa.html with Chromium.

Run from the repo root:  python3 scripts/whitepaper/build.py
"""
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = HERE / "whitepaper-v5-fa.html"
OUT = ROOT / "whitepaper-v5-fa.pdf"

FOOTER = """<div style="width:100%;font-size:8px;color:#5b6b6f;padding:0 18mm;display:flex;justify-content:space-between;
font-family:Arial,sans-serif;direction:ltr"><span>DITOMAN · Whitepaper V5 (Persian)</span>
<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(SRC.as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(500)
    page.pdf(path=str(OUT), format="A4", print_background=True, prefer_css_page_size=True,
             display_header_footer=True, header_template="<span></span>", footer_template=FOOTER)
    browser.close()
print(OUT)
