#!/usr/bin/env python3
"""Write assets/img/favicon.svg: the polar-angle colour ring with a fixation dot.

The ring is eight gradient-stroked arcs (SVG has no conic gradient).
The dot is graphite, or white when the browser uses a dark colour scheme. With --png-source it prints a
variant for rendering PNG fallbacks: no media query, and a white halo around the dot so it shows on any ground.

Usage: python3 tools/make_favicon.py            (then render the PNGs, see README "Favicon")
"""
import math
import sys
from pathlib import Path

STOPS = ["#e5483b", "#ef8f2f", "#e3c53a", "#7cc14a", "#2db39b", "#2c86d1", "#5b5bd0", "#b04aa6"]  # --polar-wheel
OUTER, INNER, DOT = 15, 9.2, 3.4   # radii in a 32-unit box
def ring():
    """Eight arcs, one per pair of neighbouring wheel colours, each stroked with a linear gradient along its chord.
    Every arc runs a little past its end in its end colour, under the next arc, so no seam shows."""
    n = len(STOPS)
    r, w = (OUTER + INNER) / 2, OUTER - INNER
    defs, arcs = [], []
    for k in range(n):
        a0, a1 = math.radians(-90 + 360 * k / n), math.radians(-90 + 360 * (k + 1) / n)
        a2 = a1 + math.radians(6)
        x0, y0 = 16 + r * math.cos(a0), 16 + r * math.sin(a0)
        x1, y1 = 16 + r * math.cos(a1), 16 + r * math.sin(a1)
        x2, y2 = 16 + r * math.cos(a2), 16 + r * math.sin(a2)
        defs.append(f'<linearGradient id="g{k}" gradientUnits="userSpaceOnUse" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}">'
                    f'<stop stop-color="{STOPS[k]}"/><stop offset="1" stop-color="{STOPS[(k + 1) % n]}"/></linearGradient>')
        arcs.append(f'<path d="M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 0 1 {x2:.2f} {y2:.2f}" stroke="url(#g{k})"/>')
    # the first arc again, without its overrun, on top of the last arc's overrun
    a0, a1 = math.radians(-90), math.radians(-90 + 360 / n)
    arcs.append(f'<path d="M{16 + r * math.cos(a0):.2f} {16 + r * math.sin(a0):.2f}A{r:.2f} {r:.2f} 0 0 1 '
                f'{16 + r * math.cos(a1):.2f} {16 + r * math.sin(a1):.2f}" stroke="url(#g0)"/>')
    return f'<defs>{"".join(defs)}</defs><g fill="none" stroke-width="{w:.1f}">{"".join(arcs)}</g>'


def svg(png_source=False):
    ring_svg = ring()
    if png_source:
        dot = f'<circle cx="16" cy="16" r="{DOT}" fill="#1b2028" stroke="#fff" stroke-width="1.3"/>'
        style = ""
    else:
        dot = f'<circle class="d" cx="16" cy="16" r="{DOT}"/>'
        style = "<style>.d{fill:#1b2028}@media (prefers-color-scheme:dark){.d{fill:#fff}}</style>"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{style}{ring_svg}{dot}</svg>\n'


if __name__ == "__main__":
    if "--png-source" in sys.argv:
        sys.stdout.write(svg(png_source=True))
    else:
        out = Path(__file__).resolve().parent.parent / "assets" / "img" / "favicon.svg"
        out.write_text(svg())
        print(f"wrote {out} ({out.stat().st_size} bytes)")
