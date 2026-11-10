"""Build the Ditoman whitepaper PDFs (Persian and English) with Chromium.

Each PDF = the original Tehran-skyline cover (cover.jpg) + the text pages.
Sources: whitepaper-v5-fa.html (Persian, IRANYekanX) and whitepaper-en.html (English).

Run from the repo root:  python3 scripts/whitepaper/build.py
"""
import io
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
JOBS = [
    ("whitepaper-v5-fa.html", "whitepaper-v5-fa.pdf", "DITOMAN · Whitepaper (Persian)", "وایت‌پیپر دیتومان"),
    ("whitepaper-en.html", "whitepaper-v5.pdf", "DITOMAN · Whitepaper", "Ditoman Whitepaper"),
]
FOOTER = """<div style="width:100%;font-size:8px;color:#5b6b6f;padding:0 18mm;display:flex;justify-content:space-between;
font-family:Arial,sans-serif;direction:ltr"><span>{label}</span>
<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>"""


def cover_page():
    buf = io.BytesIO()
    im = Image.open(HERE / "cover.jpg").convert("RGB")
    im.save(buf, "PDF", resolution=im.width / 8.27, quality=90)  # A4 width
    buf.seek(0)
    return PdfReader(buf).pages[0]


with sync_playwright() as p:
    browser = p.chromium.launch()
    for src, out, label, title in JOBS:
        page = browser.new_page()
        page.goto((HERE / src).as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)
        body = page.pdf(format="A4", print_background=True, prefer_css_page_size=True,
                        display_header_footer=True, header_template="<span></span>",
                        footer_template=FOOTER.format(label=label))
        page.close()
        w = PdfWriter()
        w.add_page(cover_page())
        for pg in PdfReader(io.BytesIO(body)).pages:
            w.add_page(pg)
        w.add_metadata({"/Title": title, "/Author": "Ditoman"})
        w.write(str(ROOT / out))
        print(out, (ROOT / out).stat().st_size)
    browser.close()
