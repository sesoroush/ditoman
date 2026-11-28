#!/usr/bin/env python3
"""Fetch a jacket image for every book in data/books/catalog.json (runs on the GitHub runner).

For each book without assets/books/<slug>.jpg: try the ISBNs listed in the catalog (Open Library, then
Google Books), then a title and author search in Open Library. What was matched goes to
data/books/covers.json so every image can be reviewed before it is used on a banner.
A file placed by hand at assets/books/<slug>.jpg is never replaced.
"""
import io, json, pathlib, re, sys, time, urllib.parse, urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "assets" / "books"
LOG = ROOT / "data" / "books" / "covers.json"
UA = "Mozilla/5.0 (compatible; book-library-covers/1.0)"


def get(url, tries=3):
    err = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as ex:  # noqa: BLE001
            err = ex
            time.sleep(3 * (i + 1))
    print("  failed", url[:110], err)
    return None


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def good(data, min_w=260):
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:  # noqa: BLE001
        return None
    w, h = im.size
    if w < min_w or h < w * 1.05 or h > w * 2.2:
        return None
    return im.convert("RGB")


def surname(authors):
    first = re.split(r",| et al| and |&", authors)[0].strip()
    if first.lower() in ("world bank", "the core team"):
        return ""
    return first.split()[-1] if first else ""


def by_isbn(book):
    """Exact edition first: the ISBNs listed for the book in the catalog."""
    for isbn in book.get("isbn", []):
        data = get(f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false", tries=1)
        im = good(data) if data else None
        if im:
            return im, {"source": "openlibrary-isbn", "id": isbn, "title": book["en"], "author": book["authors_en"], "year": book["year"]}
        for zoom in (3, 2):
            data = get(f"https://books.google.com/books/content?vid=ISBN{isbn}&printsec=frontcover&img=1&zoom={zoom}", tries=1)
            im = good(data, 300) if data else None
            if im:
                return im, {"source": "googlebooks-isbn", "id": isbn, "zoom": zoom, "title": book["en"], "author": book["authors_en"], "year": book["year"]}
    return None


def open_library(book, skip=()):
    q = {"title": book["en"], "limit": "20", "fields": "title,author_name,cover_i,first_publish_year,edition_count"}
    a = surname(book["authors_en"])
    if a:
        q["author"] = a
    raw = get("https://openlibrary.org/search.json?" + urllib.parse.urlencode(q))
    if not raw:
        return None
    want = norm(book["en"])
    docs = [d for d in json.loads(raw).get("docs", []) if d.get("cover_i") and d["cover_i"] not in skip]
    exact = [d for d in docs if norm(d.get("title", "")) == want]
    if a:  # a looser title match is only trusted when the author matches too
        exact = exact or [d for d in docs if norm(d.get("title", "")).startswith(want) and a.lower() in " ".join(d.get("author_name") or []).lower()]
    for d in sorted(exact, key=lambda d: -d.get("edition_count", 0))[:6]:
        data = get(f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg")
        im = good(data) if data else None
        if im:
            return im, {"source": "openlibrary", "id": d["cover_i"], "title": d.get("title"),
                        "author": (d.get("author_name") or [""])[0], "year": d.get("first_publish_year")}
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {}
    books = json.loads((ROOT / "data" / "books" / "catalog.json").read_text(encoding="utf-8"))["books"]
    only = set(sys.argv[1:])
    for b in books:
        dest = OUT / f"{b['slug']}.jpg"
        if dest.exists() or (only and b["slug"] not in only):
            continue
        skip = set((log.get(b["slug"]) or {}).get("rejected_ids", []))
        found = by_isbn(b) or open_library(b, skip)
        if not found:
            log[b["slug"]] = {"source": None, "rejected_ids": sorted(skip)}
            print("MISSING", b["n"], b["en"])
            continue
        im, meta = found
        im.save(dest, "JPEG", quality=92)
        meta.update(w=im.width, h=im.height)
        log[b["slug"]] = meta
        print("ok", b["n"], b["en"], "|", meta["source"], meta["title"], im.size)
        time.sleep(1)
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
