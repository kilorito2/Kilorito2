import json, os
from xml.sax.saxutils import escape
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get("OUT_DIR", os.path.join(HERE, "salida")), "cards")
os.makedirs(OUT, exist_ok=True)
SI = json.load(open(f"{HERE}/icons.json", encoding="utf-8"))
SANS = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"
TH = {
 "dark":  dict(panel="#111a21", bar="#17222b", line="#2a3641", ink="#ece7db", txt="#c3cbd1", mute="#8a95a0", amber="#f0a93a", green="#3fb950", gray="#5b6872", shine="#ffffff", shine_o=".10", blue="#3a6ea5"),
 "light": dict(panel="#f8faf9", bar="#edf1ef", line="#cdd8d3", ink="#1b2227", txt="#3b4750", mute="#5b6872", amber="#b9690b", green="#1a7f37", gray="#9aa7a1", shine="#b9690b", shine_o=".14", blue="#3a6ea5"),
}
LABEL = {"electron": "Electron", "react": "React", "ts": "TypeScript", "tailwind": "Tailwind CSS", "next": "Next.js", "three": "Three.js", "nodejs": "Node.js", "rust": "Rust"}

CARDS = [
 dict(id="sakana", slug="sakana-desktop", name="Sakana Desktop", featured=True, big="electron",
      desc="Clon de escritorio de Sakana AI Chat con una capa de proveedores de IA agnóstica.",
      tech=["electron", "react", "ts", "tailwind"], pushed="02 oct", fresh=True),
 dict(id="mirra", slug="mirra-remote", name="Mirra", featured=True, big="electron",
      desc="Mirá y controlá tu PC con Windows desde el navegador del celular, por WiFi y con WebRTC. Sin cuentas y sin nube.",
      tech=["electron", "ts", "nodejs", "·WebRTC"], pushed="12 oct", fresh=True),
 dict(id="reversefolio", slug="reversefolio", name="ReverseFolio", featured=False,
      desc="Plataforma y widget para portfolios de devs: un árbol RPG de puntos ciegos y bugs, con embeds.",
      tech=["ts", "·Web Component", "·SVG"], pushed="26 sep", fresh=True),
 dict(id="huso", slug="huso", name="Huso", featured=False,
      desc="Agenda pública open source para freelancers y equipos: reservas online, disponibilidad, zonas horarias y emails automáticos.",
      tech=["ts", "·Open source"], pushed="04 sep", fresh=False),
 dict(id="esg", slug="panel-esg", name="Panel ESG para PYMEs", featured=False,
      desc="Energía, residuos y viajes en un solo lugar, con score ESG y recomendaciones accionables.",
      tech=["ts"], pushed="04 sep", fresh=False),
 dict(id="michi", slug="michi", name="Michi", featured=False,
      desc="Navegador para Windows hecho en Rust y sin barra de pestañas: la página ocupa toda la pantalla.",
      tech=["rust", "·WebView2"], pushed="13 oct", fresh=True),
]

def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out

def chip(x, y, key, c, delay):
    if key.startswith("·"):
        label = key[1:]; icon = False
    else:
        label = LABEL[key]; icon = True
    w = 12 + (18 if icon else 12) + len(label) * 7.0 + 6
    g = (f'<g class="ch" style="transform-origin:{x + w/2:.1f}px {y + 12}px;animation-delay:{delay:.2f}s">'
         f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{c["amber"]}" fill-opacity=".09" stroke="{c["amber"]}" stroke-opacity=".4"/>')
    if icon:
        g += f'<path d="{SI[key if key in SI else key]["path"]}" transform="translate({x + 9:.1f} {y + 5.5}) scale({13/24:.4f})" fill="{c["amber"]}"/>'
        tx = x + 28
    else:
        g += f'<circle cx="{x + 13:.1f}" cy="{y + 12}" r="2.6" fill="{c["amber"]}"/>'
        tx = x + 22
    g += f'<text x="{tx:.1f}" y="{y + 16}" class="mono" font-size="11.5" fill="{c["ink"]}">{escape(label)}</text></g>'
    return g, w

def card(spec, t, idx):
    c = TH[t]
    wide = spec["featured"]
    W = 960 if wide else 472
    H = 188 if wide else 200
    size = 27 if wide else 20
    ny = 74 if wide else 68
    N = len(spec["name"])
    tw = round(N * size * 0.56)
    nx = 22
    ph = idx * 1.6                     # desfase del ciclo de escritura
    PER = 16
    steps = N
    # --- barra de titulo
    status_txt = f'act. {spec["pushed"]}'
    sx_end = W - 92
    dot_x = sx_end - len(status_txt) * 6.6 - 10
    dot_col = c["green"] if spec["fresh"] else c["gray"]
    pulse = (f'<circle class="sd" cx="{dot_x:.1f}" cy="16" r="3.2" fill="none" stroke="{dot_col}" stroke-width="1.4" style="transform-origin:{dot_x:.1f}px 16px"/>'
             if spec["fresh"] else "")
    bar = (f'<rect x="0" y="0" width="{W}" height="32" fill="{c["bar"]}"/>'
           f'<rect x="14" y="9" width="17" height="14" rx="3" fill="{c["blue"]}"/>'
           f'<text x="22.5" y="19.6" text-anchor="middle" class="mono" font-size="9" font-weight="700" fill="#fff">&gt;_</text>'
           f'<text x="40" y="20.5" class="mono" font-size="11.5" fill="{c["mute"]}">PS C:\\proyectos\\{spec["slug"]}&gt;</text>'
           f'<circle cx="{dot_x:.1f}" cy="16" r="3.2" fill="{dot_col}"/>{pulse}'
           f'<text x="{sx_end}" y="20" text-anchor="end" class="mono" font-size="11" fill="{c["mute"]}">{status_txt}</text>'
           f'<g stroke="{c["mute"]}" stroke-width="1.3" fill="none" stroke-linecap="round">'
           f'<path d="M{W-78} 16.5h9"/><rect x="{W-54}" y="11.5" width="9" height="9" rx="1.2"/><path d="M{W-28} 11.5l9 9M{W-19} 11.5l-9 9"/></g>'
           f'<line class="ul" pathLength="1" x1="0" y1="32" x2="{W}" y2="32" stroke="{c["amber"]}" stroke-opacity=".75" stroke-width="1.6" style="animation-delay:{0.2 + idx*.12:.2f}s"/>')
    # --- nombre (tipeado en bucle)
    name = (f'<text x="{nx}" y="{ny}" class="sans" font-size="{size}" font-weight="700" fill="{c["ink"]}" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{escape(spec["name"])}</text>'
            f'<rect class="cv" x="{nx - 3}" y="{ny - size}" width="{tw + 8}" height="{round(size * 1.38)}" fill="{c["panel"]}"/>'
            f'<g class="cu"><rect class="bl" x="{nx - 1}" y="{ny - size + 3}" width="2.2" height="{round(size * 1.05)}" fill="{c["amber"]}"/></g>')
    tag = ""
    if wide:
        tgx = nx + tw + 18
        tag = (f'<g class="fd" style="animation-delay:{1.0 + idx*.1:.2f}s"><rect x="{tgx}" y="{ny - 19}" width="92" height="21" rx="10.5" fill="none" stroke="{c["amber"]}" stroke-opacity=".6"/>'
               f'<text x="{tgx + 46}" y="{ny - 4.5}" text-anchor="middle" class="mono" font-size="11" fill="{c["amber"]}">★ destacado</text></g>')
    # --- descripcion
    dfs = 14.5 if wide else 13.5
    lh = 21 if wide else 19.5
    lines = wrap(spec["desc"], 68 if wide else 54)
    dy0 = ny + (30 if wide else 28)
    desc = "".join(
        f'<text class="ds sans" x="{nx}" y="{dy0 + i*lh:.1f}" font-size="{dfs}" fill="{c["txt"]}" style="animation-delay:{0.55 + idx*.12 + i*.12:.2f}s">{escape(l)}</text>'
        for i, l in enumerate(lines))
    # --- chips
    cy_ = H - 44
    chips, x = "", nx
    for k, key in enumerate(spec["tech"]):
        g, w = chip(x, cy_, key, c, 0.9 + idx*.1 + k*.1)
        chips += g; x += w + 8
    # --- repo
    if wide:
        pw = 112
        px = W - 22 - pw
        repo = (f'<g class="rp"><rect x="{px}" y="{cy_}" width="{pw}" height="24" rx="12" fill="none" stroke="{c["amber"]}" stroke-opacity=".8"/>'
                f'<text x="{px + 14}" y="{cy_ + 16}" class="mono" font-size="11.5" fill="{c["amber"]}">ver repo</text>'
                f'<text class="ar mono" x="{px + pw - 24}" y="{cy_ + 16}" font-size="12" fill="{c["amber"]}">↗</text></g>')
    else:
        repo = (f'<g class="rp"><text x="{W - 40}" y="{cy_ + 16}" text-anchor="end" class="mono" font-size="11.5" fill="{c["amber"]}">ver repo</text>'
                f'<text class="ar mono" x="{W - 22}" y="{cy_ + 16}" text-anchor="end" font-size="12" fill="{c["amber"]}">↗</text></g>')
    deco = ""
    if wide:
        cxr, cyr = W - 232, 32 + (H - 32) / 2 - 2
        key = spec["big"]
        deco = (f'<circle cx="{cxr}" cy="{cyr}" r="54" fill="none" stroke="{c["line"]}" stroke-width="1.2"/>'
                f'<circle class="orb" cx="{cxr}" cy="{cyr}" r="68" fill="none" stroke="{c["amber"]}" stroke-opacity=".45" stroke-width="1.4" stroke-dasharray="3 9" stroke-linecap="round" style="transform-origin:{cxr}px {cyr}px"/>'
                f'<g class="fl" style="transform-origin:{cxr}px {cyr}px"><circle cx="{cxr}" cy="{cyr}" r="40" fill="{c["amber"]}" fill-opacity=".08"/>'
                f'<path d="{SI[key]["path"]}" transform="translate({cxr - 30} {cyr - 30}) scale({60/24})" fill="{c["amber"]}"/></g>')
    trace = f'<rect class="tc" pathLength="1" x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="none" stroke="{c["amber"]}" stroke-width="1.6" stroke-linecap="round" style="animation-delay:{idx*1.1:.1f}s"/>'
    css = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.cd{{animation:cin .7s cubic-bezier(.2,.8,.2,1) {idx*.12:.2f}s backwards}}
@keyframes cin{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.ul{{stroke-dasharray:1;animation:ulx .9s ease-out backwards}}
@keyframes ulx{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.cv{{transform-origin:{nx + tw + 5}px {ny}px;animation:ty {PER}s linear {ph:.1f}s infinite}}
@keyframes ty{{0%{{transform:scaleX(1);animation-timing-function:steps({steps},end)}}7%{{transform:scaleX(0)}}95%{{transform:scaleX(0);animation-timing-function:steps({steps},end)}}100%{{transform:scaleX(1)}}}}
.cu{{animation:cx {PER}s linear {ph:.1f}s infinite}}
@keyframes cx{{0%{{transform:translateX(0);animation-timing-function:steps({steps},end)}}7%{{transform:translateX({tw + 4}px)}}95%{{transform:translateX({tw + 4}px);animation-timing-function:steps({steps},end)}}100%{{transform:translateX(0)}}}}
.bl{{animation:blink 1.06s steps(1) infinite}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
.ds{{animation:fdx .7s ease-out backwards}}
.fd{{animation:fdx .7s ease-out backwards}}
@keyframes fdx{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
.ch{{animation:chp .5s cubic-bezier(.3,1.7,.5,1) backwards}}
@keyframes chp{{from{{opacity:0;transform:scale(.6)}}to{{opacity:1;transform:scale(1)}}}}
.sd{{opacity:0;animation:sdp 2.4s ease-out infinite}}
@keyframes sdp{{0%{{opacity:.9;transform:scale(1)}}100%{{opacity:0;transform:scale(2.8)}}}}
.sn{{animation:shn 10s ease-in-out {2 + idx*1.3:.1f}s infinite}}
@keyframes shn{{0%{{transform:translateX(0)}}20%{{transform:translateX({W + 320}px)}}100%{{transform:translateX({W + 320}px)}}}}
.ar{{animation:arw 1.8s ease-in-out infinite}}
@keyframes arw{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(2px,-2px)}}}}
.orb{{animation:spn 40s linear infinite}}
@keyframes spn{{to{{transform:rotate(360deg)}}}}
.fl{{animation:flt 5s ease-in-out infinite alternate}}
@keyframes flt{{from{{transform:translateY(-3px) scale(1)}}to{{transform:translateY(3px) scale(1.04)}}}}
@media (prefers-reduced-motion:reduce){{
.cd,.ul,.cu,.cv,.ds,.fd,.ch,.sn,.sd,.orb,.fl,.ar{{animation:none!important}}
.cv,.cu,.sn,.sd{{display:none}}
}}
"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">{escape(spec["name"])}: {escape(spec["desc"])}</title>
<defs>
<clipPath id="cc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10"/></clipPath>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["shine"]}" stop-opacity="0"/><stop offset=".5" stop-color="{c["shine"]}" stop-opacity="{c["shine_o"]}"/><stop offset="1" stop-color="{c["shine"]}" stop-opacity="0"/></linearGradient>
</defs>
<style>{css}</style>
<g class="cd">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1.2"/>
<g clip-path="url(#cc)">
{bar}
{deco}
{name}{tag}{desc}{chips}{repo}
<g class="sn"><rect x="-200" y="-10" width="120" height="{H+20}" fill="url(#sh)" transform="skewX(-18)"/></g>
</g>
</g>
</svg>
'''

for i, spec in enumerate(CARDS):
    for t in TH:
        open(f"{OUT}/{spec['id']}-{t}.svg", "w", encoding="utf-8").write(card(spec, t, i))
print("ok")
