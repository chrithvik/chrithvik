#!/usr/bin/env python3
"""Neofetch-style info card SVG with staggered line reveal."""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

STATIC = bool(os.environ.get("STATIC"))

W, H = 980, 640
PAD = 22
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
C1 = "#58a6ff"
C2 = "#39d353"
C3 = "#f778ba"
C4 = "#d2a8ff"
C5 = "#ffa657"

LOGO = [
    ("OS", "GitHub Profile v2026", C1),
    ("Host", "chrithvik@github", C2),
    ("Kernel", "TypeScript · Python · Rust", C3),
    ("Uptime", "Building since Mar 2026", MUTED),
    ("Shell", "zsh + neovim", MUTED),
    ("DE", "Terminal aesthetic", MUTED),
    ("WM", "SVG + SMIL (no JS)", MUTED),
    ("Packages", "8 public repos", C4),
]

SECTIONS = [
    ("Now", "3D anatomy · STEM sims · open video", C1),
    ("Prev", "Medical viz · ed-tech · Flutter apps", C2),
    ("Stack", "React · Three.js · Tauri · Flutter", C3),
    ("Highlights", "Anatria-3D · Madar · OpenReel Video", C5),
]

LINE_H = 34
START_Y = TITLEBAR_H + PAD + 8
STAGGER = 0.12
SLIDE_DUR = 0.45

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    "<style>"
    f".ln{{opacity:0;animation:fade {SLIDE_DUR}s ease-out both}}"
    "@keyframes fade{0%{opacity:0;transform:translateX(12px)}100%{opacity:1;transform:translateX(0)}}"
    "@media (prefers-reduced-motion: reduce){.ln{opacity:1!important;transform:none!important;animation:none!important}}"
    "</style>",
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">chrithvik@github: ~$ neofetch</text>'
)

parts.append(
    f'<text x="{PAD}" y="{START_Y}" fill="{C1}" font-size="22" font-weight="700">'
    f"Ch Rithvik</text>"
)
parts.append(
    f'<text x="{PAD}" y="{START_Y + 28}" fill="{MUTED}" font-size="14">'
    f"Builder · 3D anatomy · STEM · open source</text>"
)

y = START_Y + 56
idx = 0
for key, val, color in LOGO:
    delay = idx * STAGGER
    idx += 1
    cls = "" if STATIC else f' class="ln" style="animation-delay:{delay:.2f}s"'
    parts.append(
        f"<g{cls}>"
        f'<text x="{PAD}" y="{y}" fill="{color}" font-size="15">{html.escape(key)}</text>'
        f'<text x="{PAD + 120}" y="{y}" fill="{INK}" font-size="15">{html.escape(val)}</text>'
        f"</g>"
    )
    y += LINE_H - 6

y += 8
for key, val, color in SECTIONS:
    delay = idx * STAGGER
    idx += 1
    cls = "" if STATIC else f' class="ln" style="animation-delay:{delay:.2f}s"'
    parts.append(
        f"<g{cls}>"
        f'<text x="{PAD}" y="{y}" fill="{color}" font-size="15" font-weight="700">{html.escape(key)}</text>'
        f'<text x="{PAD + 120}" y="{y}" fill="{INK}" font-size="15">{html.escape(val)}</text>'
        f"</g>"
    )
    y += LINE_H

parts.append(
    f'<text x="{PAD}" y="{H - PAD}" fill="{MUTED}" font-size="13">'
    f"https://github.com/chrithvik</text>"
)
parts.append("</svg>")

svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
