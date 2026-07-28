# Como instalar

Tudo vai para o repositório especial de perfil: **`Matheus2ds/Matheush2ds`** (nome do repo = seu username).

```
Matheush2ds/
├── README.md
├── assets/
│   ├── hero.svg
│   ├── terminal.svg
│   ├── stack-3d.svg
│   ├── architecture.svg
│   └── skills.svg
├── tools/                 ← geradores (opcional, só pra você editar depois)
│   ├── gen_hero.py
│   ├── gen_terminal.py
│   ├── gen_cube.py
│   └── gen_arch_skills.py
└── .github/workflows/
    ├── profile-3d.yml
    └── snake.yml
```

Depois do primeiro push, vá em **Actions** e rode `GitHub Profile 3D Contrib` e `Generate Snake Animation` manualmente uma vez. Antes disso essas duas imagens aparecem quebradas — o resto funciona na hora.

---

## O que é custom aqui

As 5 peças em `assets/` não vêm de serviço nenhum. São SVGs gerados por script, animados com **SMIL puro** (sem JavaScript, que o GitHub bloqueia):

| arquivo | o que faz |
|:--|:--|
| `hero.svg` | grid em perspectiva com fuga real, constelação de 35 nós com pacotes viajando entre eles, nome com gradiente que varre |
| `terminal.svg` | terminal que digita comando por comando; o typewriter é um retângulo da cor do fundo deslizando sobre o texto, tudo num ciclo de 26s sincronizado |
| `stack-3d.svg` | cubo 3D de verdade: 72 frames de projeção em perspectiva calculados em Python, com backface culling por produto escalar do normal |
| `architecture.svg` | request percorrendo Client → Gateway → Service → Redis/Postgres, com `animateMotion` nos paths e o response voltando pelo arco |
| `skills.svg` | barras preenchendo com `scaleX`, brilho correndo por cima e stagger entre linhas |

---

## Editando

Precisa só de Python 3 (sem dependências):

```bash
python3 tools/gen_hero.py         # → assets/hero.svg
python3 tools/gen_terminal.py     # → assets/terminal.svg
python3 tools/gen_cube.py         # → assets/stack-3d.svg
python3 tools/gen_arch_skills.py  # → assets/architecture.svg + skills.svg
```

Onde mexer:

- **Texto do terminal** → lista `script` em `gen_terminal.py`. Cada linha é `("cmd"|"out", segundo_em_que_aparece, conteúdo)`.
- **Faces do cubo** → lista `FACES` em `gen_cube.py`. Quer girar mais rápido? `DUR`. Mais suave? `FRAMES`.
- **Caixas do diagrama** → listas `cards` e `edges` em `gen_arch_skills.py`.
- **Percentuais das barras** → `skills_l` / `skills_r` no mesmo arquivo. São auto-avaliação, ajuste pro que você considera honesto.
- **Paleta** → as constantes no topo de cada script (`PRIM`, `LIGHT`, `DEEP`, `BORDER`...).

---

## Detalhes que importam

- **Não use `.svg` com JavaScript.** O GitHub serve imagem via proxy e mata script; SMIL e CSS `@keyframes` passam.
- **Fontes externas não carregam** no SVG proxiado. Os scripts usam só stacks de fonte do sistema (`ui-monospace`, `Segoe UI`), então o texto renderiza em qualquer máquina.
- **Caminho relativo funciona** (`./assets/hero.svg`) e é melhor que URL absoluta: o cache do proxy não te trava numa versão antiga.
- **Prefers-color-scheme** já está no snake. As outras peças são dark-only de propósito — o fundo `#0d1117` bate com o tema escuro do GitHub e continua legível no claro.
- **Peso total** dos assets: ~150 KB. O cubo é o maior (57 KB) porque carrega os 72 frames de geometria.
