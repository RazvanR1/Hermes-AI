#!/usr/bin/env bash
set -euo pipefail

echo "[verify] events health"
curl -fsS http://127.0.0.1:8088/events/v8/health | python3 -m json.tool

echo "[verify] emit test"
curl -fsS -X POST http://127.0.0.1:8088/events/v8/emit-test \
  -H "Content-Type: application/json" \
  -d '{"event_type":"VERIFY_TEST","mission_id":"verify-mission","message":"verify event ok","data":{"ok":true}}' | python3 -m json.tool

echo "[verify] list"
curl -fsS "http://127.0.0.1:8088/events/v8/list?limit=5" | python3 -m json.tool

echo "[verify] mission events"
curl -fsS "http://127.0.0.1:8088/events/v8/mission/verify-mission" | python3 -m json.tool

echo "[verify] OK"
