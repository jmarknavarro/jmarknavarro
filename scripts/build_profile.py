#!/usr/bin/env python3
"""Build the profile card shown in README.md.

Writes assets/profile-dark.svg and assets/profile-light.svg. README.md picks
the right one for the viewer's GitHub theme via <picture>.

    python3 scripts/build_profile.py

Edit the CONTENT section below, re-run, and commit the two SVGs. No
dependencies beyond Python 3.
"""
import os
import sys

# ---------------------------------------------------------------- CONTENT ---

NAME = "John Mark Navarro"
TITLE = "Software and embedded systems engineer."
PILL = "BUILDING N2S-S1"                      # status pill above the name
INFO = ["MANILA, PH", "EMBEDDED · MOBILE · WEB", "@JMARKNAVARRO"]
CHIP = ("N2S", "IN PROGRESS")                  # text on the chip graphic

# (category, name, description, url or None). Rows with the same category
# next to each other share one label. URLs are display text only; the
# clickable links live in README.md under the card.
PROJECTS = [
    ("HARDWARE", "N2S-S1", "2-step rev limiter controller", None),
    ("HARDWARE", "N2S-AMS", "Piggyback air suspension management", None),
    ("DESKTOP", "K8 Desk", "Mac app for coding with Claude", "k8desk.vercel.app"),
    ("ANDROID", "CineK8", "Movies, shows and anime on Android and TV", "cinek8.vercel.app"),
    ("WEB", "QRPinas", "QR Ph payment cards for GCash and Maya", "qrpinas.vercel.app"),
    ("WEB", "CineCaptions", "Cinematic subtitles for images", "cinecaptions.com"),
]

# (row label, [(name, dot colour)]). Keep each row under ~880px of pills:
# a pill is roughly 54 + 9.2 * len(name) px wide, plus a 10px gap.
STACK = [
    ("LANGUAGES", [("TypeScript", "#3b82f6"), ("JavaScript", "#f1e05a"), ("Dart", "#00B4AB"),
                   ("Kotlin", "#A97BFF"), ("C++", "#f34b7d"), ("Python", "#4b8bbe"), ("Java", "#b07219")]),
    ("FRAMEWORKS", [("React", "#61dafb"), ("Flutter", "#47c5fb"), ("Vue", "#41b883"), ("Electron", "#9feaf9"),
                    ("Vite", "#a855f7"), ("Tailwind CSS", "#38bdf8"), ("Express", "#a1a1aa")]),
    ("PLATFORMS", [("ESP32", "#e7352c"), ("Arduino", "#00979D"), ("Android", "#3ddc84"),
                   ("Cloudflare Workers", "#f38020"), ("Vercel", "#fafafa")]),
]

# ----------------------------------------------------------------- THEMES ---

THEMES = {
    "dark": dict(bg="#09090b", border="#27272a", text="#fafafa", muted="#a1a1aa", faint="#52525b",
                 grid="#3f3f46", surface="#111113", label="#8b8b94", trace="#2e2e33", accent="#60a5fa",
                 glow="#3b82f6", glowop="0.28", green="#4ade80"),
    "light": dict(bg="#ffffff", border="#e4e4e7", text="#09090b", muted="#52525b", faint="#a1a1aa",
                  grid="#d4d4d8", surface="#fafafa", label="#71717a", trace="#dcdce0", accent="#2563eb",
                  glow="#3b82f6", glowop="0.14", green="#16a34a",
                  # dot colours that wash out on white get a darker shade
                  dots={"JavaScript": "#d4a106", "React": "#0ea5c6", "Electron": "#2b8a9e",
                        "Tailwind CSS": "#0ea5e9", "Express": "#52525b", "Vercel": "#09090b",
                        "Android": "#22a35a", "Flutter": "#0284c7", "Kotlin": "#7c4dff"}),
}

# ----------------------------------------------------------------- LAYOUT ---

SANS = "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
W = 1200
HERO_H = 420
PROJ_PAD, PROJ_ROW = 18, 68
STACK_TOP, STACK_GAP = 44, 58

STYLE = """<style>
.flow{stroke-dasharray:28 420;animation:flow 4.5s linear infinite}
.f2{animation-delay:-1.5s}.f3{animation-delay:-3s}
.pulse{animation:pulse 2s ease-in-out infinite}
@keyframes flow{from{stroke-dashoffset:448}to{stroke-dashoffset:0}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.flow,.pulse{animation:none}.flow{stroke-dasharray:none;opacity:.0}}
</style>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def hero(c, card_h):
    """Hero section: name, title, info line and the animated chip."""
    traces = ["M1011,98 V40 H1060 V0", "M1059,98 V70 H1140 V30", "M987,98 V58 H930 V36",
              "M1122,161 H1160 V120 H1200", "M1122,209 H1150 V250 H1200",
              "M1035,272 V320 H990 V372", "M1083,272 V340 H1130 V420",
              "M948,185 H900 V150", "M948,233 H915 V300 H862"]
    ends = [(1140, 30), (930, 36), (990, 372), (900, 150), (862, 300)]
    pins = []
    for i in range(5):
        p = 987 + i * 24
        q = 137 + i * 24
        pins += [f"M{p},110 V98", f"M{p},260 V272", f"M960,{q} H948", f"M1110,{q} H1122"]
    flow = [(traces[0], ""), (traces[4], "f2"), (traces[5], "f3"), (traces[7], "f2")]
    sep = f'  <tspan fill="{c["border"]}">/</tspan>  '
    pill_w = round(34 + len(PILL) * 8.7 + 18)
    return f'''
{STYLE}
<defs>
 <clipPath id="card"><rect x="0.5" y="0.5" width="{W-1}" height="{card_h-1}" rx="20"/></clipPath>
 <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{c['grid']}"/></pattern>
 <radialGradient id="fade" cx="0.82" cy="0.4" r="0.75"><stop offset="0" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
 <mask id="m"><rect width="{W}" height="{HERO_H}" fill="url(#fade)"/></mask>
 <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{c['glow']}" stop-opacity="{c['glowop']}"/><stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/></radialGradient>
</defs>
<g clip-path="url(#card)">
 <rect width="{W}" height="{HERO_H}" fill="{c['bg']}"/>
 <rect width="{W}" height="{HERO_H}" fill="url(#dots)" mask="url(#m)"/>
 <ellipse cx="1035" cy="185" rx="300" ry="230" fill="url(#glow)"/>
 <g fill="none" stroke="{c['trace']}" stroke-width="1.5" stroke-linejoin="round">{''.join(f'<path d="{d}"/>' for d in traces)}</g>
 <g fill="none" stroke="{c['accent']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{''.join(f'<path class="flow {k}" d="{d}"/>' for d, k in flow)}</g>
 <g fill="{c['bg']}" stroke="{c['faint']}" stroke-width="1.5">{''.join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x, y in ends)}</g>
 <g stroke="{c['faint']}" stroke-width="2.5" stroke-linecap="round">{''.join(f'<path d="{d}"/>' for d in pins)}</g>
 <rect x="960" y="110" width="150" height="150" rx="16" fill="{c['surface']}" stroke="{c['faint']}" stroke-width="1.5"/>
 <rect x="984" y="134" width="102" height="102" rx="8" fill="none" stroke="{c['border']}" stroke-width="1.5"/>
 <circle cx="972" cy="122" r="3" fill="{c['faint']}"/>
 <text x="1035" y="190" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="600" fill="{c['text']}">{esc(CHIP[0])}</text>
 <text x="1035" y="212" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{c['muted']}">{esc(CHIP[1])}</text>

 <rect x="64.5" y="71.5" width="{pill_w}" height="31" rx="15.5" fill="{c['surface']}" stroke="{c['border']}"/>
 <circle class="pulse" cx="84" cy="87" r="4" fill="{c['green']}"/>
 <text x="98" y="91.5" font-family="{MONO}" font-size="12.5" letter-spacing="1.2" fill="{c['muted']}">{esc(PILL)}</text>

 <text x="62" y="211" font-family="{SANS}" font-size="66" font-weight="650" letter-spacing="-1.5" fill="{c['text']}">{esc(NAME)}</text>
 <text x="64" y="261" font-family="{SANS}" font-size="24" letter-spacing="-0.3" fill="{c['muted']}">{esc(TITLE)}</text>

 <line x1="64" y1="315" x2="640" y2="315" stroke="{c['border']}"/>
 <text x="64" y="351" font-family="{MONO}" font-size="13" letter-spacing="1.6" fill="{c['label']}">{sep.join(esc(s) for s in INFO)}</text>
</g>
'''


def projects(c, top):
    """Projects section, grouped by category."""
    out, prev = [], None
    for i, (label, name, desc, url) in enumerate(PROJECTS):
        cy = top + PROJ_PAD + PROJ_ROW * i + PROJ_ROW / 2
        y = top + PROJ_PAD + PROJ_ROW * i
        if label != prev:
            out.append(f'<text x="64" y="{cy+4}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{c["label"]}">{esc(label)}</text>')
        if i:  # hairline between rows: full width between groups, content-only within a group
            x1 = 64 if label != prev else 232
            out.append(f'<line x1="{x1}" y1="{y}" x2="1136" y2="{y}" stroke="{c["border"]}" stroke-opacity="0.7"/>')
        prev = label
        out.append(f'<text x="232" y="{cy+7}" font-family="{SANS}" font-size="20" font-weight="600" letter-spacing="-0.2" fill="{c["text"]}">{esc(name)}</text>'
                   f'<text x="420" y="{cy+7}" font-family="{SANS}" font-size="19" letter-spacing="-0.2" fill="{c["muted"]}">{esc(desc)}</text>')
        if url:
            out.append(f'<text x="1136" y="{cy+5}" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="0.4" fill="{c["muted"]}">{esc(url)}'
                       f'<tspan dx="8" fill="{c["accent"]}">↗</tspan></text>')
    height = PROJ_PAD * 2 + PROJ_ROW * len(PROJECTS)
    divider = f'<line x1="200" y1="{top+PROJ_PAD+10}" x2="200" y2="{top+height-PROJ_PAD-10}" stroke="{c["border"]}"/>'
    return divider + "".join(out), height


def stack(c):
    """Stack section (drawn at y=0; the caller shifts it into place)."""
    height = STACK_TOP * 2 + 36 + STACK_GAP * (len(STACK) - 1)
    body = []
    for r, (label, items) in enumerate(STACK):
        y = STACK_TOP + r * STACK_GAP
        body.append(f'<text x="64" y="{y+23}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{c["label"]}">{esc(label)}</text>')
        x = 232
        for name, col in items:
            w = 36 + len(name) * 9.2 + 18
            body.append(f'<rect x="{x+.5}" y="{y+.5}" width="{w:.0f}" height="35" rx="17.5" fill="{c["surface"]}" stroke="{c["border"]}"/>'
                        f'<circle cx="{x+20}" cy="{y+18}" r="4.5" fill="{c.get("dots", {}).get(name, col)}"/>'
                        f'<text x="{x+34}" y="{y+23.5}" font-family="{MONO}" font-size="15" fill="{c["text"]}">{esc(name)}</text>')
            x += w + 10
    return f'\n\n<line x1="200" y1="28" x2="200" y2="{height-28}" stroke="{c["border"]}"/>\n{"".join(body)}\n', height


def card(c):
    proj, proj_h = projects(c, HERO_H)
    stk, stack_h = stack(c)
    H = HERO_H + proj_h + stack_h
    stack_y = HERO_H + proj_h
    stack_names = ", ".join(n for _, items in STACK for n, _ in items)
    aria = (f"{NAME}, {TITLE.rstrip('.').lower()}. Projects: "
            + "; ".join(f"{n}, {d}" + (f" ({u})" if u else "") for _, n, d, u in PROJECTS)
            + f". Stack: {stack_names}.")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(aria)}">
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="{c['bg']}"/>
{hero(c, H)}
<line x1="0" y1="{HERO_H}" x2="{W}" y2="{HERO_H}" stroke="{c['border']}"/>
{proj}
<line x1="0" y1="{stack_y}" x2="{W}" y2="{stack_y}" stroke="{c['border']}"/>
<g transform="translate(0,{stack_y})">{stk}</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{c['border']}"/>
</svg>'''


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(out, exist_ok=True)
    for mode, colours in THEMES.items():
        path = os.path.join(out, f"profile-{mode}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(card(colours))
        print(f"wrote {os.path.relpath(path)}")


if __name__ == "__main__":
    main()
