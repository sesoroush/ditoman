"""Download brand images listed in assets/fetch.txt (run by the fetch-assets workflow).

Each line:  dest/path.ext | URL | og
  og     -> open the page and save its og:image (or twitter:image)
  direct -> save the URL itself
  commons -> URL is a search phrase; save the top 4 Wikimedia Commons images (free licences),
             with their licence and author in dest.N.txt
For every page fetched in og mode, the list of <img> sources is saved next to it
(dest + ".imgs.txt") so exact product shots can be picked in a later run.
Files land under assets/brand-src/ and are reviewed before anything is used on the site.
"""
import pathlib, re, sys, urllib.request, urllib.parse, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "brand-src"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def get(url):
    import time
    url = urllib.parse.quote(url, safe=":/?&=%~#+,;@!$'()*|")
    ua = UA if "wikimedia" not in url else "DitomanBot/1.0 (https://ditoman.com; site images) python-urllib"
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "fa,en;q=0.8"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read(), r.headers.get("Content-Type", "")
            if "wikimedia" in url:
                time.sleep(1.5)
            return data
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and attempt < 4:
                time.sleep(10 * (attempt + 1))
                continue
            raise


def main():
    log = []
    for line in (ROOT / "assets" / "fetch.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        dest, url, mode = [x.strip() for x in line.split("|")]
        target = OUT / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            if mode == "emalls":
                pid = re.search(r"~id~(\d+)", url).group(1)
                page = get(url)[0].decode("utf-8", "ignore")
                cands = re.findall(r'(https?://files\.emalls\.ir/files/Products/[^"\'\s]*?/' + pid + r'/[^"\'\s]+?\.(?:jpe?g|png|webp))', page)
                n = 0
                for c in dict.fromkeys(cands):
                    full = re.sub(r"_thumb\d*", "", c)
                    for u in (full, c):
                        try:
                            data, ctype = get(u)
                        except Exception:
                            continue
                        t = target.parent / f"{target.name}.{n}.jpg"
                        t.write_bytes(data)
                        log.append(f"OK {t.relative_to(OUT)} {len(data)} {u}")
                        n += 1
                        break
                if not n:
                    log.append(f"NONE {dest} {url}")
                continue
            if mode == "offcode":
                host, code = url.split(":", 1)
                import json
                pr = json.loads(get(f"https://{host}/api/v2/product/{code}?fields=product_name,image_front_url,selected_images")[0]).get("product", {})
                im = pr.get("image_front_url")
                full = (((pr.get("selected_images") or {}).get("front") or {}).get("display") or {})
                im = next(iter(full.values()), im) if full else im
                im = re.sub(r"\.\d+\.jpg$", ".full.jpg", im or "")
                data, ctype = get(im)
                target.write_bytes(data)
                log.append(f"OK {dest} {len(data)} {pr.get('product_name')} {im}")
                continue
            if mode == "off":
                import json
                host, brand = url.split(":", 1)  # e.g. world.openfoodfacts.org:kalleh
                api = (f"https://{host}/api/v2/search?brands_tags={urllib.parse.quote(brand)}"
                       "&fields=code,product_name,brands,image_front_url,unique_scans_n&sort_by=unique_scans_n&page_size=12")
                res = json.loads(get(api)[0])
                n = 0
                for pr in res.get("products", []):
                    im = pr.get("image_front_url")
                    if not im:
                        continue
                    im = re.sub(r"\.\d+\.jpg$", ".full.jpg", im)
                    try:
                        data, ctype = get(im)
                    except Exception:
                        data, ctype = get(pr["image_front_url"])
                    t = target.parent / f"{target.name}.{n}.jpg"
                    t.write_bytes(data)
                    log.append(f"OK {t.relative_to(OUT)} {pr.get('product_name')} | {pr.get('brands')} | {pr.get('code')}")
                    n += 1
                if not n:
                    log.append(f"NONE {dest} {url}")
                continue
            if mode == "dk":
                import json
                api = "https://api.digikala.com/v1/search/?q=" + urllib.parse.quote(url)
                body, _ = get(api)
                (target.parent / (target.name + ".json")).write_bytes(body[:400000])
                res = json.loads(body)
                prods = ((res.get("data") or {}).get("products") or [])[:8]
                for i, pr in enumerate(prods):
                    im = (((pr.get("images") or {}).get("main") or {}).get("url") or [None])[0]
                    if not im:
                        continue
                    im = im.split("?")[0]
                    data, ctype = get(im)
                    t = target.parent / f"{target.name}.{i}.jpg"
                    t.write_bytes(data)
                    log.append(f"OK {t.relative_to(OUT)} {pr.get('title_fa')} | {pr.get('title_en')}")
                continue
            if mode == "commons":
                import json
                api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
                       "&gsrnamespace=6&gsrlimit=4&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1600&gsrsearch="
                       + urllib.parse.quote(url + " filetype:bitmap"))
                res = json.loads(get(api)[0])
                for i, pg in enumerate((res.get("query") or {}).get("pages", {}).values()):
                    ii = pg["imageinfo"][0]
                    meta = ii.get("extmetadata", {})
                    data, ctype = get(ii.get("thumburl") or ii["url"])
                    t = target.parent / f"{target.name}.{i}.jpg"
                    t.write_bytes(data)
                    (target.parent / f"{target.name}.{i}.txt").write_text(
                        f'{pg["title"]}\n{ii.get("descriptionurl")}\n'
                        f'{(meta.get("LicenseShortName") or {}).get("value")}\n'
                        f'{re.sub("<[^>]+>", "", (meta.get("Artist") or {}).get("value", ""))}', encoding="utf-8")
                    log.append(f"OK {t.relative_to(OUT)} {pg['title']}")
                continue
            if mode == "og":
                body, _ = get(url)
                page = body.decode("utf-8", "ignore")
                m = (re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page)
                     or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', page)
                     or re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)', page)
                     or re.search(r'"image"\s*:\s*\[?\s*"([^"]+\.(?:jpe?g|png|webp)[^"]*)"', page))
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
