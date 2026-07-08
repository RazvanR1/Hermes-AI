#!/usr/bin/env bash
set -euo pipefail

echo "[verify] execution health"
curl -fsS http://127.0.0.1:8088/execution/v8/health
echo

echo "[verify] action registry"
curl -fsS http://127.0.0.1:8088/execution/v8/actions | python3 -m json.tool
echo

echo "[verify] linux.status"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d '{"action":"linux.status","params":{}}' | python3 -m json.tool
echo

echo "[verify] apt upgrade preview"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d '{"action":"linux.apt_upgrade_preview","params":{}}' | python3 -m json.tool
echo

echo "[verify] OK"
