# Hermes v8 Alpha 5.2 - Proxmox Plugin Core

Adaugă primul plugin Proxmox pentru Execution Framework.

## Include

- Proxmox actions în Action Registry
- SAFE:
  - `proxmox.nodes`
  - `proxmox.vm.status`
  - `proxmox.lxc.status`
- CONFIRM:
  - `proxmox.vm.start`
  - `proxmox.vm.shutdown`
  - `proxmox.vm.reboot`
  - `proxmox.vm.reset`
  - `proxmox.vm.stop`
  - `proxmox.lxc.start`
  - `proxmox.lxc.shutdown`
  - `proxmox.lxc.reboot`
  - `proxmox.lxc.stop`

## Safety

Endpointul `/execution/v8/run` execută direct doar acțiuni SAFE.
Acțiunile CONFIRM sunt înregistrate, dar blocate direct până le legăm de Mission Approval.
