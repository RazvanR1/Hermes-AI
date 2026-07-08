#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/6] Git status before install..."
git status --short

echo "[2/6] Backup changed files..."
mkdir -p .hermes-backups
cp backend/api/mission_v8.py ".hermes-backups/mission_v8.py.alpha3.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[3/6] Ensure data dir..."
mkdir -p backend/data
chown -R hermes:hermes backend/data || true

echo "[4/6] Validate imports..."
PYTHONPATH=/home/hermes/Hermes/backend python3 - <<'PY'
import mission_store_v8
import action_runner_v8
import mission_runner_v8
from api import mission_v8
print("imports ok")
PY

echo "[5/6] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[6/6] Test Alpha 3..."
curl -fsS http://127.0.0.1:8088/mission/v8/health
echo
echo "Done."
