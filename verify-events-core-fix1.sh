#!/usr/bin/env bash
set -euo pipefail

echo "[verify] permissions"
ls -ld backend/data
ls -l backend/data/events_v8.json

echo "[verify] emit test"
curl -fsS -X POST http://127.0.0.1:8088/events/v8/emit-test \
  -H "Content-Type: application/json" \
  -d '{"event_type":"VERIFY_FIX1","mission_id":"verify-mission","message":"fix1 ok","data":{"ok":true}}' | python3 -m json.tool

echo "[verify] list"
curl -fsS "http://127.0.0.1:8088/events/v8/list?limit=5" | python3 -m json.tool

echo "[verify] OK"
