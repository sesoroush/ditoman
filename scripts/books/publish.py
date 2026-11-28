#!/usr/bin/env python3
"""Send one prepared book summary to Telegram and put it on the homepage.

  python3 scripts/books/publish.py <slug>

Writes telegram/<date>-<NN>-<slug>.md (the push of that file makes .github/workflows/telegram.yml post it),
adds the story card at the top of the homepage and records the post date in data/books/state.json.
Run from the repo root, then commit and push everything it changed.
"""
import html, json, re, sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import DATA, ROOT, STATE, book, dates, load, save, tehran_today, telegram_len, telegram_text  # noqa: E402


def main(slug):
    b = book(slug)
    state = load(STATE, {})
    assert b and state.get(slug, {}).get("prepared") and (ROOT / f"{slug}.html").exists(), f"{slug} is not prepared: run build.py first"
    assert not state[slug].get("posted"), f"{slug} already went to Telegram on {state[slug]['posted']}"
    assert (ROOT / "social" / slug / "post.png").exists(), "banner missing"
    meta = json.loads((DATA / slug / "meta.json").read_text(encoding="utf-8"))
    d = dates(tehran_today())
    text = telegram_text(slug, meta)
    assert telegram_len(text) < 4096
    used = [int(m.group(1)) for f in (ROOT / "telegram").glob(f"{d['iso']}-*.md") if (m := re.match(r"\d{4}-\d\d-\d\d-(\d+)-", f.name))]
    post = ROOT / "telegram" / f"{d['iso']}-{max(used, default=0) + 1:02d}-{slug}.md"
    post.write_text(f"image: social/{slug}/post.png\n{text}", encoding="utf-8")

    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    if f'href="{slug}.html"' not in s:
        anchor = '        <div class="co-grid story-grid">\n'
        assert s.count(anchor) == 1
        e = lambda t: html.escape(t, quote=False)
        alt = html.escape(f"Book summary: {b['en']}")
        img = lambda lang, pre: (f'<img lang="{lang}" src="social/{slug}/{pre}thumb.webp" srcset="social/{slug}/{pre}thumb.webp 240w, social/{slug}/{pre}card.webp 900w" '
                                 f'sizes="(max-width: 600px) 84px, 112px" width="240" height="240" alt="{alt}" loading="lazy" />')
        card = f'''          <a class="co-card" data-kicker="خلاصه کتاب | BOOK SUMMARY" href="{slug}.html">
            <div class="co-art">{img("fa", "")}{img("en", "en-")}</div>
            <div class="co-body">
              <span class="co-cat"><span lang="fa">خلاصه کتاب</span><span lang="en">Book summary</span></span>
              <h3>{e(meta["card_en_title"])} <span lang="fa">{e(meta["h1_fa"])}</span></h3>
              <span class="co-time"><span lang="fa">{d["fa_short"]} · {str(meta["read_min"]).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))} دقیقه مطالعه</span><span lang="en">{d["en_short"]} · {meta["read_min"]} min read</span></span>
              <p>{e(meta["card_en"])}</p>
              <p class="co-fa" lang="fa">{e(meta["card_fa"])}</p>
              <span class="co-go">Read the story</span>
            </div>
          </a>
'''
        p.write_text(s.replace(anchor, anchor + card, 1), encoding="utf-8")
    state[slug]["posted"] = d["iso"]
    save(STATE, state)
    print(f"ready to push: {post.relative_to(ROOT)} ({telegram_len(text)}/4096), index.html, data/books/state.json")


if __name__ == "__main__":
    main(sys.argv[1])
