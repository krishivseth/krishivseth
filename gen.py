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
TEXT, MUTED, DIM = "#e5e5e5", "#8a8a8a", "#555555"
GREEN, BLUE, ORANGE, PURPLE, RED = "#22c55e", "#60a5fa", "#f97316", "#a855f7", "#ef4444"
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
           defs(vgrad("winbg", "#121212", "#0c0c0c"), vgrad("chipg", "#151515", "#0e0e0e")),
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="url(#winbg)" stroke="{LINE}"/>',
           f'<line x1="11" y1="1" x2="{w-11}" y2="1" stroke="#ffffff" stroke-opacity="0.05"/>',
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
    body = [defs(wash("herow", GREEN, a=0.09), wash("herob", BLUE, "1", "1", "0", "0", a=0.05)),
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#herow)"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="url(#herob)"/>']
    body += [ln for ln in network(w, h, seed=5, n=30)]
    body.append(t(24, 92, "KRISHIV SETH", 40, GREEN, "bold", extra='letter-spacing="5"'))
    body.append(f'<line x1="24" y1="106" x2="520" y2="106" stroke="{GREEN}" stroke-opacity="0.5"/>')
    body.append(t(24, 128, "SOFTWARE & SECURITY ENGINEER, AI BUILDER", 12, GREEN))
    body.append(t(24, 156, "CS + Data Science @ NYU Courant '27, Cybersecurity minor.", 12, "#cbd8ec"))
    body.append(t(24, 174, "Security infra and AppSec at Clear Street, forward deployed at Forkast (Antler '25),", 12, "#cbd8ec"))
    body.append(t(24, 192, "agentic systems at Exar North, GoTrust, Kanlet. Research at OSIRIS Lab, HBS, NYU Langone.", 12, "#cbd8ec"))
    x = w - 16
    for sname, c in [("● STATUS: ONLINE", GREEN), ("NYU: '27", TEXT), ("LOC: NYC", TEXT)]:
        ch, cwid = chip(x, 12, sname, c, right=True); body.append(ch); x -= cwid + 8
    # stat strip
    stats = [("6", "roles shipped"), ("5x", "hackathon wins"), ("3", "research labs"), ("20+", "models on consumer hw")]
    sx = w - 16 - 4 * 150
    for i, (n, lab) in enumerate(stats):
        x = sx + i * 150
        body.append(f'<rect x="{x}" y="44" width="140" height="56" rx="8" fill="{BG}" stroke="{LINE}"/>')
        body.append(t(x + 12, 70, n, 20, TEXT, "bold")); body.append(t(x + 12, 88, lab, 9.5, MUTED))
    body.append(t(24, h - 14, "krishivseth.com · terminal-first portfolio", 10, MUTED)); body.append(t(w - 16, h - 14, "type 'help' there", 10, DIM, anchor="end"))
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


def hash7(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch); h = (h * 16777619) & 0xFFFFFFFF
    return f"{h:08x}"[:7]


def project_window(slug, name, cat, color, href, desc, tags, log):
    w, h = 596, 250
    body = [defs(wash(f"pw{slug}", color, a=0.07)), f'<rect x="1" y="35" width="{w-2}" height="{h-36}" fill="url(#pw{slug})"/>']
    # tree
    body.append(f'<rect x="1" y="35" width="150" height="{h-36}" fill="{BG}" fill-opacity="0.6"/><line x1="151" y1="35" x2="151" y2="{h-1}" stroke="{LINE}"/>')
    body.append(t(14, 56, "~/projects", 9.5, DIM))
    for i, (s2, _, _, c2, *_r) in enumerate(PROJECTS):
        y = 78 + i * 24
        sel = s2 == slug
        if sel:
            body.append(f'<rect x="8" y="{y-15}" width="136" height="22" rx="5" fill="#161616"/>')
        body.append(f'<circle cx="20" cy="{y-4}" r="3" fill="{c2}"/>')
        body.append(t(30, y, s2 + "/", 10.5, TEXT if sel else MUTED, "bold" if sel else "normal"))
    # detail
    dx = 168
    body.append(t(dx, 56, f"~/projects/{slug}/README.md", 9.5, DIM))
    body.append(t(dx, 82, name, 19, color, "bold"))
    for i, ln in enumerate(textwrap.wrap(desc, 58)[:3]):
        body.append(t(dx, 104 + i * 16, ln, 11, "#c4c4c4"))
    x = dx
    for tag in tags:
        c, cwid = chip(x, 156, tag, TEXT, size=9.5); body.append(c); x += cwid + 6
    # git log
    body.append(f'<rect x="{dx}" y="186" width="{w-dx-14}" height="52" rx="6" fill="{BG}" stroke="{LINE}"/>')
    body.append(t(dx + 10, 202, "$ git log --oneline", 9.5, DIM))
    for i, line in enumerate(log[:2]):
        y = 216 + i * 14
        body.append(t(dx + 10, y, hash7(name + line), 9.5, MUTED, "bold"))
        body.append(t(dx + 66, y, line[:58], 9.5, "#c4c4c4"))
    window(slug, w, h, f"projects / {slug}", "//", body, color, href, right=cat, mark="//")


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


def mi(y, m):
    return (y - 2024) * 12 + (m - 1)


def experience_window():
    w, h = W, 330
    S, En = mi(2024, 5), mi(2026, 9)
    pct = lambda v: (v - S) / (En - S)
    body = [defs(wash("expw", ORANGE, a=0.05)), f'<rect x="1" y="35" width="{w-2}" height="{h-36}" fill="url(#expw)"/>']
    gx, gw = 150, 560
    for i, (co, role, s, e, c) in enumerate(ROLES):
        y = 60 + i * 26
        if i == 0:
            body.append(f'<rect x="14" y="{y-14}" width="{gx+gw-6}" height="24" rx="5" fill="#161616"/>')
        body.append(t(24, y + 4, co.replace(" (Antler '25)", "").replace(" Inc.", "").replace(" Group", ""), 11, TEXT if i == 0 else MUTED, "bold" if i == 0 else "normal"))
        body.append(f'<rect x="{gx}" y="{y-4}" width="{gw}" height="10" rx="3" fill="#000" stroke="#1c1c1c"/>')
        x0 = gx + pct(mi(*s)) * gw; x1 = gx + pct(mi(*e) + 1) * gw
        body.append(f'<rect x="{x0:.0f}" y="{y-3}" width="{x1-x0:.0f}" height="8" rx="2" fill="{c}"/>')
    for m, lab in [(mi(2024, 7), "Jul 24"), (mi(2025, 1), "Jan 25"), (mi(2025, 7), "Jul 25"), (mi(2026, 1), "Jan 26"), (mi(2026, 7), "Jul 26")]:
        body.append(t(gx + pct(m) * gw, 228, lab, 9.5, DIM, anchor="middle"))
    # detail
    dx = 740
    body.append(f'<line x1="{dx-16}" y1="48" x2="{dx-16}" y2="{h-14}" stroke="{LINE}"/>')
    body.append(f'<rect x="{dx-4}" y="52" width="3" height="{h-70}" rx="1.5" fill="{GREEN}"/>')
    body.append(t(dx + 10, 68, "Clear Street", 15, GREEN, "bold"))
    body.append(t(dx + 10, 86, "Cybersecurity Data Engineering &", 10.5, TEXT, "bold")); body.append(t(dx + 10, 100, "Application Security Engineering Intern", 10.5, TEXT, "bold"))
    body.append(t(dx + 10, 116, "Jun 2026 – Aug 2026 · New York, NY", 9.5, MUTED))
    y = 136
    for bl in BULLETS:
        for j, ln in enumerate(textwrap.wrap(bl, 56)[:3]):
            body.append(t(dx + 10 + (0 if j == 0 else 10), y, ("• " if j == 0 else "") + ln, 9.5, "#c4c4c4"))
            y += 13
        y += 5
    body.append(t(24, h - 16, "6 internships · 2024 → 2026", 10, MUTED)); body.append(t(gx + gw, h - 16, "tap a row on the site for details", 10, DIM, anchor="end"))
    window("experience", w, h, "experience", "##", body, right="6 roles · 2024 → 2026", mark="##")


# ================================================================ skills, research, awards windows
def skills_window():
    w, h = 596, 250
    groups = [("lang", 9, GREEN, "Python · Go · Java · Scala · TS · C · SQL · Bash"), ("web", 9, BLUE, "React · Next.js · Node · FastAPI · Flask"), ("infra", 17, ORANGE, "AWS · GCP · Terraform · K8s · Kinesis · Redis · ClickHouse"), ("ai/ml", 9, PURPLE, "fine-tuning · RAG/GraphRAG · agentic systems · LangSmith"), ("sec", 7, RED, "DevSecOps · AppSec · MCP security · supply chain")]
    mx = max(g[1] for g in groups)
    body = [defs(wash("skw", PURPLE, a=0.05)), f'<rect x="1" y="35" width="{w-2}" height="{h-36}" fill="url(#skw)"/>']
    bx, bw_, bh, gap = 24, 40, 140, 14
    for i, (k, n, c, _) in enumerate(groups):
        x = bx + i * (bw_ + gap)
        body.append(f'<rect x="{x}" y="66" width="{bw_}" height="{bh}" rx="4" fill="#000" stroke="{LINE}"/>')
        fh = bh * n / mx
        body.append(f'<rect x="{x+1}" y="{66 + bh - fh:.0f}" width="{bw_-2}" height="{fh:.0f}" rx="2" fill="{c}"/>')
        body.append(t(x + bw_ / 2, 58, str(n), 10.5, c, "bold", "middle"))
        body.append(t(x + bw_ / 2, 222, k, 9.5, MUTED, anchor="middle"))
    lx = 310
    body.append(f'<line x1="{lx-14}" y1="48" x2="{lx-14}" y2="{h-14}" stroke="{LINE}"/>')
    for i, (k, n, c, desc) in enumerate(groups):
        y = 66 + i * 36
        body.append(t(lx, y, k, 10.5, c, "bold"))
        for j, ln in enumerate(textwrap.wrap(desc, 40)[:2]):
            body.append(t(lx, y + 13 + j * 12, ln, 9.5, "#c4c4c4"))
    window("skills", w, h, "skills", "//", body, right="51 entries")


def research_window():
    w, h = 596, 250
    body = [defs(wash("rsw", GREEN, a=0.05)), f'<rect x="1" y="35" width="{w-2}" height="{h-36}" fill="url(#rsw)"/>']
    cx, cy = 110, 140
    nodes = [("OSIRIS", -90, GREEN), ("HBS", 30, BLUE), ("NYUL", 150, PURPLE)]
    for name, ang, c in nodes:
        a = math.radians(ang); x, y = cx + math.cos(a) * 64, cy + math.sin(a) * 64
        body.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{c}" stroke-opacity="0.5"/>')
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="18" fill="{BG}" stroke="{c}" stroke-width="1.5"/>')
        body.append(t(x, y + 3.5, name, 9, c, "bold", "middle"))
    body.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#000" stroke="{LINE2}" stroke-width="1.5"/>'); body.append(t(cx, cy + 3.5, "me", 8, MUTED, anchor="middle"))
    items = [("OSIRIS Lab (NYU)", GREEN, "Byzantine fault tolerance and Sybil attacks in permissionless FL. Attack surfaces in agentic and decentralised systems."),
             ("Harvard Business School & NYU", BLUE, "GNNs, NLP, and data infrastructure for group behavior across 20M+ X profiles."),
             ("NYU Langone Health", PURPLE, "Data infrastructure supporting neuroscience research.")]
    lx = 236
    body.append(f'<line x1="{lx-14}" y1="48" x2="{lx-14}" y2="{h-14}" stroke="{LINE}"/>')
    for i, (k, c, v) in enumerate(items):
        y = 64 + i * 60
        body.append(t(lx, y, k, 11, c, "bold"))
        for j, ln in enumerate(textwrap.wrap(v, 50)[:2]):
            body.append(t(lx, y + 15 + j * 13, ln, 9.5, "#c4c4c4"))
    window("research", w, h, "research", "//", body, right="3 labs")


def awards_window():
    w, h = W, 150
    body = [defs(wash("aww", GREEN, a=0.05)), f'<rect x="1" y="35" width="{w-2}" height="{h-36}" fill="url(#aww)"/>']
    wins = [("GRAND PRIZE", "YC Startup School"), ("GRAND PRIZE", "Antler"), ("GRAND PRIZE", "Microsoft x Musa Capital"), ("GRAND PRIZE", "Khosla Ventures x ForgeHacks"), ("PEOPLE'S CHOICE", "Google x HackNYU")]
    colw = (w - 48) / 5
    for i, (k, v) in enumerate(wins):
        x = 24 + i * colw; c = BLUE if "PEOPLE" in k else GREEN
        body.append(f'<rect x="{x:.0f}" y="54" width="{colw-12:.0f}" height="66" rx="8" fill="{BG}" stroke="{LINE}"/>')
        body.append(f'<rect x="{x+10:.0f}" y="66" width="3" height="42" rx="1.5" fill="{c}"/>')
        body.append(t(x + 22, 80, k, 9, c, "bold"))
        for j, ln in enumerate(textwrap.wrap(v, 22)[:2]):
            body.append(t(x + 22, 98 + j * 13, ln, 11, TEXT, "bold"))
    window("awards", w, h, "hackathons", "##", body, right="5 wins", mark="##")


def links_bar():
    w, h = W, 44
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="links">',
         defs(vgrad("chipg", "#151515", "#0e0e0e"), vgrad("dockbg", "#161616", "#0c0c0c")),
         f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="url(#dockbg)" stroke="{LINE}"/>']
    x = 14
    for k, v, c in [("web", "krishivseth.com", GREEN), ("linkedin", "in/krishiv-seth", BLUE), ("email", "ks7118@nyu.edu", TEXT), ("github", "@krishivseth", TEXT)]:
        b.append(t(x, 27, k, 10, DIM)); x += cw(k, 10) + 8
        b.append(t(x, 27, v, 11, c, "bold")); x += cw(v, 11) + 28
    c, _ = chip(w - 14, 12, "OPEN TO: SWE · security · infra (2027)", ORANGE, right=True); b.append(c)
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
