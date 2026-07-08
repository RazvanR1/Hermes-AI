#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/5] Backup operator_v8.py..."
mkdir -p .hermes-backups
cp backend/operator_v8.py ".hermes-backups/operator_v8.py.alpha5-3-1.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[2/5] Validate imports..."
PYTHONPATH="$PROJECT_DIR/backend" python3 - <<'PY'
from operator_v8 import operator_chat
r = operator_chat("repornește VM 111", source="install-test", user="installer")
step = r["mission"]["steps"][0]
print("action:", step["action"])
print("status:", r["mission"]["status"])
assert step["action"] == "proxmox.vm.reboot"
assert r["mission"]["status"] == "waiting_confirmation"
PY

echo "[3/5] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[4/5] Test health..."
curl -fsS http://127.0.0.1:8088/operator/v8/health
echo

echo "[5/5] Done."
