"""Ditoman daily press review (خلاصه روزنامه‌های ایران): cover image + website archive.

Usage:  python3 scripts/press/build.py press/data/2026-11-13.json   (Iran press, 10:00 Tehran)
        python3 scripts/press/build.py world/data/2026-11-23.json   (world press, 16:00 Tehran; or "kind": "world")

Data file:
{
  "date": "2026-11-13",
  "lead_fa": "...", "lead_en": "...",
  "sections": [ {"fa": "اقتصاد و بازار", "en": "Economy & markets",
                 "items": [ {"fa": "...", "en": "...", "src": "فرارو", "url": "https://..."} ]} ]
}
Writes press/<date>-post.png (+ .webp, 1254 px square, the reference layout on press/bg.png)
and adds the day to press/index.json, which press.html renders.
"""
import json, pathlib, sys, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "report"))
from jalali import g2j  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
FONTS = ROOT / "scripts" / "report" / "fonts"
LOGO = ROOT / "tmn-logo-512.png"
BG = ROOT / "press" / "bg.png"
FA_DIG = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
FA_M = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
FA_WD = ["دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه","شنبه","یکشنبه"]

CSS = """
@font-face{font-family:Yekan;src:url(%(f)s/IRANYekanXFaNum-Medium.woff2);font-weight:500}
@font-face{font-family:Yekan;src:url(%(f)s/IRANYekanXFaNum-Bold.woff2);font-weight:700}
@font-face{font-family:Yekan;src:url(%(f)s/IRANYekanXFaNum-ExtraBold.woff2);font-weight:800}
@font-face{font-family:Yekan;src:url(%(f)s/IRANYekanXFaNum-Black.woff2);font-weight:900}
@font-face{font-family:Play;src:url(%(f)s/PlayfairDisplay.ttf);font-weight:400 900}
@font-face{font-family:PlayI;src:url(%(f)s/PlayfairDisplay-Italic.ttf);font-weight:400 900;font-style:italic}
@font-face{font-family:Brico;src:url(%(f)s/BricolageGrotesque.ttf);font-weight:200 800}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1254px;height:1254px;overflow:hidden;position:relative;background:url(%(bg)s) 0 0/1254px 1254px no-repeat;font-family:Yekan,sans-serif;color:#151311}
.abs{position:absolute}
.logo{left:52px;top:36px;width:100px;height:100px}
.wm{left:168px;top:40px;display:flex;flex-direction:column;align-items:flex-start;gap:4px}
.wm .fa{font-weight:800;font-size:46px;line-height:1.1;direction:rtl}
.wm .en{font-family:Brico,sans-serif;font-weight:500;font-size:29px;letter-spacing:.3em;line-height:1;color:#1d1a17;margin-left:2px}
.div{left:440px;top:42px;width:2px;height:92px;background:rgba(40,34,28,.55)}
.badge{right:22px;top:48px;height:80px;padding:0 118px 0 44px;display:flex;align-items:center;background:linear-gradient(180deg,#C8262B,#A51D22);color:#fff;font-weight:700;font-size:38px;clip-path:polygon(0 0,100%% 0,100%% 100%%,22px 100%%);box-shadow:0 6px 14px rgba(0,0,0,.18)}
.badge svg{position:absolute;right:30px;top:11px;width:64px;height:58px}
.head{left:0;right:0;top:500px;text-align:center;direction:rtl;font-weight:900;font-size:112px;line-height:1.2;letter-spacing:-.01em}
.head b{color:#8E1B1B;font-weight:900}
.sub{left:0;right:0;top:642px;text-align:center;direction:rtl;font-weight:500;font-size:32px;color:#2b2622}
.rule{top:699px;height:2px;background:#6f6253}
.en1{left:0;right:0;top:734px;text-align:center;font-family:Play,serif;font-weight:800;font-size:76px;line-height:1.1;color:#141311}
.en2{left:0;right:0;top:822px;text-align:center;font-family:PlayI,serif;font-style:italic;font-weight:500;font-size:31px;line-height:1.3;color:#2b2622}
.date{left:0;right:0;top:900px;text-align:center;font-size:24px;color:#6f6253;font-weight:500}
.date .g{font-family:PlayI,serif;font-style:italic;direction:ltr;unicode-bidi:isolate}
.foot{left:0;right:0;bottom:0;height:92px;background:#121a1c;display:flex;align-items:center;justify-content:space-between;padding:0 52px}
.foot .l{font-family:Brico,sans-serif;font-weight:700;font-size:26px;letter-spacing:.16em;color:#F2F0E9}
.foot .r{font-family:PlayI,serif;font-style:italic;font-size:31px;color:#57D9C7}
"""

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>%(css)s%(xcss)s</style></head><body>%(extra)s
<img class="abs logo" src="%(logo)s">
<div class="abs wm"><div class="fa">دیتومان</div><div class="en">DITOMAN</div></div>
<div class="abs div"></div>
<div class="abs badge">مرور روز<svg viewBox="0 0 64 58" fill="none" stroke="#F3ECE0" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"><path d="M12 8h44v38a6 6 0 0 1-6 6H14a6 6 0 0 1-6-6V18h4z"/><path d="M12 8v38"/><path d="M20 18h12v12H20zM38 18h12M38 25h12M20 37h30M20 44h30"/></svg></div>
<div class="abs head">%(head_fa)s</div>
<div class="abs sub">%(sub_fa)s</div>
<div class="abs rule" style="left:60px;width:536px"></div><div class="abs rule" style="left:672px;width:522px"></div>
<div class="abs en1">%(en1)s</div>
<div class="abs en2">%(en2)s</div>
<div class="abs date" dir="rtl">%(fa_date)s &nbsp;·&nbsp; <span class="g">%(en_date)s</span></div>
<div class="abs foot"><span class="l">DITOMAN | TMN · DITOMAN.COM</span><span class="r">Learn · Connect · Evolve</span></div>
</body></html>"""


KINDS = {
    "iran": dict(dir="press",
        head_fa="خلاصه <b>روزنامه‌های</b> ایران",
        sub_fa="مرور مهم‌ترین خبرهای امروز در اقتصاد، فناوری، جامعه، صنعت، سلامت و ورزش",
        en1="Iran Daily Press Summary",
        en2="Key headlines from today’s Iranian newspapers<br>in economy, technology, society, industry, health and sports",
        e_head="Iran Daily <b>Press</b> Summary", e_sub="Key headlines from today’s Iranian newspapers",
        e_en1="ECONOMY · TECHNOLOGY · SOCIETY", e_en2="industry, health and sports, reviewed every day at 10:00 Tehran",
        extra="", xcss="", e_xcss=""),
    "world": dict(dir="world",
        head_fa="خلاصه <b>رسانه‌های</b> جهان",
        sub_fa="مرور مهم‌ترین خبرهای امروز دنیا در اقتصاد، صنعت، نوآوری، هوش مصنوعی و تجارت",
        en1="World Daily Press Summary",
        en2="Key stories from today’s global media<br>in economy, industry, innovation, AI and trade",
        e_head="World Daily <b>Press</b> Summary", e_sub="Key stories from today’s global media",
        e_en1="ECONOMY · AI · TRADE", e_en2="industry and innovation, reviewed every day at 16:00 Tehran",
        extra='<div class="abs mast"></div><svg class="abs globe" viewBox="0 0 200 200" fill="none" stroke="#2b2622" stroke-width="2.2"><circle cx="100" cy="100" r="92"/><ellipse cx="100" cy="100" rx="44" ry="92"/><ellipse cx="100" cy="100" rx="78" ry="92"/><path d="M100 8v184M8 100h184M20 55h160M20 145h160"/></svg>', xcss='.mast{left:0;right:0;top:118px;height:385px;backdrop-filter:blur(7px) sepia(.25);-webkit-mask:linear-gradient(180deg,transparent,#000 18%,#000 80%,transparent)}.globe{left:487px;top:180px;width:280px;height:280px;opacity:.55}', e_xcss='.head{font-size:88px}'),
}


def dates(d):
    g = datetime.date.fromisoformat(d)
    jy, jm, jd = g2j(g.year, g.month, g.day)
    fa = f"{FA_WD[g.weekday()]} {jd} {FA_M[jm-1]} {jy}".translate(FA_DIG)
    en = g.strftime("%A, %-d %B %Y")
    return fa, en, f"{jy}/{jm:02d}/{jd:02d}", FA_WD[g.weekday()]


HTML_EN = """<!doctype html><html><head><meta charset="utf-8"><style>%(css)s
.wm{top:58px}.badge{font-family:Brico,sans-serif;font-weight:700;font-size:30px;letter-spacing:.12em;padding-right:122px}
.head{font-family:Play,serif;font-weight:800;font-size:96px;line-height:1.15;direction:ltr;top:500px;letter-spacing:-.01em}
.sub{font-family:PlayI,serif;font-style:italic;direction:ltr;font-size:33px;top:632px}
.en1{font-family:Brico,sans-serif;font-weight:700;font-size:40px;letter-spacing:.16em;top:752px;color:#2b2622}
.en2{top:816px;font-size:30px}
%(xcss)s%(e_xcss)s</style></head><body>%(extra)s
<img class="abs logo" src="%(logo)s">
<div class="abs wm"><div class="en">DITOMAN</div></div>
<div class="abs div"></div>
<div class="abs badge">DAILY REVIEW<svg viewBox="0 0 64 58" fill="none" stroke="#F3ECE0" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"><path d="M12 8h44v38a6 6 0 0 1-6 6H14a6 6 0 0 1-6-6V18h4z"/><path d="M12 8v38"/><path d="M20 18h12v12H20zM38 18h12M38 25h12M20 37h30M20 44h30"/></svg></div>
<div class="abs head">%(e_head)s</div>
<div class="abs sub">%(e_sub)s</div>
<div class="abs rule" style="left:60px;width:536px"></div><div class="abs rule" style="left:672px;width:522px"></div>
<div class="abs en1">%(e_en1)s</div>
<div class="abs en2">%(e_en2)s</div>
<div class="abs date"><span class="g">%(en_date)s</span></div>
<div class="abs foot"><span class="l">DITOMAN | TMN · DITOMAN.COM</span><span class="r">Learn · Connect · Evolve</span></div>
</body></html>"""


def render(d, out_png, en_only=False, kind="iran"):
    from playwright.sync_api import sync_playwright
    fa, en, _, _ = dates(d)
    tpl = HTML_EN if en_only else HTML
    doc = tpl % dict(css=CSS % dict(f=FONTS.as_uri(), bg=BG.as_uri()), logo=LOGO.as_uri(), fa_date=fa, en_date=en, **KINDS[kind])
    tmp = out_png.with_suffix(".html"); tmp.write_text(doc, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1254, "height": 1254})
        pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out_png), full_page=False); b.close()
    tmp.unlink()
    from PIL import Image
    Image.open(out_png).convert("RGB").save(out_png.with_suffix(".webp"), "WEBP", quality=88, method=6)


def main(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    d = data["date"]
    kind = data.get("kind", "world" if "/world/" in str(pathlib.Path(path).resolve()) else "iran")
    od = KINDS[kind]["dir"]
    (ROOT / od).mkdir(exist_ok=True)
    out = ROOT / od / f"{d}-post.png"
    render(d, out, kind=kind)
    render(d, ROOT / od / f"{d}-post-en.png", en_only=True, kind=kind)
    fa, en, jal, wd = dates(d)
    idx_p = ROOT / od / "index.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else []
    idx = [x for x in idx if x["date"] != d]
    idx.append({"date": d, "jalali": jal, "weekday_fa": wd, "post": f"{od}/{d}-post.webp", "post_en": f"{od}/{d}-post-en.webp",
                "lead_fa": data.get("lead_fa", ""), "lead_en": data.get("lead_en", ""),
                "front_fa": data.get("front_fa", ""), "front_en": data.get("front_en", ""), "sections": data["sections"]})
    idx.sort(key=lambda x: x["date"], reverse=True)
    idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out, f"and {od}/index.json", f"({len(idx)} days)")


if __name__ == "__main__":
    main(sys.argv[1])
