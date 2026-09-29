"""Gera assets/hero-{dark,light}{,.en}.svg com o texto convertido em contorno.

Texto em contorno evita depender de fonte instalada: o SVG renderiza igual em
qualquer navegador e no proxy de imagens do GitHub.

Uso:
    npm pack @fontsource/schibsted-grotesk @fontsource/jetbrains-mono  # extraia em ./fonts
    pip install fonttools brotli uharfbuzz
    python tools/gen_hero.py ./fonts ./assets

Fontes: Schibsted Grotesk e JetBrains Mono, ambas sob a SIL Open Font License.
"""
import glob
import io
import sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else "./fonts"
OUT = sys.argv[2] if len(sys.argv) > 2 else "./assets"


def font_path(pattern):
    return glob.glob(f"{FONT_DIR}/**/{pattern}", recursive=True)[0]


class Face:
    def __init__(self, path):
        # harfbuzz precisa do binário sfnt; woff2 é descomprimido em memória
        font = TTFont(path)
        font.flavor = None
        buf = io.BytesIO()
        font.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.hbfont = hb.Font(hb.Face(data))
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def path(self, text, size, x, y, tracking=0.0):
        """Retorna (svg com <use> por glifo, largura). Glifos ficam em DEFS, em unidades da fonte."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        s = size / self.upem
        out = []
        cx = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            gid = f"{self.key}{info.codepoint}"
            if gid not in DEFS:
                pen = SVGPathPen(self.gs, ntos=lambda v: str(int(round(v))))
                self.gs[name].draw(pen)
                DEFS[gid] = pen.getCommands()
            if DEFS[gid]:
                gx = x + (cx + pos.x_offset) * s
                gy = y - pos.y_offset * s
                out.append(f'<use href="#{gid}" transform="translate({gx:.1f} {gy:.1f}) scale({s:.4f} -{s:.4f})"/>')
            cx += pos.x_advance + tracking * self.upem
        return "".join(out), cx * s


DEFS = {}

DISPLAY = Face(font_path("schibsted-grotesk-latin-800-normal.woff2")); DISPLAY.key = "d"
BODY = Face(font_path("schibsted-grotesk-latin-500-normal.woff2")); BODY.key = "b"
MONO = Face(font_path("jetbrains-mono-latin-500-normal.woff2")); MONO.key = "m"

THEMES = {
    "dark": dict(bg="#0d1117", edge="#21262d", ink="#e6edf3", muted="#9da7b3", faint="#6e7681",
                 dot="#262c34", line="#3d4651", accent="#2bb3a3"),
    "light": dict(bg="#ffffff", edge="#d0d7de", ink="#1f2328", muted="#59636e", faint="#818b98",
                  dot="#e3e8ec", line="#b6c0ca", accent="#0f766e"),
}

COPY = {
    "pt": dict(eyebrow="DESENVOLVEDOR  ·  ANALISTA DE SISTEMAS",
               tagline="Construo sistemas de gestão sob medida, SaaS B2B e integrações.",
               queue="fila",
               title="Matheus Henrique, desenvolvedor e analista de sistemas"),
    "en": dict(eyebrow="SOFTWARE DEVELOPER  ·  SYSTEMS ANALYST",
               tagline="I build custom management systems, B2B SaaS and integrations.",
               queue="queue",
               title="Matheus Henrique, software developer and systems analyst"),
}

W, H = 1200, 340
GX, GY, STEP, COLS, ROWS = 872, 86, 30, 10, 7


def g(i, j):
    return GX + i * STEP, GY + j * STEP


def build(theme, lang):
    DEFS.clear()
    c, t = THEMES[theme], COPY[lang]
    eyebrow, _ = MONO.path(t["eyebrow"], 14, 64, 104, tracking=0.12)
    name, _ = DISPLAY.path("Matheus Henrique", 74, 60, 184, tracking=-0.02)
    tag, _ = BODY.path(t["tagline"], 21, 64, 232)

    # rodapé: palavras em mono separadas por quadradinhos
    foot, sep, fx = [], [], 64
    words = ["Optima Sistemas", "TypeScript", "Python", "Java"]
    for i, word in enumerate(words):
        d, w = MONO.path(word, 13, fx, 284)
        foot.append(d)
        fx += w + 16
        if i < len(words) - 1:
            sep.append(f'<rect x="{fx-2:.1f}" y="276" width="4" height="4" rx="1"/>')
            fx += 16

    # mapa de serviços: pontos de grade + caminhos ortogonais
    web, api, db = g(0, 1), g(3, 1), g(8, 1)
    queue, worker = g(3, 5), g(8, 5)
    dots = "".join(
        f'<circle cx="{g(i, j)[0]}" cy="{g(i, j)[1]}" r="1.6"/>' for i in range(COLS) for j in range(ROWS)
    )
    p1 = f"M{web[0]},{web[1]} H{api[0]} H{db[0]}"
    p2 = f"M{api[0]},{api[1]} V{queue[1]} H{worker[0]} V{db[1]}"
    labels = [(web, "web", "above"), (api, "api", "above"), (db, "postgres", "above"),
              (queue, t["queue"], "below"), (worker, "worker", "below")]
    lab_svg = []
    for (x, y), text, where in labels:
        _, w = MONO.path(text, 12, 0, 0)
        ty = y - 16 if where == "above" else y + 26
        d, _ = MONO.path(text, 12, x - w / 2, ty)
        lab_svg.append(d)
    nodes = "".join(
        f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="3"/>' for (x, y) in [web, api, db, queue, worker]
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">{t["title"]}</title>
<defs>{"".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v)}</defs>
<style>@media (prefers-reduced-motion: reduce){{.pulse{{display:none}}}}</style>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{c["bg"]}" stroke="{c["edge"]}"/>
<g fill="{c["accent"]}">{eyebrow}</g>
<g fill="{c["ink"]}">{name}</g>
<g fill="{c["muted"]}">{tag}</g>
<g fill="{c["faint"]}">{"".join(foot)}{"".join(sep)}</g>
<g fill="{c["dot"]}">{dots}</g>
<g fill="none" stroke="{c["line"]}" stroke-width="1.5" stroke-linejoin="round"><path d="{p1}"/><path d="{p2}"/></g>
<g fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2">{nodes}</g>
<g fill="{c["faint"]}">{"".join(lab_svg)}</g>
<g class="pulse" fill="{c["accent"]}">
<circle r="3.5"><animateMotion dur="3.2s" repeatCount="indefinite" path="{p1}"/></circle>
<circle r="3.5"><animateMotion dur="4.8s" begin="1.1s" repeatCount="indefinite" path="{p2}"/></circle>
</g>
</svg>
'''
    suffix = "" if lang == "pt" else ".en"
    with open(f"{OUT}/hero-{theme}{suffix}.svg", "w") as f:
        f.write(svg)


if __name__ == "__main__":
    for th in THEMES:
        for lg in COPY:
            build(th, lg)
