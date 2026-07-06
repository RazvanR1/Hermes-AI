from typing import Dict, Any
from tools.dispatcher import execute

class Inventory:

    def collect(self) -> Dict[str, Any]:

        proxmox = execute("proxmox", "vms")

        if not proxmox.get("ok"):
            return proxmox

        infra = {
            "nodes": [],
            "summary": {
                "nodes": 0,
                "vms": 0,
                "lxc": 0,
                "running": 0,
                "stopped": 0,
            }
        }

        for node in proxmox["data"]:

            node_obj = {
                "name": node["node"],
                "vms": [],
                "lxc": [],
            }

            infra["summary"]["nodes"] += 1

            for vm in node["qemu"]:
                node_obj["vms"].append(vm)
                infra["summary"]["vms"] += 1

                if vm["status"] == "running":
                    infra["summary"]["running"] += 1
                else:
                    infra["summary"]["stopped"] += 1

            for ct in node["lxc"]:
                node_obj["lxc"].append(ct)
                infra["summary"]["lxc"] += 1

                if ct["status"] == "running":
                    infra["summary"]["running"] += 1
                else:
                    infra["summary"]["stopped"] += 1

            infra["nodes"].append(node_obj)

        return {
            "ok": True,
            "inventory": infra,
        }

inventory = Inventory()
