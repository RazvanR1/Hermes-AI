#!/usr/bin/env bash
set -euo pipefail

NODE="${NODE:-proxmox}"
TEST_VMID="${TEST_VMID:-111}"

echo "[verify] proxmox.nodes"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d '{"action":"proxmox.nodes","params":{}}' | python3 -m json.tool

echo "[verify] proxmox.vm.status VMID ${TEST_VMID}"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"proxmox.vm.status\",\"params\":{\"node\":\"${NODE}\",\"vmid\":${TEST_VMID}}}" | python3 -m json.tool

echo "[verify] direct CONFIRM block"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"proxmox.vm.reboot\",\"params\":{\"node\":\"${NODE}\",\"vmid\":${TEST_VMID}}}" | python3 -m json.tool

echo "[verify] OK"
