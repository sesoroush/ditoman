#!/usr/bin/env python3
"""Sideways navigation that is written into the pages themselves.

1. Story pages: a "newer story / older story" pair at the foot of every story, in the order
   of the homepage list (index.html is the source of truth for stories).
2. Homepage: the lesson row, all lessons in learning order, between the home-lessons markers.

Both blocks sit between HTML comment markers and are rewritten on every run, so running it
twice changes nothing. Run from the repo root, before build_en_pages.py:
    python3 scripts/build_nav.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_en_pages import h1_texts  # noqa: E402

SN_START, SN_END = "<!-- storynav:start -->", "<!-- storynav:end -->"
HL_START, HL_END = "<!-- home-lessons:start -->", "<!-- home-lessons:end -->"
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"

# learning order, the same five stages as learn.html
STAGES = [
    ("Money and trust", "پول و اعتماد", [12, 13, 19, 14, 15, 22, 23, 24, 25, 26]),
    ("Blockchain and Bitcoin", "بلاکچین و بیت‌کوین", [1, 2, 3, 4, 27, 28, 29, 30]),
    ("Using crypto safely", "استفاده‌ی امن از کریپتو", [16, 17, 5, 6, 9]),
    ("Markets and saving", "بازار و پس‌انداز", [7, 10, 18]),
    ("The future of money", "آینده‌ی پول", [11, 8, 20, 21]),
]
# Persian titles for the early lessons, whose pages carry the Persian headline in other markup
FA_TITLES = {
    1: "بلاکچین چیست؟", 2: "چرا بلاکچین مهم است", 3: "چرا بیت‌کوین ساخته شد", 4: "ساتوشی ناکاموتو کیست؟",
    5: "پیش از دست زدن به هر توکن، این‌ها را بررسی کنید", 6: "پنج پرسش پیش از خرید",
    7: "خبرهای بزرگ چطور قیمت بیت‌کوین را تکان می‌دهند", 8: "اگر پولت تاریخ انقضا داشت؟",
    9: "قفل لیکوئیدیتی واقعاً یعنی چه؟", 10: "چرا قیمت یک‌دفعه می‌ریزد؟", 11: "دلار دیجیتال، پشتوانه‌اش کجاست؟",
}
EN_TITLES = {
    1: "What is blockchain?", 2: "Why blockchain matters", 3: "Why Bitcoin was created", 4: "Who is Satoshi Nakamoto?",
    5: "How to check any token before you touch it", 6: "Five questions to ask before you buy",
    7: "How big news moves Bitcoin", 8: "What if your money had an expiry date?",
    9: "What does a liquidity lock actually mean?", 10: "Why do prices suddenly crash?", 11: "Digital dollars: what backs them?",
}


def fa_num(n):
    return "".join(FA_DIGITS[int(c)] for c in str(n))


def clean(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s or "")).split())


def esc(s):
    return html.escape(s, quote=False)


def stories():
    """Homepage stories, newest first: href, English title, Persian title, Persian thumb, English thumb."""
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    a = s.index('id="stories"')
    sec = s[a:s.index("</section>", a)]
    out = []
    for m in re.finditer(r'<a class="co-card[^"]*"([^>]*)>(.*?)</a>', sec, re.S):
        href = re.search(r'href="([^"]+)"', m.group(1)).group(1)
        body = m.group(2)
        h3 = re.search(r'<h3>(.*?)<span lang="fa">(.*?)</span></h3>', body, re.S)
        if not h3:
            continue
        img_fa = re.search(r'<img lang="fa" src="([^"]+)"', body) or re.search(r'<img src="([^"]+)"', body)
        img_en = re.search(r'<img lang="en" src="([^"]+)"', body)
        out.append(dict(href=href, en=clean(h3.group(1)), fa=clean(h3.group(2)),
                        img_fa=img_fa.group(1) if img_fa else "", img_en=img_en.group(1) if img_en else ""))
    return out


def story_link(kind, st):
    label = {"newer": ("خبر جدیدتر", "Newer story"), "older": ("خبر قدیمی‌تر", "Older story")}[kind]
    img = ""
    if st["img_fa"]:
        en_src = st["img_en"] or st["img_fa"]
        if st["img_en"]:
            img = (f'<img lang="fa" src="{st["img_fa"]}" alt="" width="72" height="72" loading="lazy" decoding="async" />'
                   f'<img lang="en" src="{en_src}" alt="" width="72" height="72" loading="lazy" decoding="async" />')
        else:
            img = f'<img src="{st["img_fa"]}" alt="" width="72" height="72" loading="lazy" decoding="async" />'
    return (f'<a class="sn sn-{kind}" href="{st["href"]}">{img}<span class="sn-t"><small><span lang="fa">{label[0]}</span>'
            f'<span lang="en">{label[1]}</span></small><b><span lang="fa" dir="rtl">{esc(st["fa"])}</span>'
            f'<span lang="en">{esc(st["en"])}</span></b></span></a>')


def story_nav(items):
    n = 0
    for i, st in enumerate(items):
        page = ROOT / st["href"]
        if not page.exists():
            continue
        src = page.read_text(encoding="utf-8")
        newer = items[i - 1] if i > 0 else None
        older = items[i + 1] if i + 1 < len(items) else None
        parts = []
        parts.append(story_link("newer", newer) if newer else
                     '<a class="sn sn-newer sn-all" href="./#stories"><span class="sn-t"><small><span lang="fa">تازه‌ترین خبر همین است</span>'
                     '<span lang="en">This is the newest story</span></small><b><span lang="fa" dir="rtl">همه‌ی مطالب</span>'
                     '<span lang="en">All stories</span></b></span></a>')
        if older:
            parts.append(story_link("older", older))
        block = f'{SN_START}\n<nav class="story-nav" aria-label="Stories">{"".join(parts)}</nav>\n{SN_END}'
        if SN_START in src:
            new = re.sub(re.escape(SN_START) + r".*?" + re.escape(SN_END), lambda m: block, src, flags=re.S)
        elif "</main>" in src:
            new = src.replace("</main>", block + "\n</main>", 1)
        else:
            continue
        if new != src:
            page.write_text(new, encoding="utf-8")
            n += 1
    return n


def lesson_titles(n):
    src = (ROOT / f"lesson{n:02d}.html").read_text(encoding="utf-8")
    fa, en = h1_texts(src)
    return (EN_TITLES.get(n) or en, FA_TITLES.get(n) or fa)


def home_lessons():
    page = ROOT / "index.html"
    src = page.read_text(encoding="utf-8")
    if HL_START not in src:
        return 0
    tiles, step = [], 0
    for k, (stage_en, stage_fa, nums) in enumerate(STAGES, 1):
        for n in nums:
            if not (ROOT / f"lesson{n:02d}.html").exists():
                continue
            step += 1
            en, fa = lesson_titles(n)
            tiles.append(
                f'<a class="ls-tile" href="lesson{n:02d}.html"><span class="ls-step"><span lang="fa">قدم {fa_num(step)}</span>'
                f'<span lang="en">Step {step}</span></span><b><span lang="fa" dir="rtl">{esc(fa)}</span><span lang="en">{esc(en)}</span></b>'
                f'<small><span lang="fa">{fa_num(k)}. {esc(stage_fa)}</span><span lang="en">{k}. {esc(stage_en)}</span></small></a>')
    block = (f'{HL_START}\n          <div class="hrow-track">\n            ' + "\n            ".join(tiles) +
             f'\n            <a class="ls-tile ls-all" href="learn.html"><b><span lang="fa" dir="rtl">همه‌ی درس‌ها و مسیر یادگیری</span>'
             f'<span lang="en">All lessons and the learning path</span></b></a>\n          </div>\n          {HL_END}')
    new = re.sub(re.escape(HL_START) + r".*?" + re.escape(HL_END), lambda m: block, src, flags=re.S)
    if new != src:
        page.write_text(new, encoding="utf-8")
        return 1
    return 0


def main():
    items = stories()
    print(f"{story_nav(items)} story pages updated of {len(items)}; homepage lesson row {'updated' if home_lessons() else 'unchanged'}")


if __name__ == "__main__":
    main()
