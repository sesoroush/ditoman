"""Download brand images listed in assets/fetch.txt (run by the fetch-assets workflow).

Each line:  dest/path.ext | URL | og
  og     -> open the page and save its og:image (or twitter:image)
  direct -> save the URL itself
For every page fetched in og mode, the list of <img> sources is saved next to it
(dest + ".imgs.txt") so exact product shots can be picked in a later run.
Files land under assets/brand-src/ and are reviewed before anything is used on the site.
"""
import pathlib, re, sys, urllib.request, urllib.parse, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "brand-src"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fa,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read(), r.headers.get("Content-Type", "")


def main():
    log = []
    for line in (ROOT / "assets" / "fetch.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        dest, url, mode = [x.strip() for x in line.split("|")]
        target = OUT / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            if mode == "og":
                body, _ = get(url)
                page = body.decode("utf-8", "ignore")
                m = (re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page)
                     or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', page)
                     or re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)', page))
                imgs = sorted(set(urllib.parse.urljoin(url, html.unescape(s)) for s in
                                  re.findall(r'<img[^>]+(?:data-src|src)=["\']([^"\']+)', page)))
                (target.parent / (target.name + ".imgs.txt")).write_text("\n".join(imgs), encoding="utf-8")
                if not m:
                    log.append(f"NO-OG {dest} {url}")
                    continue
                url = urllib.parse.urljoin(url, html.unescape(m.group(1)))
            data, ctype = get(url)
            target.write_bytes(data)
            log.append(f"OK {dest} {len(data)} {ctype} {url}")
        except Exception as ex:  # keep going; the log says what failed
            log.append(f"FAIL {dest} {url} {ex}")
    (OUT / "log.txt").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
