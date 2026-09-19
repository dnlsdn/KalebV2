"""Builds wiring.html, the interactive version of the two drawings. Run build.py first."""

import json
from pathlib import Path

HERE = Path(__file__).parent

CSS = """
:root{--bg:#0f1716;--panel:#16211f;--line:#263533;--ink:#e3ebe8;--mute:#8fa3a0;--accent:#f07c1a;
--ok:#5fd18a;--plan:#ffcf5a;--later:#9fb3c8;--open:#ff6b6b;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 "IBM Plex Sans",system-ui,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding-inline:16px;padding-block:20px 48px;display:grid;gap:16px}
header{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:12px}
h1{font:600 26px/1.1 "IBM Plex Mono",ui-monospace,monospace;margin:0;letter-spacing:-.01em;text-wrap:balance}
h1 small{display:block;font:400 13px/1.4 "IBM Plex Sans",sans-serif;color:var(--mute);margin-top:6px;letter-spacing:0}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{all:unset;cursor:pointer;padding:8px 14px;font:500 13px "IBM Plex Mono",monospace;color:var(--mute)}
.seg button[aria-pressed="true"]{background:var(--accent);color:#1b0f02}
.seg button:focus-visible,.zoom button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;font:12px "IBM Plex Mono",monospace;color:var(--mute)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend svg{flex:none}
.main{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px;align-items:start}
@media (max-width:980px){.main{grid-template-columns:1fr}}
.stage{position:relative;border:1px solid var(--line);border-radius:10px;overflow:auto;background:#0b1211;max-height:78vh}
.stage svg{display:block;width:calc(100% * var(--z,1));height:auto;min-width:0}
.zoom{position:sticky;top:8px;left:8px;float:left;z-index:2;display:flex;gap:4px;margin:8px}
.zoom button{all:unset;cursor:pointer;width:30px;height:30px;display:grid;place-items:center;border-radius:6px;
background:rgba(22,33,31,.92);border:1px solid var(--line);font:600 15px "IBM Plex Mono",monospace;color:var(--ink)}
.wire{cursor:pointer}
.wire:hover,.wire.sel{filter:drop-shadow(0 0 4px #fff) drop-shadow(0 0 2px #fff)}
.dim .wire:not(.sel){opacity:.18}
aside{position:sticky;top:12px;display:grid;gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card h2{font:600 11px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:0 0 8px}
.detail .route{font:600 15px/1.35 "IBM Plex Mono",monospace;margin:0 0 10px}
dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0;font-size:13px}
dt{color:var(--mute)} dd{margin:0}
.note{margin:10px 0 0;color:#cdd8d5;font-size:13px}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font:600 11px "IBM Plex Mono",monospace}
.st-ok .pill,.pill.ok{background:rgba(95,209,138,.15);color:var(--ok)}
.pill.plan{background:rgba(255,207,90,.15);color:var(--plan)}
.pill.later{background:rgba(159,179,200,.15);color:var(--later)}
.pill.open{background:rgba(255,107,107,.15);color:var(--open)}
.counts{display:flex;flex-wrap:wrap;gap:6px}
table{width:100%;border-collapse:collapse;font-size:13px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
th,td{text-align:left;padding:7px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font:600 11px "IBM Plex Mono",monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);background:var(--panel);position:sticky;top:0}
tbody tr{cursor:pointer} tbody tr:hover,tbody tr.sel{background:#1b2a27}
td.net{font-family:"IBM Plex Mono",monospace;white-space:nowrap}
.sw{display:inline-block;width:18px;height:4px;border-radius:2px;vertical-align:middle;margin-right:6px}
.foot{color:var(--mute);font-size:12px;display:grid;gap:4px}
.foot a{color:#9fd3ff}
@media (prefers-reduced-motion:no-preference){.wire{transition:opacity .15s}}
"""

JS = """
const DATA = __DATA__;
const NETS = __NETS__;
const STATUS = {ok:'built and measured', plan:'to build before it walks', later:'after it walks', open:'not connected on purpose'};
let view = 'current', zoom = 1, selected = null;
const $ = s => document.querySelector(s);
function esc(s){return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function wireById(id){return DATA[view].wires.find(w => w.id === id)}
function show(id){
  const w = wireById(id); if(!w) return;
  $('#detail').innerHTML = `<p class="route">${esc(w.frm)} → ${esc(w.to)}</p>
    <dl><dt>status</dt><dd><span class="pill ${w.status}">${STATUS[w.status]}</span></dd>
    <dt>net</dt><dd><span class="sw" style="background:${NETS[w.net] || '#888'}"></span>${esc(w.net)}</dd>
    <dt>wire</dt><dd>${esc(w.kind)}</dd></dl>${w.note ? `<p class="note">${esc(w.note)}</p>` : ''}`;
}
function select(id){
  selected = selected === id ? null : id;
  document.querySelectorAll('.wire').forEach(g => g.classList.toggle('sel', g.dataset.id === selected));
  document.querySelectorAll('tbody tr').forEach(r => r.classList.toggle('sel', r.dataset.id === selected));
  $('#stage').classList.toggle('dim', !!selected);
  if(selected) show(selected); else reset();
}
function reset(){$('#detail').innerHTML = '<p class="note" style="margin:0">Hover or tap a wire to see where it goes, what it is made of and what was measured on it. Tap again to clear.</p>'}
function render(){
  $('#svgbox').innerHTML = DATA[view].svg;
  document.querySelectorAll('.seg button').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === view));
  const ws = DATA[view].wires;
  const c = {}; ws.forEach(w => c[w.status] = (c[w.status] || 0) + 1);
  $('#counts').innerHTML = ['ok','plan','later','open'].filter(k => c[k]).map(k => `<span class="pill ${k}">${c[k]} · ${STATUS[k]}</span>`).join('');
  const order = {plan:0, open:1, ok:2, later:3};
  $('#rows').innerHTML = [...ws].sort((a, b) => order[a.status] - order[b.status]).map(w =>
    `<tr data-id="${w.id}"><td><span class="pill ${w.status}">${w.status}</span></td>
     <td>${esc(w.frm)}</td><td>${esc(w.to)}</td>
     <td class="net"><span class="sw" style="background:${NETS[w.net] || '#888'}"></span>${esc(w.net)}</td>
     <td>${esc(w.kind)}</td><td>${esc(w.note)}</td></tr>`).join('');
  document.querySelectorAll('.wire').forEach(g => {
    g.addEventListener('mouseenter', () => show(g.dataset.id));
    g.addEventListener('mouseleave', () => selected ? show(selected) : reset());
    g.addEventListener('click', () => select(g.dataset.id));
    g.addEventListener('keydown', e => { if(e.key === 'Enter') select(g.dataset.id) });
  });
  document.querySelectorAll('tbody tr').forEach(r => r.addEventListener('click', () => { select(r.dataset.id); $('#stage').scrollIntoView({block:'nearest', behavior:'smooth'}) }));
  selected = null; $('#stage').classList.remove('dim'); reset();
}
document.querySelectorAll('.seg button').forEach(b => b.addEventListener('click', () => {
  view = b.dataset.view; try{localStorage.setItem('kaleb-view', view)}catch(e){} render();
}));
function setZoom(z){zoom = Math.min(3, Math.max(1, z)); $('#svgbox').style.setProperty('--z', zoom)}
$('#zin').onclick = () => setZoom(zoom + .5); $('#zout').onclick = () => setZoom(zoom - .5); $('#zfit').onclick = () => setZoom(1);
try{ const v = localStorage.getItem('kaleb-view'); if(v === 'final' || v === 'current') view = v }catch(e){}
render();
"""

LEGEND_LINES = [
    ("solid", "", "built and measured"), ("12 5", "", "to build before it walks"),
    ("7 6", "", "after it walks, routing not decided"),
]


def legend():
    out = []
    for dash, _, label in LEGEND_LINES:
        d = f' stroke-dasharray="{dash}"' if dash != "solid" else ""
        out.append(f'<span><svg width="34" height="8" aria-hidden="true"><path d="M1 4H33" stroke="#e3ebe8" stroke-width="3"{d}/></svg>{label}</span>')
    out.append('<span><svg width="14" height="14" aria-hidden="true"><path d="M2 2l10 10m0-10L2 12" stroke="#ff6b6b" stroke-width="2.4"/></svg>not connected on purpose</span>')
    for w, label in ((6.5, "AWG14"), (4.8, "AWG16"), (2.6, "Dupont")):
        out.append(f'<span><svg width="34" height="10" aria-hidden="true"><path d="M1 5H33" stroke="#e53935" stroke-width="{w}"/></svg>{label}</span>')
    return "".join(out)


def main():
    data = json.loads((HERE / "wiring.json").read_text())
    from wires import NETS
    nets = dict(NETS, servo="#ffb300")
    html = f"""<title>KalebV2 Wiring</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header>
  <h1>KalebV2 Wiring<small>SpotMicroESP32 build · every connection on the bench and what is still to come</small></h1>
  <div class="seg" role="group" aria-label="Which drawing">
    <button type="button" data-view="current" aria-pressed="true">Bench today</button>
    <button type="button" data-view="final" aria-pressed="false">Robot complete</button>
  </div>
</header>
<div class="legend">{legend()}</div>
<div class="main">
  <div class="stage" id="stage">
    <div class="zoom"><button type="button" id="zin" aria-label="Zoom in">+</button><button type="button" id="zout" aria-label="Zoom out">−</button><button type="button" id="zfit" aria-label="Fit to width">↔</button></div>
    <div id="svgbox"></div>
  </div>
  <aside>
    <div class="card detail"><h2>Selected wire</h2><div id="detail"></div></div>
    <div class="card"><h2>In this drawing</h2><div class="counts" id="counts"></div></div>
    <div class="card"><h2>Read this first</h2><p class="note" style="margin:0">Power wires are drawn in the colours on the bench. Dupont colours are a convention for this drawing: 5V red, 3.3V violet, SDA yellow, SCL orange, signals blue, analog green. Screw positions on the bus bars are illustrative. There is no relay: the servo rail is live whenever the pack is connected, and in the complete robot the main switch turns it on and off.</p></div>
  </aside>
</div>
<div class="tablewrap"><table><thead><tr><th>status</th><th>from</th><th>to</th><th>net</th><th>wire</th><th>notes</th></tr></thead><tbody id="rows"></tbody></table></div>
<div class="foot">
  <span>Sources: <a href="https://github.com/michaelkubina/SpotMicroESP32" rel="noopener">michaelkubina/SpotMicroESP32</a> (BOM, Fritzing diagram) · <a href="https://github.com/runeharlyk/SpotMicroESP32-Leika" rel="noopener">runeharlyk/SpotMicroESP32-Leika</a> (components, channel map).</span>
  <span>Measured values come from the session logs in main-steps/ and current-power-&amp;-wiring-connections.md. Generated by docs/wiring/build.py and page.py.</span>
</div>
</div>
<script>{JS.replace("__DATA__", json.dumps(data)).replace("__NETS__", json.dumps(nets))}</script>
"""
    (HERE / "wiring.html").write_text(html)  # artifact body, wrapped at publish time
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">')
    (HERE / "index.html").write_text(head + html.replace("<style>", "</head><body><style>", 1).replace(
        '<link rel="preconnect"', '<meta name="color-scheme" content="dark"><link rel="preconnect"', 1) + "</body></html>")
    print("wrote wiring.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
