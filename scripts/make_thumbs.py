#!/usr/bin/env python3
"""Make small copies of each story cover for the homepage cards.

social/<slug>/post.webp (or 1-cover.webp / ig1.webp), often 1-2 MB, gets two siblings:
  thumb.webp  240 px, for the compact story cards
  card.webp   900 px, for the featured report card
Existing copies are only rebuilt when post.webp is newer. Run from the repo root.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SIZES = {"thumb.webp": (240, 78), "card.webp": (900, 80)}

COVERS = ("post.webp", "1-cover.webp", "ig1.webp")  # first one found in each folder is the cover


def covers():
    for folder in sorted(p for p in (ROOT / "social").iterdir() if p.is_dir()):
        for name in COVERS:
            if (folder / name).exists():
                yield folder / name
                break


made = 0
for post in covers():
    for name, (width, quality) in SIZES.items():
        out = post.with_name(name)
        if out.exists() and out.stat().st_mtime >= post.stat().st_mtime:
            continue
        with Image.open(post) as im:
            im = im.convert("RGB")
            h = round(im.height * width / im.width)
            im.resize((width, h), Image.LANCZOS).save(out, "WEBP", quality=quality, method=6)
        made += 1
print(f"{made} images written")
