import json
import os
import sqlite3
from datetime import datetime, timezone

DB = os.getenv("HERMES_TASK_DB", "/home/hermes/.hermes/homelab/tasks.db")

def _now():
    return datetime.now(timezone.utc).isoformat()

def _db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            plan_json TEXT,
            result_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    return conn

def create(task: str):
    from core import taskplanner
    plan = taskplanner.build(task)
    now = _now()

    conn = _db()
    cur = conn.execute(
        "INSERT INTO tasks(task,status,plan_json,result_json,created_at,updated_at) VALUES(?,?,?,?,?,?)",
        (task, "queued", json.dumps(plan, ensure_ascii=False), None, now, now),
    )
    conn.commit()
    return get(cur.lastrowid)

def get(task_id: int):
    conn = _db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not row:
        return None
    return _row(row)

def list_tasks(limit=20):
    conn = _db()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (int(limit),)).fetchall()
    return [_row(r) for r in rows]

def run(task_id: int, ctx=None):
    from core import taskruntime

    item = get(task_id)
    if not item:
        return {"ok": False, "error": "task not found", "id": task_id}

    _update(task_id, status="running")

    result = taskruntime.execute(item["task"], ctx=ctx)

    status = result.get("status", "completed")
    _update(task_id, status=status, result=result)

    return get(task_id)

def _update(task_id, status=None, result=None):
    conn = _db()
    fields = []
    values = []

    if status:
        fields.append("status=?")
        values.append(status)

    if result is not None:
        fields.append("result_json=?")
        values.append(json.dumps(result, ensure_ascii=False))

    fields.append("updated_at=?")
    values.append(_now())
    values.append(task_id)

    conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()

def _row(row):
    return {
        "id": row["id"],
        "task": row["task"],
        "status": row["status"],
        "plan": json.loads(row["plan_json"]) if row["plan_json"] else None,
        "result": json.loads(row["result_json"]) if row["result_json"] else None,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
