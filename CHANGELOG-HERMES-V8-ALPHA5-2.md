# Changelog - Hermes v8 Alpha 5.2

## Added
- backend/actions_v8_proxmox.py
- Proxmox nodes/status actions
- Proxmox VM/LXC lifecycle actions registered as CONFIRM

## Changed
- execution_v8 imports Proxmox actions
- actions_v8_runner imports Proxmox action module

## Safety
- Direct runner still allows only SAFE actions.
- Destructive/interruptive Proxmox actions require Mission Approval in a later step.
