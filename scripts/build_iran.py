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
TOP = json.loads((ROOT / "data" / "iran" / "top100.json").read_text(encoding="utf-8"))
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
.ir-card.photo .ir-panel { background: linear-gradient(90deg, rgba(4, 9, 12, 0.55), rgba(4, 9, 12, 0.08)); }
.ir-card.photo .ir-art img { object-position: right center; }
.ir-card.photo .ir-panel h3, .ir-card.photo .ir-tag { text-shadow: 0 2px 14px rgba(0, 0, 0, 0.6); }
.ir-card.photo .ir-tag { color: #d6e6e3; }
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
body[data-lang="fa"] .ir-card.photo .ir-art img { transform: scaleX(-1); }
body[data-lang="fa"] .ir-card.photo .ir-panel { background: linear-gradient(270deg, rgba(4, 9, 12, 0.55), rgba(4, 9, 12, 0.08)); }
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
.ir-leaders { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 12px; }
.ir-rank { color: var(--ir); font-size: 0.82rem; font-weight: 700; }
.ir-more { color: var(--mint); font-weight: 700; white-space: nowrap; }
.ir-top-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 18px; background: rgba(10, 24, 32, 0.6); }
.ir-top { width: 100%; border-collapse: collapse; font-size: 0.95rem; min-width: 640px; }
.ir-top th, .ir-top td { padding: 10px 14px; text-align: start; border-bottom: 1px solid var(--line); white-space: nowrap; }
.ir-top th { color: var(--muted); font-weight: 700; font-size: 0.85rem; position: sticky; top: 0; background: #0a1820; }
.ir-top tr:last-child td { border-bottom: 0; }
.ir-top td.n { color: var(--muted); width: 3.5em; }
.ir-top td.v { font-weight: 700; }
.ir-top td.v.min, .ir-top td.v.na { color: var(--muted); font-weight: 400; }
.ir-top td.name { white-space: normal; min-width: 14em; }
.ir-top a { color: var(--text); }
.ir-top a:hover { color: var(--mint); }
.ir-top .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-inline-end: 8px; vertical-align: middle; }
.ir-top-note { color: var(--muted); font-size: 0.92rem; line-height: 1.9; margin-top: 14px; max-width: 60em; }
.ir-leaders li, .ir-leaders a { display: flex; flex-direction: column; gap: 6px; }
.ir-leaders li { position: relative; border: 1px solid var(--line); border-radius: 20px; padding: 18px 18px 14px; background: linear-gradient(160deg, color-mix(in srgb, var(--sc, var(--ir)) 13%, #0c1c24), rgba(10, 24, 32, 0.75) 60%); transition: border-color 0.25s ease, transform 0.25s ease; }
.ir-leaders li:hover { border-color: color-mix(in srgb, var(--sc, var(--ir)) 60%, transparent); transform: translateY(-2px); }
.ir-leaders b { font-size: 1.12rem; font-weight: 800; line-height: 1.45; color: #eef6f2; }
.ir-leaders small { color: var(--muted); font-size: 0.86rem; }
.ir-leaders a:hover b { color: var(--ir); }
.ir-leaders .ir-rank { color: var(--sc, var(--ir)); }
.ir-v { margin-top: 10px; font-size: 1.45rem; font-weight: 800; color: #eef6f2; line-height: 1.2; }
.ir-v.min { font-size: 1.15rem; color: #cfe1df; }
.ir-v.na { font-size: 0.95rem; font-weight: 500; color: var(--muted); }
.ir-bar { display: block; height: 4px; border-radius: 4px; background: rgba(255, 255, 255, 0.07); overflow: hidden; margin-top: 2px; }
.ir-bar i { display: block; height: 100%; border-radius: 4px; background: var(--sc, var(--ir)); }
.ir-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.ir-tags > span { font-size: 0.78rem; padding: 3px 9px; border-radius: 999px; background: rgba(255, 255, 255, 0.06); color: #cfe1df; }
details.ir-more-d { margin-top: auto; border: 0; padding-top: 8px; }
.ir-more-d summary { display: inline-flex; align-items: center; gap: 6px; justify-content: flex-start; cursor: pointer; color: var(--muted); font: 500 0.84rem var(--fa); list-style: none; padding: 4px 0; }
.ir-more-d summary::after { content: "›"; font-size: 1rem; color: inherit; transform: rotate(90deg); }
.ir-more-d[open] summary::after { transform: rotate(-90deg); }
.ir-more-d summary:hover { color: var(--text); }
details.ir-top-list { border: 0; }
.ir-top-list > summary { justify-content: flex-start; gap: 10px; }
.ir-tile b, .ir-tile .vl { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
/* market map */
.ir-map-hint { color: var(--muted); font-size: 0.95rem; margin: 0 0 14px; }
.ir-map-legend { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.ir-map-legend button { display: inline-flex; align-items: center; gap: 8px; border: 1px solid var(--line); background: rgba(10, 24, 32, 0.6); color: var(--text); border-radius: 999px; padding: 6px 14px 6px 12px; font: 600 0.88rem var(--fa); cursor: default; }
.ir-map-legend button:hover, .ir-map-legend button:focus-visible { border-color: var(--c); outline: none; }
.ir-map-legend i { width: 10px; height: 10px; border-radius: 3px; background: var(--c); }
.ir-map-legend small { color: var(--muted); font-weight: 400; }
.ir-map { position: relative; height: clamp(460px, 56vw, 640px); border-radius: 22px; overflow: hidden; background: #071217; margin-bottom: 26px; }
.ir-map-g { position: absolute; padding: 0; }
.ir-map-gl { position: absolute; top: 5px; inset-inline-start: 10px; font-size: 0.82rem; font-weight: 700; color: var(--c); white-space: nowrap; overflow: hidden; max-width: calc(100% - 16px); }
.ir-tile { position: absolute; border: 0; border-radius: 10px; padding: 8px 10px; text-align: start; overflow: hidden; cursor: pointer; color: #f3fbf8;
  background: color-mix(in srgb, var(--c) calc(var(--k) * 100%), #0b1a20); display: flex; flex-direction: column; justify-content: flex-start; gap: 2px;
  transition: filter 0.25s ease, opacity 0.25s ease, box-shadow 0.25s ease; font-family: var(--fa); }
.ir-tile b { font-size: clamp(0.8rem, 1.2vw, 1.05rem); font-weight: 800; color: #fff; line-height: 1.2; }
.ir-tile .nm { font-size: 0.78rem; opacity: 0.85; line-height: 1.4; }
.ir-tile .vl { margin-top: auto; font-size: 0.82rem; font-weight: 700; opacity: 0.95; }
.ir-tile:hover { filter: brightness(1.18); }
.ir-tile:focus-visible { outline: 2px solid #fff; outline-offset: -2px; }
.ir-map.focus .ir-tile { opacity: 0.28; filter: saturate(0.5); }
.ir-map.focus .ir-tile.on, .ir-map.focus .ir-tile.fam, .ir-map.focus .ir-tile.sib { opacity: 1; filter: none; }
.ir-map.focus .ir-tile.on { box-shadow: inset 0 0 0 2px #fff; }
.ir-map.focus .ir-tile.fam { box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.55); }
.ir-sheet { position: fixed; z-index: 70; inset-inline-end: 24px; bottom: 24px; width: min(380px, calc(100vw - 32px)); max-height: min(78vh, 640px); overflow: auto;
  padding: 22px 22px 20px; border-radius: 24px; border: 1px solid color-mix(in srgb, var(--c) 45%, transparent);
  background: rgba(10, 22, 28, 0.82); -webkit-backdrop-filter: blur(22px) saturate(1.4); backdrop-filter: blur(22px) saturate(1.4);
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5); color: var(--text); font-family: var(--fa);
  opacity: 0; transform: translateY(16px) scale(0.98); transition: opacity 0.25s ease, transform 0.25s ease; }
body[data-lang="fa"] .ir-sheet { direction: rtl; }
.ir-sheet.show { opacity: 1; transform: none; }
.ir-sheet-x { position: absolute; top: 12px; inset-inline-end: 12px; width: 32px; height: 32px; border-radius: 50%; border: 0; background: rgba(255, 255, 255, 0.08); color: var(--text); font-size: 1.1rem; cursor: pointer; }
.ir-sheet-k { color: var(--c); font-weight: 700; font-size: 0.86rem; }
.ir-sheet h3 { font-size: 1.45rem; line-height: 1.35; margin: 4px 0 2px; font-weight: 800; padding-inline-end: 34px; }
.ir-sheet-path { color: var(--muted); font-size: 0.88rem; }
.ir-sheet-v { font-size: 1.8rem; font-weight: 800; margin: 12px 0 10px; }
.ir-sheet-facts { display: grid; gap: 6px; font-size: 0.88rem; padding: 12px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.ir-sheet-facts div { display: flex; justify-content: space-between; gap: 10px; }
.ir-sheet-facts dt { color: var(--muted); }
.ir-sheet-facts dd { font-weight: 700; }
.ir-sheet-facts .pending dd { font-weight: 400; color: var(--muted); opacity: 0.7; }
.ir-sheet-h { margin: 14px 0 8px; color: var(--muted); font-size: 0.85rem; font-weight: 700; }
.ir-sheet-rels { display: flex; flex-wrap: wrap; gap: 6px; }
.ir-sheet-rel { display: inline-flex; gap: 6px; align-items: baseline; border: 1px solid color-mix(in srgb, var(--c) 50%, transparent); background: color-mix(in srgb, var(--c) 14%, transparent); color: var(--text); border-radius: 999px; padding: 5px 11px; font: 500 0.82rem var(--fa); cursor: pointer; }
.ir-sheet-rel b { font-weight: 800; }
.ir-sheet-go { display: inline-block; margin-top: 16px; color: var(--mint); font-weight: 700; }
.ir-top-list { margin-top: 6px; }
.ir-top-list > summary { cursor: pointer; color: var(--mint); font-weight: 700; margin-bottom: 14px; }
@media (max-width: 720px) {
  .ir-map { height: 620px; border-radius: 18px; }
  .ir-tile { padding: 6px 7px; border-radius: 8px; }
  .ir-sheet { inset-inline: 10px; bottom: 10px; width: auto; max-height: 72vh; border-radius: 22px; }
}
@media (prefers-reduced-motion: reduce) { .ir-tile, .ir-sheet, .ir-leaders li { transition: none; } }
.ir-lf { display: flex; flex-direction: column; gap: 10px; margin: 0 0 20px; padding: 16px; border: 1px solid var(--line); border-radius: 18px; background: rgba(10, 24, 32, 0.6); }
.ir-lf-row { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.ir-lf-k { min-width: 76px; color: var(--muted); font-size: 0.9rem; font-weight: 700; }
.ir-chip { border: 1px solid var(--line-strong); background: transparent; color: var(--text); border-radius: 999px; padding: 6px 14px; font: 600 0.88rem var(--fa); cursor: pointer; }
.ir-chip:hover { border-color: var(--ir); }
.ir-chip[aria-pressed="true"] { background: var(--ir); border-color: var(--ir); color: #04261f; }
.ir-chip:focus-visible { outline: 2px solid var(--ir); outline-offset: 2px; }
.ir-lf-facts { display: grid; gap: 4px; margin-top: 8px; padding-top: 10px; border-top: 1px solid var(--line); font-size: 0.82rem; }
.ir-lf-facts > div { display: flex; justify-content: space-between; gap: 8px; }
.ir-lf-facts dt { color: var(--muted); }
.ir-lf-facts dd { font-weight: 700; text-align: end; }
.ir-lf-facts .pending dd { color: var(--muted); font-weight: 400; opacity: 0.7; }
.ir-lf-facts > div.on { color: var(--ir); }
.ir-lf-facts > div.on dd { font-size: 1rem; }
.ir-lf-none { color: var(--muted); margin-top: 12px; }
@media (max-width: 520px) { .ir-leaders { grid-template-columns: 1fr; } }
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
    "isic": {"fa": "طبقه‌بندی رسمی فعالیت‌ها", "en": "ISIC classification"},
    "guide": {"fa": "راهنمای مجوزها در ایران نویگیتر ←", "en": "Licensing guide in Iran Navigator →"},
    "subs": {"fa": "زیرشاخه‌ها", "en": "Sub-branches"},
    "subs_lead": {"fa": "هر زیرشاخه با مرجع مجوز و کد رسمی رشته‌ی فعالیتش؛ همان کدی که روی پروانه‌ی بهره‌برداری و در آمار رسمی ثبت می‌شود.", "en": "Each sub-branch with its licensing authority and ISIC code: the same code that appears on an operating licence and in official statistics."},
    "companies": {"fa": "شرکت‌های این شاخه", "en": "Companies in this branch"},
    "leaders": {"fa": "بزرگ‌ترین‌های این شاخه", "en": "The biggest in this branch"},
    "leaders_note": {"fa": "اول، شرکت‌های این شاخه از میان ۱۰۰ شرکت بزرگ بورس و فرابورس، به ترتیب ارزش بازار؛ بعد، چند نام بزرگِ بیرون از بورس. سال تأسیس، فروش و دارایی از صورت‌های مالی رسمی کم‌کم اضافه می‌شود.",
                     "en": "First, this branch's companies from the 100 largest on the Tehran Stock Exchange and Farabourse, by market value; then a few big names outside the exchange. Founding year, sales and assets are added from official statements over time."},
    "top_title": {"fa": "۱۰۰ شرکت بزرگ بورس و فرابورس", "en": "The 100 largest listed companies"},
    "top_lead": {"fa": "بزرگ‌ترین شرکت‌های بورس تهران و فرابورس به ترتیب ارزش بازار، هر کدام در شاخه‌ی خودش.", "en": "The largest companies on the Tehran Stock Exchange and Farabourse by market value, each filed under its branch."},
    "top_method": {"fa": "روش و منبع", "en": "Method and source"},
    "top_link": {"fa": "فهرست کامل ۱۰۰ شرکت ←", "en": "The full list of 100 →"},
    "col_rank": {"fa": "رتبه", "en": "Rank"},
    "col_sym": {"fa": "نماد", "en": "ISIN"},
    "col_name": {"fa": "شرکت", "en": "Company"},
    "col_branch": {"fa": "شاخه", "en": "Branch"},
    "col_market": {"fa": "بازار", "en": "Market"},
    "col_mcap": {"fa": "ارزش بازار", "en": "Market value"},
    "all_branches": {"fa": "همه", "en": "All"},
    "leaders_open": {"fa": "پرونده", "en": "Record"},
    "lf_none": {"fa": "هیچ شرکتی با این فیلتر پیدا نشد؛ اطلاعات بعضی شرکت‌ها هنوز در حال تکمیل است.", "en": "No company matches this filter yet; some companies' details are still being gathered."},
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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,700;12..96,800&family=Vazirmatn:wght@400;500;700;800&family=Lalezar&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="fonts.css?v=1" />
  <link rel="stylesheet" href="site.css?v=20261108" />
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

<script src="menu.js?v=20261107"></script>
<script src="join-bar.js?v=20261107b" defer></script>
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
    art, is_photo = hero_art(b)
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
    return (f'<a class="ir-card{" photo" if is_photo else ""}" href="iran-{e(b["slug"])}.html" style="--ir:{e(b["accent"])}">'
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


def feature_card(f, mode):
    """A wide card for a long-form Iran report (data/iran/branches.json -> section.features)."""
    art = f'<img src="{e(f["img"])}" alt="{e(f["name"]["en"])}" loading="lazy" />'
    if mode == "home":
        inner = (f'<span class="ir-kicker">{e(f["kicker"]["en"])} · <span lang="fa">{e(f["kicker"]["fa"])}</span></span>'
                 f'<h3>{e(f["name"]["en"])}<span class="ir-fa" lang="fa">{e(f["name"]["fa"])}</span></h3>'
                 f'<span class="ir-tag">{e(f["tag"]["en"])}</span>'
                 f'<span class="ir-go">Read the report · <span lang="fa">گزارش</span> →</span>')
    else:
        inner = (f'<span class="ir-kicker">{t(f["kicker"])}</span>'
                 f'<h3>{t(f["name"])}</h3>'
                 f'<span class="ir-tag">{t(f["tag"])}</span>'
                 f'<span class="ir-go">{t(UI["enter"])} <span class="i-en" lang="en">→</span><span class="i-fa" lang="fa">←</span></span>')
    return (f'<a class="ir-card wide" href="{e(f["href"])}" style="--ir:{e(f.get("accent", "#f5c86b"))}">'
            f'<div class="ir-art">{art}</div><div class="ir-panel">{inner}</div></a>')


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
        from build_companies import card_file  # noqa: E402
        return f'<img src="companies/{e(c["slug"])}/{e(card_file(c))}" alt="{e(photo["alt"]["en"])}" loading="lazy" />'
    return CART[photo["art"]]



# ---------- Comparing the big names: fields, sort and filters ----------
# Each entry in "leaders" may carry these fields (leave them out until a sourced value exists):
#   founded: year (Gregorian)         sales: annual sales, billion toman     assets: total assets, billion toman
#   figures_year: year of sales/assets   listed: true/false (Tehran Stock Exchange or Farabourse)
#   ownership: "private" | "state" | "semi" | "coop"       exporter: true/false
OWNERSHIP = {"private": {"fa": "خصوصی", "en": "Private"}, "state": {"fa": "دولتی", "en": "State-owned"},
             "semi": {"fa": "شبه‌دولتی", "en": "Semi-public"}, "coop": {"fa": "تعاونی", "en": "Cooperative"}}
YESNO = {True: {"fa": "بله", "en": "Yes"}, False: {"fa": "خیر", "en": "No"}}
PENDING = {"fa": "در حال تکمیل", "en": "Being gathered"}
MARKETS = {"bourse": {"fa": "بورس تهران", "en": "Tehran Stock Exchange"},
           "farabourse": {"fa": "فرابورس", "en": "Farabourse"},
           "base": {"fa": "بازار پایه‌ی فرابورس", "en": "Farabourse base market"}}
FIELDS = [
    ("mcap", {"fa": "ارزش بازار", "en": "Market value"}),
    ("founded", {"fa": "سال تأسیس", "en": "Founded"}),
    ("sales", {"fa": "فروش سالانه", "en": "Annual sales"}),
    ("assets", {"fa": "دارایی کل", "en": "Total assets"}),
    ("listed", {"fa": "در بورس", "en": "Listed"}),
    ("ownership", {"fa": "نوع مالکیت", "en": "Ownership"}),
    ("exporter", {"fa": "صادرکننده", "en": "Exporter"}),
]


def fa_digits(n):
    return str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def money(v):
    """Billion toman, shown as thousand-billion (همت) when large."""
    if v >= 1000:
        x = round(v / 1000, 1)
        return {"fa": f"{fa_digits(f'{x:g}')} همت", "en": f"{x:g} trn toman"}
    return {"fa": f"{fa_digits(f'{v:,.0f}').replace(',', '٬')} میلیارد تومان", "en": f"{v:,.0f} bn toman"}


def mcap_value(x):
    if x.get("mcap"):
        return money(x["mcap"])
    if x.get("mcap_min"):
        m = money(x["mcap_min"])
        return {"fa": "دست‌کم " + m["fa"], "en": "at least " + m["en"]}
    return None


def field_value(x, key):
    if key == "mcap":
        return mcap_value(x)
    v = x.get(key)
    if v is None:
        return None
    if key == "founded":
        return {"fa": fa_digits(v), "en": str(v)}
    if key in ("sales", "assets"):
        m = money(v)
        if x.get("figures_year"):
            m = {"fa": m["fa"] + f" ({fa_digits(x['figures_year'])})", "en": m["en"] + f" ({x['figures_year']})"}
        return m
    if key == "listed" and x.get("market"):
        return MARKETS[x["market"]]
    if key in ("listed", "exporter"):
        return YESNO[bool(v)]
    if key == "ownership":
        return OWNERSHIP[v]


def leader_card(x, subname, color=None, share=None):
    data = []
    for key in ("founded", "sales", "assets"):
        if x.get(key) is not None:
            data.append(f'data-{key}="{e(x[key])}"')
    if x.get("rank"):
        data.append(f'data-rank="{x["rank"]}"')
    listed = "" if x.get("listed") is None else ("no" if not x["listed"] else ("bourse" if x.get("market") == "bourse" else "fara"))
    data.append(f'data-listed="{listed}"')
    data.append(f'data-exporter="{"" if x.get("exporter") is None else ("yes" if x["exporter"] else "no")}"')
    data.append(f'data-ownership="{e(x.get("ownership") or "")}"')
    if color:
        data.append(f'style="--sc:{color}"')
    rows = "".join(
        f'<div data-f="{k}"><dt>{t(label)}</dt><dd>{t(field_value(x, k) or PENDING)}</dd></div>'
        if field_value(x, k) else
        f'<div data-f="{k}" class="pending"><dt>{t(label)}</dt><dd>{t(PENDING)}</dd></div>'
        for k, label in FIELDS)
    head = f'<b>{t(x)}</b><small>{t(subname[x["sub"]])}</small>'
    if x.get("rank"):
        approx = "≈" if not x.get("mcap") else ""
        head = (f'<span class="ir-rank">{t({"fa": f"رتبه‌ی {approx}{fa_digits(x["rank"])} · {x["sym"]}", "en": f"Rank {approx}{x["rank"]}"})}</span>' + head)
    if x.get("slug"):
        head = f'<a href="{e(x["slug"])}.html">{head}<span class="k-go">{t(UI["leaders_open"])}</span></a>'
    val = mcap_value(x)
    big = (f'<p class="ir-v{"" if x.get("mcap") else " min"}">{t(val)}</p>' if val else
           f'<p class="ir-v na">{t({"fa": "ارزش بازار: در حال تکمیل", "en": "Market value: being gathered"} if x.get("listed") else {"fa": "بیرون از بورس", "en": "Not listed"})}</p>')
    bar = f'<span class="ir-bar" aria-hidden="true"><i style="width:{max(share, 0.02) * 100:.1f}%"></i></span>' if share else ""
    tags = []
    if x.get("market"):
        tags.append(t(MARKETS[x["market"]]))
    elif x.get("listed") is False:
        tags.append(t({"fa": "غیربورسی", "en": "Not listed"}))
    if x.get("exporter"):
        tags.append(t({"fa": "صادرکننده", "en": "Exporter"}))
    if x.get("ownership"):
        tags.append(t(OWNERSHIP[x["ownership"]]))
    if x.get("family"):
        tags.append(t(TOP["families"][x["family"]]))
    tags_html = '<p class="ir-tags">' + "".join(f"<span>{g}</span>" for g in tags) + "</p>" if tags else ""
    more = f'<details class="ir-more-d"><summary>{t({"fa": "همه‌ی مشخصات", "en": "All details"})}</summary><dl class="ir-lf-facts">{rows}</dl></details>'
    return f'<li {" ".join(data)}>{head}{big}{bar}{tags_html}{more}</li>'


def chip(attr, val, label, pressed=False):
    return (f'<button type="button" class="ir-chip" data-{attr}="{val}" aria-pressed="{"true" if pressed else "false"}">'
            f'{t(label)}</button>')


LEADER_TOOLS = (
    '<div class="ir-lf" role="group">'
    f'<div class="ir-lf-row"><span class="ir-lf-k">{t({"fa": "مرتب‌سازی", "en": "Sort by"})}</span>'
    + chip("sort", "", {"fa": "ارزش بازار", "en": "Market value"}, True)
    + chip("sort", "founded", {"fa": "قدیمی‌ترین", "en": "Oldest first"})
    + chip("sort", "sales", {"fa": "بیشترین فروش", "en": "Highest sales"})
    + chip("sort", "assets", {"fa": "بیشترین دارایی", "en": "Largest assets"})
    + '</div>'
    f'<div class="ir-lf-row"><span class="ir-lf-k">{t({"fa": "بورس", "en": "Exchange"})}</span>'
    + chip("listed", "", {"fa": "همه", "en": "All"}, True)
    + chip("listed", "bourse", {"fa": "بورس تهران", "en": "Tehran Stock Exchange"})
    + chip("listed", "fara", {"fa": "فرابورس", "en": "Farabourse"})
    + chip("listed", "no", {"fa": "غیربورسی", "en": "Not listed"})
    + '</div>'
    f'<div class="ir-lf-row"><span class="ir-lf-k">{t({"fa": "مالکیت", "en": "Ownership"})}</span>'
    + chip("ownership", "", {"fa": "همه", "en": "All"}, True)
    + "".join(chip("ownership", k, v) for k, v in OWNERSHIP.items())
    + '</div>'
    f'<div class="ir-lf-row"><span class="ir-lf-k">{t({"fa": "صادرات", "en": "Exports"})}</span>'
    + chip("exporter", "", {"fa": "همه", "en": "All"}, True)
    + chip("exporter", "yes", {"fa": "صادرکننده", "en": "Exporter"})
    + chip("exporter", "no", {"fa": "غیرصادرکننده", "en": "Not exporting"})
    + '</div></div>'
)

LEADER_JS = r"""
(function () {
  var sec = document.getElementById("leaders"); if (!sec) return;
  var list = sec.querySelector(".ir-leaders"), none = sec.querySelector(".ir-lf-none");
  var items = Array.prototype.slice.call(list.children);
  var state = { sort: "", listed: "", ownership: "", exporter: "" };
  function render() {
    var shown = items.filter(function (li) {
      return ["listed", "ownership", "exporter"].every(function (k) {
        return !state[k] || li.getAttribute("data-" + k) === state[k];
      });
    });
    var order = shown.slice();
    if (state.sort) {
      order.sort(function (a, b) {
        var x = a.getAttribute("data-" + state.sort), y = b.getAttribute("data-" + state.sort);
        if (x === null && y === null) return 0; if (x === null) return 1; if (y === null) return -1;
        return state.sort === "founded" ? Number(x) - Number(y) : Number(y) - Number(x);
      });
    }
    items.forEach(function (li) { li.hidden = shown.indexOf(li) < 0; li.classList.remove("ir-lf-hl"); });
    order.forEach(function (li) { list.appendChild(li); });
    sec.querySelectorAll(".ir-lf-facts > div").forEach(function (d) {
      d.classList.toggle("on", !!state.sort && d.getAttribute("data-f") === state.sort);
    });
    sec.querySelectorAll(".ir-more-d").forEach(function (d) { d.open = !!state.sort; });
    none.hidden = shown.length > 0;
  }
  sec.querySelectorAll(".ir-chip").forEach(function (b) {
    var key = ["sort", "listed", "ownership", "exporter"].filter(function (k) { return b.hasAttribute("data-" + k); })[0];
    b.addEventListener("click", function () {
      state[key] = b.getAttribute("data-" + key);
      sec.querySelectorAll(".ir-chip[data-" + key + "]").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      render();
    });
  });
})();
"""

def branch_page(b, companies):
    art, is_photo = hero_art(b)
    caption = "" if is_photo else f'<figcaption>{t(UI["art"])}</figcaption>'
    if is_photo and b["hero"].get("credit"):
        cr = b["hero"]["credit"]
        caption = f'<figcaption>{t(cr) if isinstance(cr, dict) else e(cr)}</figcaption>'
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
    subname = {s["id"]: s for s in b["subs"]}
    top = sorted((c for c in TOP["companies"] if c["branch"] == b["slug"]), key=lambda c: c["rank"])
    syms = {c["sym"] for c in top}
    rest = [x for x in b.get("leaders", []) if x.get("sym") not in syms]
    subs_ids = [x["id"] for x in b["subs"]]
    wmax = max([c["weight"] for c in top] or [1])
    leaders = "".join(leader_card(x, subname, tint(b["accent"], subs_ids.index(x["sub"])),
                                  x["weight"] / wmax if x.get("weight") else None) for x in top + rest)
    leaders_html = (f'''<section class="ir-sec" id="leaders">
      <h2>{t(UI["leaders"])}</h2>
      <p class="ir-lead" style="margin:0 0 18px">{t(UI["leaders_note"])} <a class="ir-more" href="iran.html#top100">{t(UI["top_link"])}</a></p>
      {map_section(DATA["branches"], b["slug"])}
      {LEADER_TOOLS}
      <ul class="ir-leaders">{leaders}</ul>
      <p class="ir-lf-none" hidden>{t(UI["lf_none"])}</p>
    </section>
    <script>{LEADER_JS}</script>''' if leaders else "")
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

    {leaders_html}

    <section class="ir-sec">
      <h2>{t(UI["companies"])}</h2>
      {cos}
    </section>

    <div class="ir-notice"><span>{t(UI["notice"])}</span><span>{t(UI["reviewed"])}</span></div>
  </main>"""
    title = f'{b["name"]["en"]} | {b["name"]["fa"]} | What Iran Has | Ditoman'
    return page(title, b["intro"]["en"], f'iran-{b["slug"]}.html', body)



# ---------- Market map (iran-map.js draws it) ----------
import colorsys


def tint(hexc, i):
    """A sibling colour for sub-branch i, turned around the colour wheel from the branch accent."""
    r, g, b = (int(hexc[k:k + 2], 16) / 255 for k in (1, 3, 5))
    h, l, s_ = colorsys.rgb_to_hls(r, g, b)
    step = (i + 1) // 2 * (1 if i % 2 else -1)
    h = (h + step * 0.045) % 1
    l = min(max(l + step * 0.04, 0.45), 0.8)
    r, g, b = colorsys.hls_to_rgb(h, l, s_)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def map_section(branches, only=None):
    bmap = {b["slug"]: b for b in branches}
    items = []
    for c in TOP["companies"]:
        if only and c["branch"] != only:
            continue
        b = bmap[c["branch"]]
        subs = [x["id"] for x in b["subs"]]
        sub = b["subs"][subs.index(c["sub"])]
        color = tint(b["accent"], subs.index(c["sub"])) if only else b["accent"]
        facts = [{"k": FIELDS[0][1], "v": mcap_value(c)},
                 {"k": {"fa": "بازار", "en": "Market"}, "v": MARKETS[c["market"]]},
                 {"k": {"fa": "صادرکننده", "en": "Exporter"}, "v": YESNO[True] if c.get("exporter") else None},
                 {"k": {"fa": "نوع مالکیت", "en": "Ownership"}, "v": OWNERSHIP.get(c.get("ownership"))},
                 {"k": {"fa": "سال تأسیس", "en": "Founded"}, "v": field_value(c, "founded")},
                 {"k": {"fa": "فروش سالانه", "en": "Annual sales"}, "v": field_value(c, "sales")},
                 {"k": {"fa": "دارایی کل", "en": "Total assets"}, "v": field_value(c, "assets")}]
        items.append({
            "rank": c["rank"], "sym": c["sym"], "fa": c["fa"], "en": c["en"], "w": c["weight"],
            "short": re.sub(r"\s*\(.*?\)", "", c["en"]),
            "approx": not c.get("mcap"), "val": mcap_value(c), "b": b["slug"], "bname": b["name"],
            "sub": c["sub"], "subname": {"fa": sub["fa"], "en": sub["en"]},
            "g": c["sub"] if only else b["slug"], "gname": {"fa": sub["fa"], "en": sub["en"]} if only else b["name"],
            "color": color, "fam": c.get("family"), "famname": TOP["families"].get(c.get("family"), None),
            "facts": facts, "href": None if only else f'iran-{b["slug"]}.html#leaders'})
    if not items:
        return ""
    data = json.dumps({"items": items, "pending": PENDING}, ensure_ascii=False).replace("</", "<\\/")
    hint = {"fa": "اندازه‌ی هر کاشی، ارزش بازار شرکت است. روی هر کاشی بزنید تا جزئیات و شرکت‌های هم‌خانواده و هم‌رشته‌اش روشن شوند.",
            "en": "Each tile's size is the company's market value. Tap a tile to see its details and light up its family and its sub-branch."}
    return (f'<p class="ir-map-hint">{t(hint)}</p><div class="ir-map" role="group"></div>'
            f'<script type="application/json" id="ir-map-data">{data}</script>'
            f'<script src="iran-map.js?v=2" defer></script>')


TOP_JS = r"""
(function () {
  var sec = document.getElementById("top100"); if (!sec) return;
  var rows = sec.querySelectorAll("tbody tr");
  sec.querySelectorAll(".ir-chip").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-branch");
      sec.querySelectorAll(".ir-chip").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      rows.forEach(function (r) { r.hidden = !!v && r.getAttribute("data-branch") !== v; });
    });
  });
})();
"""


def top_section(branches):
    bmap = {b["slug"]: b for b in branches}
    rows = []
    for c in TOP["companies"]:
        b = bmap[c["branch"]]
        sub = {s["id"]: s for s in b["subs"]}[c["sub"]]
        v = mcap_value(c)
        cls = "v" if c.get("mcap") else ("v min" if v else "v na")
        approx = "" if c.get("mcap") else "≈"
        rows.append(
            f'<tr data-branch="{b["slug"]}"><td class="n">{t({"fa": approx + fa_digits(c["rank"]), "en": approx + str(c["rank"])})}</td>'
            f'<td>{t({"fa": c["sym"], "en": c["isin"]})}</td><td class="name">{t(c)}</td>'
            f'<td><a href="iran-{b["slug"]}.html#leaders"><span class="dot" style="background:{e(b["accent"])}"></span>{t(b["name"])}</a>'
            f' <small style="color:var(--muted)">· {t(sub)}</small></td>'
            f'<td>{t(MARKETS[c["market"]])}</td><td class="{cls}">{t(v or PENDING)}</td></tr>')
    chips = chip("branch", "", UI["all_branches"], True) + "".join(
        chip("branch", b["slug"], b["name"]) for b in branches if any(c["branch"] == b["slug"] for c in TOP["companies"]))
    head = "".join(f"<th>{t(UI[k])}</th>" for k in ("col_rank", "col_sym", "col_name", "col_branch", "col_market", "col_mcap"))
    return f'''<section class="ir-sec" id="top100">
      <h2>{t(UI["top_title"])}</h2>
      <p class="ir-lead" style="margin:0 0 18px">{t(UI["top_lead"])} {t({"fa": "تاریخ داده‌ها: " + TOP["as_of"]["fa"], "en": "Data as of " + TOP["as_of"]["en"]})}</p>
      {map_section(branches)}
      <details class="ir-top-list"><summary>{t({"fa": "نمایش به صورت فهرست", "en": "Show as a list"})}</summary>
      <div class="ir-lf" role="group"><div class="ir-lf-row"><span class="ir-lf-k">{t(UI["col_branch"])}</span>{chips}</div></div>
      <div class="ir-top-wrap"><table class="ir-top"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>
      <p class="ir-top-note"><b>{t(UI["top_method"])}:</b> {t(TOP["source"])} {t(TOP["method"])}</p>
    </section>
    <script>{TOP_JS}</script>'''


def hub_page(branches):
    s = DATA["section"]
    feats = "".join(feature_card(f, "hub") for f in s.get("features", []))
    cards = feats + "".join(card(b, "hub") for b in branches)
    body = f"""  <main class="k-main wrap">
    {toggle(t(UI["section"]))}
    <section class="ir-hero">
      <h1>{t(s["name"])}</h1>
      <p>{t(s["lead"])}</p>
    </section>
    <div class="ir-grid">{cards}</div>
    <p class="ir-note">{t(s["method"])} <a href="companies.html">{t(UI["all"])}</a></p>
    {top_section(branches)}
    <div class="ir-notice"><span>{t(UI["notice"])}</span><span>{t(UI["reviewed"])}</span></div>
  </main>"""
    return page("What Iran Has | ایران چه دارد | Ditoman", s["lead"]["en"], "iran.html", body)


def homepage(branches):
    path = ROOT / "index.html"
    page_html = path.read_text(encoding="utf-8")
    feats = "".join("\n          " + feature_card(f, "home") for f in DATA["section"].get("features", []))
    cards = feats + "".join("\n          " + card(b, "home") for b in branches)
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
        # Replace only this block: it runs until the next comment header, so styles after it are kept.
        i = css.index(start)
        j = css.find("\n/* ", i + len(start))
        rest = css[j:] if j != -1 else "\n"
        css = css[:i] + CARD_CSS.strip("\n") + "\n" + rest
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
    import lang_unify
    lang_unify.main()
