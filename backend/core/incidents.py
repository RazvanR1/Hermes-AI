import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("HERMES_DB_PATH", "/home/hermes/.hermes/homelab/hermes.db")


def _now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_key TEXT NOT NULL UNIQUE,
            provider TEXT NOT NULL,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            closed_at TEXT,
            confidence INTEGER DEFAULT 80,
            recommendation TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    return conn


def make_key(provider, title):
    raw = f"{provider}:{title}".lower()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "_":
            out.append("_")
    return "".join(out).strip("_")[:160]


def open_incident(provider, title, severity="warning", recommendation=None, confidence=80, metadata=None):
    conn = connect()
    ts = _now()
    key = make_key(provider, title)
    payload = json.dumps(metadata or {}, ensure_ascii=False)

    row = conn.execute("SELECT id, count(*) OVER() AS n FROM incidents WHERE incident_key=?", (key,)).fetchone()
    if row:
        conn.execute("""
            UPDATE incidents
            SET status='open', last_seen=?, closed_at=NULL,
                severity=?, recommendation=?, confidence=?, metadata=?
            WHERE incident_key=?
        """, (ts, severity, recommendation, confidence, payload, key))
    else:
        conn.execute("""
            INSERT INTO incidents (
                incident_key, provider, title, severity, status,
                first_seen, last_seen, confidence, recommendation, metadata
            )
            VALUES (?, ?, ?, ?, 'open', ?, ?, ?, ?, ?)
        """, (key, provider, title, severity, ts, ts, confidence, recommendation, payload))

    conn.commit()
    row = conn.execute("SELECT * FROM incidents WHERE incident_key=?", (key,)).fetchone()
    conn.close()
    return _to_dict(row)


def close_incident(provider, title):
    conn = connect()
    ts = _now()
    key = make_key(provider, title)
    conn.execute("""
        UPDATE incidents
        SET status='closed', closed_at=?, last_seen=?
        WHERE incident_key=? AND status='open'
    """, (ts, ts, key))
    conn.commit()
    conn.close()
    return {"closed": True, "incident_key": key, "closed_at": ts}


def list_open():
    conn = connect()
    rows = conn.execute("""
        SELECT * FROM incidents
        WHERE status='open'
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 0
                WHEN 'warning' THEN 1
                WHEN 'info' THEN 2
                ELSE 3
            END,
            first_seen ASC
    """).fetchall()
    conn.close()
    return [_to_dict(r) for r in rows]


def list_closed(limit=20):
    conn = connect()
    rows = conn.execute("""
        SELECT * FROM incidents
        WHERE status='closed'
        ORDER BY closed_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [_to_dict(r) for r in rows]


def stats():
    conn = connect()
    total = conn.execute("SELECT COUNT(*) AS n FROM incidents").fetchone()["n"]
    open_count = conn.execute("SELECT COUNT(*) AS n FROM incidents WHERE status='open'").fetchone()["n"]
    critical = conn.execute("SELECT COUNT(*) AS n FROM incidents WHERE status='open' AND severity='critical'").fetchone()["n"]
    warning = conn.execute("SELECT COUNT(*) AS n FROM incidents WHERE status='open' AND severity='warning'").fetchone()["n"]
    conn.close()
    return {
        "total": total,
        "open": open_count,
        "critical_open": critical,
        "warning_open": warning,
        "db": DB_PATH,
    }


def sync_from_report(report):
    active_keys = set()

    for msg in report.get("critical", []) or []:
        row = open_incident(
            provider=_guess_provider(msg),
            title=str(msg),
            severity="critical",
            recommendation=_recommendation(msg),
            confidence=90,
            metadata={"source": "sysadmin_report"},
        )
        active_keys.add(row["incident_key"])

    for msg in report.get("warnings", []) or []:
        row = open_incident(
            provider=_guess_provider(msg),
            title=str(msg),
            severity="warning",
            recommendation=_recommendation(msg),
            confidence=80,
            metadata={"source": "sysadmin_report"},
        )
        active_keys.add(row["incident_key"])

    opn = _extract_opnsense(report)
    if opn:
        if opn.get("status") == "error":
            row = open_incident(
                provider="opnsense",
                title="OPNsense API check failed",
                severity="warning",
                recommendation="Verifică API key/secret și conectivitatea către 192.168.1.1.",
                confidence=90,
                metadata=opn,
            )
            active_keys.add(row["incident_key"])
        if opn.get("needs_reboot"):
            row = open_incident(
                provider="opnsense",
                title="OPNsense requires reboot",
                severity="warning",
                recommendation="Planifică reboot OPNsense într-o fereastră de mentenanță.",
                confidence=90,
                metadata=opn,
            )
            active_keys.add(row["incident_key"])

    _close_missing(active_keys)

    return {"open": list_open(), "stats": stats()}


def _close_missing(active_keys):
    conn = connect()
    rows = conn.execute("SELECT incident_key FROM incidents WHERE status='open'").fetchall()
    ts = _now()
    for row in rows:
        key = row["incident_key"]
        if key not in active_keys:
            conn.execute("UPDATE incidents SET status='closed', closed_at=?, last_seen=? WHERE incident_key=?", (ts, ts, key))
    conn.commit()
    conn.close()


def _to_dict(row):
    d = dict(row)
    try:
        d["metadata"] = json.loads(d.get("metadata") or "{}")
    except Exception:
        d["metadata"] = {}
    return d


def _guess_provider(msg):
    text = str(msg).lower()
    if any(x in text for x in ["truenas", "pool", "smart", "disk", "disc"]):
        return "truenas"
    if "docker" in text or "container" in text:
        return "docker"
    if "proxmox" in text or "debian" in text:
        return "proxmox"
    if "home assistant" in text:
        return "homeassistant"
    if "opnsense" in text or "gateway" in text or "wan" in text:
        return "opnsense"
    return "homelab"


def _recommendation(msg):
    text = str(msg).lower()
    if any(x in text for x in ["degraded", "smart", "removed"]):
        return "Rezolvă storage-ul înainte de reboot sau update-uri majore."
    if "proxmox" in text or "debian" in text:
        return "Aplică update-urile într-o fereastră de mentenanță, după ce storage-ul este stabil."
    if "home assistant" in text:
        return "Verifică update-urile în interfața Home Assistant."
    if "opnsense" in text:
        return "Verifică OPNsense și planifică mentenanța dacă este nevoie."
    return "Verifică detaliile incidentului."


def _extract_opnsense(report):
    inv = report.get("inventory", {}) or {}
    comp = inv.get("components", {}) if isinstance(inv, dict) else {}
    opn = comp.get("opnsense")
    return opn if isinstance(opn, dict) else None
