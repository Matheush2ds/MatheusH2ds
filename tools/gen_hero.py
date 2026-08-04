#!/usr/bin/env python3
"""Gera assets/hero.svg - banner animado custom (SMIL puro, sem JS)."""
import math, random, os

W, H = 1200, 384
BG      = "#0d1117"
BORDER  = "#30363d"
PRIMARY = "#58a6ff"
LIGHT   = "#a5d6ff"
DEEP    = "#1f6feb"
MUTED   = "#8b949e"
TEXT    = "#c9d1d9"

VX, VY = W / 2, 258.0          # vanishing point
BY     = float(H)              # floor bottom
HALFW  = 1700.0
ROWS   = 11
FLOOR_DUR = 7.0
POW    = 2.7

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
  f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  f'aria-label="Matheus Henrique - Back-End Developer">')

# ---------------------------------------------------------------- defs
A('<defs>')
A(f'''
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="#0d1117"/>
    <stop offset="55%"  stop-color="#0f1620"/>
    <stop offset="100%" stop-color="#0b1018"/>
  </linearGradient>

  <radialGradient id="vignette" cx="50%" cy="42%" r="72%">
    <stop offset="0%"   stop-color="{DEEP}" stop-opacity="0.22"/>
    <stop offset="55%"  stop-color="{DEEP}" stop-opacity="0.06"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.35"/>
  </radialGradient>

  <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0%"   stop-color="{DEEP}"/>
    <stop offset="35%"  stop-color="{PRIMARY}"/>
    <stop offset="50%"  stop-color="#ffffff"/>
    <stop offset="65%"  stop-color="{LIGHT}"/>
    <stop offset="100%" stop-color="{DEEP}"/>
    <animateTransform attributeName="gradientTransform" type="translate"
      values="-1 0; 1 0; -1 0" keyTimes="0;0.5;1" dur="7s" repeatCount="indefinite"/>
  </linearGradient>

  <linearGradient id="ruleGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="{PRIMARY}" stop-opacity="0"/>
    <stop offset="50%"  stop-color="{LIGHT}"   stop-opacity="1"/>
    <stop offset="100%" stop-color="{PRIMARY}" stop-opacity="0"/>
  </linearGradient>

  <linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#000" stop-opacity="1"/>
    <stop offset="18%"  stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>

  <filter id="glowSoft" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="9" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/></feMerge>
  </filter>
  <filter id="glowTight" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="2.4"/>
  </filter>

  <clipPath id="frameClip">
    <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/>
  </clipPath>
  <clipPath id="floorClip">
    <rect x="0" y="{VY}" width="{W}" height="{H-VY}"/>
  </clipPath>
''')
A('</defs>')

A('<g clip-path="url(#frameClip)">')
A(f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>')
A(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# ------------------------------------------------- perspective floor
A('<g clip-path="url(#floorClip)">')

# rays from the vanishing point
A(f'<g stroke="{PRIMARY}" stroke-width="1" fill="none">')
for i in range(-13, 14):
    ex = VX + i * 118
    op = 0.16 - abs(i) * 0.0085
    if op <= 0.012:
        continue
    A(f'<line x1="{VX:.0f}" y1="{VY:.0f}" x2="{ex:.0f}" y2="{BY:.0f}" opacity="{op:.3f}">'
      f'<animate attributeName="opacity" values="{op:.3f};{op*2.1:.3f};{op:.3f}" '
      f'dur="{4.5 + abs(i) * 0.22:.1f}s" repeatCount="indefinite"/></line>')
A('</g>')

# horizontal rows flowing toward the viewer
for i in range(ROWS):
    t0 = (i + 1) / ROWS
    t1 = t0 + 1.0 / ROWS
    y0 = VY + (BY - VY) * (t0 ** POW)
    y1 = VY + (BY - VY) * (t1 ** POW)
    xa0, xb0 = VX - HALFW * t0, VX + HALFW * t0
    xa1, xb1 = VX - HALFW * t1, VX + HALFW * t1
    dly = -FLOOR_DUR * (i / ROWS)
    A(f'<line x1="{xa0:.0f}" y1="{y0:.1f}" x2="{xb0:.0f}" y2="{y0:.1f}" '
      f'stroke="{PRIMARY}" stroke-width="1.1" opacity="0.2">'
      f'<animate attributeName="y1" values="{y0:.1f};{y1:.1f}" dur="{FLOOR_DUR}s" begin="{dly:.2f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="y2" values="{y0:.1f};{y1:.1f}" dur="{FLOOR_DUR}s" begin="{dly:.2f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="x1" values="{xa0:.0f};{xa1:.0f}" dur="{FLOOR_DUR}s" begin="{dly:.2f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="x2" values="{xb0:.0f};{xb1:.0f}" dur="{FLOOR_DUR}s" begin="{dly:.2f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0;0.30;0.16;0.05" keyTimes="0;0.25;0.7;1" '
      f'dur="{FLOOR_DUR}s" begin="{dly:.2f}s" repeatCount="indefinite"/>'
      f'</line>')

# horizon glow
A(f'<rect x="0" y="{VY-1:.0f}" width="{W}" height="2" fill="{LIGHT}" opacity="0.5" filter="url(#glowSoft)"/>')
A('</g>')

# ------------------------------------------------- constellation
rnd = random.Random(20260728)
NODES = 46
pts = []
tries = 0
while len(pts) < NODES and tries < 4000:
    tries += 1
    x = rnd.uniform(24, W - 24)
    y = rnd.uniform(18, VY - 8)
    # keep the headline area breathable
    if 214 < x < 986 and 84 < y < 252:
        continue
    if all((x - px) ** 2 + (y - py) ** 2 > 3400 for px, py in pts):
        pts.append((x, y))

A('<g>')
# edges
A(f'<g stroke="{PRIMARY}" fill="none" stroke-width="0.7">')
edges = 0
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        d = math.dist(pts[i], pts[j])
        if d < 132:
            op = 0.30 * (1 - d / 132)
            per = rnd.uniform(3.4, 7.2)
            A(f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" opacity="{op:.3f}">'
              f'<animate attributeName="opacity" values="{op*0.25:.3f};{op:.3f};{op*0.25:.3f}" '
              f'dur="{per:.2f}s" begin="{rnd.uniform(0,per):.2f}s" repeatCount="indefinite"/></line>')
            edges += 1
A('</g>')

# nodes
for (x, y) in pts:
    r = rnd.choice([1.2, 1.5, 1.8, 2.3])
    per = rnd.uniform(2.6, 6.0)
    bg_ = rnd.uniform(0, per)
    A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{LIGHT}" opacity="0.5">'
      f'<animate attributeName="opacity" values="0.16;0.95;0.16" dur="{per:.2f}s" begin="{bg_:.2f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="r" values="{r};{r*1.7:.2f};{r}" dur="{per:.2f}s" begin="{bg_:.2f}s" repeatCount="indefinite"/>'
      f'</circle>')

# a few bright travelling packets across the constellation
for k in range(5):
    i = rnd.randrange(len(pts))
    j = rnd.randrange(len(pts))
    (x1, y1), (x2, y2) = pts[i], pts[j]
    dur = rnd.uniform(5.5, 9.0)
    A(f'<circle r="2.2" fill="#ffffff" opacity="0.9" filter="url(#glowTight)">'
      f'<animate attributeName="cx" values="{x1:.0f};{x2:.0f}" dur="{dur:.1f}s" begin="{k*1.6:.1f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="cy" values="{y1:.0f};{y2:.0f}" dur="{dur:.1f}s" begin="{k*1.6:.1f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0;0.95;0" dur="{dur:.1f}s" begin="{k*1.6:.1f}s" repeatCount="indefinite"/>'
      f'</circle>')

A(f'<animateTransform attributeName="transform" type="rotate" '
  f'values="-0.6 {W/2} {VY/2}; 0.6 {W/2} {VY/2}; -0.6 {W/2} {VY/2}" dur="26s" repeatCount="indefinite"/>')
A('</g>')

# ------------------------------------------------- headline
NAME = "MATHEUS HENRIQUE"
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace"
SANS = "Segoe UI,Helvetica Neue,Arial,sans-serif"

A(f'<g text-anchor="middle">')
# glow ghost
A(f'<text x="{W/2}" y="134" font-family="{SANS}" font-size="62" font-weight="800" '
  f'letter-spacing="3" fill="{PRIMARY}" opacity="0.35" filter="url(#glowSoft)">{NAME}</text>')
# main
A(f'<text x="{W/2}" y="134" font-family="{SANS}" font-size="62" font-weight="800" '
  f'letter-spacing="3" fill="url(#nameGrad)">{NAME}</text>')

# animated rule
A(f'<line x1="330" y1="160" x2="870" y2="160" stroke="url(#ruleGrad)" stroke-width="2" '
  f'stroke-dasharray="540" stroke-dashoffset="540">'
  f'<animate attributeName="stroke-dashoffset" values="540;0;0;540" keyTimes="0;0.35;0.8;1" '
  f'dur="8s" repeatCount="indefinite"/></line>')

A(f'<text x="{W/2}" y="191" font-family="{MONO}" font-size="15" letter-spacing="6.5" '
  f'fill="{MUTED}">BACK-END DEVELOPER &#183; SYSTEMS ANALYST</text>')

# status chip
chip_y = 210
A(f'<g>')
A(f'<rect x="{W/2-142:.0f}" y="{chip_y}" width="284" height="32" rx="16" '
  f'fill="#161b22" fill-opacity="0.85" stroke="{BORDER}"/>')
A(f'<circle cx="{W/2-118:.0f}" cy="{chip_y+16}" r="4.5" fill="#3fb950">'
  f'<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>')
A(f'<circle cx="{W/2-118:.0f}" cy="{chip_y+16}" r="4.5" fill="#3fb950" opacity="0.6" filter="url(#glowTight)">'
  f'<animate attributeName="r" values="4.5;10;4.5" dur="2.2s" repeatCount="indefinite"/>'
  f'<animate attributeName="opacity" values="0.55;0;0.55" dur="2.2s" repeatCount="indefinite"/></circle>')
A(f'<text x="{W/2+14:.0f}" y="{chip_y+21}" font-family="{MONO}" font-size="12.5" '
  f'letter-spacing="1.6" fill="{TEXT}">BSc CS &#183; studying AI</text>')
A('</g>')
A('</g>')

# ------------------------------------------------- corner brackets
for (cx, cy, sx, sy) in [(22, 22, 1, 1), (W-22, 22, -1, 1), (22, H-22, 1, -1), (W-22, H-22, -1, -1)]:
    A(f'<path d="M {cx} {cy+sy*26} L {cx} {cy} L {cx+sx*26} {cy}" fill="none" '
      f'stroke="{PRIMARY}" stroke-width="1.6" opacity="0.4" stroke-linecap="round">'
      f'<animate attributeName="opacity" values="0.18;0.8;0.18" dur="4s" repeatCount="indefinite"/></path>')

A(f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.5"/>')
A('</g>')
A('</svg>')

svg = "\n".join(out)
os.makedirs("assets", exist_ok=True)
with open("assets/hero.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"hero.svg  nodes={len(pts)} edges={edges} bytes={len(svg)}")
