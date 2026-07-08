#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

LAST_ACTIONS="$(ls -1t .hermes-backups/actions_v8_linux.py.alpha5-1.*.bak 2>/dev/null | head -1 || true)"
LAST_SUDOERS="$(ls -1t .hermes-backups/sudoers.hermes-privrunner.*.bak 2>/dev/null | head -1 || true)"
LAST_RUNNER="$(ls -1t .hermes-backups/hermes-privrunner.*.bak 2>/dev/null | head -1 || true)"

if [ -n "$LAST_ACTIONS" ]; then
  cp "$LAST_ACTIONS" backend/actions_v8_linux.py
fi

if [ -n "$LAST_SUDOERS" ]; then
  cp "$LAST_SUDOERS" /etc/sudoers.d/hermes-privrunner
  chmod 0440 /etc/sudoers.d/hermes-privrunner
else
  rm -f /etc/sudoers.d/hermes-privrunner
fi

if [ -n "$LAST_RUNNER" ]; then
  cp "$LAST_RUNNER" /usr/local/sbin/hermes-privrunner
  chmod 0750 /usr/local/sbin/hermes-privrunner
else
  rm -f /usr/local/sbin/hermes-privrunner
fi

systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "Rollback Alpha 5.1 done."
