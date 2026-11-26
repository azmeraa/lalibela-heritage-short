import html, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "outputs" / "ai_production.db"
OUT = ROOT / "outputs" / "ai_production_dashboard.html"

def esc(v):
    return html.escape(str(v if v is not None else "—"))

def make_table(headers, rows, ident, searchable=False):
    search = f'<input class="search" data-target="{ident}" placeholder="Search records…">' if searchable else ""
    th = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(x)}</td>" for x in row) + "</tr>" for row in rows)
    if not body:
        body = f'<tr><td colspan="{len(headers)}">No records available</td></tr>'
    return f'{search}<div class="tablebox"><table id="{ident}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

def main():
    if not DB.exists():
        raise SystemExit(f"Database not found: {DB}")
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    def count(sql):
        return db.execute(sql).fetchone()[0]

    shots = count("SELECT COUNT(*) FROM shots")
    runs = count("SELECT COUNT(*) FROM model_runs")
    success = count("SELECT COUNT(*) FROM model_runs WHERE status='success'")
    failed = count("SELECT COUNT(*) FROM model_runs WHERE status='failed'")
    assets = count("SELECT COUNT(*) FROM assets")
    present = count("SELECT COUNT(*) FROM assets WHERE exists_on_disk=1")
    feedback = count("SELECT COUNT(*) FROM audience_feedback")
    tests = count("SELECT COUNT(*) FROM audience_feedback WHERE is_test_record=1")
    real_feedback = feedback - tests
    rate = round(success / runs * 100, 1) if runs else 0
    missing = assets - present

    models = [dict(r) for r in db.execute("""
      SELECT stage, model, COUNT(*) total_runs,
      SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) successful,
      SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) failed,
      ROUND(AVG(CASE WHEN status='success' THEN latency_seconds END),2) avg_latency,
      SUM(cost_usd) recorded_cost
      FROM model_runs GROUP BY stage,model ORDER BY stage
    """)]
    scenes = [dict(r) for r in db.execute("SELECT * FROM v_scene_history ORDER BY 1")]
    asset_types = [dict(r) for r in db.execute("""
      SELECT file_type,COUNT(*) total,
      SUM(CASE WHEN exists_on_disk=1 THEN 1 ELSE 0 END) present
      FROM assets GROUP BY file_type ORDER BY total DESC
    """)]
    recent = [dict(r) for r in db.execute("""
      SELECT timestamp,stage,scene_id,status,
      ROUND(latency_seconds,2) latency_seconds,error
      FROM model_runs ORDER BY timestamp DESC LIMIT 12
    """)]
    db.close()

    cards_data = [
      ("Storyboard scenes", shots, "Structured story units", "▤", "purple"),
      ("Recorded AI runs", runs, "Logged model-run records", "◈", "cyan"),
      ("Successful runs", success, f"{rate}% recorded success rate", "✓", "green"),
      ("Failed runs", failed, "Failures retained for audit", "!", "red"),
      ("Verified assets", f"{present}/{assets}", f"{missing} missing on disk", "▧", "cyan"),
      ("Feedback records", feedback, f"{real_feedback} non-test · {tests} test", "◎", "gold")
    ]
    cards = "".join(
      f'<article class="metric card"><div class="line"><span>{label}</span><span class="bubble {tone}">{icon}</span></div><strong>{value}</strong><small>{note}</small></article>'
      for label,value,note,icon,tone in cards_data
    )

    model_cards = ""
    for m in models:
        pct = round(m["successful"] / m["total_runs"] * 100, 1) if m["total_runs"] else 0
        model_cards += f"""
        <article class="model card">
          <div class="line"><span class="tag">{esc(m['stage'].replace('_',' '))}</span><span class="status">{pct}% success</span></div>
          <h3>{esc(m['model'])}</h3><div class="bar"><i style="width:{pct}%"></i></div>
          <div class="muted tiny">{m['successful']} successful · {m['failed']} failed · {esc(m['avg_latency'])} sec avg.</div>
        </article>"""

    model_table = make_table(
      ["Stage","Model","Runs","Successful","Failed","Avg. latency (sec)","Recorded cost"],
      [[m["stage"],m["model"],m["total_runs"],m["successful"],m["failed"],m["avg_latency"],
        f'${m["recorded_cost"]:.4f}' if m["recorded_cost"] is not None else "Not recorded"] for m in models],
      "modelTable", True)
    scene_keys = list(scenes[0].keys()) if scenes else ["Scene history"]
    scene_table = make_table(scene_keys, [[r.get(k) for k in scene_keys] for r in scenes], "sceneTable", True)
    asset_table = make_table(["File type","Registered","Present on disk"],
      [[r["file_type"],r["total"],r["present"]] for r in asset_types],"assetTable")
    recent_table = make_table(["Timestamp","Stage","Scene","Status","Latency (sec)","Error"],
      [[r["timestamp"],r["stage"],r["scene_id"],r["status"],r["latency_seconds"],r["error"]] for r in recent],
      "recentTable", True)
    cost_values = [m["recorded_cost"] for m in models if m["recorded_cost"] is not None]
    cost_text = f'${sum(cost_values):.4f}' if cost_values else "Not recorded"
    asset_breakdown = "".join(
      f'<div class="assetrow"><span>{esc(r["file_type"]).upper()}</span><b>{r["present"]} / {r["total"]}</b></div>'
      for r in asset_types
    )
    verify_pct = (present / assets * 100) if assets else 0

    page = f"""
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lalibela | AI Production Intelligence</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{{--bg:#f2f4fa;--surface:#fff;--surface2:#f8f9fd;--ink:#19233d;--muted:#7b849c;--line:#e6e9f2;--navy:#111a31;--purple:#7968f5;--cyan:#30bdcc;--green:#159b78;--red:#df626e;--shadow:0 9px 28px #25335a0d}}
[data-theme=dark]{{--bg:#0e1527;--surface:#172139;--surface2:#202c46;--ink:#edf1ff;--muted:#a0abc4;--line:#2b3853;--navy:#080f20;--shadow:0 9px 28px #0003}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px 'DM Sans',sans-serif;line-height:1.6}}button,input{{font:inherit}}
.layout{{display:grid;grid-template-columns:225px 1fr;min-height:100vh}}aside{{background:var(--navy);color:white;padding:25px 17px;position:sticky;top:0;height:100vh}}
.brand{{display:flex;align-items:center;gap:10px;padding:0 8px 25px;border-bottom:1px solid #ffffff20}}.logo{{width:37px;height:37px;border-radius:12px;background:linear-gradient(135deg,#8b7cff,#31c5d1);display:grid;place-items:center;font:800 19px Manrope}}.brand b{{font:800 14px Manrope;display:block}}.brand small{{font-size:9px;color:#9da9c4;letter-spacing:1px;text-transform:uppercase}}
.navtitle{{font-size:10px;color:#74819e;letter-spacing:1.6px;text-transform:uppercase;padding:26px 10px 8px}}nav a{{display:block;padding:11px;border-radius:9px;color:#b5bfd4;text-decoration:none;font-size:13px;margin:3px 0}}nav a:hover,nav a.active{{background:#ffffff18;color:#fff}}nav a span{{display:inline-block;width:25px;color:#a99eff}}
.aside-note{{position:absolute;bottom:20px;left:17px;right:17px;border:1px solid #ffffff25;border-radius:11px;padding:12px;color:#aeb9d0;font-size:10px}}.aside-note b{{display:block;color:#fff;font-size:11px}}
main{{min-width:0;padding:0 30px 42px}}.top{{height:67px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);gap:10px}}.crumb{{font-size:11px;color:var(--muted)}}.crumb b{{color:var(--ink)}}.actions{{display:flex;gap:8px}}button{{border:1px solid var(--line);border-radius:9px;padding:9px 13px;background:var(--surface);color:var(--ink);font-size:11px}}button.primary{{background:var(--navy);color:white;border-color:var(--navy)}}
.hero{{margin:23px 0;padding:27px 29px;border-radius:17px;color:#fff;background:radial-gradient(circle at 85% 15%,#45cad34d,transparent 28%),linear-gradient(115deg,#141e3b,#322c69 70%,#5047a1);overflow:hidden}}.eyebrow{{font-size:10px;text-transform:uppercase;letter-spacing:1.6px;color:#bcb5ff;font-weight:700}}h1{{font:800 clamp(29px,3.5vw,39px) Manrope;margin:9px 0;letter-spacing:-1.1px}}.hero p{{font-size:12px;color:#d6dcf1;max-width:700px;margin:0}}.hero-foot{{display:flex;gap:18px;flex-wrap:wrap;margin-top:17px;color:#e2e7f7;font-size:10px}}.hero-foot span:before{{content:'●';color:#50d4c1;margin-right:7px}}
section{{margin:27px 0;scroll-margin-top:20px}}.secthead{{display:flex;justify-content:space-between;align-items:end;margin-bottom:13px;gap:10px}}h2{{font:800 19px Manrope;margin:0;color:var(--purple);letter-spacing:-.25px}}.sub{{font-size:12px;color:var(--muted);margin-top:4px}}.tag{{font-size:9px;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);font-weight:700}}.card,.panel{{background:var(--surface);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}}
.metrics{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.metric{{padding:15px 17px}}.line{{display:flex;justify-content:space-between;align-items:center;gap:8px}}.metric .line{{color:var(--muted);font-size:12px;font-weight:600}}.bubble{{width:29px;height:29px;border-radius:9px;display:grid;place-items:center;font-weight:700}}.purple{{background:#efedff;color:#7667ed}}.cyan{{background:#e7f8fa;color:#168e9d}}.green{{background:#e6f7f1;color:#12845f}}.red{{background:#fff0f1;color:#cf5260}}.gold{{background:#fff5e7;color:#ae792b}}.metric strong{{display:block;font:800 34px Manrope;margin:9px 0 1px;letter-spacing:-1.2px;background:linear-gradient(100deg,var(--purple),var(--cyan));-webkit-background-clip:text;background-clip:text;color:transparent}}.metric small{{color:var(--muted);font-size:11px}}
.modelgrid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.model{{padding:14px;min-width:0}}.status{{font-size:10px;padding:5px 8px;border-radius:20px;color:var(--green);background:#159b7818;font-weight:700}}.model h3{{font-size:13px;line-height:1.5;color:var(--ink);overflow-wrap:anywhere;min-height:40px;margin:14px 0}}.bar{{height:7px;background:var(--surface2);border-radius:20px;overflow:hidden}}.bar i{{height:100%;display:block;background:linear-gradient(90deg,var(--purple),var(--cyan));border-radius:20px}}.muted{{color:var(--muted)}}.tiny{{font-size:11px;margin-top:11px}}
.twocol{{display:grid;grid-template-columns:.75fr 1.25fr;gap:12px;margin-top:12px}}.panel{{padding:16px;min-width:0}}.panel h3{{font:800 14px Manrope;color:var(--cyan);margin:0 0 14px}}.ring{{width:130px;height:130px;border-radius:50%;margin:6px auto 12px;background:conic-gradient(var(--green) 0 {rate}%,var(--red) {rate}% 100%);display:grid;place-items:center;position:relative}}.ring:before{{content:'';position:absolute;inset:12px;background:var(--surface);border-radius:50%}}.ring div{{position:relative;text-align:center}}.ring b{{font:800 24px Manrope;display:block}}.ring small{{font-size:9px;color:var(--muted)}}.legend{{display:flex;justify-content:center;gap:14px;color:var(--muted);font-size:9px}}.dot{{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;background:var(--green)}}.dot.fail{{background:var(--red)}}
.search{{display:block;margin:0 0 8px auto;width:min(240px,100%);padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:var(--surface);color:var(--ink);font-size:10px;outline:none}}.search:focus{{border-color:var(--purple);box-shadow:0 0 0 3px #7968f51c}}.tablebox{{overflow:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}}table{{border-collapse:collapse;width:100%;min-width:620px;font-size:12px}}th,td{{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}}th{{background:var(--surface2);color:var(--purple);font-size:10px;text-transform:uppercase;letter-spacing:.7px;white-space:nowrap}}td{{max-width:350px;overflow-wrap:anywhere}}tbody tr:hover{{background:var(--surface2)}}tr:last-child td{{border:0}}
.assetgrid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.assetcount{{font:800 34px Manrope;color:var(--purple)}}.assetcount small{{font:500 10px 'DM Sans';color:var(--muted)}}.assetrow{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--line);font-size:12px}}.assetrow:last-child{{border:0}}.note{{padding:17px 19px;font-size:12px;border:1px solid #7968f533;border-left:3px solid var(--purple);border-radius:10px;background:#7968f50b;color:var(--muted);font-size:10px}}.note b{{color:var(--ink)}}footer{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:15px;margin-top:30px;color:var(--muted);font-size:9px}}
@media(max-width:1000px){{.layout{{grid-template-columns:180px 1fr}}main{{padding:0 18px 35px}}.modelgrid{{grid-template-columns:1fr}}.twocol{{grid-template-columns:1fr}}}}
@media(max-width:680px){{.layout{{display:block}}aside{{height:auto;position:relative;padding:13px}}.brand{{padding-bottom:10px}}.navtitle,.aside-note{{display:none}}nav{{display:flex;overflow:auto;gap:4px;margin-top:10px}}nav a{{white-space:nowrap;padding:8px}}main{{padding:0 12px 25px}}.top{{height:55px}}.metrics{{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.metric{{padding:12px}}.metric strong{{font-size:23px}}.hero{{padding:20px}}.assetgrid{{grid-template-columns:1fr}}}}
@media(max-width:390px){{.metrics{{grid-template-columns:1fr}}}}
@media print{{aside,.actions,.search{{display:none!important}}.layout{{display:block}}main{{padding:0}}body{{background:white}}.card,.panel{{box-shadow:none;break-inside:avoid}}}}
</style></head><body>
<div class="layout"><aside><div class="brand"><div class="logo">L</div><div><b>Lalibela AI</b><small>Production intelligence</small></div></div>
<div class="navtitle">Workspace</div><nav>
<a class="active" href="#overview"><span>▦</span>Overview</a><a href="#models"><span>◈</span>Model performance</a><a href="#scenes"><span>▤</span>Scene history</a><a href="#assets"><span>▧</span>Asset inventory</a><a href="#runs"><span>◷</span>Run records</a><a href="#integrity"><span>✓</span>Data integrity</a>
</nav><div class="aside-note"><b>Evidence-backed analytics</b>Metrics are generated from your local SQLite production database.</div></aside>
<main><div class="top"><div class="crumb">Projects / <b>Lalibela: A Story Carved in Stone</b></div><div class="actions"><button id="theme">◐ Theme</button><button class="primary" onclick="window.print()">⇩ Export / Print</button></div></div>
<header class="hero" id="overview"><div class="eyebrow">AI engineering · Production data · Observability</div><h1>AI Production Intelligence</h1><p>A database-backed view of storyboard structure, model execution, generation performance, production assets and audience-feedback records.</p><div class="hero-foot"><span>SQLite analytics</span><span>Python pipeline</span><span>Asset verification</span></div></header>
<section><div class="secthead"><div><h2>Production overview</h2><div class="sub">A snapshot of recorded production activity</div></div><span class="status">Database connected</span></div><div class="metrics">{cards}</div></section>
<section id="models"><div class="secthead"><div><h2>Model execution performance</h2><div class="sub">Success rates and average successful-run latency by stage</div></div></div><div class="modelgrid">{model_cards}</div><div class="twocol"><div class="panel"><h3>Run outcomes</h3><div class="ring"><div><b>{rate}%</b><small>success rate</small></div></div><div class="legend"><span><i class="dot"></i>{success} successful</span><span><i class="dot fail"></i>{failed} failed</span></div></div><div class="panel"><h3>Model performance details</h3>{model_table}</div></div></section>
<section id="scenes"><div class="secthead"><div><h2>Scene generation history</h2><div class="sub">Attempts, successes, failures and successful generation time</div></div></div>{scene_table}</section>
<section id="assets"><div class="secthead"><div><h2>Production asset inventory</h2><div class="sub">File registration and on-disk verification</div></div></div><div class="assetgrid"><div class="panel"><div class="eyebrow">Verified files</div><div class="assetcount">{present}<small> / {assets} registered</small></div><div class="bar" style="margin:10px 0"><i style="width:{verify_pct:.1f}%"></i></div><div class="sub">{missing} missing · {verify_pct:.1f}% verified</div></div><div class="panel"><h3>Files by type</h3>{asset_breakdown}</div></div><div style="margin-top:12px">{asset_table}</div></section>
<section id="runs"><div class="secthead"><div><h2>Recent model-run records</h2><div class="sub">Latest 12 entries from the execution log</div></div></div>{recent_table}</section>
<section id="integrity"><div class="secthead"><div><h2>Data integrity and reporting notes</h2><div class="sub">Important interpretation safeguards</div></div></div><div class="note"><b>Cost transparency:</b> {esc(cost_text)} in recorded model costs. Missing cost data does not mean an operation was free.<br><br><b>Feedback distinction:</b> {real_feedback} non-test feedback record(s) and {tests} test record(s). Test records are not counted as audience participants.<br><br><b>Asset verification:</b> {present} of {assets} registered files are present on disk; {missing} are missing.</div></section>
<footer><span>Generated from outputs/ai_production.db · Lalibela: A Story Carved in Stone</span><span>Refresh by rerunning create_dashboard.py</span></footer></main></div>
<div id="toast" class="toast">Theme updated</div>
<script>
document.getElementById('theme').addEventListener('click',()=>{{const root=document.documentElement;root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';const toast=document.getElementById('toast');toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1200)}});
document.querySelectorAll('.search').forEach(input=>input.addEventListener('input',()=>{{const q=input.value.toLowerCase();document.querySelectorAll('#'+input.dataset.target+' tbody tr').forEach(row=>row.style.display=row.innerText.toLowerCase().includes(q)?'':'none')}}));
const links=[...document.querySelectorAll('nav a')],sections=links.map(a=>document.querySelector(a.getAttribute('href')));window.addEventListener('scroll',()=>{{let active=sections[0];sections.forEach(s=>{{if(s.getBoundingClientRect().top<150)active=s}});links.forEach(a=>a.classList.toggle('active',a.hash==='#'+active.id))}},{{passive:true}});
</script></body></html>"""

    OUT.write_text(page, encoding="utf-8")
    print("Modern interactive dashboard created:", OUT)
    print("Open with: start outputs/ai_production_dashboard.html")

if __name__ == "__main__":
    main()
