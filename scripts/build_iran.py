"""Build the "What Iran Has" section from data/iran/branches.json.

Writes:
  iran.html              the hub: six branch cards, the Navigator card, method note
  iran-<slug>.html       one bilingual page per branch (hero, intro, official structure,
                         sub-branches, companies filed under the branch)
  index.html             the homepage block between the iran:start and iran:end markers

Header and footer are copied from posts.html so the section always matches the site.
A branch gets a real photo when its record has "hero": {"file": "...", "alt": {...}, "credit": "..."}
and the file sits in iran/<slug>/; until then the branch illustration is used.
Companies are filed under a branch by the "branch" (and optional "sub") field in data/companies/*.json.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "iran" / "branches.json").read_text(encoding="utf-8"))
COMPANIES = ROOT / "data" / "companies"
BASE = "https://ditoman.com/"
REVIEWED = {"fa": "۱۵ آبان ۱۴۰۵", "en": "6 November 2026"}

ART = {
    "industry": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><circle cx="640" cy="120" r="88" fill="none" stroke="#7ff5de" stroke-opacity=".32" stroke-width="14" stroke-dasharray="28 18"/><rect y="340" width="800" height="110" fill="#06222a"/><g fill="#06222a"><path d="M80 340V200l60-40v40l60-40v40l60-40v180z"/><rect x="300" y="150" width="34" height="190"/><rect x="350" y="110" width="34" height="230"/><path d="M420 340V230l70-46v46l70-46v110z"/></g><g fill="#eef6f2"><rect x="110" y="250" width="30" height="40"/><rect x="160" y="250" width="30" height="40"/><rect x="210" y="250" width="30" height="40"/><rect x="450" y="270" width="26" height="34"/><rect x="500" y="270" width="26" height="34"/></g><g fill="#7ff5de" fill-opacity=".9"><circle cx="317" cy="120" r="18"/><circle cx="340" cy="90" r="12"/><circle cx="367" cy="78" r="20"/><circle cx="394" cy="54" r="13"/></g><path d="M0 340h800" stroke="#7ff5de" stroke-opacity=".5" stroke-width="3"/></svg>',
    "energy": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><circle cx="150" cy="110" r="60" fill="#ff9f6b" fill-opacity=".9"/><g stroke="#eef6f2" stroke-opacity=".7" stroke-width="4" fill="none"><path d="M520 400 560 160h40l40 240M540 240h80M530 300h100M550 200h60"/><path d="M300 400V160m-40 60h80m-80 40h80"/></g><rect x="640" y="150" width="30" height="250" fill="#06222a"/><path d="M655 150c-40-50-10-90 0-110 10 20 40 60 0 110z" fill="#ff9f6b"/><path d="M0 390c80-30 160 30 240 0s160-30 240 0 160 30 240 0 60 0 80 0v60H0z" fill="#06222a"/><path d="M0 405c80-30 160 30 240 0s160-30 240 0 160 30 240 0 60 0 80 0" stroke="#2db7ff" stroke-opacity=".6" stroke-width="3" fill="none"/></svg>',
    "transport": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><path d="M0 300Q400 60 800 300" stroke="#2db7ff" stroke-width="10" fill="none"/><g stroke="#2db7ff" stroke-opacity=".6" stroke-width="4"><path d="M100 300V268M200 300V200M300 300V160M400 300V150M500 300V160M600 300V200M700 300V268"/></g><rect y="300" width="800" height="150" fill="#06222a"/><path d="M0 375h800" stroke="#eef6f2" stroke-width="6" stroke-dasharray="40 30"/><path d="M600 70l150 26-150 26 26-26z" fill="#eef6f2"/><path d="M60 420h190l-30 22H90z" fill="#eef6f2" fill-opacity=".85"/><rect x="84" y="396" width="70" height="24" fill="#eef6f2" fill-opacity=".85"/></svg>',
    "resources": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><circle cx="640" cy="90" r="34" fill="#f5c86b" fill-opacity=".9"/><path d="M0 330L220 120l120 110 90-70 150 170z" fill="#06222a"/><g fill="none" stroke="#f5c86b" stroke-opacity=".8" stroke-width="5"><path d="M330 330c0-60 80-100 160-100s160 40 160 100"/><path d="M370 330c0-40 55-70 120-70s120 30 120 70"/><path d="M410 330c0-22 35-40 80-40s80 18 80 40"/></g><rect y="330" width="800" height="120" fill="#06222a"/><path d="M0 330h800" stroke="#f5c86b" stroke-width="3" stroke-opacity=".6"/><path d="M560 250l14 10-6 16-16-2-4-16z" fill="#f5c86b"/><rect x="90" y="282" width="90" height="48" fill="#eef6f2" fill-opacity=".85"/><path d="M180 302l50-50 14 10-40 50z" fill="#eef6f2" fill-opacity=".85"/></svg>',
    "technology": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><g stroke="#8b6cff" stroke-opacity=".6" stroke-width="3"><path d="M400 225L160 120M400 225L240 340M400 225L620 110M400 225L660 330M400 225L400 60M160 120L240 340M620 110L660 330M160 120L400 60M620 110L400 60"/></g><g fill="#06222a" stroke="#8b6cff" stroke-width="4"><circle cx="160" cy="120" r="26"/><circle cx="240" cy="340" r="22"/><circle cx="620" cy="110" r="30"/><circle cx="660" cy="330" r="24"/><circle cx="400" cy="60" r="18"/></g><rect x="340" y="165" width="120" height="120" rx="18" fill="#06222a" stroke="#eef6f2" stroke-width="5"/><rect x="372" y="197" width="56" height="56" rx="8" fill="#8b6cff"/><g stroke="#eef6f2" stroke-width="5" stroke-linecap="round"><path d="M365 165v-22M400 165v-22M435 165v-22M365 285v22M400 285v22M435 285v22M340 190h-22M340 225h-22M340 260h-22M460 190h22M460 225h22M460 260h22"/></g></svg>',
    "tourism": '<svg viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="450" fill="#0d3a40"/><circle cx="650" cy="90" r="40" fill="#ff7ab3" fill-opacity=".9"/><path d="M0 300L140 180l110 90 120-130 170 140 100-70 160 90v80H0z" fill="#06222a" fill-opacity=".85"/><g fill="#eef6f2"><rect x="300" y="250" width="200" height="130"/><path d="M300 250c0-70 45-120 100-120s100 50 100 120z"/><rect x="250" y="160" width="26" height="220"/><rect x="524" y="160" width="26" height="220"/><path d="M250 160l13-30 13 30zM524 160l13-30 13 30z"/></g><g fill="#0d3a40"><path d="M330 380v-60c0-30 40-30 40 0v60zM430 380v-60c0-30 40-30 40 0v60zM380 380v-80c0-30 40-30 40 0v80z"/></g><rect y="380" width="800" height="70" fill="#06222a"/><path d="M0 380h800" stroke="#ff7ab3" stroke-opacity=".6" stroke-width="3"/></svg>',
    "navigator": '<svg viewBox="0 0 1600 350" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1600" height="350" fill="#0a1820"/><g stroke="#7ff5de" stroke-opacity=".18" stroke-width="2"><path d="M0 70h1600M0 175h1600M0 280h1600M200 0v350M500 0v350M800 0v350M1100 0v350M1400 0v350"/></g><g fill="none" stroke="#7ff5de" stroke-width="5"><circle cx="1180" cy="175" r="110" stroke-opacity=".9"/><circle cx="1180" cy="175" r="70" stroke-opacity=".35"/></g><path d="M1240 115l-34 92-92 34 34-92z" fill="#7ff5de"/><circle cx="1180" cy="175" r="10" fill="#0a1820"/><g stroke="#2db7ff" stroke-width="4" stroke-linecap="round"><path d="M80 260q180-120 360-60t300-90 280 20" fill="none" stroke-dasharray="14 12"/></g><g fill="#eef6f2"><circle cx="80" cy="260" r="9"/><circle cx="440" cy="200" r="9"/><circle cx="740" cy="110" r="9"/></g></svg>',
}

CARD_CSS = """
/* ---------- What Iran Has: branch cards (homepage + hub) ---------- */
.ir-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.ir-card { position: relative; display: block; min-width: 0; height: clamp(250px, 23vw, 300px); border-radius: 26px; overflow: hidden; background: var(--surface); isolation: isolate; --ir: var(--mint); }
.ir-card.wide { grid-column: 1 / -1; height: clamp(200px, 19vw, 260px); }
.ir-art { position: absolute; inset: 0; transition: transform 0.7s ease; }
.ir-art svg, .ir-art img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ir-card:hover .ir-art { transform: scale(1.04); }
.ir-card::after { content: ""; position: absolute; inset: 12px; border: 1px solid var(--ir); opacity: 0.45; border-radius: 18px; pointer-events: none; transition: opacity 0.3s ease; }
.ir-card:hover::after { opacity: 0.95; }
.ir-panel { position: absolute; inset: 0 auto 0 0; width: 58%; padding: 22px calc(24% + 12px) 22px 28px; background: rgba(4, 9, 12, 0.86); clip-path: polygon(0 0, 100% 0, 78% 100%, 0 100%); display: flex; flex-direction: column; justify-content: flex-end; gap: 4px; }
.ir-panel::before { content: ""; position: absolute; inset: 0; background: var(--ir); clip-path: polygon(100% 0, calc(100% - 4px) 0, calc(78% - 4px) 100%, 78% 100%); opacity: 0.9; }
.ir-kicker { color: var(--ir); font: 700 0.78rem var(--en); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: auto; }
.ir-panel h3 { font: 800 clamp(1.35rem, 2.2vw, 1.85rem)/1.05 var(--en); letter-spacing: -0.03em; color: #eef6f2; }
.ir-panel .ir-fa { display: block; font: 400 clamp(1.5rem, 2.6vw, 2.1rem)/1.25 var(--fa-display); color: #eef6f2; direction: rtl; text-align: left; }
.ir-tag { color: var(--muted); font-size: 0.88rem; line-height: 1.5; }
.ir-tag [lang="fa"] { display: inline; }
.ir-go { color: var(--ir); font-weight: 700; font-size: 0.92rem; margin-top: 6px; }
.ir-card:hover .ir-go { text-decoration: underline; text-underline-offset: 4px; }
.ir-note { margin-top: 26px; color: var(--muted); max-width: 60em; line-height: 1.8; font-size: 0.95rem; }
.ir-note a { color: var(--mint); font-weight: 700; }
@media (max-width: 760px) {
  .ir-grid { grid-template-columns: minmax(0, 1fr); gap: 14px; }
  .ir-card, .ir-card.wide { height: 230px; }
  .ir-panel { width: 76%; padding: 16px calc(24% + 8px) 16px 18px; }
  .ir-panel h3 { font-size: 1.45rem; }
  .ir-panel .ir-fa { font-size: 1.7rem; }
  .ir-kicker { font-size: 0.72rem; }
}
"""

PAGE_CSS = """
.k-main { padding: 0 0 80px; }
body[data-lang="fa"] .k-main { direction: rtl; font-family: var(--fa); }
body[data-lang="fa"] .i-en, body[data-lang="en"] .i-fa { display: none !important; }
body[data-lang="fa"] .ir-panel { inset: 0 0 0 auto; clip-path: polygon(0 0, 100% 0, 100% 100%, 22% 100%); padding: 22px 28px 22px calc(24% + 12px); align-items: flex-end; text-align: right; }
body[data-lang="fa"] .ir-panel::before { clip-path: polygon(0 0, 4px 0, calc(22% + 4px) 100%, 22% 100%); }
body[data-lang="fa"] .ir-panel .ir-fa { text-align: right; }
body[data-lang="fa"] .ir-panel h3 { font: 400 clamp(1.8rem, 3vw, 2.5rem)/1.25 var(--fa-display); letter-spacing: 0; }
body[data-lang="fa"] .ir-kicker { font-family: var(--fa); letter-spacing: 0; font-size: 0.9rem; }
.k-bar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin: 24px 0 8px; color: var(--muted); font-size: 0.95rem; }
.k-bar a:hover { color: var(--mint); }
.k-toggle { display: inline-flex; border: 1px solid var(--line-strong); border-radius: 999px; padding: 3px; direction: ltr; flex: none; }
.k-toggle button { font: 700 0.86rem var(--en); color: var(--muted); background: none; border: 0; border-radius: 999px; padding: 6px 14px; cursor: pointer; }
.k-toggle button[lang="fa"] { font-family: var(--fa); }
.k-toggle button[aria-pressed="true"] { background: var(--mint); color: #04261f; }
.ir-hero { padding: 36px 0 40px; }
.ir-hero h1 { font: 800 clamp(3rem, 9vw, 6.4rem)/0.98 var(--en); letter-spacing: -0.04em; color: #eef6f2; }
body[data-lang="fa"] .ir-hero h1 { font: 400 clamp(3rem, 10vw, 6.6rem)/1.15 var(--fa-display); letter-spacing: 0; }
.ir-hero p { font-size: clamp(1.15rem, 2.4vw, 1.5rem); max-width: 34em; margin-top: 16px; line-height: 1.65; }
.ir-lead { color: var(--muted); max-width: 46em; margin-top: 16px; line-height: 1.95; font-size: 1.05rem; }
body[data-lang="en"] .ir-lead { line-height: 1.7; }
.ir-sec { margin-top: 60px; }
.ir-sec > h2 { font-size: clamp(1.6rem, 3.4vw, 2.3rem); line-height: 1.15; letter-spacing: -0.02em; font-weight: 800; margin-bottom: 18px; }
body[data-lang="fa"] .ir-sec > h2 { letter-spacing: 0; }
.ir-figure { position: relative; margin: 26px 0 0; border-radius: 28px; overflow: hidden; height: clamp(240px, 40vw, 520px); background: var(--surface); }
.ir-figure svg, .ir-figure img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.ir-figure::after { content: ""; position: absolute; inset: 12px; border: 1px solid var(--ir); opacity: 0.5; border-radius: 20px; pointer-events: none; }
.ir-figure figcaption { position: absolute; bottom: 20px; inset-inline-start: 22px; padding: 4px 12px; border-radius: 999px; background: rgba(4, 9, 12, 0.72); color: #eaf6f5; font-size: 0.8rem; }
.ir-title { display: flex; align-items: baseline; justify-content: space-between; gap: 18px; flex-wrap: wrap; margin-top: 28px; }
.ir-title h1 { font: 800 clamp(2.6rem, 7vw, 4.8rem)/1 var(--en); letter-spacing: -0.035em; color: #eef6f2; }
body[data-lang="fa"] .ir-title h1 { font: 400 clamp(2.8rem, 8vw, 5rem)/1.2 var(--fa-display); letter-spacing: 0; }
.ir-title .ir-tagline { color: var(--ir); font-weight: 700; font-size: 1.1rem; }
.ir-official { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 28px; }
.ir-official > div { border: 1px solid var(--line); border-radius: 20px; padding: 18px 20px; background: var(--surface); }
.ir-official dt { color: var(--muted); font-size: 0.82rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
body[data-lang="fa"] .ir-official dt { letter-spacing: 0; font-size: 0.9rem; }
.ir-official dd { line-height: 1.75; font-weight: 500; }
.ir-official dd b { color: var(--ir); font-size: 1.4rem; display: block; margin-bottom: 2px; font-family: var(--en); direction: ltr; }
body[data-lang="fa"] .ir-official dd b { text-align: right; }
.ir-official a { color: var(--mint); font-weight: 700; display: inline-block; margin-top: 8px; }
.ir-subs { list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.ir-subs li { border: 1px solid var(--line); border-radius: 18px; padding: 16px 18px; background: linear-gradient(180deg, rgba(14, 33, 42, 0.9), rgba(10, 24, 32, 0.6)); display: flex; flex-direction: column; gap: 6px; }
.ir-subs b { font-size: 1.1rem; line-height: 1.35; }
.ir-subs .ir-isic { font: 700 0.78rem var(--en); color: var(--ir); letter-spacing: 0.06em; direction: ltr; align-self: flex-start; padding: 3px 8px; border-radius: 6px; background: rgba(255, 255, 255, 0.06); }
.ir-subs small { color: var(--muted); line-height: 1.6; }
.ir-cos { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.ir-co { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); border-radius: 22px; overflow: hidden; background: var(--surface); border: 1px solid var(--line); }
.ir-co:hover { border-color: var(--line-strong); }
.ir-co .ir-coart { position: relative; min-height: 180px; }
.ir-co .ir-coart svg, .ir-co .ir-coart img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ir-co div + div { padding: 20px 22px; display: flex; flex-direction: column; gap: 6px; justify-content: center; }
.ir-co h3 { font-size: 1.7rem; line-height: 1.15; font-weight: 800; }
body[data-lang="fa"] .ir-co h3 { font: 400 2rem/1.3 var(--fa-display); }
.ir-co p { color: var(--muted); line-height: 1.75; font-size: 0.97rem; }
.ir-co .k-go { color: var(--mint); font-weight: 700; margin-top: 4px; }
.ir-empty { border: 1px dashed var(--line-strong); border-radius: 20px; padding: 26px; color: var(--muted); line-height: 1.8; max-width: 44em; }
.ir-notice { margin-top: 56px; padding: 16px 20px; border-radius: 18px; border: 1px solid var(--line); color: var(--muted); font-size: 0.93rem; line-height: 1.8; display: flex; flex-wrap: wrap; gap: 6px 24px; justify-content: space-between; }
@media (max-width: 900px) { .ir-official, .ir-subs { grid-template-columns: 1fr 1fr; } .ir-cos { grid-template-columns: 1fr; } }
@media (max-width: 720px) {
  .ir-official, .ir-subs { grid-template-columns: 1fr; }
  .ir-figure { height: 240px; border-radius: 22px; }
  .ir-co { grid-template-columns: 1fr; }
  .ir-co .ir-coart { min-height: 160px; }
  body[data-lang="fa"] .ir-panel { width: 76%; padding: 16px 18px 16px calc(24% + 8px); }
}
"""

UI = {
    "section": DATA["section"]["name"],
    "enter": {"fa": "ورود", "en": "Enter"},
    "art": {"fa": "تصویرسازی · عکس واقعی به‌زودی", "en": "Illustration · real photo coming"},
    "authority": {"fa": "مرجع مجوز", "en": "Licensing authority"},
    "association": {"fa": "تشکل", "en": "Association"},
    "isic": {"fa": "طبقه‌بندی آیسیک", "en": "ISIC classification"},
    "guide": {"fa": "راهنمای مجوزها در ایران نویگیتر ←", "en": "Licensing guide in Iran Navigator →"},
    "subs": {"fa": "زیرشاخه‌ها", "en": "Sub-branches"},
    "subs_lead": {"fa": "هر زیرشاخه با مرجع مجوز و کد آیسیک آن؛ همان کدی که روی پروانه‌ی بهره‌برداری و در آمار رسمی ثبت می‌شود.", "en": "Each sub-branch with its licensing authority and ISIC code: the same code that appears on an operating licence and in official statistics."},
    "companies": {"fa": "شرکت‌های این شاخه", "en": "Companies in this branch"},
    "view": {"fa": "دیدن پرونده", "en": "View the record"},
    "empty": {"fa": "اولین پرونده‌ی این شاخه در راه است. شرکت‌ها یکی‌یکی و پس از بررسی منابع اضافه می‌شوند.", "en": "The first record in this branch is on its way. Companies are added one at a time, once their sources are checked."},
    "notice": {"fa": "اطلاعات عمومی است، نه مشاوره‌ی حقوقی؛ ساختار مجوزها تغییر می‌کند، پیش از اقدام مرجع مربوط را ببینید.", "en": "General information, not legal advice; licensing structures change, so check the relevant authority before acting."},
    "reviewed": {"fa": "آخرین بازبینی: " + REVIEWED["fa"], "en": "Last reviewed: " + REVIEWED["en"]},
    "all": {"fa": "همه‌ی شرکت‌ها، به ترتیب رشته", "en": "All companies, by sector"},
    "nav_name": {"fa": "ایران نویگیتر", "en": "Iran Navigator"},
    "nav_tag": {"fa": "چه کسی چه مجوزی می‌دهد؟ نقشه‌ی وزارتخانه‌ها و مجوزها، از ثبت شرکت تا مجوز هر رشته", "en": "Who licenses what? The map of ministries and permits, from company registration to each sector's licence"},
    "nav_kicker": {"fa": "قبل از شروع", "en": "Before you start"},
}


def e(s):
    return html.escape(str(s), quote=True)


def t(obj, tag="span"):
    return f'<{tag} class="i-fa" lang="fa">{e(obj["fa"])}</{tag}><{tag} class="i-en" lang="en">{e(obj["en"])}</{tag}>'


def chrome(active="iran.html"):
    page = (ROOT / "posts.html").read_text(encoding="utf-8")
    header = re.search(r"<header>.*?</header>", page, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", page, re.S).group(0)
    header = header.replace('<a href="posts.html" class="active">', '<a href="posts.html">')
    header = header.replace(f'<a href="{active}">', f'<a href="{active}" class="active">', 1)
    return header, footer


def page(title, desc, path, body, extra_css=""):
    header, footer = chrome()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
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
  <style>{PAGE_CSS}{extra_css}</style>
</head>
<body data-lang="fa">

  {header}

{body}

  {footer}

<script>
(function () {{
  var saved = null;
  try {{ saved = localStorage.getItem("ditoman-karnameh-lang"); }} catch (e) {{}}
  function set(l) {{
    document.body.setAttribute("data-lang", l);
    document.querySelectorAll(".k-toggle button").forEach(function (b) {{
      b.setAttribute("aria-pressed", b.getAttribute("data-set") === l ? "true" : "false");
    }});
    try {{ localStorage.setItem("ditoman-karnameh-lang", l); }} catch (e) {{}}
  }}
  document.querySelectorAll(".k-toggle button").forEach(function (b) {{
    b.addEventListener("click", function () {{ set(b.getAttribute("data-set")); }});
  }});
  set(saved === "en" ? "en" : "fa");
}})();
</script>

<script src="menu.js"></script>
<script src="join-bar.js" defer></script>
<script data-goatcounter="https://ditoman.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""


def toggle(crumb_html):
    return f'<div class="k-bar"><span>{crumb_html}</span><div class="k-toggle" role="group" aria-label="Language"><button type="button" lang="fa" data-set="fa">فارسی</button><button type="button" data-set="en">English</button></div></div>'


def hero_art(b):
    h = b.get("hero") or {}
    if h.get("file"):
        return f'<img src="iran/{e(b["slug"])}/{e(h["file"])}" alt="{e(h.get("alt", {}).get("en", b["name"]["en"]))}" loading="lazy" />', True
    return ART[b["art"]], False


def card(b, mode):
    """mode: 'home' shows both languages together; 'hub' uses the page's language toggle."""
    art, _ = hero_art(b)
    if mode == "home":
        inner = (f'<span class="ir-kicker">{e(UI["section"]["en"])}</span>'
                 f'<h3>{e(b["name"]["en"])}<span class="ir-fa" lang="fa">{e(b["name"]["fa"])}</span></h3>'
                 f'<span class="ir-tag">{e(b["tag"]["en"])}</span>'
                 f'<span class="ir-go">Enter · <span lang="fa">ورود</span> →</span>')
    else:
        inner = (f'<span class="ir-kicker">{t(UI["section"])}</span>'
                 f'<h3>{t(b["name"])}</h3>'
                 f'<span class="ir-tag">{t(b["tag"])}</span>'
                 f'<span class="ir-go">{t(UI["enter"])} <span class="i-en" lang="en">→</span><span class="i-fa" lang="fa">←</span></span>')
    return (f'<a class="ir-card" href="iran-{e(b["slug"])}.html" style="--ir:{e(b["accent"])}">'
            f'<div class="ir-art">{art}</div><div class="ir-panel">{inner}</div></a>')


def navigator_card(mode):
    if mode == "home":
        inner = (f'<span class="ir-kicker">Before you start · <span lang="fa">قبل از شروع</span></span>'
                 f'<h3>Iran Navigator<span class="ir-fa" lang="fa">ایران نویگیتر</span></h3>'
                 f'<span class="ir-tag">Who licenses what? The map of ministries and permits, from company registration to each sector&#x27;s licence</span>'
                 f'<span class="ir-go">Open the guide · <span lang="fa">راهنما</span> →</span>')
    else:
        inner = (f'<span class="ir-kicker">{t(UI["nav_kicker"])}</span>'
                 f'<h3>{t(UI["nav_name"])}</h3>'
                 f'<span class="ir-tag">{t(UI["nav_tag"])}</span>'
                 f'<span class="ir-go">{t(UI["enter"])} <span class="i-en" lang="en">→</span><span class="i-fa" lang="fa">←</span></span>')
    return (f'<a class="ir-card wide" href="navigator.html" style="--ir:#7ff5de">'
            f'<div class="ir-art">{ART["navigator"]}</div><div class="ir-panel">{inner}</div></a>')


def load_companies():
    out = []
    for f in sorted(COMPANIES.glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        if c.get("status") == "published" and c.get("branch"):
            out.append(c)
    return out


def company_art(c):
    from build_companies import ART as CART  # noqa: E402  (same folder)
    photo = c["photos"]["main"]
    if photo.get("file"):
        return f'<img src="companies/{e(c["slug"])}/{e(photo["file"])}" alt="{e(photo["alt"]["en"])}" loading="lazy" />'
    return CART[photo["art"]]


def branch_page(b, companies):
    art, is_photo = hero_art(b)
    caption = "" if is_photo else f'<figcaption>{t(UI["art"])}</figcaption>'
    if is_photo and b["hero"].get("credit"):
        caption = f'<figcaption>{e(b["hero"]["credit"])}</figcaption>'
    subs = "".join(
        f'<li><span class="ir-isic">{e(s["isic"])}</span><b>{t(s)}</b><small>{t(s["authority"])}</small></li>'
        for s in b["subs"])
    mine = [c for c in companies if c["branch"] == b["slug"]]
    if mine:
        cos = '<div class="ir-cos">' + "".join(
            f'<a class="ir-co" href="{e(c["slug"])}.html"><div class="ir-coart">{company_art(c)}</div><div>'
            f'<h3>{t(c["name"])}</h3><p>{t(c["tagline"])}</p><span class="k-go">{t(UI["view"])}</span></div></a>'
            for c in mine) + "</div>"
    else:
        cos = f'<p class="ir-empty">{t(UI["empty"])}</p>'
    crumb = f'<a href="iran.html">{t(UI["section"])}</a> <span aria-hidden="true">›</span> {t(b["name"])}'
    body = f"""  <main class="k-main wrap" style="--ir:{e(b["accent"])}">
    {toggle(crumb)}
    <figure class="ir-figure">{art}{caption}</figure>
    <div class="ir-title">
      <h1>{t(b["name"])}</h1>
      <span class="ir-tagline">{t(b["tag"])}</span>
    </div>
    <p class="ir-lead">{t(b["intro"])}</p>

    <dl class="ir-official">
      <div><dt>{t(UI["authority"])}</dt><dd>{t(b["authority"])}<a href="navigator.html#map">{t(UI["guide"])}</a></dd></div>
      <div><dt>{t(UI["association"])}</dt><dd>{t(b["association"])}</dd></div>
      <div><dt>{t(UI["isic"])}</dt><dd><b>{e(b["isic"]["section"])}</b>{t(b["isic"])}</dd></div>
    </dl>

    <section class="ir-sec">
      <h2>{t(UI["subs"])}</h2>
      <p class="ir-lead" style="margin:0 0 18px">{t(UI["subs_lead"])}</p>
      <ul class="ir-subs">{subs}</ul>
    </section>

    <section class="ir-sec">
      <h2>{t(UI["companies"])}</h2>
      {cos}
    </section>

    <div class="ir-notice"><span>{t(UI["notice"])}</span><span>{t(UI["reviewed"])}</span></div>
  </main>"""
    title = f'{b["name"]["en"]} | {b["name"]["fa"]} | What Iran Has | Ditoman'
    return page(title, b["intro"]["en"], f'iran-{b["slug"]}.html', body)


def hub_page(branches):
    s = DATA["section"]
    cards = "".join(card(b, "hub") for b in branches) + navigator_card("hub")
    body = f"""  <main class="k-main wrap">
    {toggle(t(UI["section"]))}
    <section class="ir-hero">
      <h1>{t(s["name"])}</h1>
      <p>{t(s["lead"])}</p>
    </section>
    <div class="ir-grid">{cards}</div>
    <p class="ir-note">{t(s["method"])} <a href="companies.html">{t(UI["all"])}</a></p>
    <div class="ir-notice"><span>{t(UI["notice"])}</span><span>{t(UI["reviewed"])}</span></div>
  </main>"""
    return page("What Iran Has | ایران چه دارد | Ditoman", s["lead"]["en"], "iran.html", body)


def homepage(branches):
    path = ROOT / "index.html"
    page_html = path.read_text(encoding="utf-8")
    cards = "".join("\n          " + card(b, "home") for b in branches) + "\n          " + navigator_card("home")
    block = f'''<!-- iran:start -->
    <section class="block" id="iran">
      <div class="wrap">
        <div class="head">
          <h2>What Iran has<span lang="fa">ایران چه دارد</span></h2>
          <p>A structured map of what is made, mined, moved and seen in Iran: six branches, their official sub-branches, the leading companies, and a source for every number.</p>
        </div>
        <div class="ir-grid">{cards}
        </div>
        <p class="co-all"><a class="btn btn-ghost" href="iran.html">Open the full map · <span lang="fa">نقشه‌ی کامل</span></a></p>
      </div>
    </section>
    <!-- iran:end -->'''
    if "<!-- iran:start -->" in page_html:
        page_html = re.sub(r"<!-- iran:start -->.*?<!-- iran:end -->", lambda m: block, page_html, flags=re.S)
    else:
        page_html = page_html.replace("<!-- companies:start -->", block + "\n\n    <!-- companies:start -->", 1)
    path.write_text(page_html, encoding="utf-8")


def shared_css():
    """Keep the card styles in site.css (homepage and hub both use them)."""
    css_path = ROOT / "site.css"
    css = css_path.read_text(encoding="utf-8")
    start = "/* ---------- What Iran Has: branch cards (homepage + hub) ---------- */"
    if start in css:
        css = css[: css.index(start)].rstrip("\n") + "\n" + CARD_CSS.strip("\n") + "\n"
    else:
        css = css.rstrip("\n") + "\n\n" + CARD_CSS.strip("\n") + "\n"
    css_path.write_text(css, encoding="utf-8")


def main():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    branches = DATA["branches"]
    companies = load_companies()
    shared_css()
    for b in branches:
        (ROOT / f'iran-{b["slug"]}.html').write_text(branch_page(b, companies), encoding="utf-8")
    (ROOT / "iran.html").write_text(hub_page(branches), encoding="utf-8")
    homepage(branches)
    print(f"{len(branches)} branches, {len(companies)} companies filed")


if __name__ == "__main__":
    main()
