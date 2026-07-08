#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Python imports"
PYTHONPATH=/home/hermes/Hermes/backend python3 - <<'PY'
from telegram_v8 import send_telegram_message, telegram_configured, format_mission_event
from api import telegram_v8
print("configured:", telegram_configured())
print(format_mission_event({"type":"VERIFY_TEST","mission_id":"verify","message":"ok"}))
PY

echo "[2/4] Restart API"
systemctl restart hermes-api
sleep 2

echo "[3/4] Telegram health"
curl -fsS http://127.0.0.1:8088/telegram/v8/health | python3 -m json.tool

echo "[4/4] Optional send test"
if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  curl -fsS -X POST http://127.0.0.1:8088/telegram/v8/send-test \
    -H "Content-Type: application/json" \
    -d '{"text":"Hermes Telegram foundation test ✅"}' | python3 -m json.tool
else
  echo "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set, skipping real Telegram send."
fi

echo "[verify] OK"
