"""krishivOS-styled SVG panels for the GitHub profile README.

Everything is static SVG (GitHub strips scripts and external fonts). The look
matches krishivseth.com: near-black surfaces, hairline borders, tonal
gradients instead of glows, macOS-style windows, JetBrains-ish monospace.
Run: python3 gen.py
"""
import html, math, pathlib, random, textwrap

OUT = pathlib.Path(__file__).parent / "assets-v3"
OUT.mkdir(exist_ok=True)
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
BG, CARD, LINE, LINE2 = "#0a0a0a", "#0e0e0e", "#242424", "#333333"
TEXT, MUTED, DIM = "#f0f0f0", "#a3a3a3", "#6b6b6b"
GREEN, BLUE, ORANGE, PURPLE, RED = "#22c55e", "#60a5fa", "#f97316", "#a855f7", "#ef4444"
SGREEN, SBLUE, SORANGE, SPURPLE, SRED, SPINK = "#34d17a", "#6fb0ff", "#fb923c", "#c084fc", "#f87171", "#f472b6"
SOFT = {GREEN: SGREEN, BLUE: SGREEN, ORANGE: SGREEN, PURPLE: SGREEN, RED: SGREEN, "#ec4899": SGREEN}
BODY = "#dedede"
E = lambda s: html.escape(str(s), quote=True)
W = 1208  # full row width; GitHub scales it down


def t(x, y, s, size=12, fill=TEXT, weight="normal", anchor="start", family=MONO, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{E(s)}</text>'


def cw(s, size):
    """Approximate monospace text width."""
    return len(s) * size * 0.6


def defs(*items):
    return "<defs>" + "".join(items) + "</defs>"


def vgrad(gid, top, bottom):
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>'


def wash(gid, color, x1="0", y1="0", x2="1", y2="1", a=0.08):
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{color}" stop-opacity="{a}"/><stop offset="0.55" stop-color="{color}" stop-opacity="0.02"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'


def chip(x, y, s, fg=TEXT, right=False, size=10):
    w = int(cw(s, size) + 18)
    if right:
        x = x - w
    return (f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="4" fill="url(#chipg)" stroke="{LINE}"/>'
            + t(x + w / 2, y + 14, s, size, fg, "bold", "middle")), w


def window(name, w, h, title, glyph, body, accent=MUTED, href=None, right=None, mark="//"):
    """Bento panel: hairline border, tonal gradient, '// label' header."""
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}">',
           defs(vgrad("winbg", "#151515", "#080808"), vgrad("chipg", "#1a1a1a", "#0d0d0d"),
                f'<radialGradient id="hl" cx="0.12" cy="0" r="0.9"><stop offset="0" stop-color="#ffffff" stop-opacity="0.06"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>',
                '<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0.7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.35"/></linearGradient>'),
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="url(#winbg)" stroke="#2a2a2a"/>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#hl)"/>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#shade)"/>',
           f'<line x1="11" y1="1" x2="{w-11}" y2="1" stroke="#ffffff" stroke-opacity="0.08"/>',
           t(16, 22, f"{mark} {title}", 11, TEXT, "bold")]
    if right:
        svg.append(t(w - 16, 22, right, 10, MUTED, "bold", "end"))
    svg += body
    svg.append("</svg>")
    (OUT / f"{name}.svg").write_text("\n".join(svg))


def app_tile(x, y, size, c1, c2, mark, gid):
    r = size * 0.24
    out = [defs(vgrad(gid, c1, c2)),
           f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="url(#{gid})"/>',
           f'<rect x="{x+0.5}" y="{y+0.5}" width="{size-1}" height="{size-1}" rx="{r}" fill="none" stroke="#ffffff" stroke-opacity="0.14"/>']
    out += mark(x, y, size)
    return out


# ---- app icon marks (scaled from a 60-unit box) ----
def _s(x, y, size):
    k = size / 60
    return lambda px, py: (x + px * k, y + py * k), k


def mk_terminal(x, y, size):
    p, k = _s(x, y, size)
    a, b, c = p(17, 22), p(25, 30), p(17, 38)
    d, e = p(30, 38), p(44, 38)
    return [f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]} L{c[0]},{c[1]}" stroke="{GREEN}" stroke-width="{4*k}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<line x1="{d[0]}" y1="{d[1]}" x2="{e[0]}" y2="{e[1]}" stroke="#e5e5e5" stroke-width="{4*k}" stroke-linecap="round"/>']


def mk_folder(x, y, size):
    p, k = _s(x, y, size)
    a = p(12, 17)
    return [f'<rect x="{a[0]}" y="{a[1]}" width="{38*k}" height="{30*k}" rx="{3*k}" fill="#fff" fill-opacity="0.92"/>',
            f'<rect x="{a[0]}" y="{a[1]+10*k}" width="{38*k}" height="{20*k}" rx="{3*k}" fill="#fff"/>']


def mk_brief(x, y, size):
    p, k = _s(x, y, size)
    a = p(12, 20)
    return [f'<rect x="{a[0]}" y="{a[1]}" width="{36*k}" height="{24*k}" rx="{4*k}" fill="#fff" fill-opacity="0.95"/>',
            f'<rect x="{a[0]+6*k}" y="{a[1]+9*k}" width="{16*k}" height="{3*k}" rx="{1.5*k}" fill="{ORANGE}"/>',
            f'<rect x="{a[0]+6*k}" y="{a[1]+15*k}" width="{24*k}" height="{3*k}" rx="{1.5*k}" fill="{ORANGE}" fill-opacity="0.6"/>']


def mk_bars(x, y, size):
    p, k = _s(x, y, size)
    out = []
    for bx, by, bh, op in [(14, 30, 16, 0.7), (26, 18, 28, 1), (38, 25, 21, 0.85)]:
        q = p(bx, by)
        out.append(f'<rect x="{q[0]}" y="{q[1]}" width="{7*k}" height="{bh*k}" rx="{1.5*k}" fill="#fff" fill-opacity="{op}"/>')
    return out


def mk_nodes(x, y, size):
    p, k = _s(x, y, size)
    c = p(30, 30)
    out = [f'<circle cx="{c[0]}" cy="{c[1]}" r="{5*k}" fill="#fff"/>']
    for nx, ny in [(30, 14), (44, 38), (16, 38)]:
        q = p(nx, ny)
        out.append(f'<line x1="{c[0]}" y1="{c[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#fff" stroke-width="{2.5*k}"/>')
        out.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="{4*k}" fill="#fff" fill-opacity="0.9"/>')
    return out


def mk_shield(x, y, size):
    p, k = _s(x, y, size)
    pts = [p(30, 12), p(46, 18), p(46, 30), p(30, 50), p(14, 30), p(14, 18)]
    d = "M" + " L".join(f"{a},{b}" for a, b in pts) + " Z"
    a, b, c = p(22, 30), p(28, 36), p(38, 24)
    return [f'<path d="{d}" fill="#fff" fill-opacity="0.95"/>',
            f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]} L{c[0]},{c[1]}" stroke="{RED}" stroke-width="{3.5*k}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>']


def mk_doc(x, y, size):
    p, k = _s(x, y, size)
    a = p(18, 12)
    out = [f'<rect x="{a[0]}" y="{a[1]}" width="{26*k}" height="{36*k}" rx="{2*k}" fill="#fff" stroke="#a8a29e" stroke-width="{1.5*k}"/>']
    for i, wdt in enumerate([18, 18, 12]):
        q = p(21, 28 + i * 6)
        out.append(f'<rect x="{q[0]}" y="{q[1]}" width="{wdt*k}" height="{2.5*k}" rx="{1*k}" fill="{"#57534e" if i == 0 else "#a8a29e"}"/>')
    return out


def mk_mail(x, y, size):
    p, k = _s(x, y, size)
    a = p(12, 18); b = p(14, 21); c = p(30, 33); d = p(46, 21)
    return [f'<rect x="{a[0]}" y="{a[1]}" width="{36*k}" height="{24*k}" rx="{4*k}" fill="#fff"/>',
            f'<path d="M{b[0]},{b[1]} L{c[0]},{c[1]} L{d[0]},{d[1]}" stroke="#0ea5e9" stroke-width="{3*k}" fill="none" stroke-linejoin="round"/>']


def mk_gear(x, y, size):
    p, k = _s(x, y, size)
    c = p(30, 30)
    out = [f'<circle cx="{c[0]}" cy="{c[1]}" r="{8*k}" fill="none" stroke="#fff" stroke-width="{4*k}"/>']
    for i in range(8):
        a = i * math.pi / 4
        x1, y1 = c[0] + math.cos(a) * 12 * k, c[1] + math.sin(a) * 12 * k
        x2, y2 = c[0] + math.cos(a) * 17 * k, c[1] + math.sin(a) * 17 * k
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="{4*k}" stroke-linecap="round"/>')
    return out


APPS = [
    ("terminal", "#1f2937", "#030712", mk_terminal),
    ("projects", "#3b82f6", "#1d4ed8", mk_folder),
    ("experience", "#f97316", "#c2410c", mk_brief),
    ("skills", "#a855f7", "#6d28d9", mk_bars),
    ("research", "#22c55e", "#15803d", mk_nodes),
    ("ouroboros", "#ef4444", "#991b1b", mk_shield),
    ("resume", "#f5f5f4", "#d6d3d1", mk_doc),
    ("contact", "#0ea5e9", "#0369a1", mk_mail),
    ("settings", "#6b7280", "#374151", mk_gear),
]


def folder_icon(x, y, size=44, color="#5b9dff"):
    k = size / 60
    return [f'<path d="M{x+6*k},{y+16*k} a{4*k},{4*k} 0 0 1 {4*k},-{4*k} h{13*k} l{5*k},{5*k} h{22*k} a{4*k},{4*k} 0 0 1 {4*k},{4*k} v{26*k} a{4*k},{4*k} 0 0 1 -{4*k},{4*k} h-{44*k} a{4*k},{4*k} 0 0 1 -{4*k},-{4*k} z" fill="{color}" fill-opacity="0.6"/>',
            f'<path d="M{x+6*k},{y+24*k} h{48*k} v{23*k} a{4*k},{4*k} 0 0 1 -{4*k},{4*k} h-{40*k} a{4*k},{4*k} 0 0 1 -{4*k},-{4*k} z" fill="{color}"/>',
            f'<rect x="{x+6*k}" y="{y+24*k}" width="{48*k}" height="{3*k}" fill="#fff" fill-opacity="0.22"/>']


def heat(x, y, cell=9, gap=3, seed=7, cols=12, rows=7):
    rnd = random.Random(seed)
    out = []
    lv = ["#1c1c1c", "#14532d", "#166534", "#16a34a", "#22c55e"]
    for c in range(cols):
        for r in range(rows):
            l = rnd.choices([0, 1, 2, 3, 4], weights=[45, 22, 16, 11, 6])[0]
            out.append(f'<rect x="{x + c*(cell+gap)}" y="{y + r*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{lv[l]}"/>')
    return out


def network(w, h, seed=3, n=42):
    """Node-graph wallpaper, deterministic."""
    rnd = random.Random(seed)
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.choice([GREEN, GREEN, BLUE])) for _ in range(n)]
    out = []
    for i, (x1, y1, c1) in enumerate(pts):
        for x2, y2, _ in pts[i + 1:]:
            d = math.hypot(x1 - x2, y1 - y2)
            if d < 150:
                out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c1}" stroke-opacity="{0.12*(1-d/150):.3f}"/>')
    for x, y, c in pts:
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1, 2.4):.1f}" fill="{c}" fill-opacity="0.55"/>')
    return out


# ================================================================ hero
def hero():
    w, h = W, 236
    body = [defs(wash("herow", GREEN, a=0.16)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#herow)"/>']
    body.append(t(24, 92, "KRISHIV SETH", 40, GREEN, "bold", extra='letter-spacing="5"'))
    body.append(f'<line x1="24" y1="106" x2="520" y2="106" stroke="{GREEN}" stroke-opacity="0.5"/>')
    body.append(t(24, 128, "SOFTWARE & SECURITY ENGINEER, AI BUILDER", 12, SGREEN))
    body.append(t(24, 156, "CS + Data Science @ NYU Courant '27, Cybersecurity minor.", 12, "#e6eefc"))
    body.append(t(24, 174, "Security infra and AppSec at Clear Street, forward deployed at Forkast (Antler '25),", 12, "#e6eefc"))
    body.append(t(24, 192, "agentic systems at Exar North, GoTrust, Kanlet. Research at OSIRIS Lab, HBS, NYU Langone.", 12, "#e6eefc"))
    x = w - 16
    for sname, c in [("● STATUS: ONLINE", SGREEN), ("NYU: '27", "#b0b0b0"), ("LOC: NYC", "#b0b0b0")]:
        ch, cwid = chip(x, 12, sname, c, right=True); body.append(ch); x -= cwid + 8
    body.append(t(24, h - 14, "krishivseth.com · terminal-first portfolio", 10, MUTED)); body.append(t(w - 16, h - 14, "everything below is on GitHub", 10, DIM, anchor="end"))
    window("hero", w, h, "krishiv_seth", "◈", body)


# ================================================================ project windows
PROJECTS = [
    ("orchard", "Orchard", "Open Source", GREEN, "https://github.com/krishivseth/Orchard",
     "Distributed inference and federated fine-tuning runtime spanning 10+ Apple Silicon devices. Tensor sharding and layer pruning fit 20+ open-source models onto consumer hardware.",
     ["Distributed Systems", "Tensor Sharding", "Apple Silicon"],
     ["Wrote the cluster manager and the peer discovery protocol", "Top 10% of Y Combinator applicants"]),
    ("ouroboros", "Ouroboros", "Security", RED, "https://github.com/krishivseth/Ouroboros",
     "Runtime detection for MCP tool calls against context-aware threat models. AST analysis catches tool poisoning, cross-server shadowing, and rug-pull redefinition.",
     ["Python", "AST Analysis", "MCP"],
     ["Sandboxes untrusted servers", "Provenance via OSV, Socket, Syft/Grype, OpenSSF Scorecard"]),
    ("trevor", "Trevor AI", "Hackathon Winner", PURPLE, "https://github.com/krishivseth/TrevorAI",
     "Phone-callable multi-agent system: an orchestrator voice agent fans out sub-agents for portfolio analysis, research, and trade execution against the Tradier API.",
     ["React", "TypeScript", "FastAPI", "Tradier API"],
     ["React/TypeScript dashboard updates live during the call", "Khosla Ventures x ForgeHacks Grand Prize"]),
    ("watchman", "Watchman", "Open Source", ORANGE, "https://github.com/krishivseth/watchman",
     "Ask a fleet of security cameras questions in plain English and get the matching frames back.",
     ["TypeScript", "SpacetimeDB", "Gemini"],
     ["Frame retrieval over a live camera fleet", "Natural language query layer"]),
    ("rent", "What The Rent?!", "Hackathon Winner", BLUE, "https://github.com/krishivseth/where2liv",
     "Chrome extensions for StreetEasy and Zillow that surface hidden rental costs across utilities, transit, and safety in NYC and SF.",
     ["Flask", "Next.js", "TypeScript", "Chrome APIs"],
     ["Google Maps, building disclosures, and the 311 complaints API", "Microsoft x Musa Capital Grand Prize"]),
    ("series", "Series Events", "Open Source", "#ec4899", "https://github.com/krishivseth/S_Events",
     "Event planning with group chemistry prediction, run entirely over iMessage.",
     ["TypeScript", "iMessage", "AI"],
     ["Group chemistry scoring", "Zero-install: lives in the thread"]),
]


def project_window(slug, name, cat, color, href, desc, tags, log):
    w, h = 596, 200
    sc = SOFT.get(color, color)
    body = [defs(wash(f"pw{slug}", GREEN, a=0.09)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#pw{slug})"/>']
    body.append(t(24, 62, name, 22, sc, "bold"))
    for i, ln in enumerate(textwrap.wrap(desc, 66)[:3]):
        body.append(t(24, 88 + i * 17, ln, 12, BODY))
    x = 24
    for tag in tags:
        c, cwid = chip(x, h - 52, tag, TEXT, size=9.5); body.append(c); x += cwid + 6
    link = "github.com/krishivseth/" + href.rsplit("/", 1)[1] + " ↗"
    room = int((w - 40 - cw(link, 10)) / 6) - 2
    note = log[0] if len(log[0]) <= room else log[0][:room - 1].rstrip() + "…"
    body.append(t(24, h - 14, note, 10, MUTED))
    body.append(t(w - 16, h - 14, link, 10, sc, "bold", "end"))
    window(slug, w, h, f"projects / {slug}", "//", body, color, href, right=cat)


# ================================================================ experience window
ROLES = [
    ("Clear Street", "Cybersecurity Data Eng & AppSec Intern", (2026, 6), (2026, 8), GREEN),
    ("Forkast (Antler '25)", "Forward Deployed Engineering Intern", (2026, 1), (2026, 5), BLUE),
    ("Exar North Group", "AI & Software Engineering Intern", (2025, 6), (2025, 12), ORANGE),
    ("GoTrust", "AI Engineering Intern", (2025, 8), (2025, 9), PURPLE),
    ("Kanlet Inc.", "Software Engineering Intern", (2025, 1), (2025, 5), RED),
    ("Ambee", "Data Science & Engineering Intern", (2024, 6), (2024, 8), GREEN),
]
BULLETS = [
    "Rebuilt the security team's log ingestion pipeline in Go on Kinesis: 80% lower latency, 3 TB/day across 10+ sources, p95 under 4s at 100+ concurrent queries.",
    "Built an app-sec agent harness over Joern code property graphs and a Neptune knowledge graph, cutting false positives 45% on a 120-finding benchmark.",
    "Swept 102 Java services and traced 473 findings to 5 systemic root causes.",
]


ROLE_LINES = [
    ("Jun–Aug 2026", "Clear Street", "Cybersecurity Data Engineering & AppSec Intern", "Go log pipeline on Kinesis (3 TB/day, 80% lower latency); app-sec agent harness over code property graphs, 45% fewer false positives", GREEN),
    ("Jan–May 2026", "Forkast (Antler '25)", "Forward Deployed Engineering Intern", "XGBoost demand forecasts for a Michelin-starred group (14.2% MAPE); full-stack competitor pricing app over containerized agents", BLUE),
    ("Jun–Dec 2025", "Exar North Group", "AI & Software Engineering Intern", "Agentic research platform producing 300+ write-ups a week; serverless newsletter agent for 6,000+ accounts", ORANGE),
    ("Aug–Sep 2025", "GoTrust", "AI Engineering Intern", "GraphRAG NL-to-SQL on Llama 3.2 3B across a 200+ table schema, 92% accuracy at 80% lower inference cost", PURPLE),
    ("Jan–May 2025", "Kanlet Inc.", "Software Engineering Intern", "Full-stack competitor tracking in the CRM: FastAPI over 15 sources, React lead view, 300+ qualified leads", RED),
    ("Jun–Aug 2024", "Ambee", "Data Science & Engineering Intern", "Time-series ILI risk models on AWS from 20 years of GIS data: 0.91 F1, 0.94 R²", GREEN),
]


def experience_window():
    w, h = W, 330
    body = [defs(wash("expw", BLUE, a=0.06)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#expw)"/>', f'<line x1="150" y1="44" x2="150" y2="{h-16}" stroke="{LINE}"/>']
    for i, (when, co, role, hl, c) in enumerate(ROLE_LINES):
        y = 64 + i * 44
        body.append(t(136, y, when, 10, MUTED, anchor="end"))
        body.append(f'<circle cx="150" cy="{y-4}" r="4" fill="{BG}" stroke="{SGREEN}" stroke-width="1.5"/>')
        body.append(t(168, y, co, 12, TEXT, "bold"))
        body.append(t(168 + cw(co, 12) + 12, y, role, 10.5, SBLUE))
        body.append(t(168, y + 16, hl, 10, "#cfcfcf"))
    window("experience", w, h, "experience", "##", body, right="6 internships · 2024 → 2026", mark="##")


# ================================================================ skills, research, awards windows
def skills_window():
    w, h = 596, 250
    groups = [("languages", GREEN, ["Python", "Go", "Java", "Scala", "TypeScript", "C", "SQL", "Bash"]),
              ("full-stack", BLUE, ["React", "Next.js", "Node.js", "FastAPI", "Flask", "React Native"]),
              ("infra", ORANGE, ["AWS", "GCP", "Terraform", "Kubernetes", "Kinesis", "Redis", "ClickHouse", "Postgres"]),
              ("ai / ml", PURPLE, ["fine-tuning", "RAG / GraphRAG", "agentic systems", "LangSmith", "model sharding"]),
              ("security", RED, ["DevSecOps", "AppSec", "MCP security", "supply chain", "detections"])]
    body = [defs(wash("skw", BLUE, a=0.06)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#skw)"/>']
    y = 58
    for k, c, items in groups:
        body.append(t(24, y, k, 10, SBLUE, "bold"))
        x = 110
        for it in items:
            ch, cwid = chip(x, y - 14, it, TEXT, size=9.5)
            if x + cwid > w - 16:
                break
            body.append(ch); x += cwid + 6
        y += 38
    window("skills", w, h, "skills", "//", body, right="51 entries")


def research_window():
    w, h = 596, 250
    body = [defs(wash("rsw", GREEN, a=0.08)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#rsw)"/>']
    items = [("OSIRIS Lab, NYU", "Mar 2026 – now", GREEN, "Byzantine fault tolerance and Sybil attacks in permissionless federated learning. Tooling for attack surfaces in agentic and decentralised systems."),
             ("Harvard Business School & NYU", "Nov 2024 – Sep 2025", BLUE, "GNNs, NLP models, and data infrastructure for group behavior research across 20M+ X profiles."),
             ("NYU Langone Health", "Nov 2024 – Jul 2025", PURPLE, "Data infrastructure supporting neuroscience research at a major academic medical center.")]
    for i, (k, when, c, v) in enumerate(items):
        y = 62 + i * 62
        body.append(f'<rect x="24" y="{y-12}" width="2" height="44" rx="1" fill="{SGREEN}" fill-opacity="0.6"/>')
        body.append(t(38, y, k, 12, SGREEN, "bold")); body.append(t(w - 16, y, when, 9.5, MUTED, anchor="end"))
        for j, ln in enumerate(textwrap.wrap(v, 72)[:2]):
            body.append(t(38, y + 16 + j * 13, ln, 10, "#cfcfcf"))
    window("research", w, h, "research", "//", body, right="3 labs")


def awards_window():
    w, h = W, 150
    body = [defs(wash("aww", GREEN, a=0.06)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#aww)"/>']
    wins = [("GRAND PRIZE", "YC Startup School"), ("GRAND PRIZE", "Antler"), ("GRAND PRIZE", "Microsoft x Musa Capital"), ("GRAND PRIZE", "Khosla Ventures x ForgeHacks"), ("PEOPLE'S CHOICE", "Google x HackNYU")]
    colw = (w - 48) / 5
    for i, (k, v) in enumerate(wins):
        x = 24 + i * colw; c = SBLUE
        body.append(f'<rect x="{x:.0f}" y="54" width="{colw-12:.0f}" height="66" rx="8" fill="url(#chipg)" stroke="{LINE2}"/>')
        body.append(f'<rect x="{x+10:.0f}" y="66" width="2" height="42" rx="1" fill="{c}" fill-opacity="0.6"/>')
        body.append(t(x + 22, 80, k, 9, c, "bold"))
        for j, ln in enumerate(textwrap.wrap(v, 22)[:2]):
            body.append(t(x + 22, 98 + j * 13, ln, 11, TEXT, "bold"))
    window("awards", w, h, "hackathons", "##", body, right="5 wins", mark="##")


def links_bar():
    w, h = W, 44
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="links">',
         defs(vgrad("chipg", "#1a1a1a", "#0f0f0f"), vgrad("dockbg", "#181818", "#0b0b0b")),
         f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="url(#dockbg)" stroke="#2a2a2a"/>', f'<line x1="11" y1="1" x2="{w-11}" y2="1" stroke="#ffffff" stroke-opacity="0.08"/>', defs(wash("lw", GREEN, a=0.07)), f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#lw)"/>']
    x = 14
    for k, v, c in [("web", "krishivseth.com", SGREEN), ("linkedin", "in/krishiv-seth", SBLUE), ("email", "ks7118@nyu.edu", TEXT), ("github", "@krishivseth", TEXT)]:
        b.append(t(x, 27, k, 10, DIM)); x += cw(k, 10) + 8
        b.append(t(x, 27, v, 11, c, "bold")); x += cw(v, 11) + 28
    c, _ = chip(w - 14, 12, "OPEN TO: SWE · security · infra (2027)", SBLUE, right=True); b.append(c)
    b.append("</svg>")
    (OUT / "links.svg").write_text("\n".join(b))


if __name__ == "__main__":
    for f in OUT.glob("*.svg"):
        f.unlink()
    hero()
    for p in PROJECTS:
        project_window(*p)
    experience_window()
    skills_window()
    research_window()
    awards_window()
    links_bar()
    print("generated", len(list(OUT.glob("*.svg"))), "->", OUT)
