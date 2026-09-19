"""Drawings of the physical modules on the bench.

Each function draws one module at (x, y) and returns (svg, pins), where pins maps a pin name to the
absolute coordinate a wire should end on. Proportions follow the real boards closely enough to be
recognised on the bench; they are not to scale with each other.
"""

PCB_BLUE = "#1d4f9e"
PCB_EDGE = "#113570"
PCB_GREEN = "#1f6b3a"
SILK = "#e8eef7"
TERMINAL_GREEN = "#2e9a4c"
TERMINAL_BLUE = "#2b6fd0"
SCREW = "#c9ccd1"
PIN = "#d9b44a"
HEADER = "#1a1a1a"


def text(x, y, s, size=10, anchor="middle", fill=SILK, weight=500, cls="silk"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
            f'font-weight="{weight}" class="{cls}">{s}</text>')


def screw(cx, cy, r=5):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SCREW}" stroke="#7d828a" stroke-width="1"/>'
            f'<path d="M{cx - r * .6} {cy}h{r * 1.2}M{cx} {cy - r * .6}v{r * 1.2}" stroke="#6b7078" '
            f'stroke-width="1.2"/>')


def pcb(x, y, w, h, fill=PCB_BLUE, edge=PCB_EDGE, holes=True):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>'
    if holes:
        for hx, hy in ((x + 7, y + 7), (x + w - 7, y + 7), (x + 7, y + h - 7), (x + w - 7, y + h - 7)):
            s += f'<circle cx="{hx}" cy="{hy}" r="3.2" fill="#0e1a2e" stroke="#c7b27a" stroke-width="1"/>'
    return s


def header_pin(cx, cy):
    return (f'<rect x="{cx - 4}" y="{cy - 4}" width="8" height="8" fill="{HEADER}"/>'
            f'<rect x="{cx - 1.6}" y="{cy - 1.6}" width="3.2" height="3.2" fill="{PIN}"/>')


def terminal_block(x, y, n, pitch=16, color=TERMINAL_GREEN, vertical=False):
    """Screw terminal block; returns svg and the screw centres."""
    w, h = (22, n * pitch + 4) if vertical else (n * pitch + 4, 22)
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{color}" stroke="#0d3d1d" stroke-width="1"/>'
    centres = []
    for i in range(n):
        cx, cy = (x + 11, y + 2 + pitch / 2 + i * pitch) if vertical else (x + 2 + pitch / 2 + i * pitch, y + 11)
        s += screw(cx, cy)
        centres.append((cx, cy))
    return s, centres


def lipo(x, y):
    w, h = 190, 96
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#2b2f36" stroke="#8a919c" stroke-width="1.5"/>'
         f'<rect x="{x + 10}" y="{y + 12}" width="{w - 20}" height="{h - 24}" rx="4" fill="#d6a51c"/>'
         + text(x + w / 2, y + 40, "LiPo 2S", 16, fill="#1b1b1b", weight=700)
         + text(x + w / 2, y + 58, "7.4V nominal · 8.4V full", 10, fill="#1b1b1b")
         + text(x + w / 2, y + 72, "balance lead", 9, fill="#3a3a3a"))
    # XT60 plug hanging off the pack
    px, py = x + w + 34, y + 30
    s += (f'<path d="M{x + w} {y + 34}C{x + w + 14} {y + 34} {px - 12} {py + 8} {px} {py + 8}" stroke="#e53935" stroke-width="6" fill="none"/>'
          f'<path d="M{x + w} {y + 62}C{x + w + 14} {y + 62} {px - 12} {py + 26} {px} {py + 26}" stroke="#0b0b0b" stroke-width="6" fill="none"/>'
          f'<path d="M{px} {py}h34l8 8v20l-8 8h-34z" fill="#f2c531" stroke="#9c7c10" stroke-width="1.2"/>'
          + text(px + 20, py + 21, "XT60", 9, fill="#4a3a00", weight=700))
    return s, {"pos": (px + 42, py + 12), "neg": (px + 42, py + 26)}


def blade_fuse(x, y):
    """Inline ATO blade fuse holder with its cap, 10A red blade."""
    s = (f'<rect x="{x}" y="{y}" width="70" height="30" rx="8" fill="#161616" stroke="#666" stroke-width="1.2"/>'
         f'<rect x="{x + 22}" y="{y - 12}" width="26" height="20" rx="3" fill="#d62b2b" stroke="#7d1111"/>'
         + text(x + 35, y + 2, "10A", 9, fill="#fff", weight=700)
         + text(x + 35, y + 48, "ATO blade fuse", 9, cls="lbl"))
    return s, {"in": (x, y + 15), "out": (x + 70, y + 15)}


def rocker_switch(x, y):
    s = (f'<rect x="{x}" y="{y}" width="46" height="34" rx="4" fill="#111" stroke="#777" stroke-width="1.2"/>'
         f'<rect x="{x + 8}" y="{y + 6}" width="30" height="22" rx="3" fill="#2a2a2a" stroke="#999"/>'
         + text(x + 16, y + 21, "I", 9) + text(x + 31, y + 21, "O", 9)
         + text(x + 23, y + 50, "main switch", 9, cls="lbl"))
    return s, {"in": (x, y + 17), "out": (x + 46, y + 17)}


def acs712(x, y):
    w, h = 96, 44
    s = pcb(x, y, w, h, holes=False)
    tb, sc = terminal_block(x - 4, y + 6, 2, pitch=16, vertical=True)
    s += tb
    s += f'<rect x="{x + 34}" y="{y + 14}" width="18" height="14" fill="#111"/>'
    pins = {}
    for i, name in enumerate(["VCC", "OUT", "GND"]):
        cy = y + 10 + i * 12
        s += header_pin(x + w - 8, cy) + text(x + w - 18, cy + 3, name, 7, anchor="end")
        pins[name] = (x + w - 4, cy)
    s += text(x + w / 2, y + h + 14, "ACS712 30A", 10, cls="lbl")
    pins["IP+"] = sc[0]
    pins["IP-"] = sc[1]
    return s, pins


def wago(x, y, n, label):
    pitch = 13
    w = n * pitch + 8
    s = f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="3" fill="#dfe6ea" fill-opacity=".35" stroke="#b9c3c9" stroke-width="1.2"/>'
    ports = []
    for i in range(n):
        px = x + 4 + i * pitch
        s += f'<rect x="{px}" y="{y + 4}" width="{pitch - 2}" height="18" rx="2" fill="#f07c1a" stroke="#a24e05"/>'
        ports.append((px + (pitch - 2) / 2, y + 34))
    s += text(x + w / 2, y + 31, "221", 7, fill="#36424a", weight=700)
    s += text(x + w / 2, y - 6, label, 9, cls="lbl")
    return s, {f"p{i + 1}": p for i, p in enumerate(ports)}


def lm2596(x, y):
    w, h = 132, 58
    s = pcb(x, y, w, h)
    s += (f'<rect x="{x + 22}" y="{y + 14}" width="26" height="22" fill="#222"/>'
          f'<rect x="{x + 58}" y="{y + 12}" width="30" height="30" rx="4" fill="#2a2a2a"/>'
          + text(x + 73, y + 31, "47", 8)
          + f'<rect x="{x + 96}" y="{y + 10}" width="16" height="16" rx="2" fill="#2f63c9" stroke="#bcd"/>'
          + f'<circle cx="{x + 104}" cy="{y + 18}" r="3" fill="#d8b86a"/>')
    pins = {"IN+": (x + 6, y + 18), "IN-": (x + 6, y + 42), "OUT+": (x + w - 6, y + 18), "OUT-": (x + w - 6, y + 42)}
    for n, (px, py) in pins.items():
        s += f'<circle cx="{px}" cy="{py}" r="4" fill="#cfd4da" stroke="#777"/>'
    s += text(x + 18, y + 54, "IN", 7) + text(x + w - 18, y + 54, "OUT", 7)
    s += text(x + w / 2, y + h + 14, "LM2596 · 5.00V logic", 10, cls="lbl")
    return s, pins


def szbk07(x, y):
    w, h = 196, 124
    s = ""
    # the two heatsink bars sit at battery potential
    for hy in (y - 12, y + h - 6):
        s += f'<rect x="{x + 20}" y="{hy}" width="{w - 40}" height="18" rx="2" fill="#b8c6d6" stroke="#ff6b3d" stroke-width="1.6" stroke-dasharray="4 3"/>'
        for i in range(12):
            s += f'<rect x="{x + 26 + i * 12.5}" y="{hy + 2}" width="3" height="14" fill="#8797aa"/>'
    s += pcb(x, y, w, h)
    for cx, cy in ((x + 70, y + 46), (x + 100, y + 38), (x + 70, y + 80), (x + 130, y + 82)):
        s += f'<circle cx="{cx}" cy="{cy}" r="11" fill="#1d3c2c" stroke="#9fb" stroke-width="1"/>'
    s += f'<circle cx="{x + 118}" cy="{y + 58}" r="18" fill="none" stroke="#b87333" stroke-width="7"/>'
    tb_in, sc_in = terminal_block(x + 4, y + 36, 2, pitch=20, color="#222", vertical=True)
    tb_out, sc_out = terminal_block(x + w - 26, y + 36, 2, pitch=20, color="#222", vertical=True)
    s += tb_in + tb_out
    s += text(x + 44, y + 34, "IN+", 7, anchor="start") + text(x + 44, y + 76, "IN−", 7, anchor="start")
    s += text(x + w - 32, y + 34, "OUT+", 7, anchor="end") + text(x + w - 32, y + 76, "OUT−", 7, anchor="end")
    s += text(x + w / 2, y + h + 28, "SZBK07 · 6.0V servo", 10, cls="lbl")
    s += text(x + w / 2, y - 18, "heatsinks live at battery +", 8, fill="#ff8a65", cls="warn")
    return s, {"IN+": sc_in[0], "IN-": sc_in[1], "OUT+": sc_out[0], "OUT-": sc_out[1]}


def bus_bar(x, y, color, label, n=12):
    """Twelve-screw bar, two staggered rows of six, clear cover."""
    w, h = 330, 62
    base = "#b3261e" if color == "red" else "#0d0d0d"
    s = (f'<rect x="{x - 14}" y="{y - 4}" width="{w + 28}" height="{h + 8}" rx="31" fill="{base}" stroke="#555" stroke-width="1.2"/>'
         f'<rect x="{x}" y="{y + 4}" width="{w}" height="{h - 8}" rx="24" fill="#e6f0f5" fill-opacity=".18" stroke="#cfe3ec" stroke-opacity=".5"/>')
    screws = []
    for i in range(n):
        row = i % 2
        cx = x + 42 + (i // 2) * 44 + row * 22
        cy = y + 20 + row * 22
        s += screw(cx, cy, 6)
        screws.append((cx, cy))
    s += text(x + w / 2, y + h + 18, label, 10, cls="lbl")
    return s, {f"s{i + 1}": p for i, p in enumerate(screws)}


def relay_pnp(x, y):
    """The module on the bench: blue, low-level trigger, PNP input stage, SRD-05VDC-SL-C."""
    w, h = 72, 118
    s = pcb(x, y, w, h, holes=False)
    s += (f'<rect x="{x + 10}" y="{y + 24}" width="52" height="56" rx="3" fill="#2d6fe0" stroke="#9cc0ff"/>'
          + text(x + 36, y + 48, "SONGLE", 7) + text(x + 36, y + 60, "SRD-05VDC", 7) + text(x + 36, y + 70, "-SL-C", 7)
          + f'<circle cx="{x + 16}" cy="{y + 12}" r="4" fill="#e53935"/><circle cx="{x + 56}" cy="{y + 12}" r="4" fill="#43d15b"/>')
    pins = {}
    for i, n in enumerate(["VCC", "GND", "IN"]):
        cx = x + 26 + i * 10
        s += header_pin(cx, y + 8)
        pins[n] = (cx, y - 2)
    tb, sc = terminal_block(x + 10, y + h - 26, 3, pitch=17, color=TERMINAL_BLUE)
    s += tb
    for (cx, cy), n in zip(sc, ["NO", "COM", "NC"]):
        s += text(cx, cy + 22, n, 7)
        pins[n] = (cx, cy)
    return s, pins


def relay_ky019(x, y):
    """Proposed replacement: KY-019 / HW-482, NPN input stage, active high, as michaelkubina and Nitro."""
    w, h = 72, 118
    s = pcb(x, y, w, h, fill="#15151a", edge="#444", holes=False)
    s += (f'<rect x="{x + 10}" y="{y + 24}" width="52" height="56" rx="3" fill="#2d6fe0" stroke="#9cc0ff"/>'
          + text(x + 36, y + 50, "SRD-05VDC", 7) + text(x + 36, y + 62, "KY-019", 8, weight=700)
          + f'<circle cx="{x + 56}" cy="{y + 12}" r="4" fill="#e53935"/>')
    pins = {}
    for i, n in enumerate(["S", "+", "-"]):
        cx = x + 26 + i * 10
        s += header_pin(cx, y + 8)
        pins[n] = (cx, y - 2)
    tb, sc = terminal_block(x + 10, y + h - 26, 3, pitch=17, color=TERMINAL_BLUE)
    s += tb
    for (cx, cy), n in zip(sc, ["NO", "COM", "NC"]):
        s += text(cx, cy + 22, n, 7)
        pins[n] = (cx, cy)
    return s, pins
