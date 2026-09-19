"""Renders wiring-current.svg and wiring-final.svg, and wiring.json for the interactive page.

    python3 docs/wiring/build.py
"""

import json
from html import escape
from pathlib import Path

import layout
import parts_logic as L
from parts import text
from wires import KINDS, NETS, STUBS, WIRES

HERE = Path(__file__).parent
BG = "#0f1716"
STATUS_LABEL = {"ok": "built and measured", "plan": "to build before it walks",
                "later": "after it walks", "open": "not connected on purpose"}


def in_view(tag, view):
    return tag == "both" or tag == view


def place(view):
    svg, pins = [], {}
    for name, (fn, x, y, args, tag) in layout.PLACEMENT.items():
        if not in_view(tag, view):
            continue
        s, p = fn(x, y, *args)
        cls = "part later" if tag == "final" and name in ("cam", "oled", "vsens", "gtap") else "part"
        svg.append(f'<g class="{cls}" data-part="{name}">{s}</g>')
        for k, v in p.items():
            pins[f"{name}.{k}"] = v
    return svg, pins


def resolve(route, pins):
    pts = [pins[route[0]]]
    curve_to = None
    for op, val in route[1:]:
        x, y = pts[-1]
        if op == "x":
            pts.append((val, y))
        elif op == "y":
            pts.append((x, val))
        elif op == "xy":
            px, py = pins[val]
            pts += [(px, y), (px, py)]
        elif op == "yx":
            px, py = pins[val]
            pts += [(x, py), (px, py)]
        elif op == "curve":
            curve_to = pins[val]
    if curve_to:
        (x0, y0), (x1, y1) = pts[-1], curve_to
        my = (y0 + y1) / 2
        return f"M{x0:.1f} {y0:.1f}C{x0:.1f} {my:.1f} {x1:.1f} {my:.1f} {x1:.1f} {y1:.1f}"
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def wire_svg(d, net, kind, status, wid, meta):
    width = KINDS[kind][0]
    color = NETS[net]
    dash = ' stroke-dasharray="7 6"' if status == "later" else (' stroke-dasharray="12 5"' if status == "plan" else "")
    halo = "#6a7580" if net == "GND" else "#05090a"
    title = escape(f"{meta['frm']} → {meta['to']} · {KINDS[kind][1]} · {STATUS_LABEL[status]}")
    return (f'<g class="wire st-{status}" data-id="{wid}" tabindex="0"><title>{title}</title>'
            f'<path d="{d}" fill="none" stroke="{halo}" stroke-width="{width + (1.6 if net == 'GND' else 2.4)}" stroke-linejoin="round" stroke-linecap="round" opacity=".9"{dash}/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{dash}/>'
            f'<path class="hit" d="{d}" fill="none" stroke="transparent" stroke-width="{max(width, 10)}"/></g>')


def servos(view, pins):
    out, meta = [], []
    for name, ch in layout.SERVOS:
        x, y = layout.servo_xy(ch)
        s, p = L.servo(x, y, name, ch)
        if view == "current":
            out.append(f'<g class="part ghost">{s}</g>')
            continue
        out.append(f'<g class="part">{s}</g>')
        (x0, y0), (x1, y1) = pins[f"pca.ch{ch}"], p["in"]
        lower = ch % 3 == 2
        wid = f"servo-{ch}"
        strands = ""
        for off, col in ((-2.6, "#6d4c41"), (0, "#e53935"), (2.6, "#ffb300")):
            my = (y0 + y1) / 2
            d = f"M{x0 + off:.1f} {y0}C{x0 + off:.1f} {my:.1f} {x1 + off:.1f} {my:.1f} {x1 + off:.1f} {y1}"
            strands += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.7" stroke-dasharray="12 5" opacity=".9"/>'
        if lower:
            mx, my = x1, y1 - 16
            strands += f'<rect x="{mx - 7}" y="{my - 5}" width="14" height="10" rx="1.5" fill="#111" stroke="#bbb"/>'
        note = "Extension 10-15cm on the lower leg, as in michaelkubina and Leika." if lower else ""
        m = dict(id=wid, frm=f"PCA9685 ch{ch}", to=f"{name} servo", net="servo", kind="servo lead, brown GND · red V+ · orange PWM",
                 status="plan", note=(note + " Centre at 1500µs before the horn goes on.").strip())
        meta.append(m)
        out.append(f'<g class="wire st-plan" data-id="{wid}" tabindex="0"><title>{escape(m["frm"] + " → " + m["to"])}</title>{strands}'
                   f'<path class="hit" d="M{x0} {y0}C{x0} {(y0 + y1) / 2} {x1} {(y0 + y1) / 2} {x1} {y1}" fill="none" stroke="transparent" stroke-width="12"/></g>')
    if view == "current":
        out.append(text(1395, 880, "12 × MG996R · not connected yet · 10 on the legs, 2 spares to centre", 10, cls="lbl"))
    out.append(text(1160, 628, "FRONT LEGS", 9, anchor="start", fill="#7f8f99", weight=700))
    out.append(text(1160, 748, "REAR LEGS", 9, anchor="start", fill="#7f8f99", weight=700))
    return out, meta


def stubs(view, pins):
    out, meta = [], []
    for i, s in enumerate(STUBS):
        if s["view"] != view:
            continue
        x0, y0 = pins[s["pin"]]
        x1, y1 = x0 + s["dx"], y0 + s["dy"]
        wid = f"stub-{i}"
        end = (f'<path d="M{x1 - 6} {y1 - 6}l12 12m0 -12l-12 12" stroke="#ff5252" stroke-width="2.4"/>' if s["status"] == "open"
               else f'<circle cx="{x1}" cy="{y1}" r="3.5" fill="{BG}" stroke="{NETS[s["net"]]}" stroke-width="2"/>')
        anchor = "start"
        lx = x1 + (-6 if anchor == "end" else 7) if s["dx"] == 0 else x1 + 8
        ly = y1 + 4 if s["dy"] >= 0 else y1 - 10
        m = dict(id=wid, frm=s["pin"].replace(".", " "), to=s["label"] or "ESP32, pin TBD", net=s["net"], kind="—", status=s["status"], note=s["note"])
        meta.append(m)
        out.append(f'<g class="wire st-{s["status"]}" data-id="{wid}" tabindex="0"><title>{escape(s["label"])}</title>'
                   f'<path d="M{x0} {y0}L{x1} {y1}" stroke="{NETS[s["net"]]}" stroke-width="2.4" stroke-dasharray="4 4"/>{end}'
                   f'<path class="hit" d="M{x0} {y0}L{x1} {y1}" stroke="transparent" stroke-width="12"/>'
                   + text(lx, ly, escape(s["label"]), 9, anchor=anchor, fill="#ff8a80" if s["status"] == "open" else "#c9d3dc", cls="stub")
                   + "</g>")
    return out, meta


def render(view):
    part_svg, pins = place(view)
    wire_out, meta = [], []
    for wd in WIRES:
        if not in_view(wd["view"], view):
            continue
        d = resolve(wd["route"], pins)
        m = {k: wd[k] for k in ("id", "frm", "to", "net", "status", "note")}
        m["kind"] = KINDS[wd["kind"]][1]
        meta.append(m)
        wire_out.append(wire_svg(d, wd["net"], wd["kind"], wd["status"], wd["id"], m))
    servo_out, smeta = servos(view, pins)
    rl = ("servo rail joint · WAGO 221-412", "relay removed in session 6 · rail follows the pack")
    part_svg.append(f'<path d="M1054 517H1100V392H1152" fill="none" stroke="#7f8f99" stroke-width="1" stroke-dasharray="2 3"/>'
                    + text(1156, 388, rl[0], 9, anchor="start", cls="lbl") + text(1156, 400, rl[1], 8, anchor="start", fill="#8fa0ab"))
    stub_out, stmeta = stubs(view, pins)
    title = "KalebV2 wiring · bench today (session 5)" if view == "current" else "KalebV2 wiring · target, robot complete"
    grid = (f'<pattern id="g-{view}" width="20" height="20" patternUnits="userSpaceOnUse">'
            f'<path d="M20 0H0V20" fill="none" stroke="#1c2a28" stroke-width="1"/></pattern>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {layout.W} {layout.H}" class="wiring" data-view="{view}" '
           f'font-family="IBM Plex Mono, ui-monospace, Menlo, monospace">'
           f'<defs>{grid}<style>.lbl{{fill:#c9d3dc}} .ghost{{opacity:.35}} .later{{opacity:.8}} .st-later{{opacity:.62}}</style></defs>'
           f'<rect width="{layout.W}" height="{layout.H}" fill="{BG}"/><rect width="{layout.W}" height="{layout.H}" fill="url(#g-{view})"/>'
           + text(layout.W - 16, layout.H - 14, title, 11, anchor="end", fill="#7f8f99")
           + "".join(part_svg) + '<g class="wires">' + "".join(wire_out) + "".join(servo_out) + "".join(stub_out) + "</g></svg>")
    return svg, meta + smeta + stmeta


def main():
    data = {}
    for view in ("current", "final"):
        svg, meta = render(view)
        (HERE / f"wiring-{view}.svg").write_text(svg)
        data[view] = {"svg": svg, "wires": meta}
    (HERE / "wiring.json").write_text(json.dumps(data))
    print("wrote", ", ".join(f"{v}: {len(d['wires'])} connections" for v, d in data.items()))


if __name__ == "__main__":
    main()
