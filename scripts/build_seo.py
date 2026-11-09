"""Keep search metadata and the sitemap correct on every page.

For each page at the repo root this adds whatever is missing (canonical, Open Graph,
Twitter card, icon) and structured data (JSON-LD), inside the seo:start / seo:end markers.
Tags already written by hand stay as they are. Running it twice changes nothing.
It also rewrites sitemap.xml from the pages that exist, dated by their last human edit.
"""
import datetime, html, json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ditoman.com/"
START, END = "<!-- seo:start -->", "<!-- seo:end -->"
SKIP = {"404.html"}
ARTICLES = {"iran-trees.html", "news-readers.html", "iran-vehicles.html", "fateh-reactor.html", "iran-built.html", "cinnagen.html", "iran-zinc.html", "morvarid-eo.html", "hangang.html", "staying-in.html", "pistachio-ai.html", "sina-surgical-robot.html"}
# Pages whose content comes from data files that robots update.
DATA_SOURCES = {"posts.html": ["telegram/feed.json"], "prices.html": ["market"], "calendar.html": ["calendar"]}
PDFS = ["whitepaper-v5.pdf", "whitepaper-v5-fa.pdf"]

ORG = {
    "@type": "Organization",
    "@id": BASE + "#organization",
    "name": "Ditoman",
    "alternateName": ["دیتومان", "DiToman", "Ditoman TMN"],
    "url": BASE,
    "logo": {"@type": "ImageObject", "url": BASE + "tmn-logo-512.png", "width": 512, "height": 512},
    "foundingDate": "2022",
    "sameAs": ["https://www.instagram.com/ditoman.tmn/", "https://t.me/Ditoman_tm"],
}
SITE = {
    "@type": "WebSite",
    "@id": BASE + "#website",
    "name": "Ditoman",
    "alternateName": ["دیتومان", "DiToman"],
    "url": BASE,
    "inLanguage": ["fa", "en"],
    "publisher": {"@id": BASE + "#organization"},
}


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def first_date(path):
    out = git("log", "--diff-filter=A", "--format=%cs", "--", path)
    return out.splitlines()[-1] if out else ""


def human_date(*paths):
    """Last edit by a person, ignoring the robot's own commits."""
    return git("log", "-1", "--format=%cs", "--perl-regexp", "--author=^(?!ditoman-bot)", "--", *paths)


def any_date(*paths):
    return git("log", "-1", "--format=%cs", "--", *paths)


def find(pattern, text):
    m = re.search(pattern, text, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def clean(title):
    return re.sub(r"\s*\|\s*(Ditoman Learn|Ditoman|Iranian Companies)\s*$", "", title).strip()


def crumbs(*items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
            for i, (n, u) in enumerate(items)
        ],
    }


def hero_image(text):
    for src in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', text):
        if "logo" not in src and not src.startswith(("http", "data:")):
            return src
    return "og-image.jpg"


def company_slugs():
    return {f.stem + ".html" for f in (ROOT / "data" / "companies").glob("*.json")}


def graph_for(name, title, desc, image, text):
    url = BASE + ("" if name == "index.html" else name)
    home = ("Ditoman", "")
    short = clean(title)
    if name == "index.html":
        return [ORG, SITE, {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
                            "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#organization"}}]
    is_lesson = re.fullmatch(r"lesson\d+\.html", name)
    if is_lesson or name in ARTICLES:
        short = re.sub(r"^(Ditoman Learn\s*\|\s*)?(Lesson \d+\s*\|\s*)?", "", short)
        art = {"@type": "Article", "@id": url + "#article", "mainEntityOfPage": url, "headline": short[:110],
               "description": desc, "image": BASE + image, "inLanguage": ["fa", "en"],
               "author": {"@id": BASE + "#organization"}, "publisher": ORG}
        published = first_date(name)
        if published:
            art["datePublished"] = published
        trail = [home, ("Learn", "learn.html"), (short, name)] if is_lesson else [home, (short, name)]
        return [art, crumbs(*trail)]
    page = {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
            "isPartOf": {"@id": BASE + "#website"}, "publisher": ORG}
    if name in company_slugs():
        firm = re.sub(r"\s*\(.*$", "", short)
        page["about"] = {"@type": "Organization", "name": firm}
        return [page, crumbs(home, ("Companies", "companies.html"), (short, name))]
    return [page, crumbs(home, (short, name))]


def process(path):
    name = path.name
    text = path.read_text(encoding="utf-8")
    bare = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", text, flags=re.S)
    if "</head>" not in bare:
        return
    title = find(r"<title>(.*?)</title>", bare)
    desc = find(r'<meta\s+name="description"\s+content="(.*?)"', bare)
    url = BASE + ("" if name == "index.html" else name)
    is_article = name in ARTICLES or re.fullmatch(r"lesson\d+\.html", name)
    existing_img = find(r'property="og:image"\s+content="(.*?)"', bare).replace(BASE, "")
    image = hero_image(bare) if is_article else (existing_img or "og-image.jpg")
    e = lambda s: html.escape(s, quote=True)

    tags = []
    def want(marker, tag):
        if marker not in bare:
            tags.append(tag)
    want('rel="canonical"', f'<link rel="canonical" href="{url}" />')
    want('rel="icon"', '<link rel="icon" href="ditoman-logo.png" />')
    want('og:type', f'<meta property="og:type" content="{"article" if is_article else "website"}" />')
    want('og:site_name', '<meta property="og:site_name" content="Ditoman" />')
    want('og:title', f'<meta property="og:title" content="{e(title)}" />')
    want('og:description', f'<meta property="og:description" content="{e(desc)}" />')
    want('og:url', f'<meta property="og:url" content="{url}" />')
    want('og:image', f'<meta property="og:image" content="{BASE}{image}" />')
    want('twitter:card', '<meta name="twitter:card" content="summary_large_image" />')
    data = {"@context": "https://schema.org", "@graph": graph_for(name, title, desc, image, bare)}
    payload = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    tags.append(f'<script type="application/ld+json">\n{payload}\n</script>')
    block = START + "\n" + "\n".join(tags) + "\n" + END + "\n"
    new = bare.replace("</head>", block + "</head>", 1)
    if new != text:
        path.write_text(new, encoding="utf-8")


def sitemap(pages):
    today = datetime.date.today().isoformat()
    rows = []
    def add(rel, loc):
        sources = DATA_SOURCES.get(rel)
        stamp = max(filter(None, [human_date(rel), *(any_date(s) for s in sources or [])]), default=today)
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{stamp}</lastmod></url>")
    for p in pages:
        add(p.name, BASE + ("" if p.name == "index.html" else p.name))
    for pdf in PDFS:
        add(pdf, BASE + pdf)
    body = "\n".join(rows)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n", encoding="utf-8")


def main():
    pages = sorted((p for p in ROOT.glob("*.html") if p.name not in SKIP),
                   key=lambda p: (p.name != "index.html", p.name))
    for p in pages:
        process(p)
    sitemap(pages)
    print(f"{len(pages)} pages")


if __name__ == "__main__":
    main()
