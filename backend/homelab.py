#!/usr/bin/env python3
import sys
import json

sys.path.insert(0, "/home/hermes/homelab-plugin")

from proxmox import client as proxmox

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  homelab proxmox status")
        print("  homelab proxmox storage")
        print("  homelab proxmox start <vmid|alias>")
        print("  homelab proxmox stop <vmid|alias>")
        print("  homelab proxmox shutdown <vmid|alias>")
        print("  homelab proxmox restart <vmid|alias>")
        print("  homelab proxmox snapshot <vmid|alias> [name]")
        sys.exit(1)

    module = sys.argv[1]
    command = sys.argv[2]

    if module != "proxmox":
        raise SystemExit(f"Unknown module: {module}")

    if command == "status":
        result = proxmox.status()
    elif command == "storage":
        result = proxmox.storage()
    elif command in ["start", "stop", "shutdown", "restart"]:
        if len(sys.argv) < 4:
            raise SystemExit("Missing target")
        result = proxmox.power(command, sys.argv[3])
    elif command == "snapshot":
        if len(sys.argv) < 4:
            raise SystemExit("Missing target")
        snapname = sys.argv[4] if len(sys.argv) >= 5 else None
        result = proxmox.snapshot(sys.argv[3], snapname)
    else:
        raise SystemExit(f"Unknown Proxmox command: {command}")

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
