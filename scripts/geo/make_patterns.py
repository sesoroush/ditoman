#!/usr/bin/env python3
"""Generate Ditoman's geometric ornaments as small, exact SVG files.

assets/geo/field.svg    Pattern A: seamless tile of eight-pointed stars (شمسه هشت‌پر)
                        joined by thin lines, with smaller stars at the tile edges.
assets/geo/rosette.svg  Pattern B: one large eight-pointed rosette for section edges,
                        with a faint hexagon-and-crossbar detail at its centre that
                        borrows the line language of the Ditoman mark (not the mark itself).

Both are drawn in a single colour and used as CSS masks, so the page decides the
colour and opacity. Run from the repo root: python3 scripts/geo/make_patterns.py
"""
from math import cos, sin, pi
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "assets" / "geo"


def pt(cx, cy, r, deg):
    a = deg * pi / 180
    return (cx + r * cos(a), cy + r * sin(a))


def fmt(p):
    return f"{p[0]:.2f},{p[1]:.2f}"


def poly(points):
    return '<polygon points="' + " ".join(fmt(p) for p in points) + '"/>'


def line(a, b):
    return f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}"/>'


def khatam(cx, cy, r, rot=0):
    """Eight-pointed star drawn as two overlapping squares, as in the classic khatam."""
    a = [pt(cx, cy, r, rot + k * 90) for k in range(4)]
    b = [pt(cx, cy, r, rot + 45 + k * 90) for k in range(4)]
    return [poly(a), poly(b)]


def octagram(cx, cy, r, step=3, rot=22.5):
    v = [pt(cx, cy, r, rot + k * 45) for k in range(8)]
    order, i = [], 0
    for _ in range(8):
        order.append(v[i])
        i = (i + step) % 8
    return poly(order)


def octagon(cx, cy, r, rot=22.5):
    return poly([pt(cx, cy, r, rot + k * 45) for k in range(8)])


def star(cx, cy, R, inner=0.56, rot=0):
    """Eight-pointed star outline: sixteen points alternating between tip and waist."""
    pts = []
    for k in range(16):
        pts.append(pt(cx, cy, R if k % 2 == 0 else R * inner, rot + k * 22.5))
    return poly(pts)


def field(T=120):
    c = T / 2
    R = 0.30 * T                     # main star
    parts = []
    big = [(c, c), (0, 0), (T, 0), (0, T), (T, T)]
    for (x, y) in big:
        parts.append(star(x, y, R))
        parts.append(star(x, y, R * 0.42, inner=0.62, rot=22.5))   # smaller star inside: a change of scale
    # diagonal ties: tip of the centre star to the facing tip of each corner star
    for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        a = (c + sx * R * 0.7071, c + sy * R * 0.7071)
        corner = (c + sx * c, c + sy * c)
        b = (corner[0] - sx * R * 0.7071, corner[1] - sy * R * 0.7071)
        parts.append(line(a, b))
    # axial ties meet at the edge midpoints and form a small open lozenge (the cross)
    d = 0.08 * T
    for (mx, my) in [(c, 0), (c, T), (0, c), (T, c)]:
        parts.append(poly([(mx - d, my), (mx, my - d), (mx + d, my), (mx, my + d)]).replace("/>", ' stroke-opacity=".6"/>'))
    for (x, y) in big:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            a = (x + dx * R, y + dy * R)
            b = (x + dx * (c - d), y + dy * (c - d))
            if all(-1 <= v <= T + 1 for v in (*a, *b)):
                parts.append(line(a, b).replace("/>", ' stroke-opacity=".6"/>'))
    body = "".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" width="{T}" height="{T}">'
            f'<g fill="none" stroke="#000" stroke-width="0.8" stroke-linejoin="round">{body}</g></svg>')


def rosette(S=600):
    c = S / 2
    p = []
    p.append(f'<circle cx="{c}" cy="{c}" r="{0.485 * S:.2f}"/>')
    p.append(f'<circle cx="{c}" cy="{c}" r="{0.47 * S:.2f}" stroke-opacity=".5"/>')
    p.append(octagon(c, c, 0.44 * S))
    p += khatam(c, c, 0.40 * S)
    p.append(star(c, c, 0.40 * S, inner=0.5, rot=22.5))
    p.append(octagon(c, c, 0.20 * S, rot=0))
    p += khatam(c, c, 0.17 * S, rot=22.5)
    p.append(f'<circle cx="{c}" cy="{c}" r="{0.105 * S:.2f}"/>')
    # sixteen rays joining the inner and outer stars
    for k in range(0, 16, 2):
        a = pt(c, c, 0.11 * S, k * 22.5)
        b = pt(c, c, (0.40 if k % 2 == 0 else 0.30) * S, k * 22.5)
        p.append(line(a, b).replace("/>", ' stroke-opacity=".55"/>'))
    # outer connectors: from the big star's tips to the outer ring
    for k in range(8):
        p.append(line(pt(c, c, 0.40 * S, k * 45), pt(c, c, 0.485 * S, k * 45)))
    # brand detail: a hexagon with a crossbar and diagonals, in the spirit of the
    # Ditoman mark's line work. Small, centred, and deliberately not the logo.
    h = 0.075 * S
    hexv = [pt(c, c, h, -90 + k * 60) for k in range(6)]
    p.append('<g stroke-opacity=".8">' + poly(hexv))
    top_l, top_r = (c - h * 0.62, c - h * 0.42), (c + h * 0.62, c - h * 0.42)
    p.append(line(top_l, top_r))
    p.append(line((c, c - h * 0.42), (c, c + h * 0.92)))
    p.append(line(hexv[4], (c, c + h * 0.92)))
    p.append(line(hexv[2], (c, c + h * 0.92)))
    p.append("</g>")
    body = "".join(p)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<g fill="none" stroke="#000" stroke-width="1" stroke-linejoin="round">{body}</g></svg>')


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "field.svg").write_text(field(), encoding="utf-8")
    (OUT / "rosette.svg").write_text(rosette(), encoding="utf-8")
    for f in ("field.svg", "rosette.svg"):
        print(f, (OUT / f).stat().st_size, "bytes")
