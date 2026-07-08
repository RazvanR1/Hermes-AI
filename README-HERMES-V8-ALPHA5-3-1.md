# Hermes v8 Alpha 5.3.1 - Operator Fix

Fix pentru Operator Chat:

## Fixed

- `repornește VM 111` era interpretat greșit ca `proxmox.vm.start`.
- Misiunile CONFIRM create din chat nu apăreau în `/approval/v8/pending`.

## Behavior

- `status VM 111` -> `proxmox.vm.status` SAFE
- `repornește VM 111` -> `proxmox.vm.reboot` CONFIRM
- misiunile CONFIRM primesc status `waiting_confirmation`
