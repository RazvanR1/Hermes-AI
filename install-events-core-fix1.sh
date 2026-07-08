#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/5] Backup event_bus_v8.py..."
mkdir -p .hermes-backups
cp backend/event_bus_v8.py ".hermes-backups/event_bus_v8.py.fix1.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[2/5] Ensure events store and permissions..."
mkdir -p backend/data
touch backend/data/events_v8.json
if [ ! -s backend/data/events_v8.json ]; then
  echo "[]" > backend/data/events_v8.json
fi
chown -R hermes:hermes backend/data
chmod 0755 backend/data
chmod 0644 backend/data/events_v8.json

echo "[3/5] Validate write as hermes..."
su - hermes -c "PYTHONPATH=$PROJECT_DIR/backend python3 - <<'PY'
from event_bus_v8 import emit_event, load_events
e = emit_event('FIX1_WRITE_TEST', message='write test from hermes user', source='fix1')
print(e['event_id'])
print(len(load_events(limit=10)))
PY"

echo "[4/5] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[5/5] Test health..."
curl -fsS http://127.0.0.1:8088/events/v8/health
echo
echo "Done."
