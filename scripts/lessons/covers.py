#!/usr/bin/env python3
"""Bilingual cover images for the lessons built by scripts/lessons/build.py.

Cream editorial card in the Ditoman style (same family as the lesson 11 cover): logo and
wordmark, lesson badge, English and Persian titles at the same weight, a flat vector
illustration drawn here (not a photo), and the black footer bar.
Output: lessonNN-cover.jpg, 1254 x 1254. The English-only cover is made by scripts/en_covers.py.

Run from the repo root: python3 scripts/lessons/covers.py [lesson12 ...]
"""
import html
import importlib.util
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = Path(__file__).resolve().parent / "data"
FONTS = ROOT / "scripts" / "report" / "fonts"
YEKAN = ROOT / "fonts" / "iranyekanx"
LOGO = ROOT / "tmn-logo-512.png"
SIZE = 1254

INK, TEAL, MINT, YELLOW, SAFFRON, CREAM, WHITE = "#101F22", "#0F7C74", "#57D9C7", "#FFAD00", "#F2A01F", "#F4EFE4", "#FFFDF8"


# ---- drawing helpers (all coordinates in a 480 x 480 box) ----
def coin(x, y, r, sym="$", fill=YELLOW, ink=INK):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{ink}" stroke-width="5"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * .72:.0f}" fill="none" stroke="{ink}" stroke-width="3" opacity=".45"/>'
            f'<text x="{x}" y="{y + r * .36:.0f}" font-family="Bricolage" font-weight="800" font-size="{r:.0f}" text-anchor="middle" fill="{ink}">{sym}</text>')


def note(x, y, w, h, fill=MINT, rot=0):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{h * .26:.0f}" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x + 14}" y="{y + 12}" width="22" height="10" rx="3" fill="{INK}" opacity=".5"/>'
            f'<rect x="{x + w - 36}" y="{y + h - 22}" width="22" height="10" rx="3" fill="{INK}" opacity=".5"/></g>')


def card(x, y, w, h, fill=INK, rot=0):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x + 22}" y="{y + 30}" width="{w * .2:.0f}" height="{h * .22:.0f}" rx="6" fill="{YELLOW}"/>'
            f'<rect x="{x + 22}" y="{y + h - 46}" width="{w * .55:.0f}" height="10" rx="5" fill="{MINT}"/>'
            f'<rect x="{x + 22}" y="{y + h - 26}" width="{w * .32:.0f}" height="8" rx="4" fill="{MINT}" opacity=".6"/></g>')


def phone(x, y, w, h, inner=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{INK}"/>'
            f'<rect x="{x + 10}" y="{y + 12}" width="{w - 20}" height="{h - 24}" rx="18" fill="{WHITE}"/>'
            f'<rect x="{x + w / 2 - 22}" y="{y + 18}" width="44" height="8" rx="4" fill="{INK}"/>' + inner)


def bank(x, y, s=1.0, fill=WHITE):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 70 L100 10 L200 70 Z" fill="{fill}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + "".join(f'<rect x="{24 + i * 44}" y="82" width="22" height="78" fill="{MINT}" stroke="{INK}" stroke-width="5"/>' for i in range(4))
            + f'<rect x="0" y="164" width="200" height="22" rx="4" fill="{fill}" stroke="{INK}" stroke-width="6"/><circle cx="100" cy="48" r="10" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/></g>')


def globe(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MINT}" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r * .45:.0f}" ry="{r}" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{x - r} {y} H{x + r} M{x - r * .86:.0f} {y - r * .5:.0f} H{x + r * .86:.0f} M{x - r * .86:.0f} {y + r * .5:.0f} H{x + r * .86:.0f}" stroke="{INK}" stroke-width="4" fill="none"/>')


def lock(x, y, s=1.0, fill=YELLOW):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M26 60 V40 a34 34 0 0 1 68 0 V60" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
            f'<rect x="0" y="58" width="120" height="96" rx="18" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="60" cy="98" r="12" fill="{INK}"/><rect x="54" y="100" width="12" height="30" rx="5" fill="{INK}"/></g>')


def shield(x, y, s=1.0, fill=MINT, mark="check"):
    m = ('<path d="M34 78 L58 102 L98 54" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>' % INK
         if mark == "check" else
         '<path d="M66 44 V92" stroke="%s" stroke-width="14" stroke-linecap="round"/><circle cx="66" cy="118" r="9" fill="%s"/>' % (INK, INK))
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M66 0 L132 24 V80 C132 124 104 152 66 168 C28 152 0 124 0 80 V24 Z" fill="{fill}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>{m}</g>')


def key(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><circle cx="40" cy="40" r="34" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/><circle cx="40" cy="40" r="12" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M72 40 H190 V66 M150 40 V60" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>')


def arrow(d, color=INK, w=10):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#ah-{color[1:]})"/>'


def chart(points, color=TEAL, w=10):
    return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def goldbar(x, y, w=170):
    h = w * .42
    return (f'<path d="M{x + w * .16:.0f} {y} H{x + w * .84:.0f} L{x + w} {y + h:.0f} H{x} Z" fill="{YELLOW}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{x + w * .3:.0f} {y + h * .3:.0f} H{x + w * .7:.0f}" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".5"/>')


def basket(x, y, s=1.0, fill=WHITE):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M20 50 L60 0 M140 50 L100 0" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/>'
            f'<path d="M0 50 H160 L140 140 H20 Z" fill="{fill}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M50 74 V118 M80 74 V118 M110 74 V118" stroke="{TEAL}" stroke-width="7" stroke-linecap="round"/></g>')


def bot(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M90 0 V26" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="90" cy="0" r="10" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="0" y="26" width="180" height="130" rx="34" fill="{MINT}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="58" cy="84" r="16" fill="{INK}"/><circle cx="122" cy="84" r="16" fill="{INK}"/><circle cx="63" cy="79" r="5" fill="{WHITE}"/><circle cx="127" cy="79" r="5" fill="{WHITE}"/>'
            f'<path d="M62 122 Q90 138 118 122" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<rect x="-18" y="70" width="18" height="44" rx="8" fill="{INK}"/><rect x="180" y="70" width="18" height="44" rx="8" fill="{INK}"/></g>')


def calendar(x, y, s=1.0):
    cells = "".join(f'<rect x="{18 + c * 36}" y="{62 + r * 30}" width="24" height="18" rx="4" fill="{(YELLOW if (r, c) in ((0, 1), (1, 1), (2, 1), (0, 3)) else INK)}" opacity="{1 if (r, c) in ((0, 1), (1, 1), (2, 1), (0, 3)) else .18}"/>'
                    for r in range(3) for c in range(4))
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="0" y="14" width="180" height="150" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M0 46 H180" stroke="{INK}" stroke-width="6"/><rect x="0" y="14" width="180" height="32" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M44 0 V28 M136 0 V28" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>{cells}</g>')


def chain(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">' + "".join(
        f'<rect x="{i * 96}" y="0" width="74" height="74" rx="16" fill="{(MINT, WHITE, MINT)[i]}" stroke="{INK}" stroke-width="6"/>' for i in range(3))
        + f'<path d="M74 37 H96 M170 37 H192" stroke="{INK}" stroke-width="8" stroke-linecap="round"/></g>')


def tag(x, y, text, fill=INK, color=WHITE, size=26):
    w = 26 + len(text) * size * .58
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 22}" rx="{(size + 22) / 2:.0f}" fill="{fill}"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + size + 4}" font-family="Bricolage" font-weight="800" font-size="{size}" text-anchor="middle" fill="{color}">{text}</text>')


ART = {
    # inflation: the same note, a shrinking basket, a rising price line
    "lesson12": lambda: basket(20, 70, 1.25) + basket(210, 150, .85) + basket(350, 215, .5)
    + note(40, 320, 190, 100, MINT, -6) + chart("250,420 310,380 360,395 440,300", SAFFRON, 12)
    + arrow("M410 330 L446 292", SAFFRON, 12),
    # custody: bank, phone wallet, key
    "lesson13": lambda: bank(20, 60, 1.0) + phone(270, 110, 170, 300,
        coin(355, 215, 44, "₿") + f'<rect x="298" y="290" width="114" height="16" rx="8" fill="{MINT}"/><rect x="298" y="320" width="80" height="12" rx="6" fill="{INK}" opacity=".25"/>')
    + key(40, 330, 1.0, 0),
    # card payment: card, reader, messages
    "lesson14": lambda: phone(250, 60, 190, 330,
        f'<rect x="280" y="110" width="130" height="70" rx="12" fill="{MINT}"/><text x="345" y="158" font-family="Bricolage" font-weight="800" font-size="40" text-anchor="middle" fill="{INK}">OK</text>'
        + "".join(f'<circle cx="{300 + c * 45}" cy="{225 + r * 45}" r="14" fill="{INK}" opacity=".2"/>' for r in range(3) for c in range(3)))
    + card(20, 190, 250, 160, INK, -12)
    + f'<path d="M150 120 q30 -40 70 -30 M165 150 q22 -26 50 -20" fill="none" stroke="{SAFFRON}" stroke-width="10" stroke-linecap="round"/>',
    # cross-border: globe, two notes, dashed route
    "lesson15": lambda: globe(240, 220, 150)
    + f'<path d="M70 330 Q240 40 410 330" fill="none" stroke="{SAFFRON}" stroke-width="10" stroke-dasharray="4 22" stroke-linecap="round"/>'
    + note(0, 320, 150, 84, WHITE, -8) + note(330, 320, 150, 84, YELLOW, 8) + coin(240, 90, 44, "$"),
    # transaction: wallet to wallet across blocks
    "lesson16": lambda: chain(100, 60, 1.0) + phone(20, 190, 140, 250, coin(90, 300, 36, "₿") + f'<rect x="48" y="360" width="84" height="14" rx="7" fill="{INK}" opacity=".25"/>')
    + phone(320, 190, 140, 250, f'<path d="M352 310 L378 336 L430 280" fill="none" stroke="{TEAL}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    + arrow("M176 310 H296", SAFFRON, 12) + tag(178, 236, "0x…", INK, MINT, 24),
    # scams: shield, hook, warning
    "lesson17": lambda: shield(150, 60, 1.6, MINT, "check")
    + f'<path d="M70 40 V250 q0 60 46 60 q40 0 40 -44" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M146 280 l10 -24 l12 26" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    + f'<path d="M390 290 L460 410 H320 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><path d="M390 330 V370" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><circle cx="390" cy="390" r="8" fill="{INK}"/>'
    + key(30, 360, .8, 0),
    # gold, dollar, bitcoin
    "lesson18": lambda: goldbar(20, 300, 210) + goldbar(60, 232, 150) + note(230, 110, 220, 120, MINT, 8)
    + coin(350, 320, 86, "₿") + chart("30,170 90,120 140,150 200,70", TEAL, 10) + coin(120, 90, 0.01, ""),
    # pay later: calendar of instalments, card, growing coins
    "lesson19": lambda: calendar(30, 60, 1.35) + card(220, 250, 240, 150, INK, 8)
    + coin(70, 380, 34, "1") + coin(150, 372, 42, "2") + f'<path d="M300 110 q60 -50 120 10" fill="none" stroke="{SAFFRON}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 20"/>',
    # banks: building fading into a phone
    "lesson20": lambda: f'<g opacity=".55">{bank(10, 120, 1.15)}</g>' + phone(260, 70, 190, 340, bank(300, 150, .55, MINT)
        + f'<rect x="296" y="290" width="118" height="16" rx="8" fill="{YELLOW}"/><rect x="296" y="322" width="86" height="12" rx="6" fill="{INK}" opacity=".25"/><rect x="296" y="348" width="104" height="12" rx="6" fill="{INK}" opacity=".25"/>')
    + arrow("M150 80 Q230 30 290 70", SAFFRON, 10),
    # AI: assistant, coin, sparkle
    "lesson21": lambda: bot(60, 90, 1.5) + coin(380, 330, 70, "$")
    + f'<path d="M400 60 l12 34 l34 12 l-34 12 l-12 34 l-12 -34 l-34 -12 l34 -12 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    + f'<rect x="70" y="360" width="220" height="70" rx="22" fill="{WHITE}" stroke="{INK}" stroke-width="6"/><rect x="96" y="384" width="120" height="12" rx="6" fill="{TEAL}"/><rect x="96" y="404" width="80" height="10" rx="5" fill="{INK}" opacity=".25"/>',
}

CSS = """
@font-face { font-family: Bricolage; src: url('%(fonts)s/BricolageGrotesque.ttf'); font-weight: 200 800; }
@font-face { font-family: PlayfairI; src: url('%(fonts)s/PlayfairDisplay-Italic.ttf'); font-style: italic; }
@font-face { font-family: Yekan; src: url('%(yekan)s/IRANYekanXFaNum-Black.woff2'); font-weight: 900; }
@font-face { font-family: Yekan; src: url('%(yekan)s/IRANYekanXFaNum-Medium.woff2'); font-weight: 500; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1254px; height: 1254px; }
body { background: #F4EFE4; color: #101F22; font-family: Bricolage, sans-serif; position: relative; overflow: hidden; }
.top { position: absolute; left: 84px; right: 84px; top: 70px; display: flex; justify-content: space-between; align-items: center; }
.brand { display: flex; align-items: center; gap: 20px; font-weight: 300; font-size: 36px; letter-spacing: .34em; }
.brand img { width: 76px; height: 76px; }
.badge { border: 3px solid #0F7C74; color: #0F7C74; border-radius: 999px; padding: 12px 26px; font-weight: 800; font-size: 24px; letter-spacing: .14em; }
.rule { position: absolute; left: 84px; top: 222px; width: 124px; height: 9px; border-radius: 5px; background: #0F7C74; }
.art { position: absolute; right: 60px; top: 190px; width: 470px; height: 470px; }
.disc { position: absolute; right: 30px; top: 170px; width: 520px; height: 520px; border-radius: 50%%; background: radial-gradient(circle at 35%% 30%%, rgba(87,217,199,.42), rgba(87,217,199,.14) 70%%); }
.titles { position: absolute; left: 84px; top: 262px; width: 600px; }
.fat { position: absolute; left: 84px; right: 84px; top: 690px; }
h1 { font-weight: 800; letter-spacing: -.02em; line-height: 1.08; }
h1.fa { font-family: Yekan, sans-serif; font-weight: 900; letter-spacing: 0; direction: rtl; text-align: right; line-height: 1.32; }
.sub { position: absolute; left: 84px; right: 84px; bottom: 150px; display: grid; gap: 10px; }
.sub p { font-size: 30px; line-height: 1.4; color: #37484B; }
.sub p.fa { font-family: Yekan, sans-serif; font-weight: 500; direction: rtl; text-align: right; font-size: 29px; line-height: 1.7; }
.foot { position: absolute; left: 0; right: 0; bottom: 0; height: 124px; background: #0B1416; color: #F2F0E9; display: flex; justify-content: space-between; align-items: center; padding: 0 84px; }
.foot span { font-weight: 700; font-size: 25px; letter-spacing: .2em; }
.foot i { font-family: PlayfairI, serif; font-style: italic; font-size: 36px; color: #57D9C7; }
"""

# short cover lines (English, Persian); the full subtitle is on the page
LINES = {
    "lesson12": ("Inflation, real returns and the rule of 72, in plain words.", "تورم، بازده واقعی و قاعده‌ی ۷۲ به زبان ساده."),
    "lesson13": ("Bank, exchange or personal wallet: who holds the key?", "بانک، صرافی یا کیف پول شخصی: کلید دست کیست؟"),
    "lesson14": ("One purchase, five players, and money that arrives later.", "یک خرید، پنج بازیگر و پولی که دیرتر می‌رسد."),
    "lesson15": ("SWIFT, correspondent banks, hidden costs and stablecoins.", "سوئیفت، بانک کارگزار، هزینه‌ی پنهان و استیبل‌کوین."),
    "lesson16": ("Three checks before you press Send.", "سه بررسی پیش از زدن دکمه‌ی ارسال."),
    "lesson17": ("Five common traps and one habit for each.", "پنج تله‌ی رایج و یک عادت برای هر کدام."),
    "lesson18": ("Four plain questions, three very different assets.", "چهار پرسش ساده، سه دارایی کاملاً متفاوت."),
    "lesson19": ("What an instalment plan really costs.", "خرید قسطی واقعاً چقدر تمام می‌شود."),
    "lesson20": ("Neobanks, fintech and open banking, explained.", "نئوبانک، فین‌تک و بانکداری باز به زبان ساده."),
    "lesson21": ("What works today, what is coming, and the new risks.", "چه چیزی امروز کار می‌کند، چه در راه است و ریسک‌های تازه."),
}


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LESSON


def doc(L):
    slug = L["slug"]
    en, fa = L["title"]
    n = max(len(en), int(len(fa) * 1.05))
    size = 78 if n <= 40 else 68 if n <= 52 else 60
    cat = L["badge"][0].split("•")[0].strip().upper()
    markers = "".join(
        f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>'
        for c in (INK, SAFFRON, TEAL))
    css = CSS % {"fonts": FONTS.as_uri(), "yekan": YEKAN.as_uri()}
    line_en, line_fa = LINES[slug]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="top"><div class="brand"><img src="{LOGO.as_uri()}" alt="">DITOMAN</div><div class="badge">LESSON {L["number"]} · {html.escape(cat)}</div></div>
<div class="rule"></div><div class="disc"></div>
<svg class="art" viewBox="0 0 480 480"><defs>{markers}</defs>{ART[slug]()}</svg>
<div class="titles"><h1 style="font-size:{size}px">{html.escape(en)}</h1></div>
<div class="fat"><h1 class="fa" style="font-size:{size}px">{html.escape(fa)}</h1></div>
<div class="sub"><p>{html.escape(line_en)}</p><p class="fa">{html.escape(line_fa)}</p></div>
<div class="foot"><span>DITOMAN | TMN · DITOMAN.COM</span><i>Learn · Connect · Evolve</i></div>
</body></html>"""


def main():
    only = set(sys.argv[1:])
    lessons = sorted((load(p) for p in DATA.glob("lesson*.py")), key=lambda L: L["number"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": SIZE, "height": SIZE})
        for L in lessons:
            if only and L["slug"] not in only:
                continue
            tmp = ROOT / f'{L["slug"]}-cover.tmp.html'
            tmp.write_text(doc(L), encoding="utf-8")
            pg.goto(tmp.as_uri(), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(150)
            png = ROOT / f'{L["slug"]}-cover.png'
            pg.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": SIZE, "height": SIZE})
            tmp.unlink()
            Image.open(png).convert("RGB").save(ROOT / f'{L["slug"]}-cover.jpg', "JPEG", quality=86, optimize=True, progressive=True)
            png.unlink()
            print("cover", L["slug"])
        b.close()


if __name__ == "__main__":
    main()
