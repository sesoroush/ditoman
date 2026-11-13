#!/usr/bin/env python3
"""Build lesson pages from the data files in scripts/lessons/data/.

Each data file is a Python module with one dict, LESSON (see lesson12.py for the shape).
The page shell (head styles, site header, footer, scripts) is taken from lesson11.html, so
every lesson built here matches the lessons already on the site.

Body text uses a tiny markup, one block per line:
  ## Heading        numbered section heading
  ##! Heading       heading without a number
  [[fig]]           the lesson's diagram
  **bold**          strong text
  `0x`              Latin letters and digits kept as typed inside Persian text
  anything else     a paragraph

Run from the repo root: python3 scripts/lessons/build.py [lesson12 ...]
Then run build_en_pages.py, build_seo.py and build_search.py.
"""
import html
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = Path(__file__).resolve().parent / "data"
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
FA_LETTERS = ["الف", "ب", "ج", "د"]
P_FA = '<p lang="fa" dir="rtl" style="text-align:right">'


def fa_num(n, width=0):
    return "".join(FA_DIGITS[int(c)] for c in str(n).zfill(width))


def esc(s):
    return html.escape(s, quote=False)


def inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))
    return re.sub(r"`(.+?)`", r'<bdi class="lz-lat">\1</bdi>', s)


def figure(fig, lang):
    if not fig:
        return ""
    i = 0 if lang == "en" else 1
    d = "" if lang == "en" else ' dir="rtl"'
    out = [f'<figure class="lz-fig"{d}><figcaption>{esc(fig["title"][i])}</figcaption>']
    if fig["type"] == "flow":
        out.append('<ol class="lz-flow">')
        for n, step in enumerate(fig["steps"], 1):
            num = n if lang == "en" else fa_num(n)
            out.append(f'<li><b>{num}</b><span>{inline(step[i])}</span></li>')
        out.append("</ol>")
    else:
        out.append('<div class="lz-scroll"><table class="lz-table"><thead><tr>')
        out += [f"<th>{esc(c[i])}</th>" for c in fig["cols"]]
        out.append("</tr></thead><tbody>")
        for row in fig["rows"]:
            out.append("<tr>" + "".join(f"<td>{inline(c[i])}</td>" for c in row) + "</tr>")
        out.append("</tbody></table></div>")
    out.append("</figure>")
    return "\n".join(out)


def body(text, lang, fig):
    out, n = [], 0
    p_open = '<p lang="en">' if lang == "en" else P_FA
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line == "[[fig]]":
            out.append(figure(fig, lang))
        elif line.startswith("##!"):
            out.append(f"<h3>{esc(line[3:].strip())}</h3>")
        elif line.startswith("##"):
            n += 1
            num = f"{n:02d}" if lang == "en" else fa_num(n, 2)
            out.append(f'<h3><span class="check-number">{num}.</span> {esc(line[2:].strip())}</h3>')
        else:
            out.append(f"{p_open}{inline(line)}</p>")
    return "\n".join(out)


def ul(items, lang):
    lis = "".join(f"<li>{esc(x)}</li>" for x in items)
    if lang == "en":
        return f'<ul lang="en">{lis}</ul>'
    return f'<ul lang="fa" dir="rtl" style="padding-left:0;padding-right:22px">{lis}</ul>'


def quiz(items):
    out = []
    for n, q in enumerate(items, 1):
        out.append('<div class="quiz-item">')
        out.append(f'<h3 lang="en">Question {n}</h3>')
        out.append(f'<h3 lang="fa" dir="rtl" style="text-align:right">پرسش {fa_num(n)}</h3>')
        out.append(f'<p lang="en">{esc(q["q"][0])}</p>')
        out.append(f'{P_FA}{esc(q["q"][1])}</p>')
        for k, opt in enumerate(q["options"]):
            out.append(f'<p lang="en">{"ABCD"[k]}. {esc(opt[0])}</p>')
            out.append(f'{P_FA}{FA_LETTERS[k]}. {esc(opt[1])}</p>')
        k = q["answer"]
        note = q.get("note", ("", ""))
        out.append(f'<p class="answer" lang="en">Correct answer: {"ABCD"[k]}{". " + esc(note[0]) if note[0] else ""}</p>')
        out.append(f'<p class="answer" lang="fa" dir="rtl" style="text-align:right">پاسخ درست: {FA_LETTERS[k]}{". " + esc(note[1]) if note[1] else ""}</p>')
        out.append("</div>")
    return "\n".join(out)


STYLE = """
<style>
.lz-fig { margin: 26px 0; padding: 20px; border-radius: 18px; background: rgba(87,217,199,.06); border: 1px solid rgba(87,217,199,.28); }
.lz-fig figcaption { font-weight: 800; color: #57d9c7; margin-bottom: 14px; font-size: 1.02rem; }
.lz-flow { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
.lz-flow li { display: flex; gap: 12px; align-items: flex-start; padding: 12px 14px; border-radius: 14px; background: #101f22; border: 1px solid rgba(242,240,233,.12); line-height: 1.7; }
.lz-flow b { flex: none; display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: #ffad00; color: #101f22; font-weight: 800; }
.lz-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.lz-table { width: 100%; border-collapse: collapse; min-width: 460px; font-size: .95rem; }
.lz-table th, .lz-table td { padding: 10px 12px; border-bottom: 1px solid rgba(242,240,233,.12); text-align: start; vertical-align: top; line-height: 1.6; }
.lz-table th { color: #ffad00; font-weight: 800; white-space: nowrap; }
.lz-lat { font-family: var(--en); direction: ltr; unicode-bidi: isolate; }
.lz-table td:first-child { font-weight: 700; color: #f2f0e9; }
</style>
"""


def page(L, shell_head, shell_tail, prev_slug, next_slug):
    slug, n = L["slug"], L["number"]
    cover, cover_en = f'{slug}-cover.jpg', f'{slug}-cover-en.jpg'
    alt = esc(L["title"][0]) + " Ditoman lesson image"
    title = f'{L["title"][1]} | {L["title"][0]} | Ditoman Learn'
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(title)}</title>", shell_head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  lambda m: '<meta name="description" content="' + html.escape(L["subtitle"][0]) + '"', head, count=1)
    head = re.sub(r"\s*<!-- hreflang:start -->.*?<!-- hreflang:end -->", "", head, flags=re.S)
    head = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->\n?", "", head, flags=re.S)
    head = head.replace("</head>", STYLE.strip() + "\n</head>", 1)

    rel = L["related"]
    nav = ['<a class="button" href="learn.html"><span lang="en">Back to Learn</span><span lang="fa">بازگشت به آموزش</span></a>']
    if prev_slug:
        nav.append(f'<a class="button" href="{prev_slug}.html"><span lang="en">Previous Lesson</span><span lang="fa">درس قبلی</span></a>')
    if next_slug:
        nav.append(f'<a class="button" href="{next_slug}.html"><span lang="en">Next Lesson</span><span lang="fa">درس بعدی</span></a>')
    sources = "".join(
        f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener noreferrer" style="color:#7ff5de">{esc(t)}</a></li>'
        for u, t in L["sources"])
    minutes = L["minutes"]
    main = f"""<main>
<section class="hero">
<div class="container">
<div class="hero-image">
<img lang="fa" src="{cover}" alt="{alt}" style="width:100%;height:auto"><img lang="en" src="{cover_en}" alt="{alt}" style="width:100%;height:auto">
</div>
<div class="lesson-badge" lang="en">{esc(L["badge"][0])}</div>
<div class="lesson-badge" lang="fa" dir="rtl" style="letter-spacing:0;text-transform:none;display:table;margin-left:auto">{esc(L["badge"][1])}</div>
<h1 lang="en">{esc(L["title"][0])}</h1>
<h1 lang="fa" dir="rtl" style="text-align:right">{esc(L["title"][1])}</h1>
<p class="subtitle" lang="en">{esc(L["subtitle"][0])}</p>
<p class="subtitle" lang="fa" dir="rtl" style="text-align:right;margin-left:auto">{esc(L["subtitle"][1])}</p>
<div class="meta-grid">
<div class="meta-box"><span lang="en">Level</span><span lang="fa" dir="rtl" style="letter-spacing:0;text-transform:none">سطح</span><strong lang="en">Beginner</strong><strong lang="fa" dir="rtl" style="display:block">مقدماتی</strong></div>
<div class="meta-box"><span lang="en">Reading Time</span><span lang="fa" dir="rtl" style="letter-spacing:0;text-transform:none">زمان مطالعه</span><strong lang="en">{minutes} Minutes</strong><strong lang="fa" dir="rtl" style="display:block">{fa_num(minutes)} دقیقه</strong></div>
<div class="meta-box"><span lang="en">Learning Points</span><span lang="fa" dir="rtl" style="letter-spacing:0;text-transform:none">امتیاز یادگیری</span><strong lang="en">20 LP</strong><strong lang="fa" dir="rtl" style="display:block">۲۰ امتیاز</strong></div>
<div class="meta-box"><span lang="en">Quiz</span><span lang="fa" dir="rtl" style="letter-spacing:0;text-transform:none">آزمونک</span><strong lang="en">{len(L["quiz"])} Questions</strong><strong lang="fa" dir="rtl" style="display:block">{fa_num(len(L["quiz"]))} پرسش</strong></div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<h2 class="section-title" lang="en">Lesson Content</h2>
<h2 class="section-title" lang="fa" dir="rtl" style="text-align:right">محتوای درس</h2>
<p class="section-subtitle" lang="en">Read the lesson in English or Persian.</p>
<p class="section-subtitle" lang="fa" dir="rtl" style="text-align:right;margin-left:auto">درس را به فارسی یا انگلیسی بخوانید.</p>

<div class="language-toggle">
<button class="lang-button active" onclick="showLanguage('en')">English</button>
<button class="lang-button" onclick="showLanguage('fa')">فارسی</button>
</div>

<div class="lesson-content en" id="en-content">
{body(L["en"], "en", L.get("fig"))}
</div>

<div class="lesson-content fa" id="fa-content">
{body(L["fa"], "fa", L.get("fig"))}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="self-check">
<h2 class="section-title" lang="en">{esc(rel["title"][0])}</h2>
<h2 class="section-title" lang="fa" dir="rtl" style="text-align:right">{esc(rel["title"][1])}</h2>
<p lang="en">{esc(rel["text"][0])}</p>
{P_FA}{esc(rel["text"][1])}</p>
<div class="cta-row">
<a class="cta" href="{rel["links"][0][0]}"><span lang="en">{esc(rel["links"][0][1])}</span><span lang="fa">{esc(rel["links"][0][2])}</span></a>
<a class="button" href="{rel["links"][1][0]}"><span lang="en">{esc(rel["links"][1][1])}</span><span lang="fa">{esc(rel["links"][1][2])}</span></a>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container grid-two">
<div class="card">
<h3 lang="en">Key Concepts</h3>
<h3 lang="fa" dir="rtl" style="text-align:right">مفاهیم کلیدی</h3>
{ul(L["concepts"][0], "en")}
{ul(L["concepts"][1], "fa")}
</div>
<div class="card">
<h3 lang="en">Learning Objectives</h3>
<h3 lang="fa" dir="rtl" style="text-align:right">اهداف یادگیری</h3>
{ul(L["objectives"][0], "en")}
{ul(L["objectives"][1], "fa")}
</div>
</div>
</section>

<section class="section">
<div class="container">
<h2 class="section-title" lang="en">Quiz</h2>
<h2 class="section-title" lang="fa" dir="rtl" style="text-align:right">آزمونک</h2>
<p class="section-subtitle" lang="en">Check what stayed with you. The answer is under each question.</p>
<p class="section-subtitle" lang="fa" dir="rtl" style="text-align:right;margin-left:auto">ببین چه چیزی در ذهنت مانده. پاسخ زیر هر پرسش آمده است.</p>
<div class="quiz-list">
{quiz(L["quiz"])}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="card">
<h3 lang="en">Sources</h3>
<h3 lang="fa" dir="rtl" style="text-align:right">منابع</h3>
<ul>{sources}</ul>
<p lang="en" style="font-size:0.95rem">{esc(L["source_note"][0])}</p>
<p lang="fa" dir="rtl" style="text-align:right;font-size:0.95rem">{esc(L["source_note"][1])}</p>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="instagram-box">
<h2 class="section-title"><span lang="fa">با هم دنبال می‌کنیم</span><span lang="en">Follow along</span></h2>
<p lang="en">New lessons are announced first on Ditoman's channels.</p>
{P_FA}درس‌های تازه اول در کانال‌های دیتومان معرفی می‌شوند.</p>
<div class="cta-row">
{chr(10).join(nav)}
</div>
</div>
</div>
</section>
</main>
"""
    return head + main + shell_tail


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LESSON


def main():
    shell = (ROOT / "lesson11.html").read_text(encoding="utf-8")
    a, b = shell.index("<main>"), shell.index("</main>") + len("</main>\n")
    head, tail = shell[:a], shell[b:]
    lessons = sorted((load(p) for p in DATA.glob("lesson*.py")), key=lambda L: L["number"])
    slugs = ["lesson11"] + [L["slug"] for L in lessons]
    only = set(sys.argv[1:])
    for i, L in enumerate(lessons, 1):
        if only and L["slug"] not in only:
            continue
        nxt = slugs[i + 1] if i + 1 < len(slugs) else None
        (ROOT / f'{L["slug"]}.html').write_text(page(L, head, tail, slugs[i - 1], nxt), encoding="utf-8")
        print("built", L["slug"], "|", L["title"][0])


if __name__ == "__main__":
    main()
