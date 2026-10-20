"""Hero card for the pavwlik GitHub profile README, in a light and a dark variant.

Run from this folder: python build_card.py  (writes ../assets/hero-light.svg and hero-dark.svg)
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
    "light": dict(bg="#FFFFFF", ink="#18202E", muted="#5A6474", rule="#E2E5EA", done="#16935A", accent="#3346D3"),
    "dark": dict(bg="#0E1525", ink="#E9EDF4", muted="#8E99AD", rule="#26304A", done="#3CCB8B", accent="#8C99FF"),
}

LEFT = {
    "name": "Pavel Bureš",
    "role1": "Automatizace, interní nástroje",
    "role2": "a vývoj",
    "job": "IT specialista v ROI digital",
    "founder": "Zakladatel Edulity a Hearflow",
    "where": "Nové Strašecí",
    "open": "Otevřený novým příležitostem",
}
RIGHT_HEAD = "Pomáhám lidem s AI."
RIGHT_BODY = [
    "Učím, jak s ní pracovat a psát prompty,",
    "a automatizuju práci, kterou by jinak",
    "dělali ručně. Ať jim zbyde čas",
    "na důležitější věci.",
]
PROJECTS = [
    ("Edulity", "maturita přes hry, 4 500+ studentů"),
    ("Hearflow", "z nahrávky přednášky skripta"),
]


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
    alltext = "".join(LEFT.values()) + RIGHT_HEAD + "".join(RIGHT_BODY) + "".join(a + b for a, b in PROJECTS)

    left = f'''
<text x="56" y="128" class="name">{LEFT["name"]}</text>
<text x="58" y="172" class="role">{LEFT["role1"]}</text>
<text x="58" y="202" class="role">{LEFT["role2"]}</text>
<text x="58" y="262" class="meta">{LEFT["job"]}</text>
<text x="58" y="290" class="meta">{LEFT["founder"]}</text>
<line x1="58" y1="336" x2="440" y2="336" stroke="{t["rule"]}" stroke-width="1"/>
<text x="58" y="374" class="small">{LEFT["where"]}</text>
<circle cx="196" cy="368" r="4.5" fill="{t["done"]}"/>
<text x="210" y="374" class="small">{LEFT["open"]}</text>'''

    x = 560
    right = f'<text x="{x}" y="128" class="lead">{esc(RIGHT_HEAD)}</text>'
    for i, line in enumerate(RIGHT_BODY):
        right += f'<text x="{x}" y="{172 + i * 28}" class="body">{esc(line)}</text>'
    for i, (name, what) in enumerate(PROJECTS):
        y = 318 + i * 56
        right += f'<text x="{x}" y="{y}" class="proj">{name}</text>'
        right += f'<text x="{x}" y="{y + 24}" class="small">{esc(what)}</text>'

    css = f'''{font_face(alltext)}
text{{font-family:'{FAMILY}',system-ui,sans-serif;fill:{t["ink"]}}}
.name{{font-size:64px;font-weight:760;letter-spacing:-2px}}
.role{{font-size:25px;font-weight:450;fill:{t["muted"]}}}
.meta{{font-size:18px;font-weight:560}}
.small{{font-size:15px;fill:{t["muted"]}}}
.lead{{font-size:28px;font-weight:700;letter-spacing:-.6px}}
.body{{font-size:18px;fill:{t["muted"]}}}
.proj{{font-size:18px;font-weight:650;fill:{t["accent"]}}}'''

    label = ("Pavel Bureš. Automatizace, interní nástroje a vývoj. IT specialista v ROI digital, zakladatel Edulity a Hearflow. "
             f"{RIGHT_HEAD} " + " ".join(RIGHT_BODY))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<style>{css}</style>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="20" fill="{t["bg"]}" stroke="{t["rule"]}" stroke-width="1.5"/>
<line x1="508" y1="56" x2="508" y2="{h - 56}" stroke="{t["rule"]}" stroke-width="1"/>
{left}{right}
</svg>'''


if __name__ == "__main__":
    for name, t in THEMES.items():
        p = os.path.join(OUT, f"hero-{name}.svg")
        open(p, "w", encoding="utf-8").write(hero(t))
        print(os.path.abspath(p), os.path.getsize(p))
