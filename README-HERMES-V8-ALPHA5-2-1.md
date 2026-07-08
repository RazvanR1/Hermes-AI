# Hermes v8 Alpha 5.2.1 - Proxmox Client Fix

Fix pentru eroarea:

`ProxmoxClient unavailable`

Pluginul Proxmox folosește acum un client intern direct, bazat pe variabilele din `/etc/default/hermes`.

Variabile acceptate:

- `PROXMOX_URL`
- `PROXMOX_API_URL`
- `PVE_URL`
- `PROXMOX_TOKEN_ID`
- `PVE_TOKEN_ID`
- `PROXMOX_TOKEN_SECRET`
- `PVE_TOKEN_SECRET`
- `PROXMOX_VERIFY_SSL`

Exemplu:

```bash
PROXMOX_URL=https://192.168.1.140:8006
PROXMOX_TOKEN_ID=root@pam!hermes
PROXMOX_TOKEN_SECRET=xxxxxxxx
PROXMOX_VERIFY_SSL=false
```
