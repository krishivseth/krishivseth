import textwrap, html, pathlib, math, random
OUT = pathlib.Path(__file__).parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark":  dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e", chip_bg="#21262d", chip_fg="#c9d1d9"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#57606a", chip_bg="#eaeef2", chip_fg="#24292f"),
}
esc = lambda s: html.escape(s, quote=True)

def pill(x, y, label, t, accent=None):
    w = int(len(label) * 6.6 + 18)
    fill = t["chip_bg"]; fg = t["chip_fg"]
    return (f'<rect x="{x}" y="{y}" rx="10" ry="10" width="{w}" height="20" fill="{fill}"/>'
            f'<text x="{x + w/2}" y="{y+14}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{fg}">{esc(label)}</text>', w)

def card(slug, title, desc, tags, accent, theme):
    t = THEMES[theme]; W, H = 560, 250
    lines = textwrap.wrap(desc, 70)[:5]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>')
    parts.append(f'<rect x="0" y="0" width="6" height="{H}" rx="3" fill="{accent}"/>')
    parts.append(f'<circle cx="34" cy="36" r="6" fill="{accent}"/>')
    parts.append(f'<text x="50" y="42" font-family="{FONT}" font-size="20" font-weight="700" fill="{t["text"]}">{esc(title)}</text>')
    for i, ln in enumerate(lines):
        parts.append(f'<text x="28" y="{80 + i*22}" font-family="{FONT}" font-size="14" fill="{t["muted"]}">{esc(ln)}</text>')
    x = 28
    for tag in tags:
        s, w = pill(x, H - 40, tag, t); parts.append(s); x += w + 8
    parts.append('</svg>')
    (OUT / f"{slug}-{theme}.svg").write_text("\n".join(parts))

def banner(theme):
    t = THEMES[theme]; W, H = 1200, 300
    g1, g2 = ("#0d1117", "#161b22") if theme == "dark" else ("#f6f8fa", "#ffffff")
    node_fill = "#6366f1"; line = "#6366f1"
    rnd = random.Random(7)
    nodes = [(rnd.randint(860, 1150), rnd.randint(36, 264)) for _ in range(16)]
    edges = []
    for i, (x1, y1) in enumerate(nodes):
        d = sorted(range(len(nodes)), key=lambda j: math.hypot(nodes[j][0]-x1, nodes[j][1]-y1))[1:3]
        edges += [(i, j) for j in d]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Krishiv Seth">',
         f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
         f'<radialGradient id="glow" cx="0.85" cy="0.5" r="0.5"><stop offset="0" stop-color="#6366f1" stop-opacity="0.22"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#g)" stroke="{t["border"]}"/>',
         f'<rect x="0" y="0" width="{W}" height="{H}" rx="16" fill="url(#glow)"/>']
    for i, j in edges:
        p.append(f'<line x1="{nodes[i][0]}" y1="{nodes[i][1]}" x2="{nodes[j][0]}" y2="{nodes[j][1]}" stroke="{line}" stroke-opacity="0.35" stroke-width="1.2"/>')
    for k, (x, y) in enumerate(nodes):
        r = 5 if k % 4 else 8
        p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{node_fill}" fill-opacity="{0.9 if r == 8 else 0.6}"/>')
    p.append(f'<text x="64" y="118" font-family="{FONT}" font-size="54" font-weight="800" letter-spacing="-1" fill="{t["text"]}">Krishiv Seth</text>')
    p.append(f'<text x="66" y="158" font-family="{FONT}" font-size="20" fill="{t["muted"]}">Agentic systems, distributed inference, and security tooling.</text>')
    x = 66
    for label in ["NYU Courant '27", "CS + Data Science", "Cybersecurity", "5x hackathon winner", "New York"]:
        s, w = pill(x, 196, label, t); p.append(s); x += w + 10
    p.append(f'<text x="66" y="258" font-family="{MONO}" font-size="13" fill="{t["muted"]}">most recently: Clear Street (security engineering)  ·  Forkast (forward deployed engineering)</text>')
    p.append('</svg>')
    (OUT / f"banner-{theme}.svg").write_text("\n".join(p))

PROJECTS = [
    ("orchard", "Orchard", "Distributed LLM inference across the Apple devices you already own. Splits a model's transformer layers across Macs, iPads and iPhones and streams hidden states between them, with a KV cache, a cluster manager, and a desktop app on top. Top 10% of YC applicants.", ["Python", "PyTorch", "FastAPI", "React", "Electron"], "#6366f1"),
    ("ouroboros", "Ouroboros", "Runtime security for AI agents and MCP servers. Classifies tool calls against context-aware threat models, uses AST analysis to catch tool poisoning and rug-pull redefinitions, sandboxes untrusted servers, and scores dependency provenance.", ["Python", "Security", "MCP"], "#ef4444"),
    ("trevor", "Trevor AI", "A phone-callable investment agent. An orchestrator voice agent fans out sub-agents for portfolio analysis, research, and trade execution in real time, with a dashboard that updates live during the call.", ["TypeScript", "FastAPI", "Voice agents"], "#10b981"),
    ("watchman", "Watchman", "Turns a fleet of security cameras into a live feed you can question in plain English. Continuously indexes footage and answers questions like \"was anyone at the door in the last few minutes?\" with the matching frames.", ["TypeScript", "SpacetimeDB", "Gemini"], "#f59e0b"),
    ("rent", "What The Rent?!", "Chrome extensions for StreetEasy and Zillow that surface the hidden costs of a rental in NYC and SF: utilities, transit, and safety, with neighbourhood insights and safe route mapping built from public building and 311 data.", ["Python", "Next.js", "Chrome extension"], "#0ea5e9"),
    ("series", "Series Events", "Event planning with group chemistry prediction. Create and manage events over iMessage with a conversational bot and send personalised invitations to the people most likely to click.", ["TypeScript", "iMessage", "AI"], "#ec4899"),
]
for theme in THEMES:
    banner(theme)
    for slug, title, desc, tags, accent in PROJECTS:
        card(slug, title, desc, tags, accent, theme)
print("generated", len(list(OUT.glob("*.svg"))), "svgs")
