#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST="$(ls -1t .hermes-backups/event_bus_v8.py.fix1.*.bak 2>/dev/null | head -1 || true)"
if [ -z "$LAST" ]; then
  echo "No fix1 backup found."
  exit 1
fi

cp "$LAST" backend/event_bus_v8.py
chown -R hermes:hermes backend/data || true

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback Events Core Fix1 done."
