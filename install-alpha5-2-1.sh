#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/6] Backup Proxmox action file..."
mkdir -p .hermes-backups
cp backend/actions_v8_proxmox.py ".hermes-backups/actions_v8_proxmox.py.alpha5-2-1.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[2/6] Check /etc/default/hermes Proxmox env..."
if [ -f /etc/default/hermes ]; then
  grep -E "PROXMOX|PVE" /etc/default/hermes | sed -E 's/(SECRET|TOKEN).*/\\1=***hidden***/' || true
else
  echo "WARNING: /etc/default/hermes missing"
fi

echo "[3/6] Validate Python imports..."
set -a
[ -f /etc/default/hermes ] && . /etc/default/hermes
set +a

PYTHONPATH="$PROJECT_DIR/backend" python3 - <<'PY'
import actions_v8_proxmox
from actions_v8_registry import list_actions
print("imports ok")
print([k for k in list_actions().keys() if k.startswith("proxmox.")])
PY

echo "[4/6] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[5/6] Test health..."
curl -fsS http://127.0.0.1:8088/execution/v8/health
echo

echo "[6/6] Done."
