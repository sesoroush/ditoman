#!/usr/bin/env python3
"""Icons for the follow row (join-bar.js): img/social/<id>.png, 104 px square (52 px at 2x).

Sources are the apps' own icons fetched by the fetch-assets workflow into assets/brand-src/social/.
A plain background around an icon (white or black) is made transparent from the corners inward,
then the whole icon is fitted inside the square without cropping.
Run from the repo root: python3 scripts/make_social_icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "brand-src" / "social"
OUT = ROOT / "img" / "social"
SIZE = 104
ICONS = {
    "telegram": "telegram.png",
    "bale": "bale.png",
    "rubika": "rubika-commons.png.3.jpg",  # Wikimedia Commons, File:Rubika_new_icon.png
    "eitaa": "eitaa.png",
    "instagram": "instagram.png",
}


def clear_background(im):
    im = im.convert("RGBA")
    w, h = im.size
    corner = im.getpixel((0, 0))
    if corner[3] == 0:
        return im
    key = (255, 0, 255, 0)
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(im, xy, key, thresh=40)
    px = im.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == key:
                px[x, y] = (0, 0, 0, 0)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in ICONS.items():
        im = clear_background(Image.open(SRC / src))
        box = im.getbbox()
        if box:
            im = im.crop(box)  # trims only the now-transparent margin
        im.thumbnail((SIZE, SIZE), Image.LANCZOS)
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2), im)
        canvas.save(OUT / f"{name}.png", optimize=True)
        print(name, im.size, (OUT / f"{name}.png").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
