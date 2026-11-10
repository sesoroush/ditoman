"""Shrink the published site without any quality loss.

1. Every large published PNG (> 150 KB, not a logo or icon) that pages use gets a
   lossless WebP twin. The script checks pixel-for-pixel that the WebP decodes to the
   same image and keeps it only if it is at least 10% smaller.
2. Published references (HTML, CSS, JS, JSON, XML) are switched from .png to .webp.
   telegram/*.md posts are not touched: the Telegram workflow still sends the PNG.
3. The PNG originals, and images no page uses, are listed in an auto-managed block of
   _config.yml so GitHub Pages does not publish them. They stay in the repo as sources.

Run after adding new covers:  python3 scripts/optimize_images.py
"""
import io, os, re, sys, pathlib
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BEGIN, END = "  # BEGIN auto: optimize_images.py", "  # END auto: optimize_images.py"
MIN_BYTES = 150_000
KEEP = re.compile(r"(^|/)(logo[^/]*|ditoman-logo\.png|tmn-logo-\d+\.png|og-image\.\w+|favicon[^/]*)$")
# folders rebuilt by scheduled workflows keep their PNGs (their JSON is regenerated)
SKIP = ("calendar/", "market/")
TEXT_EXT = (".html", ".css", ".js", ".json", ".xml", ".webmanifest")


def manual_excludes():
    out, inside = [], False
    for line in (ROOT / "_config.yml").read_text().splitlines():
        if line.startswith(BEGIN): inside = True; continue
        if line.startswith(END): inside = False; continue
        m = re.match(r'\s*-\s*"?([^"]+)"?\s*$', line)
        if m and not inside: out.append(m.group(1))
    return out


def published(excl):
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        r = p.relative_to(ROOT).as_posix()
        if r.startswith((".", "_")) or "/." in r: continue
        if any(r == e or r.startswith(e.rstrip("/") + "/") for e in excl): continue
        yield r


def to_webp(png):
    im = Image.open(png)
    im.load()
    if im.mode not in ("RGB", "RGBA"): im = im.convert("RGBA")
    buf = io.BytesIO()
    im.save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
    data = buf.getvalue()
    back = Image.open(io.BytesIO(data)).convert(im.mode)
    if not np.array_equal(np.asarray(back), np.asarray(im)):
        return png, None, "pixels differ"
    if len(data) > 0.9 * os.path.getsize(png):
        return png, None, "not smaller"
    pathlib.Path(png[:-4] + ".webp").write_bytes(data)
    return png, len(data), "ok"


def main():
    excl = manual_excludes()
    files = list(published(excl))
    texts = {f: (ROOT / f).read_text(encoding="utf-8") for f in files
             if f.endswith(TEXT_EXT) and not f.startswith("telegram/") or f == "telegram/feed.json"}
    blob = "\n".join(texts.values())

    def used(f):
        return f in blob or os.path.basename(f) in blob

    cands = [f for f in files if f.endswith(".png") and not KEEP.search(f) and not f.startswith(SKIP)
             and os.path.getsize(f) > MIN_BYTES and used(f)]
    todo = [f for f in cands if not os.path.exists(f[:-4] + ".webp")]
    with ProcessPoolExecutor() as ex:
        for png, size, why in ex.map(to_webp, todo):
            print(f"{why:13} {png}" + (f"  {os.path.getsize(png)/1e6:.2f} -> {size/1e6:.2f} MB" if size else ""))
    converted = [f for f in cands if os.path.exists(f[:-4] + ".webp")]

    # switch references (full path and bare file name) in published text files
    for f, s in texts.items():
        if f.startswith(SKIP): continue
        o = s
        for png in converted:
            web = png[:-4] + ".webp"
            s = s.replace(png, web)
            b = os.path.basename(png)
            if b in s and os.path.dirname(f) == os.path.dirname(png):
                s = re.sub(r'(?<![\w/.-])' + re.escape(b), os.path.basename(web), s)
        if s != o:
            (ROOT / f).write_text(s, encoding="utf-8")
            print("updated", f)

    blob = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in texts)
    unused = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))
              and not KEEP.search(f) and not f.startswith(SKIP) and not used(f)]
    hidden = sorted(set(converted) | set(unused))

    cfg = (ROOT / "_config.yml").read_text().splitlines()
    if BEGIN in cfg:
        a, b = cfg.index(BEGIN), cfg.index(END)
        cfg = cfg[:a] + cfg[b + 1:]
    block = [BEGIN, "  # PNG originals with a lossless WebP twin, and images no page uses"] + \
            [f'  - "{h}"' for h in hidden] + [END]
    i = max(i for i, l in enumerate(cfg) if l.strip().startswith("- "))
    cfg = cfg[:i + 1] + block + cfg[i + 1:]
    (ROOT / "_config.yml").write_text("\n".join(cfg) + "\n")

    after = sum(os.path.getsize(f) for f in published(manual_excludes() + hidden))
    print(f"{len(converted)} WebP twins, {len(hidden)} files kept out of the site; published size {after/1e6:.1f} MB")


if __name__ == "__main__":
    main()
