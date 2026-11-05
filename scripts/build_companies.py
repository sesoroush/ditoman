"""Build the Iranian companies section from data/companies/*.json.

Each JSON file is one company record. This script writes:
  <slug>.html       one bilingual profile page per company
  companies.html    the directory, grouped by sector
  index.html        the homepage block between the companies:start and companies:end markers

Header and footer are copied from posts.html so the section always matches the site.
Records with "status": "draft" are built too; set "published" once a record is approved.
Photos go in companies/<slug>/ and are named in the record's "file" fields.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "companies"
BASE = "https://ditoman.com/"

EVIDENCE = {
    "company": {"fa": "گفته‌ی خود شرکت", "en": "Company statement"},
    "press": {"fa": "گزارش رسانه", "en": "Press report"},
    "independent": {"fa": "آمار مستقل تجارت", "en": "Independent trade data"},
    "wiki": {"fa": "ویکی‌پدیا", "en": "Wikipedia"},
}

ART = {
    "bottles": '<svg viewBox="0 0 800 500" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><rect width="800" height="500" fill="#0d3a40"/><rect y="400" width="800" height="100" fill="#06222a"/><g fill="#eef6f2"><path d="M120 400V230q0-34 34-44v-46h52v46q34 10 34 44v170z"/><path d="M450 400V210q0-30 30-40v-60h40v60q30 10 30 40v190z"/></g><g fill="#7ff5de"><path d="M280 400V260q0-40 40-52v-58h60v58q40 12 40 52v140z"/><rect x="590" y="220" width="110" height="180" rx="16"/><rect x="618" y="180" width="54" height="40"/></g><g fill="#0d3a40"><rect x="140" y="280" width="80" height="60"/><rect x="310" y="290" width="80" height="60"/><rect x="470" y="270" width="60" height="60"/><rect x="610" y="280" width="70" height="60"/></g></svg>',
    "store": '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><rect width="400" height="300" fill="#eef6f2"/><rect x="60" y="110" width="280" height="190" fill="#2fb9a4"/><path d="M60 110 84 62h232l24 48z" fill="#0d3a40"/><rect x="90" y="150" width="130" height="90" fill="#eef6f2"/><rect x="246" y="150" width="64" height="150" fill="#0d3a40"/><g fill="#7ff5de"><rect x="102" y="166" width="24" height="60"/><rect x="142" y="166" width="24" height="60"/><rect x="182" y="166" width="24" height="60"/></g></svg>',
    "cinema": '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="400" height="300" fill="#12505a"/><rect x="70" y="54" width="260" height="124" rx="6" fill="#eef6f2"/><g fill="#06222a"><circle cx="90" cy="244" r="26"/><circle cx="162" cy="244" r="26"/><circle cx="234" cy="244" r="26"/><circle cx="306" cy="244" r="26"/></g><path d="M178 90v52l46-26z" fill="#2fb9a4"/></svg>',
    "plant": '<svg viewBox="0 0 800 500" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><rect width="800" height="500" fill="#0d3a40"/><circle cx="640" cy="110" r="52" fill="#7ff5de"/><g fill="#06222a"><rect x="110" y="170" width="86" height="210" rx="43"/><rect x="214" y="130" width="86" height="250" rx="43"/><rect x="318" y="190" width="86" height="190" rx="43"/><rect x="430" y="250" width="270" height="130"/><path d="M430 250l54-46v46l54-46v46l54-46v46l54-46v46z"/></g><path d="M0 345c90-44 170 26 270 2s150-74 262-34 180 40 268-6v193H0z" fill="#eef6f2"/></svg>',
    "cheese": '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="400" height="300" fill="#eef6f2"/><path d="M70 196 300 92c18 26 28 58 28 104z" fill="#7ff5de"/><path d="M70 196h258v44H70z" fill="#2fb9a4"/><circle cx="238" cy="160" r="15" fill="#2fb9a4"/><circle cx="288" cy="143" r="9" fill="#2fb9a4"/><circle cx="176" cy="218" r="10" fill="#0d3a40"/><circle cx="270" cy="222" r="7" fill="#0d3a40"/></svg>',
    "office": '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><rect width="400" height="300" fill="#12505a"/><g fill="#7ff5de"><rect x="138" y="62" width="124" height="238"/></g><g fill="#0d3a40"><rect x="156" y="84" width="24" height="30"/><rect x="188" y="84" width="24" height="30"/><rect x="220" y="84" width="24" height="30"/><rect x="156" y="128" width="24" height="30"/><rect x="188" y="128" width="24" height="30"/><rect x="220" y="128" width="24" height="30"/><rect x="156" y="172" width="24" height="30"/><rect x="188" y="172" width="24" height="30"/><rect x="220" y="172" width="24" height="30"/><rect x="184" y="240" width="32" height="60"/></g></svg>',
}

CSS = """
.k-main { padding: 28px 0 80px; }
body[data-lang="fa"] .k-main, body[data-lang="fa"] .k-dir { direction: rtl; font-family: var(--fa); }
body[data-lang="fa"] .i-en, body[data-lang="en"] .i-fa { display: none !important; }
.k-bar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 20px; color: var(--muted); font-size: 0.95rem; }
.k-bar a:hover { color: var(--mint); }
.k-toggle { display: inline-flex; border: 1px solid var(--line-strong); border-radius: 999px; padding: 3px; direction: ltr; flex: none; }
.k-toggle button { font: 700 0.86rem var(--en); color: var(--muted); background: none; border: 0; border-radius: 999px; padding: 6px 14px; cursor: pointer; }
.k-toggle button[lang="fa"] { font-family: var(--fa); }
.k-toggle button[aria-pressed="true"] { background: var(--mint); color: #04261f; }

.k-gallery { display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; gap: 10px; height: clamp(300px, 46vw, 540px); }
.k-shot { position: relative; overflow: hidden; margin: 0; border-radius: 14px; background: var(--surface); }
.k-shot.main { grid-row: 1 / 3; border-radius: 22px; }
.k-shot svg, .k-shot img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.k-shot figcaption { position: absolute; bottom: 10px; inset-inline-start: 10px; padding: 3px 10px; border-radius: 999px; background: rgba(4, 9, 12, 0.72); color: #eaf6f5; font-size: 0.76rem; }

.k-id { display: flex; align-items: center; gap: 20px; margin-top: 26px; }
.k-logo { flex: none; width: 92px; height: 92px; border-radius: 22px; background: #eef6f2; overflow: hidden; }
.k-logo img { width: 100%; height: 100%; object-fit: contain; }
.k-id h1 { font-size: clamp(2.6rem, 7vw, 4.6rem); line-height: 1; letter-spacing: -0.03em; font-weight: 800; }
body[data-lang="fa"] .k-id h1 { font-family: var(--fa-display); font-weight: 400; letter-spacing: 0; }
.k-tagline { font-size: clamp(1.1rem, 2.2vw, 1.4rem); color: var(--text); max-width: 34em; margin: 14px 0 26px; line-height: 1.6; font-weight: 500; }
.k-facts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-block: 1px solid var(--line); }
.k-facts > div { padding: 16px 0; padding-inline-end: 16px; }
.k-facts dt { color: var(--muted); font-size: 0.86rem; margin-bottom: 3px; }
.k-facts dd { font-weight: 700; line-height: 1.45; }

.k-sec { margin-top: 64px; }
.k-sec > h2 { font-size: clamp(1.6rem, 3.4vw, 2.3rem); line-height: 1.15; letter-spacing: -0.02em; font-weight: 800; margin-bottom: 22px; }
body[data-lang="fa"] .k-sec > h2 { letter-spacing: 0; }
.k-prose { max-width: 42em; font-size: 1.08rem; line-height: 1.95; }
body[data-lang="en"] .k-prose { line-height: 1.7; }
sup.k-ref { font-size: 0.72em; margin-inline-start: 2px; }
sup.k-ref a { color: var(--mint); padding: 0 1px; }

.k-leader { display: flex; gap: 26px; align-items: flex-start; }
.k-leader + .k-leader { margin-top: 30px; }
.k-chips { list-style: none; display: flex; flex-wrap: wrap; gap: 8px; max-width: 54em; }
.k-chips li { padding: 7px 14px; border: 1px solid var(--line-strong); border-radius: 999px; font-weight: 500; }
.k-portrait { flex: none; width: 136px; height: 136px; border-radius: 50%; overflow: hidden; background: #12505a; color: #eef6f2; display: grid; place-items: center; font: 700 2.4rem var(--fa); }
.k-portrait img { width: 100%; height: 100%; object-fit: cover; }
.k-leader h3 { font-size: 1.5rem; line-height: 1.25; font-weight: 800; }
.k-role { color: var(--mint); margin: 2px 0 10px; font-weight: 500; }

.k-ledger { list-style: none; border-top: 1px solid var(--line-strong); }
.k-ledger li { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 6px 28px; padding: 20px 0; border-bottom: 1px solid var(--line); align-items: baseline; }
.k-num { font-size: clamp(1.7rem, 4vw, 2.7rem); font-weight: 800; line-height: 1.15; color: #eef6f2; letter-spacing: -0.02em; }
body[data-lang="fa"] .k-num { letter-spacing: 0; }
.k-where { display: block; color: var(--muted); font-size: 0.88rem; margin-top: 6px; }
.k-tag { color: var(--mint); font-weight: 700; }
.k-tag.independent { background: var(--mint); color: #04261f; padding: 1px 8px; border-radius: 6px; }

.k-time { list-style: none; position: relative; padding-inline-start: 22px; max-width: 46em; }
.k-time::before { content: ""; position: absolute; inset-block: 8px; inset-inline-start: 4px; width: 2px; background: var(--line-strong); }
.k-time li { position: relative; padding-bottom: 20px; }
.k-time li::before { content: ""; position: absolute; top: 9px; inset-inline-start: -22px; width: 10px; height: 10px; border-radius: 50%; background: #eef6f2; }
.k-time b { display: block; font-size: 1.15rem; color: var(--mint); }

.k-markets { display: flex; flex-wrap: wrap; gap: 8px 26px; margin: 18px 0 26px; font-size: clamp(1.5rem, 3.6vw, 2.3rem); font-weight: 800; color: #eef6f2; }
.k-note { max-width: 42em; margin-top: 26px; line-height: 1.85; }
.k-note h3 { font-size: 1.15rem; font-weight: 800; margin-bottom: 4px; }
.k-europe { background: #eef6f2; color: #0d2a30; padding: 24px 26px; border-radius: 20px; margin-top: 30px; max-width: 46em; }
.k-europe h3 { font-size: 1.35rem; font-weight: 800; margin-bottom: 6px; }
.k-europe sup.k-ref a { color: #0b6c5d; }
.k-open { list-style: none; max-width: 44em; }
.k-open li { padding: 10px 0; border-bottom: 1px solid var(--line); }
.k-sources { list-style: none; direction: ltr; text-align: left; font-family: var(--en); font-size: 0.95rem; }
.k-sources li { padding: 7px 0; display: flex; gap: 10px; }
.k-sources a { color: var(--mint); text-decoration: underline; text-underline-offset: 3px; overflow-wrap: anywhere; }
.k-disclose { max-width: 44em; color: var(--muted); margin-top: 22px; font-size: 0.95rem; line-height: 1.85; }

.k-dir { padding: 0 0 80px; }
.k-dhero { padding: 54px 0 46px; }
.k-dhero h1 { font: 400 clamp(3.2rem, 10vw, 7rem)/1.15 var(--fa-display); color: #eef6f2; }
body[data-lang="en"] .k-dhero h1 { font: 800 clamp(2.9rem, 9vw, 6.4rem)/1 var(--en); letter-spacing: -0.04em; }
.k-dhero p { font-size: clamp(1.15rem, 2.4vw, 1.5rem); max-width: 32em; margin-top: 16px; line-height: 1.65; }
.k-how { color: var(--muted); max-width: 44em; margin-top: 18px; line-height: 1.85; }
.k-sector h2 { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; padding-bottom: 12px; border-bottom: 1px solid var(--line-strong); margin-bottom: 22px; }
.k-card { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: 0; border-radius: 24px; overflow: hidden; background: var(--surface); }
.k-card:hover .k-go { text-decoration: underline; }
.k-card .k-shot { min-height: 300px; border-radius: 0; }
.k-card-body { padding: 26px 28px; display: flex; flex-direction: column; gap: 10px; justify-content: center; }
.k-card-body h3 { font-size: 2.4rem; line-height: 1.1; font-weight: 800; }
body[data-lang="fa"] .k-card-body h3 { font: 400 2.8rem var(--fa-display); }
.k-card-body p { line-height: 1.8; }
.k-go { color: var(--mint); font-weight: 700; margin-top: 6px; }

@media (max-width: 720px) {
  .k-gallery { grid-template-columns: 1fr 1fr; grid-template-rows: 2fr 1fr; height: 420px; }
  .k-shot.main { grid-column: 1 / 3; grid-row: 1; }
  .k-id { gap: 14px; margin-top: 20px; }
  .k-logo { width: 68px; height: 68px; border-radius: 16px; }
  .k-facts { grid-template-columns: 1fr 1fr; }
  .k-sec { margin-top: 50px; }
  .k-leader { flex-direction: column; gap: 16px; }
  .k-portrait { width: 112px; height: 112px; }
  .k-ledger li { grid-template-columns: 1fr; }
  .k-europe { padding: 20px; }
  .k-card { grid-template-columns: 1fr; }
  .k-card .k-shot { min-height: 220px; }
}
"""

JS = """
<script>
(function () {
  var saved = null;
  try { saved = localStorage.getItem("ditoman-karnameh-lang"); } catch (e) {}
  function set(l) {
    document.body.setAttribute("data-lang", l);
    document.querySelectorAll(".k-toggle button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-set") === l ? "true" : "false");
    });
    try { localStorage.setItem("ditoman-karnameh-lang", l); } catch (e) {}
  }
  document.querySelectorAll(".k-toggle button").forEach(function (b) {
    b.addEventListener("click", function () { set(b.getAttribute("data-set")); });
  });
  set(saved === "en" ? "en" : "fa");
})();
</script>
"""

TOGGLE = ('<div class="k-toggle" role="group" aria-label="Language">'
          '<button type="button" lang="fa" data-set="fa">فارسی</button>'
          '<button type="button" data-set="en">English</button></div>')

UI = {
    "section": {"fa": "شرکت‌های ایرانی", "en": "Iranian companies"},
    "about": {"fa": "در یک نگاه", "en": "At a glance"},
    "leader": {"fa": "بنیان‌گذار", "en": "Founder"},
    "leaders": {"fa": "مدیران", "en": "Leadership"},
    "record": {"fa": "به زبان عدد", "en": "In numbers"},
    "timeline": {"fa": "مسیر", "en": "The path so far"},
    "exports": {"fa": "بازارهای صادراتی", "en": "Export markets"},
    "open": {"fa": "هنوز تأیید نشده", "en": "Not yet confirmed"},
    "sources": {"fa": "منابع", "en": "Sources"},
    "checked": {"fa": "آخرین بررسی:", "en": "Last checked:"},
    "art": {"fa": "تصویرسازی", "en": "Illustration"},
    "open_card": {"fa": "دیدن پرونده", "en": "View the record"},
}


def e(s):
    return html.escape(str(s), quote=True)


def t(obj, tag="span"):
    """Both languages; CSS shows the one that is selected."""
    return (f'<{tag} class="i-fa" lang="fa">{e(obj["fa"])}</{tag}>'
            f'<{tag} class="i-en" lang="en">{e(obj["en"])}</{tag}>')


def refs(ids):
    links = "".join(f'<a href="#src{i}">[{i}]</a>' for i in ids)
    return f'<sup class="k-ref">{links}</sup>'


def chrome():
    """Header and footer from posts.html, with its active nav state removed."""
    page = (ROOT / "posts.html").read_text(encoding="utf-8")
    header = re.search(r"<header>.*?</header>", page, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", page, re.S).group(0)
    header = header.replace('<a href="posts.html" class="active">', '<a href="posts.html">')
    header = header.replace('<a href="companies.html">', '<a href="companies.html" class="active">', 1)
    return header, footer


def shot(photo, slug, cls=""):
    alt = photo["alt"]
    if photo.get("file"):
        inner = f'<img src="companies/{e(slug)}/{e(photo["file"])}" alt="{e(alt["en"])}" loading="lazy" />'
        caption = t(alt)
    else:
        inner = ART[photo["art"]]
        caption = t(UI["art"])
    return f'<figure class="k-shot {cls}">{inner}<figcaption>{caption}</figcaption></figure>'


def page(title, desc, path, body, image=None):
    header, footer = chrome()
    robots = '<meta name="robots" content="noindex" />' if image == "draft" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  {robots}
  <link rel="icon" href="ditoman-logo.png" />
  <link rel="canonical" href="{BASE}{path}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Ditoman" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{BASE}{path}" />
  <meta property="og:image" content="{BASE}og-image.jpg" />
  <meta name="theme-color" content="#04090c" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,700;12..96,800&family=Vazirmatn:wght@400;500;700;800&family=Lalezar&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="site.css" />
  <style>{CSS}</style>
</head>
<body data-lang="fa">

  {header}

{body}

  {footer}
{JS}
<script src="menu.js"></script>
<script data-goatcounter="https://ditoman.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""


def company_page(c):
    slug = c["slug"]
    ph = c["photos"]
    facts = "".join(
        f'<div><dt>{t(f["label"])}</dt><dd>{t(f["value"])}{refs(f["src"])}</dd></div>' for f in c["facts"])
    ledger = "".join(
        f'<li><div class="k-num">{t(r["value"])}</div><div>{t(r["label"])}'
        f'<span class="k-where"><span class="k-tag {r["evidence"]}">{t(EVIDENCE[r["evidence"]])}</span> '
        f'{t(r["when"])}{refs(r["src"])}</span></div></li>' for r in c["record"])
    timeline = "".join(f'<li><b>{t(x["year"])}</b>{t(x["text"])}</li>' for x in c["timeline"])
    people = c.get("leaders") or [c["leader"]]
    leaders_html = ""
    for lead in people:
        portrait = (f'<img src="companies/{e(slug)}/{e(lead["photo"])}" alt="{e(lead["name"]["en"])}" />'
                    if lead.get("photo") else t(lead["initials"]))
        leaders_html += f'''<div class="k-leader">
        <div class="k-portrait">{portrait}</div>
        <div>
          <h3>{t(lead["name"])}</h3>
          <p class="k-role">{t(lead["role"])}</p>
          <p class="k-prose">{t(lead["bio"])}{refs(lead["src"])}</p>
        </div>
      </div>'''
    leaders_title = UI["leaders"] if len(people) > 1 else UI["leader"]
    domains_html = ""
    if c.get("domains"):
        d = c["domains"]
        chips = "".join(f'<li>{t(i)}</li>' for i in d["items"])
        domains_html = f'''<section class="k-sec">
      <h2>{t(d["title"])}{refs(d["src"])}</h2>
      <ul class="k-chips">{chips}</ul>
      <div class="k-europe">
        <h3>{t(d["note_title"])}</h3>
        <p>{t(d["note"])}{refs(d["note_src"])}</p>
      </div>
    </section>'''
    sources = "".join(
        f'<li id="src{s["id"]}"><span>[{s["id"]}]</span><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])}</a></li>'
        for s in c["sources"])
    open_items = "".join(f'<li class="i-fa" lang="fa">{e(x)}</li>' for x in c["unconfirmed"]["fa"]) + \
                 "".join(f'<li class="i-en" lang="en">{e(x)}</li>' for x in c["unconfirmed"]["en"])
    exports_html = ""
    if c.get("exports"):
        ex = c["exports"]
        markets = "".join(f"<span>{t(m)}</span>" for m in ex["markets"])
        ctx = ex["context"]
        exports_html = f'''<section class="k-sec">
      <h2>{t(UI["exports"])}</h2>
      <p class="k-prose">{t(ex["intro"])}{refs(ex["intro_src"])}</p>
      <div class="k-markets">{markets}</div>
      <ul class="k-ledger">
        <li><div class="k-num">{t(ctx["value"])}</div><div>{t(ctx["label"])}
          <span class="k-where"><span class="k-tag {ctx["evidence"]}">{t(EVIDENCE[ctx["evidence"]])}</span>{refs(ctx["src"])}</span></div></li>
      </ul>
      <div class="k-note">
        <h3>{t(ex["offices_title"])}</h3>
        <p>{t(ex["offices"])}{refs(ex["offices_src"])}</p>
      </div>
      <div class="k-europe">
        <h3>{t(ex["europe_title"])}</h3>
        <p>{t(ex["europe"])}{refs(ex["europe_src"])}</p>
      </div>
    </section>'''
    logo = (f'<div class="k-logo"><img src="companies/{e(slug)}/{e(c["logo"])}" alt="{e(c["name"]["en"])} logo" /></div>'
            if c.get("logo") else "")
    body = f"""  <main class="k-main wrap">
    <div class="k-bar">
      <a href="companies.html">{t(UI["section"])}</a>
      {TOGGLE}
    </div>
    <div class="k-gallery">
      {shot(ph["main"], slug, "main")}
      {shot(ph["product"], slug)}
      {shot(ph["office"], slug)}
    </div>
    <div class="k-id">
      {logo}
      <h1>{t(c["name"])}</h1>
    </div>
    <p class="k-tagline">{t(c["tagline"])}</p>
    <dl class="k-facts">{facts}</dl>

    <section class="k-sec">
      <h2>{t(UI["about"])}</h2>
      <p class="k-prose">{t(c["summary"])}{refs(c.get("summary_src", [1, 6]))}</p>
    </section>

    <section class="k-sec">
      <h2>{t(leaders_title)}</h2>
      {leaders_html}
    </section>

    {domains_html}

    <section class="k-sec">
      <h2>{t(UI["record"])}</h2>
      <ul class="k-ledger">{ledger}</ul>
    </section>

    <section class="k-sec">
      <h2>{t(UI["timeline"])}{refs(c["timeline_src"])}</h2>
      <ol class="k-time">{timeline}</ol>
    </section>

    {exports_html}

    <section class="k-sec">
      <h2>{t(UI["open"])}</h2>
      <ul class="k-open">{open_items}</ul>
    </section>

    <section class="k-sec">
      <h2>{t(UI["sources"])}</h2>
      <ul class="k-sources">{sources}</ul>
      <p class="k-disclose">{t(c["disclosure"])}<br />{t(UI["checked"])} {t(c["last_checked"])}</p>
    </section>
  </main>"""
    title = f'{c["name"]["en"]} ({c["name"]["fa"]}) | Iranian Companies | Ditoman'
    return page(title, c["tagline"]["en"], f"{slug}.html", body,
                "draft" if c["status"] == "draft" else None)


def directory(companies):
    sectors = {}
    for c in companies:
        sectors.setdefault(c["sector"]["id"], {"name": c["sector"], "items": []})["items"].append(c)
    blocks = []
    for s in sectors.values():
        cards = "".join(
            f'<a class="k-card" href="{e(c["slug"])}.html">{shot(c["photos"]["main"], c["slug"])}'
            f'<div class="k-card-body"><h3>{t(c["name"])}</h3><p>{t(c["tagline"])}</p>'
            f'<span class="k-go">{t(UI["open_card"])}</span></div></a>' for c in s["items"])
        blocks.append(f'<section class="k-sector"><h2>{t(s["name"])}</h2>{cards}</section>')
    heading = {"fa": "معرفی شرکت‌های ایرانی", "en": "Meet Iran's companies"}
    intro = {
        "fa": "پرونده‌ی شرکت‌های ایرانی به فارسی و انگلیسی: سابقه، محصول، مدیران، آمار و منبع هر عدد.",
        "en": "Records of Iranian companies in Persian and English: history, products, leadership, figures, and a source for each number.",
    }
    how = {
        "fa": "کنار هر عدد نوشته‌ایم از کجا آمده: گفته‌ی خود شرکت، گزارش رسانه یا آمار مستقل. پرونده‌ها با هم کامل می‌شوند و هر شرکت بعد از بررسی منابعش اضافه می‌شود.",
        "en": "Each number says where it came from: the company itself, a press report, or independent data. Records grow over time, and a company is added once its sources are checked.",
    }
    body = f"""  <main class="k-dir wrap">
    <div class="k-bar" style="margin-top:24px"><span></span>{TOGGLE}</div>
    <div class="k-dhero">
      <h1>{t(heading)}</h1>
      <p>{t(intro)}</p>
      <p class="k-how">{t(how)}</p>
    </div>
    {"".join(blocks)}
  </main>"""
    draft = all(c["status"] == "draft" for c in companies)
    return page("Iranian Companies | Ditoman", intro["en"], "companies.html", body,
                "draft" if draft else None)


def homepage(companies):
    """Update the homepage block. Both languages show together, like the rest of the homepage."""
    path = ROOT / "index.html"
    page_html = path.read_text(encoding="utf-8")
    cards = "".join(
        f'''
          <a class="co-card" href="{e(c["slug"])}.html">
            <div class="co-art">{c_image(c)}</div>
            <div class="co-body">
              <span class="co-sector">{e(c["sector"]["en"])} <span lang="fa">{e(c["sector"]["fa"])}</span></span>
              <h3>{e(c["name"]["en"])} <span lang="fa">{e(c["name"]["fa"])}</span></h3>
              <p>{e(c["tagline"]["en"])}</p>
              <p class="co-fa" lang="fa">{e(c["tagline"]["fa"])}</p>
              <span class="co-go">View the record</span>
            </div>
          </a>''' for c in companies)
    block = f'''<!-- companies:start -->
    <section class="block" id="companies">
      <div class="wrap">
        <div class="head">
          <h2>Meet Iran's companies<span lang="fa">معرفی شرکت‌های ایرانی</span></h2>
          <p>History, products, leadership and figures, sector by sector, with a source for each number.</p>
        </div>
        <div class="co-grid">{cards}
        </div>
        <p class="co-all"><a class="btn btn-ghost" href="companies.html">See all companies</a></p>
      </div>
    </section>
    <!-- companies:end -->'''
    if "<!-- companies:start -->" in page_html:
        page_html = re.sub(r"<!-- companies:start -->.*?<!-- companies:end -->", lambda m: block, page_html, flags=re.S)
    else:
        page_html = page_html.replace('<section class="block" id="story">', block + '\n\n    <section class="block" id="story">', 1)
    path.write_text(page_html, encoding="utf-8")


def c_image(c):
    photo = c["photos"]["main"]
    if photo.get("file"):
        return f'<img src="companies/{e(c["slug"])}/{e(photo["file"])}" alt="{e(photo["alt"]["en"])}" loading="lazy" />'
    return ART[photo["art"]]


def main():
    companies = sorted((json.loads(f.read_text(encoding="utf-8")) for f in DATA.glob("*.json")),
                       key=lambda c: c["slug"])
    for c in companies:
        (ROOT / f'{c["slug"]}.html').write_text(company_page(c), encoding="utf-8")
    (ROOT / "companies.html").write_text(directory(companies), encoding="utf-8")
    homepage(companies)
    print(f"{len(companies)} companies")


if __name__ == "__main__":
    main()
