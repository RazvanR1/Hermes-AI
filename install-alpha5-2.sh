#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/7] Git status..."
git status --short || true

echo "[2/7] Backup changed files..."
mkdir -p .hermes-backups
cp backend/actions_v8_runner.py ".hermes-backups/actions_v8_runner.py.alpha5-2.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true
cp backend/api/execution_v8.py ".hermes-backups/execution_v8.py.alpha5-2.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[3/7] Validate Proxmox env/client..."
PYTHONPATH="$PROJECT_DIR/backend" python3 - <<'PY'
from actions_v8_registry import list_actions
import actions_v8_proxmox
print("proxmox module import ok")
print([k for k in list_actions().keys() if k.startswith("proxmox.")])
PY

echo "[4/7] Validate API imports..."
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

echo "[6/7] Test health/actions..."
curl -fsS http://127.0.0.1:8088/execution/v8/health
echo
curl -fsS http://127.0.0.1:8088/execution/v8/actions
echo

echo "[7/7] Done."
