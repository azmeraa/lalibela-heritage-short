import html
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "outputs" / "ai_production.db"
OUT = ROOT / "outputs" / "ai_production_dashboard.html"


def esc(value):
    return html.escape(str(value if value is not None else "—"))


def table(headers, rows):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{esc(v)}</td>" for v in row) + "</tr>"
    if not rows:
        body = f'<tr><td colspan="{len(headers)}">No records available</td></tr>'
    return f"<div class='table-wrap'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def main():
    if not DB.exists():
        raise SystemExit(f"Database not found: {DB}")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    def scalar(sql):
        return conn.execute(sql).fetchone()[0]

    shots = scalar("SELECT COUNT(*) FROM shots")
    runs = scalar("SELECT COUNT(*) FROM model_runs")
    successes = scalar("SELECT COUNT(*) FROM model_runs WHERE status='success'")
    failures = scalar("SELECT COUNT(*) FROM model_runs WHERE status='failed'")
    assets = scalar("SELECT COUNT(*) FROM assets")
    existing = scalar("SELECT COUNT(*) FROM assets WHERE exists_on_disk=1")
    feedback = scalar("SELECT COUNT(*) FROM audience_feedback")
    test_feedback = scalar(
        "SELECT COUNT(*) FROM audience_feedback WHERE is_test_record=1"
    )
    actual_feedback = feedback - test_feedback

    success_rate = (successes / runs * 100) if runs else 0
    missing = assets - existing

    model_rows = conn.execute("""
        SELECT stage, model,
               COUNT(*) AS total_runs,
               SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) AS successful,
               SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed,
               ROUND(AVG(CASE WHEN status='success'
                              THEN latency_seconds END), 2) AS avg_latency,
               SUM(cost_usd) AS recorded_cost
        FROM model_runs
        GROUP BY stage, model
        ORDER BY stage
    """).fetchall()

    model_table = table(
        ["Stage", "Model", "Runs", "Successful", "Failed",
         "Avg. success latency (sec)", "Recorded cost (USD)"],
        [[r["stage"], r["model"], r["total_runs"], r["successful"],
          r["failed"], r["avg_latency"],
          f'{r["recorded_cost"]:.4f}' if r["recorded_cost"] is not None else "Not recorded"]
         for r in model_rows]
    )

    scene_rows = conn.execute("""
        SELECT * FROM v_scene_history ORDER BY 1
    """).fetchall()
    scene_headers = list(scene_rows[0].keys()) if scene_rows else [
        "Scene history"
    ]
    scene_values = [[r[h] for h in scene_headers] for r in scene_rows]
    scene_table = table(scene_headers, scene_values)

    asset_rows = conn.execute("""
        SELECT file_type, COUNT(*) AS total,
               SUM(CASE WHEN exists_on_disk=1 THEN 1 ELSE 0 END) AS present
        FROM assets
        GROUP BY file_type
        ORDER BY total DESC
    """).fetchall()
    asset_table = table(
        ["File type", "Registered", "Present on disk"],
        [[r["file_type"], r["total"], r["present"]] for r in asset_rows]
    )

    recent_rows = conn.execute("""
        SELECT timestamp, stage, scene_id, status,
               ROUND(latency_seconds, 2) AS latency_seconds, error
        FROM model_runs
        ORDER BY timestamp DESC
        LIMIT 8
    """).fetchall()
    recent_table = table(
        ["Timestamp", "Stage", "Scene", "Status", "Latency (sec)", "Error"],
        [[r["timestamp"], r["stage"], r["scene_id"], r["status"],
          r["latency_seconds"], r["error"]] for r in recent_rows]
    )

    cost_values = [r["recorded_cost"] for r in model_rows
                   if r["recorded_cost"] is not None]
    cost_text = (
        f"${sum(cost_values):.4f}"
        if cost_values else "Not recorded"
    )

    conn.close()

    cards = [
        ("Storyboard scenes", shots, "Structured story units"),
        ("Recorded AI runs", runs, "All logged model-run records"),
        ("Successful runs", successes, f"{success_rate:.1f}% success rate"),
        ("Failed runs", failures, "Failures retained for audit"),
        ("Verified assets", f"{existing}/{assets}", f"{missing} missing"),
        ("Audience records", feedback, f"{actual_feedback} non-test · {test_feedback} test"),
    ]
    card_html = "".join(
        f"<article class='metric'><span>{esc(label)}</span>"
        f"<strong>{esc(value)}</strong><small>{esc(note)}</small></article>"
        for label, value, note in cards
    )

    stage_html = ""
    for r in model_rows:
        total = r["total_runs"] or 0
        pct = (r["successful"] / total * 100) if total else 0
        stage_html += f"""
        <div class="stage">
          <div class="stage-label"><strong>{esc(r['stage'])}</strong>
          <span>{r['successful']}/{total} successful · {pct:.0f}%</span></div>
          <div class="bar"><div style="width:{pct:.1f}%"></div></div>
        </div>"""

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lalibela | AI Production Intelligence</title>
<style>
:root {{
  --ink:#172033; --muted:#687386; --line:#e5e9f0;
  --paper:#f5f7fb; --panel:#fff; --accent:#6757d9;
  --green:#16845b; --red:#c14e4e;
}}
* {{box-sizing:border-box}}
body {{margin:0;background:var(--paper);color:var(--ink);
  font-family:Inter,"Segoe UI",Arial,sans-serif;line-height:1.5}}
header {{background:#172033;color:#fff;padding:34px max(5vw,22px)}}
header .eyebrow {{color:#b9b3ff;text-transform:uppercase;
  letter-spacing:2px;font-size:11px;font-weight:700}}
h1 {{font-size:clamp(25px,4vw,38px);margin:8px 0}}
header p {{color:#d1d7e3;margin:0;max-width:760px}}
main {{max-width:1250px;margin:30px auto;padding:0 22px 50px}}
.section {{margin:30px 0}}
.section h2 {{font-size:19px;margin:0 0 14px}}
.metrics {{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}
.metric,.panel {{background:var(--panel);border:1px solid var(--line);
  border-radius:13px;padding:19px}}
.metric span,.metric small {{display:block;color:var(--muted)}}
.metric span {{font-size:13px}}
.metric strong {{display:block;font-size:29px;margin:7px 0}}
.metric small {{font-size:12px}}
.panel {{margin-bottom:14px}}
.stage {{margin:15px 0}}
.stage-label {{display:flex;justify-content:space-between;gap:12px;
  font-size:13px;margin-bottom:7px}}
.stage-label span {{color:var(--muted)}}
.bar {{height:9px;background:#edf0f5;border-radius:20px;overflow:hidden}}
.bar div {{height:100%;background:var(--accent);border-radius:20px}}
.table-wrap {{overflow-x:auto;background:white;border:1px solid var(--line);
  border-radius:12px}}
table {{width:100%;border-collapse:collapse;font-size:12px;min-width:650px}}
th,td {{padding:11px 13px;text-align:left;border-bottom:1px solid var(--line);
  vertical-align:top}}
th {{background:#f7f8fc;color:#4b5568;font-weight:700;white-space:nowrap}}
tr:last-child td {{border-bottom:0}}
.note {{border-left:3px solid var(--accent);padding:13px 16px;
  background:#fff;border-radius:0 9px 9px 0;color:#4d586b;font-size:13px}}
footer {{color:var(--muted);font-size:12px;margin-top:32px}}
@media(max-width:760px) {{
  .metrics {{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .stage-label {{flex-direction:column;gap:2px}}
}}
@media(max-width:430px) {{
  .metrics {{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<header>
  <div class="eyebrow">AI Engineering · Production Data · Observability</div>
  <h1>Lalibela — AI Production Intelligence</h1>
  <p>A database-backed view of storyboard structure, model execution,
  generation performance, production assets and audience-feedback records.</p>
</header>
<main>
  <section class="section">
    <h2>Production overview</h2>
    <div class="metrics">{card_html}</div>
  </section>

  <section class="section">
    <h2>Model execution performance</h2>
    <div class="panel">
      {stage_html}
    </div>
    {model_table}
  </section>

  <section class="section">
    <h2>Scene generation history</h2>
    {scene_table}
  </section>

  <section class="section">
    <h2>Production asset inventory</h2>
    {asset_table}
    <p class="note">Asset verification: {existing} of {assets} registered
    files are present on disk. Missing assets: {missing}.</p>
  </section>

  <section class="section">
    <h2>Recent model-run records</h2>
    {recent_table}
  </section>

  <section class="section">
    <h2>Data integrity and reporting notes</h2>
    <div class="note">
      <strong>Cost transparency:</strong> {esc(cost_text)} in recorded model
      costs. A missing cost value means it was not captured; it does not mean
      the operation was free.<br><br>
      <strong>Feedback distinction:</strong> {actual_feedback} non-test
      feedback record(s) and {test_feedback} test record(s) are stored in
      this database. Test records are not counted as audience participants.
    </div>
  </section>

  <footer>
    Generated from outputs/ai_production.db · Lalibela: A Story Carved in Stone
    · Standalone dashboard; refresh by rerunning create_dashboard.py
  </footer>
</main>
</body>
</html>"""

    OUT.write_text(document, encoding="utf-8")
    print("Dashboard created:", OUT)
    print("Open it with: start outputs/ai_production_dashboard.html")


if __name__ == "__main__":
    main()
