#!/usr/bin/env bash
set -euo pipefail

echo "[verify] reboot VM 111 should become proxmox.vm.reboot and waiting_confirmation"
curl -fsS -X POST http://127.0.0.1:8088/operator/v8/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"repornește VM 111","source":"verify","user":"mircea"}' | python3 -m json.tool

echo "[verify] pending approvals should include operator-proxmox-action"
curl -fsS http://127.0.0.1:8088/approval/v8/pending | python3 -m json.tool

echo "[verify] OK"
