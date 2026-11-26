#!/usr/bin/env python3
"""Cross-links inside the text: a company name, a concept or a topic that has its own page
becomes a link to that page (class "xl"), in the same language as the text around it.

  - terms come from data/links.json (topics) and from each company page's h1 (company names)
  - a term is used only if the target page itself contains it, each target is linked once per
    page and language, never from a page to itself, never inside headings, links or buttons
  - Persian text links to X.html, English text to X.en.html, other editions to X.<lang>.html

Run it last in the build chain. The other build scripts call strip() on what they read, because
translations are keyed by whole text nodes; running this script twice changes nothing.
  python3 scripts/build_links.py           write the links
  python3 scripts/build_links.py --strip   remove them
  python3 scripts/build_links.py --report  print what links where, write nothing
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "ar", "tr", "ru", "zh", "pt", "es", "fr", "de")
XL = re.compile(r'<a class="xl" href="[^"]*">(.*?)</a>', re.S)
TOK = re.compile(r"<!--.*?-->|<(script|style|svg|template|noscript|textarea)\b.*?</\1\s*>|"
                 r"<[a-zA-Z/!][^<>\"']*(?:(?:\"[^\"]*\"|'[^']*')[^<>\"']*)*>|[^<]+|<", re.S | re.I)
TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "li", "dd", "blockquote", "td"}
NEVER = {"a", "button", "h1", "h2", "h3", "h4", "h5", "h6", "nav", "header", "footer", "label", "select", "option",
         "sup", "sub", "code", "pre", "summary", "th", "dt", "figcaption", "caption", "title", "head", "time", "cite"}
NOCLASS = re.compile(r"\b(sources|subtitle|k-tagline|k-ref|tagline|breadcrumb|byline|meta|lang-btn|language-toggle|"
                     r"ir-rank|ir-tags|ir-v|quiz|self-check|answer|option|disclaimer|share|toc|chip|tag|badge|kicker|"
                     r"hero-lede|hero-paths|art-tag|foot|caption|credit|note-src)\b")
FA = re.compile(r"[؀-ۿ]")
ZW = "‌"
MAX_PER_BLOCK = 3
SUFFIX = {"en": ("s", "es"), "ru": None, "tr": None, "de": None, "pt": ("s", "es"), "es": ("s", "es"), "fr": ("s",)}


def strip(s):
    """Remove the links this script wrote, leaving the words."""
    return XL.sub(r"\1", s) if 'class="xl"' in s else s


def text_of(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def page_lang(name):
    parts = name.split(".")
    return parts[-2] if len(parts) > 2 and parts[-2] in LANGS else "fa"


def file_of(stem, lang):
    return stem + (".html" if lang == "fa" else f".{lang}.html")


def norm(s):
    return s.replace(ZW, "").replace(" ", "").lower()


def company_names():
    out = {}
    for p in sorted(ROOT.glob("*.html")):
        if p.name.count(".") > 1:
            continue
        s = p.read_text(encoding="utf-8")
        if "Iranian Companies" not in s[:4000]:
            continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if not m:
            continue
        fa = re.search(r'lang="fa"[^>]*>(.*?)</span>', m.group(1), re.S)
        en = re.search(r'lang="en"[^>]*>(.*?)</span>', m.group(1), re.S)
        if not fa or not en:
            continue
        clean = lambda t: re.sub(r"\s*\(.*?\)", "", text_of(t)).strip()
        e = re.sub(r"\s+(Co\.|Company|Co)$", "", clean(en.group(1))).rstrip("!")
        out[p.stem] = {"fa": [clean(fa.group(1))], "en": ["=" + e]}
    return out


def term_regex(term, lang):
    cs = term.startswith("=")
    t = term[1:] if cs else term
    pat = re.escape(t).replace(re.escape(ZW), f"[{ZW} ]?").replace(r"\ ", r"[  ]")
    return pat, cs


def load():
    cfg = json.loads((ROOT / "data" / "links.json").read_text(encoding="utf-8"))
    targets = company_names()
    targets.update({k: v for k, v in cfg["company_names"].items()})
    for k, v in cfg["topics"].items():
        for lang, terms in v.items():
            targets.setdefault(k, {}).setdefault(lang, [])
            targets[k][lang] = targets[k][lang] + [t for t in terms if t not in targets[k][lang]]
    trusted = set(cfg.get("trusted", [])) | set(cfg["company_names"])
    dropped = []
    table = {}   # lang -> [(pattern, case_sensitive, target, term)]
    for stem, by_lang in targets.items():
        for lang, terms in by_lang.items():
            f = ROOT / file_of(stem, lang)
            if not f.exists():
                continue
            body = norm(text_of(strip(f.read_text(encoding="utf-8"))))
            for term in terms:
                bare = term.lstrip("=")
                if stem not in trusted and norm(bare) not in body:
                    dropped.append((stem, lang, bare))
                    continue
                pat, cs = term_regex(term, lang)
                table.setdefault(lang, []).append((pat, cs, stem, bare))
    rx = {}
    for lang, rows in table.items():
        rows.sort(key=lambda r: -len(r[3]))
        # longest first; one alternation, each row a named group
        parts = [f"(?P<g{i}>{'' if cs else '(?i:'}{pat}{'' if cs else ')'})" for i, (pat, cs, _, _) in enumerate(rows)]
        rx[lang] = (re.compile("|".join(parts)), rows)
    return cfg, rx, dropped


def is_letter(ch, lang):
    if not ch:
        return False
    if lang == "zh":
        return False
    return ch.isalnum() or ch == ZW or ch == "_"


AVOID = []
# "Lesson 13" in the text of another lesson links to that lesson
LESSON = {"fa": r"درس[ \u200c]([۰-۹]{1,2})", "en": r"Lesson (\d{1,2})", "ar": r"الدرس (\d{1,2})", "tr": r"Ders (\d{1,2})",
          "ru": r"[Уу]рок[а-я]{0,2} (\d{1,2})", "zh": r"第 ?(\d{1,2}) ?课", "pt": r"(?:[Ll]ição|[Aa]ula) (\d{1,2})",
          "es": r"[Ll]ección (\d{1,2})", "fr": r"[Ll]eçon (\d{1,2})", "de": r"Lektion (\d{1,2})"}
LESSON = {k: re.compile(v) for k, v in LESSON.items()}


def find(text, lang, rx, used, self_stem, budget):
    """Yield (start, end, target) for the links to make in one text node."""
    pattern, rows = rx
    pos, out = 0, []
    while budget > len(out):
        m = pattern.search(text, pos)
        if not m:
            break
        row = rows[int(m.lastgroup[1:])]
        a, b, stem = m.start(), m.end(), row[2]
        pos = a + 1
        if stem == self_stem or stem in used:
            pos = b
            continue
        if a and is_letter(text[a - 1], lang):
            continue
        around = text[max(0, a - 30):b + 30].lower()
        if any(x in around for x in AVOID):
            continue
        rest = text[b:]
        if lang in ("fa", "ar"):
            sfx = re.match("(?:" + ZW + r"(?:های|ها|هایی|ی)|های|ها)(?![\u0600-\u06FF" + ZW + "])", rest) if lang == "fa" else None
            if sfx:
                b += sfx.end()
            elif rest[:1] and is_letter(rest[0], lang):
                continue
        elif lang != "zh":
            tail = re.match(r"\w*", rest).group(0)
            allowed = SUFFIX.get(lang, ())
            if tail:
                if allowed is None and len(tail) <= 3:
                    b += len(tail)
                elif allowed and tail in allowed:
                    b += len(tail)
                else:
                    continue
        used.add(stem)
        out.append((a, b, stem))
        pos = b
    for m in LESSON[lang].finditer(text) if lang in LESSON else ():
        if len(out) >= budget:
            break
        n = int(m.group(1).translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")))
        stem, a, b = f"lesson{n:02d}", m.start(), m.end()
        if stem == self_stem or stem in used or text[b:b + 1].isdigit() or any(a < y and x < b for x, y, _ in out):
            continue
        used.add(stem)
        out.append((a, b, stem))
    return sorted(out)


def link_page(src, name, rx, existing, stats):
    flang = page_lang(name)
    stem = name.split(".")[0]
    used = {}       # text language -> targets already linked
    stack = []      # (tag, region, block, never)
    out = []
    in_body = False
    block_count = [0]
    for m in TOK.finditer(src):
        tok = m.group(0)
        if tok[0] != "<" or tok == "<":
            if not in_body or not stack or not tok.strip():
                out.append(tok)
                continue
            region = next((s[1] for s in reversed(stack) if s[1]), None)
            blocked = any(s[3] for s in stack)
            in_block = any(s[2] for s in stack)
            if blocked or not in_block:
                out.append(tok)
                continue
            has_fa = bool(FA.search(tok))
            if flang in ("fa", "en"):
                tl = region if region in ("fa", "en") else ("fa" if has_fa else None)
                if tl == "en" and has_fa:
                    tl = None
            elif flang == "ar":
                tl = "ar" if (region in (None, "fa", "ar") and has_fa) else None
            else:
                tl = flang if (region != "fa" and not has_fa) else None
            if not tl or tl not in rx:
                out.append(tok)
                continue
            hits = find(tok, tl, rx[tl], used.setdefault(tl, set()), stem, MAX_PER_BLOCK - block_count[0])
            if not hits:
                out.append(tok)
                continue
            buf, last = [], 0
            for a, b, target in hits:
                href = file_of(target, tl)
                if href not in existing:
                    used[tl].discard(target)
                    continue
                buf.append(tok[last:a])
                buf.append(f'<a class="xl" href="{href}">{tok[a:b]}</a>')
                last = b
                block_count[0] += 1
                stats[(name, href)] = tok[a:b]
            buf.append(tok[last:])
            out.append("".join(buf))
            continue
        out.append(tok)
        t = TAG.match(tok)
        if not t:
            continue
        closing, tag = t.group(1) == "/", t.group(2).lower()
        if tag == "body":
            in_body = not closing
        if tag in VOID or tok.endswith("/>") or tag in ("script", "style", "svg", "template", "noscript", "textarea"):
            continue
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    del stack[i:]
                    break
            if tag in BLOCK:
                block_count[0] = 0
            continue
        lang = re.search(r'\slang="([a-z]{2})', tok)
        region = lang.group(1) if lang else None
        cls = re.search(r'\sclass="([^"]*)"', tok)
        idm = re.search(r'\sid="([^"]*)"', tok)
        if not region and idm and idm.group(1) in ("fa-content", "en-content"):
            region = idm.group(1)[:2]
        never = tag in NEVER or bool(cls and NOCLASS.search(cls.group(1))) or 'translate="no"' in tok \
            or " data-en=" in tok or " hidden" in tok and tag != "div"
        if tag in BLOCK:
            block_count[0] = 0
        if tag == "a" and any(x[2] for x in stack):
            href = re.search(r'href="([^"#?:]+)\.html', tok)
            if href:   # already linked by hand in the text: do not link the same page again
                for l in ("fa", "en", flang):
                    used.setdefault(l, set()).add(href.group(1).split(".")[0])
        stack.append((tag, region, tag in BLOCK, never))
    return "".join(out)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    pages = sorted(p for p in ROOT.glob("*.html"))
    if mode == "--strip":
        n = 0
        for p in pages:
            s = p.read_text(encoding="utf-8")
            t = strip(s)
            if t != s:
                p.write_text(t, encoding="utf-8")
                n += 1
        print(f"links removed from {n} pages")
        return
    cfg, rx, dropped = load()
    AVOID[:] = [x.lower() for x in cfg.get("avoid", [])]
    skip = set(cfg["skip_sources"])
    existing = {p.name for p in pages}
    stats, changed = {}, 0
    for p in pages:
        s = p.read_text(encoding="utf-8")
        base = strip(s)
        new = base if p.name.split(".")[0] in skip else link_page(base, p.name, rx, existing, stats)
        if strip(new) != base:
            raise SystemExit(f"text changed on {p.name}; nothing written for it")
        if new != s:
            changed += 1
            if mode != "--report":
                p.write_text(new, encoding="utf-8")
    by_target = Counter(h for (_, h) in stats)
    by_page = Counter(n for (n, _) in stats)
    print(f"{len(stats)} links on {len(by_page)} pages ({changed} files changed); {len(dropped)} glossary terms unused")
    if mode == "--report":
        for (n, h), w in sorted(stats.items()):
            print(f"{n}\t{h}\t{w}")
        print("-- terms not found on their own target page:")
        for d in dropped:
            print("  ", *d)
        print("-- most linked:", by_target.most_common(25))


if __name__ == "__main__":
    main()
