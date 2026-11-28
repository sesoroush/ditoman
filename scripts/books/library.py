#!/usr/bin/env python3
"""Rebuild the book library on books.html from data/books/catalog.json and data/books/state.json.

Persian and English each get: the table of published summaries and the categorised grid of all
books in the catalog (a card links to its summary once the page exists). Run from the repo root.
"""
import html, re, sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import ROOT, STATE, catalog, fa_num, load  # noqa: E402

# summaries published before the 100-book list (not part of it)
LEGACY = [
    ("book-stop-letting-everything-affect-you", "نگذار هر چیزی روی تو اثر بگذارد", "Stop Letting Everything Affect You", "دنیل چیدیاک، ۲۰۲۵", "Daniel Chidiac, 2025",
     "بیش‌فکری، مرزبندی، خودتخریبی و ربطش به تصمیم‌های مالی", "Overthinking, boundaries, self-sabotage and what it means for money decisions"),
    ("book-absent-superpower", "ابرقدرت غایب", "The Absent Superpower", "پیتر زایهان، ۲۰۱۶", "Peter Zeihan, 2016",
     "انقلاب شیل، جهانی بدون پلیس آمریکا، چین، روسیه و خلیج فارس", "Shale, a world without America as policeman, China, Russia, the Gulf"),
]
CSS = """<style>
.bks{margin:8px 0 26px}.bks h3{display:flex;align-items:center;gap:10px;margin:26px 0 14px}.bks h3 i{width:12px;height:12px;border-radius:50%;display:inline-block}
.bgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(136px,1fr));gap:14px}
.bc{position:relative;min-height:230px;border-radius:6px 12px 12px 6px;padding:14px 12px 12px 18px;background:radial-gradient(ellipse 90% 60% at 70% 20%,rgba(255,255,255,.08),transparent 70%),linear-gradient(160deg,#13283f,#0a1a2b);box-shadow:0 10px 24px rgba(0,0,0,.45),inset 7px 0 0 var(--c);display:flex;flex-direction:column;overflow:hidden;text-decoration:none}
a.bc{transition:transform .15s ease,box-shadow .15s ease}a.bc:hover{transform:translateY(-4px);box-shadow:0 16px 30px rgba(0,0,0,.55),inset 7px 0 0 var(--c)}
.bc .k{font-size:11px;font-weight:700;color:var(--c);letter-spacing:.04em}
.bc .tf{margin-top:8px;font-weight:900;font-size:17px;line-height:1.4;background:linear-gradient(180deg,#FFE7A3,#E9B94A);-webkit-background-clip:text;color:transparent}
.bc .te{margin-top:6px;font-size:11.5px;line-height:1.35;color:#d8dde2;direction:ltr;text-align:left}
.bc .a{margin-top:auto;font-size:12px;font-weight:700;color:#F2F0E9}.bc .ae{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:10.5px;color:#9fb0bd;direction:ltr;text-align:left}
.bc .dm{margin-top:8px;padding-top:6px;border-top:1px solid rgba(255,255,255,.1);font-size:9px;letter-spacing:.25em;color:#57D9C7;direction:ltr;text-align:left;font-family:Inter,sans-serif}
.bc .rd{align-self:flex-start;margin-top:8px;padding:2px 9px;border-radius:20px;background:#57D9C7;color:#0a1a2b;font-size:10.5px;font-weight:800}
.bks[dir=ltr] .bc .tf{font-size:15px;line-height:1.3}
.lesson-content a.bc,.lesson-content a.bc:hover{text-decoration:none;border-bottom:0}
.bdesc{font-size:12.5px;line-height:1.6;color:#b9c6c9;margin-top:6px}
.bwrap{display:flex;flex-direction:column}
</style>"""
e = lambda t: html.escape(str(t), quote=False)


def card(b, c, ready, en):
    tag, close = (f'<a class="bc" href="{b["slug"]}.html" style="--c:{c["color"]}">', "</a>") if ready else (f'<div class="bc" style="--c:{c["color"]}">', "</div>")
    if en:
        rd = '<span class="rd">Summary ready</span>' if ready else ""
        return (f'<div class="bwrap">{tag}<span class="k">{e(c["en"])} · {b["year"]}</span><span class="tf">{e(b["en"])}</span>{rd}'
                f'<span class="a">{e(b["authors_en"])}</span><span class="dm">DITOMAN</span>{close}<div class="bdesc">{e(b["note_en"])}</div></div>')
    rd = '<span class="rd">خلاصه آماده است</span>' if ready else ""
    return (f'<div class="bwrap">{tag}<span class="k">{e(c["fa"])} · {fa_num(b["year"])}</span><span class="tf">{e(b["fa"])}</span>'
            f'<span class="te">{e(b["en"])}</span>{rd}<span class="a">{e(b["authors_fa"])}</span><span class="ae">{e(b["authors_en"])}</span>'
            f'<span class="dm">DITOMAN</span>{close}<div class="bdesc">{e(b["note_fa"])}</div></div>')


def grid(cat, ready, en):
    out = f'<div class="bks" dir="{"ltr" if en else "rtl"}">'
    for c in cat["categories"]:
        books = [b for b in cat["books"] if b["cat"] == c["key"]]
        small = "" if en else f' <small style="color:#9fb0bd;font-weight:500">{e(c["en"])}</small>'
        out += f'<h3><i style="background:{c["color"]}"></i>{e(c["en"] if en else c["fa"])}{small}</h3><div class="bgrid">' + "".join(card(b, c, b["slug"] in ready, en) for b in books) + "</div>"
    return out + "</div>"


def table(cat, state, en):
    rows = sorted((b for b in cat["books"] if state.get(b["slug"], {}).get("prepared")), key=lambda b: state[b["slug"]]["prepared"], reverse=True)
    link = lambda slug, text: f'<a href="https://ditoman.com/{slug}.html" target="_blank" rel="noopener" style="color:#57D9C7">{e(text)}</a>'
    if en:
        t = "<div class=\"tw\"><table><tr><th>Book</th><th>Author</th><th>Subject</th></tr>"
        t += "".join(f'<tr><td>{link(b["slug"], b["en"])}</td><td>{e(b["authors_en"])}, {b["year"]}</td><td>{e(b["note_en"])}</td></tr>' for b in rows)
        t += "".join(f"<tr><td>{link(s, te)}</td><td>{e(ae)}</td><td>{e(de)}</td></tr>" for s, tf, te, af, ae, df, de in LEGACY)
    else:
        t = "<div class=\"tw\"><table><tr><th>کتاب</th><th>نویسنده</th><th>موضوع</th></tr>"
        t += "".join(f'<tr><td>{link(b["slug"], b["fa"] + "؛ " + b["en"])}</td><td>{e(b["authors_fa"])}، {fa_num(b["year"])}</td><td>{e(b["note_fa"])}</td></tr>' for b in rows)
        t += "".join(f"<tr><td>{link(s, tf + '؛ ' + te)}</td><td>{e(af)}</td><td>{e(df)}</td></tr>" for s, tf, te, af, ae, df, de in LEGACY)
    return t + "</table></div>"


def block(name, body):
    return f"<!-- {name}:start -->\n{body}\n<!-- {name}:end -->"


def put(s, name, body, first_time):
    a, z = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    if a in s:
        return s[:s.index(a)] + block(name, body) + s[s.index(z) + len(z):]
    start, end = first_time(s)
    return s[:start] + block(name, body) + s[end:]


def refresh():
    cat, state = catalog(), load(STATE, {})
    ready = {slug for slug, v in state.items() if v.get("prepared") and (ROOT / f"{slug}.html").exists()}
    n, k = len(cat["books"]), len(cat["categories"])
    p = ROOT / "books.html"
    s = p.read_text(encoding="utf-8")
    en_at = lambda t: t.index('<div class="lesson-content en"')
    more = "" if n >= 100 else f" فعلاً {fa_num(n)} کتاب در {fa_num(k)} حوزه فهرست شده و بقیه‌ی حوزه‌ها به‌زودی اضافه می‌شود."
    more_en = "" if n >= 100 else f" So far {n} books in {k} fields are listed; the remaining fields follow soon."
    fa_lib = (f'<h3><span class="check-number">2.</span> {e(cat["title_fa"])}</h3>\n'
              f"<p>کتابخانه‌ی دیتومان: صد کتاب در ده حوزه، از رمزارز و فین‌تک تا اقتصاد، سرمایه‌گذاری، توسعه و اقتصاد سیاسی.{more} "
              "هر روز خلاصه‌ی یک کتاب در کانال دیتومان منتشر می‌شود؛ کارت‌هایی که برچسب «خلاصه آماده است» دارند به صفحه‌ی خلاصه‌ی کامل می‌روند.</p>\n"
              f"{CSS}\n{grid(cat, ready, False)}\n"
              "<blockquote>کارت‌ها طراحی دیتومان‌اند، نه جلد اصلی کتاب‌ها. عنوان فارسی، ترجمه‌ی دیتومان از عنوان اصلی است و ممکن است با نام ترجمه‌های منتشرشده در ایران فرق داشته باشد. این فهرست انتخاب تحریریه است، نه رتبه‌بندی فروش.</blockquote>")
    en_lib = (f'<h3><span class="check-number">2.</span> {e(cat["title_en"])}</h3>\n'
              f"<p>The Ditoman library: one hundred books in ten fields, from crypto and fintech to economics, investing, development and political economy.{more_en} "
              "One book summary goes out on the Ditoman channel every day; cards marked “Summary ready” open the full summary.</p>\n"
              f"{grid(cat, ready, True)}\n"
              "<blockquote>The cards are Ditoman designs, not the books' jackets. The list is an editorial selection, not a sales ranking.</blockquote>")

    def fa_first(t):
        start = t.index('<h3><span class="check-number">2.</span>')
        note = t.index("</blockquote>", t.index("کارت‌ها طراحی دیتومان‌اند", start)) + len("</blockquote>")
        return start, note

    def en_first(t):
        start = t.index('<h3><span class="check-number">2.</span>', en_at(t))
        return start, t.index("</p>", start) + len("</p>")

    def table_first(lang_en):
        def f(t):
            head = "<div class=\"tw\"><table><tr><th>Book</th>" if lang_en else "<div class=\"tw\"><table><tr><th>کتاب</th>"
            start = t.index(head)
            return start, t.index("</table></div>", start) + len("</table></div>")
        return f

    s = put(s, "books-lib-fa", fa_lib, fa_first)
    s = put(s, "books-lib-en", en_lib, en_first)
    s = put(s, "books-table-fa", table(cat, state, False), table_first(False))
    s = put(s, "books-table-en", table(cat, state, True), table_first(True))
    s = re.sub(r'<div class="stat"><b lang="fa">[^<]*</b><b lang="en">[^<]*</b><span lang="fa">کتاب در کتابخانه</span>',
               f'<div class="stat"><b lang="fa">{fa_num(n)}</b><b lang="en">{n}</b><span lang="fa">کتاب در کتابخانه</span>', s, count=1)
    p.write_text(s, encoding="utf-8")
    print(f"library: {n} books, {k} fields, {len(ready)} summaries ready")


if __name__ == "__main__":
    refresh()
