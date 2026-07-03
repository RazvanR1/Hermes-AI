import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("HOMELAB_HISTORY_DB", "/home/hermes/.hermes/homelab/history.db")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            mode TEXT,
            status TEXT,
            score INTEGER,
            critical_count INTEGER,
            warnings_count INTEGER,
            healthy_count INTEGER,
            today_count INTEGER,
            opnsense_status TEXT,
            opnsense_updates INTEGER,
            opnsense_needs_reboot INTEGER,
            payload TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_key TEXT NOT NULL UNIQUE,
            component TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'open'
        )
    """)
    _migrate(conn)
    conn.commit()
    return conn


def _migrate(conn):
    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(snapshots)").fetchall()
    }
    wanted = {
        "opnsense_status": "TEXT",
        "opnsense_updates": "INTEGER",
        "opnsense_needs_reboot": "INTEGER",
    }
    for name, typ in wanted.items():
        if name not in columns:
            conn.execute(f"ALTER TABLE snapshots ADD COLUMN {name} {typ}")


def record(report):
    conn = _connect()
    ts = datetime.now(timezone.utc).isoformat()

    opn = _extract_opnsense(report)

    conn.execute(
        """
        INSERT INTO snapshots (
            timestamp, mode, status, score,
            critical_count, warnings_count, healthy_count, today_count,
            opnsense_status, opnsense_updates, opnsense_needs_reboot,
            payload
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ts,
            report.get("mode"),
            report.get("status"),
            report.get("score"),
            len(report.get("critical", [])),
            len(report.get("warnings", [])),
            len(report.get("healthy", [])),
            len(report.get("today", [])),
            opn.get("status"),
            opn.get("updates_count"),
            1 if opn.get("needs_reboot") else 0,
            json.dumps(report, ensure_ascii=False),
        ),
    )

    _sync_events(conn, report, ts)

    conn.commit()
    conn.close()

    return {
        "recorded": True,
        "timestamp": ts,
        "db": DB_PATH,
        "opnsense": opn,
    }


def latest(limit=5):
    conn = _connect()
    rows = conn.execute(
        """
        SELECT id, timestamp, mode, status, score,
               critical_count, warnings_count, healthy_count, today_count,
               opnsense_status, opnsense_updates, opnsense_needs_reboot
        FROM snapshots
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def latest_payload():
    conn = _connect()
    row = conn.execute(
        "SELECT payload FROM snapshots ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["payload"])


def previous_payload():
    conn = _connect()
    row = conn.execute(
        "SELECT payload FROM snapshots ORDER BY id DESC LIMIT 1 OFFSET 1"
    ).fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["payload"])


def open_events():
    conn = _connect()
    rows = conn.execute(
        """
        SELECT event_key, component, severity, title, first_seen, last_seen, count, status
        FROM events
        WHERE status = 'open'
        ORDER BY severity, first_seen
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stats():
    conn = _connect()
    row = conn.execute(
        """
        SELECT
            COUNT(*) AS count,
            MIN(timestamp) AS first_seen,
            MAX(timestamp) AS last_seen,
            AVG(score) AS average_score,
            MIN(score) AS min_score,
            MAX(score) AS max_score
        FROM snapshots
        """
    ).fetchone()
    events_count = conn.execute(
        "SELECT COUNT(*) AS count FROM events WHERE status = 'open'"
    ).fetchone()["count"]
    conn.close()

    out = dict(row)
    out["open_events"] = events_count
    return out


def _extract_opnsense(report):
    opn = (
        report.get("raw", {})
        .get("dashboard", {})
        .get("data", {})
        .get("health", {})
        .get("opnsense", {})
    )

    if not isinstance(opn, dict):
        opn = {}

    return {
        "status": "ok" if opn.get("ok") else "error",
        "updates_count": opn.get("updates_count") or 0,
        "needs_reboot": bool(opn.get("needs_reboot") or opn.get("upgrade_needs_reboot")),
        "version": opn.get("product_version"),
        "repository": opn.get("repository"),
    }


def _sync_events(conn, report, ts):
    active = []

    for msg in report.get("critical", []) or []:
        text = str(msg)
        key = _event_key("critical", text)
        active.append(key)
        _upsert_event(conn, key, "homelab", "critical", text, ts)

    for msg in report.get("warnings", []) or []:
        text = str(msg)
        key = _event_key("warning", text)
        active.append(key)
        _upsert_event(conn, key, "homelab", "warning", text, ts)

    opn = _extract_opnsense(report)
    if opn.get("status") == "error":
        key = "opnsense_api_error"
        active.append(key)
        _upsert_event(conn, key, "opnsense", "warning", "OPNsense API check failed", ts)
    if opn.get("needs_reboot"):
        key = "opnsense_reboot_required"
        active.append(key)
        _upsert_event(conn, key, "opnsense", "warning", "OPNsense requires reboot", ts)

    # Close events that disappeared.
    if active:
        placeholders = ",".join("?" for _ in active)
        conn.execute(
            f"""
            UPDATE events
            SET status='closed', last_seen=?
            WHERE status='open' AND event_key NOT IN ({placeholders})
            """,
            [ts] + active,
        )
    else:
        conn.execute(
            "UPDATE events SET status='closed', last_seen=? WHERE status='open'",
            (ts,),
        )


def _upsert_event(conn, key, component, severity, title, ts):
    row = conn.execute(
        "SELECT id, count FROM events WHERE event_key=?",
        (key,),
    ).fetchone()

    if row:
        conn.execute(
            """
            UPDATE events
            SET last_seen=?, count=?, status='open', severity=?, title=?
            WHERE event_key=?
            """,
            (ts, row["count"] + 1, severity, title, key),
        )
    else:
        conn.execute(
            """
            INSERT INTO events (event_key, component, severity, title, first_seen, last_seen, count, status)
            VALUES (?, ?, ?, ?, ?, ?, 1, 'open')
            """,
            (key, component, severity, title, ts),
        )


def _event_key(kind, text):
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif keep and keep[-1] != "_":
            keep.append("_")
    slug = "".join(keep).strip("_")[:120]
    return f"{kind}_{slug}"
