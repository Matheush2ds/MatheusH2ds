"""Gera os SVGs do README: header, products, pipeline e stack, em PT e EN, temas claro e escuro.

Todo texto vira contorno (path). O SVG renderiza igual em qualquer navegador e no
proxy de imagens do GitHub, sem depender de fonte instalada em quem visita.

Uso:
    mkdir fonts && cd fonts
    npm pack @fontsource/instrument-sans @fontsource/ibm-plex-mono
    for f in *.tgz; do tar xzf "$f"; done; cd ..
    pip install fonttools brotli uharfbuzz
    python tools/build_assets.py ./fonts ./assets

Fontes: Instrument Sans e IBM Plex Mono, ambas sob a SIL Open Font License.
"""
import glob
import io
import sys
from xml.sax.saxutils import escape

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else "./fonts"
OUT = sys.argv[2] if len(sys.argv) > 2 else "./assets"
W = 1200
PAD = 64
DEFS = {}


def font_path(name):
    return glob.glob(f"{FONT_DIR}/**/{name}", recursive=True)[0]


class Face:
    def __init__(self, key, filename):
        tt = TTFont(font_path(filename))
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        self.key = key
        self.tt = TTFont(io.BytesIO(data))
        self.hb = hb.Font(hb.Face(data))
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def _shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return buf

    def width(self, text, size, tracking=0.0):
        buf = self._shape(text)
        adv = sum(p.x_advance for p in buf.glyph_positions)
        return (adv + tracking * self.upem * len(buf.glyph_positions)) * size / self.upem

    def uses(self, text, size, x, y, tracking=0.0):
        buf = self._shape(text)
        s = size / self.upem
        out, cx = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            gid = f"{self.key}{info.codepoint}"
            if gid not in DEFS:
                pen = SVGPathPen(self.gs, ntos=lambda v: str(int(round(v))))
                self.gs[self.order[info.codepoint]].draw(pen)
                DEFS[gid] = pen.getCommands()
            if DEFS[gid]:
                gx = x + (cx + pos.x_offset) * s
                gy = y - pos.y_offset * s
                out.append(f'<use href="#{gid}" transform="translate({gx:.2f} {gy:.2f}) scale({s:.5f} -{s:.5f})"/>')
            cx += pos.x_advance + tracking * self.upem
        return "".join(out)


DISPLAY = Face("d", "instrument-sans-latin-700-normal.woff2")
TITLE = Face("t", "instrument-sans-latin-600-normal.woff2")
MEDIUM = Face("e", "instrument-sans-latin-500-normal.woff2")
BODY = Face("b", "instrument-sans-latin-400-normal.woff2")
MONO = Face("m", "ibm-plex-mono-latin-500-normal.woff2")

THEMES = {
    "dark": dict(bg="#08121f", edge="#1b2b41", ink="#edf2f8", muted="#9aabc0", faint="#64768e",
                 line="#2b3e58", hair="#14233a", dot="#16263d", accent="#f2b35b"),
    "light": dict(bg="#fbfaf6", edge="#e2ded3", ink="#151c27", muted="#525c6a", faint="#868d98",
                  line="#c4c9d0", hair="#ebe7dd", dot="#e4e0d5", accent="#b25f0c"),
}


def text(face, s, size, x, y, fill, anchor="start", tracking=0.0):
    if anchor != "start":
        w = face.width(s, size, tracking)
        x -= w / 2 if anchor == "middle" else w
    return f'<g fill="{fill}">{face.uses(s, size, x, y, tracking)}</g>'


def runs(parts, size, x, y):
    """Texto com trechos de pesos/cores diferentes na mesma linha: [(face, texto, cor)]."""
    out = []
    for face, s, fill in parts:
        out.append(text(face, s, size, x, y, fill))
        x += face.width(s, size)
    return "".join(out)


def eyebrow(s, c, y=84):
    return text(MONO, s, 12.5, PAD, y, c["accent"], tracking=0.14)


def frame(h, c, title, body, extra_defs=""):
    defs = "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
        f'role="img" aria-labelledby="t">\n<title id="t">{escape(title)}</title>\n'
        f"<defs>{extra_defs}{defs}</defs>\n"
        "<style>@media (prefers-reduced-motion: reduce){.pulse{display:none}}</style>\n"
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="16" fill="{c["bg"]}" stroke="{c["edge"]}"/>\n'
        f"{body}\n</svg>\n"
    )


def node(x, y, c, r=6, hot=False):
    fill = c["accent"] if hot else c["bg"]
    stroke = c["accent"] if hot else c["line"]
    halo = f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="{c["accent"]}" fill-opacity="0.18"/>' if hot else ""
    return f'{halo}<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


# ---------------------------------------------------------------- textos

COPY = {
    "pt": dict(
        header=dict(
            eyebrow="ENGENHARIA DE SOFTWARE  ·  ANÁLISE DE SISTEMAS  ·  GESTÃO DE PROJETOS",
            line1=[("Fundador da ", 0), ("Optima Sistemas", 1), (". Construo SaaS B2B, plataformas", 0)],
            line2="operacionais, arquitetura back-end e integrações.",
            foot=["Arquitetura de Software", "TypeScript", "Python", "Java"],
            queue="fila",
            title="Matheus Henrique: engenharia de software, análise de sistemas e gestão de projetos",
        ),
        products=dict(
            eyebrow="CAMADAS DE CADA SISTEMA  ·  OPTIMA SISTEMAS",
            cols=[
                ("Optima Control", "SAAS MULTI-TENANT",
                 [("Next.js", "app router"), ("Prisma", "migrations"), ("PostgreSQL", "RLS por tenant")], 2,
                 "Isolamento por tenant testado no CI"),
                ("Portal SST", "EPI E NR-1",
                 [("API Gateway", "roteamento"), ("Node.js + FastAPI", "TS e Python"), ("PostgreSQL", "persistência")], 0,
                 "Entrega de EPI e risco psicossocial"),
                ("ERP de Temporada", "OPERAÇÃO E REPASSE",
                 [("React", "painel web"), ("Express + Sequelize", "monolito modular"), ("PostgreSQL", "transações ACID")], 2,
                 "Reservas, enxoval, limpeza e financeiro"),
            ],
            title="Optima Control, Portal SST e ERP de Temporada: camadas de cada produto",
        ),
        pipeline=dict(
            eyebrow="DO COMMIT À PRODUÇÃO  ·  OPTIMA SISTEMAS",
            stages=[("commit", "GitHub Actions"), ("lint e tipos", "ESLint · tsc"), ("testes", "Vitest"),
                    ("migrations + RLS", "Prisma · Postgres"), ("E2E", "Playwright"), ("deploy", "produção")],
            after=[("observabilidade", "logs estruturados"), ("backup agendado", "cron no CI"),
                   ("ensaio de restauração", "restaura e confere")],
            lane="DEPOIS DO DEPLOY",
            title="Pipeline: commit, lint e tipos, testes, migrations com RLS, E2E e deploy, seguido de observabilidade, backup e ensaio de restauração",
        ),
        stack=dict(
            eyebrow="FERRAMENTAS DO DIA A DIA",
            rows=[("BACK-END E APIS", ["TypeScript", "Node.js", "Express", "Python", "FastAPI", "Java", "Spring Boot"]),
                  ("FRONT-END", ["Next.js", "React"]),
                  ("DADOS", ["PostgreSQL", "MySQL", "SQL Server", "Prisma", "Sequelize", "Redis"]),
                  ("INFRA E QUALIDADE", ["Docker", "GitHub Actions", "Linux", "Playwright", "Vitest"])],
            title="Stack tecnológica",
        ),
    ),
    "en": dict(
        header=dict(
            eyebrow="SOFTWARE ENGINEERING  ·  SYSTEMS ANALYSIS  ·  PROJECT MANAGEMENT",
            line1=[("Founder at ", 0), ("Optima Sistemas", 1), (". I build B2B SaaS, operational", 0)],
            line2="platforms, backend architecture and integrations.",
            foot=["Software Architecture", "TypeScript", "Python", "Java"],
            queue="queue",
            title="Matheus Henrique: software engineering, systems analysis and project management",
        ),
        products=dict(
            eyebrow="HOW EACH SYSTEM IS LAYERED  ·  OPTIMA SISTEMAS",
            cols=[
                ("Optima Control", "MULTI-TENANT SAAS",
                 [("Next.js", "app router"), ("Prisma", "migrations"), ("PostgreSQL", "per-tenant RLS")], 2,
                 "Tenant isolation tested in CI"),
                ("Portal SST", "PPE & NR-1",
                 [("API Gateway", "routing"), ("Node.js + FastAPI", "TS and Python"), ("PostgreSQL", "persistence")], 0,
                 "PPE delivery and psychosocial risk"),
                ("ERP de Temporada", "OPS & PAYOUTS",
                 [("React", "web panel"), ("Express + Sequelize", "modular monolith"), ("PostgreSQL", "ACID transactions")], 2,
                 "Bookings, linens, cleaning and finance"),
            ],
            title="Optima Control, Portal SST and ERP de Temporada: layers of each product",
        ),
        pipeline=dict(
            eyebrow="FROM COMMIT TO PRODUCTION  ·  OPTIMA SISTEMAS",
            stages=[("commit", "GitHub Actions"), ("lint & types", "ESLint · tsc"), ("unit tests", "Vitest"),
                    ("migrations + RLS", "Prisma · Postgres"), ("E2E suite", "Playwright"), ("deploy", "production")],
            after=[("observability", "structured logs"), ("scheduled backup", "CI cron jobs"),
                   ("restore drill", "restore & verify")],
            lane="AFTER DEPLOY",
            title="Pipeline: commit, lint and types, tests, migrations with RLS, E2E and deploy, followed by observability, backups and restore drills",
        ),
        stack=dict(
            eyebrow="DAY-TO-DAY TOOLS",
            rows=[("BACKEND & APIS", ["TypeScript", "Node.js", "Express", "Python", "FastAPI", "Java", "Spring Boot"]),
                  ("FRONTEND", ["Next.js", "React"]),
                  ("DATA", ["PostgreSQL", "MySQL", "SQL Server", "Prisma", "Sequelize", "Redis"]),
                  ("INFRA & QA", ["Docker", "GitHub Actions", "Linux", "Playwright", "Vitest"])],
            title="Technology stack",
        ),
    ),
}


# ---------------------------------------------------------------- peças

def header(c, t):
    H = 360
    parts = [eyebrow(t["eyebrow"], c, y=98)]
    parts.append(text(DISPLAY, "Matheus Henrique", 78, PAD - 4, 182, c["ink"], tracking=-0.025))
    parts.append(runs([(MEDIUM if k else BODY, s, c["ink"] if k else c["muted"]) for s, k in t["line1"]], 21, PAD, 232))
    parts.append(text(BODY, t["line2"], 21, PAD, 262, c["muted"]))

    x, foot = PAD, []
    for i, w in enumerate(t["foot"]):
        foot.append(text(MONO, w, 12.5, x, 312, c["faint"]))
        x += MONO.width(w, 12.5) + 14
        if i < len(t["foot"]) - 1:
            foot.append(f'<circle cx="{x:.1f}" cy="308" r="2" fill="{c["line"]}"/>')
            x += 14
    parts.extend(foot)

    # mapa de serviços com cantos arredondados
    web, api, db = (812, 138), (960, 138), (1108, 138)
    q, wk = (960, 262), (1108, 262)
    r = 26
    p1 = f"M{web[0]},{web[1]} H{db[0]}"
    p2 = (f"M{api[0]},{api[1]} V{q[1]-r} Q{q[0]},{q[1]} {q[0]+r},{q[1]} "
          f"H{wk[0]-r} Q{wk[0]},{wk[1]} {wk[0]},{wk[1]-r} V{db[1]}")
    dots = "".join(f'<circle cx="{776 + i*28}" cy="{90 + j*28}" r="1.5"/>' for i in range(14) for j in range(8))
    parts.append(f'<g fill="{c["dot"]}" mask="url(#fade)">{dots}</g>')
    parts.append(f'<g fill="none" stroke="{c["line"]}" stroke-width="1.5"><path d="{p1}"/><path d="{p2}"/></g>')
    for (x_, y_), label, below, hot in [(web, "web", 0, 0), (api, "api", 0, 0), (db, "postgres", 0, 1),
                                         (q, t["queue"], 1, 0), (wk, "worker", 1, 0)]:
        parts.append(node(x_, y_, c, hot=hot))
        parts.append(text(MONO, label, 12, x_, y_ + 30 if below else y_ - 20, c["faint"], anchor="middle"))
    parts.append(
        f'<g class="pulse" fill="{c["accent"]}">'
        f'<circle r="3.5"><animateMotion dur="3.6s" repeatCount="indefinite" path="{p1}"/></circle>'
        f'<circle r="3.5"><animateMotion dur="5.4s" repeatCount="indefinite" path="{p2}"/></circle></g>'
    )
    mask = ('<linearGradient id="fg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset="0.35" stop-color="#fff"/></linearGradient>'
            '<mask id="fade"><rect x="740" y="60" width="460" height="280" fill="url(#fg)"/></mask>')
    return H, mask, "\n".join(parts)


def products(c, t):
    H = 412
    parts = [eyebrow(t["eyebrow"], c)]
    xs, colw = [PAD, 440, 816], 320
    for sx in (416, 792):
        parts.append(f'<line x1="{sx}" y1="124" x2="{sx}" y2="374" stroke="{c["hair"]}" stroke-width="1.5"/>')
    pulses = []
    for i, (name, kind, layers, hot, note) in enumerate(t["cols"]):
        x0 = xs[i]
        parts.append(text(TITLE, name, 25, x0, 150, c["ink"], tracking=-0.01))
        parts.append(text(MONO, kind, 11.5, x0, 176, c["accent"], tracking=0.12))
        ys = [228, 278, 328]
        nx = x0 + 6
        parts.append(f'<line x1="{nx}" y1="{ys[0]-5}" x2="{nx}" y2="{ys[-1]-5}" stroke="{c["line"]}" stroke-width="1.5"/>')
        pulses.append(f'<circle r="3"><animateMotion dur="{2.6 + i*0.5:.1f}s" repeatCount="indefinite" '
                      f'path="M{nx},{ys[0]-5} V{ys[-1]-5}"/></circle>')
        for j, (tech, role) in enumerate(layers):
            parts.append(node(nx, ys[j] - 5, c, r=5, hot=(j == hot)))
            parts.append(text(MEDIUM, tech, 16.5, x0 + 26, ys[j], c["ink"]))
            parts.append(text(MONO, role, 12, x0 + colw, ys[j], c["faint"], anchor="end"))
        parts.append(f'<line x1="{x0}" y1="350" x2="{x0+colw}" y2="350" stroke="{c["hair"]}" stroke-width="1.5"/>')
        parts.append(text(BODY, note, 14.5, x0, 378, c["muted"]))
    parts.append(f'<g class="pulse" fill="{c["accent"]}">{"".join(pulses)}</g>')
    return H, "", "\n".join(parts)


def pipeline(c, t):
    H = 372
    parts = [eyebrow(t["eyebrow"], c)]
    y, ly = 170, 292
    xs = [104 + i * 198 for i in range(6)]  # 104 .. 1094
    end = xs[-1]
    lane_end = 380
    path = f"M{xs[0]},{y} H{end} C{end+62},{y} {end+62},{ly} {end},{ly} H{lane_end}"
    parts.append(f'<path d="M{xs[0]},{y} H{end}" fill="none" stroke="{c["line"]}" stroke-width="2"/>')
    parts.append(f'<path d="M{end},{y} C{end+62},{y} {end+62},{ly} {end},{ly} H{lane_end}" fill="none" '
                 f'stroke="{c["line"]}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    for i, (name, tool) in enumerate(t["stages"]):
        hot = i in (3, 5)
        parts.append(text(MONO, f"{i+1:02d}", 11.5, xs[i], y - 24, c["accent"] if hot else c["faint"], anchor="middle"))
        parts.append(node(xs[i], y, c, r=7, hot=hot))
        parts.append(text(TITLE, name, 16, xs[i], y + 38, c["ink"], anchor="middle"))
        parts.append(text(MONO, tool, 12, xs[i], y + 60, c["faint"], anchor="middle"))
    for k, (name, desc) in enumerate(t["after"]):
        ax = 904 - k * 236
        hot = k == len(t["after"]) - 1
        parts.append(node(ax, ly, c, r=6, hot=hot))
        parts.append(text(TITLE, name, 15, ax, ly + 34, c["ink"], anchor="middle"))
        parts.append(text(MONO, desc, 12, ax, ly + 54, c["faint"], anchor="middle"))
    parts.append(text(MONO, t["lane"], 11.5, PAD, ly + 4, c["faint"], tracking=0.12))
    parts.append(f'<g class="pulse" fill="{c["accent"]}"><circle r="3.5">'
                 f'<animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle></g>')
    return H, "", "\n".join(parts)


def stack(c, t):
    rows = t["rows"]
    top, step = 142, 54
    H = top + step * (len(rows) - 1) + 58
    parts = [eyebrow(t["eyebrow"], c)]
    for i, (cat, names) in enumerate(rows):
        y = top + i * step
        if i:
            parts.append(f'<line x1="{PAD}" y1="{y-33}" x2="{W-PAD}" y2="{y-33}" stroke="{c["hair"]}" stroke-width="1.5"/>')
        parts.append(text(MONO, cat, 11.5, PAD, y, c["faint"], tracking=0.12))
        x = 300
        for j, n in enumerate(names):
            parts.append(text(MEDIUM, n, 18, x, y + 1, c["ink"]))
            x += MEDIUM.width(n, 18) + 15
            if j < len(names) - 1:
                parts.append(f'<circle cx="{x:.1f}" cy="{y-5}" r="2" fill="{c["line"]}"/>')
                x += 15
    return H, "", "\n".join(parts)


PIECES = {"header": header, "products": products, "pipeline": pipeline, "stack": stack}

if __name__ == "__main__":
    for lang, copy in COPY.items():
        for theme, c in THEMES.items():
            for name, fn in PIECES.items():
                DEFS.clear()
                h, extra, body = fn(c, copy[name])
                if name != "header":  # sobe o conteúdo para o respiro de cima igualar o de baixo
                    body, h = f'<g transform="translate(0 -18)">{body}</g>', h - 18
                svg = frame(h, c, copy[name]["title"], body, extra)
                suffix = "" if lang == "pt" else ".en"
                with open(f"{OUT}/{name}-{theme}{suffix}.svg", "w", encoding="utf-8") as f:
                    f.write(svg)
