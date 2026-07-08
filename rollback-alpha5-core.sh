#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST_BACKUP="$(ls -1t .hermes-backups/server.py.alpha5-core.*.bak 2>/dev/null | head -1 || true)"

if [ -z "$LAST_BACKUP" ]; then
  echo "No Alpha 5 server.py backup found."
  exit 1
fi

echo "Restoring $LAST_BACKUP"
cp "$LAST_BACKUP" backend/api/server.py

echo "Removing Alpha 5 Core files"
rm -f backend/actions_v8_registry.py
rm -f backend/actions_v8_linux.py
rm -f backend/actions_v8_runner.py
rm -f backend/api/execution_v8.py

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback done."
