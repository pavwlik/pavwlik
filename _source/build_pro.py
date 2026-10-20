"""Hero image for the pavwlik GitHub profile README, in a light and a dark variant.

The right column is a night-run timeline: the automations that finish before the team
starts work. It checks itself off once on load; reduced motion shows the finished state.
"""
import base64
import io
import os

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)
FAMILY = "Schibsted Grotesk"

THEMES = {
    "light": dict(bg="#FFFFFF", ink="#18202E", muted="#5A6474", rule="#E2E5EA", done="#16935A", accent="#3346D3", halo="#EEF0FD"),
    "dark": dict(bg="#0E1525", ink="#E9EDF4", muted="#8E99AD", rule="#26304A", done="#3CCB8B", accent="#7D8BFF", halo="#1B2444"),
}

LEFT = {
    "name": "Pavel Bureš",
    "role1": "Automation, internal tools",
    "role2": "and development",
    "job": "IT specialist at ROI digital",
    "founder": "Founder of Edulity and Hearflow",
    "where": "Nové Strašecí, Czechia",
    "open": "Open to new opportunities",
}
RUN_TITLE = "While the team sleeps"
RUN = [
    ("02:00", "Import yesterday's orders from the ERP"),
    ("02:04", "Sync stock levels across sales channels"),
    ("02:06", "Flag products with a falling margin"),
    ("02:07", "Draft purchase orders for low stock"),
]
RUN_END = ("07:30", "Summary waiting in the team chat")


def font_face(text):
    rules = []
    for fn, rng in (("sg-latin.woff2", "U+0000-00FF,U+2000-206F"), ("sg-latin-ext.woff2", "U+0100-02FF")):
        font = TTFont(os.path.join(HERE, "fonts", fn))
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:'{FAMILY}';font-weight:400 900;"
                     f"src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{rng}}}")
    return "".join(rules)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hero(t):
    w, h = 1000, 440
    alltext = "".join(LEFT.values()) + RUN_TITLE + "".join(a + b for a, b in RUN) + "".join(RUN_END)

    # timeline geometry
    tx, ty, gap = 560, 132, 54
    line_x = tx + 70
    rows = ""
    step = 0.45
    for i, (time, task) in enumerate(RUN):
        y = ty + i * gap
        d = f"{0.5 + i * step:.2f}s"
        rows += f'''
<text x="{tx}" y="{y + 5}" class="t">{time}</text>
<circle cx="{line_x}" cy="{y}" r="10" fill="{t["bg"]}" stroke="{t["rule"]}" stroke-width="1.5"/>
<g class="on" style="animation-delay:{d}">
  <circle cx="{line_x}" cy="{y}" r="10" fill="{t["done"]}"/>
  <path d="M{line_x - 4.5} {y}l3 3 6-6.5" fill="none" stroke="{t["bg"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<text x="{line_x + 26}" y="{y + 5}" class="task">{esc(task)}</text>'''
    ye = ty + len(RUN) * gap + 14
    end_delay = f"{0.5 + len(RUN) * step + 0.2:.2f}s"
    rows += f'''
<text x="{tx}" y="{ye + 5}" class="t">{RUN_END[0]}</text>
<circle cx="{line_x}" cy="{ye}" r="10" fill="{t["bg"]}" stroke="{t["rule"]}" stroke-width="1.5"/>
<g class="on" style="animation-delay:{end_delay}">
  <circle cx="{line_x}" cy="{ye}" r="16" fill="{t["halo"]}"/>
  <circle cx="{line_x}" cy="{ye}" r="6" fill="{t["accent"]}"/>
</g>
<text x="{line_x + 26}" y="{ye + 5}" class="task strong">{esc(RUN_END[1])}</text>'''
    track_len = ye - ty
    track = (f'<line x1="{line_x}" y1="{ty}" x2="{line_x}" y2="{ye}" stroke="{t["rule"]}" stroke-width="1.5"/>'
             f'<line class="fill" x1="{line_x}" y1="{ty}" x2="{line_x}" y2="{ye}" stroke="{t["done"]}" stroke-width="1.5" '
             f'stroke-dasharray="{track_len}" stroke-dashoffset="0"/>')
    fill_dur = 0.5 + len(RUN) * step + 0.2

    left = f'''
<text x="56" y="128" class="name">{LEFT["name"]}</text>
<text x="58" y="172" class="role">{LEFT["role1"]}</text>
<text x="58" y="202" class="role">{LEFT["role2"]}</text>
<text x="58" y="262" class="meta">{LEFT["job"]}</text>
<text x="58" y="290" class="meta">{LEFT["founder"]}</text>
<line x1="58" y1="336" x2="440" y2="336" stroke="{t["rule"]}" stroke-width="1"/>
<text x="58" y="374" class="small">{LEFT["where"]}</text>
<circle cx="268" cy="368" r="4.5" fill="{t["done"]}"/>
<text x="282" y="374" class="small">{LEFT["open"]}</text>'''

    css = f'''{font_face(alltext)}
text{{font-family:'{FAMILY}',system-ui,sans-serif;fill:{t["ink"]}}}
.name{{font-size:64px;font-weight:760;letter-spacing:-2px}}
.role{{font-size:25px;font-weight:450;fill:{t["muted"]}}}
.meta{{font-size:18px;font-weight:560}}
.small{{font-size:15px;fill:{t["muted"]}}}
.head{{font-size:15px;font-weight:640;fill:{t["muted"]}}}
.t{{font-size:15px;font-weight:500;fill:{t["muted"]};font-variant-numeric:tabular-nums}}
.task{{font-size:17px;font-weight:450}}
.strong{{font-weight:650}}
.on{{animation:on .3s ease-out both}}
@keyframes on{{from{{opacity:0}}to{{opacity:1}}}}
.fill{{animation:fill {fill_dur:.2f}s linear both .3s}}
@keyframes fill{{from{{stroke-dashoffset:{track_len}}}to{{stroke-dashoffset:0}}}}
@media (prefers-reduced-motion:reduce){{.on,.fill{{animation:none}}}}'''

    label = (f"Pavel Bureš. Automation, internal tools and development. IT specialist at ROI digital, founder of Edulity and Hearflow. "
             f"{RUN_TITLE}: " + "; ".join(f"{a} {b}" for a, b in RUN) + f"; {RUN_END[0]} {RUN_END[1]}.")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<style>{css}</style>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="20" fill="{t["bg"]}" stroke="{t["rule"]}" stroke-width="1.5"/>
<line x1="508" y1="56" x2="508" y2="{h - 56}" stroke="{t["rule"]}" stroke-width="1"/>
{left}
<text x="{tx}" y="84" class="head">{RUN_TITLE}</text>
{track}{rows}
</svg>'''


if __name__ == "__main__":
    for name, t in THEMES.items():
        p = os.path.join(OUT, f"hero-{name}.svg")
        open(p, "w", encoding="utf-8").write(hero(t))
        print(p, os.path.getsize(p))
