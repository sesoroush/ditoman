"""Ditoman daily market report — renders the story card (1080x1920) and Telegram caption from market/latest.json.

Design is fixed here; each day only the data changes."""
import base64, json, sys, datetime, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FONTS = HERE / "fonts"
sys.path.insert(0, str(HERE))
from jalali import g2j

FA_MONTHS = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
FA_DAYS = ["دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه","شنبه","یکشنبه"]
FA_DIG = str.maketrans("0123456789.", "۰۱۲۳۴۵۶۷۸۹٫")
THEMES = {
  "dark": dict(bg="#0c0b0a", paper="#141210", ink="#f2ebe0", muted="#a39b8f", rule="rgba(242,235,224,.18)",
               accent="#d6262f", up="#2fbfa3", down="#e2434b", glow="radial-gradient(1100px 800px at 85% -5%, rgba(214,38,47,.16), transparent 60%), radial-gradient(900px 700px at 0% 105%, rgba(47,191,163,.10), transparent 60%)"),
  "ft":   dict(bg="#fff1e5", paper="#f2dfce", ink="#0d0c0b", muted="#3d3834", rule="rgba(13,12,11,.28)",
               accent="#8a0a35", up="#05636b", down="#b30000", glow="none"),
}

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def fmt(v, dp): return f"{v:,.{dp}f}"

def chg(pct, fa=False):
    if pct is None: return '<span class="chg flat">—</span>'
    cls = "up" if pct > 0 else "down" if pct < 0 else "flat"
    arrow = "▲" if pct > 0 else "▼" if pct < 0 else "•"
    n = f"{abs(pct):.2f}"
    return f'<span class="chg {cls}" dir="ltr">{arrow} {n.translate(FA_DIG) + "٪" if fa else n + "%"}</span>'

def render(data, out_png, theme="ft", sample=False):
    T = THEMES[theme]
    d = datetime.date.fromisoformat(data["date"])
    jy, jm, jd = g2j(d.year, d.month, d.day)
    fa_date = f'{FA_DAYS[d.weekday()]} {str(jd).translate(FA_DIG)} {FA_MONTHS[jm-1]} {str(jy).translate(FA_DIG)}'
    en_date = d.strftime("%A %d %B %Y").upper()
    j_doy = (jm-1)*31 + jd if jm <= 6 else 186 + (jm-7)*30 + jd
    g_doy = d.timetuple().tm_yday
    g_len = 366 if (d.year%4==0 and (d.year%100!=0 or d.year%400==0)) else 365
    j_len = 365  # Persian year length; 366 only in leap years
    doy_fa = f"روز {str(j_doy).translate(FA_DIG)} از {str(j_len).translate(FA_DIG)} روز سال {str(jy).translate(FA_DIG)}"
    doy_en = f"DAY {g_doy} OF {g_len}"
    doy_both = f"روز {str(j_doy).translate(FA_DIG)} سال {str(jy).translate(FA_DIG)} • روز {str(g_doy).translate(FA_DIG)} سال {str(d.year).translate(FA_DIG)}"

    def rows(items, fa_digits=False):
        h = []
        for it in items:
            v = fmt(it["value"], it.get("dp", 2))
            if fa_digits: v = v.translate(FA_DIG)
            pre = f'<span class="cur">{it["unit_pre"]}</span>' if it.get("unit_pre") else ""
            h.append(f'''<div class="row">
  <div class="nm"><span class="fa">{it["fa"]}</span><span class="en">{it["en"]}</span></div>
  <div class="vl" dir="ltr">{pre}{v}</div>
  {chg(it.get("chg"), fa_digits)}
</div>''')
        return "".join(h)

    fx = "".join(f'''<div class="fx"><span class="pair" dir="ltr">{it["en"]}</span>
  <span class="fxv" dir="ltr">{fmt(it["value"], it.get("dp", 4))}</span>{chg(it.get("chg"))}</div>''' for it in data["forex"])

    font = lambda f: b64(FONTS / f)
    css = f'''
@font-face {{ font-family: Vz; src: url(data:font/woff2;base64,{font("Vazirmatn-Regular.woff2")}); font-weight:400; }}
@font-face {{ font-family: Vz; src: url(data:font/woff2;base64,{font("Vazirmatn-Medium.woff2")}); font-weight:500; }}
@font-face {{ font-family: Vz; src: url(data:font/woff2;base64,{font("Vazirmatn-Bold.woff2")}); font-weight:700; }}
@font-face {{ font-family: Vz; src: url(data:font/woff2;base64,{font("Vazirmatn-ExtraBold.woff2")}); font-weight:800; }}
@font-face {{ font-family: Br; src: url(data:font/ttf;base64,{font("BricolageGrotesque.ttf")}); font-weight:200 800; }}
@font-face {{ font-family: Pf; src: url(data:font/ttf;base64,{font("PlayfairDisplay.ttf")}); font-weight:400 900; }}
@font-face {{ font-family: Pf; src: url(data:font/ttf;base64,{font("PlayfairDisplay-Italic.ttf")}); font-weight:400 900; font-style:italic; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1920px; overflow:hidden; background:{T["bg"]}; color:{T["ink"]}; font-family: Vz, Br, sans-serif; position:relative; }}
body::before {{ content:""; position:absolute; inset:0; background:{T["glow"]}; }}
.page {{ position:relative; direction:rtl; padding:84px 60px 0; }}
.caps {{ font-family:Br; font-weight:800; letter-spacing:.3em; text-transform:uppercase; font-size:18px; color:{T["muted"]}; }}
.mast {{ display:flex; justify-content:space-between; align-items:center; }}
.brand {{ display:flex; align-items:center; gap:16px; direction:ltr; }}
.brand img {{ width:58px; height:58px; border-radius:50%; }}
.brand b {{ font-family:Pf; font-weight:600; font-size:34px; letter-spacing:.34em; }}
.tag {{ font-family:Br; font-weight:800; font-size:16px; letter-spacing:.24em; color:#fff; background:{T["accent"]}; padding:8px 14px; }}
.rule2 {{ margin-top:26px; border-top:1px solid {T["ink"]}; border-bottom:1px solid {T["rule"]}; height:6px; opacity:.85; }}
.dateline {{ display:flex; justify-content:space-between; align-items:center; padding:14px 0 0; }}
.dateline .fa {{ font-weight:700; font-size:24px; color:{T["muted"]}; }}
.dateline .en {{ direction:ltr; font-family:Br; font-weight:800; font-size:16px; letter-spacing:.2em; color:{T["muted"]}; font-size:18px; }}
.kicker {{ display:none; }}
.dateline {{ align-items:flex-start; }}
.dl {{ display:flex; flex-direction:column; align-items:flex-end; gap:4px; }}
.dl .en {{ direction:ltr; font-family:Br; font-weight:800; font-size:18px; letter-spacing:.2em; color:{T["muted"]}; }}
.dl .doy {{ font-weight:800; font-size:22px; color:{T["accent"]}; }}
.dateline.doy .fa {{ color:{T["accent"]}; font-size:22px; }}
.dateline.doy .en {{ color:{T["accent"]}; font-size:15px; }}
h1 {{ direction:ltr; text-align:left; font-family:Pf; font-weight:700; font-size:72px; line-height:.96; margin-top:26px; letter-spacing:-.02em; margin-top:10px; }}
h1 i {{ color:{T["accent"]}; font-weight:700; }}
  .h1fa {{ font-weight:800; font-size:40px; margin-top:-46px; }}
.h1fa span {{ color:{T["accent"]}; }}
.time {{ display:inline-block; margin-top:14px; font-weight:500; font-size:22px; color:{T["muted"]}; }}
.sec {{ margin-top:22px; }}
.sh {{ display:flex; justify-content:space-between; align-items:baseline; padding-bottom:12px; border-bottom:2px solid {T["ink"]}; }}
.sh .fa {{ font-weight:800; font-size:31px; color:{T["accent"]}; }}
.sh .en.caps {{ color:{T["accent"]}; }}
.sh .fa::before {{ content:""; display:inline-block; width:26px; height:4px; background:{T["accent"]}; margin-left:14px; vertical-align:middle; }}
.sh .en {{ direction:ltr; }}
.row {{ display:grid; grid-template-columns: 330px 1fr 158px; align-items:center; gap:24px; padding:5px 18px; border-radius:12px; }}
.sec .row:nth-of-type(even) {{ background:rgba(138,10,53,.07); }}
.sh + .row {{ margin-top:6px; }}
.nm {{ display:flex; flex-direction:column; }}
.nm .fa {{ font-weight:800; font-size:31px; line-height:1.3; }}
.nm .en {{ direction:ltr; text-align:right; font-family:Br; font-weight:800; font-size:15px; letter-spacing:.18em; text-transform:uppercase; color:{T["muted"]}; }}
.vl {{ display:flex; align-items:baseline; gap:6px; font-family:Pf; font-weight:900; font-size:45px; letter-spacing:-.01em; font-variant-numeric:lining-nums tabular-nums; }}
.vl .cur {{ font-family:Pf; font-size:1em; color:{T["ink"]}; font-weight:900; }}
.row .vl {{ justify-content:flex-end; padding-left:8px; }}
.chg {{ justify-self:end; font-family:Br; font-weight:800; font-size:24px; font-variant-numeric:tabular-nums; white-space:nowrap; }}
.row .chg {{ justify-self:start; padding:6px 14px; border-radius:999px; min-width:140px; text-align:center; }}
.row .chg.up {{ background:rgba(5,99,107,.12); }} .row .chg.down {{ background:rgba(179,0,0,.10); }} .row .chg.flat {{ background:rgba(13,12,11,.06); }}
.chg.up {{ color:{T["up"]}; }} .chg.down {{ color:{T["down"]}; }} .chg.flat {{ color:{T["muted"]}; }}
.fxg {{ direction:ltr; display:grid; grid-template-columns:repeat(3,1fr); }}
.fx {{ direction:ltr; display:flex; flex-direction:column; gap:2px; padding:9px 18px 8px; border-bottom:1px solid {T["rule"]}; border-left:1px solid {T["rule"]}; }}
.fx:nth-child(3n+1) {{ border-left:0; padding-left:0; }}
.fx:nth-last-child(-n+3) {{ border-bottom:0; }}
.pair {{ font-family:Br; font-weight:800; font-size:16px; letter-spacing:.2em; color:{T["muted"]}; }}
.fxv {{ font-family:Pf; font-weight:900; font-size:42px; line-height:1.1; font-variant-numeric:lining-nums tabular-nums; }}
.fx .chg {{ justify-self:auto; font-size:20px; }}
.foot {{ position:absolute; left:60px; right:60px; bottom:54px; direction:ltr; }}
.foot .r {{ border-top:1px solid {T["rule"]}; padding-top:16px; display:flex; justify-content:space-between; align-items:baseline; }}
.foot .r .caps {{ font-size:16px; letter-spacing:.26em; color:{T["ink"]}; }}
.foot .r em {{ font-family:Pf; font-style:italic; font-size:25px; color:{T["muted"]}; }}
.src {{ margin-top:10px; font-family:Br; font-size:15px; color:{T["muted"]}; opacity:.85; }}
.sample {{ position:absolute; top:60px; left:50%; transform:translateX(-50%); background:#ffcc4d; color:#1a1300; font:800 20px Vz; padding:8px 20px; border-radius:999px; }}
'''
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
{'<div class="sample">SAMPLE · نمونه</div>' if sample else ''}
<div class="page">
  <div class="mast">
    <div class="tag" dir="ltr">MARKETS · {data.get("edition","DAILY")}</div>
    <div class="brand"><img src="data:image/png;base64,{b64(ROOT/"ditoman-logo.png")}"><b>DITOMAN</b></div>
  </div>
  <div class="rule2"></div>
  <div class="dateline"><span class="fa">{fa_date} · {data["time_fa"]}</span>
    <span class="dl"><span class="en">{en_date}</span><span class="doy">{doy_both}</span></span></div>

  <div class="kicker caps" dir="ltr" style="text-align:left">The Daily Markets Report</div>
  <h1>Markets <i>Tonight.</i></h1>
  <div class="h1fa">بازارها، <span>امشب.</span></div>

  <div class="sec">
    <div class="sh"><span class="fa">ایران · به تومان</span><span class="en caps">Iran · Toman</span></div>
    {rows(data["iran"], fa_digits=True)}
  </div>
  <div class="sec">
    <div class="sh"><span class="fa">بین‌الملل · به دلار</span><span class="en caps">Global · USD</span></div>
    {rows(data["global"])}
  </div>
  <div class="sec">
    <div class="sh"><span class="fa">کالاهای غذایی · دلار در تن</span><span class="en caps">Food · USD per tonne</span></div>
    {rows(data["food"])}
  </div>
  <div class="sec">
    <div class="sh"><span class="fa">فارکس</span><span class="en caps">Forex</span></div>
    <div class="fxg">{fx}</div>
  </div>
</div>
<div class="foot">
  <div class="r"><span class="caps">Ditoman / People · Ideas · A Fairer Tomorrow</span><em>ditoman.com · t.me/Ditoman_tm</em></div>
  <div class="src">{data["sources"]}</div>
</div>
</body></html>'''
    html_path = ROOT / "market" / ".card.html"; html_path.write_text(html, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
        pg.goto(html_path.as_uri()); pg.wait_for_timeout(400)
        over = pg.evaluate('''()=>{const s=[...document.querySelectorAll('.sec')].pop().getBoundingClientRect();const f=document.querySelector('.foot').getBoundingClientRect();return [Math.round(s.bottom),Math.round(f.top)]}''')
        pg.screenshot(path=str(out_png)); b.close()
    return over

def from_latest(path):
    L = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    g, f, i = L["global"], L["forex"], L["iran"]
    nz = lambda x: x.get("chg_hist") if x.get("chg_hist") is not None else (None if x.get("chg") in (None, 0, 0.0) else x["chg"])
    return {
      "date": L["fetched_utc"][:10], "time_fa": "۲۱:۰۰ تهران",
      "global": [
        {"en":"Bitcoin","fa":"بیت‌کوین","value":g["btc"]["value"],"dp":0,"unit_pre":"$","chg":g["btc"]["chg"]},
        {"en":"Gold · per ounce","fa":"طلا · هر اونس","value":g["gold"]["value"],"dp":2,"unit_pre":"$","chg":g["gold"]["chg"]},
        {"en":"Brent crude","fa":"نفت برنت","value":g["brent"]["value"],"dp":2,"unit_pre":"$","chg":g["brent"]["chg"]},
        {"en":"Natural gas","fa":"گاز طبیعی","value":g["natgas"]["value"],"dp":3,"unit_pre":"$","chg":g["natgas"]["chg"]}],
      "iran": [
        {"en":"US dollar · open market","fa":"دلار آزاد","value":i["usd"]["value_toman"],"dp":0,"chg":nz(i["usd"])},
        {"en":"Euro","fa":"یورو","value":i["eur"]["value_toman"],"dp":0,"chg":nz(i["eur"])},
        {"en":"UAE dirham","fa":"درهم امارات","value":i["aed"]["value_toman"],"dp":0,"chg":nz(i["aed"])},
        {"en":"18k gold · per gram","fa":"طلای ۱۸ عیار · گرمی","value":i["gold18_gram"]["value_toman"],"dp":0,"chg":nz(i["gold18_gram"])},
        {"en":"Emami gold coin","fa":"سکه امامی","value":i["coin_emami"]["value_toman"],"dp":0,"chg":nz(i["coin_emami"])}],
      "food": [
        {"en":"Wheat · CBOT","fa":"گندم","value":g["wheat"]["value"]/100/0.0272155,"dp":1,"unit_pre":"$","chg":g["wheat"]["chg"]},
        {"en":"Corn · CBOT","fa":"ذرت","value":g["corn"]["value"]/100/0.0254012,"dp":1,"unit_pre":"$","chg":g["corn"]["chg"]},
        {"en":"Soybeans · CBOT","fa":"سویا","value":g["soybeans"]["value"]/100/0.0272155,"dp":1,"unit_pre":"$","chg":g["soybeans"]["chg"]}],
      "forex": [{"en":k,"value":v["value"],"dp":2 if k in ("USD/JPY","USD/TRY") else 4,"chg":v["chg"]} for k,v in f.items()],
      "sources": "Sources: Yahoo Finance (global, CBOT grains, forex) · TGJU (Iran open market) · " + L["fetched_utc"][:16].replace("T"," ") + " UTC",
    }


FA_NUM = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

def tehran_now(utc_iso):
    t = datetime.datetime.fromisoformat(utc_iso) + datetime.timedelta(hours=3, minutes=30)  # Iran has no DST since 2022
    return t

def caption(data, L):
    d = datetime.date.fromisoformat(data["date"])
    jy, jm, jd = g2j(d.year, d.month, d.day)
    fa_date = f'{FA_DAYS[d.weekday()]} {str(jd).translate(FA_NUM)} {FA_MONTHS[jm-1]} {str(jy).translate(FA_NUM)}'
    i = {x["fa"]: x for x in data["iran"]}; g = {x["fa"]: x for x in data["global"]}
    def ch(x):
        c = x.get("chg")
        if c is None: return ""
        return f' ({"▲" if c > 0 else "▼"}{abs(c):.2f}٪)'.translate(FA_NUM)
    def toman(x): return f'{x["value"]:,.0f}'.translate(FA_NUM)
    lines = [
        "📊 گزارش روزانه‌ی بازار | دیتومان",
        fa_date,
        "",
        f'💵 دلار آزاد: {toman(i["دلار آزاد"])} تومان{ch(i["دلار آزاد"])}',
        f'🟡 طلای ۱۸ عیار (گرمی): {toman(i["طلای ۱۸ عیار · گرمی"])} تومان{ch(i["طلای ۱۸ عیار · گرمی"])}',
        f'🪙 سکه امامی: {toman(i["سکه امامی"])} تومان{ch(i["سکه امامی"])}',
        f'₿ بیت‌کوین: ${g["بیت‌کوین"]["value"]:,.0f}{ch(g["بیت‌کوین"])}',
        f'🛢 نفت برنت: ${g["نفت برنت"]["value"]:,.2f}{ch(g["نفت برنت"])}',
        "",
        "Daily Market Report: Iran, global, food and forex.",
        "ditoman.com",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    L = json.loads((ROOT / "market" / "latest.json").read_text(encoding="utf-8"))
    data = from_latest(ROOT / "market" / "latest.json")
    t = tehran_now(L["fetched_utc"])
    day = t.date() - datetime.timedelta(days=1) if t.hour < 4 else t.date()   # after midnight still counts as "tonight"
    data["date"] = day.isoformat()
    data["time_fa"] = f"{t:%H:%M}".translate(FA_NUM) + " تهران"
    out = ROOT / "market" / "reports" / f"{day.isoformat()}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fit = render(data, out, theme="ft")
    if fit[0] > fit[1]:
        print(f"WARNING: content overlaps footer {fit}", file=sys.stderr)
    (ROOT / "market" / "caption.txt").write_text(caption(data, L), encoding="utf-8")
    hist = ROOT / "market" / "history" / f"{day.isoformat()}.json"
    hist.parent.mkdir(parents=True, exist_ok=True)
    hist.write_text(json.dumps(L, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
