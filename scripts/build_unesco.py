"""Build iran-unesco.html: every Iranian property on UNESCO's World Heritage List.

Data:   data/iran/unesco.json
Photos: free-licence Wikimedia Commons images fetched into assets/brand-src/unesco/
        (<id>.N.jpg with <id>.N.txt = title, page, licence, author). PICK below chooses
        which ones to use; each is resized and gets the Ditoman watermark.
Output: iran-unesco.html and iran/tourism/unesco/<id>-<n>.webp

Run from the repo root:  python3 scripts/build_unesco.py
"""
import json, pathlib, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_iran import page, t, e, fa_digits  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "iran" / "unesco.json").read_text(encoding="utf-8"))
SRC = ROOT / "assets" / "brand-src" / "unesco"
OUT = ROOT / "iran" / "tourism" / "unesco"
PICK = json.loads((ROOT / "data" / "iran" / "unesco_pick.json").read_text()) if (ROOT / "data" / "iran" / "unesco_pick.json").exists() else {}
LOGO = Image.open(ROOT / "ditoman-logo.png").convert("RGBA")
FONT = ROOT / "scripts" / "report" / "fonts" / "BricolageGrotesque.ttf"
FA_FONT = ROOT / "fonts" / "iranyekanx" / "IRANYekanXFaNum-Bold.woff2"


def watermark(im):
    """Small Ditoman mark in the bottom corner: logo + DITOMAN | دیتومان."""
    im = im.convert("RGBA")
    w, h = im.size
    s = max(w, h) / 1400
    lg = LOGO.resize((int(46 * s), int(46 * s)), Image.LANCZOS)
    font = ImageFont.truetype(str(FONT), int(22 * s))
    text = "DITOMAN.COM"
    d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=font)
    pad = int(14 * s)
    bw, bh = int(lg.width + tw + pad * 3), int(lg.height + pad)
    x, y = int(22 * s), h - bh - int(22 * s)
    plate = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=(4, 9, 12, 150))
    im.alpha_composite(plate, (x, y))
    im.alpha_composite(lg, (x + pad // 2, y + pad // 2))
    ImageDraw.Draw(im).text((x + pad + lg.width + pad // 2, y + bh / 2), text, font=font, fill=(238, 246, 242, 235), anchor="lm")
    return im.convert("RGB")


def photos(site):
    """Prepared photos for a site: list of (web path, credit text, source page)."""
    out = []
    idx = PICK.get(site["id"], [0, 1, 2, 3])
    for n, i in enumerate(idx):
        src = SRC / f"{site['id']}.{i}.jpg"
        meta = SRC / f"{site['id']}.{i}.txt"
        if not src.exists() or not meta.exists():
            continue
        title, url, lic, author = (meta.read_text(encoding="utf-8").split("\n") + ["", "", "", ""])[:4]
        try:
            im = ImageOps.exif_transpose(Image.open(src))
        except Exception:
            continue
        if im.width < 600:
            continue
        im.thumbnail((1400, 1400))
        OUT.mkdir(parents=True, exist_ok=True)
        dest = OUT / f"{site['id']}-{n}.webp"
        watermark(im).save(dest, "WEBP", quality=80, method=6)
        author = re.sub(r"\s+", " ", author).strip()[:60] or "Wikimedia Commons"
        out.append((f"iran/tourism/unesco/{dest.name}", f"{author} · {lic or 'see source'}", url))
    return out


TYPE = {"c": {"fa": "فرهنگی", "en": "Cultural"}, "n": {"fa": "طبیعی", "en": "Natural"}}

CSS = """
.un-tbl{overflow-x:auto;margin:14px 0}.un-tbl table{width:100%;border-collapse:collapse;font-size:.95rem}.un-tbl th,.un-tbl td{padding:9px 10px;border-bottom:1px solid rgba(127,245,222,.15);text-align:start}.un-tbl th{color:var(--muted);font-weight:600}.un-me td{color:#7ff5de;font-weight:800}.un-note{color:var(--muted);font-size:.9rem;margin:10px 0 18px}html:not([data-lang="en"]) .un-tbl table{direction:rtl}#compare,#tourism{margin-top:34px}
.un-hero { padding: 40px 0 10px; }
.un-hero h1 { font: 400 clamp(2.4rem, 7vw, 4.8rem)/1.2 var(--fa-display); color: #eef6f2; }
body[data-lang="en"] .un-hero h1 { font: 800 clamp(2.2rem, 6vw, 4.2rem)/1.05 var(--en); letter-spacing: -0.03em; }
.un-hero p { max-width: 44em; color: var(--muted); font-size: 1.1rem; line-height: 1.9; margin-top: 14px; }
.un-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 28px 0 10px; }
.un-stats div { border: 1px solid var(--line); border-radius: 18px; padding: 16px; background: rgba(10, 24, 32, 0.6); }
.un-stats b, .un-stats b span { display: block; font-size: 2.1rem; font-weight: 800; color: #f472b6; line-height: 1.3; }
.un-stats span { color: var(--muted); font-size: 0.92rem; }
.un-time { display: flex; align-items: flex-end; gap: 4px; height: 150px; margin: 30px 0 6px; padding: 0 4px; border-bottom: 1px solid var(--line); }
.un-time i { flex: 1; background: linear-gradient(180deg, #f472b6, #9d174d); border-radius: 6px 6px 0 0; min-height: 2px; position: relative; }
.un-time i[data-n="0"] { background: rgba(255, 255, 255, 0.05); }
.un-time i b { position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: 0.75rem; color: #fbcfe8; font-style: normal; }
.un-axis { display: flex; justify-content: space-between; color: var(--muted); font-size: 0.8rem; margin-bottom: 30px; direction: ltr; }
.un-odd { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 14px 0 40px; }
.un-odd a { display: block; border: 1px solid color-mix(in srgb, #f472b6 40%, transparent); border-radius: 18px; padding: 16px 18px; background: rgba(244, 114, 182, 0.06); color: inherit; }
.un-odd b { display: block; font-size: 1.05rem; margin-bottom: 6px; color: #fbcfe8; }
.un-odd span { color: #d6e6e3; line-height: 1.8; font-size: 0.95rem; }
.un-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }
.un-site { border: 1px solid var(--line); border-radius: 22px; overflow: hidden; background: rgba(10, 24, 32, 0.7); scroll-margin-top: 90px; }
.un-main { position: relative; aspect-ratio: 16 / 10; background: #0b1a20; }
.un-main img { width: 100%; height: 100%; object-fit: cover; display: block; }
.un-year { position: absolute; top: 14px; inset-inline-start: 14px; background: rgba(4, 9, 12, 0.78); color: #fff; border-radius: 999px; padding: 4px 12px; font-weight: 800; }
.un-type { position: absolute; top: 14px; inset-inline-end: 14px; border-radius: 999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; background: #f472b6; color: #3b0a24; }
.un-type.n { background: #86efac; color: #052e16; }
.un-body { padding: 16px 20px 18px; }
.un-body h3 { font-size: 1.3rem; font-weight: 800; color: #eef6f2; line-height: 1.5; }
.un-body .un-p { color: #f9a8d4; font-size: 0.9rem; margin: 2px 0 8px; }
.un-body p { color: #d6e6e3; line-height: 1.9; }
.un-thumbs { display: flex; gap: 8px; margin-top: 12px; }
.un-thumbs button { flex: 1; aspect-ratio: 4 / 3; border: 2px solid transparent; border-radius: 10px; overflow: hidden; padding: 0; cursor: pointer; background: none; }
.un-thumbs button[aria-pressed="true"] { border-color: #f472b6; }
.un-thumbs img { width: 100%; height: 100%; object-fit: cover; display: block; }
.un-credit { margin-top: 10px; font: 0.75rem var(--en); color: var(--muted); direction: ltr; text-align: left; }
.un-credit a { color: var(--muted); text-decoration: underline; }
.un-src { margin: 40px 0 10px; color: var(--muted); font-size: 0.92rem; line-height: 1.9; }
.un-src a { color: var(--mint); }
@media (max-width: 900px) { .un-list, .un-odd { grid-template-columns: 1fr; } .un-stats { grid-template-columns: repeat(2, 1fr); } }
"""

JS = """
document.querySelectorAll('.un-site').forEach(function (s) {
  var main = s.querySelector('.un-main img'), credit = s.querySelector('.un-credit');
  s.querySelectorAll('.un-thumbs button').forEach(function (b) {
    b.addEventListener('click', function () {
      main.src = b.getAttribute('data-src');
      credit.innerHTML = b.getAttribute('data-credit');
      s.querySelectorAll('.un-thumbs button').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
    });
  });
});
"""

ODD = [
    ("shahr-e-sukhteh", {"fa": "قدیمی‌ترین چشم مصنوعی", "en": "The oldest artificial eye"},
     {"fa": "در شهر سوخته چشمی مصنوعی از حدود ۴۸۰۰ سال پیش پیدا شده و جامی که نقش بزش، پشت سر هم، حرکت را نشان می‌دهد.",
      "en": "Shahr-e Sukhteh gave us an artificial eye about 4,800 years old, and a bowl whose goat drawings play like an early animation."}),
    ("maymand", {"fa": "روستایی که در دل سنگ زندگی می‌کند", "en": "A village living inside rock"},
     {"fa": "مردم میمند هنوز زمستان را در خانه‌های کنده‌شده در کوه می‌گذرانند.",
      "en": "In Maymand, families still spend the winter in homes carved into the hillside."}),
    ("lut", {"fa": "داغ‌ترین سطح زمین", "en": "The hottest ground on Earth"},
     {"fa": "ماهواره‌ها بالاترین دمای سطح زمین را بارها در بیابان لوت اندازه گرفته‌اند.",
      "en": "Satellites have repeatedly measured the hottest land-surface temperatures on Earth in the Lut Desert."}),
    ("trans-iranian-railway", {"fa": "یک راه‌آهن، میراث جهانی", "en": "A railway on the list"},
     {"fa": "راه‌آهن سراسری، با ۱۳۹۴ کیلومتر ریل از خزر تا خلیج فارس، از معدود راه‌آهن‌های ثبت‌شده در جهان است.",
      "en": "The 1,394 km Trans-Iranian Railway is one of very few railways on the World Heritage List."}),
    ("gonbad-e-qabus", {"fa": "هزار سال آجر روی آجر", "en": "A thousand years of brick"},
     {"fa": "گنبد قابوس با ۵۳ متر ارتفاع از سال ۱۰۰۶ میلادی بدون فرو ریختن ایستاده است.",
      "en": "Gonbad-e Qabus, 53 metres of brick, has stood since 1006 CE."}),
    ("bisotun", {"fa": "کلید خواندن خط میخی", "en": "The key to cuneiform"},
     {"fa": "سنگ‌نوشته‌ی سه‌زبانه‌ی بیستون همان سنگ رُزتای خط میخی است.",
      "en": "Bisotun's trilingual inscription did for cuneiform what the Rosetta Stone did for hieroglyphs."}),
]


def site_card(s, ph):
    main = (f'<img src="{e(ph[0][0])}" alt="{e(s["en"])}" loading="lazy" />' if ph else "")
    credit = (f'Photo: {e(ph[0][1])} · <a href="{e(ph[0][2])}" target="_blank" rel="noopener">Wikimedia Commons</a>' if ph else "")
    thumbs = ""
    if len(ph) > 1:
        thumbs = '<div class="un-thumbs">' + "".join(
            f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-src="{e(p[0])}" '
            f'data-credit="{e("Photo: " + p[1] + " · <a href=\"" + p[2] + "\" target=\"_blank\" rel=\"noopener\">Wikimedia Commons</a>")}">'
            f'<img src="{e(p[0])}" alt="" loading="lazy" /></button>' for i, p in enumerate(ph)) + "</div>"
    year = t({"fa": fa_digits(s["year"]), "en": str(s["year"])})
    return f'''<article class="un-site" id="{e(s["id"])}">
      <div class="un-main">{main}<span class="un-year">{year}</span><span class="un-type {s["type"]}">{t(TYPE[s["type"]])}</span></div>
      <div class="un-body"><h3>{t(s)}</h3><div class="un-p">{t({"fa": s["pfa"], "en": s["pen"]})}</div>
      <p>{t({"fa": s["dfa"], "en": s["den"]})}</p>{thumbs}<div class="un-credit">{credit}</div></div>
    </article>'''


def compare_html():
    c = DATA.get("compare")
    if not c:
        return ""
    rows = ""
    for fa, en, n, pop in c["rows"]:
        per = n / pop * 10
        me = ' class="un-me"' if en == "Iran" else ""
        rows += (f'<tr{me}><td>{t({"fa": fa, "en": en})}</td><td>{t({"fa": fa_digits(n), "en": str(n)})}</td>'
                 f'<td>{t({"fa": fa_digits(f"{pop:.1f}".replace(".", "٫")), "en": f"{pop:,.1f}"})}</td>'
                 f'<td>{t({"fa": fa_digits(f"{per:.1f}".replace(".", "٫")), "en": f"{per:.1f}"})}</td></tr>')
    head = (f'<tr><th>{t({"fa": "کشور", "en": "Country"})}</th><th>{t({"fa": "آثار جهانی", "en": "Sites"})}</th>'
            f'<th>{t({"fa": "جمعیت ۲۰۲۶ (میلیون)", "en": "Population 2026 (m)"})}</th>'
            f'<th>{t({"fa": "اثر به ازای هر ۱۰ میلیون نفر", "en": "Sites per 10m people"})}</th></tr>')
    return f'''
    <h2 id="compare">{t({"fa": "ایران در برابر همسایه‌ها و جهان", "en": "Iran against its neighbours and the world"})}</h2>
    <p>{t({"fa": "ایران با ۳۰ اثر، دهمین کشور جهان در فهرست میراث جهانی است؛ جلوتر از ژاپن و آمریکا (هر کدام ۲۷ اثر) و ترکیه (۲۲ اثر). در منطقه فقط روسیه (۳۳ اثر) از ایران جلوتر است، ولی جمعیتش بیش از یک‌ونیم برابر ایران است. اگر تعداد آثار را بر جمعیت تقسیم کنیم، ایران با حدود ۳٫۲ اثر به ازای هر ۱۰ میلیون نفر، از ترکیه (۲٫۵)، روسیه (۲٫۳)، عربستان (۲٫۳) و عراق (۱٫۳) بالاتر است. کشورهای کوچک مثل ارمنستان و عمان در این شاخص بالا می‌آیند، چون جمعیتشان کم است.", "en": "With 30 sites Iran ranks 10th in the world, ahead of Japan and the United States (27 each) and Turkey (22). In the region only Russia (33) is ahead, with more than one and a half times Iran's population. Per 10 million people Iran has about 3.2 sites, more than Turkey (2.5), Russia (2.3), Saudi Arabia (2.3) and Iraq (1.3). Small countries such as Armenia and Oman score high on this measure because their populations are small."})}</p>
    <div class="un-tbl"><table>{head}{rows}</table></div>
    <p class="un-note">{t({"fa": "تعداد آثار پس از اجلاس ۲۰۲۶ بوسان (StatRanker، اکتبر ۲۰۲۶)؛ جمعیت برآورد سازمان ملل برای ۲۰۲۶. آثار مشترک بین چند کشور برای هر کشور یک بار شمرده می‌شوند.", "en": "Site counts after the 2026 Busan session (StatRanker, Oct 2026); population is the UN estimate for 2026. Sites shared between countries count once for each."})}</p>
    <h2 id="tourism">{t({"fa": "از میراث تا ارز: فرصت گردشگری", "en": "From heritage to hard currency: the tourism opportunity"})}</h2>
    <p>{t({"fa": "ایران در سال ۱۴۰۳ حدود ۷٫۴ میلیون ورود اتباع خارجی و حدود ۷٫۴ میلیارد دلار درآمد گردشگری اعلام کرد (این عدد همه‌ی ورودهای مرزی، از جمله زائران را می‌شمارد). ترکیه با ۲۲ اثر جهانی، در ۲۰۲۵ حدود ۵۲٫۸ میلیون گردشگر خارجی و ۶۵٫۲ میلیارد دلار درآمد داشت؛ نزدیک ۹ برابر ایران. یعنی ایران آثار بیشتری دارد، اما هنوز سهم کوچکی از درآمد گردشگری منطقه را می‌گیرد. هدف برنامه‌ی هفتم توسعه، رسیدن به ۱۵ میلیون گردشگر خارجی است. اگر درها بازتر شود و پرواز، ویزا، پرداخت بین‌المللی و هتل‌ها آماده باشند، همین ۳۰ اثر می‌توانند یکی از بزرگ‌ترین منابع ارزی و اشتغال کشور شوند.", "en": "In the Iranian year to March 2025, Iran reported about 7.4 million foreign arrivals and about $7.4 billion in tourism revenue (border entries, including pilgrims). Turkey, with 22 World Heritage Sites, had about 52.8 million foreign visitors and $65.2 billion in tourism income in 2025, nearly nine times Iran's. Iran has more sites but still earns a small share of the region's tourism income. The Seventh Development Plan targets 15 million foreign visitors. If the doors open wider and flights, visas, international payments and hotels are ready, these 30 sites could become one of the country's largest sources of foreign currency and jobs."})}</p>
    <p class="un-note">{t({"fa": "آیا ثبت جهانی خودبه‌خود گردشگر می‌آورد؟ نه همیشه. یک فراتحلیل ۴۳ مطالعه (Annals of Tourism Research، ۲۰۱۹) اثر میانگین معناداری پیدا نکرد، اما پژوهش‌هایی درباره‌ی کشورهای در حال توسعه و چین اثر مثبت دیده‌اند. ثبت جهانی در را باز می‌کند؛ زیرساخت، تبلیغ و دسترسی است که گردشگر را می‌آورد.", "en": "Does a listing bring tourists by itself? Not always. A meta-analysis of 43 studies (Annals of Tourism Research, 2019) found no significant average effect, while studies of developing countries and China found positive effects. Listing opens the door; infrastructure, promotion and access bring the visitors."})}</p>
'''


def main():
    sites = sorted(DATA["sites"], key=lambda s: (s["year"], s["en"]))
    cards, n_photos = [], 0
    for s in sites:
        ph = photos(s)
        n_photos += len(ph)
        cards.append(site_card(s, ph))
    years = list(range(1979, 2027))
    count = {y: sum(1 for s in sites if s["year"] == y) for y in years}
    bars = "".join(f'<i data-n="{count[y]}" style="height:{count[y] * 40}px" title="{y}: {count[y]}">'
                   + (f"<b>{count[y]}</b>" if count[y] else "") + "</i>" for y in years)
    nat = sum(1 for s in sites if s["type"] == "n")
    stats = [
        ({"fa": fa_digits(len(sites)), "en": str(len(sites))}, {"fa": "اثر ثبت‌شده", "en": "inscribed sites"}),
        ({"fa": f"{fa_digits(len(sites) - nat)} + {fa_digits(nat)}", "en": f"{len(sites) - nat} + {nat}"}, {"fa": "فرهنگی + طبیعی", "en": "cultural + natural"}),
        ({"fa": "۱۹۷۹", "en": "1979"}, {"fa": "نخستین ثبت، سه اثر", "en": "first listing, three sites"}),
        ({"fa": fa_digits(DATA["tentative"]), "en": str(DATA["tentative"])}, {"fa": "اثر در فهرست انتظار", "en": "on the tentative list"}),
    ]
    stats_html = "".join(f"<div><b>{t(a)}</b><span>{t(b)}</span></div>" for a, b in stats)
    odd = "".join(f'<a href="#{i}"><b>{t(h)}</b><span>{t(x)}</span></a>' for i, h, x in ODD)
    src = " · ".join(f'<a href="{e(x["u"])}" target="_blank" rel="noopener">{e(x["t"])}</a>' for x in DATA["sources"])
    body = f'''  <main class="wrap">
    <section class="un-hero">
      <p style="margin:0"><a href="iran-tourism.html">{t({"fa": "ایران چه دارد › گردشگری و فرهنگ", "en": "What Iran Has › Tourism & culture"})}</a></p>
      <h1>{t({"fa": "۳۰ اثر ایران در فهرست میراث جهانی یونسکو", "en": "Iran's 30 UNESCO World Heritage Sites"})}</h1>
      <p>{t({"fa": "از تخت جمشید در ۱۹۷۹ تا قلعه‌ی الموت در ۲۰۲۶؛ همه‌ی آثار ایران در فهرست میراث جهانی، به ترتیب سال ثبت، با عکس و خلاصه‌ای کوتاه. چند تا از آن‌ها را حتی بسیاری از خود ما هم نمی‌شناسیم.", "en": "From Persepolis in 1979 to Alamut in 2026: every Iranian site on the World Heritage List, in order of inscription, with photos and a short note. Some of them are little known even inside Iran."})}</p>
      <div class="un-stats">{stats_html}</div>
      <div class="un-time" aria-label="Inscriptions per year">{bars}</div>
      <div class="un-axis"><span>1979</span><span>2003</span><span>2015</span><span>2026</span></div>
      <p style="margin-top:0">{t({"fa": "بعد از سه ثبت سال ۱۹۷۹، ایران ۲۴ سال اثری به فهرست اضافه نکرد. از ۲۰۰۳ به بعد تقریباً هر سال یک اثر تازه ثبت شده است.", "en": "After the first three in 1979, Iran added nothing for 24 years. Since 2003 a new site has been inscribed almost every year."})}</p>
    </section>
    <h2 style="margin-top:30px">{t({"fa": "شگفت‌انگیزهایی که کمتر کسی می‌داند", "en": "Surprises few people know"})}</h2>
    <div class="un-odd">{odd}</div>
{compare_html()}
    <h2>{t({"fa": "همه‌ی آثار، به ترتیب سال ثبت", "en": "Every site, by year of inscription"})}</h2>
    <div class="un-list" style="margin-top:16px">{"".join(cards)}</div>
    <p class="un-src">{t({"fa": "منابع:", "en": "Sources:"})} {src}<br>{t({"fa": "عکس‌ها از ویکی‌مدیا کامنز با مجوز آزاد؛ نام عکاس و مجوز زیر هر عکس آمده است.", "en": "Photos from Wikimedia Commons under free licences; photographer and licence are under each photo."})}</p>
  </main>
  <script>{JS}</script>'''
    html = page("Iran's UNESCO World Heritage Sites | آثار جهانی ایران | Ditoman",
                "All 30 Iranian sites on UNESCO's World Heritage List, from Persepolis (1979) to Alamut (2026), with photos.",
                "iran-unesco.html", body, CSS)
    (ROOT / "iran-unesco.html").write_text(html, encoding="utf-8")
    print(len(sites), "sites,", n_photos, "photos")


if __name__ == "__main__":
    main()
    import lang_unify
    lang_unify.main()
