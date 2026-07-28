#!/usr/bin/env python3
"""Gera assets/stack-3d.svg - cubo 3D de verdade: projecao em perspectiva
calculada frame a frame em Python e animada com SMIL (sem JS)."""
import math, os

W, H = 620, 620
CX, CY = W / 2, 288.0
SCALE = 107.0
CAM_D = 4.15                 # distancia da camera
FOCAL = 3.45
FRAMES = 72
DUR = 20.0

BODY   = "#0d1117"
BORDER = "#30363d"
PRIM   = "#58a6ff"
LIGHT  = "#a5d6ff"
DEEP   = "#1f6feb"
MUTED  = "#8b949e"
MONO   = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace"

# vertices do cubo (half-size 1)
V = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
     (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]

# faces: (indices ccw, normal, label)
FACES = [
    ([4, 5, 6, 7], (0, 0, 1),  "JAVA"),
    ([1, 0, 3, 2], (0, 0, -1), "PYTHON"),
    ([5, 1, 2, 6], (1, 0, 0),  "SPRING"),
    ([0, 4, 7, 3], (-1, 0, 0), "NODE.JS"),
    ([4, 0, 1, 5], (0, -1, 0), "DOCKER"),
    ([3, 7, 6, 2], (0, 1, 0),  "POSTGRES"),
]


def rot(p, yaw, pitch):
    x, y, z = p
    cy_, sy_ = math.cos(yaw), math.sin(yaw)
    x, z = x * cy_ + z * sy_, -x * sy_ + z * cy_
    cx_, sx_ = math.cos(pitch), math.sin(pitch)
    y, z = y * cx_ - z * sx_, y * sx_ + z * cx_
    return (x, y, z)


def proj(p):
    x, y, z = p
    k = FOCAL / (CAM_D - z)
    return (CX + x * k * SCALE, CY - y * k * SCALE, z)


# ------------------------------------------------ pre-calculo dos frames
poly_pts   = [[] for _ in FACES]
poly_op    = [[] for _ in FACES]
lbl_pos    = [[] for _ in FACES]
lbl_op     = [[] for _ in FACES]
lbl_size   = [[] for _ in FACES]
vert_pos   = [[] for _ in V]
vert_r     = [[] for _ in V]

for fi in range(FRAMES + 1):                    # +1 fecha o loop
    t = (fi % FRAMES) / FRAMES
    yaw = 2 * math.pi * t
    pitch = math.radians(17 + 11 * math.sin(2 * math.pi * t))

    rv = [rot(v, yaw, pitch) for v in V]
    pv = [proj(v) for v in rv]

    for i, (x, y, z) in enumerate(pv):
        vert_pos[i].append((x, y))
        depth = (z + 1.75) / 3.5
        vert_r[i].append(1.8 + 2.4 * depth)

    for k, (idx, n, label) in enumerate(FACES):
        rn = rot(n, yaw, pitch)
        c3 = tuple(sum(rv[i][a] for i in idx) / 4 for a in range(3))
        view = (-c3[0], -c3[1], CAM_D - c3[2])
        vl = math.sqrt(sum(c * c for c in view)) or 1.0
        ndv = sum(rn[a] * view[a] / vl for a in range(3))

        poly_pts[k].append(" ".join(f"{pv[i][0]:.1f},{pv[i][1]:.1f}" for i in idx))
        poly_op[k].append(0.20 if ndv > 0 else 0.045)

        pc = proj(c3)
        lbl_pos[k].append((pc[0], pc[1]))
        lbl_op[k].append(round(max(0.0, ndv) ** 1.35, 3))
        lbl_size[k].append(round(17.0 * (FOCAL / (CAM_D - c3[2])) * 0.92, 2))

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="Cubo 3D com a stack de tecnologias">')

A('<defs>')
A(f'''
  <radialGradient id="cAura" cx="50%" cy="46%" r="52%">
    <stop offset="0%"   stop-color="{DEEP}" stop-opacity="0.30"/>
    <stop offset="60%"  stop-color="{DEEP}" stop-opacity="0.07"/>
    <stop offset="100%" stop-color="{BODY}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="cFace" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="{LIGHT}"/>
    <stop offset="50%"  stop-color="{PRIM}"/>
    <stop offset="100%" stop-color="{DEEP}"/>
  </linearGradient>
  <linearGradient id="cRing" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="{PRIM}" stop-opacity="0"/>
    <stop offset="50%"  stop-color="{LIGHT}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{PRIM}" stop-opacity="0"/>
  </linearGradient>
  <filter id="cGlow" x="-70%" y="-70%" width="240%" height="240%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
  <filter id="cGlowS" x="-90%" y="-90%" width="280%" height="280%">
    <feGaussianBlur stdDeviation="1.9"/>
  </filter>
''')
A('</defs>')

A(f'<rect width="{W}" height="{H}" fill="{BODY}" rx="16"/>')
A(f'<rect width="{W}" height="{H}" fill="url(#cAura)" rx="16"/>')

# base holografica
A(f'<g opacity="0.55">')
for i, ry in enumerate([12, 22, 34, 48]):
    A(f'<ellipse cx="{CX}" cy="498" rx="{60 + i*54}" ry="{ry}" fill="none" stroke="{PRIM}" '
      f'stroke-width="1" opacity="{0.34 - i*0.06:.2f}">'
      f'<animate attributeName="opacity" values="0.05;{0.40 - i*0.06:.2f};0.05" '
      f'dur="{3.6 + i*0.5}s" repeatCount="indefinite"/></ellipse>')
A(f'<ellipse cx="{CX}" cy="498" rx="86" ry="17" fill="{DEEP}" opacity="0.22" filter="url(#cGlow)">'
  f'<animate attributeName="rx" values="70;104;70" dur="{DUR}s" repeatCount="indefinite"/></ellipse>')
A('</g>')

# anel orbital
A(f'<ellipse cx="{CX}" cy="{CY}" rx="205" ry="60" fill="none" stroke="url(#cRing)" '
  f'stroke-width="1.6" opacity="0.5">'
  f'<animateTransform attributeName="transform" type="rotate" '
  f'values="0 {CX} {CY};360 {CX} {CY}" dur="{DUR*1.6:.0f}s" repeatCount="indefinite"/></ellipse>')

# satelites em orbita
for k in range(3):
    ph = k * (DUR / 3)
    A(f'<circle r="3.2" fill="{LIGHT}" filter="url(#cGlowS)">'
      f'<animateMotion dur="{DUR*1.6:.0f}s" begin="-{ph:.1f}s" repeatCount="indefinite" '
      f'path="M {CX-205} {CY} a 205 60 0 1 0 410 0 a 205 60 0 1 0 -410 0"/>'
      f'<animate attributeName="opacity" values="0.35;1;0.35" dur="{DUR*0.8:.0f}s" repeatCount="indefinite"/>'
      f'</circle>')


def vals(seq):
    return ";".join(seq)


# ------------------------------------------------ faces
A('<g>')
for k, (idx, n, label) in enumerate(FACES):
    A(f'<polygon points="{poly_pts[k][0]}" fill="url(#cFace)" fill-opacity="{poly_op[k][0]}" '
      f'stroke="{PRIM}" stroke-width="1.7" stroke-opacity="0.85" stroke-linejoin="round">')
    A(f'<animate attributeName="points" values="{vals(poly_pts[k])}" dur="{DUR}s" '
      f'calcMode="linear" repeatCount="indefinite"/>')
    A(f'<animate attributeName="fill-opacity" values="{vals(f"{o:.3f}" for o in poly_op[k])}" '
      f'dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>')
    A('</polygon>')
A('</g>')

# ------------------------------------------------ vertices
for i in range(len(V)):
    xs = vals(f"{p[0]:.1f}" for p in vert_pos[i])
    ys = vals(f"{p[1]:.1f}" for p in vert_pos[i])
    rs = vals(f"{r:.2f}" for r in vert_r[i])
    A(f'<circle cx="{vert_pos[i][0][0]:.1f}" cy="{vert_pos[i][0][1]:.1f}" r="3" fill="#ffffff" '
      f'filter="url(#cGlowS)" opacity="0.95">'
      f'<animate attributeName="cx" values="{xs}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'<animate attributeName="cy" values="{ys}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'<animate attributeName="r"  values="{rs}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'</circle>')

# ------------------------------------------------ labels nas faces
for k, (idx, n, label) in enumerate(FACES):
    xs = vals(f"{p[0]:.1f}" for p in lbl_pos[k])
    ys = vals(f"{p[1] + 5:.1f}" for p in lbl_pos[k])
    ops = vals(f"{o:.3f}" for o in lbl_op[k])
    fss = vals(f"{s:.2f}" for s in lbl_size[k])
    A(f'<text x="{lbl_pos[k][0][0]:.1f}" y="{lbl_pos[k][0][1]+5:.1f}" text-anchor="middle" '
      f'font-family="{MONO}" font-size="{lbl_size[k][0]}" font-weight="700" letter-spacing="1.4" '
      f'fill="#ffffff" opacity="{lbl_op[k][0]}">{label}'
      f'<animate attributeName="x" values="{xs}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'<animate attributeName="y" values="{ys}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="{ops}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'<animate attributeName="font-size" values="{fss}" dur="{DUR}s" calcMode="linear" repeatCount="indefinite"/>'
      f'</text>')

# ------------------------------------------------ legenda
A(f'<text x="{CX}" y="566" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
  f'fill="{MUTED}" letter-spacing="3.2">MY STACK &#183; RENDERIZADO EM SVG PURO</text>')
A(f'<rect x="0.8" y="0.8" width="{W-1.6}" height="{H-1.6}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.6"/>')
A('</svg>')

svg = "\n".join(out)
os.makedirs("assets", exist_ok=True)
with open("assets/stack-3d.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"stack-3d.svg frames={FRAMES} bytes={len(svg)}")
