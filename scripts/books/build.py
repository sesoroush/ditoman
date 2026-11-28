#!/usr/bin/env python3
"""Build one Ditoman book-summary page (Persian + English in one file) and its banner.

Input:  scripts/books/data/<slug>/meta.json, fa.md, en.md, telegram.md   (see scripts/books/README.md)
Output: <slug>.html, social/<slug>/* (banner in the fixed template + English cover),
        data/books/state.json (prepared date), books.html (library), build_seo.py ARTICLES, data/links.json.
The English twin page, story links, search index and sitemap are made by the "Search upkeep" workflow after the push.

Run from the repo root:  python3 scripts/books/build.py <slug> [--no-cover]
"""
import html, json, re, sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import ROOT, DATA, STATE, book, dates, load, save, tehran_today, telegram_len, telegram_text  # noqa: E402

CHROME = "book-stop-letting-everything-affect-you"   # an existing book page: head, header and footer are taken from it
LINK = 'style="color:#57D9C7"'


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("http"):
            return f'<a href="{url}" target="_blank" rel="noopener" {LINK}>{text}</a>'
        return f'<a href="{url}" {LINK}>{text}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)


def md(text):
    """Small Markdown subset -> the HTML the site's article pages use. `## ` headings are numbered from 1."""
    out, n = [], 0
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l.rstrip() for l in block.strip().splitlines()]
        first = lines[0]
        if first.startswith("## "):
            n += 1
            out.append(f'<h3><span class="check-number">{n}.</span> {inline(first[3:])}</h3>')
            lines = lines[1:]
            if not lines:
                continue
            first = lines[0]
        if first.startswith("### "):
            out.append(f'<p style="margin-top:26px"><strong style="color:#FFC24A;font-size:1.14em">{inline(first[4:])}</strong></p>')
            lines = lines[1:]
            if not lines:
                continue
            first = lines[0]
        if first.startswith("|"):
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if not re.fullmatch(r"\|[\s:|-]+\|?", l.strip())]
            t = "<div class=\"tw\"><table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
            for r in rows[1:]:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</table></div>")
        elif first.startswith("- "):
            out.extend(f"<ul>\n<li>{inline(l[2:])}</li>\n</ul>" for l in lines if l.startswith("- "))
        elif first.startswith("> "):
            out.append("<blockquote>" + inline(" ".join(l[2:] if l.startswith("> ") else l for l in lines)) + "</blockquote>")
        elif first.startswith("~ "):
            out.append(f'<p style="color:#9fb6b9">{inline(" ".join(lines)[2:])}</p>')
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(out)


def build(slug, cover=True):
    b = book(slug)
    assert b, f"{slug} is not in data/books/catalog.json"
    d = DATA / slug
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    tpl = (ROOT / f"{CHROME}.html").read_text(encoding="utf-8")
    today = dates(tehran_today())
    state = load(STATE, {})
    if state.get(slug, {}).get("prepared"):
        import datetime
        today = dates(datetime.date.fromisoformat(state[slug]["prepared"]))

    title = f"Book Summary: {b['en']} | خلاصه کتاب {b['fa']} | Ditoman"
    src = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t, quote=False)}</a></li>' for t, u in meta["sources"])
    more_fa = "".join(f'<li><a href="{h}">{html.escape(f, quote=False)}</a></li>' for h, f, _ in meta["more"])
    more_en = "".join(f'<li><a href="{h}">{html.escape(e, quote=False)}</a></li>' for h, _, e in meta["more"])
    fa = md((d / "fa.md").read_text(encoding="utf-8"))
    en = md((d / "en.md").read_text(encoding="utf-8"))
    # the honest-basis note always closes section 1
    def with_basis(body, note):
        cut = body.find('<h3><span class="check-number">2.</span>')
        assert cut > 0, "fa.md and en.md need at least two `## ` sections"
        return body[:cut] + f"<blockquote>{html.escape(note, quote=False)}</blockquote>\n" + body[cut:]
    fa = with_basis(fa, meta["basis_fa"])
    en = with_basis(en, meta["basis_en"])
    fa += (f'\n<h3>بیشتر بخوانید</h3><ul><li><a href="books.html">همه‌ی خلاصه کتاب‌های دیتومان</a></li>{more_fa}'
           '<li><a href="prices.html">قیمت لحظه‌ای تتر، بیت‌کوین و طلا</a></li></ul>'
           f'\n<h3>منابع</h3><ul class="sources">{src}</ul><p style="color:#9fb6b9;margin-top:10px">آخرین بازبینی: {today["fa_long"]}. '
           'این صفحه خلاصه و تحلیل دیتومان است و جایگزین کتاب نیست؛ تصویر جلد فقط برای معرفی کتاب آمده و حقوق آن متعلق به ناشر است.</p>')
    en += (f'\n<h3>Read more</h3><ul><li><a href="books.html">All Ditoman book summaries</a></li>{more_en}'
           '<li><a href="prices.html">Live prices: Tether, Bitcoin and gold</a></li></ul>'
           f'\n<h3>Sources</h3><ul class="sources">{src}</ul><p style="color:#9fb6b9;margin-top:10px">Last reviewed {today["en_long"]}. '
           "A Ditoman summary and analysis, not a substitute for the book; the cover image identifies the book and remains the publisher's.</p>")
    assert "**" not in fa + en, "unclosed ** in fa.md or en.md"

    head = tpl[:tpl.index("<body")]
    head = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->\n?", "", head, flags=re.S)
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{html.escape(title, quote=False)}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?" />', lambda m: f'<meta name="description" content="{html.escape(meta["desc_fa"])}" />', head, flags=re.S)
    head = head.replace(CHROME, slug)
    body = tpl[tpl.index("<body"):]
    top = body[:body.index("<main>")]
    nav_at = body.index("<!-- storynav:start -->")
    follow = body[body.index('<section class="section">\n<div class="container">\n<div class="instagram-box">'):nav_at]
    tail = body[body.index("<!-- storynav:end -->") + len("<!-- storynav:end -->"):]
    alt = html.escape(f"Ditoman book summary cover with the jacket of {b['en']}")
    e = lambda t: html.escape(t, quote=False)
    stats = "".join(f'<div class="stat"><b lang="fa">{e(s[0])}</b><b lang="en">{e(s[1])}</b><span lang="fa">{e(s[2])}</span><span lang="en">{e(s[3])}</span></div>\n' for s in meta["stats"])
    hero = f'''<main>
<section class="hero">
<div class="container">
<div class="hero-image"><img lang="fa" src="social/{slug}/card.webp" srcset="social/{slug}/card.webp 900w, social/{slug}/post.webp 1254w" sizes="(max-width: 600px) 92vw, 760px" alt="{alt}" onerror="this.parentElement.style.display='none'"><img lang="en" src="social/{slug}/en-card.webp" srcset="social/{slug}/en-card.webp 900w, social/{slug}/en.webp 1080w" sizes="(max-width: 600px) 92vw, 760px" alt="{alt}" onerror="this.parentElement.style.display='none'"></div>
<div class="lesson-badge"><span lang="en">Book summary</span><span lang="fa">خلاصه کتاب</span></div>
<h1 lang="fa" dir="rtl" style="text-align:right">{e(meta["h1_fa"])}</h1>
<h1 lang="en">{e(meta["h1_en"])}</h1>
<p class="subtitle" lang="fa" dir="rtl" style="text-align:right">{e(meta["sub_fa"])}</p>
<p class="subtitle" lang="en">{e(meta["sub_en"])}</p>
<div class="stats">
{stats}</div></div></section>
<section class="section"><div class="container">
<div class="language-toggle"><button class="lang-button active" onclick="showLanguage('fa')">فارسی</button><button class="lang-button" onclick="showLanguage('en')">English</button></div>
<div class="lesson-content fa" id="fa-content" dir="rtl" style="text-align:right">
{fa}</div>
<div class="lesson-content en" id="en-content" style="display:none">
{en}</div>
</div>
</section>

'''
    page = head + top + hero + follow + "<!-- storynav:start -->\n<!-- storynav:end -->" + tail
    assert CHROME not in page and "Chidiac" not in page, "text of the template page was left behind"
    (ROOT / f"{slug}.html").write_text(page, encoding="utf-8")

    # Telegram text must be ready and fit one message
    tg = telegram_text(slug, meta)
    n = telegram_len(tg)
    assert n < 4096, f"telegram.md is too long: {n} UTF-16 units with the footer (limit 4096)"
    assert "\n* " not in tg and not re.search(r"(?<!\*)\*(?!\*)", tg), "single asterisks in telegram.md: only **bold** pairs are allowed"

    rc = 0
    if cover:
        import cover as cover_mod
        rc = cover_mod.make(slug)

    state.setdefault(slug, {}).setdefault("prepared", tehran_today().isoformat())
    save(STATE, state)
    # SEO article list and cross-link keywords
    p = ROOT / "scripts" / "build_seo.py"
    s = p.read_text(encoding="utf-8")
    if f'"{slug}.html"' not in s:
        p.write_text(s.replace('ARTICLES = {"', f'ARTICLES = {{"{slug}.html", "', 1), encoding="utf-8")
    p = ROOT / "data" / "links.json"
    s = p.read_text(encoding="utf-8")
    if f'"{slug}"' not in s and meta.get("link_words"):
        key = '  "book-absent-superpower": {'
        assert s.count(key) == 1
        s = s.replace(key, f'  "{slug}": {json.dumps(meta["link_words"], ensure_ascii=False)},\n{key}', 1)
        json.loads(s)
        p.write_text(s, encoding="utf-8")
    import library
    library.refresh()
    print(f"built {slug}.html ({len(page)} bytes); Telegram text {n}/4096")
    return rc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(build(args[0], cover="--no-cover" not in sys.argv))
