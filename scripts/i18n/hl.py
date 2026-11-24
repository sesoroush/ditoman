"""One hreflang block for every language a page exists in (decided by which files are on disk)."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
BASE = "https://ditoman.com/"
HSTART, HEND = "<!-- hreflang:start -->", "<!-- hreflang:end -->"
ORDER = ["fa", "en", "ar", "zh", "tr", "ru", "pt", "es", "fr", "de"]


def base_of(name):
    for suf in (".en.html", ".ar.html", ".zh.html", ".tr.html", ".ru.html", ".pt.html", ".es.html", ".fr.html", ".de.html", ".html"):
        if name.endswith(suf):
            return name[: -len(suf)]
    return name


def url(base, lang):
    if lang == "fa":
        return BASE if base == "index" else BASE + base + ".html"
    return BASE + base + "." + lang + ".html"


def block(name):
    b = base_of(name)
    langs = [l for l in ORDER if (ROOT / (b + ".html" if l == "fa" else f"{b}.{l}.html")).exists() or l in ("fa",)]
    rows = [f'  <link rel="alternate" hreflang="{l}" href="{url(b, l)}" />' for l in langs]
    rows.append(f'  <link rel="alternate" hreflang="x-default" href="{url(b, "fa")}" />')
    return HSTART + "\n" + "\n".join(rows) + "\n  " + HEND


def put(src, name):
    bl = block(name)
    if HSTART in src:
        return re.sub(re.escape(HSTART) + r".*?" + re.escape(HEND), lambda m: bl, src, flags=re.S)
    return src.replace("</head>", "  " + bl + "\n</head>", 1)
