"""Ditoman daily market calendar: renders the post (1080x1350) and story (1080x1920)
images from one day's data file and adds the day to calendar/index.json for the website.

Usage:  python3 scripts/calendar/build.py calendar/data/2026-10-28.json

Data file (all text plain, no HTML; Persian may contain Latin numbers like 3.75–4.00%):
{
  "date": "2026-10-28",
  "headline_fa": "امروز، روزِ",          # headline text before the highlighted part
  "headline_hl": "فدرال رزرو",            # highlighted part (turquoise marker)
  "key":   {"kick_en": "FOMC RATE DECISION", "fa": "تصمیم نرخ بهرهٔ آمریکا",
            "story_fa": "تصمیم نرخ بهرهٔ فدرال رزرو",          # optional, shorter title for the story
            "body_fa": "...one or two sentences...", "story_note_fa": "...short...",
            "tehran": "21:30", "lisbon": "18:00", "en": "US Fed (FOMC) rate decision", "expected": "Hold 3.75–4.00%"},
  "today": [ {"fa": "...", "note_fa": "...", "tehran": "17:15", "lisbon": "13:45", "en": "...", "expected": "..."} ],   # 0-3 items
  "week":  [ {"day_fa": "پنجشنبه", "date": "2026-10-29", "fa": "...", "note_fa": "...", "tehran": "16:00", "lisbon": "12:30", "en": "...", "expected": "..."} ],  # 0-4 items
  "sources": ["https://..."]
}
The story shows the key event plus the first two "today" items (or the first week items if today has fewer).
Exits with status 2 if any text overflows its box, so the caller knows to shorten it.
"""
import html, json, os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "report"))
from jalali import g2j  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FA_DIG = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
FA_M = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
FA_WD = ["دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه","شنبه","یکشنبه"]
EN_M = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
EN_WD = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

import re, datetime
def e(s): return html.escape(str(s or ""))
def nums(s):
    """Escape and wrap Latin numbers/percentages so they read left-to-right inside Persian text."""
    return re.sub(r"~?[\d.]+(?:[–-][\d.]+)?%?", lambda m: '<span class="ltr">' + m.group(0) + "</span>", e(s))
def chip(it, cls="chip"):
    return f'<div class="{cls}"><span class="t">Tehran {e(it["tehran"])}</span><span class="s">· Lisbon {e(it["lisbon"])}</span></div>'

def page(css, body, title):
    return f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>{e(title)}</title><link rel="stylesheet" href="base.css"><style>{css}</style></head><body>{body}</body></html>'

POST_CSS = """.page{width:1080px;height:1350px}.mast{height:96px}
.head{padding:36px 56px 22px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.head h1{font-weight:800;font-size:62px;line-height:1.25}
.head .date{direction:ltr;display:flex;flex-direction:column;gap:6px;align-items:flex-start;flex-shrink:0}
.head .date .fa{direction:rtl;font-weight:700;font-size:26px;color:var(--teal)}
.head .date .en{font-family:Play,serif;font-style:italic;font-size:24px;color:var(--muted)}
.hero{margin:14px 56px 0;border:3px solid var(--ink);background:var(--ink);color:var(--cream);display:flex;align-items:stretch;position:relative;flex-shrink:0}
.hero .txt{flex:1;padding:28px 32px;display:flex;flex-direction:column;gap:12px}
.hero .kick{font-family:Brico,sans-serif;font-weight:700;letter-spacing:.18em;font-size:16px;color:var(--pop);direction:ltr;text-align:right}
.hero h2{font-weight:800;font-size:44px;line-height:1.35}
.hero p{font-size:23px;line-height:1.75;color:#E6DED0}
.hero .time{width:270px;background:var(--pop);color:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border-right:3px solid var(--ink)}
.hero .time .big{font-family:Brico,sans-serif;font-weight:800;font-size:76px;line-height:1;direction:ltr}
.hero .time .lab{font-weight:700;font-size:20px}
.hero .time .sm{font-family:Brico,sans-serif;font-size:19px;direction:ltr;margin-top:8px;font-weight:600}
.stamp{position:absolute;right:28px;top:-24px;transform:rotate(3deg);background:var(--cream);border:3px solid var(--ink);padding:6px 16px;font-weight:800;font-size:20px;color:var(--ink)}
.sec{padding:24px 56px 0}
.sec h3{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:10px;margin-bottom:4px}
.sec h3 .fa{font-weight:800;font-size:32px}
.sec h3 .en{font-family:Play,serif;font-style:italic;font-weight:500;font-size:24px;color:var(--teal);direction:ltr}
.row{display:flex;justify-content:space-between;align-items:center;gap:22px;padding:14px 0;border-bottom:1px solid var(--rule)}
.row:last-child{border-bottom:none}
.row .what{display:flex;flex-direction:column;gap:3px}
.row .what b{font-weight:800;font-size:27px}
.row .what span{font-size:20px;color:var(--muted);line-height:1.6}
.row .chip{font-size:19px;flex-shrink:0}
.day{font-weight:800;color:var(--teal);font-size:20px;margin-left:14px}
.foot{height:76px;margin-top:auto}"""

STORY_CSS = """.page{width:1080px;height:1920px}
.mast{height:110px;margin-top:120px;border-top:3px solid var(--ink)}
.head{padding:70px 64px 50px;display:flex;flex-direction:column;gap:18px}
.head .date{font-weight:700;font-size:32px;color:var(--teal)}
.head .date .en{font-family:Play,serif;font-style:italic;font-weight:400;color:var(--muted);font-size:28px;margin-right:14px;direction:ltr;unicode-bidi:isolate}
.head h1{font-weight:800;font-size:92px;line-height:1.25}
.items{padding:0 64px;display:flex;flex-direction:column;gap:40px}
.item{border:3px solid var(--ink);display:flex;align-items:stretch;background:#fff8ee}
.item .n{width:120px;display:flex;align-items:center;justify-content:center;font-family:Play,serif;font-weight:800;font-size:72px;border-left:3px solid var(--ink);background:var(--cream);flex-shrink:0}
.item .body{flex:1;padding:40px 36px;display:flex;flex-direction:column;gap:16px}
.item b{font-weight:800;font-size:46px;line-height:1.35}
.item p{font-size:29px;color:var(--muted);line-height:1.65}
.item .chip{font-size:27px;align-self:flex-start}
.item.top{background:var(--ink);color:var(--cream)}
.item.top .n{background:var(--pop);color:var(--ink)}
.item.top p{color:#E6DED0}
.item.top .chip{background:var(--pop);border-color:var(--pop)}
.item.top .chip .t,.item.top .chip .s{color:var(--ink)}
.note{margin:70px 64px 0;font-size:36px;font-weight:700;line-height:1.7;text-align:center}
.foot{height:90px;margin-top:auto;margin-bottom:150px}"""

MAST = ('<div class="mast" dir="ltr"><div class="brand">DITOMAN</div><div class="tag"><span>{en}</span><span class="dot"></span>'
        '<span style="font-family:Vaz;letter-spacing:0;color:var(--teal)">{fa}</span></div></div>')
FOOT = '<div class="foot" dir="ltr"><span class="l">DITOMAN | PEOPLE • IDEAS • A FAIRER TOMORROW</span><span class="r">ditoman.com</span></div>'

def build(d):
    y, m, dd = map(int, d["date"].split("-"))
    wd = datetime.date(y, m, dd).weekday()
    jy, jm, jd = g2j(y, m, dd)
    fa_date = f"{FA_WD[wd]} {str(jd).translate(FA_DIG)} {FA_M[jm-1]} {str(jy).translate(FA_DIG)}"
    k = d["key"]
    h1 = f'{e(d["headline_fa"])} <span class="hl">{e(d["headline_hl"])}</span>'

    rows_today = "".join(f'<div class="row"><div class="what"><b>{e(t["fa"])}</b><span>{nums(t.get("note_fa"))}</span></div>{chip(t)}</div>' for t in d.get("today", [])[:3])
    rows_week = "".join(f'<div class="row"><div class="what"><b><span class="day">{e(w.get("day_fa"))}</span>{e(w["fa"])}</b><span>{nums(w.get("note_fa"))}</span></div>{chip(w)}</div>' for w in d.get("week", [])[:4])
    post = ('<div class="page">' + MAST.format(en="MARKET CALENDAR", fa="تقویم بازار") +
            f'<div class="head"><h1>{h1}</h1><div class="date"><span class="fa">{fa_date}</span><span class="en">{EN_WD[wd]}, {dd} {EN_M[m-1]} {y}</span></div></div>'
            f'<div class="hero"><div class="stamp">مهم‌ترین خبر روز</div><div class="txt"><div class="kick">{e(k.get("kick_en"))}</div><h2>{e(k["fa"])}</h2><p>{nums(k.get("body_fa"))}</p></div>'
            f'<div class="time"><div class="lab">به وقت تهران</div><div class="big">{e(k["tehran"])}</div><div class="sm">Lisbon {e(k["lisbon"])}</div></div></div>'
            + (f'<div class="sec"><h3><span class="fa">بقیهٔ امروز</span><span class="en">Also today</span></h3>{rows_today}</div>' if rows_today else "")
            + (f'<div class="sec"><h3><span class="fa">{e(d.get("week_label_fa","بقیهٔ هفته"))}</span><span class="en">{e(d.get("week_label_en","This week"))}</span></h3>{rows_week}</div>' if rows_week else "")
            + FOOT + "</div>")

    picks = [dict(k, fa=k.get("story_fa") or k["fa"], note_fa=k.get("story_note_fa") or k.get("body_fa"))]
    for t in d.get("today", []) + [dict(w, fa=f'{w.get("day_fa", "")}: {w["fa"]}') for w in d.get("week", [])]:
        if len(picks) == 3: break
        picks.append(t)
    items = "".join(f'<div class="item{" top" if i == 0 else ""}"><div class="n">{i+1}</div><div class="body"><b>{e(p["fa"])}</b><p>{nums(p.get("note_fa"))}</p>{chip(p)}</div></div>' for i, p in enumerate(picks))
    story = ('<div class="page">' + MAST.format(en="TODAY", fa="امروز") +
             f'<div class="head"><div class="date">{fa_date}<span class="en">{dd} {EN_M[m-1]} {y}</span></div><h1>{str(len(picks)).translate(FA_DIG)} خبر مهمِ <span class="hl">امروز</span></h1></div>'
             f'<div class="items">{items}</div><div class="note">آمار قیمت‌ها: <span class="hl">امشب ساعت ۲۰:۰۰ تهران</span></div>' + FOOT + "</div>")
    return fa_date, page(POST_CSS, post, "post"), page(STORY_CSS, story, "story")

def main(path):
    d = json.load(open(path, encoding="utf-8"))
    date = d["date"]
    fa_date, post_html, story_html = build(d)
    out = ROOT / "calendar"; out.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h, src in [("post", 1080, 1350, post_html), ("story", 1080, 1920, story_html)]:
            tmp = HERE / f"_{name}.html"
            tmp.write_text(src, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            over = pg.evaluate("""() => { const pg = document.querySelector('.page'); const bad = [];
                if (pg.scrollHeight > pg.clientHeight + 1) bad.push('page height ' + pg.scrollHeight);
                const foot = document.querySelector('.foot').getBoundingClientRect();
                document.querySelectorAll('.page > *:not(.foot)').forEach(el => { const r = el.getBoundingClientRect(); if (r.bottom > foot.top + 1) bad.push('overlaps footer: ' + el.className); });
                document.querySelectorAll('h1,h2,b,p,.chip').forEach(el => { if (el.scrollWidth > el.clientWidth + 2) bad.push('too wide: ' + el.textContent.slice(0, 40)); });
                return bad; }""")
            bad += [f"{name}: {x}" for x in over]
            pg.screenshot(path=str(out / f"{date}-{name}.png"))
            tmp.unlink()
        b.close()
    idx_path = out / "index.json"
    idx = json.load(open(idx_path, encoding="utf-8")) if idx_path.exists() else []
    idx = [x for x in idx if x.get("date") != date]
    jy, jm, jd = g2j(*map(int, date.split("-")))
    k = d["key"]
    idx.append({
        "date": date, "jalali": f"{jy}/{jm:02d}/{jd:02d}", "weekday_fa": fa_date.split(" ")[0],
        "headline_fa": f'{d["headline_fa"]} {d["headline_hl"]}'.strip(),
        "post": f"calendar/{date}-post.png", "story": f"calendar/{date}-story.png",
        "today": [{"key": True, "fa": k["fa"], "en": k.get("en", ""), "tehran": k["tehran"], "lisbon": k["lisbon"],
                   "note_fa": k.get("body_fa", ""), "expected": k.get("expected", "")}] + d.get("today", []),
        "week": d.get("week", []), "sources": d.get("sources", []),
    })
    idx.sort(key=lambda x: x["date"], reverse=True)
    json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Wrote calendar/{date}-post.png, calendar/{date}-story.png, calendar/index.json")
    if bad:
        print("OVERFLOW:\n  " + "\n  ".join(bad)); sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1])
