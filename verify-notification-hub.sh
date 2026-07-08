#!/usr/bin/env bash
set -euo pipefail

cd /home/hermes/Hermes

echo "[1/3] Python imports"
PYTHONPATH=/home/hermes/Hermes/backend python3 - <<'PY'
from notifications.hub import notify

result = notify({
    "type": "VERIFY_NOTIFICATION_HUB",
    "level": "info",
    "mission_id": "verify",
    "message": "Notification Hub verify OK",
    "source": "verify",
})
print(result)
assert result["ok"] is True
PY

echo "[2/3] Compile"
python3 -m py_compile \
  backend/notifications/models.py \
  backend/notifications/hub.py \
  backend/notifications/registry.py \
  backend/notifications/connectors/telegram.py

echo "[3/3] Git status"
git status --short

echo "[verify] OK"
