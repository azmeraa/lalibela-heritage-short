import csv
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "outputs" / "ai_production.db"

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def relative_path(value):
    return str(value).replace("\\", "/").lstrip("./")

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS shots (
        shot_id TEXT PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(project_id),
        title TEXT,
        start_seconds REAL,
        end_seconds REAL,
        duration_seconds REAL,
        location_visual TEXT,
        image_prompt TEXT,
        motion_prompt TEXT,
        narration_language TEXT,
        narration_text TEXT,
        subtitle_language TEXT,
        subtitle_text TEXT
    );

    CREATE TABLE IF NOT EXISTS model_runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL REFERENCES projects(project_id),
        timestamp TEXT,
        stage TEXT,
        model TEXT,
        scene_id TEXT,
        status TEXT,
        latency_seconds REAL,
        cost_usd REAL,
        attempt INTEGER,
        output_file TEXT,
        error TEXT,
        parameters_json TEXT,
        raw_json TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS assets (
        asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL REFERENCES projects(project_id),
        shot_id TEXT REFERENCES shots(shot_id),
        model_run_id INTEGER REFERENCES model_runs(run_id),
        file_path TEXT NOT NULL UNIQUE,
        file_type TEXT,
        file_size_bytes INTEGER,
        sha256 TEXT,
        exists_on_disk INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audience_feedback (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL REFERENCES projects(project_id),
        participant_code TEXT,
        film TEXT,
        submitted_at TEXT,
        is_test_record INTEGER NOT NULL DEFAULT 0,
        responses_json TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_runs_scene ON model_runs(scene_id);
    CREATE INDEX IF NOT EXISTS idx_runs_stage ON model_runs(stage);
    CREATE INDEX IF NOT EXISTS idx_runs_status ON model_runs(status);
    CREATE INDEX IF NOT EXISTS idx_assets_shot ON assets(shot_id);
    CREATE INDEX IF NOT EXISTS idx_feedback_participant
        ON audience_feedback(participant_code);

    DROP VIEW IF EXISTS v_model_performance;
    DROP VIEW IF EXISTS v_scene_history;

    CREATE VIEW v_model_performance AS
    SELECT
        stage,
        model,
        COUNT(*) AS total_attempts,
        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS successes,
        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failures,
        ROUND(AVG(CASE WHEN status = 'success'
                       THEN latency_seconds END), 2) AS avg_success_latency,
        ROUND(SUM(cost_usd), 4) AS known_cost_usd
    FROM model_runs
    GROUP BY stage, model;

    CREATE VIEW v_scene_history AS
    SELECT
        s.shot_id,
        s.title,
        COUNT(r.run_id) AS generation_attempts,
        SUM(CASE WHEN r.status = 'success' THEN 1 ELSE 0 END) AS successes,
        SUM(CASE WHEN r.status = 'failed' THEN 1 ELSE 0 END) AS failures,
        ROUND(SUM(CASE WHEN r.status = 'success'
                       THEN r.latency_seconds ELSE 0 END), 2)
            AS successful_generation_seconds
    FROM shots s
    LEFT JOIN model_runs r
        ON r.scene_id = s.shot_id
    GROUP BY s.shot_id, s.title;
    """)
    conn.commit()

def import_project(conn, data):
    project = data.get("project", {})
    if isinstance(project, dict):
        name = project.get("title") or project.get("name") or \
               "Lalibela: A Story Carved in Stone"
        description = json.dumps(project, ensure_ascii=False)
    else:
        name = str(project) if project else \
               "Lalibela: A Story Carved in Stone"
        description = str(project)

    conn.execute("""
        INSERT INTO projects(project_id, name, description)
        VALUES (1, ?, ?)
        ON CONFLICT(project_id) DO UPDATE SET
            name=excluded.name, description=excluded.description
    """, (name, description))

    for shot in data.get("shots", []):
        narration = shot.get("narration") or {}
        subtitle = shot.get("subtitle") or {}
        conn.execute("""
            INSERT INTO shots VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(shot_id) DO UPDATE SET
                title=excluded.title,
                start_seconds=excluded.start_seconds,
                end_seconds=excluded.end_seconds,
                duration_seconds=excluded.duration_seconds,
                location_visual=excluded.location_visual,
                image_prompt=excluded.image_prompt,
                motion_prompt=excluded.motion_prompt,
                narration_language=excluded.narration_language,
                narration_text=excluded.narration_text,
                subtitle_language=excluded.subtitle_language,
                subtitle_text=excluded.subtitle_text
        """, (
            shot["shot_id"], shot.get("title"),
            shot.get("start_seconds"), shot.get("end_seconds"),
            shot.get("duration_seconds"), shot.get("location_visual"),
            shot.get("image_prompt"), shot.get("motion_prompt"),
            narration.get("language"), narration.get("text"),
            subtitle.get("language"), subtitle.get("text")
        ))
    conn.commit()

def import_runs(conn):
    path = ROOT / "logs" / "runs.jsonl"
    if not path.exists():
        raise FileNotFoundError(path)

    # Re-import safely: replace the imported run history as one transaction.
    conn.execute("DELETE FROM assets")
    conn.execute("DELETE FROM model_runs")

    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            scene = r.get("scene_id") or r.get("shot_id")
            cursor = conn.execute("""
                INSERT INTO model_runs (
                    project_id, timestamp, stage, model, scene_id,
                    status, latency_seconds, cost_usd, attempt,
                    output_file, error, parameters_json, raw_json
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r.get("timestamp"), r.get("stage"), r.get("model"),
                scene, r.get("status"), r.get("latency_seconds"),
                r.get("cost_usd"), r.get("attempt"),
                r.get("output_file") or r.get("output"),
                r.get("error"),
                json.dumps(r.get("parameters"), ensure_ascii=False),
                json.dumps(r, ensure_ascii=False)
            ))
            run_id = cursor.lastrowid
            output = r.get("output_file") or r.get("output")
            if output:
                register_asset(conn, output, scene, run_id)
    conn.commit()

def register_asset(conn, value, shot_id=None, run_id=None):
    clean = relative_path(value)
    path = ROOT / clean
    exists = path.is_file()
    suffix = path.suffix.lower().lstrip(".") or "unknown"
    size = path.stat().st_size if exists else None
    digest = sha256_file(path) if exists else None

    conn.execute("""
        INSERT INTO assets (
            project_id, shot_id, model_run_id, file_path,
            file_type, file_size_bytes, sha256, exists_on_disk
        ) VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
            shot_id=excluded.shot_id,
            model_run_id=excluded.model_run_id,
            file_type=excluded.file_type,
            file_size_bytes=excluded.file_size_bytes,
            sha256=excluded.sha256,
            exists_on_disk=excluded.exists_on_disk
    """, (shot_id, run_id, clean, suffix, size, digest, int(exists)))

def scan_assets(conn):
    folders = ["assets", "outputs"]
    for folder in folders:
        base = ROOT / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                rel = path.relative_to(ROOT).as_posix()
                if rel.endswith((".db", "-journal", "-wal", "-shm")):
                    continue
                register_asset(conn, rel)
    conn.commit()

def import_feedback(conn):
    path = ROOT / "outputs" / "audience_feedback.csv"
    if not path.exists():
        return

    conn.execute("DELETE FROM audience_feedback")
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            code = row.get("Participant Code", "")
            conn.execute("""
                INSERT INTO audience_feedback (
                    project_id, participant_code, film, submitted_at,
                    is_test_record, responses_json
                ) VALUES (1, ?, ?, ?, ?, ?)
            """, (
                code, row.get("Film"), row.get("Date and Time"),
                int(code.upper().startswith("TEST")),
                json.dumps(row, ensure_ascii=False)
            ))
    conn.commit()

def print_summary(conn):
    print("\n========== AI PRODUCTION DATABASE ==========")
    print("Database:", DB)
    queries = [
        ("Storyboard shots", "SELECT COUNT(*) FROM shots"),
        ("AI model attempts", "SELECT COUNT(*) FROM model_runs"),
        ("Successful runs", "SELECT COUNT(*) FROM model_runs WHERE status='success'"),
        ("Failed runs", "SELECT COUNT(*) FROM model_runs WHERE status='failed'"),
        ("Registered assets", "SELECT COUNT(*) FROM assets"),
        ("Assets found on disk", "SELECT COUNT(*) FROM assets WHERE exists_on_disk=1"),
        ("Feedback records", "SELECT COUNT(*) FROM audience_feedback"),
        ("Test feedback records", "SELECT COUNT(*) FROM audience_feedback WHERE is_test_record=1")
    ]
    for label, sql in queries:
        print(f"{label:25} {conn.execute(sql).fetchone()[0]}")

    print("\nMODEL PERFORMANCE")
    for row in conn.execute("""
        SELECT stage, model, total_attempts, successes, failures,
               avg_success_latency, known_cost_usd
        FROM v_model_performance ORDER BY stage
    """):
        print(row)

    print("\nSCENE GENERATION HISTORY")
    for row in conn.execute("""
        SELECT shot_id, title, generation_attempts, successes,
               failures, successful_generation_seconds
        FROM v_scene_history ORDER BY shot_id
    """):
        print(row)

def main():
    storyboard_path = ROOT / "storyboard.json"
    if not storyboard_path.exists():
        raise FileNotFoundError(storyboard_path)

    data = json.loads(storyboard_path.read_text(encoding="utf-8"))
    conn = connect()
    try:
        create_schema(conn)
        import_project(conn, data)
        import_runs(conn)
        scan_assets(conn)
        import_feedback(conn)
        print_summary(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
