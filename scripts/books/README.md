# Ditoman book summaries: how they are made

Ditoman's library is a list of 100 books in ten fields (`data/books/catalog.json`). Every book gets a
bilingual summary page on ditoman.com, a banner in the fixed book template, and a short Telegram post.
One summary goes to Telegram every day at 10:00 Tehran, picked at random from the prepared ones.

## Files

| Path | What it is |
|---|---|
| `data/books/catalog.json` | The list: number, slug, field, titles, authors, year, one-line notes |
| `data/books/state.json` | Per slug: `prepared` date (page is on the site) and `posted` date (went to Telegram) |
| `data/books/covers.json` | Which jacket image was fetched for each book; `"rejected": true` = wrong image, do not use |
| `assets/books/<slug>.jpg` | The book's real jacket. A banner is never made without it |
| `scripts/books/data/<slug>/` | The summary's text: `meta.json`, `fa.md`, `en.md`, `telegram.md` |
| `scripts/books/build.py` | Text + jacket → `<slug>.html`, `social/<slug>/*`, library on `books.html` |
| `scripts/books/publish.py` | Prepared book → Telegram post file + homepage card |
| `scripts/books/pick.py` | Random pick (`post`, `prepare N`, `status`) |
| `scripts/books/library.py` | Rebuilds the library block on `books.html` |
| `scripts/books/fetch_covers.py` | Runs on the GitHub runner (workflow "Fetch book jackets") |

The model to copy for a new book is `scripts/books/data/book-the-east-asian-miracle/`.

## Preparing a summary (site only, nothing goes to Telegram)

1. `python3 scripts/books/pick.py prepare 3` gives random books that have a reviewed jacket and no summary yet.
2. Research each book with WebSearch (and WebFetch where pages open): the publisher's page, the author's own
   page, a library or bookshop record, and one or two serious reviews. Confirm title, authors, publisher,
   first publication year, edition and what the book covers. Use the catalog's facts only after checking them;
   if the catalog is wrong (author, year), fix `catalog.json` too.
3. Write the four files in `scripts/books/data/<slug>/` (formats below).
4. `python3 scripts/books/build.py <slug>`. Exit code 2 = the banner text does not fit: shorten it and rerun.
5. Look at `social/<slug>/post.png` with the Read tool: the layout must be exactly the fixed template, nothing
   clipped, the jacket is the right book. Open nothing else.
6. Commit and push everything the build changed (`<slug>.html`, `social/<slug>`, `scripts/books/data/<slug>`,
   `data/books/state.json`, `books.html`, `scripts/build_seo.py`, `data/links.json`).

## Sending the day's book to Telegram

1. `python3 scripts/books/pick.py post` gives one prepared, not-yet-posted book. If it prints nothing, prepare one first.
2. `python3 scripts/books/publish.py <slug>`, then commit and push. The push of `telegram/<date>-NN-<slug>.md`
   makes the Telegram workflow send the banner and the text.

## What a summary must be (editorial rules)

- **Honest about its basis.** We usually have not read the full text. The summary rests on the publisher's
  description, the table of contents, the author's public talks and serious reviews. `basis_fa` / `basis_en`
  in `meta.json` say exactly that, and the builder prints it at the end of section 1. Never present a lesson
  as a quotation; never invent page numbers, sales figures, chapter titles or quotes.
- **Our own words.** No passages copied from the book or from reviews. At most one short quoted phrase.
- **Every number has a source** in `sources`, and is one we verified in this session.
- **Fixed shape: "ten lessons".** Section 1 «در یک نگاه» (facts table + the idea in one line), section 2 what the
  book is and why we picked it, section 3 the ten lessons (each `### درس N. …`, two or three short paragraphs,
  a «نکته‌ی درس:» line, and where one fits a `~ در دیتومان: [lesson](lessonNN.html)` line), section 4 a table,
  section 5 «نگاه دیتومان» (what it means for an Iranian reader: work, skills, business, saving), section 6
  critique and limits (real criticisms of the book, plus the limits of our summary), section 7 who it is for,
  «جمع‌بندی دیتومان» and «پرسش پایانی». The English file mirrors the Persian one section for section.
- **Voice.** «با هم دنبال می‌کنیم»: we look at it together, we do not lecture. Hopeful, practical, calm.
  Lead with learning, skill and the future.
- **Neutral.** No political stance from any side. For books on politics, power, a country's system or its
  leaders: report the author's argument as the author's, give the main criticisms, take no side.
- **No financial advice.** No buy/sell signals, no price predictions, no disclaimer line.
- **Wording.** Brand is always «دیتومان». Never «زیر فشار» or «نشان بدهی». Persian digits in Persian text.
  Never the founders' names or "OBSERVIANDA". No asterisks anywhere except `**bold**` pairs, which the
  builder and the Telegram workflow turn into real bold.
- **Airy layout.** Short paragraphs; one idea per paragraph; a blank line between blocks.
- **Links.** Link the Ditoman lessons and pages that cover the same idea (`lesson01.html` … `lesson30.html`,
  `learn.html`, other `book-*.html` pages), and real outside sources that open.

## File formats

`meta.json`

```json
{
 "h1_fa": "خلاصه کتاب «روان‌شناسی پول»؛ ده درس درباره‌ی رفتار ما با پول",
 "h1_en": "Book summary: The Psychology of Money, ten lessons on how we behave with money",
 "sub_fa": "یک جمله‌ی معرفی برای زیر تیتر",
 "sub_en": "One sentence under the headline",
 "desc_fa": "توضیح متای صفحه، حدود ۱۶۰ نویسه، با پایان «Ditoman book summary.»",
 "card_en_title": "Short English title for the homepage card and the English cover",
 "card_fa": "یک جمله برای کارت صفحه‌ی اول",
 "card_en": "One sentence for the homepage card",
 "read_min": 12,
 "stats": [["۲۰۲۰", "2020", "سال انتشار", "published"], ["…", "…", "…", "…"], ["۱۰ درس", "10 lessons", "چارچوب آموزشی دیتومان", "Ditoman's teaching frame"], ["۱۲ دقیقه", "12 min", "خلاصه‌ی کامل", "full summary"]],
 "basis_fa": "این صفحه خلاصه و تحلیل دیتومان است، نه متن کتاب. … بر پایه‌ی چه منابعی نوشته شده …",
 "basis_en": "This page is Ditoman's summary and analysis, not the book's text. …",
 "more": [["lesson22.html", "پول ماهانه‌ام کجا می‌رود؟", "Where does my monthly money go?"]],
 "sources": [["Publisher: title (publisher page)", "https://…"]],
 "hashtags": "#خلاصه_کتاب #سواد_مالی #سرمایه_گذاری #کتاب #دیتومان",
 "link_words": {"fa": ["روان‌شناسی پول"], "en": ["The Psychology of Money"]},
 "cover": {
  "gold": "روان‌شناسی",
  "white": "پول",
  "teal": "ده درس درباره‌ی رفتار ما با پول",
  "author": "نویسنده: مورگان هاوزل",
  "latin": "Morgan Housel · The Psychology of Money · 2020",
  "bullets": ["یک جمله‌ی کوتاه.", "یک جمله‌ی کوتاه دیگر."],
  "tags": ["سواد مالی", "رفتار", "پس‌انداز"]
 }
}
```

`fa.md` and `en.md`: a small Markdown subset. `## ` section (numbered automatically from 1), `### ` lesson
heading, plain paragraphs, `- ` bullets, `> ` note, `| a | b |` tables (first row is the header),
`~ ` a muted line, `**bold**`, `[text](url)`. Do not write the «بیشتر بخوانید» and «منابع» sections: the
builder adds them from `more` and `sources`.

`telegram.md`: the post without the image line and without the footer (the scripts add the links to the full
page, the library and the live prices, the signature and the hashtags). First line
`📚 **خلاصه کتاب | <Persian title>؛ <hook>**`, a two- or three-line opening, then the ten lessons, each as an
emoji + bold heading on its own line, a blank line, and one or two sentences, and a bold closing line.
Keep it under about 2,700 characters so the whole post stays below Telegram's 4,096 limit.

## The banner (fixed template, do not redesign)

`scripts/books/cover.py` holds the approved layout: logo block centred on top, «خلاصه کتاب» pill, gold title
line, white second line, teal subtitle, thin rule, author line, Latin line, a box with two bullets on the
left; the real jacket as a standing book on the right; three tags and the ditoman.com pill below. Only the
texts, the jacket and the faint background glow change. Keep the gold line to one or two words where
possible, the bullets to one short sentence each. If a book has no usable jacket, do not make a banner and do
not prepare the book: `pick.py status` lists those, and Soroush sends the image.
