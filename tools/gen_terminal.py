#!/usr/bin/env python3
"""Gera assets/terminal.svg - terminal fake com typewriter em loop (SMIL puro)."""
import os

W, H = 1200, 508
T = 26.0                       # loop total
BODY   = "#0d1117"
CHROME = "#161b22"
BORDER = "#30363d"
PRIM   = "#58a6ff"
LIGHT  = "#a5d6ff"
KEY    = "#79c0ff"
MUTED  = "#8b949e"
TEXT   = "#c9d1d9"
GREEN  = "#3fb950"
MONO   = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace"

FS   = 15.5
CH   = FS * 0.601              # largura de caractere monospace
LH   = 26.5
X0   = 32
Y0   = 96
FADE = (22.4, 23.8)            # janela de fade-out do ciclo


def esc(s: str) -> str:
    o = []
    for c in s:
        if c == "&":
            o.append("&amp;")
        elif c == "<":
            o.append("&lt;")
        elif c == ">":
            o.append("&gt;")
        elif ord(c) < 128:
            o.append(c)
        else:
            o.append(f"&#{ord(c)};")
    return "".join(o)


def kt(v):
    return max(0.0, min(1.0, v / T))


def appear(t_on):
    """opacity: invisivel -> visivel em t_on -> fade no fim do ciclo."""
    a, b = kt(t_on), kt(t_on) + 0.0015
    f0, f1 = kt(FADE[0]), kt(FADE[1])
    return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
            f'keyTimes="0;{a:.5f};{b:.5f};{f0:.5f};{f1:.5f};1" '
            f'dur="{T}s" repeatCount="indefinite" fill="freeze"/>')


rows = []          # (kind, t_on, content)
# kind: "cmd" | "out" | "gap"
# idioma: `python3 tools/gen_terminal.py` (pt-BR) ou `LANG_OUT=en python3 ...`
LANG_OUT = os.environ.get("LANG_OUT", "pt").lower()

if LANG_OUT == "en":
    OUT_FILE = "assets/terminal-en.svg"
    L = {
        "t1":   "Developer",
        "t2":   "Systems Analyst",
        "role": "BSc in Computer Science  •  postgrad in Artificial Intelligence",
        "open": "open to back-end roles",
    }
else:
    OUT_FILE = "assets/terminal.svg"
    L = {
        "t1":   "Desenvolvedor",
        "t2":   "Analista de Sistemas",
        "role": "Bacharel em Ciência da Computação  •  pós em Inteligência Artificial",
        "open": "aberto a oportunidades back-end",
    }

script = [
    ("cmd", 0.5,  "whoami"),
    ("out", 1.75, [(TEXT, "Matheus Henrique"), (MUTED, "  •  "),
                   (LIGHT, L["t1"]), (MUTED, " & "), (LIGHT, L["t2"])]),
    ("out", 2.30, [(MUTED, L["role"])]),
    ("gap", 0,    None),
    ("cmd", 3.40, "cat stack.json"),
    ("out", 4.70, [(MUTED, "{")]),
    ("out", 5.00, [(KEY, '  "apis"'), (MUTED, ": "), (LIGHT, '"REST · GraphQL · gRPC"'), (MUTED, ",")]),
    ("out", 5.55, [(KEY, '  "architecture"'), (MUTED, ": "), (LIGHT, '"Hexagonal · DDD · SOLID"'), (MUTED, ",")]),
    ("out", 6.10, [(KEY, '  "data"'), (MUTED, ": "), (LIGHT, '"PostgreSQL · Redis · MySQL"'), (MUTED, ",")]),
    ("out", 6.65, [(KEY, '  "quality"'), (MUTED, ": "), (LIGHT, '"Clean Code · TDD · Observability"')]),
    ("out", 7.15, [(MUTED, "}")]),
    ("gap", 0,    None),
    ("cmd", 8.10, "cat status.txt"),
    ("out", 9.45, [(GREEN, "● "), (TEXT, L["open"])]),
]

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="Terminal: sobre Matheus Henrique">')

A('<defs>')
A(f'''
  <linearGradient id="tChrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#1c2430"/>
    <stop offset="100%" stop-color="#161b22"/>
  </linearGradient>
  <linearGradient id="tEdge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="{PRIM}" stop-opacity="0.55"/>
    <stop offset="50%"  stop-color="{BORDER}"/>
    <stop offset="100%" stop-color="{PRIM}" stop-opacity="0.35"/>
  </linearGradient>
  <filter id="tGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
  <clipPath id="tClip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath>
  <clipPath id="tBody"><rect x="2" y="46" width="{W-4}" height="{H-96}"/></clipPath>
''')
A('</defs>')

A('<g clip-path="url(#tClip)">')
A(f'<rect width="{W}" height="{H}" fill="{BODY}"/>')

# ------------------------------------------------- title bar
A(f'<rect x="0" y="0" width="{W}" height="46" fill="url(#tChrome)"/>')
A(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{BORDER}"/>')
for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
    A(f'<circle cx="{28 + i*22}" cy="23" r="6.5" fill="{col}" opacity="0.9"/>')
A(f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="13" '
  f'fill="{MUTED}" letter-spacing="1.2">matheus@github &#8212; ~/dev &#8212; zsh</text>')
A(f'<text x="{W-30}" y="28" text-anchor="end" font-family="{MONO}" font-size="12" fill="{PRIM}" '
  f'opacity="0.8">&#9679; live'
  f'<animate attributeName="opacity" values="0.25;0.9;0.25" dur="2.4s" repeatCount="indefinite"/></text>')

# ------------------------------------------------- body
A('<g clip-path="url(#tBody)">')

y = Y0
last_cmd_end = 0.0
for kind, t_on, content in script:
    if kind == "gap":
        y += LH * 0.55
        continue

    if kind == "cmd":
        type_dur = max(0.55, len(content) * 0.062)
        px = X0 + CH * 2.4                      # texto comeca depois do prompt
        wpx = len(content) * CH + 12
        A(f'<g>{appear(t_on)}')
        A(f'<text x="{X0}" y="{y:.1f}" font-family="{MONO}" font-size="{FS}" fill="{GREEN}" '
          f'font-weight="600">&#10095;</text>')
        A(f'<text x="{px:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{FS}" fill="#ffffff">'
          f'{esc(content)}</text>')
        # cover rect que desliza revelando o comando (typewriter)
        a0, a1 = kt(t_on), kt(t_on + type_dur)
        A(f'<rect x="{px:.1f}" y="{y-FS:.1f}" width="{wpx:.1f}" height="{FS*1.45:.1f}" fill="{BODY}">'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="0 0;0 0;{wpx:.1f} 0;{wpx:.1f} 0" keyTimes="0;{a0:.5f};{a1:.5f};1" '
          f'dur="{T}s" repeatCount="indefinite"/></rect>')
        # cursor que acompanha a digitacao
        A(f'<rect x="{px:.1f}" y="{y-FS+1.5:.1f}" width="{CH:.1f}" height="{FS*1.15:.1f}" fill="{PRIM}" opacity="0">'
          f'<animate attributeName="opacity" values="0;0;0.95;0.95;0" '
          f'keyTimes="0;{a0:.5f};{a0+0.0015:.5f};{a1:.5f};{min(a1+0.002,1):.5f}" '
          f'dur="{T}s" repeatCount="indefinite"/>'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="0 0;0 0;{len(content)*CH:.1f} 0;{len(content)*CH:.1f} 0" '
          f'keyTimes="0;{a0:.5f};{a1:.5f};1" dur="{T}s" repeatCount="indefinite"/></rect>')
        A('</g>')
        last_cmd_end = t_on + type_dur
    else:
        A(f'<g>{appear(t_on)}')
        A(f'<text x="{X0 + CH*2.4:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{FS}">')
        for col, frag in content:
            A(f'<tspan fill="{col}" xml:space="preserve">{esc(frag)}</tspan>')
        A('</text>')
        A('</g>')
    y += LH

# prompt final com cursor piscando
y += LH * 0.25
A(f'<g>{appear(10.5)}')
A(f'<text x="{X0}" y="{y:.1f}" font-family="{MONO}" font-size="{FS}" fill="{GREEN}" font-weight="600">&#10095;</text>')
A(f'<rect x="{X0 + CH*2.4:.1f}" y="{y-FS+1.5:.1f}" width="{CH:.1f}" height="{FS*1.15:.1f}" fill="{PRIM}">'
  f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" '
  f'dur="1.1s" repeatCount="indefinite"/></rect>')
A('</g>')
A('</g>')

# ------------------------------------------------- status bar
sy = H - 34
A(f'<rect x="0" y="{sy}" width="{W}" height="34" fill="{CHROME}"/>')
A(f'<line x1="0" y1="{sy}" x2="{W}" y2="{sy}" stroke="{BORDER}"/>')
segs = [(PRIM, "⎇ main"), (MUTED, "java 21"), (MUTED, "node 22"), (MUTED, "docker ✓"),
        (MUTED, "postgres 16")]
sx = 30
for col, label in segs:
    A(f'<text x="{sx}" y="{sy+22}" font-family="{MONO}" font-size="12" fill="{col}" '
      f'letter-spacing="0.8">{esc(label)}</text>')
    sx += len(label) * 8 + 34
A(f'<text x="{W-30}" y="{sy+22}" text-anchor="end" font-family="{MONO}" font-size="12" '
  f'fill="{MUTED}">matheushenriqueds1223@gmail.com</text>')

A(f'<rect x="0.9" y="0.9" width="{W-1.8}" height="{H-1.8}" rx="14" fill="none" '
  f'stroke="url(#tEdge)" stroke-width="1.8"/>')
A('</g>')
A('</svg>')

svg = "\n".join(out)
os.makedirs("assets", exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"-> {OUT_FILE}")
print(f"terminal.svg bytes={len(svg)} last_y={y:.0f} (H={H})")
