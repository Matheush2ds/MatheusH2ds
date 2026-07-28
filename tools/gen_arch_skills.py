#!/usr/bin/env python3
"""Gera assets/architecture.svg (fluxo de request animado) e
assets/skills.svg (barras de proficiencia animadas)."""
import os

BODY   = "#0d1117"
CARD   = "#161b22"
BORDER = "#30363d"
PRIM   = "#58a6ff"
LIGHT  = "#a5d6ff"
DEEP   = "#1f6feb"
MUTED  = "#8b949e"
TEXT   = "#c9d1d9"
GREEN  = "#3fb950"
AMBER  = "#d29922"
MONO   = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace"
os.makedirs("assets", exist_ok=True)


def esc(s):
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


# ══════════════════════════════════════════════════ ARCHITECTURE
W, H = 1200, 440
CYCLE = 3.6
CW, CH_ = 168, 96

cards = [
    # x,    y,   title,          sub,                accent
    (28,   168, "CLIENT",        "web / mobile",      PRIM),
    (272,  168, "API GATEWAY",   "auth · rate limit", PRIM),
    (516,  168, "SERVICE LAYER", "use cases · DDD",   LIGHT),
    (768,   56, "REDIS",         "cache · 2ms",       AMBER),
    (768,  280, "POSTGRESQL",    "source of truth",   GREEN),
    (1004, 168, "OBSERVABILITY", "logs · traces",     "#a371f7"),
]
#         path,                                    label,       lx,  ly, anchor,   delay
edges = [
    ("M 196 216 L 272 216",                        "HTTP",      234, 202, "middle", 0.00),
    ("M 440 216 L 516 216",                        "validate",  478, 202, "middle", 0.50),
    ("M 684 216 C 728 216 730 104 768 104",        "cache hit", 726, 128, "end",    1.00),
    ("M 684 216 C 728 216 730 328 768 328",        "SQL",       726, 312, "end",    1.00),
    ("M 684 216 L 1004 216",                       "events",    844, 202, "middle", 1.45),
]
RETURN = "M 600 264 C 600 402 112 402 112 264"

o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="Ciclo de vida de um request">')
A('<defs>')
A(f'''
  <radialGradient id="aAura" cx="50%" cy="50%" r="70%">
    <stop offset="0%" stop-color="{DEEP}" stop-opacity="0.13"/>
    <stop offset="100%" stop-color="{BODY}" stop-opacity="0"/>
  </radialGradient>
  <filter id="aGlow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="3.4"/>
  </filter>
''')
A('</defs>')
A(f'<rect width="{W}" height="{H}" rx="16" fill="{BODY}"/>')
A(f'<rect width="{W}" height="{H}" rx="16" fill="url(#aAura)"/>')

# grid de fundo
A(f'<g stroke="{BORDER}" stroke-width="0.6" opacity="0.35">')
for gx in range(40, W, 40):
    A(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}"/>')
for gy in range(40, H, 40):
    A(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>')
A('</g>')

A(f'<text x="34" y="46" font-family="{MONO}" font-size="14" font-weight="700" fill="{TEXT}" '
  f'letter-spacing="3.4">REQUEST LIFECYCLE</text>')
A(f'<text x="34" y="68" font-family="{MONO}" font-size="11.5" fill="{MUTED}" letter-spacing="1.4">'
  f'como eu penso um back-end</text>')

# ---- edges
A(f'<g fill="none" stroke-linecap="round">')
for d, label, lx, ly, anc, delay in edges:
    A(f'<path d="{d}" stroke="{BORDER}" stroke-width="2.4"/>')
    A(f'<path d="{d}" stroke="{PRIM}" stroke-width="2.4" stroke-dasharray="7 9" opacity="0.75">'
      f'<animate attributeName="stroke-dashoffset" values="32;0" dur="1.1s" repeatCount="indefinite"/>'
      f'</path>')
A(f'<path d="{RETURN}" stroke="{BORDER}" stroke-width="2.2"/>')
A(f'<path d="{RETURN}" stroke="{GREEN}" stroke-width="2.2" stroke-dasharray="5 11" opacity="0.6">'
  f'<animate attributeName="stroke-dashoffset" values="0;32" dur="1.3s" repeatCount="indefinite"/></path>')
A('</g>')

for d, label, lx, ly, anc, delay in edges:
    A(f'<text x="{lx}" y="{ly}" text-anchor="{anc}" font-family="{MONO}" font-size="10.5" '
      f'fill="{MUTED}" letter-spacing="1.1">{esc(label)}</text>')
A(f'<text x="356" y="392" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
  f'fill="{GREEN}" letter-spacing="1.1" opacity="0.9">response &#183; 200 OK</text>')

# ---- cards
for (x, y, title, sub, accent) in cards:
    A(f'<g>')
    A(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH_}" rx="12" fill="{CARD}" '
      f'stroke="{BORDER}" stroke-width="1.4"/>')
    A(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH_}" rx="12" fill="none" '
      f'stroke="{accent}" stroke-width="1.6" opacity="0.15">'
      f'<animate attributeName="opacity" values="0.12;0.75;0.12" dur="{CYCLE}s" repeatCount="indefinite"/>'
      f'</rect>')
    A(f'<path d="M {x+14} {y+1} L {x+CW-14} {y+1}" stroke="{accent}" stroke-width="2.6" '
      f'stroke-linecap="round" opacity="0.9"/>')
    A(f'<text x="{x+CW/2}" y="{y+44}" text-anchor="middle" font-family="{MONO}" font-size="13.5" '
      f'font-weight="700" fill="#ffffff" letter-spacing="1.6">{esc(title)}</text>')
    A(f'<text x="{x+CW/2}" y="{y+66}" text-anchor="middle" font-family="{MONO}" font-size="11" '
      f'fill="{MUTED}" letter-spacing="0.6">{esc(sub)}</text>')
    A(f'<circle cx="{x+CW-16}" cy="{y+CH_-16}" r="3" fill="{accent}">'
      f'<animate attributeName="opacity" values="0.2;1;0.2" dur="{CYCLE/2}s" repeatCount="indefinite"/></circle>')
    A('</g>')

# ---- pulsos de request
for d, label, lx, ly, anc, delay in edges:
    for rep in (0, CYCLE / 2):
        A(f'<circle r="4.6" fill="#ffffff" filter="url(#aGlow)">'
          f'<animateMotion path="{d}" dur="{CYCLE}s" begin="{delay+rep:.2f}s" '
          f'repeatCount="indefinite" keyPoints="0;1" keyTimes="0;0.42" calcMode="linear"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.38;0.44" '
          f'dur="{CYCLE}s" begin="{delay+rep:.2f}s" repeatCount="indefinite"/></circle>')
        A(f'<circle r="2.6" fill="{LIGHT}">'
          f'<animateMotion path="{d}" dur="{CYCLE}s" begin="{delay+rep:.2f}s" '
          f'repeatCount="indefinite" keyPoints="0;1" keyTimes="0;0.42" calcMode="linear"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.38;0.44" '
          f'dur="{CYCLE}s" begin="{delay+rep:.2f}s" repeatCount="indefinite"/></circle>')

A(f'<circle r="4.6" fill="{GREEN}" filter="url(#aGlow)">'
  f'<animateMotion path="{RETURN}" dur="{CYCLE}s" begin="1.9s" repeatCount="indefinite" '
  f'keyPoints="0;1" keyTimes="0;0.5" calcMode="linear"/>'
  f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.46;0.52" '
  f'dur="{CYCLE}s" begin="1.9s" repeatCount="indefinite"/></circle>')

# ---- chip de latencia
A(f'<g>')
A(f'<rect x="{W-244}" y="34" width="210" height="34" rx="17" fill="{CARD}" stroke="{BORDER}"/>')
A(f'<circle cx="{W-224}" cy="51" r="4.5" fill="{GREEN}">'
  f'<animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
A(f'<text x="{W-208}" y="56" font-family="{MONO}" font-size="12" fill="{TEXT}" letter-spacing="1.1">'
  f'p95 38ms &#183; 0 downtime</text>')
A('</g>')

A(f'<rect x="0.8" y="0.8" width="{W-1.6}" height="{H-1.6}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.6"/>')
A('</svg>')
svg = "\n".join(o)
open("assets/architecture.svg", "w", encoding="utf-8").write(svg)
print(f"architecture.svg bytes={len(svg)}")


# ══════════════════════════════════════════════════ SKILLS
SW, SH = 1200, 384
LOOP = 11.0
skills_l = [("Java", 92), ("Spring Boot", 84), ("Node.js / NestJS", 78),
            ("TypeScript", 76), ("Python", 70)]
skills_r = [("PostgreSQL", 86), ("Docker", 74), ("Git & CI/CD", 88),
            ("React / Next.js", 66), ("Linux", 72)]

o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW} {SH}" width="{SW}" height="{SH}" '
  f'role="img" aria-label="Barras de proficiencia">')
A('<defs>')
A(f'''
  <linearGradient id="sBar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="{DEEP}"/>
    <stop offset="55%"  stop-color="{PRIM}"/>
    <stop offset="100%" stop-color="{LIGHT}"/>
  </linearGradient>
  <linearGradient id="sShine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#ffffff" stop-opacity="0"/>
    <stop offset="50%"  stop-color="#ffffff" stop-opacity="0.85"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="sAura" cx="50%" cy="0%" r="90%">
    <stop offset="0%" stop-color="{DEEP}" stop-opacity="0.14"/>
    <stop offset="100%" stop-color="{BODY}" stop-opacity="0"/>
  </radialGradient>
  <filter id="sGlow" x="-20%" y="-160%" width="140%" height="420%">
    <feGaussianBlur stdDeviation="3.2"/>
  </filter>
''')
A('</defs>')
A(f'<rect width="{SW}" height="{SH}" rx="16" fill="{BODY}"/>')
A(f'<rect width="{SW}" height="{SH}" rx="16" fill="url(#sAura)"/>')
A(f'<text x="{SW/2}" y="52" text-anchor="middle" font-family="{MONO}" font-size="14" '
  f'font-weight="700" fill="{TEXT}" letter-spacing="4.6">PROFICI&#202;NCIA</text>')
A(f'<line x1="{SW/2-70}" y1="66" x2="{SW/2+70}" y2="66" stroke="{PRIM}" stroke-width="2" opacity="0.7"/>')

TRACK = 300
ROWH = 46


def bars(items, ox, oy):
    for i, (name, pct) in enumerate(items):
        y = oy + i * ROWH
        bx = ox + 172
        v = pct / 100.0
        d = i * 0.14
        A(f'<text x="{ox}" y="{y+4}" font-family="{MONO}" font-size="13" fill="{TEXT}" '
          f'letter-spacing="0.7">{esc(name)}</text>')
        A(f'<rect x="{bx}" y="{y-7}" width="{TRACK}" height="9" rx="4.5" fill="#1b2230" '
          f'stroke="{BORDER}" stroke-width="0.8"/>')
        kt = "0;0.30;0.88;1"
        vv = f"0 1;{v:.3f} 1;{v:.3f} 1;0 1"
        A(f'<g transform="translate({bx} 0)">')
        A(f'<rect x="0" y="{y-7}" width="{TRACK}" height="9" rx="4.5" fill="url(#sBar)" opacity="0.55" '
          f'filter="url(#sGlow)">'
          f'<animateTransform attributeName="transform" type="scale" values="{vv}" keyTimes="{kt}" '
          f'dur="{LOOP}s" begin="{d:.2f}s" repeatCount="indefinite" additive="sum"/></rect>')
        A(f'<rect x="0" y="{y-7}" width="{TRACK}" height="9" rx="4.5" fill="url(#sBar)">'
          f'<animateTransform attributeName="transform" type="scale" values="{vv}" keyTimes="{kt}" '
          f'dur="{LOOP}s" begin="{d:.2f}s" repeatCount="indefinite" additive="sum"/></rect>')
        A('</g>')
        # shine correndo sobre a barra preenchida
        fw = TRACK * v
        A(f'<rect x="{bx}" y="{y-7}" width="46" height="9" rx="4.5" fill="url(#sShine)" opacity="0">'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="0 0;{fw-46:.0f} 0" keyTimes="0;1" dur="1.9s" begin="{2.2+d:.2f}s" '
          f'repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;0.6;0" dur="1.9s" begin="{2.2+d:.2f}s" '
          f'repeatCount="indefinite"/></rect>')
        A(f'<text x="{bx+TRACK+16}" y="{y+4}" font-family="{MONO}" font-size="12.5" '
          f'fill="{PRIM}" font-weight="700">{pct}'
          f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.26;0.34;0.9;1" '
          f'dur="{LOOP}s" begin="{d:.2f}s" repeatCount="indefinite"/></text>')


bars(skills_l, 60, 122)
bars(skills_r, 640, 122)
A(f'<line x1="{SW/2}" y1="100" x2="{SW/2}" y2="{SH-46}" stroke="{BORDER}" stroke-width="1" opacity="0.7"/>')
A(f'<text x="{SW/2}" y="{SH-20}" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
  f'fill="{MUTED}" letter-spacing="2">auto-avalia&#231;&#227;o &#183; atualizado 2026</text>')
A(f'<rect x="0.8" y="0.8" width="{SW-1.6}" height="{SH-1.6}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.6"/>')
A('</svg>')
svg = "\n".join(o)
open("assets/skills.svg", "w", encoding="utf-8").write(svg)
print(f"skills.svg bytes={len(svg)}")
