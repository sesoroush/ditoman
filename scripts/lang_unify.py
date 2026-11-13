"""Give every page the one site-wide language switch (lang.js).

Run from the repo root:  python3 scripts/lang_unify.py
It is safe to run again; the page generators call it after they write their pages.

For each page it:
  - loads lang.js (the header EN / فارسی button, remembered across the site),
  - sets the saved language before the page paints, so there is no flash,
  - gives the older lesson and story pages the same main menu as the rest of the site.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION = "20261113c"
EARLY = ('<script>try{if(localStorage.getItem("ditoman-lang")==="en")'
         'document.documentElement.setAttribute("data-lang","en")}catch(e){}</script>')
TAG = f'<script src="lang.js?v={VERSION}" defer></script>'

MENU = [("learn.html", "Learn"), ("iran.html", "Iran"), ("companies.html", "Companies"),
        ("prices.html", "Prices"), ("calendar.html", "Calendar"), ("tmn.html", "TMN"),
        ("index.html#whitepapers", "Whitepaper"), ("posts.html", "Posts")]


def menu(active):
    links = "\n".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{n}</a>' for h, n in MENU)
    return f'<nav class="nav-links">\n{links}\n</nav>'


def fix(path):
    s = path.read_text(encoding="utf-8")
    orig = s
    if "lang.js" in s:
        s = re.sub(r'lang\.js\?v=[\w.]+', f"lang.js?v={VERSION}", s)
    else:
        if 'data-lang=' not in s.split("<body", 1)[0]:
            s = s.replace("</head>", f"{EARLY}\n</head>", 1)
        s = s.replace("</body>", f"{TAG}\n</body>", 1)
    # Older pages: same menu as the rest of the site (no Home / Roadmap / Navigator items)
    if "site.css" not in s and '<nav class="nav-links">' in s:
        active = "learn.html" if path.name.startswith("lesson") else ("tmn.html" if path.name == "tmn.html" else "posts.html")
        s = re.sub(r'<nav class="nav-links">.*?</nav>', lambda m: menu(active), s, count=1, flags=re.S)
    if s != orig:
        path.write_text(s, encoding="utf-8")
        return True
    return False


def main():
    changed = [p.name for p in sorted(ROOT.glob("*.html")) if fix(p)]
    print(f"{len(changed)} pages updated")


if __name__ == "__main__":
    main()
