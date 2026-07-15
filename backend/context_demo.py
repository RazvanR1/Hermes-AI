from __future__ import annotations

import json
import sys

from context_engine import (
    GuestType,
    proxmox_context_provider,
)


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 context_demo.py "
            "<vmid> [vm|lxc]"
        )
        return 1

    try:
        vmid = int(sys.argv[1])
    except ValueError:
        print("VMID trebuie să fie numeric.")
        return 1

    guest_type = (
        GuestType(sys.argv[2].lower())
        if len(sys.argv) >= 3
        else None
    )

    context = proxmox_context_provider.get_guest(
        vmid,
        guest_type,
    )

    print(
        json.dumps(
            context.to_dict(),
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0 if context.exists else 2


if __name__ == "__main__":
    raise SystemExit(main())
