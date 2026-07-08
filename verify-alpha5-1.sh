#!/usr/bin/env bash
set -euo pipefail

echo "[verify] sudoers"
visudo -cf /etc/sudoers.d/hermes-privrunner

echo "[verify] direct as hermes"
su - hermes -c 'sudo -n /usr/local/sbin/hermes-privrunner linux.apt_upgrade_preview | head -20'

echo "[verify] API apt update"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d '{"action":"linux.apt_update","params":{}}' | python3 -m json.tool

echo "[verify] OK"
