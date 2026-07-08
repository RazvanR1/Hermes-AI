#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/7] Git status before install..."
git status --short || true

echo "[2/7] Backup server.py..."
mkdir -p .hermes-backups
cp backend/api/server.py ".hermes-backups/server.py.alpha5-core.$(date +%Y%m%d-%H%M%S).bak"

echo "[3/7] Patch backend/api/server.py..."
python3 - <<'PY'
from pathlib import Path

p = Path("backend/api/server.py")
text = p.read_text()

if "from api import execution_v8" not in text:
    lines = text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("from api import") or line.startswith("import "):
            insert_at = i + 1
    lines.insert(insert_at, "from api import execution_v8")
    text = "\n".join(lines) + "\n"

if "app.include_router(execution_v8.router)" not in text:
    marker = "app.include_router(approval_v8.router)"
    if marker in text:
        text = text.replace(marker, marker + "\napp.include_router(execution_v8.router)", 1)
    else:
        text += "\napp.include_router(execution_v8.router)\n"

if 'app.include_router(execution_v8.router, prefix="/api/v1")' not in text:
    marker = 'app.include_router(approval_v8.router, prefix="/api/v1")'
    if marker in text:
        text = text.replace(marker, marker + '\napp.include_router(execution_v8.router, prefix="/api/v1")', 1)
    else:
        text += '\napp.include_router(execution_v8.router, prefix="/api/v1")\n'

p.write_text(text)
PY

echo "[4/7] Validate imports..."
PYTHONPATH="$PROJECT_DIR/backend" python3 - <<'PY'
from api import execution_v8
from actions_v8_registry import list_actions
print("imports ok")
print(list_actions())
PY

echo "[5/7] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[6/7] Test API..."
curl -fsS http://127.0.0.1:8088/execution/v8/health
echo
curl -fsS http://127.0.0.1:8088/execution/v8/actions
echo

echo "[7/7] Done."
