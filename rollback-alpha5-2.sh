#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST_RUNNER="$(ls -1t .hermes-backups/actions_v8_runner.py.alpha5-2.*.bak 2>/dev/null | head -1 || true)"
LAST_API="$(ls -1t .hermes-backups/execution_v8.py.alpha5-2.*.bak 2>/dev/null | head -1 || true)"

if [ -n "$LAST_RUNNER" ]; then cp "$LAST_RUNNER" backend/actions_v8_runner.py; fi
if [ -n "$LAST_API" ]; then cp "$LAST_API" backend/api/execution_v8.py; fi

rm -f backend/actions_v8_proxmox.py

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback Alpha 5.2 done."
