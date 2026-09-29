"""Gera os cartões de projeto e o diagrama de pipeline do perfil.

Saída em assets/:
    projects-{dark,light}{,.en}.svg
    pipeline-{dark,light}{,.en}.svg

Usa as mesmas fontes e o mesmo esquema de glifos reaproveitados do gen_hero.py.
    python tools/gen_cards.py ./fonts ./assets
"""
from gen_hero import DEFS, DISPLAY, BODY, MONO, OUT

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", edge="#21262d", chip="#20262e", ink="#e6edf3",
                 muted="#9da7b3", faint="#6e7681", line="#3d4651", accent="#2bb3a3"),
    "light": dict(bg="#ffffff", card="#f6f8fa", edge="#d0d7de", chip="#eaeef2", ink="#1f2328",
                  muted="#59636e", faint="#818b98", line="#b6c0ca", accent="#0f766e"),
}

PROJECTS = {
    "pt": [
        dict(kind="SAAS B2B", name="Optima Control",
             text="Gestão completa para dedetizadoras: ordens de serviço, estoque, "
                  "contas a pagar e receber, cobrança integrada e certificados em PDF "
                  "com assinatura digital.",
             flow=["OS", "execução", "certificado", "cobrança"],
             stack=["Next.js", "Prisma", "PostgreSQL", "Playwright"]),
        dict(kind="SEGURANÇA DO TRABALHO", name="Portal SST",
             text="Entrega de EPI com assinatura digital e mapeamento de risco "
                  "psicossocial (NR-1), atrás de um API gateway com login único.",
             flow=["gateway", "EPI", "psicossocial", "PDF"],
             stack=["Node.js", "FastAPI", "Prisma", "PostgreSQL"]),
        dict(kind="OPERAÇÃO E FINANCEIRO", name="ERP de temporada",
             text="Aluguel por temporada de ponta a ponta: reservas, kits de enxoval, "
                  "almoxarifado, ordens de limpeza e repasse ao proprietário.",
             flow=["reserva", "kit", "limpeza", "repasse"],
             stack=["Express", "Sequelize", "PostgreSQL", "React"]),
    ],
    "en": [
        dict(kind="B2B SAAS", name="Optima Control",
             text="End-to-end management for pest control companies: work orders, "
                  "inventory, payables and receivables, integrated billing and PDF "
                  "certificates with digital signature.",
             flow=["order", "service", "certificate", "billing"],
             stack=["Next.js", "Prisma", "PostgreSQL", "Playwright"]),
        dict(kind="OCCUPATIONAL SAFETY", name="Portal SST",
             text="PPE delivery with digital signature and psychosocial risk "
                  "assessment (Brazil's NR-1), behind an API gateway with single sign-on.",
             flow=["gateway", "PPE", "psychosocial", "PDF"],
             stack=["Node.js", "FastAPI", "Prisma", "PostgreSQL"]),
        dict(kind="OPERATIONS AND FINANCE", name="Vacation rental ERP",
             text="Short-term rentals end to end: bookings, linen kits, stockroom, "
                  "cleaning orders and owner payouts.",
             flow=["booking", "kit", "cleaning", "payout"],
             stack=["Express", "Sequelize", "PostgreSQL", "React"]),
    ],
}

PIPELINE = {
    "pt": dict(
        eyebrow="DO COMMIT À PRODUÇÃO  ·  OPTIMA CONTROL",
        stages=[("commit", "GitHub Actions"), ("lint e tipos", "ESLint · tsc"), ("testes", "Vitest"),
                ("migrations + RLS", "Prisma · Postgres"), ("E2E", "Playwright"), ("deploy", "Railway")],
        ops=[("backup agendado", "cron no CI"), ("ensaio de restauração", "restaura e confere")],
        title="Pipeline do Optima Control, do commit ao deploy, com backup e ensaio de restauração"),
    "en": dict(
        eyebrow="FROM COMMIT TO PRODUCTION  ·  OPTIMA CONTROL",
        stages=[("commit", "GitHub Actions"), ("lint and types", "ESLint · tsc"), ("tests", "Vitest"),
                ("migrations + RLS", "Prisma · Postgres"), ("E2E", "Playwright"), ("deploy", "Railway")],
        ops=[("scheduled backup", "cron in CI"), ("restore drill", "restores and checks")],
        title="Optima Control pipeline, from commit to deploy, with backups and a restore drill"),
}


def wrap(face, text, size, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        _, w = face.path(trial, size, 0, 0)
        if w > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    lines.append(cur)
    return lines


def arrow(x, y, color):
    return (f'<path d="M{x-6:.1f},{y} H{x+5:.1f} M{x+1:.1f},{y-3.5} L{x+5:.1f},{y} L{x+1:.1f},{y+3.5}" '
            f'fill="none" stroke="{color}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>')


def svg_doc(w, h, title, body, defs_extra=""):
    defs = "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t">\n<title id="t">{title}</title>\n<defs>{defs}{defs_extra}</defs>\n'
            f'<style>@media (prefers-reduced-motion: reduce){{.pulse{{display:none}}}}</style>\n{body}</svg>\n')


def projects(theme, lang):
    DEFS.clear()
    c = THEMES[theme]
    cards = PROJECTS[lang]
    CW, GAP, PAD = 384, 24, 26
    inner = CW - 2 * PAD
    blocks, heights = [], []
    for i, p in enumerate(cards):
        x0 = i * (CW + GAP)
        parts = []
        eb, _ = MONO.path(p["kind"], 11.5, x0 + PAD, 50, tracking=0.12)
        parts.append(f'<g fill="{c["accent"]}">{eb}</g>')
        nm, _ = DISPLAY.path(p["name"], 27, x0 + PAD, 88, tracking=-0.01)
        parts.append(f'<g fill="{c["ink"]}">{nm}</g>')
        y = 122
        txt = []
        for line in wrap(BODY, p["text"], 15.5, inner):
            d, _ = BODY.path(line, 15.5, x0 + PAD, y)
            txt.append(d)
            y += 23
        parts.append(f'<g fill="{c["muted"]}">{"".join(txt)}</g>')
        blocks.append((x0, parts, y, p))
        heights.append(y)

    top_flow = max(heights) + 14
    body = []
    for x0, parts, _, p in blocks:
        # fluxo do produto, em mono, com setas desenhadas
        fx, fy = x0 + PAD, top_flow
        flow, arrows = [], []
        for j, step in enumerate(p["flow"]):
            d, w = MONO.path(step, 12, fx, fy)
            flow.append(d)
            fx += w
            if j < len(p["flow"]) - 1:
                arrows.append(arrow(fx + 12, fy - 4, c["line"]))
                fx += 24
        parts.append(f'<g fill="{c["faint"]}">{"".join(flow)}</g>{"".join(arrows)}')
        # divisória e chips da stack
        hy = top_flow + 22
        parts.append(f'<path d="M{x0+PAD},{hy} H{x0+CW-PAD}" stroke="{c["edge"]}" stroke-width="1"/>')
        cx, cy = x0 + PAD, hy + 18
        chips = []
        for s in p["stack"]:
            _, w = MONO.path(s, 12, 0, 0)
            cwid = w + 16
            if cx + cwid > x0 + CW - PAD:
                cx, cy = x0 + PAD, cy + 32
            d, _ = MONO.path(s, 12, cx + 8, cy + 16.5)
            chips.append(f'<rect x="{cx:.1f}" y="{cy}" width="{cwid:.1f}" height="24" rx="6" fill="{c["chip"]}"/>'
                         f'<g fill="{c["muted"]}">{d}</g>')
            cx += cwid + 8
        parts.append("".join(chips))
        p["_bottom"] = cy + 24
        body.append(parts)

    H = int(max(p["_bottom"] for _, _, _, p in blocks) + PAD)
    out = []
    for (x0, _, _, _), parts in zip(blocks, body):
        out.append(f'<rect x="{x0+0.5}" y="0.5" width="{CW-1}" height="{H-1}" rx="12" '
                   f'fill="{c["card"]}" stroke="{c["edge"]}"/>')
        out.append("".join(parts))
    title = "Projetos selecionados" if lang == "pt" else "Selected work"
    title += ": " + ", ".join(p["name"] for p in cards)
    suffix = "" if lang == "pt" else ".en"
    with open(f"{OUT}/projects-{theme}{suffix}.svg", "w") as f:
        f.write(svg_doc(1200, H, title, "\n".join(out) + "\n"))


def pipeline(theme, lang):
    DEFS.clear()
    c, t = THEMES[theme], PIPELINE[lang]
    W, H = 1200, 340
    out = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{c["card"]}" stroke="{c["edge"]}"/>']
    eb, _ = MONO.path(t["eyebrow"], 12, 48, 52, tracking=0.12)
    out.append(f'<g fill="{c["accent"]}">{eb}</g>')

    n = len(t["stages"])
    xs = [120 + i * (960 / (n - 1)) for i in range(n)]
    ym = 126
    main = f"M{xs[0]},{ym} H{xs[-1]}"
    yo = 236
    ox = [xs[-1] - 240, xs[-1] - 560]
    loop = f"M{xs[-1]},{ym + 76} V{yo} H{ox[1]}"
    out.append(f'<g fill="none" stroke="{c["line"]}" stroke-width="1.5" stroke-linejoin="round">'
               f'<path d="{main}"/><path d="{loop}" stroke-dasharray="4 5"/></g>')

    labels, caps = [], []
    for x, (label, cap) in zip(xs, t["stages"]):
        _, w = BODY.path(label, 17, 0, 0)
        d, _ = BODY.path(label, 17, x - w / 2, ym + 40)
        labels.append(d)
        _, w = MONO.path(cap, 12.5, 0, 0)
        d, _ = MONO.path(cap, 12.5, x - w / 2, ym + 62)
        caps.append(d)
    for x, (label, cap) in zip(ox, t["ops"]):
        _, w = BODY.path(label, 17, 0, 0)
        d, _ = BODY.path(label, 17, x - w / 2, yo + 40)
        labels.append(d)
        _, w = MONO.path(cap, 12.5, 0, 0)
        d, _ = MONO.path(cap, 12.5, x - w / 2, yo + 62)
        caps.append(d)
    out.append(f'<g fill="{c["ink"]}">{"".join(labels)}</g>')
    out.append(f'<g fill="{c["faint"]}">{"".join(caps)}</g>')

    nodes = "".join(f'<circle cx="{x:.1f}" cy="{ym}" r="8"/>' for x in xs)
    nodes += "".join(f'<rect x="{x-7:.1f}" y="{yo-7}" width="14" height="14" rx="3"/>' for x in ox)
    out.append(f'<g fill="{c["card"]}" stroke="{c["accent"]}" stroke-width="2">{nodes}</g>')
    out.append(f'<circle cx="{xs[-1]:.1f}" cy="{ym}" r="3.5" fill="{c["accent"]}"/>')
    out.append(f'<g class="pulse" fill="{c["accent"]}">'
               f'<circle r="4"><animateMotion dur="5s" repeatCount="indefinite" path="{main}"/></circle>'
               f'<circle r="3.5"><animateMotion dur="6s" begin="2.5s" repeatCount="indefinite" path="{loop}"/></circle>'
               f'</g>')
    suffix = "" if lang == "pt" else ".en"
    with open(f"{OUT}/pipeline-{theme}{suffix}.svg", "w") as f:
        f.write(svg_doc(W, H, t["title"], "\n".join(out) + "\n"))


if __name__ == "__main__":
    for th in THEMES:
        for lg in PROJECTS:
            projects(th, lg)
            pipeline(th, lg)
