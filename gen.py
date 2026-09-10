"""Mission-control style SVG panels for the GitHub profile README."""
import html, math, pathlib, random, textwrap
OUT = pathlib.Path(__file__).parent / "assets"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
BG, PANEL, BORDER, TEXT, MUTED, DIM = "#0a0a0a", "#0e0e0e", "#262626", "#e5e5e5", "#8a8a8a", "#3a3a3a"
GREEN, BLUE, ORANGE, PURPLE, RED = "#22c55e", "#3b82f6", "#f97316", "#a855f7", "#ef4444"
E = lambda s: html.escape(s, quote=True)
WIDE, NARROW, GAP = 800, 392, 16   # 800 + 16 + 392 = 1208 ~ full row; 392*3 + 32 = 1208

def t(x, y, s, size=12, fill=TEXT, weight="normal", anchor="start", family=MONO, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{E(s)}</text>'

def panel(name, w, h, label, body, kind="//"):
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}">',
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>',
           t(20, 26, f"{kind} {label}", 12, TEXT, "bold")]
    svg += body
    svg.append("</svg>")
    (OUT / f"{name}.svg").write_text("\n".join(svg))

def chip(x, y, s, fg=TEXT, stroke=BORDER, right=False):
    w = int(len(s) * 7.3 + 20)
    if right: x = x - w
    return f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="4" fill="{BG}" stroke="{stroke}"/>' + t(x + w/2, y + 15, s, 11, fg, "bold", "middle"), w

def glow(cx, cy, r, color, op=0.18, gid="g"):
    return (f'<defs><radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<rect x="1" y="1" width="100%" height="100%" rx="10" fill="url(#{gid})"/>')

def area(x0, y0, w, h, color, seed, gid):
    rnd = random.Random(seed); n = 28
    pts = [(x0 + i * w / (n - 1), y0 + h - rnd.uniform(0.25, 0.95) * h) for i in range(n)]
    # smooth-ish by averaging neighbours
    pts = [(x, (pts[max(i-1,0)][1] + y + pts[min(i+1,n-1)][1]) / 3) for i, (x, y) in enumerate(pts)]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    fillp = path + f" L{x0+w},{y0+h} L{x0},{y0+h} Z"
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity="0.35"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="{fillp}" fill="url(#{gid})"/><path d="{path}" fill="none" stroke="{color}" stroke-opacity="0.8" stroke-width="1.5"/>')

# ---------------------------------------------------------------- header
def header():
    w, h = 1208, 48
    body = [t(8, 31, "◈ krishiv_seth", 17, TEXT, "bold")]
    x = w - 8
    for s in ["STATUS: BUILDING", "SCHOOL: NYU '27", "LOC: NYC"]:
        c, cw = chip(x, 13, s, right=True); body.append(c); x -= cw + 10
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="krishiv_seth">'] + body + ["</svg>"]
    (OUT / "header.svg").write_text("\n".join(svg))

# ---------------------------------------------------------------- row 1
def about():
    w, h = WIDE, 250
    body = [glow(400, 250, 420, GREEN, 0.10, "ga"), area(20, 120, w - 40, 110, GREEN, 3, "aa")]
    lines = [
        "CS + Data Science at NYU Courant (Class of 2027), Cybersecurity minor.",
        "I build agentic systems, distributed inference, and security tooling.",
        "Most recently: security engineering at Clear Street,",
        "forward deployed engineering at Forkast (Antler '25).",
    ]
    for i, ln in enumerate(lines):
        body.append(t(20, 58 + i * 21, ln, 14, TEXT if i < 2 else MUTED))
    body.append(t(w - 20, 26, "5x hackathon winner", 11, GREEN, "bold", "end"))
    body.append(t(20, h - 14, "agents", 11, MUTED)); body.append(t(w/2, h - 14, "inference", 11, MUTED, anchor="middle")); body.append(t(w - 20, h - 14, "security", 11, MUTED, anchor="end"))
    panel("about", w, h, "about", body)

def focus():
    w, h = NARROW, 250
    body = [glow(196, 125, 150, BLUE, 0.22, "gf")]
    for (cx, cy) in [(120, 88), (272, 88), (100, 178)]:
        body.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#000" stroke="{DIM}"/>')
    body.append(t(w/2, 128, "agents", 30, TEXT, "bold", "middle"))
    body.append(t(w/2, 152, "CURRENT FOCUS", 11, MUTED, anchor="middle", extra='letter-spacing="2"'))
    body.append(t(w/2, 172, "+ inference  + security", 11, DIM, anchor="middle"))
    body.append(t(20, h - 14, "OSIRIS Lab", 11, MUTED)); body.append(t(w - 20, h - 14, "since 2026", 11, MUTED, anchor="end"))
    panel("focus", w, h, "focus", body, "##")

def stack():
    w, h = NARROW, 250
    body = [glow(196, 120, 140, PURPLE, 0.14, "gs")]
    body.append(t(w/2, 118, "8", 34, TEXT, "bold", "middle")); body.append(t(w/2, 140, "LANGUAGES", 11, MUTED, anchor="middle", extra='letter-spacing="2"'))
    cols = [("Python", "Go", "TS"), ("Java", "Scala", "Rust"), ("C", "SQL", "Bash")]
    for i, col in enumerate(cols):
        x = 66 + i * 130
        for j, s in enumerate(col):
            body.append(t(x, 182 + j * 16, s, 11, TEXT if j == 0 else MUTED, anchor="middle"))
    panel("stack", w, h, "languages", body)

# ---------------------------------------------------------------- row 2: experience + projects wide
def experience():
    w, h = NARROW, 300
    rows = [("2026", "Clear Street", "security eng", GREEN), ("2026", "Forkast", "forward deployed", BLUE), ("2025", "Exar North", "ai software eng", PURPLE),
            ("2025", "GoTrust", "ai eng", ORANGE), ("2025", "Kanlet", "software eng", MUTED), ("2024", "Ambee", "data science", MUTED), ("2023", "UPL", "cybersecurity", MUTED)]
    body = [f'<line x1="66" y1="46" x2="66" y2="{h-30}" stroke="{DIM}" stroke-width="1"/>']
    for i, (yr, co, role, c) in enumerate(rows):
        y = 60 + i * 33
        body.append(t(54, y + 4, yr, 11, MUTED, anchor="end"))
        body.append(f'<circle cx="66" cy="{y}" r="4" fill="{PANEL}" stroke="{c}" stroke-width="1.5"/>')
        body.append(t(82, y + 4, co, 13, TEXT, "bold")); body.append(t(w - 20, y + 4, role, 12, MUTED, anchor="end"))
    panel("experience", w, h, "experience", body)

def projects():
    w, h = WIDE, 300
    body = [glow(400, 150, 380, BLUE, 0.08, "gp")]
    stages = [("Orchard", "distributed inference", GREEN), ("Ouroboros", "MCP runtime security", RED), ("Trevor AI", "voice trading agent", PURPLE),
              ("Watchman", "camera fleet Q&A", ORANGE), ("What The Rent?!", "hidden rent costs", BLUE), ("Series Events", "chemistry events", "#ec4899")]
    cw, ch, gap = 120, 64, 8; x0 = 20; y0 = 118
    for i, (name, sub, c) in enumerate(stages):
        x = x0 + i * (cw + gap)
        body.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="6" fill="{BG}" stroke="{c}" stroke-opacity="0.8"/>')
        body.append(t(x + cw/2, y0 + 27, name, 11, c, "bold", "middle"))
        body.append(t(x + cw/2, y0 + 45, sub, 9, MUTED, anchor="middle"))
    # progress bar
    seg = (w - 40) / len(stages)
    for i, (_, _, c) in enumerate(stages):
        body.append(f'<rect x="{20 + i*seg}" y="{y0 + ch + 30}" width="{seg - 4}" height="4" rx="2" fill="{c}" fill-opacity="0.9"/>')
    for x, k, v in [(20, "stack", "pytorch · fastapi · react · electron"), (w/2 - 60, "infra", "aws · terraform · docker · k8s"), (w - 230, "data", "postgres · redis · pgvector")]:
        body.append(t(x, 250, k, 10, DIM)); body.append(t(x + 44, 250, v, 10, MUTED))
    body.append(t(20, h - 16, "6 shipped", 11, TEXT)); body.append(t(w/2, h - 16, "all open source", 11, MUTED, anchor="middle")); body.append(t(w - 20, h - 16, "details below ↓", 11, MUTED, anchor="end"))
    body.append(t(w - 20, 26, "Orchard: top 10% of YC applicants", 11, GREEN, "bold", "end"))
    body.append(t(20, 60, "Everything I ship is on GitHub. Six projects, each solving a problem I actually had.", 12, MUTED))
    body.append(t(20, 80, "Agents, inference, security, and a couple of things that just needed to exist.", 12, DIM))
    panel("projects", w, h, "projects", body, "##")

# ---------------------------------------------------------------- project cards (3 per row)
def project_card(slug, name, desc, tags, color, visual=None):
    w, h = 596, 176
    body = [glow(120, 176, 260, color, 0.14, f"g{slug}")]
    body.append(f'<rect x="0" y="0" width="5" height="{h}" rx="2.5" fill="{color}"/>')
    body.append(t(24, 58, name, 24, TEXT, "bold"))
    for i, ln in enumerate(textwrap.wrap(desc, 62)[:2]):
        body.append(t(24, 90 + i * 22, ln, 15, MUTED))
    x = 24
    for tag in tags:
        c, cw = chip(x, h - 40, tag, TEXT); body.append(c); x += cw + 8
    body.append(t(w - 20, h - 25, "↗", 16, color, anchor="end"))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{E(name)}">',
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'] + body + ["</svg>"]
    (OUT / f"{slug}.svg").write_text("\n".join(svg))

def vis_nodes(color):
    cx, cy = NARROW - 70, 180; out = [f'<circle cx="{cx}" cy="{cy}" r="9" fill="#000" stroke="{color}"/>']
    for k in range(6):
        a = k * math.pi / 3; x, y = cx + 34 * math.cos(a), cy + 34 * math.sin(a)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{color}" stroke-opacity="0.5"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{BG}" stroke="{color}"/>')
    return out
def vis_bars(color):
    out = []; vals = [0.85, 0.4, 0.25, 0.15, 0.1]; cols = [color, BLUE, ORANGE, PURPLE, MUTED]
    for i, v in enumerate(vals):
        x = NARROW - 130 + i * 22
        out.append(f'<rect x="{x}" y="150" width="16" height="60" rx="3" fill="{BG}" stroke="{DIM}"/>')
        out.append(f'<rect x="{x+1}" y="{210 - 58*v:.0f}" width="14" height="{58*v:.0f}" rx="2" fill="{cols[i]}" fill-opacity="0.8"/>')
    return out
def vis_pipeline(color):
    out = []; steps = ["call", "plan", "search", "trade"]
    for i, s in enumerate(steps):
        x = NARROW - 208 + i * 48
        out.append(f'<rect x="{x}" y="166" width="40" height="26" rx="4" fill="{BG}" stroke="{color if i==3 else DIM}"/>')
        out.append(t(x + 20, 183, s, 9, color if i == 3 else MUTED, anchor="middle"))
        if i < 3: out.append(f'<path d="M{x+41},179 l5,0" stroke="{color}" stroke-opacity="0.7"/>')
    return out
def vis_heatmap(color):
    rnd = random.Random(11); out = []
    for r in range(4):
        for c in range(9):
            op = rnd.choice([0.08, 0.2, 0.45, 0.8])
            out.append(f'<rect x="{NARROW - 150 + c*14}" y="{152 + r*14}" width="11" height="11" rx="2" fill="{color}" fill-opacity="{op}"/>')
    return out
def vis_sparkline(color):
    return [area(NARROW - 160, 150, 140, 60, color, 5, "sp")]
def vis_dots(color):
    rnd = random.Random(4); out = []
    for _ in range(14):
        x, y, r = rnd.randint(NARROW-160, NARROW-24), rnd.randint(150, 210), rnd.choice([2, 3, 5])
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" fill-opacity="{rnd.choice([0.3,0.6,0.9])}"/>')
    return out

PROJECTS = [
    ("orchard", "Orchard", "Distributed LLM inference across the Apple devices you already own. Layer-split sharding with a KV cache.", ["python", "pytorch", "electron"], GREEN, vis_nodes),
    ("ouroboros", "Ouroboros", "Runtime security for AI agents and MCP servers. Catches tool poisoning and rug-pulls before they run.", ["python", "security", "mcp"], RED, vis_bars),
    ("trevor", "Trevor AI", "A phone-callable investment agent. Call it, and sub-agents research, analyse and trade while you talk.", ["typescript", "fastapi", "voice"], PURPLE, vis_pipeline),
    ("watchman", "Watchman", "Ask a fleet of security cameras questions in plain English and get the matching frames back.", ["typescript", "spacetimedb", "gemini"], ORANGE, vis_heatmap),
    ("rent", "What The Rent?!", "Chrome extensions for StreetEasy and Zillow that surface the hidden costs of a rental in NYC and SF.", ["python", "next.js", "extension"], BLUE, vis_sparkline),
    ("series", "Series Events", "Event planning with group chemistry prediction, run entirely over iMessage.", ["typescript", "imessage", "ai"], "#ec4899", vis_dots),
]

# ---------------------------------------------------------------- row: awards / research / links
def awards():
    w, h = NARROW, 220
    body = []
    c, cw = chip(w - 20, 14, "5 wins", GREEN, GREEN, right=True); body.append(c)
    items = [("GRAND PRIZE", "YC Startup School", GREEN), ("GRAND PRIZE", "Antler", GREEN), ("GRAND PRIZE", "Microsoft x Musa Capital", GREEN),
             ("GRAND PRIZE", "Khosla Ventures x ForgeHacks", GREEN), ("PEOPLE'S CHOICE", "Google x HackNYU", BLUE)]
    for i, (k, v, c) in enumerate(items):
        y = 62 + i * 24
        body.append(f'<rect x="20" y="{y-11}" width="4" height="14" rx="2" fill="{c}"/>')
        body.append(t(32, y, k, 9, c, "bold")); body.append(t(140, y, v, 12, TEXT))
    body.append(t(20, h - 14, "YC Startup School (flown out) · CodePath Cyber (Honors)", 10, MUTED))
    panel("awards", w, h, "awards", body)

def research():
    w, h = NARROW, 220
    body = [glow(196, 110, 160, PURPLE, 0.10, "gr")]
    items = [("NYU OSIRIS Lab", "byzantine fault tolerance; attack surfaces in agentic AI + blockchain"), ("Harvard Business School", "NLP + data infra for group behaviour on social media"), ("NYU Langone Health", "data infrastructure for neuroscience research")]
    for i, (k, v) in enumerate(items):
        y = 62 + i * 48
        body.append(t(20, y, k, 12, TEXT, "bold"))
        for j, ln in enumerate(textwrap.wrap(v, 46)[:2]):
            body.append(t(20, y + 16 + j * 14, ln, 11, MUTED))
    panel("research", w, h, "research", body, "##")

def links():
    w, h = 1208, 64
    body = [glow(604, 32, 500, GREEN, 0.08, "gl")]
    items = [("web", "krishivseth.com", GREEN, 20), ("linkedin", "in/krishiv-seth", BLUE, 250), ("github", "@krishivseth", TEXT, 500)]
    for k, v, c, x in items:
        body.append(t(x, 42, k, 11, MUTED)); body.append(t(x + 70, 42, v, 12, c, "bold"))
    body.append(t(660, 42, "off-screen: photo · gym · guitar", 11, MUTED))
    ch, cw = chip(w - 20, 21, "OPEN TO: agents · inference · security", ORANGE, ORANGE, right=True); body.append(ch)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="links">',
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'] + body + ["</svg>"]
    (OUT / "links.svg").write_text("\n".join(svg))


def hero():
    w, h = 1208, 230
    body = [glow(300, 230, 520, GREEN, 0.10, "gh"), area(20, 118, w - 40, 96, GREEN, 3, "ah")]
    body.append(t(20, 64, "Krishiv Seth", 30, TEXT, "bold"))
    body.append(t(20, 92, "agentic systems · distributed inference · security tooling", 14, MUTED))
    x = w - 20
    for sname in ["STATUS: BUILDING", "NYU '27", "NYC"]:
        c, cw = chip(x, 16, sname, right=True); body.append(c); x -= cw + 10
    body.append(t(20, h - 14, "CS + Data Science, Cybersecurity minor", 11, MUTED))
    body.append(t(w - 20, h - 14, "5x hackathon winner", 11, GREEN, "bold", "end"))
    panel("hero", w, h, "krishiv_seth", body)

hero()
for slug, name, desc, tags, color, vis in PROJECTS:
    project_card(slug, name, desc, tags, color, vis)
print("generated", len(list(OUT.glob("*.svg"))))
