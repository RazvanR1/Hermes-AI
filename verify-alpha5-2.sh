#!/usr/bin/env bash
set -euo pipefail

NODE="${NODE:-proxmox}"
TEST_VMID="${TEST_VMID:-111}"

echo "[verify] health"
curl -fsS http://127.0.0.1:8088/execution/v8/health | python3 -m json.tool

echo "[verify] actions include proxmox"
curl -fsS http://127.0.0.1:8088/execution/v8/actions | python3 -m json.tool | grep -E "proxmox\.(nodes|vm.status|lxc.status)" || true

echo "[verify] proxmox.nodes"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d '{"action":"proxmox.nodes","params":{}}' | python3 -m json.tool

echo "[verify] proxmox.vm.status for VMID ${TEST_VMID}"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"proxmox.vm.status\",\"params\":{\"node\":\"${NODE}\",\"vmid\":${TEST_VMID}}}" | python3 -m json.tool

echo "[verify] CONFIRM action direct block"
curl -fsS -X POST http://127.0.0.1:8088/execution/v8/run \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"proxmox.vm.reboot\",\"params\":{\"node\":\"${NODE}\",\"vmid\":${TEST_VMID}}}" | python3 -m json.tool

echo "[verify] OK"
