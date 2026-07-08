#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST="$(ls -1t .hermes-backups/server.py.events-core.*.bak 2>/dev/null | head -1 || true)"

if [ -z "$LAST" ]; then
  echo "No Events Core server.py backup found."
  exit 1
fi

cp "$LAST" backend/api/server.py

rm -f backend/event_bus_v8.py
rm -f backend/mission_events_v8.py
rm -f backend/api/events_v8.py

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback Events Core done."
