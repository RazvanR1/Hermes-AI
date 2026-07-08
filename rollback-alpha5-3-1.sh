#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST="$(ls -1t .hermes-backups/operator_v8.py.alpha5-3-1.*.bak 2>/dev/null | head -1 || true)"

if [ -z "$LAST" ]; then
  echo "No Alpha 5.3.1 backup found."
  exit 1
fi

cp "$LAST" backend/operator_v8.py

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback Alpha 5.3.1 done."
