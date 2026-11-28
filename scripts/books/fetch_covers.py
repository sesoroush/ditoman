#!/usr/bin/env python3
"""Fetch a jacket image for every book in data/books/catalog.json (runs on the GitHub runner).

For each book without assets/books/<slug>.jpg: look the title up in Open Library, then in
Google Books, and save the largest front cover found. What was matched goes to
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


def open_library(book):
    q = {"title": book["en"], "limit": "20", "fields": "title,author_name,cover_i,first_publish_year,edition_count"}
    a = surname(book["authors_en"])
    if a:
        q["author"] = a
    raw = get("https://openlibrary.org/search.json?" + urllib.parse.urlencode(q))
    if not raw:
        return None
    want = norm(book["en"])
    docs = [d for d in json.loads(raw).get("docs", []) if d.get("cover_i")]
    exact = [d for d in docs if norm(d.get("title", "")) == want] or [d for d in docs if norm(d.get("title", "")).startswith(want)]
    for d in sorted(exact, key=lambda d: -d.get("edition_count", 0))[:4]:
        data = get(f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg")
        im = good(data) if data else None
        if im:
            return im, {"source": "openlibrary", "id": d["cover_i"], "title": d.get("title"),
                        "author": (d.get("author_name") or [""])[0], "year": d.get("first_publish_year")}
    return None


def google_books(book):
    q = f'intitle:"{book["en"]}"'
    a = surname(book["authors_en"])
    if a:
        q += f" inauthor:{a}"
    raw = get("https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({"q": q, "maxResults": "10", "printType": "books"}))
    if not raw:
        return None
    want = norm(book["en"])
    for item in json.loads(raw).get("items", []):
        v = item.get("volumeInfo", {})
        if not norm(v.get("title", "")).startswith(want[:40]):
            continue
        if not v.get("imageLinks"):
            continue
        for zoom in (3, 2, 1):
            data = get(f"https://books.google.com/books/content?id={item['id']}&printsec=frontcover&img=1&zoom={zoom}", tries=1)
            im = good(data, 300 if zoom > 1 else 120) if data else None
            if im:
                return im, {"source": "googlebooks", "id": item["id"], "zoom": zoom, "title": v.get("title"),
                            "author": (v.get("authors") or [""])[0], "year": (v.get("publishedDate") or "")[:4]}
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
        found = open_library(b)
        if not found or found[0].width < 300:
            alt = google_books(b)
            if alt and (not found or alt[0].width > found[0].width):
                found = alt
        if not found:
            log[b["slug"]] = {"source": None}
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
