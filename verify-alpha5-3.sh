#!/usr/bin/env bash
set -euo pipefail

echo "[verify] operator health"
curl -fsS http://127.0.0.1:8088/operator/v8/health | python3 -m json.tool

echo "[verify] chat status VM 111"
curl -fsS -X POST http://127.0.0.1:8088/operator/v8/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"status VM 111","source":"verify","user":"mircea"}' | python3 -m json.tool

echo "[verify] chat reboot VM 111 should create CONFIRM mission"
curl -fsS -X POST http://127.0.0.1:8088/operator/v8/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"repornește VM 111","source":"verify","user":"mircea"}' | python3 -m json.tool

echo "[verify] pending approvals"
curl -fsS http://127.0.0.1:8088/approval/v8/pending | python3 -m json.tool

echo "[verify] OK"
