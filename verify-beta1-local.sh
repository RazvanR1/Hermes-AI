#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Import check"
PYTHONPATH=/home/hermes/Hermes/backend python3 - <<'PY'
from beta1_execution_pipeline_v8 import execute_approved_steps
from approval_engine_v8 import approve_step, list_pending_approvals
print("imports ok")
PY

echo "[2/5] Restart API"
systemctl restart hermes-api
sleep 2
curl -fsS http://127.0.0.1:8088/operator/v8/health
echo

echo "[3/5] Create SAFE status mission"
MID="$(curl -fsS -X POST http://127.0.0.1:8088/operator/v8/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"status VM 111","source":"beta1-verify","user":"mircea"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["summary"]["mission_id"])')"
echo "SAFE mission: $MID"

echo "[4/5] Run safe step through mission API"
curl -fsS -X POST "http://127.0.0.1:8088/mission/v8/$MID/run-safe" | python3 -m json.tool

echo "[5/5] Create CONFIRM mission only - DO NOT approve automatically"
curl -fsS -X POST http://127.0.0.1:8088/operator/v8/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"repornește VM 111","source":"beta1-verify","user":"mircea"}' | python3 -m json.tool

echo
echo "Pending approvals:"
curl -fsS http://127.0.0.1:8088/approval/v8/pending | python3 -m json.tool

echo
echo "OK. Atenție: dacă aprobi misiunea de reboot, VM 111 chiar se repornește."
