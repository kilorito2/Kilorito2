import math, os
import os
_QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR", os.path.join(_QUI, "salida"))
os.makedirs(OUT, exist_ok=True)
SANS = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"
TH = {
 "dark": dict(ink="#ece7db", mute="#8a95a0", amber="#f0a93a", line="#2a3641", hi="#ffe2a8"),
 "light": dict(ink="#1b2227", mute="#5b6872", amber="#b9690b", line="#cdd8d3", hi="#8a4c04"),
}
AXES = [("Frontend",4.5),("UI y animación",4.0),("Apps de escritorio",3.5),("Backend y APIs",3.0),("Arquitectura",3.5),("Herramientas",3.5)]
cx, cy, R = 280, 200, 120
n = len(AXES)
T = 6.0          # periodo del barrido
D = 2.7          # arranque del barrido (despues del intro)

def pt(i, r):
    a = -math.pi/2 + i*2*math.pi/n
    return cx + r*math.cos(a), cy + r*math.sin(a)
def pu(u, r):   # u grados desde arriba, horario
    a = math.radians(u)
    return cx + r*math.sin(a), cy - r*math.cos(a)

def radar(t):
    c = TH[t]
    css = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.rg{{transform-origin:{cx}px {cy}px;animation:ringin .7s cubic-bezier(.2,.8,.2,1) backwards}}
@keyframes ringin{{from{{opacity:0;transform:scale(.1)}}to{{opacity:1;transform:scale(1)}}}}
.sp{{stroke-dasharray:1;animation:spoke .8s ease-out backwards}}
@keyframes spoke{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.grow{{transform-origin:{cx}px {cy}px;animation:grow 1.3s cubic-bezier(.34,1.45,.5,1) 1.1s backwards}}
@keyframes grow{{from{{transform:scale(.04);opacity:0}}20%{{opacity:1}}to{{transform:scale(1);opacity:1}}}}
.br{{transform-origin:{cx}px {cy}px;animation:breathe 5s ease-in-out 2.6s infinite alternate}}
@keyframes breathe{{from{{transform:scale(1)}}to{{transform:scale(1.035)}}}}
.fl{{animation:flp 5s ease-in-out 2.6s infinite alternate}}
@keyframes flp{{from{{fill-opacity:.18}}to{{fill-opacity:.32}}}}
.tr{{stroke-dasharray:.14 .86;opacity:0;animation:trace 4.2s linear {D}s infinite}}
@keyframes trace{{0%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:-1;opacity:1}}}}
.pop{{animation:dpop .55s cubic-bezier(.3,1.8,.5,1) backwards}}
@keyframes dpop{{from{{opacity:0;transform:scale(.1)}}to{{opacity:1;transform:scale(1)}}}}
.dp{{animation:dhit {T}s linear infinite}}
@keyframes dhit{{0%{{transform:scale(1.9)}}9%{{transform:scale(1)}}100%{{transform:scale(1)}}}}
.pg{{opacity:0;animation:ping {T}s ease-out infinite}}
@keyframes ping{{0%{{opacity:.95;transform:scale(1)}}14%{{opacity:0;transform:scale(4.2)}}100%{{opacity:0;transform:scale(4.2)}}}}
.lb{{animation:lbin .6s ease-out backwards,lit {T}s linear infinite}}
@keyframes lbin{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes lit{{0%{{fill:{c['amber']}}}6%{{fill:{c['amber']}}}34%{{fill:{c['ink']}}}100%{{fill:{c['ink']}}}}}
.sf{{opacity:0;animation:sfade .8s ease-out {D}s forwards}}
@keyframes sfade{{to{{opacity:1}}}}
.sw{{transform-origin:{cx}px {cy}px;animation:sweep {T}s linear {D}s infinite}}
@keyframes sweep{{to{{transform:rotate(360deg)}}}}
.ix{{opacity:.28;animation:ixl {T}s linear infinite}}
@keyframes ixl{{0%{{opacity:1}}30%{{opacity:.28}}100%{{opacity:.28}}}}
.cp{{transform-origin:{cx}px {cy}px;animation:cpulse 2.4s ease-out infinite}}
@keyframes cpulse{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(4)}}}}
.ft{{animation:lbin .8s ease-out 2.3s backwards}}
@media (prefers-reduced-motion:reduce){{
.rg,.sp,.grow,.br,.fl,.pop,.dp,.lb,.lt,.ft,.ix{{animation:none!important}}
.sf,.sw,.tr,.pg,.cp{{display:none}}
}}
"""
    rings = ""
    for lvl in range(1, 6):
        pts = " ".join(f"{pt(i, R*lvl/5)[0]:.1f},{pt(i, R*lvl/5)[1]:.1f}" for i in range(n))
        rings += f'<polygon class="rg" points="{pts}" fill="none" stroke="{c["line"]}" stroke-width="1" style="animation-delay:{0.1+lvl*0.12:.2f}s"/>'
    spokes = "".join(
        f'<line class="sp" pathLength="1" x1="{cx}" y1="{cy}" x2="{pt(i,R)[0]:.1f}" y2="{pt(i,R)[1]:.1f}" stroke="{c["line"]}" stroke-width="1" style="animation-delay:{0.35+i*0.08:.2f}s"/>'
        for i in range(n))
    # puntos de interseccion que se encienden cuando pasa el barrido
    ix = ""
    for i in range(n):
        for lvl in range(1, 6):
            x, y = pt(i, R*lvl/5)
            ix += f'<circle class="ix" cx="{x:.1f}" cy="{y:.1f}" r="1.6" fill="{c["amber"]}" style="animation-delay:{D+i*T/n:.2f}s"/>'
    dpts = [pt(i, R*v/5) for i, (_, v) in enumerate(AXES)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in dpts)
    pathd = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in dpts) + " Z"
    dots = ""
    for i, (x, y) in enumerate(dpts):
        d = D + i*T/n
        dly = 2.0 + i*0.1
        dots += (f'<g class="pop" style="transform-origin:{x:.1f}px {y:.1f}px;animation-delay:{dly:.2f}s">'
                 f'<circle class="dp" cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{c["amber"]}" style="transform-origin:{x:.1f}px {y:.1f}px;animation-delay:{d:.2f}s"/></g>')
    pings = "".join(
        f'<circle class="pg" cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="none" stroke="{c["amber"]}" stroke-width="1.6" style="transform-origin:{x:.1f}px {y:.1f}px;animation-delay:{D+i*T/n:.2f}s"/>'
        for i, (x, y) in enumerate(dpts))
    # barrido
    N, dd = 16, 2.6
    wedge = ""
    for k in range(N):
        x0, y0 = pu(-(k+1)*dd, R); x1, y1 = pu(-k*dd, R)
        a = 0.26*(1-k/N)**1.7
        wedge += f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{c["amber"]}" fill-opacity="{a:.3f}"/>'
    tx, ty = pu(0, R)
    sweep = (f'<g class="sf" clip-path="url(#hx)"><g class="sw">{wedge}'
             f'<line x1="{cx}" y1="{cy}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{c["amber"]}" stroke-width="1.6" stroke-linecap="round" stroke-opacity=".9"/></g></g>')
    hexpts = " ".join(f"{pt(i,R)[0]:.1f},{pt(i,R)[1]:.1f}" for i in range(n))
    labels = ""
    for i, (name, _) in enumerate(AXES):
        x, y = pt(i, R+20)
        cosv = math.cos(-math.pi/2 + i*2*math.pi/n)
        sinv = math.sin(-math.pi/2 + i*2*math.pi/n)
        anchor = "middle" if abs(cosv) < .2 else ("start" if cosv > 0 else "end")
        dy = 4 if abs(sinv) < .9 else (-2 if y < cy else 14)
        labels += (f'<text class="lb sans" x="{x:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}" font-size="14" fill="{c["ink"]}" '
                   f'style="animation-delay:{0.9+i*0.1:.2f}s,{D+i*T/n:.2f}s">{name}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 400" width="560" height="400" role="img" aria-labelledby="t">
<title id="t">Radar de áreas de trabajo: frontend, UI y animación, apps de escritorio, backend y APIs, arquitectura y herramientas.</title>
<defs><clipPath id="hx"><polygon points="{hexpts}"/></clipPath><filter id="gl" filterUnits="userSpaceOnUse" x="0" y="0" width="560" height="400"><feGaussianBlur stdDeviation="3.5"/></filter></defs>
<style>{css}</style>
{rings}{spokes}{ix}
<circle class="cp" cx="{cx}" cy="{cy}" r="3" fill="none" stroke="{c['amber']}" stroke-width="1.5"/>
{sweep}
<g class="grow"><g class="br"><polygon class="fl" points="{poly}" fill="{c["amber"]}" fill-opacity=".22" stroke="{c["amber"]}" stroke-width="2.5" stroke-linejoin="round"/>
<path class="tr" pathLength="1" d="{pathd}" fill="none" stroke="{c['amber']}" stroke-width="6" stroke-linecap="round" filter="url(#gl)"/>
<path class="tr" pathLength="1" d="{pathd}" fill="none" stroke="{c['hi']}" stroke-width="2.5" stroke-linecap="round"/>
{dots}</g></g>
{pings}
{labels}
<text class="ft mono" x="280" y="392" text-anchor="middle" font-size="12" fill="{c["mute"]}">areas: 6 · escala 1 a 5</text>
</svg>
'''
os.makedirs(OUT, exist_ok=True)
for t in TH:
    open(f"{OUT}/radar-{t}.svg", "w", encoding="utf-8").write(radar(t))
print("ok")
