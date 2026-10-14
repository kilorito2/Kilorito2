import math
import os
import random

import os
_QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR", os.path.join(_QUI, "salida"))
os.makedirs(OUT, exist_ok=True)
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"
SANS = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(
        panel="#121a21", line="#2a3641", ink="#ece7db", mute="#8a95a0",
        node="#1b232b", lk_stroke="#4b5662", lk_text="#6d7883", lk_line="#394552", lk_label="#6d7883",
        green="#5eb5a2", amber="#f0a93a", blue="#6fa8ff", coral="#f07a67",
    ),
    "light": dict(
        panel="#f8faf9", line="#cdd8d3", ink="#1b2227", mute="#5b6872",
        node="#ffffff", lk_stroke="#aab5b0", lk_text="#8d9a95", lk_line="#c3cec9", lk_label="#7e8b86",
        green="#23796a", amber="#b9690b", blue="#2f62c9", coral="#c0432f",
    ),
}

ARMS = {
    "esc": dict(title="Escritorio", color="green", cx=140),
    "fro": dict(title="Frontend", color="amber", cx=340),
    "3d": dict(title="3D y animación", color="blue", cx=585),
    "her": dict(title="Herramientas", color="coral", cx=820),
}

# tier: root (raiz de rama), node, cap (capstone). learned=False -> gris con candado.
# Los nodos grises son un ejemplo: editar a gusto.
N = lambda id, label, mono, x, y, arm, learned, parents, tier="node": dict(
    id=id, label=label, mono=mono, x=x, y=y, arm=arm, learned=learned, parents=parents, tier=tier)

NODES = [
    N("R", "kilorito2", "~", 480, 590, None, True, [], "base"),
    # Escritorio
    N("e0", "Electron", "El", 140, 500, "esc", True, ["R"], "root"),
    N("e1", "Node.js", "No", 85, 430, "esc", True, ["e0"]),
    N("e2", "Rust", "Rs", 195, 430, "esc", True, ["e0"]),
    N("e3", "SQLite", "SQ", 50, 360, "esc", False, ["e1"]),
    N("e4", "Tauri", "Ta", 140, 360, "esc", False, ["e1", "e2"]),
    N("e5", "Escritorio pro", "*", 140, 250, "esc", False, ["e4"], "cap"),
    # Frontend
    N("f0", "HTML", "HT", 340, 500, "fro", True, ["R"], "root"),
    N("f1", "CSS", "CS", 295, 430, "fro", True, ["f0"]),
    N("f2", "JavaScript", "JS", 385, 430, "fro", True, ["f0"]),
    N("f3", "Tailwind", "Tw", 260, 360, "fro", True, ["f1"]),
    N("f4", "TypeScript", "TS", 385, 360, "fro", True, ["f2"]),
    N("f5", "React", "Rx", 325, 290, "fro", True, ["f3", "f4"]),
    N("f6", "Vite", "Vi", 430, 290, "fro", True, ["f4"]),
    N("f7", "Next.js", "Nx", 380, 220, "fro", True, ["f5", "f6"]),
    N("f8", "Testing", "Te", 275, 220, "fro", False, ["f5"]),
    N("f9", "Accesibilidad", "a11y", 465, 220, "fro", False, ["f6"]),
    N("f10", "Frontend pro", "*", 330, 150, "fro", False, ["f7", "f8"], "cap"),
    # 3D y animacion
    N("a0", "GSAP", "Gs", 585, 500, "3d", True, ["R"], "root"),
    N("a1", "Lenis", "Ln", 540, 430, "3d", True, ["a0"]),
    N("a2", "Three.js", "Th", 630, 430, "3d", True, ["a0"]),
    N("a3", "Shaders GLSL", "Sh", 585, 360, "3d", False, ["a1", "a2"]),
    N("a4", "Blender", "Bl", 675, 360, "3d", False, ["a2"]),
    N("a5", "3D pro", "*", 630, 250, "3d", False, ["a3", "a4"], "cap"),
    # Herramientas
    N("h0", "Git", "Gt", 820, 500, "her", True, ["R"], "root"),
    N("h1", "GitHub", "GH", 775, 430, "her", True, ["h0"]),
    N("h2", "VS Code", "VS", 865, 430, "her", True, ["h0"]),
    N("h3", "Vercel", "Vc", 740, 360, "her", True, ["h1"]),
    N("h4", "Netlify", "Nl", 865, 360, "her", True, ["h2"]),
    N("h5", "GitHub Actions", "CI", 805, 290, "her", False, ["h3", "h4"]),
    N("h6", "Docker", "Dk", 895, 290, "her", False, ["h4"]),
    N("h7", "PostgreSQL", "Pg", 705, 290, "her", False, ["h3"]),
    N("h8", "DevOps", "*", 820, 200, "her", False, ["h5", "h6"], "cap"),
]
BY = {n["id"]: n for n in NODES}

# profundidad (para escalonar la animacion de crecimiento)
depth = {}
for n in NODES:
    depth[n["id"]] = 0 if not n["parents"] else 1 + max(depth[p] for p in n["parents"])

R_OF = {"base": 24, "root": 22, "node": 18, "cap": 26}
STEP = 0.26

import json
_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "icons.json"), encoding="utf-8") as _f:
    SI = json.load(_f)

VSCODE_D = ("M90.767 127.126a7.97 7.97 0 0 0 6.35-.244l26.353-12.681a8 8 0 0 0 4.53-7.209V21.009a8 8 0 0 0-4.53-7.21L97.117 1.12a7.97 7.97 0 0 0-9.093 1.548l-50.45 46.026L15.6 32.013a5.33 5.33 0 0 0-6.807.302l-7.048 6.411a5.335 5.335 0 0 0-.006 7.888L20.796 64L1.74 81.387a5.336 5.336 0 0 0 .006 7.887l7.048 6.411a5.33 5.33 0 0 0 6.807.303l21.974-16.68l50.45 46.025a8 8 0 0 0 2.743 1.793Zm5.252-92.183L57.74 64l38.28 29.058V34.943Z")
# glifos genericos (lucide, ISC): no son logos de marca
STROKE_GLYPHS = {
    "a11y": '<circle cx="16" cy="4" r="1"/><path d="m18 19l1-7l-6 1M5 8l3-3l5.5 3l-2.36 3.5m-6.9 3a5 5 0 0 0 6.88 6"/><path d="M13.76 17.5a5 5 0 0 0-6.88-6"/>',
    "scroll": '<rect width="14" height="20" x="5" y="2" rx="7"/><path d="M12 6v4"/>',
    "sparkles": '<path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594zM20 2v4m2-2h-4"/><circle cx="4" cy="20" r="2"/>',
}
# nodo -> logo
ICON_OF = {
    "e0": "electron", "e1": "nodejs", "e2": "rust", "e3": "sqlite", "e4": "tauri",
    "f0": "html", "f1": "css", "f2": "js", "f3": "tailwind", "f4": "ts", "f5": "react", "f6": "vite", "f7": "next",
    "f8": "testing", "f9": "@a11y",
    "a0": "gsap", "a1": "@scroll", "a2": "three", "a3": "@sparkles", "a4": "blender",
    "h0": "git", "h1": "github", "h2": "@vscode", "h3": "vercel", "h4": "netlify",
    "h5": "actions", "h6": "docker", "h7": "postgres",
}


def icon(n, color, size):
    key = ICON_OF.get(n["id"])
    x, y = n["x"], n["y"]
    if key is None:
        return f'<text x="{x}" y="{y + 4}" text-anchor="middle" class="mono" font-size="12" font-weight="700" fill="{color}">{n["mono"]}</text>'
    if key == "@vscode":
        sc = size / 128
        return (f'<path d="{VSCODE_D}" transform="translate({x - size / 2:.2f} {y - size / 2:.2f}) scale({sc:.4f})" '
                f'fill="{color}" fill-rule="evenodd"/>')
    if key.startswith("@"):
        sc = size / 24
        return (f'<g transform="translate({x - size / 2:.2f} {y - size / 2:.2f}) scale({sc:.4f})" fill="none" stroke="{color}" '
                f'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">{STROKE_GLYPHS[key[1:]]}</g>')
    sc = size / 24
    return (f'<path d="{SI[key]["path"]}" transform="translate({x - size / 2:.2f} {y - size / 2:.2f}) scale({sc:.4f})" fill="{color}"/>')




W0 = 3.4        # segundos: cuando arranca la onda de energia (despues del intro)
P = 8.0         # periodo de la onda
WSTEP = 0.34    # segundos que tarda la onda en pasar de un nivel al siguiente
TEASE = 1.2     # segundos que dura el intento de desbloqueo de cada nodo gris
ARM_ORDER = list(ARMS.keys())

GRAYS = sorted([n for n in NODES if not n["learned"]], key=lambda n: (depth[n["id"]], ARM_ORDER.index(n["arm"])))
TEASE_T = len(GRAYS) * TEASE
TEASE_IDX = {n["id"]: i for i, n in enumerate(GRAYS)}


def lock(n, c):
    r = R_OF[n["tier"]]
    cx, cy = n["x"] + r * 0.72, n["y"] + r * 0.72
    d = W0 + 1.0 + TEASE_IDX[n["id"]] * TEASE
    return (
        f'<g class="lk" style="animation-delay:{d:.2f}s;transform-origin:{cx:.1f}px {cy:.1f}px">'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8.5" fill="{c["panel"]}" stroke="{c["lk_stroke"]}" stroke-width="1.6"/>'
        f'<rect x="{cx - 3.6:.1f}" y="{cy - 0.6:.1f}" width="7.2" height="5.2" rx="1" fill="{c["lk_text"]}"/>'
        f'<path d="M{cx - 2.2:.1f} {cy - 0.8:.1f}v-1.8a2.2 2.2 0 0 1 4.4 0v1.8" fill="none" stroke="{c["lk_text"]}" stroke-width="1.5"/>'
        f"</g>"
    )


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def tree(t):
    c = THEMES[t]
    col = lambda arm: c[ARMS[arm]["color"]] if arm else c["ink"]
    rnd = random.Random(11)

    edges_gray, edges_col, heads, pulses = [], [], [], []
    for n in NODES:
        for p in n["parents"]:
            a = BY[p]
            d = STEP * depth[p] + 0.15
            both = a["learned"] and n["learned"]
            stroke = col(n["arm"]) if both else c["lk_line"]
            wid = 4 if both else 2.5
            xy = f'x1="{a["x"]}" y1="{a["y"]}" x2="{n["x"]}" y2="{n["y"]}" pathLength="1"'
            ln = f'<line class="e" {xy} stroke="{stroke}" stroke-width="{wid}" stroke-linecap="round" style="animation-delay:{d:.2f}s"/>'
            if both:
                edges_col.append(ln)
                heads.append(f'<line class="hd" {xy} stroke="{c["ink"]}" stroke-width="5" stroke-linecap="round" style="animation-delay:{d:.2f}s"/>')
                pulses.append(f'<line class="pl" {xy} stroke="{c["ink"]}" stroke-width="3.2" stroke-linecap="round" '
                              f'style="animation-delay:{W0 + depth[p] * WSTEP:.2f}s"/>')
            else:
                edges_gray.append(ln)

    under, nodes_svg, labels, motes = [], [], [], []
    for n in NODES:
        r = R_OF[n["tier"]]
        x, y = n["x"], n["y"]
        dn = STEP * depth[n["id"]]
        k = col(n["arm"])
        org = f"transform-origin:{x}px {y}px"
        g = f'<g class="n" style="animation-delay:{dn:.2f}s;{org}">'
        if n["tier"] == "base":
            under.append(f'<circle class="wr" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c["ink"]}" stroke-width="2.5" style="animation-delay:{W0:.2f}s;{org}"/>')
            g += (f'<circle class="halo" cx="{x}" cy="{y}" r="{r + 6}" fill="none" stroke="{c["ink"]}" stroke-width="2" style="{org}"/>'
                  f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["node"]}" stroke="{c["ink"]}" stroke-width="3"/>'
                  f'<text x="{x}" y="{y + 7}" text-anchor="middle" class="mono" font-size="22" font-weight="700" fill="{c["ink"]}">~</text>')
        elif n["learned"]:
            under.append(f'<circle class="bu" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{k}" stroke-width="3" style="animation-delay:{dn + 0.22:.2f}s;{org}"/>')
            under.append(f'<circle class="wr" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{k}" stroke-width="2.5" style="animation-delay:{W0 + depth[n["id"]] * WSTEP:.2f}s;{org}"/>')
            if n["tier"] == "root":
                g += (f'<circle class="halo" cx="{x}" cy="{y}" r="{r + 6}" fill="none" stroke="{k}" stroke-width="2" '
                      f'style="{org};animation-delay:{(sum(map(ord, n["id"])) % 20) / 10:.1f}s"/>')
            g += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["node"]}" stroke="{k}" stroke-width="3"/>'
                  f'<circle cx="{x}" cy="{y}" r="{r - 4}" fill="{k}" fill-opacity=".14"/>'
                  f'<circle class="wf" cx="{x}" cy="{y}" r="{r - 3}" fill="{k}" style="animation-delay:{W0 + depth[n["id"]] * WSTEP:.2f}s"/>')
            if n["tier"] == "root":
                g += f'<circle cx="{x}" cy="{y}" r="{r + 3}" fill="none" stroke="{c["ink"]}" stroke-opacity=".85" stroke-width="1.4"/>'
            g += icon(n, k, 33 if r >= 22 else 20)
            # particulas que suben por las ramas aprendidas
            for _ in range(2 if n["tier"] != "root" else 3):
                mx = x + rnd.uniform(-16, 16)
                my = y + rnd.uniform(-12, 6)
                sz = rnd.uniform(1.3, 2.4)
                dur = rnd.uniform(5.5, 9.0)
                dly = W0 - 1 + rnd.uniform(0, 8)
                motes.append(
                    f'<circle class="mt" cx="{mx:.1f}" cy="{my:.1f}" r="{sz:.1f}" fill="{k}" '
                    f'style="--dx:{rnd.uniform(-10, 10):.0f}px;--dy:{-rnd.uniform(45, 95):.0f}px;animation-duration:{dur:.1f}s;animation-delay:{dly:.1f}s"/>')
        else:
            idx = TEASE_IDX[n["id"]]
            td = W0 + 1.0 + idx * TEASE
            under.append(f'<circle class="tz" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c["lk_stroke"]}" stroke-width="2.5" style="animation-delay:{td:.2f}s;{org}"/>')
            g += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["node"]}" stroke="{c["lk_stroke"]}" stroke-width="2.5"/>'
            if n["tier"] == "cap":
                under.append(f'<circle class="orb" cx="{x}" cy="{y}" r="{r + 8}" fill="none" stroke="{c["lk_stroke"]}" stroke-width="1.6" '
                             f'stroke-dasharray="3 7" stroke-linecap="round" style="{org}"/>')
                g += f'<g class="tw" style="{org};animation-delay:{(sum(map(ord, n["id"])) % 30) / 10:.1f}s">{star(x, y, 12, c["lk_text"])}</g>'
            else:
                g += icon(n, c["lk_text"], 20)
            g += lock(n, c)
        g += "</g>"
        nodes_svg.append(g)
        lab_col = c["ink"] if n["learned"] else c["lk_label"]
        labels.append(
            f'<text class="lb" x="{x}" y="{y + r + 16}" text-anchor="middle" font-size="12.5" '
            f'font-weight="{600 if n["learned"] else 500}" fill="{lab_col}" stroke="{c["panel"]}" stroke-width="5" '
            f'stroke-linejoin="round" paint-order="stroke" style="animation-delay:{dn + 0.2:.2f}s">{n["label"]}</text>')

    titles = ""
    for key, a in ARMS.items():
        mem = [n for n in NODES if n["arm"] == key]
        got = sum(1 for n in mem if n["learned"])
        titles += (f'<text x="{a["cx"]}" y="64" text-anchor="middle" font-size="16" font-weight="700" fill="{c[a["color"]]}" class="tt">'
                   f'{a["title"]}<tspan fill="{c["mute"]}" font-weight="500"> {got}/{len(mem)}</tspan></text>')
    total = sum(1 for n in NODES if n["arm"])
    got_all = sum(1 for n in NODES if n["arm"] and n["learned"])

    legend = (
        f'<circle cx="46" cy="654" r="7" fill="{c["node"]}" stroke="{c["amber"]}" stroke-width="2.5"/>'
        f'<text x="60" y="658.5" font-size="12.5" fill="{c["mute"]}">aprendido</text>'
        f'<circle cx="150" cy="654" r="7" fill="{c["node"]}" stroke="{c["lk_stroke"]}" stroke-width="2.5"/>'
        f'<text x="164" y="658.5" font-size="12.5" fill="{c["mute"]}">por desbloquear</text>'
        f'<text x="914" y="658.5" text-anchor="end" font-size="12.5" fill="{c["mute"]}">{got_all}/{total} desbloqueados</text>'
    )

    s = TEASE / TEASE_T * 100   # % del ciclo que dura un intento
    q = lambda f: f * s
    css = f"""
.mono{{font-family:{MONO}}}
text{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.e{{stroke-dasharray:1;animation:draw .5s ease-out both}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.hd{{stroke-dasharray:.05 1;opacity:0;animation:head .6s ease-out forwards}}
@keyframes head{{0%{{stroke-dashoffset:0;opacity:1}}83%{{stroke-dashoffset:-.95;opacity:1}}100%{{stroke-dashoffset:-.95;opacity:0}}}}
.n{{animation:pop .55s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{opacity:0;transform:scale(.1)}}to{{opacity:1;transform:scale(1)}}}}
.bu{{opacity:0;animation:burst .8s ease-out both}}
@keyframes burst{{0%{{opacity:.95;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
.lb{{animation:fade .5s ease-out both}}
.tt{{animation:fade .8s ease-out .2s both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.pl{{stroke-dasharray:.07 .93;opacity:0;animation:zap {P}s linear infinite}}
@keyframes zap{{0%{{stroke-dashoffset:0;opacity:1}}4%{{stroke-dashoffset:-1;opacity:1}}4.01%,100%{{stroke-dashoffset:-1;opacity:0}}}}
.wr{{opacity:0;animation:wring {P}s ease-out infinite}}
@keyframes wring{{0%{{opacity:0;transform:scale(1)}}2%{{opacity:.85;transform:scale(1.12)}}15%{{opacity:0;transform:scale(1.9)}}100%{{opacity:0}}}}
.wf{{opacity:0;animation:wflash {P}s ease-out infinite}}
@keyframes wflash{{0%{{opacity:0}}2%{{opacity:.5}}13%{{opacity:0}}100%{{opacity:0}}}}
.halo{{animation:breathe 3.6s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{opacity:.15;transform:scale(1)}}50%{{opacity:.6;transform:scale(1.22)}}}}
.mt{{opacity:0;animation:rise 7s ease-out infinite}}
@keyframes rise{{0%{{opacity:0;transform:translate(0,0)}}15%{{opacity:.75}}100%{{opacity:0;transform:translate(var(--dx),var(--dy))}}}}
.lk{{animation:wig {TEASE_T:.1f}s ease-in-out infinite}}
@keyframes wig{{0%{{transform:rotate(0)}}{q(.15):.2f}%{{transform:rotate(-18deg)}}{q(.35):.2f}%{{transform:rotate(15deg)}}{q(.55):.2f}%{{transform:rotate(-9deg)}}{q(.75):.2f}%{{transform:rotate(5deg)}}{q(1):.2f}%,100%{{transform:rotate(0)}}}}
.tz{{opacity:0;animation:tease {TEASE_T:.1f}s ease-out infinite}}
@keyframes tease{{0%{{opacity:0;transform:scale(1)}}{q(.1):.2f}%{{opacity:.8}}{q(1):.2f}%{{opacity:0;transform:scale(1.7)}}100%{{opacity:0}}}}
.orb{{animation:spin 30s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.tw{{animation:twinkle 4.2s ease-in-out infinite}}
@keyframes twinkle{{0%,100%{{opacity:.6;transform:scale(1)}}50%{{opacity:1;transform:scale(1.14)}}}}
@media (prefers-reduced-motion:reduce){{.e,.n,.bu,.lb,.tt,.hd,.pl,.wr,.wf,.halo,.mt,.lk,.tz,.orb,.tw{{animation:none!important}}.pl,.hd,.mt,.bu,.wr,.wf,.tz{{display:none}}}}
"""
    alt = "Árbol de habilidades. " + " ".join(
        f'{ARMS[k]["title"]}: ' + ", ".join(
            f'{n["label"]}{"" if n["learned"] else " (por desbloquear)"}' for n in NODES if n["arm"] == k) + "."
        for k in ARMS)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 680" width="960" height="680" role="img" aria-labelledby="t">
<title id="t">{alt}</title>
<defs>
<filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="960" height="680"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>{css}</style>
<rect x="1" y="1" width="958" height="678" rx="14" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="2"/>
{titles}
{"".join(edges_gray)}
<g filter="url(#glow)">{"".join(edges_col)}</g>
<g filter="url(#glow)">{"".join(heads)}{"".join(pulses)}</g>
{"".join(motes)}
{"".join(under)}
{"".join(nodes_svg)}
{"".join(labels)}
{legend}
</svg>
'''


for t in THEMES:
    with open(os.path.join(OUT, f"stack-{t}.svg"), "w", encoding="utf-8") as f:
        f.write(tree(t))
print("ok", len(GRAYS), "grises, ciclo", TEASE_T, "s")
